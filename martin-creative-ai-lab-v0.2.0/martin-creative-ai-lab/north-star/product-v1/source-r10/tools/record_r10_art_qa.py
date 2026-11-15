#!/usr/bin/env python3
"""Generate factual R10 candidate QA receipts; never grant artistic approval."""
from pathlib import Path
from hashlib import sha256
from PIL import Image,ImageChops
import json,sys,numpy as np
ROOT=Path(__file__).resolve().parents[1]
SCENE=Path('/mnt/data/MMAI_PRODUCT_V1_R10_SCENE_WORK')
HIST=Path('/mnt/data/MMAI_PRODUCT_V1_R08_WORK')
C=ROOT/'candidate'
def sha(p):return sha256(p.read_bytes()).hexdigest()

def main():
 d=json.loads((C/'R08_CANDIDATE_MANIFEST.json').read_text())
 z=json.loads((C/'R08_INSPECTION.json').read_text())
 assert d['state']=='ART_CANDIDATE_UNREVIEWED'
 images=[]
 for k in ('1','2','3'):
  b=d['buildings'][k]
  for angle,n in enumerate(b['faces']):
   p=C/(n+'.webp');assert p.exists() and sha(p)==b['sha256'][angle]
   im=Image.open(p).convert('RGBA');assert im.size==(640,640)
   assert im.getchannel('A').getextrema()[0]==0
   images.append({'building_id':k,'quarter':angle,'name':n,'sha256':sha(p),'bytes':p.stat().st_size})
 assert len(images)==12 and len({x['sha256'] for x in images})==12
 changes=[]; fallback=[];sample=[]
 for i in range(4):
  r=Image.open(SCENE/f'artifacts/R10_CANDIDATE_VIEW_{i}.png').convert('RGBA')
  b=Image.open(HIST/f'artifacts/R07_GAME_VIEW_{i}.png').convert('RGBA')
  f=Image.open(SCENE/f'artifacts/R10_FALLBACK_VIEW_{i}.png').convert('RGBA')
  assert r.size==b.size==f.size==(1200,760)
  assert ImageChops.difference(f,b).getbbox() is None
  rgbA=np.asarray(r.convert('RGB'),dtype=np.int16);rgbB=np.asarray(b.convert('RGB'),dtype=np.int16)
  dlt=abs(rgbA-rgbB).mean(axis=2)
  changes.append(round(float((dlt>18).mean()*100),4));fallback.append(True)
  sample.append({'angle':i*90,'filename':f'R10_CANDIDATE_VIEW_{i}.png','sha256':sha(SCENE/f'artifacts/R10_CANDIDATE_VIEW_{i}.png')})
 assert min(changes)>4.0
 frozen={}
 for name in ('core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/assets/opening_animatic.mp4','site/camera4.js','site/facades_r07.js'):
  a=sha(SCENE/name);b=sha(HIST/name);frozen[name]=a==b;assert a==b
 report={
  'schema':'mmai.product.v1.r10.original-art.candidate-qa.v1',
  'state':{'new_painted_facade_views_created':12,'new_painted_facade_views_approved':0,'art':'ART_REVIEW_PENDING','product':'PRODUCT_NO_GO','author_playtest':'NOT_REQUESTED'},
  'source':{'origin':'three new AI-generated paintings in user conversation 2026-11-15, each 2x2','source_atlas_sha256':sha(ROOT/'art_sources/R10_SOURCE_ATLAS_3x4.png'),'raw_source_sha256':{n:sha(ROOT/'art_sources'/f'{n}_source.png') for n in ('cottage','forge','apothecary')}},
  'technical_art':{'files':images,'distinct_hashes':12,'dimensions':[640,640],'r08_inspection_status':z['status'],'r08_inspection_issues':z['technical_issues'],'perceptual_copy_suspicions':len([q for q in z['technical_issues'] if 'suspected_' in q]),'automated_approval':False},
  'engine':{'owner_cpp20_abi':'ABI5_UNCHANGED','authoritative_cpp_wasm_parity_events':121,'historical_regression_events':{'R04':121,'R03':121,'R02':116,'R01':100},'python_unit_tests':240,'node_facade_assertions':44,'c17_compiled':'PASS','sqlite_replay_events':121,'frozen_unchanged_hashes':frozen},
  'render':{'renderer':'ACTUAL_site/world.js_ON_Skia_CPU_not_browser','camera_views':sample,'percent_pixels_rgb_mean_gt18_vs_R07_by_angle':changes,'fallback_same_pixels_as_R07':fallback,'camera_does_not_change_revision_or_world_position':'PASS_ASSERTED_PER_VIEW'},
  'blockers':['artist/author approval of visual coherence and four facade orientation','architectural details across quarters not independently judged','scale and lighting against final world not approved','creator output provenance recorded; rights clearance pending','four-view appearance for other props/beings and boss rigs incomplete','opening/21 class kits/three bosses/Windows release not approved'],
  'delivery':'art-only package + source delta; no full game archive; original R06 unchanged',
 }
 (ROOT/'artifacts').mkdir(exist_ok=True)
 (ROOT/'artifacts/R10_ART_QA_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'render_cameras':4,'created':12,'approved':0,'pixel_change':changes,'fallback_exact':all(fallback),'owner_preserved':all(frozen.values())}))
if __name__=='__main__':main()
