/* ================================================================
   AUTOKITCH · OPTİMUM HAT · MOTOR
   Robot çekmeceden hamuru alır → tabla (Atosa tipi) basar + dozajlar → tek sıra konveyör fırın
   → kesme plakası → sipariş kutusu (aynı siparişin lahmacunları aynı kutuda) → robot kutuyu ve
   içeceği QR dolabına koyar. Varsayılan: hazne 1000 mm (3,2 göz), pişme 210 sn, akıllı robot sırası.
   Süreler sn · hat yerleşimi cm · topping ve fırın içi mm.
   ================================================================ */
const T0 = { takeDough:8, pressDrop:6, boxTake:5, lockerPlace:8, drinkTake:6, drinkPlace:5, customerPickup:150 };

const CFG = { lahm:true, chamber:1000, extra:100, bake:210, pitch:310, pressCycle:4,
  dose:20, sucBack:1.5, vX:500, zMove:1, stripDown:1, push:1.2, atosaTur:60, onceden:true, akilli:true,
  cutPide:15, cutLahm:5, fold:15, lid:3, siparisKutu:true, lahmKutu:3,
  rail:50, robotK:1, drinkPct:50, seed:1, gapSec:90, randArr:true, lockers:12,
  scenario:'tek3', hedefDk:25, lahmPct:65 };

/* STORE tam 3 gün (çekmece v2): pide 12 × 20 · lahmacun 18 × 35 · içecek 4 × 56 · kutu şarjörü 506 blank */
const STOK = { pide:240, lahm:600, icecek:210, kutu:506 };
const KOLON = [ {ad:'K1 PİDE', tur:'pide', n:6}, {ad:'K2 PİDE', tur:'pide', n:6}, {ad:'K3 LAHM', tur:'lahm', n:9},
                {ad:'K4 LAHM', tur:'lahm', n:9}, {ad:'K5 İÇECEK', tur:'drink', n:4} ];

/* YERLEŞİM (mm, hat başından): PRESS 0–700 · TOPPING 700–1700 · FIRIN 1700–
   P pres ekseni · K 6 kaset ağzı (adım 150) · XN fırın bandı burnu · F tabla fırın ağzında
   TR tabla yarıçapı 170 (Ø340: ürün Ø300 + itici payı) */
const G = { P:350, K:[770, 920, 1070, 1220, 1370, 1520], XN:1640, F:1470, TR:170 };
const KASET = [{ad:'KAŞAR', kisa:'KŞR', renk:'#f2e2a0'}, {ad:'SUCUK', kisa:'SCK', renk:'#8f2f1f'}, {ad:'HARÇ', kisa:'HRÇ', renk:'#b23a2a'},
               {ad:'HARÇ', kisa:'HRÇ', renk:'#b23a2a'}, {ad:'KIYMA', kisa:'KIY', renk:'#9a4a30'}, {ad:'KUŞBAŞI', kisa:'KUŞ', renk:'#7a3b22'}];
/* pide çeşidi (gramaj araştırması, ekonomik Ø30) — menü karışımı belli değil: 4 çeşit eşit */
const PIDE_TUR = [{ad:'kaşarlı', mal:[[0,130]]}, {ad:'sucuklu', mal:[[0,90],[1,70]]}, {ad:'kıymalı', mal:[[4,160]]}, {ad:'kuşbaşılı', mal:[[5,145]]}];

/* ---------- senaryolar (tabla–bant simiyle aynı talep modeli) ---------- */
function rng(seed){ return function(){ seed|=0; seed=seed+0x6D2B79F5|0; let t=Math.imul(seed^seed>>>15,1|seed);
  t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
function mkItems(rnd, cfg){
  if(cfg.lahm && rnd() < cfg.lahmPct/100){ const it=['lahm','lahm']; if(rnd()<0.15) it.push('lahm'); return it; }
  const r=rnd(), n = r<0.65?1 : r<0.90?2 : 3, it=[]; for(let i=0;i<n;i++) it.push('pide'); return it;
}
const AKSAM_EGRI=[0.28, 0.42, 0.30];
const SEN={ tek3:{}, uc:{}, aksam:{saat:17, n:53, egri:AKSAM_EGRI}, cmt:{saat:17, n:74, egri:AKSAM_EGRI}, surekli:{saat:18}, bos:{} };
function scenarioOrders(cfg){
  const o=[], rnd=rng((cfg.seed||1)*7919+13);
  switch(cfg.scenario){
    case 'tek3': o.push({arr:0, items:['lahm','lahm','lahm'], drink:true}); break;
    case 'uc':   o.push({arr:0, items:['lahm','lahm','lahm'], drink:true}, {arr:30, items:['pide','pide'], drink:false}, {arr:60, items:['lahm','lahm'], drink:true}); break;
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
/* ---------- hat yerleşimi (cm) ---------- */
function ovenW(c){ return Math.round((c.chamber+c.extra)/10); }
function layout(c){
  const S=[]; let x=0; const add=(id,w,label)=>{ S.push({id,x0:x,w,cx:x+w/2,label}); x+=w; };
  add('PRESS',70,'PRESS'); add('TOPPING',100,'TOPPING'); add('OVEN',ovenW(c),'FIRIN'); add('KESME',60,'KESME'); add('PACK',70,'KUTU'); x+=20; add('PICKUP',124,'QR DOLABI');
  const m={}; S.forEach(s=>m[s.id]=s); m._all=S; m._len=x; m._storeEnd=m.KESME.x0+m.KESME.w; return m;
}

/* =================================================================
   MOTOR
   ================================================================= */
class Sim{
  constructor(cfg, orders){
    this.cfg=JSON.parse(JSON.stringify(cfg)); this.T={...T0};
    const c=this.cfg; this.L=layout(c);
    this.t=0; this.endT=null; this.log=[]; this.orders=[]; this.products=[]; this.nextPid=1; this.injN=0; this.entries=0;
    this.pendingOrders=orders.map((o,i)=>({id:i+1, arr:o.arr, items:o.items.slice(), drink:o.drink}));
    this.lane={bake:c.bake, v:c.chamber/c.bake, Ltot:c.chamber+c.extra, items:[], free:0};
    this.press={working:false};
    this.tray={x:G.P, z:'seyir', state:'bekliyor', p:null, reserved:null, steps:[], step:null, left:0, gram:0, label:'', dosing:null, strip:0, pushT0:0, waitFrom:null, cycleStart:0, turEnd:0, cycles:[]};
    this.plate={p:null, end:0, queue:[]};
    this.pack={ready:1, folding:false, end:0, open:null, closing:false, lidEnd:0, boxed:[]};
    this.lockers=[]; for(let i=0;i<c.lockers;i++) this.lockers.push({p:null, free:0, n:0});
    this.robot={x:35, carry:null, steps:[], step:null, left:0, ty:150, label:'', job:null};
    const cw=(this.L._storeEnd-4)/5; this.storeCol=(i)=>2+cw*i+cw/2; this.storeOpen=null;
    this.stock={pide:STOK.pide, lahm:c.lahm?STOK.lahm:0, icecek:STOK.icecek, kutu:STOK.kutu-1};
    /* doluluk sayaçları (sn) */
    this.u={tabla:{calisir:0, birakma:0, firin:0, hamur:0}, robot:{kol:0, yol:0, bekle:0, bos:0}, firinDolu:0, kesme:0, katlama:0, kapak:0};
    this.done=false; this.deliveredUnits=0; this.delivered={pide:0, lahm:0, drink:0}; this.boxesUsed=0;
  }
  say(s){ this.log.push({t:this.t, s}); if(this.log.length>300) this.log.shift(); }
  fmt(s){ s=Math.max(0,Math.round(s)); return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0'); }
  saat(t){ const S=SEN[this.cfg.scenario]; if(!S||S.saat===undefined) return null;
    const x=S.saat*3600+Math.max(0,t), h=Math.floor(x/3600)%24, m=Math.floor(x/60)%60;
    return String(h).padStart(2,'0')+':'+String(m).padStart(2,'0'); }
  tuket(kind){ const S=this.stock;
    if(kind==='lahm'){ if(S.lahm>0) S.lahm--; else this.say('<b>LAHMACUN HAMURU YOK</b>'); return; }
    if(S.pide>0) S.pide--; else this.say('<b>PİDE HAMURU YOK</b>'); }

  /* --- sipariş --- */
  releaseOrders(){ while(this.pendingOrders.length && this.pendingOrders[0].arr<=this.t+1e-9){ const o=this.pendingOrders.shift(); this.addOrder(o.items, o.arr, o.id, o.drink); } }
  addOrder(items, arr, id, drink){
    const c=this.cfg, ord={id:id||(900+(++this.injN)), arr, items:items.slice(), products:[], doneT:null, drink:null, drinkDone:false, drinkBusy:false, lahmToplam:0, lahmKutulanan:0};
    const icecek = (drink===true||drink===false) ? drink : (c.drinkPct>0 && ((ord.id*37)%100) < c.drinkPct);
    if(icecek) ord.drink='kutu';
    /* pideler önce, lahmacunlar arka arkaya → fırından arka arkaya çıkar, aynı kutuya düşer */
    const sirali=items.map(k=>c.lahm?k:'pide').sort((a,b)=>(a==='pide'?0:1)-(b==='pide'?0:1));
    sirali.forEach((k,i)=>ord.products.push(this.mkProduct(k, ord, i)));
    ord.lahmToplam=ord.products.filter(q=>q.kind==='lahm').length;
    this.orders.push(ord); this.say(`<b>Sipariş #${ord.id}</b> geldi: ${this.itemsText(ord)}`);
    this.done=false; this.endT=null;
    return ord;
  }
  mkProduct(kind, ord, i){
    let tur, adim;
    if(kind==='lahm'){ tur='lahmacun'; adim=[{k:((ord.id+i)%2)?3:2, g:108}]; }          // harç 108 g · iki harç kaseti sırayla
    else { const P=PIDE_TUR[(ord.id*7+i*3)%4]; tur=P.ad; adim=P.mal.map(([k,g])=>({k,g})); }
    adim.sort((a,b)=>a.k-b.k);
    const p={id:this.nextPid++, kind, tur, adim, order:ord, state:'wait'}; this.products.push(p); return p;
  }
  kisa(o){ const p=o.products.filter(q=>q.kind==='pide').length, l=o.products.filter(q=>q.kind==='lahm').length;
    return [p?p+'P':'', l?l+'L':'', o.drink?'İ':''].filter(Boolean).join('+'); }
  itemsText(o){ const pp=o.products.filter(q=>q.kind==='pide').map(q=>q.tur), l=o.products.filter(q=>q.kind==='lahm').length;
    return [pp.length?`${pp.length} pide (${pp.join(', ')})`:'', l?`${l} lahmacun`:'', o.drink?'içecek':''].filter(Boolean).join(' + '); }
  checkOrder(o){
    if(o.doneT!==null) return;
    if(o.products.every(q=>q.state==='done') && (!o.drink || o.drinkDone)){
      o.doneT=this.t; this.say(`<b>Sipariş #${o.id} TESLİM</b> — ${this.fmt(o.doneT-o.arr)} bekledi`);
      this.lockers.forEach(l=>{ if(l.p && l.p.order===o) l.free=this.t+this.T.customerPickup; });
    }
  }
  /* STORE: hangi kolon, hangi çekmece (en üstteki dolu çekmeceden alır) */
  cekmece(kind){ const S=this.stock;
    if(kind==='drink') return {kol:4, sira:Math.max(0,Math.ceil(S.icecek/56)-1)};
    if(kind==='lahm') return S.lahm>285 ? {kol:2, sira:Math.max(0,Math.ceil((S.lahm-285)/35)-1)} : {kol:3, sira:Math.max(0,Math.ceil(S.lahm/35)-1)};
    return S.pide>120 ? {kol:0, sira:Math.max(0,Math.ceil((S.pide-120)/20)-1)} : {kol:1, sira:Math.max(0,Math.ceil(S.pide/20)-1)};
  }
  kolonDolu(ci){ const S=this.stock;
    if(ci===0) return Math.ceil(Math.max(0,S.pide-120)/20); if(ci===1) return Math.ceil(Math.min(S.pide,120)/20);
    if(ci===2) return Math.ceil(Math.max(0,S.lahm-285)/35); if(ci===3) return Math.ceil(Math.min(S.lahm,285)/35);
    return Math.ceil(S.icecek/56); }
  cekmeceY(sira){ return 16+(sira+0.5)*(80/9); }
  lockerX(i){ const s=this.L.PICKUP, col=i%2; return s.x0+12+col*(s.w-24)/2+(s.w-24)/4; }
  lockerY(i){ const row=Math.floor(i/2), rows=Math.ceil(this.cfg.lockers/2); return 158-row*(118/rows)-(118/rows)/2; }
  lockerFor(o){ let li=this.lockers.findIndex(l=>l.p && l.p.order===o); if(li<0) li=this.lockers.findIndex(l=>!l.p); return li; }

  /* --- robot işleri --- */
  go(x, y, at){ return {go:true, x, y, at}; }
  act(dur, label, y, fn, startFn){ return {act:true, dur:dur*this.cfg.robotK, label, y, fn, startFn}; }
  nextStartable(){ for(const o of this.orders){ const p=o.products.find(q=>q.state==='wait'); if(p) return p; } return null; }
  canStart(){ const Tr=this.tray; return Tr.reserved===null && (this.cfg.onceden || Tr.state==='bekliyor' || Tr.state==='donus'); }
  pickJob(){
    const c=this.cfg;
    const boxed=this.pack.boxed.filter(b=>this.lockerFor(b.order)>=0).sort((a,b)=>a.closedT-b.closedT);
    const drinks=this.orders.filter(o=>o.drink && !o.drinkDone && !o.drinkBusy && o.products.some(q=>!['wait','starting','carry'].includes(q.state)) && this.lockerFor(o)>=0);
    const acil=drinks.find(o=>o.products.every(q=>q.state==='done'));
    const p=this.canStart()?this.nextStartable():null;
    if(!c.akilli){                                   // basit sıra: önce kutu, sonra hamur, sonra içecek
      if(boxed.length) return this.jobDeliver(boxed[0]);
      if(acil) return this.jobDrink(acil);
      if(p) return this.jobStart(p);
      if(drinks.length) return this.jobDrink(drinks[0]);
      return null;
    }
    /* AKILLI SIRA: tabla sonraki hamuru ne zaman isteyecek? kutu / içecek işi ancak hamur zamanında gelecekse yapılır */
    if(p){
      const T=this.T, R=this.robot, Tr=this.tray, k=c.robotK;
      const need = Tr.state==='calisiyor' ? Tr.turEnd : this.t;
      const ck=this.cekmece(p.kind), sx=this.storeCol(ck.kol), px=this.L.PRESS.cx, lx=this.L.PICKUP.x0+this.L.PICKUP.w/2;
      const fetch=(x)=>(Math.abs(x-sx)+Math.abs(sx-px))/c.rail + T.takeDough*k;
      if(boxed.length){ const kx=this.L.PACK.cx, dur=(Math.abs(R.x-kx)+Math.abs(kx-lx))/c.rail+(T.boxTake+T.lockerPlace)*k;
        if(this.t+dur+fetch(lx)+1<=need || boxed.length>=3) return this.jobDeliver(boxed[0]); }
      if(drinks.length){ const o=acil||drinks[0], dx=this.storeCol(this.cekmece('drink').kol), dur=(Math.abs(R.x-dx)+Math.abs(dx-lx))/c.rail+(T.drinkTake+T.drinkPlace)*k;
        if(this.t+dur+fetch(lx)+1<=need || acil) return this.jobDrink(o); }
      return this.jobStart(p);
    }
    if(boxed.length) return this.jobDeliver(boxed[0]);
    if(drinks.length) return this.jobDrink(acil||drinks[0]);
    return null;
  }
  jobStart(p){
    const T=this.T, S=[]; p.state='starting';
    const ck=this.cekmece(p.kind), y=this.cekmeceY(ck.sira);
    S.push(this.go(this.storeCol(ck.kol), y, 'STORE'),
      this.act(T.takeDough, `K${ck.kol+1} çekmecesi açık · hamur topunu KAVRA`, y, ()=>{ this.robot.carry={kind:p.kind, st:'dough'}; p.state='carry'; this.tuket(p.kind); this.storeOpen=null; }, ()=>{ this.storeOpen=ck; }));
    S.push(this.go(this.L.PRESS.cx, 150, 'PRESS'));
    this.tray.reserved=p;
    S.push({wait:true, y:150, label:'hamur elde · tabla pres altına dönüyor', cond:()=>this.tray.state==='bekliyor'});
    S.push(this.act(T.pressDrop, 'hamuru TABLAYA bırak (pres altı)', 150, ()=>{ this.robot.carry=null; this.trayLoad(p); }, ()=>{ this.tray.state='yukleniyor'; }));
    return {name:`HAMUR #${p.id} (${p.tur}) · sipariş #${p.order.id}`, steps:S, p};
  }
  jobDeliver(bx){
    const S=[], T=this.T, o=bx.order, li=this.lockerFor(o); if(li<0) return null;
    const Lk=this.lockers[li]; if(!Lk.p) Lk.p={order:o};
    this.pack.boxed=this.pack.boxed.filter(x=>x!==bx); bx.items.forEach(q=>q.state='delivering');
    const ne=`${bx.items.length} ${bx.kind==='pide'?'pide':'lahmacun'}`;
    S.push(this.go(this.L.PACK.cx, 140, 'KUTU'), this.act(T.boxTake, `kutuyu KAVRA (#${o.id} · ${ne})`, 140, ()=>{ this.robot.carry={kind:bx.kind, st:'box', oid:o.id, n:bx.items.length}; }));
    const lx=this.lockerX(li), ly=this.lockerY(li);
    S.push(this.go(lx, ly, 'QR DOLABI'), this.act(T.lockerPlace, `kutuyu göz ${li+1}'e koy`, ly, ()=>{
      this.robot.carry=null; Lk.n++;
      bx.items.forEach(q=>{ q.state='done'; q.doneT=this.t; this.deliveredUnits++; this.delivered[q.kind]++; });
      this.checkOrder(o); }));
    return {name:`KUTU #${o.id} (${ne}) → göz ${li+1}`, steps:S, bx};
  }
  jobDrink(o){
    const S=[], T=this.T, li=this.lockerFor(o); if(li<0) return null;
    const Lk=this.lockers[li]; if(!Lk.p) Lk.p={order:o};
    o.drinkBusy=true;
    const ck=this.cekmece('drink'), y=this.cekmeceY(ck.sira);
    S.push(this.go(this.storeCol(ck.kol), y, 'STORE'), this.act(T.drinkTake, 'K5 çekmecesinden içeceği KAVRA', y,
      ()=>{ const St=this.stock; if(St.icecek>0) St.icecek--; else this.say('<b>İÇECEK YOK</b>'); this.robot.carry={kind:'drink', st:'kutu'}; this.storeOpen=null; }, ()=>{ this.storeOpen=ck; }));
    const lx=this.lockerX(li), ly=this.lockerY(li);
    S.push(this.go(lx, ly, 'QR DOLABI'), this.act(T.drinkPlace, `içeceği göz ${li+1}'e koy`, ly, ()=>{
      this.robot.carry=null; o.drinkDone=true; o.drinkBusy=false; this.delivered.drink++; Lk.n++; this.checkOrder(o); }));
    return {name:`İÇECEK #${o.id} → göz ${li+1}`, steps:S, o};
  }

  /* --- TABLA: robot hamuru bırakınca tablanın tüm turu kurulur --- */
  tact(dur, label, fn, startFn){ return {act:true, dur, label, fn, startFn}; }
  trayLoad(p){
    const Tr=this.tray, c=this.cfg, S=[];
    /* ATOSA: ürün başına en az c.atosaTur sn (üretici: bir pizza en fazla 1 dk) — kısa kalan süre dozaja eklenir */
    let top=2*c.zMove+c.pressCycle, xx=G.P;
    for(const a of p.adim){ top+=Math.abs(G.K[a.k]-xx)/c.vX+2*c.zMove+c.dose+c.sucBack; xx=G.K[a.k]; }
    top+=Math.abs(G.F-xx)/c.vX+c.stripDown+c.push+Math.abs(G.F-G.P)/c.vX;
    const ek=Math.max(0,(c.atosaTur||0)-top), dz=c.dose+ek/p.adim.length;
    Tr.reserved=null; Tr.p=p; Tr.gram=0; Tr.state='calisiyor'; Tr.cycleStart=this.t; Tr.turEnd=this.t+top+ek; p.state='tabla';
    this.say(`Tabla: tartı hamuru gördü → #${p.id} ${p.tur}`);
    S.push(this.tact(c.zMove, 'örse iner', ()=>{ Tr.z='ors'; }, ()=>{ Tr.z='iniyor'; }));
    S.push(this.tact(c.pressCycle, 'PRES tablanın üstüne basıyor (kuvvet örste)', ()=>{ this.press.working=false; p.state='base'; this.say(`Pres: #${p.id} tablada basıldı`); }, ()=>{ this.press.working=true; }));
    S.push(this.tact(c.zMove, 'örsten kalkar', ()=>{ Tr.z='seyir'; }, ()=>{ Tr.z='kalkiyor'; }));
    for(const a of p.adim){
      const K=KASET[a.k];
      S.push({move:true, x:G.K[a.k], label:`→ K${a.k+1} ${K.ad} altına`});
      S.push(this.tact(c.zMove, `ağıza kalkar (K${a.k+1})`, ()=>{ Tr.z='agiz'; }, ()=>{ Tr.z='kalkiyor'; }));
      S.push(this.tact(dz, `DOZAJ ${K.ad} · döner + kayar`,
        ()=>{ Tr.gram+=a.g; Tr.dosing=null; this.say(`Tabla: K${a.k+1} ${K.ad} ${a.g} g ✓ · tartı ${Math.round(Tr.gram)} g`); },
        ()=>{ Tr.dosing={k:a.k, g:a.g, g0:Tr.gram, dur:dz}; }));
      S.push(this.tact(c.sucBack, 'helezon geri emer · klape kapanır'));
      S.push(this.tact(c.zMove, 'iner', ()=>{ Tr.z='seyir'; }, ()=>{ Tr.z='iniyor'; }));
    }
    S.push({move:true, x:G.F, label:'→ fırın ağzına', fn:()=>{ p.state='topped'; }});
    S.push({wait:true, label:'fırın sırası bekleniyor', cond:()=>this.t + c.stripDown + c.push >= this.lane.free - 1e-9,
      startFn:()=>{ Tr.waitFrom=this.t; },
      fn:()=>{ if(Tr.waitFrom!==null && this.t-Tr.waitFrom>=1) this.say(`Tabla: fırın sırası ${Math.round(this.t-Tr.waitFrom)} sn beklendi`); Tr.waitFrom=null; }});
    S.push(this.tact(c.stripDown, 'itici iner (ürünün arkasına)', null, ()=>{ Tr.strip=1; }));
    S.push(this.tact(c.push, 'itici ürünü fırın bandına iter',
      ()=>{ Tr.p=null; Tr.gram=0; this.laneEnter(p); this.say(`Tabla: #${p.id} fırın bandına geçti · tartı 0 g ✓`); },
      ()=>{ Tr.strip=2; Tr.pushT0=this.t; }));
    S.push({move:true, x:G.P, label:'← pres altına dönüş (boş)', startFn:()=>{ Tr.state='donus'; Tr.strip=0; }, fn:()=>{ Tr.cycles.push(this.t-Tr.cycleStart); }});
    S.push(this.tact(0, '', ()=>{ Tr.state='bekliyor'; Tr.label=''; }));
    Tr.steps=S;
  }
  stepTray(dt){
    const Tr=this.tray, c=this.cfg;
    if(Tr.step && Tr.step.wait) this.u.tabla.firin+=dt;
    else if(Tr.state==='bekliyor' && !Tr.step && !Tr.steps.length) this.u.tabla.hamur+=dt;
    else if(Tr.state==='yukleniyor') this.u.tabla.birakma+=dt;
    else this.u.tabla.calisir+=dt;
    let left=dt, guard=0;
    while(left>1e-9 && guard++<200){
      if(!Tr.step){
        if(!Tr.steps.length) break;
        Tr.step=Tr.steps.shift(); const s=Tr.step; Tr.label=s.label||''; if(s.act) Tr.left=s.dur; if(s.startFn) s.startFn();
      }
      const s=Tr.step;
      if(s.move){ const d=s.x-Tr.x, need=Math.abs(d)/c.vX;
        if(need<=left){ Tr.x=s.x; left-=need; Tr.step=null; if(s.fn) s.fn(); } else { Tr.x+=Math.sign(d)*c.vX*left; left=0; } }
      else if(s.wait){ if(s.cond()){ Tr.step=null; if(s.fn) s.fn(); } else left=0; }
      else { const use=Math.min(left, Tr.left); Tr.left-=use; left-=use; if(Tr.left<=1e-9){ Tr.step=null; if(s.fn) s.fn(); } }
    }
  }

  /* --- FIRIN (tek sıra, sürekli bant) --- */
  laneEnter(p){ const La=this.lane; La.items.push({p, x:0}); La.free=this.t+this.cfg.pitch/La.v; p.state='baking'; this.entries++;
    this.say(`${p.kind==='pide'?'Pide':'Lahmacun'} #${p.id} <b>fırına girdi</b>`); }

  /* --- KUTU: katlama · kutu ağzı · kapak --- */
  stepPack(dt){
    const c=this.cfg, Pk=this.pack, Pl=this.plate;
    if(Pk.folding){ this.u.katlama+=dt; if(this.t>=Pk.end){ Pk.folding=false; Pk.ready++; } }
    if(!Pk.folding && Pk.ready<1 && this.stock.kutu>0){ Pk.folding=true; Pk.end=this.t+c.fold; this.stock.kutu--; }
    if(Pk.closing){
      this.u.kapak+=dt;
      if(this.t>=Pk.lidEnd){ const b=Pk.open; Pk.closing=false; Pk.open=null; b.closedT=this.t; b.items.forEach(q=>q.state='boxed'); Pk.boxed.push(b);
        this.say(`Kutu #${b.order.id} kapandı · ${b.items.length} ${b.kind==='pide'?'pide':'lahmacun'} · robot alacak`); }
      return;
    }
    if(!(Pl.p && Pl.p.state==='boxWait')) return;
    const p=Pl.p, o=p.order, istif=c.siparisKutu && p.kind==='lahm';
    if(Pk.open && !(istif && Pk.open.order===o && Pk.open.kind==='lahm' && Pk.open.items.length<Pk.open.need)){
      Pk.closing=true; Pk.lidEnd=this.t+c.lid; return;              // açık kutu başka ürünün: önce kapanır (normalde olmaz)
    }
    if(!Pk.open){
      if(Pk.ready<1) return;
      Pk.ready--; this.boxesUsed++;
      Pk.open={order:o, kind:p.kind, items:[], need:istif?Math.min(c.lahmKutu, o.lahmToplam-o.lahmKutulanan):1};
    }
    Pl.p=null; p.state='inbox'; Pk.open.items.push(p); if(p.kind==='lahm') o.lahmKutulanan++;
    this.say(`#${p.id} kutuya düştü · kutu #${o.id} ${Pk.open.items.length}/${Pk.open.need}`);
    if(Pk.open.items.length>=Pk.open.need){ Pk.closing=true; Pk.lidEnd=this.t+c.lid; }
  }

  /* --- zaman adımı --- */
  step(dt){
    if(this.done){ this.t+=dt; return; }
    const c=this.cfg, R=this.robot;
    this.t+=dt; this.releaseOrders();
    // FIRIN: bant sürekli akar
    const La=this.lane, h0=c.extra/2, h1=h0+c.chamber;
    this.u.firinDolu+=dt*La.items.filter(it=>it.x>=h0 && it.x<=h1).length;
    for(const it of La.items) it.x+=La.v*dt;
    for(const it of La.items.filter(it=>it.x>=La.Ltot)){ La.items.splice(La.items.indexOf(it),1); it.p.state='exit'; this.plate.queue.push(it.p); }
    // TABLA
    this.stepTray(dt);
    // KESME PLAKASI
    const Pl=this.plate;
    if(Pl.p && Pl.p.state==='cutting') this.u.kesme+=dt;
    if(!Pl.p && Pl.queue.length){ const p=Pl.queue.shift(); Pl.p=p; p.state='cutting'; Pl.end=this.t+(p.kind==='pide'?c.cutPide:c.cutLahm); }
    if(Pl.p && Pl.p.state==='cutting' && this.t>=Pl.end) Pl.p.state='boxWait';
    // KUTU
    this.stepPack(dt);
    // müşteri QR ile alır
    for(const l of this.lockers) if(l.p && l.free && this.t>=l.free){ l.p=null; l.free=0; l.n=0; }
    // ROBOT
    let left=dt, guard=0;
    while(left>1e-9 && guard++<200){
      if(!R.step){
        if(R.steps.length){ R.step=R.steps.shift(); this.beginStep(R.step); }
        else { const j=this.pickJob(); if(!j || !j.steps.length){ R.label=''; this.u.robot.bos+=left; break; } R.job=j; R.steps=j.steps.slice(); this.say(`Robot: <b>${j.name}</b>`); continue; }
      }
      const s=R.step;
      if(s.go){ const d=s.x-R.x, need=Math.abs(d)/c.rail;
        if(need<=left){ R.x=s.x; this.u.robot.yol+=need; left-=need; R.step=null; } else { R.x+=Math.sign(d)*c.rail*left; this.u.robot.yol+=left; left=0; } }
      else if(s.wait){ if(s.cond()) R.step=null; else { this.u.robot.bekle+=left; left=0; } }
      else { const use=Math.min(left, R.left); R.left-=use; this.u.robot.kol+=use; left-=use; if(R.left<=1e-9){ if(s.fn) s.fn(); R.step=null; } }
    }
    if(!this.pendingOrders.length && this.orders.length && this.orders.every(o=>o.doneT!==null)){ this.done=true; this.endT=this.t; }
  }
  beginStep(s){ const R=this.robot;
    if(s.go){ R.ty=s.y; R.label='→ '+s.at; }
    else if(s.wait){ R.ty=s.y; R.label=s.label; }
    else { R.left=s.dur; R.ty=s.y; R.label=s.label; if(s.startFn) s.startFn(); } }

  metrics(){
    const done=this.orders.filter(o=>o.doneT!==null), w=done.map(o=>o.doneT-o.arr), span=Math.max(this.endT!==null?this.endT:this.t, 1);
    const srt=[...w].sort((a,b)=>a-b), H=this.cfg.hedefDk*60, ort=a=>a.length?a.reduce((x,y)=>x+y,0)/a.length:null;
    return { delivered:done.length, avg:ort(w), max:w.length?Math.max(...w):null,
      p95:w.length?srt[Math.min(srt.length-1, Math.floor(srt.length*0.95))]:null, asan:w.filter(x=>x>H).length,
      queue:this.orders.filter(o=>o.doneT===null).length, urun:{...this.delivered}, kutu:this.boxesUsed, span, tur:ort(this.tray.cycles) };
  }
  snapshot(){ return JSON.parse(JSON.stringify({t:this.t, u:this.u, urun:this.deliveredUnits, kutu:this.boxesUsed, giris:this.entries})); }
}

/* iki anlık görüntü arası doluluk (0–1) */
function doluluk(a, b, c){
  const sure=b.t-a.t, d=(g,k)=>(b.u[g][k]-a.u[g][k])/sure;
  return { sure, urun:b.urun-a.urun, kutu:b.kutu-a.kutu, giris:b.giris-a.giris,
    tabla:{calisir:d('tabla','calisir'), birakma:d('tabla','birakma'), firin:d('tabla','firin'), hamur:d('tabla','hamur')},
    robot:{kol:d('robot','kol'), yol:d('robot','yol'), bekle:d('robot','bekle'), bos:d('robot','bos')},
    firin:(b.u.firinDolu-a.u.firinDolu)/sure/(c.chamber/c.pitch), kesme:(b.u.kesme-a.u.kesme)/sure,
    katlama:(b.u.katlama-a.u.katlama)/sure, kapak:(b.u.kapak-a.u.kapak)/sure };
}
/* başsız koşu: senaryonun tamamı */
function headless(cfg, h){
  const s=new Sim(cfg, scenarioOrders(cfg)); if(!s.pendingOrders.length) return null;
  const dt=h||0.5; let g=0; while(!s.done && s.t<6*3600 && g++<80000) s.step(dt);
  return s;
}
/* HAT DOLU: sipariş 20 sn'de bir · ilk 60 dk ısınma (sayılmaz) · sonraki 60 dk ölçüm · 3 farklı akışın ortalaması */
function tamYuk(cfg, seeds){
  const R=[];
  for(const sd of (seeds||[1,2,3])){
    const cf=Object.assign(JSON.parse(JSON.stringify(cfg)),{scenario:'surekli', gapSec:20, seed:sd});
    const s=new Sim(cf, scenarioOrders(cf)), dt=0.25;
    while(s.t<3600-1e-9) s.step(dt);
    const a=s.snapshot();
    while(s.t<7200-1e-9) s.step(dt);
    R.push(doluluk(a, s.snapshot(), s.cfg));
  }
  const ort=f=>R.reduce((x,r)=>x+f(r),0)/R.length;
  return { n:R.length, urun:ort(r=>r.urun), kutu:ort(r=>r.kutu), giris:ort(r=>r.giris),
    tabla:{calisir:ort(r=>r.tabla.calisir), birakma:ort(r=>r.tabla.birakma), firin:ort(r=>r.tabla.firin), hamur:ort(r=>r.tabla.hamur)},
    robot:{kol:ort(r=>r.robot.kol), yol:ort(r=>r.robot.yol), bekle:ort(r=>r.robot.bekle), bos:ort(r=>r.robot.bos)},
    firin:ort(r=>r.firin), kesme:ort(r=>r.kesme), katlama:ort(r=>r.katlama), kapak:ort(r=>r.kapak) };
}
