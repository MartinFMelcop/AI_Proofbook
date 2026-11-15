"""Full composed R05 source archive, no files overwritten on remote sources."""
from pathlib import Path
import json,hashlib,zipfile,os
ROOT=Path(__file__).resolve().parents[1]
TARGET=Path('/mnt/data/MMAI_PRODUCT_V1_20261115_R05.zip')
for i in range(4):
 old=ROOT/'artifacts'/f'R05_SKIA_VIEW_{i}.png'
 if old.exists(): old.unlink() # pre-review duplicate of internal geometry, now explicitly named GEOMETRY
ignore={'R05_PACKAGE_MANIFEST.json','R05_PACKAGING_RECEIPT.json'}
files=sorted((p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.pyo') and p.name not in ignore),key=lambda p:str(p.relative_to(ROOT)))
manifest={'schema':'mmai.product.v1.r05.integrity.v1','base':'R04 full snapshot, independently preserved','base_drive_id':'1tU1Tk6g7JshWv5IGlUdLx7-gTf0f-zif','state':'PRODUCT_NO_GO','art':'ART_REVIEW_PENDING','files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(ROOT/'R05_PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
files.append(ROOT/'R05_PACKAGE_MANIFEST.json')
assert not TARGET.exists(),f'R05 ZIP already exists; refuse overwrite {TARGET}'
with zipfile.ZipFile(TARGET,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(TARGET) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(files)
 for p in files:
  rel=p.relative_to(ROOT).as_posix()
  assert hashlib.sha256(z.read(rel)).digest()==hashlib.sha256(p.read_bytes()).digest(),rel
sha=hashlib.sha256(TARGET.read_bytes()).hexdigest()
result={'schema':'mmai.r05.packaging.receipt.v1','zip':TARGET.name,'bytes':TARGET.stat().st_size,'sha256':sha,'members':len(files),'verification':'ZIP_CRC_AND_EACH_MEMBER_SHA256_PASS','remote_binary_readback':'NOT_PERFORMED','author_art':'NOT_APPROVED'}
(ROOT/'artifacts/R05_PACKAGING_RECEIPT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result,ensure_ascii=False))
