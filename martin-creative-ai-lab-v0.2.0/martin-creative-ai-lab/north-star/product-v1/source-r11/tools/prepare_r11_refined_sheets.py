#!/usr/bin/env python3
"""R11: physically prepare four genuine painted views per source sheet.

This is a cutout, alpha-spill and ground-pivot pipeline, not an image painter,
not an art approval, and never rotates a picture to fabricate another face.
The three source sheets were newly generated in the author conversation.
"""
from pathlib import Path
from PIL import Image
import cv2
import numpy as np
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'art_sources'/'r11_sources'
OUT = ROOT/'art_sources'/'r11_cutouts'
WEBP = ROOT/'site'/'assets'/'world'
CATEGORIES = ('cottage','forge','apothecary')
SIZE = 640

def sha(b): return hashlib.sha256(b).hexdigest()

def clean_quad(quad):
    # Preserve opaque paint. Trim generated transparent/red matte contamination.
    a=quad.copy()
    alpha=a[:,:,3]
    r,g,b=[a[:,:,i].astype(np.int16) for i in range(3)]
    hot_red=(r>162)&(g<110)&(b<112)&(r>g*1.7)&(r>b*1.55)
    solid=((alpha>96)&(~hot_red)).astype(np.uint8)
    # Each subject is one physical cutout; isolated flecks are spill, not art.
    solid=cv2.morphologyEx(solid,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    count,lab,stats,_=cv2.connectedComponentsWithStats(solid,8)
    if count<2: raise AssertionError('missing foreground component')
    idx=1+int(np.argmax(stats[1:,cv2.CC_STAT_AREA]))
    main=(lab==idx).astype(np.uint8)
    # Connect fine leaves/decor attached within ~8px, but never the halo cloud.
    region=cv2.dilate(main,np.ones((9,9),np.uint8),iterations=1)
    dist=cv2.distanceTransform(1-main,cv2.DIST_L2,3)
    # Contaminant red splashes outside edges get clear alpha; near-edge pixels
    # get a soft antialias while the inside paint is left exactly unchanged.
    red_outside=hot_red&(dist>1.8)
    alpha[red_outside]=0
    alpha[region==0]=0
    # Feather edge no more than 2px, preserve detail within main area.
    edge=(region>0)&(main==0)
    alpha[edge]=(alpha[edge].astype(np.float32)*.70).astype(np.uint8)
    a[:,:,3]=alpha
    a[alpha<12]=0
    return a

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    all_rows=[]; atlas=Image.new('RGBA',(4*SIZE,3*SIZE))
    for row,kind in enumerate(CATEGORIES):
        source=SRC/(kind+'.png'); assert source.is_file(),source
        original=Image.open(source).convert('RGBA')
        assert original.size == (1254,1254)
        pixels=np.asarray(original)
        faces=[]
        for face in range(4):
            r,c=divmod(face,2)
            raw=clean_quad(pixels[r*627:(r+1)*627,c*627:(c+1)*627])
            cut=Image.fromarray(raw,'RGBA');box=cut.getchannel('A').getbbox()
            if box is None: raise AssertionError(f'empty {kind} {face}')
            cut=cut.crop(box)
            # Consistent ground pivot, modest art scale; no interpolation of pose.
            scale=min(534/cut.width,548/cut.height,1.2)
            w,h=round(cut.width*scale),round(cut.height*scale)
            if w<280 or h<320:raise AssertionError('subject cropped too far')
            cut=cut.resize((w,h),Image.Resampling.LANCZOS)
            cell=Image.new('RGBA',(SIZE,SIZE))
            x=(SIZE-w)//2;y=611-h
            if min(x,y)<8:raise AssertionError(f'bad fit {kind} {face}: {x},{y}')
            cell.alpha_composite(cut,(x,y))
            atlas.alpha_composite(cell,(face*SIZE,row*SIZE))
            pn=OUT/f'r11_{kind}_{face}.png';wn=WEBP/f'r11_{kind}_{face}.webp'
            cell.save(pn,optimize=True)
            cell.save(wn,format='WEBP',lossless=True,method=5)
            faces.append({'angle':face*90,'source_quadrant':[r,c],
                'crop_box':box,'target_box':cell.getchannel('A').getbbox(),
                'png_sha256':sha(pn.read_bytes()),'webp_sha256':sha(wn.read_bytes()),
                'colors_unique':len(cell.getcolors(640*640) or []),
                'opaque_pixels':int((np.asarray(cell)[:,:,3]>190).sum())})
        all_rows.append({'building':kind,'source_file':source.name,
          'source_sha256':sha(source.read_bytes()),'faces':faces})
    atlas_path=OUT/'R11_PAINTED_ATLAS_3x4.png';atlas.save(atlas_path,optimize=True)
    manifest={
      'schema':'mmai.r11.paint-preflight.v1','status':'CANDIDATE_NOT_APPROVED',
      'source':'Newly generated original four-perspective sheets, conversation 2026-11-15',
      'paintings':12,'author_art_ack':False,'rights_review_complete':False,
      'no_fabricated_rotations_or_mirrors':True,'cell_size':[SIZE,SIZE],
      'atlas_file':atlas_path.name,'atlas_sha256':sha(atlas_path.read_bytes()),
      'buildings':all_rows}
    (OUT/'R11_SOURCE_AND_CUTOUT_RECEIPT.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    return manifest

if __name__=='__main__':
    m=build();print(json.dumps({'images':m['paintings'],'atlas_sha256':m['atlas_sha256'],'faces_by_building':{v['building']:len(v['faces']) for v in m['buildings']}}))
