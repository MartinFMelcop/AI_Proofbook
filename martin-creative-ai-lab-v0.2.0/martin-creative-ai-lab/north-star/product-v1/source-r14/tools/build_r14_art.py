#!/usr/bin/env python3
"""R14: cut ORIGINAL generated sprite sheets, remove dark matte, preserve source+provenance.
    LAB ART CANDIDATE; does not approve painting, rights, 4-view architectural consistency or gameplay.
"""
from pathlib import Path
import numpy as np, cv2, json, hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site/assets/world'; OUT.mkdir(parents=True,exist_ok=True)
SOURCES=ROOT/'art_sources/r14_original_sheets'; SOURCES.mkdir(parents=True,exist_ok=True)
INPUT=SOURCES  # The eight original ImageGen sheets are preserved with the R14 art package.
SHEETS={
 'cottage':('chalé_medieval_sombrio_em_quatro_vistas_isométrica.png',2,640),
 'forge':('forja_medieval_em_quatro_ângulos_isométricos.png',2,640),
 'apothecary':('folha_de_ativos_da_botica_encantada.png',2,640),
 'hero':('herói_aventureiro_em_ciclo_de_caminhada.png',4,320),
 'guard_npc':('guarda_da_estrela_do_norte_em_movimento.png',4,320),
 'ruinguard':('vigia_das_ruínas_ciclo_de_ataque.png',4,420),
 'wraith':('folha_de_sprites_do_sussurro_do_brejo.png',4,420),
 'guardian_tree':('árvore_guardiã_folha_de_animação.png',4,420)
}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assets={}; stats={}; names=[]

def matte_remove(tile):
    rgb=np.asarray(tile.convert('RGB'),np.uint8)
    h,w=rgb.shape[:2]
    c=24
    # All generated sheets share an explicit, dark navy neutral background.
    corners=np.concatenate([rgb[:c,:c].reshape(-1,3),rgb[:c,-c:].reshape(-1,3),rgb[-c:,:c].reshape(-1,3),rgb[-c:,-c:].reshape(-1,3)],axis=0)
    bg=np.median(corners.astype(np.float32),axis=0)
    dist=np.sqrt(np.sum((rgb.astype(np.float32)-bg)**2,axis=2))
    sure=(dist>24).astype('uint8')
    sure=cv2.morphologyEx(sure,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    n,lab,stat,cent=cv2.connectedComponentsWithStats(sure,8)
    min_area=100 if h>500 else 32
    keep=np.zeros((h,w),np.uint8)
    for i in range(1,n):
        area=stat[i,cv2.CC_STAT_AREA]
        if area>=min_area: keep[lab==i]=255
    keep=cv2.dilate(keep,np.ones((5,5),np.uint8),iterations=1)
    soft=np.clip((dist-8)/30,0,1)*255
    soft=cv2.GaussianBlur(soft,(3,3),0.65)
    alpha=np.uint8(np.clip(soft,0,255))* (keep>0).astype(np.uint8)
    rgba=np.dstack((rgb,alpha))
    return Image.fromarray(rgba,'RGBA'),float((alpha>0).mean()),bg.tolist()

for key,(fn,grid,size) in SHEETS.items():
    src=INPUT/fn
    if not src.is_file():raise RuntimeError(f'MISSING_AUTHORED_GENERATION: {src}')
    original=Image.open(src).convert('RGB')
    # Original sources are immutable once archived; never modify the user-supplied/generated sheet bytes.
    w,h=original.size
    records=[]
    for row in range(grid):
        for col in range(grid):
            crop=original.crop((round(col*w/grid),round(row*h/grid),round((col+1)*w/grid),round((row+1)*h/grid)))
            img,opacity,bg=matte_remove(crop)
            if not 0.04<opacity<0.78:raise AssertionError(f'ALPHA_SEGMENTATION_SUSPECT {key}_{row}_{col} occupancy {opacity:.2f}')
            region=img.getchannel('A').getbbox()
            if region is None:raise AssertionError('EMPTY_SPRITE')
            trim=img.crop(region)
            # Fixed transparent square with floor anchor; never change actual internal pixels/morphology.
            canvas=Image.new('RGBA',(size,size),(0,0,0,0))
            maxwidth=size-30;maxheight=size-32
            ratio=min(maxwidth/trim.width,maxheight/trim.height,1.6)
            dest=(max(1,round(trim.width*ratio)),max(1,round(trim.height*ratio)))
            trim=trim.resize(dest,Image.Resampling.LANCZOS)
            canvas.alpha_composite(trim,((size-dest[0])//2,size-15-dest[1]))
            asset=f'r14_{key}_{row}_{col}'
            output=OUT/(asset+'.webp')
            canvas.save(output,'WEBP',quality=84,method=1)
            if not Image.open(output).getbands()==('R','G','B','A'):raise AssertionError('WEBP_NO_ALPHA')
            record={'name':asset,'source':fn,'row':row,'col':col,'source_sha256':sha(src),'webp_sha256':sha(output),'alpha_occupancy':round(opacity,4),'trim_bbox':list(region),'dims':[size,size],'rights':'ART_CANDIDATE_RIGHTS_REVIEW_PENDING'}
            records.append(record);names.append(asset)
    assets[key]=records
    stats[key]={'input':fn,'grid':grid,'frames':len(records),'source_sha256':sha(src),'asset_sha_unique':len({v['webp_sha256'] for v in records})==len(records)}
    assert stats[key]['asset_sha_unique']
report={'schema':'mmai.r14.original_generated_art_intake.v1','result':'PRODUCED_UNAPPROVED',
        'status':'ART_REVIEW_PENDING / PRODUCT_NO_GO','source_sheets':len(SHEETS),'sprites_created':len(names),
        'sheet_stats':stats,'assets':assets,'notes':['Crops are from genuinely generated authored-image sheets, not turned or recolored copies of one angle.',
        'Foreground alpha is automatic background subtraction; may eat dark edges and needs visual review.',
        'Distinct SHA/frame does not prove perspective continuity or full animation cycle.',
        'Neither world state nor C++ ABI5 are modified by this script.']}
(ROOT/'artifacts/R14_ART_RECEIPT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_sheets':len(SHEETS),'sprites':len(names),'all_unique_per_sheet':all(v['asset_sha_unique'] for v in stats.values()),'keys':list(stats)},ensure_ascii=False))
