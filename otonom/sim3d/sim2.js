/* ================= ÇİZİM ================= */
function seg(mesh,a,b){ const v=b.clone().sub(a), L=v.length()||1; mesh.scale.set(1,L,1); mesh.position.copy(a).addScaledVector(v,.5); mesh.quaternion.setFromUnitVectors(V(0,1,0),v.normalize()); }
function basis(mesh){ const m=new THREE.Matrix4().makeBasis(xAxis(),S.u.clone(),S.t.clone()); mesh.quaternion.setFromRotationMatrix(m); }
function yUp(mesh,u){ mesh.quaternion.setFromUnitVectors(V(0,1,0),u.clone().normalize()); }
function ciz(){
  const r=R(), z=railZ(), P=PRES(), D=S.dunya;
  ray.position.set(1750,60,z); araba.position.set(S.carX,190,z);
  const kt=tabanY(); kaide.scale.y=Math.max(1,kt-320); kaide.position.set(S.carX,320+(kt-320)/2,z);
  tabanM.scale.set(r.taban/150,1,r.taban/150); tabanM.position.set(S.carX,kt+60,z);
  const W=Wof(S), k=ik(W); S.sonIK=k;
  seg(ustKol,k.Sh,k.E); seg(onKol,k.E,k.W); eklem[0].position.copy(k.Sh); eklem[1].position.copy(k.E); eklem[2].position.copy(k.W);
  const Wd=k.W, t=S.t, u=S.u, x=xAxis(), pt=(tt,uu,xx=0)=>Wd.clone().addScaledVector(t,tt).addScaledVector(u,uu).addScaledVector(x,xx);
  seg(bilekM,Wd,pt(U.BILEK,0)); kokM.position.copy(pt(U.BILEK+50,-14)); basis(kokM);
  catalM.position.copy(pt(U.BILEK+U.FORK/2,U.FORK_U)); basis(catalM); kepce.position.copy(pt(U.BILEK+U.FORK+10,U.FORK_U)); basis(kepce); altPed.position.copy(pt(690,-48)); basis(altPed);
  // yükler
  const tcpD=tcpOf(Wd,S,S.yuk);
  if(S.tasi==='tepsi'){ tepsiM.visible=true; tepsiM.position.copy(tcpD); yUp(tepsiM,u); }
  else if(D.tepsi){ tepsiM.visible=true; tepsiM.position.copy(D.tepsi); tepsiM.quaternion.set(0,0,0,1); } else tepsiM.visible=false;
  const tep=S.tasi==='tepsi'?tcpD:D.tepsi, tu=S.tasi==='tepsi'?u:V(0,1,0);
  tabanMesh.visible=kasarM.visible=false;
  if(D.pideKutuda&&D.kutu){ tabanMesh.visible=kasarM.visible=true; tabanMesh.position.copy(D.kutu).setY(D.kutu.y-22.5+3+4); kasarM.position.copy(D.kutu).setY(D.kutu.y-22.5+3+8+2.5); tabanMesh.quaternion.set(0,0,0,1); kasarM.quaternion.set(0,0,0,1); }
  else if(tep&&D.tepsiUst){ tabanMesh.visible=true; tabanMesh.position.copy(tep).addScaledVector(tu,9); yUp(tabanMesh,tu); if(D.tepsiUst!=='taban'){ kasarM.visible=true; kasarM.position.copy(tep).addScaledVector(tu,15.5); yUp(kasarM,tu); } }
  tabanMesh.material.color.set(D.tepsiUst==='pismis'?0xd9a45a:0xf0d9a8);
  if(S.tasi==='top'){ topM.visible=true; topM.position.copy(tcpD); } else if(D.top){ topM.visible=true; topM.position.copy(D.top); } else topM.visible=false;
  if(S.tasi==='kutu'){ kutuM.visible=true; kutuM.position.copy(tcpD); basis(kutuM); } else if(D.kutu){ kutuM.visible=true; kutuM.position.copy(D.kutu); kutuM.quaternion.set(0,0,0,1); } else kutuM.visible=false;
  kutuM.material.opacity=D.kutuKapali?1:.55;
  rafTepsi.forEach((m,i)=>m.visible=i<D.rafN);
  altPlaka.position.set(P.cx,P.plaka-6,P.cz); ustPlaka.position.set(P.cx,P.plaka+250-D.ustPlakaY,P.cz);
  presAgiz.position.y=(P.y[0]+P.y[1])/2; presAgiz.scale.y=(P.y[1]-P.y[0])/210;
  bicak.position.y=KES.y[1]+100-D.bicakY;
  Object.entries(KOLON).forEach(([kk,K])=>{ const a=S.cek[kk]||0, m=cekMesh[kk]; m.visible=a>0.02; if(m.visible){ const y=K.kotlar[S.cekI[kk]]; m.scale.z=Math.max(.01,a); m.position.set((K.x0+K.x1)/2,y+(K.ic+30)/2,a*CEK_ACIK/2); } });
  // çarpışma
  const hits=carpisma(k); S.temas=hits; temasM.forEach((m,i)=>{ m.visible=i<hits.length; if(m.visible) m.position.copy(hits[i].p); });
  erisimW.position.copy(k.Sh); erisimW.scale.setScalar(k.maxD);
  const oz={}; hits.forEach(h=>{ oz[h.parca+' → '+h.engel]=1; });
  out.innerHTML=`<b>${r.ad}</b> · omuz→bilek <b>${k.D.toFixed(0)}</b> / ${k.maxD.toFixed(0)} → <span class="${k.ok?'ok':'yok'}"><b>${k.ok?'YETİŞİYOR':'YETİŞMİYOR'}</b>${k.ok?'':' ('+(k.D-k.maxD).toFixed(0)+' mm eksik)'}</span><br>
    temas: <span class="${hits.length?'yok':'ok'}"><b>${hits.length?hits.length+' nokta':'yok'}</b></span> ${Object.keys(oz).slice(0,4).join(' · ')}<br>
    <span style="color:#8a94a4">dirsek ${k.dirsek} · bilek x ${W.x.toFixed(0)} · y ${W.y.toFixed(0)} · z ${W.z.toFixed(0)} · araba ${S.carX.toFixed(0)} · yük ${S.tasi||'boş'}</span>`;
}
function resize(){ const w=innerWidth-(innerWidth>760?360:0), h=innerWidth>760?innerHeight:innerHeight*.45; renderer.setSize(w,h,true); camera.aspect=w/h; camera.updateProjectionMatrix(); }
addEventListener('resize',resize); resize();
const CAM={iso:[[-1200,2600,5200],[1900,900,0]], on:[[1900,1100,6200],[1900,1000,0]], ust:[[1900,7000,600],[1900,0,400]], yan:[[-4500,1400,600],[1200,900,300]], robot:[[S.carX-1500,1800,2400],[S.carX,1100,100]]};
function kamera(k){ const c=CAM[k]; if(k==='robot'){ c[0][0]=S.carX-1500; c[1][0]=S.carX; } camera.position.set(...c[0]); controls.target.set(...c[1]); controls.update(); }
kamera('iso');
document.querySelectorAll('[data-cam]').forEach(b=>b.onclick=()=>kamera(b.dataset.cam));
[model,omuz,railz,pay,plaka,goz,cekS,siraS,topS].forEach(e=>e.addEventListener('input',()=>{ omuz_v.textContent=omuz.value; railz_v.textContent=railz.value; if(!anim) hazirla(); }));
(function loop(){ ciz(); renderer.render(scene,camera); requestAnimationFrame(loop); })();

/* ================= SENARYO OLUŞTURUCU ================= */
let anim=null, ADIM=[];
const ROT=(v,ax,a)=>v.clone().applyAxisAngle(ax,a);
function senaryo(){
  const st=[], cur={carX:S.carX, tcp:S.tcp.clone(), t:S.t.clone(), u:S.u.clone(), yuk:S.yuk};
  const snap=()=>({carX:cur.carX, tcp:cur.tcp.clone(), t:cur.t.clone(), u:cur.u.clone(), yuk:cur.yuk});
  const H=()=>1/(+hiz.value);
  function mv(ad,to,sure,cb){ const a=snap(); const b=snap(); if(to.tcp) b.tcp.copy(to.tcp); if(to.carX!==undefined) b.carX=to.carX;
    st.push({ad,sure:sure*H(),basla:()=>{ S.t.copy(a.t); S.u.copy(a.u); S.yuk=a.yuk; },fn:e=>{ S.carX=a.carX+(b.carX-a.carX)*e; S.tcp.lerpVectors(a.tcp,b.tcp,e); },bitir:cb}); cur.tcp.copy(b.tcp); cur.carX=b.carX; }
  function kay(ad,x,sure){ const a=snap(); st.push({ad,sure:sure*H(),fn:e=>{ const d=(x-a.carX)*e; S.carX=a.carX+d; S.tcp.copy(a.tcp); S.tcp.x+=d; }}); cur.tcp.x+=x-cur.carX; cur.carX=x; }
  function don(ad,ax,deg,pivotT,sure,cb){ // ax dünya ekseni; pivot = W + pivotT·t (pivotT null → tcp sabit)
    const a=snap(), W0=Wof(a), Pv=pivotT===null?a.tcp.clone():W0.clone().addScaledVector(a.t,pivotT), rad=deg*Math.PI/180;
    st.push({ad,sure:sure*H(),basla:()=>{ S.yuk=a.yuk; },fn:e=>{ const th=rad*e; S.t.copy(ROT(a.t,ax,th)); S.u.copy(ROT(a.u,ax,th)); if(pivotT===null){ S.tcp.copy(a.tcp); } else { const W=Pv.clone().add(ROT(W0.clone().sub(Pv),ax,th)); S.tcp.copy(tcpOf(W,S,a.yuk)); } },bitir:cb});
    cur.t=ROT(a.t,ax,rad); cur.u=ROT(a.u,ax,rad); if(pivotT!==null){ const W=Pv.clone().add(ROT(W0.clone().sub(Pv),ax,rad)); cur.tcp=tcpOf(W,cur,a.yuk); } }
  function bekle(ad,sure,fn){ st.push({ad,sure:sure*H(),fn:fn||(()=>{})}); }
  function yuk(ad,yeni,fn){ const a=snap(), W=Wof(a); cur.tcp=tcpOf(W,cur,yeni); cur.yuk=yeni; st.push({ad,sure:0.05,basla:()=>{ const Wn=Wof(S); S.yuk=yeni; S.tcp.copy(tcpOf(Wn,S,yeni)); if(fn) fn(); },fn:()=>{}}); }
  const D=S.dunya, P=PRES(), G=FIR[+goz.value], gozTaban=G[0]+100, K=KOLON[cekS.value], ki=siraS.value==='alt'?0:K.kotlar.length-1, kot=K.kotlar[ki];
  const kx=(K.x0+K.x1)/2, topX=topS.value==='yakin'?K.x1-80:topS.value==='uzak'?K.x0+80:kx, topY=kot+15+U.TOP_R, topZ=350;
  const TR=1300, TZ=220;                                     // taşıma kotu / tepsi z (rim 30 dışarıda)
  const carFor=x=>Math.min(RAY_X[1],Math.max(RAY_X[0],x-300));
  function tepsiKoy(ad,cx,cy,cz,carx,cbBirak){ // tepsi çatalda → yüzeye bırak, çatal boş çıkar
    kay('→ '+ad,carx,1.2); mv(ad+': ağız hizası',{tcp:V(cx,cy+20,TZ)},1.0); mv(ad+': içeri',{tcp:V(cx,cy+20,cz)},1.2); mv(ad+': indir',{tcp:V(cx,cy,cz)},.4);
    yuk('bırak','bos',()=>{ S.tasi=null; D.tepsi=V(cx,cy,cz); if(cbBirak) cbBirak(); }); mv(ad+': çatal çıkar',{tcp:V(cx,cy,TZ)},1.0); }
  function tepsiAl(ad,cx,cy,cz,carx){ kay('→ '+ad,carx,1.2); mv(ad+': ağız hizası',{tcp:V(cx,cy,TZ)},1.0); mv(ad+': çatal altına',{tcp:V(cx,cy,cz)},1.2);
    yuk('al','tepsi',()=>{ S.tasi='tepsi'; D.tepsi=null; }); mv(ad+': kaldır',{tcp:V(cx,cy+20,cz)},.4); mv(ad+': çıkar',{tcp:V(cx,cy+20,TZ)},1.0); mv('taşıma kotu',{tcp:V(cx,TR,TZ)},.8); }
  // 1 · tepsi nişinden boş tepsi
  const rafY=RAF.taban+15+5+25*(D.rafN-1);
  mv('başlangıç · taşıma pozu',{tcp:V(cur.carX+300,TR,TZ)},.6);
  tepsiAl('tepsi nişi',RAF.cx,rafY,RAF.cz,carFor(RAF.cx)); st[st.length-4].bitir=()=>{ D.rafN--; };
  // 2 · tepsi prese
  tepsiKoy('pres',P.cx,P.plaka+20,P.cz,carFor(P.cx));
  mv('taşıma kotu',{tcp:V(P.cx,TR,TZ)},.8);
  // 3 · hamur topu: çekmece yanına kay, çatal ray boyunca (−x), kepçe üstten
  const sagda=topX>=kx, yan=sagda?K.x1+100+R().taban/2:K.x0-100-R().taban/2;   // araba açık çekmecenin yanında (topa yakın taraf)
  kay('→ çekmece '+cekS.value+(sagda?' (sağ)':' (sol)'),yan,1.4);
  bekle('çekmece açılır',1.0,e=>{ S.cek[cekS.value]=e; S.cekI[cekS.value]=ki; D.top=V(topX,topY,topZ*e); });
  const yanAl = topY>=711;                                                     // çatal düzlemi = top + 53,5 → kaide üstü 748 + pay                                                     // üst sıralar: çatal yatay (−x), ped çatal altında; alt sıralar: çatal dikey, ped uçta
  mv('dönüş payı · z +60',{tcp:V(cur.carX+300,cur.tcp.y,260)},.5);
  if(yanAl){
    don('çatal ray boyunca ('+(sagda?'−x':'+x')+') · pivot 200',V(0,1,0),sagda?90:-90,200,.9); yuk('alt ped modu','topAlt');
    mv('topun üstüne · çatal yatay',{tcp:V(topX,topY+150,topZ)},1.2); mv('in, vakum',{tcp:V(topX,topY,topZ)},.8);
    yuk('top alındı','topAlt',()=>{ S.tasi='top'; D.top=null; }); mv('kaldır',{tcp:V(topX,topY+150,topZ)},.7);
    bekle('çekmece kapanır',.9,e=>{ S.cek[cekS.value]=1-e; });
    mv('dışarı 400 · bilek z 750',{tcp:V(topX,topY+150,topZ+400)},.9);
    don('çatal hatta döner (bilek sabit)',V(0,1,0),sagda?-90:90,0,1.2);       // t: ∓x → −z, top z 55
  } else {
    don('çatal dikey (uç aşağı) · bilek sabit',V(1,0,0),-90,0,.9); yuk('uç ped modu','top');
    mv('topun üstüne · çatal dikey',{tcp:V(topX,topY+150,topZ)},1.2); mv('in, vakum',{tcp:V(topX,topY,topZ)},.8);
    yuk('top alındı','top',()=>{ S.tasi='top'; D.top=null; }); mv('kaldır',{tcp:V(topX,topY+150,topZ)},.7);
    bekle('çekmece kapanır',.9,e=>{ S.cek[cekS.value]=1-e; });
    mv('dışarı 118',{tcp:V(topX,topY+150,topZ+117.5)},.5);
    don('çatal hatta döner · pivot çatal üstü 430',V(1,0,0),90,430,1.2);       // t: −y → −z; bilek z 858, top z 70
  }
  kay('→ pres',carFor(P.cx),1.4);
  if(cur.tcp.y<800) mv('kaide üstüne yüksel · y 800',{tcp:V(cur.tcp.x,800,cur.tcp.z)},.6);
  mv('pres x hizası',{tcp:V(P.cx,cur.tcp.y,cur.tcp.z)},.8);
  mv('pres ağız kotuna yüksel',{tcp:V(P.cx,P.plaka+20+5+U.TOP_R+20,cur.tcp.z)},1.0);
  mv('pres ağız hizası',{tcp:V(P.cx,P.plaka+20+5+U.TOP_R+20,55)},.8);
  mv('pres: top içeri',{tcp:V(P.cx,P.plaka+20+5+U.TOP_R+20,P.cz)},1.3); mv('pres: topu tepsi ortasına',{tcp:V(P.cx,P.plaka+20+5+U.TOP_R,P.cz)},.4);
  yuk('bırak','bos',()=>{ S.tasi=null; D.top=V(P.cx,P.plaka+25+U.TOP_R,P.cz); }); mv('pres: çatal çıkar',{tcp:V(P.cx,P.plaka+20+80,TZ)},1.0);
  bekle('PRES · 5 s (hızlı)',1.6,e=>{ const a=e<.5?e*2:2-e*2; D.ustPlakaY=a*(250-25-8); if(e>.55){ D.top=null; D.tepsiUst='taban'; } });
  // 4 · tepsi + taban topping'e (spiral)
  tepsiAl('pres',P.cx,P.plaka+20,P.cz,carFor(P.cx));
  const TY=1120; kay('→ topping',carFor(NOZ.x),1.4); mv('topping: ağız hizası',{tcp:V(NOZ.x,TY,TZ)},1.0); mv('topping: nozul altına',{tcp:V(NOZ.x,TY,NOZ.z)},1.3);
  { const a=snap(); st.push({ad:'KAŞAR · spiral 2 tur',sure:2.4*H(),fn:e=>{ const th=e*4*Math.PI, rr=110*e; S.tcp.set(NOZ.x+rr*Math.cos(th),TY,NOZ.z+rr*Math.sin(th)); if(e>.3) D.tepsiUst='kasar'; }}); cur.tcp.set(NOZ.x+110,TY,NOZ.z); }
  mv('topping: merkeze',{tcp:V(NOZ.x,TY,NOZ.z)},.6); mv('topping: çıkar',{tcp:V(NOZ.x,TY,TZ)},1.2); mv('taşıma kotu',{tcp:V(NOZ.x,TR,TZ)},.8);
  // 5 · fırın
  tepsiKoy('fırın göz '+(+goz.value+1),2450,gozTaban+20,-360,carFor(2450));
  bekle('FIRIN · 240 s (hızlı)',1.6,e=>{ if(e>.8) D.tepsiUst='pismis'; });
  tepsiAl('fırın',2450,gozTaban+20,-360,carFor(2450));
  // 6 · kesim
  tepsiKoy('kesim',KES.cx,KES.y[0]+20,KES.cz,carFor(KES.cx));
  bekle('YILDIZ BIÇAK · 100 strok',1.2,e=>{ const a=e<.5?e*2:2-e*2; D.bicakY=a*100; });
  tepsiAl('kesim',KES.cx,KES.y[0]+20,KES.cz,carFor(KES.cx));
  // 7 · sprey
  tepsiKoy('sprey',YAG.cx,YAG.y[0]+20,YAG.cz,carFor(YAG.cx));
  bekle('SPREY · tereyağı',1.0);
  tepsiAl('sprey',YAG.cx,YAG.y[0]+20,YAG.cz,carFor(YAG.cx));
  // 8 · kutulama: kutu plakada açık; tepsi kutunun üstüne, eğ, geri çek → pide kayar
  st[st.length-1].bitir=()=>{ D.kutu=V(KUT.cx,KUT.plaka+22.5,KUT.cz); D.kutuKapali=false; };
  kay('→ kutulama',carFor(KUT.cx),1.4); mv('kutu: ağız hizası',{tcp:V(KUT.cx,620,TZ)},1.0); mv('kutu: kutunun üstüne',{tcp:V(KUT.cx,620,KUT.cz)},1.3);
  don('tepsiyi 8° eğ (pivot kavrama)',V(1,0,0),-8,120,.6);
  { const a=snap(); const b=a.tcp.clone(); b.z+=350; st.push({ad:'geri çek → pide kutuya kayar',sure:1.0*H(),fn:e=>{ S.tcp.lerpVectors(a.tcp,b,e); if(e>.7){ D.pideKutuda=true; D.tepsiUst=''; } }}); cur.tcp.copy(b); }
  don('tepsiyi düzelt',V(1,0,0),8,120,.5); mv('kutu: çıkar',{tcp:V(KUT.cx,620,TZ)},.9); mv('taşıma kotu',{tcp:V(KUT.cx,TR,TZ)},.8);
  // 9 · boş tepsi nişe
  tepsiKoy('tepsi nişi',RAF.cx,RAF.taban+20+25*(D.rafN-1),RAF.cz,carFor(RAF.cx),()=>{ D.tepsi=null; D.rafN++; });
  bekle('KUTU KAPANIR · flap',1.0,e=>{ if(e>.8) D.kutuKapali=true; });
  // 10 · kutuyu al (çatal plakadaki kanala girer)
  kay('→ kutu',carFor(KUT.cx),1.2); yuk('kutu modu','kutu'); mv('kutu: ağız hizası',{tcp:V(KUT.cx,KUT.plaka+22.5,TZ)},.9); mv('kutu: çatal altına',{tcp:V(KUT.cx,KUT.plaka+22.5,KUT.cz)},1.2);
  yuk('kutu alındı','kutu',()=>{ S.tasi='kutu'; D.kutu=null; D.pideKutuda=false; }); mv('kutu: kaldır',{tcp:V(KUT.cx,KUT.plaka+42.5,KUT.cz)},.4); mv('kutu: çıkar',{tcp:V(KUT.cx,KUT.plaka+42.5,TZ)},1.1);
  // 11 · 180° dönüş (pivot çatal üstünde 400, koridor ortası z 450)
  kay('→ dönüş yeri',2900,1.0); mv('dönüş: kot 1150',{tcp:V(cur.tcp.x,1150,cur.tcp.z)},.8); mv('dönüş: pivot üstü · bilek z 830',{tcp:V(2900,1150,290)},.8);
  don('180° DÖNÜŞ · pivot çatal üstü 383 · z 447',V(0,1,0),180,383,2.2);
  // 12 · QR göz (sol kolon, en alt)
  const qx=(QR.kol[0][0]+QR.kol[0][1])/2, qy=QR.satir[0]+22.5;
  kay('→ QR dolabı',carFor(qx),1.2); mv('QR: göz üstü hizası',{tcp:V(qx,1150,QR.z[0]-200)},.9); mv('QR: göz hizasına in',{tcp:V(qx,qy+20,QR.z[0]-200)},1.0); mv('QR: içeri',{tcp:V(qx,qy+20,QR.z[0]+220)},1.2); mv('QR: indir',{tcp:V(qx,qy,QR.z[0]+220)},.4);
  yuk('bırak','bos',()=>{ S.tasi=null; D.kutu=V(qx,qy,QR.z[0]+220); D.kutuKapali=true; }); mv('QR: çatal çıkar',{tcp:V(qx,qy,QR.z[0]-200)},1.0);
  bekle('TESLİM · göz kilitlenir',.8);
  return st;
}
function hazirla(){ // sıfır durumu
  S.carX=1100; S.t.set(0,0,-1); S.u.set(0,1,0); S.yuk='bos'; S.tasi=null; S.tcp.set(1400,1300,200);
  S.cek={K1:0,K2:0,K3:0}; Object.assign(S.dunya,{tepsi:null,top:null,kutu:null,kutuKapali:false,tepsiUst:'',pideKutuda:false,rafN:6,ustPlakaY:0,bicakY:0});
  log.innerHTML=''; step.textContent='';
}
function dur(){ if(anim){ cancelAnimationFrame(anim); anim=null; } }
function play(){
  dur(); hazirla(); ADIM=senaryo(); let i=0, t0=performance.now(), started=false, rec={yok:false,minD:0,hits:{}};
  const ease=t=>t<.5?2*t*t:-1+(4-2*t)*t;
  function frame(now){
    const a=ADIM[i]; if(!started){ if(a.basla) a.basla(); started=true; t0=now; rec={yok:false,eksik:0,hits:{}}; }
    const t=Math.min(1,(now-t0)/(a.sure*1000)); a.fn(ease(t)); ciz(); step.textContent=(i+1)+'/'+ADIM.length+' · '+a.ad;
    const k=S.sonIK; if(k&&!k.ok){ rec.yok=true; rec.eksik=Math.max(rec.eksik,k.D-k.maxD); } S.temas.forEach(h=>{ rec.hits[h.parca+' → '+h.engel]=1; });
    if(t>=1){ if(a.bitir) a.bitir(); const hs=Object.keys(rec.hits); const d=document.createElement('div');
      d.innerHTML=`<b>${i+1}</b> ${a.ad} — <span class="${rec.yok?'yok':'ok'}">${rec.yok?'erişim YOK (−'+rec.eksik.toFixed(0)+')':'erişim OK'}</span> · <span class="${hs.length?'yok':'ok'}">${hs.length?'TEMAS: '+hs.join(', '):'temas yok'}</span>`;
      if(a.sure>0.06) log.appendChild(d); i++; started=false; if(i>=ADIM.length){ anim=null; const ny=log.querySelectorAll('span.yok').length; step.innerHTML='bitti · '+ADIM.length+' adım · '+(ny?'<span class="yok">'+ny+' sorunlu satır</span>':'<span class="ok">erişim tam, temas yok</span>'); return; } }
    anim=requestAnimationFrame(frame);
  }
  anim=requestAnimationFrame(frame);
}
$('play').onclick=play; $('stop').onclick=()=>{ dur(); step.textContent+=' (durdu)'; };
hazirla();

function debugAdim(idx,n=16){ hazirla(); const A=senaryo(); let outp=null; for(let i=0;i<=idx;i++){ const a=A[i]; if(a.basla) a.basla(); const hs=[]; let maxD=0,minOK=true; for(let s=0;s<=n;s++){ a.fn(s/n); ciz(); const k=S.sonIK; maxD=Math.max(maxD,k.D); if(!k.ok) minOK=false; S.temas.forEach(h=>hs.push([s,h.parca,h.engel,h.p.x.toFixed(0),h.p.y.toFixed(0),h.p.z.toFixed(0)])); } if(a.bitir) a.bitir(); if(i===idx) outp={ad:a.ad,maxD:maxD.toFixed(0),ok:minOK,E:S.sonIK.E.toArray().map(v=>v.toFixed(0)),W:S.sonIK.W.toArray().map(v=>v.toFixed(0)),hits:hs.slice(0,12)}; } return outp; }
