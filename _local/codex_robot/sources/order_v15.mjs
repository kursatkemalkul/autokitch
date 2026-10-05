import fs from 'node:fs';import{T,C,matrix,rig,root,read,box,hits,intersects,robot,solid,update}from './geometry.mjs';import{environment,obstacles,products,productAt,tcpScene}from './world.mjs';import{env}from './layout_v11.mjs';import{clipGripNotch}from '../../../otonom/hat/robot-main-v1/grip-notch.js';
rig.setRailForward(.5);const grid=read('qr_grid_v13.json'),src=read('source_dense_v12.json'),delivery=read('qr_delivery_v15.json'),clone=structuredClone;
for(const product of Object.values(products))for(const p of product.parts){const ids=Array.from(new Set(p.g.index.array)),map=new Map(ids.map((id,i)=>[id,i])),v=[];for(const id of ids)v.push(p.g.attributes.position.getX(id),p.g.attributes.position.getY(id),p.g.attributes.position.getZ(id));const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(v,3));g.setIndex(Array.from(p.g.index.array,id=>map.get(id)));g.computeBoundingBox();p.g=g;p.bvh=null;p.box=g.boundingBox.clone().applyMatrix4(p.m);}
for(const o of obstacles.filter(o=>o.name==='E_KALIP__sac__NEST')){clipGripNotch(T,o.g,o.m);o.bvh=null;update(o,o.m);}
const base=obstacles.filter(o=>!o.name.startsWith('QR_')),cab=env(grid,2,850);
let checks=0,drawers={},carrying=null,local=null,placed={},frames=[],st=null;
const worldTCP=s=>C.clone().multiply(matrix(rig.tcp(s.q,s.rail,s.jaw))),point=s=>{if(!carrying)return null;return new T.Vector3(...local).applyMatrix4(worldTCP(s)).toArray();};
function check(s){checks++;environment(drawers,{});const obs=[...base,...cab],h=hits(s,obs);if(h.length)return h;if(carrying){const p=point(s);productAt(carrying,p,carrying==='Box'?Math.atan2(worldTCP(s).elements[8],worldTCP(s).elements[10]):0);for(const a of products[carrying].parts){for(const b of robot)if(!b.body.includes('/Gripper/')&&intersects(a,b))return ['PRODUCT>'+b.body];for(const b of obs)if(intersects(a,b))return ['PRODUCT>'+b.name];}}return [];}
const angle=x=>Math.atan2(Math.sin(x),Math.cos(x)),mix=(a,b,t)=>({q:a.q.map((q,i)=>q+angle(b.q[i]-q)*t),rail:a.rail+(b.rail-a.rail)*t,jaw:a.jaw+(b.jaw-a.jaw)*t});
function frame(s,label){st=clone(s);const h=check(st);if(h.length)throw Error(label+' '+h);frames.push({state:clone(st),stage:label,drawers:clone(drawers),carrying,product:point(st),placed:clone(placed)});}
function edge(a,b,d=.025){const n=Math.max(1,Math.ceil(Math.max(...a.q.map((q,i)=>Math.abs(angle(b.q[i]-q))))/d),Math.ceil(Math.abs(a.rail-b.rail)/.01));for(let i=0;i<=n;i++)if(check(mix(a,b,i/n)).length)return false;return true;}
function append(b,label){const a=clone(st),n=Math.max(24,Math.ceil(Math.max(...a.q.map((q,i)=>Math.abs(angle(b.q[i]-q))))/.04),Math.ceil(Math.abs(a.rail-b.rail)/.012));for(let i=1;i<=n;i++){const t=i/n;frame(mix(a,b,t*t*(3-2*t)),label);}}
function connect(b,label){console.log('CONNECT',label,'goal',check(b));if(edge(st,b)){append(b,label);return;}if(carrying&&cartesianConnect(b,label))return;if(edge(st,b)){append(b,label);return;}if(!process.argv.includes('--resume-box')){const qs=[[0,-1.4,1.4,-Math.PI/2,-Math.PI/2,0],[0,-1.8,1.8,-Math.PI/2,-Math.PI/2,0],[Math.PI,-1.4,1.4,-Math.PI/2,-Math.PI/2,0],[Math.PI,-1.8,1.8,-Math.PI/2,-Math.PI/2,0],[-Math.PI/2,-2,2.2,0,-Math.PI/2,0],[-Math.PI/2,-2,2.5,.5,-Math.PI/2,0],[Math.PI/2,-2,2.2,0,-Math.PI/2,0]];for(const q of qs){let a={q,rail:st.rail,jaw:st.jaw},c={q,rail:b.rail,jaw:b.jaw};if(!check(a).length&&!check(c).length&&edge(st,a)&&edge(a,c)&&edge(c,b)){append(a,label+' · kolu topla');append(c,label+' · rayda ilerle');append(b,label+' · yaklaş');return;}}if(carrying==='Box'){const begin=clone(st),m0=rig.tcp(begin.q,begin.rail,begin.jaw),m1=rig.tcp(b.q,b.rail,b.jaw);for(const z of [1.15,1.05,1.3])for(const y of [1.4,1.55,1.25])for(const x of [4.75,4.9,4.55]){let a,c;try{let ma=m0.slice(),mc=m1.slice();ma[3]=mc[3]=x;ma[7]=mc[7]=-z;ma[11]=mc[11]=y;a=solveTCP(ma,4.6,begin.jaw,begin.q);c=solveTCP(mc,4.6,b.jaw,b.q);}catch{continue;}if(!check(a).length&&!check(c).length&&edge(begin,a)&&edge(a,c)&&edge(c,b)){console.log('BOX_CORRIDOR',x,y,z);append(a,label+' · boş koridora çık');append(c,label+' · yatay yönlen');append(b,label+' · girişe yaklaş');return;}}}}const begin=clone(st);let random=73537,rand=()=>{random=(random*1664525+1013904223)>>>0;return random/4294967296;},trees=[[{s:begin,parent:-1}],[{s:b,parent:-1}]],side=0;const dist=(a,b)=>Math.hypot(...a.q.map((q,i)=>angle(b.q[i]-q)),2*(a.rail-b.rail));const extend=(tree,goal)=>{let ix=0,d=Infinity;tree.forEach((v,i)=>{const dd=dist(v.s,goal);if(dd<d){d=dd;ix=i;}});const next=mix(tree[ix].s,goal,Math.min(1,.45/d));if(!edge(tree[ix].s,next,.04))return null;tree.push({s:next,parent:ix});return tree.length-1;},chain=(tr,i)=>{let arr=[];while(i>=0){arr.push(tr[i].s);i=tr[i].parent;}return arr.reverse();};for(let n=0;n<1500;n++){let A=trees[side],B=trees[1-side],goal=n%4===0?B[0].s:{q:Array.from({length:6},()=>rand()*2*Math.PI-Math.PI),rail:1.176+rand()*3.684,jaw:begin.jaw};let i=extend(A,goal);if(i!=null)for(let k=0;k<30;k++){let j=extend(B,A[i].s);if(j==null)break;if(dist(B[j].s,A[i].s)<1e-6){let route=side===0?[...chain(A,i),...chain(B,j).reverse()]:[...chain(B,j),...chain(A,i).reverse()];for(let u=0;u<40;u++){const x=Math.floor(rand()*(route.length-2)),y=x+2+Math.floor(rand()*(route.length-x-2));if(edge(route[x],route[y]))route.splice(x+1,y-x-1);}if(!route.every((v,i)=>!i||edge(route[i-1],v,.025)))break;console.log('RRT_FOUND',n,route.length);for(const s of route.slice(1))append(s,label+' · denetlenen geçiş');return;}}side=1-side;if(n%100===99)console.log('RRT',n,trees.map(t=>t.length));}throw Error('Transit not found '+label);}
function solveTCP(m,rail,jaw,seed){let a=rig.solve(m,rail,jaw,seed);if(!a.valid)for(const q of [...Object.values(read('poses_v10.json')).map(v=>v.q),[0,-1.8,1.8,-1.57,-1.57,0],[3.14,-1.8,1.8,-1.57,-1.57,0]]){a=rig.solve(m,rail,jaw,q);if(a.valid)break;}if(!a.valid)throw Error('IK');return{q:a.q,rail,jaw};}
function attach(key,p){carrying=key;local=new T.Vector3(...p).applyMatrix4(worldTCP(st).invert()).toArray();}
function solveCandidate(row,rail,jaw,q,goal){let a=rig.solve(row,rail,jaw,q);if(a.valid)return a;for(const seed of [goal,...Object.values(read('poses_v12.json')).map(p=>p.q)]){a=rig.solve(row,rail,jaw,seed);if(a.valid&&!check({q:a.q,rail,jaw}).length)return a;}return a;}

function cartesianConnect(b,label){
 const start=clone(st),m0=worldTCP(start),m1=worldTCP(b),p0=new T.Vector3().setFromMatrixPosition(m0),p1=new T.Vector3().setFromMatrixPosition(m1),r0=new T.Quaternion().setFromRotationMatrix(m0),r1=new T.Quaternion().setFromRotationMatrix(m1);
 for(const height of [Math.max(p0.y,p1.y,.98),1.12])for(const z of [1.05,1.15]){
  const sourceRail=Math.max(1.176,Math.min(4.86,p0.x+.35));
  const way=[{p:p0,r:r0,rail:start.rail},{p:p0,r:r0,rail:sourceRail},{p:new T.Vector3(p0.x,p0.y,z),r:r0,rail:sourceRail},{p:new T.Vector3(p0.x,height,z),r:r0,rail:sourceRail},{p:new T.Vector3(p1.x,height,z),r:r0,rail:b.rail},{p:new T.Vector3(p1.x,height,z),r:r1,rail:b.rail},{p:p1,r:r1,rail:b.rail}],out=[];let q=start.q,ok=true;
  for(let j=1;j<way.length&&ok;j++){const a=way[j-1],c=way[j],n=Math.max(30,Math.ceil(a.p.distanceTo(c.p)/.009),Math.ceil(Math.abs(a.rail-c.rail)/.01));for(let i=1;i<=n;i++){const t=i/n,ps=a.p.clone().lerp(c.p,t),rs=a.r.clone().slerp(c.r,t),m=C.clone().invert().multiply(new T.Matrix4().compose(ps,rs,new T.Vector3(1,1,1))),row=Array.from({length:16},(_,k)=>m.elements[(k%4)*4+Math.floor(k/4)]),rail=a.rail+(c.rail-a.rail)*t,jaw=start.jaw+(b.jaw-start.jaw)*((j-1+t)/(way.length-1)),ik=solveCandidate(row,rail,jaw,q,b.q),s={q:ik.q,rail,jaw},why=ik.valid?check(s):['IK'];if(why.length){console.log('BLOCK',j,i,why,ps.toArray());ok=false;break;}const prev=out.at(-1)||start,delta=Math.max(...q.map((v,k)=>Math.abs(angle(s.q[k]-v))));if(delta>.08){if(!edge(prev,s)){console.log('BRANCH_BLOCK',j,i,delta);ok=false;break;}const count=Math.ceil(delta/.035);for(let k=1;k<count;k++)out.push(mix(prev,s,k/count));}out.push(s);q=s.q;}}
  console.log('CARTESIAN_TRY',label,height,z,out.length,ok);
  if(ok&&edge(out.at(-1),b)){console.log('CARTESIAN',label,height,z,out.length);for(const s of out)frame(s,label);append(b,label);return true;}
 }
 return false;
}
function addPlaced(key,p){productAt(key,p,0);for(const a of products[key].parts)cab.push(solid('PLACED_'+key,a.g.clone(),a.m.clone()));}
function save(){const summary={version:15,passed:true,completed:Object.keys(placed),frames:frames.length,checks,ideal_grasp:true,continuous_collision_certified:false,qr_column:2,qr_floor_mm:850,method:'Native robot/self/full machine and fixed QR, sampled Cartesian/edge collision checks; ideal attachment, rigid products, no physical grip validation.'};fs.writeFileSync(root+'order_v15.json',JSON.stringify({summary,trajectory:frames}));fs.writeFileSync(root+'order_v15.checkpoint.json',JSON.stringify({drawers,carrying,local,placed,frames,st}));console.log('SAVED',summary.completed,frames.length);}
function sourcePick(key){
 const path=src.results.find(r=>r.key===key+'_pick').path,d=products[key].drawer;
 if(!st){drawers={};frame(path[0].state,key+' · başlangıç');}else connect(path[0].state,key+' · kaynağa yaklaş');
 for(let i=1;i<=25;i++){drawers={[d]:.7*i/25};frame(st,key+' · çekmeceyi aç');}
 for(const f of path){drawers=f.drawers;if(f.carrying&&!carrying){st=f.state;attach(key,tcpScene(st).map((v,i)=>v+f.offset[i]));}frame(f.state,f.stage);}
 for(let i=1;i<=25;i++){drawers={[d]:.7*(1-i/25)};frame(st,key+' · çekmeceyi kapat');}drawers={};
}
function sourceBox(){
 const g=read('grasp_v14.json').results.find(r=>r.key==='Box'),a=g.path[0],tcp=rig.tcp(a.q,a.rail,a.jaw),initial=tcp.slice();initial[7]-=.22;initial[11]+=.10;
 const pre=solveTCP(initial,a.rail,a.jaw,a.q);connect(pre,'Kutu · ön kenara yaklaş');
 let q=st.q;for(let i=1;i<=45;i++){const t=i/45,m=initial.map((v,k)=>v+(tcp[k]-v)*t),s=solveTCP(m,a.rail,a.jaw,q);frame(s,'Kutu · ön kenara gir');q=s.q;}
 for(const s of g.path)frame(s,'Kutu · üst ve alt pedleri kapat');attach('Box',g.product);
 const held=rig.tcp(st.q,st.rail,st.jaw);q=st.q;for(let i=1;i<=12;i++){const m=held.slice();m[11]+=.006*i/12;const s=solveTCP(m,st.rail,st.jaw,q);frame(s,'Kutu · yataktan 6 mm kaldır');q=s.q;}
 const raised=rig.tcp(st.q,st.rail,st.jaw);for(let i=1;i<=90;i++){const m=raised.slice();m[7]-=.48*i/90;const s=solveTCP(m,st.rail,st.jaw,q);frame(s,'Kutu · tamamen yataktan geri çık');q=s.q;}
 const outside=rig.tcp(st.q,st.rail,st.jaw);for(let i=1;i<=45;i++){const m=outside.slice();m[11]+=.10*i/45;const s=solveTCP(m,st.rail,st.jaw,q);frame(s,'Kutu · koridorda yatay kaldır');q=s.q;}
}
function deliver(key){
 const task=delivery.result.tasks.find(t=>t.key===key),path=[...task.sequence].reverse();
 connect(path[0].state,key+' · QR girişine taşı');
 // The source and target are nominal grasp geometry. Align only in the free approach corridor, explicitly ideal.
 const desired=new T.Vector3(...path[0].product).applyMatrix4(worldTCP(st).invert()).toArray(),prior=local;
 if(Math.hypot(...desired.map((v,i)=>v-prior[i]))>.003)console.log('IDEAL_ALIGNMENT',key,desired.map((v,i)=>v-prior[i]));
 for(let i=1;i<=15;i++){local=prior.map((v,k)=>v+(desired[k]-v)*i/15);frame(st,key+' · ideal tutuş hizası');}
 for(const f of path)frame(f.state,key+' · QR gözüne yerleştir');
 placed[key]=point(st);carrying=null;
 // Check the explicit finger-opening transition as well as the retreat.
 append(task.exit[0].state,key+' · parmakları aç');for(const f of task.exit)frame(f.state,key+' · QR’den geri çekil');
 if(key==='Box'){const high=placed.Box.slice();for(let i=1;i<=20;i++){placed.Box=[high[0],high[1]-.025*i/20,high[2]];frame(st,'Kutu · ideal olarak rafa oturt');}}
 addPlaced(key,placed[key]);save();
}
try{
 if(fs.existsSync(root+'order_v15.checkpoint.json'))({drawers,carrying,local,placed,frames,st}=read('order_v15.checkpoint.json'));
 for(const key of Object.keys(placed))addPlaced(key,placed[key]);
 for(const key of ['Cola','Dessert','Box']){if(placed[key])continue;if(key==='Box')sourceBox();else sourcePick(key);deliver(key);}
}catch(e){console.error(e.stack);fs.writeFileSync(root+'order_v15.error.json',JSON.stringify({error:e.message,frames:frames.length,checks,last:frames.at(-1)},null,2));process.exitCode=1;}
