#!/usr/bin/env python3
"""R07 additive QA — no artistic acceptance, no new gameplay authority."""
from pathlib import Path
import subprocess,hashlib,json,unittest,sys
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[1];A=R/'artifacts'
def run(*argv):
 p=subprocess.run(list(map(str,argv)),cwd=R,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(f'{argv}: {p.returncode}\n{p.stdout[-1500:]}\n{p.stderr[-1500:]}')
 return p.stdout.strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Verify the complete archive owner and all previous source modules still run.
run('sh','tools/build.sh')
run('cc','-std=c17','-Wall','-Wextra','-Werror','-O2','tests/c17_abi_r05.c','-Icore','-Lartifacts','-lns_world_r05','-Wl,-rpath,$ORIGIN','-o','artifacts/c17_abi_r05')
c17=json.loads(run('./artifacts/c17_abi_r05'))
suite=unittest.defaultTestLoader.discover(str(R/'tests'),pattern='test_*.py',top_level_dir=str(R/'tests'))
count=suite.countTestCases();run('python','-m','unittest','discover','-s','tests','-p','test_*.py','-q')
for f in ['site/world.js','site/index.html','site/atmosphere_r07.js','site/facades_r07.js']:
 if f.endswith('.js'):run('node','--check',f)
face=json.loads(run('node','tests/test_r07_facade_contract.mjs').splitlines()[-1]);assert face['PASS']
from validate_facades_r07 import validate
facade=validate(json.loads((R/'docs/R07_FACADE_ART_GATE.json').read_text()),R/'site/assets/world')
assert facade['status']=='BLOCKED' and not facade['eligible_for_art_approval']
wasm=json.loads(run('node','tests/test_world_r05_wasm.mjs').splitlines()[-1]);assert wasm['PASS'] and wasm['events']==121
hist={}
for k,n,path in [('R04',121,'tests/test_world_r04_wasm_history.mjs'),('R03',121,'tests/test_world_r03_wasm_history.mjs'),('R02',116,'tests/test_world_r02_wasm_history.mjs'),('R01',100,'tests/test_world_wasm.mjs')]:
 v=json.loads(run('node',path).splitlines()[-1]);assert v['PASS'] and v['events']==n;hist[k]=n
ui=json.loads(run('node','tests/test_world_r05_ui.mjs').splitlines()[-1]);assert ui['PASS'] and ui['orientationCycles']==4
from world_r05_ledger import Ledger
ledger=Ledger(A/'R05_SQLITE_WORLD_JOURNAL.sqlite')
try:sql=ledger.verify('fixture-r05-six-seventeen')
finally:ledger.close()
assert sql['events']==121
views=[json.loads(x) for x in run('node','tests/render_world_skia_r07.mjs').splitlines()];assert [v['angle'] for v in views]==[0,90,180,270]
boss=json.loads(run('node','tests/render_r07_bosses_skia.mjs').splitlines()[-1]);assert boss['PASS'] and len(boss['scenes'])==3
motion=[json.loads(x) for x in run('node','tests/render_r07_motion_skia.mjs').splitlines()];assert len(motion)==4
change=[]
for i in range(4):
 old=np.asarray(Image.open(A/f'R06_GAME_VIEW_{i}.png').convert('RGB'),dtype=np.int16)
 new=np.asarray(Image.open(A/f'R07_GAME_VIEW_{i}.png').convert('RGB'),dtype=np.int16)
 assert old.shape==new.shape==(760,1200,3)
 change.append(round(float((np.abs(old-new).mean(axis=2)>18).mean()*100),4))
unchanged=['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/assets/world/r04_cottage.webp','site/assets/world/r04_forge.webp','site/assets/world/r04_apothecary.webp','site/assets/opening_animatic.mp4']
legacy=json.loads((R/'R06_PACKAGE_MANIFEST.json').read_text())['files']
assert all(sha(R/k)==legacy[k] for k in unchanged)
report={
 'schema':'mmai.product.v1.r07.qa.v1','date':'2026-11-15',
 'status':{'engineering':'LAB_PASS','art':'ART_BLOCKED_GENERATION_FAILED','product':'PRODUCT_NO_GO','facades_four_original_paintings':'NOT_CREATED','author_test':'NOT_REQUESTED','windows':'NOT_RUN','real_browser':'NOT_RUN'},
 'tests':{'python_unittest':count,'js_facade_assertions':face['checks'],'c17':c17,'wasm_current':wasm['events'],'wasm_regressions':hist,'ui_simulated':ui,'sqlite_journal':sql,'skia_real_world_views':views,'skia_real_boss_views':boss['scenes'],'skia_real_motion_views':motion,'physical_facade_gate':facade},
 'visual':{'r06_to_r07_pixel_change_percent_by_camera_L1_RGB_gt18':change,'interpretation':'Observer-only lighting/grounding: minimal scene change, no art quality increase established','R05_geometry_study':'STILL_ART_REJECTED','R04_rich_billboard':'KEPT_AS_DEFAULT','new_painted_four_facades':'FAILED_NOT_GENERATED'},
 'unchanged_sha256':{k:sha(R/k) for k in unchanged},
 'source_sha256':{k:sha(R/k) for k in ['site/world.js','site/index.html','site/atmosphere_r07.js','site/facades_r07.js','tools/validate_facades_r07.py','docs/R07_FACADE_ART_GATE.json']},
 'gates':{'classes':'21_HISTORICAL_RESEARCH_KITS_ONLY','bosses':'B01_B02_PROPOSED_B03_RAVE_MASTERS_HISTORIC_NOT_NORTH_STAR_CANON','beings':'R06_DERIVED_ANIMATIONS_ONLY','opening':'18S_ANIMATIC_NOT_FINAL','multiplayer':'NOT_IMPLEMENTED'}
}
(A/'R07_TEST_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
print(json.dumps({'status':'LAB_PASS_PRODUCT_NO_GO','python':count,'facadeJS':face['checks'],'WASM':wasm['events'],'regressions':hist,'Skia':{'world':len(views),'boss':len(boss['scenes']),'motion':len(motion)},'pixel_change':change,'painted_facades':facade['status']}))
