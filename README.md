# FactoryWorks Showcase

This is the hand-made modpack to showcase all my Factoryworks mods in one place.
I have added the usual performance/QOL mods along with some well known tech mods released for Minecraft 26.1.2.

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

## Store page

`publish/` holds the CurseForge page: `summary.txt`, `description.md`, and the icon and cover that
`publish/make-cover.py` draws from the mods' own covers.
