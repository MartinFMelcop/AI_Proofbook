"""Deterministic, original pixel-material study for the same Canvas renderer.
Ground art generated from code; not artistically certified or imported canon.
"""
from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
import random,math,hashlib,json
root=Path(__file__).resolve().parent.parent
out=root/'site/assets/world'
out.mkdir(parents=True,exist_ok=True)
colors={0:(48,80,70),1:(76,84,88),2:(49,85,62),3:(31,75,96),4:(39,45,45),6:(65,79,60),7:(127,117,99),8:(50,60,59),9:(78,73,74)}
receipts=[]
for t,col in colors.items():
 rng=random.Random(20261115+t*103)
 im=Image.new('RGBA',(128,72));px=im.load();base=col
 for y in range(im.height):
  for x in range(im.width):
   on=(abs(x-63.5)/63.5+abs(y-35.5)/35.5)<=1
   if not on:continue
   grain=rng.gauss(0,6)
   grain+=math.sin(x*.32+y*.17)*2+math.sin(y*.47-x*.12)*2
   if t==3:grain+=5*math.sin((x-y*.4)*.21)
   elif t in (2,6):grain+=2*math.sin(x*.3)*math.cos(y*.6)
   p=tuple(max(0,min(255,int(v+grain))) for v in base)
   px[x,y]=(*p,255)
 d=ImageDraw.Draw(im,'RGBA')
 if t==3:
  for k in range(14):
   x=rng.randrange(5,110);y=rng.randrange(9,64)
   d.arc((x,y,x+18,y+8),start=200,end=350,fill=(127,181,187,125),width=1)
 elif t in (1,7,9):
  for i in range(6):
   x=rng.randrange(10,117);y=rng.randrange(9,62)
   d.line((x-15,y-3,x,y,x+13,y-1),fill=(25,32,39,115),width=1)
   d.line((x-7,y-4,x+2,y+1),fill=(157,147,130,65),width=1)
  if t==7:
   for i in range(4):
    x=rng.randrange(20,112);y=rng.randrange(15,60)
    d.line((x-17,y+2,x+18,y-1),fill=(224,208,157,65),width=1)
 else:
  for i in range(17 if t in (0,2,6) else 6):
   x=rng.randrange(2,126);y=rng.randrange(3,70)
   if px[x,y][3]==0:continue
   c=(145,166,110,144) if t in (0,2,6) else (114,130,116,70)
   d.line((x,y+2,x-1,y-2,x+1,y-3),fill=c,width=1)
 # Inlaid polished edge, matched in each rotation.
 outline=[(64,0),(127,35),(64,71),(0,35),(64,0)]
 d.line(outline,fill=(17,24,29,115),width=2)
 path=out/f'material_{t}.webp';im.save(path,'WEBP',quality=87,method=6)
 receipts.append({'tile_code':t,'path':str(path.relative_to(root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'origin':'original Python raster shader'})
(root/'docs/R02_MATERIAL_RECEIPTS.json').write_text(json.dumps({'model':'procedural material fixture','approval':'ART_REVIEW_PENDING','tiles':receipts},indent=2)+'\n')
print('procedural materials',len(receipts))
