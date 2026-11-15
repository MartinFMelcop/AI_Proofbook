"""Rebuild 2.5D art research exports from locally preserved image sources.
Requires Pillow + numpy; transforms are repeatable, but artwork is NOT author-approved.
"""
from pathlib import Path
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'art_sources';OUT=ROOT/'site/assets/world'
OUT.mkdir(exist_ok=True,parents=True)
for name in ['watchtower','deadpine','runestone','brazier','wagon','well']:
 image=Image.open(SRC/'world_props'/f'{name}.png').convert('RGBA')
 image.thumbnail((280,325),Image.Resampling.LANCZOS)
 image.save(OUT/f'{name}.webp',format='WEBP',quality=90,method=6)
sheet=Image.open(SRC/'hero_four_view_sheet_source.png').convert('RGB')
w,h=sheet.size
for i,(ix,iy) in enumerate([(0,0),(1,0),(0,1),(1,1)]):
 image=sheet.crop((ix*w//2,iy*h//2,(ix+1)*w//2,(iy+1)*h//2))
 a=np.asarray(image,dtype=np.uint8)
 darkness=np.max(255-a.astype(np.float32),axis=2)
 alpha=np.clip((darkness-18)*6.5,0,255).astype('uint8')
 image=Image.fromarray(np.concatenate([a,alpha[:,:,None]],axis=2),'RGBA')
 bounds=image.getchannel('A').getbbox()
 if bounds:image=image.crop(bounds)
 image.thumbnail((245,325),Image.Resampling.LANCZOS)
 image.save(OUT/f'hero_{i}.webp',format='WEBP',quality=88,method=6)
print('10 world art exports regenerated from local sources; ART_NOT_APPROVED')
