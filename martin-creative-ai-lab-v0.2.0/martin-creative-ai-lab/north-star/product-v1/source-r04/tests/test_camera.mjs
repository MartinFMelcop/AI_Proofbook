import assert from 'node:assert/strict';import fs from 'node:fs';import vm from 'node:vm';
const context={};vm.runInNewContext(fs.readFileSync(new URL('../site/camera4.js',import.meta.url),'utf8'),context);
const c=context.NSCamera4;assert.ok(c);for(let q=0;q<4;q++){assert.equal(c.turn(q,1),(q+1)%4);assert.equal(c.turn(q,-1),(q+3)%4);}
let q=0;for(let i=0;i<4;i++)q=c.turn(q,1);assert.equal(q,0);
console.log(JSON.stringify({suite:'camera_four_views',state:'PASS',views:4}));
