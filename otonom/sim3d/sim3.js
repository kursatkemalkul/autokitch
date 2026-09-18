/* ================= SİPARİŞLER (eski sim ile aynı model: Yemeksepeti 2023 akşam eğrisi) ================= */
const SEN={ tek:{ad:'Tek sipariş · full detay'}, uc:{ad:'3 müşteri (0 · 60 · 120 s)'}, aksam:{ad:'AKŞAM PİKİ · hafta içi · 17–20 h · 53 sipariş',n:53,egri:[.28,.42,.30]}, cmt:{ad:'CUMARTESİ AKŞAMI · 74 sipariş',n:74,egri:[.28,.42,.30]} };
function rng(seed){ let s=(seed>>>0)||1; return ()=>{ s=(s*1664525+1013904223)>>>0; return s/4294967296; }; }
function mkItems(rnd){ if(rnd()<0.65){ const it=['lahm','lahm']; if(rnd()<0.15) it.push('lahm'); return it; } const r=rnd(), n=r<0.65?1:r<0.90?2:3; return Array(n).fill('pide'); }
function siparisler(cfg){ const o=[], rnd=rng(cfg.seed*7919+13);
  if(cfg.sen==='tek') o.push({arr:0, items:[cfg.urun], kola:cfg.kola, tatli:cfg.tatli});
  else if(cfg.sen==='uc') o.push({arr:0,items:['pide'],kola:true,tatli:false},{arr:60,items:['lahm','lahm'],kola:true,tatli:true},{arr:120,items:['pide'],kola:false,tatli:false});
  else { const Sn=SEN[cfg.sen]; Sn.egri.forEach((pay,i)=>{ const n=Math.round(Sn.n*pay); for(let k=0;k<n;k++) o.push({arr:i*3600+rnd()*3600, items:mkItems(rnd), kola:rnd()<0.5, tatli:rnd()<0.25}); }); }
  o.sort((a,b)=>a.arr-b.arr); o.forEach((x,i)=>{ x.id=i+1; x.nesneler=[]; x.goz=-1; x.kutuSay=0; x.kolaTeslim=!x.kola; x.tatliTeslim=!x.tatli; x.teslim=null; }); return o; }

/* ================= STOK KONUMLARI ================= */
function topPos(kolon,sira,k){ const K=KOLON[kolon], kot=K.kotlar[sira], y=kot+15+EL.TOP_R;
  if(kolon==='K1'||(kolon==='K2'&&sira<2)) return V(K.x0+115+130*(k%4), y, 70+135*Math.floor(k/4));
  return V(K.x0+100+105*(k%5), y, 68+91*Math.floor(k/5)); }   // iç 580 × 640: top merkezleri duvardan ≥ 48
function stokKur(){ const s={pide:[],lahm:[]}; for(let i=0;i<2;i++) s.pide.push({kolon:'K2',sira:i,n:20,k:0}); for(let i=0;i<6;i++) s.pide.push({kolon:'K1',sira:i,n:20,k:0});
  for(let i=2;i<8;i++) s.lahm.push({kolon:'K2',sira:i,n:35,k:0}); for(let i=0;i<6;i++) s.lahm.push({kolon:'K3',sira:i,n:35,k:0});
  s.kola=[{kat:1,n:24,k:0},{kat:0,n:24,k:0}]; s.tatli=[{kat:1,n:10,k:0},{kat:0,n:10,k:0}]; return s; }   // E çekmecesi: üst kat önce · alt katta en öndeki tatlı FR5 erişimi dışında (4)
function stokAl(st,tip){ const q=st[tip].find(d=>d.k<d.n); if(!q) return null; const k=q.k++;
  if(tip==='kola'||tip==='tatli'){ const pos=icecekPos(tip,q.kat,k); if(tip==='kola'){ const yan=cekmeceYani(KOLON.KI,pos,YUK.kola.L); if(yan===null) return stokAl(st,tip); return {kat:q.kat,pos,yan}; } return {kat:q.kat,pos}; }
  const pos=topPos(q.kolon,q.sira,k), yan=cekmeceYani(KOLON[q.kolon],pos,YUK.top.L); if(yan===null){ st.erisilemeyen=(st.erisilemeyen||0)+1; return stokAl(st,tip); } return {kolon:q.kolon,sira:q.sira,pos,yan}; }

/* ================= ERİŞİM ÖN TESTİ ================= */
function erisiyorMu(W,carX){ return ikq(W,carX).ok; }
function gozler(){ return FIR.map((f,g)=>{ const taban=f[0]+100; return {g, tip:g===0?'pide':'lahm', sure:g===0?HIZ.firin.pide:HIZ.firin.lahm, ok:erisiyorMu(V(FIR_X.cx,taban+60,TZ+500),carFor(FIR_X.cx))&&erisiyorMu(V(FIR_X.cx,taban+60,FIR_X.cz+500),carFor(FIR_X.cx)), p:null, doneAt:0}; }); }

/* ================= ÇİZELGELEYİCİ (tek robot · greedy öncelik) ================= */
function planla(cfg){
  const O=siparisler(cfg), stok=stokKur(), G=gozler(), plan=[], not=[];
  const tepsiler=[]; for(let i=0;i<NIS.n;i++) tepsiler.push({tip:'tepsi',raf:i,pos:nisPos(i),icerik:'',bos:true});
  const P=[]; O.forEach(o=>o.items.forEach((tip,j)=>P.push({id:P.length+1,o,tip,stage:'bekliyor',readyAt:o.arr,tray:null,goz:-1})));
  const R_={press:0,topping:0,kesim:0,sprey:0,kutu:0};                         // meşguliyet bitiş zamanı
  const gozTip=t=>G.filter(g=>g.tip===t&&g.ok);
  if(!gozTip('pide').length) not.push('pide gözü (göz 1) erişilemiyor → pide üretilemez'); if(!gozTip('lahm').length) not.push('lahmacun gözü erişilemiyor');
  const gozSay={pide:gozTip('pide').length,lahm:gozTip('lahm').length};
  const dolap=qrKapak.map((q,i)=>({i,ri:q.ri,ci:q.ci,o:null,freeAt:0})).sort((a,b)=>a.ri-b.ri||a.ci-b.ci);
  const cur={carX:1100,tcp:V(1400,TR,TZ),t:V(0,0,-1),u:V(0,1,0),yuk:'bos',parmak:70};
  let t=0, sonBitis=0, robotBusy=0; const bekleme={robot:0,pres:0,topping:0,firin:0,kesim:0,sprey:0,kutu:0,dolap:0,tepsi:0};
  const gozAl=(tip,t)=>gozTip(tip).find(g=>!g.p||g.doneAt<=t&&g.p.stage!=='firinda'&&g.p.stage!=='kesimde'&&false)||gozTip(tip).find(g=>!g.p);
  const dolapAl=(o,t)=>{ if(o.goz>=0) return true; const d=dolap.find(d=>!d.o||d.freeAt<=t); if(!d) return false; if(d.o) d.o=null; d.o=o; o.goz=d.i; return true; };
  const blok=(tip,ad,t0,steps,ref)=>{ const s=steps.reduce((a,x)=>a+x.sure,0); const b={tip,ad,t0,t1:t0+s,steps,ref}; plan.push(b); return b; };
  let guard=0;
  while(guard++<20000){
    const cands=[];
    for(const p of P){ const o=p.o;
      if(p.stage==='presde'&&p.readyAt<=t&&R_.topping<=t){ const g=gozTip(p.tip).find(g=>!g.p); if(g) cands.push({pri:4,p,g,tip:'TOP',ready:p.readyAt}); }
      else if(p.stage==='firinda'&&p.readyAt<=t&&R_.kesim<=t) cands.push({pri:3,p,tip:'KES',ready:p.readyAt});
      else if(p.stage==='kesimde'&&p.readyAt<=t&&R_.sprey<=t) cands.push({pri:2,p,tip:'SPR',ready:p.readyAt});
      else if(p.stage==='spreyde'&&p.readyAt<=t&&R_.kutu<=t&&o.kolaTeslim&&o.tatliTeslim&&dolapAl(o,t)) cands.push({pri:1,p,tip:'FIN',ready:p.readyAt}); }   // göz düzeni: önce sol şerit (kola, tatlı), sonra sağa kutu → parmaklar kutuya değmez
    for(const o of O){ if(o.arr>t||o.teslim) continue; const ilk=o.items.length?P.find(p=>p.o===o):null; const yolda=ilk&&['firinda','kesimde','spreyde','bitti'].indexOf(ilk.stage)>=0, acil=ilk&&['kesimde','spreyde'].indexOf(ilk.stage)>=0?0.5:5;
      if(yolda&&o.kola&&!o.kolaTeslim&&!o.kolaYolda&&dolapAl(o,t)) cands.push({pri:acil,o,tip:'KOLA',ready:o.arr}); if(yolda&&o.tatli&&!o.tatliTeslim&&!o.tatliYolda&&(!o.kola||o.kolaTeslim)&&dolapAl(o,t)) cands.push({pri:acil,o,tip:'TATLI',ready:o.arr}); }
    const wip=P.filter(p=>['presde','firinda','kesimde','spreyde'].indexOf(p.stage)>=0).length;
    const yeni=P.find(p=>p.stage==='bekliyor'&&p.o.arr<=t);
    if(yeni&&R_.press<=t&&tepsiler.some(x=>x.bos)&&wip<5){ const g=gozTip(yeni.tip); const bos=g.filter(x=>!x.p).length, yakin=P.filter(p=>p.tip===yeni.tip&&p.stage==='presde').length; if(bos>yakin) cands.push({pri:6,p:yeni,tip:'START',ready:yeni.o.arr}); }
    if(!cands.length){ const ev=[]; P.forEach(p=>{ if(p.readyAt>t&&p.stage!=='bekliyor'&&p.stage!=='bitti') ev.push(p.readyAt); if(p.stage==='bekliyor'&&p.o.arr>t) ev.push(p.o.arr); }); ev.push(R_.press,R_.topping,R_.kesim,R_.sprey,R_.kutu); dolap.forEach(d=>{ if(d.o&&d.freeAt>t) ev.push(d.freeAt); });
      const nx=ev.filter(x=>x>t); if(!nx.length) break; t=Math.min(...nx); continue; }
    cands.sort((a,b)=>a.pri-b.pri||a.ready-b.ready); const c=cands[0], B=insaci(cur); let ad='', ref=c.p||c.o;
    if(c.tip==='START'){ const p=c.p; p.tray=tepsiler.find(x=>x.bos); p.tray.bos=false; const s=stokAl(stok,p.tip); if(!s){ p.stage='iptal'; not.push('stok bitti: '+p.tip); continue; } p.kolon=s.kolon; p.sira=s.sira; p.topPos=s.pos; p.yan=s.yan; ad='#'+p.id+' '+p.tip+' · başlat (tepsi → pres altı → hamur tepsinin ortasına)';
      G_baslat(B,p); const b=blok('robot',ad,t,B.st,p); const C=insaci({...cur}); G_presCevrim(C,p); blok('istasyon','PRES #'+p.id,b.t1,C.st,p); p.stage='presde'; p.readyAt=b.t1+HIZ.pres; R_.press=1e12; bekleme.robot+=Math.max(0,t-c.ready); t=b.t1; }
    else if(c.tip==='TOP'){ const p=c.p; p.goz=c.g.g; c.g.p=p; ad='#'+p.id+' '+p.tip+' · presten al → topping → fırın '+(p.goz+1); G_topping(B,p); const b=blok('robot',ad,t,B.st,p); R_.press=t+20; R_.topping=b.t1; p.stage='firinda'; p.readyAt=b.t1+c.g.sure; c.g.doneAt=p.readyAt; b.firin=[b.t1,p.readyAt,p.goz]; t=b.t1; }
    else if(c.tip==='KES'){ const p=c.p; ad='#'+p.id+' · fırından al → kesim'; G_kesim(B,p); const b=blok('robot',ad,t,B.st,p); G.find(g=>g.g===p.goz).p=null; const C=insaci({...cur}); G_kesimCevrim(C); blok('istasyon','KESİM #'+p.id,b.t1,C.st,p); R_.kesim=1e12; p.stage='kesimde'; p.readyAt=b.t1+HIZ.kesim; bekleme.firin+=Math.max(0,t-c.ready); t=b.t1; }
    else if(c.tip==='SPR'){ const p=c.p; ad='#'+p.id+' · kesimden al → sprey'; G_sprey(B,p); const b=blok('robot',ad,t,B.st,p); R_.kesim=t+15; const C=insaci({...cur}); G_spreyCevrim(C); blok('istasyon','SPREY #'+p.id,b.t1,C.st,p); R_.sprey=1e12; p.stage='spreyde'; p.readyAt=b.t1+HIZ.sprey; t=b.t1; }
    else if(c.tip==='FIN'){ const p=c.p, o=p.o; ad='#'+p.id+' · spreyden al → kutu → QR göz '+(o.goz+1)+' → tepsi nişe'; G_bitir(B,p,o); const b=blok('robot',ad,t,B.st,p); R_.sprey=t+15; R_.kutu=b.t1; p.stage='bitti'; p.tray.bos=true; o.kutuSay++; teslimKontrol(o,b.t1); t=b.t1; }
    else if(c.tip==='KOLA'||c.tip==='TATLI'){ const o=c.o, tip=c.tip==='KOLA'?'kola':'tatli'; const s=stokAl(stok,tip); if(!s){ if(tip==='kola') o.kolaTeslim=true; else o.tatliTeslim=true; not.push('stok bitti: '+tip); continue; }
      o[tip+'Stok']=s; if(tip==='kola') o.kolaYolda=true; else o.tatliYolda=true; ad='sipariş '+o.id+' · '+(tip==='kola'?'içecek':'tatlı')+' → QR göz '+(o.goz+1); G_icecek(B,o,tip); const b=blok('robot',ad,t,B.st,o); if(tip==='kola') o.kolaTeslim=true; else o.tatliTeslim=true; teslimKontrol(o,b.t1); t=b.t1; }
    { const rb=plan.filter(b=>b.tip==='robot').pop(); if(rb) robotBusy+=rb.t1-rb.t0; } sonBitis=Math.max(sonBitis,t);
  }
  function teslimKontrol(o,t1){ if(o.teslim) return; if(o.items.every((_,j)=>P.find(p=>p.o===o&&p.stage!=='bitti'&&p.stage!=='iptal')===undefined)&&o.kolaTeslim&&o.tatliTeslim){ o.teslim=t1; const d=dolap.find(d=>d.o===o); if(d){ d.freeAt=t1+HIZ.musteri; const C={st:[]}; C.st.push({ad:'MÜŞTERİ ALDI · sipariş '+o.id,sure:2,fn:()=>{},bitir:()=>{ o.nesneler.forEach(n=>nesneSil(n)); o.nesneler=[]; }}); plan.push({tip:'musteri',ad:'müşteri '+o.id,t0:d.freeAt,t1:d.freeAt+2,steps:C.st,ref:o}); } } }
  plan.sort((a,b)=>a.t0-b.t0);
  const teslim=O.filter(o=>o.teslim), bek=teslim.map(o=>o.teslim-o.arr).sort((a,b)=>a-b), ort=bek.length?bek.reduce((a,b)=>a+b,0)/bek.length:0;
  const kpi={siparis:O.length, teslim:teslim.length, urun:P.length, ort:ort, max:bek.length?bek[bek.length-1]:0, p95:bek.length?bek[Math.floor(bek.length*0.95)]:0, gec:bek.filter(b=>b>1500).length, sure:sonBitis, robot:sonBitis?robotBusy/sonBitis:0, not, gozSay,
    erisilemeyen:stok.erisilemeyen||0, urunSure:P.filter(p=>p.stage==='bitti').length?plan.filter(b=>b.tip==='robot'&&b.ref&&b.ref.tip).reduce((a,b)=>a+(b.t1-b.t0),0)/P.filter(p=>p.stage==='bitti').length:0, bekleme, O, P};
  return {plan,kpi,tepsiler,O,P,G};
}

/* ================= OYNATICI (zaman tabanlı · bloklar paralel) ================= */
let anim=null, OYN=null;
function hazirla(planSonuc){ S.carX=1100; S.t.set(0,0,-1); S.u.set(0,1,0); S.yuk='bos'; S.tasi=null; S.parmak=70; S.tcp.set(1400,TR,TZ);
  Object.keys(KOLON).forEach(k=>{ S.cek[k]=0; S.cekI[k]=0; }); S.kapak=[0,0,0]; S.qrk={}; S.itme=0; S.akis=null; S.ustPlakaY=0; S.bicakY=0;
  S.nesne.slice().forEach(n=>nesneSil(n)); Object.values(HAVUZ).forEach(h=>h.forEach(m=>{ m.visible=false; m.userData.sahip=null; }));
  if(planSonuc){ planSonuc.tepsiler.forEach(tp=>{ tp.icerik=''; tp.dolu=undefined; tp.pos=nisPos(tp.raf); nesneGoster(tp); }); planSonuc.plan.forEach(b=>b.steps.forEach(s=>{ s._basladi=false; })); }   // _basladi sıfırlanmazsa 2. oynatmada basla() çalışmaz → tepsi/yük kaybolur
  log.innerHTML=''; step.textContent=''; }
const ease=t=>t<.5?2*t*t:-1+(4-2*t)*t;
function saat(T){ const b=+($('saat0').value||17)*3600+T; const h=Math.floor(b/3600)%24, m=Math.floor(b%3600/60), s=Math.floor(b%60); return `${h}:${m<10?'0':''}${m}:${s<10?'0':''}${s}`; }
function oynat(planSonuc){ dur(); hazirla(planSonuc); const bl=planSonuc.plan.map(b=>({...b,cursor:0,acc:0,started:false})); OYN={T:0,bl,son:performance.now(),planSonuc,kayit:{}};
  function frame(now){ const dt=Math.min(0.1,(now-OYN.son)/1000); OYN.son=now; OYN.T+=dt*(+hiz.value); const T=OYN.T; let robotAd='', bitti=true, nextT=Infinity;
    for(const b of bl){ if(T<b.t0){ bitti=false; nextT=Math.min(nextT,b.t0); continue; } let ls=b.t0+b.acc;
      while(b.cursor<b.steps.length){ const s=b.steps[b.cursor]; if(T<ls) break; if(!s._basladi){ if(s.basla) s.basla(); s._basladi=true; }
        if(T>=ls+s.sure){ s.fn(1); if(s.bitir) s.bitir(); b.cursor++; b.acc+=s.sure; ls+=s.sure; continue; } s.fn(ease((T-ls)/s.sure)); if(b.tip==='robot') robotAd=b.ad+' — '+s.ad; break; }
      if(b.cursor<b.steps.length) bitti=false; }
    ciz(); const k=S.sonIK; if(robotAd){ const key=robotAd.split(' — ')[0]; const r=OYN.kayit[key]||(OYN.kayit[key]={yok:false,eks:0,hits:{}}); if(k&&!k.ok){ r.yok=true; r.eks=Math.max(r.eks,k.D-k.maxD); } S.temas.forEach(h=>{ r.hits[h.parca+' → '+h.engel]=1; }); }
    step.innerHTML=`<span style="color:#8a94a4">${saat(T)}</span> · ${robotAd||'<span style="color:#8a94a4">robot boşta</span>'}`;
    if(!robotAd&&isFinite(nextT)&&nextT-T>3&&(+hiz.value)<10) OYN.T=nextT-1;                          // boşta: ileri sar
    if(bitti){ anim=null; step.innerHTML='bitti · '+saat(T); ozetYaz(); return; } anim=requestAnimationFrame(frame); }
  anim=requestAnimationFrame(frame); }
function dur(){ if(anim){ cancelAnimationFrame(anim); anim=null; } }
function ozetYaz(){ if(!OYN) return; log.innerHTML=''; Object.entries(OYN.kayit).forEach(([ad,r])=>{ const hs=Object.keys(r.hits); const d=document.createElement('div'); d.innerHTML=`${ad} — <span class="${r.yok?'yok':'ok'}">${r.yok?'erişim YOK (−'+r.eks.toFixed(0)+')':'erişim OK'}</span> · <span class="${hs.length?'yok':'ok'}">${hs.length?'TEMAS: '+hs.slice(0,4).join(', '):'temas yok'}</span>`; log.appendChild(d); }); }
/* sessiz kontrol: her robot adımı 12 örnekle */
function sessizKontrol(planSonuc,nOrnek){ dur(); hazirla(planSonuc); const rows=[]; const bl=planSonuc.plan.slice(); // zaman sırasıyla; istasyon bloklarını da uygula
  const evs=[]; bl.forEach(b=>{ let ls=b.t0; b.steps.forEach(s=>{ evs.push({t:ls,b,s}); ls+=s.sure; }); }); evs.sort((a,b)=>a.t-b.t);
  for(const e of evs){ const s=e.s; if(s.basla) s.basla(); let yok=false,eks=0,hits={}; const n=e.b.tip==='robot'?(nOrnek||12):1; for(let i=0;i<=n;i++){ s.fn(i/n); if(e.b.tip==='robot'){ ciz(); const k=S.sonIK; if(!k.ok){ yok=true; eks=Math.max(eks,k.D-k.maxD); } S.temas.forEach(h=>{ hits[h.parca+'→'+h.engel.split(' ')[0]]=1; }); } } if(s.bitir) s.bitir();
    if(e.b.tip==='robot'&&s.sure>0.06){ const hs=Object.keys(hits); rows.push({b:e.b.ad,s:s.ad,yok,eks,hs,sure:s.sure,uz:!!s.uzadi}); } }
  log.innerHTML=''; let sorun=0; rows.forEach((r,i)=>{ if(!(r.yok||r.hs.length)) return; sorun++; const d=document.createElement('div'); d.innerHTML=`<b>${r.b}</b> · ${r.s} — <span class="${r.yok?'yok':'ok'}">${r.yok?'YOK −'+r.eks.toFixed(0):'ok'}</span> ${r.hs.length?'· <span class="yok">'+r.hs.join(', ')+'</span>':''}`; log.appendChild(d); });
  const uzN=rows.filter(r=>r.uz).length; const d=document.createElement('div'); d.innerHTML=`<b>${rows.length} robot adımı</b> · ${uzN} adım eklem hız sınırıyla (${HIZ.eklem}°/s) yavaşladı · ${sorun?'<span class="yok">'+sorun+' sorunlu</span>':'<span class="ok">erişim tam · temas yok</span>'}`; log.prepend(d); hazirla(planSonuc); return rows; }

/* ================= KPI + GANTT ================= */
function fmt(s){ return s>=60?(s/60).toFixed(1)+' dk':s.toFixed(0)+' s'; }
function kpiYaz(ps){ const k=ps.kpi, e=$('kpi'); const robotUrun=ps.plan.filter(b=>b.tip==='robot'&&b.ref&&b.ref.tip);
  const tekUrun={}; robotUrun.forEach(b=>{ const t=b.ref.tip; tekUrun[t]=(tekUrun[t]||0)+(b.t1-b.t0); }); const nP={}; ps.P.forEach(p=>{ if(p.stage==='bitti') nP[p.tip]=(nP[p.tip]||0)+1; });
  const rows=[['Sipariş / ürün',`${k.siparis} / ${k.urun}`],['Teslim edilen',`${k.teslim} sipariş`],['Toplam süre',fmt(k.sure)],['Ortalama bekleme',`<b>${fmt(k.ort)}</b>`],['En uzun bekleme',fmt(k.max)],['%95 bekleme',fmt(k.p95)],['25 dk üstü',`${k.gec} sipariş`],['Robot doluluk',(k.robot*100).toFixed(0)+' %']];
  Object.keys(nP).forEach(t=>rows.push(['Robot süresi / '+t,fmt(tekUrun[t]/nP[t])+' (robot kolu ürün başına)']));
  const mak={}; robotUrun.forEach(b=>{ const key=b.ad.indexOf('başlat')>=0?'başlat (tepsi+hamur)':b.ad.indexOf('topping')>=0?'topping+fırına koy':b.ad.indexOf('fırından')>=0?'fırından al+kesim':b.ad.indexOf('kesimden')>=0?'kesimden al+sprey':'spreyden al+kutu+QR+niş'; (mak[key]=mak[key]||[]).push(b.t1-b.t0); });
  Object.entries(mak).forEach(([kk,arr])=>rows.push(['&nbsp;&nbsp;'+kk,fmt(arr.reduce((a,b)=>a+b,0)/arr.length)]));
  const ick=ps.plan.filter(b=>b.tip==='robot'&&b.ad.indexOf('içecek')>=0), tat=ps.plan.filter(b=>b.tip==='robot'&&b.ad.indexOf('tatlı')>=0);
  if(ick.length) rows.push(['&nbsp;&nbsp;içecek → QR',fmt(ick.reduce((a,b)=>a+b.t1-b.t0,0)/ick.length)]); if(tat.length) rows.push(['&nbsp;&nbsp;tatlı → QR',fmt(tat.reduce((a,b)=>a+b.t1-b.t0,0)/tat.length)]);
  rows.push(['Kullanılabilir göz',`pide ${k.gozSay.pide} · lahm ${k.gozSay.lahm}`]);
  const bk=Object.entries(k.bekleme).filter(x=>x[1]>0).sort((a,b)=>b[1]-a[1]); if(bk.length) rows.push(['Darboğaz (bekleme)',bk.map(x=>x[0]+' '+fmt(x[1])).slice(0,3).join(' · ')]);
  if(k.erisilemeyen) rows.push(['Erişilemeyen stok',k.erisilemeyen+' top/kutu atlandı (kol o konuma yetişmiyor)']);
  if(k.not.length) rows.push(['Not',k.not.join(' · ')]);
  e.innerHTML='<table>'+rows.map(r=>`<tr><td>${r[0]}</td><td>${r[1]}</td></tr>`).join('')+'</table>';
  const sl=$('siparisler'); sl.innerHTML=ps.O.slice(0,80).map(o=>`<div>#${o.id} ${saat(o.arr)} · ${o.items.join('+')}${o.kola?' +içecek':''}${o.tatli?' +tatlı':''} → ${o.teslim?'<span class="'+((o.teslim-o.arr)>1500?'yok':'ok')+'">'+fmt(o.teslim-o.arr)+'</span>':'<span class="yok">teslim yok</span>'}</div>`).join('');
}
function gantt(ps){ const c=$('gantt'), W=Math.max(1200,Math.ceil(ps.kpi.sure/3600*1400)+80), H=230; c.width=W; c.height=H; const g=c.getContext('2d'); g.fillStyle='#0d1016'; g.fillRect(0,0,W,H);
  const T0=0, T1=Math.max(600,ps.kpi.sure), x=t=>60+(t-T0)/(T1-T0)*(W-80), rows=['robot','pres','topping','fırın 1','fırın 2','fırın 3','kesim','sprey','kutu','QR dolabı'], ry=i=>18+i*20;
  g.font='11px sans-serif'; g.fillStyle='#8a94a4'; rows.forEach((r,i)=>g.fillText(r,4,ry(i)+12));
  for(let h=0;h<=T1/3600;h++){ const xx=x(h*3600); g.strokeStyle='#2a2f3a'; g.beginPath(); g.moveTo(xx,10); g.lineTo(xx,H-10); g.stroke(); g.fillText(saat(h*3600),xx+3,H-2); }
  const renk={START:'#3ddc84',TOP:'#ffb340',KES:'#ff8c40',SPR:'#c084fc',FIN:'#2997ff',KOLA:'#ff5c5c',TATLI:'#f5e6c8'};
  ps.plan.forEach(b=>{ if(b.tip==='robot'){ const key=b.ad.indexOf('başlat')>=0?'START':b.ad.indexOf('topping')>=0?'TOP':b.ad.indexOf('kesim')>=0&&b.ad.indexOf('fırından')>=0?'KES':b.ad.indexOf('sprey')>=0&&b.ad.indexOf('kesimden')>=0?'SPR':b.ad.indexOf('kutu')>=0?'FIN':b.ad.indexOf('içecek')>=0?'KOLA':'TATLI'; g.fillStyle=renk[key]||'#fff'; g.fillRect(x(b.t0),ry(0),Math.max(1,x(b.t1)-x(b.t0)),16); if(b.firin){ g.fillStyle='#d08060'; g.fillRect(x(b.firin[0]),ry(3+b.firin[2]),Math.max(1,x(b.firin[1])-x(b.firin[0])),16); } }
    else if(b.tip==='istasyon'){ const i=b.ad.indexOf('PRES')===0?1:b.ad.indexOf('KESİM')===0?6:7; g.fillStyle='#4a5568'; g.fillRect(x(b.t0),ry(i),Math.max(1,x(b.t1)-x(b.t0)),16); } });
  ps.plan.filter(b=>b.tip==='robot'&&b.ad.indexOf('topping')>=0).forEach(b=>{ g.fillStyle='#ffb340'; g.fillRect(x(b.t0+20),ry(2),Math.max(1,x(b.t1-30)-x(b.t0+20)),16); });
  ps.plan.filter(b=>b.tip==='robot'&&b.ad.indexOf('kutu')>=0).forEach(b=>{ g.fillStyle='#2997ff'; g.fillRect(x(b.t0+10),ry(8),Math.max(1,x(b.t1-40)-x(b.t0+10)),16); });
  ps.O.forEach(o=>{ if(!o.teslim) return; g.fillStyle='rgba(41,151,255,.35)'; g.fillRect(x(o.arr),ry(9),Math.max(1,x(o.teslim+HIZ.musteri)-x(o.arr)),16); g.fillStyle='#fff'; g.fillRect(x(o.arr),ry(9),1,16); });
  const L=Object.entries(renk); L.forEach(([k,c],i)=>{ g.fillStyle=c; g.fillRect(60+i*110,H-22,10,10); g.fillStyle='#c9ccd3'; g.fillText(k,74+i*110,H-13); });
}

/* ================= UI ================= */
let PLAN=null;
function cfg(){ return {sen:$('sen').value, urun:$('urun').value, kola:$('kola').checked, tatli:$('tatli').checked, seed:+$('seed').value||1}; }
function planlaUI(){ dur(); hazirla(); const k=+$('hizp').value; HIZ.serbest=600*k; HIZ.orta=400*k; HIZ.ince=200*k; HIZ.mikro=80*k; HIZ.ray=500*k; PLAN=planla(cfg()); kpiYaz(PLAN); gantt(PLAN); hazirla(PLAN); step.textContent='plan hazır · '+PLAN.plan.filter(b=>b.tip==='robot').length+' robot görevi · ▶ ile oynat'; return PLAN; }
$('planla').onclick=planlaUI; $('play').onclick=()=>{ if(!PLAN) planlaUI(); oynat(PLAN); }; $('stop').onclick=()=>{ dur(); step.textContent+=' (durdu)'; };
$('kontrol').onclick=()=>{ if(!PLAN) planlaUI(); sessizKontrol(PLAN); };
[model,omuz,railz,pay,plaka].forEach(e=>e.addEventListener('input',()=>{ omuz_v.textContent=omuz.value; railz_v.textContent=railz.value; if(!anim){ PLAN=null; hazirla(); } }));
$('sen').addEventListener('change',()=>{ PLAN=null; hazirla(); });
hazirla(); planlaUI();

/* belirli bir sim zamanına git (görsel kontrol) */
function zamanaGit(ps,T){ dur(); hazirla(ps); const bl=ps.plan.map(b=>({...b})); let robotAd='';
  for(const b of bl){ if(T<b.t0) continue; let ls=b.t0; for(const s of b.steps){ if(T<ls) break; if(s.basla) s.basla(); if(T>=ls+s.sure){ s.fn(1); if(s.bitir) s.bitir(); ls+=s.sure; continue; } s.fn(ease((T-ls)/s.sure)); if(b.tip==='robot') robotAd=b.ad+' — '+s.ad; break; } }
  ciz(); step.innerHTML=saat(T)+' · '+robotAd; return robotAd; }
