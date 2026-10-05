import fs from 'node:fs';
const p='otonom/hat/robot-main-v1/light-app.js';let s=fs.readFileSync(p,'utf8');
s=s.replace('rigRail.position.x=(d.rail_start_m+d.rail_end_m)/2;',`const rr=reach.rail_requirement; if(rr){$('rail-measure').textContent+=' 12 gözün tüm ürünleri için sağ araba sınırı '+Math.round(rr.carriage_max_m*1000)+' mm; birleşik ray önerisi '+rr.recommended_with_50mm_each_end_mm+' mm. Bu kapsam ayrı giriş/çıkış yollarından hesaplandı.';} const railStart=rr?.rail_start_m??d.rail_start_m,railEnd=rr?.rail_end_m??d.rail_end_m; rigRail.position.x=(railStart+railEnd)/2;`);
s=s.replace('(d.rail_end_m-d.rail_start_m)/(5.1-.936)','(railEnd-railStart)/(5.1-.936)').replace('[d.rail_start_m,d.rail_end_m]','[railStart,railEnd]');
fs.writeFileSync(p,s);
