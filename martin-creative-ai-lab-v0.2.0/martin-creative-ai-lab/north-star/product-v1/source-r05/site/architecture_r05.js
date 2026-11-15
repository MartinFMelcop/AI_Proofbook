/** Experimental scene geometry R05: camera-true four-face volumes, not final DCC art.
 * Coordinates and footprint centers belong to the compiled world owner. All projected
 * surfaces are observer-only. A facade is a physical face with a persistent world normal,
 * NOT a flipped sprite or a separate world map per camera orientation.
 */
(function(root){'use strict';
const SPECS=Object.freeze({
  1:{name:'casa',w:.92,l:2.84,wall:76,roof:27,stone:'#7a7c7b',timber:'#3b2830',roofColor:'#334556',windows:'#ffd58a',banner:'#ad6a68'},
  2:{name:'forja',w:.92,l:1.91,wall:69,roof:21,stone:'#706b67',timber:'#4b312d',roofColor:'#3f3d48',windows:'#ff9944',banner:'#b54d47'},
  3:{name:'boticário',w:.92,l:1.91,wall:72,roof:23,stone:'#85837a',timber:'#382c39',roofColor:'#3e5553',windows:'#d0e8a3',banner:'#5f9c73'}
});
const palettes=Object.freeze({warm:'#ffcd84',shadow:'#101c24',gold:'#cfa66e'});
function draw(ctx,project,id,centerX,centerY,zoom=1,opacity=1,ms=0){
 const s=SPECS[id];if(!s)return {drawn:false};
 const x0=centerX-s.w/2,x1=centerX+s.w/2,y0=centerY-s.l/2,y1=centerY+s.l/2;
 const v=(x,y,z=0)=>{const q=project(x,y);return [q.x,q.y-z*zoom];};
 const xz=[x0,x1],yz=[y0,y1];
 const pts=[v(x0,y0),v(x1,y0),v(x1,y1),v(x0,y1)];
 const top=[v(x0,y0,s.wall),v(x1,y0,s.wall),v(x1,y1,s.wall),v(x0,y1,s.wall)];
 const ridge=[v((x0+x1)/2,y0,s.wall+s.roof),v((x0+x1)/2,y1,s.wall+s.roof)];
 const poly=(points,fill,stroke='#15212c')=>{ctx.beginPath();ctx.moveTo(...points[0]);for(let j=1;j<points.length;j++)ctx.lineTo(...points[j]);ctx.closePath();ctx.fillStyle=fill;ctx.fill();ctx.strokeStyle=stroke;ctx.lineWidth=.8*zoom;ctx.stroke();};
 const line=(a,b,color,width=1)=>{ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.strokeStyle=color;ctx.lineWidth=width*zoom;ctx.stroke();};
 const mix=(a,b,t)=>[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t];
 ctx.save();ctx.globalAlpha=opacity;
 // Ground contact: a small undercroft shadow exactly anchored to blocked cells.
 const c=v(centerX,centerY);ctx.beginPath();ctx.ellipse(c[0],c[1]+3*zoom,29*zoom,13*zoom,0,0,Math.PI*2);
 ctx.fillStyle='#050d12a8';ctx.fill();
 const faces=[];
 for(let j=0;j<4;j++){
  const k=(j+1)%4,face=[pts[j],pts[k],top[k],top[j]],depth=(pts[j][1]+pts[k][1])/2;
  faces.push({j,face,depth});
 }
 // Paint rear to front in *camera* projection; each wall remains in its own world axis.
 faces.sort((a,b)=>a.depth-b.depth);
 for(const f of faces){
  const j=f.j,k=(j+1)%4;
  poly(f.face,j%2?s.stone:'#9c958c');
  line(pts[j],top[j],s.timber,6);line(pts[k],top[k],s.timber,6);
  line(mix(pts[j],top[j],.53),mix(pts[k],top[k],.53),s.timber,3);
  // Two dimensionally stable windows projected on each wall (including rear walls).
  const n=s.l>2.2 && (j===1||j===3)?2:1;
  for(let t=0;t<n;t++){
   const u=n===2?.31+t*.38:.5,h=.45,size=n===2?.12:.17;
   const left=v(x0,y0);void left;
   const interp=(a,b,u)=>mix(a,b,u);
   const footL=interp(pts[j],pts[k],u-size),footR=interp(pts[j],pts[k],u+size);
   const roofL=interp(top[j],top[k],u-size),roofR=interp(top[j],top[k],u+size);
   const lp=interp(footL,roofL,h-.12),rp=interp(footR,roofR,h-.12),rt=interp(footR,roofR,h+.12),lt=interp(footL,roofL,h+.12);
   poly([lp,rp,rt,lt],'#161c27',s.timber);ctx.globalAlpha=opacity*(.74+.18*Math.sin(ms/960+id+t));
   poly([interp(lp,rp,.10),interp(lp,rp,.90),interp(lt,rt,.90),interp(lt,rt,.10)],s.windows,s.windows);
   ctx.globalAlpha=opacity;line(interp(lp,lt,.5),interp(rp,rt,.5),s.timber,2.1);
  }
  // A single physical shop entrance faces south (+world Y), never teleports as camera rotates.
  if(j===2){
   let b=mix(pts[2],pts[3],.5),u=mix(top[2],top[3],.5);
   const a=mix(b,u,.04),c1=mix(b,u,.64);
   const l=mix(pts[2],pts[3],.35),r=mix(pts[2],pts[3],.65),l1=mix(top[2],top[3],.35),r1=mix(top[2],top[3],.65);
   poly([mix(l,l1,.04),mix(r,r1,.04),mix(r,r1,.63),mix(l,l1,.63)],'#1d2429',s.timber);
   line(a,c1,s.banner,2);
  }
 }
 // Gabled roof actually has two distinct sloping planes and a ridge in world space.
 const leftRoof=[v(x0-.13,y0-.13,s.wall),v(x0-.13,y1+.13,s.wall),ridge[1],ridge[0]];
 const rightRoof=[v(x1+.13,y0-.13,s.wall),v(x1+.13,y1+.13,s.wall),ridge[1],ridge[0]];
 const roofs=[leftRoof,rightRoof];roofs.sort((a,b)=>a.reduce((n,p)=>n+p[1],0)-b.reduce((n,p)=>n+p[1],0));
 roofs.forEach((roof,i)=>{poly(roof,i===0?s.roofColor:'#273843');for(let k=1;k<=5;k++){
   const u=k/6;line(mix(roof[0],roof[3],u),mix(roof[1],roof[2],u),'#c9bbc42c',.65);
  }});
 // World-fixed roof finial, with an emitter on the forge, never a translated character sprite.
 const e=v(centerX,y0,s.wall+s.roof+4);ctx.beginPath();ctx.arc(e[0],e[1],2.6*zoom,0,2*Math.PI);
 ctx.fillStyle=id===2?'#ff7b38':'#ddba81';ctx.fill();
 ctx.restore();
 return {drawn:true,facades:4,roofPlanes:2,worldCenter:[centerX,centerY],id};
}
const API={draw,SPECS};
if(typeof module!=='undefined'&&module.exports)module.exports=API;else root.NSArchitectureR05=API;
})(typeof globalThis!=='undefined'?globalThis:this);
