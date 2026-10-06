// One GLB: published v10l machine + approved QR62 meshes, native UR10e FK and merged timelines.
// Integration draft: audit checks geometry/channels, not full motion clearance.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import {spawnSync} from 'node:child_process';
import * as T from '../robot_integrated_v22/vendor/three.mjs';
import {Rig} from '../../../otonom/hat/robot-integrated-v25/rig.js';
import {compileOrder} from '../../../otonom/hat/robot-integrated-v25/workflow-v16.js';
import {installServices} from './services.mjs';
const source=process.env.MACHINE_NATIVE;
if(!source)throw Error('Set MACHINE_NATIVE to the exact uncompressed published v10l + QR62 GLB.');
const A='otonom/hat3d/robot-integrated-v25/',OUT=A;
const read=n=>JSON.parse(fs.readFileSync(A+n,'utf8'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function parse(b){const size=b.readUInt32LE(12);return {j:JSON.parse(b.subarray(20,20+size)),bin:b.subarray(28+size,28+size+b.readUInt32LE(20+size))};}
const raw=fs.readFileSync(source);
const provenance=read('source_provenance.json');
if(sha(raw)!==provenance.prepared_sha256)throw Error('Not the verified last local model!');
const {j:g,bin}=parse(raw),original=structuredClone(g),originalMeshCount=g.meshes.length;
const chunks=[bin],pad=n=>(n+3)&~3;let offset=bin.length;
function bytes(b){if(offset%4){const p=Buffer.alloc(4-offset%4);chunks.push(p);offset+=p.length;}const start=offset;chunks.push(b);offset+=b.length;return start;}
function acc(values,size,type=5126,target=null){const Typed=type===5125?Uint32Array:Float32Array,a=new Typed(values),b=Buffer.from(a.buffer),view=g.bufferViews.length;g.bufferViews.push({buffer:0,byteOffset:bytes(b),byteLength:b.length,...(target?{target}:{} )});const min=Array(size).fill(Infinity),max=Array(size).fill(-Infinity);for(let i=0;i<a.length;i++){min[i%size]=Math.min(min[i%size],a[i]);max[i%size]=Math.max(max[i%size],a[i]);}const id=g.accessors.length;g.accessors.push({bufferView:view,componentType:type,count:a.length/size,type:['','SCALAR','VEC2','VEC3','VEC4'][size],min,max});return id;}
function node(n,root=true){const id=g.nodes.length;g.nodes.push(n);if(root)g.scenes[g.scene||0].nodes.push(id);return id;}
function mesh(name,geo,color,translation=[0,0,0],extras={}){const pos=geo.attributes.position,norm=geo.attributes.normal;const p={attributes:{POSITION:acc(pos.array,3,5126,34962)},indices:acc(geo.index?.array||Array.from({length:pos.count},(_,i)=>i),1,5125,34963)};if(norm)p.attributes.NORMAL=acc(norm.array,3,5126,34962);g.materials??=[];p.material=g.materials.length;g.materials.push({name:name+'_material',pbrMetallicRoughness:{baseColorFactor:[(color>>16&255)/255,(color>>8&255)/255,(color&255)/255,1],metallicFactor:.15,roughnessFactor:.75},doubleSided:false});const m=g.meshes.length;g.meshes.push({name,primitives:[p]});return node({name,mesh:m,translation,extras});}
const removedNames=[];
// Replace the previous QR. Counter had explicitly been discarded in robot-layout work.
g.scenes[g.scene||0].nodes=g.scenes[g.scene||0].nodes.filter(i=>{const name=g.nodes[i].name||'';const remove=/^(ROBOT_UR10E_NATIVE$|TEZGAH_|DUZ_TEZGAH|CELL62_|QR_ROBOT_KONTROL|QR_UPS|QR_KILIT_KARTI|QR_MUSTERI_PANELI|ELK_QR_KUTU|INSAN_180cm)/.test(name)||/^QR62_BAY_\d+_(fixed_bracket|AZM|door_bracket|tongue|body_|actuator_|M12|lock_cable|duct_clip)/.test(name)||/^QR62_(cable_duct_|main_panel_backplate|lock_board_backplate|board_standoff_|scanner_backplate|reader_backplate|customer_upper_face|lower_fan|upper_fan)/.test(name)||(i<provenance.publishedNodeCount&&/^(QR_|ELK_QR)/.test(name));if(remove)removedNames.push(g.nodes[i].name);return !remove;});
const removed=new Set(original.nodes.map((n,i)=>removedNames.includes(n.name)?i:-1).filter(i=>i>=0));
const robotRaw=fs.readFileSync(A+'ur10e_short.glb'),r=parse(robotRaw),no=g.nodes.length,mo=g.meshes.length,ao=g.accessors.length,vo=g.bufferViews.length,ro=g.materials?.length||0,bo=bytes(r.bin);
for(const v of r.j.bufferViews)g.bufferViews.push({...v,buffer:0,byteOffset:bo+(v.byteOffset||0)});
for(const a of r.j.accessors)g.accessors.push({...a,bufferView:a.bufferView+vo});
for(const m of r.j.meshes)g.meshes.push({...m,primitives:m.primitives.map(p=>({...p,attributes:Object.fromEntries(Object.entries(p.attributes).map(([k,v])=>[k,v+ao])),...(p.indices!=null?{indices:p.indices+ao}:{}),...(p.material!=null?{material:p.material+ro}:{})}))});
g.materials.push(...(r.j.materials||[]));
for(const n of r.j.nodes)g.nodes.push({...n,name:'UR10E_'+n.name,...(n.mesh!=null?{mesh:n.mesh+mo}:{}),...(n.children?{children:n.children.map(i=>i+no)}:{}),extras:{kat:'ROBOT',mek:'Robot/UR10e'}});
node({name:'ROBOT_UR10E_NATIVE',rotation:[-Math.SQRT1_2,0,0,Math.SQRT1_2],children:r.j.scenes[r.j.scene||0].nodes.map(i=>i+no),extras:{kat:'ROBOT',mek:'Robot/UR10e'}});
const rigData=read('rig.json'),rig=new Rig(rigData,{mountForward:.1,railForward:.5}),bodyNodes={};
for(const [body,name]of Object.entries(rigData.body_nodes))bodyNodes[body]=r.j.nodes.findIndex(n=>n.name===name)+no;
const C=new T.Matrix4().makeRotationX(-Math.PI/2),M=x=>new T.Matrix4().set(...x);
const base=read('order_v25.json'),config=read('workflow_v16.json'),grid=read('qr_grid_v13.json'),light=read('light_scene_v14.json');
// Preserve all 12 step62 QR bays, locks, doors and transferred electrical devices.
const services=installServices({g,mesh,node,bodyNodes,read});
const drawers={Dough:'CEK_K1_lahm_1',Cola:'CEK_K5_ic1_1',Dessert:'CEK_K6_tatli_1'},products={};
function rawAcc(id){const a=original.accessors[id],v=original.bufferViews[a.bufferView],size={SCALAR:1,VEC3:3,VEC4:4}[a.type],format={5126:['getFloat32',4],5125:['getUint32',4],5123:['getUint16',2]}[a.componentType],dv=new DataView(bin.buffer,bin.byteOffset,bin.byteLength),out=[];for(let i=0;i<a.count;i++)for(let k=0;k<size;k++)out.push(dv[format[0]]((v.byteOffset||0)+(a.byteOffset||0)+i*(v.byteStride||size*format[1])+k*format[1],true));return out;}
const splitStock=[];
// Split one existing stock item into a moving node. All vertex positions/normals
// remain byte-identical: only its triangle indices move to a separate scene node.
for(const key of ['Dough','Cola','Dessert']){
 const p=light.stockProducts[key],closed=[...p.centre],children=[];
 for(let ni=0;ni<original.nodes.length;ni++){const n=original.nodes[ni];if(!n.name?.startsWith(drawers[key]+'__')||!/__hamur__|__kutu_icecek__/.test(n.name)||n.mesh==null)continue;
  for(let pi=0;pi<g.meshes[n.mesh].primitives.length;pi++){const prim=g.meshes[n.mesh].primitives[pi],v=rawAcc(prim.attributes.POSITION),idx=rawAcc(prim.indices),take=[],keep=[],radius=key==='Dough'?.047:key==='Cola'?.041:.052;
   for(let i=0;i<idx.length;i+=3){const ids=idx.slice(i,i+3),c=[0,1,2].map(k=>ids.reduce((s,id)=>s+v[id*3+k],0)/3);(Math.abs(c[0]-closed[0])<radius&&Math.abs(c[2]-closed[2])<radius&&Math.abs(c[1]-closed[1])<(key==='Cola'?.07:.055)?take:keep).push(...ids);}
   if(!take.length)continue;
   prim.indices=acc(keep,1,5125,34963);const mi=g.meshes.length;g.meshes.push({name:'ROBOT25_'+key+'_stock_shape',primitives:[{...prim,indices:acc(take,1,5125,34963)}]});const id=node({name:'ROBOT25_'+key+'_stock_shape',mesh:mi,translation:closed.map(x=>-x)},false);children.push(id);splitStock.push({product:key,source:n.name,moved_triangles:take.length/3,remaining_triangles:keep.length/3});
  }
 }
 if(!children.length)throw Error('Could not identify original stock '+key);
 products[key]=node({name:'ROBOT25_PRODUCT_'+key,translation:closed,children,extras:{kat:'URUN',mek:'Çevre/Ürün'}});
}
products.Box=mesh('ROBOT25_PRODUCT_Box',new T.BoxGeometry(.32,.045,.32),0xc4a26a,[4.6591115,1.0051,-.2060135],{kat:'URUN',mek:'Çevre/Ürün'});
const sourcePositions=Object.fromEntries(Object.keys(products).map(k=>[k,g.nodes[products[k]].translation]));
const lookup=new Map(g.nodes.map((n,i)=>[n.name,i]));
const latestDurum=JSON.parse(fs.readFileSync('otonom/hat3d/v3/durum.json'));
const summary=[];
function channel(a,id,path,times,values,size,interpolation='LINEAR'){const si=a.samplers.length;a.samplers.push({input:times,output:acc(values,size),interpolation});a.channels.push({sampler:si,target:{node:id,path}});}
function trs(m){const p=new T.Vector3(),q=new T.Quaternion(),s=new T.Vector3();m.decompose(p,q,s);return {p:p.toArray(),q:q.toArray()};}
function readAcc(id){const a=original.accessors[id],v=original.bufferViews[a.bufferView],dv=new DataView(bin.buffer,bin.byteOffset,bin.byteLength),out=[],size={SCALAR:1,VEC3:3,VEC4:4}[a.type];if(a.componentType!==5126)throw Error('animation type');for(let i=0;i<a.count*size;i++)out.push(dv.getFloat32((v.byteOffset||0)+(a.byteOffset||0)+i*4,true));return out;}
for(const recipe of config.recipes){
 const current=latestDurum.siparis.find(s=>s.kod===recipe.id),originalAnim=original.animations.find(a=>a.name==='siparis_'+recipe.id);
 const rcp=current?{...recipe,events:current.adim.map(a=>({name:a.ad,time_s:a.t})),source:'published v10l native machine timeline'}:{...recipe};
 const opener=rcp.events.find(e=>e.name.startsWith('AÇICI'))?.time_s??0,ready=rcp.events.find(e=>e.name==='ROBOT → QR')?.time_s; if(ready!=null)rcp.processing_after_dough_s=ready-opener; config.recipes[config.recipes.findIndex(x=>x.id===recipe.id)]=rcp;
 const record=compileOrder(base,rcp),frames=record.trajectory,times=acc(frames.map(f=>f.time_s),1),a={name:'siparis_birlesik_'+recipe.id,samplers:[],channels:[],extras:{machine:'published v10l + QR62',robot:'UR10e',ideal_grasp:true,collision_certified:false,integration_draft:true}};
 const matrixFrames=frames.map(f=>rig.matrices(f.state.q,f.state.rail,f.state.jaw));
 for(const [k,id]of services.chain.entries()){
  const poses=frames.map(f=>services.chainPose(k,f.state.rail)),ts=poses.flatMap(p=>p.p),rs=poses.flatMap(p=>[0,0,Math.sin(p.angle/2),Math.cos(p.angle/2)]);
  channel(a,id,'translation',times,ts,3);channel(a,id,'rotation',times,rs,4);
  if(recipe.id===config.recipes[0].id){g.nodes[id].translation=ts.slice(0,3);g.nodes[id].rotation=rs.slice(0,4);}
 }
 for(const [body,id]of Object.entries(bodyNodes)){const ts=[],rs=[];let previous=null;for(const w of matrixFrames){const t=trs(M(w[body]));if(previous&&t.q.reduce((s,x,i)=>s+x*previous[i],0)<0)t.q=t.q.map(x=>-x);ts.push(...t.p);rs.push(...t.q);previous=t.q;}channel(a,id,'translation',times,ts,3);channel(a,id,'rotation',times,rs,4);if(recipe.id===config.recipes[0].id){delete g.nodes[id].matrix;g.nodes[id].translation=ts.slice(0,3);g.nodes[id].rotation=rs.slice(0,4);}}
 for(const [name,id]of lookup){const match=name.match(/^(CEK_K\d+_[^_]+_\d+)__/);if(!match||!name.includes('CEKMECE'))continue;const initial=g.nodes[id].translation||[0,0,0],values=[];for(const f of frames)values.push(initial[0],initial[1],initial[2]+(f.drawers[match[1]]||0)*(name.includes('CEKMECE_ARA')?.5:1));channel(a,id,'translation',times,values,3);}
 const handoff=record.events.find(e=>e.name==='table.robot_clear').time_s,boxSource=frames.find(f=>f.carrying==='Box')?.time_s??Infinity;
 for(let i=0;i<original.nodes.length;i++)if(original.nodes[i].name==='E_KUTU__B_ROOT')channel(a,i,'scale',times,frames.flatMap(()=>[0,0,0]),3,'STEP');
 for(const [key,id]of Object.entries(products)){const pos=[],rot=[],sc=[];for(let i=0;i<frames.length;i++){const f=frames[i];const p=f.carrying===key&&f.product?f.product:f.placed[key]||sourcePositions[key].map((v,k)=>v+(k===2?(f.drawers[drawers[key]]||0):0));pos.push(...p);let yaw=0;if(key==='Box'&&f.carrying==='Box'){const m=C.clone().multiply(M(rig.tcp(f.state.q,f.state.rail,f.state.jaw)));yaw=Math.atan2(m.elements[8],m.elements[10]);}rot.push(0,Math.sin(yaw/2),0,Math.cos(yaw/2));const visible=key==='Box'?(f.time_s>=(record.summary.machine_ready_s??(record.gate.time_s+.001))):key==='Dough'?f.time_s<handoff+1:true;sc.push(...(visible?[1,1,1]:[0,0,0]));}channel(a,id,'translation',times,pos,3);channel(a,id,'rotation',times,rot,4);channel(a,id,'scale',times,sc,3,'STEP');}
 // Retain the exact native machine cycle, delayed until the robot clears the table.
 // Do not reuse the old native QR, stock-drawer, robot or box-pickup channels.
 for(const c of originalAnim?.channels||[]){const name=original.nodes[c.target.node].name||'';if(removed.has(c.target.node)||name.startsWith('CEK_')||name.startsWith('E_KUTU__')||name.includes('ROBOT')||name.startsWith('UR10E_'))continue;const sm=originalAnim.samplers[c.sampler],t=readAcc(sm.input).map(v=>v<=opener?handoff*v/opener:handoff+v-opener),input=acc(t,1);a.samplers.push({...sm,input});a.channels.push({...c,sampler:a.samplers.length-1});}
 g.animations.push(a);const stages=frames.filter((f,i)=>!i||f.stage!==frames[i-1].stage).map(f=>({t:f.time_s,ad:f.stage,not_:'Kayıtlı robot hareketi · ideal tutuş · güncel makineyle tam çarpışma onayı yok.'}));
 summary.push({kod:'birlesik_'+recipe.id,recipe:recipe.id,ad:recipe.name+' + robot',sure:frames.at(-1).time_s,adim:[...record.events.filter(e=>e.time_s!==null).map(e=>({t:e.time_s,ad:e.name,not_:'Makine/robot eşgüdüm kaydı.'})),...stages].sort((a,b)=>a.t-b.t),stages,gate:record.gate,robot_frames:frames.length,robot_tasks:['Dough','Cola','Dessert','Box']});
}
// model-viewer exposes inactive glTF materials too. Remove inactive service
// materials so the existing main-page material controls never touch unloaded ones.
const activeMaterials=new Set(),visit=id=>{const n=g.nodes[id];if(n.mesh!=null)for(const p of g.meshes[n.mesh].primitives)if(p.material!=null)activeMaterials.add(p.material);for(const c of n.children||[])visit(c);};for(const n of g.scenes[g.scene||0].nodes)visit(n);
const matMap=new Map([...activeMaterials].sort((a,b)=>a-b).map((id,i)=>[id,i]));g.materials=[...matMap.keys()].map(id=>g.materials[id]);for(const m of g.meshes)for(const p of m.primitives)if(p.material!=null)p.material=matMap.get(p.material)??0;
g.buffers=[{byteLength:pad(offset)}];if(offset%4)chunks.push(Buffer.alloc(4-offset%4));g.asset.generator='AUTOKITCH published v10l + QR62 + native UR10e integrated v25 (draft)';g.scenes[g.scene||0].extras.robotIntegration={version:25,source_sha256:sha(raw),source_robot_sha256:sha(robotRaw),collision_certified:false,removed_previous_service_nodes:removedNames,ideal_grasp:true};
const outBin=Buffer.concat(chunks),jb0=Buffer.from(JSON.stringify(g)),jb=Buffer.concat([jb0,Buffer.alloc(pad(jb0.length)-jb0.length,32)]),head=Buffer.alloc(20),bh=Buffer.alloc(8);head.writeUInt32LE(0x46546c67,0);head.writeUInt32LE(2,4);head.writeUInt32LE(28+jb.length+outBin.length,8);head.writeUInt32LE(jb.length,12);head.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(outBin.length,0);bh.writeUInt32LE(0x004e4942,4);
const build='_local/codex_robot_v25';fs.mkdirSync(build,{recursive:true});fs.mkdirSync(OUT,{recursive:true});const native=build+'/combined_native.glb',packed=build+'/combined_meshopt.glb';fs.writeFileSync(native,Buffer.concat([head,jb,bh,outBin]));
function standalone(prefix,file){const h={asset:{version:'2.0',generator:'AUTOKITCH v17 archive'},scene:0,scenes:[{nodes:[]}],nodes:[],meshes:[],materials:[],accessors:[],bufferViews:[],buffers:[]},parts=[];let length=0;
 const amap=new Map(),mmap=new Map();const copyAcc=id=>{if(amap.has(id))return amap.get(id);const a=g.accessors[id],v=g.bufferViews[a.bufferView],b=outBin.subarray(v.byteOffset||0,(v.byteOffset||0)+v.byteLength);while(length%4){parts.push(Buffer.alloc(1));length++;}const vi=h.bufferViews.length;h.bufferViews.push({...v,buffer:0,byteOffset:length});parts.push(b);length+=b.length;const ai=h.accessors.length;h.accessors.push({...a,bufferView:vi});amap.set(id,ai);return ai;};
 for(const n of g.nodes.filter(n=>n.name?.startsWith(prefix)&&n.mesh!=null)){const m=g.meshes[n.mesh],mi=h.meshes.length;h.meshes.push({...m,primitives:m.primitives.map(p=>{let material;if(p.material!=null){if(!mmap.has(p.material)){mmap.set(p.material,h.materials.length);h.materials.push(g.materials[p.material]);}material=mmap.get(p.material);}return {...p,attributes:Object.fromEntries(Object.entries(p.attributes).map(([k,v])=>[k,copyAcc(v)])),indices:copyAcc(p.indices),...(material!=null?{material}:{})};})});h.scenes[0].nodes.push(h.nodes.length);h.nodes.push({...n,mesh:mi});}
 while(length%4){parts.push(Buffer.alloc(1));length++;}h.buffers=[{byteLength:length}];const q0=Buffer.from(JSON.stringify(h)),q=Buffer.concat([q0,Buffer.alloc(pad(q0.length)-q0.length,32)]),hh=Buffer.alloc(20),bb=Buffer.alloc(8);hh.writeUInt32LE(0x46546c67,0);hh.writeUInt32LE(2,4);hh.writeUInt32LE(28+q.length+length,8);hh.writeUInt32LE(q.length,12);hh.writeUInt32LE(0x4e4f534a,16);bb.writeUInt32LE(length,0);bb.writeUInt32LE(0x004e4942,4);fs.writeFileSync(file,Buffer.concat([hh,q,bb,...parts]));
}
// No separate cabinet replaces the preserved safety cabinet.
const enc=spawnSync(process.execPath,['arastirma/_uretec/robot_integrated_v22/meshopt/meshopt_kucult.mjs',native,packed,'--idx','seq'],{encoding:'utf8'});console.log(enc.stdout);if(enc.status!==0)throw Error(enc.stderr);
const packedBytes=fs.readFileSync(packed);fs.writeFileSync(OUT+'hat3_robot_v25.glb.gz',zlib.gzipSync(packedBytes,{level:9}));
const preserved=originalMeshCount===original.meshes.length&&Buffer.compare(outBin.subarray(0,bin.length),bin)===0;
const manifest={version:25,status:'integration draft; NOT production-ready',machine:'latest main v10l + QR62',published_source_sha256:provenance.published_sha256,source_sha256:sha(raw),removed_service_nodes:removedNames,source_meshes:originalMeshCount,machine_binary_preserved:preserved,stock_split:splitStock,combined_nodes:g.nodes.length,combined_animations:g.animations.map(a=>a.name),raw_web_bytes:packedBytes.length,raw_web_sha256:sha(packedBytes),gzip_bytes:fs.statSync(OUT+'hat3_robot_v25.glb.gz').size,orders:summary,known_open:['Supplier confirmation of 3684 mm custom stroke and dynamic moments','Full latest-model motion clearance not yet certified','Electrical protection/safety schematic not completed','Gate screen removed at user request: guarding incomplete','Second lahmacun pickup and all12 QR full routes remain open'],collision_certified:false,physics:false,services:{wall:services.wall,qr_customer:services.qr_customer,layout_scan:read('layout_scan.json'),rail:{manufacturer:services.cad.manufacturer,source_step_sha256:services.cad.source_step_sha256,source_stroke_mm:3000,concept_stroke_mm:3684,axis_world_z_m:.96,mount_y_m:.13},chain:services.chain_spec,ports:services.portRoutes,ducts:services.ducts,mount_nodes:services.mounts,chain_nodes:services.chain,floor_plan:services.floor_plan,legacy_carriage_removed:services.legacy_carriage_removed,legacy_yellow_controller_removed:services.legacy_yellow_controller_removed,glass_screen_removed:true,protective_guard_complete:false}};
fs.writeFileSync(OUT+'manifest.json',JSON.stringify(manifest,null,2));console.log(JSON.stringify({preserved,nodes:g.nodes.length,animations:g.animations.length,gzip_bytes:manifest.gzip_bytes}));


fs.writeFileSync(OUT+'workflow_v25.json',JSON.stringify(config,null,2));
