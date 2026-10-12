# FactoryWorks Showcase

This is the hand-made modpack to showcase all my Factoryworks mods in one place.
I have added the usual performance/QOL mods along with some well known tech mods released for Minecraft 26.1.2.

Install it from [CurseForge](https://www.curseforge.com/minecraft/modpacks/factoryworks-showcase).

## Why?

Because creating mods is fun but seeing them integrating in a real pack is even more fun!

A bug in one of the suite's mods goes on that mod's tracker; one in the pack itself goes
[here](https://github.com/5thlayer/factoryworks-showcase/issues).

## Working on the pack

The pack is a [packwiz](https://packwiz.infra.link) manifest. packwiz has no releases, so
`mise.toml` pins it by commit, with the Go that builds it:

    mise install

- Add a mod: `packwiz cf add <slug>`. Every jar comes from CurseForge, so the export bundles none.
- Check the manifest: `scripts/check.sh`.
- Build the zip: `packwiz cf export`.

Configs ship only as `.json`, `.toml`, `.txt`, `.cfg` or `.properties`: CurseForge warns on import
about any other file type in a modpack, so `.packwizignore` keeps the rest out.

## Releasing

A change a player will notice adds its line under `## Unreleased` in `CHANGELOG.md` as it lands;
the mods added, updated and removed are listed by the release itself. `scripts/changelog.py mods`
shows that list so far.

1. `scripts/release.sh <version>` from a clean `main`: it writes the version's changelog section,
   bumps `pack.toml`, runs the check, exports the zip, commits, and tags `v<version>` with the zip's
   sha256. It pushes and uploads nothing.
2. `git push origin HEAD v<version>`.
3. `scripts/upload.py <version>`: the zip goes to CurseForge, as a release, and to the tag's GitHub
   release, with the changelog section as notes on both. `--dry-run` shows what it would send, and
   `--site curseforge` or `--site github` retries one. The CurseForge token is the one the mods
   upload with: `publish/upload.env` names it in 1Password, and `op` asks to be unlocked.

The zip `release.sh` exports is the release: a later export never matches it byte for byte, since
packwiz writes the mods in a different order each time. So the upload checks it against the tag's
sha256, and the GitHub release keeps it.

A version that can break a world from the one before (a mod removed, a FactoryWorks mod moved a
minor version, which below 1.0 is a breaking change, or Minecraft or NeoForge moved) bumps the minor
version; anything else is the next patch.

## Store page

`publish/` holds the CurseForge page: `summary.txt`, `description.md`, and the icon and cover that
`publish/make-cover.py` draws from the mods' own covers.
