/* ================================================================
   AUTOKITCH · TABLA – BANT karşılaştırma · ÇİZİM (ön görünüş, 1000 × 600 tuval)
   ================================================================ */
const COL={idle:'#2e2e33', edge:'#4a4a50', work:'#ff453a', done:'#30d158', txt:'#F5F5F7', dim:'#86868B', dough:'#e9d9a8', base:'#f3e6bf',
  baked:'#b5651d', lahm:'#c9392b', box:'#d9c7a3', bant:'#2997FF', firin:'#ff9f0a', amber:'#ffd60a'};
const FONT=getComputedStyle(document.body).fontFamily;
function rr(ctx,x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
function lbl(ctx,txt,x,y,size,color,align,bold){ ctx.font=`${bold?'600 ':''}${size||11}px ${FONT}`; ctx.fillStyle=color||COL.txt; ctx.textAlign=align||'center'; ctx.textBaseline='middle'; ctx.fillText(txt,x,y); }
function sbox(ctx,x,y,w,h,state,txt,sub){
  ctx.fillStyle = state==='work'?'rgba(255,69,58,.18)': state==='done'?'rgba(48,209,88,.18)':'#1a1a1d';
  rr(ctx,x,y,w,h,3); ctx.fill(); ctx.lineWidth=state==='idle'?1:2; ctx.strokeStyle=state==='work'?COL.work:state==='done'?COL.done:COL.edge; ctx.stroke();
  const n=(txt?1:0)+(sub?1:0), top=y+h/2-(n-1)*6;
  if(txt) lbl(ctx,txt,x+w/2,top,10,state==='work'?COL.work:state==='done'?COL.done:COL.dim);
  if(sub) lbl(ctx,sub,x+w/2,top+(txt?12:0),9,COL.dim);
}
function item(ctx,kind,st,x,y,s,oid){
  s=s||1; const r=(kind==='pide'?15:13)*s;
  if(st==='dough'){ ctx.fillStyle=COL.dough; ctx.beginPath(); ctx.arc(x,y-5*s,7*s,0,7); ctx.fill(); return; }
  if(kind==='drink'){ ctx.fillStyle='#d23b3b'; rr(ctx,x-4*s,y-12*s,8*s,12*s,2); ctx.fill(); return; }
  if(st==='box'){ ctx.fillStyle=COL.box; rr(ctx,x-r,y-8*s,2*r,12*s,2); ctx.fill(); if(oid) lbl(ctx,'#'+oid,x,y-2*s,8,'#3a3020'); return; }
  ctx.fillStyle = st==='base'?COL.base : (st==='baked'||st==='cut')?(kind==='pide'?COL.baked:'#8f2f1f') : (kind==='pide'?'#e3b95a':COL.lahm);
  ctx.beginPath(); ctx.ellipse(x,y,r,r*0.38,0,0,7); ctx.fill();
  if(st==='cut'){ ctx.strokeStyle='#3a2410'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(x-r,y); ctx.lineTo(x+r,y); ctx.stroke(); }
  ctx.strokeStyle='rgba(0,0,0,.35)'; ctx.lineWidth=1; ctx.beginPath(); ctx.ellipse(x,y,r,r*0.38,0,0,7); ctx.stroke();
}
function yagis(ctx,x,y0,y1,t,renk){ ctx.fillStyle=renk; const H=Math.max(4,y1-y0);
  for(let i=0;i<6;i++){ const yy=y0+((t*45+i*H/6)%H); ctx.beginPath(); ctx.arc(x+((i*7)%9)-4, yy, 1.8, 0, 7); ctx.fill(); } }

function drawSim(cv, sim){
  const ctx=cv.getContext('2d'), W=cv.width, H=cv.height, L=sim.L, c=sim.cfg, t=sim.t;
  const PX=(W-36)/L._len, X0=18, FLOOR=H-14, RAILY=208;
  const cmx=cm=>X0+cm*PX, cmy=cm=>FLOOR-cm*PX, mmx=mm=>cmx(mm/10), mmy=mm=>cmy(mm/10);
  ctx.fillStyle='#0b0b0c'; ctx.fillRect(0,0,W,H); ctx.fillStyle='#141416'; ctx.fillRect(0,FLOOR,W,H-FLOOR);
  const tabla=sim.mode==='tabla', Tr=sim.tray, B=sim.belt, La=sim.lane;

  /* ---- üst bilgi satırları ---- */
  const sa=sim.saat(t);
  lbl(ctx, sa?('saat '+sa):sim.fmt(t), 16, 20, 16, '#fff', 'left', true);
  lbl(ctx, sim.fmt(t)+(sim.done?'  ·  SENARYO BİTTİ ✓':''), 16, 40, 11, sim.done?COL.done:COL.dim, 'left');
  if(tabla){
    const act=Tr.step&&Tr.step.act&&Tr.left>0.05, bek=Tr.waitFrom!==null;
    let g=Tr.gram; if(Tr.dosing && Tr.step && Tr.step.act){ g=Tr.dosing.g0+Tr.dosing.g*(1-Tr.left/Tr.dosing.dur); }
    const d = Tr.state==='bekliyor' ? 'pres altında hazır · boş' : (Tr.label||'') + (act?` · ${Math.ceil(Tr.left)} sn`:'') + (bek?` · ${Math.round(t-Tr.waitFrom)} sn`:'');
    lbl(ctx, `TABLA · ${d}`, 16, 64, 12, Tr.state==='bekliyor'?COL.dim:COL.amber, 'left', true);
    lbl(ctx, `tartı ${Math.round(g)} g${Tr.p?' · #'+Tr.p.id+' '+Tr.p.tur:''}${Tr.cycles.length?' · son tur '+Math.round(Tr.cycles[Tr.cycles.length-1])+' sn':''}`, 16, 82, 10, COL.dim, 'left');
  } else {
    const d = B.stopped ? `DURDU · fırın sırası ${Math.round(t-B.stopSince)} sn` : (B.items.length?`akıyor · ${B.v.toFixed(1)} mm/sn`:'boş');
    lbl(ctx, `BANT · ${d} · bantta ${B.items.length} ürün`, 16, 64, 12, B.stopped?COL.work:(B.items.length?COL.amber:COL.dim), 'left', true);
    lbl(ctx, `ürün bantta ${Math.round((G.XOUT-G.XIN)/B.v)} sn akar (${G.XOUT-G.XIN} mm)${B.transits.length?' · son geçiş '+Math.round(B.transits[B.transits.length-1])+' sn':''}`, 16, 82, 10, COL.dim, 'left');
  }
  const capIn=c.chamber/c.pitch, inCh=La.items.filter(it=>it.x>=c.extra/2 && it.x<=c.extra/2+c.chamber).length, sir=Math.max(0, La.free-t);
  lbl(ctx, `FIRIN · haznede ${inCh}/${capIn.toFixed(1)} · ${La.bake} sn · ${La.v.toFixed(2)} mm/sn · sonraki giriş ${sir>0?Math.ceil(sir)+' sn sonra':'hazır'}`, 16, 102, 11, COL.firin, 'left');
  const S=sim.stock;
  lbl(ctx, `STOK · pide ${S.taze}/${S.taze0} · lahmacun ${S.lahm}/${S.lahm0} · içecek ${S.kutu}/${S.kutu0}`, 16, 120, 10, COL.dim, 'left');

  /* ---- robot rayı + kabinler ---- */
  ctx.fillStyle='#3a3a40'; ctx.fillRect(cmx(-4), RAILY-3, cmx(L._len+4)-cmx(-4), 6);
  lbl(ctx, `ROBOT RAYI · ${c.rail} cm/sn`, W-16, RAILY-14, 9, COL.dim, 'right');
  for(const s of L._all){ const x=cmx(s.x0), w=s.w*PX, top=cmy(197);
    ctx.fillStyle='#1c1c1f'; rr(ctx,x+1,top,w-2,197*PX,4); ctx.fill(); ctx.strokeStyle='#3a3a3e'; ctx.lineWidth=1; ctx.stroke();
    lbl(ctx, s.label, x+w/2, top-9, 10, '#c9c9ce'); }

  /* ---- STORE (hattın altında, 5 kolon) ---- */
  { const x0=cmx(2), x1=cmx(L._storeEnd-2), cw=(x1-x0)/5, yAlt=cmy(16), yUst=cmy(96), ac=sim.storeOpen, dh=(yAlt-yUst)/7;
    const KOL=[{ad:'K1 PİDE',n:6,dolu:Math.ceil(Math.max(0,S.taze-120)/20),r:COL.dough},{ad:'K2 PİDE',n:7,dolu:Math.ceil(Math.min(S.taze,120)/20)+1,r:COL.dough},
      {ad:'K3 LAHM',n:5,dolu:Math.ceil(Math.max(0,S.lahm-150)/30),r:COL.dough},{ad:'K4 LAHM',n:5,dolu:Math.ceil(Math.min(S.lahm,150)/30),r:COL.dough},{ad:'K5 İÇECEK',n:5,dolu:Math.ceil(S.kutu/56),r:'#d23b3b'}];
    KOL.forEach((k,ci)=>{ const kx=x0+ci*cw; lbl(ctx,k.ad,kx+cw/2,yAlt+7,8,COL.dim);
      for(let i=0;i<k.n;i++){ const yy=yAlt-(i+1)*dh, on=i<k.dolu, acik=ac&&ac.kol===ci&&ac.sira===i;
        ctx.fillStyle=acik?'rgba(41,151,255,.35)':on?'#232327':'#171717'; ctx.fillRect(kx+2,yy+1,cw-4,dh-2);
        ctx.strokeStyle=acik?COL.bant:on?'#4a4a50':'#2a2a2e'; ctx.lineWidth=acik?2:1; ctx.strokeRect(kx+2,yy+1,cw-4,dh-2);
        if(on){ ctx.fillStyle=k.r; for(let j=0;j<3;j++){ ctx.beginPath(); ctx.arc(kx+10+j*((cw-20)/2), yy+dh/2, 1.8, 0, 7); ctx.fill(); } } } }); }

  /* ---- TOPPING: kasetler (depo + dozaj) ---- */
  const KW=14*PX, yK0=cmy(166), yK1=cmy(147), yD0=cmy(188), yD1=cmy(170), aktif=new Set(tabla?(Tr.dosing?[Tr.dosing.k]:[]):B.active);
  G.K.forEach((k,i)=>{ const x=mmx(k)-KW/2;
    ctx.fillStyle='#202024'; ctx.fillRect(x,yD0,KW,yD1-yD0); ctx.strokeStyle='#34343a'; ctx.strokeRect(x,yD0,KW,yD1-yD0);
    ctx.fillStyle=aktif.has(i)?'rgba(255,69,58,.22)':'#2a2a30'; ctx.fillRect(x,yK0,KW,yK1-yK0); ctx.strokeStyle=aktif.has(i)?COL.work:'#4a4a50'; ctx.strokeRect(x,yK0,KW,yK1-yK0);
    lbl(ctx,KASET[i].kisa,mmx(k),(yK0+yK1)/2,8,aktif.has(i)?'#fff':'#c9c9ce');
    ctx.fillStyle=aktif.has(i)?COL.work:'#55555c'; ctx.fillRect(mmx(k)-3,yK1,6,3); });

  if(tabla){
    /* PRES: tabla modunda alt tablasız pres + örs */
    const pxP=mmx(G.P), plY=sim.press.working?cmy(131):cmy(148);
    ctx.fillStyle='#2a2a30'; ctx.fillRect(pxP-22*PX,cmy(190),44*PX,cmy(160)-cmy(190)); lbl(ctx,'PRES',pxP,cmy(175),9,sim.press.working?COL.work:COL.dim);
    ctx.fillStyle='#55555c'; ctx.fillRect(pxP-2,cmy(160),4,plY-cmy(160)); ctx.fillStyle=sim.press.working?COL.work:'#77777e'; ctx.fillRect(pxP-18*PX,plY,36*PX,4);
    ctx.fillStyle='#3a3a40'; ctx.fillRect(pxP-16*PX,cmy(123),32*PX,cmy(113)-cmy(123)); lbl(ctx,'ÖRS',pxP,cmy(118),8,COL.dim);
    /* kızak rayı + damlama tavası + fırın bandı burnu */
    ctx.fillStyle='#34343a'; ctx.fillRect(mmx(150),cmy(110),mmx(1660)-mmx(150),4);
    ctx.fillStyle='#26262a'; ctx.fillRect(mmx(150),cmy(104),mmx(1660)-mmx(150),3);
    ctx.fillStyle=COL.firin; ctx.fillRect(mmx(G.XN),cmy(130),mmx(1700)-mmx(G.XN),3);
    /* tabla */
    let tx=Tr.x; const dosAct=Tr.dosing && Tr.step && Tr.step.act;
    if(dosAct){ const fr=1-Tr.left/Tr.dosing.dur; tx=Tr.x-150*fr; }
    const zY={seyir:128, agiz:141, ors:124, iniyor:126, kalkiyor:134}[Tr.z]||128, ty=cmy(zY), tw=34*PX;
    ctx.fillStyle='#55555c'; ctx.fillRect(mmx(tx)-2,ty+3,4,cmy(110)-ty-3); ctx.fillStyle='#3a3a40'; ctx.fillRect(mmx(tx)-9,cmy(112),18,6);
    ctx.fillStyle=Tr.state==='bekliyor'?'#d9d9de':'#f0f0f3'; ctx.fillRect(mmx(tx)-tw/2,ty,tw,3);
    if(Tr.p){
      let px=mmx(tx), st=Tr.p.state==='tabla'?'dough':(Tr.p.state==='base'?'base':'topped');
      if(Tr.strip===2 && Tr.step && Tr.step.act){ const fr=Math.min(1,(t-Tr.pushT0)/Math.max(0.1,c.push)); px=mmx(Tr.x+(G.XN+150-Tr.x)*fr); }
      item(ctx,Tr.p.kind,st==='topped'&&Tr.p.kind==='pide'?'base':st,px,ty-3,0.8);
      if(Tr.p.kind==='pide' && Tr.p.adim.length && (Tr.gram>0||dosAct)){ ctx.fillStyle='#b23a2a'; for(let i=0;i<4;i++){ ctx.beginPath(); ctx.arc(px-9+i*6,ty-3,1.6,0,7); ctx.fill(); } }
      if(dosAct){ const ang=t*2.2; ctx.strokeStyle='#fff'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(px,ty-3); ctx.lineTo(px+Math.cos(ang)*10,ty-3+Math.sin(ang)*4); ctx.stroke();
        yagis(ctx,mmx(G.K[Tr.dosing.k]),yK1+3,ty-8,t,KASET[Tr.dosing.k].renk); }
    }
    if(Tr.strip){ const bx=Tr.strip===2&&Tr.step&&Tr.step.act ? mmx(Tr.x-G.TR+(G.XN+150-Tr.x)*Math.min(1,(t-Tr.pushT0)/Math.max(0.1,c.push))) : mmx(Tr.x-G.TR-10);
      ctx.fillStyle=COL.amber; ctx.fillRect(bx-2,ty-16,4,14); lbl(ctx,'itici',bx,ty-22,8,COL.amber); }
  } else {
    /* PRES → aktarım */
    const P=sim.press, px0=cmx(L.PRESS.x0), pw=L.PRESS.w*PX;
    const st=P.p?(P.stage==='basiyor'?'work':'done'):'idle';
    sbox(ctx,px0+5,cmy(190),pw-10,cmy(152)-cmy(190),st, P.stage==='basiyor'?`PRES ${Math.ceil(P.end-t)} sn`:P.stage==='aktarim'?`AKTARIM ${Math.ceil(P.end-t)} sn`:P.stage==='giris'?'BANT GİRİŞİ BEKLİYOR':'PRES', P.p?'#'+P.p.id:'');
    ctx.fillStyle='#55555c'; ctx.fillRect(mmx(200),cmy(130),mmx(520)-mmx(200),3);
    if(P.p){ let x=mmx(G.P); if(P.stage==='aktarim') x=mmx(G.P+(G.XIN-G.P)*(1-Math.max(0,P.end-t)/Math.max(0.1,c.toBelt))); if(P.stage==='giris') x=mmx(G.XIN);
      item(ctx,P.p.kind,P.stage==='basiyor'?'dough':'base',x,cmy(131)-3,0.8); }
    /* bant + başlıklar */
    ctx.fillStyle=B.stopped?'rgba(255,69,58,.6)':COL.bant; ctx.fillRect(mmx(G.XIN-150),cmy(130),mmx(1700)-mmx(G.XIN-150),4);
    G.K.forEach((k,i)=>{ const on=aktif.has(i); ctx.fillStyle=on?'rgba(255,69,58,.5)':'#1f2a33'; ctx.fillRect(mmx(k)-KW/2,cmy(145),KW,cmy(139)-cmy(145)); ctx.strokeStyle=on?COL.work:'#2f4050'; ctx.strokeRect(mmx(k)-KW/2,cmy(145),KW,cmy(139)-cmy(145)); });
    for(const it of B.items){ const x=mmx(it.X), y=cmy(131)-3;
      item(ctx,it.p.kind,'base',x,y,0.8);
      if(it.gram>0){ ctx.fillStyle='#b23a2a'; for(let i=0;i<4;i++){ ctx.beginPath(); ctx.arc(x-9+i*6,y,1.6,0,7); ctx.fill(); } }
      for(const a of it.p.adim){ const k=G.K[a.k]; if(!B.stopped && Math.abs(it.X-k)<=G.WIN/2 && !it.doneK[a.k]) yagis(ctx,mmx(k),cmy(139),y-6,t,KASET[a.k].renk); } }
  }

  /* ---- FIRIN ---- */
  { const x0=mmx(1700), x1=mmx(1700+La.Ltot), hz0=mmx(1700+c.extra/2), hz1=mmx(1700+c.extra/2+c.chamber);
    ctx.fillStyle='#19140f'; ctx.fillRect(x0,cmy(162),x1-x0,cmy(100)-cmy(162)); ctx.strokeStyle=COL.firin; ctx.lineWidth=1.5; ctx.strokeRect(x0,cmy(162),x1-x0,cmy(100)-cmy(162));
    ctx.fillStyle=inCh?'rgba(255,159,10,.14)':'rgba(255,159,10,.05)'; ctx.fillRect(hz0,cmy(156),hz1-hz0,cmy(106)-cmy(156));
    ctx.setLineDash([5,4]); ctx.strokeRect(hz0,cmy(156),hz1-hz0,cmy(106)-cmy(156)); ctx.setLineDash([]);
    ctx.fillStyle='#55555c'; ctx.fillRect(x0,cmy(130),x1-x0,3);
    lbl(ctx,`hazne ${c.chamber} · aynı anda ${capIn.toFixed(1)} ürün`,(x0+x1)/2,cmy(151),9,COL.firin);
    for(const it of La.items){ const x=mmx(1700+it.x); if(x>x1) continue; item(ctx,it.p.kind,it.x>c.extra/2+c.chamber*0.7?'baked':'base',x,cmy(131)-3,0.75); }
    ctx.fillStyle='#202024'; ctx.fillRect(x0+4,cmy(190),x1-x0-8,cmy(168)-cmy(190)); lbl(ctx,'EGZOZ · filtre',(x0+x1)/2,cmy(179),9,COL.dim); }

  /* ---- KESME ---- */
  { const s=L.KESME, x=cmx(s.x0), w=s.w*PX, p=sim.plate.p; let st='idle', a='SPREY + KESİCİ', b='plaka';
    if(p){ if(p.state==='cutting'){ st='work'; a=`${p.kind==='pide'?'KESİM':'GEÇİŞ'} ${Math.ceil(sim.plate.end-t)} sn`; b='#'+p.id; } else { st='done'; a='KUTU BEKLİYOR'; b='#'+p.id; } }
    sbox(ctx,x+4,cmy(190),w-8,cmy(152)-cmy(190),st,a,b);
    ctx.fillStyle='#55555c'; ctx.fillRect(x+4,cmy(130),w-8,3);
    if(p) item(ctx,p.kind,p.state==='cutting'?'baked':'cut',x+w/2,cmy(131)-3,0.75);
    if(sim.plate.queue.length) lbl(ctx,`sırada ${sim.plate.queue.length}`,x+w/2,cmy(122),9,COL.work); }

  /* ---- PACK ---- */
  { const s=L.PACK, x=cmx(s.x0), w=s.w*PX, Pk=sim.pack;
    sbox(ctx,x+4,cmy(190),w-8,cmy(152)-cmy(190),Pk.folding?'work':'idle',Pk.folding?`KATLANIYOR ${Math.ceil(Pk.end-t)} sn`:(Pk.ready?'KUTU HAZIR ✓':'KUTU YOK'),'şarjör');
    if(Pk.boxed.length){ sbox(ctx,x+4,cmy(148),w-8,cmy(118)-cmy(148),'done',`KUTUDA ×${Pk.boxed.length}`,'robot alacak');
      Pk.boxed.slice(0,3).forEach((p,i)=>item(ctx,p.kind,'box',x+w/2-14+i*14,cmy(108),0.5,p.order.id)); } }

  /* ---- PICKUP ---- */
  { const s=L.PICKUP, rows=Math.ceil(c.lockers/2), lw=(s.w-24)/2*PX-4, lh=118/rows*PX-4;
    for(let i=0;i<c.lockers;i++){ const lx=cmx(sim.lockerX(i)), ly=cmy(sim.lockerY(i)), l=sim.lockers[i];
      if(!l.p){ sbox(ctx,lx-lw/2,ly-lh/2,lw,lh,'idle',String(i+1),''); continue; }
      const o=l.p.order, tam=o.doneT!==null, dk=((tam?o.doneT:t)-o.arr)/60;
      sbox(ctx,lx-lw/2,ly-lh/2,lw,lh,l.pending?'work':'done',`#${o.id} ${sim.kisa(o)}`,`${tam?'':'~'}${dk.toFixed(1)} dk`); }
    lbl(ctx,'QR dolabı · göz = sipariş',cmx(s.x0+s.w/2),cmy(30),9,COL.dim); }

  /* ---- ROBOT ---- */
  { const R=sim.robot, rx=cmx(R.x), hy=cmy(R.ty||150);
    ctx.fillStyle='#d0d0d6'; rr(ctx,rx-18,RAILY-11,36,20,4); ctx.fill(); ctx.fillStyle=COL.bant; ctx.fillRect(rx-18,RAILY+7,36,3);
    const ex=rx+(hy-RAILY)*0.16, ey=RAILY+10+(hy-RAILY)*0.45;
    ctx.strokeStyle='#e6e6ea'; ctx.lineWidth=6; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(rx,RAILY+10); ctx.lineTo(ex,ey); ctx.lineTo(rx,hy-10); ctx.stroke();
    ctx.strokeStyle=COL.bant; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(rx-7,hy-4); ctx.lineTo(rx-8,hy+5); ctx.moveTo(rx+7,hy-4); ctx.lineTo(rx+8,hy+5); ctx.stroke();
    if(R.carry) item(ctx,R.carry.kind,R.carry.st,rx,hy+2,0.8,R.carry.oid);
    if(R.label){ const txt=R.step&&R.step.act?`${R.label} · ${Math.ceil(R.left)} sn`:R.label; ctx.font=`11px ${FONT}`; const tw=ctx.measureText(txt).width+16;
      const bx=Math.max(4,Math.min(W-tw-4,rx-tw/2)); ctx.fillStyle='rgba(0,0,0,.8)'; rr(ctx,bx,RAILY-40,tw,18,4); ctx.fill(); lbl(ctx,txt,bx+tw/2,RAILY-31,11,R.step&&R.step.act?COL.firin:'#fff'); }
    else if(!sim.done) lbl(ctx,'robot boşta',rx,RAILY-31,10,COL.dim); }
}
