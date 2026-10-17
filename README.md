# FactoryWorks Showcase

This is the hand-made modpack to showcase all my [FactoryWorks](https://github.com/5thlayer/factoryworks) mods in one place.
I have added the usual performance/QOL mods along with some well known tech mods released for Minecraft 26.1.2.

Install it from [CurseForge](https://www.curseforge.com/minecraft/modpacks/factoryworks-showcase).

## The suite

- **[Groundworks](https://github.com/5thlayer/groundworks)**: lay whole lines of blocks in one drag, previewed before you click
- **[Beltworks](https://github.com/5thlayer/beltworks)**: Factorio-style grid belts for any tech mod
- **[Pipeworks](https://github.com/5thlayer/pipeworks)**: Factorio-style fluid pipes and tanks, where every connected run is one segment holding one fluid
- **[Wireworks](https://github.com/5thlayer/wireworks)**: Factorio-style electric poles that power every machine in reach
- **[Craftworks](https://github.com/5thlayer/craftworks)**: ask for an item, and every step is planned, paid up front and crafted over time
- **[Fieldworks](https://github.com/5thlayer/fieldworks)**: ore patches, oil fields and the Harvester that works them
- **[Voidworks](https://github.com/5thlayer/voidworks)**: harvest void from the world, carry it downhill between dimensions, and spend it to upgrade items
- **[Gearworks](https://github.com/5thlayer/gearworks)**: one FE-powered suit, a grid of upgrades, and Levels without a cap

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

### Playing it locally

Import the pack into the CurseForge app once, as a profile named like the pack, "FactoryWorks Showcase",
and play it once from there so CurseForge installs its NeoForge. From then on `scripts/launch.py`
(or skillworks' quicklaunch, in this checkout) plays that profile offline, into its most recent save,
as this checkout stands:

- the configs and `kubejs/` that `index.toml` lists are copied into the profile;
- each FactoryWorks mod whose checkout sits beside this one, `../<mod>`, with a jar in `build/libs` at
  the pack's version or later, replaces the pack's jar, which is set aside in the profile's
  `.showcase-local/` and put back on the next run.

`--released` plays the pack's own jars, `--dry-run` says what it would copy, swap and run, and
`SHOWCASE_INSTANCE` names a profile elsewhere. To try a mod's change in the pack, build the mod and
launch.

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
