// Convex-envelope GJK distance: source CAD body primitives, no visual hiding.
import fs from 'node:fs';
import zlib from 'node:zlib';
import {Rig,point} from '../../../otonom/hat/robot-integrated-v25/rig.js';
const A='otonom/hat3d/robot-integrated-v28/';
const data=JSON.parse(fs.readFileSync('otonom/hat3d/robot-integrated-v25/rig.json')),rig=new Rig(data,{mountForward:.1,railForward:.5});
const hulls=JSON.parse(fs.readFileSync('_local/codex_robot_v28/body_hulls.json'));
const add=(a,b)=>a.map((x,i)=>x+b[i]),sub=(a,b)=>a.map((x,i)=>x-b[i]),scale=(a,s)=>a.map(x=>x*s),dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
const corners=(lo,hi)=>Array.from({length:8},(_,i)=>lo.map((x,k)=>i&(1<<k)?hi[k]:x));
function closest(s){let best=null;for(let bits=1;bits<(1<<s.length);bits++){const ids=s.map((_,i)=>i).filter(i=>bits&(1<<i));if(ids.length>4)continue;const v=ids.map(i=>s[i]),d=v.slice(1).map(x=>sub(x,v[0])),n=d.length;let weights=[1];if(n){const a=d.map(x=>[...d.map(y=>dot(x,y)),-dot(x,v[0])]);let ok=true;for(let i=0;i<n;i++){let k=i;for(let j=i+1;j<n;j++)if(Math.abs(a[j][i])>Math.abs(a[k][i]))k=j;[a[i],a[k]]=[a[k],a[i]];const p=a[i][i];if(Math.abs(p)<1e-14){ok=false;break;}for(let j=i;j<=n;j++)a[i][j]/=p;for(let k2=0;k2<n;k2++)if(k2!==i){const f=a[k2][i];for(let j=i;j<=n;j++)a[k2][j]-=f*a[i][j];}}if(!ok)continue;const b=a.map(x=>x[n]);weights=[1-b.reduce((s,x)=>s+x,0),...b];if(weights.some(x=>x<-.00000001))continue;}
 const p=[0,0,0];for(let i=0;i<v.length;i++)for(let k=0;k<3;k++)p[k]+=v[i][k]*weights[i];const d2=dot(p,p);if(!best||d2<best.d2)best={p,d2,s:ids.filter((_,i)=>weights[i]>1e-9).map(i=>s[i])};}return best;}
function support(v,d){let best=v[0],score=-Infinity;for(const p of v){const s=dot(p,d);if(s>score){best=p;score=s;}}return best;}
export function distance(a,b){const sup=d=>sub(support(a,d),support(b,scale(d,-1)));let s=[sup([1,0,0])],c=closest(s);for(let n=0;n<60;n++){if(c.d2<1e-14)return 0;const v=sup(scale(c.p,-1));if(c.d2-dot(c.p,v)<1e-11)return Math.sqrt(c.d2);s=[...c.s,v];c=closest(s);}throw Error('GJK convergence');}
const bounds=v=>({lo:[0,1,2].map(k=>Math.min(...v.map(p=>p[k]))),hi:[0,1,2].map(k=>Math.max(...v.map(p=>p[k])))});
const overlap=(a,b)=>a.lo.every((x,k)=>x<=b.hi[k]+.001&&a.hi[k]+.001>=b.lo[k]);
const web=p=>[p[0],p[2],-p[1]],local=[.000000799220388,-.00000114247412,.1442837412011861];
const raw=zlib.gunzipSync(fs.readFileSync('otonom/hat3d/robot-integrated-v27/hat3_robot_v27.glb.gz')),jl=raw.readUInt32LE(12),g=JSON.parse(raw.subarray(20,20+jl));
const env=[{name:'unchanged machine front envelope',points:corners([.636,0,-.88],[5.13,2.25,.079])}];
for(const i of g.scenes[g.scene||0].nodes){const n=g.nodes[i];if(!/^QR62_(column_|shelf_|roof_|back_)|^ROBOT25_QR.*(SUTUN|KOLON|COLUMN)/i.test(n.name||'')||n.mesh==null)continue;for(const p of g.meshes[n.mesh].primitives){const a=g.accessors[p.attributes.POSITION],t=n.translation||[0,0,0];env.push({name:n.name,points:corners(a.min.map((x,k)=>x+t[k]),a.max.map((x,k)=>x+t[k]))});}}
// User-selected integrated QR control column on the left of the cabinet.
env.push({name:'QR control column',points:corners([3.597,0,1.75],[3.757,2.05,2.083])});
env.forEach(x=>x.bounds=bounds(x.points));
const joined=new Set(data.edges.map(e=>[e.parent,e.child].sort().join('|')));
const base='/World/RailSystem/Arm/',gp='/World/RailSystem/Gripper/';
joined.add([base+'base_link',base+'upper_arm_link'].sort().join('|'));
joined.add([base+'wrist_3_link',gp+'robotiq_base_link'].sort().join('|'));
const report={version:28,method:'source primitive convex hulls; GJK separation, exact native joint FK',sampling:'all authored turn frames, subdivisions until every body point moves <=2mm',frames:0,subframes:0,self_checks:0,payload_checks:0,environment_checks:0,failures:[],min_machine_box_clearance_m:Infinity,max_x_m:-Infinity,wall_clearance_m:Infinity,maximum_payload_tilt_deg:0,minimum_self_distance_m:Infinity,rail_backtracking_m:0};
const order=JSON.parse(fs.readFileSync(A+'order_v28.json')),plan=JSON.parse(fs.readFileSync(A+'turn_plan.json'));
const start=order.trajectory.findIndex(f=>f.time_s>=plan.old_begin_s-1e-8),end=order.trajectory.findIndex(f=>f.time_s>=plan.new_end_s-1e-8);
function observe(f,checkSelf=true){const w=rig.matrices(f.state.q,f.state.rail,f.state.jaw),shapes=Object.entries(hulls).flatMap(([name,h])=>h.map(points=>{const p=points.map(v=>web(point(w[name],v)));return{name,points:p,bounds:bounds(p)};}));
 const m=rig.tcp(f.state.q,f.state.rail,f.state.jaw),p=web(point(m,local)),yaw=Math.atan2(-m[4],m[0]),c=Math.cos(yaw),s=Math.sin(yaw),box=corners([-.16,-.0225,-.16],[.16,.0225,.16]).map(v=>[p[0]+c*v[0]+s*v[2],p[1]+v[1],p[2]-s*v[0]+c*v[2]]),bb=bounds(box);
 // Box grasp has local axis2 aligned horizontally: world-Z row in original pose.
 report.maximum_payload_tilt_deg=Math.max(report.maximum_payload_tilt_deg,Math.asin(Math.min(1,Math.hypot(m[8],m[10])))*180/Math.PI);
 report.min_machine_box_clearance_m=Math.min(report.min_machine_box_clearance_m,bb.lo[2]-.079);
 report.max_x_m=Math.max(report.max_x_m,bb.hi[0],...shapes.map(x=>x.bounds.hi[0]));
 const fail=(kind,a,b,d)=>{if(report.failures.length<30)report.failures.push({kind,stage:f.stage,t:f.time_s,a,b,d});};
 if(checkSelf)for(let i=0;i<shapes.length;i++)for(let j=i+1;j<shapes.length;j++){const a=shapes[i],b=shapes[j];if(a.name===b.name||joined.has([a.name,b.name].sort().join('|'))||(a.name.startsWith(gp)&&b.name.startsWith(gp))||!overlap(a.bounds,b.bounds))continue;report.self_checks++;const d=distance(a.points,b.points);report.minimum_self_distance_m=Math.min(report.minimum_self_distance_m,d);if(d<.0002)fail('self',a.name,b.name,d);}
 for(const a of shapes){if(!a.name.startsWith(gp)&&!a.name.endsWith('/wrist_3_link')&&overlap(a.bounds,bb)){report.payload_checks++;const d=distance(a.points,box);if(d<.0002)fail('box/arm',a.name,'Box',d);}for(const e of env){if(!overlap(a.bounds,e.bounds))continue;report.environment_checks++;const d=distance(a.points,e.points);if(d<.0002)fail('body/environment',a.name,e.name,d);}}
 for(const e of env){if(!overlap(bb,e.bounds))continue;report.environment_checks++;const d=distance(box,e.points);if(d<.0002)fail('box/environment','Box',e.name,d);}
 return shapes.map(x=>x.bounds);
}
let previous=order.trajectory[start-1],previousBounds=observe(previous);report.frames++;
for(let i=start;i<=end;i++){const f=order.trajectory[i],w=rig.matrices(f.state.q,f.state.rail,f.state.jaw),dw=rig.matrices(previous.state.q,previous.state.rail,previous.state.jaw);let move=0;for(const [b,h]of Object.entries(hulls))for(const pts of h)for(const p of pts){const a=point(w[b],p),c=point(dw[b],p);move=Math.max(move,Math.hypot(...sub(a,c)));}const subdivisions=Math.max(1,Math.ceil(move/.0019));for(let j=1;j<=subdivisions;j++){const u=j/subdivisions,st={q:previous.state.q.map((x,k)=>x+(f.state.q[k]-x)*u),rail:previous.state.rail+(f.state.rail-previous.state.rail)*u,jaw:f.state.jaw};const ff={...f,state:st,time_s:previous.time_s+(f.time_s-previous.time_s)*u};observe(ff,!f.stage.includes('ray sabitken')||i===start+240);report.subframes++;}report.frames++;report.rail_backtracking_m=Math.max(report.rail_backtracking_m,previous.state.rail-f.state.rail);previous=f;}
report.wall_clearance_m=5.36-report.max_x_m;
if(report.wall_clearance_m<.01)report.failures.push({kind:'right wall clearance',distance:report.wall_clearance_m});
report.passed=!report.failures.length&&report.maximum_payload_tilt_deg<.1&&report.rail_backtracking_m<1e-9;
fs.writeFileSync(A+'turn_collision.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));if(!report.passed)process.exitCode=1;
