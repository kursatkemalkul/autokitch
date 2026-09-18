/* ================= SİPARİŞLER (eski sim ile aynı model: Yemeksepeti 2023 akşam eğrisi) ================= */
const SEN={ fullpide:{ad:'TAM YÜK · 1 saat · yalnız pide'}, fulllahm:{ad:'TAM YÜK · 1 saat · yalnız lahmacun'}, full:{ad:'TAM YÜK · 1 saat · içeceksiz'}, fullic:{ad:'TAM YÜK · 1 saat · içecek + tatlı'}, akis:{ad:'Sürekli akış · 1 saat'}, tek:{ad:'Tek sipariş · full detay'}, uc:{ad:'3 müşteri (0 · 60 · 120 s)'}, aksam:{ad:'AKŞAM PİKİ · hafta içi · 17–20 h · 53 sipariş',n:53,egri:[.28,.42,.30]}, cmt:{ad:'CUMARTESİ AKŞAMI · 74 sipariş',n:74,egri:[.28,.42,.30]} };
function rng(seed){ let s=(seed>>>0)||1; return ()=>{ s=(s*1664525+1013904223)>>>0; return s/4294967296; }; }
function mkItems(rnd){ if(rnd()<0.65){ const it=['lahm','lahm']; if(rnd()<0.15) it.push('lahm'); return it; } const r=rnd(), n=r<0.65?1:r<0.90?2:3; return Array(n).fill('pide'); }
function siparisler(cfg){ const o=[], rnd=rng(cfg.seed*7919+13);
  if(cfg.sen==='tek') o.push({arr:0, items:[cfg.urun], kola:cfg.kola, tatli:cfg.tatli});
  else if(cfg.sen==='akis'){ const ar=Math.max(20,cfg.aralik||120); for(let tt=0;tt<3600;tt+=ar) o.push({arr:tt, items:mkItems(rnd), kola:rnd()<0.5, tatli:rnd()<0.25}); }   // 2D hat simülasyonundaki sınır testi
  else if(cfg.sen==='fullpide'||cfg.sen==='fulllahm'){ for(let k=0;k<80;k++) o.push({arr:0, items:[cfg.sen==='fullpide'?'pide':'lahm'], kola:false, tatli:false}); }
  else if(cfg.sen==='full'||cfg.sen==='fullic'){ for(let k=0;k<45;k++) o.push({arr:0, items:mkItems(rnd), kola:cfg.sen==='fullic'&&rnd()<0.5, tatli:cfg.sen==='fullic'&&rnd()<0.25}); }   // tam yük: kuyruk hep dolu (45 sipariş t=0'da) · ürün karışımı ve içecek %50 / tatlı %25 akşam modeliyle aynı
  else if(cfg.sen==='uc') o.push({arr:0,items:['pide'],kola:true,tatli:false},{arr:60,items:['lahm','lahm'],kola:true,tatli:true},{arr:120,items:['pide'],kola:false,tatli:false});
  else { const Sn=SEN[cfg.sen]; Sn.egri.forEach((pay,i)=>{ const n=Math.round(Sn.n*pay); for(let k=0;k<n;k++) o.push({arr:i*3600+rnd()*3600, items:mkItems(rnd), kola:rnd()<0.5, tatli:rnd()<0.25}); }); }
  o.sort((a,b)=>a.arr-b.arr); o.forEach((x,i)=>{ x.id=i+1; x.nesneler=[]; x.goz=-1; x.kutuSay=0; x.kolaTeslim=!x.kola; x.tatliTeslim=!x.tatli; x.teslim=null; }); return o; }

/* ================= STOK KONUMLARI ================= */
const OPT={tut:true,   /* tut: kesim + spreyde tepsi robotun elinde kalır (bırak-al yok), kutu müsaitse zincirleme kutu + QR */ firinEsnek:true, raf:'yok',   /* 2 robotta aktarma gözü: 'hep' = SOL hep göze bırakır · 'yok' = SOL doğrudan fırına (v17 akışı) · 'karma' = fırın kolonu doluysa göz */ tek:true, zincir:true, firinOnden:95, sagYon:-1, evSol:1300, evSag:3300};   // evSol / evSag: işi olmayan robotun kolunu toplayıp beklediği yer (diğerinin çalışma alanının dışında)   // sagYon: 2 robotta SAĞ robot fırın/kesim/sprey/nişe hangi yandan yanaşır (−1 = sağından: SOL robotun bölgesine girmez)   // firinOnden: fırın gözü bu kadar saniye içinde boşalacaksa sıradaki ürün ŞİMDİ başlatılır (hamur+pres+topping ~100 s sürer; göz boşalmasını bekleyip sonra başlamak fırını boş bekletir)   // tek: çekmece + pres aynı araba konumundan · zincir: sırada ürün varsa tepsi QR'dan doğrudan prese
function topPos(kolon,sira,k){ const K=KOLON[kolon], kot=K.kotlar[sira], y=kot+15+EL.TOP_R;
  if(kolon==='K1'||(kolon==='K2'&&sira<2)) return V(K.x0+115+130*(k%4), y, 70+135*Math.floor(k/4));
  return V(K.x0+100+105*(k%5), y, 68+91*Math.floor(k/5)); }   // iç 580 × 640: top merkezleri duvardan ≥ 48
function stokKur(){ const s={pide:[],lahm:[]}; for(let i=5;i>=0;i--) s.pide.push({kolon:'K1',sira:i,n:20,k:0}); for(let i=1;i>=0;i--) s.pide.push({kolon:'K2',sira:i,n:20,k:0});   // pide: önce K1 (presin tam altı · tek duruş), üst çekmeceden başla
  for(let i=2;i<8;i++) s.lahm.push({kolon:'K2',sira:i,n:35,k:0}); for(let i=0;i<6;i++) s.lahm.push({kolon:'K3',sira:i,n:35,k:0});
  s.kola=[{kat:1,n:24,k:0},{kat:0,n:24,k:0}]; s.tatli=[{kat:1,n:10,k:0},{kat:0,n:10,k:0}]; return s; }   // E çekmecesi: üst kat önce · alt katta en öndeki tatlı FR5 erişimi dışında (4)
/* ================= ERİŞİM ÖN TESTİ ================= */
function erisiyorMu(W,carX){ return ikq(W,carX).ok; }
function gozler(){ return FIR.map((f,g)=>{ const taban=f[0]+100; return {g, tip:g===2?'pide':'lahm', sure:g===2?HIZ.firin.pide:HIZ.firin.lahm, /* pafta: göz 1–2 lahmacun · göz 3 pide */ ok:erisiyorMu(V(FIR_X.cx,taban+60,TZ+500),carFor(FIR_X.cx,taban+20,FIR_X.cz,1))&&erisiyorMu(V(FIR_X.cx,taban+60,FIR_X.cz+500),carFor(FIR_X.cx,taban+20,FIR_X.cz,1)), p:null, doneAt:0}; }); }

/* ================= ÇİZELGELEYİCİ · 1 ya da 2 robot AYNI RAYDA =================
   DİNAMİK GÖREV DAĞITIMI: boşalan robot, YAPABİLDİĞİ işlerden en önceliklisini alır (sabit rol yok).
     - yalnız SOL yapabilir : tepsi + hamur → pres (pres x 350, SAĞ robot oraya giremez: SOL'a rayda yer kalmaz) · presten al → topping → fırın
     - yalnız SAĞ yapabilir : kutu + QR (kutulama x 3550, SOL oraya giremez)
     - ikisi de yapabilir    : fırından al → kesim · kesim → sprey · içecek · tatlı (SOL yalnız QR'ın sol sütununa)
     - "asıl sahibi" SAĞ olan ortak işleri SOL ancak kendi işi yokken ve SAĞ ≥ 8 s daha meşgulken alır (SOL darboğaz: pres + topping yalnız onda)
   RAY KİLİDİ: her görev parçası iki aralık ayırır — ALT (araba, y < 260): araba merkezleri arası ≥ 430 · ÜST (kaide + kol + yük): aralıklar arası ≥ 100.
     Parça, diğer robotun ayırdığı aralıkla çakışıyorsa bekler; beklediği yer de çakışıyorsa görev hiç başlamaz (daha geç denenir).
     Boşta duran robot yoldaysa kolunu toplayıp (park pozu) kenara çekilir. */
const PAY_UST=100, PAY_ALT=430;
function stokBak(st,tip,tercih){ for(;;){ const q=st[tip].find(d=>d.k<d.n); if(!q) return null; const k=q.k;
    if(tip==='kola'||tip==='tatli'){ const pos=icecekPos(tip,q.kat,k); if(tip==='tatli') return {q,kat:q.kat,pos}; const yan=cekmeceYani(KOLON.KI,pos,YUK.kola.L,tercih); if(yan===null){ q.k++; st.erisilemeyen=(st.erisilemeyen||0)+1; continue; } return {q,kat:q.kat,pos,yan}; }
    const pos=topPos(q.kolon,q.sira,k), yan=cekmeceYani(KOLON[q.kolon],pos,YUK.top.L,OPT.tek?presErisir:null); if(yan===null){ q.k++; st.erisilemeyen=(st.erisilemeyen||0)+1; continue; } return {q,kolon:q.kolon,sira:q.sira,pos,yan,tek:OPT.tek&&presErisir(yan)}; } }
function planla(cfg){
  const N=cfg.robot===2?2:1; S.n=N;
  const O=siparisler(cfg), stok=stokKur(), G=gozler(), plan=[], not=[];
  const tepsiler=[]; for(let i=0;i<NIS.n;i++) tepsiler.push({tip:'tepsi',raf:i,pos:nisPos(i),icerik:'',bos:true});
  const P=[]; O.forEach(o=>o.items.forEach((tip,j)=>P.push({id:P.length+1,o,tip,stage:'bekliyor',readyAt:o.arr,tray:null,goz:-1})));
  const R_={press:0,topping:0,kesim:0,sprey:0,kutu:0,raf:0};
  const gozTip=tp=>G.filter(g=>(OPT.firinEsnek||g.tip===tp)&&g.ok);   /* firinEsnek: 3 göz de hem pide/pizza hem lahmacun pişirir · süre ürüne göre (Kemal 18 Eyl 2026) */
  if(!gozTip('pide').length) not.push('pide gözü erişilemiyor'); if(!gozTip('lahm').length) not.push('lahmacun gözü erişilemiyor');
  const gozSay={pide:gozTip('pide').length,lahm:gozTip('lahm').length};
  const dolap=qrKapak.map((q,i)=>({i,ri:q.ri,ci:q.ci,o:null,freeAt:0})).sort((a,b)=>a.ri-b.ri||a.ci-b.ci);
  const kopya=c=>({carX:c.carX,tcp:c.tcp.clone(),t:c.t.clone(),u:c.u.clone(),yuk:c.yuk,parmak:c.parmak});
  const RBT=[]; for(let i=0;i<N;i++){ const x=robotX0(N,i); RBT.push({i,t:0,bitis:0,busy:0,res:[],is:{},yon:(N===2&&i===1)?OPT.sagYon:1,cur:{carX:x,tcp:parkTcp(x),t:V(0,0,-1),u:V(0,1,0),yuk:'bos',parmak:70}}); }
  let t=0, sonBitis=0, zincir=null; const sayac={tek:0,zincir:0,start:0,yolver:0,rayBekleme:0,yardim:0,neden:{}};
  const dolapAl=(o,t)=>{ if(o.goz>=0) return true; const ickili=o.kola||o.tatli, sira=N>1?(ickili?dolap.slice().sort((a,b)=>a.ci-b.ci||a.ri-b.ri):dolap.slice().sort((a,b)=>b.ci-a.ci||a.ri-b.ri)):dolap, d=sira.find(d=>!d.o||d.freeAt<=t); if(!d) return false; d.o=o; d.freeAt=Infinity; o.goz=d.i; return true; };   // 2 robot: içecekli sipariş önce SOL sütun (SOL robot da yardım edebilsin), içeceksiz önce SAĞ sütun
  const blok=(tip,ad,t0,steps,ref,ri)=>{ const s=steps.reduce((a,x)=>a+x.sure,0); const b={tip,ad,t0,t1:t0+s,steps,ref,ri:ri||0}; plan.push(b); return b; };
  /* sıradaki başlatılacak ürün: fırın gözü uygun olan İLK ürün (sıradaki pide fırın bekliyorsa arkadaki lahmacun öne geçer — robot boş durmaz) */
  const startAday=(wipDus)=>{ const wip=P.filter(p=>['presde','rafta','firinda','kesimde','spreyde'].indexOf(p.stage)>=0).length-(wipDus||0); if(R_.press>t||wip>=NIS.n) return null; const bakildi={};
    for(const p of P){ if(p.stage!=='bekliyor'||p.o.arr>t||bakildi[p.tip]) continue; bakildi[p.tip]=1; const g=gozTip(p.tip), bos=g.filter(x=>!x.p||(x.doneAt-t)<=OPT.firinOnden).length, yakin=P.filter(q=>(OPT.firinEsnek||q.tip===p.tip)&&(q.stage==='presde'||q.stage==='rafta')).length; if(bos>yakin) return p; } return null; };
  /* --- ray kilidi --- */
  const catis=(ri,a,b)=>{ const L=ri===0?a:b, Rr=ri===0?b:a; return L.hi+PAY_UST>Rr.lo||L.c1+PAY_ALT>Rr.c0; };
  const birles=(a,b)=>({lo:Math.min(a.lo,b.lo),hi:Math.max(a.hi,b.hi),c0:Math.min(a.c0,b.c0),c1:Math.max(a.c1,b.c1)});
  /* görev → parçalar: bol() işaretlerinde ve 350 mm'den uzun her ray yolculuğunun başında/sonunda kesilir → yolculuk kısa bir parça olur, durakta yapılan iş yalnız o durağın çevresini ayırır */
  function parcala(B,oc0,ri){ const isaret={}; B.bolmeler.forEach(x=>{ isaret[x.i]=x.ad; }); const kes=new Set([0]); B.bolmeler.forEach(x=>kes.add(x.i)); B.st.forEach((s,i)=>{ if(s.x1!==undefined&&Math.abs(s.x1-s.x0)>350){ kes.add(i); kes.add(i+1); } });
    const sira=[...kes].filter(i=>i<B.st.length).sort((a,b)=>a-b).concat([B.st.length]), segs=[]; let son=oc0, ek='', acik=null;
    /* AÇIK ÇEKMECE de yer kaplar (z 0–700): açıkken diğer robotun arabası / kolu o kolonun önüne giremez → aralığa çekmecenin x'i eklenir */
    const cekEk=(oc,K)=>ri===1?{lo:Math.min(oc.lo,K.x0),hi:oc.hi,c0:Math.min(oc.c0,K.x0+200),c1:oc.c1}:{lo:oc.lo,hi:Math.max(oc.hi,K.x1),c0:oc.c0,c1:Math.max(oc.c1,K.x1-200)};
    for(let k=0;k<sira.length-1;k++){ const steps=B.st.slice(sira[k],sira[k+1]); if(!steps.length) continue; if(isaret[sira[k]]!==undefined) ek=isaret[sira[k]]; let oc=son, dur=0, cekVar=acik;
      steps.forEach(s=>{ dur+=s.sure; if(s.oc) oc=birles(oc,s.oc); if(s.ocSon) son=s.ocSon; if(s.cek){ if(s.cek.hedef>0.5){ acik=s.cek.k; cekVar=acik; } else { cekVar=cekVar||s.cek.k; acik=null; } } });
      if(cekVar&&ri!==undefined) oc=cekEk(oc,KOLON[cekVar]); if(acik&&ri!==undefined) son=cekEk(son,KOLON[acik]); segs.push(Object.assign({steps,dur,ek,son},oc)); } return segs; }
  /* robotu park pozuna alıp x'e çeken adımlar (kol toplanır: üst aralık = araba ± 110) */
  function parkKur(rb,hedef){ const c=kopya(rb.cur), PB=insaci(c,rb.yon); PB.park('yol ver · kolu topla'); if(Math.abs(hedef-c.carX)>1) PB.kay('yol ver → x '+hedef.toFixed(0),hedef); return PB; }
  function parkHedef(ri,engeller,x){ let h=x; for(const e of engeller){ h=ri===0?Math.min(h,e.lo-PAY_UST-110,e.c0-PAY_ALT):Math.max(h,e.hi+PAY_UST+110,e.c1+PAY_ALT); } return (h<RAY_X[0]-0.5||h>RAY_X[1]+0.5)?null:h; }
  function parkIsle(rb,engeller,tp){ const hedef=parkHedef(rb.i,engeller,rb.cur.carX); if(hedef===null) return false; const oc0=isgalDurum(rb.cur), PB=parkKur(rb,hedef), sg=parcala(PB,oc0,rb.i)[0]; if(!sg) return true;
    const pb=blok('robot','yol ver',tp,PB.st,null,rb.i); pb.yolver=1; rb.res.push({t0:tp,t1:pb.t1,lo:sg.lo,hi:sg.hi,c0:sg.c0,c1:sg.c1,ne:'yol veriyor'}); rb.cur=PB.cur; rb.bitis=pb.t1; rb.t=Math.max(rb.t,pb.t1); sayac.yolver++; sonBitis=Math.max(sonBitis,pb.t1); return true; }
  /* görevi en erken uygun zamana yerleştir; olmuyorsa null */
  function yerlestir(r,B,oc0){ let segs=parcala(B,oc0,r.i); const o=N>1?RBT[1-r.i]:null;
    if(!o){ let ts=t; return {segs:segs.map(sg=>{ const x={t0:ts,sg}; ts+=sg.dur; return x; }),son:ts,bekleme:0}; }
    for(const sg of segs) if(parkHedef(o.i,[sg],o.i===1?RAY_X[1]:RAY_X[0])===null) return null;                          // diğer robot rayın ucuna çekilse bile sığmıyor → bu robot bu işi yapamaz
    const dene=(tBas)=>{ let ts=tBas, dur=oc0; const out=[], neden=[]; let bek=0;
      for(let k=0;k<segs.length;k++){ const sg=segs[k]; let t0=ts, gd=0; let sonCak=null; while(gd++<500){ const cak=o.res.find(q=>q.t1>t0+1e-6&&q.t0<t0+sg.dur-1e-6&&catis(r.i,sg,q)); if(!cak) break; t0=cak.t1; sonCak=cak; }
        if(t0>ts+1e-6){ const engel=o.res.find(q=>q.t1>ts+1e-6&&q.t0<t0-1e-6&&catis(r.i,dur,q)); if(engel) return {ok:false,sonra:engel.t1}; bek+=t0-ts; neden.push([(sg.ek||'ilk parça')+' ← '+((sonCak&&sonCak.ne)||'?'),t0-ts]); }
        out.push({t0,sg}); ts=t0+sg.dur; dur=sg.son; }
      return {ok:true,out,son:ts,bek,dur,neden}; };
    const ara=()=>{ let tb=t; for(let i=0;i<80;i++){ const d=dene(tb); if(d.ok){ d.tBas=tb; return d; } tb=Math.max(tb+0.5,d.sonra); } return null; };
    let sonuc=ara(); if(!sonuc) return null;
    { const rest=isgalDurum(o.cur), eng=sonuc.out.filter(x=>x.t0+x.sg.dur>o.bitis+1e-6&&catis(r.i,x.sg,rest)).map(x=>x.sg);                 // diğeri son işinden sonra durduğu yerde engel → kenara çekilir
      if(eng.length){ if(!parkIsle(o,eng,Math.max(o.bitis,t))) return null; sonuc=ara(); if(!sonuc) return null; } }
    const ileride=o.res.filter(q=>q.t1>sonuc.son&&catis(r.i,sonuc.dur,q));                                        // iş bitince durduğu yer diğerinin ileride ayırdığı aralıkta mı → iş sonuna "yol ver" parçası eklenir
    if(ileride.length){ const c=kopya(B.cur), hedef=parkHedef(r.i,ileride,c.carX); if(hedef!==null){ const PB=insaci(c,r.yon); PB.park('yol ver · kolu topla'); if(Math.abs(hedef-c.carX)>1) PB.kay('yol ver → x '+hedef.toFixed(0),hedef); const ps=parcala(PB,sonuc.dur,r.i)[0]; if(ps){ ps.ek='yol ver'; ps.yolver=1; segs=segs.concat([ps]); B.cur=PB.cur;
          const s2=ara(); if(!s2) return null; sonuc=s2; } } }
    if(sonuc.tBas>t+1e-6) sonuc.neden.push(['görev başlayamadı (bekleme yeri de kapalı)',sonuc.tBas-t]);
    return {segs:sonuc.out,son:sonuc.son,bekleme:sonuc.bek+(sonuc.tBas-t),neden:sonuc.neden}; }
  function isle(r,B,plc,ad,ref){ let ilk=null, son=null, ts=t, dur=isgalDurum(r.cur); const bl=[];
    for(const {t0,sg} of plc.segs){ if(t0>ts+1e-6) r.res.push({t0:ts,t1:t0,lo:dur.lo,hi:dur.hi,c0:dur.c0,c1:dur.c1,ne:'ray bekliyor (x '+((dur.c0+dur.c1)/2).toFixed(0)+')'});
      const b=blok('robot',sg.yolver?'yol ver':ad+(sg.ek?' · '+sg.ek:''),t0,sg.steps,sg.yolver?null:ref,r.i); b.ek=sg.ek; if(sg.yolver){ b.yolver=1; sayac.yolver++; } else r.busy+=sg.dur;
      r.res.push({t0,t1:b.t1,lo:sg.lo,hi:sg.hi,c0:sg.c0,c1:sg.c1,ne:(sg.yolver?'yol ver':ad.replace(/#\d+ /,'').replace(/sipariş \d+ · /,'').slice(0,26)+(sg.ek?' · '+sg.ek:''))}); if(!ilk&&!sg.yolver) ilk=b; if(!sg.yolver){ son=b; bl.push(b); } ts=b.t1; dur=sg.son; }
    sayac.rayBekleme+=plc.bekleme; (plc.neden||[]).forEach(([k,v])=>{ const kk=(r.i?'SAĞ ':'SOL ')+ad.replace(/#\d+ /,'').replace(/sipariş \d+ · /,'').replace(/ → QR göz \d+.*/,'').replace(/ \d+$/,'').slice(0,34)+' · '+k; sayac.neden[kk]=(sayac.neden[kk]||0)+v; }); r.cur=B.cur; r.t=ts; r.bitis=ts; sonBitis=Math.max(sonBitis,ts); return {ilk,son,bl,t0:ilk.t0,t1:son.t1}; }
  function teslimKontrol(o,t1){ if(o.teslim) return; if(P.find(p=>p.o===o&&p.stage!=='bitti'&&p.stage!=='iptal')===undefined&&o.kolaTeslim&&o.tatliTeslim){ o.teslim=t1; const d=dolap.find(d=>d.o===o); if(d){ d.freeAt=t1+HIZ.musteri; plan.push({tip:'musteri',ad:'müşteri '+o.id,t0:d.freeAt,t1:d.freeAt+2,ri:0,ref:o,steps:[{ad:'MÜŞTERİ ALDI · sipariş '+o.id,sure:2,fn:()=>{},bitir:()=>{ o.nesneler.forEach(n=>nesneSil(n)); o.nesneler=[]; }}]}); } } }
  const istBos=()=>({carX:0,tcp:V(0,0,0),t:V(0,0,-1),u:V(0,1,0),yuk:'bos',parmak:70});
  /* kim yapabilir · kimin asıl işi */
  const yapabilir=(r,c)=>N===1||(r.i===0?(c.tip!=='FIN'&&(OPT.solFirina||c.tip!=='FIRINA')&&((c.tip!=='KOLA'&&c.tip!=='TATLI')||qrKapak[c.o.goz].ci===0)):(c.tip!=='START'&&c.tip!=='TOP'));
  const asil=(r,c)=>N===1||(r.i===0?(c.tip==='START'||c.tip==='TOP'):(c.tip!=='START'&&c.tip!=='TOP'));
  let guard=0;
  while(guard++<120000){
    const r=RBT.slice().sort((a,b)=>a.t-b.t||a.i-b.i)[0]; if(!isFinite(r.t)) break; t=r.t; const o=N>1?RBT[1-r.i]:null;
    tepsiler.forEach(tp=>{ if(tp.bosAt!==undefined&&tp.bosAt<=t){ tp.bos=true; tp.bosAt=undefined; } });
    /* ön kontrol: durduğum yer, diğerinin önceden ayırdığı bir aralığın içinde mi → önce kenara çekil */
    if(o&&r.bitis<=t){ const ben=isgalDurum(r.cur), gel=o.res.filter(q=>q.t1>t&&catis(r.i,ben,q)); if(gel.length&&parkIsle(r,o.res.filter(q=>q.t1>t),t)) continue; }
    const cands=[];
    if(zincir&&N===1){ cands.push({pri:-1,p:zincir.p,tip:'START',ready:zincir.p.o.arr,elde:zincir.tray}); zincir=null; } else {
      for(const p of P){ const oo=p.o;
        if(p.stage==='presde'&&p.readyAt<=t&&R_.topping<=t){ if(N>1){ const g=gozTip(p.tip).find(g=>!g.p), rafBos=R_.raf<=t; if(g||rafBos) cands.push({pri:4,p,g,rafBos,tip:'TOP',ready:p.readyAt}); } else { const g=gozTip(p.tip).find(g=>!g.p); if(g) cands.push({pri:4,p,g,tip:'TOP',ready:p.readyAt}); } }
        else if(p.stage==='rafta'&&p.readyAt<=t){ const g=gozTip(p.tip).find(g=>!g.p); if(g) cands.push({pri:2.5,p,g,tip:'FIRINA',ready:p.readyAt}); }
        else if(p.stage==='firinda'&&p.readyAt<=t&&R_.kesim<=t&&(!OPT.tut||R_.sprey<=t)) cands.push({pri:3,p,tip:'KES',ready:p.readyAt});
        else if(p.stage==='kesimde'&&p.readyAt<=t&&R_.sprey<=t) cands.push({pri:2,p,tip:'SPR',ready:p.readyAt});
        else if(p.stage==='spreyde'&&p.readyAt<=t&&R_.kutu<=t&&oo.kolaTeslim&&oo.tatliTeslim&&(oo.icBitis||0)<=t&&dolapAl(oo,t)) cands.push({pri:1,p,tip:'FIN',ready:p.readyAt}); }   // göz düzeni: önce sol şerit (kola, tatlı), sonra sağa kutu
      for(const oo of O){ if(oo.arr>t||oo.teslim) continue; const ilk=P.find(p=>p.o===oo); const yolda=ilk&&['presde','rafta','firinda','kesimde','spreyde','bitti'].indexOf(ilk.stage)>=0, acil=ilk&&['kesimde','spreyde'].indexOf(ilk.stage)>=0?0.5:5;
        if(yolda&&oo.kola&&!oo.kolaTeslim&&!oo.kolaYolda&&dolapAl(oo,t)) cands.push({pri:acil,o:oo,tip:'KOLA',ready:oo.arr}); if(yolda&&oo.tatli&&!oo.tatliTeslim&&!oo.tatliYolda&&(!oo.kola||(oo.kolaTeslim&&(oo.icBitis||0)<=t))&&dolapAl(oo,t)) cands.push({pri:acil,o:oo,tip:'TATLI',ready:oo.arr}); }
      const yeni=startAday(0); if(yeni&&tepsiler.some(x=>x.bos)) cands.push({pri:6,p:yeni,tip:'START',ready:yeni.o.arr}); }
    let benim=cands.filter(c=>yapabilir(r,c)); const kendi=benim.filter(c=>asil(r,c));
    if(kendi.length) benim=kendi; else if(o&&(o.bitis-t<8||(r.i===0&&P.some(p=>p.stage==='presde')))) benim=[];              // yardım: kendi işim yok VE asıl sahibi ≥ 8 s daha meşgul · SOL, preste ürün varken yardıma gitmez (topping işi birkaç saniyeye geliyor)
    benim.sort((a,b)=>a.pri-b.pri||a.ready-b.ready);
    let yapildi=false;
    for(const c of benim){ const cur=kopya(r.cur), B=insaci(cur,r.yon), oc0=isgalDurum(r.cur); let ad='', s=null;
      if(c.tip==='START'){ const p=c.p; s=stokBak(stok,p.tip); if(!s){ p.stage='iptal'; not.push('stok bitti: '+p.tip); continue; } p.tray=c.elde||tepsiler.find(x=>x.bos); p.kolon=s.kolon; p.sira=s.sira; p.topPos=s.pos; p.yan=s.yan; p.carPres=s.tek?s.yan:carPres();
        ad='#'+p.id+' '+p.tip+' · başlat (tepsi → pres altı → hamur tepsinin ortasına)'; G_baslat(B,p,!!c.elde); }
      else if(c.tip==='TOP'){ const p=c.p; c.raf=!!o&&(OPT.raf==='hep'?true:OPT.raf==='yok'?false:(!c.g||(c.rafBos&&o.res.some(q=>q.t1>t+30&&q.t0<t+70&&q.lo<3130)))); if(o&&(c.raf?!c.rafBos:!c.g)) continue;   /* karma: fırın kolonu o sırada SAĞ robotta ise aktarma gözüne bırak, boşsa doğrudan fırına */
        if(c.raf){ ad='#'+p.id+' '+p.tip+' · presten al → topping → aktarma gözü'; G_topping(B,p,null,true); } else { p.goz=c.g.g; ad='#'+p.id+' '+p.tip+' · presten al → topping → fırın '+(p.goz+1); G_topping(B,p,(o&&r.i===0)?NIS.cx-450:null); } }
      else if(c.tip==='FIRINA'){ const p=c.p; p.goz=c.g.g; ad='#'+p.id+' · raftan al → fırın '+(p.goz+1); G_firina(B,p);
        c.takas=R_.kesim<=t?P.filter(q=>q.stage==='firinda'&&q.goz!==p.goz&&q.readyAt<=t+(OPT.takasPay||15)).sort((a,b)=>a.readyAt-b.readyAt)[0]:null;                     // değiş-tokuş: fırının önündeyken yandaki gözdeki pişmişi de al
        if(c.takas){ ad+=' + #'+c.takas.id+' pişmişi al → kesim'; B.bol('pişmişi al → kesim'); G_kesim(B,c.takas); } }
      else if(c.tip==='KES'&&OPT.tut){ const p=c.p, oo=p.o; c.fin=(N===1||r.i===1)&&R_.kutu<=t&&oo.kolaTeslim&&oo.tatliTeslim&&(oo.icBitis||0)<=t&&!!dolapAl(oo,t); c.zn=(c.fin&&N===1&&OPT.zincir)?startAday(1):null;
        ad='#'+p.id+' · fırından al → kesim → sprey (tepsi elde)'+(c.fin?' → kutu → QR göz '+(oo.goz+1)+(c.zn?' → tepsi elde kalır (sıradaki #'+c.zn.id+')':' → tepsi nişe'):' → spreyde bırak'); G_kesimTut(B,p,oo,c.fin,!!c.zn); }
      else if(c.tip==='KES'){ ad='#'+c.p.id+' · fırından al → kesim'; G_kesim(B,c.p); }
      else if(c.tip==='SPR'){ ad='#'+c.p.id+' · kesimden al → sprey'; G_sprey(B,c.p); }
      else if(c.tip==='FIN'){ const p=c.p, oo=p.o; c.zn=(N===1&&OPT.zincir)?startAday(1):null; ad='#'+p.id+' · spreyden al → kutu → QR göz '+(oo.goz+1)+(c.zn?' → tepsi elde kalır (sıradaki #'+c.zn.id+')':' → tepsi nişe'); G_bitir(B,p,oo,!!c.zn); }
      else { const oo=c.o, tip=c.tip==='KOLA'?'kola':'tatli'; s=stokBak(stok,tip,(N>1&&r.i===1)?(cx=>cx>KOLON.KI.x1):null); if(!s){ if(tip==='kola') oo.kolaTeslim=true; else oo.tatliTeslim=true; not.push('stok bitti: '+tip); continue; }
        oo[tip+'Stok']=s; ad='sipariş '+oo.id+' · '+(tip==='kola'?'içecek':'tatlı')+' → QR göz '+(oo.goz+1); G_icecek(B,oo,tip); }
      /* 2 robot: iş ortak bölgede bitiyorsa robot işin SONUNDA kendi tarafına çekilir (diğeri gelip "yol ver" diye bekletmesin) — SOL: fırından nişin önüne · SAĞ: nişten / QR'dan kolunu toplayıp x 3300'e */
      if(o){ if(r.i===1&&(c.tip==='FIN'||(c.tip==='KES'&&c.fin)||c.tip==='KOLA'||c.tip==='TATLI')&&cur.carX<OPT.evSag-60){ B.bol('çekil'); B.park('kolu topla'); B.kay('kendi tarafına çekil · SOL robota yol aç',OPT.evSag); } }
      const plc=yerlestir(r,B,oc0); if(!plc) continue;
      const b=isle(r,B,plc,ad,c.p||c.o); if(!asil(r,c)) sayac.yardim++; r.is[c.tip]=(r.is[c.tip]||0)+1; if(s) s.q.k++;
      if(c.tip==='START'){ const p=c.p; p.tray.bos=false; sayac.start++; if(s.tek) sayac.tek++; if(c.elde) sayac.zincir++; const C=insaci(istBos()); G_presCevrim(C,p); blok('istasyon','PRES #'+p.id,b.t1,C.st,p); p.stage='presde'; p.readyAt=b.t1+HIZ.pres; R_.press=1e12; }
      else if(c.tip==='TOP'&&c.raf){ const p=c.p; const tb=b.bl.filter(x=>x.ek==='topping'); R_.press=tb.length?tb[0].t0:b.t0+20; R_.topping=tb.length?tb[tb.length-1].t1:b.t1; R_.raf=1e12; p.stage='rafta'; p.readyAt=b.t1; }
      else if(c.tip==='FIRINA'){ const p=c.p; c.g.p=p; const al=b.bl.filter(x=>x.ek==='fırına götür'), fb=al[al.length-1]||b.son; R_.raf=al.length?al[0].t0:b.t0+10; p.stage='firinda'; p.readyAt=fb.t1+(OPT.firinEsnek?HIZ.firin[p.tip]:c.g.sure); c.g.doneAt=p.readyAt; fb.firin=[fb.t1,p.readyAt,p.goz]; sayac.firina=(sayac.firina||0)+1;
        if(c.takas){ const q=c.takas; G.find(g=>g.g===q.goz).p=null; const C=insaci(istBos()); G_kesimCevrim(C); blok('istasyon','KESİM #'+q.id,b.t1,C.st,q); R_.kesim=1e12; q.stage='kesimde'; q.readyAt=b.t1+HIZ.kesim; sayac.takas=(sayac.takas||0)+1; } }
      else if(c.tip==='TOP'){ const p=c.p; c.g.p=p; const tb=b.bl.filter(x=>x.ek==='topping'); R_.press=tb.length?tb[0].t0:b.t0+20; R_.topping=tb.length?tb[tb.length-1].t1:b.t1; const fb=b.bl.filter(x=>x.ek==='fırına götür').pop()||b.son; p.stage='firinda'; p.readyAt=fb.t1+(OPT.firinEsnek?HIZ.firin[p.tip]:c.g.sure); c.g.doneAt=p.readyAt; fb.firin=[fb.t1,p.readyAt,p.goz]; }
      else if(c.tip==='KES'&&OPT.tut){ const p=c.p, oo=p.o; G.find(g=>g.g===p.goz).p=null; const ks=b.bl.filter(x=>x.ek==='kesim · tepsi elde'), ss=b.bl.filter(x=>x.ek==='sprey · tepsi elde'); R_.kesim=ks.length?ks[ks.length-1].t1:b.t1;
        if(c.fin){ const kutuSon=b.bl.filter(x=>x.ek==='kutu + QR').pop()||b.son; kutuSon.bitis=1; R_.sprey=ss.length?ss[ss.length-1].t1:b.t1; R_.kutu=kutuSon.t1; p.stage='bitti'; p.bitti=kutuSon.t1; if(c.zn) zincir={p:c.zn,tray:p.tray}; else p.tray.bosAt=b.t1; oo.kutuSay++; teslimKontrol(oo,kutuSon.t1); sayac.tutFin=(sayac.tutFin||0)+1; }
        else { R_.sprey=1e12; p.stage='spreyde'; p.readyAt=b.t1; sayac.tutBirak=(sayac.tutBirak||0)+1; } }
      else if(c.tip==='KES'){ const p=c.p; G.find(g=>g.g===p.goz).p=null; const C=insaci(istBos()); G_kesimCevrim(C); blok('istasyon','KESİM #'+p.id,b.t1,C.st,p); R_.kesim=1e12; p.stage='kesimde'; p.readyAt=b.t1+HIZ.kesim; }
      else if(c.tip==='SPR'){ const p=c.p; R_.kesim=b.t0+15; const C=insaci(istBos()); G_spreyCevrim(C); blok('istasyon','SPREY #'+p.id,b.t1,C.st,p); R_.sprey=1e12; p.stage='spreyde'; p.readyAt=b.t1+HIZ.sprey; }
      else if(c.tip==='FIN'){ const p=c.p, oo=p.o; const kutuSon=b.bl.filter(x=>x.ek==='kutu + QR').pop()||b.son; kutuSon.bitis=1; R_.sprey=b.t0+15; R_.kutu=kutuSon.t1; p.stage='bitti'; p.bitti=kutuSon.t1; if(c.zn) zincir={p:c.zn,tray:p.tray}; else p.tray.bosAt=b.t1; oo.kutuSay++; teslimKontrol(oo,kutuSon.t1); }
      else { const oo=c.o; if(c.tip==='KOLA'){ oo.kolaYolda=true; oo.kolaTeslim=true; } else { oo.tatliYolda=true; oo.tatliTeslim=true; } const qb=b.bl.filter(x=>x.ek==="QR'a götür").pop()||b.son; oo.icBitis=Math.max(oo.icBitis||0,qb.t1); teslimKontrol(oo,qb.t1); }
      if(o&&o.t>o.bitis) o.t=Math.max(t,o.bitis);                                                    // diğer robot olay bekliyorsa uyandır: bu iş ona yeni iş çıkarmış olabilir (saati ileride / sonsuzda kalmasın)
      yapildi=true; break; }
    if(!yapildi&&o){ const ev_=r.i===0?OPT.evSol:OPT.evSag; if(r.i===0?r.cur.carX>OPT.evSol+400:r.cur.carX<OPT.evSag-300){ /* yalnız ortak bölgede (diğerinin işine engel olacağı yerde) kaldıysa */ const cur=kopya(r.cur), B=insaci(cur,r.yon), oc0=isgalDurum(r.cur); B.park('eve dön · kolu topla'); B.kay('eve dön → x '+ev_,ev_); const plc=yerlestir(r,B,oc0);
        if(plc&&plc.bekleme<0.5){ let ts=t; plc.segs.forEach(({t0,sg})=>{ const b=blok('robot','eve dön',t0,sg.steps,null,r.i); b.yolver=1; r.res.push({t0,t1:b.t1,lo:sg.lo,hi:sg.hi,c0:sg.c0,c1:sg.c1,ne:'eve dönüyor'}); ts=b.t1; }); r.cur=B.cur; r.t=ts; r.bitis=ts; sayac.eve=(sayac.eve||0)+1; sonBitis=Math.max(sonBitis,ts); continue; } } }
    if(!yapildi){ const ev=[]; P.forEach(p=>{ if(p.readyAt>t&&p.stage!=='bekliyor'&&p.stage!=='bitti') ev.push(p.readyAt); if(p.stage==='bekliyor'&&p.o.arr>t) ev.push(p.o.arr); }); ev.push(R_.press,R_.topping,R_.kesim,R_.sprey,R_.kutu); dolap.forEach(d=>{ if(d.freeAt>t) ev.push(d.freeAt); }); tepsiler.forEach(tp=>{ if(tp.bosAt!==undefined&&tp.bosAt>t) ev.push(tp.bosAt); }); O.forEach(q=>{ if((q.icBitis||0)>t) ev.push(q.icBitis); });
      if(o){ if(isFinite(o.t)&&o.t>t) ev.push(o.t); if(o.bitis>t) ev.push(o.bitis); const q=o.res.filter(q=>q.t1>t).map(q=>q.t1); if(q.length) ev.push(Math.min(...q)); if(benim.length) ev.push(t+2); }
      const nx=ev.filter(x=>x>t+1e-6&&x<1e11); r.t=nx.length?Math.min(...nx):Infinity; }
  }
  tepsiler.forEach(tp=>{ tp.bosAt=undefined; });
  plan.sort((a,b)=>a.t0-b.t0);
  const teslim=O.filter(o=>o.teslim), bek=teslim.map(o=>o.teslim-o.arr).sort((a,b)=>a-b), ort=bek.length?bek.reduce((a,b)=>a+b,0)/bek.length:0, biten=P.filter(p=>p.stage==='bitti').length;
  const kpi={N, siparis:O.length, teslim:teslim.length, urun:P.length, ort, max:bek.length?bek[bek.length-1]:0, gec:bek.filter(b=>b>1500).length, sure:sonBitis, robotlar:RBT.map(q=>sonBitis?q.busy/sonBitis:0), robot:sonBitis?Math.max(...RBT.map(q=>q.busy))/sonBitis:0, isler:RBT.map(q=>q.is), not, gozSay,
    erisilemeyen:stok.erisilemeyen||0, sayac, urunSure:biten?plan.filter(b=>b.tip==='robot'&&b.ref&&b.ref.tip).reduce((a,b)=>a+(b.t1-b.t0),0)/biten:0, O, P};
  return {plan,kpi,tepsiler,O,P,G,N};
}

/* ================= OYNATICI (zaman tabanlı · bloklar paralel · ileri/geri sarılabilir) ================= */
let anim=null, OYN=null;
function hazirla(planSonuc){ ROB.forEach((rb,i)=>{ const x=robotX0(planSonuc?planSonuc.N:1,i); rb.carX=x; rb.t.set(0,0,-1); rb.u.set(0,1,0); rb.yuk='bos'; rb.tasi=null; rb.parmak=70; rb.tcp.copy(parkTcp(x)); }); S.ri=0; S.n=planSonuc?planSonuc.N:S.n;
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
  const hh=[0,0,0,0], ht=[{pide:0,lahm:0},{pide:0,lahm:0}]; let icS=0; ps.plan.filter(b=>b.bitis).forEach(b=>{ const i=Math.min(3,Math.floor(b.t1/3600)); hh[i]++; if(i<2&&b.ref&&ht[i][b.ref.tip]!==undefined) ht[i][b.ref.tip]++; }); ps.plan.forEach(b=>{ if(b.tip==='robot'&&b.t1<=3600&&(b.ek==="QR'a götür")) icS++; });
  /* robot ne yaptı */
  const mak={}; ps.plan.filter(b=>b.tip==='robot'&&!b.yolver).forEach(b=>{ const key=b.ad.indexOf('raftan')>=0?'raftan al → fırın (+ değiş-tokuş)':b.ad.indexOf('başlat')>=0?'tepsi + hamur → pres':b.ad.indexOf('topping')>=0?'topping → fırın':b.ad.indexOf('fırından')>=0?'fırın → kesim':b.ad.indexOf('kesimden')>=0?'kesim → sprey':b.ad.indexOf('kutu')>=0?'kutu → QR → tepsi':b.ad.indexOf('içecek')>=0?'içecek → QR':'tatlı → QR'; const gk=key+'#'+(b.ref?(b.ref.id||0):0)+(b.ref&&b.ref.tip?'p':'o'); mak[key]=mak[key]||{}; mak[key][gk]=(mak[key][gk]||0)+(b.t1-b.t0); });
  /* hat dengesi: istasyonun çalıştığı süre / toplam süre */
  const dol={pres:0,topping:0,'fırın 1':0,'fırın 2':0,'fırın 3':0,kesim:0,sprey:0,kutu:0};
  ps.plan.forEach(b=>{ if(b.tip==='istasyon'){ const d=b.t1-b.t0; if(b.ad.indexOf('PRES')===0) dol.pres+=d; else if(b.ad.indexOf('KESİM')===0) dol.kesim+=d; else dol.sprey+=d; }
    if(b.firin) dol['fırın '+(b.firin[2]+1)]+=b.firin[1]-b.firin[0]; if(b.tip==='robot') b.steps.forEach(st=>{ if(st.ad.indexOf('DOZAJI')>=0) dol.topping+=st.sure; if(st.ad.indexOf('KUTU KAPAĞI')>=0||st.ad.indexOf('İTİCİ')>=0) dol.kutu+=st.sure; }); });
  const bar=(ad,v,renk)=>`<tr><td>${ad}</td><td style="width:58%"><div style="background:#1f242e;border-radius:4px;height:9px;margin-top:4px"><div style="width:${Math.min(100,v*100).toFixed(0)}%;height:9px;border-radius:4px;background:${renk||(v>.85?'#ff5c5c':v>.6?'#ffb340':'#3ddc84')}"></div></div></td><td style="width:44px">${(v*100).toFixed(0)} %</td></tr>`;
  const cok=k.siparis>3;
  let h='<table>'+[['Sipariş · ürün',`${k.siparis} · ${k.urun}`],['Teslim edilen',`${k.teslim} sipariş`],
    cok?['Çıkan ürün · 1. / 2. / 3. saat / sonrası',`<b>${hh[0]} / ${hh[1]} / ${hh[2]}</b> / ${hh[3]}`]:null,
    cok?['1. saat · pide + lahmacun',`${ht[0].pide} + ${ht[0].lahm}`+(icS?` · ayrıca ${icS} içecek / tatlı taşındı`:'')]:null, cok?['2. saat · pide + lahmacun',`${ht[1].pide} + ${ht[1].lahm}`]:null,
    ['Ortalama bekleme',`<b>${fmt(k.ort)}</b>`],['En uzun bekleme',fmt(k.max)], cok?['25 dk üstü bekleyen',`<span class="${k.gec?'yok':'ok'}">${k.gec} sipariş</span>`]:null,
    ['Son teslim',saat(k.sure)]].filter(Boolean).map(r=>`<tr><td>${r[0]}</td><td>${r[1]}</td></tr>`).join('')+'</table>';
  h+='<h2>Hat dengesi</h2><table>'+k.robotlar.map((v,i)=>bar(k.N>1?(i?'ROBOT SAĞ':'ROBOT SOL'):'ROBOT',v,v>.85?'#ff5c5c':(i?'#ff8c40':'#2997ff'))).join('')+Object.entries(dol).map(([a,v])=>bar(a,v/T)).join('')+'</table>';
  h+='<h2>Robot ne yaptı · ortalama süre</h2><table>'+Object.entries(mak).map(([a,g])=>{ const v=Object.values(g); return `<tr><td>${a}</td><td>${fmt(v.reduce((x,y)=>x+y,0)/v.length)} × ${v.length}</td></tr>`; }).join('')+`<tr><td><b>ürün başına robot</b></td><td><b>${fmt(k.urunSure)}</b> ${k.N>1?'(iki robotun toplamı)':'→ en fazla '+(3600/Math.max(1,k.urunSure)).toFixed(0)+' ürün/saat'}</td></tr>${k.N>1?`<tr><td>ray kilidi</td><td>${k.sayac.yolver} kez yol verme · ${fmt(k.sayac.rayBekleme)} bekleme</td></tr><tr><td>fırında değiş-tokuş</td><td>${k.sayac.takas||0} / ${k.sayac.firina||0} fırına koyuşta pişmiş de alındı</td></tr>${OPT.tut?`<tr><td>tepsi elde (kesim + sprey)</td><td>${k.sayac.tutFin||0} ürün kutuya kadar elde · ${k.sayac.tutBirak||0} ürün spreyde bırakıldı</td></tr>`:''}<tr><td>iş bölümü</td><td>${k.isler.map((m,i)=>(i?'SAĞ: ':'SOL: ')+Object.entries(m).map(([a,b])=>({START:'başlat',TOP:'topping',FIRINA:'fırına koy',KES:'kesim',SPR:'sprey',FIN:'kutu+QR',KOLA:'içecek',TATLI:'tatlı'}[a])+' '+b).join(' · ')).join('<br>')}</td></tr>`:''}</table>`;
  const nt=[...new Set(k.not)]; if(k.erisilemeyen) nt.push(k.erisilemeyen+' stok konumu atlandı (kol yetişmiyor)'); if(nt.length) h+=`<div class="amb" style="margin-top:6px">${nt.join(' · ')}</div>`;
  e.innerHTML=h;
  $('siparisler').innerHTML=ps.O.slice(0,120).map(o=>`<div>#${o.id} ${saat(o.arr)} · ${o.items.join('+')}${o.kola?' +içecek':''}${o.tatli?' +tatlı':''} → ${o.teslim?'<span class="'+((o.teslim-o.arr)>1500?'yok':'ok')+'">'+fmt(o.teslim-o.arr)+'</span>':'<span class="yok">teslim yok</span>'}</div>`).join('');
}
/* ================= ZAMAN ÇİZELGESİ + OYNATMA ÇUBUĞU ================= */
let GX=null, GH=0, GHmax=0;                                   // GH: zaman çizelgesinin açık yüksekliği (0 = kapalı, yalnız oynatma çubuğu görünür)
function altKur(){ $('gwrap').style.height=GH+'px'; $('scrubwrap').style.bottom=GH+'px'; $('tut').style.bottom=(GH+30)+'px'; }
try{ const v=localStorage.getItem('ak_gantt_h'); if(v!==null) GH=Math.max(0,+v||0); }catch(e){}
(function(){ const t=$('tut'); let y0=0, h0=0;
  t.addEventListener('pointerdown',e=>{ y0=e.clientY; h0=GH; t.setPointerCapture(e.pointerId); t._sur=true; e.preventDefault(); });
  t.addEventListener('pointermove',e=>{ if(!t._sur) return; GH=Math.max(0,Math.min(GHmax,h0+(y0-e.clientY))); altKur(); });
  const birak=()=>{ if(!t._sur) return; t._sur=false; try{ localStorage.setItem('ak_gantt_h',GH); }catch(e2){} };
  t.addEventListener('pointerup',birak); t.addEventListener('pointercancel',birak);
  t.addEventListener('dblclick',()=>{ GH=GH>20?0:GHmax; altKur(); try{ localStorage.setItem('ak_gantt_h',GH); }catch(e){} }); })();
altKur();
function gantt(ps){ const c=$('gantt'), W=Math.max(1200,Math.ceil(ps.kpi.sure/3600*1400)+80), N=ps.N, rows=(N>1?['robot SOL','robot SAĞ']:['robot']).concat(['pres','topping','fırın 1','fırın 2','fırın 3','kesim','sprey','kutu','QR dolabı']), H=30+rows.length*19; c.width=W; c.height=H; const g=c.getContext('2d'); g.fillStyle='#0d1016'; g.fillRect(0,0,W,H);
  const T1=Math.max(600,ps.kpi.sure), x=t=>70+t/T1*(W-90), ry=i=>6+i*19, o=N>1?1:0; GX={x,T1,W};
  g.font='11px sans-serif'; g.fillStyle='#8a94a4'; rows.forEach((r,i)=>g.fillText(r,4,ry(i)+12));
  for(let h=0;h<=T1/3600;h++){ const xx=x(h*3600); g.strokeStyle='#2a2f3a'; g.beginPath(); g.moveTo(xx,2); g.lineTo(xx,H-14); g.stroke(); g.fillText(saat(h*3600),xx+3,H-3); }
  const renk={START:'#3ddc84',TOP:'#ffb340',FIRINA:'#e0533a',KES:'#ff8c40',SPR:'#c084fc',FIN:'#2997ff',KOLA:'#ff5c5c',TATLI:'#f5e6c8',YOL:'#596273'};
  ps.plan.forEach(b=>{ if(b.tip==='robot'){ const key=b.yolver?'YOL':b.ad.indexOf('raftan')>=0?'FIRINA':b.ad.indexOf('başlat')>=0?'START':b.ad.indexOf('topping')>=0?'TOP':b.ad.indexOf('fırından')>=0?'KES':b.ad.indexOf('kesimden')>=0?'SPR':b.ad.indexOf('kutu')>=0?'FIN':b.ad.indexOf('içecek')>=0?'KOLA':'TATLI'; g.fillStyle=renk[key]; g.fillRect(x(b.t0),ry(b.ri||0),Math.max(1,x(b.t1)-x(b.t0)),15);
      if(b.firin){ g.fillStyle='#d08060'; g.fillRect(x(b.firin[0]),ry(3+o+b.firin[2]),Math.max(1,x(b.firin[1])-x(b.firin[0])),15); }
      b.steps.forEach(()=>{}); if(key==='TOP'&&!b.firin){ g.fillStyle='#ffb340'; g.fillRect(x(b.t0+15),ry(2+o),Math.max(1,x(b.t1)-x(b.t0+15)),15); } if(b.bitis){ g.fillStyle='#2997ff'; g.fillRect(x(b.t0+8),ry(8+o),Math.max(1,x(b.t0+30)-x(b.t0+8)),15); } }
    else if(b.tip==='istasyon'){ const i=b.ad.indexOf('PRES')===0?1:b.ad.indexOf('KESİM')===0?6:7; g.fillStyle='#4a5568'; g.fillRect(x(b.t0),ry(i+o),Math.max(1,x(b.t1)-x(b.t0)),15); } });
  ps.O.forEach(q=>{ if(!q.teslim) return; g.fillStyle='rgba(41,151,255,.35)'; g.fillRect(x(q.arr),ry(9+o),Math.max(1,x(q.teslim+HIZ.musteri)-x(q.arr)),15); g.fillStyle='#fff'; g.fillRect(x(q.arr),ry(9+o),1,15); });
  GHmax=H+8; if(GH>GHmax) GH=GHmax; altKur(); const sc=$('scrub'); sc.max=Math.ceil(ps.kpi.sure); sc.value=0; kafaKoy(0); }
function kafaKoy(T){ const k=$('kafa'); if(!k||!GX||GH<20) return; k.style.left=GX.x(T)+'px'; const w=$('gwrap'); if(anim){ const xx=GX.x(T); if(xx<w.scrollLeft+60||xx>w.scrollLeft+w.clientWidth-80) w.scrollLeft=Math.max(0,xx-w.clientWidth/3); } }

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
