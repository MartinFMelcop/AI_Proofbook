#!/usr/bin/env python3
"""Versioned full R06 snapshot. Preserves the pre-existing R05 source members."""
from pathlib import Path
import hashlib,json,zipfile,os
ROOT=Path(__file__).resolve().parents[1]
OUT=Path('/mnt/data/MMAI_PRODUCT_V1_20261115_R06.zip')
EXCLUDE={'R06_PACKAGE_MANIFEST.json','R06_SHA256SUMS'}

def paths():return sorted((p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'),key=lambda p:p.relative_to(ROOT).as_posix())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
original=json.loads((ROOT/'R05_PACKAGE_MANIFEST.json').read_text())['files']
for n in ['core/world_r05.cpp','core/world_r05.h','site/assets/world/r04_cottage.webp','site/assets/world/r04_forge.webp','site/assets/world/r04_apothecary.webp','site/assets/opening_animatic.mp4']:
 assert digest(ROOT/n)==original[n],n
names=[p.relative_to(ROOT).as_posix() for p in paths() if p.relative_to(ROOT).as_posix() not in EXCLUDE]
hashes={name:digest(ROOT/name) for name in names}
manifest={'schema':'mmai.product.v1.r06.full-snapshot.manifest.v1','base':'R05 full snapshot, original R00-R05 files preserved','base_drive_id':'1nbRdNSH8vOQiWFfMEm5ZLDLi-v08wFmd','product_state':'PRODUCT_NO_GO','art_state':'ART_REVIEW_PENDING','note':'R06 generated new motion frames and Skia receipts; not a canon game, art or native Windows build','files':hashes}
(ROOT/'R06_PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
(ROOT/'R06_SHA256SUMS').write_text(''.join(f'{val}  {name}\n' for name,val in sorted(hashes.items())))
# consistent zip ordering, timestamps and mode; no files changed after manifest.
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for p in paths():
  rel=p.relative_to(ROOT).as_posix();info=zipfile.ZipInfo(rel,date_time=(2026,11,15,7,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED
  info.external_attr=(0o100644)<<16
  z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 for name,val in hashes.items():
  assert hashlib.sha256(z.read(name)).hexdigest()==val,name
 assert len(set(z.namelist()))==len(z.namelist())
 assert len(z.namelist())==len(hashes)+2
print(json.dumps({'zip':str(OUT),'bytes':OUT.stat().st_size,'files':len(hashes)+2,'zip_sha256':digest(OUT),'member_sha256_all':'MATCH','crc':'PASS','state':'PRODUCT_NO_GO'}))
