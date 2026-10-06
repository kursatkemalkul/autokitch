import fs from 'node:fs';
import {Rig,point} from '../../../otonom/hat/robot-integrated-v25/rig.js';
const A='otonom/hat3d/robot-integrated-v25/';
const rig=new Rig(JSON.parse(fs.readFileSync(A+'rig.json')),{mountForward:.1,railForward:.5});
const old=JSON.parse(fs.readFileSync(A+'order_v25.json')).trajectory;
const web=p=>[p[0],p[2],-p[1]],local=[.000000799220388,-.00000114247412,.1442837412011861];
const ix=old.findIndex(f=>f.stage==='Kutu · duvardan uzak koridora çek');
for(const i of [ix-1,old.findIndex(f=>f.stage==='Box · ideal tutuş hizası')]){
 const f=old[i],w=rig.matrices(f.state.q,f.state.rail,f.state.jaw);
 console.log(JSON.stringify({stage:f.stage,q:f.state.q,rail:f.state.rail,product:web(point(rig.tcp(f.state.q,f.state.rail,f.state.jaw),local)),bodies:Object.fromEntries(Object.entries(w).filter(([b])=>b.includes('/Arm/')).map(([b,m])=>[b.split('/').at(-1),web(point(m,[0,0,0]))]))}));
}
const f=old[ix-1];
for(const angle of [-Math.PI/2,-Math.PI,Math.PI/2,Math.PI]){const q=[...f.state.q];q[0]+=angle;console.log(JSON.stringify({angle,product:web(point(rig.tcp(q,f.state.rail,f.state.jaw),local))}));}
