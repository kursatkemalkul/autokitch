import fs from 'node:fs';const dir='arastirma/_uretec/robot_main_v1/';
const old=fs.readFileSync(dir+'rail_animation_v12.mjs','utf8'),setup=old.slice(old.indexOf('const target='),old.indexOf('let light='));
let common=fs.readFileSync(dir+'order_v15.mjs','utf8');common=common.slice(0,common.indexOf('try{\n if(fs.existsSync'));
common=common.replace('const base=obstacles.filter',setup+'\nconst base=obstacles.filter');
const body=`
try{
 let order=read('order_v15.json');const dough=read('dough_v15.json');if(order.summary.completed.includes('Dough')){const c=read('order_v15.checkpoint.json');order={summary:{completed:Object.keys(c.placed)},trajectory:c.frames};}if(!dough.summary.passed||!['Cola','Dessert','Box'].every(k=>order.summary.completed.includes(k)))throw Error('Tasks incomplete');
 frames=clone(dough.trajectory);st=clone(frames.at(-1).state);drawers={};placed=clone(frames.at(-1).placed);carrying=null;local=null;checks=dough.summary.checks;
 addPlaced('Dough',placed.Dough);
 connect(order.trajectory[0].state,'İçecek çekmecesine geç');
 for(const f of order.trajectory){drawers=f.drawers;placed={Dough:dough.summary.table_m,...f.placed};carrying=f.carrying;if(carrying&&f.product)local=new T.Vector3(...f.product).applyMatrix4(worldTCP(f.state).invert()).toArray();frame(f.state,f.stage);}
 // Add real checked intermediate joint/TCP samples where the tip moves too far per playback frame.
 const sparse=clone(frames),doughObs=cab.filter(o=>o.name==='PLACED_Dough');for(const o of doughObs)cab.splice(cab.indexOf(o),1);frames=[];carrying=null;drawers=clone(sparse[0].drawers);placed=clone(sparse[0].placed);frame(sparse[0].state,sparse[0].stage);
 for(let i=1;i<sparse.length;i++){if(i===dough.trajectory.length)cab.push(...doughObs);const a=sparse[i-1],b=sparse[i],same=a.carrying&&a.carrying===b.carrying,dp=same&&a.product&&b.product?Math.hypot(...a.product.map((v,k)=>v-b.product[k])):0,n=Math.max(1,Math.ceil(dp/.018),Math.ceil(Math.max(...a.state.q.map((v,k)=>Math.abs(Math.atan2(Math.sin(b.state.q[k]-v),Math.cos(b.state.q[k]-v)))))/.035),Math.ceil(Math.abs(b.state.rail-a.state.rail)/.012));
  for(let j=1;j<=n;j++){const t=j/n,s=mix(a.state,b.state,t);drawers=Object.fromEntries([...new Set([...Object.keys(a.drawers),...Object.keys(b.drawers)])].map(k=>[k,(a.drawers[k]||0)+((b.drawers[k]||0)-(a.drawers[k]||0))*t]));placed=clone(j===n?b.placed:a.placed);carrying=same?b.carrying:j===n?b.carrying:a.carrying;
   if(carrying&&same){const la=new T.Vector3(...a.product).applyMatrix4(worldTCP(a.state).invert()),lb=new T.Vector3(...b.product).applyMatrix4(worldTCP(b.state).invert());local=la.lerp(lb,t).toArray();}else if(carrying){const p=j===n?b.product:a.product;local=new T.Vector3(...p).applyMatrix4(worldTCP(s).invert()).toArray();}
   frame(s,b.stage);
  }
 }
 const angle=x=>Math.atan2(Math.sin(x),Math.cos(x));let joint=0,rail=0,productStep=0;
 for(let i=1;i<frames.length;i++){const a=frames[i-1],b=frames[i];joint=Math.max(joint,...b.state.q.map((v,k)=>Math.abs(angle(v-a.state.q[k]))));rail=Math.max(rail,Math.abs(a.state.rail-b.state.rail));if(a.carrying&&a.carrying===b.carrying&&a.product&&b.product)productStep=Math.max(productStep,Math.hypot(...a.product.map((v,k)=>v-b.product[k])));}
 if(joint>.16||rail>.03||productStep>.035)throw Error('Motion discontinuity '+JSON.stringify({joint,rail,productStep}));
 const summary={version:15,passed:true,completed:['Dough','Cola','Dessert','Box'],frames:frames.length,checks,ideal_grasp:true,continuous_collision_certified:false,rigid_dough:true,dough_stock_count:42,table_fixed:true,qr_floor_mm:850,qr_column:2,max_joint_step_deg:joint*180/Math.PI,max_rail_step_mm:rail*1000,max_carried_product_step_mm:productStep*1000,final_positions_m:placed,method:'One order: rigid dough to unchanged table centre, Cola rear-right, Dessert front-right, Box left of same fixed QR bay. Sampled native mesh motion/self/environment checks, ideal grip and explicit corridor grip alignment; no grip-force or falling simulation.'};
 fs.writeFileSync(root+'order_v15.json',JSON.stringify({summary,trajectory:frames}));fs.writeFileSync(root+'order_v15.audit.json',JSON.stringify(summary,null,2));console.log('COMPLETE',summary);
}catch(e){console.error(e.stack);fs.writeFileSync(root+'finish_v15.error.json',JSON.stringify({error:e.message,last:frames.at(-1),checks},null,2));process.exitCode=1;}
`;
fs.writeFileSync(dir+'finish_order_v15.mjs',common+body);
