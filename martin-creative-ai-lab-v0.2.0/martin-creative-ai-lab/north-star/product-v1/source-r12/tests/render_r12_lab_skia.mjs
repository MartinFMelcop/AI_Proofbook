// R12 spatially anchored visual lab: source = actual site/world.js + original ABI5 WASM; review-only.
/** Headless Skia executes ACTUAL site/world.js Canvas draw routines, unlike a mocked context.
  * NOT a browser, NOT GPU or human art approval. No network, no external assets. */
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url),{Canvas,Image}=req('skia-canvas');
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
process.chdir(path.join(root,'site'));
globalThis.NSCamera4=req('../site/camera4.js');globalThis.NSArchitectureR05=req('../site/architecture_r05.js');globalThis.NSAmbienceR06=req('../site/ambience_r06.js');globalThis.NSFacadeR07=req('../site/facades_r07.js');globalThis.NSAtmosphereR07=req('../site/atmosphere_r07.js');globalThis.NSArchitecturePreviewMode=false;globalThis.NSR10ArtPreview=false;globalThis.NSR11ArtPreview=false;globalThis.NSR12VisualLab=true;globalThis.NSR12AssetAnchors=req('../site/r12_asset_anchors.js');globalThis.NSFinishingR12=req('../site/r12_finishing.js');globalThis.Image=Image;
Object.defineProperty(Image.prototype,'naturalWidth',{get(){return this.width;}});
Object.defineProperty(Image.prototype,'naturalHeight',{get(){return this.height;}});
const wasm=fs.readFileSync(path.join(root,'site/product.wasm'));
const {instance}=await WebAssembly.instantiate(wasm,{}),e=instance.exports;
assert.equal(e.nsw_abi(),5);assert.equal(e.nsw_wasm_create(6,17),1);
const action=(type,value=0)=>e.nsw_wasm_apply(e.nsw_wasm_revision(),type,value);
const targets=new Map(),canvas=new Canvas(1200,760);
canvas.getBoundingClientRect=()=>({width:1200,height:760,left:0,top:0});
canvas.addEventListener=()=>{};canvas.removeEventListener=()=>{};
const ids=['world-location','world-quest-title','world-quest-text','world-hp','world-sp','world-herbs','world-kit-primary','world-kit-secondary','world-profession','world-npc-state','world-remedies','world-camera','world-coordinates','world-boss-name','world-boss-hp','world-boss-bar','world-boss-tell','world-interact-hint','world-notice','world-combat','world-interact'];
for(const id of ids)targets.set(id,{textContent:'',style:{},hidden:true,querySelectorAll(){return[];}});
targets.set('world-canvas',canvas);
globalThis.document={getElementById(id){return targets.get(id);}};
globalThis.devicePixelRatio=1;
let raf=[],listener;
globalThis.requestAnimationFrame=fn=>{raf.push(fn);return raf.length;};
globalThis.cancelAnimationFrame=()=>{};
globalThis.addEventListener=(t,fn)=>{if(t==='keydown')listener=fn;};
globalThis.removeEventListener=()=>{};
globalThis.performance={now:()=>1000};
const world=req('../site/world.js');
const tile=(x,y)=>e.nsw_tile(x,y);let start=[e.nsw_wasm_x(),e.nsw_wasm_y()];
const key=(x,y)=>`${x},${y}`,prev=new Map([[key(...start),null]]),q=[start],dirs=[[0,-1],[1,0],[0,1],[-1,0]];
let goal=[12,12];
for(let i=0;i<q.length;i++){const [x,y]=q[i];if(x===goal[0]&&y===goal[1])break;
 for(let k=0;k<4;k++){let [dx,dy]=dirs[k],xx=x+dx,yy=y+dy;if(xx<1||yy<1||xx>22||yy>18||[3,4,8,9].includes(tile(xx,yy)))continue;
 let s=key(xx,yy);if(prev.has(s))continue;prev.set(s,{p:key(x,y),d:k});q.push([xx,yy]);}}
let seq=[],cur=key(...goal);if(!prev.has(cur))throw Error('no path');while(prev.get(cur)){const p=prev.get(cur);seq.push(p.d);cur=p.p;}
for(const d of seq.reverse())assert.equal(action(1,d),1);
world.mount({engine:e,action,profile:{primary:6,secondary:17,classNames:{6:'Knight',17:'Bard'}},openMenu(){},lastMessage:'R12 Skia owner fixture'});
await new Promise(r=>setTimeout(r,900)); // asset decoding; not a timing/performance benchmark
const revisionBeforeRender=e.nsw_wasm_revision(),worldBefore=[e.nsw_wasm_x(),e.nsw_wasm_y()];
for(let i=0;i<4;i++){
 if(i)world.rotate(1);
 const f=raf.find(fn=>fn.name==='draw');assert.equal(typeof f,'function');f(2500+i*300);
 const dst=path.join(root,'artifacts',`R12_LAB_VIEW_${i}.png`);
 fs.writeFileSync(dst,await canvas.toBuffer('png'));
 assert.equal(e.nsw_wasm_revision(),revisionBeforeRender,'render changed owner revision');
 assert.deepEqual([e.nsw_wasm_x(),e.nsw_wasm_y()],worldBefore,'camera changed position');
 const stat=fs.statSync(dst);assert.ok(stat.size>100000,`render too small ${stat.size}`);
 console.log(JSON.stringify({source:"REAL_WORLD_JS_SKIA_R12",angle:i*90,bytes:stat.size,file:path.basename(dst),title:targets.get('world-quest-title').textContent}));
}
world.unmount();
