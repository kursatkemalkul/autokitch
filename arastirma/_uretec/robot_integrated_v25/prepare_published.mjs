import fs from 'node:fs';
import zlib from 'node:zlib';
import crypto from 'node:crypto';
import {MeshoptDecoder} from '../robot_integrated_v22/meshopt/package/meshopt_decoder.mjs';
const OUT='_local/codex_robot_v25/',A='otonom/hat3d/robot-integrated-v25/';
fs.mkdirSync(OUT,{recursive:true});
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function parse(b){const l=b.readUInt32LE(12);return {j:JSON.parse(b.subarray(20,20+l)),bin:b.subarray(28+l,28+l+b.readUInt32LE(20+l))};}
function save(j,bin,file){const pad=n=>(n+3)&~3,j0=Buffer.from(JSON.stringify(j)),jb=Buffer.concat([j0,Buffer.alloc(pad(j0.length)-j0.length,32)]),bb=Buffer.concat([bin,Buffer.alloc(pad(bin.length)-bin.length)]),h=Buffer.alloc(20),bh=Buffer.alloc(8);j.buffers=[{byteLength:bb.length}];h.writeUInt32LE(0x46546c67,0);h.writeUInt32LE(2,4);h.writeUInt32LE(28+jb.length+bb.length,8);h.writeUInt32LE(jb.length,12);h.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(bb.length,0);bh.writeUInt32LE(0x004e4942,4);const b=Buffer.concat([h,jb,bh,bb]);fs.writeFileSync(file,b);return b;}
// Extract only the approved, unheated 3x4 QR, transferred devices and cell gate.
if(process.argv.includes('--extract-qr')){
 const {j:s,bin:sb}=parse(fs.readFileSync(OUT+'source62.glb'));
 const t={asset:{version:'2.0'},scene:0,scenes:[{nodes:[]}],nodes:[],meshes:[],materials:[],accessors:[],bufferViews:[],buffers:[{byteLength:0}]},chunks=[];let offset=0;
 const am=new Map(),mm=new Map(),mt=new Map(),nm=new Map();
 const ca=id=>{if(am.has(id))return am.get(id);const a=s.accessors[id],v=s.bufferViews[a.bufferView],b=sb.subarray(v.byteOffset||0,(v.byteOffset||0)+v.byteLength);if(offset%4){const p=Buffer.alloc(4-offset%4);chunks.push(p);offset+=p.length;}const vi=t.bufferViews.length;t.bufferViews.push({...v,buffer:0,byteOffset:offset});chunks.push(b);offset+=b.length;const ai=t.accessors.length;t.accessors.push({...a,bufferView:vi});am.set(id,ai);return ai;};
 const cm=id=>{if(mm.has(id))return mm.get(id);const m=s.meshes[id],mi=t.meshes.length;t.meshes.push({...m,primitives:m.primitives.map(p=>{let material;if(p.material!=null){if(!mt.has(p.material)){mt.set(p.material,t.materials.length);t.materials.push(s.materials[p.material]);}material=mt.get(p.material);}return {...p,attributes:Object.fromEntries(Object.entries(p.attributes).map(([k,a])=>[k,ca(a)])),indices:ca(p.indices),...(material!=null?{material}:{})};})});mm.set(id,mi);return mi;};
 const cn=id=>{if(nm.has(id))return nm.get(id);const n=s.nodes[id],ni=t.nodes.length;t.nodes.push({...n});nm.set(id,ni);if(n.mesh!=null)t.nodes[ni].mesh=cm(n.mesh);if(n.children)t.nodes[ni].children=n.children.map(cn);return ni;};
 for(const id of s.scenes[s.scene||0].nodes)if(/^(QR62_|CELL62_|QR_ROBOT_KONTROL|QR_UPS|QR_KILIT_KARTI|QR_MUSTERI_PANELI|ELK_QR_KUTU)/.test(s.nodes[id].name||''))t.scenes[0].nodes.push(cn(id));
 t.buffers=[{byteLength:(offset+3)&~3}];const temp=OUT+'qr_only.glb';const raw=save(t,Buffer.concat(chunks),temp);fs.writeFileSync(A+'qr_safety_native.glb.gz',zlib.gzipSync(raw,{level:9}));console.log('QR extracted',t.nodes.length,raw.length);
}
const published=fs.readFileSync('_local/codex_robot_v25/source_cleaned.glb');
// Exact upstream and removal evidence are recorded by clean_source.py.
const {j,bin}=parse(published);await MeshoptDecoder.ready;
const chunks=[];let offset=0;
for(const v of j.bufferViews){let b;const e=v.extensions?.EXT_meshopt_compression;if(e){b=Buffer.alloc(v.byteLength);MeshoptDecoder.decodeGltfBuffer(b,e.count,e.byteStride,bin.subarray(e.byteOffset,e.byteOffset+e.byteLength),e.mode,e.filter);}else b=bin.subarray(v.byteOffset||0,(v.byteOffset||0)+v.byteLength);if(offset%4){const p=Buffer.alloc(4-offset%4);chunks.push(p);offset+=p.length;}v.buffer=0;v.byteOffset=offset;delete v.extensions;chunks.push(b);offset+=b.length;}
j.extensionsUsed=(j.extensionsUsed||[]).filter(x=>x!=='EXT_meshopt_compression');j.extensionsRequired=(j.extensionsRequired||[]).filter(x=>x!=='EXT_meshopt_compression');
const publishedNodeCount=j.nodes.length,publishedMeshCount=j.meshes.length,publishedBinBytes=offset;
// Append separate QR source without changing a published machine node or accessor.
const {j:q,bin:qb}=parse(zlib.gunzipSync(fs.readFileSync(A+'qr_safety_native.glb.gz')));
if(offset%4){const p=Buffer.alloc(4-offset%4);chunks.push(p);offset+=p.length;}const qbo=offset,vo=j.bufferViews.length,ao=j.accessors.length,mo=j.meshes.length,no=j.nodes.length,mato=j.materials.length;
chunks.push(qb);offset+=qb.length;j.bufferViews.push(...q.bufferViews.map(v=>({...v,buffer:0,byteOffset:qbo+(v.byteOffset||0)})));j.accessors.push(...q.accessors.map(a=>({...a,bufferView:vo+a.bufferView})));j.materials.push(...q.materials);j.meshes.push(...q.meshes.map(m=>({...m,primitives:m.primitives.map(p=>({...p,attributes:Object.fromEntries(Object.entries(p.attributes).map(([k,a])=>[k,a+ao])),indices:p.indices+ao,material:p.material+mato}))})));j.nodes.push(...q.nodes.map(n=>({...n,...(n.mesh!=null?{mesh:n.mesh+mo}:{}),...(n.children?{children:n.children.map(i=>i+no)}:{})})));j.scenes[j.scene||0].nodes.push(...q.scenes[q.scene||0].nodes.map(i=>i+no));
j.buffers=[{byteLength:(offset+3)&~3}];const raw=save(j,Buffer.concat(chunks),OUT+'published_with_qr.glb');const report={published_sha256:sha(published),prepared_sha256:sha(raw),publishedNodeCount,publishedMeshCount,publishedBinBytes,qr_nodes:q.nodes.length,units:'metres, Y-up',qr_heating:false};fs.writeFileSync(A+'source_provenance.json',JSON.stringify(report,null,2));console.log(report);
