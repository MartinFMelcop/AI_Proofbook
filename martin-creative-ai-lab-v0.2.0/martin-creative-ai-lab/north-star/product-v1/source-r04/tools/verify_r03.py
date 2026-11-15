#!/usr/bin/env python3
"""Rebuild, execute and record R03 laboratory gates; never claim RPG/author ART_PASS."""
import hashlib,json,subprocess,sys,os,re
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1]
R02=Path('/mnt/data/MMAI_PRODUCT_V1_R02_WORK') # optional local audit source

def cmd(a,env=None):
 p=subprocess.run(a,cwd=ROOT,capture_output=True,text=True,env=env)
 if p.returncode:raise RuntimeError('COMMAND FAILED '+repr(a)+'\n'+p.stdout+'\n'+p.stderr)
 return (p.stdout+p.stderr).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks={}
cmd(['sh','tools/build.sh'])
checks['native_cpp20_c17_wasm32']={'status':'PASS','note':'Linux .so; clang freestanding WASM32; no Windows claim'}
out=cmd([sys.executable,'-m','unittest','discover','-s','tests','-p','test_*.py','-q'])
count=int(re.search(r'Ran (\d+) tests?',out).group(1))
if count<132:raise RuntimeError('python regression count decreased '+str(count))
checks['python_regressions_sqlite_class_negative']={'status':'PASS','tests':count,'note':'includes R00/R01/R02 and R03 tests'}
trace=json.loads((ROOT/'artifacts/R03_WORLD_NATIVE_TRACE.json').read_text())
if not trace['events'] or trace['events'][-1]['state']['quest']!=7:raise AssertionError('native trace missing finale')
if len(trace['events'])!=121:raise AssertionError('native trace expected 121')
checks['native_cpp20_trace']={'status':'PASS','accepted_events':len(trace['events']),'original_native':True}
for label,js in [('r03_native_wasm_parity','tests/test_world_r03_wasm.mjs'),('r02_historical_wasm','tests/test_world_r02_wasm_history.mjs'),('r01_historical_wasm','tests/test_world_wasm.mjs'),('camera_quarter_turns','tests/test_camera.mjs'),('ui_mock_canvas','tests/test_world_ui.mjs')]:
 response=json.loads(cmd(['node',js]).splitlines()[-1])
 if response.get('PASS') is False or response.get('state')=='FAIL':raise AssertionError(response)
 checks[label]={'status':'PASS',**response}
cmd(['cc','-std=c17','-Wall','-Wextra','-Werror','-Icore','tests/c17_abi_r03.c','-Lartifacts','-lns_world_r03','-o','artifacts/c17_abi_r03'])
res=json.loads(cmd(['./artifacts/c17_abi_r03'],env={**os.environ,'LD_LIBRARY_PATH':str(ROOT/'artifacts')}))
checks['C17_consumer']={'status':'PASS',**res}
shots=[json.loads(x) for x in cmd(['node','tests/render_world_skia_r03.mjs']).splitlines()]
if sorted(x['angle'] for x in shots)!=[0,90,180,270]:raise AssertionError('missing quarter view')
frames=[Image.open(ROOT/'artifacts'/shot['file']).convert('RGB') for shot in shots]
if not all(x.size==(1200,760) for x in frames):raise AssertionError('bad Skia dimensions')
if not all(ImageChops.difference(frames[0],f).getbbox() for f in frames[1:]):raise AssertionError('identical views')
checks['real_renderer_Skia_CPU']={'status':'PASS','views':4,'size':[1200,760],'images':[x['file'] for x in shots], 'limitation':'Actual site/world.js on Skia Canvas, not Chromium/Windows/visual acceptance'}
# Inspect decode/shape/source, not aesthetic quality.
for n in range(1,5):
 for c in range(4):
  im=Image.open(ROOT/f'site/assets/world/npc_{n}_{c}.webp').convert('RGBA')
  assert im.size==(192,224)
  assert im.getchannel('A').getextrema()[1]>=240
for k in [0,1,2,3,4,6,7,8,9]:
 for v in range(5):assert Image.open(ROOT/f'site/assets/world/material_{k}_{v}.webp').size==(128,72)
checks['sprite_and_material_source_decode']={'status':'PASS','npc_sprites':16,'ground_material_variants':45,'approval':'ART_REVIEW_PENDING'}
from_file=ROOT/'artifacts/R03_SQLITE_WORLD_JOURNAL.sqlite'
sys.path.insert(0,str(ROOT/'tools'))
from world_r03_ledger import Ledger
ledger=Ledger(from_file)
try:
 record=ledger.verify('fixture-r03-six-seventeen');assert record['events']==121
 checks['SQLite_journal_replay']={'status':'PASS','events':record['events'],'revision':record['revision'],'status_of_authority':'LAB_ONLY'}
finally:ledger.close()
# Assert the prior R02 sources/media *in this copy* remained byte-for-byte unchanged.
history=['core/world.cpp','core/world.h','core/world_r02.cpp','core/world_r02.h','core/product.cpp','core/product.h',
 'artifacts/R01_TEST_REPORT.json','artifacts/R02_TEST_REPORT.json',
 'site/assets/opening_animatic.mp4','art_sources/hero_r02_walk_sheet.png']
if R02.exists():
 for file in history:
  if sha(ROOT/file)!=sha(R02/file):raise AssertionError('historical source was modified '+file)
 checks['preserved_R02_historical_source_hashes']={'status':'PASS','files':len(history)}
else:checks['preserved_R02_historical_source_hashes']={'status':'NOT_RUN','reason':'R02 local reference not available'}
seconds=float(cmd(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1','site/assets/opening_animatic.mp4']))
assert 17.7<=seconds<=18.4
checks['original_opening_animatic_duration']={'status':'PASS','seconds':round(seconds,3),'art_grade':'ANIMATIC_NOT_FINAL'}
checks['real_browser_Windows']={'status':'NOT_RUN','no_admin_bypass':True}
checks['native_Windows_standard_user']={'status':'NOT_RUN'}
checks['3_boss_canonical_status']={'status':'NOT_CANON','detail':'B01/B02 proposed, B03 Rave Masters independent source'}
checks['21_full_class_kits']={'status':'NOT_CANON','detail':'21 research signature+utility+passive combinations, no owner ACK or balance'}
checks['NPC_quality']={'status':'ART_REVIEW_PENDING','detail':'Four illustrated NPC facing poses but no complete gait, reactive speech animation or visual human acceptance'}
checks['game_product']={'status':'PRODUCT_NO_GO'}
manifest={'schema':'mmai.product.v1.r03.qa.v1','date':'2026-11-15','work_type':'single_composed_product_v1','product_gate':'PRODUCT_NO_GO','art_gate':'ART_REVIEW_PENDING','owner_authority':'world_r03.cpp C++20 ABI3 only','author_test_requested':False,
 'source_provenance':['MMAI C02 baseline','Combat Philosophies R01–R21','Rave Masters GDD separate historical reference'],
 'checks':checks,'sha256':{p:sha(ROOT/p) for p in ['core/world_r03.cpp','core/world_r03.h','site/product.wasm','site/world.js','site/app.js','docs/R03_CLASS_KITS_LAB.json','artifacts/R03_WORLD_NATIVE_TRACE.json','artifacts/R03_SQLITE_WORLD_JOURNAL.sqlite']}}
path=ROOT/'artifacts/R03_TEST_REPORT.json';path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
print(json.dumps({'status':'ENGINEERING_LAB_PASS','python_tests':count,'native_wasm_parity':len(trace['events']),'R02_historic_actions':116,'R01_historic_actions':100,'Skia_views':4,'NPC_sprites':16,'material_variants':45,'product':'PRODUCT_NO_GO','report':str(path.relative_to(ROOT))}))
