import fs from 'node:fs';
import crypto from 'node:crypto';
const root='_local/codex_robot_v20/',out='otonom/hat3d/robot-integrated-v18/';
function parse(p){const b=fs.readFileSync(p),l=b.readUInt32LE(12);return{j:JSON.parse(b.subarray(20,20+l)),bin:b.subarray(28+l,28+l+b.readUInt32LE(20+l))};}
const a=parse(root+'published_with_qr.glb'),b=parse(root+'combined_native.glb'),m=JSON.parse(fs.readFileSync(out+'manifest.json')),errors=[];
const roots=new Set(b.j.scenes[b.j.scene||0].nodes),splits=new Set(m.stock_split.map(s=>s.source));
for(let i=0;i<a.j.nodes.length;i++){
 if(JSON.stringify(a.j.nodes[i])!==JSON.stringify(b.j.nodes[i]))errors.push('Changed source node '+i);
 if(a.j.scenes[a.j.scene||0].nodes.includes(i)&&!roots.has(i)&&!(/^(ROBOT_UR10E_NATIVE$|TEZGAH_|DUZ_TEZGAH)/.test(a.j.nodes[i].name||'')||(i<JSON.parse(fs.readFileSync(out+'source_provenance.json')).publishedNodeCount&&/^(QR_|ELK_QR)/.test(a.j.nodes[i].name||''))))errors.push('Missing source root '+i);
}
if(Buffer.compare(a.bin,b.bin.subarray(0,a.bin.length)))errors.push('Source geometry buffer changed');
function values(g,id){const x=g.j.accessors[id],v=g.j.bufferViews[x.bufferView],size={SCALAR:1,VEC3:3,VEC4:4}[x.type],f={5126:['readFloatLE',4],5125:['readUInt32LE',4],5123:['readUInt16LE',2]}[x.componentType],r=[];for(let i=0;i<x.count;i++)for(let k=0;k<size;k++)r.push(g.bin[f[0]]((v.byteOffset||0)+(x.byteOffset||0)+i*(v.byteStride||size*f[1])+k*f[1]));return r;}
const triangles=x=>{const r=[];for(let i=0;i<x.length;i+=3)r.push(x.slice(i,i+3).join(','));return r.sort();};
for(let i=0;i<a.j.meshes.length;i++){
 const node=a.j.nodes.find(n=>n.mesh===i),changed=splits.has(node?.name);
 for(let k=0;k<a.j.meshes[i].primitives.length;k++){
  const p=a.j.meshes[i].primitives[k],q=b.j.meshes[i].primitives[k];
  if(JSON.stringify(p.attributes)!==JSON.stringify(q.attributes))errors.push('Vertex accessor changed '+i);
  if(p.indices!==q.indices){
   if(!changed){errors.push('Unexpected triangle split '+i);continue;}
   const key=m.stock_split.find(s=>s.source===node.name).product,newMesh=b.j.meshes.find(x=>x.name==='ROBOT18_'+key+'_stock_shape');
   const original=triangles(values(a,p.indices)),union=triangles([...values(b,q.indices),...values(b,newMesh.primitives[k].indices)]);
   if(JSON.stringify(original)!==JSON.stringify(union))errors.push('Stock triangle union differs '+key);
  }
 }
}
const checks=[];
for(const s of m.orders){
 const clip=b.j.animations.find(x=>x.name==='siparis_'+s.kod);if(!clip){errors.push('Missing clip '+s.recipe);continue;}
 const body=clip.channels.find(c=>b.j.nodes[c.target.node].name==='UR10E_body_00'&&c.target.path==='translation'),carriage=clip.channels.find(c=>b.j.nodes[c.target.node].name==='UR10E_body_07'&&c.target.path==='translation');
 if(!body||!carriage){errors.push('No robot/carriage channels '+s.recipe);continue;}
 const positions=values(b,clip.samplers[carriage.sampler].output),x=positions.filter((_,i)=>i%3===0),times=values(b,clip.samplers[carriage.sampler].input);
 if(Math.max(...x)-Math.min(...x)<2)errors.push('Rail does not travel '+s.recipe);
 if(x.some(v=>v<.936-.001||v>5.1+.001))errors.push('Rail centre outside envelope '+s.recipe);
 for(let i=1;i<times.length;i++)if(times[i]<=times[i-1])errors.push('Non-increasing clock '+s.recipe);
 for(const key of ['Dough','Cola','Dessert','Box'])if(!clip.channels.some(c=>b.j.nodes[c.target.node].name==='ROBOT18_PRODUCT_'+key&&c.target.path==='translation'))errors.push('Missing product '+key);
 checks.push({recipe:s.recipe,channels:clip.channels.length,frames:times.length,rail_centre_min_m:Math.min(...x),rail_centre_max_m:Math.max(...x),gate:s.gate});
}
const rail=b.j.nodes.find(n=>n.name==='ROBOT18_RAY');if(!rail||!roots.has(b.j.nodes.indexOf(rail)))errors.push('No active rail');
if([...roots].some(i=>/^(TEZGAH_|DUZ_TEZGAH)/.test(b.j.nodes[i].name||'')))errors.push('Bench still active');
const report={published_source_sha256:m.published_source_sha256,removed_user_requested_bench:true,version:18,source_sha256:m.source_sha256,preserved_source_nodes:a.j.nodes.length,preserved_geometry_buffer_bytes:a.bin.length,stock_triangle_union_checked:true,orders:checks,errors,passed:!errors.length,scope:'geometry preservation and playable robot/rail/product channels only',full_collision_certified:false,production_ready:false};
fs.writeFileSync(out+'integration_audit.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));if(errors.length)process.exit(1);
