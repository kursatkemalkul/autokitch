import fs from 'node:fs';
import * as T from './vendor/three.mjs';
import {MeshBVH} from './vendor/bvh.mjs';
import {Rig} from '../../../otonom/hat/robot-main-v1/rig.js';
export {T};
export const root='otonom/hat3d/robot-main-v1/';
export const read=n=>JSON.parse(fs.readFileSync(root+n,'utf8'));
export const rig=new Rig(read('rig.json'),{mountForward:.10}), poses=read('poses.json');
export const C=new T.Matrix4().makeRotationX(-Math.PI/2), matrix=a=>new T.Matrix4().set(...a);
export function clean(g){const p=g.attributes.position,idx=g.index,k=[],tr=new T.Triangle();for(let i=0;i<(idx?idx.count:p.count);i+=3){const ids=[0,1,2].map(j=>idx?idx.getX(i+j):i+j);[tr.a,tr.b,tr.c].forEach((v,j)=>v.fromBufferAttribute(p,ids[j]));if(tr.getArea()>1e-12)k.push(...ids);}g.setIndex(k);g.computeBoundingBox();return g;}
export function solid(name,g,m=new T.Matrix4(),body=null){clean(g);return {name,g,m,body,box:g.boundingBox.clone().applyMatrix4(m),bvh:null};}
export function box(name,min,max){const lo=new T.Vector3(...min),hi=new T.Vector3(...max),s=hi.clone().sub(lo);return solid(name,new T.BoxGeometry(s.x,s.y,s.z),new T.Matrix4().makeTranslation(...lo.add(hi).multiplyScalar(.5).toArray()));}
export function loadGLB(path){const b=fs.readFileSync(path),len=b.readUInt32LE(12),j=JSON.parse(b.subarray(20,20+len).toString()),bin=b.subarray(28+len);const out=[];function acc(id){const a=j.accessors[id],v=j.bufferViews[a.bufferView],n={SCALAR:1,VEC2:2,VEC3:3,VEC4:4,MAT4:16}[a.type],f={5126:['getFloat32',4],5125:['getUint32',4],5123:['getUint16',2],5121:['getUint8',1]}[a.componentType],dv=new DataView(bin.buffer,bin.byteOffset,bin.byteLength),res=[];for(let i=0;i<a.count;i++)for(let k=0;k<n;k++)res.push(dv[f[0]]((v.byteOffset||0)+(a.byteOffset||0)+i*(v.byteStride||n*f[1])+k*f[1],true));return res;}
 function node(id,parent){const n=j.nodes[id],m=n.matrix?new T.Matrix4().fromArray(n.matrix):new T.Matrix4().compose(new T.Vector3(...(n.translation||[0,0,0])),new T.Quaternion(...(n.rotation||[0,0,0,1])),new T.Vector3(...(n.scale||[1,1,1])));m.premultiply(parent);if(n.mesh!=null)for(const p of j.meshes[n.mesh].primitives){const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(acc(p.attributes.POSITION),3));if(p.indices!=null)g.setIndex(acc(p.indices));out.push(solid(n.name||j.meshes[n.mesh].name,g,m.clone()));}for(const c of n.children||[])node(c,m);}
 for(const n of j.scenes[j.scene||0].nodes)node(n,new T.Matrix4());return out;
}
export const robot=read('collision.json').map(s=>{const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(s.vertices.flat(),3));g.setIndex(s.faces.flat());const a=solid(s.path,g,new T.Matrix4(),s.body);a.bvh=new MeshBVH(g);g.boundsTree=a.bvh;return a;});
export const machine=loadGLB('otonom/hat3d/v3/hat3_v7.glb').filter(s=>!['ROBOT_1','ROBOT_1_KOL'].includes(s.name));
export function update(s,m){s.m=m;s.box.copy(s.g.boundingBox).applyMatrix4(m);}
export function intersects(a,b){if(!a.box.intersectsBox(b.box))return false;if(!a.bvh){a.bvh=new MeshBVH(a.g);a.g.boundsTree=a.bvh;}if(!b.bvh){b.bvh=new MeshBVH(b.g);b.g.boundsTree=b.bvh;}a.g.boundsTree=a.bvh;b.g.boundsTree=b.bvh;return a.bvh.intersectsGeometry(b.g,a.m.clone().invert().multiply(b.m));}
export function hits(state,obstacles=machine,limit=1){const w=rig.matrices(state.q,state.rail,state.jaw);for(const a of robot)update(a,C.clone().multiply(matrix(w[a.body])));const h=[];for(const a of robot){for(const b of obstacles){if(intersects(a,b)){h.push(a.body.split('/').pop()+' > '+b.name);if(h.length>=limit)return h;}}}for(let i=0;i<robot.length;i++)for(let j=i+1;j<robot.length;j++){const a=robot[i],b=robot[j];if(a.body===b.body||rig.adjacent.has([a.body,b.body].sort().join('|'))||a.body.includes('/Gripper/')&&b.body.includes('/Gripper/'))continue;if(intersects(a,b)){h.push(a.body.split('/').pop()+' > '+b.body.split('/').pop());if(h.length>=limit)return h;}}return h;}




