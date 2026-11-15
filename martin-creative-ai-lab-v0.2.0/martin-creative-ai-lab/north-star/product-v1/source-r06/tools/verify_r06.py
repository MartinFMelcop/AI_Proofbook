#!/usr/bin/env python3
"""Single R06 validation checkpoint. Engineering PASS ≠ product or art GO."""
from pathlib import Path
import subprocess,hashlib,json,unittest,sys,re
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'artifacts'

def run(*cmd):
 p=subprocess.run(list(map(str,cmd)),cwd=ROOT,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(f'Failed {cmd}, returncode {p.returncode}\n{p.stdout[-4000:]}\n{p.stderr[-4000:]}')
 return p.stdout.strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def nodejson(script):return json.loads(run('node',script).splitlines()[-1])
run('sh','tools/build.sh')
run('cc','-std=c17','-Wall','-Wextra','-Werror','-O2','tests/c17_abi_r05.c','-Icore','-Lartifacts','-lns_world_r05','-Wl,-rpath,$ORIGIN','-o','artifacts/c17_abi_r05')
c17=json.loads(run('./artifacts/c17_abi_r05'))
assert c17.get('PASS') and c17['abi']==5
for script in ('site/world.js','site/ambience_r06.js','site/app.js','site/architecture_r05.js'):
 run('node','--check',script)
suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py',top_level_dir=str(ROOT/'tests'))
count=suite.countTestCases();run('python','-m','unittest','discover','-s','tests','-p','test_*.py','-q');assert count>=205
curr=nodejson('tests/test_world_r05_wasm.mjs');assert curr['PASS'] and curr['events']==121
hist={}
for k,script,n in [('R04','tests/test_world_r04_wasm_history.mjs',121),('R03','tests/test_world_r03_wasm_history.mjs',121),('R02','tests/test_world_r02_wasm_history.mjs',116),('R01','tests/test_world_wasm.mjs',100)]:
 a=nodejson(script);assert a['PASS'] and a['events']==n;hist[k]=a['events']
ui=nodejson('tests/test_world_r05_ui.mjs');assert ui['PASS'] and ui['orientationCycles']==4
cam=nodejson('tests/test_camera.mjs');assert cam['views']==4
from world_r05_ledger import Ledger
ledger=Ledger(ART/'R05_SQLITE_WORLD_JOURNAL.sqlite')
try:l=ledger.verify('fixture-r05-six-seventeen')
finally:ledger.close()
assert l['events']==121
try:
 Ledger(ART/'R05_SQLITE_WORLD_JOURNAL.sqlite',create=True)
 raise AssertionError('SQLite overwrite not blocked')
except FileExistsError:pass
# actual Skia in-process executes R06 world.js, not a promotional asset
views=[json.loads(t) for t in run('node','tests/render_world_skia_r06.mjs').splitlines()]
assert len(views)==4 and [r['angle'] for r in views]==[0,90,180,270]
boss=nodejson('tests/render_r06_bosses_skia.mjs')
assert boss['PASS'] and len(boss['scenes'])==3 and all(x['state_unchanged'] for x in boss['scenes'])
motion=[json.loads(t) for t in run('node','tests/render_r06_motion_skia.mjs').splitlines()]
assert len(motion)==4
compare={}
for i in range(4):
 a=np.asarray(Image.open(ART/f'R05_GAME_VIEW_{i}.png').convert('RGB'),dtype=np.int16)
 b=np.asarray(Image.open(ART/f'R06_GAME_VIEW_{i}.png').convert('RGB'),dtype=np.int16)
 assert a.shape==b.shape==(760,1200,3)
 compare[str(i)]={'percent_changed_rgb_l1_gt18':round(float((np.abs(a-b).mean(axis=2)>18).mean()*100),3),'r06_png_bytes':int((ART/f'R06_GAME_VIEW_{i}.png').stat().st_size)}
for i in range(1,4):
 a=np.asarray(Image.open(ART/'R06_MOTION_FRAME_0.png').convert('RGB'),dtype=np.int16)
 b=np.asarray(Image.open(ART/f'R06_MOTION_FRAME_{i}.png').convert('RGB'),dtype=np.int16)
 delta=float((np.abs(a-b).mean(axis=2)>10).mean()*100)
 assert delta>.10,('missing visible motion frame',i,delta)
 compare.setdefault('motion',{})[str(i)]=round(delta,3)
old=np.asarray(Image.open(ART/'R05_BOSS_2.png').convert('RGB'),dtype=np.int16)
new=np.asarray(Image.open(ART/'R06_BOSS_2.png').convert('RGB'),dtype=np.int16)
compare['boss_2_percent_changed']=round(float((np.abs(old-new).mean(axis=2)>18).mean()*100),3)
assert compare['boss_2_percent_changed']>.04
previous=json.loads((ROOT/'R05_PACKAGE_MANIFEST.json').read_text())['files']
unchanged=['core/world_r05.cpp','core/world_r05.h','site/app.js','site/assets/opening_animatic.mp4', 'site/assets/world/npc_1_0.webp','site/assets/world/r04_cottage.webp','site/assets/world/r04_forge.webp','site/assets/world/r04_apothecary.webp','site/assets/world/r04_wisp.webp','site/assets/world/r04_guardian_boss.webp']
for n in unchanged:assert sha(ROOT/n)==previous[n],n
report={
 'schema':'mmai.product.v1.r06.qa.v1','date':'2026-11-15',
 'status':{'engineering':'LAB_PASS','art':'ART_REVIEW_PENDING','product':'PRODUCT_NO_GO','facades_4_authored_painted':'NOT_PRODUCED_IMAGE_GENERATION_FAILED','new_boss_art':'DERIVED_STUDY_NOT_CANON','player_test':'NOT_REQUESTED','real_browser':'NOT_RUN','Windows':'NOT_RUN'},
 'checks':{'python_testcases':count,'c17_cpp20':c17,'current_CPP_WASM_events':curr['events'],'historic_WASM_events':hist,'ui_simulated':ui,'camera':cam,'sqlite_journal':l,'skia_game_views':views,'skia_bosses':boss['scenes'],'skia_motion_frames':motion,'derived_npc_motion_frames':48,'derived_boss_motion_frames':18,'derived_wraith_frames':16,'unchanged_R05_sources':{p:sha(ROOT/p) for p in unchanged},'visual_deltas_not_quality_scores':compare},
 'constraints':{'current_owner':'world_r05.cpp ABI5 UNCHANGED','art_assets':'original R04 structures preserved as rendered, R05 rejected geometry remains internal only','class_kits':'21 research only; 441 selection configurations, NO canon or balance','bosses':'B01 B02 proposed; B03 Rave Masters separate; NONE approved','opening':'18 sec animatic unchanged, NOT final','multiplayer':'not implemented','rights':'original generated sources and deterministic derived studies only, final rights review pending'}
}
for name in ('site/world.js','site/ambience_r06.js','site/product.wasm','docs/R06_MOTION_RECEIPTS.json','docs/R06_WRAITH_RECEIPTS.json'):
 report.setdefault('sha256',{})[name]=sha(ROOT/name)
(ART/'R06_TEST_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
print(json.dumps({'result':'LAB_PASS_PRODUCT_NO_GO','python':count,'cpp_wasm':curr['events'],'regression':hist,'skia':{'game':len(views),'bosses':len(boss['scenes']),'motion':len(motion)},'sqlite':l['events'],'diff_not_score':compare},ensure_ascii=False))
