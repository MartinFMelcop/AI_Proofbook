import assert from 'node:assert/strict';import fs from 'node:fs';import {createRequire} from 'node:module';
const req=createRequire(import.meta.url),{Canvas}=req('skia-canvas');
const stage=req('../site/r13_stagecraft.js');
let checks=0;const ok=(expr,msg)=>{assert.ok(expr,msg);checks++};
const p={x:210,y:280},pl={x:5,y:14},bo={x:19,y:4};
const original=[JSON.stringify(pl),JSON.stringify(bo)];
ok(stage.readonly===true,'graphics should be readonly');
ok(JSON.stringify(stage.focus(pl,bo,false))===JSON.stringify(pl),'no combat focus');
const focus=stage.focus(pl,bo,true);ok(focus.x>pl.x&&focus.x<bo.x,'camera x interpolation');
ok(focus.y>bo.y&&focus.y<pl.y,'camera y interpolation');
ok(original[0]===JSON.stringify(pl)&&original[1]===JSON.stringify(bo),'owner coordinates untouched');
const invalid=stage.focus(pl,null,true);ok(JSON.stringify(invalid)===JSON.stringify(pl),'missing boss fallback');
const backgrounds=new Set();
for(let b=1;b<=3;b++){
 const canvas=new Canvas(420,420),ctx=canvas.getContext('2d');
 for(const [i,ms] of [1200,1600].entries()){
  ctx.clearRect(0,0,420,420);
  const before=stage.before(ctx,p,b,1,ms,1,b*2);
  const after=stage.after(ctx,p,b,1,ms,1,b*2);
  ok(before.kind===b&&before.owner_intent===1&&before.owner_pattern===b*2&&before.visual_only,'owner metadata pass through');
  ok(after.kind===b&&after.visual_only,'post stage visual only');
  backgrounds.add((await canvas.toBuffer('png')).toString('base64').slice(0,35000));
 }
}
ok(backgrounds.size===6,'distinct boss aesthetics and time samples');
for(let b=1;b<=3;b++){
 const canvas=new Canvas(300,300),ctx=canvas.getContext('2d');
 const a=stage.before(ctx,p,b,1,1500,0,b);const z=stage.after(ctx,p,b,1,1500,0,b);
 ok(a.owner_intent===0&&a.owner_pattern===b,'boss window context preserved');
 ok(z.visual_only,'no damage/action authority');
}
const src=fs.readFileSync(new URL('../site/r13_stagecraft.js',import.meta.url),'utf8');
ok(!/nsw_wasm_apply|\.apply\s*\(|gameplay\.set|nsw_.*_set\s*\(/.test(src),'no authority/actions in visual module');
console.log(JSON.stringify({suite:'R13_ART_DIRECTION_PURE_CONTRACT',PASS:true,checks,boss_styles:3,visual_frames:6,owner_writes:0}));
