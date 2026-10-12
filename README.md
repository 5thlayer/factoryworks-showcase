# FactoryWorks Showcase

A CurseForge modpack for Minecraft 26.1.2 / NeoForge that puts every mod of the
[FactoryWorks](https://github.com/5thlayer/factoryworks) suite in one world, beside the third-party
mods chosen to play with them. It curates jars and configs and adds no content of its own
([ADR-0131](https://github.com/5thlayer/factoryworks/blob/main/docs/adr/0131-the-showcase-returns-as-a-curated-pack-with-no-content-of-its-own.md)).

A bug in one of the suite's mods goes on that mod's tracker; one in the pack itself goes
[here](https://github.com/5thlayer/factoryworks-showcase/issues).

## Working on the pack

The pack is a [packwiz](https://packwiz.infra.link) manifest. packwiz has no releases, so it is
pinned by commit:

    go install github.com/packwiz/packwiz@dfd8b68a4796

- Add a mod: `packwiz cf add <slug>`. Every jar comes from CurseForge, so the export bundles none.
- Check the manifest: `scripts/check.sh`.
- Build the zip: `packwiz cf export`.

Configs ship only as `.json`, `.toml`, `.txt`, `.cfg` or `.properties`: CurseForge warns on import
about any other file type in a modpack, so `.packwizignore` keeps the rest out.
