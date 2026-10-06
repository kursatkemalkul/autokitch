import fs from 'node:fs';
import crypto from 'node:crypto';
const root='_local/codex_robot_v23/',out='otonom/hat3d/robot-integrated-v23/';
function parse(p){const b=fs.readFileSync(p),l=b.readUInt32LE(12);return{j:JSON.parse(b.subarray(20,20+l)),bin:b.subarray(28+l,28+l+b.readUInt32LE(20+l))};}
const a=parse(root+'published_with_qr.glb'),b=parse(root+'combined_native.glb'),m=JSON.parse(fs.readFileSync(out+'manifest.json')),errors=[];
const roots=new Set(b.j.scenes[b.j.scene||0].nodes),splits=new Set(m.stock_split.map(s=>s.source));
for(let i=0;i<a.j.nodes.length;i++){
 if(JSON.stringify(a.j.nodes[i])!==JSON.stringify(b.j.nodes[i])&&a.j.nodes[i].name!=='QR_ROBOT_KONTROL__robot_kutu')errors.push('Changed source node '+i);
 if(a.j.scenes[a.j.scene||0].nodes.includes(i)&&!roots.has(i)&&!m.removed_service_nodes.includes(a.j.nodes[i].name))errors.push('Missing source root '+i);
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
   const key=m.stock_split.find(s=>s.source===node.name).product,newMesh=b.j.meshes.find(x=>x.name==='ROBOT23_'+key+'_stock_shape');
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
 const basePositions=values(b,clip.samplers[body.sampler].output);
 for(let i=0;i<positions.length;i+=3){
  // Native Isaac Y becomes -world Z. Manufacturer carriage centre is local Y=-.100.
  if(Math.abs(basePositions[i]-positions[i])>1e-6||Math.abs(basePositions[i+1]-(positions[i+1]-.100))>1e-6)errors.push('Robot/rail centre mismatch '+s.recipe+' frame '+i/3);
  if(Math.abs(basePositions[i+2]-.130)>1e-6)errors.push('Robot mounting height changed '+s.recipe);
 }
 if(Math.max(...x)-Math.min(...x)<2)errors.push('Rail does not travel '+s.recipe);
 if(x.some(v=>v<.936-.001||v>5.1+.001))errors.push('Rail centre outside envelope '+s.recipe);
 for(let i=1;i<times.length;i++)if(times[i]<=times[i-1])errors.push('Non-increasing clock '+s.recipe);
 for(const key of ['Dough','Cola','Dessert','Box'])if(!clip.channels.some(c=>b.j.nodes[c.target.node].name==='ROBOT23_PRODUCT_'+key&&c.target.path==='translation'))errors.push('Missing product '+key);
 checks.push({recipe:s.recipe,channels:clip.channels.length,frames:times.length,robot_and_carriage_centres_match:true,rail_centre_min_m:Math.min(...x),rail_centre_max_m:Math.max(...x),gate:s.gate});
}
const rail=b.j.nodes.find(n=>n.name==='ROBOT23_IGUS_PERFIL');if(!rail||!roots.has(b.j.nodes.indexOf(rail)))errors.push('No active manufacturer CAD rail');
if(m.services.rail.axis_world_z_m!==.96)errors.push('Rail centre mismatch');
if(m.services.chain.radius_m<m.services.chain.cable_dynamic_min_radius_m)errors.push('Cable bend too tight');
if(m.services.rail.source_stroke_mm!==3000||m.services.rail.concept_stroke_mm!==3684)errors.push('Lost custom-stroke disclosure');
const controller=b.j.nodes.find(n=>n.name==='ROBOT23_UR_KONTROL_KUTUSU');
if(!controller||JSON.stringify(controller.translation)!==JSON.stringify([4.5925,.3115,1.909]))errors.push('Controller not under QR');
if([...roots].some(i=>b.j.nodes[i].name?.startsWith('QR_ROBOT_KONTROL')))errors.push('Legacy yellow control box still active');
const cartNode=b.j.nodes.find(n=>n.name==='UR10E_body_07');
if((cartNode.children||[]).some(i=>b.j.nodes[i].name?.startsWith('UR10E_body_07_mesh')))errors.push('Legacy blue simulator plates still attached');
const floor=m.services.floor_plan;
if(!floor?.single_connected_trench||floor.lid_top_y_m!==0||floor.depth_m!==.080)errors.push('Floor trench continuity / flush level invalid');
for(const n of b.j.nodes.filter(n=>n.name?.startsWith('ROBOT23_ZEMIN_SIFIR_KAPAK'))){for(const p of b.j.meshes[n.mesh].primitives){const v=values(b,p.attributes.POSITION);for(let i=1;i<v.length;i+=3)if(v[i]+(n.translation?.[1]||0)>1e-7||v[i]+(n.translation?.[1]||0)<-.0060001)errors.push('Lid not flush '+n.name);}}
for(const d of m.services.ducts)if(d.points.every(p=>p[1]<0)&&d.nodes.length)errors.push('Surface floor duct remains '+d.name);
if([...roots].some(i=>b.j.nodes[i].name==='ELK_ZEMIN__kapak'||b.j.nodes[i].name?.startsWith('ZEMIN_DOSEME')))errors.push('Old damaged floor still visible');
for(const s of m.orders){const clip=b.j.animations.find(x=>x.name==='siparis_'+s.kod);for(const id of m.services.chain_nodes)if(!clip.channels.some(c=>c.target.node===id&&c.target.path==='translation'))errors.push('Cable chain not animated '+s.recipe);}
if([...roots].some(i=>b.j.nodes[i].name?.startsWith('CELL62_')))errors.push('Requested divider assembly still present');
if([...roots].some(i=>/^(TEZGAH_|DUZ_TEZGAH)/.test(b.j.nodes[i].name||'')))errors.push('Bench still active');
const report={published_source_sha256:m.published_source_sha256,removed_user_requested_bench:true,version:23,source_sha256:m.source_sha256,preserved_source_nodes:a.j.nodes.length,preserved_geometry_buffer_bytes:a.bin.length,stock_triangle_union_checked:true,orders:checks,errors,passed:!errors.length,scope:'source preservation, chain channel continuity, catalogue cable radius, manufacturer CAD provenance, old plate/box removal, connected recessed trench and exact flush lid heights; full motion clearance not certified',full_collision_certified:false,production_ready:false};
fs.writeFileSync(out+'integration_audit.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));if(errors.length)process.exit(1);
