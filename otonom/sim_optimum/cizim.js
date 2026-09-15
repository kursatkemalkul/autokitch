/* ================================================================
   AUTOKITCH · OPTİMUM HAT · ÇİZİM (ön görünüş, 1000 × 600 tuval)
   ================================================================ */
const COL={idle:'#2e2e33', edge:'#4a4a50', work:'#ff453a', done:'#30d158', txt:'#F5F5F7', dim:'#86868B', dough:'#e9d9a8', base:'#f3e6bf',
  baked:'#b5651d', lahm:'#c9392b', box:'#d9c7a3', bant:'#2997FF', firin:'#ff9f0a', amber:'#ffd60a'};
const FONT=getComputedStyle(document.body).fontFamily;
function rr(ctx,x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.arcTo(x+w,y,x+w,y+h,r); ctx.arcTo(x+w,y+h,x,y+h,r); ctx.arcTo(x,y+h,x,y,r); ctx.arcTo(x,y,x+w,y,r); ctx.closePath(); }
function lbl(ctx,txt,x,y,size,color,align,bold){ ctx.font=`${bold?'600 ':''}${size||11}px ${FONT}`; ctx.fillStyle=color||COL.txt; ctx.textAlign=align||'center'; ctx.textBaseline='middle'; ctx.fillText(String(txt).replace(/(\d)\.(\d)/g,'$1,$2'),x,y); }
function sbox(ctx,x,y,w,h,state,txt,sub){
  ctx.fillStyle = state==='work'?'rgba(255,69,58,.18)': state==='done'?'rgba(48,209,88,.18)':'#1a1a1d';
  rr(ctx,x,y,w,h,3); ctx.fill(); ctx.lineWidth=state==='idle'?1:2; ctx.strokeStyle=state==='work'?COL.work:state==='done'?COL.done:COL.edge; ctx.stroke();
  const n=(txt?1:0)+(sub?1:0), top=y+h/2-(n-1)*6;
  if(txt) lbl(ctx,txt,x+w/2,top,10,state==='work'?COL.work:state==='done'?COL.done:COL.dim);
  if(sub) lbl(ctx,sub,x+w/2,top+(txt?12:0),9,COL.dim);
}
function item(ctx,kind,st,x,y,s,oid,n){
  s=s||1; const r=(kind==='pide'?15:13)*s;
  if(st==='dough'){ ctx.fillStyle=COL.dough; ctx.beginPath(); ctx.arc(x,y-5*s,7*s,0,7); ctx.fill(); return; }
  if(kind==='drink'){ ctx.fillStyle='#d23b3b'; rr(ctx,x-4*s,y-12*s,8*s,12*s,2); ctx.fill(); return; }
  if(st==='box'){ const bw=Math.max(2*r,26); ctx.fillStyle=COL.box; rr(ctx,x-bw/2,y-8*s,bw,12*s,2); ctx.fill(); if(oid) lbl(ctx,'#'+oid+(n>1?' ×'+n:''),x,y-2*s,8,'#3a3020'); return; }
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
  const cmx=cm=>X0+cm*PX, cmy=cm=>FLOOR-cm*PX, mmx=mm=>cmx(mm/10);
  ctx.fillStyle='#0b0b0c'; ctx.fillRect(0,0,W,H); ctx.fillStyle='#141416'; ctx.fillRect(0,FLOOR,W,H-FLOOR);
  const Tr=sim.tray, La=sim.lane, Pk=sim.pack, S=sim.stock;

  /* ---- üst bilgi satırları ---- */
  const sa=sim.saat(t);
  lbl(ctx, sa?('saat '+sa):sim.fmt(t), 16, 20, 16, '#fff', 'left', true);
  lbl(ctx, sim.fmt(t)+(sim.done?'  ·  SENARYO BİTTİ ✓':''), 16, 40, 11, sim.done?COL.done:COL.dim, 'left');
  { const act=Tr.step&&Tr.step.act&&Tr.left>0.05, bek=Tr.waitFrom!==null;
    let g=Tr.gram; if(Tr.dosing && Tr.step && Tr.step.act){ g=Tr.dosing.g0+Tr.dosing.g*(1-Tr.left/Tr.dosing.dur); }
    const d = Tr.state==='bekliyor' ? 'pres altında hazır · hamur bekliyor' : Tr.state==='yukleniyor' ? 'robot hamuru bırakıyor'
      : (Tr.label||'') + (act?` · ${Math.ceil(Tr.left)} sn`:'') + (bek?` · ${Math.round(t-Tr.waitFrom)} sn`:'');
    lbl(ctx, `TABLA · ${d}`, 16, 62, 12, Tr.state==='bekliyor'?COL.dim:COL.amber, 'left', true);
    lbl(ctx, `tartı ${Math.round(g)} g${Tr.p?' · #'+Tr.p.id+' '+Tr.p.tur+' · sipariş #'+Tr.p.order.id:''}${Tr.cycles.length?' · son tur '+Math.round(Tr.cycles[Tr.cycles.length-1])+' sn':''}`, 16, 79, 10, COL.dim, 'left'); }
  const capIn=c.chamber/c.pitch, inCh=La.items.filter(it=>it.x>=c.extra/2 && it.x<=c.extra/2+c.chamber).length, sir=Math.max(0, La.free-t);
  lbl(ctx, `FIRIN · haznede ${inCh} / ${capIn.toFixed(1)} göz · ${La.bake} sn · ${La.v.toFixed(2)} mm/sn · sonraki giriş ${sir>0?Math.ceil(sir)+' sn sonra':'hazır'}`, 16, 98, 11, COL.firin, 'left');
  const ob=Pk.open;
  lbl(ctx, `KUTU · ${Pk.closing?'kapak kapanıyor':ob?`açık kutu #${ob.order.id} · ${ob.items.length}/${ob.need}`:'kutu ağzı boş'} · kapalı, robot bekliyor ${Pk.boxed.length} · kullanılan kutu ${sim.boxesUsed}`, 16, 115, 10, COL.box, 'left');
  lbl(ctx, `STOK · pide ${S.pide}/${STOK.pide} · lahmacun ${S.lahm}/${STOK.lahm} · içecek ${S.icecek}/${STOK.icecek} · kutu şarjörü ${S.kutu}/${STOK.kutu}`, 16, 131, 10, COL.dim, 'left');

  /* ---- robot rayı + kabinler ---- */
  ctx.fillStyle='#3a3a40'; ctx.fillRect(cmx(-4), RAILY-3, cmx(L._len+4)-cmx(-4), 6);
  lbl(ctx, `ROBOT RAYI · ${c.rail} cm/sn`, W-16, RAILY-14, 9, COL.dim, 'right');
  for(const s of L._all){ const x=cmx(s.x0), w=s.w*PX, top=cmy(197);
    ctx.fillStyle='#1c1c1f'; rr(ctx,x+1,top,w-2,197*PX,4); ctx.fill(); ctx.strokeStyle='#3a3a3e'; ctx.lineWidth=1; ctx.stroke();
    lbl(ctx, s.label, x+w/2, top-9, 10, '#c9c9ce'); }

  /* ---- STORE (hattın altında, 5 kolon, tam 3 gün) ---- */
  { const x0=cmx(2), x1=cmx(L._storeEnd-2), cw=(x1-x0)/5, yAlt=cmy(16), yUst=cmy(96), ac=sim.storeOpen, dh=(yAlt-yUst)/9;
    KOLON.forEach((k,ci)=>{ const kx=x0+ci*cw, dolu=sim.kolonDolu(ci), renk=k.tur==='drink'?'#d23b3b':COL.dough;
      lbl(ctx,k.ad,kx+cw/2,yAlt+7,8,COL.dim);
      for(let i=0;i<k.n;i++){ const yy=yAlt-(i+1)*dh, on=i<dolu, acik=ac&&ac.kol===ci&&ac.sira===i;
        ctx.fillStyle=acik?'rgba(41,151,255,.35)':on?'#232327':'#171717'; ctx.fillRect(kx+2,yy+1,cw-4,dh-2);
        ctx.strokeStyle=acik?COL.bant:on?'#4a4a50':'#2a2a2e'; ctx.lineWidth=acik?2:1; ctx.strokeRect(kx+2,yy+1,cw-4,dh-2);
        if(on){ ctx.fillStyle=renk; for(let j=0;j<3;j++){ ctx.beginPath(); ctx.arc(kx+10+j*((cw-20)/2), yy+dh/2, 1.8, 0, 7); ctx.fill(); } } } }); }

  /* ---- TOPPING: kasetler ---- */
  const KW=14*PX, yK0=cmy(166), yK1=cmy(147), yD0=cmy(188), yD1=cmy(170), aktif=new Set(Tr.dosing?[Tr.dosing.k]:[]);
  G.K.forEach((k,i)=>{ const x=mmx(k)-KW/2;
    ctx.fillStyle='#202024'; ctx.fillRect(x,yD0,KW,yD1-yD0); ctx.strokeStyle='#34343a'; ctx.strokeRect(x,yD0,KW,yD1-yD0);
    ctx.fillStyle=aktif.has(i)?'rgba(255,69,58,.22)':'#2a2a30'; ctx.fillRect(x,yK0,KW,yK1-yK0); ctx.strokeStyle=aktif.has(i)?COL.work:'#4a4a50'; ctx.strokeRect(x,yK0,KW,yK1-yK0);
    lbl(ctx,KASET[i].kisa,mmx(k),(yK0+yK1)/2,8,aktif.has(i)?'#fff':'#c9c9ce');
    ctx.fillStyle=aktif.has(i)?COL.work:'#55555c'; ctx.fillRect(mmx(k)-3,yK1,6,3); });

  /* ---- PRES (tablanın üstüne basar) + ÖRS ---- */
  { const pxP=mmx(G.P), plY=sim.press.working?cmy(131):cmy(148);
    ctx.fillStyle='#2a2a30'; ctx.fillRect(pxP-22*PX,cmy(190),44*PX,cmy(160)-cmy(190)); lbl(ctx,'PRES',pxP,cmy(175),9,sim.press.working?COL.work:COL.dim);
    ctx.fillStyle='#55555c'; ctx.fillRect(pxP-2,cmy(160),4,plY-cmy(160)); ctx.fillStyle=sim.press.working?COL.work:'#77777e'; ctx.fillRect(pxP-18*PX,plY,36*PX,4);
    ctx.fillStyle='#3a3a40'; ctx.fillRect(pxP-16*PX,cmy(123),32*PX,cmy(113)-cmy(123)); lbl(ctx,'ÖRS',pxP,cmy(118),8,COL.dim); }
  /* kızak rayı + damlama tavası + fırın bandı burnu */
  ctx.fillStyle='#34343a'; ctx.fillRect(mmx(150),cmy(110),mmx(1660)-mmx(150),4);
  ctx.fillStyle='#26262a'; ctx.fillRect(mmx(150),cmy(104),mmx(1660)-mmx(150),3);
  ctx.fillStyle=COL.firin; ctx.fillRect(mmx(G.XN),cmy(130),mmx(1700)-mmx(G.XN),3);
  /* ---- TABLA ---- */
  { let tx=Tr.x; const dosAct=Tr.dosing && Tr.step && Tr.step.act;
    if(dosAct){ const fr=1-Tr.left/Tr.dosing.dur; tx=Tr.x-150*fr; }
    const zY={seyir:128, agiz:141, ors:124, iniyor:126, kalkiyor:134}[Tr.z]||128, ty=cmy(zY), tw=34*PX;
    ctx.fillStyle='#55555c'; ctx.fillRect(mmx(tx)-2,ty+3,4,cmy(110)-ty-3); ctx.fillStyle='#3a3a40'; ctx.fillRect(mmx(tx)-9,cmy(112),18,6);
    ctx.fillStyle=Tr.state==='bekliyor'?'#d9d9de':'#f0f0f3'; ctx.fillRect(mmx(tx)-tw/2,ty,tw,3);
    if(Tr.p){
      let px=mmx(tx); const st=Tr.p.state==='tabla'?'dough':(Tr.p.state==='base'?'base':'topped');
      if(Tr.strip===2 && Tr.step && Tr.step.act){ const fr=Math.min(1,(t-Tr.pushT0)/Math.max(0.1,c.push)); px=mmx(Tr.x+(G.XN+150-Tr.x)*fr); }
      item(ctx,Tr.p.kind,st==='topped'&&Tr.p.kind==='pide'?'base':st,px,ty-3,0.8);
      if(Tr.p.kind==='pide' && Tr.p.adim.length && (Tr.gram>0||dosAct)){ ctx.fillStyle='#b23a2a'; for(let i=0;i<4;i++){ ctx.beginPath(); ctx.arc(px-9+i*6,ty-3,1.6,0,7); ctx.fill(); } }
      if(dosAct){ const ang=t*2.2; ctx.strokeStyle='#fff'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(px,ty-3); ctx.lineTo(px+Math.cos(ang)*10,ty-3+Math.sin(ang)*4); ctx.stroke();
        yagis(ctx,mmx(G.K[Tr.dosing.k]),yK1+3,ty-8,t,KASET[Tr.dosing.k].renk); }
    }
    if(Tr.strip){ const bx=Tr.strip===2&&Tr.step&&Tr.step.act ? mmx(Tr.x-G.TR+(G.XN+150-Tr.x)*Math.min(1,(t-Tr.pushT0)/Math.max(0.1,c.push))) : mmx(Tr.x-G.TR-10);
      ctx.fillStyle=COL.amber; ctx.fillRect(bx-2,ty-16,4,14); lbl(ctx,'itici',bx,ty-22,8,COL.amber); } }

  /* ---- FIRIN (tek sıra) ---- */
  { const x0=mmx(1700), x1=mmx(1700+La.Ltot), hz0=mmx(1700+c.extra/2), hz1=mmx(1700+c.extra/2+c.chamber);
    ctx.fillStyle='#19140f'; ctx.fillRect(x0,cmy(162),x1-x0,cmy(100)-cmy(162)); ctx.strokeStyle=COL.firin; ctx.lineWidth=1.5; ctx.strokeRect(x0,cmy(162),x1-x0,cmy(100)-cmy(162));
    ctx.fillStyle=inCh?'rgba(255,159,10,.14)':'rgba(255,159,10,.05)'; ctx.fillRect(hz0,cmy(156),hz1-hz0,cmy(106)-cmy(156));
    ctx.setLineDash([5,4]); ctx.strokeRect(hz0,cmy(156),hz1-hz0,cmy(106)-cmy(156)); ctx.setLineDash([]);
    ctx.fillStyle='#55555c'; ctx.fillRect(x0,cmy(130),x1-x0,3);
    lbl(ctx,`hazne ${c.chamber} · ${capIn.toFixed(1)} göz`,(x0+x1)/2,cmy(151),9,COL.firin);
    for(const it of La.items){ const x=mmx(1700+it.x); if(x>x1) continue; item(ctx,it.p.kind,it.x>c.extra/2+c.chamber*0.7?'baked':'base',x,cmy(131)-3,0.75); }
    ctx.fillStyle='#202024'; ctx.fillRect(x0+4,cmy(190),x1-x0-8,cmy(168)-cmy(190)); lbl(ctx,'EGZOZ · filtre',(x0+x1)/2,cmy(179),9,COL.dim); }

  /* ---- KESME PLAKASI ---- */
  { const s=L.KESME, x=cmx(s.x0), w=s.w*PX, p=sim.plate.p; let st='idle', a='SPREY + KESİCİ', b='plaka';
    if(p){ if(p.state==='cutting'){ st='work'; a=`${p.kind==='pide'?'KESİM':'GEÇİŞ'} ${Math.ceil(sim.plate.end-t)} sn`; b='#'+p.id+' · sip. #'+p.order.id; } else { st='done'; a='KUTU BEKLİYOR'; b='#'+p.id; } }
    sbox(ctx,x+4,cmy(190),w-8,cmy(152)-cmy(190),st,a,b);
    ctx.fillStyle='#55555c'; ctx.fillRect(x+4,cmy(130),w-8,3);
    if(p) item(ctx,p.kind,p.state==='cutting'?'baked':'cut',x+w/2,cmy(131)-3,0.75);
    if(sim.plate.queue.length) lbl(ctx,`sırada ${sim.plate.queue.length}`,x+w/2,cmy(122),9,COL.work); }

  /* ---- KUTU: katlama · kutu ağzı (sipariş kutusu) · kapalı kutular ---- */
  { const s=L.PACK, x=cmx(s.x0), w=s.w*PX;
    sbox(ctx,x+4,cmy(190),w-8,cmy(166)-cmy(190),Pk.folding?'work':'idle',Pk.folding?`KATLANIYOR ${Math.ceil(Pk.end-t)} sn`:(Pk.ready?'KUTU HAZIR ✓':'KUTU YOK'),`şarjör ${S.kutu}`);
    const b=Pk.open;
    if(b){
      sbox(ctx,x+4,cmy(162),w-8,cmy(138)-cmy(162),Pk.closing?'work':'done', Pk.closing?`KAPAK ${Math.max(0,Math.ceil(Pk.lidEnd-t))} sn`:`AÇIK KUTU #${b.order.id}`, `${b.items.length}/${b.need} ${b.kind==='pide'?'pide':'lahmacun'}`);
      ctx.fillStyle=COL.box; rr(ctx,x+w/2-22,cmy(132),44,10,2); ctx.fill();
      b.items.forEach((q,i)=>item(ctx,q.kind,'cut',x+w/2,cmy(132)-1-i*4,0.6));
    } else sbox(ctx,x+4,cmy(162),w-8,cmy(138)-cmy(162),'idle','KUTU AĞZI','boş');
    if(Pk.boxed.length){ sbox(ctx,x+4,cmy(118),w-8,cmy(98)-cmy(118),'done',`KAPALI ×${Pk.boxed.length}`,'robot alacak');
      Pk.boxed.slice(0,3).forEach((bx,i)=>item(ctx,bx.kind,'box',x+w/2-28+i*28,cmy(90),0.5,bx.order.id,bx.items.length)); } }

  /* ---- QR DOLABI ---- */
  { const s=L.PICKUP, rows=Math.ceil(c.lockers/2), lw=(s.w-24)/2*PX-4, lh=118/rows*PX-4;
    for(let i=0;i<c.lockers;i++){ const lx=cmx(sim.lockerX(i)), ly=cmy(sim.lockerY(i)), l=sim.lockers[i];
      if(!l.p){ sbox(ctx,lx-lw/2,ly-lh/2,lw,lh,'idle',String(i+1),''); continue; }
      const o=l.p.order, tam=o.doneT!==null, dkk=((tam?o.doneT:t)-o.arr)/60;
      sbox(ctx,lx-lw/2,ly-lh/2,lw,lh,tam?'done':'work',`#${o.id} ${sim.kisa(o)}`,`${tam?'hazır · ':''}${dkk.toFixed(1)} dk`); }
    lbl(ctx,'göz = sipariş · kutular + içecek aynı gözde',cmx(s.x0+s.w/2),cmy(30),9,COL.dim); }

  /* ---- ROBOT ---- */
  { const R=sim.robot, rx=cmx(R.x), hy=cmy(R.ty||150);
    ctx.fillStyle='#d0d0d6'; rr(ctx,rx-18,RAILY-11,36,20,4); ctx.fill(); ctx.fillStyle=COL.bant; ctx.fillRect(rx-18,RAILY+7,36,3);
    const ex=rx+(hy-RAILY)*0.16, ey=RAILY+10+(hy-RAILY)*0.45;
    ctx.strokeStyle='#e6e6ea'; ctx.lineWidth=6; ctx.lineCap='round'; ctx.beginPath(); ctx.moveTo(rx,RAILY+10); ctx.lineTo(ex,ey); ctx.lineTo(rx,hy-10); ctx.stroke();
    ctx.strokeStyle=COL.bant; ctx.lineWidth=2; ctx.beginPath(); ctx.moveTo(rx-7,hy-4); ctx.lineTo(rx-8,hy+5); ctx.moveTo(rx+7,hy-4); ctx.lineTo(rx+8,hy+5); ctx.stroke();
    if(R.carry) item(ctx,R.carry.kind,R.carry.st,rx,hy+2,0.8,R.carry.oid,R.carry.n);
    if(R.label){ const txt=R.step&&R.step.act?`${R.label} · ${Math.ceil(R.left)} sn`:R.label; ctx.font=`11px ${FONT}`; const tw=ctx.measureText(txt).width+16;
      const bx=Math.max(4,Math.min(W-tw-4,rx-tw/2)); ctx.fillStyle='rgba(0,0,0,.8)'; rr(ctx,bx,RAILY-40,tw,18,4); ctx.fill(); lbl(ctx,txt,bx+tw/2,RAILY-31,11,R.step&&R.step.act?COL.firin:'#fff'); }
    else if(!sim.done) lbl(ctx,'robot boşta',rx,RAILY-31,10,COL.dim); }
}
