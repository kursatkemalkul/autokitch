// Platform-neutral workflow. Browser and future Isaac adapter consume the same events.
export const TASK_NAMES={Dough:'Hamur',Cola:'İçecek',Dessert:'Tatlı',Box:'Kutu'};
export function taskFor(stage){return /^(Box|Kutu)/.test(stage)?'Box':/^(Dessert|Tatlı)/.test(stage)?'Dessert':/^(Cola|İçecek)/.test(stage)?'Cola':'Dough';}
export function frameAt(record,t){const f=record.trajectory;let lo=0,hi=f.length-1;while(lo<hi){let m=Math.ceil((lo+hi)/2);if(f[m].time_s<=t)lo=m;else hi=m-1;}const next=Math.min(lo+1,f.length-1),dt=f[next].time_s-f[lo].time_s;return {index:lo,next,mix:dt?Math.min(1,Math.max(0,(t-f[lo].time_s)/dt)):0};}
export function durations(record){const out={Dough:0,Cola:0,Dessert:0,Box:0};for(let i=1;i<record.trajectory.length;i++)out[taskFor(record.trajectory[i].stage)]+=record.trajectory[i].time_s-record.trajectory[i-1].time_s;return out;}
export function compileOrder(record,recipe,{machineReadyAfter=null}={}){
 const trajectory=structuredClone(record.trajectory),clear=trajectory.findIndex(f=>f.stage==='İçecek çekmecesine geç'),box=trajectory.findIndex(f=>taskFor(f.stage)==='Box'),handoff=trajectory[Math.max(0,clear-1)].time_s;
 const delay=machineReadyAfter??recipe.processing_after_dough_s,gateTime=trajectory[box-1].time_s,ready=delay===null?null:handoff+delay,wait=ready===null?0:Math.max(0,ready-gateTime),gateIndex=box-1;
 if(wait){const hold=structuredClone(trajectory[box-1]);hold.time_s+=wait;hold.stage='Makine kutuyu hazırlıyor · hazır sinyali bekleniyor';for(let i=box;i<trajectory.length;i++)trajectory[i].time_s+=wait;trajectory.splice(box,0,hold);}
 const opener=recipe.events.find(e=>e.name.startsWith('AÇICI'))?.time_s;
 const events=recipe.events.filter(e=>!e.name.startsWith('ÇEKMECE')&&!e.name.startsWith('ROBOT')&&!e.name.startsWith('QR')).map(e=>({time_s:handoff+e.time_s-(opener??0),name:e.name,source:recipe.source}));
 events.push({time_s:0,name:'order.accepted / qr.reserved'},{time_s:handoff,name:'table.robot_clear'},{time_s:ready,name:'machine.box_ready'},{time_s:trajectory.at(-1).time_s,name:'order.complete'});
 events.sort((a,b)=>(a.time_s??Infinity)-(b.time_s??Infinity));
 return {...record,trajectory,summary:{...record.summary,duration_s:trajectory.at(-1).time_s,recipe:recipe.id,wait_s:wait,machine_ready_s:ready},events,gate:ready===null?{index:gateIndex,time_s:gateTime,event:'machine.box_ready'}:null,recipe};
}
export function validateMotionContract(record,config){const errors=[];if(config.phase_schema.joint_order.length!==6)errors.push('UR10e joint order');for(let i=0;i<record.trajectory.length;i++){const f=record.trajectory[i];if(!Number.isFinite(f.time_s)||f.state.q.length!==6||!f.state.q.every(Number.isFinite))errors.push('Invalid frame '+i);if(i&&f.time_s<=record.trajectory[i-1].time_s)errors.push('Non-monotonic clock '+i);}return errors;}

// Discrete-event load plan, not an animation or physical proof for every locker/dough slot.
export function planDemand(arrivals,config,record,{pickupSeconds=150,recipeIds=['kasarli','kiymali','kusbasili','sucuklu']}={}){
 const timing=durations(record),resources={robot:0,table:0,oven:Array(4).fill(0),cut:0,pack:0,qr:Array(12).fill(0)},jobs=[],log=[],robotCalendar=[];
 const reserve=(resource,start,duration,label,order)=>{let a=resource==='robot'?start:Math.max(start,resources[resource]);if(resource==='robot'){for(const slot of robotCalendar){if(a+duration<=slot.start_s)break;if(a<slot.end_s)a=slot.end_s;}}resources[resource]=Math.max(resources[resource],a+duration);const slot={order,resource,start_s:a,end_s:a+duration,label};log.push(slot);if(resource==='robot'){robotCalendar.push(slot);robotCalendar.sort((x,y)=>x.start_s-y.start_s);}return a+duration;};
 const eventDelta=(r,a,b,fallback)=>{const x=r.events.find(e=>e.name.startsWith(a)),y=r.events.find(e=>e.name.startsWith(b));return x&&y?y.time_s-x.time_s:fallback;};
 for(let oi=0;oi<arrivals.length;oi++){
  const order=arrivals[oi],id=oi+1,bay=resources.qr.indexOf(Math.min(...resources.qr)),admit=Math.max(order.arr,resources.qr[bay]);let done=admit,units=0;
  const recipeSequence=order.items.map((k,j)=>k==='lahm'?'lahmacun':recipeIds[(oi+j)%recipeIds.length]);
  if(recipeSequence.some(k=>!config.recipes.find(r=>r.id===k)?.events.length)){jobs.push({id,arrival_s:order.arr,state:'awaiting recipe timing',recipes:recipeSequence});continue;}
  let boxCount=0;
  // Pair lahmacun units into one box, using the source two-cycle machine recipe.
  for(let j=0;j<recipeSequence.length;j++){
   const r=config.recipes.find(r=>r.id===recipeSequence[j]);let count=r.id==='lahmacun'&&recipeSequence[j+1]==='lahmacun'?2:1;if(count===2)j++;units+=count;boxCount++;
   const doughStart=Math.max(admit,resources.table),loaded=reserve('robot',doughStart,timing.Dough*count,'dough → table',id);
   const prep=eventDelta(r,'AÇICI','FIRIN',30),bake=eventDelta(r,'FIRIN','KESME',203.15),cut=eventDelta(r,'KESME','KUTU',10.52),pack=eventDelta(r,'KUTU','ROBOT → QR',7.41),slot=resources.oven.indexOf(Math.min(...resources.oven)),ovenIn=Math.max(loaded+prep,resources.oven[slot]);resources.table=ovenIn;resources.oven[slot]=ovenIn+bake;
   log.push({order:id,resource:'table',start_s:loaded,end_s:ovenIn,label:r.name},{order:id,resource:'oven',start_s:ovenIn,end_s:ovenIn+bake,label:r.name});
   const cutEnd=reserve('cut',ovenIn+bake,cut,'cut',id),ready=reserve('pack',cutEnd,pack,'box ready',id);
   // Optional side items occupy robot during the machine's bake window.
   if(boxCount===1){let available=loaded;if(order.cola!==false){available=reserve('robot',available,timing.Cola,'cola → QR',id);done=Math.max(done,available);}if(order.dessert===true){available=reserve('robot',available,timing.Dessert,'dessert → QR',id);done=Math.max(done,available);}}
   done=Math.max(done,reserve('robot',ready,timing.Box,'closed box → QR',id));
  }
  resources.qr[bay]=done+pickupSeconds;jobs.push({id,arrival_s:order.arr,admitted_s:admit,complete_s:done,wait_s:done-order.arr,bay,units,boxes:boxCount,recipes:recipeSequence,state:'planned',geometry_validated:false});
 }
 const completed=jobs.filter(j=>j.state==='planned'),horizon=Math.max(1,...completed.map(j=>j.complete_s)),robotBusy=log.filter(e=>e.resource==='robot').reduce((n,e)=>n+e.end_s-e.start_s,0);
 return {jobs,events:log.sort((a,b)=>a.start_s-b.start_s),summary:{orders:jobs.length,completed:completed.length,units:completed.reduce((n,j)=>n+j.units,0),max_wait_s:Math.max(0,...completed.map(j=>j.wait_s)),robot_utilization:robotBusy/horizon,clearance_geometry_certified:false,method:'FIFO discrete-event load estimate using current motion timings and legacy arrival generator; does not validate multi-box bay capacity or all pickup/QR trajectories.'}};
}
