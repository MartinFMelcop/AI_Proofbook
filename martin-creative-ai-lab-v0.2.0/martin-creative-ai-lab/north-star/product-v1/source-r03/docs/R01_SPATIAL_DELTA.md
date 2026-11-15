# MMORPG Maker AI — North Star PRODUCT V1 — R01 SPATIAL INTEGRATION

2026-11-15 | Product V1 composed release line | `INTERNAL_PREPRODUCTION / PRODUCT_NO_GO`.

## Revision objective

Replace the previous series of story-gate buttons with a **genuine navigable isometric world** consuming **one** deterministic C++20 world state. Do not represent this increment as an author-approved game; the author requires the *whole* splash → opening → start/menu → character creation (21 profiles, up to two) → adventure/professions/skills/quests → 3 bosses with genuinely satisfactory art and beings before submitting a build for testing.

## Actual files changed/added

- `core/world.h`, `core/world.cpp`: one C17 ABI + C++20 state owner for a 24 × 20 map with tiles/collision, river and traversable bridge, NPC positions, stage-locked and proximity-checked interactables, herb collection and remedy crafting, boss start/win, announced target, defense, techniques, potion, retreat, local revision and per-session state. All gameplay mutations are inside C++.
- `site/world.js`: Canvas isometric projections of the same 24×20 map, 4 quarter-turn views preserving world coordinates, 3/4 actor sprites, scenery, follow-camera, water/embers, tile picking, client path proposal, keyboard movement, NPC presentation, boss telegraphs, HUD.
- `site/app.js`, `site/index.html`, `site/style.css`: one integrated experience. State is reconstructed by strict native WASM replay from localStorage. Old story-panel UI is not part of the current flow.
- `site/assets/world`: six authored experimental props sourced from the historic P03 asset set and four character-facing images derived from a fresh AI-generated sheet. Provenance and art approval remain separate.
- `tools/build.sh`: compile one world.cpp module to the playable `site/product.wasm`. Build the old `product.cpp` separately under `artifacts/product_legacy.wasm` and `libns_product.so` **for regression only**, preventing two gameplay authorities inside the client.
- `tools/spatial_journal_sqlite.py`: a separate Python + SQLite offline fixture journal. 100 accepted C++ actions are hash-chained and verified. The game UI does **not** use SQLite as its save backend; its localStorage is a replay input, not account security.

## Native test and runtime evidence

- Linux: g++ 14.2.0 C++20 compile with -Wall -Wextra -Werror, and clang 17 wasm32 compile PASSED.
- Python `unittest`: 60 passing cases, including historic C++ product regressions, 21 profiles/420 pair selections, spatial collision, quest proximity/order, resource handling, boss telegraph/defense/retreat, recovery, two-session isolation, simulated-Canvas structural checks and SQLite tamper detection.
- Native differential oracle: 100 ordered accepted world intents to three victories. WASM replay matched the native C++ world state **field-for-field after every intent**. Native final state: quest=7, defeats=3, health=21, revision=100.
- Canvas/DOM simulation under Node + actual WebAssembly: 670 draw calls observed, 4 × 90° camera turns leaving native state unchanged, key-driven movement accepted and remote interaction denied. **NOT** a browser render/quality PASS.
- SQLite laboratory: 100-event journal, integrity_check=ok, SHA256 chain, overwrite refusal, corruption detection, no Maker/MER mutations.

## Unclosed gates

- `ART_REVIEW_PENDING`: in-game image/animation consistency and beings behavior not author-approved; AI-generated assets cannot certify gameplay readability or 4-view consistency. Real browser Chromium still blocked with `ERR_BLOCKED_BY_ADMINISTRATOR` in this executor.
- `OPENING_FINAL_PENDING`: an 18-second original animatic exists, but not a complete polished animated anime opening.
- `CLASS_KITS_PENDING`: 21 historical research profiles are selectable; specialized abilities/dual builds are **not** implemented or canonized. Only generic experimental attack/guard/observe/technique actions exist.
- `BOSS_ART_AND_AI_PENDING`: three spatial encounters have native telegraphs and outcomes but no authored high-quality animation or approved pattern diversity; B01 and B02 proposed, B03 a separate Rave Masters legacy reference, none canonized for North Star.
- `PROFESSIONS_NOT_CANON`: herb gathering/crafting is mechanically stateful, but names, recipes and progression are fixture-only.
- `WINDOWS_NOT_RUN`: no Windows native build; HTML requires trusted HTTP hosting for WebAssembly; no installer, multiplayer, accounts or Steam.
- `AUTHOR_ACK_PENDING`: all original author/owner gates and VEA rights unchanged. Do not merge the draft PR as a release.

## References and preservation

C02 baseline `103SZI0xfvsaJxb15FXpsJs7BpltzQCmfkP-UUCsqVas`, C02 master `1-VSJGFCjpv2jKHG_v1JsubtAKhVL_uSDzHxhTHosZws`, F5 `1O3CFRjHQBZV84DDZQa5gsXsnrl3aBJkslf6T5hzQ0LY`, F6 `1EhTn82WnDNI2QTKnY2XVNYWISc2laQp_B6Ny9AeLmYM`, Combat Philosophies `1hd8QM4x5aKP3gh6LnaedpbauHzMpFFZJM47N0-kBKY8`, separate Rave Masters GDD `1Q3LwmkiD-p2gvw65756ZLk1bkNmJc32Z`. Author direction C (own engine) and NS-CAM-4VIEW-001 are additive. Historic Unity/C#/Blender, R51/R60/R61/INT-C01-001, RP-R03-P03/RP-G02-A03, C30, Arena S1, VEA and 737 critiques retained unchanged.
