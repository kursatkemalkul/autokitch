import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import assert from 'node:assert/strict';
import {Rig,I,mul} from '../../../otonom/hat/robot-main-v1/rig.js';
const here=path.dirname(fileURLToPath(import.meta.url));
const out=path.resolve(here,'../../../otonom/hat3d/robot-main-v1');
const read=n=>JSON.parse(fs.readFileSync(path.join(out,n),'utf8'));
const rig=new Rig(read('rig.json')),refs=read('fk_reference.json'),report=[];
for(const r of refs){const m=rig.tcp(r.q,r.rail,r.jaw),pe=Math.hypot(m[3]-r.tcp[0],m[7]-r.tcp[1],m[11]-r.tcp[2]);assert(pe<1e-8,r.key);for(let i=0;i<3;i++)for(let j=0;j<3;j++)assert(Math.abs(m[4*i+j]-r.rotation[i][j])<1e-8);const seed=r.q.map((v,i)=>v+[.025,-.02,.015,-.01,.02,-.015][i]);const solved=rig.solve(m,r.rail,r.jaw,seed);assert(solved.valid,r.key+' IK');const offset=I();offset[3]=.005;const nearby=rig.solve(mul(offset,m),r.rail,r.jaw,r.q);assert(nearby.valid,r.key+' translated IK');report.push({key:r.key,fk_error_m:pe,ik_error_m:solved.position,ik_angle_deg:solved.angle,nearby_ik_error_m:nearby.position});}
const unreachable=I();unreachable[3]=20;assert(!rig.solve(unreachable,2.65,10,refs[0].q).valid);
const a=rig.tcp(refs[0].q,1.7,10),b=rig.tcp(refs[0].q,2.0,10);assert(Math.abs(b[3]-a[3]-.3)<1e-9);
assert(Math.abs(rig.anchor(0)[2]-rig.anchor(45)[2])>.005,'Jaw TCP compensation must change');
fs.writeFileSync(path.join(out,'kinematic_checks.json'),JSON.stringify({passed:true,reference:'Native USD / Python FK',poses:report,unreachable_rejected:true,rail_delta_verified:true,jaw_tcp_compensated:true,physics_verified:false},null,2));
console.log(JSON.stringify({passed:true,poses:report.length,max_fk_error_m:Math.max(...report.map(r=>r.fk_error_m)),unreachable_rejected:true},null,2));
