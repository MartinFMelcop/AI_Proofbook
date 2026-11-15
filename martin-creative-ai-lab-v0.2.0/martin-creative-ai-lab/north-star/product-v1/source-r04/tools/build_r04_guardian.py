from PIL import Image,ImageDraw,ImageFilter
import numpy as np
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];p=R/'site/assets/world/r04_eldertree.webp'
im=Image.open(p).convert('RGBA');a=np.asarray(im).copy()
# Separate boss variant from decorative forest assets, LAB_ONLY; no canonical entity claim.
rgb=a[:,:,:3].astype(np.float32);alpha=a[:,:,3]
green=rgb[:,:,1]>rgb[:,:,0]*1.11
rgb[green,0]=np.clip(rgb[green,0]*.9+20,0,255)
rgb[green,1]=np.clip(rgb[green,1]*.60,0,255)
rgb[green,2]=np.clip(rgb[green,2]*.9+29,0,255)
a[:,:,:3]=rgb.astype(np.uint8)
base=Image.fromarray(a,'RGBA');w,h=base.size
d=ImageDraw.Draw(base,'RGBA')
# Implied face on central trunk; stylized, not fully four-facing.
d.polygon([(w*.43,h*.50),(w*.48,h*.485),(w*.475,h*.505)],fill=(235,137,244,255))
d.polygon([(w*.53,h*.485),(w*.59,h*.50),(w*.54,h*.505)],fill=(235,137,244,255))
d.arc((w*.46,h*.52,w*.57,h*.59),30,150,fill=(179,71,197,230),width=4)
for i in range(5):
 x=int(w*(.39+i*.06));d.line([(w*.50,h*.64),(x,h*.81)],fill=(149,71,189,135),width=3)
out=R/'site/assets/world/r04_guardian_boss.webp';base.save(out,'WEBP',lossless=True)
(R/'docs/R04_GUARDIAN_RECEIPT.json').write_text(json.dumps({'file':str(out.relative_to(R)),'source':str(p.relative_to(R)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'approval':'LAB_ONLY_NOT_CANON_NOT_FOUR_FACING'},indent=2)+'\n')
print('guardian sprite saved',base.size)
