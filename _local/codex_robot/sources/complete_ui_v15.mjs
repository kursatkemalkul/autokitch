import fs from 'node:fs';const path='otonom/hat/robot-main-v1/light-app.js';let s=fs.readFileSync(path,'utf8');
s=s.replace("d.completed.join(' / ')","d.completed.map(k=>({Dough:'Hamur',Cola:'Kola',Dessert:'Tatlı',Box:'Kutu'}[k])).join(' / ')");
s+=`
// Snapshot buttons use the same audited motion as playback, including the held/released product.
function orderPose(place){if(!railRecord)return;playing=false;lastTime=0;const k=$('product').value,i=railRecord.trajectory.findIndex(f=>place?f.placed[k]:f.carrying===k);if(i<0)return;clipStart=0;clipEnd=null;playTime=i/15;railFrame(i);const p=place?railRecord.trajectory[i].placed[k]:railRecord.trajectory[i].product;camera.position.set(p[0]+.65,p[1]+.65,p[2]+.95);orbit.target.set(p[0],p[1]+.06,p[2]);orbit.update();$('status').textContent=(place?'Bırakma':'Alma')+' pozu · '+k+' · aynı sipariş kaydı';render();}
$('pick').onclick=()=>orderPose(false);$('place').onclick=()=>orderPose(true);
`;
fs.writeFileSync(path,s);const html='otonom/hat/makine_robot.html';let h=fs.readFileSync(html,'utf8');h=h.replace('Hamur → tabla bölümü sıradaki çalışma.','Hamur da çekmeceden alınır ve mevcut tablanın merkezine bırakılır.');h=h.replace('light-app.js?v=15','light-app.js?v=15-complete');fs.writeFileSync(html,h);
