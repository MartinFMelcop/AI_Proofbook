#!/usr/bin/env python3
"""Independent, read-only owner verification plus R12 lab graphics evidence.
This program does NOT certify authored art, film, kits, boss identity or product release.
"""
from pathlib import Path
from PIL import Image,ImageChops
from zipfile import ZipFile
import subprocess,hashlib,json,re
import numpy as np
R=Path(__file__).resolve().parents[1]
ZIP=Path('/mnt/data/MMAI_PRODUCT_V1_20261115_R06.zip')
def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha(p):return sha_bytes(Path(p).read_bytes())
def run(*cmd):
 p=subprocess.run(cmd,cwd=R,text=True,capture_output=True)
 if p.returncode:raise RuntimeError(f'FAILED {cmd}:\n{p.stdout[-1500:]}\n{p.stderr[-1800:]}')
 return p.stdout+'\n'+p.stderr

def image_stats(old,new):
 a=np.asarray(Image.open(old).convert('RGB'),dtype=np.int16)
 b=np.asarray(Image.open(new).convert('RGB'),dtype=np.int16)
 if a.shape!=(760,1200,3) or b.shape!=(760,1200,3):raise AssertionError('invalid Skia frame dimensions')
 diff=np.abs(a-b).mean(2)
 return {'rgb_L1_gt18_pixel_pct':round(float((diff>18).mean()*100),4),
         'mean_rgb_difference':round(float(diff.mean()),4)}

def main():
 u=run('python3','-m','unittest','discover','-s','tests','-p','test_*.py','-q')
 cases=int(re.search(r'Ran (\d+) tests',u).group(1))
 assert cases>=251,cases
 run('sh','tools/build.sh')
 run('cc','-std=c17','-Wall','-Wextra','-Werror','-O2','tests/c17_abi_r05.c','-Icore','-Lartifacts','-lns_world_r05','-Wl,-rpath,$ORIGIN','-o','artifacts/c17_abi_r05')
 c17=json.loads(run('./artifacts/c17_abi_r05').strip().splitlines()[0]);assert c17['PASS'] and c17['abi']==5
 node=json.loads(run('node','tests/test_r07_facade_contract.mjs').strip().splitlines()[0]);assert node['PASS'] and node['checks']==44
 r12node=json.loads(run('node','tests/test_r12_visual_contract.mjs').strip().splitlines()[0]);assert r12node['PASS'] and r12node['checks']>=67
 seq={}
 for v,filename,n in [('R05','test_world_r05_wasm.mjs',121),('R04','test_world_r04_wasm_history.mjs',121),('R03','test_world_r03_wasm_history.mjs',121),('R02','test_world_r02_wasm_history.mjs',116),('R01','test_world_wasm.mjs',100)]:
  report=json.loads(run('node','tests/'+filename).strip().splitlines()[0]);assert report['PASS'] and report['events']==n
  seq[v]=n
 run('python3','tools/world_r05_ledger.py','verify','artifacts/R05_SQLITE_WORLD_JOURNAL.sqlite')
 drawn=run('node','tests/render_r12_lab_skia.mjs')
 default=run('node','tests/render_r12_fallback_skia.mjs')
 bosses=json.loads(run('node','tests/render_r12_boss_motion_skia.mjs').strip().splitlines()[0]);assert bosses['PASS'] and len(bosses['scenes'])==6
 beings=run('node','tests/render_r12_being_motion_skia.mjs')
 assert drawn.count('R12_LAB_VIEW_')==4 and default.count('R12_DEFAULT_FALLBACK_VIEW_')==4 and beings.count('R12_BEING_MOTION_FRAME_')==4
 with ZipFile(ZIP) as z:
  files=['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/assets/opening_animatic.mp4','site/camera4.js']
  immutable={v:sha(R/v)==sha_bytes(z.read(v)) for v in files}
 assert all(immutable.values()),immutable
 arr=json.loads((R/'art_sources/R12_SILHOUETTE_ALIGNMENT.json').read_text())
 assert len(arr['faces'])==12
 vstats={}
 for i in range(4):
  r11=R/f'artifacts/R11_CANDIDATE_VIEW_{i}.png';r12=R/f'artifacts/R12_LAB_VIEW_{i}.png'
  fb=Image.open(R/f'artifacts/R12_DEFAULT_FALLBACK_VIEW_{i}.png').convert('RGBA')
  oldfb=Image.open(R/f'artifacts/R11_FALLBACK_VIEW_{i}.png').convert('RGBA')
  assert ImageChops.difference(fb,oldfb).getbbox() is None,'default fallback changed'
  s=image_stats(r11,r12);assert s['rgb_L1_gt18_pixel_pct']>0.5,s
  s['fallback_identical_to_R11']=True;vstats[str(i*90)]=s
 effects={}
 for b in (1,2,3):
  p=R/f'artifacts/R12_BOSS_{b}_FRAME_0.png';q=R/f'artifacts/R12_BOSS_{b}_FRAME_1.png'
  s=image_stats(p,q);assert s['rgb_L1_gt18_pixel_pct']>.1,s
  effects[str(b)]=s
 being={}
 for i in (1,2,3):
  s=image_stats(R/'artifacts/R12_BEING_MOTION_FRAME_0.png',R/f'artifacts/R12_BEING_MOTION_FRAME_{i}.png')
  assert s['rgb_L1_gt18_pixel_pct']>.1,s
  being[str(i)]=s
 # Inputs are existing R11 artwork, fully unmodified.
 painting_sha={}
 for key in arr['faces']:
  painting_sha[key]=sha(R/'site/assets/world'/f'r11_{key}.webp')
  assert painting_sha[key]==arr['faces'][key]['sha256']
 report={'schema':'mmai.product.v1.r12.actual.renderer.qa.v1',
   'technical_status':'PASS', 'art_status':'ART_REVIEW_PENDING', 'product_status':'PRODUCT_NO_GO',
   'engine':'C++20/C17 owner ABI5 unchanged', 'cpp_wasm_accepted_intents':seq,
   'python_unittest_cases':cases,'node_r07_assertions':44,'node_r12_assertions':r12node['checks'],
   'c17_abi5':'PASS_EXECUTED','sqlite_historical_121_event_journal':'VERIFIED',
   'renderer':'actual site/world.js with skia-canvas CPU; NOT browser/Windows',
   'skia_camera_views':4,'skia_default_fallback_views':4,'skia_temporal_boss_frames':6,'skia_temporal_being_frames':4,
   'four_camera_improvements':vstats,'three_boss_temporal_differences':effects,'being_temporal_differences':being,
   'original_cxx_and_wasm_hashes_unchanged':immutable,
   'twelve_R11_artworks_unchanged_by_sha256':True,'artwork_sha256':painting_sha,
   'new_art_created':False,'new_skeleton_rigs_created':False,'bosses_canonized':False,
   'limitations':['Image generator returned an error; no painted roof/door/chimney fixes were created',
     'Four-view painted architecture remains candidate with differing door/chimney details',
     'Animated sprite warping and effects are temporal lab presentation, not hand-authored skeletal rigs',
     'Three boss identities, 21 kit identities, rights and canon gates remain unapproved',
     'No normal-user Windows browser or GPU run; no finished opening or multiplayer MMO']}
 out=R/'artifacts/R12_TEST_REPORT.json';out.write_text(json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
 print(json.dumps({'PASS':True,'technical':'LAB_PASS_PRODUCT_NO_GO','python':cases,'node_visual_checks':r12node['checks'],'actions':seq,'skia_frames':18,'camera_change':vstats,'boss_motion':effects,'frozen_code':immutable},ensure_ascii=False))

if __name__=='__main__':main()
