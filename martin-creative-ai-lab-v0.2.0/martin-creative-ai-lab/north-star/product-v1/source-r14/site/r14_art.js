/* North Star R14: observational asset selection only. NO gameplay logic or canon decisions.
 * New ImageGen-sourced art is a private candidate, not AUTHOR_ART_APPROVED.
 * Each frame is an independent, physically stored sprite cropped from an original sprite sheet.
 */
(function(root){'use strict';
 const buildings={1:'cottage',2:'forge',3:'apothecary'};
 const characterKeys=['hero','guard_npc','ruinguard','wraith','guardian_tree'];
 const assetKeys=()=>[
   ...Object.values(buildings).flatMap(name=>Array.from({length:4},(_,f)=>`r14_${name}_${Math.floor(f/2)}_${f%2}`)),
   ...characterKeys.flatMap(name=>Array.from({length:4},(_,r)=>Array.from({length:4},(_,f)=>`r14_${name}_${r}_${f}`)).flat())
 ];
 const four=i=>Number.isInteger(i)&&i>=0&&i<4;
 const facing=(name,face,frame)=>four(face)&&four(frame)?`r14_${name}_${face}_${frame}`:null;
 const art={
   assetKeys,
   building:(id,face)=> buildings[id]&&four(face)?`r14_${buildings[id]}_${Math.floor(face/2)}_${face%2}`:null,
   hero:(face,frame)=>facing('hero',face,frame),
   guard:(face,frame)=>facing('guard_npc',face,frame),
   boss:(id,face,frame)=> ({1:'ruinguard',2:'wraith',3:'guardian_tree'}[id]?facing(({1:'ruinguard',2:'wraith',3:'guardian_tree'})[id],face,frame):null),
   candidateStatus:'R14_ORIGINAL_SHEET_CUTOUT_NOT_APPROVED'
 };
 root.NSArtR14=Object.freeze(art);
 if(typeof module!=='undefined'&&module.exports)module.exports=art;
})(typeof globalThis!=='undefined'?globalThis:this);
