/* North Star 4-view camera: purely observational, no gameplay authority.
 * 0,1,2,3 are quarter-turns relative to the authored world axes.
 * Clockwise positive in the screen presentation (not world mutation).
 * 2026-11-15 / NS-CAM-4VIEW-001 / MIT-style demo code, not final art.
 */
(function (root) {
  'use strict';
  function validQuarter(value) {
    if (!Number.isSafeInteger(value)) throw new RangeError('camera quarter must be a safe integer');
    return ((value % 4) + 4) % 4;
  }
  function turn(quarter, delta) {
    if (delta !== 1 && delta !== -1) throw new RangeError('turn must be one quarter clockwise or counterclockwise');
    return validQuarter(validQuarter(quarter) + delta);
  }
  function rotateGrid(x, y, quarter, cols, rows) {
    if (![x, y, cols, rows].every(Number.isFinite) || cols < 1 || rows < 1)
      throw new RangeError('invalid camera coordinates/grid');
    const u = x - (cols - 1) / 2;
    const v = y - (rows - 1) / 2;
    switch (validQuarter(quarter)) {
      case 0: return {u, v};
      case 1: return {u: -v, v: u};
      case 2: return {u: -u, v: -v};
      case 3: return {u: v, v: -u};
    }
  }
  function project(x, y, quarter, cols, rows, centerX=584, centerY=305, halfWidth=44, halfHeight=24) {
    if (![centerX, centerY, halfWidth, halfHeight].every(Number.isFinite) || halfWidth <= 0 || halfHeight <= 0)
      throw new RangeError('invalid projection');
    const {u, v} = rotateGrid(x, y, quarter, cols, rows);
    return {x: centerX + (u - v)*halfWidth, y: centerY + (u + v)*halfHeight};
  }
  function orderedTiles(cols, rows, quarter) {
    if (!Number.isSafeInteger(cols) || !Number.isSafeInteger(rows) || cols < 1 || rows < 1 || cols * rows > 10000)
      throw new RangeError('invalid board dimensions');
    const tiles=[];
    for(let y=0;y<rows;y++) for(let x=0;x<cols;x++) tiles.push({x,y,p:project(x,y,quarter,cols,rows)});
    return tiles.sort((a,b)=>a.p.y-b.p.y || a.p.x-b.p.x || a.y-b.y || a.x-b.x);
  }
  const api=Object.freeze({validQuarter, turn, rotateGrid, project, orderedTiles});
  if (typeof module!=='undefined' && module.exports) module.exports=api;
  else root.NSCamera4=api;
})(typeof globalThis!=='undefined' ? globalThis : this);
