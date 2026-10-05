// Small access notch under the front box edge; dimensions in scene metres.
export const notch={min:[4.619,.952,-.095],max:[4.699,.985,.010]};
export function clipGripNotch(T,g,m){
 const p=g.attributes.position,idx=g.index,out=[],inv=m.clone().invert();
 const planes=[[0,notch.min[0],true],[0,notch.max[0],false],[1,notch.min[1],true],[1,notch.max[1],false],[2,notch.min[2],true],[2,notch.max[2],false]];
 function clip(poly,axis,value,greater){const r=[];for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length],da=(a.getComponent(axis)-value)*(greater?1:-1),db=(b.getComponent(axis)-value)*(greater?1:-1);if(da>=0)r.push(a);if((da>=0)!==(db>=0))r.push(a.clone().lerp(b,da/(da-db)));}return r;}
 function emit(poly){for(let j=1;j<poly.length-1;j++)for(const v of [poly[0],poly[j],poly[j+1]])out.push(...v.clone().applyMatrix4(inv).toArray());}
 for(let i=0;i<(idx?idx.count:p.count);i+=3){let poly=[0,1,2].map(k=>new T.Vector3().fromBufferAttribute(p,idx?idx.getX(i+k):i+k).applyMatrix4(m));for(const [axis,value,greater]of planes){emit(clip(poly,axis,value,!greater));poly=clip(poly,axis,value,greater);if(poly.length<3)break;}}
 for(const k of Object.keys(g.attributes))g.deleteAttribute(k);g.setIndex(null);g.setAttribute('position',new T.Float32BufferAttribute(out,3));g.computeVertexNormals();g.computeBoundingBox();g.boundsTree=null;
}

