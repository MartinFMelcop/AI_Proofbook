# MMORPG Maker AI — North Star PRODUCT V1 R16

Status: **ENGINEERING_LAB_PASS / ART_REVIEW_PENDING / PRODUCT_NO_GO** (15 Nov 2026).

## Material change actually made

- Generated **92 new image files** `site/assets/world/r16_*.webp` from exactly the 92 existing R14 candidate assets. This is a conservative technical **pixel-level alpha-edge refinement** (blending fringe RGB with nearest painted fully opaque pixels plus removal of near-invisible alpha<=4 compression residue); **not** new creative paintings, new architectural sides or rigs. Source R14 images and eight original sheets remain byte-exact unchanged, their SHA receipts recorded.
- A dedicated `NSR16ArtLab=true` internal preview selects the physically derived images while leaving `NSR15ArtLab`/normal default OFF. It still calls the exact R15 native-owned boss observer: `boss_intent=1` permits painted preparation/telegraph frames 0 and 1; `boss_intent=2` after accepted native `Defender` action permits 2 and 3. No JavaScript combat authority added.
- Preserved the four RCT2-like camera orientations. Kept original candidate art and the previously published R15 presentation unchanged when the internal R16 flag is OFF.

## Evidence executed, not inferred

- `python3 tools/refine_r16_alpha.py` -> 92 physically stored, hash-distinct derivatives; manifest at `artifacts/R16_ALPHA_REFINEMENT_MANIFEST.json` documents source/destination SHA, dimensions, modified pixel count, retention of major alpha silhouettes. **3,033,486 source decoded RGBA pixels** affected across 92 files, including near-invisible pixels; this figure is *not* an improvement metric.
- `python3 tools/verify_r12.py` run in the R16 assembled tree: **257 Python PASS**, compiled and executed C17 ABI5, current **121 native↔WASM actions**, historical R04=121/R03=121/R02=116/R01=100 regressions, journal SQLite verified. Nothing in the C++ owner, WASM, class/quest/profession state or history was modified.
- Node tests: R07=44, R12=67, R13=26, R14=191, R15=363, R16=292: **983 PASS**; each of these suites actually executed in the R16 tree.
- Real `site/world.js` in **Skia CPU**, loading the unchanged compiled `site/product.wasm`: four native-camera captures (0,90,180,270), 12 frames of three native adjudicated boss encounters, four frames of accepted character movement, and four default-control frames = **24 actual Canvas frames**. Native boss states remained [1,1,2,2] and painted frames [0,1,2,3], with actual revisions progressing only after an accepted Defender action, and render never modifying revision/player position.
- 108 source, art and ABI-related files matched the preserved R15 baseline by SHA. Four R16 OFF screenshots exactly match the R15 fallback pixel-by-pixel.
- R15→R16 in-scene change above mean RGB L1>18 is **0.1975% to 0.1978%** across the four cameras. This is a small pixel correction, **not** a substantial aesthetic jump or proof of artistic quality.

## Reproduction without changing R06/R15 historical files

1. Assemble the previously preserved R06 and deltas R07–R15 into a *separate working copy* (or take the unchanged R15 worktree).
2. Apply this ZIP overlay: `site/r16_art.js`, `site/r16_presentation.js`, the patched `site/world.js` and `site/index.html`, then `site/assets/world/r16_*.webp`. Original 92 R14 art files stay unchanged.
3. To rebuild the derivatives from original R14 images instead of consuming stored assets, run `python3 tools/refine_r16_alpha.py` (requires Pillow, NumPy and SciPy).
4. For the consumer patch from a fresh, *unmodified* R15 copy only, run `python3 tools/patch_r16_consumer.py`; do not reapply this exact-string patch twice.
5. Set `MMAI_R15_BASELINE_PATH` to the preserved R15 worktree path and run `python3 tools/verify_r16_art_delta.py --rerun`; this reruns the native regressions and four Skia scripts instead of relying on the recorded logs. Node needs the already used `skia-canvas` package and the same C++ WASM baseline.

## Art, quality and authorship boundaries

- Pixel-level matte improvements are genuinely stored in the derived sprite bytes, but have **not** repaired painted doors, roofs and chimneys across four perspectives. No new generated painting: the image-generation attempt failed and was not repeated.
- No skeleton/mesh rig; painted 4x4 frames are study cycles, and other beings besides the guard remain at earlier experimental maturity.
- No human rights approval, class kit canon, three boss identities canon, final artistic opening, Windows/Chromium/GPU proof, persistent MMO service or PRODUCT_GO. Continue `ART_REVIEW_PENDING` and never present this as the finished RPG.
- Existing main, Makers, MER, VEA, C02, Rave Masters independently, R00–R15 and legacy gates remain untouched. PR #3 remains DRAFT; no merge.

**Decision:** this revision justifies one compact *delta of physically modified sprites and reproducible sources*, not a new 90MB+ game archive. Aesthetic quality remains blocked and future work should target true painterly cleanup and coherent authored animations, not increasing validation counts.
