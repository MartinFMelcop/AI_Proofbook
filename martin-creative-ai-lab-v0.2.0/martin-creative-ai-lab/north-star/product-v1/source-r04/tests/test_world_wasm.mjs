import fs from 'node:fs';import assert from 'node:assert/strict';
const root=new URL('../',import.meta.url);
const trace=JSON.parse(fs.readFileSync(new URL('artifacts/WORLD_NATIVE_TRACE.json',root),'utf8'));
const wasm=fs.readFileSync(new URL('artifacts/world_r01.wasm',root));
const {instance}=await WebAssembly.instantiate(wasm,{});const w=instance.exports;
assert.equal(w.nsw_abi(),1);
assert.equal(w.nsw_wasm_create(trace.inputs.primary,trace.inputs.secondary),1);
let accepted=0;
for(const e of trace.trace){
 assert.equal(w.nsw_wasm_revision(),e.rev,'pre-revision');
 const rc=w.nsw_wasm_apply(e.rev,e.type,e.value);
 assert.equal(rc,e.code,`result mismatch action ${accepted}`);
 for(const [field,val] of Object.entries(e.state)){
  const accessor=w['nsw_wasm_'+({'active_boss':'boss','target_x':'boss_target_x','target_y':'boss_target_y'}[field]||field)];
  assert.equal(typeof accessor,'function',field);
  assert.equal(accessor(),val,`diff ${field} at ${accepted}`);
 }
 accepted++;
}
assert.equal(w.nsw_wasm_quest(),7);assert.equal(w.nsw_wasm_defeats(),3);
// stale replay and invalid action never advance revision
const pre=w.nsw_wasm_revision();assert.equal(w.nsw_wasm_apply(0,1,0),10);assert.equal(w.nsw_wasm_revision(),pre);
assert.equal(w.nsw_wasm_apply(pre,99,0),11);assert.equal(w.nsw_wasm_revision(),pre);
console.log(JSON.stringify({suite:'native_cpp_vs_wasm_spatial_parity',PASS:true,events:accepted,quest:w.nsw_wasm_quest(),defeats:w.nsw_wasm_defeats(),revision:pre}));
