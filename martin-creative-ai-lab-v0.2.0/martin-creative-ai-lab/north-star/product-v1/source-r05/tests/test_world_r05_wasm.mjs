// Independent Node WebAssembly replay of a 121-event C++20 native trace.
import fs from 'node:fs';import assert from 'node:assert/strict';
const base=new URL('../',import.meta.url);
const fixture=JSON.parse(fs.readFileSync(new URL('artifacts/R05_WORLD_NATIVE_TRACE.json',base),'utf8'));
const bytes=fs.readFileSync(new URL('site/product.wasm',base));
const {instance}=await WebAssembly.instantiate(bytes,{}),e=instance.exports;
assert.equal(e.nsw_abi(),5);assert.equal(e.nsw_wasm_create(fixture.profile.primary,fixture.profile.secondary),1);
let count=0;
for(const ev of fixture.events){
 assert.equal(e.nsw_wasm_revision(),ev.rev,'revision before '+count);
 assert.equal(e.nsw_wasm_apply(ev.rev,ev.type,ev.value),ev.code,'receipt '+count);
 for(const [field,value] of Object.entries(ev.state)){
  const getter=e['nsw_wasm_'+field];assert.equal(typeof getter,'function','missing '+field);
  assert.equal(getter(),value,'step '+count+' '+field);
 }
 for(let i=1;i<=4;i++)assert.equal(e.nsw_wasm_being_behavior(i),ev.beings[i-1],`npc ${i} step ${count}`);
 const probes=[[e.nsw_wasm_x(),e.nsw_wasm_y()],[e.nsw_wasm_boss_target_x(),e.nsw_wasm_boss_target_y()],
  [Math.min(23,e.nsw_wasm_boss_target_x()+2),e.nsw_wasm_boss_target_y()],[23,19]];
 assert.equal(e.nsw_wasm_boss_threat_radius(),ev.threat.radius,'threat radius '+count);
 for(let j=0;j<probes.length;j++)assert.equal(e.nsw_wasm_boss_threatens(...probes[j]),ev.threat.tiles[j],'threat tile '+count+'/'+j);
 for(let i=1;i<=4;i++)assert.equal(e.nsw_wasm_being_facing(i),ev.facings[i-1],`facing ${i} step ${count}`);
 for(const [x,y,id] of [[10,7,1],[10,8,1],[10,9,1],[17,8,2],[17,9,2],[20,10,3],[20,11,3],[9,8,0],[23,19,0]])assert.equal(e.nsw_wasm_structure_at(x,y),id);
 count++;
}
assert.equal(e.nsw_wasm_quest(),7);assert.equal(e.nsw_wasm_defeats(),3);
for(let i=1;i<=21;i++){
 assert.ok(e.nsw_wasm_kit_cost(i)>=1 && e.nsw_wasm_kit_aux_cost(i)>=1);
 assert.equal(e.nsw_wasm_kit_mode(i),i);assert.ok(e.nsw_wasm_kit_passive_family(i)>=1);
}
const rev=e.nsw_wasm_revision();
for(const [t,v,c] of [[1,999,11],[2,9,11],[11,1,14],[12,0,11]]){
 assert.equal(e.nsw_wasm_apply(rev,t,v),c,`reject ${t}`);assert.equal(e.nsw_wasm_revision(),rev);
}
assert.equal(e.nsw_wasm_apply(rev-1,1,0),10);assert.equal(e.nsw_wasm_revision(),rev);
console.log(JSON.stringify({suite:'r05_authoritative_native_vs_wasm',PASS:true,events:count,kitProfiles:21,abilitiesPerProfile:2,passiveFamilies:7,finalQuest:e.nsw_wasm_quest()}));
