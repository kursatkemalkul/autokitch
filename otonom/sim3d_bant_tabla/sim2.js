/* ================= ÇİZİM ================= */
function seg(mesh,a,b){ const v=b.clone().sub(a), L=v.length()||1; mesh.scale.set(1,L,1); mesh.position.copy(a).addScaledVector(v,.5); mesh.quaternion.setFromUnitVectors(V(0,1,0),v.normalize()); }
function basisQ(x,u,t){ const m=new THREE.Matrix4().makeBasis(x.clone(),u.clone(),t.clone()); return new THREE.Quaternion().setFromRotationMatrix(m); }
function yUp(mesh,u){ mesh.quaternion.setFromUnitVectors(V(0,1,0),u.clone().normalize()); }

function cizRobot(ri){ S.ri=ri; const Mx=ROBM[ri], r=R(), z=railZ(), kt=tabanY();
  Mx.araba.position.set(S.carX,190,z); Mx.kaide.scale.y=Math.max(1,kt-320); Mx.kaide.position.set(S.carX,320+(kt-320)/2,z);
  Mx.tabanM.scale.set(r.taban/150,1,r.taban/150); Mx.tabanM.position.set(S.carX,kt+60,z);
  const W=Wof(S), k=ik(W); S.sonIK=k;
  seg(Mx.ustKol,k.Sh,k.E); seg(Mx.onKol,k.E,k.W); Mx.eklem[0].position.copy(k.Sh); Mx.eklem[1].position.copy(k.E); Mx.eklem[2].position.copy(k.W);
  const Wd=k.W, t=S.t.clone(), u=S.u.clone(), x=xAxis(), pt=(tt,uu,xx=0)=>Wd.clone().addScaledVector(t,tt).addScaledVector(u,uu).addScaledVector(x,xx), Q=basisQ(x,u,t);
  seg(Mx.bilekM,Wd,pt(EL.BILEK,0)); Mx.avucM.position.copy(pt(EL.BILEK+EL.AVUC/2,0)); Mx.avucM.quaternion.setFromUnitVectors(V(0,1,0),t); Mx.pimM.position.copy(pt(EL.BILEK+EL.AVUC+EL.PIM/2,0)); Mx.pimM.quaternion.copy(Mx.avucM.quaternion);
  Mx.parmakM.forEach((m,i)=>{ m.position.copy(pt(EL.BILEK+EL.AVUC+EL.PARMAK/2,0,(i?1:-1)*(S.parmak/2+EL.PARMAK_W/2))); m.quaternion.copy(Q); });
  return {ri,k,W,c:tcpOf(Wd,S,S.yuk),x,t,u,n:S.tasi,pts:orneklem(k)}; }


function tepsiGoster(g,n,pos,q){ g.position.copy(pos); g.quaternion.copy(q); const ud=g.userData; ud.kutu.visible=(n.icerik==='kutu'); if(ud.kutu.visible) kutuGoster(ud.kutu,{kapali:true,kapanma:1}); }
/* ürün (tepsisiz): top → taban → dozajlı → pişmiş */
function urunGoster(g,n){ g.position.copy(n.pos); g.rotation.set(0,n.rot||0,0); const ic=n.icerik||'', ud=g.userData; ud.top.visible=(ic==='top'); ud.taban.visible=(ic==='taban'||ic==='ustlu'||ic==='pismis'); ud.taban.material.color.set(ic==='pismis'?0xd9a45a:0xf0d9a8);
  ud.ust.visible=(ic==='ustlu'||ic==='pismis'); ud.ust.material.color.set(ic==='pismis'?(n.urun==='lahm'?0x8a3a22:0xe0a030):(n.urun==='lahm'?0xb0402a:0xffd24a)); const d=ic==='pismis'?1:Math.max(.06,n.dolu===undefined?1:n.dolu); ud.ust.scale.set(d,1,d); }
function ciz(){
  const P=PRES(); ray.position.set(HAT.boy/2,60,railZ()); const RS=[];
  for(let ri=0;ri<2;ri++){ const vis=ri<(S.n||1); ROBM[ri].hepsi.forEach(m=>{ m.visible=vis; }); if(vis) RS.push(cizRobot(ri)); }
  S.ri=0; const q=RS[0];
  const QX=new THREE.Quaternion().setFromAxisAngle(V(1,0,0),Math.PI/2);
  S.nesne.forEach(o=>{ if(!o.mesh) nesneGoster(o); if(!o.mesh) return; const qq2=RS.find(a=>a.n===o)||q, tut=!!RS.find(a=>a.n===o);
    if(o.tip==='urun'){ urunGoster(o.mesh,o); return; }
    if(tut){ if(o.tip==='tepsi') tepsiGoster(o.mesh,o,qq2.c,basisQ(qq2.x.clone().negate(),qq2.u,qq2.t.clone().negate())); else { o.mesh.position.copy(qq2.c); if(o.tip==='kola') yUp(o.mesh,qq2.t); else if(o.tip!=='top') yUp(o.mesh,qq2.u); } }
    else { if(o.tip==='tepsi') tepsiGoster(o.mesh,o,o.pos,new THREE.Quaternion()); else { o.mesh.position.copy(o.pos); if(o.yatik) o.mesh.quaternion.copy(QX); else o.mesh.quaternion.set(0,0,0,1); } if(o.tip==='kutu') kutuGoster(o.mesh,o); } });
  /* makine hareketleri */
  if(!TABLA) altPlaka.position.set(P.cx,P.plaka-6,P.cz); ustPlaka.position.set(P.cx,P.plaka+230-S.ustPlakaY,P.cz); presAgiz.position.y=(P.y[0]+P.y[1])/2;
  bicak.position.set(KESP.cx,PK+230-S.bicakY,KESP.cz); itici.position.set(KESP.cx-200+S.itme*(KUT.cx-KESP.cx),PK+30,KESP.cz);
  if(TABLA){ tablaM.position.set(S.tabla.x,S.tabla.y-6,EKSEN); tablaM.rotation.y=S.tabla.rot||0; const y0=1120, y1=S.tabla.y-12; tablaKol.scale.set(1,Math.max(1,y1-y0),1); tablaKol.position.set(S.tabla.x,(y0+y1)/2,EKSEN); }
  Object.entries(KOLON).forEach(([kk,K])=>{ const a=S.cek[kk]||0, m=cekMesh[kk]; m.visible=a>0.02; if(m.visible){ const y=K.kotlar[S.cekI[kk]]; m.scale.z=Math.max(.01,a); m.position.set((K.x0+K.x1)/2,y+(K.tip==='icecek'?17:(K.ic+30)/2),a*K.acik/2); } });
  const hk=(QR.goz_h-10)/2; qrKapak.forEach((qq,i)=>{ const a=S.qrk[i]||0, th=-a*Math.PI/2; qq.m.rotation.set(th,0,0); qq.m.position.set(qq.x, qq.y+(hk*Math.cos(th)-7*Math.sin(th)), QR.z[0]+(hk*Math.sin(th)+7*Math.cos(th))); });
  akisM.visible=!!S.akis; if(S.akis){ const y0=S.akis.y0, y1=NOZ.alt; akisM.scale.set(1,Math.max(1,y1-y0),1); akisM.position.set(S.akis.x,(y0+y1)/2,S.akis.z); akisM.material.color.set(S.akis.renk); }
  S.ri=0; ROB[0].temas=carpisma(q.k);
  const tum=ROB[0].temas; temasM.forEach((m,i)=>{ m.visible=i<tum.length; if(m.visible) m.position.copy(tum[i].p); });
  { const k=q.k, hs=ROB[0].temas, oz={}; hs.forEach(h=>{ oz[h.parca+' → '+h.engel]=1; }); const n=q.n;
    out.innerHTML=`<b style="color:#2997ff">Robot</b> · erişim <span class="${k.ok?'ok':'yok'}"><b>${k.ok?'tam':'YOK −'+(k.D-k.maxD).toFixed(0)}</b></span> · temas <span class="${hs.length?'yok':'ok'}"><b>${hs.length?hs.length+' nokta':'yok'}</b></span> ${Object.keys(oz).slice(0,2).join(' · ')}<br><span style="color:#8a94a4">araba x ${ROB[0].carX.toFixed(0)} · yük ${n?n.tip+(n.icerik?' ('+n.icerik+')':''):'boş'}</span>`; }
}
function resize(){ const ps=!!window.PANELSIZ, w=innerWidth-((!ps&&innerWidth>760)?380:0), h=(ps||innerWidth>760)?innerHeight:innerHeight*.45; renderer.setSize(w,h,true); camera.aspect=w/h; camera.updateProjectionMatrix(); }   // panel=0 (karşılaştırma penceresi): sağ menü yok, tuval tam ekran
addEventListener('resize',resize); resize();


const CAM={iso:[[-1500,3000,7000],[2650,900,0]], on:[[2650,1100,8200],[2650,1000,0]], ust:[[2650,9000,600],[2650,0,400]]};
/* karşılaştırma penceresi: hattın tamamı kadraja girsin — dar pencerede kamera yatay açıya göre geri çekilir (tam karşıdan) */
function kameraSigdir(){ const boy=(typeof HAT==='object'&&HAT.boy)?HAT.boy:3900, cx=boy/2;
  const vf=camera.fov*Math.PI/180, hf=2*Math.atan(Math.tan(vf/2)*camera.aspect), d=(boy*0.55)/Math.tan(hf/2)+380;
  camera.position.set(cx,1220,d); controls.target.set(cx,1010,-250); controls.update(); }
function kamera(k){ const c=CAM[k]; camera.position.set(...c[0]); controls.target.set(...c[1]); controls.update(); }
kamera('iso');
let takip=false; $('takip').onchange=e=>{ takip=e.target.checked; };
(function loop(){ if(takip&&anim){ controls.target.lerp(V(ROB[0].carX+300,1000,100),.08); const d=camera.position.clone().sub(controls.target); camera.position.copy(controls.target).add(d.setLength(Math.max(2600,d.length()))); controls.update(); } ciz(); renderer.render(scene,camera); requestAnimationFrame(loop); })();

/* ================= ADIM İNŞACISI (sim3d · HAT v19 ile aynı) ================= */
/* ================= ADIM İNŞACISI ================= */
const ROT=(v,ax,a)=>v.clone().applyAxisAngle(ax,a);
/* döndürme sonrası yön vektörünü temizle: 1e-16 mertebesindeki birikim "tam 300 mm" gibi sınır testlerini rastgele tetikliyordu */
const TEMIZ=v=>{ const f=x=>Math.abs(x)<1e-9?0:(Math.abs(Math.abs(x)-1)<1e-9?Math.sign(x):x); v.set(f(v.x),f(v.y),f(v.z)); return v; };
const TR=1300, TZ=220;
/* araba hedefin yanında durur: yon +1 → solunda (kol +x'e uzanır) · yon −1 → sağında (kol −x'e uzanır). Kot + derinlik verilirse 4 pozun (ağız önü / içeri × indir / kaldır) hepsine kol yetişen EN UZAK ofset seçilir;
   tepsi kaide kotunun altındaysa ofset ≥ 280 (tepsi r170 + kaide r100). İstenen yan rayın dışına düşüyorsa öbür yan denenir. */
const carFor=(x,y,cz,yon)=>{ yon=yon||1; const icinde=c=>c>=RAY_X[0]&&c<=RAY_X[1];
  /* bir yan için: 4 pozun hepsine yetişen en uzak ofset; hiçbiri tam tutmuyorsa o yanın en yakın ofseti (yan DEĞİŞTİRİLMEZ — yan değişimi alçak tepside kaide çevresinden dolaşma gerektirir); yan rayın dışındaysa null */
  const dene=sg=>{ if(y===undefined){ const c=x-sg*300; return icinde(c)?c:null; } const alcak=y<tabanY()+160; let yedek=null; for(const off of (alcak?[300,280]:[300,280,250,220,200])){ const c=x-sg*off; if(!icinde(c)) continue; yedek=c; let tam=true; for(const dy of [20,40]) for(const z of [TZ,cz===undefined?TZ:cz]){ const k=ikq(V(x,y+dy,z+500),c); if(!k.ok||k.E.z<55) tam=false; } if(tam) return c; } return yedek; };
  const a=dene(yon); if(a!==null) return a; const b=dene(-yon); if(b!==null) return b; return Math.min(RAY_X[1],Math.max(RAY_X[0],x-yon*300)); };
/* park pozu: kol toplanır, bilek robotun tam önünde (dz +380) → üst aralık = araba ± 110 */
const parkTcp=x=>V(x,TR,railZ()+380-500);
/* bir durumun rayda kapladığı aralık — ALT: araba merkezi c0..c1 · ÜST: kaide ± 110, dirsek ± 60, bilek ± 55, uç/yük (tepsi ± 180, diğer ± 70) */
function isgalDurum(a){ const W=Wof(a), k=ikq(W,a.carX), tepsi=a.yuk==='tepsi', uz=tepsi?500:(a.yuk==='bos'?190:320), gen=tepsi?180:70, uc=W.clone().addScaledVector(a.t,uz);
  const xs=[a.carX-110,a.carX+110,k.E.x-60,k.E.x+60,W.x-55,W.x+55,uc.x-gen,uc.x+gen]; return {lo:Math.min(...xs),hi:Math.max(...xs),c0:a.carX,c1:a.carX}; }
const ocBirles=(a,b)=>({lo:Math.min(a.lo,b.lo),hi:Math.max(a.hi,b.hi),c0:Math.min(a.c0,b.c0),c1:Math.max(a.c1,b.c1)});
/* trapez hız profili: hız v, ivme a → süre (kısa yolda üçgen) */
function sureHesap(mm,v,a){ if(mm<1) return 0.1; return mm<v*v/a?2*Math.sqrt(mm/a):mm/v+v/a; }
/* eklem hız sınırı: yol boyunca taban / omuz / ön kol açı değişimi → süre en az bu kadar (ease tepe hızı ×2) */
function eklemSure(ornek){ let prev=null, mx=0; const N=10; for(let i=0;i<=N;i++){ const o=ornek(i/N), q=ikq(o.W,o.carX).q; if(prev) for(let j=0;j<3;j++){ let d=Math.abs(q[j]-prev[j]); if(j===0&&d>Math.PI) d=2*Math.PI-d; mx=Math.max(mx,d); } prev=q; } return mx*N*2/(HIZ.eklem*Math.PI/180); }
/* istasyon kapağı / çekmece / itici animasyonu — tek başına adım ya da bir robot hareketiyle AYNI ANDA (ek) */
function kapakAnim(tip,idx,hedef,fn,onBasla){ let a0=null; const get=()=>tip==='cek'?(S.cek[idx]||0):tip==='fir'?(S.kapak[idx]||0):tip==='qr'?(S.qrk[idx]||0):S.itme;
  const set=v=>{ if(tip==='cek') S.cek[idx]=v; else if(tip==='fir') S.kapak[idx]=v; else if(tip==='qr') S.qrk[idx]=v; else S.itme=v; };
  return {sure:tip==='cek'?HIZ.cekmece:tip==='fir'?HIZ.kapak:tip==='qr'?HIZ.qrkapak:HIZ.itici, gecikme:0, cek:tip==='cek'?{k:idx,hedef}:null, basla:()=>{ a0=get(); if(onBasla) onBasla(); }, fn:e=>{ const v=a0+(hedef-a0)*e; set(v); if(fn) fn(e,v); }}; }
/* araba çekmecenin önündeyken çekmece açılamaz: x aralığından çıkana kadar geçen süre */
function gecikmeHesap(x0,x1,K){ const a=K.x0-175, b=K.x1+175; if(x0<=a||x0>=b) return 0; const cik=x1<=a?a:b; return Math.abs(x0-cik)/HIZ.ray+HIZ.ray/HIZ.ivmeRay; }
function insaci(cur,yon){  // cur: {carX,tcp,t,u,yuk,parmak} · yon: hedefe hangi yandan yanaşılır (+1 sol · −1 sağ)
  yon=yon||1; const st=[]; const snap=()=>({carX:cur.carX, tcp:cur.tcp.clone(), t:cur.t.clone(), u:cur.u.clone(), yuk:cur.yuk, parmak:cur.parmak});
  const ekFn=(ek,s)=>ek?(e=>{ const ee=ek.gecikme?Math.max(0,Math.min(1,(e*s-ek.gecikme)/ek.sure)):e; ek.fn(ee); }):null;
  /* kaide koruması: el −z yönündeyken düz yol alçaktan (omuz altı) kendi kaidesinin üstünden/içinden geçiyorsa → önce taşıma kotuna (TR) yüksel, karşıya geç, sonra in */
  function kaideYakin(a,b){ const Wa=Wof(a), Wb=Wof(b), tepsi=a.yuk==='tepsi', yl=omuzY()+90; for(let i=0;i<=12;i++){ const W=Wa.clone().lerp(Wb,i/12); for(const L of (tepsi?[0,140,330,500]:[0,140,230])){ const q=W.clone().addScaledVector(a.t,L), lim=(tepsi&&L>=330?300:175)-1; if(q.y<yl&&Math.hypot(q.x-a.carX,q.z-railZ())<lim) return true; } } return false; }
  /* omuz ekseni koruması: bilek düz yolda omuz eksenine 170'ten fazla yaklaşıyorsa (taban 180° savrulur) → önce robotun tam önüne, koridor tarafına (dz +380) açıl */
  function eksenYakin(a,b){ const Wa=Wof(a), Wb=Wof(b); let mn=1e9; for(let i=0;i<=12;i++){ const W=Wa.clone().lerp(Wb,i/12); mn=Math.min(mn,Math.hypot(W.x-a.carX,W.z-railZ())); } return mn<170; }
  function mv(ad,to,v,cb,ek){ const a=snap(), b=snap(); if(to.tcp) b.tcp.copy(to.tcp);
    if(!to._d&&!to._e&&a.t.z<-0.99&&eksenYakin(a,b)){ const Wa=Wof(a), Wb=Wof(b), Wm=V(a.carX,Math.max(Wa.y,Wb.y),railZ()+380); mv(ad+' · önce robotun önüne açıl (omuz ekseni)',{tcp:tcpOf(Wm,a,a.yuk),_e:1},v); return mv(ad,{tcp:b.tcp,_e:1},v,cb,ek); }
    if(!to._d&&a.t.z<-0.99&&a.yuk!=='top'&&kaideYakin(a,b)){ mv(ad+' · önce yüksel (kaide üstünden geçecek)',{tcp:V(a.tcp.x,TR,TZ),_d:1},v); mv(ad+' · kaide üstünden karşıya',{tcp:V(b.tcp.x,TR,TZ),_d:1},v); return mv(ad,{tcp:b.tcp,_d:1},v,cb,ek); } let s=sureHesap(a.tcp.distanceTo(b.tcp),v||HIZ.serbest,HIZ.ivmeKol), uz=false;
    const Wa=Wof(a), Wb=Wof(b), se=eklemSure(e=>({W:Wa.clone().lerp(Wb,e),carX:a.carX})); if(se>s){ s=se; uz=true; } if(ek) s=Math.max(s,ek.gecikme+ek.sure); const ef=ekFn(ek,s);
    const ocB=isgalDurum(b); st.push({ad,sure:s,uzadi:uz,cek:ek?ek.cek:null,oc:ocBirles(isgalDurum(a),ocB),ocSon:ocB,basla:()=>{ S.t.copy(a.t); S.u.copy(a.u); S.yuk=a.yuk; S.parmak=a.parmak; if(ek&&ek.basla) ek.basla(); },fn:e=>{ S.tcp.lerpVectors(a.tcp,b.tcp,e); if(ef) ef(e); },bitir:cb}); cur.tcp.copy(b.tcp); return s; }
  function kay(ad,x,cb,ek){ const a=snap(); let s=sureHesap(Math.abs(x-a.carX),HIZ.ray,HIZ.ivmeRay); if(ek) s=Math.max(s,ek.gecikme+ek.sure); const ef=ekFn(ek,s);
    const bK=snap(); bK.tcp.x+=x-a.carX; bK.carX=x; const ocB=isgalDurum(bK); st.push({ad,sure:s,x0:a.carX,x1:x,cek:ek?ek.cek:null,oc:ocBirles(isgalDurum(a),ocB),ocSon:ocB,basla:()=>{ S.t.copy(a.t); S.u.copy(a.u); S.yuk=a.yuk; S.parmak=a.parmak; if(ek&&ek.basla) ek.basla(); },fn:e=>{ const d=(x-a.carX)*e; S.carX=a.carX+d; S.tcp.copy(a.tcp); S.tcp.x+=d; if(ef) ef(e); },bitir:cb}); cur.tcp.x+=x-cur.carX; cur.carX=x; return s; }
  function don(ad,ax,deg,pivotT,s,cb){ const a=snap(), W0=Wof(a), Pv=W0.clone().addScaledVector(a.t,pivotT||0), rad=deg*Math.PI/180, Wat=th=>Pv.clone().add(ROT(W0.clone().sub(Pv),ax,th));
    const se=eklemSure(e=>({W:Wat(rad*e),carX:a.carX})); let uz=false; if(se>s){ s=se; uz=true; }
    st.push({ad,sure:s,uzadi:uz,basla:()=>{ S.yuk=a.yuk; S.parmak=a.parmak; },fn:e=>{ const th=rad*e; S.t.copy(ROT(a.t,ax,th)); S.u.copy(ROT(a.u,ax,th)); S.tcp.copy(tcpOf(Wat(th),S,a.yuk)); },bitir:cb});
    cur.t=TEMIZ(ROT(a.t,ax,rad)); cur.u=TEMIZ(ROT(a.u,ax,rad)); cur.tcp=tcpOf(Wat(rad),cur,a.yuk);
    { const m=snap(); m.t=ROT(a.t,ax,rad/2); m.u=ROT(a.u,ax,rad/2); m.tcp=tcpOf(Wat(rad/2),m,a.yuk); const ocB=isgalDurum(snap()), son=st[st.length-1]; son.oc=ocBirles(ocBirles(isgalDurum(a),isgalDurum(m)),ocB); son.ocSon=ocB; } return s; }
  function bekle(ad,s,fn,cb,basla){ st.push({ad,sure:s,basla,fn:fn||(()=>{}),bitir:cb}); return s; }
  function yuk(ad,yeni,fn){ const a=snap(), W=Wof(a); cur.tcp=tcpOf(W,cur,yeni); cur.yuk=yeni; st.push({ad,sure:0.05,basla:()=>{ const Wn=Wof(S); S.yuk=yeni; S.tcp.copy(tcpOf(Wn,S,yeni)); if(fn) fn(); },fn:()=>{}}); return 0.05; }
  function parmak(ad,acik,fn){ const a=snap(); st.push({ad,sure:HIZ.parmak,fn:e=>{ S.parmak=a.parmak+(acik-a.parmak)*e; },bitir:fn}); cur.parmak=acik; return HIZ.parmak; }
  function kapak(ad,tip,idx,hedef,fn,onBasla,cb){ const k=kapakAnim(tip,idx,hedef,fn,onBasla); st.push({ad,sure:k.sure,cek:k.cek,basla:k.basla,fn:k.fn,bitir:cb}); return k.sure; }
  function tasima(ad){ return mv(ad||'taşıma pozu',{tcp:V(cur.carX+300*yon,TR,TZ)}); }
  function park(ad){ return mv(ad||'park pozu',{tcp:parkTcp(cur.carX)}); }
  /* elle yazılan adım (spiral, geri çekme…): bitiş tcp'si + yanal pay verilir, işgal aralığı kaydedilir */
  function elle(step,bTcp,pay){ const a=snap(); cur.tcp.copy(bTcp); const oa=isgalDurum(a), ob=isgalDurum(snap()), o=ocBirles(oa,ob); o.lo-=(pay||0); o.hi+=(pay||0); step.oc=o; step.ocSon=ob; st.push(step); }
  const bolmeler=[]; function bol(ad){ bolmeler.push({i:st.length,ad}); }
  return {st,cur,yon,mv,kay,don,bekle,yuk,parmak,kapak,tasima,park,elle,snap,bol,bolmeler};
}

/* ================= GÖREV İNŞACILARI ================= */
/* ağza giriş: son 120 mm yavaş, öncesi orta hız */
function gir(B,ad,hedef,vson){ const dz=hedef.z-B.cur.tcp.z; if(Math.abs(dz)>200){ const ara=hedef.clone(); ara.z=hedef.z-Math.sign(dz)*120; B.mv(ad,{tcp:ara},HIZ.orta); B.mv(ad+' · son 120 yavaş',{tcp:hedef},vson||HIZ.ince); } else B.mv(ad,{tcp:hedef},vson||HIZ.ince); }

/* ortak: tepsi koy / al (el yatay, sap +z tarafında · pim ↔ dişi soket) */
function tepsiKoy(B,tray,ad,cx,cy,cz,cb,carx,ustten){ if(ustten) B.mv('yüksel · tepsi omuz üstünden geçecek',{tcp:V(B.cur.tcp.x,TR,TZ)}); B.kay('→ '+ad,carx===undefined?carFor(cx,cy,cz,B.yon):carx); if(ustten) B.mv(ad+': omuz üstünden karşıya',{tcp:V(cx,TR,TZ)}); B.mv(ad+': ağız hizası',{tcp:V(cx,cy+20,TZ)}); gir(B,ad+': içeri',V(cx,cy+20,cz)); B.mv(ad+': indir',{tcp:V(cx,cy,cz)},HIZ.mikro);
  B.bekle('pim çözülür',HIZ.pim); B.yuk('tepsi bırakıldı','bos',()=>{ S.tasi=null; tray.pos=V(cx,cy,cz); if(cb) cb(); }); B.mv(ad+': el çıkar',{tcp:V(cx,cy,TZ)},HIZ.orta); }
function tepsiAl(B,tray,ad,cx,cy,cz,cb,carx,ek){ B.kay('→ '+ad,carx===undefined?carFor(cx,cy,cz,B.yon):carx,null,ek); B.mv(ad+': ağız hizası',{tcp:V(cx,cy,TZ)}); gir(B,ad+': pim sokete',V(cx,cy,cz));
  B.bekle('pim kilitlenir',HIZ.pim); B.yuk('tepsi alındı','tepsi',()=>{ S.tasi=tray; if(cb) cb(); }); B.mv(ad+': kaldır',{tcp:V(cx,cy+20,cz)},HIZ.mikro); B.mv(ad+': çıkar',{tcp:V(cx,cy+20,TZ)},HIZ.orta); }

function cekmeceYani(K,pos,L,tercih){ const Wy=pos.y+L; let en=null; for(let off=100+R().taban/2; off<=600; off+=25) for(const cx of [K.x0-off,K.x1+off]){ if(cx<RAY_X[0]||cx>RAY_X[1]) continue;
    const k=ikq(V(pos.x,Wy,pos.z),cx), k2=ikq(V(pos.x,Wy+170,pos.z),cx); if(!k.ok||!k2.ok||Math.min(k.E.z,k2.E.z)<100||k.rr<200) continue; const skor=Math.abs(pos.x-cx)-(tercih&&tercih(cx)?3000:0); if(!en||skor<en.skor) en={cx,skor}; }
  return en?en.cx:null; }


/* pres / tabla: araba bu konumdayken top ağızdan içeri bırakılabilir mi? (bilek omuz eksenine yaklaşmaz, ön kol ağzın içinden geçer) */
function presErisir(cx){ const P=PRES(), by=P.plaka+100, pozlar=[V(P.cx,by,720),V(P.cx,by,120+YUK.top.L),V(P.cx,by,P.cz+YUK.top.L)];
  for(const W of pozlar){ const k=ikq(W,cx); if(!k.ok||k.rr<160||k.E.z<50) return false; if(W.z<0){ const t=k.E.z/(k.E.z-W.z), xc=k.E.x+t*(W.x-k.E.x), yc=k.E.y+t*(W.y-k.E.y); if(xc<P.x[0]+50||xc>P.x[1]-50||yc<P.y[0]+45||yc>P.y[1]-45) return false; } } return true; }
const gecen=B=>B.st.reduce((a,s)=>a+s.sure,0);
/* G1 · HAMUR: çekmeceden top → pres ağzından içeri (bantlı: alt plakanın · tablalı: tablanın tam ortasına) · hazirAt: pres / tabla bu andan önce boş değil → ağız önünde bekler */
function G_hamur(B,p,t0,hazirAt){ const P=PRES(), ballH={tip:'top',pos:p.topPos.clone(),icerik:''}, by=P.plaka+100, cp=p.carPres||carPres();
  const K=KOLON[p.kolon], yan=p.yan, sagda=yan>K.x1;
  const ac=kapakAnim('cek',p.kolon,1,e=>{ ballH.pos.z=p.topPos.z*e; },()=>{ S.cekI[p.kolon]=p.sira; ballH.pos.copy(p.topPos); ballH.pos.z=0; nesneGoster(ballH); }); ac.gecikme=gecikmeHesap(B.cur.carX,yan,K);
  B.tasima('taşıma pozu'); B.kay('→ çekmece '+p.kolon+(sagda?' (sağ)':' (sol)')+' · araba çekilince çekmece açılır',yan,null,ac);
  B.mv('çekmece yanı · el için boşluk',{tcp:V(B.cur.carX+(sagda?-300:300),B.cur.tcp.y,280)}); B.don('el dikey (parmaklar aşağı)',V(1,0,0),-90,0,0.9); B.yuk('kavrama modu','top');
  B.parmak('parmaklar açılır',120); B.mv('topun üstüne',{tcp:V(p.topPos.x,p.topPos.y+150,p.topPos.z)}); B.mv('in',{tcp:p.topPos.clone()},HIZ.ince);
  B.parmak('parmaklar kapanır · top kavrandı',85,()=>{ S.tasi=ballH; }); B.mv('kaldır',{tcp:V(p.topPos.x,p.topPos.y+150,p.topPos.z)},HIZ.ince);
  B.mv('yüksel · çekmece kapanır',{tcp:V(p.topPos.x,900,350)},null,null,kapakAnim('cek',p.kolon,0));
  B.don('el yatay · top önde',V(1,0,0),90,0,0.9);
  const ayniTaraf=(p.topPos.x-yan)*(P.cx-cp)>0;
  if(!ayniTaraf) B.mv('taşıma · robotun önüne açıl',{tcp:V(yan,by,railZ()+380-YUK.top.L)});
  B.bol(TABLA?'tablaya bırak':'prese bırak'); B.kay(cp===yan?'araba yerinde · pres buradan erişiliyor':'→ pres',cp); if(!ayniTaraf) B.mv('omuz önünden pres tarafına',{tcp:V(cp,by,railZ()+380-YUK.top.L)}); B.mv('pres ağzı önü',{tcp:V(P.cx,by,120)});
  const bek=hazirAt-(t0+gecen(B)); if(bek>0.05) B.bekle(TABLA?'tabla pres altına dönüyor · bekle':'pres boşalıyor · bekle',bek+0.3);
  gir(B,'ağızdan içeri · '+(TABLA?'tablanın':'alt plakanın')+' tam ortası',V(P.cx,by,P.cz));
  B.parmak('parmaklar açılır · top '+(TABLA?'tablada':'alt plakada'),120,()=>{ nesneSil(ballH); }); const birakT=t0+gecen(B);
  B.mv('el ağızdan çıkar',{tcp:V(P.cx,by,120)},HIZ.orta); B.parmak('parmaklar 70',70); B.yuk('boş el','bos');
  return birakT; }
/* G2 · KUTU: kutulama ağzında bekleyen tepsi + kapalı kutu → QR gözü SAĞ bölme → tepsi ağza geri */
function G_kutu(B,p,o,tray,t0,hazirAt){ const cy=KUT.trayY;
  B.tasima('taşıma pozu'); B.kay('→ kutulama ağzı',carFor(KUT.cx,cy,KUT.cz,1)); B.mv('kutulama: ağız hizası',{tcp:V(KUT.cx,cy,TZ)});
  const bek=hazirAt-(t0+gecen(B)); if(bek>0.05) B.bekle('kutu kapanıyor · bekle',bek+0.3);
  gir(B,'kutulama: pim sokete',V(KUT.cx,cy,KUT.cz)); B.bekle('pim kilitlenir',HIZ.pim);
  B.yuk('tepsi + kapalı kutu alındı','tepsi',()=>{ S.tasi=tray; if(p.kutuN) nesneSil(p.kutuN); tray.icerik='kutu'; }); const alT=t0+gecen(B);
  B.mv('kutulama: kaldır',{tcp:V(KUT.cx,cy+20,KUT.cz)},HIZ.mikro); B.mv('kutulama: çıkar',{tcp:V(KUT.cx,cy+20,TZ)},HIZ.orta);
  B.bol('kutu → QR'); const q=qrKapak[o.goz], kat=o.kutuSay||0, taban=q.y+30+47*kat, bx=q.k0+QR.kutuX, ust=q.y+215;
  B.kay('→ QR dolabı',carFor(bx,undefined,undefined,1)); B.mv('dönüş pozu · bilek z 755 · tepsi omuz üstünde',{tcp:V(bx,1150,255)}); B.don('180° DÖNÜŞ · pivot tepsi+el ortası',V(0,1,0),180,335,2.0);
  B.mv('QR: göz üstünde bekle (kapak süpürmesinin dışı)',{tcp:V(bx,ust,700)}); B.kapak('QR kapağı açılır','qr',o.goz,1);
  B.mv('QR: göz kotuna in',{tcp:V(bx,taban,700)},HIZ.orta); gir(B,'QR: kutu SAĞ bölmeye · arka duvara 15 kala',V(bx,taban,QR.kutuZ));
  { const a=B.snap(), b=a.tcp.clone(); b.z=700; const yeni={tip:'kutu',pos:V(bx,q.y+EL.KUTU_H/2+2+47*kat,QR.kutuZ),kapali:true,kapanma:1,icerik:'pide'};
    B.elle({ad:'tepsi geri çekilir · göz ağzındaki tek yönlü klape kutuyu tutar → kutu gözde kalır',sure:1.4,fn:e=>{ S.tcp.lerpVectors(a.tcp,b,e); if(e>.5&&tray.icerik==='kutu'){ tray.icerik=''; nesneGoster(yeni); o.nesneler.push(yeni); } }},b,0); }
  const teslimT=t0+gecen(B);
  B.mv('QR: yukarı çık',{tcp:V(bx,ust,700)}); B.kapak('QR kapağı kapanır','qr',o.goz,0);
  B.mv('dönüş pozu',{tcp:V(bx,1150,585)}); B.don('180° geri dönüş',V(0,1,0),-180,335,2.0);
  B.bol('tepsiyi ağza geri bırak'); tepsiKoy(B,tray,'kutulama ağzı',KUT.cx,cy,KUT.cz,null,carFor(KUT.cx,cy,KUT.cz,1));
  let geriT=t0; { let a=0; for(const s of B.st){ a+=s.sure; if(s.ad==='tepsi bırakıldı') geriT=t0+a; } }
  return {alT,teslimT,geriT}; }

/* G6 · içecek / tatlı: B MODÜLÜ · K3 ÜSTÜNDEKİ 2 KATLI ÇEKMECEDEN (pafta v7 yeri, v11'de geri geldi) → QR gözü SOL şerit
   kola: üstten kavranır (el dikey) → el +z'ye yatırılır, kutu yatık → şeridin DERİNİNE (sol ileri) · tatlı: yandan kavranır (el yatay +x, kap dik kalır) → şeridin ROBOT tarafına (sol arka) */
function G_icecek(B,o,tip){ const it=o[tip+'Stok'], c=it.pos, H={tip,pos:c.clone(),icerik:''}, q=qrKapak[o.goz], sx=q.k0+QR.serit, K=KOLON.KI;
  const ac=kapakAnim('cek','KI',1,e=>{ H.pos.z=c.z*e; },()=>{ S.cekI.KI=it.kat; H.yatik=false; H.pos.copy(c); H.pos.z=0; nesneGoster(H); });
  B.tasima('taşıma pozu · kol çekmece kotunun üstünde');
  if(tip==='kola'){ const cx=it.yan; ac.gecikme=gecikmeHesap(B.cur.carX,cx,K);
    B.kay('→ içecek çekmecesi (K3 üstü) · '+(it.kat+1)+'. kat · araba çekilince açılır',cx,null,ac);
    const yon=cx>K.x1?-300:300, Yk=c.y+170;                                   // araba çekmecenin hangi yanındaysa el o yanda döner · kaldırma kotu: kutu altı ön panelin (kot+134) üstünde
    B.mv('çekmece yanı · el çekmece üstü kotunda',{tcp:V(B.cur.carX+yon,1350,280)}); B.don('el dikey (parmaklar aşağı)',V(1,0,0),-90,0,0.9); B.yuk('üstten kavrama','kola'); B.parmak('parmaklar açılır',110);
    B.mv('kutunun üstüne',{tcp:V(c.x,Yk,c.z)}); B.mv('in · parmaklar kutunun üst 45 mm’sine',{tcp:c.clone()},HIZ.ince); B.parmak('parmaklar kapanır · kutu kavrandı',66,()=>{ S.tasi=H; }); B.mv('kaldır',{tcp:V(c.x,Yk,c.z)},HIZ.ince);
    B.mv('koridor ortasına çekil · çekmece kapanır',{tcp:V(B.cur.carX+yon,Yk,720)},null,null,kapakAnim('cek','KI',0)); if(yon<0) B.mv('omuz önünden QR tarafına',{tcp:V(B.cur.carX+300,Yk,720)});
    B.mv('dönüş pozu',{tcp:V(B.cur.carX+300,Yk,350)}); B.don('el QR yönüne yatar (kutu yatık · +z)',V(1,0,0),-90,0,1.0);
    B.bol('QR\'a götür'); B.kay('→ QR göz '+(o.goz+1)+' · sol şerit',Math.min(RAY_X[1],sx-100));
    B.mv('QR: göz üstünde bekle',{tcp:V(sx,q.y+250,722.5)}); B.kapak('QR kapağı açılır','qr',o.goz,1);
    B.mv('QR: şerit kotuna in',{tcp:V(sx,q.y+48,722.5)},HIZ.orta); gir(B,'QR: kola şeridin derinine (SOL İLERİ)',V(sx,q.y+48,QR.kolaZ));
    B.parmak('parmaklar açılır · kola 12 mm’den yatık bırakılır',82,()=>{ S.tasi=null; H.pos=V(sx,q.y+EL.KOLA_R+1,QR.kolaZ); H.yatik=true; o.nesneler.push(H); });
    B.mv('QR: el çıkar',{tcp:V(sx,q.y+48,722.5)},HIZ.orta); B.mv('QR: yukarı',{tcp:V(sx,q.y+250,722.5)}); B.kapak('QR kapağı kapanır','qr',o.goz,0);
    B.mv('dönüş pozu',{tcp:V(B.cur.carX+300,1000,722.5)}); B.don('el geri döner (aşağıdan −z’ye)',V(1,0,0),180,0,1.6); B.parmak('parmaklar 70',70); B.yuk('boş el','bos');
  } else { const cx=Math.min(RAY_X[1],c.x+YUK.tatli.L+330), Yt=c.y+140; ac.gecikme=gecikmeHesap(B.cur.carX,cx,K);      // araba çekmecenin SAĞINDA · el −x yönünde girer (kap dik kalır)
    B.kay('→ içecek çekmecesi (K3 üstü) · tatlı köşesi · '+(it.kat+1)+'. kat · araba çekilince açılır',cx,null,ac);
    B.mv('dönüş pozu',{tcp:V(cx-200,1000,280)}); B.don('el −x yönüne (yatay · kap dik kalır)',V(0,1,0),90,140,1.0); B.yuk('yandan kavrama','tatli'); B.parmak('parmaklar açılır',120);
    B.mv('kap hizası · çekmecenin sağı',{tcp:V(c.x+130,c.y,c.z)}); B.mv('kaba yanaş',{tcp:c.clone()},HIZ.ince); B.parmak('parmaklar kapanır · kap kavrandı',88,()=>{ S.tasi=H; }); B.mv('kaldır · kap altı ön panelin üstüne',{tcp:V(c.x,Yt,c.z)},HIZ.ince);
    B.mv('geri çek · çekmece kapanır',{tcp:V(cx-290,Yt,620)},null,null,kapakAnim('cek','KI',0));
    B.bol('QR\'a götür'); B.kay('→ QR göz '+(o.goz+1)+' · sol şerit',Math.min(RAY_X[1],Math.max(RAY_X[0],sx-200))); B.mv('el şerit hizasına · robotun önünden',{tcp:V(sx-90,Yt,620)}); B.don('el QR yönüne (+z)',V(0,1,0),90,140,1.0);
    B.mv('QR: göz üstünde bekle',{tcp:V(sx,q.y+250,710)}); B.kapak('QR kapağı açılır','qr',o.goz,1);
    B.mv('QR: şerit kotuna in',{tcp:V(sx,q.y+34,710)},HIZ.orta); B.mv('QR: tatlı şeridin robot tarafına (SOL ARKA)',{tcp:V(sx,q.y+34,QR.tatliZ)},HIZ.ince); B.mv('indir',{tcp:V(sx,q.y+31,QR.tatliZ)},HIZ.mikro);
    B.parmak('parmaklar açılır · tatlı bırakıldı',104,()=>{ S.tasi=null; H.pos=V(sx,q.y+EL.TATLI_H/2+1,QR.tatliZ); o.nesneler.push(H); });
    B.mv('QR: el çıkar',{tcp:V(sx,q.y+31,710)},HIZ.orta); B.mv('QR: yukarı',{tcp:V(sx,q.y+250,710)}); B.kapak('QR kapağı kapanır','qr',o.goz,0);
    B.mv('dönüş yüksekliği',{tcp:V(sx,985,710)}); B.don('el geri döner (−z)',V(0,1,0),180,140,1.6); B.parmak('parmaklar 70',70); B.yuk('boş el','bos');
  }
}

