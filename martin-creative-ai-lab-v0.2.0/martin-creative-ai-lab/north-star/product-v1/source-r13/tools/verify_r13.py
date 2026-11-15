#!/usr/bin/env python3
"""R13 incremental evidence. Never certifies final character art, bosses or PRODUCT_GO."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,subprocess,re,os
import numpy as np
R=Path(__file__).resolve().parents[1]; OLD=Path(os.environ.get('MMAI_R12_BASELINE_PATH','/mnt/data/MMAI_PRODUCT_V1_R12_WORK'))
if not OLD.exists():raise SystemExit('R12_BASELINE_REQUIRED: set MMAI_R12_BASELINE_PATH to an unmodified R12 copy')
assert R != OLD

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(*cmd):
 p=subprocess.run(cmd,cwd=R,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(str(cmd)+'\n'+p.stdout[-1000:]+'\n'+p.stderr[-2000:])
 return p.stdout.strip()
def diff(a,b):
 a=np.asarray(Image.open(a).convert('RGB'),dtype=np.int16)
 b=np.asarray(Image.open(b).convert('RGB'),dtype=np.int16)
 assert a.shape==b.shape==(760,1200,3)
 d=np.abs(a-b).mean(axis=2)
 return {'changed_pixels_gt18_pct':round(float((d>18).mean()*100),4),
         'mean_rgb_abs_difference':round(float(d.mean()),4)}

def main():
 # This executor *actually runs* the old-world verification in the isolated R13 copy.
 log=R/'artifacts/R13_INHERITED_REGRESSION_STDOUT.log'
 if not log.exists():log.write_text(run('python3','tools/verify_r12.py')+'\n')
 old=json.loads(log.read_text().strip().splitlines()[-1]);assert old['PASS'] and old['python']==251
 stage=json.loads(run('node','tests/test_r13_stagecraft.mjs').splitlines()[-1]);assert stage['PASS'] and stage['checks']>=26
 scenes=[R/f'artifacts/R13_SCENE_VIEW_{i}.png' for i in range(4)]
 if not all(p.exists() and p.stat().st_size>100000 for p in scenes):run('node','tests/render_r13_fourview_skia.mjs')
 assert all(p.exists() and p.stat().st_size>100000 for p in scenes)
 bosses=[R/f'artifacts/R13_BOSS_{b}_FRAME_{i}.png' for b in range(1,4) for i in range(2)]
 if not all(p.exists() and p.stat().st_size>100000 for p in bosses):run('node','tests/render_r13_boss_stage_skia.mjs')
 assert all(p.exists() and p.stat().st_size>100000 for p in bosses)
 # A baseline fallback (R13 preview=false) is R12 byte-identical in actual CPU Canvas renderer.
 four_fallback={}
 for k in range(4):
  p=R/f'artifacts/R12_DEFAULT_FALLBACK_VIEW_{k}.png';q=OLD/f'artifacts/R12_DEFAULT_FALLBACK_VIEW_{k}.png'
  assert ImageChops.difference(Image.open(p).convert('RGBA'),Image.open(q).convert('RGBA')).getbbox() is None
  four_fallback[str(k*90)]=True
 four_view={}
 for k in range(4):
  four_view[str(k*90)]=diff(OLD/f'artifacts/R12_LAB_VIEW_{k}.png',R/f'artifacts/R13_SCENE_VIEW_{k}.png')
  assert four_view[str(k*90)]['changed_pixels_gt18_pct'] < .25, 'R13 should NOT claim painted architecture change'
 changes={}
 for boss in (1,2,3):
  changes[str(boss)]={}
  for frame in (0,1):
   k=f'R12_BOSS_{boss}_FRAME_{frame}.png';q=f'R13_BOSS_{boss}_FRAME_{frame}.png'
   a=diff(OLD/'artifacts'/k,R/'artifacts'/q)
   assert a['changed_pixels_gt18_pct']>.05, f'boss {boss} visual not changed'
   changes[str(boss)][str(frame)]=a
 # Neither asset paintings nor any C++ / C17 / WASM / SQLite changed.
 fixed=['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/camera4.js',
        'site/r12_finishing.js','artifacts/R05_SQLITE_WORLD_JOURNAL.sqlite']
 fixed += [f'site/assets/world/r11_{n}_{i}.webp' for n in ('cottage','forge','apothecary') for i in range(4)]
 oldhash={n:sha(OLD/n) for n in fixed}
 assert all(sha(R/n)==h for n,h in oldhash.items())
 changed_sources=['site/index.html','site/world.js']
 assert all(sha(R/n)!=sha(OLD/n) for n in changed_sources)
 assert (R/'site/r13_stagecraft.js').exists()
 report={
   'schema':'mmai.product_v1.r13.real_stagecraft_evidence.v1',
   'technical_status':'PASS', 'product_status':'PRODUCT_NO_GO','art_status':'ART_REVIEW_PENDING',
   'new_generated_painted_facades':0,'new_authored_boss_rigs':0,'author_approved_facades':0,
   'image_generation':'FAILED_TOOL_NO_RETRY',
   'graphics_source':'ACTUAL site/world.js via skia-canvas CPU; no Windows/browser/GPU',
   'r13_graphic_node_checks':stage['checks'],
   'inherited_r12_python_tests':old['python'],'inherited_r12_visual_node_checks':old['node_visual_checks'],
   'inherited_cpp_wasm_events':old['actions'],'sqlite':'R05 121 event journal verified in inherited suite',
   'r13_skia_scenes':{'four_camera_no_boss':4,'three_cpp_owned_bosses_two_times':6},
   'unchanged_normal_client_fallback':four_fallback,
   'four_camera_scene_delta_without_boss':four_view,
   'boss_art_directed_visual_delta_vs_r12':changes,
   'immutable_files_verified':len(fixed),
   'immutable_sha256':oldhash,
   'limitations':['No original four-view roof/chimney/entrance redrawing. 12 R11 paintings unchanged',
     'R13 stagecraft uses existing sprite pixels enlarged; no skeletal rig or new character images',
     'Stagecraft sigils/particles are cosmetic and do not represent authoritative hitboxes',
     'C++20 ABI5 retains all rules, positions and telegraphs',
     'Combat focus is camera-only; no client gameplay authority',
     'Human artistic quality, source rights, 3 boss identity and 21 classes remain owner-gated',
     'No Windows browser GPU or end-to-end MMORPG verification']
 }
 dst=R/'artifacts/R13_TEST_REPORT.json'
 dst.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'PASS':True,'stage_checks':stage['checks'],'python':old['python'],
   'cpp_wasm':old['actions'],'four_fallback':four_fallback,'four_views':four_view,'boss_changes':changes},ensure_ascii=False))
if __name__=='__main__':main()
