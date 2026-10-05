export const replaced=n=>/^(?:DUZ_TEZGAH|TEZGAH_)/.test(n)||n==='ROBOT_RAY'||n.startsWith('ROBOT_ZINCIR_OLUGU')||n==='A_ONYUZ__on_seffaf__SERVIS_KAPAGI'||n.startsWith('QR_')||n.startsWith('ELK_QR')||n.startsWith('ROBOT_ENERJI_ZINCIRI')||n.startsWith('ROBOT_KABLOSU')||n.startsWith('ROBOT_KABLO_KOPRUSU');
const stops=[[4.500,4.555],[4.585,4.645],[4.675,4.735],[4.765,4.805]];
export function removeFrontStops(T,g,m,name){if(!name.startsWith('E_KALIP__'))return 0;const p=g.attributes.position,idx=g.index,keep=[],v=new T.Vector3();let count=0;for(let i=0;i<(idx?idx.count:p.count);i+=3){const ids=[0,1,2].map(k=>idx?idx.getX(i+k):i+k),pts=ids.map(id=>v.fromBufferAttribute(p,id).applyMatrix4(m).clone());const remove=stops.some(([x0,x1])=>pts.every(v=>v.x>=x0-.0002&&v.x<=x1+.0002&&v.y>=.9178&&v.y<=.9817&&v.z>=-.0441&&v.z<=-.0377));if(remove)count++;else keep.push(...ids);}if(count){g.setIndex(keep);g.computeBoundingBox();g.boundsTree=null;}return count;}
export const cableChannel={name:'ROBOT_V4_COVERED_CABLE_CHANNEL',min:[.936,.012,.495],max:[5.1,.055,.565]};
export const mountAdapter={name:'ROBOT_V4_MOUNT_ADAPTER',min:[-.12,-.22,.011],max:[.12,.12,.035]}; // Carriage-local Isaac coordinates; 100mm forward offset, base height unchanged.
export const boxSupportParts=[];
export const stationShift=name=>/^(?:DUZ_TEZGAH|TEZGAH_)/.test(name)?.30:0;
// Robot-side box pickup aperture in the existing E front cover. Retain all outside faces.
export function boxPickupWindow(T,g,m,name){
 if(name!=='E_GOVDE__on_seffaf')return;
 const planes=[[0,4.484,true],[0,4.834,false],[1,.965,true],[1,1.130,false],[2,.040,true],[2,.090,false]],p=g.attributes.position,idx=g.index,out=[],inv=m.clone().invert();
 function clip(poly,axis,value,greater){const result=[];for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length],da=(a.getComponent(axis)-value)*(greater?1:-1),db=(b.getComponent(axis)-value)*(greater?1:-1);if(da>=0)result.push(a);if((da>=0)!==(db>=0))result.push(a.clone().lerp(b,da/(da-db)));}return result;}
 function emit(poly){for(let j=1;j<poly.length-1;j++)for(const v of [poly[0],poly[j],poly[j+1]])out.push(...v.clone().applyMatrix4(inv).toArray());}
 for(let i=0;i<(idx?idx.count:p.count);i+=3){let poly=[0,1,2].map(k=>new T.Vector3().fromBufferAttribute(p,idx?idx.getX(i+k):i+k).applyMatrix4(m));for(const [axis,value,greater] of planes){emit(clip(poly,axis,value,!greater));poly=clip(poly,axis,value,greater);if(poly.length<3)break;}}
 for(const key of Object.keys(g.attributes))g.deleteAttribute(key);g.setIndex(null);g.setAttribute('position',new T.Float32BufferAttribute(out,3));g.computeVertexNormals();g.computeBoundingBox();g.boundsTree=null;
}


