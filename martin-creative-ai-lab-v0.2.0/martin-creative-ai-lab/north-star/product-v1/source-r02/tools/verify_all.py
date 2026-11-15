#!/usr/bin/env python3
"""Collect reproducible, narrowly scoped engineering verification for PRODUCT V1 R01.
No browser bypass, no Windows claim, no artistic judgment.
"""
import hashlib,json,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def run(command):
 p=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
 if p.returncode!=0:raise RuntimeError(f'{command}:\n{p.stdout}\n{p.stderr}')
 return p.stdout.strip(),p.stderr.strip()

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
 result={'schema':'mmai.product.r01.verification.v1','stage':'INTERNAL_PREPRODUCTION','product_gate':'PRODUCT_NO_GO',
 'art_gate':'ART_REVIEW_PENDING','platform':'Linux executor; Windows NOT_RUN', 'checks':{}}
 out,err=run(['sh','tools/build.sh']);result['checks']['CXX20_and_wasm32_build']={'status':'PASS','note':'g++ and clang++ compile with -Werror; not Windows'}
 out,err=run([sys.executable,'-m','unittest','discover','-s','tests','-p','test_*.py','-q'])
 m=re.search(r'Ran (\d+) tests?',err);n=int(m.group(1)) if m else None
 result['checks']['Python_native_structure_SQLite']={'status':'PASS' if n==60 else 'CHECK','count':n,'note':'One-time examples and negative regressions; not 60 independent systems'}
 if n!=60:raise RuntimeError('Unexpected Python count: '+repr(n))
 out,err=run([sys.executable,'tests/generate_world_trace.py']);result['checks']['Native_100_accepted_intents']={'status':'PASS',**json.loads(out)}
 for label,script in [('Legacy_WASM','tests/test_wasm.mjs'),('Native_WASM_parity','tests/test_world_wasm.mjs'),('Canvas_WASM_simulated','tests/test_world_ui.mjs'),('Camera_4_quarters','tests/test_camera.mjs')]:
  out,err=run(['node',script]);result['checks'][label]={'status':'PASS',**json.loads(out)}
 out,err=run([sys.executable,'tools/spatial_journal_sqlite.py','verify','artifacts/world_lab_fixture.sqlite']);result['checks']['SQLite_hashed_journal']={'status':'PASS',**json.loads(out)}
 out,err=run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1','site/assets/opening_animatic.mp4']);duration=float(out)
 result['checks']['opening_animatic_seconds']={'status':'PASS' if 17.7<duration<18.4 else 'FAIL','seconds':duration,'note':'duration only, not final animation/art acceptance'}
 if result['checks']['opening_animatic_seconds']['status']!='PASS':raise RuntimeError('video duration wrong')
 from PIL import Image
 assets=list((ROOT/'site/assets/world').glob('*.webp'))
 assert len(assets)==10
 for asset in assets:
  with Image.open(asset) as im:im.verify()
 result['checks']['world_image_decode']={'status':'PASS','count':len(assets),'approval':'ART_REVIEW_PENDING'}
 result['checks']['Chromium_browser']={'status':'NOT_RUN','note':'Previously ERR_BLOCKED_BY_ADMINISTRATOR; no bypass attempted'}
 result['checks']['Windows_native']={'status':'NOT_RUN','note':'cross-compiler and Windows executor unavailable'}
 result['checks']['Human_art_and_beings_quality']={'status':'PENDING_AUTHOR','note':'no inference from code checks'}
 result['sha256']={str(f):digest(ROOT/f) for f in ['core/world.cpp','core/world.h','site/product.wasm','artifacts/libns_world.so','artifacts/WORLD_NATIVE_TRACE.json','artifacts/world_lab_fixture.sqlite','site/assets/opening_animatic.mp4']}
 (ROOT/'artifacts/R01_TEST_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 print(json.dumps({'python_tests':n,'spatial_trace_actions':100,'world_image_assets':len(assets),'opening_seconds':duration,'product_gate':result['product_gate'],'report':'artifacts/R01_TEST_REPORT.json'}))
if __name__=='__main__':main()
