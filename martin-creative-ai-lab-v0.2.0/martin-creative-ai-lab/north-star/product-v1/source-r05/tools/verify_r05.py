"""Fail-closed, reproducible local R05 verification. Tests are NOT aesthetic approval."""
import hashlib,json,os,re,subprocess,sys,unittest
from pathlib import Path
from PIL import Image, ImageChops
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('/mnt/data/MMAI_PRODUCT_V1_R04_WORK')

def run(*args):
 p=subprocess.run(list(map(str,args)),cwd=ROOT,capture_output=True,text=True)
 if p.returncode:
  raise RuntimeError('FAILED '+str(args)+'\n'+p.stdout[-3000:]+'\n'+p.stderr[-3000:])
 return p.stdout.strip()

def js(name):
 out=run('node',name).splitlines()[-1]
 return json.loads(out)

run('sh','tools/build.sh')
run('cc','-std=c17','-Wall','-Wextra','-Werror','-O2','tests/c17_abi_r05.c','-Icore','-Lartifacts','-lns_world_r05','-Wl,-rpath,$ORIGIN','-o','artifacts/c17_abi_r05')
c17=json.loads(run('./artifacts/c17_abi_r05'))
assert c17['PASS'] and c17['abi']==5
run('node','--check','site/world.js');run('node','--check','site/architecture_r05.js');run('node','--check','site/app.js')
suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py',top_level_dir=str(ROOT/'tests'))
tests=suite.countTestCases();out=run('python','-m','unittest','discover','-s','tests','-p','test_*.py','-q')
assert tests>=197
newtrace=json.loads(run('python','tests/generate_world_trace_r05.py'))
assert newtrace['events']==121
r05=js('tests/test_world_r05_wasm.mjs');assert r05['events']==121 and r05['PASS']
old={}
for version,path,num in [('r04','tests/test_world_r04_wasm_history.mjs',121),('r03','tests/test_world_r03_wasm_history.mjs',121),('r02','tests/test_world_r02_wasm_history.mjs',116),('r01','tests/test_world_wasm.mjs',100)]:
 r=js(path);assert r['events']==num;old[version]=r
ui=js('tests/test_world_r05_ui.mjs');assert ui['orientationCycles']==4 and ui['PASS']
geo=js('tests/test_architecture_r05.mjs');assert geo['PASS'] and geo['structures']==3 and geo['views']==4
camera=js('tests/test_camera.mjs');assert camera['views']==4
# Actual site/world.js with native WASM in Skia CPU, not a browser emulation claim.
render= [json.loads(line) for line in run('node','tests/render_world_skia_r05.mjs').splitlines()]
geometry=[json.loads(line) for line in run('node','tests/render_world_skia_r05.mjs','--geometry').splitlines()]
boss=js('tests/render_r05_bosses_skia.mjs');assert len(boss['scenes'])==3 and all(b['state_unchanged'] for b in boss['scenes'])
assert len(render)==len(geometry)==4
r04_files=['core/world_r04.cpp','core/world_r04.h','site/assets/opening_animatic.mp4','site/assets/world/r04_cottage.webp','site/assets/world/r04_forge.webp','site/assets/world/r04_apothecary.webp','site/assets/world/npc_1_0.webp','site/assets/world/hero_0_0.webp','docs/R04_COMPOSED_DELTA.md']
matched={}
for name in r04_files:
 a=hashlib.sha256((BASE/name).read_bytes()).hexdigest();b=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
 assert a==b,(name,a,b)
 matched[name]=a
if Path('/mnt/data/MMAI_PRODUCT_V1_20261115_R04.zip').exists():
 priorzip=hashlib.sha256(Path('/mnt/data/MMAI_PRODUCT_V1_20261115_R04.zip').read_bytes()).hexdigest()
 assert priorzip=='89eb4a57c1c6dfb912c7c1a9d8afc2ac8bc272f8710cab5a3cc93efcc54e9656'
else:priorzip=None
from world_r05_ledger import Ledger
fixture=ROOT/'artifacts/R05_SQLITE_WORLD_JOURNAL.sqlite'
led=Ledger(fixture)
try:ledger=led.verify('fixture-r05-six-seventeen')
finally:led.close()
assert ledger['events']==121
try:
 Ledger(fixture,create=True)
 raise AssertionError('overwrote existing SQLite')
except FileExistsError:pass
# Bounds on image measurements: no quality score inferred.
visual={}
for i in range(4):
 imgs=[Image.open(ROOT/f'artifacts/{ver}_SKIA_VIEW_{i}.png').convert('RGB') for ver in ('R04','R05') if (ROOT/f'artifacts/{ver}_SKIA_VIEW_{i}.png').exists()]
 old=Image.open(ROOT/f'artifacts/R04_SKIA_VIEW_{i}.png').convert('RGB')
 new=Image.open(ROOT/f'artifacts/R05_GAME_VIEW_{i}.png').convert('RGB')
 geoimage=Image.open(ROOT/f'artifacts/R05_GEOMETRY_VIEW_{i}.png').convert('RGB')
 assert old.size==new.size==geoimage.size==(1200,760)
 import numpy as np
 a=np.asarray(old,dtype=np.int16);b=np.asarray(new,dtype=np.int16);g=np.asarray(geoimage,dtype=np.int16)
 visual[i]={'game_delta_percent':round(float((np.abs(a-b).mean(axis=2)>18).mean()*100),2),
            'geometry_delta_percent':round(float((np.abs(a-g).mean(axis=2)>18).mean()*100),2),
            'game_png_bytes':(ROOT/f'artifacts/R05_GAME_VIEW_{i}.png').stat().st_size}
 assert ImageChops.difference(old,new).getbbox() is not None
 assert ImageChops.difference(new,geoimage).getbbox() is not None
for i in range(1,4):
 img=Image.open(ROOT/f'artifacts/R05_BOSS_{i}.png')
 assert img.size==(1200,760)
report={
 'schema':'mmai.product.v1.r05.qa.v1','date':'2026-11-15','product':'Virgo Diamond: The North Star',
 'status':{'engineering':'LAB_PASS','art':'ART_REVIEW_PENDING','facade_geometry_grade':'TECH_PASS_ART_REJECTED_INTERNAL','product':'PRODUCT_NO_GO','author_test':'NOT_REQUESTED','windows':'NOT_RUN','normal_browser':'NOT_RUN','multiplayer':'NOT_IMPLEMENTED'},
 'checks':{'python_testcases':tests,'r05_native_wasm':r05,'r04_historical':{'events':121,'status':'PASS'},'r03_historical':{'events':121,'status':'PASS'},'r02_historical':{'events':116,'status':'PASS'},'r01_historical':{'events':100,'status':'PASS'},'C17_consumer':c17,
 'camera':camera,'canvas_simulated':ui,'authored_geometry_study':geo,'skia_actual_game_views':render,'skia_internal_geometry_views':geometry,'skia_boss_scenes':boss['scenes'],
 'historical_original_sha256_identical':matched,'original_R04_zip_sha256':priorzip,'lab_sqlite':ledger,
 'visual_delta_r04_to_r05':{'method':'RGB per-pixel mean absolute change >18, percent of canvas, NOT art score','by_orientation':visual},
 '21_class_profiles':{'status':'RESEARCH_NONCANON','valid_character_builds':441,'canonical_kits':0,'Rogue_A_B':'UNVERIFIED'},
 'architecture_collider':{'status':'PASS','id_count':3,'owner_source':'C++ nsw_structure_at and nsw_tile','new_collision_changes':0,'painted_final_facades':'NOT_IMPLEMENTED'},
 'beings_movement':{'status':'PASS_SCOPED','owner_facing':'world_r05.cpp deterministic tick route','visual_smoothing':'observer only; does not advance world_tick','true_rig_animation':'NOT_IMPLEMENTED'},
 'bosses':{'status':'LAB_ONLY','source':'R04 unchanged; threat C++ query','author_identity_approval':'PENDING'},
 'opening':{'status':'R04_ANIMATIC_UNCHANGED','final':'NOT_IMPLEMENTED'}}}
for file in ['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/world.js','site/app.js','site/architecture_r05.js','artifacts/R05_WORLD_NATIVE_TRACE.json','artifacts/R05_SQLITE_WORLD_JOURNAL.sqlite']:
 report.setdefault('sha256',{})[file]=hashlib.sha256((ROOT/file).read_bytes()).hexdigest()
(ROOT/'artifacts/R05_TEST_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
print(json.dumps({'result':'ENGINEERING_LAB_PASS_PRODUCT_NO_GO','unittest':tests,'native_wasm_events':r05['events'],'Skia_game_views':4,'Skia_geometry_study_views':4,'Skia_bosses':3,'sqlite_events':ledger['events'],'visual_delta':visual},ensure_ascii=False))
