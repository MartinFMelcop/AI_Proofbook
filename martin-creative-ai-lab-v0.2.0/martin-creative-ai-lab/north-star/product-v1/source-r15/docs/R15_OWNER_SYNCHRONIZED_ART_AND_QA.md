# North Star — PRODUCT V1 R15 | visual synchronization proof, not an author-approved game

**Status:** ENGINEERING_LAB_PASS / ART_REVIEW_PENDING / PRODUCT_NO_GO. No Windows build or product release.

## Scope and provenance

R15 modifies only the same R14 composite game's *optional* real Canvas viewer. It does not fork or modify core/world_r05.cpp, world_r05.h, site/product.wasm (ABI5), SQLite journal, four camera matrices, character/class kits, quests or the opening. No main-branch merge, Maker/MER/VEA/canon changes or boss canonization.

**Inputs**: R06 complete package Drive 1vfOaM9mHEPJpqHklSsyLyUOtxdYz4OwT; art R14 Drive 1jel3JX7tc0kHwdDTXmfyZl6Qx0y-yDn6; source deltas R07–R13 as already present on draft PR #3 branch mmai/product-v1-composite-20261115. Apply R15 source files only to a disposable copy of that assembled R14 tree. Do not overwrite historical packages. `source-r15/` on the HUB will contain these text files; this ZIP also contains screenshots generated from the real `site/world.js` Skia CPU.

## R15 material technical change

The R14 boss sheet has 4 rows of direction and 4 columns of painted action sequence. The old visual used `floor(ms/170)%4` regardless of boss state: this could show an attack before the owner had adjudicated it. R15 `NSPresentationR15` selects frames strictly after sampling native `nsw_wasm_boss_intent`, turn, phase and pattern. For `intent=1` the only visible frames are columns 0 (prepare) and 1 (telegraph). A *real accepted* C++ action (the reproduced tests use `Defend`) moves owner intent to 2; only then do columns 2 (post-adjudication impact) and 3 (recovery) render. No JS-generated damage, fictitious priority or opponent intent. Native `nsw_wasm_boss_threatens(x,y)` is the only danger truth; a readable screen-space label uses its result and cannot be hidden behind trees.

R15 measures the *existing* alpha silhouettes on all 92 R14 WebP frames to calibrate painted ground/boot anchors and building scale in the real four-angle renderer. Frames and eight original source sheets are unchanged by SHA-256. Actor sprites are selected after a native accepted movement; no client-owned position changes. R15 is enabled only when the test harness opts into `NSR15ArtLab=true`. The normal client stays fallback-identical in all four angles. Revisions and player coordinates do not change during any render call.

## Reproduction

From the assembled R14 copy with `source-r15/` overlaid at the same file paths, dependencies from R06/R14 and a clean native toolchain:

```
python3 tools/verify_r15.py
node tests/test_r15_owner_visual_phase.mjs
node tests/render_r15_fourview_skia.mjs
node tests/render_r15_boss_phase_skia.mjs
node tests/render_r15_actor_motion_skia.mjs
node tests/render_r15_fallback_skia.mjs
```

`verify_r15.py` reruns the native/C17/WASM/SQLite suite and all graphical tests by default; the optional environment flag `MMAI_R15_REUSE_SAME_TURN_PASSED_RUNS=1` was used to assemble an independently checked report after the monolithic invocation timed out, using the passed individual same-turn runs. Without the flag, all tests execute again. The monolithic timeout is **not** counted as a PASS.

## Evidence actually checked

- 257 Python unit tests PASS; 44 R07 + 67 R12 + 26 R13 + 191 R14 + 363 R15 = 691 Node checks PASS.
- C17/ABI5 executable PASS; native C++ vs WebAssembly 121 actions and historic R04=121, R03=121, R02=116, R01=100 PASS; SQLite journal replay 121 existing events PASS.
- 24 actual renderer frames: 4 four-angle village views; 4 identical default fallbacks; 4 true actor motion frames after accepted native movement; 12 boss frames across 3 accepted C++ encounters × (2 before/2 after native defend).
- Native owner intent [1,1,2,2], sprite frame [0,1,2,3] in every real boss encounter. The actual acceptance increments owner revision; drawing never does. Affected boss sprites alter 3–6.6% of pixels between neighboring stages, primarily by action pose, not a quality grade.
- R14→R15 four-angle visual change 8.3–8.9% above mean RGB-L1 threshold >18. All 4 fallback frames pixel-exact R14. Source/C++/WASM/original art + SQLite 109 SHA-256 comparisons PASS.
- The browser binary is absent; **only real source Canvas via Skia CPU** was run, not Windows, Chromium/GPU or a human gameplay acceptance session.

## Open gates / negative evidence

**Image generation failed** and was not retried. No newly painted roofs, entrances, chimneys, dark alpha fringes or new sprites were produced; the 92 existing frames receive *render-time anchor correction only*. Building four-view architectural identity, clean transparent edges, artistic quality, rights, all 21 kits and three boss identities, original opening, live MMORPG, Windows and user-facing product approval remain pending. `PRODUCT_NO_GO / ART_REVIEW_PENDING`; preserve R51/R60/R61/INT-C01-001, RP pending, C30, Arena HOLD, author owners C/E/B/D ACK gates. No merge into main.
