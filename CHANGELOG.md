# Changelog

What each version of the pack changes, newest first; each version's section is its notes on
CurseForge and GitHub. Under Unreleased goes a line for each change a player will notice that the
mod list doesn't already say: a config the pack changed, why a mod came in or went out. A release
adds the mods added, updated and removed, read from the manifest (`scripts/changelog.py`).

## Unreleased

- Fieldworks moves to 0.4.0. Two neighbouring drill heads no longer draw a wall between them, and a working Harvester lights its power face (the Burner's firebox or the Electric's coil) and gives off light.
- Breaking: patches and oil fields keep a clearance of 16 blocks from those of another kind, and the rarer one keeps its place. Land generated after updating is laid out differently, so a seed's patches and oil fields change. Those already in a world stay.

## 0.6.0

- Fieldworks moves to 0.3.0. Patches now cover every mineral the -works recipes use: redstone, gold and diamond in the Overworld, and quartz, glowstone and netherite on the Nether floor, so a Nether factory has its own resources. Rare patches lie further out, with diamond beyond 1500 blocks and netherite beyond 250 Nether blocks. Coal patches are now richer than iron ones. A Harvester reaches down through air and fluids to the source below it and shows drill heads at work. The pack's config turns on all six new patches.
- Breaking: oil wells, uranium, diamond and netherite need the Electric Harvester with their recipe held. Uranium and diamond take drilling mud, and netherite takes magma slurry, crafted from a lava bucket and soul soil. A decayed oil well stays at its floor. The new patches appear only in land you haven't explored yet.

### Mods

- Updated Fieldworks: `fieldworks-0.2.9.jar` → `fieldworks-0.3.0.jar`

## 0.5.2

- Beltworks moves to 0.5.6 and Groundworks to 0.6.2. Feeders now swing an arm like Factorio's inserters, at their tier's inserter's pace, and never lose what their hand holds; they wear a new look and mark their head and tail. Items on a belt no longer flicker where they overlap.
- A stretch of belt, or any Groundworks Stretch, is refused whole on ground a claim mod protects, and the blocks it lays count as placed by you. A torch, sign, banner or head aimed at a block's side is previewed as the wall one it places.

### Mods

- Updated Beltworks: `beltworks-0.5.2.jar` → `beltworks-0.5.6.jar`
- Updated Groundworks: `groundworks-0.6.0.jar` → `groundworks-0.6.2.jar`

## 0.5.1

- Craftworks moves to 0.10.5: the craftables list no longer stutters the server, and EMI's Craftables lists every recipe the Personal Assembler can make now, in place of the Assembling tab above the item index.

### Mods

- Updated kc00l's Craftworks: `craftworks-0.10.4.jar` → `craftworks-0.10.5.jar`

## 0.5.0

Groundworks moves to 0.6.0, and Beltworks, Pipeworks, Wireworks, Craftworks and Fieldworks move with it.

- Rotate and Reverse Rotate turn a block placed against the side of another block, not only one placed on top: a Beltworks feeder or belt end, a Pipeworks outlet, a trapdoor, a hopper or a log now turns a quarter per press there. A block that hangs on a wall, such as a ladder or a wall torch, stays on its wall, and a press that wouldn't change what the preview shows says why on the action bar.
- A Beltworks slope can climb over water, lava and other fluids.
- Craftworks' craftables list keeps up in big packs, filling in as it is worked out, and Sophisticated Backpacks' backpacks and upgrades are made in the Assemblers.
- Fieldworks' Harvesters wear art of their own.

### Mods

- Updated Beltworks: `beltworks-0.5.0.jar` → `beltworks-0.5.2.jar`
- Updated Fieldworks: `fieldworks-0.2.7.jar` → `fieldworks-0.2.9.jar`
- Updated Groundworks: `groundworks-0.5.13.jar` → `groundworks-0.6.0.jar`
- Updated kc00l's Craftworks: `craftworks-0.10.2.jar` → `craftworks-0.10.4.jar`
- Updated kc00l's Pipeworks: `pipeworks-0.4.0.jar` → `pipeworks-0.4.1.jar`
- Updated Wireworks: `wireworks-0.6.4.jar` → `wireworks-0.6.5.jar`

## 0.4.2

### Mods

- Added Swivel - Better 3rd Person / Third Person Camera, Free Look & Orbit Camera (Controller Support) (`swivel-neoforge-1.2.0+mc26.1-26.1.2.jar`)

## 0.4.1

- Craftworks moves to 0.10.2, so clicking a recipe in EMI's Craftables list or a favorited recipe queues it in the Personal Assembler again, or opens the Crafting Plan naming what is missing; since 0.4.0 the click did nothing.

### Mods

- Updated kc00l's Craftworks: `craftworks-0.10.1.jar` → `craftworks-0.10.2.jar`

## 0.4.0

Voidworks and Gearworks join the pack, and Groundworks, Pipeworks, Wireworks, Craftworks and Fieldworks move to their newest releases.

- Voidworks joins the pack, the seventh FactoryWorks mod: harvest void from the world, carry it downhill between dimensions on Void Dragons, and spend it to upgrade items.
- Gearworks joins the pack, the eighth FactoryWorks mod: an FE-powered suit whose Gear Grid holds upgrades you level without a cap, and a lance that bores through rock.

Among what the others bring:

- Groundworks' Assemblies: holding a beacon, conduit, carved pumpkin or obsidian, the preview draws the whole structure it builds, a beacon's pyramid, a conduit's frame, an iron, snow or copper golem or a Nether portal's frame, and one click places all of it, paid from your inventory. `V` steps through a block's Assemblies.
- Pipeworks' pipes and tanks are iron grey, its Pump and Outlet have textures of their own, storage tanks that touch draw as one tank, and flowing water and lava stop at a pipe instead of washing it away.
- Craftworks turns more mods' crafting recipes into Assembling recipes: those keyed by an item tag, and those that build on the item they upgrade, such as a factory tier upgrade, which keep that item's data.
- Clicking a Fieldworks Gallery scene's sign builds it again from the start, so the Harvesters can be watched draining their patches again, the Showcase's Creative Pole and all.

### Mods

- Added kc00l's Gearworks (`gearworks-0.2.0.jar`)
- Added Voidworks (`voidworks-0.2.0.jar`)
- Updated Fieldworks: `fieldworks-0.2.6.jar` → `fieldworks-0.2.7.jar`
- Updated Groundworks: `groundworks-0.5.11.jar` → `groundworks-0.5.13.jar`
- Updated kc00l's Craftworks: `craftworks-0.9.1.jar` → `craftworks-0.10.1.jar`
- Updated kc00l's Pipeworks: `pipeworks-0.3.2.jar` → `pipeworks-0.4.0.jar`
- Updated Wireworks: `wireworks-0.6.3.jar` → `wireworks-0.6.4.jar`

## 0.3.0

Beltworks, Pipeworks, Wireworks and Fieldworks move to their newest releases. Among what they bring:

- A Beltworks belt climbs only where you set it to, with a new Climb key, unbound by default, that cycles up, down and level. Slopes in a world saved before this version flatten when a tile beside them changes, and must be set again.
- Each of the four ships a Gallery datapack, off by default, that builds a working scene of each of its features with `/function <mod>:gallery/build`.
- Fieldworks' gallery puts a Wireworks Creative Pole beside its Electric Harvester, which then runs for good instead of stopping when its starting charge is spent.

### Mods

- Updated Beltworks: `beltworks-0.4.3.jar` → `beltworks-0.5.0.jar`
- Updated Fieldworks: `fieldworks-0.2.4.jar` → `fieldworks-0.2.6.jar`
- Updated kc00l's Pipeworks: `pipeworks-0.3.1.jar` → `pipeworks-0.3.2.jar`
- Updated Wireworks: `wireworks-0.6.2.jar` → `wireworks-0.6.3.jar`

## 0.2.0

Every FactoryWorks mod moves to its newest release. Among what they bring:

- Wireworks' Boiler turns water into steam, and its machines wear real textures in place of stand-ins, the Steam Engine a flywheel that turns while it burns, as Craftworks' Assemblers and Refiner do.
- Craftworks' Assemblers take fluids in and out by bucket, at every tier.
- Pipeworks' pipes and tanks fill and empty from a bucket or any other fluid item.
- Fieldworks' Harvesters are crafted at a crafting table, and drilling mud brews from clay.
- The FactoryWorks items share one Works tab in the creative menu.

Each mod's changelog on its CurseForge page has the rest.

### Mods

- Updated Beltworks: `beltworks-0.4.1.jar` → `beltworks-0.4.3.jar`
- Updated Fieldworks: `fieldworks-0.2.0.jar` → `fieldworks-0.2.4.jar`
- Updated Groundworks: `groundworks-0.5.7.jar` → `groundworks-0.5.11.jar`
- Updated kc00l's Craftworks: `craftworks-0.7.0.jar` → `craftworks-0.9.1.jar`
- Updated kc00l's Pipeworks: `pipeworks-0.2.0.jar` → `pipeworks-0.3.1.jar`
- Updated Wireworks: `wireworks-0.5.0.jar` → `wireworks-0.6.2.jar`

## 0.1.0

The first version on CurseForge: the six FactoryWorks mods beside 98 others, for Minecraft 26.1.2 on
NeoForge 26.1.2.109.
