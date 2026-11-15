"""Extract authored-as-concept sheet 3x3 into isolated transparent scene props.
Source was generated specifically for R04 and remains available in art_sources.
Not certified 4-facing assets. Purely visual consumer; no authority for collisions.
"""
from PIL import Image
from pathlib import Path
import numpy as np
from scipy.ndimage import binary_fill_holes, binary_dilation, gaussian_filter, label
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'art_sources/r04_architecture_sheet.png'
OUT=ROOT/'site/assets/world';OUT.mkdir(parents=True,exist_ok=True)
NAMES=['cottage','forge','apothecary','stonebridge','lamppost','fountain','blossom','eldertree','shrine']
im=Image.open(SRC).convert('RGB')
w,h=im.size
meta=[]
for idx,name in enumerate(NAMES):
 r,c=divmod(idx,3)
 box=(round(c*w/3)+3,round(r*h/3)+3,round((c+1)*w/3)-3,round((r+1)*h/3)-3)
 crop=np.asarray(im.crop(box)).copy().astype(np.float32)
 # Outside-white mask. Do not use chroma key on dark artwork details.
 whiteness=np.min(crop,axis=2)
 nearwhite=(whiteness>231)&((crop.max(axis=2)-crop.min(axis=2))<23)
 # Keep nonwhite foreground, anti-aliased edges and enclosed tiny highlights.
 foreground=~nearwhite
 # Remove isolated noise by looking at connected subject extent, not a manual bounding box.
 components,count=label(foreground)
 sizes=np.bincount(components.ravel());sizes[0]=0
 main=components==np.argmax(sizes)
 extent=binary_dilation(main,iterations=2)
 interior=binary_fill_holes(main)
 base=main|interior
 alpha=np.uint8(np.clip(gaussian_filter(base.astype(float),0.8)*255,0,255))
 rgba=np.concatenate([np.uint8(crop),alpha[...,None]],axis=2)
 a=Image.fromarray(rgba,'RGBA')
 bbox=a.getchannel('A').getbbox()
 if bbox:a=a.crop(bbox)
 a.thumbnail((500,500),Image.Resampling.LANCZOS)
 dst=OUT/f'r04_{name}.webp'
 a.save(dst,'WEBP',quality=91,method=6,lossless=True)
 meta.append({'asset':name,'file':str(dst.relative_to(ROOT)),'size':list(a.size),'alpha_extrema':a.getchannel('A').getextrema(),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'art_status':'NONCANON_R04_CONCEPT_NOT_FOUR_FACING'})
(ROOT/'docs/R04_ARCHITECTURE_ASSET_RECEIPTS.json').write_text(json.dumps({'schema':'mmai.r04.architecture.receipts','source':'art_sources/r04_architecture_sheet.png','source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'assets':meta,'purpose':'Visual scene props, not canonical world objects; image-facing only'},indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'assets':len(meta),'sizes':[(x['asset'],x['size']) for x in meta]}))
