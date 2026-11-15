#!/usr/bin/env python3
"""Deterministic, non-generative motion studies from existing R03/R04 source sprites.
Four directions remain their own R03/R04 paintings. These are deform cycles, NOT rigs.
Keep original assets untouched. All outputs have source hashes in docs/R06_MOTION_RECEIPTS.json.
"""
from pathlib import Path
import hashlib, json, math
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'site/assets/world'
DIRS=range(4)

def morph(src,phase,kind):
    im=Image.open(ASSETS/src).convert('RGBA')
    a=np.array(im,dtype=np.uint8)
    H,W=a.shape[:2]
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
    theta=phase*math.pi/2
    # Body (high y) has a subtle counter-shift against gait. The skirt/boot zone
    # follows two opposing steps; torso and head preserve painted identity.
    h=np.clip((yy/H-.48)/.42,0,1)
    split=np.tanh((xx-W*.50)/(W*.095))
    amplitude=1.0 if kind=='npc' else .70
    dx=(2.1*np.sin(theta)*np.sin(np.pi*yy/H) + 3.5*h*split*np.sin(theta+.30))*amplitude
    dy=(1.6*np.cos(theta)*np.sin(np.pi*yy/H) + 1.6*h*np.sin(theta+split*.75))*amplitude
    dx+=.8*np.sin(theta+.3)*(1-h)
    # inverse image map keeps pixels inside 192x224 / boss image extents
    coords=[np.clip(yy-dy,0,H-1),np.clip(xx-dx,0,W-1)]
    output=np.stack([map_coordinates(a[:,:,i],coords,order=1,mode='constant',cval=0) for i in range(4)],axis=-1)
    # keep premultiply out of output to maintain alpha independent of brightness
    return Image.fromarray(output,'RGBA')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for i in range(1,5):
 for face in DIRS:
  src=f'npc_{i}_{face}.webp'; origin=ASSETS/src
  for phase in range(1,4):
   dest=ASSETS/f'npc_{i}_{face}_motion_{phase}.webp'
   morph(src,phase,'npc').save(dest,'WEBP',lossless=True,method=6)
   records.append(dict(source=src,source_sha256=sha(origin),target=dest.name,sha256=sha(dest),kind='npc_deform_study',face=face,phase=phase))
# Boss motion cycles based on original source, no new creature design.
for i in range(4):
 src=f'r04_ruinguardian_{i}.webp'
 for phase in range(1,4):
  dest=ASSETS/f'r06_boss_guard_{i}_motion_{phase}.webp'
  morph(src,phase,'boss').save(dest,'WEBP',lossless=True,method=6)
  records.append(dict(source=src,source_sha256=sha(ASSETS/src),target=dest.name,sha256=sha(dest),kind='boss_deform_study',face=i,phase=phase))
for slug,src in [('wisp','r04_wisp.webp'),('tree','r04_guardian_boss.webp')]:
 for phase in range(1,4):
  dest=ASSETS/f'r06_boss_{slug}_motion_{phase}.webp'
  morph(src,phase,'boss').save(dest,'WEBP',lossless=True,method=6)
  records.append(dict(source=src,source_sha256=sha(ASSETS/src),target=dest.name,sha256=sha(dest),kind='boss_deform_study',face='view_facing_billboard',phase=phase))
receipt={'schema':'mmai.r06.motion.receipt.v1','method':'scipy.ndimage.map_coordinates deterministic local deformation','claims':['not keyframed body rig','not new original boss identity','not art approved'], 'frames':records,'count':len(records)}
(ROOT/'docs/R06_MOTION_RECEIPTS.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'generated':len(records),'npc':48,'boss':18,'all_alpha_rgba':True,'first':records[0]['target']},ensure_ascii=False))
