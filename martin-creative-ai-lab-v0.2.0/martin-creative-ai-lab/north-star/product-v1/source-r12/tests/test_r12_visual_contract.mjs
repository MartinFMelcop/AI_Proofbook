import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url);
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const {Canvas,Image}=req('skia-canvas');
Object.defineProperty(Image.prototype,'naturalWidth',{get(){return this.width;}});
Object.defineProperty(Image.prototype,'naturalHeight',{get(){return this.height;}});
globalThis.NSR12AssetAnchors=req('../site/r12_asset_anchors.js');
const fx=req('../site/r12_finishing.js');
let n=0;const ok=(v)=>{assert.ok(v);n++};
for(let sid=1;sid<=3;sid++)for(let view=0;view<4;view++){
 const building=['cottage','forge','apothecary'][sid-1];const v=fx.measured(sid,view);
 ok(v&&v.silhouette_h>490&&v.silhouette_h<570);
 ok(v.anchor_x>280&&v.anchor_x<350);
 ok(v.anchor_y>=595&&v.anchor_y<=620);
 const bytes=fs.readFileSync(path.join(root,'site/assets/world',`r11_${building}_${view}.webp`));
 const img=new Image();img.src=bytes;await new Promise(r=>setTimeout(r,70));
 const c=new Canvas(450,450),ctx=c.getContext('2d');
 const a=fx.building(ctx,img,{x:225,y:350},sid,view,1,.94,2350);
 ok(a&&a.source==='R11_PAINTED_NOT_APPROVED'&&a.visible_height>185);
 ok(a.ground_x===225&&a.ground_y===350);
}
const c=new Canvas(320,320),ctx=c.getContext('2d');
for(let b=1;b<=3;b++){
 const img=new Image();img.src=fs.readFileSync(path.join(root,'site/assets/world',`r04_ruinguardian_0.webp`));
 await new Promise(r=>setTimeout(r,80));
 const o=fx.boss(ctx,img,{x:160,y:270},b,2500,1,1,b);
 ok(o&&o.boss===b&&o.gameplay_mutation===false&&o.owner_pattern===b);
}
const empty=new Canvas(64,64),e=empty.getContext('2d');ok(fx.actor(e,null,10,10,2000,true)===false);
ok(fx.building(e,null,{x:2,y:2},1,0,1,1,2000)===false);
const source=fs.readFileSync(path.join(root,'site/world.js'),'utf8');
ok(source.includes('NSR12VisualLab===true'));
ok(!source.includes('nsw_wasm_apply('));
console.log(JSON.stringify({suite:'R12_VISUAL_CONTRACT',PASS:true,checks:n,visual_only:true,author_art_approved:false}));
