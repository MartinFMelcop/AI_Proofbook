import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url);
const F=req('../site/facades_r07.js'),L=req('../site/atmosphere_r07.js'),C=req('../site/camera4.js');
const zeros='a'.repeat(64),other=['b','c','d'].map(c=>c.repeat(64));
let checks=0;
const check=(condition,msg)=>{assert.ok(condition,msg);checks++};
const ready=(id)=>({state:'AUTHOR_ART_APPROVED',buildings:{[id]:{license_checked:true,scale_anchor_reviewed:true,faces:[0,1,2,3].map(i=>`r07_cottage_${i}`),sha256:[zeros,...other]}}});
const fakeImages=Object.fromEntries([0,1,2,3].map(i=>[`r07_cottage_${i}`,{complete:true,naturalWidth:200}]));
for(let id=1;id<=3;id++)for(let q=0;q<4;q++){
 let r=F.resolve(id,q,null,{});
 check(!r.approved&&r.name===F.fallback[id],'default must be R04 fallback');
}
check(F.validManifest(ready(1),1),'valid review-approved manifest structurally accepted');
for(let q=0;q<4;q++)check(F.resolve(1,q,ready(1),fakeImages).name===`r07_cottage_${q}`,'directional mapping');
for(const bad of ['ART_CANDIDATE_REVIEW','ART_REVIEW_PENDING','ART_BLOCKED']){
 let m=ready(1);m.state=bad;check(!F.validManifest(m,1),'nonapproved status must fail');
}
for(const mutate of [
 m=>m.buildings[1].sha256[1]=m.buildings[1].sha256[0],
 m=>m.buildings[1].faces[1]=m.buildings[1].faces[0],
 m=>m.buildings[1].license_checked=false,
 m=>m.buildings[1].scale_anchor_reviewed=false,
 m=>m.buildings[1].sha256[2]='not-a-hash',
 m=>m.buildings[1].faces.pop()
]){let m=ready(1);mutate(m);check(!F.validManifest(m,1),'tampered manifest must fail');}
check(F.resolve(1,0,ready(1),{}).source==='R04_FALLBACK_MISSING_TEXTURE','missing texture fail closed');
for(const id of [0,4,99]){assert.throws(()=>F.resolve(id,0,ready(1),fakeImages),RangeError);checks++;}
for(const q of [-1,4,0.5,NaN]){assert.throws(()=>F.resolve(1,q,ready(1),fakeImages),RangeError);checks++;}
for(let q=0;q<4;q++){
 const proj=(x,y)=>C.project(x,y,q,24,20,0,0,38,20),v=L.shadowVector(proj,10,8);
 check(Number.isFinite(v.dx)&&Number.isFinite(v.dy),'finite rotated shadow');
 check(Math.abs(v.dx)>0&&Math.abs(v.dy)>0,'nonzero 2d shadow projection');
}
const shadows=[0,1,2,3].map(q=>{const proj=(x,y)=>C.project(x,y,q,24,20,0,0,38,20);return L.shadowVector(proj,10,8);});
check(new Set(shadows.map(x=>Math.sign(x.dx)+','+Math.sign(x.dy))).size===4,'shadow changes quadrant with camera');
let fills=0;const ctx={
 save(){},restore(){},beginPath(){},ellipse(){},fill(){fills++;},fillRect(){fills++;},
 createRadialGradient(){return {addColorStop(){}}},createLinearGradient(){return {addColorStop(){}}}
};
const proj=(x,y)=>C.project(x,y,0,24,20,0,0,38,20);
L.cast(ctx,proj,10,8,1,2);L.light(ctx,proj,10,8,1200,85);L.chimney(ctx,proj,10,8,1200);L.veil(ctx,1200,760,1200);
check(fills>=4,'atmosphere actually paints on canvas');
console.log(JSON.stringify({PASS:true,checks,facade:'fail_closed',shadow_four_views:true,render_only:true}));
