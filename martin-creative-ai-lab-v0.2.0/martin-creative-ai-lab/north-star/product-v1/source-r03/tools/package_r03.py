"""One full non-destructive R03 source package, with independent SHA256 receipts.
No code execution other than packaging. No environment-dependent paths in the ZIP.
"""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
DST=Path('/mnt/data/MMAI_PRODUCT_V1_20261115_R03.zip')
assert ROOT.exists()
EXCLUDE={'__pycache__','.pytest_cache','.DS_Store','SHA256SUMS'}
files=sorted([p for p in ROOT.rglob('*') if p.is_file() and not any(x in EXCLUDE or x.endswith('.pyc') for x in p.relative_to(ROOT).parts)],key=lambda p:p.relative_to(ROOT).as_posix())
lines=[]
for p in files:
 name=p.relative_to(ROOT).as_posix()
 lines.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+name)
(ROOT/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
files.append(ROOT/'SHA256SUMS')
files.sort(key=lambda p:p.relative_to(ROOT).as_posix())
if DST.exists():raise FileExistsError('Refusing implicit overwrite: '+str(DST))
with ZipFile(DST,'w',compression=ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:
  name='MMAI_PRODUCT_V1_R03/'+p.relative_to(ROOT).as_posix()
  info=ZipInfo(filename=name,date_time=(2026,11,15,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o644<<16
  z.writestr(info,p.read_bytes(),compress_type=ZIP_DEFLATED,compresslevel=6)
with ZipFile(DST) as z:
 bad=z.testzip();assert bad is None,bad
 paths=z.namelist()
 for line in (ROOT/'SHA256SUMS').read_text().splitlines():
  h,name=line.split('  ',1)
  assert hashlib.sha256(z.read('MMAI_PRODUCT_V1_R03/'+name)).hexdigest()==h,name
 result={'zip':str(DST),'bytes':DST.stat().st_size,'members':len(paths),'SHA256':hashlib.sha256(DST.read_bytes()).hexdigest(),'crc':'PASS','per_entry_sha':'PASS','gate':'PRODUCT_NO_GO'}
 print(json.dumps(result))
