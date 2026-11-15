import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url),root=path.resolve(new URL('..',import.meta.url).pathname);
const art=req('../site/r14_art.js');let checks=0;
function ok(x,why){assert.ok(x,why);checks++}
ok(art.candidateStatus==='R14_ORIGINAL_SHEET_CUTOUT_NOT_APPROVED','candidate only');
const keys=art.assetKeys();ok(keys.length===92,'source sheet frame count');ok(new Set(keys).size===92,'names distinct');
for(let i=1;i<=3;i++)for(let face=0;face<4;face++){
 const name=art.building(i,face);ok(name&&keys.includes(name),'building name');ok(fs.statSync(path.join(root,'site/assets/world',name+'.webp')).size>500,'asset exists');
}
for(let face=0;face<4;face++)for(let frame=0;frame<4;frame++){
 for(const name of [art.hero(face,frame),art.guard(face,frame),...Array.from({length:3},(_,i)=>art.boss(i+1,face,frame))]){
  ok(keys.includes(name),'registered sprite');ok(fs.statSync(path.join(root,'site/assets/world',name+'.webp')).size>500,'not empty');
 }
}
ok(art.building(4,0)===null,'invalid building');ok(art.boss(0,0,0)===null,'invalid boss');ok(art.hero(-1,0)===null,'invalid facing');
const src=fs.readFileSync(path.join(root,'site/r14_art.js'),'utf8');ok(!/nsw_wasm_apply|\.apply\s*\(|world_tick\s*\+\+|engine\.set/i.test(src),'no authority');
console.log(JSON.stringify({PASS:true,checks,source_sprite_keys:keys.length,buildings:12,other_character_frames:80}));
