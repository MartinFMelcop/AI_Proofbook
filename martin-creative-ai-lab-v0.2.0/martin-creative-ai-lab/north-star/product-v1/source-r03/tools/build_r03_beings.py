"""Four-facing NPC *concept* artwork to replace geometric cones, never ART_APPROVED.
Input is an original generated raster sheet, R03-owned, preserving source provenance.
"""
from pathlib import Path
import numpy as np, cv2, hashlib, json
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'art_sources/r03_npc_four_view_original.png'
if not SRC.exists(): raise FileNotFoundError(SRC)
image=Image.open(SRC).convert('RGB')
w,h=image.size
assert w>900 and h>900
out=ROOT/'site/assets/world';out.mkdir(exist_ok=True,parents=True)
ids=['guard','leader','merchant','herbalist']
receipts=[]
for row,who in enumerate(ids):
 for col in range(4):
  crop=np.asarray(image.crop((round(col*w/4),round(row*h/4),round((col+1)*w/4),round((row+1)*h/4))).convert('RGB'))
  hh,ww=crop.shape[:2]
  hi=crop.max(axis=2);lo=crop.min(axis=2)
  candidate=(lo>=170)&((hi-lo)<=42) # near-white neutral source paper
  seed=np.zeros((hh+2,ww+2),np.uint8)
  # flood only candidate, do NOT erase isolated white clothing
  cc=np.zeros((hh+2,ww+2),np.uint8)
  cc[1:-1,1:-1]=(candidate.astype(np.uint8)*255)
  border=np.zeros((hh,ww),np.uint8);border[0,:]=1;border[-1,:]=1;border[:,0]=1;border[:,-1]=1
  seed[:]=0
  mask=cc[1:-1,1:-1].copy()
  # flood-fill background in a binary connectivity mask from all four borders
  from scipy.ndimage import binary_propagation
  bg=binary_propagation(border.astype(bool)&candidate,mask=candidate)
  # inner holes often exist between arms, remove only neutral large components
  # OpenCV labels avoid aggressive erasure of light accessories
  remain=candidate & ~bg
  n,lab,stats,_=cv2.connectedComponentsWithStats(remain.astype(np.uint8),8)
  for k in range(1,n):
   if stats[k,cv2.CC_STAT_AREA]>85 and (stats[k,cv2.CC_STAT_WIDTH]>20 or stats[k,cv2.CC_STAT_HEIGHT]>20):bg |= lab==k
  fg=(~bg).astype(np.uint8)*255
  # smooth anti-alias boundaries, retain full opacity away from the boundary
  fg=cv2.morphologyEx(fg,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
  fg=cv2.GaussianBlur(fg,(3,3),.7)
  rgba=np.dstack((crop,fg))
  if int(np.count_nonzero(fg>140))<5000:raise AssertionError(f'Unusable sprite {who} {col}')
  yy,xx=np.where(fg>30)
  l,r,t,b=int(xx.min()),int(xx.max()+1),int(yy.min()),int(yy.max()+1)
  obj=Image.fromarray(rgba,'RGBA').crop((l,t,r,b))
  # uniform pixel canvas and feet-aligned pivot
  target=Image.new('RGBA',(192,224),(0,0,0,0))
  scale=min(164/obj.width,204/obj.height)
  obj=obj.resize((int(round(obj.width*scale)),int(round(obj.height*scale))),Image.Resampling.LANCZOS)
  target.alpha_composite(obj,((192-obj.width)//2,220-obj.height))
  dst=out/f'npc_{row+1}_{col}.webp'
  target.save(dst,'WEBP',quality=93,method=6)
  receipts.append({'being':row+1,'character':who,'view':col,'src_bbox':[l,t,r,b],'alpha_pixels':int(np.count_nonzero(np.asarray(target.getchannel('A'))>128)),'file':str(dst.relative_to(ROOT)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
payload={'source':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'source_resolution':[w,h],'orientations':[0,90,180,270],'sprites':receipts,'approval':'ART_REVIEW_PENDING','note':'not a rig, no human visual approval, four-view poses not independently authored animations'}
(ROOT/'docs/R03_NPC_ART_RECEIPTS.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'npc_sprites':len(receipts),'bytes':sum((ROOT/r['file']).stat().st_size for r in receipts),'smallest_alpha':min(r['alpha_pixels'] for r in receipts)}))
