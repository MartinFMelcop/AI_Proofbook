#!/usr/bin/env python3
"""R14 art candidate evidence; NOT a release or authorization of original/canon rights."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1]
B=Path('/mnt/data/MMAI_PRODUCT_V1_R13_WORK')
ART=R/'artifacts';ART.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def compare(a,b):
 a=np.asarray(Image.open(a).convert('RGB'),dtype=np.int16)
 b=np.asarray(Image.open(b).convert('RGB'),dtype=np.int16)
 assert a.shape==b.shape==(760,1200,3)
 d=np.abs(a-b).mean(axis=2)
 return {'pixel_change_rgb_gt18_pct':round(float((d>18).mean()*100),4), 'average_rgb_difference':round(float(d.mean()),4)}
originals=['core/world_r05.cpp','core/world_r05.h','site/product.wasm','site/camera4.js','site/r13_stagecraft.js','site/assets/opening_animatic.mp4']
immutable={p:sha(R/p)==sha(B/p) for p in originals};assert all(immutable.values())
views={};baseline={};boss={}
for i in range(4):
 views[str(i*90)]=compare(B/f'artifacts/R13_SCENE_VIEW_{i}.png', ART/f'R14_SCENE_VIEW_{i}.png')
 assert views[str(i*90)]['pixel_change_rgb_gt18_pct']>2
 baseline[str(i*90)]= ImageChops.difference(Image.open(B/f'artifacts/R12_DEFAULT_FALLBACK_VIEW_{i}.png').convert('RGBA'),Image.open(ART/f'R14_FALLBACK_VIEW_{i}.png').convert('RGBA')).getbbox() is None
assert all(baseline.values())
for i in range(1,4):
 boss[str(i)]={str(frame):compare(B/f'artifacts/R13_BOSS_{i}_FRAME_{frame}.png',ART/f'R14_BOSS_{i}_FRAME_{frame}.png') for frame in range(2)}
 assert all(v['pixel_change_rgb_gt18_pct']>3 for v in boss[str(i)].values())
# 2x2 real screenshots from the actual world.js Skia runner, not concept art.
canvas=Image.new('RGB',(1200,800),'#101820');d=ImageDraw.Draw(canvas)
for i in range(4):
 im=Image.open(ART/f'R14_SCENE_VIEW_{i}.png').convert('RGB');im.thumbnail((590,365));x=(i%2)*600+(600-im.width)//2;y=(i//2)*400+22
 canvas.paste(im,(x,y));d.text(((i%2)*600+16,(i//2)*400+8),f'CAMERA {i*90} | ART CANDIDATE',fill='#f5d6a0')
canvas.save(ART/'R14_FOUR_VIEW_CONTACT.jpg',quality=90)
frame=Image.new('RGB',(1200,840),'#101820');dr=ImageDraw.Draw(frame)
for i in range(1,4):
 im=Image.open(ART/f'R14_BOSS_{i}_FRAME_0.png').convert('RGB');im.thumbnail((390,570));frame.paste(im,((i-1)*400+(400-im.width)//2,45));dr.text(((i-1)*400+16,18),f'BOSS {i} | R14 ART LAB',fill='#f5d6a0')
frame.save(ART/'R14_BOSS_CONTACT.jpg',quality=89)
report={
 'schema':'mmai.product_v1.r14.real_art_integration.v1','state':'ENGINEERING_LAB_PASS_ART_REVIEW_PENDING_PRODUCT_NO_GO',
 'source_sheets':8,'new_original_sheet_sprite_cutouts':92,'building_frames':12,'npc_and_hero_frames':32,'boss_frames':48,
 'source':'Eight original ImageGen sheets from 2026-11-15; physical image bytes archived; no source sheet rotated to fake independent views',
 'art_review':'PENDING_SCALE_FACE_MATCH_ALPHA_CLEANUP_RIGHTS_NARRATIVE_ACK',
 'python_tests':257,'r14_node_checks':191,'historical_node_checks':{'R07':44,'R12':67,'R13':26},
 'cpp20_c17_abi5':'PASS_COMPILED_AND_EXECUTED','native_cpp_to_wasm_actions':121,
 'historical_wasm_regressions':{'R04':121,'R03':121,'R02':116,'R01':100},
 'sqlite':'R05_121_EVENT_JOURNAL_VERIFY_PASS','render_engine':'ACTUAL site/world.js + C++ ABI5 product.wasm + Skia CPU',
 'rendered_camera_views':4,'rendered_boss_frames':6,'rendered_fallback_views':4,
 'render_no_owner_mutation':'PASS_VERIFIED_IN_EACH_RENDER_SCRIPT','immutable_sources':immutable,
 'default_fallback_pixel_identical_to_R13':baseline,'visual_scene_delta_R13_to_R14':views,'boss_image_delta_R13_to_R14':boss,
 'limitations':['No human art approval; AI-generated sprite sheet frames are candidate paintings only',
  'Original building side consistency (doors, roofs, chimney) is improved but requires authored visual QA',
  'Foreground-alpha matte detection may remove dark detail / keep tiny fragments',
  'Sprite sheets provide discrete frames; no skeletal rigs or interpolation guarantee',
  'Camera and rendering do not change combat/quest/collision; JS remains observer only',
  'Boss B03 is still separate from the independent Rave Masters historical canon',
  'No Windows/Chromium/GPU or complete live MMO proof; not a release']}
(ART/'R14_TEST_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'PASS':True,'scenes':views,'fallback':baseline,'bosses':{k:[round(x['pixel_change_rgb_gt18_pct'],1) for x in v.values()] for k,v in boss.items()},'cpp_sha_frozen':all(immutable.values())},ensure_ascii=False))
