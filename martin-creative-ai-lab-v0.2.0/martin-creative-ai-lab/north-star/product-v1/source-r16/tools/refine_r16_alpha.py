#!/usr/bin/env python3
"""R16 conservation-first fringe cleanup of R14 source-derived sprites.

Produces r16_*.webp beside unchanged r14_*.webp. This changes edge pixels,
not painted architecture, rigging, gameplay state, or the authorial status.
"""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'site/assets/world'
MANIFEST = ROOT / 'artifacts/R16_ALPHA_REFINEMENT_MANIFEST.json'
sha = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
results=[]
for source in sorted(ART.glob('r14_*.webp')):
    before=sha(source)
    with Image.open(source) as original: im=original.convert('RGBA')
    x=np.asarray(im, dtype=np.uint8).copy()
    alpha=x[:,:,3].astype(np.float32)
    solid=alpha>=220
    if solid.any():
        dist, indices=distance_transform_edt(~solid, return_indices=True)
        nearest=x[indices[0],indices[1],:3].astype(np.float32)
        sel=(alpha>=12)&(alpha<220)&(dist<=4.0)
        # A conservative edge-only matte correction. Use adjacent fully-painted
        # pixels; never reimagine doors, faces, silhouettes or interiors.
        blend=np.where(sel, 0.32*(1.0-alpha/255.0),0).astype(np.float32)
        rgb=x[:,:,:3].astype(np.float32)
        rgb=rgb*(1-blend[:,:,None])+nearest*blend[:,:,None]
        x[:,:,:3]=np.clip(np.rint(rgb),0,255).astype(np.uint8)
    # Suppress only very faint compression residue, without eroding the shape.
    faint=alpha<=4
    x[:,:,3][faint]=0
    x[:,:,:3][faint]=0
    # Keep alpha >=5 untouched, because painted sparks, smoke and magic are art.
    after_im=Image.fromarray(x,'RGBA')
    out=ART/source.name.replace('r14_','r16_',1)
    after_im.save(out,'WEBP',lossless=True,method=0)
    reread=np.asarray(Image.open(out).convert('RGBA'))
    # Conservation bounds: the important painted core stays opaque and a
    # major part of the original subject cannot disappear accidentally.
    orig=np.asarray(im)
    preserved_core=(reread[:,:,3][orig[:,:,3]>=220]>=215).mean()
    assert preserved_core>0.99, (source.name, preserved_core)
    assert reread.shape==orig.shape
    alpha_major_flip=((orig[:,:,3]>=128)!=(reread[:,:,3]>=128)).mean()
    assert alpha_major_flip<0.012,(source.name,alpha_major_flip)
    changed=np.any(orig!=reread,axis=2)
    count=int(changed.sum())
    assert count>0,(source.name,'refinement no effect')
    assert sha(source)==before
    results.append({'asset':source.name,'derived':out.name,'source_sha256':before,'derived_sha256':sha(out),
      'pixels_changed':count,'changed_pct':round(float(changed.mean()*100),4),
      'alpha_major_flip_pct':round(float(alpha_major_flip*100),5),'core_alpha_retention':round(float(preserved_core),6),
      'size':list(im.size),'bytes':out.stat().st_size})
assert len(results)==92,len(results)
report={'schema':'mmai.r16.conservative_painted_edge_cleanup.v1','status':'ART_CANDIDATE_NOT_APPROVED',
        'source_originals_preserved':92,'derived_sprites':92,
        'visual_method':'nearest opaque local RGB edge decontamination + alpha<=4 compression-residue removal',
        'does_not':'repaint roofs/doors/chimneys, certify rights, certify original rig or canon',
        'stats':{'min_changed_pct':min(r['changed_pct'] for r in results),
                 'max_changed_pct':max(r['changed_pct'] for r in results),
                 'total_changed_pixels':sum(r['pixels_changed'] for r in results)},
        'assets':results}
MANIFEST.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'PASS':True,'sprites':len(results),**report['stats'],'manifest':str(MANIFEST)}))
