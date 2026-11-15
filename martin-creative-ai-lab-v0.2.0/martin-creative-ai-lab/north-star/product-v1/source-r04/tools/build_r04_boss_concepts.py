"""Derive lab enemy silhouettes from existing R03 art; procedural wisp is original.
Gameplay enemy identities are NOT canon, and no pack is 'final boss quality'.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'site/assets/world'
records=[]
# B01 derive from lab guards: not a new, authored humanoid entity.
for i in range(4):
 src=OUT/f'npc_1_{i}.webp'; im=Image.open(src).convert('RGBA')
 a=np.asarray(im).copy().astype(np.float32);rgb=a[:,:,:3]; alpha=a[:,:,3]
 lum=(.2126*rgb[:,:,0]+.7152*rgb[:,:,1]+.0722*rgb[:,:,2])[...,None]
 tint=np.array([48,45,76],dtype=np.float32)
 rgb[:]=np.minimum(255,lum*.58+tint*.55)
 # Gold trim survives a little; magma red mantle highlights.
 hot=(a[:,:,0]>a[:,:,1]*1.2)&(a[:,:,0]>a[:,:,2]*1.14)&(alpha>50)
 rgb[hot]=np.array([143,52,69],dtype=np.float32)
 a[:,:,:3]=rgb
 out=Image.fromarray(a.astype('uint8'),'RGBA')
 d=ImageDraw.Draw(out,'RGBA');w,h=im.size
 d.ellipse([w*.44,h*.18,w*.49,h*.2],fill=(255,67,58,238));d.ellipse([w*.52,h*.18,w*.57,h*.2],fill=(255,67,58,238))
 dst=OUT/f'r04_ruinguardian_{i}.webp';out.save(dst,'WEBP',lossless=True)
 records.append({'boss':'B01','direction':i,'path':str(dst.relative_to(ROOT)),'source':str(src.relative_to(ROOT)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
# B02 semi-abstract spectral swamp stalker with solid hood and ribbon-like spectral form.
S=500; im=Image.new('RGBA',(S,S),(0,0,0,0));base=Image.new('RGBA',(S,S));d=ImageDraw.Draw(base,'RGBA')
# diffuse halo behind, multiple tendrils
for k in range(12):
 ang=2*math.pi*k/12
 cx,cy=247,200
 fx=210*math.cos(ang)+cx;fy=180*math.sin(ang)+cy
 mids=(cx+90*math.cos(ang+.36),cy+100*math.sin(ang+.36))
 d.line([(cx,cy),mids,(fx,fy)],fill=(25,180,163,110),width=12)
 d.ellipse((fx-8,fy-8,fx+8,fy+8),fill=(70,245,211,130))
blur=base.filter(ImageFilter.GaussianBlur(18));im.alpha_composite(blur)
d=ImageDraw.Draw(im,'RGBA')
# tattered ethereal cloak silhouette
cloak=[(250,95),(320,126),(359,220),(314,285),(344,367),(282,345),(310,443),(246,397),(201,468),(214,363),(166,395),(183,280),(143,236),(175,148)]
d.polygon(cloak,fill=(22,39,68,235),outline=(48,163,162,240),width=4)
for j in range(11):
 x=170+j*17
 d.line([(250,145),(x,280),(x+(j%3-1)*24,405)],fill=(34+j*5,144+j*3,171,125),width=3)
# hood, face void, bioluminescent glyph and eyes
d.ellipse((175,67,325,227),fill=(17,25,43,255),outline=(122,224,203,255),width=7)
d.polygon([(196,134),(245,101),(302,137),(276,215),(215,212)],fill=(10,13,29,255))
d.arc((179,70,323,230),math.pi*.99*180/math.pi,355,fill=(143,242,225,225),width=4)
d.ellipse((215,156,240,172),fill=(66,252,218,255));d.ellipse((264,155,290,171),fill=(66,252,218,255))
d.line([(240,195),(254,217),(266,196)],fill=(111,225,221,220),width=3)
# heart flame
for rad in [36,22,10]:d.ellipse((250-rad,275-rad,250+rad,275+rad),fill=(27,213,178,65+rad),outline=(130,247,235,240),width=2)
for i in range(15):
 k=i*31; y=300+i*7
 d.arc((155+(k%100),y,295+(k%100),y+70),18,135,fill=(30,173,190,80),width=3)
out=OUT/'r04_wisp.webp';im.save(out,'WEBP',lossless=True);records.append({'boss':'B02','path':str(out.relative_to(ROOT)),'source':'PIL originally procedural lab spirit','sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
(ROOT/'docs/R04_BOSS_ASSET_RECEIPTS.json').write_text(json.dumps({'status':'LAB_CONCEPT_NOT_CANON','assets':records},indent=2)+'\n')
print('generated',len(records),'boss concept sprites')
