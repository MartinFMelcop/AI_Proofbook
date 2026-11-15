# MMORPG Maker AI · North Star PRODUCT V1 — composite preproduction

**Author's direction (2026-11-15):** own engine (C++20/C17/Python+AI/SQL; Assembly only if benchmarked). No new Unity/C#-specific production. Historical Unity/C#/VEA/Workbench preserved. Four 90° camera views are a product requirement, distinct from VEA four-view asset production.

**This workstream is `INTERNAL_PREPRODUCTION / ART_REVIEW_PENDING / PRODUCT_NO_GO`**, not a deliverable ready for the author's RPG quality review. Do not distribute another technical test as a North Star game.

## One composed, versioned work package

- **Drive technical/source ZIP:** https://drive.google.com/file/d/1fsbHm8vHKnTD7nj8M-Ua8NbQWbLb8uz0/view
- 17,935,594 bytes; local SHA-256: `27a194e6e76d6bd3be44586f968919a519774313544a9388a853c3c568be10f5` (no remote byte-for-byte readback).
- **Drive master progress + gates:** https://docs.google.com/document/d/1HwKtQ3WLnCFEKMtjUN4cwYi0uRMQickM6SJHZNJkZPU/edit
- The archive contains 33 files: native C++20 core, C17 ABI header, wasm32 compilation, Python and Node tests, an original logo concept, an 18-second original motion-comic animatic and instrumental score, title/menu/creator/prologue interface, asset sources and status manifests.
- Native logic: 33 Python structure/C++ tests and Node WASM/camera suites PASS in Linux. Chromium UI `ERR_BLOCKED_BY_ADMINISTRATOR`; Windows and final game render NOT_RUN.

## Product flow / noncanonical sources

Studio splash → opening animatic → press-to-start title → main/options menu → character identity and up to two of 21 historic R01–R21 class profiles → opening adventure stages → three *mechanical fixture encounters* → epilogue.

21 profiles are a design direction, not 21 implemented class kits. Rogue A and Rogue B are separate research profiles with a shared legacy ROGUE key; their independence is unproven.

Rave Masters v0.2 (separate historical work): https://drive.google.com/file/d/1Q3LwmkiD-p2gvw65756ZLk1bkNmJc32Z/view. Its initial road/guard/dog/7-house village/Rose disappearance/forest/fairies/Guardian Tree minichefe are REFERENCES, not automatically North Star canon. It does **not** specify three North Star bosses. B01 `Vigia das Ruínas` and B02 `Sussurro do Brejo` are proposals; B03 `Árvore Guardiã` is a Rave Masters legacy source, NOT a canonized North Star boss.

## Exit gates before author's acceptance

1. Original brand and opening: author art approval, actual audiovisual animation/mix and publication rights.
2. Native rendered 2.5D world with camera orbit in 4 quarter-turns, readable occlusion/collisions and real NPC beings.
3. Real class kits for 1–2 choices, professions/skills, spatial exploration, quests and 3 authored bosses with real combat behavior and counterplay.
4. Complete persistence/authority, Windows under non-admin standard user, accessibility, reproducible tests and human review.
5. C/E/B/D owner acknowledgements and independent canon gates, preserving R51/R60/R61/INT-C01-001 OPEN, RP-R03-P03/RP-G02-A03 PENDING, C30 STOP_DOCUMENTARY_PENDING_OWNER, Arena S1 HOLD, C05-P01–P07 OPEN, F5/VEA decisions and 737 critiques.

This change is additive and reviewable. Existing baselines, Makers, MER, VEA, Unity and independent works are unchanged.


## R01 — World-owned spatial slice, no product promotion (2026-11-15)

**One composed revision of the same V1**, not a disconnected demo:
- New source ZIP (full, standalone snapshot) https://drive.google.com/file/d/19U1f3Yr7xhfResYMdrEtDAduJA6yscaV/view (22,111,513 bytes; SHA-256 local `cfce150ea5cd021c0fcd9ae30e2502f5ecec262117cbeeb86ab402338fefe553`; Google Drive size/parent readback only, remote binary hash not verified).
- R00 remains preserved at Drive ID `1fsbHm8vHKnTD7nj8M-Ua8NbQWbLb8uz0`; R01 supplements it and becomes the active laboratory source. No historical overwrite.
- World owner: `core/world.cpp`, one C++20-to-wasm32 executable rule set with a C ABI. The previous `core/product.cpp` is built separately only for legacy regression.
- Reality of play: a 24x20 grid rendered isometrically, native tile collisions, river/bridge, WASD/click movement, four actual orthographic quarter-turn projections, deterministic basic NPC routes, guard/leader/herbs/crafting, and three distinct mechanical encounters with telegraphs/guard/retreat, in one title/menu/creator/opening product flow.
- Evidence: 60 Python tests PASS; **100 native C++ intentions replayed in real WASM with matching state after each action**, 4 rotations + input observed under simulated Canvas/DOM, local hash-chained SQLite journal of 100 actions verified, 18-second H.264/AAC animatic unchanged. Browser rendering, Windows, art quality and player UX remain NOT_RUN/NOT_APPROVED.
- The 21 historical classes are selectable **but 21 class kits are not implemented**; skills are noncanonical laboratory techniques. B01/B02 are proposals; B03 is a separate Rave Masters legacy minichefe. No canonical boss, region or class power has been introduced.
- Art direction: extra 4-facing character sheet plus 6 prop sources, all derivations and source hashes in the package; 4-view object self-orientation, rigs, animations, performance and artistic acceptance are **pending**.
- Python/SQLite handles a reproducible **laboratory journal only**, not account persistence or browser save infrastructure. No multiplayer authority proven.
- Technical details in `docs/R01_SPATIAL_DELTA.md` and `artifacts/R01_TEST_REPORT.json` inside the R01 ZIP; this PR remains **DRAFT / PRODUCT_NO_GO**.

Next source-consumer work: four-facing coherent in-game architecture and animation with artistic gates; real 1–2-class kit binding; beings with personality-specific behavior; richer authored three-boss encounters; Windows standard-user build and human art/play review. No extra author-facing test ZIP until composite quality warrants it.


## R02 — Class research modes, bounded beings, materials and real Canvas render (2026-11-15)

**Same composite PRODUCT V1, new isolated revision, still `DRAFT / ART_REVIEW_PENDING / PRODUCT_NO_GO`.**

- R02 complete source package on Drive: https://drive.google.com/file/d/1I81NOh4eI83g-gYGJkGZtOyIbjzTeDVL/view, 29,080,893 bytes, 124 files. Local ZIP SHA-256 `ec71760455d19fedc78639fee42f859a33841d0bc199bc469929e2b4ef804fa8` (archive member CRC and SHA256 verified locally; remote readback confirmed size/folder only, not binary digest). Historic R00 and R01 remain unmodified.
- C++20 `core/world_r02.cpp`/C17 `world_r02.h` new **ABI 2** (old `world.cpp` ABI1 unchanged). Native `libns_world_r02.so` and new `site/product.wasm` use ONE experimental world authority; source and artifacts live in the R02 ZIP, not yet mirrored as executable source in GitHub. All 21 profiles R01–R21 can use **differentiated RESEARCH/LAB_ONLY** ability modes selected primary or secondary, including conditional costs and effects; **NOT 21 approved class kits**.
- New optional mining → smelting → tool upgrade loop with measurable attack changes, bounded C++ being behavioral modes (idle/patrol/attentive/working/concerned/alert; no true RPG AI), three distinct boss-fixture telegraphs, phase/patterns and counterplay. Two bosses proposed; the Tree belongs to a separate Rave Masters GDD historical source and is not canon North Star.
- Four 90° camera projections rendered by **actual** `site/world.js` Canvas code under Skia CPU. 16 concept pose frames and nine deterministic material tiles. Four Skia PNG artifacts in ZIP are **not browser captures**. On internal inspection the scene still has repeated grid textures and geometric NPCs: **art gate stays pending**.
- Technical evidence: **101 Python unittest PASS**, C17 executable linked to C++20 ABI2 PASS, **116 native intents** with field-by-field WASM parity incl being behavior, 100 archived R01 actions parity, 4 distinct Skia renders, SQLite 116-event verified hash-chain/replay, 6 preserved R01 source/asset SHA256 matches. Opening is unchanged 18s motion-comic, not a finished anime-quality video.
- Lab SQLite ledger is NOT authoritative online account/save. Client localStorage journal is version 3 ABI2, fails closed on incompatible R01 save (does not overwrite old key). Windows, real browser, art approval and multiplayer are NOT_RUN / NOT_APPROVED.
- Reproducibility details: `docs/R02_COMPOSED_DELTA.md`, `artifacts/R02_TEST_REPORT.json`, `docs/R02_CLASS_RESEARCH_BINDINGS.json` inside R02 ZIP.

Next gate **ART / authored gameplay quality**: player and beings consistent across 4 camera views, production animation/visual world, specialized 21 kits with author adjudication, three authored boss identities/patterns, opening and normal-user Windows build. Do not issue another fragmented user-test executable or promote any technical pass to `PRODUCT_GO`.


### Source mirror on the same draft PR

After the full R02 source ZIP was uploaded to Drive and its local integrity verified, **49 UTF-8 sources** (C/C++, Python, JavaScript, CSS, HTML, tests, documentation) were additionally committed under [source-r02](source-r02/) on this branch. Sample readback of 7 actual files matched the source bundle exactly. All large source art, animation, compiled binaries and rendered evidence remain in the single ZIP on Drive; no binary duplication or main-branch merge. The transient 228 KB JSON bridge used for this push was deleted from Drive after verification. This supersedes the earlier note saying the source was not mirrored to GitHub.


## R03 — Real renderer improvement, illustrated NPCs, two-action research kits (2026-11-15)

**One complete R03 increment, still `PRODUCT_NO_GO / ART_REVIEW_PENDING`; NOT a game release or author test.**

- **Drive R03 full source, artwork, tests and evidence:** https://drive.google.com/file/d/1gV0_gPI9P_7sQ7UWZt4lnKSAF0CYJklB/view — 37,147,998 bytes, 223 ZIP members, local SHA-256 `6f99e378ee19b2cef319e04aef4c427b48ab27d19af9699ed4ea73f7755a3ce8`, internal CRC and individual SHA-256 verified locally. Drive metadata readback matched size and parent; remote byte-for-byte hash NOT computed.
- **GitHub R03 source:** [source-r03/](source-r03/) contains **77 actual UTF-8 source/test/contract files** (C++20/ABI C17, JavaScript, Python+SQLite, UI, docs). Sample of 11 critical files had exact content readback vs temporary transport; that bridge file was deleted. Assets, binaries, video, SQLite and 4 Skia frames remain in the R03 ZIP only. R01/R02 source folders and their Drive archives preserved.
- **Gameplay owner** `core/world_r03.cpp` ABI3; new R03-only localStorage key and version4 fail closed on old saves. Signature+utility+bounded passive for 21 research profiles, including a reduced passive for the secondary class. **Not approved real 21 class kits**, no canon skill IDs, no independent Rogue A/B proven.
- **Art renderer** actual `site/world.js` executed on Skia CPU with four 1200×760 camera views. The NPC cones are replaced by 4 illustrated archetypes × 4 orientations with original-source/alpha receipts. Nine terrain materials now have 5 variants each (45 total) and less black grid; torches have light gradients. **Still below visual acceptance:** the map remains sparse, other props lack true four-sided art, NPCs lack rich animation, and bosses remain illustrated by mechanical placeholders.
- **Bounded beings and bosses:** near-only causal talk-mask and last-talk tick, no cross-session mind-reading; B01/B02/B03 have distinct laboratory attack patterns incl phase corrosive SP loss and root pressure, with both natural play and explicitly *synthetic* phase tests. B03 is still an independent Rave Masters historical miniboss reference, not North Star canon.
- **Executed verification:** 132 Python unit tests, 121 R03 C++20→WASM parity steps, R02 116 and R01 100 archived WASM steps, C17 executable, 121-event SQLite causal journal and negative checks, 4 real Skia Canvas renders, 10 historical R02 source SHA matches, 16+45 art images decoded. **Windows/browser normal user, final opening, human art, network MMO and three actual author-approved bosses NOT_RUN/NOT_APPROVED.**
- Details and source anchors: `source-r03/docs/R03_COMPOSED_DELTA.md`, `source-r03/docs/R03_VISUAL_AUDIT.md`, `source-r03/artifacts/R03_TEST_REPORT.json`.

Continue on the **same** V1 package and PR; do not open fragmented author-facing demos. Next gate is the qualitative jump: detailed architecture/vegetation, richer NPC/hero motion in all four views, boss creature art and counterplay, 21 class kits with canon owners/balance, cinematic-quality opening and standard-user Windows build. Historical blocks and independent work remain unchanged; main is untouched.
