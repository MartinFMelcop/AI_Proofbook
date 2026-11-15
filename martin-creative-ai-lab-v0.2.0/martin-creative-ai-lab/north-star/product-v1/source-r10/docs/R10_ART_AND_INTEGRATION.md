# North Star — PRODUCT V1 / R10 · original four-view painted art candidate

**15 Nov 2026 · ART_REVIEW_PENDING / PRODUCT_NO_GO · noncanonical**

## What actually changed

The earlier R09 asset blocker is materially reduced: three original AI-generated **2×2 painted view sheets** exist in the current conversation for cottage, forge and apothecary. They contain four distinct artistically depicted orientations per structure, **not geometric/rotated/mirrored substitutions**. The 3×4 source atlas and 12 real 640×640 RGBA assets were prepared using the existing R08 import method. The source art files, generated atlas, receipts and original SHA-256 are included.

This is *candidate art*, not `AUTHOR_ART_APPROVED`: the R08 inspector finds 3/3 buildings with four physical, unique image hashes and coherent automatic anchor measurements. Its status remains `BLOCKED` for unverified `license_checked` and `scale_anchor_reviewed` flags on all three buildings, and **no software operation may change those to true**. Human artistic and rights reviews are pending. Building visual continuity is plausible but not rigorously established; door/banner/porch/chimney arrangements may change across angles and need artist corrections.

## Actual game consumer (isolated preview)

`site/world.js` adds an **opt-in diagnostic** `globalThis.NSR10ArtPreview===true` before `NSWorld.mount()`. Only in that mode does it load and display `r10_cottage_0..3`, `r10_forge_0..3`, and `r10_apothecary_0..3`, selected by the existing `corner` from the same RCT2-style 90° camera policy. The drawn scene is watermarked `R10 ART CANDIDATE · NOT APPROVED`.

In the default mode `NSR10ArtPreview` is false/undefined: normal selection still uses the existing `NSFacadeR07.resolve(...)` gate and the R04 illustrated fallback. **The candidate preview does not set, spoof or bypass `AUTHOR_ART_APPROVED`.** No new gameplay JS authority was created.

### Apply to an isolated working copy, never the historical archive

1. Extract the preserved R06 complete product ZIP into a new folder (never overwrite R06). Apply existing `source-r07/`, then `source-r08/` from the same draft PR #3.
2. Overlay this package's `site/world.js`, `site/assets/world/r10_*.webp`, and `tests/render_r10_*.mjs` into the isolated copy. Keep `site/product.wasm`, C++ owner and C17 ABI5 from R06.
3. For internal rendering only, set `NSR10ArtPreview=true` before the world mounts. Never set `NSFacadeR07Manifest.state=AUTHOR_ART_APPROVED` without an author-approved art/license adjudication.
4. Execute `node tests/render_r10_candidate_skia.mjs` and `node tests/render_r10_fallback_skia.mjs`, with Node+Skia installed, to reproduce the screenshots. Do not portray these as Windows or browser captures.

## Evidence executed in this operation

- 12 actual cutouts, all 640×640 RGBA, 12 distinct SHA-256 values; original sheets and normalized 3×4 atlas present.
- R08 perceptual/physical inspector: no suspected copied/mirrored/recolored facade pairs and no anchor mismatch; **BLOCKED** solely by unverified license and visual anchor approval. Heuristic, not originality proof.
- 4 real `site/world.js` screenshots executed with Skia CPU at 0°/90°/180°/270°, not mockups. Against R07 base, 4.7041 / 5.5599 / 4.8991 / 5.7510 percent of pixels had mean absolute RGB change greater than 18; this is a *change metric, not an artistic score*.
- R10 candidate watermark; four camera turns preserved owner revision/position. With preview disabled, 4/4 captures were pixel-identical to the historical R07 game view.
- Rebuilt C++20 native and WebAssembly, compiled/ran the external C17 consumer: PASS; Python unittest **240 PASS**; JS facade checks **44 PASS**; C++↔WASM owner **121 actions PASS**; historical R04 121, R03 121, R02 116, R01 100 PASS; SQLite journal **121-event replay PASS**.
- Frozen `core/world_r05.cpp/.h`, `site/product.wasm`, `camera4.js`, `facades_r07.js`, and the original opening compared byte-for-byte against the preserved R08 work copy: exact matches.

## Remaining gates

- **AUTHOR_ART_APPROVED not granted.** Check each facade manually under all four views for plausible continuous topology: roof direction, chimney, door/entry, signage, colors and footprint. Get written acknowledgment of the visual design and provenance/license.
- The current game stage remains a limited laboratory 24×20 scene. Higher quality backgrounds, final being rigs and animations, bosses and opening, full 21 class kits, Windows user build and actual MMORPG are not authorized or proved.
- Product status **PRODUCT_NO_GO**. No new full-game ZIP and no player test request.

## Immutable sources

R00–R06, Makers, MER, VEA, C02/F5/F6, independent Rave Masters canon, C/E/B/D owner gates and `main` must remain untouched. Publish only this art candidate and incremental source under the existing PR #3 branch.
