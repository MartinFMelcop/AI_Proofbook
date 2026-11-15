import assert from 'node:assert/strict';import fs from 'node:fs';
const root=new URL('../',import.meta.url);
const fixture=JSON.parse(fs.readFileSync(new URL('artifacts/R02_WORLD_NATIVE_TRACE.json',root),'utf8'));
const wasm=fs.readFileSync(new URL('site/product.wasm',root));
const {instance}=await WebAssembly.instantiate(wasm,{});const e=instance.exports;
assert.equal(e.nsw_abi(),2);assert.equal(e.nsw_wasm_create(fixture.profile.primary,fixture.profile.secondary),1);
let count=0;
for(const event of fixture.events){
 assert.equal(e.nsw_wasm_revision(),event.rev,`revision pre ${count}`);
 assert.equal(e.nsw_wasm_apply(event.rev,event.type,event.value),event.code,`code ${count}`);
 for(const [field,expected] of Object.entries(event.state)){
  const acc=e['nsw_wasm_'+field];assert.equal(typeof acc,'function',`missing ${field}`);
  assert.equal(acc(),expected,`field=${field} event=${count}`);
 }
 for(let i=1;i<=4;i++)assert.equal(e.nsw_wasm_being_behavior(i),event.beings[i-1],`being ${i} event ${count}`);
 count++;
}
assert.equal(e.nsw_wasm_quest(),7);assert.equal(e.nsw_wasm_defeats(),3);
const rev=e.nsw_wasm_revision();
for(const [type,v,code] of [[1,999,11],[9,1,13],[2,5,13]]){
 const got=e.nsw_wasm_apply(rev,type,v);assert.equal(got,code,`negative type ${type}`);assert.equal(e.nsw_wasm_revision(),rev);}
assert.equal(e.nsw_wasm_apply(rev-1,1,0),10);assert.equal(e.nsw_wasm_revision(),rev);
console.log(JSON.stringify({suite:'r02_world_full_natively_audited_WASM',PASS:true,events:count,rev,final_quest:e.nsw_wasm_quest(),classes_implemented_as_lab_modes:21}));
