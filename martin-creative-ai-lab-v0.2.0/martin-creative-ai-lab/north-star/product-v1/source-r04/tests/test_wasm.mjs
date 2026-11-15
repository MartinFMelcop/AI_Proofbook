import fs from 'node:fs';import assert from 'node:assert/strict';
const bytes=fs.readFileSync(new URL('../artifacts/product_legacy.wasm',import.meta.url));const {instance}=await WebAssembly.instantiate(bytes,{});const w=instance.exports;
assert.equal(w.nsp_abi(),1);assert.equal(w.nsp_wasm_create(8,16),1);
assert.equal(w.nsp_wasm_primary(),8);assert.equal(w.nsp_wasm_secondary(),16);
const run=(t,v=0)=>w.nsp_wasm_apply(w.nsp_wasm_revision(),t,v);
assert.equal(run(2),12);assert.equal(w.nsp_wasm_revision(),0);
for(let gate=1;gate<=4;gate++)assert.equal(run(1,gate),1);
for(let boss=1;boss<=3;boss++){
 assert.equal(run(2),2);assert.equal(w.nsp_wasm_boss(),boss);
 while(w.nsp_wasm_boss()) assert.ok([1,3,4].includes(run(3)));
 assert.equal(w.nsp_wasm_defeats(),boss);
}
assert.equal(w.nsp_wasm_step(),7);assert.equal(w.nsp_wasm_boss(),0);
console.log(JSON.stringify({suite:'composite_wasm',state:'PASS',revision:w.nsp_wasm_revision(),health:w.nsp_wasm_health(),bosses:w.nsp_wasm_defeats(),bytes:bytes.length}));
