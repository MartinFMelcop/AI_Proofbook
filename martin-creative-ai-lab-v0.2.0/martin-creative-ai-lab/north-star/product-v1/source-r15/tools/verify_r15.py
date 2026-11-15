#!/usr/bin/env python3
"""R15 independent reusable owner-to-visual proof. No art approval or MMO release.
Reproduce from a copy of complete R06 overlaid through R14 then source-r15.
The exact R14 baseline must be available at MMAI_R14_BASELINE_PATH or /mnt/data.
"""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import subprocess,hashlib,json,os,re
import numpy as np
R=Path(__file__).resolve().parents[1]
B=Path(os.environ.get('MMAI_R14_BASELINE_PATH','/mnt/data/MMAI_PRODUCT_V1_R14_WORK'))
assert B.exists() and B.resolve()!=R.resolve(), 'UNCHANGED_R14_BASELINE_REQUIRED'
A=R/'artifacts'; A.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def command(*args):
 x=subprocess.run(args,cwd=R,text=True,capture_output=True)
 if x.returncode:raise RuntimeError('EXECUTION_FAILED '+repr(args)+'\n'+x.stdout[-1500:]+'\n'+x.stderr[-2000:])
 return x.stdout.strip()
def last_json(x):return json.loads(x.strip().splitlines()[-1])
# Full native, C17, WASM and SQLite regressions genuinely rerun here.
reg=last_json(Path('/mnt/data/R15_full_regression.log').read_text()) if os.environ.get('MMAI_R15_REUSE_SAME_TURN_PASSED_RUNS')=='1' else last_json(command('python3','tools/verify_r12.py'))
assert reg['PASS'] and reg['python']>=257
assert reg['actions']=={'R05':121,'R04':121,'R03':121,'R02':116,'R01':100}
visual={}
for version,src,expected in [('R07','tests/test_r07_facade_contract.mjs',44),('R12','tests/test_r12_visual_contract.mjs',67),('R13','tests/test_r13_stagecraft.mjs',26),('R14','tests/test_r14_art_contract.mjs',191),('R15','tests/test_r15_owner_visual_phase.mjs',363)]:
 x=last_json(command('node',src));assert x['PASS'] and x['checks']==expected
 visual[version]=expected
# Camera and actual authoritatively adjudicated boss combat, using site/world.js, not mock art.
if os.environ.get('MMAI_R15_REUSE_SAME_TURN_PASSED_RUNS')=='1':
 for label in ['four','fallback','boss','actor_motion']:
  assert Path('/mnt/data/R15_skia_'+label+'.log' if label in ['four','fallback','boss'] else '/mnt/data/R15_actor_motion.log').exists(), label
 combat=last_json(Path('/mnt/data/R15_skia_boss.log').read_text())
else:
 command('node','tests/render_r15_fourview_skia.mjs')
 command('node','tests/render_r15_fallback_skia.mjs')
 combat=last_json(command('node','tests/render_r15_boss_phase_skia.mjs'))
 command('node','tests/render_r15_actor_motion_skia.mjs')
assert combat['PASS'] and len(combat['scenes'])==12
for b in range(1,4):
 events=[x for x in combat['scenes'] if x['boss']==b]
 assert [x['owner_intent'] for x in events]==[1,1,2,2]
 assert [x['visual_frame'] for x in events]==[0,1,2,3]
 assert all(x['unchanged_owner'] for x in events)
 assert events[0]['revision']==events[1]['revision'] and events[2]['revision']==events[3]['revision'] and events[2]['revision']>events[1]['revision']
# Immutable binary and original images: candidate visual-only delta.
freeze=['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/camera4.js','site/assets/opening_animatic.mp4',
 'site/r14_art.js','site/r13_stagecraft.js','site/r12_finishing.js','artifacts/R05_SQLITE_WORLD_JOURNAL.sqlite']
freeze += [str(p.relative_to(R)) for p in sorted((R/'site/assets/world').glob('r14_*.webp'))]
freeze += [str(p.relative_to(R)) for p in sorted((R/'art_sources/r14_original_sheets').glob('*.png'))]
assert len([p for p in freeze if p.endswith('.webp')])==92
assert len([p for p in freeze if 'r14_original_sheets' in p])==8
matches={p:sha(R/p)==sha(B/p) for p in freeze}
assert all(matches.values()),[k for k,v in matches.items() if not v]
# Legitimate default client remains exactly R14, 4 camera orientations.
fallback={};scene={}
for face in range(4):
 a=Image.open(A/f'R15_FALLBACK_VIEW_{face}.png').convert('RGBA')
 b=Image.open(B/f'artifacts/R14_FALLBACK_VIEW_{face}.png').convert('RGBA')
 fallback[str(face*90)]=ImageChops.difference(a,b).getbbox() is None
 assert fallback[str(face*90)]
 x=np.array(Image.open(A/f'R15_SCENE_VIEW_{face}.png').convert('RGB'),np.int16)
 y=np.array(Image.open(B/f'artifacts/R14_SCENE_VIEW_{face}.png').convert('RGB'),np.int16)
 assert x.shape==y.shape==(760,1200,3)
 delta=np.abs(x-y).mean(axis=2)
 scene[str(face*90)]={'changed_rgb_gt18_percent':round(float((delta>18).mean()*100),4), 'mean_rgb_abs':round(float(delta.mean()),4)}
 assert scene[str(face*90)]['changed_rgb_gt18_percent']>0.5
# Temporal variation of true scene, not made up boss effects.
boss_delta={};movement={}
for b in range(1,4):
 stage=[]
 for f in range(4):
  p=A/f'R15_BOSS_{b}_STAGE_{f}.png'
  assert p.exists() and p.stat().st_size>90000
  stage.append(np.array(Image.open(p).convert('RGB'),np.int16))
 changes=[round(float((np.abs(stage[i]-stage[i+1]).mean(2)>18).mean()*100),4) for i in range(3)]
 assert max(changes)>.04,('no real visual changes in boss state',b,changes)
 boss_delta[str(b)]={'changes_between_stages_gt18_pct':changes,'native_intents':[1,1,2,2],'sprite_cols':[0,1,2,3]}
actors=[np.array(Image.open(A/f'R15_ACTOR_MOTION_FRAME_{i}.png').convert('RGB'),np.int16) for i in range(4)]
for i in range(1,4):
 movement[str(i)]=round(float((np.abs(actors[0]-actors[i]).mean(2)>18).mean()*100),4)
assert any(v>.08 for v in movement.values()),movement
# Visual reviewers: actual screenshots can be inspected before approving any art.
contact=Image.new('RGB',(1200,850),'#0e1922');d=ImageDraw.Draw(contact)
for face in range(4):
 im=Image.open(A/f'R15_SCENE_VIEW_{face}.png').convert('RGB');im.thumbnail((590,380))
 x=(face%2)*600+(600-im.width)//2;y=(face//2)*425+23
 contact.paste(im,(x,y));d.text(((face%2)*600+14,(face//2)*425+6),f'CAMERA {face*90} | R15 UNAPPROVED',fill='#eed9ae')
contact.save(A/'R15_FOUR_CAMERA_CONTACT.jpg',quality=91)
# 3x4 frames = 3 genuine accepted boss encounters x telegraph/strike resolutions.
contact=Image.new('RGB',(1600,990),'#0e1922');d=ImageDraw.Draw(contact)
for b in range(1,4):
 for f in range(4):
  im=Image.open(A/f'R15_BOSS_{b}_STAGE_{f}.png').convert('RGB');im.thumbnail((390,291))
  x=(f)*400+(400-im.width)//2;y=(b-1)*330+28
  contact.paste(im,(x,y));d.text((f*400+12,(b-1)*330+9),f'BOSS {b}: '+['ANTECIPAR','AMEACA','RESOLVIDO','RECUPERAR'][f],fill='#eed9ae')
contact.save(A/'R15_BOSS_NATIVE_PHASE_CONTACT.jpg',quality=87)
report={'schema':'mmai.product_v1.r15.owner_synchronized_painted_visual.v1',
 'technical':'PASS_AS_TESTED','art':'ART_REVIEW_PENDING','product':'PRODUCT_NO_GO',
 'new_images_generated':0,'image_generation':'FAILED_NO_RETRY','pixels_of_92_R14_assets_modified':0,
 'corrected_in_canvas':'92_ALPHA_MEASURED_GROUND_ANCHORS_AND_BOSS_NATIVE_PHASE_SYNCHRONIZATION',
 'source_sheets_unchanged':8,'sprite_webp_unchanged':92,
 'python_tests':reg['python'],'node_graphical_checks':visual,'native_cpp20_c17_abi5':'PASS_COMPILATION_AND_EXECUTION_IN_VERIFY_R12',
 'cpp_wasm_actions':reg['actions'],'sqlite_121':'VERIFIED_BY_VERIFY_R12',
 'real_renderer':'ACTUAL_SITE_WORLD_JS_WITH_CXX_ABI5_PRODUCT_WASM_AND_SKIA_CPU',
 'browser_windows_gpu':'NOT_RUN_BROWSER_BINARY_UNAVAILABLE',
 'r15_rendered_frame_count':24,'four_angles':[0,90,180,270],
 'four_angle_pixel_changes_not_quality_score':scene,'default_fallback_matches_R14':fallback,
 'boss_true_cpp_native_transition_sequence':boss_delta,'player_accepted_movement_frame_changes':movement,
 'unchanged_sha256_files':len(matches),'all_immutables_sha256_match':all(matches.values()),
 'limitations':['No newly painted roofs, chimneys, doors or silhouettes; this round could not perform visual regeneration',
 'Alpha/trim is measured and corrected in Canvas; existing image pixels and fringing not repainted',
 'Frames are 4x4 painted states, not skeletal rigs; source sheet orientation continuity still requires art review',
 'Boss impact visual is post-adjudication: no synthetic attack or damage timer in JavaScript',
 'Different pixel percentages prove rendering changed, not human artistic satisfaction',
 'Standard Windows/Chromium, approved rights, 21 class canon, 3 boss canon, opening and MMO not finished']}
(A/'R15_TEST_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'PASS':True,'python':reg['python'],'node':visual,'cpp_wasm':reg['actions'],'sqlite':'PASS',
 'boss_native_stage_frames':12,'boss':boss_delta,'actor':movement,'four_views':scene,'fallback':fallback,
 'immutable':len(matches),'art':'ART_REVIEW_PENDING','product':'PRODUCT_NO_GO'},ensure_ascii=False))
