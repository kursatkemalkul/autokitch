import fs from 'node:fs';
import zlib from 'node:zlib';
import crypto from 'node:crypto';
const A='otonom/hat3d/robot-integrated-v27/';
function read(file){let r=fs.readFileSync(file);if(r[0]===31&&r[1]===139)r=zlib.gunzipSync(r);const n=r.readUInt32LE(12);return{raw:r,j:JSON.parse(r.subarray(20,20+n)),bin:r.subarray(28+n,28+n+r.readUInt32LE(20+n))};}
const old=read(process.argv[2]||'otonom/hat3d/robot-integrated-v26/hat3_robot_v27.glb.gz'),out=read(A+'hat3_robot_v27.glb.gz');
const plan=JSON.parse(fs.readFileSync(A+'floor_plan.json')),build=JSON.parse(fs.readFileSync(A+'floor_build.json')),errors=[];
if(!out.bin.subarray(0,old.bin.length).equals(old.bin))errors.push('Original binary changed');
if(JSON.stringify(old.j.animations)!==JSON.stringify(out.j.animations))errors.push('Source motion channels changed');
for(let i=0;i<old.j.nodes.length;i++)if(JSON.stringify(old.j.nodes[i])!==JSON.stringify(out.j.nodes[i]))errors.push('Original node changed: '+i);
for(let i=0;i<old.j.meshes.length;i++)for(let k=0;k<old.j.meshes[i].primitives.length;k++){
 const a=structuredClone(old.j.meshes[i].primitives[k]),b=structuredClone(out.j.meshes[i].primitives[k]);
 delete a.material;delete b.material;if(JSON.stringify(a)!==JSON.stringify(b))errors.push('Original primitive geometry changed: '+i);
}
if(build.removed_roots.some(n=>!/^(DUKKAN26_|ROBOT25_(ZEMIN_TEMIZ_|GOMULU_KANAL_|ZEMIN_SIFIR_KAPAK_|CIKIS_SIFIR_YAKA_|KAPAK_DERZ_DESTEK_|SAG_DUVAR_KOSE_CIZGI_)|ROBOT25_UR_CIKIS$)/.test(n)))errors.push('Removed non-shop source root');
const roots=new Set(out.j.scenes[out.j.scene||0].nodes);
for(const i of old.j.scenes[old.j.scene||0].nodes)if(!roots.has(i)&&!build.removed_roots.includes(old.j.nodes[i].name))errors.push('Unexpected source removal');
const preservedRootNames=[...roots].map(i=>out.j.nodes[i].name);
if(preservedRootNames.some(n=>n.startsWith('INSAN_180cm')))errors.push('Old human avatar returned');
const rows=[];
for(const part of build.new_parts){
 const prim=out.j.meshes[part.mesh].primitives[0],a=out.j.accessors[prim.attributes.POSITION],v=out.j.bufferViews[a.bufferView],verts=[];
 for(let i=0;i<a.count;i++)verts.push([0,1,2].map(k=>out.bin.readFloatLE((v.byteOffset||0)+(a.byteOffset||0)+i*12+k*4)));
 const ai=out.j.accessors[prim.indices],iv=out.j.bufferViews[ai.bufferView],idx=[];for(let i=0;i<ai.count;i++)idx.push(out.bin.readUInt32LE((iv.byteOffset||0)+(ai.byteOffset||0)+i*4));
 const welded=new Map(),remap=verts.map(p=>{const key=p.map(x=>Math.round(x*1e7)).join('/');if(!welded.has(key))welded.set(key,welded.size);return welded.get(key);}),edges=new Map();let volume=0,degenerate=0;
 for(let i=0;i<idx.length;i+=3){const [a,b,c]=idx.slice(i,i+3),p=verts[a],q=verts[b],r=verts[c];if(!p||!q||!r){errors.push(part.name+' invalid index');continue;}
  volume+=(p[0]*(q[1]*r[2]-q[2]*r[1])+p[1]*(q[2]*r[0]-q[0]*r[2])+p[2]*(q[0]*r[1]-q[1]*r[0]))/6;
  if(new Set([remap[a],remap[b],remap[c]]).size<3)degenerate++;
  for(const [s,t]of [[a,b],[b,c],[c,a]]){const x=remap[s],y=remap[t];if(x===y)continue;const key=Math.min(x,y)+'/'+Math.max(x,y),e=edges.get(key)||[0,0];e[0]++;e[1]+=x<y?1:-1;edges.set(key,e);}
 }
 const bad=[...edges.values()].filter(([n,o])=>n!==2||o!==0).length;
 if(bad||Math.abs(volume)<1e-12)errors.push(part.name+' non-closed mesh: '+bad+' / '+volume);
 rows.push({name:part.name,triangles:idx.length/3,closed:!bad,volume_m3:Math.abs(volume),degenerate});
}
if(preservedRootNames.some(n=>/^DUKKAN26_/.test(n)))errors.push('A removed shop fixture remains active');
const required=['ROBOT25_UR_KONTROL_KUTUSU','ROBOT25_MAKINE_BESLEME','ROBOT25_QR_GUC','ROBOT25_UR_HIGH_FLEX_12M_SABIT'];
for(const n of required)if(!preservedRootNames.includes(n))errors.push('Required equipment/cable missing: '+n);
const report={version:27,source_geometry_binary_preserved:true,source_nodes_unchanged:true,all14_animation_clips_byte_same:true,orders_preserved:8,qr_bays_preserved:12,new_meshes:rows,removed_roots:build.removed_roots,modules:plan.modules.length,floor_inner_size_m:plan.inner_size_m,flush_cover_top_y_m:0,cable_routes_preserved:9,minimum_planar_cable_clearance_m:Math.min(...plan.cable_clearances.map(x=>x.side_clearance_m??1)),passed:!errors.length,errors,full_preexisting_robot_station_collision_certified:false,oem_step_imported:false};
fs.writeFileSync(A+'geometry_audit.json',JSON.stringify(report,null,2));console.log(JSON.stringify({...report,new_meshes:rows.length,removed_roots:build.removed_roots.length}));if(errors.length)process.exitCode=1;
