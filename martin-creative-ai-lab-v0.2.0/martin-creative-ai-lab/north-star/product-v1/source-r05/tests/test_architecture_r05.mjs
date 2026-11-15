// Pure render-only geometry validation against four real NSCamera4 projections.
import assert from 'node:assert/strict';import {createRequire} from 'node:module';
const req=createRequire(import.meta.url);
const C=req('../site/camera4.js'),A=req('../site/architecture_r05.js');
const shapes=[];
const ctx=new Proxy({save(){},restore(){},beginPath(){},moveTo(x,y){shapes.push([x,y]);},lineTo(){},closePath(){},fill(){},stroke(){},ellipse(){},arc(){},fillRect(){},fillText(){}},
 {get(o,k){if(k in o)return o[k];return undefined;},set(o,k,v){o[k]=v;return true;}});
for(let id=1;id<=3;id++){
 const samples=[];
 for(let corner=0;corner<4;corner++){
  const project=(x,y)=>C.project(x,y,corner,24,20,500,350,38,20);
  shapes.length=0;
  const out=A.draw(ctx,project,id,id===1?10:id===2?17:20,id===1?8:id===2?8:10,1,1,1500);
  assert.equal(out.facades,4);assert.equal(out.roofPlanes,2);
  assert.ok(shapes.length>25,'expect nontrivial facade drawing');
  samples.push(JSON.stringify(shapes));
 }
 assert.equal(new Set(samples).size,4,'four projections must not be a single billboard');
}
const snap=A.draw(ctx,(x,y)=>({x,y}),99,1,1);assert.equal(snap.drawn,false);
console.log(JSON.stringify({suite:'r05_four_sided_projection_geometry',PASS:true,structures:3,views:4,artApproval:'NO'}));
