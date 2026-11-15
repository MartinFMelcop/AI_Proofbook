#!/usr/bin/env python3
"""One NONCANON experimental boss wraith, transformed from an existing generated
herbalist sprite for four camera orientations. This is neither independent
illustration nor approved original character art. No external artwork used.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
from scipy.ndimage import map_coordinates, gaussian_filter
R=Path(__file__).resolve().parents[1]; SRC=R/'site/assets/world'; W,H=256,320
entries=[]
for face in range(4):
 src=SRC/f'npc_4_{face}.webp'; im=Image.open(src).convert('RGBA'); box=im.getbbox(); crop=im.crop(box)
 crop.thumbnail((165,257),Image.Resampling.LANCZOS)
 for phase in range(4):
  t=phase*math.pi/2
  body=Image.new('RGBA',(W,H),(0,0,0,0));x=W//2-crop.width//2+round(2*math.sin(t));y=39+round(2*math.cos(t));body.alpha_composite(crop,(x,y))
  a=np.asarray(body,dtype=np.float32)
  alpha=a[:,:,3]/255
  # Recolor keeping original fabric texture and embroidery detail.
  lum=(.23*a[:,:,0]+.69*a[:,:,1]+.08*a[:,:,2])/255
  core=np.empty_like(a,dtype=np.uint8)
  core[:,:,0]=np.clip(9+30*lum,0,255).astype(np.uint8)
  core[:,:,1]=np.clip(35+115*lum,0,255).astype(np.uint8)
  core[:,:,2]=np.clip(55+145*lum,0,255).astype(np.uint8)
  core[:,:,3]=a[:,:,3].astype(np.uint8)
  spirit=Image.fromarray(core,'RGBA')
  bloom=np.uint8(np.clip(gaussian_filter(alpha,sigma=8)*100,0,115))
  glow=np.zeros_like(core);glow[:,:,0]=16;glow[:,:,1]=159;glow[:,:,2]=211;glow[:,:,3]=bloom
  out=Image.fromarray(glow,'RGBA')
  # Wisps are translucent torn cloth, behind the textured body.
  d=ImageDraw.Draw(out,'RGBA')
  for k in range(5):
   base=W//2+(k-2)*18
   wave=round(8*math.sin(t+k))
   d.polygon([(base-15,218),(base+10,208),(base+8+wave,275+3*k),(base-12+wave,310-3*k)],fill=(28,128+10*k,171+6*k,55))
  out.alpha_composite(spirit)
  # One eyes/rune highlight, still visual only.
  d=ImageDraw.Draw(out,'RGBA')
  cy=91+round(2*math.cos(t));cx=W//2
  d.ellipse((cx-9,cy-3,cx-2,cy+1),fill=(128,240,248,182))
  d.ellipse((cx+2,cy-3,cx+9,cy+1),fill=(128,240,248,182))
  dest=SRC/f'r06_wraith_{face}_{phase}.webp';out.save(dest,'WEBP',lossless=True,method=6)
  entries.append({'source':src.name,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'target':dest.name,'target_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'face':face,'frame':phase,'provenance':'DERIVED_EXISTING_NPC_ART_NONCANON'})
(R/'docs/R06_WRAITH_RECEIPTS.json').write_text(json.dumps({'schema':'mmai.r06.boss.art.derived.v1','source':'R03 generated NPC #4 illustrations, NOT a new independent painted boss','approval':'ART_REVIEW_PENDING','entries':entries},indent=2)+'\n')
print('Generated derived wraith frames',len(entries))
