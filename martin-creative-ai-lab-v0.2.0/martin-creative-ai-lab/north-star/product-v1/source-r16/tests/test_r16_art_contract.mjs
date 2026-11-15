import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url),root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
globalThis.NSArtR14=req('../site/r14_art.js');
globalThis.NSPresentationR15=req('../site/r15_presentation.js');
globalThis.NSR15Anchors=req('../site/r15_anchors.js');
const r16=req('../site/r16_art.js'),pres=req('../site/r16_presentation.js');
let checks=0;const ok=(v,msg)=>{assert.ok(v,msg);checks++};
const old=globalThis.NSArtR14.assetKeys(),all=r16.assetKeys();
ok(all.length===92&&new Set(all).size===92,'92 unique R16 art files');
for(let i=0;i<all.length;i++){
 ok(all[i]===old[i].replace('r14_','r16_'),'mapped from physical prior asset');
 ok(fs.existsSync(path.join(root,'site/assets/world',all[i]+'.webp')),'asset physically readable');
}
for(let id=1;id<=3;id++)for(let face=0;face<4;face++)ok(r16.building(id,face)===globalThis.NSArtR14.building(id,face).replace('r14_','r16_'),'real four-face building');
for(let face=0;face<4;face++)for(let frame=0;frame<4;frame++){
 ok(r16.hero(face,frame).startsWith('r16_'),'hero painted cycle');
 ok(r16.guard(face,frame).startsWith('r16_'),'guard painted cycle');
 for(let boss=1;boss<=3;boss++)ok(r16.boss(boss,face,frame).startsWith('r16_'),'boss painted 4x4');
}
for(let intent of [1,2])for(let ms of [0,60,180,340,700]){
 ok(intent===1?pres.bossStage(intent,ms)<2:pres.bossStage(intent,ms)>=2,'no impact before C++ resolution');
}
const sample=r16.hero(0,0),painted=globalThis.NSR15Anchors['r14_'+sample.slice(4)];
let observedDraws=0;
const ctx={save(){},restore(){},drawImage(){observedDraws++},set globalAlpha(v){},set shadowColor(v){},set shadowBlur(v){}};
const img={complete:true,naturalWidth:320,naturalHeight:320};
ok(!!painted && !!pres.actor(ctx,img,100,100,500,true,sample),'adapter reuses measured original pivot');
ok(observedDraws===1,'real paint call');
ok(pres.actor(ctx,img,100,100,500,true,'forged_fake_image')===false,'failclosed unknown name');
ok(r16.boss(0,0,0)===null&&r16.hero(5,0)===null,'illegal art frame not mapped');
const consumer=fs.readFileSync(path.join(root,'site/r16_presentation.js'),'utf8');
ok(!/nsw_wasm_apply|nsw_.*_set\s*\(|\.apply\s*\(/.test(consumer),'R16 cannot mutate C++ owner');
console.log(JSON.stringify({PASS:true,suite:'R16_INTACT_OWNER_AND_TRUE_PAINTED_ASSETS',checks,files:all.length}));
