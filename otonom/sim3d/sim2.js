/* ================= ÇİZİM ================= */
function seg(mesh,a,b){ const v=b.clone().sub(a), L=v.length()||1; mesh.scale.set(1,L,1); mesh.position.copy(a).addScaledVector(v,.5); mesh.quaternion.setFromUnitVectors(V(0,1,0),v.normalize()); }
function basisQ(x,u,t){ const m=new THREE.Matrix4().makeBasis(x.clone(),u.clone(),t.clone()); return new THREE.Quaternion().setFromRotationMatrix(m); }
function yUp(mesh,u){ mesh.quaternion.setFromUnitVectors(V(0,1,0),u.clone().normalize()); }
const ICERIK_RENK={taban:0xf0d9a8, kasar:0xf0d9a8, harc:0xf0d9a8, pismis:0xd9a45a};
function tepsiGoster(g,n,pos,q){ g.position.copy(pos); g.quaternion.copy(q); const ic=n.icerik||'';
  g.userData.taban.visible=['taban','kasar','harc','pismis'].indexOf(ic)>=0; g.userData.taban.material.color.set(ICERIK_RENK[ic]||0xf0d9a8);
  g.userData.kasar.visible=(ic==='kasar'||ic==='harc'||ic==='pismis'); g.userData.kasar.material.color.set(ic==='harc'?0xb0402a:ic==='pismis'?0xe0a030:0xffd24a);
  g.userData.kutu.visible=(ic==='kutu'); }
function ciz(){
  const r=R(), z=railZ(), P=PRES();
  ray.position.set(1950,60,z); araba.position.set(S.carX,190,z);
  const kt=tabanY(); kaide.scale.y=Math.max(1,kt-320); kaide.position.set(S.carX,320+(kt-320)/2,z);
  tabanM.scale.set(r.taban/150,1,r.taban/150); tabanM.position.set(S.carX,kt+60,z);
  const W=Wof(S), k=ik(W); S.sonIK=k;
  seg(ustKol,k.Sh,k.E); seg(onKol,k.E,k.W); eklem[0].position.copy(k.Sh); eklem[1].position.copy(k.E); eklem[2].position.copy(k.W);
  const Wd=k.W, t=S.t, u=S.u, x=xAxis(), pt=(tt,uu,xx=0)=>Wd.clone().addScaledVector(t,tt).addScaledVector(u,uu).addScaledVector(x,xx), Q=basisQ(x,u,t);
  seg(bilekM,Wd,pt(EL.BILEK,0)); avucM.position.copy(pt(EL.BILEK+EL.AVUC/2,0)); avucM.quaternion.setFromUnitVectors(V(0,1,0),t); pimM.position.copy(pt(EL.BILEK+EL.AVUC+EL.PIM/2,0)); pimM.quaternion.copy(avucM.quaternion);
  parmakM.forEach((m,i)=>{ m.position.copy(pt(EL.BILEK+EL.AVUC+EL.PARMAK/2,0,(i?1:-1)*(S.parmak/2+EL.PARMAK_W/2))); m.quaternion.copy(Q); });
  // yükler + dünya nesneleri
  const c=tcpOf(Wd,S,S.yuk), n=S.tasi;
  S.nesne.forEach(o=>{ if(!o.mesh) nesneGoster(o); if(!o.mesh) return; if(o===n){ if(o.tip==='tepsi') tepsiGoster(o.mesh,o,c,basisQ(x.clone().negate(),u,t.clone().negate())); else if(o.tip==='top'){ o.mesh.position.copy(c); } else { o.mesh.position.copy(c); yUp(o.mesh,u); } }
    else { if(o.tip==='tepsi') tepsiGoster(o.mesh,o,o.pos,new THREE.Quaternion()); else { o.mesh.position.copy(o.pos); o.mesh.quaternion.set(0,0,0,1); } if(o.tip==='kutu') o.mesh.material.opacity=o.kapali?1:.55; } });
  // istasyon hareketleri
  const kz=P.cz+(PRES_KIZAK.disari-P.cz)*S.kizak; kizakM.position.set(P.cx,P.plaka-10,kz); altPlaka.position.set(P.cx,P.plaka-26,P.cz); ustPlaka.position.set(P.cx,P.plaka+230-S.ustPlakaY,P.cz);
  presAgiz.position.y=(P.y[0]+P.y[1])/2; presAgiz.scale.y=(P.y[1]-P.y[0])/180;
  bicak.position.y=KES.y[1]+100-S.bicakY; itici.position.set(KUT.cx,KUT.plaka+25,KUT.cz-175+S.itme*KUT.itme);
  Object.entries(KOLON).forEach(([kk,K])=>{ const a=S.cek[kk]||0, m=cekMesh[kk]; m.visible=a>0.02; if(m.visible){ const y=K.kotlar[S.cekI[kk]]; m.scale.z=Math.max(.01,a); m.position.set((K.x0+K.x1)/2,y+(K.ic+30)/2,a*K.acik/2); } });
  firinKapak.forEach((kp,i)=>{ const a=S.kapak[i]||0, h=kp.f[1]-kp.f[0]-80, th=-a*Math.PI/2; kp.m.rotation.set(th,0,0);
    kp.m.position.set(FIR_X.cx, kp.f[1]-40+(-h/2*Math.cos(th)+8*Math.sin(th)), (-h/2)*Math.sin(th)-8*Math.cos(th)); });
  qrKapak.forEach((q,i)=>{ const a=S.qrk[i]||0, th=-a*Math.PI/2; q.m.rotation.set(th,0,0); q.m.position.set(q.x, q.y+(85*Math.cos(th)-7*Math.sin(th)), QR.z[0]+(85*Math.sin(th)+7*Math.cos(th))); });
  const hits=carpisma(k); S.temas=hits; temasM.forEach((m,i)=>{ m.visible=i<hits.length; if(m.visible) m.position.copy(hits[i].p); });
  erisimW.position.copy(k.Sh); erisimW.scale.setScalar(k.maxD);
  const oz={}; hits.forEach(h=>{ oz[h.parca+' → '+h.engel]=1; });
  out.innerHTML=`<b>${r.ad}</b> · omuz→bilek <b>${k.D.toFixed(0)}</b> / ${k.maxD.toFixed(0)} → <span class="${k.ok?'ok':'yok'}"><b>${k.ok?'YETİŞİYOR':'YETİŞMİYOR'}</b>${k.ok?'':' ('+(k.D-k.maxD).toFixed(0)+' mm eksik)'}</span><br>
    temas: <span class="${hits.length?'yok':'ok'}"><b>${hits.length?hits.length+' nokta':'yok'}</b></span> ${Object.keys(oz).slice(0,4).join(' · ')}<br>
    <span style="color:#8a94a4">dirsek ${k.dirsek} · bilek x ${W.x.toFixed(0)} · y ${W.y.toFixed(0)} · z ${W.z.toFixed(0)} · araba ${S.carX.toFixed(0)} · yük ${n?n.tip+(n.icerik?' ('+n.icerik+')':''):'boş'} · parmak ${S.parmak.toFixed(0)}</span>`;
}
function resize(){ const w=innerWidth-(innerWidth>760?380:0), h=innerWidth>760?innerHeight:innerHeight*.45; renderer.setSize(w,h,true); camera.aspect=w/h; camera.updateProjectionMatrix(); }
addEventListener('resize',resize); resize();
const CAM={iso:[[-1200,2600,5400],[2000,900,0]], on:[[2000,1100,6600],[2000,1000,0]], ust:[[2000,7500,600],[2000,0,400]], yan:[[-4800,1400,600],[1200,900,300]], robot:[[0,1800,2400],[0,1100,100]]};
function kamera(k){ const c=CAM[k]; if(k==='robot'){ c[0][0]=S.carX-1500; c[1][0]=S.carX; } camera.position.set(...c[0]); controls.target.set(...c[1]); controls.update(); }
kamera('iso');
document.querySelectorAll('[data-cam]').forEach(b=>b.onclick=()=>kamera(b.dataset.cam));
let takip=false; $('takip').onchange=e=>{ takip=e.target.checked; };
(function loop(){ if(takip&&anim){ controls.target.lerp(V(S.carX+300,1000,100),.08); const d=camera.position.clone().sub(controls.target); camera.position.copy(controls.target).add(d.setLength(Math.max(2600,d.length()))); controls.update(); } ciz(); renderer.render(scene,camera); requestAnimationFrame(loop); })();

/* ================= ADIM İNŞACISI ================= */
const ROT=(v,ax,a)=>v.clone().applyAxisAngle(ax,a);
const TR=1300, TZ=220, FZ=60;   // FZ: fırın yaklaşma z'si (tepsi kenarı kapak boşluğunda; bilek 560)
const carFor=x=>Math.min(RAY_X[1],Math.max(RAY_X[0],x-300));
function insaci(cur){  // cur: {carX,tcp,t,u,yuk,parmak}
  const st=[]; const snap=()=>({carX:cur.carX, tcp:cur.tcp.clone(), t:cur.t.clone(), u:cur.u.clone(), yuk:cur.yuk, parmak:cur.parmak});
  const sure=(mm,v)=>mm/v+0.25;
  function mv(ad,to,v,cb){ const a=snap(), b=snap(); if(to.tcp) b.tcp.copy(to.tcp); if(to.carX!==undefined) b.carX=to.carX; const d=Math.max(a.tcp.distanceTo(b.tcp),Math.abs(b.carX-a.carX)); const s=sure(d,v||HIZ.serbest);
    st.push({ad,sure:s,basla:()=>{ S.t.copy(a.t); S.u.copy(a.u); S.yuk=a.yuk; S.parmak=a.parmak; },fn:e=>{ S.carX=a.carX+(b.carX-a.carX)*e; S.tcp.lerpVectors(a.tcp,b.tcp,e); },bitir:cb}); cur.tcp.copy(b.tcp); cur.carX=b.carX; return s; }
  function kay(ad,x,cb){ const a=snap(); const s=sure(Math.abs(x-a.carX),HIZ.ray); st.push({ad,sure:s,basla:()=>{ S.t.copy(a.t); S.u.copy(a.u); S.yuk=a.yuk; S.parmak=a.parmak; },fn:e=>{ const d=(x-a.carX)*e; S.carX=a.carX+d; S.tcp.copy(a.tcp); S.tcp.x+=d; },bitir:cb}); cur.tcp.x+=x-cur.carX; cur.carX=x; return s; }
  function don(ad,ax,deg,pivotT,s,cb){ const a=snap(), W0=Wof(a), Pv=pivotT===null?a.tcp.clone():W0.clone().addScaledVector(a.t,pivotT), rad=deg*Math.PI/180;
    st.push({ad,sure:s,basla:()=>{ S.yuk=a.yuk; S.parmak=a.parmak; },fn:e=>{ const th=rad*e; S.t.copy(ROT(a.t,ax,th)); S.u.copy(ROT(a.u,ax,th)); if(pivotT===null) S.tcp.copy(a.tcp); else { const W=Pv.clone().add(ROT(W0.clone().sub(Pv),ax,th)); S.tcp.copy(tcpOf(W,S,a.yuk)); } },bitir:cb});
    cur.t=ROT(a.t,ax,rad); cur.u=ROT(a.u,ax,rad); if(pivotT!==null){ const W=Pv.clone().add(ROT(W0.clone().sub(Pv),ax,rad)); cur.tcp=tcpOf(W,cur,a.yuk); } return s; }
  function bekle(ad,s,fn,cb){ st.push({ad,sure:s,fn:fn||(()=>{}),bitir:cb}); return s; }
  function yuk(ad,yeni,fn){ const a=snap(), W=Wof(a); cur.tcp=tcpOf(W,cur,yeni); cur.yuk=yeni; st.push({ad,sure:0.05,basla:()=>{ const Wn=Wof(S); S.yuk=yeni; S.tcp.copy(tcpOf(Wn,S,yeni)); if(fn) fn(); },fn:()=>{}}); return 0.05; }
  function parmak(ad,acik,fn){ const a=snap(); st.push({ad,sure:HIZ.parmak,fn:e=>{ S.parmak=a.parmak+(acik-a.parmak)*e; },bitir:fn}); cur.parmak=acik; return HIZ.parmak; }
  function kapak(ad,tip,idx,hedef,fn){ const s=tip==='cek'?HIZ.cekmece:tip==='fir'?HIZ.kapak:tip==='qr'?HIZ.qrkapak:tip==='itici'?HIZ.itici:HIZ.kizak; let a0=null;
    st.push({ad,sure:s,basla:()=>{ a0=tip==='cek'?(S.cek[idx]||0):tip==='fir'?(S.kapak[idx]||0):tip==='qr'?(S.qrk[idx]||0):tip==='itici'?S.itme:S.kizak; },
      fn:e=>{ const v=a0+(hedef-a0)*e; if(tip==='cek') S.cek[idx]=v; else if(tip==='fir') S.kapak[idx]=v; else if(tip==='qr') S.qrk[idx]=v; else if(tip==='itici') S.itme=v; else S.kizak=v; if(fn) fn(e,v); }}); return s; }
  function tasima(ad){ return mv(ad||'taşıma pozu',{tcp:V(cur.carX+300,TR,TZ)}); }
  return {st,cur,mv,kay,don,bekle,yuk,parmak,kapak,tasima,snap};
}

/* ================= GÖREV İNŞACILARI ================= */
/* ortak: tepsi koy / al (el yatay, sap +z tarafında) */
function tepsiKoy(B,tray,ad,cx,cy,cz,cb,carx){ B.kay('→ '+ad,carx||carFor(cx)); B.mv(ad+': ağız hizası',{tcp:V(cx,cy+20,TZ)}); B.mv(ad+': içeri',{tcp:V(cx,cy+20,cz)},HIZ.ince); B.mv(ad+': indir',{tcp:V(cx,cy,cz)},HIZ.mikro);
  B.bekle('pim çözülür',HIZ.pim); B.yuk('tepsi bırakıldı','bos',()=>{ S.tasi=null; tray.pos=V(cx,cy,cz); if(cb) cb(); }); B.mv(ad+': el çıkar',{tcp:V(cx,cy,TZ)},HIZ.ince); }
function tepsiAl(B,tray,ad,cx,cy,cz,cb,carx){ B.kay('→ '+ad,carx||carFor(cx)); B.mv(ad+': ağız hizası',{tcp:V(cx,cy,TZ)}); B.mv(ad+': pim sokete',{tcp:V(cx,cy,cz)},HIZ.ince);
  B.bekle('pim kilitlenir',HIZ.pim); B.yuk('tepsi alındı','tepsi',()=>{ S.tasi=tray; if(cb) cb(); }); B.mv(ad+': kaldır',{tcp:V(cx,cy+20,cz)},HIZ.mikro); B.mv(ad+': çıkar',{tcp:V(cx,cy+20,TZ)},HIZ.ince); B.tasima(); }
function nisPos(i){ return V(NIS.cx, NIS.raf0+NIS.pitch*i+20, NIS.cz); }
/* G1 · nişten tepsi → pres kızağı → hamur topu → tepsiye (kızak dışarıda) */
function G_baslat(B,p){ const P=PRES(), tray=p.tray, ballH={tip:'top',pos:p.topPos.clone(),icerik:''};
  B.kapak('pres kızağı dışarı','kizak',0,1);
  tepsiAl(B,tray,'tepsi nişi',NIS.cx,nisPos(tray.raf).y,NIS.cz);
  tepsiKoy(B,tray,'pres kızağı',P.cx,P.plaka+20,PRES_KIZAK.disari,null,carPres()); B.tasima();
  // hamur: araba çekmecenin yanına (topa yakın taraf), el dikey
  const K=KOLON[p.kolon], kx=(K.x0+K.x1)/2, sagda=p.topPos.x>=kx, yan=sagda?K.x1+100+R().taban/2:Math.max(RAY_X[0],K.x0-100-R().taban/2);
  B.kay('→ çekmece '+p.kolon+(sagda?' (sağ)':' (sol)'),yan);
  B.kapak('çekmece açılır','cek',p.kolon,1,(e)=>{ ballH.pos.z=p.topPos.z*e; if(e>0.02&&!ballH.mesh) nesneGoster(ballH); });
  B.st[B.st.length-1].basla=(function(b0){ return ()=>{ if(b0) b0(); S.cekI[p.kolon]=p.sira; ballH.pos.copy(p.topPos); ballH.pos.z=0; }; })(B.st[B.st.length-1].basla);
  B.mv('parmak boşluğu · z +60',{tcp:V(B.cur.carX+300,B.cur.tcp.y,280)}); B.don('el dikey (parmaklar aşağı)',V(1,0,0),-90,0,0.9); B.yuk('kavrama modu','top');
  B.parmak('parmaklar açılır',120); B.mv('topun üstüne',{tcp:V(p.topPos.x,p.topPos.y+150,p.topPos.z)}); B.mv('in',{tcp:p.topPos.clone()},HIZ.ince);
  B.parmak('parmaklar kapanır · top kavrandı',85,()=>{ S.tasi=ballH; }); B.mv('kaldır',{tcp:V(p.topPos.x,p.topPos.y+150,p.topPos.z)},HIZ.ince);
  B.kapak('çekmece kapanır','cek',p.kolon,0);
  B.mv('yüksel · z 350',{tcp:V(p.topPos.x,900,350)});
  const ty=P.plaka+20+5+EL.TOP_R; B.kay('→ pres',carPres()); B.mv('kızak kotuna yüksel',{tcp:V(B.cur.tcp.x,ty+120,PRES_KIZAK.disari)}); B.mv('kızak üstü',{tcp:V(P.cx,ty+120,PRES_KIZAK.disari)}); B.mv('topu tepsi ortasına indir',{tcp:V(P.cx,ty,PRES_KIZAK.disari)},HIZ.ince);
  B.parmak('parmaklar açılır · top tepside',120,()=>{ nesneSil(ballH); tray.icerik='top'; }); B.mv('kaldır',{tcp:V(P.cx,ty+150,PRES_KIZAK.disari)},HIZ.ince); B.mv('dışarı 120',{tcp:V(P.cx,ty+150,PRES_KIZAK.disari+120)});
  B.don('el yatay',V(1,0,0),90,0,0.9); B.yuk('boş el','bos'); B.parmak('parmaklar 70',70); B.tasima();
}
/* pres çevrimi (istasyon işi · robot yok): kızak içeri 2 s + pres 5 s + kızak dışarı 2 s */
function G_presCevrim(B,p){ const tray=p.tray; B.kapak('kızak içeri','kizak',0,0); B.bekle('PRES · '+HIZ.pres+' s',HIZ.pres,e=>{ const a=e<.5?e*2:2-e*2; S.ustPlakaY=a*(230-25-8); if(e>.55) tray.icerik='taban'; }); B.kapak('kızak dışarı','kizak',0,1); }
/* G2 · tepsiyi kızaktan al → topping (spiral) → fırın */
function G_topping(B,p){ const P=PRES(), tray=p.tray, noz=p.tip==='pide'?NOZ.kasar:NOZ.harc, ds=p.tip==='pide'?HIZ.kasar:HIZ.harc;
  tepsiAl(B,tray,'pres kızağı',P.cx,P.plaka+20,PRES_KIZAK.disari,null,carPres());
  B.kay('→ topping',carFor(noz.x)); B.mv('topping: ağız hizası',{tcp:V(noz.x,T_Y,TZ)}); B.mv('topping: nozul altına',{tcp:V(noz.x,T_Y,NOZ.z)},HIZ.ince);
  { const a=B.snap(); B.st.push({ad:(p.tip==='pide'?'KAŞAR':'HARÇ')+' · spiral · '+ds+' s',sure:ds,fn:e=>{ const th=e*4*Math.PI, rr=110*e; S.tcp.set(noz.x+rr*Math.cos(th),T_Y,NOZ.z+rr*Math.sin(th)); if(e>.3) tray.icerik=p.tip==='pide'?'kasar':'harc'; }}); B.cur.tcp.set(noz.x+110,T_Y,NOZ.z); }
  B.mv('topping: merkeze',{tcp:V(noz.x,T_Y,NOZ.z)},HIZ.ince); B.mv('topping: çıkar',{tcp:V(noz.x,T_Y,TZ)},HIZ.ince); B.tasima();
  const g=p.goz, taban=FIR[g][0]+100; B.kay('→ fırın göz '+(g+1),carFirin()); B.kapak('fırın kapağı açılır','fir',g,1);
  B.mv('fırın: kapak kotu',{tcp:V(FIR_X.cx,taban+40,TZ)}); B.mv('fırın: kapak hizası',{tcp:V(FIR_X.cx,taban+40,FZ)},HIZ.ince); B.mv('fırın: içeri',{tcp:V(FIR_X.cx,taban+40,FIR_X.cz)},HIZ.ince); B.mv('fırın: taşa indir',{tcp:V(FIR_X.cx,taban+20,FIR_X.cz)},HIZ.mikro);
  B.bekle('pim çözülür',HIZ.pim); B.yuk('tepsi fırında','bos',()=>{ S.tasi=null; tray.pos=V(FIR_X.cx,taban+20,FIR_X.cz); }); B.mv('fırın: el çıkar',{tcp:V(FIR_X.cx,taban+20,FZ)},HIZ.ince); B.mv('geri',{tcp:V(FIR_X.cx,taban+20,TZ)});
  B.kapak('fırın kapağı kapanır','fir',g,0); B.tasima();
}
/* G3 · fırından al → kesim */
function G_kesim(B,p){ const tray=p.tray, g=p.goz, taban=FIR[g][0]+100;
  B.kay('→ fırın göz '+(g+1),carFirin()); B.kapak('fırın kapağı açılır','fir',g,1); B.st[B.st.length-1].basla=()=>{ tray.icerik='pismis'; };
  B.mv('fırın: kapak kotu',{tcp:V(FIR_X.cx,taban+20,TZ)}); B.mv('fırın: kapak hizası',{tcp:V(FIR_X.cx,taban+20,FZ)},HIZ.ince); B.mv('fırın: pim sokete',{tcp:V(FIR_X.cx,taban+20,FIR_X.cz)},HIZ.ince); B.bekle('pim kilitlenir',HIZ.pim);
  B.yuk('tepsi alındı','tepsi',()=>{ S.tasi=tray; }); B.mv('fırın: kaldır',{tcp:V(FIR_X.cx,taban+40,FIR_X.cz)},HIZ.mikro); B.mv('fırın: çıkar',{tcp:V(FIR_X.cx,taban+40,FZ)},HIZ.ince); B.mv('geri',{tcp:V(FIR_X.cx,taban+40,TZ)}); B.kapak('fırın kapağı kapanır','fir',g,0); B.tasima();
  tepsiKoy(B,tray,'kesim',KES.cx,KES.y[0]+20,KES.cz); B.tasima();
}
function G_kesimCevrim(B){ B.bekle('YILDIZ BIÇAK · '+HIZ.kesim+' s',HIZ.kesim,e=>{ const a=e<.5?e*2:2-e*2; S.bicakY=a*100; }); }
/* G4 · kesimden al → sprey */
function G_sprey(B,p){ const tray=p.tray; tepsiAl(B,tray,'kesim',KES.cx,KES.y[0]+20,KES.cz); tepsiKoy(B,tray,'sprey',YAG.cx,YAG.y[0]+20,YAG.cz); B.tasima(); }
function G_spreyCevrim(B){ B.bekle('SPREY · tereyağı · '+HIZ.sprey+' s',HIZ.sprey); }
/* G5 · spreyden al → kutu (pide kutuya kayar, kutu kapanır, itici kutuyu tepsiye iter) → QR (kutu arka duvara dayanır, tepsi çekilir) → tepsi nişe */
function G_bitir(B,p,o){ const tray=p.tray, kutuH={tip:'kutu',pos:V(KUT.cx,KUT.plaka+22.5,KUT.cz),kapali:false};
  tepsiAl(B,tray,'sprey',YAG.cx,YAG.y[0]+20,YAG.cz);
  B.kay('→ kutulama',carFor(KUT.cx),()=>{ nesneGoster(kutuH); });
  B.mv('kutu: ağız hizası',{tcp:V(KUT.cx,580,TZ)}); B.mv('kutu: açık kutunun üstüne',{tcp:V(KUT.cx,580,KUT.cz)},HIZ.ince);
  B.don('tepsi 8° eğilir (pivot soket)',V(1,0,0),-8,EL.BILEK+EL.AVUC+EL.PIM,0.5);
  { const a=B.snap(), b=a.tcp.clone(); b.z+=350; B.st.push({ad:'geri çek → pide kutuya kayar',sure:1.2,fn:e=>{ S.tcp.lerpVectors(a.tcp,b,e); if(e>.7){ tray.icerik=''; kutuH.icerik='pide'; } }}); B.cur.tcp.copy(b); }
  B.don('tepsi düzelir',V(1,0,0),8,EL.BILEK+EL.AVUC+EL.PIM,0.4);
  B.mv('kutu: plaka hizasına in',{tcp:V(KUT.cx,KUT.plaka-5,TZ)},HIZ.ince); B.mv('kutu: tepsi plakanın önüne',{tcp:V(KUT.cx,KUT.plaka-5,-15)},HIZ.ince);
  B.bekle('KUTU KAPANIR · flap · '+HIZ.kapan+' s',HIZ.kapan,e=>{ if(e>.8) kutuH.kapali=true; });
  B.kapak('İTİCİ · kutu tepsiye','itici',0,1,(e)=>{ kutuH.pos.z=KUT.cz+KUT.itme*e; if(e>.98){ nesneSil(kutuH); tray.icerik='kutu'; } });
  B.kapak('itici geri','itici',0,0); B.mv('kutu: tepsi + kutu çıkar',{tcp:V(KUT.cx,KUT.plaka-5,TZ)},HIZ.ince); B.mv('yüksel',{tcp:V(KUT.cx,800,TZ)});
  // QR: 180° dönüş (pivot tepsi+el ortası 335 · bilek 785 → 115)
  const q=qrKapak[o.goz], kat=o.kutuSay||0, taban=q.y+30+45*kat+(kat?5:0);   // +30: avuç açık kapağın (rampa) üstünde kalsın
  B.kay('→ QR dolabı',carFor(q.x)); B.mv('dönüş pozu · bilek z 755',{tcp:V(B.cur.carX+300,950,255)}); B.don('180° DÖNÜŞ · pivot 335 · z 420',V(0,1,0),180,335,2.0);
  B.mv('QR: göz hizası',{tcp:V(q.x,taban,700)}); B.kapak('QR kapağı açılır','qr',o.goz,1); B.mv('QR: kutu arka duvara 15 kala',{tcp:V(q.x,taban,1165)},HIZ.ince);
  { const a=B.snap(), b=a.tcp.clone(); b.z=700; const yeni={tip:'kutu',pos:V(q.x,q.y+22.5+45*kat,1180),kapali:true}; B.st.push({ad:'tepsi geri çekilir → kutu göze kalır',sure:1.2,fn:e=>{ S.tcp.lerpVectors(a.tcp,b,e); if(e>.6&&tray.icerik==='kutu'){ tray.icerik=''; nesneGoster(yeni); o.nesneler.push(yeni); } }}); B.cur.tcp.copy(b); }
  B.kapak('QR kapağı kapanır','qr',o.goz,0); B.mv('dönüş pozu',{tcp:V(q.x,950,585)}); B.don('180° geri dönüş',V(0,1,0),-180,335,2.0); B.tasima();
  tepsiKoy(B,tray,'tepsi nişi',NIS.cx,nisPos(tray.raf).y,NIS.cz); B.tasima();
}
/* G6 · içecek / tatlı: şarjör ön yuvasından yandan kavra (kutu yatık iner → bilek 90° yatık kavrar, sonra dik çevirir) → QR gözü */
function G_icecek(B,o,tip){ const Y=YUVA[tip], H={tip,pos:V(Y.x,Y.y,Y.z),icerik:''}, hh=tip==='kola'?EL.KOLA_H:EL.TATLI_H;
  B.kay('→ '+(tip==='kola'?'içecek':'tatlı')+' şarjörü',carFor(Y.x));
  B.bekle('ŞARJÖR · '+(tip==='kola'?'kutu yuvaya yatık iner':'kap yuvaya iner'),2,null,()=>{ nesneGoster(H); });
  if(Y.yatay) B.don('bilek 90° yatık · parmaklar dikey kapanacak',V(0,0,1),-90,0,0.6);
  B.yuk('yandan kavrama modu',tip); B.parmak('parmaklar açılır',110);
  B.mv('yuva önü',{tcp:V(Y.x,Y.y,Y.z+250)}); B.mv('in · parmaklar '+(tip==='kola'?'kutunun üst ucuna':'kabın üst kısmına'),{tcp:V(Y.x,Y.y,Y.z)},HIZ.ince);
  B.parmak('parmaklar kapanır · kavrandı',tip==='kola'?60:84,()=>{ S.tasi=H; }); B.mv('çıkar',{tcp:V(Y.x,Y.y,Y.z+250)},HIZ.ince);
  if(Y.yatay) B.don('kutu dik çevrilir',V(0,0,1),90,0,0.6);
  const q=qrKapak[o.goz], gx=q.x+(tip==='kola'?-100:100), gy=q.y+10+hh/2;
  B.kay('→ QR dolabı',carFor(gx)); B.mv('dönüş pozu',{tcp:V(B.cur.carX+300,950,220)}); B.don('180° dönüş (pivot avuç)',V(0,1,0),180,120,1.2);
  B.mv('QR: göz hizası',{tcp:V(gx,gy+8,700)}); B.kapak('QR kapağı açılır','qr',o.goz,1); B.mv('QR: içeri',{tcp:V(gx,gy+8,973)},HIZ.ince); B.mv('QR: indir',{tcp:V(gx,gy,973)},HIZ.mikro);
  B.parmak('parmaklar açılır · bırakıldı',110,()=>{ S.tasi=null; H.pos=V(gx,gy,973); o.nesneler.push(H); }); B.mv('QR: el çıkar',{tcp:V(gx,gy,700)},HIZ.ince);
  B.kapak('QR kapağı kapanır','qr',o.goz,0); B.mv('dönüş pozu',{tcp:V(gx,950,400)}); B.don('180° geri dönüş',V(0,1,0),-180,120,1.2); B.parmak('parmaklar 70',70); B.yuk('boş el','bos'); B.tasima();
}
