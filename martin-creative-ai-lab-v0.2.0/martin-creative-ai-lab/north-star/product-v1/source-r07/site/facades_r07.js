/* Fail-closed facade art selection. Painting all 4 directions is REQUIRED before
 * an authored multi-view house can replace R04's illustrated fallback.
 * A rotated or mirrored copy of the same painting does not pass this gate.
 */
(function(root){'use strict';
const fallback=Object.freeze({1:'r04_cottage',2:'r04_forge',3:'r04_apothecary'});
const ids=Object.freeze([1,2,3]);
function validManifest(manifest,id){
 if(!ids.includes(id)||!manifest||manifest.state!=='AUTHOR_ART_APPROVED')return false;
 const item=manifest.buildings?.[id];
 if(!item||item.license_checked!==true||item.scale_anchor_reviewed!==true)return false;
 const files=item.faces,hashes=item.sha256;
 if(!Array.isArray(files)||files.length!==4||!Array.isArray(hashes)||hashes.length!==4)return false;
 if(files.some((f,i)=>typeof f!=='string'||!/^r07_([a-z]+)_[0-3]$/.test(f)||!f.endsWith('_'+i)))return false;
 if(hashes.some(h=>typeof h!=='string'||!/^[0-9a-f]{64}$/.test(h)))return false;
 if(new Set(files).size!==4||new Set(hashes).size!==4)return false;
 return true;
}
function resolve(id,quarter,manifest,images){
 if(!ids.includes(id))throw new RangeError('unknown structure ID');
 if(!Number.isSafeInteger(quarter)||quarter<0||quarter>3)throw new RangeError('invalid camera view');
 const expected=fallback[id];
 if(!validManifest(manifest,id))return {name:expected,source:'R04_FALLBACK',approved:false};
 const face=manifest.buildings[id].faces[quarter];
 const image=images?.[face];
 if(!image||!image.complete||!image.naturalWidth)return {name:expected,source:'R04_FALLBACK_MISSING_TEXTURE',approved:false};
 return {name:face,source:'AUTHOR_APPROVED_FOUR_FACE',approved:true};
}
const api=Object.freeze({fallback,ids,validManifest,resolve});
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.NSFacadeR07=api;
})(typeof globalThis!=='undefined'?globalThis:this);
