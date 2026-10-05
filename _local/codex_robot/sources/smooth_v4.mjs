import fs from 'node:fs';
const path='otonom/hat3d/robot-main-v1/order_trajectory_v4.json',r=JSON.parse(fs.readFileSync(path)),out=[];
for(const f of r.trajectory){const prev=out.at(-1);if(prev&&f.carrying&&f.carrying===prev.carrying&&f.carrying!=='Box'&&Math.hypot(...f.offset.map((v,k)=>v-prev.offset[k]))>.005){
 for(let i=1;i<=12;i++){const g=structuredClone(prev);g.offset=prev.offset.map((v,k)=>v+(f.offset[k]-v)*i/12);g.stage=f.stage+' · ideal tutuş geçişi';out.push(g);}
}out.push(f);}
r.trajectory=out;r.frames=out.length;fs.writeFileSync(path,JSON.stringify(r));console.log('SMOOTHED',out.length);
