// Append the native approved UR10e without changing any source-machine geometry.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import {fileURLToPath} from 'node:url';
import * as T from './vendor/three.mjs';
import {Rig} from './vendor/rig.mjs';
const HERE=path.dirname(fileURLToPath(import.meta.url));
const input=process.argv[2],output=process.argv[3];
function parse(b){const l=b.readUInt32LE(12);return {j:JSON.parse(b.subarray(20,20+l)),bin:b.subarray(28+l,28+l+b.readUInt32LE(20+l))};}
const {j:g,bin}=parse(fs.readFileSync(input));
const chunks=[bin];let off=bin.length;
function bytes(b){if(off%4){const p=Buffer.alloc(4-off%4);chunks.push(p);off+=p.length;}const n=off;chunks.push(b);off+=b.length;return n;}
const r=parse(fs.readFileSync(path.join(HERE,'inputs/ur10e_short.glb'))),no=g.nodes.length,mo=g.meshes.length,ao=g.accessors.length,vo=g.bufferViews.length,ro=g.materials.length,bo=bytes(r.bin);
for(const v of r.j.bufferViews)g.bufferViews.push({...v,buffer:0,byteOffset:bo+(v.byteOffset||0)});
for(const a of r.j.accessors)g.accessors.push({...a,bufferView:a.bufferView+vo});
for(const m of r.j.meshes)g.meshes.push({...m,primitives:m.primitives.map(p=>({...p,attributes:Object.fromEntries(Object.entries(p.attributes).map(([k,v])=>[k,v+ao])),...(p.indices!=null?{indices:p.indices+ao}:{}),...(p.material!=null?{material:p.material+ro}:{})}))});
g.materials.push(...(r.j.materials||[]));
for(const n of r.j.nodes)g.nodes.push({...n,name:'UR10E_'+n.name,...(n.mesh!=null?{mesh:n.mesh+mo}:{}),...(n.children?{children:n.children.map(i=>i+no)}:{}),extras:{kat:'ROBOT',mek:'Robot/UR10e'}});
g.scenes[g.scene||0].nodes.push(g.nodes.length);
g.nodes.push({name:'ROBOT_UR10E_NATIVE',rotation:[-Math.SQRT1_2,0,0,Math.SQRT1_2],children:r.j.scenes[r.j.scene||0].nodes.map(i=>i+no)});
const data=JSON.parse(fs.readFileSync(path.join(HERE,'inputs/rig.json'))),grid=JSON.parse(fs.readFileSync(path.join(HERE,'inputs/qr_grid_v13.json')));
const rig=new Rig(data,{mountForward:.1,railForward:.5});
const state=grid.results.find(x=>x.floor_mm===1112&&x.column===1).tasks.find(x=>x.key==='Cola').state;
const w=rig.matrices(state.q,state.rail,state.jaw);
for(const [body,name]of Object.entries(data.body_nodes)){
 const n=g.nodes[no+r.j.nodes.findIndex(n=>n.name===name)],m=new T.Matrix4().set(...w[body]);
 const p=new T.Vector3(),q=new T.Quaternion(),s=new T.Vector3();m.decompose(p,q,s);
 delete n.matrix;n.translation=p.toArray();n.rotation=q.toArray();n.scale=s.toArray();
}
if(off%4){chunks.push(Buffer.alloc(4-off%4));off+=4-off%4;}
g.buffers=[{byteLength:off}];g.scenes[g.scene||0].extras.robotQRStep62.robot={type:'UR10e',units:'m',state,railForward_m:.5,mountForward_m:.1,kinematic_only:true};
const b0=Buffer.from(JSON.stringify(g)),b=Buffer.concat([b0,Buffer.alloc((4-b0.length%4)%4,32)]),header=Buffer.alloc(20),bh=Buffer.alloc(8);
header.writeUInt32LE(0x46546c67,0);header.writeUInt32LE(2,4);header.writeUInt32LE(28+b.length+off,8);header.writeUInt32LE(b.length,12);header.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(off,0);bh.writeUInt32LE(0x004e4942,4);
const raw=Buffer.concat([header,b,bh,...chunks]);fs.writeFileSync(output,raw);
const packed=zlib.gzipSync(raw,{level:9});fs.writeFileSync(output+'.gz',packed);
const manifest={step:62,model:'hat3_v10d',raw_bytes:raw.length,raw_sha256:crypto.createHash('sha256').update(raw).digest('hex'),gzip_bytes:packed.length,robot:'UR10e',qr:[3,4],layout_only:true,production_ready:false,physics:false};
fs.writeFileSync(output+'.manifest.json',JSON.stringify(manifest,null,2)+'\n');console.log(JSON.stringify(manifest));
