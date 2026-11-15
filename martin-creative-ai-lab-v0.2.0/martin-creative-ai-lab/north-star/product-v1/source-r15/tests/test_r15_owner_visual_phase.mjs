/* R15 verification of the visual meaning of original painted frames.
 * No hit/damage is calculated or submitted in this consumer. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url);
globalThis.NSR15Anchors=req('../site/r15_anchors.js');
const p=req('../site/r15_presentation.js');
const art=req('../site/r14_art.js');
let checks=0;const ok=(v,msg)=>{assert.ok(v,msg);checks++};
for(const intent of [1,2])for(const e of [0,150,160,200,239,240,600,10000]){
 const f=p.bossStage(intent,e);
 ok(intent===1?f<2:f>=2,'never render unadjudicated boss strike');
 ok(f>=0&&f<=3,'frame within original sheet');
}
for(const [intent,expected] of [[1,[0,1]],[2,[2,3]]]){
 ok(p.bossStage(intent,0)===expected[0],'state initial');
 ok(p.bossStage(intent,400)===expected[1],'state after elapsed');
}
for(let b=1;b<=3;b++)for(let face=0;face<4;face++)for(let intent=1;intent<=2;intent++){
 const owner={boss:b,face,intent,turn:11,phase:0,pattern:2};
 const obj=p.observedBoss(owner,190);
 ok(obj.visual_only && obj.owner_intent===intent && obj.frame=== (intent===1?1:2),'source intent preserved');
 ok(art.boss(b,face,obj.frame) in globalThis.NSR15Anchors,'authored 4x4 frame must exist');
}
ok(p.observedBoss({boss:1,intent:0},0)===null,'fail-closed inactive');
ok(p.observedBoss(null,0)===null,'fail-closed missing owner');
for(const name of art.assetKeys()){
 const m=globalThis.NSR15Anchors[name];
 ok(m.width===m.height&&[320,420,640].includes(m.width),'expected fixed pixel cell');
 ok(m.anchor_y>m.bbox[1]&&m.anchor_y<=m.height,'feet on painted silhouette');
 ok(m.anchor_x>=m.bbox[0]&&m.anchor_x<=m.bbox[2],'pivot in silhouette');
}
const src=fs.readFileSync(new URL('../site/r15_presentation.js',import.meta.url),'utf8');
ok(!/nsw_wasm_apply|\.apply\s*\(|gameplay\.set|nsw_.*_set\s*\(/.test(src),'no authority/intent writes');
console.log(JSON.stringify({PASS:true,suite:'R15_OWNER_INTENT_TO_SPRITE_PHASE',checks,artFrames:art.assetKeys().length,originalsModified:0}));
