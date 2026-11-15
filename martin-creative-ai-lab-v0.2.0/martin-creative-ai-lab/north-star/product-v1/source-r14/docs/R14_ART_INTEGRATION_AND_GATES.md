# MMORPG Maker AI — PRODUCT V1 R14 — original art, in-game lab only

**ENGINEERING_LAB_PASS / ART_REVIEW_PENDING / PRODUCT_NO_GO.** Date: 2026-11-15. This revision is an additive overlay on R06 full gameplay with R07–R13 source/art deltas. The normal client has **not** received author-approved changes.

## Provenance and concrete changes
Eight original image-generation sheets are archived in `art_sources/r14_original_sheets/` without alteration. `tools/build_r14_art.py` crops actual quadrants (three 2×2 building sheets) and the 4×4 frames for hero, guard, B01 ruins guardian, B02 swamp wraith, and B03 guardian tree. It creates **92 distinct RGBA WebP** files: 12 architectural views, 32 character/guard poses, and 48 boss frames. Dark matte extraction uses a heuristic and the resulting 92 frames require pixel-level art cleanup and human quality/rights review. Different poses do not prove continuity or constitute skeletal rigs. B01/B02 remain proposed and B03 retains its distinct historical Rave Masters source; no canon gate is closed.

`site/r14_art.js` is a pure art lookup. `site/world.js` draws new sprites **only** if `NSR14ArtLab===true`. World coordinates, NPC state, tiles, quests, collisions, healing, classes, boss attack telegraphs and boss damage stay exclusively in `core/world_r05.cpp` / C17 ABI5 via `product.wasm`; `site/r14_art.js` never mutates world state. The default fallback remains pixel-identical in all 4 camera orientations. Art previews are labeled `R14 ORIGINAL ART LAB · NOT APPROVED`.

## Actual execution (not synthetic screenshots)
- `python3 -m unittest discover -s tests -p 'test_*.py' -q`: **257 tests PASS** (251 inherited and six R14 additions).
- `node tests/test_r14_art_contract.mjs`: **191 checks PASS**; R07=44, R12=67 and R13=26 historical Node visual assertions PASS.
- `sh tools/build.sh`, compiled and executed C17 ABI5 consumer PASS.
- `node tests/test_world_r05_wasm.mjs`: **121** accepted actions and native↔WASM parity PASS; four independent regressions R04 **121**, R03 **121**, R02 **116**, R01 **100** PASS.
- SQLite journal: `python3 tools/world_r05_ledger.py verify artifacts/R05_SQLITE_WORLD_JOURNAL.sqlite` PASS.
- Actual `site/world.js` via CPU Skia with real `site/product.wasm`: 4 R14 camera views, 6 boss frames and 4 default fallback frames; test runners assert gameplay revision and player position unchanged by painting/rotating.
- 4/4 default frames pixel-identical to R13's non-lab baseline. Pixel-delta R13→R14 for in-game scenery: 9.1124%, 9.5695%, 8.5763%, 8.5990%; bosses 22.5–26.8%. These measure **visual change, not artistic merit**.
- 6 baseline sources (C++ .cpp/.h, wasm, camera, existing stagecraft and original opening) SHA-256-identical to R13.

## Not authorized/implemented
No AUTHOR_ART_APPROVED, no approval of 21 kits, three boss identities, independent lore or owners C/E/B/D, no final opening, no final animation/rig, no Windows/Chromium/GPU standard-user execution, no online MMORPG. No main merge or Canon/MER/Makers/VEA modifications. R51/R60/R61/INT-C01-001 and all documented historical blocks remain OPEN. R14 pack is **new images and their in-game integration/evidence only, not the whole game**. The next increment should target refining alpha and four-facing world asset consistency and then articulate actual being/boss motion, while maintaining fail-closed release gates.
