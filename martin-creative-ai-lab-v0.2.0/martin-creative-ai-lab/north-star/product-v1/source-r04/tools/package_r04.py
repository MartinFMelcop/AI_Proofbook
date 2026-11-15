from pathlib import Path
import zipfile,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'MMAI_PRODUCT_V1_20261115_R04.zip'
def sha(d):return hashlib.sha256(d).hexdigest()
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name not in ['SHA256SUMS','R04_PACKAGE_MANIFEST.json'])
assert len(files)>180
contents={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in files}
report={'schema':'mmai.r04.composed.package.manifest.v1','date':'2026-11-15','product_gate':'PRODUCT_NO_GO','art_gate':'ART_REVIEW_PENDING','source_revision':'R03 Drive 1gV0_gPI9P_7sQ7UWZt4lnKSAF0CYJklB','code':'C++20/C17 ABI4, Python/SQLite, JS Canvas, WASM32','file_count_excluding_manifest':len(contents),'sha256':contents}
(ROOT/'R04_PACKAGE_MANIFEST.json').write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
manifest_sha=sha((ROOT/'R04_PACKAGE_MANIFEST.json').read_bytes());contents['R04_PACKAGE_MANIFEST.json']=manifest_sha
(ROOT/'SHA256SUMS').write_text(''.join(f'{hash}  {name}\n' for name,hash in sorted(contents.items())))
files.extend([ROOT/'R04_PACKAGE_MANIFEST.json',ROOT/'SHA256SUMS'])
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8,allowZip64=True) as z:
 for p in sorted(files,key=lambda f:str(f.relative_to(ROOT))):
  name=str(p.relative_to(ROOT)).replace('\\','/')
  info=zipfile.ZipInfo(name,date_time=(2026,11,15,6,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o644<<16)
  z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=8)
with zipfile.ZipFile(OUT) as z:
 assert z.testzip() is None
 for name,expected in contents.items():assert sha(z.read(name))==expected,name
 assert len(z.namelist())==len(files)
print(json.dumps({'archive':str(OUT),'file_count':len(files),'bytes':OUT.stat().st_size,'sha256':sha(OUT.read_bytes()),'CRC':'PASS','per_file_SHA256':'PASS','product':'PRODUCT_NO_GO'}))
