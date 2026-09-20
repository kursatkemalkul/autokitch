/* ================= SİPARİŞLER (sim3d ile aynı talep modeli: Yemeksepeti 2023 akşam eğrisi) ================= */
const SEN={ fullpide:{ad:'TAM YÜK · yalnız pide'}, fulllahm:{ad:'TAM YÜK · yalnız lahmacun'}, full:{ad:'TAM YÜK · içeceksiz'}, fullic:{ad:'TAM YÜK · içecek + tatlı'}, akis:{ad:'Sürekli akış · 1 saat'}, tek:{ad:'Tek sipariş'}, uc:{ad:'3 müşteri (0 · 60 · 120 s)'}, aksam:{ad:'AKŞAM PİKİ · hafta içi · 17–20 h · 53 sipariş',n:53,egri:[.28,.42,.30]}, cmt:{ad:'CUMARTESİ AKŞAMI · 74 sipariş',n:74,egri:[.28,.42,.30]} };
function rng(seed){ let s=(seed>>>0)||1; return ()=>{ s=(s*1664525+1013904223)>>>0; return s/4294967296; }; }
function mkItems(rnd){ if(rnd()<0.65){ const it=['lahm','lahm']; if(rnd()<0.15) it.push('lahm'); return it; } const r=rnd(), n=r<0.65?1:r<0.90?2:3; return Array(n).fill('pide'); }
function siparisler(cfg){ const o=[], rnd=rng(cfg.seed*7919+13);
  if(cfg.sen==='tek') o.push({arr:0, items:[cfg.urun], kola:cfg.kola, tatli:cfg.tatli});
  else if(cfg.sen==='akis'){ const ar=Math.max(20,cfg.aralik||120); for(let tt=0;tt<3600;tt+=ar) o.push({arr:tt, items:mkItems(rnd), kola:rnd()<0.5, tatli:rnd()<0.25}); }
  else if(cfg.sen==='fullpide'||cfg.sen==='fulllahm'){ for(let k=0;k<150;k++) o.push({arr:0, items:[cfg.sen==='fullpide'?'pide':'lahm'], kola:false, tatli:false}); }
  else if(cfg.sen==='full'||cfg.sen==='fullic'){ for(let k=0;k<75;k++) o.push({arr:0, items:mkItems(rnd), kola:cfg.sen==='fullic'&&rnd()<0.5, tatli:cfg.sen==='fullic'&&rnd()<0.25}); }   // tam yük: kuyruk hep dolu (75 sipariş t=0'da) · karışım ve içecek %50 / tatlı %25 akşam modeliyle aynı
  else if(cfg.sen==='uc') o.push({arr:0,items:['pide'],kola:true,tatli:false},{arr:60,items:['lahm','lahm'],kola:true,tatli:true},{arr:120,items:['pide'],kola:false,tatli:false});
  else { const Sn=SEN[cfg.sen]; Sn.egri.forEach((pay,i)=>{ const n=Math.round(Sn.n*pay); for(let k=0;k<n;k++) o.push({arr:i*3600+rnd()*3600, items:mkItems(rnd), kola:rnd()<0.5, tatli:rnd()<0.25}); }); }
  o.sort((a,b)=>a.arr-b.arr); o.forEach((x,i)=>{ x.id=i+1; x.nesneler=[]; x.goz=-1; x.kutuSay=0; x.kolaTeslim=!x.kola; x.tatliTeslim=!x.tatli; x.teslim=null; }); return o; }

/* ================= STOK KONUMLARI (MODÜL B = HAT v19) ================= */
const OPT={tek:true, wip:8, kutuSure:46, takt:0, ic2:false};   /* ic2: içecek + tatlıyı İKİNCİ ROBOT taşır (ana robot yalnız hamur + kutu) → iki robotlu hattın üst sınırı */   /* wip: makinede aynı anda en çok ürün (hamurdan teslimata · CONWIP) · kutuSure: robot kutulama ağzına vardıktan sonra boş tepsi + açık kutunun yeniden hazır olmasına kadar geçen süre (ileri bakış için) */
function topPos(kolon,sira,k){ const K=KOLON[kolon], kot=K.kotlar[sira], y=kot+15+EL.TOP_R;
  if(kolon==='K1'||(kolon==='K2'&&sira<2)) return V(K.x0+115+130*(k%4), y, 70+135*Math.floor(k/4));
  return V(K.x0+100+105*(k%5), y, 68+91*Math.floor(k/5)); }
function stokKur(){ const s={pide:[],lahm:[]}; for(let i=5;i>=0;i--) s.pide.push({kolon:'K1',sira:i,n:20,k:0}); for(let i=1;i>=0;i--) s.pide.push({kolon:'K2',sira:i,n:20,k:0});
  for(let i=2;i<8;i++) s.lahm.push({kolon:'K2',sira:i,n:35,k:0}); for(let i=0;i<6;i++) s.lahm.push({kolon:'K3',sira:i,n:35,k:0});
  s.kola=[{kat:1,n:24,k:0},{kat:0,n:24,k:0}]; s.tatli=[{kat:1,n:10,k:0},{kat:0,n:10,k:0}]; return s; }
function stokBak(st,tip){ for(;;){ const q=st[tip].find(d=>d.k<d.n); if(!q) return null; const k=q.k;
    if(tip==='kola'||tip==='tatli'){ const pos=icecekPos(tip,q.kat,k); if(tip==='tatli') return {q,kat:q.kat,pos}; const yan=cekmeceYani(KOLON.KI,pos,YUK.kola.L,null); if(yan===null){ q.k++; st.erisilemeyen=(st.erisilemeyen||0)+1; continue; } return {q,kat:q.kat,pos,yan}; }
    const pos=topPos(q.kolon,q.sira,k), yan=cekmeceYani(KOLON[q.kolon],pos,YUK.top.L,OPT.tek?presErisir:null); if(yan===null){ q.k++; st.erisilemeyen=(st.erisilemeyen||0)+1; continue; } return {q,kolon:q.kolon,sira:q.sira,pos,yan,tek:OPT.tek&&presErisir(yan)}; } }

/* ================= ÇİZELGELEYİCİ · TEK ROBOT + MAKİNE =================
   ROBOT işleri (öncelik sırasıyla): 1) kutulama ağzında bekleyen KAPALI KUTU → QR gözü → tepsi ağza geri · 2) içecek / tatlı (siparişin ürünü yoldaysa) · 3) sıradaki ürünün HAMURU → pres / tabla.
   MAKİNE (robotsuz, olay tabanlı): pres → (bant: geçiş + adımlı bant, başlık altından geçerken dozaj | tabla: örs · pres · hazne altı · dozaj · fırın ağzı · itici · dönüş) → konveyör fırın (tek hız,
   girişler arası ≥ adım / bant hızı) → kesme plakası (yıldız bıçak + sprey) → itici ürünü tepsideki açık kutuya iter → kapak kapanır. Tepsi robottayken ya da kutu katlanırken ürün plakada bekler;
   plaka doluyken fırından ürün gelirse SIKIŞMA notu düşer. */
function planla(cfg){
  S.n=1; const O=siparisler(cfg), stok=stokKur(), plan=[], not=[];
  if(OPT.ic2) O.forEach(o=>{ o.kolaTeslim=true; o.tatliTeslim=true; });   // ikinci robot içeceği/tatlıyı ürün gelmeden gözüne koyar (engel olmaz)
  const P=[]; O.forEach(o=>o.items.forEach(tip=>P.push({id:P.length+1,o,tip,stage:'bekliyor',faz:{}})));
  const tepsi={tip:'tepsi',raf:0,pos:V(KUT.cx,KUT.trayY,KUT.cz),icerik:''};
  const dolap=qrKapak.map((q,i)=>({i,ri:q.ri,ci:q.ci,o:null,freeAt:0})).sort((a,b)=>a.ri-b.ri||a.ci-b.ci);
  const dolapAl=(o,t)=>{ if(o.goz>=0) return true; const d=dolap.find(d=>!d.o||d.freeAt<=t); if(!d) return false; d.o=o; d.freeAt=Infinity; o.goz=d.i; return true; };
  const N=cfg.robot===2?2:1; S.n=N;
  const blok=(tip,ad,t0,steps,ref,ri)=>{ const s=steps.reduce((a,x)=>a+x.sure,0); const b={tip,ad,t0,t1:t0+s,steps,ref,ri:ri||0}; plan.push(b); return b; };
  /* 2 ROBOT (Kemal 20 Eyl 2026): SOL robot yalnız hamur (pres/tabla ucu) · SAĞ robot kutu + QR + içecek/tatlı.
     İkisi aynı rayda: bir robotun görev boyunca süpürdüğü x aralığı diğerininkiyle çakışırsa sonra gelen bekler. */
  const mkRB=(i,x)=>({i,t:0,busy:0,is:{},res:[],cur:{carX:x,tcp:parkTcp(x),t:V(0,0,-1),u:V(0,1,0),yuk:'bos',parmak:70}});
  const RBT=[mkRB(0,1100),mkRB(1,4400)], RB=RBT[0];
  const PAY=450;
  const xAralik=(B,bas)=>{ let lo=bas,hi=bas; B.st.forEach(st0=>{ if(st0.x1!==undefined){ lo=Math.min(lo,st0.x0,st0.x1); hi=Math.max(hi,st0.x0,st0.x1); } }); return [lo-PAY,hi+PAY]; };
  const cakAralik=(B,bas)=>{ const [lo,hi]=xAralik(B,bas); return {lo,hi}; };
  /* görev BAŞLAMADAN önce: diğer robotun aynı anda süpürdüğü aralıkla çakışıyor mu? çakışıyorsa beklenecek an */
  const cakBekle=(r,B,bas,t0)=>{ if(N<2) return 0; const [lo,hi]=xAralik(B,bas), t1=t0+gecen(B), o=RBT[1-r.i]; let en=0;
    o.res.forEach(q=>{ if(q.t1>t0+1e-6&&q.t0<t1-1e-6&&q.hi>lo&&q.lo<hi) en=Math.max(en,q.t1); }); return en; };
  const vF=FIRIN.hazne/HIZ.pisme, firinSure=(FIRIN.x[1]-FIRIN.x[0])/vF, girisAralik=Math.max(FIRIN.adim/vF,OPT.takt||0);   /* fırına girişler arası: en az ürün adımı (350 mm) · TAKT verilirse robotun ürün başına işine göre seyreltilir → kutular robotun yetişebileceği aralıkla çıkar */
  const MK={presBos:0, bantSon:-1e9, durus:[], firinBos:0, plakaBos:0, katlaBitis:0, kutuKonT:0, kutuHazir:HIZ.kutuKoy, kuyruk:[], tur:[]};
  MK.katlaBitis=HIZ.katla;                                                                                  // t=0: bir katlanmış kutu tepside hazır, ikincisi katlanıyor
  let t=0, sonBitis=0; const sayac={sikisma:0,presBek:0,kutuBek:0};
  /* bant: t0 anından sonra bandın mm kadar ilerlediği an (duruşlar atlanır) · iki an arasında bandın aldığı yol */
  const bantZaman=(t0,mm)=>{ let kalan=mm/HIZ.bantV, tt=t0; for(const [s0,s1] of MK.durus){ if(s1<=tt) continue; if(tt+kalan<=s0) break; kalan-=Math.max(0,s0-tt); tt=Math.max(tt,s1); } return tt+kalan; };
  const bantYol=(t0,t1)=>{ let dur=0; for(const [s0,s1] of MK.durus){ const a=Math.max(s0,t0), b=Math.min(s1,t1); if(b>a) dur+=b-a; } return Math.max(0,(t1-t0-dur))*HIZ.bantV; };
  const nozOf=p=>p.tip==='pide'?NOZ.kasar:(p.id%2?NOZ.harc:NOZ.harc2);
  /* bırakma anı td belli olunca ürünün makine yolculuğu (fırın çıkışına kadar) kesinleşir */
  function makineKur(p,td){ const f=p.faz, noz=nozOf(p); p.noz=noz; p.td=td;
    if(!TABLA){ f.pres=[td,td+HIZ.pres]; f.gecis=[f.pres[1],f.pres[1]+HIZ.gecis];
      const eb=Math.max(f.gecis[1],bantZaman(MK.bantSon,FIRIN.adim)); f.bantBek=[f.gecis[1],eb];
      /* fırın sırası: ürün fırın ağzının 350 mm GERİSİNDE bekler (öndeki ürün fırın bandında yavaş gider; ağızda beklerse üst üste binerler) → öndekiyle arası hiçbir an 350'den az olmaz */
      const a1=bantZaman(eb,BANT.cikis-FIRIN.adim-BANT.giris), kalk=Math.max(a1,MK.firinBos-FIRIN.adim/HIZ.bantV); if(kalk>a1+1e-6){ MK.durus.push([a1,kalk]); MK.durus.sort((x,y)=>x[0]-y[0]); }
      const a=bantZaman(eb,BANT.cikis-BANT.giris), eo=a;
      f.bant=[eb,a]; f.doz=[bantZaman(eb,noz.x-150-BANT.giris),bantZaman(eb,noz.x+150-BANT.giris)]; f.firinBek=[a,eo]; f.firin=[eo,eo+firinSure];
      MK.bantSon=eb; MK.presBos=eb; MK.firinBos=eo+girisAralik; }
    else { const tz=HIZ.tablaZ, v=HIZ.tablaV, doz0=p.tip==='pide'?HIZ.kasar:HIZ.harc; let tt=td;
      /* ATOSA ÜRETİCİ VERİSİ: bir ürün en az atosaTur (60 sn) sürer → hesapla çıkan tur kısaysa fark dozaja eklenir (fırın sırası beklemesi ayrıca eklenir) */
      const nominal=4*tz+HIZ.pres+Math.abs(noz.x-TAB.pres)/v+doz0+HIZ.geriEm+Math.abs(TAB.firin-noz.x)/v+HIZ.siyir+HIZ.it+(TAB.firin-TAB.pres)/v, doz=doz0+Math.max(0,HIZ.atosaTur-nominal); p.dozSure=doz;
      const ekle=(ad,s)=>{ f[ad]=[tt,tt+s]; tt+=s; };
      ekle('ors',tz); ekle('pres',HIZ.pres); ekle('kalk',tz); ekle('git1',Math.abs(noz.x-TAB.pres)/v); ekle('agiz',tz); ekle('doz',doz); ekle('em',HIZ.geriEm); ekle('in',tz); ekle('git2',Math.abs(TAB.firin-noz.x)/v);
      const bek=Math.max(0,MK.firinBos-(tt+HIZ.siyir+HIZ.it)); ekle('firinBek',bek); ekle('siyir',HIZ.siyir); ekle('it',HIZ.it);
      f.firin=[tt,tt+firinSure]; MK.firinBos=tt+girisAralik; f.don=[tt,tt+(TAB.firin-TAB.pres)/v]; MK.presBos=f.don[1]; MK.tur.push(MK.presBos-td); }
    p.plakaGelis=f.firin[1]+HIZ.plakaGecis; p.stage='makinede'; MK.kuyruk.push(p); }
  /* fırından çıkanlar: plaka → kesim → sprey → (açık kutu tepside hazırsa) kutuya it → kapak. Tepsinin dönüş anı bilinmiyorsa (kapalı kutu hâlâ robotu bekliyor) sıradaki ürün çözülemez. */
  function kuyrukIsle(){ while(MK.kuyruk.length&&MK.kutuHazir!==null){ const p=MK.kuyruk.shift(), f=p.faz, gel=p.plakaGelis;
      if(MK.plakaBos>gel+0.05){ sayac.sikisma++; not.push('SIKIŞMA: #'+p.id+' fırın çıkışında '+(MK.plakaBos-gel).toFixed(0)+' sn bekledi (plaka dolu)'); }
      const bas=Math.max(gel,MK.plakaBos); f.plaka=[f.firin[1],f.firin[1]+HIZ.plakaGecis]; f.kes=[bas,bas+HIZ.kesim]; f.sprey=[f.kes[1],f.kes[1]+HIZ.sprey];
      const it0=Math.max(f.sprey[1],MK.kutuHazir); f.kutuBek=[f.sprey[1],it0]; f.kutuIt=[it0,it0+HIZ.itici]; f.kapan=[f.kutuIt[1],f.kutuIt[1]+HIZ.kapan]; sayac.kutuBek+=it0-f.sprey[1];
      p.kutuKonT=MK.kutuKonT; p.kutudaAt=f.kapan[1]; MK.plakaBos=f.kutuIt[1]; MK.kutuHazir=null; } }
  function tepsiDondu(geriT){ MK.kutuKonT=Math.max(geriT,MK.katlaBitis); MK.kutuHazir=MK.kutuKonT+HIZ.kutuKoy; MK.katlaBitis=MK.kutuKonT+HIZ.katla; kuyrukIsle(); }
  function teslimKontrol(o,t1){ if(o.teslim) return; if(P.find(p=>p.o===o&&p.stage!=='bitti'&&p.stage!=='iptal')===undefined&&o.kolaTeslim&&o.tatliTeslim){ o.teslim=t1; const d=dolap.find(d=>d.o===o); if(d){ d.freeAt=t1+HIZ.musteri; plan.push({tip:'musteri',ad:'müşteri '+o.id,t0:d.freeAt,t1:d.freeAt+2,ri:0,ref:o,steps:[{ad:'MÜŞTERİ ALDI · sipariş '+o.id,sure:2,fn:()=>{},bitir:()=>{ o.nesneler.forEach(n=>nesneSil(n)); o.nesneler=[]; }}]}); } } }
  const kopya=c=>({carX:c.carX,tcp:c.tcp.clone(),t:c.t.clone(),u:c.u.clone(),yuk:c.yuk,parmak:c.parmak});
  const KUTU_X=carFor(KUT.cx,KUT.trayY,KUT.cz,1);
  let guard=0;
  while(guard++<200000){
    const r=RBT.slice(0,N).reduce((a,b)=>b.t<a.t?b:a); t=r.t; if(!isFinite(t)) break;
    const yol=x=>Math.abs(r.cur.carX-x)/HIZ.ray+2, cands=[];
    for(const p of P){ if(p.stage==='makinede'&&p.kutudaAt!==undefined&&p.kutudaAt<=t+yol(KUTU_X)){ const oo=p.o; if(oo.kolaTeslim&&oo.tatliTeslim&&(oo.icBitis||0)<=t&&dolapAl(oo,t)) cands.push({pri:1,p,tip:'KUTU',ready:p.kutudaAt}); } }
    for(const oo of O){ if(oo.arr>t||oo.teslim) continue; const ur=P.filter(p=>p.o===oo), yolda=ur.some(p=>p.stage!=='bekliyor'&&p.stage!=='iptal'), acil=ur.some(p=>p.kutudaAt!==undefined&&p.stage==='makinede'&&p.kutudaAt<=t+90)?0:3;
      if(yolda&&oo.kola&&!oo.kolaTeslim&&dolapAl(oo,t)) cands.push({pri:acil,o:oo,tip:'KOLA',ready:oo.arr}); else if(yolda&&oo.tatli&&!oo.tatliTeslim&&(!oo.kola||oo.kolaTeslim)&&dolapAl(oo,t)) cands.push({pri:acil,o:oo,tip:'TATLI',ready:oo.arr}); }
    if(MK.presBos<=t+22&&P.filter(q=>q.stage==='makinede').length<OPT.wip){ const p=P.find(p=>p.stage==='bekliyor'&&p.o.arr<=t); if(p) cands.push({pri:6,p,tip:'HAMUR',ready:p.o.arr}); }
    cands.sort((a,b)=>a.pri-b.pri||a.ready-b.ready);
    let yapildi=false;
    const kutulu=P.find(q=>q.stage==='makinede'&&q.kutudaAt!==undefined), gelSonra=MK.kuyruk.length?MK.kuyruk[0].plakaGelis:Infinity;
    /* İLERİ BAKIŞ: kutu dışı bir iş, sıradaki ürün plakaya gelmeden tepsinin dönmesini geciktirecekse alınmaz (plaka dolu kalır → fırın çıkışı sıkışır) */
    const gecikir=(B,oo)=>{ if(N>1&&r.i===0) return false;   /* 2 robotta hamuru SOL robot koyar, kutu tepsisini geciktirmez */
      if(!kutulu||(oo&&oo===kutulu.o)) return false; const A=t+gecen(B)+Math.abs(B.cur.carX-KUTU_X)/HIZ.ray+2; return A>Math.max(kutulu.kutudaAt,gelSonra-OPT.kutuSure)+0.5; };
    const benim=c=>N<2||(r.i===0?c.tip==='HAMUR':c.tip!=='HAMUR');
    for(const c of cands){ if(!benim(c)) continue; const cur=kopya(r.cur), B=insaci(cur,1); let ad='', b=null;
      if(c.tip==='HAMUR'){ const p=c.p, s=stokBak(stok,p.tip); if(!s){ p.stage='iptal'; not.push('stok bitti: '+p.tip); continue; } p.kolon=s.kolon; p.sira=s.sira; p.topPos=s.pos; p.yan=s.yan; p.carPres=s.tek?s.yan:carPres();
        ad='#'+p.id+' '+p.tip+' · hamur → '+(TABLA?'tabla':'pres'); const td=G_hamur(B,p,t,MK.presBos); if(gecikir(B,null)){ sayac.ertelenen=(sayac.ertelenen||0)+1; continue; }
        { const ck=cakBekle(r,B,cur.carX,t); if(ck>t+1e-6){ r.t=ck; sayac.rayBek=(sayac.rayBek||0)+(ck-t); yapildi=true; break; } } s.q.k++; b=blok('robot',ad,t,B.st,p,r.i); makineKur(p,td); kuyrukIsle(); }
      else if(c.tip==='KUTU'){ const p=c.p, oo=p.o; ad='#'+p.id+' · kutu → QR göz '+(oo.goz+1)+' → tepsi geri'; const z=G_kutu(B,p,oo,tepsi,t,p.kutudaAt);
        { const ck=cakBekle(r,B,cur.carX,t); if(ck>t+1e-6){ r.t=ck; sayac.rayBek=(sayac.rayBek||0)+(ck-t); yapildi=true; break; } }
        b=blok('robot',ad,t,B.st,p,r.i); b.bitis=1; b.bitisT=z.teslimT; p.stage='bitti'; p.bitti=z.teslimT; p.alT=z.alT; oo.kutuSay++; teslimKontrol(oo,z.teslimT); tepsiDondu(z.geriT); }
      else { const oo=c.o, tip=c.tip==='KOLA'?'kola':'tatli', s=stokBak(stok,tip); if(!s){ if(tip==='kola') oo.kolaTeslim=true; else oo.tatliTeslim=true; not.push('stok bitti: '+tip); continue; }
        oo[tip+'Stok']=s; ad='sipariş '+oo.id+' · '+(tip==='kola'?'içecek':'tatlı')+' → QR göz '+(oo.goz+1); G_icecek(B,oo,tip); if(gecikir(B,oo)){ sayac.ertelenen=(sayac.ertelenen||0)+1; continue; }
        { const ck=cakBekle(r,B,cur.carX,t); if(ck>t+1e-6){ r.t=ck; sayac.rayBek=(sayac.rayBek||0)+(ck-t); yapildi=true; break; } } s.q.k++; b=blok('robot',ad,t,B.st,oo,r.i); if(tip==='kola') oo.kolaTeslim=true; else oo.tatliTeslim=true; oo.icBitis=Math.max(oo.icBitis||0,b.t1); b.icecek=1; teslimKontrol(oo,b.t1); }
      r.res.push(Object.assign({t0:b.t0,t1:b.t1},cakAralik(B,cur.carX))); r.cur=B.cur; r.busy+=b.t1-b.t0; r.is[c.tip]=(r.is[c.tip]||0)+1; r.t=b.t1; sonBitis=Math.max(sonBitis,b.t1); yapildi=true; break; }
    if(!yapildi){ const ev=[]; P.forEach(p=>{ if(p.stage==='bekliyor'&&p.o.arr>t) ev.push(p.o.arr); if(p.stage==='makinede'&&p.kutudaAt!==undefined) ev.push(p.kutudaAt-yol(KUTU_X)); }); if(P.some(p=>p.stage==='bekliyor'&&p.o.arr<=t)) ev.push(MK.presBos-22);
      dolap.forEach(d=>{ if(d.freeAt>t&&isFinite(d.freeAt)) ev.push(d.freeAt); }); O.forEach(q=>{ if((q.icBitis||0)>t) ev.push(q.icBitis); });
      if(N>1) RBT.forEach(q=>{ if(q!==r&&isFinite(q.t)&&q.t>t) ev.push(q.t); });
      const nx=ev.filter(x=>x>t+1e-6); if(nx.length) r.t=Math.min(...nx); else if(P.some(p=>p.stage==='makinede'||p.stage==='bekliyor')) r.t=t+5; else r.t=Infinity; }
  }
  /* ---- makine blokları (ürün yolculuğu · oynatıcı için) ---- */
  P.forEach(p=>{ if(!p.td&&p.td!==0) return; makineBlok(p,plan,tepsi); });
  plan.sort((a,b)=>a.t0-b.t0);
  const teslim=O.filter(o=>o.teslim), bek=teslim.map(o=>o.teslim-o.arr).sort((a,b)=>a-b), ort=bek.length?bek.reduce((a,b)=>a+b,0)/bek.length:0, biten=P.filter(p=>p.stage==='bitti').length;
  plan.forEach(b=>{ if(b.tip!=='musteri') sonBitis=Math.max(sonBitis,b.t1); });
  const kpi={N, robotDoluluk:RBT.slice(0,N).map(q=>sonBitis?q.busy/sonBitis:0), robotIs:RBT.slice(0,N).map(q=>q.is), siparis:O.length, teslim:teslim.length, urun:P.length, biten, ort, max:bek.length?bek[bek.length-1]:0, gec:bek.filter(b=>b>1500).length, sure:sonBitis, robot:sonBitis?Math.max(...RBT.slice(0,N).map(q=>q.busy))/sonBitis:0, isler:RB.is, not,
    erisilemeyen:stok.erisilemeyen||0, sayac, tur:MK.tur, urunSure:biten?plan.filter(b=>b.tip==='robot').reduce((a,b)=>a+(b.t1-b.t0),0)/biten:0, O, P};
  return {plan,kpi,tepsi,O,P,N:1,bantYol};
}
/* ürünün makine içindeki yolculuğu → oynatıcı adımları (doğrusal zaman · lin) */
function makineBlok(p,plan,tepsi){ const f=p.faz, P_=PRES(), st=[], u={tip:'urun',pos:V(P_.cx,PK,P_.cz),icerik:'top',dolu:0,urun:p.tip,rot:0}; p.urunN=u; let son=p.td;
  const adim=(ar,ad,fn,basla,bitir)=>{ if(!ar) return; if(ar[0]>son+1e-6) st.push({ad:'bekliyor',sure:ar[0]-son,lin:true,fn:()=>{}}); if(ar[1]-ar[0]>1e-6){ st.push({ad,sure:ar[1]-ar[0],lin:true,fn:fn||(()=>{}),basla,bitir}); } else { if(basla||bitir) st.push({ad,sure:0.001,lin:true,fn:()=>{},basla,bitir}); } son=Math.max(son,ar[1]); };
  const presFn=e=>{ const a=e<.4?e/.4:e>.6?(1-e)/.4:1; S.ustPlakaY=a*190; if(e>.45) u.icerik='taban'; }, goster=()=>{ u.icerik='top'; u.dolu=0; u.rot=0; u.pos.set(P_.cx,PK,P_.cz); nesneGoster(u); };
  const noz=p.noz, renk=noz.renk;
  if(!TABLA){
    adim(f.pres,'PRES · '+HIZ.pres+' s',presFn,goster,()=>{ S.ustPlakaY=0; u.icerik='taban'; });
    adim(f.gecis,'pres → bant geçişi',e=>{ u.pos.set(P_.cx+(BANT.giris-P_.cx)*e,PK,P_.cz+(EKSEN-P_.cz)*e); });
    adim(f.bantBek,'bant girişi bekliyor (adım 350)');
    adim(f.bant,'TOPPING BANDI · başlık altından geçerken dozaj',e=>{ const T=f.bant[0]+e*(f.bant[1]-f.bant[0]), x=BANT.giris+PLANLA_bantYol(f.bant[0],T); u.pos.set(Math.min(BANT.cikis,x),PK,EKSEN);
        const w0=noz.x-150, w1=noz.x+150; if(x>=w0&&x<=w1){ u.icerik='ustlu'; u.dolu=Math.max(u.dolu,(x-w0)/300); S.akis={x:noz.x,z:EKSEN,renk,y0:PK+12,sahip:u}; } else { if(x>w1){ u.icerik='ustlu'; u.dolu=1; } if(S.akis&&S.akis.sahip===u) S.akis=null; } },null,()=>{ u.icerik='ustlu'; u.dolu=1; if(S.akis&&S.akis.sahip===u) S.akis=null; });
    adim(f.firinBek,'fırın sırası · bant durdu');
  } else {
    const tb=S.tabla, tasi=()=>{ u.pos.set(tb.x,tb.y,EKSEN); u.rot=tb.rot; };
    adim(f.ors,'tabla örse iner',e=>{ tb.x=TAB.pres; tb.y=PK-20*e; tasi(); },()=>{ tb.x=TAB.pres; tb.y=PK; tb.rot=0; goster(); u.pos.set(TAB.pres,PK,EKSEN); });
    adim(f.pres,'PRES tablanın üstüne basar · '+HIZ.pres+' s',presFn,null,()=>{ S.ustPlakaY=0; u.icerik='taban'; });
    adim(f.kalk,'tabla örsten kalkar',e=>{ tb.y=PK-20*(1-e); tasi(); });
    adim(f.git1,'tabla → '+(p.tip==='pide'?'kaşar':'harç')+' haznesinin altına',e=>{ tb.x=TAB.pres+(noz.x-TAB.pres)*e; tb.y=PK; tasi(); });
    adim(f.agiz,'tabla ağıza kalkar (+'+TAB.kalk+')',e=>{ tb.y=PK+TAB.kalk*e; tasi(); });
    adim(f.doz,(p.tip==='pide'?'KAŞAR':'HARÇ')+' DOZAJI · tabla döner + kayar',e=>{ tb.rot=e*Math.PI*4; tb.x=noz.x+60*Math.sin(e*Math.PI*2); tb.y=PK+TAB.kalk; u.icerik='ustlu'; u.dolu=e; tasi(); S.akis={x:noz.x,z:EKSEN,renk,y0:PK+TAB.kalk+12,sahip:u}; },null,()=>{ u.dolu=1; tb.x=noz.x; if(S.akis&&S.akis.sahip===u) S.akis=null; });
    adim(f.em,'helezon geri emer · klape kapanır'); adim(f.in,'tabla iner',e=>{ tb.y=PK+TAB.kalk*(1-e); tasi(); });
    adim(f.git2,'tabla → fırın ağzı',e=>{ tb.x=noz.x+(TAB.firin-noz.x)*e; tb.y=PK; tasi(); });
    adim(f.firinBek,'fırın sırası bekleniyor'); adim(f.siyir,'itici iner (ürünün arkasına)');
    adim(f.it,'itici ürünü fırın bandına iter',e=>{ u.pos.set(TAB.firin+(FIRIN.x[0]-TAB.firin)*e,PK,EKSEN); });
    plan.push({tip:'makine',ad:'tabla dönüşü #'+p.id,t0:f.don[0],t1:f.don[1],ri:0,ref:p,steps:[{ad:'tabla pres altına döner (boş)',sure:f.don[1]-f.don[0],lin:true,fn:e=>{ tb.x=TAB.firin+(TAB.pres-TAB.firin)*e; tb.y=PK; tb.rot=0; }}]});
  }
  adim(f.firin,'KONVEYÖR FIRIN · '+HIZ.pisme+' s',e=>{ u.pos.set(FIRIN.x[0]+(FIRIN.x[1]-FIRIN.x[0])*e,PK,EKSEN); if(e>.72) u.icerik='pismis'; },null,()=>{ u.icerik='pismis'; });
  if(f.plaka){
    adim(f.plaka,'fırın çıkışı → kesme plakası',e=>{ u.pos.set(FIRIN.x[1]+(KESP.cx-FIRIN.x[1])*e,PK,EKSEN); });
    adim(f.kes,'YILDIZ BIÇAK · '+HIZ.kesim+' s',e=>{ const a=e<.5?e*2:2-e*2; S.bicakY=a*200; },null,()=>{ S.bicakY=0; });
    adim(f.sprey,'TEREYAĞI SPREYİ · '+HIZ.sprey+' s'); adim(f.kutuBek,'kutu / tepsi bekleniyor');
    const kN={tip:'kutu',pos:V(KUT.cx,KUT.trayY+5+EL.KUTU_H/2,KUT.cz),kapali:false,kapanma:0,icerik:''}; p.kutuN=kN;
    plan.push({tip:'makine',ad:'kutu #'+p.id,t0:p.kutuKonT,t1:p.kutuKonT+HIZ.kutuKoy,ri:0,ref:p,steps:[{ad:'katlanmış açık kutu tepsiye kondu',sure:HIZ.kutuKoy,lin:true,basla:()=>{ kN.kapali=false; kN.kapanma=0; kN.icerik=''; kN.pos.set(KUT.cx,KUT.trayY+5+EL.KUTU_H/2,KUT.cz); nesneGoster(kN); },fn:()=>{}}]});
    adim(f.kutuIt,'İTİCİ · ürün plakadan açık kutuya',e=>{ S.itme=e; u.pos.set(KESP.cx+(KUT.cx-KESP.cx)*e,PK-(PK-KUT.trayY-18)*Math.max(0,(e-.75)/.25),EKSEN); },null,()=>{ S.itme=0; nesneSil(u); kN.icerik='pide'; });
    adim(f.kapan,'KUTU KAPAĞI KAPANIR · '+HIZ.kapan+' s',e=>{ kN.kapanma=e; },null,()=>{ kN.kapanma=1; kN.kapali=true; });
  }
  const b={tip:'makine',ad:'#'+p.id+' '+p.tip+' · makine',t0:p.td,t1:son,steps:st,ref:p,ri:0}; plan.push(b); }
let PLANLA_bantYol=()=>0;
/* TAKT kendini ayarlar: 1. geçiş (taktsız) robotun ürün başına saf işini ölçer (hamur + kutu, beklemeler hariç). Sonra fırın giriş aralığı için üç aday denenir
   (taktsız · saf iş × 1,04 · saf iş × 1,10) ve SIKIŞMASIZ olanlardan ilk 2 saatte en çok ürün çıkaran seçilir. Tablalı hatta tabla turu (Atosa 60 sn) zaten tempoyu verir → çoğu zaman taktsız kazanır;
   bantlıda kutular robotun yetişebileceği tempoda çıksın diye takt kazanır (plaka dolu kalmaz, robot kutulama ağzında boş beklemez). */
function planlaOto(cfg){ OPT.takt=0; const p1=planla(cfg); if(p1.kpi.urun<4) return p1;
  const saf=b=>b.steps.reduce((a,s)=>a+(s.ad.indexOf('· bekle')>=0?0:s.sure),0), ort=a=>a.length?a.reduce((x,y)=>x+y,0)/a.length:0;
  const H=ort(p1.plan.filter(b=>b.tip==='robot'&&b.ad.indexOf('hamur')>=0).map(saf)), K=ort(p1.plan.filter(b=>b.tip==='robot'&&b.bitis).map(saf)), taban=FIRIN.adim/(FIRIN.hazne/HIZ.pisme);
  const puan=ps=>ps.plan.filter(b=>b.bitis&&b.bitisT<=7200).length-(ps.kpi.sayac.sikisma?1e6:0)-ps.kpi.ort/1e5;
  const isSuresi=(cfg.robot===2)?Math.max(H,K):(H+K);   /* 2 robot: hamur SOL'da, kutu SAĞ'da → paralel, toplanmaz */
  let en=p1, enT=0; for(const kat of [1.04,1.10]){ const tk=Math.max(taban,isSuresi*kat); if(tk<=taban+0.5) continue; OPT.takt=tk; const ps=planla(cfg); if(puan(ps)>puan(en)+1e-9){ en=ps; enT=tk; } }
  OPT.takt=enT; en.kpi.takt=enT; en.kpi.hamurSure=H; en.kpi.kutuSure=K; return en; }

/* ================= OYNATICI (zaman tabanlı · bloklar paralel · ileri/geri sarılabilir) ================= */
let anim=null, OYN=null;
function hazirla(ps){ [[0,1100],[1,4400]].forEach(([i,x])=>{ const rb=ROB[i]; rb.carX=x; rb.t.set(0,0,-1); rb.u.set(0,1,0); rb.yuk='bos'; rb.tasi=null; rb.parmak=70; rb.tcp.copy(parkTcp(x)); }); S.ri=0;
  Object.keys(KOLON).forEach(k=>{ S.cek[k]=0; S.cekI[k]=0; }); S.qrk={}; S.itme=0; S.akis=null; S.ustPlakaY=0; S.bicakY=0; S.tabla.x=TAB.pres; S.tabla.y=PK; S.tabla.rot=0;
  S.nesne.slice().forEach(n=>nesneSil(n)); Object.values(HAVUZ).forEach(h=>h.forEach(m=>{ m.visible=false; m.userData.sahip=null; }));
  if(ps){ ps.P.forEach(p=>{ if(p.urunN) p.urunN.mesh=null; if(p.kutuN) p.kutuN.mesh=null; }); ps.tepsi.mesh=null; ps.tepsi.icerik=''; ps.tepsi.pos=V(KUT.cx,KUT.trayY,KUT.cz); nesneGoster(ps.tepsi); ps.O.forEach(o=>{ o.nesneler=[]; }); ps.plan.forEach(b=>b.steps.forEach(s=>{ s._basladi=false; })); PLANLA_bantYol=ps.bantYol||(()=>0); }
  log.innerHTML=''; }
const ease=t=>t<.5?2*t*t:-1+(4-2*t)*t;
function saat(T){ const b=+($('saat0').value||17)*3600+T; const h=Math.floor(b/3600)%24, m=Math.floor(b%3600/60), s=Math.floor(b%60); return `${h}:${m<10?'0':''}${m}:${s<10?'0':''}${s}`; }
function motor(T){ const robotAd=['',''], adim=['','']; let makine=[], bitti=true, nextT=Infinity;
  for(const b of OYN.bl){ if(T<b.t0){ bitti=false; nextT=Math.min(nextT,b.t0); continue; } S.ri=b.ri||0; let ls=b.t0+b.acc;
    while(b.cursor<b.steps.length){ const s=b.steps[b.cursor]; if(T<ls) break; if(!s._basladi){ if(s.basla) s.basla(); s._basladi=true; }
      if(T>=ls+s.sure){ s.fn(1); if(s.bitir) s.bitir(); b.cursor++; b.acc+=s.sure; ls+=s.sure; continue; } const e=(T-ls)/s.sure; s.fn(s.lin?e:ease(e)); if(b.tip==='robot'){ robotAd[b.ri||0]=b.ad; adim[b.ri||0]=s.ad; } else if(b.tip==='makine'&&s.ad!=='bekliyor') makine.push((b.ref?'#'+b.ref.id+' ':'')+s.ad); break; }
    if(b.cursor<b.steps.length) bitti=false; }
  S.ri=0; return {robotAd,adim,makine,bitti,nextT}; }
function durumYaz(T,m){ const ps=OYN.ps; if(!ps._bit){ ps._bit=ps.plan.filter(b=>b.bitis).map(b=>b.bitisT).sort((a,b)=>a-b); ps._tes=ps.O.filter(o=>o.teslim).map(o=>o.teslim).sort((a,b)=>a-b); }
  const say=(a)=>{ let n=0; while(n<a.length&&a[n]<=T) n++; return n; }, N=(ps.kpi&&ps.kpi.N)||1;
  const satir=i=>{ const ad=m.robotAd[i]; return ad?(ad.split(' · ')[0]+' · '+m.adim[i]):'<span style="color:#8a94a4">boşta</span>'; };
  const ne=satir(0);
  step.innerHTML=`<div><span style="color:#8a94a4">${saat(T)}</span> · ÇIKAN ÜRÜN <b style="color:#3ddc84">${say(ps._bit)}</b> / ${ps.kpi.urun} <span style="color:#8a94a4">· teslim ${say(ps._tes)} / ${ps.kpi.siparis} sipariş</span></div><div><span style="color:#2997ff">${N>1?'SOL':'ROBOT'}</span> <span style="color:#d5dbe6;font-weight:500">${ne}</span></div>${N>1?`<div><span style="color:#ff8c40">SAĞ</span> <span style="color:#d5dbe6;font-weight:500">${satir(1)}</span></div>`:''}<div><span style="color:#ffb340">MAKİNE</span> <span style="color:#c9ccd3;font-weight:500">${m.makine.length?m.makine.slice(0,3).join(' · ')+(m.makine.length>3?' · +'+(m.makine.length-3):''):'<span style="color:#8a94a4">boş</span>'}</span></div>`;
  const sc=$('scrub'); if(sc&&!sc._tut) sc.value=T; $('scrubT').textContent=saat(T)+' / '+saat(OYN.ps.kpi.sure); kafaKoy(T); }
function zamanaGit(ps,T){ if(!OYN||OYN.ps!==ps) OYN={ps,T:0,bl:[],son:0}; hazirla(ps); OYN.bl=ps.plan.map(b=>({...b,cursor:0,acc:0})); OYN.T=Math.max(0,Math.min(ps.kpi.sure+3,T)); const m=motor(OYN.T); ciz(); durumYaz(OYN.T,m); if(window.sonucCiz) sonucCiz(HATTIP,ps,OYN.T); return m; }
function oynat(ps){ dur(); if(!OYN||OYN.ps!==ps||OYN.T>=ps.kpi.sure) zamanaGit(ps,0); OYN.son=performance.now(); $('play').textContent='❚❚ Duraklat';
  function frame(now){ const dt=Math.min(0.1,(now-OYN.son)/1000); OYN.son=now; OYN.T+=dt*(+hiz.value); const m=motor(OYN.T); ciz(); durumYaz(OYN.T,m);
    if(!m.robotAd[0]&&!m.makine.length&&isFinite(m.nextT)&&m.nextT-OYN.T>3&&(+hiz.value)<10) OYN.T=m.nextT-1;
    if(m.bitti){ anim=null; $('play').textContent='▶ Oynat'; return; } anim=requestAnimationFrame(frame); }
  anim=requestAnimationFrame(frame); }
function dur(){ if(anim){ cancelAnimationFrame(anim); anim=null; } const p=$('play'); if(p) p.textContent='▶ Oynat'; }
/* tüm planı zaman adımlarıyla tara: erişim + çarpışma (çevre · kendi gövdesi) */
function sessizKontrol(ps,adimSn){ dur(); zamanaGit(ps,0); const dt=adimSn||(ps.kpi.sure>2500?0.7:0.25), kayit={}; let n=0;
  for(let T=0;T<=ps.kpi.sure+1;T+=dt){ const m=motor(T); ciz(); n++; if(!m.robotAd[0]) continue; const k=ROB[0].sonIK, key=m.robotAd[0].replace(/#\d+ /,'').replace(/sipariş \d+ · /,'').replace(/göz \d+/,'göz')+' | '+m.adim[0]; if((k&&!k.ok)||ROB[0].temas.length){ const r=kayit[key]||(kayit[key]={b:m.robotAd[0],s:m.adim[0],yok:false,eks:0,hs:{},n:0}); r.n++; if(k&&!k.ok){ r.yok=true; r.eks=Math.max(r.eks,k.D-k.maxD); } ROB[0].temas.forEach(h=>{ r.hs[h.parca+'→'+h.engel.split(' ').slice(0,2).join(' ')]=1; }); } }
  const rows=Object.values(kayit).map(r=>({b:r.b,s:r.s,yok:r.yok,eks:r.eks,hs:Object.keys(r.hs),n:r.n}));
  log.innerHTML=`<div><b>${n} an tarandı</b> (${dt} sn arayla) · ${rows.length?'<span class="yok">'+rows.length+' sorunlu adım</span>':'<span class="ok">erişim tam · temas yok</span>'}</div>`+rows.slice(0,40).map(r=>`<div><b>${r.b}</b> · ${r.s} — ${r.yok?'<span class="yok">erişim YOK −'+r.eks.toFixed(0)+'</span> ':''}<span class="yok">${r.hs.join(', ')}</span></div>`).join('');
  zamanaGit(ps,0); return rows; }

/* ================= KPI + GANTT ================= */
function fmt(s){ return s>=60?(s/60).toFixed(1)+' dk':s.toFixed(0)+' s'; }
function kpiYaz(ps){ const k=ps.kpi, e=$('kpi'), T=Math.max(1,k.sure);
  const hh=[0,0,0,0], ht=[{pide:0,lahm:0},{pide:0,lahm:0}]; ps.plan.filter(b=>b.bitis).forEach(b=>{ const i=Math.min(3,Math.floor(b.bitisT/3600)); hh[i]++; if(i<2) ht[i][b.ref.tip]++; });
  const icS=ps.plan.filter(b=>b.icecek&&b.t1<=3600).length;
  const mak={}; ps.plan.filter(b=>b.tip==='robot').forEach(b=>{ const key=b.ad.indexOf('hamur')>=0?'hamur: çekmece → '+(TABLA?'tabla':'pres'):b.ad.indexOf('kutu')>=0?'kutu → QR → tepsi geri':b.ad.indexOf('içecek')>=0?'içecek → QR':'tatlı → QR'; (mak[key]=mak[key]||[]).push(b.t1-b.t0); });
  const dol={pres:0}; dol[TABLA?'tabla':'bant']=0; dol['fırın (4 ürünlük)']=0; dol['kesme + sprey']=0; dol.kutu=0;
  ps.P.forEach(p=>{ const f=p.faz; if(!f.pres) return; dol.pres+=f.pres[1]-f.pres[0]; if(TABLA){ if(f.don) dol.tabla+=f.don[1]-p.td; } else if(f.bant) dol.bant+=(f.bant[1]-f.bant[0])/5; if(f.firin) dol['fırın (4 ürünlük)']+=(f.firin[1]-f.firin[0])/(FIRIN.hazne/FIRIN.adim+0.29); if(f.kes) dol['kesme + sprey']+=f.sprey[1]-f.kes[0]; if(f.kutuIt) dol.kutu+=f.kapan[1]-f.kutuIt[0]; });
  const bar=(ad,v,renk)=>`<tr><td>${ad}</td><td style="width:58%"><div style="background:#1f242e;border-radius:4px;height:9px;margin-top:4px"><div style="width:${Math.min(100,v*100).toFixed(0)}%;height:9px;border-radius:4px;background:${renk||(v>.85?'#ff5c5c':v>.6?'#ffb340':'#3ddc84')}"></div></div></td><td style="width:44px">${(v*100).toFixed(0)} %</td></tr>`;
  const cok=k.siparis>3;
  let h='<table>'+[['Sipariş · ürün',`${k.siparis} · ${k.urun}`],['Teslim edilen',`${k.teslim} sipariş · ${k.biten} ürün`],
    cok?['Çıkan ürün · 1. / 2. / 3. saat / sonrası',`<b>${hh[0]} / ${hh[1]} / ${hh[2]}</b> / ${hh[3]}`]:null,
    cok?['1. saat · pide + lahmacun',`${ht[0].pide} + ${ht[0].lahm}`+(icS?` · ayrıca ${icS} içecek / tatlı taşındı`:'')]:null, cok?['2. saat · pide + lahmacun',`${ht[1].pide} + ${ht[1].lahm}`]:null,
    ['Ortalama bekleme',`<b>${fmt(k.ort)}</b>`],['En uzun bekleme',fmt(k.max)], cok?['25 dk üstü bekleyen',`<span class="${k.gec?'yok':'ok'}">${k.gec} sipariş</span>`]:null,
    ['Son teslim',saat(k.sure)]].filter(Boolean).map(r=>`<tr><td>${r[0]}</td><td>${r[1]}</td></tr>`).join('')+'</table>';
  h+='<h2>Hat dengesi</h2><table>'+bar('ROBOT',k.robot,k.robot>.85?'#ff5c5c':'#2997ff')+Object.entries(dol).map(([a,v])=>bar(a,v/T)).join('')+'</table>';
  h+='<h2>Robot ne yaptı · ortalama süre</h2><table>'+Object.entries(mak).map(([a,v])=>`<tr><td>${a}</td><td>${fmt(v.reduce((x,y)=>x+y,0)/v.length)} × ${v.length}</td></tr>`).join('')+`<tr><td><b>ürün başına robot</b></td><td><b>${fmt(k.urunSure)}</b> → en fazla ${(3600/Math.max(1,k.urunSure)).toFixed(0)} ürün/saat</td></tr>`
    +(k.hamurSure?`<tr><td>fırın giriş temposu (takt)</td><td>${k.takt?k.takt.toFixed(0)+' s (robot: hamur '+k.hamurSure.toFixed(0)+' + kutu '+k.kutuSure.toFixed(0)+' s)':'yok · tempoyu '+(TABLA?'tabla turu':'robot')+' veriyor'}</td></tr>`:'')+`<tr><td>fırın tavanı</td><td>${(3600/(FIRIN.adim/(FIRIN.hazne/HIZ.pisme))).toFixed(0)} ürün/saat (hazne ${FIRIN.hazne} · ${HIZ.pisme} s)</td></tr>`+(TABLA&&k.tur.length?`<tr><td>tabla turu (ortalama)</td><td>${fmt(k.tur.reduce((a,b)=>a+b,0)/k.tur.length)} → en fazla ${(3600/(k.tur.reduce((a,b)=>a+b,0)/k.tur.length)).toFixed(0)} ürün/saat</td></tr>`:'')
    +`<tr><td>plakada kutu / tepsi bekleme</td><td>${fmt(k.sayac.kutuBek/Math.max(1,k.biten))} / ürün</td></tr><tr><td>sıkışma (plaka doluyken ürün geldi)</td><td><span class="${k.sayac.sikisma?'yok':'ok'}">${k.sayac.sikisma} kez</span></td></tr></table>`;
  const nt=[...new Set(k.not)].slice(0,6); if(k.erisilemeyen) nt.push(k.erisilemeyen+' stok konumu atlandı (kol yetişmiyor)'); if(nt.length) h+=`<div class="amb" style="margin-top:6px">${nt.join(' · ')}</div>`;
  e.innerHTML=h;
  $('siparisler').innerHTML=ps.O.slice(0,160).map(o=>`<div>#${o.id} ${saat(o.arr)} · ${o.items.join('+')}${o.kola?' +içecek':''}${o.tatli?' +tatlı':''} → ${o.teslim?'<span class="'+((o.teslim-o.arr)>1500?'yok':'ok')+'">'+fmt(o.teslim-o.arr)+'</span>':'<span class="yok">teslim yok</span>'}</div>`).join('');
}
let GX=null, GH=0, GHmax=0;
function altKur(){ $('gwrap').style.height=GH+'px'; $('scrubwrap').style.bottom=GH+'px'; $('tut').style.bottom=(GH+30)+'px'; }
try{ const v=localStorage.getItem('ak_gantt_h'); if(v!==null) GH=Math.max(0,+v||0); }catch(e){}
(function(){ const t=$('tut'); let y0=0, h0=0;
  t.addEventListener('pointerdown',e=>{ y0=e.clientY; h0=GH; t.setPointerCapture(e.pointerId); t._sur=true; e.preventDefault(); });
  t.addEventListener('pointermove',e=>{ if(!t._sur) return; GH=Math.max(0,Math.min(GHmax,h0+(y0-e.clientY))); altKur(); });
  const birak=()=>{ if(!t._sur) return; t._sur=false; try{ localStorage.setItem('ak_gantt_h',GH); }catch(e2){} };
  t.addEventListener('pointerup',birak); t.addEventListener('pointercancel',birak);
  t.addEventListener('dblclick',()=>{ GH=GH>20?0:GHmax; altKur(); try{ localStorage.setItem('ak_gantt_h',GH); }catch(e){} }); })();
altKur();
function gantt(ps){ const c=$('gantt'), W=Math.max(1200,Math.ceil(ps.kpi.sure/3600*1400)+80), rows=['robot','pres',TABLA?'tabla':'bant','fırın','kesme','kutu','QR dolabı'], H=30+rows.length*19; c.width=W; c.height=H; const g=c.getContext('2d'); g.fillStyle='#0d1016'; g.fillRect(0,0,W,H);
  const T1=Math.max(600,ps.kpi.sure), x=t=>70+t/T1*(W-90), ry=i=>6+i*19; GX={x,T1,W};
  g.font='11px sans-serif'; g.fillStyle='#8a94a4'; rows.forEach((r,i)=>g.fillText(r,4,ry(i)+12));
  for(let h=0;h<=T1/3600;h++){ const xx=x(h*3600); g.strokeStyle='#2a2f3a'; g.beginPath(); g.moveTo(xx,2); g.lineTo(xx,H-14); g.stroke(); g.fillStyle='#8a94a4'; g.fillText(saat(h*3600),xx+3,H-3); }
  const renk={HAMUR:'#3ddc84',KUTU:'#2997ff',KOLA:'#ff5c5c',TATLI:'#f5e6c8'}, dik=(a,i,c,al)=>{ if(!a) return; g.globalAlpha=al||1; g.fillStyle=c; g.fillRect(x(a[0]),ry(i),Math.max(1,x(a[1])-x(a[0])),15); g.globalAlpha=1; };
  ps.plan.forEach(b=>{ if(b.tip==='robot'){ const key=b.ad.indexOf('hamur')>=0?'HAMUR':b.ad.indexOf('kutu')>=0?'KUTU':b.ad.indexOf('içecek')>=0?'KOLA':'TATLI'; dik([b.t0,b.t1],0,renk[key]); } });
  ps.P.forEach(p=>{ const f=p.faz; if(!f.pres) return; dik(f.pres,1,'#4a5568'); if(TABLA) dik([p.td,f.don?f.don[1]:p.td],2,'#ffb340',.8); else dik(f.bant,2,'#ffb340',.45); dik(f.firin,3,'#d08060',.35); if(f.kes) dik([f.kes[0],f.sprey[1]],4,'#c084fc'); if(f.kutuIt) dik([f.kutuIt[0],f.kapan[1]],5,'#2997ff'); });
  ps.O.forEach(q=>{ if(!q.teslim) return; g.fillStyle='rgba(41,151,255,.35)'; g.fillRect(x(q.arr),ry(6),Math.max(1,x(q.teslim+HIZ.musteri)-x(q.arr)),15); g.fillStyle='#fff'; g.fillRect(x(q.arr),ry(6),1,15); });
  GHmax=H+8; if(GH>GHmax) GH=GHmax; altKur(); const sc=$('scrub'); sc.max=Math.ceil(ps.kpi.sure); sc.value=0; kafaKoy(0); }
function kafaKoy(T){ const k=$('kafa'); if(!k||!GX||GH<20) return; k.style.left=GX.x(T)+'px'; const w=$('gwrap'); if(anim){ const xx=GX.x(T); if(xx<w.scrollLeft+60||xx>w.scrollLeft+w.clientWidth-80) w.scrollLeft=Math.max(0,xx-w.clientWidth/3); } }

/* ================= UI ================= */
let PLAN=null;
function cfg(){ return {robot:+($('robotN')?$('robotN').value:1), sen:$('sen').value, urun:$('urun').value, kola:$('kola').checked, tatli:$('tatli').checked, seed:+$('seed').value||1, aralik:+$('aralik').value||120}; }
function planlaUI(){ dur(); if(window.sonucTemizle) sonucTemizle(); PLAN=planlaOto(cfg()); OYN=null; kpiYaz(PLAN); gantt(PLAN); zamanaGit(PLAN,0); step.innerHTML='<div>plan hazır · '+PLAN.plan.filter(b=>b.tip==='robot').length+' robot görevi</div><div style="color:#8a94a4">▶ ile oynat ya da alttaki çubuğu sürükle</div>'; return PLAN; }
$('planla').onclick=planlaUI; $('play').onclick=()=>{ if(anim){ dur(); return; } if(!PLAN) planlaUI(); oynat(PLAN); }; $('stop').onclick=()=>{ dur(); if(PLAN) zamanaGit(PLAN,0); };
$('kontrol').onclick=()=>{ if(!PLAN) planlaUI(); $('kontrol').textContent='taranıyor…'; setTimeout(()=>{ sessizKontrol(PLAN); $('kontrol').textContent='Tüm adımları tara · erişim + çarpışma'; },30); };
function senUI(){ const v=$('sen').value; $('tekRow').style.display=v==='tek'?'':'none'; $('akisRow').style.display=v==='akis'?'':'none'; }
['sen','robotN','aralik','urun','kola','tatli'].forEach(id=>$(id).addEventListener('change',()=>{ senUI(); planlaUI(); })); senUI();
/* SENARYO ÜÇ HATTA ORTAK: hat değiştirince (robotlu ↔ bantlı ↔ tablalı) ve karşılaştırma ekranına geçince son seçilen senaryo korunur */
try{ if(!window.PANELSIZ){ const v=localStorage.getItem('ak_sen'); if(v&&[...$('sen').options].some(o=>o.value===v)) $('sen').value=v; } }catch(e){}
$('sen').addEventListener('change',()=>{ try{ if(!window.PANELSIZ) localStorage.setItem('ak_sen',$('sen').value); }catch(e){} });
senUI();
$('hat').value=HATTIP; $('hat').addEventListener('change',()=>{ const v=$('hat').value; if(v==='robot') location.href='../sim3d/'; else if(v==='karsilastir') location.href='../karsilastir/'; else location.search='?hat='+v; });   // üç hat aynı seçicide: robotlu hat ayrı sayfa (tepsili akış + 2 robot)
(function(){ const sc=$('scrub'); let bekleyen=null, calisiyordu=false;
  const git=()=>{ if(bekleyen===null) return; const T=bekleyen; bekleyen=null; if(PLAN) zamanaGit(PLAN,T); };
  sc.addEventListener('pointerdown',()=>{ sc._tut=true; calisiyordu=!!anim; dur(); });
  sc.addEventListener('input',()=>{ const ilk=bekleyen===null; bekleyen=+sc.value; if(ilk) requestAnimationFrame(git); });
  const birak=()=>{ if(!sc._tut) return; sc._tut=false; if(calisiyordu&&PLAN) oynat(PLAN); };
  sc.addEventListener('pointerup',birak); sc.addEventListener('change',birak);
  $('gantt').addEventListener('click',e=>{ if(!GX||!PLAN) return; const r=$('gantt').getBoundingClientRect(), T=(e.clientX-r.left-70)/(GX.W-90)*GX.T1; const c=!!anim; dur(); zamanaGit(PLAN,T); if(c) oynat(PLAN); }); })();
planlaUI();
