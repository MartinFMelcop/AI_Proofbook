"""R03 visual candidate: no black individual-cell outlines, five ground variants per terrain type.
Pure deterministic painterly texture. Keeps material art as LAB study, not ART_APPROVED.
"""
from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
import random,math,json,hashlib
ROOT=Path(__file__).resolve().parent.parent
DST=ROOT/'site/assets/world';DST.mkdir(parents=True,exist_ok=True)
BASE={0:(47,78,62),1:(79,83,86),2:(46,78,62),3:(31,73,90),4:(38,43,47),6:(69,82,62),7:(121,112,95),8:(48,63,57),9:(77,69,70)}
entries=[]
W,H=128,72
for kind,base in BASE.items():
 for variant in range(5):
  rng=random.Random(kind*9929+variant*19837+20261115)
  im=Image.new('RGBA',(W,H),(0,0,0,0));px=im.load()
  for yy in range(H):
   for xx in range(W):
    # perfect diamond clip, soft physical transition. No black stroke between same ground type.
    q=abs((xx+.5-W/2)/(W/2))+abs((yy+.5-H/2)/(H/2))
    if q>1:continue
    noise=rng.gauss(0,4.1)+math.sin(xx*.14+variant*4)*3+math.cos(yy*.22+kind)*2
    if kind==3:noise+=math.sin(xx*.08+yy*.15+variant)*5
    shade=1.6*((H-yy)/H)
    pix=tuple(max(0,min(255,int(b+noise+shade))) for b in base)
    px[xx,yy]=(*pix,255)
  draw=ImageDraw.Draw(im,'RGBA')
  if kind in (0,2,6):
   for i in range(72):
    x=rng.randrange(8,120);y=rng.randrange(5,68)
    if px[x,y][3]<255:continue
    L=rng.randrange(2,6)
    draw.line((x,y,x-1,y-L,x+1,y-L-1),fill=(127,168,94,rng.randrange(20,63)),width=1)
    if rng.random()<.12:draw.point((x+3,y-1),fill=(192,174,102,95))
  elif kind in (1,7,9):
   for i in range(12):
    x=rng.randrange(10,118);y=rng.randrange(11,62)
    if px[x,y][3]<255:continue
    dx=rng.randrange(6,22);dy=rng.randrange(3,10)
    draw.line((x-dx//2,y,x,y+dy//3,x+dx//2,y+dy//5),fill=(25,27,30,48),width=1)
    draw.line((x-dx//2,y-1,x,y+dy//3-1),fill=(193,177,152,30),width=1)
  elif kind==3:
   for i in range(12):
    x=rng.randrange(10,106);y=rng.randrange(10,60)
    if px[x,y][3]<255:continue
    draw.arc((x,y,x+17,y+7),180,350,fill=(136,185,201,70),width=1)
  elif kind in (4,8):
   for i in range(19):
    x=rng.randrange(10,114);y=rng.randrange(10,58)
    if px[x,y][3]<255:continue
    draw.ellipse((x,y,x+2,y+2),fill=(104,115,111,30))
  name=f'material_{kind}_{variant}.webp'
  path=DST/name;im.save(path,'WEBP',quality=89,method=6)
  entries.append({'tile':kind,'variant':variant,'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(ROOT/'docs/R03_MATERIAL_RECEIPTS.json').write_text(json.dumps({'approval':'ART_REVIEW_PENDING','algorithm':'deterministic procedural raster; no per-cell dark outline','variants':entries},indent=2)+'\n')
print(json.dumps({'materials':len(entries),'bytes':sum((ROOT/x['path']).stat().st_size for x in entries)}))
