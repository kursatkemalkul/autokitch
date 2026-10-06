// Append only shop geometry; preserve source machine/QR/robot and animation bytes.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import * as T from '../robot_integrated_v22/vendor/three.mjs';
import {cableMesh,sweep,ductMesh} from '../robot_integrated_v25/sweep.mjs';
const A='otonom/hat3d/robot-integrated-v27/',LOCAL='_local/codex_robot_v27/';
const input=process.argv[2]||'otonom/hat3d/robot-integrated-v26/hat3_robot_v27.glb.gz';
let raw=fs.readFileSync(input);if(raw[0]===31&&raw[1]===139)raw=zlib.gunzipSync(raw);
const jl=raw.readUInt32LE(12),g=JSON.parse(raw.subarray(20,20+jl)),bin=raw.subarray(28+jl,28+jl+raw.readUInt32LE(20+jl));
const original=structuredClone(g),plan=JSON.parse(fs.readFileSync(A+'floor_plan.json'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),pad=n=>(n+3)&~3;
const chunks=[bin];let offset=bin.length;
const newParts=[],removed=[];
g.scenes[g.scene||0].nodes=g.scenes[g.scene||0].nodes.filter(i=>{const drop=/^(DUKKAN26_|ROBOT25_(ZEMIN_TEMIZ_|GOMULU_KANAL_|ZEMIN_SIFIR_KAPAK_|CIKIS_SIFIR_YAKA_|KAPAK_DERZ_DESTEK_|SAG_DUVAR_KOSE_CIZGI_)|ROBOT25_UR_CIKIS$)/.test(g.nodes[i].name||'');if(drop)removed.push(g.nodes[i].name);return !drop;});
function acc(values,size,type=5126,target=34962){const a=type===5125?new Uint32Array(values):new Float32Array(values),b=Buffer.from(a.buffer);if(offset%4){const p=Buffer.alloc(pad(offset)-offset);chunks.push(p);offset+=p.length;}const vi=g.bufferViews.length;g.bufferViews.push({buffer:0,byteOffset:offset,byteLength:b.length,target});chunks.push(b);offset+=b.length;const lo=Array(size).fill(Infinity),hi=Array(size).fill(-Infinity);for(let i=0;i<a.length;i++){lo[i%size]=Math.min(lo[i%size],a[i]);hi[i%size]=Math.max(hi[i%size],a[i]);}const ai=g.accessors.length;g.accessors.push({bufferView:vi,componentType:type,count:a.length/size,type:size===1?'SCALAR':'VEC'+size,min:lo,max:hi});return ai;}
const materials=new Map();
function material(color,alpha=1){const key=color+':'+alpha;if(materials.has(key))return materials.get(key);const id=g.materials.length;g.materials.push({name:'FLOOR27_'+key,pbrMetallicRoughness:{baseColorFactor:[(color>>16&255)/255,(color>>8&255)/255,(color&255)/255,alpha],metallicFactor:color===0xb9c3c8?.7:0,roughnessFactor:.7},...(alpha<1?{alphaMode:'BLEND',doubleSided:true}:{})});materials.set(key,id);return id;}
function add(name,geo,color,at=[0,0,0],note='generic planning envelope',alpha=1){geo.computeVertexNormals();const p={attributes:{POSITION:acc(geo.attributes.position.array,3),NORMAL:acc(geo.attributes.normal.array,3)},indices:acc(geo.index?.array||Array.from({length:geo.attributes.position.count},(_,i)=>i),1,5125,34963),material:material(color,alpha)};const mi=g.meshes.length,ni=g.nodes.length;g.meshes.push({name:'FLOOR27_'+name,primitives:[p]});g.nodes.push({name:'FLOOR27_'+name,mesh:mi,translation:at,extras:{kat:/ZEMIN|DUVAR/.test(name)?'DUKKAN':'GUC',mek:/ZEMIN|DUVAR/.test(name)?'Çevre/Dükkân hattı':'Robot/Elektrik',part:name,connection:note,version:27}});g.scenes[g.scene||0].nodes.push(ni);const a=p.attributes.POSITION;const b=g.accessors[a];newParts.push({name:g.nodes[ni].name,node:ni,mesh:mi,lo:b.min.map((v,i)=>v+at[i]),hi:b.max.map((v,i)=>v+at[i]),connection:note});return ni;}
const box=(name,lo,hi,c=0xb9c3c8,note)=>add(name,new T.BoxGeometry(...hi.map((v,i)=>v-lo[i])),c,lo.map((v,i)=>(v+hi[i])/2),note);
const line=(name,a,b,c=0x72838c,r=.002)=>add(name,cableMesh([a,b],r),c,[0,0,0],'visual architectural boundary; no opaque wall');
function outline(name,lo,hi,color=0x72838c){for(const axis of [0,1,2])for(let j=0;j<4;j++){const other=[0,1,2].filter(x=>x!==axis),a=[...lo],b=[...lo];b[axis]=hi[axis];for(let k=0;k<2;k++)a[other[k]]=b[other[k]]=(j&(1<<k))?hi[other[k]]:lo[other[k]];if(a.some((v,i)=>v!==b[i]))line(name+'_'+axis+'_'+j,a,b,color);}}
function shape(poly){const s=new T.Shape(poly.outer.map(p=>new T.Vector2(...p)));for(const h of poly.holes)s.holes.push(new T.Path(h.map(p=>new T.Vector2(...p))));return s;}
// Split cap bridge edges at collinear polygon vertices: remove true T-junctions.
function closeCapEdges(geo){
 const v=geo.attributes.position.array,unique=new Map();
 for(let i=0;i<v.length/3;i++){const key=[v[i*3],v[i*3+1],v[i*3+2]].map(x=>Math.round(x*1e7)).join('/');if(!unique.has(key))unique.set(key,i);}
 const candidates=[...unique.values()],src=geo.index?.array||Array.from({length:v.length/3},(_,i)=>i),out=[];
 const point=i=>[v[i*3],v[i*3+1],v[i*3+2]];
 function split(a,b,c,depth=0){
  if(depth>20)throw Error('Unresolved cap subdivision');
  for(const [s,e,k]of [[a,b,c],[b,c,a],[c,a,b]]){
   const p=point(s),q=point(e),d=q.map((x,i)=>x-p[i]),len=d.reduce((x,y)=>x+y*y,0);if(len<1e-15)continue;
   let found=null,best=1;
   for(const j of candidates){if(j===s||j===e||j===k)continue;const r=point(j),t=r.reduce((sum,x,i)=>sum+(x-p[i])*d[i],0)/len;
    if(t<1e-6||t>1-1e-6)continue;const ds=r.reduce((sum,x,i)=>sum+(x-p[i]-t*d[i])**2,0);
    if(ds<2.5e-13&&t<best){found=j;best=t;}}
   if(found!=null){split(s,found,k,depth+1);split(found,e,k,depth+1);return;}
  }
  out.push(a,b,c);
 }
 for(let i=0;i<src.length;i+=3)split(src[i],src[i+1],src[i+2]);
 geo.setIndex(out);return geo;
}
function surface(name,polys,t,top,col=0xa8afb3,note='catalogue channel part; butt joint, supported in screed'){
 for(const [i,p] of polys.entries()){const geo=new T.ExtrudeGeometry(shape(p),{depth:t,bevelEnabled:false});geo.rotateX(Math.PI/2);if(p.holes.length>1)closeCapEdges(geo);add(name+'_'+i,geo,col,[0,top,0],note);}
}
surface('ZEMIN',plan.floor,.010,0,0xdbdbd6,'compact continuous floor, old sink bores and former channel footprint filled');
for(const m of plan.modules){
 surface(m.name+'_TABAN',m.bottom,.0015,-.0985);
 surface(m.name+'_YAN',m.side,.0955,-.003);
 surface(m.name+'_AYIRICI',m.divider,.0015,-.0375,0x99a5ae,'separate mains/data tiers; apertures only at actual equipment risers');
 surface(m.name+'_KAPAK',m.cover,.003,0,0xc1c6c8,'flush removable cover, nominal catalogue layout; load approval pending');
 surface(m.name+'_KAPAK_DESTEK',m.ledge,.0015,-.003,0x99a5ae,'continuous ledge at inner wall face; cover supported');
}
const exitSpec=JSON.parse(fs.readFileSync('otonom/hat3d/robot-integrated-v25/floor_plan.json')).duct_specs.find(x=>x.name==='UR_CIKIS');exitSpec.width_m=.080;add('UR_KONTROL_CIKIS_80',ductMesh(exitSpec),0xa9b4bc,[0,0,0],'80x70 hollow exit sleeve; unchanged controller gland and cable');
surface('CIKIS_YAKA',plan.flush_collars,.003,0,0xc1c6c8,'flush collar, actual equipment throat cutout; no empty floor holes');
outline('SAG_DUVAR',[5.360,0,-.88],[5.360,2.4,2.17]);
outline('ARKA_DUVAR',[.636,0,-.88],[5.36,2.4,-.88]);
// Strip inactive-only materials, as required by the main model material controls.
const used=new Set(),visit=i=>{const n=g.nodes[i];if(n.mesh!=null)for(const p of g.meshes[n.mesh].primitives)if(p.material!=null)used.add(p.material);for(const c of n.children||[])visit(c);};for(const i of g.scenes[g.scene||0].nodes)visit(i);
const map=new Map([...used].sort((a,b)=>a-b).map((a,i)=>[a,i]));g.materials=[...map.keys()].map(i=>g.materials[i]);for(const m of g.meshes)for(const p of m.primitives)if(p.material!=null)p.material=map.get(p.material)??0;
if(offset%4)chunks.push(Buffer.alloc(pad(offset)-offset));const outBin=Buffer.concat(chunks);g.buffers[0].byteLength=outBin.length;
g.asset.generator='AUTOKITCH v27 compact floor and standard channel layout';delete g.scenes[g.scene||0].extras.shopIntegration;g.scenes[g.scene||0].extras.floorIntegration={version:27,source_sha256:sha(raw),motion_changed:false};
const j0=Buffer.from(JSON.stringify(g)),j=Buffer.concat([j0,Buffer.alloc(pad(j0.length)-j0.length,32)]),h=Buffer.alloc(20),bh=Buffer.alloc(8);h.writeUInt32LE(0x46546c67,0);h.writeUInt32LE(2,4);h.writeUInt32LE(28+j.length+outBin.length,8);h.writeUInt32LE(j.length,12);h.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(outBin.length,0);bh.writeUInt32LE(0x004e4942,4);const output=Buffer.concat([h,j,bh,outBin]);
fs.mkdirSync(LOCAL,{recursive:true});fs.writeFileSync(LOCAL+'combined_meshopt.glb',output);fs.writeFileSync(A+'hat3_robot_v27.glb.gz',zlib.gzipSync(output,{level:9}));
if(process.argv[3]){fs.mkdirSync(path.dirname(process.argv[3]),{recursive:true});fs.writeFileSync(process.argv[3],output);}
const oldManifest=JSON.parse(fs.readFileSync('otonom/hat3d/robot-integrated-v26/manifest.json'));
const proof={version:27,source_input:input,source_sha256:sha(raw),source_binary_preserved:outBin.subarray(0,bin.length).equals(bin),original_node_count:original.nodes.length,original_mesh_count:original.meshes.length,removed_roots:removed,new_parts:newParts,animations_unchanged:JSON.stringify(g.animations)===JSON.stringify(original.animations),raw_web_sha256:sha(output),raw_web_bytes:output.length,gzip_sha256:sha(fs.readFileSync(A+'hat3_robot_v27.glb.gz')),gzip_bytes:fs.statSync(A+'hat3_robot_v27.glb.gz').size,passed:true};
if(!proof.source_binary_preserved||!proof.animations_unchanged)throw Error('Source geometry or animation changed');
fs.writeFileSync(A+'manifest.json',JSON.stringify({...oldManifest,version:27,raw_web_sha256:proof.raw_web_sha256,raw_web_bytes:proof.raw_web_bytes,gzip_bytes:proof.gzip_bytes,combined_nodes:g.nodes.length,shop:{removed:true},floor:plan,floor_source_sha256:proof.source_sha256,services:{...oldManifest.services,floor_plan:plan,shop:{removed:true}},known_open:[...oldManifest.known_open,...plan.open]},null,2));
fs.writeFileSync(A+'floor_build.json',JSON.stringify(proof,null,2));console.log(JSON.stringify({...proof,new_parts:newParts.length,removed_roots:removed.length}));
