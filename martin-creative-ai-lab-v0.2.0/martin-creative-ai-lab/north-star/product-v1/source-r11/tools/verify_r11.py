#!/usr/bin/env python3
"""Reproducible R11 candidate proof. No product/canon/art approval implied."""
from pathlib import Path
from PIL import Image,ImageChops
import hashlib, subprocess, json, re
import numpy as np

R=Path(__file__).resolve().parents[1]
R10=Path('/mnt/data/MMAI_PRODUCT_V1_R10_SCENE_WORK')
A=R/'art_sources/r11_cutouts'

def sh(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(*args):
 p=subprocess.run(args,cwd=R,text=True,capture_output=True)
 if p.returncode:raise AssertionError('RUN '+str(args)+'\n'+p.stdout[-2400:]+'\n'+p.stderr[-2400:])
 return p.stdout+'\n'+p.stderr

def main():
 p=run('python','-m','unittest','discover','-s','tests','-p','test_*.py','-q')
 tests=int(re.search(r'Ran (\d+) tests',p).group(1))
 assert tests==240,tests
 run('sh','tools/build.sh')
 run('cc','-std=c17','-Wall','-Wextra','-Werror','-O2','tests/c17_abi_r05.c','-Icore','-Lartifacts','-lns_world_r05','-Wl,-rpath,$ORIGIN','-o','artifacts/c17_abi_r05')
 c17=json.loads(run('./artifacts/c17_abi_r05').strip().splitlines()[0]);assert c17['PASS'] and c17['abi']==5
 nodeChecks=json.loads(run('node','tests/test_r07_facade_contract.mjs').strip().splitlines()[0]);assert nodeChecks['checks']==44
 seq={}
 for version,filename,n in [('r05','test_world_r05_wasm.mjs',121),('r04','test_world_r04_wasm_history.mjs',121),('r03','test_world_r03_wasm_history.mjs',121),('r02','test_world_r02_wasm_history.mjs',116),('r01','test_world_wasm.mjs',100)]:
  data=json.loads(run('node','tests/'+filename).strip().splitlines()[0]);assert data['PASS'] and data['events']==n,(version,data)
  seq[version]=n
 run('python','tools/world_r05_ledger.py','verify','artifacts/R05_SQLITE_WORLD_JOURNAL.sqlite')
 renderC=run('node','tests/render_r11_candidate_skia.mjs')
 renderF=run('node','tests/render_r11_fallback_skia.mjs')
 assert renderC.count('R11_CANDIDATE_VIEW_')==4 and renderF.count('R11_FALLBACK_VIEW_')==4
 original=['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/assets/opening_animatic.mp4','site/facades_r07.js','site/camera4.js']
 unchanged={p:sh(R/p)==sh(R10/p) for p in original}
 assert all(unchanged.values())
 assets={}
 manifest=json.loads((A/'R11_SOURCE_AND_CUTOUT_RECEIPT.json').read_text())
 assert manifest['paintings']==12 and not manifest['author_art_ack']
 for b in ['cottage','forge','apothecary']:
  assets[b]=[]
  for i in range(4):
   p=R/'site/assets/world'/f'r11_{b}_{i}.webp'
   with Image.open(p) as img:
    assert img.mode=='RGBA' and img.size==(640,640)
    a=np.asarray(img.getchannel('A'))
    assert a.max()==255 and (a>190).sum()>50000
   assets[b].append(sh(p))
  assert len(set(assets[b]))==4
 assert len(set(v for rows in assets.values() for v in rows))==12
 stats={}
 for i in range(4):
  old=Image.open(R10/f'artifacts/R10_CANDIDATE_VIEW_{i}.png').convert('RGB')
  new=Image.open(R/f'artifacts/R11_CANDIDATE_VIEW_{i}.png').convert('RGB')
  fb=Image.open(R/f'artifacts/R11_FALLBACK_VIEW_{i}.png').convert('RGBA')
  r10fb=Image.open(R10/f'artifacts/R10_FALLBACK_VIEW_{i}.png').convert('RGBA')
  assert old.size==new.size==(1200,760)
  assert ImageChops.difference(fb,r10fb).getbbox() is None,'Fallback changed!'
  diff=np.abs(np.asarray(old,dtype=np.int16)-np.asarray(new,dtype=np.int16)).mean(axis=2)
  pct=round(float((diff>18).mean()*100),4)
  assert pct>0.05,'R11 had no substantive scene delta'
  stats[str(i*90)]={'rgb_L1_gt18_pixel_pct_R10_to_R11':pct,
    'r11_png_bytes':(R/f'artifacts/R11_CANDIDATE_VIEW_{i}.png').stat().st_size,
    'fallback_matches_R10_pixelwise':True}
 report={
  'schema':'mmai.product.v1.r11.visual.candidate.qa.v1',
  'technical_status':'PASS','art_status':'PENDING_AUTHOR_AESTHETICS_AND_PROVENANCE_REVIEW',
  'product_status':'PRODUCT_NO_GO','approved_artwork_count':0,
  'source_sheets':3,'original_painted_views':12,'four_facing_billboard_art':'CANDIDATE',
  'core_abi':5,'cpp_wasm_accepted_intents':seq,'python_tests':tests,
  'node_facade_contract_assertions':44,'c17':'PASS',
  'sqlite_historical_journal':'VERIFIED_R05_121_EVENTS',
  'renderer':'Actual site/world.js with Node Skia Canvas, no Chromium/Windows',
  'skia_views':4,'canvas_stats':stats,
  'historic_code_hashes_unchanged':unchanged,
  'twelve_output_asset_sha256_unique':True,'asset_sha256':assets,
  'limitations':['No final art owner ACK','Building geometry/four side consistency needs human visual review',
   'Not animated boss/being rigs','Normal Windows browser not run','No multiplayer',
   'AI painting generation itself not a gameplay screenshot'],
 }
 dst=R/'artifacts/R11_TEST_REPORT.json';dst.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'RESULT':'PASS_TECH_ONLY_PRODUCT_NO_GO','python_tests':tests,'native_wasm_events':seq,'skia_views':4,'fallback_exact':True,'visual_deltas':stats},ensure_ascii=False))

if __name__=='__main__':main()
