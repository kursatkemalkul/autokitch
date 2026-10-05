import fs from 'node:fs';
import {rig,poses,root} from './geometry.mjs';
import {environment,collision,tcpScene,products,productAt,obstacles} from './world.mjs';
import {solutions,target} from './reach.mjs';
import {layout} from '../../../otonom/hat/robot-main-v1/qr-layout.js';
const clone=x=>JSON.parse(JSON.stringify(x)),angle=x=>Math.atan2(Math.sin(x),Math.cos(x)),lerp=(a,b,t)=>({q:a.q.map((q,i)=>q+angle(b.q[i]-q)*t),rail:a.rail+(b.rail-a.rail)*t,jaw:a.jaw+(b.jaw-a.jaw)*t});
const distance=(a,b)=>Math.hypot(...a.q.map((q,i)=>angle(b.q[i]-q)),(a.rail-b.rail)*2),near=(a,b)=>b.q.map((q,i)=>a.q[i]+angle(q-a.q[i]));
let frames=[],drawers={},trays={},placed={},carrying=null,touching=null,offset=[0,0,0],stage='',s=null,checks=0;
let boxLocal=null;const currentOffset=st=>{if(carrying!=='Box')return offset;const m=rig.tcp(st.q,st.rail,st.jaw),n=Math.hypot(m[2],m[6]);return [.1516*m[2]/n,-.012,-.1516*m[6]/n];};const boxYaw=st=>{const m=rig.tcp(st.q,st.rail,st.jaw);return Math.atan2(m[2],m[6]);};const loc=st=>tcpScene(st).map((v,i)=>v+currentOffset(st)[i]);
function check(st){checks++;if(carrying==='Box'){const m=rig.tcp(st.q,st.rail,st.jaw);if(Math.hypot(m[2],m[6])<.3)return ['Box wrist tilt exceeds preview envelope'];}if(checks%1000===0)console.log('CHECK',stage,checks);return collision(st,carrying?{key:carrying,position:loc(st),yaw:carrying==='Box'?boxYaw(st):0}:{});}
function push(){const h=check(s);if(h.length)throw Error(stage+': '+h.join(', '));const d=clone(s);d.q=d.q.map(angle);frames.push({state:d,drawers:clone(drawers),trays:clone(trays),qr:0,placed:clone(placed),carrying,touching,offset:[...currentOffset(s)],carried_yaw:carrying==='Box'?boxYaw(s):0,placed_box_yaw:placed.Box?Math.PI:0,stage});}
function edge(a,b,fine=false){const n=Math.max(1,Math.ceil(Math.max(...a.q.map((q,i)=>Math.abs(angle(b.q[i]-q))))/(fine?.035:.12)),Math.ceil(Math.abs(a.rail-b.rail)/(fine?.01:.04)));for(let i=1;i<=n;i++)if(check(lerp(a,b,i/n)).length)return false;return true;}
function append(b,seconds=1){const a=clone(s),n=Math.max(Math.ceil(seconds*30),Math.ceil(Math.max(...a.q.map((q,i)=>Math.abs(angle(b.q[i]-q))))/.025),Math.ceil(Math.abs(a.rail-b.rail)/.008));for(let i=1;i<=n;i++){const t=i/n;const smooth=t*t*(3-2*t);s=lerp(a,b,smooth);push();}}
let randomState=19072;const rand=()=>{randomState=(1664525*randomState+1013904223)>>>0;return randomState/4294967296;};
function path(a,b){if(edge(a,b,true))return [b];const trees=[[{s:a,parent:-1}],[{s:b,parent:-1}]];let side=0;function extend(tree,goal){let idx=0,d=Infinity;for(let i=0;i<tree.length;i++){const t=distance(tree[i].s,goal);if(t<d){d=t;idx=i;}}const from=tree[idx].s,t=Math.min(1,.32/d),next=lerp(from,goal,t);if(!edge(from,next))return null;tree.push({s:next,parent:idx});return tree.length-1;}const chain=(tree,i)=>{const p=[];while(i>=0){p.push(tree[i].s);i=tree[i].parent;}return p.reverse();};for(let n=0;n<16000;n++){const A=trees[side],B=trees[1-side],goal=n%6===0?B[0].s:{q:Array.from({length:6},()=>rand()*2*Math.PI-Math.PI),rail:Math.max(1.176,Math.min(a.rail,b.rail)-.15)+rand()*(Math.min(4.86,Math.max(a.rail,b.rail)+.15)-Math.max(1.176,Math.min(a.rail,b.rail)-.15)),jaw:a.jaw};const i=extend(A,goal);if(i!=null){let j;for(let k=0;k<30;k++){j=extend(B,A[i].s);if(j==null)break;if(distance(B[j].s,A[i].s)<1e-6){let route=side===0?[...chain(A,i),...chain(B,j).reverse()]:[...chain(B,j),...chain(A,i).reverse()];for(let m=0;m<150;m++){const u=Math.floor(rand()*(route.length-2)),v=u+2+Math.floor(rand()*(route.length-u-2));if(edge(route[u],route[v],true))route.splice(u+1,v-u-1);}if(route.every((p,k)=>!k||edge(route[k-1],p,true)))return route.slice(1);break;}}}side=1-side;if(n%100===99)console.log('RRT',stage,n+1,trees.map(t=>t.length),checks);}throw Error('Path not found '+stage);}
function moveTo(candidates){console.log('MOVE',stage,candidates.length);const clear=candidates.filter(v=>!check(v).length).sort((a,b)=>distance(s,a)-distance(s,b));if(!clear.length)throw Error('No clear target '+stage);for(const b of clear.slice(0,5)){if(edge(s,b,true)){append(b,1.5);return;}}const stows=[[0,-1.4,1.4,-Math.PI/2,-Math.PI/2,0],[0,-1.8,1.8,-Math.PI/2,-Math.PI/2,0],[0,-2.2,1.8,-1.170796,-Math.PI/2,0],[Math.PI,-1.4,1.4,-Math.PI/2,-Math.PI/2,0],[Math.PI,-1.8,1.4,-1.170796,-Math.PI/2,0],[-Math.PI/2,-1.8,2.5,.5,-Math.PI/2,0],[-Math.PI/2,-2,2.2,0,-Math.PI/2,0],[-Math.PI/2,-2,2.2,.5,-Math.PI/2,0],[-Math.PI/2,-2,2.5,.5,-Math.PI/2,0]];
 for(const goal of clear.slice(0,4))for(const q of stows){const a={q,rail:s.rail,jaw:s.jaw},b={q,rail:goal.rail,jaw:s.jaw};if(!check(a).length&&!check(b).length&&edge(s,a,true)&&edge(a,b,true)&&edge(b,goal,true)){append(a,1.3);append(b,Math.max(1,Math.abs(a.rail-b.rail)/.2));append(goal,1.5);return;}}
 const goal=clear[0];for(const q of stows){const a={q,rail:s.rail,jaw:s.jaw},b={q,rail:goal.rail,jaw:s.jaw};if(check(a).length||check(b).length||!edge(a,b,true))continue;console.log('Stow route',stage);const first=path(s,a);for(const v of first)append(v,.4);append(b,Math.max(1,Math.abs(a.rail-b.rail)/.2));const last=path(s,goal);for(const v of last)append(v,.4);return;}
 const route=path(s,goal);for(const b of route)append(b,.35);}
function line(p,r,rail,jaw,seconds=1){const m=rig.tcp(s.q,s.rail,s.jaw),p0=[m[3],m[7],m[11]],a=clone(s),n=Math.ceil(seconds*30);for(let i=1;i<=n;i++){const t=i/n,pt=p0.map((v,k)=>v+(p[k]-v)*t),rr=a.rail+(rail-a.rail)*t,jj=a.jaw+(jaw-a.jaw)*t;const sol=rig.solve(target(pt,r),rr,jj,s.q);if(!sol.valid)throw Error('IK line '+stage);const next={q:sol.q,rail:rr,jaw:jj};if(!edge(s,next,true))throw Error('Line collision '+stage+' '+check(next));s=next;push();}}
function vary(map,key,to,label){stage=label;const a=map[key]||0;for(let i=1;i<=40;i++){map[key]=a+(to-a)*i/40;environment(drawers,trays);push();}}
function choose(p,r,jaw,rails){return solutions(p,r,jaw,rails,s?[s.q]:[]);}
const specs=[['Dough','Hamur','CEK_K1_lahm_1',null],['Cola','İçecek','CEK_K5_ic1_1','23'],['Dessert','Tatlı','CEK_K6_tatli_1','23'],['Box','Pide kutusu',null,'20']];
try{let done=[];if(process.argv.includes('--resume')&&fs.existsSync(root+'order_trajectory_v4.partial.json')){const saved=JSON.parse(fs.readFileSync(root+(process.argv.includes('--resume-box')?'order_trajectory_v4.box_lift.json':'order_trajectory_v4.partial.json')));frames=saved.trajectory;const f=frames.at(-1);s=clone(f.state);drawers=clone(f.drawers);trays=clone(f.trays);placed=clone(f.placed);carrying=f.carrying;touching=f.touching;offset=[...f.offset];done=Object.keys(placed);console.log('RESUME',done,frames.length);}environment(drawers,trays);for(const [key,label,d,tray] of specs){if(done.includes(key))continue;const pick=clone(poses[key+'_pick']),place=clone(poses[key+'_place']);if(key==='Box')pick.tcp[2]+=.012;
 const r=pick.rotation,jaw=pick.jaw,open=Math.max(0,jaw-(key==='Cola'||key==='Dessert'?1:5)),p=pick.tcp;const rails=key==='Dough'?[1.715,1.85,2.05]:key==='Cola'?[2.18,2.32,2.4]:key==='Dessert'?[4.15,4.4,4.65,2.55]:[3.8,4,4.2,4.4,4.6,4.86];const approachHeight=key==='Dough'?.16:key==='Box'?.16:.26;const pre=key==='Box'?[p[0],p[1]-.46,p[2]]:p.map((v,i)=>i===2?v+approachHeight:v);
 if(!(key==='Box'&&carrying==='Box')){stage=label+' · kaynağın önüne git';const candidates=choose(pre,r,open,rails).filter(st=>{if(!d)return true;const a=drawers[d]||0;let valid=true;for(let i=0;i<=15;i++){drawers[d]=.7*i/15;environment(drawers,trays);if(check(st).length){valid=false;break;}}drawers[d]=a;environment(drawers,trays);return valid;});if(!s){s=candidates.find(v=>!check(v).length);if(!s)throw Error('initial');push();}else moveTo(candidates);
 if(d)vary(drawers,d,.7,label+' · çekmece açılıyor'); stage=label+' · yaklaş';let success=false;
 for(const end of choose(p,r,open,rails).sort((a,b)=>distance(s,a)-distance(s,b))){if(check(end).length)continue;let prev=end,reverse=[end],ok=true;for(let i=1;i<=60;i++){const pt=p.map((v,k)=>v+(pre[k]-v)*i/60),sol=rig.solve(target(pt,r),end.rail,open,prev.q),next={q:sol.q,rail:end.rail,jaw:open};if(!sol.valid||!edge(prev,next,true)){ok=false;break;}reverse.push(next);prev=next;}if(!ok)continue;moveTo([reverse.at(-1)]);for(const next of reverse.reverse().slice(1))append(next,.03);success=true;break;}
 if(!success)throw Error('No approach '+key); touching=key;stage=label+' · kavra';line(p,r,s.rail,jaw,.4);carrying=key;offset=products[key].centre.map((v,i)=>v-tcpScene(s)[i]);if(d)offset[2]+=.7;if(key==='Box'){const m=rig.tcp(s.q,s.rail,s.jaw),v=[offset[0],-offset[2],offset[1]];boxLocal=[0,1,2].map(i=>m[i]*v[0]+m[4+i]*v[1]+m[8+i]*v[2]);}
 stage=label+' · kaldır';// first millimetre clears the support surface
 if(key==='Box'){stage=label+' · önden yatay çıkar';line([p[0],p[1]-.46,p[2]],r,s.rail,jaw,1.3);}const lift=p.map((v,i)=>i===2?v+(key==='Cola'?.29:.18):i===1&&key==='Box'?v-.46:v);line(lift,r,s.rail,jaw,1.3);
 stage=label+' · çekmeceden uzaklaş';const away=lift.map((v,i)=>i===1?v-.20:v);if(key==='Dessert')moveTo(choose(away,r,jaw,rails));else if(key!=='Box')line(away,r,s.rail,jaw,1.2);if(d)vary(drawers,d,0,label+' · çekmece kapanıyor');
 }if(key==='Box')fs.writeFileSync(root+'order_trajectory_v4.box_lift.json',JSON.stringify({version:4,trajectory:frames}));let goal,product,pr=place.rotation,targetRails;
 if(key==='Dough'){goal=place.tcp;product=[1.086,1.024,-.17];goal=[...goal];goal[2]=product[1]+.008;targetRails=[1.176,1.3,1.5];}
 else if(key==='Cola'){product=[5.29,layout.floors[2]+.0575+.001,.91];goal=[product[0],-product[2],product[1]+.014];targetRails=[4.86,4.7,4.5];}
 else if(key==='Dessert'){product=[5.13,layout.floors[2]+.03+.001,.68];goal=[product[0],-product[2],product[1]+.014];targetRails=[4.86,4.7,4.5];}
 else{pr=[[0,-1,0],[0,0,-1],[1,0,0]];product=[3.995,layout.floors[2]+.0225+.001,.71];goal=[product[0],-product[2]+.1516,product[1]+.012];targetRails=[3.295,3.495,3.63,3.795,4.195];}
 // Rotate in free corridor; ideal upright grasp is explicit. Change offset only while away from walls.
 if(key==='Box'&&!trays[tray])vary(trays,tray,.30,'QR '+tray+' · yükleme tepsisi dışarı çıkıyor');stage=label+' · hedef girişine yönlen';const safe=key==='Box'?[goal[0],goal[1],goal[2]+.10]:[goal[0],key==='Dough'?-.50:-.65,Math.max(.65,goal[2]+.13)];moveTo(choose(safe,pr,jaw,targetRails));const newOffset=product.map((v,i)=>v-[goal[0],goal[2],-goal[1]][i]);if(key!=='Box')offset=newOffset;
 if(tray&&!trays[tray])vary(trays,tray,.30,'QR '+tray+' · yükleme tepsisi dışarı çıkıyor');
 const deliveryStart=frames.length;stage=label+' · hedefe yaklaş';const pp=key==='Dough'?[goal[0],-.45,goal[2]]:[goal[0],goal[1],goal[2]+.10];let good=false;
 for(const end of choose(goal,pr,jaw,targetRails).sort((a,b)=>distance(s,a)-distance(s,b))){if(check(end).length){console.log('End hit',key,end.rail,check(end));continue;}let prev=end,reverse=[end],ok=true;for(let i=1;i<=60;i++){const pt=goal.map((v,k)=>v+(pp[k]-v)*i/60),sol=rig.solve(target(pt,pr),end.rail,jaw,prev.q),next={q:sol.q,rail:end.rail,jaw};if(!sol.valid||!edge(prev,next,true)){console.log('Reverse fail',key,end.rail,i,pt,sol.valid,check(next));ok=false;break;}reverse.push(next);prev=next;}if(!ok)continue;
  moveTo([reverse.at(-1)]);for(const next of reverse.reverse().slice(1))append(next,.03);good=true;break;
 }
 if(!good&&key==='Dough'){console.log('Planning curved side approach');moveTo(choose(goal,pr,jaw,targetRails));good=true;}if(!good)throw Error('No placement '+key); placed[key]=product;carrying=null;stage=label+' · bırak';line(goal,pr,s.rail,open,.5);stage=label+' · elini geri çek';const retreat=frames.slice(deliveryStart,-16).map(f=>f.state).reverse();for(const next of retreat)append({...next,jaw:open},.01);touching=null;
 console.log('DONE',key,frames.length,checks);fs.writeFileSync(root+'order_trajectory_v4.partial.json',JSON.stringify({version:4,frames:frames.length,trajectory:frames}));
 }
 stage='Sipariş tamamlandı · tepsiler QR içine giriyor';for(let i=1;i<=40;i++){for(const key of Object.keys(trays))trays[key]=.30*(1-i/40);for(const [key,, ,tray] of specs)if(tray)placed[key][2]+=.30/40;environment(drawers,trays);push();}
 const record={version:4,physics:false,collision_approved:false,discrete_surface_checked:true,machine_base:rig.data.machine_base_commit,tip_sha256:rig.data.tip_sha256,pose_signature:JSON.stringify(poses),frames:frames.length,trajectory:frames,findings:[],checks,layout,plan_error:null};fs.writeFileSync(root+'order_trajectory_v4.json',JSON.stringify(record));console.log('COMPLETE',frames.length,checks);
}catch(e){console.error(e.stack);fs.writeFileSync(root+'planning_error.json',JSON.stringify({stage,error:e.message,frames:frames.length,checks,state:s},null,2));process.exitCode=1;}
























