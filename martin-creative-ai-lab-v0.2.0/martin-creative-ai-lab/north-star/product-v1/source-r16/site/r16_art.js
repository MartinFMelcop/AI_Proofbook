/* R16 OPT-IN: physical alpha-refined derivatives of the unchanged R14 original
 * artwork. Key selection only. All gameplay and animation phase adjudication
 * remains inside the existing C++ ABI5 and R15 visual observer.
 */
(function(root){'use strict';
 const prior=root.NSArtR14;
 const name=s=>s&&s.startsWith('r14_')?'r16_'+s.slice(4):null;
 const api=Object.freeze({
   assetKeys:()=>prior.assetKeys().map(name),
   building:(id,face)=>name(prior.building(id,face)),
   hero:(face,frame)=>name(prior.hero(face,frame)),
   guard:(face,frame)=>name(prior.guard(face,frame)),
   boss:(id,face,frame)=>name(prior.boss(id,face,frame)),
   visualOnly:true,approved:false,status:'ART_CANDIDATE_EDGE_REFINEMENT_ONLY'
 });
 root.NSArtR16=api;
 if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(typeof globalThis!=='undefined'?globalThis:this);
