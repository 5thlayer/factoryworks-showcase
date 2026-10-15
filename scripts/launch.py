#!/usr/bin/env python3
# Plays the pack as this checkout stands, in the CurseForge profile it was imported into, with the local
# builds of the FactoryWorks mods beside it: no export, no zip, no copying by hand.
#
#   scripts/launch.py [--dry-run] [--released] [save]
#
# Before each launch it brings the profile up to the checkout and the mod checkouts beside it:
#   - every file index.toml lists outside mods/ (configs, kubejs/) is copied in, so a change to the
#     pack's own files shows without an export;
#   - a FactoryWorks mod whose checkout sits beside this one, ../<mod>, with a jar in build/libs at the
#     pack's version or later, takes the place of the pack's jar. The pack's jar is set aside in
#     .showcase-local/ and put back on the next run, so --released plays the pack as CurseForge has it.
# It then starts the game the way CurseForge would, from its Install/ folder and bundled Java, offline
# as the profile's last player, or Dev, into the most recent save unless given one. Singleplayer checks
# no token. It refuses while a game of the profile is running, since it rewrites mods/.
#
# The profile is CurseForge's, named as pack.toml names the pack, under the Minecraft root CurseForge's
# settings give; SHOWCASE_INSTANCE names another.
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACK = tomllib.loads((ROOT / "pack.toml").read_text())
CURSEFORGE_SETTINGS = Path.home() / ".config/CurseForge/storage.json"
SET_ASIDE = ".showcase-local"
OS_NAME = {"darwin": "osx", "win32": "windows"}.get(sys.platform, "linux")


def fail(message):
    sys.exit(f"launch: {message}")


def instance():
    if named := os.environ.get("SHOWCASE_INSTANCE"):
        found = Path(named)
    else:
        try:
            settings = json.loads(CURSEFORGE_SETTINGS.read_text())
            root = json.loads(settings["minecraft-settings"])["minecraftRoot"]
        except (OSError, KeyError, ValueError):
            fail(f"no Minecraft root in {CURSEFORGE_SETTINGS}; set SHOWCASE_INSTANCE to the profile's folder.")
        found = Path(root) / "Instances" / PACK["name"]
    if not (found / "minecraftinstance.json").is_file():
        fail(f"no CurseForge profile at {found}: import the pack into CurseForge once, as \"{PACK['name']}\".")
    return found


def jar_mod(jar):
    """The mod id and version a jar's neoforge.mods.toml declares, or None for a jar that declares none."""
    try:
        with zipfile.ZipFile(jar) as z:
            text = z.read("META-INF/neoforge.mods.toml").decode()
    except (KeyError, zipfile.BadZipFile):
        return None
    mod = re.search(r'^\s*modId\s*=\s*"([^"]+)"', text, re.M)
    version = re.search(r'^\s*version\s*=\s*"([^"]+)"', text, re.M)
    return (mod[1], version[1]) if mod and version else None


def version_key(version):
    return tuple(int(n) for n in re.findall(r"\d+", version))


def local_build(mod):
    """The newest jar the checkout ../<mod> built, if it builds that mod."""
    libs = ROOT.parent / mod / "build" / "libs"
    jars = [j for j in libs.glob("*.jar") if not j.name.endswith("-sources.jar")] if libs.is_dir() else []
    for jar in sorted(jars, key=lambda j: j.stat().st_mtime, reverse=True):
        if (found := jar_mod(jar)) and found[0] == mod:
            return jar, found[1]
    return None


def put_back(game):
    """Undo the last run's swaps: its local jars out of mods/, the pack's jars back in."""
    aside = game / SET_ASIDE
    record = aside / "installed.json"
    if record.is_file():
        for name in json.loads(record.read_text()):
            (game / "mods" / name).unlink(missing_ok=True)
        record.unlink()
    if aside.is_dir():
        for jar in aside.glob("*.jar"):
            shutil.move(jar, game / "mods" / jar.name)


def sync(game, released, dry):
    if not dry:
        put_back(game)
    index = tomllib.loads((ROOT / "index.toml").read_text())
    copied = 0
    for entry in index["files"]:
        path = entry["file"]
        if entry.get("metafile") or path.startswith("mods/"):
            continue
        source, target = ROOT / path, game / path
        if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == entry["hash"]:
            continue
        copied += 1
        if not dry:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    print(f"pack files: {copied} copied in" if copied else "pack files: as the checkout has them", file=sys.stderr)
    if released:
        print("mods: as the pack has them (--released)", file=sys.stderr)
        return
    installed = []
    for jar in sorted((game / "mods").glob("*.jar")):
        if not (declared := jar_mod(jar)):
            continue
        mod, version = declared
        if not (local := local_build(mod)) or version_key(local[1]) < version_key(version):
            continue
        name = f"{local[0].stem}-local.jar"
        print(f"mods: {mod} {version} -> local {local[1]} ({local[0].relative_to(ROOT.parent)})", file=sys.stderr)
        if not dry:
            (game / SET_ASIDE).mkdir(exist_ok=True)
            shutil.move(jar, game / SET_ASIDE / jar.name)
            shutil.copyfile(local[0], game / "mods" / name)
            installed.append(name)
    if installed:
        (game / SET_ASIDE / "installed.json").write_text(json.dumps(installed, indent=2) + "\n")
    elif not dry:
        print("mods: no local build at the pack's version or later", file=sys.stderr)


def player(game):
    """The profile's last signed-in player, whom its saves know, or Dev under the offline UUID."""
    try:
        cached = [e for e in json.loads((game / "usercache.json").read_text()) if e["name"] != "Dev"]
    except (OSError, ValueError):
        cached = []
    if cached:
        latest = max(cached, key=lambda e: e["expiresOn"])
        return latest["name"], latest["uuid"].replace("-", "")
    digest = bytearray(hashlib.md5(b"OfflinePlayer:Dev").digest())
    digest[6] = (digest[6] & 0x0F) | 0x30
    digest[8] = (digest[8] & 0x3F) | 0x80
    return "Dev", bytes(digest).hex()


def rules_pass(entry):
    for rule in entry.get("rules") or []:
        # Feature-gated arguments (quick play, demo, a custom resolution) stay off: enabling none and
        # letting them through would hand Minecraft its own placeholders as values.
        if "features" in rule:
            return False
        matches = rule.get("os", {}).get("name") in (None, OS_NAME)
        if (rule["action"] == "allow") != matches:
            return False
    return True


def command(game, save):
    install = game.parent.parent / "Install"
    version = f"neoforge-{PACK['versions']['neoforge']}"
    try:
        nf = json.loads((install / f"versions/{version}/{version}.json").read_text())
        mc = json.loads((install / f"versions/{nf['inheritsFrom']}/{nf['inheritsFrom']}.json").read_text())
    except OSError:
        fail(f"CurseForge has not installed {version} in {install}: play the profile once from CurseForge.")
    libs = install / "libraries"
    classpath = []
    for lib in nf["libraries"] + mc["libraries"]:
        if not rules_pass(lib):
            continue
        group, artifact, ver, *classifier = lib["name"].split(":")
        jar = libs.joinpath(*group.split("."), artifact, ver,
                            f"{artifact}-{ver}{'-' + classifier[0] if classifier else ''}.jar")
        if jar.exists() and str(jar) not in classpath:
            classpath.append(str(jar))
    # NeoForge finds the Minecraft jar itself; on the classpath too, it is a second module exporting
    # net.minecraft and the module layer fails to resolve.
    classpath.append(str(install / f"versions/{version}/{version}.jar"))
    name, uuid = player(game)
    subs = {
        "library_directory": str(libs), "classpath_separator": os.pathsep, "version_name": version,
        "natives_directory": str(install / "natives"), "launcher_name": "showcase-launch",
        "launcher_version": "1", "classpath": os.pathsep.join(classpath), "auth_player_name": name,
        "version_type": "release", "game_directory": str(game), "assets_root": str(install / "assets"),
        "assets_index_name": mc["assets"], "auth_uuid": uuid, "auth_access_token": "0", "clientid": "0",
        "auth_xuid": "0", "user_type": "legacy",
    }

    def expand(args):
        out = []
        for arg in args:
            if isinstance(arg, dict):
                if rules_pass(arg):
                    out.extend(arg["value"] if isinstance(arg["value"], list) else [arg["value"]])
            else:
                out.append(arg)
        return [re.sub(r"\$\{(\w+)\}", lambda m: subs.get(m[1], m[0]), a) for a in out]

    java = install / "java" / mc["javaVersion"]["component"] / "bin" / "java"
    cmd = [str(java), "-Xmx6G", *expand(nf["arguments"]["jvm"] + mc["arguments"]["jvm"]), nf["mainClass"],
           *expand(mc["arguments"]["game"] + nf["arguments"]["game"])]
    if save:
        cmd += ["--quickPlaySingleplayer", save]
    return cmd, name


def main():
    parser = argparse.ArgumentParser(description="Play the pack as the checkout stands, with local mod builds.")
    parser.add_argument("--dry-run", action="store_true", help="say what it would copy, swap and run; change nothing")
    parser.add_argument("--released", action="store_true", help="play the pack's own mod jars, no local builds")
    parser.add_argument("save", nargs="?", help="the save to open; the most recent by default")
    args = parser.parse_args()

    game = instance()
    running = subprocess.run(["pgrep", "-f", "--", f"--gameDir {game}"], capture_output=True, text=True).stdout.split()
    if running:
        fail(f"a game of the profile is running (pid {', '.join(running)}); close it first.")
    saves = game / "saves"
    save = args.save
    if save and not (saves / save / "level.dat").is_file():
        fail(f"no save \"{save}\" in {saves}.")
    if not save:
        latest = sorted(saves.glob("*/level.dat"), key=lambda p: p.stat().st_mtime)
        save = latest[-1].parent.name if latest else None

    sync(game, args.released, args.dry_run)
    cmd, name = command(game, save)
    print(f"profile: {game}", file=sys.stderr)
    print(f"save: {save or 'none, to the menu'}; player: {name}", file=sys.stderr)
    if args.dry_run:
        print("run: " + " ".join(cmd[:2]) + " ... " + " ".join(cmd[-4:]), file=sys.stderr)
        return
    os.chdir(game)
    sys.exit(subprocess.call(cmd))


if __name__ == "__main__":
    main()
