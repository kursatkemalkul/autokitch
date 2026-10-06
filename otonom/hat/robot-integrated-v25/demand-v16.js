function rng(seed){ return function(){ seed|=0; seed=seed+0x6D2B79F5|0; let t=Math.imul(seed^seed>>>15,1|seed);
  t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function mkItems(rnd, cfg){
  if(cfg.lahm && rnd() < cfg.lahmPct/100){ const it=['lahm','lahm']; if(rnd()<0.15) it.push('lahm'); return it; }
  const r=rnd(), n = r<0.65?1 : r<0.90?2 : 3, it=[]; for(let i=0;i<n;i++) it.push('pide'); return it;
}
const AKSAM_EGRI=[0.28, 0.42, 0.30];
const SEN={ tek:{sure:0}, uc:{sure:0}, aksam:{saat:17, n:53, egri:AKSAM_EGRI}, cmt:{saat:17, n:74, egri:AKSAM_EGRI}, surekli:{saat:18} };
function scenarioOrders(cfg){
  const o=[], rnd=rng((cfg.seed||1)*7919+13), mix = cfg.lahm ? ['pide','lahm','lahm'] : ['pide','pide'];
  switch(cfg.scenario){
    case 'tek': o.push({arr:0, items:mix}); break;
    case 'uc':  o.push({arr:0, items:['pide','pide']}, {arr:60, items:mix}, {arr:120, items:['pide']}); break;
    case 'surekli': { const gap=cfg.gapSec;
      if(cfg.randArr){ let t=0; while(t<3600){ t += -Math.log(1-rnd())*gap; if(t<3600) o.push({arr:t, items:mkItems(rnd,cfg)}); } }
      else { for(let t=0;t<3600;t+=gap) o.push({arr:t, items:mkItems(rnd,cfg)}); }
      break; }
    default: { const S=SEN[cfg.scenario]; if(!S||!S.egri) break;
      S.egri.forEach((pay,i)=>{ const n=Math.round(S.n*pay); for(let k=0;k<n;k++) o.push({arr:i*3600+rnd()*3600, items:mkItems(rnd,cfg)}); }); }
  }
  o.sort((a,b)=>a.arr-b.arr);
  return o;
}

export {scenarioOrders,SEN};
export const defaultDemand={lahm:true,lahmPct:65,seed:1,gapSec:90,randArr:true};
