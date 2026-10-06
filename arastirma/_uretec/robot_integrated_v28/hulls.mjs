import fs from 'node:fs';
import * as T from '../robot_integrated_v22/vendor/three.mjs';
const A='otonom/hat3d/robot-integrated-v25/',raw=fs.readFileSync(A+'ur10e_short.glb'),jl=raw.readUInt32LE(12),g=JSON.parse(raw.subarray(20,20+jl)),bin=raw.subarray(28+jl);
const rig=JSON.parse(fs.readFileSync(A+'rig.json'));
const matrix=n=>n.matrix?new T.Matrix4().fromArray(n.matrix):new T.Matrix4().compose(new T.Vector3(...n.translation||[0,0,0]),new T.Quaternion(...n.rotation||[0,0,0,1]),new T.Vector3(...n.scale||[1,1,1]));
function points(id,m){const n=g.nodes[id],out=[];if(n.mesh!=null)for(const p of g.meshes[n.mesh].primitives){const a=g.accessors[p.attributes.POSITION],v=g.bufferViews[a.bufferView],pts=[];for(let i=0;i<a.count;i++){const off=(v.byteOffset||0)+(a.byteOffset||0)+i*(v.byteStride||12),pt=new T.Vector3(bin.readFloatLE(off),bin.readFloatLE(off+4),bin.readFloatLE(off+8)).applyMatrix4(m);pts.push(pt.toArray());}out.push(pts);}for(const c of n.children||[])out.push(...points(c,m.clone().multiply(matrix(g.nodes[c]))));return out;}
const shapes={};for(const [b,n] of Object.entries(rig.body_nodes))if(!b.endsWith('/Carriage')&&!b.endsWith('/RailBase'))shapes[b]=points(g.nodes.findIndex(x=>x.name===n),new T.Matrix4());
fs.writeFileSync('_local/codex_robot_v28/body_points.json',JSON.stringify(shapes));
console.log(JSON.stringify(Object.fromEntries(Object.entries(shapes).map(([k,v])=>[k.split('/').at(-1),v.map(x=>x.length)]))));
