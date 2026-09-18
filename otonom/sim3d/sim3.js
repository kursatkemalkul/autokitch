/* ================= SİPARİŞLER (eski sim ile aynı model: Yemeksepeti 2023 akşam eğrisi) ================= */
const SEN={ akis:{ad:'Sürekli akış · 1 saat'}, tek:{ad:'Tek sipariş · full detay'}, uc:{ad:'3 müşteri (0 · 60 · 120 s)'}, aksam:{ad:'AKŞAM PİKİ · hafta içi · 17–20 h · 53 sipariş',n:53,egri:[.28,.42,.30]}, cmt:{ad:'CUMARTESİ AKŞAMI · 74 sipariş',n:74,egri:[.28,.42,.30]} };
function rng(seed){ let s=(seed>>>0)||1; return ()=>{ s=(s*1664525+1013904223)>>>0; return s/4294967296; }; }
function mkItems(rnd){ if(rnd()<0.65){ const it=['lahm','lahm']; if(rnd()<0.15) it.push('lahm'); return it; } const r=rnd(), n=r<0.65?1:r<0.90?2:3; return Array(n).fill('pide'); }
function siparisler(cfg){ const o=[], rnd=rng(cfg.seed*7919+13);
  if(cfg.sen==='tek') o.push({arr:0, items:[cfg.urun], kola:cfg.kola, tatli:cfg.tatli});
  else if(cfg.sen==='akis'){ const ar=Math.max(20,cfg.aralik||120); for(let tt=0;tt<3600;tt+=ar) o.push({arr:tt, items:mkItems(rnd), kola:rnd()<0.5, tatli:rnd()<0.25}); }   // 2D hat simülasyonundaki sınır testi
  else if(cfg.sen==='uc') o.push({arr:0,items:['pide'],kola:true,tatli:false},{arr:60,items:['lahm','lahm'],kola:true,tatli:true},{arr:120,items:['pide'],kola:false,tatli:false});
  else { const Sn=SEN[cfg.sen]; Sn.egri.forEach((pay,i)=>{ const n=Math.round(Sn.n*pay); for(let k=0;k<n;k++) o.push({arr:i*3600+rnd()*3600, items:mkItems(rnd), kola:rnd()<0.5, tatli:rnd()<0.25}); }); }
  o.sort((a,b)=>a.arr-b.arr); o.forEach((x,i)=>{ x.id=i+1; x.nesneler=[]; x.goz=-1; x.kutuSay=0; x.kolaTeslim=!x.kola; x.tatliTeslim=!x.tatli; x.teslim=null; }); return o; }

/* ================= STOK KONUMLARI ================= */
const OPT={tek:true, zincir:true, firinOnden:70};   // firinOnden: fırın gözü bu kadar saniye içinde boşalacaksa sıradaki ürün ŞİMDİ başlatılır (hamur+pres+topping ~100 s sürer; göz boşalmasını bekleyip sonra başlamak fırını boş bekletir)   // tek: çekmece + pres aynı araba konumundan · zincir: sırada ürün varsa tepsi QR'dan doğrudan prese
function topPos(kolon,sira,k){ const K=KOLON[kolon], kot=K.kotlar[sira], y=kot+15+EL.TOP_R;
  if(kolon==='K1'||(kolon==='K2'&&sira<2)) return V(K.x0+115+130*(k%4), y, 70+135*Math.floor(k/4));
  return V(K.x0+100+105*(k%5), y, 68+91*Math.floor(k/5)); }   // iç 580 × 640: top merkezleri duvardan ≥ 48
function stokKur(){ const s={pide:[],lahm:[]}; for(let i=5;i>=0;i--) s.pide.push({kolon:'K1',sira:i,n:20,k:0}); for(let i=1;i>=0;i--) s.pide.push({kolon:'K2',sira:i,n:20,k:0});   // pide: önce K1 (presin tam altı · tek duruş), üst çekmeceden başla
  for(let i=2;i<8;i++) s.lahm.push({kolon:'K2',sira:i,n:35,k:0}); for(let i=0;i<6;i++) s.lahm.push({kolon:'K3',sira:i,n:35,k:0});
  s.kola=[{kat:1,n:24,k:0},{kat:0,n:24,k:0}]; s.tatli=[{kat:1,n:10,k:0},{kat:0,n:10,k:0}]; return s; }   // E çekmecesi: üst kat önce · alt katta en öndeki tatlı FR5 erişimi dışında (4)
function stokAl(st,tip){ const q=st[tip].find(d=>d.k<d.n); if(!q) return null; const k=q.k++;
  if(tip==='kola'||tip==='tatli'){ const pos=icecekPos(tip,q.kat,k); if(tip==='kola'){ const yan=cekmeceYani(KOLON.KI,pos,YUK.kola.L); if(yan===null) return stokAl(st,tip); return {kat:q.kat,pos,yan}; } return {kat:q.kat,pos}; }
  const pos=topPos(q.kolon,q.sira,k), yan=cekmeceYani(KOLON[q.kolon],pos,YUK.top.L,OPT.tek?presErisir:null); if(yan===null){ st.erisilemeyen=(st.erisilemeyen||0)+1; return stokAl(st,tip); } return {kolon:q.kolon,sira:q.sira,pos,yan,tek:OPT.tek&&presErisir(yan)}; }

/* ================= ERİŞİM ÖN TESTİ ================= */
function erisiyorMu(W,carX){ return ikq(W,carX).ok; }
function gozler(){ return FIR.map((f,g)=>{ const taban=f[0]+100; return {g, tip:g===2?'pide':'lahm', sure:g===2?HIZ.firin.pide:HIZ.firin.lahm, /* pafta: göz 1–2 lahmacun · göz 3 pide */ ok:erisiyorMu(V(FIR_X.cx,taban+60,TZ+500),carFor(FIR_X.cx,taban+20,FIR_X.cz))&&erisiyorMu(V(FIR_X.cx,taban+60,FIR_X.cz+500),carFor(FIR_X.cx,taban+20,FIR_X.cz)), p:null, doneAt:0}; }); }

/* ================= ÇİZELGELEYİCİ · 1 ya da 2 robot AYNI RAYDA =================
   2 robot: SOL robot = tepsi + hamur + pres + topping + fırına koyma + içecek/tatlı (çekmece onun bölgesinde; QR'ın SOL sütununa koyar) · SAĞ robot = fırından alma + kesim + sprey + kutu + QR + tepsiyi nişe geri. İçecekli/tatlılı siparişe QR'ın sol sütunundan göz verilir (SOL robot sağ sütuna giderse SAĞ robota rayda yer kalmıyor).
   Ray kilidi: görev parçalara bölünür, her parça arabanın gezdiği x aralığını ayırır; iki araba arası hiçbir an ARALIK'tan az olamaz. Çakışan parça bekler; yolda boşta duran robot kenara çekilir. */
const ARALIK=800;
function planla(cfg){
  const N=cfg.robot===2?2:1; S.n=N;
  const O=siparisler(cfg), stok=stokKur(), G=gozler(), plan=[], not=[];
  const tepsiler=[]; for(let i=0;i<NIS.n;i++) tepsiler.push({tip:'tepsi',raf:i,pos:nisPos(i),icerik:'',bos:true});
  const P=[]; O.forEach(o=>o.items.forEach((tip,j)=>P.push({id:P.length+1,o,tip,stage:'bekliyor',readyAt:o.arr,tray:null,goz:-1})));
  const R_={press:0,topping:0,kesim:0,sprey:0,kutu:0};
  const gozTip=tp=>G.filter(g=>g.tip===tp&&g.ok);
  if(!gozTip('pide').length) not.push('pide gözü erişilemiyor'); if(!gozTip('lahm').length) not.push('lahmacun gözü erişilemiyor');
  const gozSay={pide:gozTip('pide').length,lahm:gozTip('lahm').length};
  const dolap=qrKapak.map((q,i)=>({i,ri:q.ri,ci:q.ci,o:null,freeAt:0})).sort((a,b)=>a.ri-b.ri||a.ci-b.ci);
  const RBT=[]; for(let i=0;i<N;i++){ const x=N===1?1100:(i?3300:1100); RBT.push({i,t:0,bitis:0,busy:0,res:[],cur:{carX:x,tcp:V(x+300,TR,TZ),t:V(0,0,-1),u:V(0,1,0),yuk:'bos',parmak:70}}); }
  const SOLUN={START:1,TOP:1,KOLA:1,TATLI:1}, rol=(i,tip)=>N===1||(i===0?!!SOLUN[tip]:!SOLUN[tip]);
  let t=0, sonBitis=0, zincir=null; const sayac={tek:0,zincir:0,start:0,yolver:0,rayBekleme:0};
  const dolapAl=(o,t)=>{ if(o.goz>=0) return true; const sol=N>1&&(o.kola||o.tatli), d=(sol?dolap.filter(d=>d.ci===0):N>1?dolap.slice().sort((a,b)=>b.ci-a.ci||a.ri-b.ri):dolap).find(d=>!d.o||d.freeAt<=t); if(!d) return false; d.o=o; d.freeAt=Infinity; o.goz=d.i; return true; };   // göz teslim + müşteri süresi dolana kadar başkasına verilmez
  const blok=(tip,ad,t0,steps,ref,ri)=>{ const s=steps.reduce((a,x)=>a+x.sure,0); const b={tip,ad,t0,t1:t0+s,steps,ref,ri:ri||0}; plan.push(b); return b; };
  const startAday=(wipDus)=>{ const wip=P.filter(p=>['presde','firinda','kesimde','spreyde'].indexOf(p.stage)>=0).length-(wipDus||0); const yeni=P.find(p=>p.stage==='bekliyor'&&p.o.arr<=t); if(!(yeni&&R_.press<=t&&wip<5)) return null; const g=gozTip(yeni.tip), bos=g.filter(x=>!x.p||(x.doneAt-t)<=OPT.firinOnden).length, yakin=P.filter(p=>p.tip===yeni.tip&&p.stage==='presde').length; return bos>yakin?yeni:null; };
  /* --- ray kilidi --- */
  const catis=(ri,a,b)=>ri===0?(a.hi+ARALIK>b.lo):(a.lo-ARALIK<b.hi);
  function parcala(B,car0){ const kes=[0].concat(B.bolmeler.map(x=>x.i)).concat([B.st.length]), adlar=[''].concat(B.bolmeler.map(x=>x.ad)), segs=[]; let car=car0;
    for(let k=0;k<kes.length-1;k++){ const steps=B.st.slice(kes[k],kes[k+1]); if(!steps.length) continue; let lo=car,hi=car,dur=0; steps.forEach(s=>{ dur+=s.sure; if(s.x1!==undefined){ lo=Math.min(lo,s.x0,s.x1); hi=Math.max(hi,s.x0,s.x1); car=s.x1; } }); segs.push({steps,lo,hi,dur,ek:adlar[k]}); } return segs; }
  function koy(r,B,ad,ref){ const segs=parcala(B,B.car0), o=N>1?RBT[1-r.i]:null; let ts=t, ilk=null, son=null, durX=B.car0;
    for(const sg of segs){ let t0=ts;
      if(o){ let gd=0; while(gd++<400){ const cak=o.res.find(q=>q.t1>t0+1e-6&&q.t0<t0+sg.dur-1e-6&&catis(r.i,sg,q)); if(!cak) break; t0=cak.t1; }
        if(t0+sg.dur>o.bitis&&catis(r.i,sg,{lo:o.cur.carX,hi:o.cur.carX})){        // o.bitis = son işinin bittiği an (saat değil: saat olay beklerken ileri atlar)                                  // diğer robot boşta ve yolda → kenara çekilir
          const hedef=Math.min(RAY_X[1],Math.max(RAY_X[0],r.i===0?sg.hi+ARALIK:sg.lo-ARALIK)), tp=Math.max(o.bitis,t), PB=insaci(o.cur), x0=o.cur.carX; PB.tasima('yol ver · taşıma pozu'); PB.kay('yol ver → x '+hedef.toFixed(0),hedef);
          const pb=blok('robot','yol ver',tp,PB.st,null,o.i); pb.yolver=1; o.res.push({t0:tp,t1:pb.t1,lo:Math.min(x0,hedef),hi:Math.max(x0,hedef)}); o.bitis=pb.t1; o.t=Math.max(o.t,pb.t1); sayac.yolver++; t0=Math.max(t0,pb.t1); } }
      if(t0>ts+0.01){ sayac.rayBekleme+=t0-ts; r.res.push({t0:ts,t1:t0,lo:durX,hi:durX}); }                 // beklerken durduğu yer de ayrılmış sayılır (diğer robot oradan geçemez)
      const b=blok('robot',ad+(sg.ek?' · '+sg.ek:''),t0,sg.steps,ref,r.i); r.res.push({t0,t1:b.t1,lo:sg.lo,hi:sg.hi}); r.busy+=sg.dur; if(!ilk) ilk=b; son=b; ts=b.t1; const ks=sg.steps.filter(x=>x.x1!==undefined); if(ks.length) durX=ks[ks.length-1].x1; }
    r.t=ts; r.bitis=ts; sonBitis=Math.max(sonBitis,ts); return {ilk,son,t0:ilk.t0,t1:son.t1}; }
  function teslimKontrol(o,t1){ if(o.teslim) return; if(P.find(p=>p.o===o&&p.stage!=='bitti'&&p.stage!=='iptal')===undefined&&o.kolaTeslim&&o.tatliTeslim){ o.teslim=t1; const d=dolap.find(d=>d.o===o); if(d){ d.freeAt=t1+HIZ.musteri; plan.push({tip:'musteri',ad:'müşteri '+o.id,t0:d.freeAt,t1:d.freeAt+2,ri:0,ref:o,steps:[{ad:'MÜŞTERİ ALDI · sipariş '+o.id,sure:2,fn:()=>{},bitir:()=>{ o.nesneler.forEach(n=>nesneSil(n)); o.nesneler=[]; }}]}); } } }
  let guard=0;
  while(guard++<60000){
    const r=RBT.slice().sort((a,b)=>a.t-b.t||a.i-b.i)[0]; if(!isFinite(r.t)) break; t=r.t;
    tepsiler.forEach(tp=>{ if(tp.bosAt!==undefined&&tp.bosAt<=t){ tp.bos=true; tp.bosAt=undefined; } });
    /* ön kontrol: bu robot, diğerinin ÖNCEDEN ayırdığı bir ray aralığının içinde bekliyorsa önce kenara çekilir (yoksa diğeri içinden geçer) */
    if(N>1){ const o=RBT[1-r.i], x=r.cur.carX, q=o.res.filter(q=>q.t1>t&&catis(r.i,{lo:x,hi:x},q)).sort((a,b)=>a.t0-b.t0)[0];
      if(q){ const lim=o.res.filter(z=>z.t1>t), hedef=Math.min(RAY_X[1],Math.max(RAY_X[0],r.i===0?Math.min(...lim.map(z=>z.lo))-ARALIK:Math.max(...lim.map(z=>z.hi))+ARALIK));
        if(Math.abs(hedef-x)>1){ const PB=insaci(r.cur); PB.tasima('yol ver · taşıma pozu'); PB.kay('yol ver → x '+hedef.toFixed(0),hedef); const pb=blok('robot','yol ver',t,PB.st,null,r.i); pb.yolver=1; r.res.push({t0:t,t1:pb.t1,lo:Math.min(x,hedef),hi:Math.max(x,hedef)}); r.t=pb.t1; r.bitis=pb.t1; sayac.yolver++; sonBitis=Math.max(sonBitis,r.t); continue; } } }
    const cands=[];
    if(zincir&&N===1){ cands.push({pri:-1,p:zincir.p,tip:'START',ready:zincir.p.o.arr,elde:zincir.tray}); zincir=null; } else {
      for(const p of P){ const o=p.o;
        if(p.stage==='presde'&&p.readyAt<=t&&R_.topping<=t){ const g=gozTip(p.tip).find(g=>!g.p); if(g) cands.push({pri:4,p,g,tip:'TOP',ready:p.readyAt}); }
        else if(p.stage==='firinda'&&p.readyAt<=t&&R_.kesim<=t) cands.push({pri:3,p,tip:'KES',ready:p.readyAt});
        else if(p.stage==='kesimde'&&p.readyAt<=t&&R_.sprey<=t) cands.push({pri:2,p,tip:'SPR',ready:p.readyAt});
        else if(p.stage==='spreyde'&&p.readyAt<=t&&R_.kutu<=t&&o.kolaTeslim&&o.tatliTeslim&&dolapAl(o,t)) cands.push({pri:1,p,tip:'FIN',ready:p.readyAt}); }   // göz düzeni: önce sol şerit (kola, tatlı), sonra sağa kutu
      for(const o of O){ if(o.arr>t||o.teslim) continue; const ilk=P.find(p=>p.o===o); const yolda=ilk&&['firinda','kesimde','spreyde','bitti'].indexOf(ilk.stage)>=0, acil=ilk&&['kesimde','spreyde'].indexOf(ilk.stage)>=0?0.5:5;
        if(yolda&&o.kola&&!o.kolaTeslim&&!o.kolaYolda&&dolapAl(o,t)) cands.push({pri:acil,o,tip:'KOLA',ready:o.arr}); if(yolda&&o.tatli&&!o.tatliTeslim&&!o.tatliYolda&&(!o.kola||o.kolaTeslim)&&dolapAl(o,t)) cands.push({pri:acil,o,tip:'TATLI',ready:o.arr}); }
      const yeni=startAday(0); if(yeni&&tepsiler.some(x=>x.bos)) cands.push({pri:6,p:yeni,tip:'START',ready:yeni.o.arr}); }
    const benim=cands.filter(c=>rol(r.i,c.tip));
    if(!benim.length){ const ev=[]; P.forEach(p=>{ if(p.readyAt>t&&p.stage!=='bekliyor'&&p.stage!=='bitti') ev.push(p.readyAt); if(p.stage==='bekliyor'&&p.o.arr>t) ev.push(p.o.arr); }); ev.push(R_.press,R_.topping,R_.kesim,R_.sprey,R_.kutu); dolap.forEach(d=>{ if(d.freeAt>t) ev.push(d.freeAt); }); tepsiler.forEach(tp=>{ if(tp.bosAt!==undefined&&tp.bosAt>t) ev.push(tp.bosAt); }); RBT.forEach(q=>{ if(q!==r&&isFinite(q.t)&&q.t>t) ev.push(q.t); });
      const nx=ev.filter(x=>x>t&&x<1e11); r.t=nx.length?Math.min(...nx):Infinity; continue; }
    benim.sort((a,b)=>a.pri-b.pri||a.ready-b.ready); const c=benim[0], B=insaci(r.cur); B.car0=r.cur.carX; let ad='';
    if(c.tip==='START'){ const p=c.p; p.tray=c.elde||tepsiler.find(x=>x.bos); p.tray.bos=false; const s=stokAl(stok,p.tip); if(!s){ p.stage='iptal'; p.tray.bos=true; not.push('stok bitti: '+p.tip); continue; } p.kolon=s.kolon; p.sira=s.sira; p.topPos=s.pos; p.yan=s.yan; p.carPres=s.tek?s.yan:carPres(); sayac.start++; if(s.tek) sayac.tek++; if(c.elde) sayac.zincir++;
      ad='#'+p.id+' '+p.tip+' · başlat (tepsi → pres altı → hamur tepsinin ortasına)'; G_baslat(B,p,!!c.elde); const b=koy(r,B,ad,p); const C=insaci({carX:0,tcp:V(0,0,0),t:V(0,0,-1),u:V(0,1,0),yuk:'bos',parmak:70}); G_presCevrim(C,p); blok('istasyon','PRES #'+p.id,b.t1,C.st,p); p.stage='presde'; p.readyAt=b.t1+HIZ.pres; R_.press=1e12; }
    else if(c.tip==='TOP'){ const p=c.p; p.goz=c.g.g; c.g.p=p; ad='#'+p.id+' '+p.tip+' · presten al → topping → fırın '+(p.goz+1); G_topping(B,p); const b=koy(r,B,ad,p); R_.press=b.t0+20; R_.topping=b.ilk.t1; p.stage='firinda'; p.readyAt=b.t1+c.g.sure; c.g.doneAt=p.readyAt; b.son.firin=[b.t1,p.readyAt,p.goz]; }
    else if(c.tip==='KES'){ const p=c.p; ad='#'+p.id+' · fırından al → kesim'; G_kesim(B,p); const b=koy(r,B,ad,p); G.find(g=>g.g===p.goz).p=null; const C=insaci({carX:0,tcp:V(0,0,0),t:V(0,0,-1),u:V(0,1,0),yuk:'bos',parmak:70}); G_kesimCevrim(C); blok('istasyon','KESİM #'+p.id,b.t1,C.st,p); R_.kesim=1e12; p.stage='kesimde'; p.readyAt=b.t1+HIZ.kesim; }
    else if(c.tip==='SPR'){ const p=c.p; ad='#'+p.id+' · kesimden al → sprey'; G_sprey(B,p); const b=koy(r,B,ad,p); R_.kesim=b.t0+15; const C=insaci({carX:0,tcp:V(0,0,0),t:V(0,0,-1),u:V(0,1,0),yuk:'bos',parmak:70}); G_spreyCevrim(C); blok('istasyon','SPREY #'+p.id,b.t1,C.st,p); R_.sprey=1e12; p.stage='spreyde'; p.readyAt=b.t1+HIZ.sprey; }
    else if(c.tip==='FIN'){ const p=c.p, o=p.o; const zn=(N===1&&OPT.zincir)?startAday(1):null; ad='#'+p.id+' · spreyden al → kutu → QR göz '+(o.goz+1)+(zn?' → tepsi elde kalır (sıradaki #'+zn.id+')':' → tepsi nişe'); G_bitir(B,p,o,!!zn); const b=koy(r,B,ad,p); b.ilk.bitis=1; R_.sprey=b.t0+15; R_.kutu=b.ilk.t1; p.stage='bitti'; p.bitti=b.ilk.t1; if(zn) zincir={p:zn,tray:p.tray}; else p.tray.bosAt=b.t1; o.kutuSay++; teslimKontrol(o,b.ilk.t1); }
    else { const o=c.o, tip=c.tip==='KOLA'?'kola':'tatli'; const s=stokAl(stok,tip); if(!s){ if(tip==='kola') o.kolaTeslim=true; else o.tatliTeslim=true; not.push('stok bitti: '+tip); continue; }
      o[tip+'Stok']=s; if(tip==='kola') o.kolaYolda=true; else o.tatliYolda=true; ad='sipariş '+o.id+' · '+(tip==='kola'?'içecek':'tatlı')+' → QR göz '+(o.goz+1); G_icecek(B,o,tip); const b=koy(r,B,ad,o); if(tip==='kola') o.kolaTeslim=true; else o.tatliTeslim=true; teslimKontrol(o,b.t1); }
  }
  tepsiler.forEach(tp=>{ tp.bosAt=undefined; });
  plan.sort((a,b)=>a.t0-b.t0);
  const teslim=O.filter(o=>o.teslim), bek=teslim.map(o=>o.teslim-o.arr).sort((a,b)=>a-b), ort=bek.length?bek.reduce((a,b)=>a+b,0)/bek.length:0, biten=P.filter(p=>p.stage==='bitti').length;
  const kpi={N, siparis:O.length, teslim:teslim.length, urun:P.length, ort, max:bek.length?bek[bek.length-1]:0, gec:bek.filter(b=>b>1500).length, sure:sonBitis, robotlar:RBT.map(q=>sonBitis?q.busy/sonBitis:0), robot:sonBitis?Math.max(...RBT.map(q=>q.busy))/sonBitis:0, not, gozSay,
    erisilemeyen:stok.erisilemeyen||0, sayac, urunSure:biten?plan.filter(b=>b.tip==='robot'&&b.ref&&b.ref.tip).reduce((a,b)=>a+(b.t1-b.t0),0)/biten:0, O, P};
  return {plan,kpi,tepsiler,O,P,G,N};
}

/* ================= OYNATICI (zaman tabanlı · bloklar paralel · ileri/geri sarılabilir) ================= */
let anim=null, OYN=null;
function hazirla(planSonuc){ ROB.forEach((rb,i)=>{ const x=(planSonuc&&planSonuc.N===2)?(i?3300:1100):1100; rb.carX=x; rb.t.set(0,0,-1); rb.u.set(0,1,0); rb.yuk='bos'; rb.tasi=null; rb.parmak=70; rb.tcp.set(x+300,TR,TZ); }); S.ri=0; S.n=planSonuc?planSonuc.N:S.n;
  Object.keys(KOLON).forEach(k=>{ S.cek[k]=0; S.cekI[k]=0; }); S.kapak=[0,0,0]; S.qrk={}; S.itme=0; S.akis=null; S.ustPlakaY=0; S.bicakY=0;
  S.nesne.slice().forEach(n=>nesneSil(n)); Object.values(HAVUZ).forEach(h=>h.forEach(m=>{ m.visible=false; m.userData.sahip=null; }));
  if(planSonuc){ planSonuc.tepsiler.forEach(tp=>{ tp.icerik=''; tp.dolu=undefined; tp.pos=nisPos(tp.raf); nesneGoster(tp); }); planSonuc.O.forEach(o=>{ o.nesneler=[]; }); planSonuc.plan.forEach(b=>b.steps.forEach(s=>{ s._basladi=false; })); }
  log.innerHTML=''; }
const ease=t=>t<.5?2*t*t:-1+(4-2*t)*t;
function saat(T){ const b=+($('saat0').value||17)*3600+T; const h=Math.floor(b/3600)%24, m=Math.floor(b%3600/60), s=Math.floor(b%60); return `${h}:${m<10?'0':''}${m}:${s<10?'0':''}${s}`; }
/* motor: T anına kadar olan her şeyi uygular (yalnız ileri) */
function motor(T){ const robotAd=['',''], adim=['','']; let bitti=true, nextT=Infinity;
  for(const b of OYN.bl){ if(T<b.t0){ bitti=false; nextT=Math.min(nextT,b.t0); continue; } S.ri=b.ri||0; let ls=b.t0+b.acc;
    while(b.cursor<b.steps.length){ const s=b.steps[b.cursor]; if(T<ls) break; if(!s._basladi){ if(s.basla) s.basla(); s._basladi=true; }
      if(T>=ls+s.sure){ s.fn(1); if(s.bitir) s.bitir(); b.cursor++; b.acc+=s.sure; ls+=s.sure; continue; } s.fn(ease((T-ls)/s.sure)); if(b.tip==='robot'){ robotAd[b.ri||0]=b.ad; adim[b.ri||0]=s.ad; } break; }
    if(b.cursor<b.steps.length) bitti=false; }
  S.ri=0; return {robotAd,adim,bitti,nextT}; }
function durumYaz(T,m){ const N=OYN.ps.N, satir=i=>`<span style="color:${i?'#ff8c40':'#2997ff'}">${N>1?(i?'SAĞ':'SOL'):'robot'}</span> ${m.robotAd[i]?m.robotAd[i]+' — '+m.adim[i]:'<span style="color:#8a94a4">boşta</span>'}`;
  step.innerHTML=`<span style="color:#8a94a4">${saat(T)}</span> · `+satir(0)+(N>1?'<br>'+satir(1):''); const sc=$('scrub'); if(sc&&!sc._tut) sc.value=T; $('scrubT').textContent=saat(T)+' / '+saat(OYN.ps.kpi.sure); kafaKoy(T); }
/* zamana git: geriye de gider (baştan T'ye kadar yeniden kurar) */
function zamanaGit(ps,T){ if(!OYN||OYN.ps!==ps) OYN={ps,T:0,bl:[],son:0}; hazirla(ps); OYN.bl=ps.plan.map(b=>({...b,cursor:0,acc:0})); OYN.T=Math.max(0,Math.min(ps.kpi.sure+3,T)); const m=motor(OYN.T); ciz(); durumYaz(OYN.T,m); return m; }
function oynat(ps){ dur(); if(!OYN||OYN.ps!==ps||OYN.T>=ps.kpi.sure) zamanaGit(ps,0); OYN.son=performance.now(); $('play').textContent='❚❚ Duraklat';
  function frame(now){ const dt=Math.min(0.1,(now-OYN.son)/1000); OYN.son=now; OYN.T+=dt*(+hiz.value); const m=motor(OYN.T); ciz(); durumYaz(OYN.T,m);
    if(!m.robotAd[0]&&!m.robotAd[1]&&isFinite(m.nextT)&&m.nextT-OYN.T>3&&(+hiz.value)<10) OYN.T=m.nextT-1;                          // herkes boşta: ileri sar
    if(m.bitti){ anim=null; $('play').textContent='▶ Oynat'; return; } anim=requestAnimationFrame(frame); }
  anim=requestAnimationFrame(frame); }
function dur(){ if(anim){ cancelAnimationFrame(anim); anim=null; } const p=$('play'); if(p) p.textContent='▶ Oynat'; }
/* tüm planı zaman adımlarıyla tara: erişim + çarpışma (çevre · kendi gövdesi · diğer robot) */
function sessizKontrol(ps,adimSn){ dur(); zamanaGit(ps,0); const dt=adimSn||(ps.kpi.sure>2500?0.7:0.25), kayit={}; let n=0;
  for(let T=0;T<=ps.kpi.sure+1;T+=dt){ const m=motor(T); ciz(); n++; for(let i=0;i<ps.N;i++){ if(!m.robotAd[i]) continue; const k=ROB[i].sonIK, key=(ps.N>1?(i?'SAĞ · ':'SOL · '):'')+m.robotAd[i]+' | '+m.adim[i]; if((k&&!k.ok)||ROB[i].temas.length){ const r=kayit[key]||(kayit[key]={b:m.robotAd[i],s:m.adim[i],yok:false,eks:0,hs:{}}); if(k&&!k.ok){ r.yok=true; r.eks=Math.max(r.eks,k.D-k.maxD); } ROB[i].temas.forEach(h=>{ r.hs[h.parca+'→'+h.engel.split(' ').slice(0,2).join(' ')]=1; }); } } }
  const rows=Object.values(kayit).map(r=>({b:r.b,s:r.s,yok:r.yok,eks:r.eks,hs:Object.keys(r.hs)}));
  log.innerHTML=`<div><b>${n} an tarandı</b> (${dt} sn arayla) · ${rows.length?'<span class="yok">'+rows.length+' sorunlu adım</span>':'<span class="ok">erişim tam · temas yok</span>'}</div>`+rows.slice(0,40).map(r=>`<div><b>${r.b}</b> · ${r.s} — ${r.yok?'<span class="yok">erişim YOK −'+r.eks.toFixed(0)+'</span> ':''}<span class="yok">${r.hs.join(', ')}</span></div>`).join('');
  zamanaGit(ps,0); return rows; }

/* ================= KPI + GANTT ================= */
function fmt(s){ return s>=60?(s/60).toFixed(1)+' dk':s.toFixed(0)+' s'; }
function kpiYaz(ps){ const k=ps.kpi, e=$('kpi'), T=Math.max(1,k.sure);
  /* saatlik çıkış (kutusu QR'a konan ürün) */
  const hh=[0,0,0,0]; ps.plan.filter(b=>b.bitis).forEach(b=>{ hh[Math.min(3,Math.floor(b.t1/3600))]++; });
  /* robot ne yaptı */
  const mak={}; ps.plan.filter(b=>b.tip==='robot'&&!b.yolver).forEach(b=>{ const key=b.ad.indexOf('başlat')>=0?'tepsi + hamur → pres':b.ad.indexOf('topping')>=0?'topping → fırın':b.ad.indexOf('fırından')>=0?'fırın → kesim':b.ad.indexOf('kesimden')>=0?'kesim → sprey':b.ad.indexOf('kutu')>=0?'kutu → QR → tepsi':b.ad.indexOf('içecek')>=0?'içecek → QR':'tatlı → QR'; (mak[key]=mak[key]||[]).push(b.t1-b.t0); });
  /* hat dengesi: istasyonun çalıştığı süre / toplam süre */
  const dol={pres:0,topping:0,'fırın 1':0,'fırın 2':0,'fırın 3':0,kesim:0,sprey:0,kutu:0};
  ps.plan.forEach(b=>{ if(b.tip==='istasyon'){ const d=b.t1-b.t0; if(b.ad.indexOf('PRES')===0) dol.pres+=d; else if(b.ad.indexOf('KESİM')===0) dol.kesim+=d; else dol.sprey+=d; }
    if(b.firin) dol['fırın '+(b.firin[2]+1)]+=b.firin[1]-b.firin[0]; if(b.tip==='robot') b.steps.forEach(st=>{ if(st.ad.indexOf('DOZAJI')>=0) dol.topping+=st.sure; if(st.ad.indexOf('KUTU KAPAĞI')>=0||st.ad.indexOf('İTİCİ')>=0) dol.kutu+=st.sure; }); });
  const bar=(ad,v,renk)=>`<tr><td>${ad}</td><td style="width:58%"><div style="background:#1f242e;border-radius:4px;height:9px;margin-top:4px"><div style="width:${Math.min(100,v*100).toFixed(0)}%;height:9px;border-radius:4px;background:${renk||(v>.85?'#ff5c5c':v>.6?'#ffb340':'#3ddc84')}"></div></div></td><td style="width:44px">${(v*100).toFixed(0)} %</td></tr>`;
  const cok=k.siparis>3;
  let h='<table>'+[['Sipariş · ürün',`${k.siparis} · ${k.urun}`],['Teslim edilen',`${k.teslim} sipariş`],
    cok?['Çıkan ürün · 1. / 2. / 3. saat / sonrası',`<b>${hh[0]} / ${hh[1]} / ${hh[2]}</b> / ${hh[3]}`]:null,
    ['Ortalama bekleme',`<b>${fmt(k.ort)}</b>`],['En uzun bekleme',fmt(k.max)], cok?['25 dk üstü bekleyen',`<span class="${k.gec?'yok':'ok'}">${k.gec} sipariş</span>`]:null,
    ['Son teslim',saat(k.sure)]].filter(Boolean).map(r=>`<tr><td>${r[0]}</td><td>${r[1]}</td></tr>`).join('')+'</table>';
  h+='<h2>Hat dengesi</h2><table>'+k.robotlar.map((v,i)=>bar(k.N>1?(i?'ROBOT SAĞ':'ROBOT SOL'):'ROBOT',v,v>.85?'#ff5c5c':(i?'#ff8c40':'#2997ff'))).join('')+Object.entries(dol).map(([a,v])=>bar(a,v/T)).join('')+'</table>';
  h+='<h2>Robot ne yaptı · ortalama süre</h2><table>'+Object.entries(mak).map(([a,v])=>`<tr><td>${a}</td><td>${fmt(v.reduce((x,y)=>x+y,0)/v.length)} × ${v.length}</td></tr>`).join('')+`<tr><td><b>ürün başına robot</b></td><td><b>${fmt(k.urunSure)}</b> ${k.N>1?'(iki robotun toplamı)':'→ en fazla '+(3600/Math.max(1,k.urunSure)).toFixed(0)+' ürün/saat'}</td></tr>${k.N>1?`<tr><td>ray kilidi</td><td>${k.sayac.yolver} kez yol verme · ${fmt(k.sayac.rayBekleme)} bekleme</td></tr>`:''}</table>`;
  const nt=[...new Set(k.not)]; if(k.erisilemeyen) nt.push(k.erisilemeyen+' stok konumu atlandı (kol yetişmiyor)'); if(nt.length) h+=`<div class="amb" style="margin-top:6px">${nt.join(' · ')}</div>`;
  e.innerHTML=h;
  $('siparisler').innerHTML=ps.O.slice(0,120).map(o=>`<div>#${o.id} ${saat(o.arr)} · ${o.items.join('+')}${o.kola?' +içecek':''}${o.tatli?' +tatlı':''} → ${o.teslim?'<span class="'+((o.teslim-o.arr)>1500?'yok':'ok')+'">'+fmt(o.teslim-o.arr)+'</span>':'<span class="yok">teslim yok</span>'}</div>`).join('');
}
/* ================= ZAMAN ÇİZELGESİ + OYNATMA ÇUBUĞU ================= */
let GX=null;
function gantt(ps){ const c=$('gantt'), W=Math.max(1200,Math.ceil(ps.kpi.sure/3600*1400)+80), N=ps.N, rows=(N>1?['robot SOL','robot SAĞ']:['robot']).concat(['pres','topping','fırın 1','fırın 2','fırın 3','kesim','sprey','kutu','QR dolabı']), H=30+rows.length*19; c.width=W; c.height=H; const g=c.getContext('2d'); g.fillStyle='#0d1016'; g.fillRect(0,0,W,H);
  const T1=Math.max(600,ps.kpi.sure), x=t=>70+t/T1*(W-90), ry=i=>6+i*19, o=N>1?1:0; GX={x,T1,W};
  g.font='11px sans-serif'; g.fillStyle='#8a94a4'; rows.forEach((r,i)=>g.fillText(r,4,ry(i)+12));
  for(let h=0;h<=T1/3600;h++){ const xx=x(h*3600); g.strokeStyle='#2a2f3a'; g.beginPath(); g.moveTo(xx,2); g.lineTo(xx,H-14); g.stroke(); g.fillText(saat(h*3600),xx+3,H-3); }
  const renk={START:'#3ddc84',TOP:'#ffb340',KES:'#ff8c40',SPR:'#c084fc',FIN:'#2997ff',KOLA:'#ff5c5c',TATLI:'#f5e6c8',YOL:'#596273'};
  ps.plan.forEach(b=>{ if(b.tip==='robot'){ const key=b.yolver?'YOL':b.ad.indexOf('başlat')>=0?'START':b.ad.indexOf('topping')>=0?'TOP':b.ad.indexOf('fırından')>=0?'KES':b.ad.indexOf('kesimden')>=0?'SPR':b.ad.indexOf('kutu')>=0?'FIN':b.ad.indexOf('içecek')>=0?'KOLA':'TATLI'; g.fillStyle=renk[key]; g.fillRect(x(b.t0),ry(b.ri||0),Math.max(1,x(b.t1)-x(b.t0)),15);
      if(b.firin){ g.fillStyle='#d08060'; g.fillRect(x(b.firin[0]),ry(3+o+b.firin[2]),Math.max(1,x(b.firin[1])-x(b.firin[0])),15); }
      b.steps.forEach(()=>{}); if(key==='TOP'&&!b.firin){ g.fillStyle='#ffb340'; g.fillRect(x(b.t0+15),ry(2+o),Math.max(1,x(b.t1)-x(b.t0+15)),15); } if(b.bitis){ g.fillStyle='#2997ff'; g.fillRect(x(b.t0+8),ry(8+o),Math.max(1,x(b.t0+30)-x(b.t0+8)),15); } }
    else if(b.tip==='istasyon'){ const i=b.ad.indexOf('PRES')===0?1:b.ad.indexOf('KESİM')===0?6:7; g.fillStyle='#4a5568'; g.fillRect(x(b.t0),ry(i+o),Math.max(1,x(b.t1)-x(b.t0)),15); } });
  ps.O.forEach(q=>{ if(!q.teslim) return; g.fillStyle='rgba(41,151,255,.35)'; g.fillRect(x(q.arr),ry(9+o),Math.max(1,x(q.teslim+HIZ.musteri)-x(q.arr)),15); g.fillStyle='#fff'; g.fillRect(x(q.arr),ry(9+o),1,15); });
  $('gwrap').style.height=(H+8)+'px'; $('scrubwrap').style.bottom=(H+8)+'px'; const sc=$('scrub'); sc.max=Math.ceil(ps.kpi.sure); sc.value=0; kafaKoy(0); }
function kafaKoy(T){ const k=$('kafa'); if(!k||!GX) return; k.style.left=GX.x(T)+'px'; const w=$('gwrap'); if(anim){ const xx=GX.x(T); if(xx<w.scrollLeft+60||xx>w.scrollLeft+w.clientWidth-80) w.scrollLeft=Math.max(0,xx-w.clientWidth/3); } }

/* ================= UI ================= */
let PLAN=null;
function cfg(){ return {sen:$('sen').value, urun:$('urun').value, kola:$('kola').checked, tatli:$('tatli').checked, seed:+$('seed').value||1, aralik:+$('aralik').value||120, robot:+$('robotN').value||1}; }
function planlaUI(){ dur(); const k=+$('hizp').value; HIZ.serbest=600*k; HIZ.orta=400*k; HIZ.ince=200*k; HIZ.mikro=80*k; HIZ.ray=500*k; PLAN=planla(cfg()); OYN=null; kpiYaz(PLAN); gantt(PLAN); zamanaGit(PLAN,0); step.innerHTML='plan hazır · '+PLAN.plan.filter(b=>b.tip==='robot'&&!b.yolver).length+' robot görevi · ▶ ile oynat ya da alttaki çubuğu sürükle'; return PLAN; }
$('planla').onclick=planlaUI; $('play').onclick=()=>{ if(anim){ dur(); return; } if(!PLAN) planlaUI(); oynat(PLAN); }; $('stop').onclick=()=>{ dur(); if(PLAN) zamanaGit(PLAN,0); };
$('kontrol').onclick=()=>{ if(!PLAN) planlaUI(); $('kontrol').textContent='taranıyor…'; setTimeout(()=>{ sessizKontrol(PLAN); $('kontrol').textContent='Tüm adımları tara · erişim + çarpışma'; },30); };
function senUI(){ const v=$('sen').value; $('tekRow').style.display=v==='tek'?'':'none'; $('akisRow').style.display=v==='akis'?'':'none'; }
['sen','robotN','aralik','urun','kola','tatli'].forEach(id=>$(id).addEventListener('change',()=>{ senUI(); planlaUI(); })); senUI();
/* oynatma çubuğu: tutup sürükle → o ana gider (geri de) */
(function(){ const sc=$('scrub'); let bekleyen=null, calisiyordu=false;
  const git=()=>{ if(bekleyen===null) return; const T=bekleyen; bekleyen=null; if(PLAN) zamanaGit(PLAN,T); };
  sc.addEventListener('pointerdown',()=>{ sc._tut=true; calisiyordu=!!anim; dur(); });
  sc.addEventListener('input',()=>{ const ilk=bekleyen===null; bekleyen=+sc.value; if(ilk) requestAnimationFrame(git); });
  const birak=()=>{ if(!sc._tut) return; sc._tut=false; if(calisiyordu&&PLAN) oynat(PLAN); };
  sc.addEventListener('pointerup',birak); sc.addEventListener('change',birak);
  $('gantt').addEventListener('click',e=>{ if(!GX||!PLAN) return; const r=$('gantt').getBoundingClientRect(), T=(e.clientX-r.left-70)/(GX.W-90)*GX.T1; const c=!!anim; dur(); zamanaGit(PLAN,T); if(c) oynat(PLAN); }); })();
planlaUI();
