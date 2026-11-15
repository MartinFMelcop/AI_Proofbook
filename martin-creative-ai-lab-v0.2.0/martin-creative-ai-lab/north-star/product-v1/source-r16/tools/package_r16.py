#!/usr/bin/env python3
"""Compact R16 image-derivative package, no R06/R14 historical duplication."""
from pathlib import Path
import zipfile, json, hashlib
R=Path(__file__).resolve().parents[1]
F=Path('/mnt/data/MMAI_PRODUCT_V1_R16_MATTE_DELTA.zip')
files=[*sorted((R/'site/assets/world').glob('r16_*.webp'))]
relative=[p.relative_to(R) for p in files]
relative += [Path(p) for p in [
 'site/index.html','site/world.js','site/r16_art.js','site/r16_presentation.js',
 'tools/refine_r16_alpha.py','tools/patch_r16_consumer.py','tools/verify_r16_art_delta.py',
 'tests/test_r16_art_contract.mjs','tests/render_r16_fourview_skia.mjs',
 'tests/render_r16_fallback_skia.mjs','tests/render_r16_boss_phase_skia.mjs',
 'tests/render_r16_actor_motion_skia.mjs','tools/package_r16.py',
 'docs/R16_ART_EVIDENCE_AND_GATES.md',
 'artifacts/R16_ALPHA_REFINEMENT_MANIFEST.json','artifacts/R16_TEST_REPORT.json',
 'artifacts/R16_VISUAL_COMPARE_R15.json','artifacts/R16_NATIVE_REGRESSION.log',
 'artifacts/R16_BOSS_TRACE.log','artifacts/R16_FOUR_CAMERA_CONTACT.jpg',
 'artifacts/R16_BOSS_NATIVE_PHASE_CONTACT.jpg']]
assert len(files)==92 and all((R/p).is_file() for p in relative)
with zipfile.ZipFile(F,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4) as z:
 for p in relative: z.write(R/p,str(p))
sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(F) as z:
 bad=z.testzip();assert bad is None,bad
 assert set(z.namelist())==set(map(str,relative))
 members={name:sha(z.read(name)) for name in z.namelist()}
 assert all(members[str(p)]==sha((R/p).read_bytes()) for p in relative)
report={'package':F.name,'bytes':F.stat().st_size,'sha256':sha(F.read_bytes()),
 'members':len(members),'derived_physical_sprites':92,'status':'ART_REVIEW_PENDING_PRODUCT_NO_GO',
 'zip_crc_and_every_member_sha256':'PASS','members_sha256':members}
Path('/mnt/data/MMAI_PRODUCT_V1_R16_PACKAGE_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='members_sha256'}))
