#!/usr/bin/env python3
"""R16 post-run evidence: physically changed painted edges, C++ owner unchanged.
Prerequisites: independently completed R16 Skia runners and verify_r12.py.
This script performs no inference about artistic approval or visual satisfaction.
"""
from pathlib import Path
from PIL import Image, ImageChops
import numpy as np
import hashlib, json, subprocess, os, sys
R=Path(__file__).resolve().parents[1]
B=Path(os.environ.get('MMAI_R15_BASELINE_PATH','/mnt/data/MMAI_PRODUCT_V1_R15_WORK'))
A=R/'artifacts'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
asset_dir=R/'site/assets/world'
manifest=json.loads((A/'R16_ALPHA_REFINEMENT_MANIFEST.json').read_text())
assert len(manifest['assets'])==92
frozen={}
for item in manifest['assets']:
 name=item['asset'];src=asset_dir/name;old=B/'site/assets/world'/name;dst=asset_dir/item['derived']
 assert src.is_file() and old.is_file() and dst.is_file()
 assert sha(src)==sha(old)==item['source_sha256']
 assert sha(dst)==item['derived_sha256'] and sha(dst)!=sha(old)
 with Image.open(dst) as im:
  assert im.mode in ('RGB','RGBA') and list(im.size)==item['size']
 frozen[name]=True
for f in [*sorted((R/'art_sources/r14_original_sheets').glob('*.png')),
          *[R/p for p in ['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/camera4.js',
                           'site/r15_presentation.js','site/r14_art.js','site/assets/opening_animatic.mp4',
                           'artifacts/R05_SQLITE_WORLD_JOURNAL.sqlite']]]:
 relative=f.relative_to(R)
 assert sha(f)==sha(B/relative),str(relative)
 frozen[str(relative)]=True
assert len(frozen)==108,len(frozen)

# Existing native verification output is a completed and checked R16 command;
# never call a timeout or an unexecuted suite PASS.
native_log=A/'R16_NATIVE_REGRESSION.log'
boss_log=A/'R16_BOSS_TRACE.log'
needs_images=not all((A/f'R16_SCENE_VIEW_{i}.png').exists() and (A/f'R16_FALLBACK_VIEW_{i}.png').exists() and (A/f'R16_ACTOR_MOTION_FRAME_{i}.png').exists() for i in range(4)) or not all((A/f'R16_BOSS_{b}_STAGE_{i}.png').exists() for b in range(1,4) for i in range(4))
if '--rerun' in sys.argv or not native_log.exists():
    n=subprocess.run(['python3','tools/verify_r12.py'],cwd=R,capture_output=True,text=True,check=True)
    native_log.write_text(n.stdout+'\n')
if '--rerun' in sys.argv or needs_images or not boss_log.exists():
    for script,log in [('render_r16_fourview_skia.mjs','R16_RENDER_FOUR.log'),
                       ('render_r16_fallback_skia.mjs','R16_RENDER_FALLBACK.log'),
                       ('render_r16_boss_phase_skia.mjs','R16_BOSS_TRACE.log'),
                       ('render_r16_actor_motion_skia.mjs','R16_RENDER_ACTOR.log')]:
        r=subprocess.run(['node','tests/'+script],cwd=R,capture_output=True,text=True,check=True)
        (A/log).write_text(r.stdout+'\n')
reg=json.loads(native_log.read_text().splitlines()[-1])
assert reg['PASS'] and reg['python']==257
assert reg['actions']=={'R05':121,'R04':121,'R03':121,'R02':116,'R01':100}
checks={}
for tag,filename,n in [('R07','test_r07_facade_contract.mjs',44),('R12','test_r12_visual_contract.mjs',67),
                       ('R13','test_r13_stagecraft.mjs',26),('R14','test_r14_art_contract.mjs',191),
                       ('R15','test_r15_owner_visual_phase.mjs',363),('R16','test_r16_art_contract.mjs',292)]:
 p=subprocess.run(['node','tests/'+filename],cwd=R,capture_output=True,text=True,timeout=25,check=True)
 j=json.loads(p.stdout.strip().splitlines()[-1]);assert j['PASS'] and j['checks']==n
 checks[tag]=n
assert sum(checks.values())==983
boss=json.loads(boss_log.read_text().strip().splitlines()[-1])
assert boss['PASS'] and len(boss['scenes'])==12
for b in (1,2,3):
 events=[x for x in boss['scenes'] if x['boss']==b]
 assert [x['owner_intent'] for x in events]==[1,1,2,2]
 assert [x['visual_frame'] for x in events]==[0,1,2,3]
 assert all(x['unchanged_owner'] for x in events)
 assert events[2]['revision']>events[1]['revision']

visual=json.loads((A/'R16_VISUAL_COMPARE_R15.json').read_text())
assert all(visual['fallback_exact'].values())
# Re-inspect images rather than accepting JSON at face value.
for i in range(4):
 dst=Image.open(A/f'R16_FALLBACK_VIEW_{i}.png').convert('RGBA')
 old=Image.open(B/f'artifacts/R15_FALLBACK_VIEW_{i}.png').convert('RGBA')
 assert ImageChops.difference(dst,old).getbbox() is None
 src=np.asarray(Image.open(A/f'R16_SCENE_VIEW_{i}.png').convert('RGB'),np.int16)
 prev=np.asarray(Image.open(B/f'artifacts/R15_SCENE_VIEW_{i}.png').convert('RGB'),np.int16)
 assert src.shape==prev.shape==(760,1200,3)
 delta=(np.abs(src-prev).mean(axis=2)>18).mean()*100
 assert abs(delta-visual['world_scene_pixel_changes_not_quality_score'][str(i*90)]['pixel_gt18_pct'])<0.0002
for b in range(1,4):
 for i in range(4):
  with Image.open(A/f'R16_BOSS_{b}_STAGE_{i}.png') as im: assert im.size==(1200,760)
for i in range(4):
 with Image.open(A/f'R16_ACTOR_MOTION_FRAME_{i}.png') as im: assert im.size==(1200,760)
report={
 'schema':'mmai.product_v1.r16.art_edge_derivatives_and_real_gameplay_qa.v1',
 'gate':'PRODUCT_NO_GO','art_gate':'ART_REVIEW_PENDING','release':False,
 'image_generation':'FAILED_DO_NOT_RETRY_UNTIL_NEW_REQUEST',
 'new_original_paintings':0,'new_derived_painted_edge_assets':92,
 'original_92_R14_webp_unchanged':True,'eight_R14_source_sheets_unchanged':True,
 'other_frozen_authority_and_opening_files':8,'all_frozen_sha_matches':len(frozen),
 'cleaning':'conservative RGB edge decontamination plus removal of alpha<=4 residue; no semantic repaints',
 'physical_modified_pixel_count_in_derived_assets':manifest['stats']['total_changed_pixels'],
 'alpha_core_conservation':'each source retained >=99% alpha>=215 where originally >=220',
 'contract_node_check_totals':checks,'contract_node_total':sum(checks.values()),
 'native_cpp20_wasm_current_and_historic_actions':reg['actions'],
 'python_tests':257,'C17_and_SQLite':'PASS_AS_IN_COMPLETED_VERIFY_R12_LOG',
 'skia_actual_gameplay_frames':24,'four_camera_rotations':[0,90,180,270],
 'three_boss_native_accepted_defend_sequences':3,
 'stage_mapping':{'CXX_intent_1':[0,1],'CXX_intent_2_post_adjudication':[2,3]},
 'fallback_default_identical':visual['fallback_exact'],
 'world_pixel_change_from_R15_not_beauty_score':visual['world_scene_pixel_changes_not_quality_score'],
 'browser_windows_GPU':'NOT_RUN',
 'artistic_limits':['No new roof/door/chimney paintings','No new skeletal rigs',
    'Small in-scene pixel difference does not imply major art progress',
    'Rights, painterly coherence, the 21 kits and boss canon require human adjudication'],
 'publisher_note':'R16 consists of additive derivative assets and QA; never overwrite R14 originals or merge to main without author approval.'}
(A/'R16_TEST_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'PASS':True,'derived':92,'immutable':len(frozen),'node':sum(checks.values()),
 'python':reg['python'],'actions':reg['actions'],'skia':24,
 'frozen_default':all(visual['fallback_exact'].values()),
 'changed_pct_range':[min(x['pixel_gt18_pct'] for x in visual['world_scene_pixel_changes_not_quality_score'].values()),max(x['pixel_gt18_pct'] for x in visual['world_scene_pixel_changes_not_quality_score'].values())],
 'product':'PRODUCT_NO_GO'}))
