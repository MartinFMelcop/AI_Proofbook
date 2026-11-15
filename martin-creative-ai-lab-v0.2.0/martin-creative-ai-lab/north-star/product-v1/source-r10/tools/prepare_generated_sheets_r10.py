#!/usr/bin/env python3
"""Convert three original 2x2 AI-generated sheets to one 3x4 candidate atlas.

Uses neither rotations nor reflections to fabricate sides. Order is supplied
by the original top-left/top-right/bottom-left/bottom-right arrangement.
This only PREPARES candidate art, never approves visual quality or copyright.
"""
from pathlib import Path
from hashlib import sha256
from PIL import Image, ImageFilter
import cv2
import numpy as np
import json

ROOT=Path(__file__).resolve().parents[1]
SOURCES=[('cottage',ROOT/'art_sources/cottage_source.png'),('forge',ROOT/'art_sources/forge_source.png'),('apothecary',ROOT/'art_sources/apothecary_source.png')]
OUT=ROOT/'art_sources/R10_SOURCE_ATLAS_3x4.png'
TILE=640

def main():
    atlas=Image.new('RGBA',(4*TILE,3*TILE),(0,0,0,0))
    data={'schema':'mmai.r10.generated-art-preflight.v1','state':'ART_CANDIDATE_UNREVIEWED',
          'artwork_generated_in_this_conversation':True,'source_approval':'PENDING_AUTHOR',
          'image_generation_provenance':'OpenAI image generation in user conversation 2026-11-15',
          'rights_independently_verified':False,'buildings':{},'no_rotated_or_mirrored_views':True}
    for row,(name,src) in enumerate(SOURCES):
        original=Image.open(src).convert('RGBA')
        if original.size!=(1254,1254):raise ValueError('unexpected source dimensions: '+str(src))
        a=np.array(original)
        faces=[]
        for face in range(4):
            r,c=divmod(face,2)
            square=a[r*627:(r+1)*627,c*627:(c+1)*627].copy()
            # Keep the largest coherent painted object; discard isolated image-gen halo specks.
            mask=(square[:,:,3]>118).astype(np.uint8)
            num,labels,stats,_=cv2.connectedComponentsWithStats(mask,8)
            if num<2:raise ValueError(f'{name} face{face}: no painted component')
            label=1+int(np.argmax(stats[1:,cv2.CC_STAT_AREA]))
            body=(labels==label).astype(np.uint8)*255
            body=cv2.morphologyEx(body,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
            # Antialias cutout: image alpha remains source-derived, without invented pixels.
            feather=cv2.GaussianBlur(body,(3,3),.7).astype(np.float32)/255.0
            square[:,:,3]=np.clip(square[:,:,3].astype(np.float32)*feather,0,255).astype(np.uint8)
            square[square[:,:,3]<10,:]=0
            raw=Image.fromarray(square,'RGBA')
            bbox=raw.getchannel('A').getbbox()
            if not bbox:raise ValueError(f'{name} face{face}: empty after cleanup')
            cut=raw.crop(bbox)
            scale=min(538/cut.width,548/cut.height,1.15)
            output=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
            cell=Image.new('RGBA',(TILE,TILE),(0,0,0,0))
            x=(TILE-output.width)//2
            y=612-output.height # fixed ground pivot across facades
            if x<10 or y<10:raise ValueError('bad margins')
            cell.alpha_composite(output,(x,y))
            dst=ROOT/'art_sources'/f'R10_{name}_{face}.png'
            cell.save(dst)
            atlas.alpha_composite(cell,(face*TILE,row*TILE))
            faces.append({'angle':face*90,'source_quadrant':[r,c],'source_sha256':sha256(src.read_bytes()).hexdigest(),
                          'cutout_png':dst.name,'png_sha256':sha256(dst.read_bytes()).hexdigest(),
                          'artwork_bbox':list(bbox),'target_bbox':list(cell.getchannel('A').getbbox())})
        data['buildings'][name]={'source_image':src.name,'faces':faces}
    atlas.save(OUT)
    data['atlas']={'path':OUT.name,'size':list(atlas.size),'sha256':sha256(OUT.read_bytes()).hexdigest()}
    (ROOT/'art_sources/R10_SOURCE_RECEIPT.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'atlas':str(OUT),'source_buildings':len(SOURCES),'faces':sum(len(x['faces']) for x in data['buildings'].values()),'sha256':data['atlas']['sha256']}))
if __name__=='__main__':main()
