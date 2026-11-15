#!/usr/bin/env python3
"""R08 additive reproducibility. Does NOT create or distribute a game build."""
import hashlib, json, subprocess
from pathlib import Path
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1]
R07=R.parent/'MMAI_PRODUCT_V1_R07_WORK'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    p=subprocess.run(['python','tools/verify_r07.py'],cwd=R,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(f'R07 integrated verifier failed: {p.stdout[-1500:]} {p.stderr[-2000:]}')
    old=json.loads(p.stdout.strip().splitlines()[-1])
    if old['python']!=234 or old['facadeJS']!=44 or old['WASM']!=121:
        raise AssertionError(old)
    frozen=['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/world.js','site/index.html','site/facades_r07.js','site/assets/opening_animatic.mp4','site/assets/world/r04_cottage.webp','site/assets/world/r04_forge.webp','site/assets/world/r04_apothecary.webp']
    equal={name:sha(R/name)==sha(R07/name) for name in frozen}
    if not all(equal.values()):raise AssertionError('R08 changed original source/engine')
    scenes=[f'R07_GAME_VIEW_{i}.png' for i in range(4)]+[f'R07_BOSS_{i}.png' for i in [1,2,3]]
    screenshots={}
    for name in scenes:
        a=Image.open(R07/'artifacts'/name).convert('RGBA')
        b=Image.open(R/'artifacts'/name).convert('RGBA')
        screenshots[name]=ImageChops.difference(a,b).getbbox() is None
    if not all(screenshots.values()):raise AssertionError('R08 should not change gameplay render')
    report={
      'schema':'mmai.product.v1.r08.qa.v1','date':'2026-11-15',
      'status':{'product':'PRODUCT_NO_GO','art':'ART_BLOCKED_FACADES',
       'new_original_paintings':0,'requested_original_facades':12,
       'human_art_approval':'PENDING','release':'NOT_AUTHORIZED',
       'browser_windows':'NOT_RUN','source_only_delta':True},
      'source_recovery':{'original_R04_sheet':'one view per building, not a 3x4 atlas',
       'VEA_recovery_folder':'1YnCuJBiLPUIdZkozt4FC_Gi_K9JoKr3S: 17 direct children, code/interop/recovery archives; no approved 12-face atlas found among listed files; inner archives not exhaustively inspected',
       'new_art_generation':'FAILED; no retry'},
      'verification':{'python_unittest':old['python'],
       'r08_new_tests':19,'node_facade_checks':old['facadeJS'],
       'c17':'PASS_ABI5','native_cpp_wasm_parity':old['WASM'],
       'historical_wasm_regressions':old['regressions'],
       'sqlite_journal':'PASS_121_EVENTS',
       'skia_real_canvas':old['Skia'],
       'same_scene_r07_vs_r08_pixel_identical':screenshots,
       'frozen_engine_ui_art_source_sha_identical':equal,
       'negative_tests':['rotated/mirrored copy','recolor of same view','duplicate hashes','missing files','wrong SHA256','misaligned ground anchor','unverified rights','opaque images','incomplete atlas','wrong grid','overwrite refused','R04 single-side sheet cannot masquerade as atlas']},
      'art_gate':{'status':'BLOCKED','reason':'12 independent painted views absent',
       'software_gate_cannot_grant_author_art_approved':True,
       'perceptual_detection_is_heuristic_not_proof_of_originality':True},
      'delivery':{'full_archive':'NO_NEW_ZIP','baseline_drive_r06':'1vfOaM9mHEPJpqHklSsyLyUOtxdYz4OwT',
       'delta':'source-r08/ in existing PR #3','main':'UNCHANGED'}
    }
    (R/'artifacts/R08_TEST_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
    print(json.dumps({'PASS':True,'python':old['python'],'r08_new':19,'js_checks':old['facadeJS'],'wasm':old['WASM'],'screenshots_identical':len(screenshots),'art':'BLOCKED','product':'NO_GO'}))

if __name__=='__main__':main()
