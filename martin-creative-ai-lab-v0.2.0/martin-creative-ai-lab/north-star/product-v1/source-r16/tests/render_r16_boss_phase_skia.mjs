/** Source-based actual Canvas render of the three C++-owned boss combat states.
 * This is LAB art evidence, not a gameplay screenshot captured on Windows.
 */
import fs from 'node:fs';import path from 'node:path';import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url),{Canvas,Image}=req('skia-canvas');
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
process.chdir(path.join(root,'site'));globalThis.NSCamera4=req('../site/camera4.js');globalThis.NSArchitectureR05=req('../site/architecture_r05.js');globalThis.NSAmbienceR06=req('../site/ambience_r06.js');globalThis.NSFacadeR07=req('../site/facades_r07.js');globalThis.NSAtmosphereR07=req('../site/atmosphere_r07.js');globalThis.NSR12AssetAnchors=req('../site/r12_asset_anchors.js');globalThis.NSFinishingR12=req('../site/r12_finishing.js');globalThis.NSR12VisualLab=false;globalThis.NSR13ArtLab=false;globalThis.NSR14ArtLab=false;globalThis.NSR15ArtLab=false;globalThis.NSR16ArtLab=true;globalThis.NSR15Anchors=req('../site/r15_anchors.js');globalThis.NSPresentationR15=req('../site/r15_presentation.js');globalThis.NSArtR14=req('../site/r14_art.js');globalThis.NSArtR16=req('../site/r16_art.js');globalThis.NSPresentationR16=req('../site/r16_presentation.js');globalThis.NSStagecraftR13=req('../site/r13_stagecraft.js');globalThis.NSR10ArtPreview=false;globalThis.NSR11ArtPreview=false;globalThis.Image=Image;
Object.defineProperty(Image.prototype,'naturalWidth',{get(){return this.width;}});
Object.defineProperty(Image.prototype,'naturalHeight',{get(){return this.height;}});
const wasm=fs.readFileSync(path.join(root,'site/product.wasm'));
const {instance}=await WebAssembly.instantiate(wasm,{}),e=instance.exports;
assert.equal(e.nsw_abi(),5);
const trace=JSON.parse(fs.readFileSync(path.join(root,'artifacts/R05_WORLD_NATIVE_TRACE.json'),'utf8'));
const canvas=new Canvas(1200,760);canvas.getBoundingClientRect=()=>({width:1200,height:760,left:0,top:0});
canvas.addEventListener=()=>{};canvas.removeEventListener=()=>{};
const dom=new Map(),fields=['world-location','world-quest-title','world-quest-text','world-hp','world-sp','world-herbs','world-kit-primary','world-kit-secondary','world-profession','world-npc-state','world-remedies','world-camera','world-coordinates','world-boss-name','world-boss-hp','world-boss-bar','world-boss-tell','world-interact-hint','world-notice','world-combat','world-interact'];
for(const k of fields)dom.set(k,{textContent:'',style:{},hidden:true,querySelectorAll(){return[];}});
dom.set('world-canvas',canvas);globalThis.document={getElementById(k){return dom.get(k)}};
globalThis.devicePixelRatio=1;let raf=[];globalThis.requestAnimationFrame=fn=>(raf.push(fn),raf.length);globalThis.cancelAnimationFrame=()=>{};
globalThis.addEventListener=()=>{};globalThis.removeEventListener=()=>{};globalThis.performance={now:()=>2500};
const world=req('../site/world.js');const action=(type,v=0)=>e.nsw_wasm_apply(e.nsw_wasm_revision(),type,v);
const owner={engine:e,action,profile:{primary:6,secondary:17,classNames:{6:'Knight',17:'Bard'}},openMenu(){},lastMessage:'R06 boss visual evidence | lab'};
const rootPresentation=globalThis.NSPresentationR15;const result=[];
for(let b=1;b<=3;b++){
 assert.equal(e.nsw_wasm_create(6,17),1);
 let expected=null;
 for(const ev of trace.events){
  assert.equal(action(ev.type,ev.value),ev.code);
  if(e.nsw_wasm_boss()===b && e.nsw_wasm_boss_intent()===1){expected=ev;break;}
 }
 assert.ok(expected,'missing real accepted boss trigger '+b);
 world.mount(owner);await new Promise(r=>setTimeout(r,850));
 if(b===2)world.rotate(1);if(b===3){world.rotate(1);world.rotate(1);}
 const draw=raf.find(fn=>fn.name==='draw');assert.equal(typeof draw,'function');
 let revision=e.nsw_wasm_revision(),coords=[e.nsw_wasm_x(),e.nsw_wasm_y()];
 assert.equal(e.nsw_wasm_boss_intent(),1,'C++ must issue telegraph first');
 assert.equal(e.nsw_wasm_boss_threat_radius()>0,true,'native threat footprint present');
 const ownerSignature=[];
 for(let frame=0;frame<4;frame++){
  // This is the ACTUAL C++ action adjudication point. Rendering itself never calls apply.
  if(frame===2){const rc=action(4,0);assert.ok(rc>0&&rc<10,'C++ defend accepted');
   assert.equal(e.nsw_wasm_boss_intent(),2,'C++ resolved the attack before visual impact');
   revision=e.nsw_wasm_revision();coords=[e.nsw_wasm_x(),e.nsw_wasm_y()];}
  const elapsed=[0,360,0,340][frame];
  const ms=3200+b*150 + (frame<2?elapsed:800+elapsed);
  const snapshotIntent=e.nsw_wasm_boss_intent();
  draw(ms);
  assert.equal(e.nsw_wasm_revision(),revision,'render must never mutate C++ revision');
  assert.deepEqual([e.nsw_wasm_x(),e.nsw_wasm_y()],coords,'render must never move player');
  const stage=rootPresentation.bossStage(snapshotIntent,elapsed);
  const dst=path.join(root,'artifacts',`R16_BOSS_${b}_STAGE_${frame}.png`);
  fs.writeFileSync(dst,await canvas.toBuffer('png'));
  assert.ok(fs.statSync(dst).size>90000,'nontrivial actual Skia render');
  result.push({boss:b,frame,angle:(b-1)*90,revision,owner_intent:snapshotIntent,visual_frame:stage,file:path.basename(dst),bytes:fs.statSync(dst).size,unchanged_owner:true});
  ownerSignature.push(snapshotIntent);
 }
 assert.deepEqual(ownerSignature,[1,1,2,2],'must span native tell and resolved attack');
 world.unmount();raf=[];
}
console.log(JSON.stringify({suite:'R14_ACTUAL_CANVAS_SKIA_BOSS_ART',PASS:true,scenes:result}));
