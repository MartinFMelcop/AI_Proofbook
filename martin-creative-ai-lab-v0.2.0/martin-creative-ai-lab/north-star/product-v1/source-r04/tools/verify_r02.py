#!/usr/bin/env python3
"""Rebuild and verify R02 with strictly scoped statuses. No browser/security bypass."""
import subprocess,sys,os,json,hashlib,re
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parent.parent

def cmd(args,env=None):
 p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,env=env)
 if p.returncode:raise RuntimeError(f'{args}\n{p.stdout}\n{p.stderr}')
 return (p.stdout+p.stderr).strip()

def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

checks={}
cmd(['sh','tools/build.sh']);checks['cpp20_native_wasm32']={'status':'PASS','note':'GCC native -Werror; freestanding clang WASM; not Windows'}
out=cmd([sys.executable,'-m','unittest','discover','-s','tests','-p','test_*.py','-q'])
count=int(re.search(r'Ran (\d+) tests?',out).group(1))
if count!=101:raise RuntimeError(f'wrong python test count {count}')
checks['python_core_sqlite_art_structure']={'status':'PASS','tests':count}
for label,command in [('native_r01', [sys.executable,'tests/generate_world_trace.py']),('native_r02',[sys.executable,'tests/generate_world_trace_r02.py'])]:
 output=cmd(command);data=json.loads(output.splitlines()[-1]);checks[label]={'status':'PASS',**data}
for label,src in [('R00_WASM','tests/test_wasm.mjs'),('R01_WASM','tests/test_world_wasm.mjs'),('R02_WASM','tests/test_world_r02_wasm.mjs'),('R02_mock_canvas','tests/test_world_ui.mjs'),('camera_quarters','tests/test_camera.mjs')]:
 checks[label]={'status':'PASS',**json.loads(cmd(['node',src]).splitlines()[-1])}
cmd(['cc','-std=c17','-Wall','-Wextra','-Werror','-Icore','tests/c17_abi_r02.c','-Lartifacts','-lns_world_r02','-o','artifacts/c17_abi_r02'])
checks['C17_to_cpp20']={'status':'PASS',**json.loads(cmd(['./artifacts/c17_abi_r02'],env={**os.environ,'LD_LIBRARY_PATH':str(ROOT/'artifacts')}))}
logs=cmd(['node','tests/render_world_skia.mjs']).splitlines()
shots=[json.loads(line) for line in logs]
assert len(shots)==4 and sorted(x['angle'] for x in shots)==[0,90,180,270]
ims=[Image.open(ROOT/'artifacts'/x['file']).convert('RGB') for x in shots]
assert all(im.size==(1200,760) for im in ims)
assert all(ImageChops.difference(ims[0],im).getbbox() is not None for im in ims[1:])
checks['actual_canvas_renderer_skia']={'status':'PASS','frames':4,'angles':[0,90,180,270],'note':'CPU Skia renders actual site/world.js; NOT Chromium, NOT visual/art PASS','png_bytes':[x['bytes'] for x in shots]}
from_file=ROOT/'artifacts/R02_SQLITE_WORLD_JOURNAL.sqlite'
if not from_file.exists():cmd([sys.executable,'tools/create_r02_journal_fixture.py'])
sys.path.insert(0,str(ROOT/'tools'))
from world_r02_ledger import Ledger
l=Ledger(from_file)
try:
 entry=l.verify('fixture-r02-six-seventeen')
 assert entry['events']==116
 checks['sqlite_receipts']={'status':'PASS','events':entry['events'],'revision':entry['revision'],'role':'LAB_ONLY'}
finally:l.close()
for i in range(4):
 for j in range(4):
  p=ROOT/f'site/assets/world/hero_{i}_{j}.webp'
  with Image.open(p) as im:assert im.size==(224,224)
for i in [0,1,2,3,4,6,7,8,9]:
 with Image.open(ROOT/f'site/assets/world/material_{i}.webp') as im:assert im.size==(128,72)
checks['study_assets']={'status':'PASS','hero_frames':16,'material_tiles':9,'approval':'ART_REVIEW_PENDING'}
for filename,expected in {
 'core/world.cpp':'98ad2f408caf913410eae80d9064c6b494e0758aee295e805c6a1a56fb41ea7f',
 'core/world.h':'2738a4ed305cff0c969541cc0f051765339c74c5c94c70a664cb2ef9bd3e29d0',
 'core/product.cpp':'5893c20925dfad8ec085c68fdf3625298a024ec91ee1071f7d03294f3255684d',
 'core/product.h':'31cf30a08e8fe61e3d331d50cb4e664271a2eeb046f7882ade7fa4d606a7a824',
 'artifacts/R01_TEST_REPORT.json':'887e7176c718520fbf4f4bb6808fba96f0290444765a016b88ec30fde12f2a7f',
 'site/assets/opening_animatic.mp4':'3534f226398ea0fd297fbd0324d1747bf35ad2b8d85f4516d4478128c1b11e9c'
}.items():assert sha(filename)==expected,filename
checks['legacy_file_integrity']={'status':'PASS','checked':6,'note':'Legacy R01/R00 bytes preserved; new game client uses R02 only'}
try:
 secs=float(cmd(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1','site/assets/opening_animatic.mp4']))
 assert 17.7<=secs<=18.4
 checks['opening_duration']={'status':'PASS','seconds':secs,'note':'old animatic unchanged; NOT final artistic animation'}
except FileNotFoundError:checks['opening_duration']={'status':'NOT_RUN'}
checks.update({'real_browser':{'status':'NOT_RUN','reason':'Chromium permission restrictions in previous attempts; no bypass'},'windows_player':{'status':'NOT_RUN'},'human_art_and_beings':{'status':'PENDING_AUTHOR','observed':'Skia render shows incomplete character/world consistency and geometric NPCs'},'network_mmo':{'status':'NOT_IMPLEMENTED'},'class_kit_canon':{'status':'NOT_AUTHORIZED'},'boss_canon':{'status':'NOT_AUTHORIZED'}})
report={'schema':'mmai.product.v1.r02.validation.v1','date':'2026-11-15','scope':'LAB_FIXTURE_ONLY','product_gate':'PRODUCT_NO_GO','art_gate':'ART_REVIEW_PENDING','author_test_requested':False,'checks':checks,
 'source_digests':{p:sha(p) for p in ['core/world_r02.cpp','core/world_r02.h','site/product.wasm','site/world.js','site/classes_r02.js','tools/world_r02_ledger.py','artifacts/R02_WORLD_NATIVE_TRACE.json','artifacts/R02_SQLITE_WORLD_JOURNAL.sqlite']}}
outpath=ROOT/'artifacts/R02_TEST_REPORT.json';outpath.write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8')
print(json.dumps({'python_unittests':count,'legacy_intents':100,'r02_intents':116,'four_real_skia_frames':4,'C17':'PASS','SQLite':'PASS','PRODUCT':'PRODUCT_NO_GO','report':str(outpath.relative_to(ROOT))}))
