/* ================================================================
   AUTOKITCH · TABLA – BANT karşılaştırma · MOTOR
   İki motor aynı saatle, aynı siparişlerle koşar.
   Süreler sn · hat yerleşimi cm · topping ve fırın içi mm.
   ================================================================ */
const T0 = { takeDough:8, pressDrop:6, boxTake:5, lockerPlace:8, drinkTake:6, drinkPlace:5, customerPickup:150 };

const CFG = { lahm:true, chamber:1400, extra:100, bakePide:240, bakeLahm:180, tekHiz:'pide', pitch:350, pressCycle:4,
  dose:20, sucBack:1.5, vX:500, zMove:1, stripDown:1, push:1.2, toBelt:5,
  cutPide:15, cutLahm:5, fold:15, rail:50, robotK:1, drinkPct:50, seed:1, gapSec:90, randArr:true, lockers:12,
  scenario:'cmt', hedefDk:25, lahmPct:65 };

/* YERLEŞİM (mm, hat başından): PRESS 0–700 · TOPPING 700–1700 · FIRIN 1700– (pafta v4)
   P    pres ekseni (tabla burada hamuru alır, pres tablanın üstüne basar)
   K    6 kaset ağzı, adım 150 (son kaset fırın duvarından 180 mm geride: Ø340 tabla çarpmasın)
   XN   fırın bandı burnu (topping bölmesine 60 mm taşar) · F tabla fırın ağzında (ön kenarı burna yanaşık)
   XIN  bantlı: presten banda aktarılan ürünün merkezi · XOUT bant sonu (fırın bandına geçiş)
   WIN  bantlı başlık penceresi = ürün çapı 300 (ürün başlığın altından tamamen geçerken dozaj alır)
   TR   tabla yarıçapı 170 (Ø340: pide Ø300 + itici payı) */
const G = { P:350, K:[770, 920, 1070, 1220, 1370, 1520], XN:1640, F:1470, XIN:610, XOUT:1680, WIN:300, TR:170 };
const KASET = [{ad:'KAŞAR', kisa:'KŞR', renk:'#f2e2a0'}, {ad:'SUCUK', kisa:'SCK', renk:'#8f2f1f'}, {ad:'HARÇ', kisa:'HRÇ', renk:'#b23a2a'},
               {ad:'HARÇ', kisa:'HRÇ', renk:'#b23a2a'}, {ad:'KIYMA', kisa:'KIY', renk:'#9a4a30'}, {ad:'KUŞBAŞI', kisa:'KUŞ', renk:'#7a3b22'}];
/* pide çeşidi (gramaj araştırması, ekonomik Ø30) — menü karışımı belli değil: 4 çeşit eşit */
const PIDE_TUR = [{ad:'kaşarlı', mal:[[0,130]]}, {ad:'sucuklu', mal:[[0,90],[1,70]]}, {ad:'kıymalı', mal:[[4,160]]}, {ad:'kuşbaşılı', mal:[[5,145]]}];

/* ---------- senaryolar (robotlu ve bantlı simle birebir aynı talep modeli) ---------- */
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
/* ---------- hat yerleşimi (cm) ---------- */
function ovenW(c){ return Math.round((c.chamber+c.extra)/10); }
function layout(c){
  const S=[]; let x=0; const add=(id,w,label)=>{ S.push({id,x0:x,w,cx:x+w/2,label}); x+=w; };
  add('PRESS',70,'PRESS'); add('TOPPING',100,'TOPPING'); add('OVEN',ovenW(c),'FIRIN'); add('KESME',60,'KESME'); add('PACK',70,'PACK'); x+=20; add('PICKUP',124,'PICKUP');
  const m={}; S.forEach(s=>m[s.id]=s); m._all=S; m._len=x; m._storeEnd=m.KESME.x0+m.KESME.w; return m;
}

/* =================================================================
   MOTOR · mode 'tabla' | 'bant'
   ================================================================= */
class Sim{
  constructor(cfg, orders, mode){
    this.mode=mode; this.cfg=JSON.parse(JSON.stringify(cfg)); this.T={...T0};
    const c=this.cfg; this.L=layout(c);
    this.t=0; this.endT=null; this.log=[]; this.orders=[]; this.products=[]; this.nextPid=1; this.injN=0;
    this.pendingOrders=orders.map((o,i)=>({id:i+1, arr:o.arr, items:o.items.slice()}));
    const bake=(c.tekHiz==='lahm'&&c.lahm)?c.bakeLahm:c.bakePide;
    this.lane={bake, v:c.chamber/bake, Ltot:c.chamber+c.extra, items:[], free:0, busy:0};
    this.press={p:null, stage:null, end:0, working:false};
    this.tray={x:G.P, z:'seyir', state:'bekliyor', p:null, reserved:null, steps:[], step:null, left:0, gram:0, label:'', dosing:null, strip:0, pushT0:0, waitFrom:null, cycleStart:0, cycles:[]};
    this.belt={v:G.WIN/c.dose, items:[], stopped:false, stopSince:null, active:[], transits:[]};
    this.plate={p:null, end:0, queue:[]};
    this.pack={ready:1, folding:false, end:0, boxed:[]};
    this.busy={press:0, tas:0, kesici:0, pack:0};
    this.lockers=[]; for(let i=0;i<c.lockers;i++) this.lockers.push({p:null, free:0});
    this.robot={x:35, carry:null, steps:[], step:null, left:0, ty:150, label:'', busy:0, job:null};
    const cw=(this.L._storeEnd-4)/5; this.storeCol=(i)=>2+cw*i+cw/2; this.storeOpen=null;
    /* STORE bant/tabla altında: K1–K2 pide 240 · K3–K4 lahmacun 300 · K5 içecek 280 */
    this.stock={taze:240, taze0:240, lahm:(c.lahm?300:0), lahm0:(c.lahm?300:0), kutu:280, kutu0:280};
    this.done=false; this.deliveredUnits=0; this.delivered={pide:0, lahm:0, drink:0};
  }
  say(s){ this.log.push({t:this.t, s}); if(this.log.length>300) this.log.shift(); }
  fmt(s){ s=Math.max(0,Math.round(s)); return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0'); }
  saat(t){ const S=SEN[this.cfg.scenario]; if(!S||S.saat===undefined) return null;
    const x=S.saat*3600+Math.max(0,t), h=Math.floor(x/3600)%24, m=Math.floor(x/60)%60;
    return String(h).padStart(2,'0')+':'+String(m).padStart(2,'0'); }
  tuket(kind){ const S=this.stock;
    if(kind==='lahm'){ if(S.lahm>0) S.lahm--; else this.say('<b>LAHMACUN HAMURU YOK</b>'); return; }
    if(S.taze>0) S.taze--; else this.say('<b>PİDE HAMURU YOK</b>'); }

  /* --- sipariş --- */
  releaseOrders(){ while(this.pendingOrders.length && this.pendingOrders[0].arr<=this.t+1e-9){ const o=this.pendingOrders.shift(); this.addOrder(o.items, o.arr, o.id); } }
  addOrder(items, arr, id){
    const c=this.cfg, ord={id:id||(900+(++this.injN)), arr, items:items.slice(), products:[], doneT:null, drink:null, drinkDone:false, drinkBusy:false};
    if(c.drinkPct>0 && ((ord.id*37)%100) < c.drinkPct) ord.drink='kutu';
    items.forEach((k,i)=>ord.products.push(this.mkProduct(c.lahm?k:'pide', ord, i)));
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
  cekmece(kind){ const S=this.stock;
    if(kind==='drink') return {kol:4, sira:Math.max(0,Math.ceil(S.kutu/56)-1)};
    if(kind==='lahm') return S.lahm>150 ? {kol:2, sira:Math.max(0,Math.ceil((S.lahm-150)/30)-1)} : {kol:3, sira:Math.max(0,Math.ceil(S.lahm/30)-1)};
    return S.taze>120 ? {kol:0, sira:Math.max(0,Math.ceil((S.taze-120)/20)-1)} : {kol:1, sira:Math.max(0,Math.ceil(S.taze/20)-1)};
  }
  cekmeceY(sira){ return 22+sira*11; }
  lockerX(i){ const s=this.L.PICKUP, col=i%2; return s.x0+12+col*(s.w-24)/2+(s.w-24)/4; }
  lockerY(i){ const row=Math.floor(i/2), rows=Math.ceil(this.cfg.lockers/2); return 158-row*(118/rows)-(118/rows)/2; }

  /* --- robot işleri --- */
  go(x, y, at){ return {go:true, x, y, at}; }
  act(dur, label, y, fn, startFn){ return {act:true, dur:dur*this.cfg.robotK, label, y, fn, startFn}; }
  nextStartable(){ for(const o of this.orders){ const p=o.products.find(q=>q.state==='wait'); if(p) return p; } return null; }
  canStart(){
    if(this.mode==='tabla'){ const Tr=this.tray; return Tr.reserved===null && (Tr.state==='bekliyor' || Tr.state==='donus'); }
    return !this.press.p;
  }
  pickJob(){
    const cands=[];
    for(const p of this.pack.boxed) if(this.lockers.some(l=>!l.p || l.p.order===p.order)) cands.push({pri:0, t:p.boxedT, mk:()=>this.jobDeliver(p)});
    for(const o of this.orders) if(o.drink && !o.drinkDone && !o.drinkBusy && o.products.some(q=>!['wait','starting','carry'].includes(q.state)) && this.lockers.some(l=>!l.p || l.p.order===o)){
      const sadece=o.products.every(q=>q.state==='done'); cands.push({pri:sadece?0:5, t:o.arr, mk:()=>this.jobDrink(o)});
    }
    if(this.canStart()){ const p=this.nextStartable(); if(p) cands.push({pri:1, t:p.order.arr, mk:()=>this.jobStart(p)}); }
    if(!cands.length) return null;
    cands.sort((a,b)=>a.pri-b.pri || a.t-b.t);
    return cands[0].mk();
  }
  jobStart(p){
    const T=this.T, c=this.cfg, S=[]; p.state='starting';
    const ck=this.cekmece(p.kind), y=this.cekmeceY(ck.sira);
    S.push(this.go(this.storeCol(ck.kol), y, 'STORE'),
      this.act(T.takeDough, 'çekmeceden hamur topunu KAVRA', y, ()=>{ this.robot.carry={kind:p.kind, st:'dough'}; p.state='carry'; this.tuket(p.kind); this.storeOpen=null; }, ()=>{ this.storeOpen=ck; }));
    S.push(this.go(this.L.PRESS.cx, 150, 'PRESS'));
    if(this.mode==='tabla'){
      this.tray.reserved=p;
      S.push({wait:true, y:150, label:'tabla pres altına dönüyor', cond:()=>this.tray.state==='bekliyor'});
      S.push(this.act(T.pressDrop, 'hamuru TABLAYA bırak', 150, ()=>{ this.robot.carry=null; this.trayLoad(p); }, ()=>{ this.tray.state='yukleniyor'; }));
    } else {
      S.push(this.act(T.pressDrop, 'hamuru prese bırak', 150, ()=>{ this.robot.carry=null; const P=this.press; P.p=p; P.stage='basiyor'; P.working=true; P.end=this.t+c.pressCycle; p.state='pressing'; this.say(`Pres: #${p.id} basılıyor`); }));
    }
    return {name:`HAMUR #${p.id} (${p.tur})`, steps:S, p};
  }
  jobDeliver(p){
    const S=[], T=this.T;
    let li=this.lockers.findIndex(l=>l.p && l.p.order===p.order); if(li<0) li=this.lockers.findIndex(l=>!l.p); if(li<0) return null;
    const Lk=this.lockers[li]; if(!Lk.p || Lk.p.kind==='drink') Lk.p=p; Lk.pending=true; Lk.n=(Lk.n||0)+1;
    this.pack.boxed=this.pack.boxed.filter(x=>x!==p); p.state='delivering';
    S.push(this.go(this.L.PACK.cx, 140, 'PACK'), this.act(T.boxTake, 'kutuyu KAVRA', 140, ()=>{ this.robot.carry={kind:p.kind, st:'box', oid:p.order.id}; }));
    const lx=this.lockerX(li), ly=this.lockerY(li);
    S.push(this.go(lx, ly, 'PICKUP'), this.act(T.lockerPlace, `göz ${li+1}'e koy`, ly, ()=>{
      this.robot.carry=null; Lk.pending=false; p.state='done'; p.doneT=this.t; this.deliveredUnits++; this.delivered[p.kind]++; this.checkOrder(p.order); }));
    return {name:`KUTU #${p.id} → göz ${li+1}`, steps:S, p};
  }
  jobDrink(o){
    const S=[], T=this.T;
    let li=this.lockers.findIndex(l=>l.p && l.p.order===o); if(li<0) li=this.lockers.findIndex(l=>!l.p); if(li<0) return null;
    const Lk=this.lockers[li]; if(!Lk.p){ Lk.p={order:o, kind:'drink', state:'drinkslot'}; Lk.pending=true; }
    o.drinkBusy=true;
    const ck=this.cekmece('drink'), y=this.cekmeceY(ck.sira);
    S.push(this.go(this.storeCol(ck.kol), y, 'STORE'), this.act(T.drinkTake, 'K5 çekmecesinden içeceği KAVRA', y,
      ()=>{ const St=this.stock; if(St.kutu>0) St.kutu--; else this.say('<b>İÇECEK YOK</b>'); this.robot.carry={kind:'drink', st:'kutu'}; this.storeOpen=null; }, ()=>{ this.storeOpen=ck; }));
    const lx=this.lockerX(li), ly=this.lockerY(li);
    S.push(this.go(lx, ly, 'PICKUP'), this.act(T.drinkPlace, `içeceği göz ${li+1}'e koy`, ly, ()=>{
      this.robot.carry=null; o.drinkDone=true; o.drinkBusy=false; this.delivered.drink++; Lk.n=(Lk.n||0)+1;
      Lk.pending = (Lk.p.kind==='drink' && !o.products.some(q=>q.state==='done')); this.checkOrder(o); }));
    return {name:`İÇECEK #${o.id}`, steps:S, o};
  }

  /* --- TABLA: robot hamuru bırakınca tablanın tüm turu kurulur --- */
  tact(dur, label, fn, startFn){ return {act:true, dur, label, fn, startFn}; }
  trayLoad(p){
    const Tr=this.tray, c=this.cfg, S=[];
    Tr.reserved=null; Tr.p=p; Tr.gram=0; Tr.state='calisiyor'; Tr.cycleStart=this.t; p.state='tabla';
    this.say(`Tabla: tartı hamuru gördü → #${p.id} ${p.tur}`);
    S.push(this.tact(c.zMove, 'örse iner', ()=>{ Tr.z='ors'; }, ()=>{ Tr.z='iniyor'; }));
    S.push(this.tact(c.pressCycle, 'PRES tablanın üstüne basıyor (kuvvet örste)', ()=>{ this.press.working=false; p.state='base'; this.say(`Pres: #${p.id} tablada basıldı`); }, ()=>{ this.press.working=true; }));
    S.push(this.tact(c.zMove, 'örsten kalkar', ()=>{ Tr.z='seyir'; }, ()=>{ Tr.z='kalkiyor'; }));
    for(const a of p.adim){
      const K=KASET[a.k];
      S.push({move:true, x:G.K[a.k], label:`→ K${a.k+1} ${K.ad} altına`});
      S.push(this.tact(c.zMove, `ağıza kalkar (K${a.k+1})`, ()=>{ Tr.z='agiz'; }, ()=>{ Tr.z='kalkiyor'; }));
      S.push(this.tact(c.dose, `DOZAJ ${K.ad} · döner + kayar`,
        ()=>{ Tr.gram+=a.g; Tr.dosing=null; this.say(`Tabla: K${a.k+1} ${K.ad} ${a.g} g ✓ · tartı ${Math.round(Tr.gram)} g`); },
        ()=>{ Tr.dosing={k:a.k, g:a.g, g0:Tr.gram, dur:c.dose}; }));
      S.push(this.tact(c.sucBack, 'helezon geri emer · klape kapanır'));
      S.push(this.tact(c.zMove, 'iner', ()=>{ Tr.z='seyir'; }, ()=>{ Tr.z='iniyor'; }));
    }
    S.push({move:true, x:G.F, label:'→ fırın ağzına', fn:()=>{ p.state='topped'; }});
    S.push({wait:true, label:'fırın sırası bekleniyor', cond:()=>this.t + c.stripDown + c.push >= this.lane.free - 1e-9,
      startFn:()=>{ Tr.waitFrom=this.t; },
      fn:()=>{ if(Tr.waitFrom!==null && this.t-Tr.waitFrom>=1) this.say(`Tabla: fırın sırası ${Math.round(this.t-Tr.waitFrom)} sn beklendi`); Tr.waitFrom=null; }});
    S.push(this.tact(c.stripDown, 'itici iner (pidenin arkasına)', null, ()=>{ Tr.strip=1; }));
    S.push(this.tact(c.push, 'itici pideyi fırın bandına iter',
      ()=>{ Tr.p=null; Tr.gram=0; this.laneEnter(p); this.say(`Tabla: #${p.id} fırın bandına geçti · tartı 0 g ✓`); },
      ()=>{ Tr.strip=2; Tr.pushT0=this.t; }));
    S.push({move:true, x:G.P, label:'← pres altına dönüş (boş)', startFn:()=>{ Tr.state='donus'; Tr.strip=0; }, fn:()=>{ Tr.cycles.push(this.t-Tr.cycleStart); }});
    S.push(this.tact(0, '', ()=>{ Tr.state='bekliyor'; Tr.label=''; }));
    Tr.steps=S;
  }
  stepTray(dt){
    const Tr=this.tray, c=this.cfg;
    if(Tr.state!=='bekliyor') this.busy.tas+=dt;
    if(this.press.working) this.busy.press+=dt;
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

  /* --- BANT: pres → aktarım → sürekli bant → başlık altında dozaj → bant sonu fırın sırası --- */
  stepBelt(dt){
    const B=this.belt, c=this.cfg, P=this.press;
    if(P.p){ this.busy.press+=dt;
      if(P.stage==='basiyor' && this.t>=P.end){ P.stage='aktarim'; P.working=false; P.end=this.t+c.toBelt; P.p.state='transfer'; }
      if(P.stage==='aktarim' && this.t>=P.end){ P.stage='giris'; P.p.state='entryWait'; }
    }
    if(B.items.length) this.busy.tas+=dt;
    B.active=[];
    let stop=false; const front=B.items[0];
    if(front && front.X>=G.XOUT-1e-9){
      if(this.t>=this.lane.free-1e-9){
        B.items.shift(); B.transits.push(this.t-front.tIn);
        if(B.stopSince!==null){ if(this.t-B.stopSince>=1) this.say(`Bant: ${Math.round(this.t-B.stopSince)} sn durdu (fırın sırası)`); B.stopSince=null; }
        this.laneEnter(front.p);
      } else { stop=true; if(B.stopSince===null) B.stopSince=this.t; }
    }
    B.stopped=stop;
    if(!stop){
      const adv=B.v*dt;
      for(const it of B.items){
        const x0=it.X, x1=Math.min(G.XOUT, it.X+adv); it.X=x1;
        for(const a of it.p.adim){
          if(it.doneK[a.k]) continue;
          const k=G.K[a.k], w0=k-G.WIN/2, w1=k+G.WIN/2, ov=Math.min(x1,w1)-Math.max(x0,w0);
          if(ov>0){ it.gram+=a.g*ov/G.WIN; B.active.push(a.k); }
          if(x1>=w1-1e-9){ it.doneK[a.k]=true; this.say(`Bant: K${a.k+1} ${KASET[a.k].ad} → #${it.p.id} ${a.g} g ✓`); }
        }
        if(it.p.adim.every(a=>it.doneK[a.k])) it.p.state='topped';
      }
    }
    if(P.p && P.stage==='giris'){
      const last=B.items[B.items.length-1];
      if(!last || last.X-G.XIN>=c.pitch-1e-9){
        B.items.push({p:P.p, X:G.XIN, gram:0, doneK:{}, tIn:this.t}); P.p.state='belt';
        this.say(`Pres → bant: #${P.p.id} banda geçti`); P.p=null; P.stage=null;
      }
    }
  }

  /* --- FIRIN --- */
  laneEnter(p){ const La=this.lane; La.items.push({p, x:0}); La.free=this.t+this.cfg.pitch/La.v; p.state='baking';
    this.say(`${p.kind==='pide'?'Pide':'Lahmacun'} #${p.id} <b>fırına girdi</b>`); }

  /* --- zaman adımı --- */
  step(dt){
    if(this.done){ this.t+=dt; return; }
    const c=this.cfg, R=this.robot;
    this.t+=dt; this.releaseOrders();
    // FIRIN: bant sürekli akar; haznedeki ürün sayısı / kapasite = doluluk
    const La=this.lane, h0=c.extra/2, h1=h0+c.chamber;
    La.busy+=dt*Math.min(1, La.items.filter(it=>it.x>=h0 && it.x<=h1).length/(c.chamber/c.pitch));
    for(const it of La.items) it.x+=La.v*dt;
    for(const it of La.items.filter(it=>it.x>=La.Ltot)){ La.items.splice(La.items.indexOf(it),1); it.p.state='exit'; this.plate.queue.push(it.p); }
    // TOPPING
    if(this.mode==='tabla') this.stepTray(dt); else this.stepBelt(dt);
    // KESME PLAKASI
    const Pl=this.plate;
    if(Pl.p) this.busy.kesici+=dt;
    if(!Pl.p && Pl.queue.length){ const p=Pl.queue.shift(); Pl.p=p; p.state='cutting'; Pl.end=this.t+(p.kind==='pide'?c.cutPide:c.cutLahm); }
    if(Pl.p && Pl.p.state==='cutting' && this.t>=Pl.end) Pl.p.state='boxWait';
    if(Pl.p && Pl.p.state==='boxWait' && this.pack.ready>0){ const p=Pl.p; Pl.p=null; this.pack.ready--; p.state='boxed'; p.boxedT=this.t; this.pack.boxed.push(p); }
    // PACK: hep bir katlanmış kutu hazır
    const Pk=this.pack;
    if(Pk.folding) this.busy.pack+=dt;
    if(!Pk.folding && Pk.ready<1){ Pk.folding=true; Pk.end=this.t+c.fold; }
    if(Pk.folding && this.t>=Pk.end){ Pk.folding=false; Pk.ready++; }
    // müşteri alır
    for(const l of this.lockers) if(l.p && !l.pending && l.free && this.t>=l.free){ l.p=null; l.free=0; l.n=0; }
    // ROBOT
    let left=dt, guard=0;
    while(left>1e-9 && guard++<200){
      if(!R.step){
        if(R.steps.length){ R.step=R.steps.shift(); this.beginStep(R.step); }
        else { const j=this.pickJob(); if(!j || !j.steps.length){ R.label=''; break; } R.job=j; R.steps=j.steps.slice(); this.say(`Robot: <b>${j.name}</b>`); continue; }
      }
      const s=R.step;
      if(s.go){ const d=s.x-R.x, need=Math.abs(d)/c.rail;
        if(need<=left){ R.x=s.x; R.busy+=need; left-=need; R.step=null; } else { R.x+=Math.sign(d)*c.rail*left; R.busy+=left; left=0; } }
      else if(s.wait){ if(s.cond()) R.step=null; else { R.busy+=left; left=0; } }
      else { const use=Math.min(left, R.left); R.left-=use; R.busy+=use; left-=use; if(R.left<=1e-9){ if(s.fn) s.fn(); R.step=null; } }
    }
    if(!this.pendingOrders.length && this.orders.length && this.orders.every(o=>o.doneT!==null)){ this.done=true; this.endT=this.t; }
  }
  beginStep(s){ const R=this.robot;
    if(s.go){ R.ty=s.y; R.label='→ '+s.at; }
    else if(s.wait){ R.ty=s.y; R.label=s.label; }
    else { R.left=s.dur; R.ty=s.y; R.label=s.label; if(s.startFn) s.startFn(); } }

  metrics(){
    const done=this.orders.filter(o=>o.doneT!==null), w=done.map(o=>o.doneT-o.arr), span=Math.max(this.endT!==null?this.endT:this.t, 1);
    const srt=[...w].sort((a,b)=>a-b), H=this.cfg.hedefDk*60, cyc=this.tray.cycles, tr=this.belt.transits, ort=a=>a.length?a.reduce((x,y)=>x+y,0)/a.length:null;
    return { delivered:done.length, avg:ort(w), max:w.length?Math.max(...w):null,
      p95:w.length?srt[Math.min(srt.length-1, Math.floor(srt.length*0.95))]:null, asan:w.filter(x=>x>H).length,
      robot:this.robot.busy/span, oven:this.lane.busy/span, tas:this.busy.tas/span, press:this.busy.press/span,
      queue:this.orders.filter(o=>o.doneT===null).length, thr:this.deliveredUnits>0?this.deliveredUnits/(span/3600):null,
      urun:{...this.delivered}, span, tur: this.mode==='tabla' ? ort(cyc) : ort(tr) };
  }
}
/* başsız koşu */
function headless(cfg, mode, h){
  const s=new Sim(cfg, scenarioOrders(cfg), mode); if(!s.pendingOrders.length) return null;
  const dt=h||0.5; let g=0; while(!s.done && s.t<6*3600 && g++<80000) s.step(dt);
  return s.metrics();
}
