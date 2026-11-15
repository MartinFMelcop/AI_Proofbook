#!/usr/bin/env python3
"""Strict ART ASSET admission. Never authorizes artistic quality automatically.
Use as preflight on an *author provided/approved* four-side atlas. R07 ships none.
"""
from __future__ import annotations
from pathlib import Path
from hashlib import sha256
from PIL import Image,ImageChops
import json,re
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'site/assets/world'
TARGETS={'1':'r07_cottage','2':'r07_forge','3':'r07_apothecary'}

def validate(d:dict, assets:Path=ASSETS):
 errors=[]
 if d.get('state') != 'AUTHOR_ART_APPROVED': errors.append('approval_not_granted')
 buildings=d.get('buildings',{})
 for id,name in TARGETS.items():
  b=buildings.get(id) or {}
  for fld in ('license_checked','scale_anchor_reviewed'):
   if b.get(fld) is not True:errors.append(f'{id}:{fld}_not_verified')
  faces,hashes=b.get('faces'),b.get('sha256')
  if not isinstance(faces,list) or len(faces)!=4 or not isinstance(hashes,list) or len(hashes)!=4:
   errors.append(f'{id}:missing_4_faces');continue
  if faces != [f'{name}_{i}' for i in range(4)]:errors.append(f'{id}:face_order_or_identity')
  if any(not isinstance(h,str) or not re.fullmatch('[a-f0-9]{64}',h) for h in hashes):
   errors.append(f'{id}:invalid_sha256');continue
  if len(set(hashes))!=4:errors.append(f'{id}:reused_source_hash')
  dims=[];actual_hashes=[]
  for i,base in enumerate(faces):
   if not isinstance(base,str) or '/' in base or '\\' in base or '..' in base:
    errors.append(f'{id}:{i}:invalid_filename');continue
   path=assets/(base+'.webp')
   if not path.is_file():errors.append(f'{id}:{i}:missing');continue
   raw=path.read_bytes();h=sha256(raw).hexdigest();actual_hashes.append(h)
   if h!=hashes[i]:errors.append(f'{id}:{i}:hash_mismatch')
   try:
    with Image.open(path) as im:
     if im.mode!='RGBA':errors.append(f'{id}:{i}:not_rgba')
     w,hh=im.size;dims.append((w,hh))
     if w<128 or hh<128 or w>2048 or hh>2048:errors.append(f'{id}:{i}:dimensions_out_of_range')
     if im.getchannel('A').getextrema()[0]>=16:errors.append(f'{id}:{i}:no_transparency')
     if not im.getchannel('A').getbbox():errors.append(f'{id}:{i}:empty_sprite')
   except Exception:errors.append(f'{id}:{i}:unreadable')
  if len(dims)==4 and len(set(dims))!=1:errors.append(f'{id}:inconsistent_canvas_dimensions')
  if len(actual_hashes)==4 and len(set(actual_hashes))!=4:errors.append(f'{id}:identical_asset_bytes')
 return {'status':'READY_FOR_HUMAN_VISUAL_REVIEW_ONLY' if not errors else 'BLOCKED','errors':sorted(set(errors)),'eligible_for_art_approval':False}

if __name__=='__main__':
 path=ROOT/'docs/R07_FACADE_ART_GATE.json'
 print(json.dumps(validate(json.loads(path.read_text())),indent=2))
