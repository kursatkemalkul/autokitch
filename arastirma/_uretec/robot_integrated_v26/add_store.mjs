// Append only shop geometry; preserve source machine/QR/robot and animation bytes.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import * as T from '../robot_integrated_v22/vendor/three.mjs';
import {cableMesh,sweep} from '../robot_integrated_v25/sweep.mjs';
const A='otonom/hat3d/robot-integrated-v26/',LOCAL='_local/codex_robot_v26/';
const input=process.argv[2]||'otonom/hat3d/robot-integrated-v25/hat3_robot_v25.glb.gz';
let raw=fs.readFileSync(input);if(raw[0]===31&&raw[1]===139)raw=zlib.gunzipSync(raw);
const jl=raw.readUInt32LE(12),g=JSON.parse(raw.subarray(20,20+jl)),bin=raw.subarray(28+jl,28+jl+raw.readUInt32LE(20+jl));
const original=structuredClone(g),plan=JSON.parse(fs.readFileSync(A+'shop_plan.json'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),pad=n=>(n+3)&~3;
const chunks=[bin];let offset=bin.length;
const newParts=[],removed=[];
g.scenes[g.scene||0].nodes=g.scenes[g.scene||0].nodes.filter(i=>{const drop=/^ROBOT25_(ZEMIN_TEMIZ_|SAG_DUVAR_KOSE_CIZGI_)/.test(g.nodes[i].name||'');if(drop)removed.push(g.nodes[i].name);return !drop;});
function acc(values,size,type=5126,target=34962){const a=type===5125?new Uint32Array(values):new Float32Array(values),b=Buffer.from(a.buffer);if(offset%4){const p=Buffer.alloc(pad(offset)-offset);chunks.push(p);offset+=p.length;}const vi=g.bufferViews.length;g.bufferViews.push({buffer:0,byteOffset:offset,byteLength:b.length,target});chunks.push(b);offset+=b.length;const lo=Array(size).fill(Infinity),hi=Array(size).fill(-Infinity);for(let i=0;i<a.length;i++){lo[i%size]=Math.min(lo[i%size],a[i]);hi[i%size]=Math.max(hi[i%size],a[i]);}const ai=g.accessors.length;g.accessors.push({bufferView:vi,componentType:type,count:a.length/size,type:size===1?'SCALAR':'VEC'+size,min:lo,max:hi});return ai;}
const materials=new Map();
function material(color,alpha=1){const key=color+':'+alpha;if(materials.has(key))return materials.get(key);const id=g.materials.length;g.materials.push({name:'DUKKAN26_'+key,pbrMetallicRoughness:{baseColorFactor:[(color>>16&255)/255,(color>>8&255)/255,(color&255)/255,alpha],metallicFactor:color===0xb9c3c8?.7:0,roughnessFactor:.7},...(alpha<1?{alphaMode:'BLEND',doubleSided:true}:{})});materials.set(key,id);return id;}
function add(name,geo,color,at=[0,0,0],note='generic planning envelope',alpha=1){geo.computeVertexNormals();const p={attributes:{POSITION:acc(geo.attributes.position.array,3),NORMAL:acc(geo.attributes.normal.array,3)},indices:acc(geo.index?.array||Array.from({length:geo.attributes.position.count},(_,i)=>i),1,5125,34963),material:material(color,alpha)};const mi=g.meshes.length,ni=g.nodes.length;g.meshes.push({name:'DUKKAN26_'+name,primitives:[p]});g.nodes.push({name:'DUKKAN26_'+name,mesh:mi,translation:at,extras:{kat:'DUKKAN',mek:'Çevre/Dükkân hattı',part:name,connection:note,version:26}});g.scenes[g.scene||0].nodes.push(ni);const a=p.attributes.POSITION;const b=g.accessors[a];newParts.push({name:g.nodes[ni].name,node:ni,mesh:mi,lo:b.min.map((v,i)=>v+at[i]),hi:b.max.map((v,i)=>v+at[i]),connection:note});return ni;}
const box=(name,lo,hi,c=0xb9c3c8,note)=>add(name,new T.BoxGeometry(...hi.map((v,i)=>v-lo[i])),c,lo.map((v,i)=>(v+hi[i])/2),note);
const line=(name,a,b,c=0x72838c,r=.002)=>add(name,cableMesh([a,b],r),c,[0,0,0],'visual architectural boundary; no opaque wall');
function outline(name,lo,hi,color=0x72838c){for(const axis of [0,1,2])for(let j=0;j<4;j++){const other=[0,1,2].filter(x=>x!==axis),a=[...lo],b=[...lo];b[axis]=hi[axis];for(let k=0;k<2;k++)a[other[k]]=b[other[k]]=(j&(1<<k))?hi[other[k]]:lo[other[k]];if(a.some((v,i)=>v!==b[i]))line(name+'_'+axis+'_'+j,a,b,color);}}
function shape(poly){const s=new T.Shape(poly.outer.map(p=>new T.Vector2(...p)));for(const h of poly.holes)s.holes.push(new T.Path(h.map(p=>new T.Vector2(...p))));return s;}
for(const [i,p]of plan.floor.entries()){const geo=new T.ExtrudeGeometry(shape(p),{depth:.010,bevelEnabled:false});geo.rotateX(Math.PI/2);add('ZEMIN_'+i,geo,0xdbdbd6,[0,0,0],'continuous floor, existing flush trench retained; three actual water/drain bores');}
const left=plan.inner_bounds[0][0],right=plan.inner_bounds[1][0],back=plan.inner_bounds[0][2],front=plan.inner_bounds[1][2],P=plan.partition.z_m;
outline('SAG_DUVAR',[right,0,back],[right,2.4,front]);
outline('SOL_DUVAR',[left,0,back],[left,2.4,front]);
outline('ARKA_DUVAR',[left,0,back],[right,2.4,back]);
// Front wall with a real entrance opening; architectural limits remain lines.
outline('ON_DUVAR_KAPI_UST',[left,2.130,front],[right,2.4,front]);
outline('ON_DUVAR_SAG',[left+1.000,0,front],[right,2.130,front]);
outline('ARA_DUVAR',[left+1.000,0,P],[3.587,2.05,P]);
outline('ARA_DUVAR_QR_BIRLESIM',[3.587,0,2.083],[3.597,2.05,P]);
// The outline represents the proposed fixed guard, not a certified barrier.
for(const d of plan.doors){const [a,b]=d.x_m,z=d.z_m;
 box(d.name+'_SOL_KASA',[a-.05,0,z-.018],[a-.008,2.130,z+.018],0x96a2a9,'jamb fixed to left wall/floor');
 box(d.name+'_SAG_KASA',[b+.008,0,z-.018],[b+.05,2.130,z+.018],0x96a2a9,'jamb anchored at partition/front wall');
 box(d.name+'_UST_KASA',[a-.008,2.088,z-.018],[b+.008,2.130,z+.018],0x96a2a9,'header between jambs; clear opening 900 x 2080');
 const l=a+.003,r=b-.003;
 box(d.name+'_KANAT_SOL',[l,.008,z-.012],[l+.025,2.075,z+.012],0xb9c3c8,'leaf on two jamb hinges');
 box(d.name+'_KANAT_SAG',[r-.025,.008,z-.012],[r,2.075,z+.012],0xb9c3c8,'leaf crossmembers welded');
 for(const y of [.008,2.05])box(d.name+'_KANAT_ENINE_'+y,[l+.025,y,z-.012],[r-.025,y+.025,z+.012],0xb9c3c8,'leaf crossmember butt joint');
 for(const y of [.260,1.700])box(d.name+'_MENTESE_'+y,[a-.011,y,z-.020],[a+.012,y+.070,z+.020],0x5f6d75,'hinge on own jamb and leaf');
 line(d.name+'_KULP',[r-.0125,.930,z+.025],[r-.120,.930,z+.025],0xadb9bf,.008);
 line(d.name+'_KULP_AYAK',[r-.0125,.930,z+.012],[r-.0125,.930,z+.025],0xadb9bf,.008);
 if(d.interlock_required)box(d.name+'_EMNIYET_YERI',[b+.010,.975,z+.018],[b+.042,1.045,z+.042],0x7b8a96,'reserved safety interlock envelope; final circuit not designed');
 // Opening arc is on the staff/outside side, never into the robot corridor.
 const pts=Array.from({length:25},(_,i)=>[l+d.swing_radius_m*Math.cos(i*Math.PI/48),.003,z+d.swing_radius_m*Math.sin(i*Math.PI/48)]);
 for(let i=0;i<pts.length-1;i+=2)line(d.name+'_ACILMA_YAYI_'+i,pts[i],pts[i+1],0x9cabaf,.0013);
}
// Real open leg space; wall-mounted rear rail and four hollow 30x30x2 legs.
function profile(name,a,b,width=.030,t=.002){const w=width/2;return add(name,sweep([a,b],[[-w,-w],[w,-w],[w,w],[-w,w],[-w+t,-w+t],[w-t,-w+t],[w-t,w-t],[-w+t,w-t]],null,true),0x8f9da5,[0,0,0],'hollow section, welded to own underframe; foot on floor');}
const desk=plan.desk.bounds,x0=desk[0][0],x1=desk[1][0],z0=desk[0][2],z1=desk[1][2];
box('OTURMA_TEZGAHI_TABLA',desk[0],desk[1],0xd1bca0,'30 mm purchased furniture top on underframe; height 770 mm');
for(const x of [x0+.040,x1-.040])for(const z of [z0+.035,z1-.035]){profile('MASA_AYAK_'+x+'_'+z,[x,.010,z],[x,.710,z]);box('MASA_AYAK_PABUC_'+x+'_'+z,[x-.022,0,z-.022],[x+.022,.010,z+.022],0x40494f,'rubber foot seated on floor');}
for(const z of [z0+.035,z1-.035])profile('MASA_UST_KUSAK_'+z,[x0+.025,.725,z],[x1-.025,.725,z]);
for(const x of [x0+.040,x1-.040])profile('MASA_YAN_KUSAK_'+x,[x,.725,z0+.050],[x,.725,z1-.050]);
// Compact chair instead of a human avatar. Legs/support are connected.
const cc=plan.chair.centre,cx=cc[0],cz=cc[2];
box('SANDALYE_OTURAK',[cx-.230,.445,cz-.215],[cx+.230,.475,cz+.215],0x444d54,'generic seat on welded frame');
for(const x of [cx-.185,cx+.185])for(const z of [cz-.170,cz+.170])profile('SANDALYE_AYAK_'+x+'_'+z,[x,0,z],[x,.445,z],.022,.002);
for(const x of [cx-.185,cx+.185])profile('SANDALYE_ARKA_DESTEK_'+x,[x,.445,cz-.170],[x,.880,cz-.170],.022,.002);
box('SANDALYE_SIRT',[cx-.230,.680,cz-.192],[cx+.230,.900,cz-.170],0x444d54,'backrest on two rear uprights');
// Separate standing-height wash bay, with an actual empty 300x300x150 bowl.
const sb=plan.sink.bounds,sx=plan.sink.bowl_centre_xz[0],sz=plan.sink.bowl_centre_xz[1];
for(const x of [sb[0][0]+.035,sb[1][0]-.035])for(const z of [z0+.035,z1-.035])profile('LAVABO_AYAK_'+x+'_'+z,[x,.010,z],[x,.865,z]);
for(const z of [z0+.035,z1-.035])profile('LAVABO_UST_KUSAK_'+z,[sb[0][0]+.020,.880,z],[sb[1][0]-.020,.880,z]);
for(const x of [sb[0][0]+.035,sb[1][0]-.035])profile('LAVABO_YAN_KUSAK_'+x,[x,.880,z0+.050],[x,.880,z1-.050]);
function roundRect(x,z,w,d,r){const s=new T.Shape();s.moveTo(x-w/2+r,z-d/2);s.lineTo(x+w/2-r,z-d/2);s.quadraticCurveTo(x+w/2,z-d/2,x+w/2,z-d/2+r);s.lineTo(x+w/2,z+d/2-r);s.quadraticCurveTo(x+w/2,z+d/2,x+w/2-r,z+d/2);s.lineTo(x-w/2+r,z+d/2);s.quadraticCurveTo(x-w/2,z+d/2,x-w/2,z+d/2-r);s.lineTo(x-w/2,z-d/2+r);s.quadraticCurveTo(x-w/2,z-d/2,x-w/2+r,z-d/2);return s;}
function sheet(name,s,top,thick){const geo=new T.ExtrudeGeometry(s,{depth:thick,bevelEnabled:false,curveSegments:12});geo.rotateX(Math.PI/2);return add(name,geo,0xb9c3c8,[0,top,0],'own welded stainless sheet; nominal layout, not OEM CAD');}
const top=new T.Shape([[sb[0][0],z0],[sb[1][0],z0],[sb[1][0],z1],[sb[0][0],z1]].map(p=>new T.Vector2(...p)));top.holes.push(roundRect(sx,sz,.300,.300,.008));sheet('LAVABO_TABLA',top,.900,.003);
const sides=roundRect(sx,sz,.302,.302,.009);sides.holes.push(roundRect(sx,sz,.300,.300,.008));sheet('LAVABO_HAZNE_DUVAR',sides,.897,.150);
const bottom=roundRect(sx,sz,.302,.302,.009),hole=new T.Path();hole.absarc(sx,sz,.016,0,2*Math.PI,true);bottom.holes.push(hole);sheet('LAVABO_HAZNE_TABAN',bottom,.748,.001);
box('LAVABO_SICRAMA_ETEGI',[sb[0][0],.900,z1-.003],[sb[1][0],1.000,z1],0xb9c3c8,'TIG to rear edge of sink top');
const faucetX=sx,faucetZ=sz+.220;
add('EL_YIKAMA_BATARYA',cableMesh([[faucetX,.900,faucetZ],[faucetX,1.040,faucetZ],[faucetX,1.060,faucetZ-.015],[faucetX,1.060,sz+.040]],.012),0xb9c3c8,[0,0,0],'generic elbow-operated hot/cold mixer envelope on sink deck');
add('BATARYA_DIRSEK_KOLU',cableMesh([[faucetX,1.020,faucetZ],[faucetX+.100,1.090,faucetZ]],.005),0x6a7b83,[0,0,0],'mixer operating lever');
// Plumbing has dedicated holes and runs away from all electrical trenches.
function tube(name,pts,r,color){const outer=Array.from({length:20},(_,i)=>[r*Math.cos(i*Math.PI/10),r*Math.sin(i*Math.PI/10)]),inner=outer.map(([x,y])=>[x*(r-.0015)/r,y*(r-.0015)/r]);return add(name,sweep(pts,outer.concat(inner),null,true),color,[0,0,0],'hollow pipe, unions at mixer/trap; building connection concealed in front wall');}
for(const [i,x]of [3.290,3.325].entries()){tube(i?'SICAK_SU':'SOGUK_SU',[[x,-.080,front+.025],[x,-.080,3.470],[x,.550,3.470],[x,.580,3.440],[x,.600,3.400],[faucetX+(i?.018:-.018),.650,faucetZ],[faucetX+(i?.018:-.018),.900,faucetZ]],.008,i?0xb44a42:0x4d83a4);box('SU_KESME_VANASI_'+i,[x-.013,.515,3.457],[x+.013,.545,3.483],0x697c86,'isolation valve retained in pipe under basin');}
tube('LAVABO_SIFON',[[sx,.747,sz],[sx,.615,sz],[sx,.590,sz+.025],[sx,.590,sz+.085],[sx,.615,sz+.110],[sx,.650,sz+.110],[3.455,.650,sz+.110],[3.455,.600,3.470],[3.455,-.100,3.470],[3.455,-.100,front+.025]],.016,0xd2d8d9);
box('SABUNLUK',[3.112,1.020,front-.080],[3.212,1.250,front],0xe2e5e4,'wall-mounted refillable soap dispenser, generic envelope');
box('KAGIT_HAVLULUK',[3.277,1.180,front-.090],[3.557,1.530,front],0xe2e5e4,'wall-mounted paper dispenser, generic envelope');
// Strip inactive-only materials, as required by the main model material controls.
const used=new Set(),visit=i=>{const n=g.nodes[i];if(n.mesh!=null)for(const p of g.meshes[n.mesh].primitives)if(p.material!=null)used.add(p.material);for(const c of n.children||[])visit(c);};for(const i of g.scenes[g.scene||0].nodes)visit(i);
const map=new Map([...used].sort((a,b)=>a-b).map((a,i)=>[a,i]));g.materials=[...map.keys()].map(i=>g.materials[i]);for(const m of g.meshes)for(const p of m.primitives)if(p.material!=null)p.material=map.get(p.material)??0;
if(offset%4)chunks.push(Buffer.alloc(pad(offset)-offset));const outBin=Buffer.concat(chunks);g.buffers[0].byteLength=outBin.length;
g.asset.generator='AUTOKITCH v26 compact shop appended to exact v25';g.scenes[g.scene||0].extras.shopIntegration={version:26,source_sha256:sha(raw),robot_motion_changed:false,plan};
const j0=Buffer.from(JSON.stringify(g)),j=Buffer.concat([j0,Buffer.alloc(pad(j0.length)-j0.length,32)]),h=Buffer.alloc(20),bh=Buffer.alloc(8);h.writeUInt32LE(0x46546c67,0);h.writeUInt32LE(2,4);h.writeUInt32LE(28+j.length+outBin.length,8);h.writeUInt32LE(j.length,12);h.writeUInt32LE(0x4e4f534a,16);bh.writeUInt32LE(outBin.length,0);bh.writeUInt32LE(0x004e4942,4);const output=Buffer.concat([h,j,bh,outBin]);
fs.mkdirSync(LOCAL,{recursive:true});fs.writeFileSync(LOCAL+'combined_meshopt.glb',output);fs.writeFileSync(A+'hat3_robot_v26.glb.gz',zlib.gzipSync(output,{level:9}));
if(process.argv[3]){fs.mkdirSync(path.dirname(process.argv[3]),{recursive:true});fs.writeFileSync(process.argv[3],output);}
const oldManifest=JSON.parse(fs.readFileSync('otonom/hat3d/robot-integrated-v25/manifest.json'));
const proof={version:26,source_input:input,source_sha256:sha(raw),source_binary_preserved:outBin.subarray(0,bin.length).equals(bin),original_node_count:original.nodes.length,original_mesh_count:original.meshes.length,removed_roots:removed,new_parts:newParts,animations_unchanged:JSON.stringify(g.animations)===JSON.stringify(original.animations),raw_web_sha256:sha(output),raw_web_bytes:output.length,gzip_sha256:sha(fs.readFileSync(A+'hat3_robot_v26.glb.gz')),gzip_bytes:fs.statSync(A+'hat3_robot_v26.glb.gz').size,passed:true};
if(!proof.source_binary_preserved||!proof.animations_unchanged)throw Error('Source geometry or animation changed');
fs.writeFileSync(A+'manifest.json',JSON.stringify({...oldManifest,version:26,raw_web_sha256:proof.raw_web_sha256,raw_web_bytes:proof.raw_web_bytes,gzip_bytes:proof.gzip_bytes,combined_nodes:g.nodes.length,shop:plan,shop_source_sha256:proof.source_sha256,services:{...oldManifest.services,shop:plan},known_open:[...oldManifest.known_open,...plan.open]},null,2));
fs.writeFileSync(A+'shop_build.json',JSON.stringify(proof,null,2));console.log(JSON.stringify({...proof,new_parts:newParts.length,removed_roots:removed.length}));
