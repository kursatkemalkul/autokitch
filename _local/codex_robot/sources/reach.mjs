import fs from 'node:fs';
import {rig,poses,machine,box,hits,root} from './geometry.mjs';
import {environment,collision,obstacles as worldObstacles} from './world.mjs';
import {layout,qrParts} from '../../../otonom/hat/robot-main-v1/qr-layout.js';
const qrNames=n=>n.startsWith('QR_')||n.startsWith('ELK_QR')||n.startsWith('ELK_ANA_PANO');
export const obstacles=machine.filter(s=>!qrNames(s.name)).concat(qrParts().map(p=>box(p.name,p.min,p.max)));
export function target(p,r){return [...r[0],p[0],...r[1],p[1],...r[2],p[2],0,0,0,1];}
export const rot=poses.Cola_place.rotation;
export const seeds=[...Object.values(poses).map(v=>v.q),[-Math.PI, -1, -1.5, 0,-.3,Math.PI/2],[-Math.PI,-2,1.5,-2.5,-.3,Math.PI/2]];
export function solutions(p,r,jaw,rails,extra=[]){const out=[];for(const rail of rails)for(const seed of [...extra,...seeds]){const a=rig.solve(target(p,r),rail,jaw,seed);if(a.valid){const s={q:a.q.map(q=>Math.atan2(Math.sin(q),Math.cos(q))),rail,jaw};if(!out.some(b=>b.rail===rail&&s.q.every((q,i)=>Math.abs(Math.atan2(Math.sin(q-b.q[i]),Math.cos(q-b.q[i])))<.05)))out.push(s);}}return out;}
if(process.argv[1]?.endsWith('reach.mjs')){
 const boxOnly=process.argv.includes('--box-only'),old=boxOnly?JSON.parse(fs.readFileSync(root+'qr_reach.json')):null;const report=[];for(let r=0;r<3;r++)for(let c=0;c<4;c++){const x=layout.x+(c+.5)*layout.pitch,tray=r+''+c;environment({}, {[tray]:layout.stroke});const checks=boxOnly?old.shelves.find(s=>s.shelf===tray).checks.filter(c=>c.type!=='Box'):[];
 for(const type of (boxOnly?['Box']:['Cola','Dessert','Box'])){const floor=layout.floors[r],jaw=poses[type+'_pick'].jaw,rotation=poses[type+'_place'].rotation,product=type==='Cola'?[x,floor+.0585,.91]:type==='Dessert'?[x,floor+.031,.68]:[x,floor+.0235,.71],p=[x,-product[2]+(type==='Box'?.1516:0),product[1]+(type==='Box'?.012:.014)],rails=[x-.7,x-.5,x-.365,x-.2,x+.2].map(v=>Math.max(1.176,Math.min(4.86,v))),sol=solutions(p,rotation,jaw,rails),offset=product.map((v,i)=>v-[p[0],p[2],-p[1]][i]);let passed=null;
 for(const end of sol){if(collision(end,{key:type,position:product,yaw:type==='Box'?Math.PI:0}).length)continue;let prev=end,ok=true;const approach=[];for(let i=0;i<=45;i++){const pt=type==='Box'?[p[0],p[1],p[2]+.10*i/45]:[p[0],p[1]+.20*i/45,p[2]],q=rig.solve(target(pt,rotation),end.rail,jaw,prev.q);const next={q:q.q,rail:end.rail,jaw},m=rig.tcp(q.q,next.rail,jaw),pos=[m[3]+offset[0],m[11]+offset[1],-m[7]+offset[2]];if(!q.valid||collision(next,{key:type,position:pos,yaw:type==='Box'?Math.PI:0}).length){ok=false;break;}approach.push(next);prev=next;}if(ok){passed={state:end,entry:approach.at(-1),samples:approach.length};break;}}
 checks.push({type,product,p,solutions:sol.length,passed:!!passed,example_hit:sol[0]?collision(sol[0],{key:type,position:product,yaw:type==='Box'?Math.PI:0}):['IK'],...passed});}
 report.push({shelf:tray,checks});console.log(tray,checks.map(c=>c.type+':'+c.passed).join(' '));}
 fs.writeFileSync(root+'qr_reach.json',JSON.stringify({layout,method:'All 12 extended trays: can, dessert and 320mm box; native whole robot and product surfaces; 46 entry/exit samples per task; no force or continuous-sweep certification',all_clear:report.every(r=>r.checks.every(c=>c.passed)),shelves:report},null,2));
}






