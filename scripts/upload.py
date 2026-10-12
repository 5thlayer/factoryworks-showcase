#!/usr/bin/env python3
# Upload the released <version> to CurseForge and to its tag's GitHub release: the zip
# scripts/release.sh exported, checked against the sha256 its tag carries, with that version's
# changelog section as its notes.
#
#   scripts/upload.py <version> [--dry-run] [--site curseforge|github]
#
# Each site goes on its own: a failure on one leaves the other, and --site retries just one. A site
# that already has the version is refused, since a published version never changes.
#
# CurseForge takes $CURSEFORGE_TOKEN, an upload API token, which is never printed. When it is
# missing, the script runs itself again through `op run --env-file=publish/upload.env`, which fills
# it in from 1Password for that run only; the token is the account's, the same the mods upload with.
# $CURSEFORGE_PROJECT_ID overrides the pack's project. GitHub goes through `gh`, and needs the tag
# pushed first. --dry-run prints what it would send and contacts nothing.
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURSEFORGE_PROJECT = "1718156"
CURSEFORGE_UPLOAD = "https://minecraft.curseforge.com"
# The upload API can't list a project's files, so the website's own listing, which needs no key, does.
CURSEFORGE_API = "https://www.curseforge.com"
REPO = "5thlayer/factoryworks-showcase"


class Refused(Exception):
    pass


class Published(Refused):
    """The site already has the version, so there is nothing to retry."""


def fail(message):
    sys.exit(f"upload: {message}")


def run(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def send(method, url, headers, body=None):
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read() or b"null")
    except urllib.error.HTTPError as error:
        raise Refused(f"{method} {url} answered {error.code}: {error.read().decode(errors='replace')[:500]}")
    except urllib.error.URLError as error:
        raise Refused(f"{method} {url} failed: {error.reason}")


def multipart(fields):
    boundary = uuid.uuid4().hex
    body = b""
    for name, filename, content_type, data in fields:
        disposition = f'form-data; name="{name}"' + (f'; filename="{filename}"' if filename else "")
        body += (f"--{boundary}\r\nContent-Disposition: {disposition}\r\n"
                 f"Content-Type: {content_type}\r\n\r\n").encode() + data + b"\r\n"
    return f"multipart/form-data; boundary={boundary}", body + f"--{boundary}--\r\n".encode()


def through_op(args):
    """Runs the script again under `op run` when the CurseForge token is missing, once."""
    env_file = ROOT / "publish/upload.env"
    if (os.environ.get("CURSEFORGE_TOKEN") or os.environ.get("UPLOAD_THROUGH_OP")
            or not env_file.is_file() or not shutil.which("op")):
        return
    os.environ["UPLOAD_THROUGH_OP"] = "1"
    sys.stdout.flush()
    os.execvp("op", ["op", "run", f"--env-file={env_file}", "--", sys.executable, __file__, *args])


class Release:
    def __init__(self, version, dry_run):
        self.version, self.dry_run = version, dry_run
        self.tag = f"v{version}"
        pack = tomllib.loads((ROOT / "pack.toml").read_text())
        self.name = f"{pack['name']} {version}"
        self.zip = ROOT / f"{pack['name']}-{version}.zip"
        message = run("git", "tag", "-l", "--format=%(contents)", self.tag).stdout
        if not message:
            fail(f"{self.tag} doesn't exist; only a version scripts/release.sh tagged is uploaded.")
        released = next((line.split()[-1] for line in message.splitlines() if line.startswith("zip sha256 ")), None)
        if not released:
            fail(f"{self.tag} names no zip sha256, so there is no zip to check against it.")
        if not self.zip.is_file():
            fail(f"{self.zip.name} is missing; a later export never matches the released zip, so it can't be rebuilt.")
        self.data = self.zip.read_bytes()
        if hashlib.sha256(self.data).hexdigest() != released:
            fail(f"{self.zip.name} isn't the zip {self.tag} released (sha256 {released}).")
        # The tag's own pack.toml, whatever HEAD has moved on to.
        tagged = tomllib.loads(run("git", "show", f"{self.tag}:pack.toml").stdout)
        self.minecraft = tagged["versions"]["minecraft"]
        self.notes = run(sys.executable, str(ROOT / "scripts/changelog.py"), "notes", version)
        if self.notes.returncode:
            fail(self.notes.stderr.strip())
        self.notes = self.notes.stdout.strip()
        self.agent = f"5thlayer/factoryworks-showcase/{version}"

    def described(self):
        return f"{self.zip.name} ({len(self.data)} bytes)"

    def curseforge(self):
        project = os.environ.get("CURSEFORGE_PROJECT_ID", CURSEFORGE_PROJECT)
        upload = os.environ.get("CURSEFORGE_UPLOAD_URL", CURSEFORGE_UPLOAD).rstrip("/")
        api = os.environ.get("CURSEFORGE_API_URL", CURSEFORGE_API).rstrip("/")
        api_headers = {"User-Agent": self.agent, "Accept": "application/json"}
        files = f"{api}/api/v1/mods/{project}/files"
        # Every upload is a release: CurseForge's app only offers a pack that has one.
        metadata = {"changelog": self.notes, "changelogType": "markdown",
                    "displayName": self.name, "releaseType": "release"}
        if self.dry_run:
            print(f"GET {files}")
            print(f"GET {upload}/api/game/version-types and {upload}/api/game/versions, "
                  f"for the ids of Minecraft {self.minecraft} and NeoForge")
            print(f"POST {upload}/api/projects/{project}/upload-file")
            print(f"  metadata: {json.dumps({**metadata, 'gameVersions': f'<ids of {self.minecraft}, NeoForge>'}, indent=2)}")
            print(f"  file: {self.described()}")
            return
        if not os.environ.get("CURSEFORGE_TOKEN"):
            raise Refused("$CURSEFORGE_TOKEN is not set, and publish/upload.env didn't fill it in through op run.")
        upload_headers = {"X-Api-Token": os.environ["CURSEFORGE_TOKEN"], "User-Agent": self.agent}
        # A published version is final on CurseForge: it is never replaced.
        if {self.zip.name, self.name} & self.curseforge_files(files, api_headers):
            raise Published(f"CurseForge already has {self.version}, and a published version never changes.")
        metadata["gameVersions"] = self.curseforge_game_versions(upload, upload_headers)
        content_type, body = multipart([("metadata", None, "application/json", json.dumps(metadata).encode()),
                                        ("file", self.zip.name, "application/zip", self.data)])
        created = send("POST", f"{upload}/api/projects/{project}/upload-file",
                       {**upload_headers, "Content-Type": content_type}, body)
        print(f"Uploaded {self.zip.name} to CurseForge as {self.version} ({created.get('id')}); it shows once reviewed.")

    def curseforge_files(self, url, headers):
        """The file and display names of every file the project has, across the listing's pages."""
        names, page_index, seen = set(), 0, 0
        while True:
            page = send("GET", f"{url}?{urllib.parse.urlencode({'pageIndex': page_index, 'pageSize': 50})}", headers)
            names |= {f.get("fileName") for f in page["data"]} | {f.get("displayName") for f in page["data"]}
            seen += len(page["data"])
            if not page["data"] or seen >= page["pagination"].get("totalCount", 0):
                return names
            page_index += 1

    def curseforge_game_versions(self, upload, headers):
        """The ids of the Minecraft version and of NeoForge, the two game versions 0.1.0 carries."""
        types = send("GET", f"{upload}/api/game/version-types", headers)
        minecraft = {t["id"] for t in types if t["slug"].startswith("minecraft-")}
        loaders = {t["id"] for t in types if t["slug"] == "modloader"}
        versions = send("GET", f"{upload}/api/game/versions", headers)
        ids = []
        for name, kinds in [(self.minecraft, minecraft), ("NeoForge", loaders)]:
            found = [v["id"] for v in versions if v["name"] == name and v["gameVersionTypeID"] in kinds]
            if len(found) != 1:
                raise Refused(f"CurseForge names {len(found)} game versions {name}; it needs exactly one.")
            ids += found
        return ids

    def github(self):
        create = ["gh", "release", "create", self.tag, str(self.zip), "--repo", REPO,
                  "--verify-tag", "--title", self.name, "--notes-file", "-"]
        if self.dry_run:
            print(shlex.join(create))
            print(f"  notes: {len(self.notes)} characters from CHANGELOG.md; file: {self.described()}")
            return
        if not shutil.which("gh"):
            raise Refused("gh is not installed.")
        remote = run("git", "ls-remote", "origin", f"refs/tags/{self.tag}^{{}}").stdout.split()
        local = run("git", "rev-parse", f"{self.tag}^{{commit}}").stdout.strip()
        if not remote or remote[0] != local:
            raise Refused(f"origin doesn't have {self.tag} as tagged here; push it first: git push origin {self.tag}")
        if run("gh", "release", "view", self.tag, "--repo", REPO).returncode == 0:
            raise Published(f"GitHub already has a release for {self.tag}, and a published version never changes.")
        created = subprocess.run(create, cwd=ROOT, input=self.notes, capture_output=True, text=True)
        if created.returncode:
            raise Refused(f"gh release create failed: {created.stderr.strip()}")
        print(f"Released {self.zip.name} on GitHub: {created.stdout.strip()}")


SITES = {"curseforge": ("CurseForge", Release.curseforge), "github": ("GitHub", Release.github)}


def main(args):
    usage = "usage: scripts/upload.py <major.minor.patch> [--dry-run] [--site curseforge|github]"
    dry_run = "--dry-run" in args
    rest = [a for a in args if a != "--dry-run"]
    sites = list(SITES)
    if "--site" in rest:
        at = rest.index("--site")
        if at + 1 >= len(rest) or rest[at + 1] not in SITES:
            fail(usage)
        sites, rest = [rest[at + 1]], rest[:at] + rest[at + 2:]
    if len(rest) != 1 or not all(p.isdigit() for p in rest[0].split(".")) or rest[0].count(".") != 2:
        fail(usage)

    release = Release(rest[0], dry_run)
    if "curseforge" in sites and not dry_run:
        through_op(args)
    failed, published = [], []
    for site in sites:
        name, upload = SITES[site]
        try:
            upload(release)
        except Refused as refused:
            print(f"upload: {name}: {refused}", file=sys.stderr)
            (published if isinstance(refused, Published) else failed).append(site)
    if published and not failed:
        sys.exit(1)
    if failed:
        done = "" if len(failed) == len(sites) else "; the other site is done"
        fail(f"retry with {' and '.join('--site ' + site for site in failed)} once fixed{done}.")


if __name__ == "__main__":
    main(sys.argv[1:])
