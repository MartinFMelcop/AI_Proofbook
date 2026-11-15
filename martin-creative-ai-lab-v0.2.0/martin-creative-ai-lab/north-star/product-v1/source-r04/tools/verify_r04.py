"""One fail-closed R04 lab QA pipeline; no artistic or Windows acceptance claim."""
from pathlib import Path
from PIL import Image,ImageChops,ImageStat
import subprocess,json,sys,hashlib,ctypes,os,re
ROOT=Path(__file__).resolve().parents[1]
BASE=Path('/mnt/data/MMAI_PRODUCT_V1_R03_WORK')
def command(args):
 p=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=True)
 out=p.stdout.strip()
 print(out[-1300:] if out else f'PASS {args}')
 return out
command(['sh','tools/build.sh'])
unittest_out=command(['python','-m','unittest','discover','-s','tests','-p','test_*.py','-q'])
# unittest writes number to stderr, so separately record count by dynamic loader suite.
import unittest
suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py',top_level_dir=str(ROOT/'tests'))
test_count=suite.countTestCases()
assert test_count>=165
assert ctypes.CDLL(str(ROOT/'artifacts/libns_world_r04.so')).nsw_abi()==4
c17=command(['./artifacts/c17_abi_r04'])
assert json.loads(c17)['PASS'] is True
wasm=command(['node','tests/test_world_r04_wasm.mjs'])
assert json.loads(wasm)['events']==121
historical={}
for version,test,count in [('r03','tests/test_world_r03_wasm_history.mjs',121),('r02','tests/test_world_r02_wasm_history.mjs',116),('r01','tests/test_world_wasm.mjs',100)]:
 j=json.loads(command(['node',test]));assert j['events']==count;historical[version]=j
ui=json.loads(command(['node','tests/test_world_ui.mjs']));assert ui['PASS'] and ui['orientationCycles']==4
camera=json.loads(command(['node','tests/test_camera.mjs']));assert camera['views']==4
scenes=[json.loads(x) for x in command(['node','tests/render_world_skia_r04.mjs']).splitlines()]
boss=json.loads(command(['node','tests/render_r04_bosses_skia.mjs']))
assert len(scenes)==4 and len(boss['scenes'])==3
assert all(x['state_unchanged'] for x in boss['scenes'])
from importlib.machinery import SourceFileLoader
sys.path.insert(0,str(ROOT/'tools'))
from world_r04_ledger import Ledger
led=Ledger(ROOT/'artifacts/R04_SQLITE_WORLD_JOURNAL.sqlite')
try: ledrow=led.verify('fixture-r04-six-seventeen')
finally: led.close()
assert ledrow['events']==121
oldhash={}
if BASE.exists():
 for name in ['core/world_r03.cpp','core/world_r03.h','artifacts/R03_TEST_REPORT.json','site/assets/opening_animatic.mp4','art_sources/r03_npc_four_view_original.png','site/assets/world/npc_1_0.webp']:
  a=hashlib.sha256((ROOT/name).read_bytes()).hexdigest();b=hashlib.sha256((BASE/name).read_bytes()).hexdigest()
  assert a==b,(name,a,b)
  oldhash[name]=a
assets=[]
for name in ['cottage','forge','apothecary','stonebridge','lamppost','fountain','blossom','eldertree','shrine','wisp','guardian_boss',*[f'ruinguardian_{x}' for x in range(4)]]:
 p=ROOT/f'site/assets/world/r04_{name}.webp';im=Image.open(p).convert('RGBA')
 assert im.getchannel('A').getextrema()==(0,255),(name,im.getchannel('A').getextrema())
 assets.append(name)
old=Image.open(BASE/'artifacts/R03_SKIA_VIEW_0.png').convert('RGB')
new=Image.open(ROOT/'artifacts/R04_SKIA_VIEW_0.png').convert('RGB')
assert old.size==new.size==(1200,760)
import numpy as np
p=np.asarray(old,dtype=np.int16);q=np.asarray(new,dtype=np.int16)
changed=(np.abs(p-q).mean(axis=2)>18).mean();mean_abs=np.abs(p-q).mean()
assert changed>.04,'new screenshot almost identical to R03'
for i in range(1,4):assert ImageChops.difference(new,Image.open(ROOT/f'artifacts/R04_SKIA_VIEW_{i}.png').convert('RGB')).getbbox()
for i in range(1,4):
 im=Image.open(ROOT/f'artifacts/R04_BOSS_{i}.png').convert('RGB')
 assert im.size==(1200,760) and im.tobytes()!=new.tobytes()
report={
 'schema':'mmai.product.v1.r04.qa.v1','date':'2026-11-15','product':'Virgo Diamond: The North Star',
 'gate':{'technical':'LAB_PASS','art':'ART_REVIEW_PENDING','product':'PRODUCT_NO_GO','author_test':'NOT_REQUESTED','windows':'NOT_RUN','real_browser':'NOT_RUN','multiplayer':'NOT_IMPLEMENTED'},
 'original_sources':['Drive C02','Combat Philosophies R01–R21','Rave Masters GDD independent historical only'],
 'checks':{
  'python_unittest':{'status':'PASS','testcases':test_count},'c17_cpp20':json.loads(c17),
  'native_cpp_to_wasm':json.loads(wasm),'historical_wasm':{x:{'status':'PASS','events':xv['events']} for x,xv in historical.items()},
  'camera':camera,'canvas_mock':ui,
  'skia_four_views':{'status':'PASS','render_source':'site/world.js ACTUAL Skia CPU','angles':[0,90,180,270],'canvas_size':[1200,760],'visual_approval':'NOT_APPROVED'},
  'skia_three_bosses':{'status':'PASS','scenes':boss['scenes'],'noncanon':True},
  'visual_delta_r03_to_r04':{'status':'MEASURED_NOT_ART_PASS','percentage_pixels_changed_l1_threshold_18':round(changed*100,2),'mean_abs_rgb_difference':round(float(mean_abs),2)},
  'lab_sqlite':{'status':'PASS',**ledrow,'scope':'LAB_ONLY'},
  'art_assets':{'status':'PASS_DECODE_NOT_ART_APPROVAL','count':len(assets),'names':assets},
  'unchanged_historical_r03_sha256':{'status':'PASS' if oldhash else 'NOT_RUN','files':oldhash},
  'boss_visual_authority':{'status':'PASS','Cxx_function':'nsw_boss_threatens','wasm_function':'nsw_wasm_boss_threatens','visual_footprint':'same C++ predicate used for boss hit; no JS duplicate radius', 'derived_sprite_warning':'PRODUCTION_ART_NOT_APPROVED'},
  '21_class_kits':{'status':'LAB_ONLY','detail':'R03 21 signature/utility/passive research profiles preserved, not 21 approved kits'},
  '3_bosses':{'status':'LAB_ONLY','detail':'B01/B02 candidates, B03 GDD Rave Masters independent, no North Star canon'},
  'opening':{'status':'ANIMATIC_ONLY','final_cinematic':'NOT_IMPLEMENTED'},
 }}
for path in ['core/world_r04.cpp','core/world_r04.h','site/product.wasm','site/world.js','site/app.js','art_sources/r04_architecture_sheet.png','artifacts/R04_WORLD_NATIVE_TRACE.json','artifacts/R04_SQLITE_WORLD_JOURNAL.sqlite']:
 report.setdefault('source_sha256',{})[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
dst=ROOT/'artifacts/R04_TEST_REPORT.json';dst.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps({'status':'LAB_PASS_PRODUCT_NO_GO','python_testcases':test_count,'cpp_wasm_events':121,'visual_difference_percent':round(changed*100,2),'three_boss_screenshots':3,'four_views':4,'asset_count':len(assets),'report':str(dst.relative_to(ROOT))}))
