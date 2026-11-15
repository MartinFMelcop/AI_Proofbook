"""Deterministic full composed R02 ZIP; verify each entry before reporting success.
R01 and older artefacts are preserved within the one R02 source snapshot.
"""
from pathlib import Path
import zipfile,hashlib,os,json
ROOT=Path(__file__).resolve().parent.parent
ZIP=ROOT.parent/'MMAI_PRODUCT_V1_20261115_R02.zip'
FILES=sorted(f for f in ROOT.rglob('*') if f.is_file() and f.name!='SHA256SUMS' and '__pycache__' not in f.parts and not f.name.endswith('.pyc'))
assert not ZIP.exists(),'The package is already present; do not overwrite without explicit version change'
lines=[f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(ROOT).as_posix()}' for f in FILES]
(ROOT/'SHA256SUMS').write_text('\n'.join(lines)+'\n',encoding='utf-8')
FILES.append(ROOT/'SHA256SUMS')
with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED,compresslevel=7,strict_timestamps=True) as z:
 for file in sorted(FILES):
  info=zipfile.ZipInfo('MMAI_PRODUCT_V1_20261115_R02/'+file.relative_to(ROOT).as_posix(),date_time=(2026,11,15,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
  z.writestr(info,file.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=7)
with zipfile.ZipFile(ZIP) as z:
 assert z.testzip() is None
 inside={i.filename.removeprefix('MMAI_PRODUCT_V1_20261115_R02/'):i for i in z.infolist()}
 for line in lines:
  digest,rel=line.split('  ',1)
  assert hashlib.sha256(z.read(inside[rel])).hexdigest()==digest,rel
 assert len(z.namelist())==len(FILES)
print(json.dumps({'path':str(ZIP),'bytes':ZIP.stat().st_size,'sha256':hashlib.sha256(ZIP.read_bytes()).hexdigest(),'members':len(FILES),'verification':'CRC+SHA256_PER_ENTRY_PASS','gate':'PRODUCT_NO_GO'}))
