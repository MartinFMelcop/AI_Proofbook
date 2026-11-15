"""Noncanonical 4-view x 4-pose concept sheet: crop original cells, preserve pivots and alpha.
Source art must remain in art_sources. This does NOT prove animation/rig fidelity.
"""
from pathlib import Path
from PIL import Image
import hashlib,json
root=Path(__file__).resolve().parent.parent
source=root/'art_sources/hero_r02_walk_sheet.png'
if not source.exists():raise FileNotFoundError(source)
im=Image.open(source).convert('RGBA');w,h=im.size
if w<900 or h<900:raise ValueError('unexpected tiny source')
files=[]
for direction in range(4):
 for frame in range(4):
  x0=round(frame*w/4);x1=round((frame+1)*w/4)
  y0=round(direction*h/4);y1=round((direction+1)*h/4)
  tile=im.crop((x0,y0,x1,y1))
  bb=tile.getchannel('A').point(lambda a:255 if a>40 else 0).getbbox()
  if not bb:raise ValueError(f'empty cell {direction},{frame}')
  obj=tile.crop(bb)
  # Source generator fills some cells to their boundaries; flag visible edge touch in receipt.
  # consistent pivot: last alpha pixel centered x=110, y=215.
  fit=Image.new('RGBA',(224,224),(0,0,0,0))
  scale=min(182/obj.width,209/obj.height,1.35)
  rw=max(1,int(obj.width*scale));rh=max(1,int(obj.height*scale))
  resized=obj.resize((rw,rh),Image.Resampling.LANCZOS)
  fit.alpha_composite(resized,((224-rw)//2,220-rh))
  path=root/f'site/assets/world/hero_{direction}_{frame}.webp'
  fit.save(path,'WEBP',quality=90,method=6)
  files.append({'orientation':direction,'pose':frame,'path':path.relative_to(root).as_posix(),'pivot':[112,220], 'source_alpha_bbox':[int(i) for i in bb], 'possible_cell_bleed':bb[0]==0 or bb[1]==0 or bb[2]>=tile.width or bb[3]>=tile.height, 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(root/'docs/R02_HERO_ANIMATION_RECEIPTS.json').write_text(json.dumps({'source':source.relative_to(root).as_posix(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_resolution':[w,h],'cols':4,'rows':4,'frames':files,'approval':'ART_REVIEW_PENDING','note':'4x4 frame groups generated as motion studies, not a verified rig or continuous animation'},indent=2)+'\n')
print(json.dumps({'source_px':im.size,'frames':len(files),'size':sum((root/f['path']).stat().st_size for f in files)}))
