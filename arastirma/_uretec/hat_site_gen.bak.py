# -*- coding: utf-8 -*-
# AUTOKITCH — otonom/hat/ site üreteci (7 Eyl 2026)
# Hiyerarşi: index (DÜKKAN 3B: makine tek grup kırmızı + dolap/ekran/kod/service) → makine.html (istasyonlar + robot 3B) → birim sayfaları (aynı 6 başlık)
import io, os, shutil
ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH"
AR = os.path.join(ROOT, 'arastirma'); OUT = os.path.join(ROOT, 'otonom', 'hat'); IMG = os.path.join(OUT, 'img')
os.makedirs(IMG, exist_ok=True)

# ---------------- görseller ----------------
IMGS = {
 'ist1_store_detay_v4.png':'1_STORE/ist1_store_detay_v4.png','ist1_store_detay_v3.png':'1_STORE/ist1_store_detay_v3.png','ist1_store_detay_v2.png':'1_STORE/ist1_store_detay_v2.png',
 'ist2_pres_detay_v8.png':'2_PRESS/ist2_pres_detay_v8.png','ist2_pres_detay_v6.png':'2_PRESS/ist2_pres_detay_v6.png','ist2_pres_detay_v5.png':'2_PRESS/ist2_pres_detay_v5.png',
 'ist3_topping_detay_v27.png':'3_TOPPING/ist3_topping_detay_v27.png','ist3_topping_detay_v26.png':'3_TOPPING/ist3_topping_detay_v26.png','ist3_topping_detay_v25.png':'3_TOPPING/ist3_topping_detay_v25.png','ist3_topping_detay_v24.png':'3_TOPPING/ist3_topping_detay_v24.png','kap_geometri_v1.png':'3_TOPPING/kap_geometri_v1.png',
 'ist4_oven_detay_v5.png':'4_OVEN/ist4_oven_detay_v5.png','ist4_oven_detay_v4.png':'4_OVEN/ist4_oven_detay_v4.png','ist4_oven_detay_v3.png':'4_OVEN/ist4_oven_detay_v3.png','ist4_oven_detay_v2.png':'4_OVEN/ist4_oven_detay_v2.png',
 'kutu_istasyonu_teknik_v4.png':'5_PACK/kutu_istasyonu_teknik_v4.png',
 'teslim_dolabi_teknik_v2.png':'6_PICKUP/teslim_dolabi_teknik_v2.png','pickup_dolap_teknik_v1.png':'6_PICKUP/pickup_dolap_teknik_v1.png','siparis_ekrani_teknik_v2.png':'6_PICKUP/siparis_ekrani_teknik_v2.png','kiosk_siparis_ekrani_v1.png':'6_PICKUP/kiosk_siparis_ekrani_v1.png','kod_unitesi_teknik_v1.png':'6_PICKUP/kod_unitesi_teknik_v1.png',
 'robot_tepsi_el_v1.png':'8_ROBOT/robot_tepsi_el_v1.png','tepsi_hareket_analizi_v2.png':'8_ROBOT/tepsi_hareket_analizi_v2.png',
 'hat_on_gorunus_teknik_v51.png':'FULL_MAKINE/hat_on_gorunus_teknik_v51.png','hat_dis_kapak_gorunus_v2.png':'FULL_MAKINE/hat_dis_kapak_gorunus_v2.png','dukkan_plani_v7.png':'FULL_MAKINE/dukkan_plani_v7.png',
}
OLDIMG = os.path.join(ROOT,'otonom','img')
for dst,src in IMGS.items():
    p=os.path.join(AR,src)
    if os.path.exists(p): shutil.copy2(p, os.path.join(IMG,dst))
    else: print('YOK', src)
for f in ('kombine_el_detay.png','kutu_istasyonu_teknik_v3.png','picnic_kap_helezon.webp','picnic_kap_tarak.webp','picnic_tarak_detay.png','picnic_reload_pepp.png','picnic_istasyon.webp'):
    p=os.path.join(OLDIMG,f)
    if os.path.exists(p): shutil.copy2(p, os.path.join(IMG,f))

# ---------------- CSS ----------------
CSS = r'''
:root{--bg:#f5f7fa;--card:#fff;--ink:#0f1726;--mut:#68758a;--line:#dfe6f0;--blue:#2456c8;--green:#178a56;--red:#c0392b;--orange:#c47c18;--purple:#6b4fa8;--maxw:1120px;--font:"SF Pro Display","SF Pro Text",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);-webkit-font-smoothing:antialiased;line-height:1.55}
a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
.top{position:sticky;top:0;z-index:20;background:rgba(245,247,250,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.top .in{max-width:var(--maxw);margin:0 auto;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:14px;font-size:13.5px}
.crumb a{color:var(--mut)}.crumb span{color:var(--mut);margin:0 6px}.crumb b{color:var(--ink)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:28px 20px 60px}
h1{font-size:34px;letter-spacing:-.02em;margin:6px 0 4px;line-height:1.15}h1 .tag{display:inline-block;font-size:12px;letter-spacing:.08em;font-weight:700;padding:3px 9px;border-radius:999px;color:#fff;vertical-align:middle;margin-left:10px}
.lead{font-size:16px;color:var(--mut);max-width:820px;margin:0 0 18px}
.scene{position:relative;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;height:560px;margin:14px 0 10px}
.scene canvas{display:block;width:100%;height:100%}
.tip{position:absolute;pointer-events:none;background:rgba(15,23,38,.92);color:#fff;font-size:13px;font-weight:600;padding:6px 10px;border-radius:8px;transform:translate(12px,-30px);display:none;white-space:nowrap}
.hint{position:absolute;left:14px;bottom:12px;font-size:12px;color:var(--mut);background:rgba(255,255,255,.85);padding:4px 8px;border-radius:6px}
.legend{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 26px}
.legend a{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;font-size:13px;font-weight:600;color:var(--ink)}
.legend a:hover{border-color:var(--blue);text-decoration:none}.legend i{width:12px;height:12px;border-radius:3px;display:inline-block}
h2{font-size:20px;letter-spacing:-.01em;margin:34px 0 10px;padding-top:18px;border-top:1px solid var(--line)}h2 small{color:var(--mut);font-weight:500;font-size:13px;margin-left:8px}
h3{font-size:15px;margin:18px 0 6px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:10px 0}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:760px){.grid2{grid-template-columns:1fr}.scene{height:420px}}
.kv{display:grid;grid-template-columns:200px 1fr;gap:6px 14px;font-size:14px}.kv b{color:var(--mut);font-weight:600}
ol.steps{padding-left:22px;font-size:14.5px}ol.steps li{margin:6px 0}
table{width:100%;border-collapse:collapse;font-size:13.5px}th{text-align:left;color:var(--mut);font-weight:600;border-bottom:1px solid var(--line);padding:6px 8px}td{padding:7px 8px;border-bottom:1px solid #eef2f7;vertical-align:top}
.st{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px}.st.ok{background:#e6f5ec;color:var(--green)}.st.on{background:#fff3df;color:var(--orange)}.st.ac{background:#fde8e6;color:var(--red)}
figure{margin:12px 0}figure img{width:100%;display:block;border:1px solid var(--line);border-radius:12px;background:#fff}figcaption{font-size:12.5px;color:var(--mut);margin-top:6px}
.thumbs{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px}.thumbs a{display:block}.thumbs img{width:100%;border:1px solid var(--line);border-radius:8px;background:#fff}.thumbs span{display:block;font-size:12px;color:var(--mut);margin-top:3px}
.ver li{margin:4px 0;font-size:13.5px}.note{font-size:13px;color:var(--mut)}
.chip{display:inline-block;padding:2px 8px;border-radius:6px;font-size:12px;font-weight:700;color:#fff;margin-right:6px}
.foot{max-width:var(--maxw);margin:0 auto;padding:18px 20px 40px;font-size:12px;color:var(--mut);border-top:1px solid var(--line)}
'''

# ---------------- 3B sahne betiği ----------------
SCENE_JS = r'''
// AUTOKITCH hat/scene.js — basit kutu modeli, hover = grup vurgusu, tık = sayfa. Ölçüler cm. x: soldan sağa, y: önden (sokak) arkaya, z: yukarı.
function buildScene(el, items, opts){
  opts=opts||{}; const W=el.clientWidth, H=el.clientHeight;
  const scene=new THREE.Scene(); scene.background=new THREE.Color(0xf7f8fa);
  const cam=new THREE.PerspectiveCamera(38, W/H, 1, 6000); const c=opts.center||[210,132,90];
  const D=(opts.depth||264); cam.position.set(c[0]+(opts.camOff?opts.camOff[0]:0), c[2]+(opts.camOff?opts.camOff[2]:420), D/2+(opts.camOff?opts.camOff[1]:620));
  const ren=new THREE.WebGLRenderer({antialias:true}); ren.setPixelRatio(Math.min(devicePixelRatio,2)); ren.setSize(W,H); el.appendChild(ren.domElement);
  const ctr=new THREE.OrbitControls(cam, ren.domElement); ctr.target.set(c[0],c[2],D/2); ctr.enableDamping=true; ctr.maxPolarAngle=Math.PI/2.05; ctr.update();
  scene.add(new THREE.HemisphereLight(0xffffff,0xd9dde3,1.05)); const dl=new THREE.DirectionalLight(0xffffff,.55); dl.position.set(300,600,400); scene.add(dl);
  const grid=new THREE.GridHelper(1400,28,0xdde3ea,0xe9edf2); grid.position.y=-0.5; scene.add(grid);
  const meshes=[]; const byItem={};
  function toWorld(x,y,z){ return [x, z, (opts.depth||264)-y]; }   // y (derinlik) → -Z: sokak (y=0) kameraya yakın (Z=depth)
  items.forEach(it=>{
    byItem[it.id]={item:it,meshes:[]};
    (it.boxes||[]).forEach(b=>{
      const [x,y,z,w,d,h]=b; const geo=new THREE.BoxGeometry(w,h,d);
      const mat=new THREE.MeshStandardMaterial({color:new THREE.Color(it.color||'#cfd3d8'),roughness:.6,metalness:.05,transparent:!!it.opacity,opacity:it.opacity||1});
      const m=new THREE.Mesh(geo,mat); const p=toWorld(x+w/2,y+d/2,z+h/2); m.position.set(p[0],p[1],p[2]); m.userData.item=it; scene.add(m);
      const eg=new THREE.LineSegments(new THREE.EdgesGeometry(geo),new THREE.LineBasicMaterial({color:0x1d2430,transparent:true,opacity:it.opacity?0.25:0.55})); m.add(eg);
      if(it.href){meshes.push(m)} byItem[it.id].meshes.push(m);
    });
  });
  const tip=document.createElement('div'); tip.className='tip'; el.appendChild(tip);
  const ray=new THREE.Raycaster(); const mouse=new THREE.Vector2(); let hover=null;
  function setHover(it){
    if(hover===it) return;
    if(hover){ byItem[hover.id].meshes.forEach(m=>{m.material.color.set(hover.color||'#cfd3d8'); m.material.emissive.set(0x000000)}); }
    hover=it;
    if(hover){ byItem[hover.id].meshes.forEach(m=>{m.material.color.set(hover.hover||hover.color); m.material.emissive.set(hover.hover||hover.color); m.material.emissiveIntensity=.35}); el.style.cursor=hover.href?'pointer':'default'; }
    else el.style.cursor='default';
  }
  el.addEventListener('pointermove',e=>{
    const r=el.getBoundingClientRect(); mouse.x=((e.clientX-r.left)/r.width)*2-1; mouse.y=-((e.clientY-r.top)/r.height)*2+1;
    ray.setFromCamera(mouse,cam); const hit=ray.intersectObjects(meshes,false)[0];
    if(hit){ setHover(hit.object.userData.item); tip.style.display='block'; tip.style.left=(e.clientX-r.left)+'px'; tip.style.top=(e.clientY-r.top)+'px'; tip.textContent=hover.name+(hover.href?'  →':''); }
    else { setHover(null); tip.style.display='none'; }
  });
  el.addEventListener('pointerleave',()=>{setHover(null); tip.style.display='none'});
  let down=null; el.addEventListener('pointerdown',e=>{down=[e.clientX,e.clientY]});
  el.addEventListener('pointerup',e=>{ if(down&&Math.hypot(e.clientX-down[0],e.clientY-down[1])<6&&hover&&hover.href){ location.href=hover.href; } down=null; });
  window.addEventListener('resize',()=>{const W=el.clientWidth,H=el.clientHeight; cam.aspect=W/H; cam.updateProjectionMatrix(); ren.setSize(W,H)});
  (function loop(){ requestAnimationFrame(loop); ctr.update(); ren.render(scene,cam); })();
}
'''

# ---------------- ortak parçalar ----------------
COL = {'store':'#5b8def','press':'#e08a2e','topping':'#8e5bd6','oven':'#d94a3a','pack':'#d9b43a','robot':'#2456c8','makine':'#cfd3d8','dolap':'#178a56','ekran':'#2b2e33','kod':'#8a9199','service':'#c47c18','tezgah':'#b9946a'}
HEAD = '''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title><link rel="stylesheet" href="hat.css">%s</head><body>
<div class="top"><div class="in"><div class="crumb">%s</div><div><a href="../">← Store</a></div></div></div>
<div class="wrap">'''
FOOT = '''</div><div class="foot">AUTOKITCH · HAT · Yol C canlı tasarım defteri · kaynak: arastirma/ (DUZEN.md, PROBLEMLER.md, paftalar) · %s</div></body></html>'''
THREE = '<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script><script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script><script src="scene.js"></script>'
DATE='7 Eyl 2026'
def crumb(*parts):
    out=[]
    for i,(t,h) in enumerate(parts):
        out.append(('<b>%s</b>'%t) if h is None else ('<a href="%s">%s</a>'%(h,t)))
    return '<span>›</span>'.join(out)
def st(s):
    s=s.upper(); k='ok' if ('ÇÖZ' in s or 'KARAR' in s or 'DÜZELT' in s) else ('ac' if 'AÇIK' in s else 'on'); return '<span class="st %s">%s</span>'%(k,s)
def problems(rows):
    h='<table><tr><th style="width:44px">#</th><th>Problem</th><th style="width:110px">Durum</th><th>Çözüm / not</th></tr>'
    for r in rows: h+='<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td></tr>'%(r[0],r[1],st(r[2]),r[3])
    return h+'</table>'
def kv(rows): return '<div class="kv">'+''.join('<b>%s</b><span>%s</span>'%(a,b) for a,b in rows)+'</div>'
def steps(lst): return '<ol class="steps">'+''.join('<li>%s</li>'%s for s in lst)+'</ol>'
def fig(src,cap): return '<figure><img src="img/%s" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>'%(src,cap,cap)
def thumbs(lst): return '<div class="thumbs">'+''.join('<a href="img/%s" target="_blank"><img src="img/%s" loading="lazy"><span>%s</span></a>'%(s,s,c) for s,c in lst)+'</div>'
def sup(rows):
    h='<table><tr><th>Tedarikçi / ürün</th><th>Ne</th><th style="width:150px">Fiyat / durum</th></tr>'
    for r in rows: h+='<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>'%r
    return h+'</table>'
def ver(lst): return '<ul class="ver">'+''.join('<li>%s</li>'%s for s in lst)+'</ul>'
SIX=['Ne yapar · çalışma senaryosu','Özellikler · karar özeti','Teknik resimler','Tedarikçiler · fiyatlar','Soru işaretleri · açık konular','Sürüm geçmişi']
def page(fn,title,tag,color,crumbs,lead,sections,hero='',scripts='',extra_head=''):
    body=HEAD%(title,extra_head,crumbs)
    body+='<h1>%s<span class="tag" style="background:%s">%s</span></h1><p class="lead">%s</p>'%(title,color,tag,lead)+hero
    for i,(h,c) in enumerate(sections): body+='<h2>%d · %s</h2>'%(i+1,h)+c
    body+=scripts+FOOT%DATE
    io.open(os.path.join(OUT,fn),'w',encoding='utf-8').write(body); print('yazildi',fn)

io.open(os.path.join(OUT,'hat.css'),'w',encoding='utf-8').write(CSS); io.open(os.path.join(OUT,'scene.js'),'w',encoding='utf-8').write(SCENE_JS)

# ================= DÜKKAN (index) =================
DUKKAN_ITEMS = '''[
 {id:'zemin',name:'',color:'#eef1f5',boxes:[[0,0,-2,420,264,2]]},
 {id:'duvar',name:'',color:'#e3e6ea',opacity:.35,boxes:[[0,264,0,420,6,300],[-6,0,0,6,270,300],[420,0,0,6,270,300]]},
 {id:'on',name:'',color:'#e3e6ea',opacity:.12,boxes:[[0,-6,0,420,6,300]]},
 {id:'kapi',name:'Sokak kapısı 75×210 (eleman · kurye · ikmal)',color:'#b9c0c9',boxes:[[0,-6,0,75,6,210]]},
 {id:'pencere',name:'Tezgah penceresi 130×100 (sürme cam)',color:'#bfe0f5',opacity:.6,boxes:[[85,-6,100,130,6,100]]},
 {id:'duvar2',name:'İnce duvar 6 (2 sac + yalıtım)',color:'#d9c9ad',opacity:.55,boxes:[[0,84,0,296,6,220]]},
 {id:'makine',name:'MAKİNE — hat (5 istasyon) + robot',href:'makine.html',color:'#cfd3d8',hover:'#d94a3a',boxes:[[0,180,0,140,84,197],[140,180,0,70,84,197],[210,180,0,70,84,197],[280,180,0,70,84,197],[350,180,0,70,84,197],[60,130,0,300,10,8],[190,115,0,40,40,70],[204,129,70,12,12,90],[204,129,150,12,70,12]]},
 {id:'service',name:'SERVICE 70×84×197 + tezgah',href:'service.html',color:'#c47c18',hover:'#f0a030',boxes:[[222,0,0,70,84,197],[80,0,0,140,30,95]]},
 {id:'dolap',name:'TESLİM DOLABI 124×52×165 (12 dolap)',href:'dolap.html',color:'#178a56',hover:'#2ec27e',boxes:[[296,0,0,124,52,165]]},
 {id:'ekran',name:'SİPARİŞ EKRANI 45×14 (SERVICE sırtında)',href:'ekran.html',color:'#2b2e33',hover:'#5b6270',boxes:[[224,-14,85,45,14,104]]},
 {id:'kod',name:'KOD ÜNİTESİ 20×8×34',href:'kod.html',color:'#8a9199',hover:'#b8c0c9',boxes:[[272,-8,110,20,8,34]]}
]'''
MAKINE_ITEMS = '''[
 {id:'zemin',name:'',color:'#eef1f5',boxes:[[0,0,-2,420,180,2]]},
 {id:'store',name:'1 · STORE — soğuk depo 140×84×197',href:'store.html',color:'#5b8def',hover:'#8fb4ff',boxes:[[0,90,0,140,84,197]]},
 {id:'press',name:'2 · PRESS — hamur presi 70×84×197',href:'press.html',color:'#e08a2e',hover:'#f5b364',boxes:[[140,90,0,70,84,197]]},
 {id:'topping',name:'3 · TOPPING — malzeme dozajı 70×84×197',href:'topping.html',color:'#8e5bd6',hover:'#b48ef0',boxes:[[210,90,0,70,84,197]]},
 {id:'oven',name:'4 · OVEN — fırın + kesme + yağ 70×84×197',href:'oven.html',color:'#d94a3a',hover:'#f07a6c',boxes:[[280,90,0,70,84,197]]},
 {id:'pack',name:'5 · PACK — kutu açıcı 70×84×197',href:'pack.html',color:'#d9b43a',hover:'#f0cf6a',boxes:[[350,90,0,70,84,197]]},
 {id:'robot',name:'ROBOT — ray 300 + kol (16–20 kg sınıfı)',href:'robot.html',color:'#2456c8',hover:'#5b8def',boxes:[[60,40,0,300,10,8],[190,25,0,40,40,70],[204,39,70,12,12,90],[204,39,150,12,70,12]]}
]'''
def legend(items):
    return '<div class="legend">'+''.join('<a href="%s"><i style="background:%s"></i>%s</a>'%(h,c,n) for n,h,c in items)+'</div>'

genel_senaryo = steps([
 'Müşteri kaldırımdaki <a href="ekran.html">sipariş ekranından</a> ya da uygulamadan sipariş verir, ÖKC POS ile öder; fişte sipariş numarası ve 4 haneli dolap kodu yazar. Platform siparişleri (Yemeksepeti, Getir, Trendyol Go) entegratörle BEYİN\'e düşer.',
 'BEYİN reçeteyi kuyruğa alır; fırın BEKLEME (340 °C) ya da EKO (250 °C) konumundan hazırlanır. Robot <a href="store.html">STORE</a>\'dan taze hamur topunu pençeyle alır.',
 'Top <a href="press.html">PRESS</a>\'te tepsi içinde Ø29 ısıtmalı plakayla açılır; pide bundan sonra hep tepsidedir (Ø32, kulp 6).',
 'Robot tepsiyi <a href="topping.html">TOPPING</a> katlarına sürer; kaplar helezonla gramaj döker (kaşar, sucuk küp, kıyma, kuşbaşı); tepsi tepsi düzleminde dönmez, kaplar sabittir.',
 '<a href="oven.html">OVEN</a>: sadeyağ spreyi (4 ml), taş fırın 3–4 dk (Omake çift katlı, motorlu cam kapak), çıkışta kesme presi 4 parça.',
 '<a href="pack.html">PACK</a>: üstten beslemeli kutu açıcı kutuyu kalıpta 1 vuruşta açar; tepsi eğilir, 4 parça kutuya kayar; flaplar ve kapak kapanır.',
 'Robot kutuyu pençeyle <a href="dolap.html">TESLİM DOLABI</a>\'nın arka klapesinden boş dolaba iter; içecek ve tatlı STORE\'dan aynı dolaba konur. Kod aktif olur, SMS gider.',
 'Müşteri ya da kurye <a href="kod.html">kod ünitesine</a> PIN/QR girer; kapı açılır, alır; kapı kendiliğinden kapanır, dolap serbest kalır.',
 'Eleman haftada bir gelir: kaplar, kutu demetleri, yağ kabı; <a href="service.html">SERVICE</a> dolabı ve tezgah onun. Günlük kova ve tepsi yıkama.'])
index_sections=[
 ('Genel çalışma senaryosu — siparişten teslime', '<div class="card">'+genel_senaryo+'</div>'),
 ('Dükkan · özellikler ve karar özeti', '<div class="card">'+kv([('İç ölçü','420 × 264 = 11,1 m² (al-git, müşteri içeri girmez; kaldırımdan sipariş ve teslim)'),('Arka duvar','HAT 420: STORE 140 · PRESS 70 · TOPPING 70 · OVEN 70 · PACK 70, hepsi 84 derin, 197 yüksek'),('Robot koridoru','90 derin, ray 300 (x 60–360), eksen ince duvara 14, hat önüne 76'),('İnce duvar','6 cm (2 sac + yalıtım), x 0–296; tek kapı 70 kilitli, açılınca robot durur'),('Ön sıra (cephe hattı)','kapı 75 · tezgah 140×30 (pencere 130) · SERVICE 70×84 sırtı sokağa · teslim dolabı 124×52; ekran + kod SERVICE sırtında'),('Dolap arkası','32 + duvar payı 6 = 38 robot alanına açık (ince duvar dolap arkasında yok)'),('Robot erişimi','CRX-20iA/L 142: dolap dibi 119/132, TOPPING kap dibi çatalla 113, STORE/PACK uçları 111 ✓'),('Not','tezgah arkasında elemana 54 cm kalıyor (dar); ön zon 100 yapılırsa 11,8 m²')])+'</div>'),
 ('Teknik resimler', fig('dukkan_plani_v7.png','Dükkan planı v7 — plan + sokak cephesi (7 Eyl 2026)')+fig('hat_dis_kapak_gorunus_v2.png','Hat dış görünüş v2 — kapalı paneller, robot açıklıkları koyu')),
 ('Tedarikçiler · fiyatlar (genel)', '<div class="card">'+sup([('Fersah','PZP-400 pide/pizza presi (PRESS)','teklif alındı, bkz. PRESS'),('Omake / Cafemarkt','FPZ01.E21 çift katlı taş fırın (OVEN)','40.169 TL'),('Picnic (referans)','helezonlu kap + tarak dozaj mantığı (TOPPING)','referans'),('KioSelf · Onega · İnnova · Kardo','32" sipariş kiosku + ÖKC POS + fiş','50–120 bin TL (teklif)'),('pudo · Easy Point · Emanetmatik · Fitekno','kilit kartı, kabin (teslim dolabı)','özel yapım 60–90 bin TL'),('Fanuc CRX-20iA/L · Doosan H2017 · TM20','kobot 16–20 kg, menzil 142–170','teklif alınacak')])+'</div>'),
 ('Soru işaretleri · açık konular (hat geneli)', '<div class="card">'+problems([('G1','Robot kol arızası — hat durur','ÖNERİ VAR','yedek uç + servis sözleşmesi; eleman manuel teslim'),('G3','Elektrik kesintisi sipariş ortasında','ÖNERİ VAR','mini UPS yalnız BEYİN; fırın kapalı kalır, sipariş iade'),('G4','Kol kalibrasyonu kayarsa','ÖNERİ VAR','referans pimleri + kamera kontrolü'),('G5','Hijyen denetimi (belediye/tarım)','AÇIK','kapalı panel, yıkanabilir tepsi, eleman günlük temizlik'),('R-T3','Tepsi havuzu / yıkama (8–10 tepsi, ~80/gün)','AÇIK','bulaşık listesi SERVICE\'te'),('R-T4','Kol doluluğu ~%85 (103 sn/pide)','AÇIK','iki fırın katı + kutu ön hazırlığı ile pik 25–30/saat'),('⑦','Kol yükü 15,2 kg (kıyma kabı + kap + çatal), menzil ≥ 130','AÇIK','16–20 kg sınıfı kobot; CRX-20iA/L 142 / H2017 170 / TM20 130'),('⑤','Fersah Ø30 taban sorusu','AÇIK','tekrar sorulacak'),('①','STORE v5 (−18 kaset katı klapeli)','ÖNERİ VAR','Kemal onayı')])+'</div>'),
 ('Sürüm geçmişi', ver(['Dükkan v7 (7 Eyl): düz cephe, ön sıra SERVICE derinliğinde, 11,1 m²','Dükkan v5–v6 (7 Eyl): tek sıra cephe, kademeli deneme (reddedildi)','Dükkan v1–v4 (7 Eyl): kroki okuma denemeleri; v4 kroki birebir','HAT v51 (6 Eyl): PACK v4 kutu açıcı ile tüm hat; HAT v50: OVEN v5 tek yağ kabı; HAT v48: OVEN v3 kolon 70','HAT v44–v47 (4–5 Eyl): STORE v4, PRESS v8, TOPPING v25/v26, KONTROL kutusu','Yol C kararı (Ağu 2026): merkez mutfaksız, tek dükkân, bir kişilik hat']))]
index_hero='<div class="scene" id="s1"><div class="hint">sürükle: döndür · tekerlek: yakınlaştır · üstüne gel: birim · tıkla: sayfası</div></div>'+legend([('MAKİNE (hat + robot)','makine.html','#d94a3a'),('SERVICE + tezgah','service.html','#c47c18'),('Teslim dolabı','dolap.html','#178a56'),('Sipariş ekranı','ekran.html','#2b2e33'),('Kod ünitesi','kod.html','#8a9199')])
index_scripts='<script>buildScene(document.getElementById("s1"),%s,{depth:264,center:[210,132,50],camOff:[0,430,680]});</script>'%DUKKAN_ITEMS
page('index.html','DÜKKAN — HAT · Yol C','ÜST SAYFA','#1d2430',crumb(('Store','../'),('HAT',None)),'Tek dükkân, bir kişilik otonom pide hattı. 3B modelde makine tek gruptur (kırmızı); tıklayınca istasyonlara ayrılır. Diğer birimler doğrudan kendi sayfasına gider. Kutular gerçek ölçüde, ileride gerçek modellerle değişir.',index_sections,index_hero,index_scripts,THREE)

# ================= MAKİNE =================
makine_sections=[
 ('Ne yapar · çalışma senaryosu', '<div class="card"><p>Makine = arka duvardaki 5 istasyon + önündeki raylı robot. Bir pide için robot sırayla: STORE (hamur) → PRESS (tepsi, açma) → TOPPING (3 katta dozaj) → OVEN (sprey, pişirme, kesme) → PACK (kutu) → teslim dolabı. Pide press\'ten kutuya kadar tepsidedir; robot pideye dokunmaz. Kap, kutu, yağ ve hamur ikmali elemanın haftalık işidir.</p>'+steps(['Robot ray üzerinde 300 cm gider; her istasyonun robot açıklığı (klape) o an açılır, soğuk kabinler kapalı kalır.','Uç değiştirici PRESS altındadır: TEPSİ eli (kulp 6), PENÇE (hamur, kutu, içecek), ÇATAL (kap taşıma, forklift gibi).','Bir pide 4 dakikada bir çıkar; iki fırın katıyla pik 25–30/saat. Robot doluluğu ~%85.'])+'</div>'),
 ('Özellikler · karar özeti', '<div class="card">'+kv([('Kabin standardı','70 (STORE 140) × 84 derin × 197 yüksek; gövde 185 + ayak/plint 12; TOPPING, OVEN, PACK\'te ayak yerine plint'),('Toplam hat','420 cm; robot koridoru 90; ray 300'),('Robot','tek kol 16–20 kg sınıfı, menzil ≥ 142; en ağır yük kıyma kabı 7,5 + kap 5,7 + çatal 2,0 = 15,2 kg'),('Tepsi zinciri','pide Ø30 → tepsi Ø32 + kulp 6; PRESS plaka Ø29, OVEN hazne 40 (38 ✓), PACK kalıp 32,5'),('Kontrol','BEYİN (PICKUP panosunda): PLC I/O, fırın SSR + termokupl, kilit kartı, robot arayüzü; kiosk yalnız istemci'),('Kapalı panel','cam yok; robot açıklıkları klape; eleman kapıları turuncu (dış görünüş v2)')])+'</div>'),
 ('Teknik resimler', fig('hat_on_gorunus_teknik_v51.png','HAT v51 — tüm istasyonlar ön + üst görünüş, KONTROL kutusu (6 Eyl 2026)')+fig('hat_dis_kapak_gorunus_v2.png','Dış görünüş v2 — kapalı paneller')),
 ('Tedarikçiler · fiyatlar', '<div class="card">'+sup([('Fanuc CRX-20iA/L','kobot 20 kg, menzil 1418','teklif alınacak'),('Doosan H2017','kobot 20 kg, menzil 1700','teklif alınacak'),('Techman TM20','kobot 20 kg, menzil 1300','sınırda'),('7. eksen ray','lineer ray 3 m, servo','entegratör'),('Entegratör','kabinler, klapeler, pano, devreye alma','teklif')])+'<p class="note">İstasyon bazlı tedarikçiler her istasyonun sayfasında.</p></div>'),
 ('Soru işaretleri · açık konular', '<div class="card">'+problems([('⑦','Kol yükü 15,2 kg + menzil ≥ 142 — kobot sınıfı','AÇIK','CRX-20iA/L / H2017; ya da kıyma 2 günlük dolum (6 kg)'),('⑫','Robot tepsi eli v2 (kulp 6 + çatal)','AÇIK','çizilecek'),('⑬','Çatal ucu: 2 lama 16×12 × 50 + sırt plakası','ÖNERİ VAR','haftada ≈ 14 kap değişimi + 4 STORE→ALT'),('R-T2','Sıcak tepsi ile uç','ÖNERİ VAR','kulp ısı köprüsü kesik, paslanmaz'),('G4','Kalibrasyon kayması','ÖNERİ VAR','pim + kamera')])+'</div>'),
 ('Sürüm geçmişi', ver(['HAT v51 (6 Eyl): PACK v4','HAT v50/v49: OVEN v5/v4 (kesme presi OVEN\'e taşındı)','HAT v48: OVEN v3, kolon 70, hat 420','HAT v46–v47 (5 Eyl): TOPPING v25/v26, STORE v5 öneri, 8 ajanlı denetim','HAT v44 (4 Eyl): tüm istasyonlar + KONTROL','HAT v22–v43 (Ağu): yerleşim ve kabin standardı denemeleri']))]
makine_hero='<div class="scene" id="s2"><div class="hint">sürükle: döndür · üstüne gel: istasyon · tıkla: sayfası</div></div>'+legend([('1 STORE','store.html',COL['store']),('2 PRESS','press.html',COL['press']),('3 TOPPING','topping.html',COL['topping']),('4 OVEN','oven.html',COL['oven']),('5 PACK','pack.html',COL['pack']),('ROBOT','robot.html',COL['robot'])])
makine_scripts='<script>buildScene(document.getElementById("s2"),%s,{depth:180,center:[210,90,70],camOff:[0,400,430]});</script>'%MAKINE_ITEMS
page('makine.html','MAKİNE — hat + robot','5 İSTASYON + ROBOT','#d94a3a',crumb(('Store','../'),('HAT','index.html'),('Makine',None)),'Arka duvardaki beş istasyon ve önündeki raylı robot. Her istasyon kendi rengiyle; tıklayınca o istasyonun sayfası açılır.',makine_sections,makine_hero,makine_scripts,THREE)

# ================= İSTASYONLAR =================
def unit(fn,title,tag,color,lead,sen,ozel,res,ted,sor,ver_,parent=('Makine','makine.html')):
    page(fn,title,tag,color,crumb(('Store','../'),('HAT','index.html'),parent,(title.split(' — ')[0],None)),lead,list(zip(SIX,[sen,ozel,res,ted,sor,ver_])))

unit('store.html','1 · STORE — soğuk depo','140 × 84 × 197',COL['store'],'Hamur topları, içecek, tatlı ve donmuş TOPPING kapları. İki soğutma grubu, tam çekmeceli kapaksız kasa; robot çekmeceyi pençeyle çeker.',
 '<div class="card">'+steps(['Üstte +3 °C bölüm: sol modül 4 içecek çekmecesi (7 kanal) + 1 L çekmecesi; sağ modül 8 taze hamur çekmecesi (20 top, çukurlu tepsi 53×65).','Altta −18 bandı: sol modülde klapeli KASET KATI (4 donmuş TOPPING kabı 14×68×24, robot çatalla önden alır — v5 önerisi), altında 4 donmuş hamur çekmecesi (20 top).','Robot sipariş gelince taze çekmeceyi 70 cm tam açar, pençeyle topu alır, PRESS\'e götürür. Gece donmuş toplar taze bölüme taşınır (çözülme senkronu).','Eleman haftada 1: hamur tepsileri, içecek, tatlı; donmuş kapları kaset katına sürer.'])+'</div>',
 '<div class="card">'+kv([('Soğutma','2 grup: −18 (1/3 HP) ve +3 (1/4 HP), bölme 28, üstten servis'),('Çekmeceler','17 çekmece + 1 klapeli kaset katı; PU 60/80, ray 12,7, 70 tam açılım; kapak yok'),('Yatay ayırıcı','PU 80, z 69–77'),('Kaset katı (v5)','z 40–69 sol modül: 4 kap 14×68×24 yan yana (4×14 + 3×1 + 0,5 = 59,5 ✓), L raf, klape 6'),('Kapasite','taze 8 × 20 = 160 top; donmuş 4 × 20 = 80 top; içecek 4 × 7 kanal × 11 kutu')])+'</div>',
 fig('ist1_store_detay_v4.png','STORE v4 — alt buzluk 6 çekmece, tam çekmeceli kasa (4 Eyl 2026)')+thumbs([('ist1_store_detay_v3.png','v3'),('ist1_store_detay_v2.png','v2')]),
 '<div class="card">'+sup([('Soğutma grubu','1/3 HP −18 + 1/4 HP +3, yatay kompresör','entegratör / Klimasan tipi'),('Çekmece rayı','12,7 mm tam açılım, 40 kg','Hettich / Accuride'),('PU panel','60/80 mm sandviç','yerli')])+'</div>',
 '<div class="card">'+problems([('S1','Çekmece/raf motoru sıkışırsa robot bekler','ÖNERİ VAR','akım limiti + 2. deneme + alarm'),('S2','Servis kapağı açık kalırsa soğuk kaçar','ÇÖZÜLDÜ','kapak yok, çekmece; sensör'),('S3','Donmuş top zamanında çözülmezse','ÇÖZÜLDÜ','gece taşıma, 6 saat çözülme'),('S4','Elektrik kesintisi — soğuk zincir','ÖNERİ VAR','PU kütle + 4 saat tolerans, alarm'),('S5','Yanlış/boş çukurdan alma','ÇÖZÜLDÜ','sayaç + kamera'),('①','v5 kaset katı onayı','ÖNERİ VAR','Kemal')])+'</div>',
 ver(['v5 öneri (5 Eyl): −18 kaset katı üstte, klapeli, 4 kap sol modül','v4 (4 Eyl): alt buzluk, 19 çekmece, gerçek kalınlıklar','v1–v3 (Ağu): üst buzluk, kapaklı denemeler']))

unit('press.html','2 · PRESS — hamur presi','70 × 84 × 197',COL['press'],'Fersah PZP-400 pide/pizza presi: top tepsi içinde Ø29 ısıtmalı plakayla açılır. Üstte kova ve kol boşluğu, altta uç yuvaları ve tepsi rafı.',
 '<div class="card">'+steps(['Robot tepsiyi alt plakaya bırakır (tepsi Ø32 rafta bekler), pençeyle hamur topunu tepsiye koyar.','Üst plaka Ø29 ısıtmalı iner, 8–12 sn basar; hamur tepsi bordürüne çarpmaz.','Robot tepsiyi kulpundan alır, TOPPING\'e gider. Pres alt plakası zeminden ~90.','Uç değiştirme: PRESS altındaki yatay yuvalarda pençe ve çatal; kolda tepsi eli.','Kova 30 L (kapaksız, poşetli, öne çekilir): eleman her gün boşaltır; huni yok, pençe bırakır.'])+'</div>',
 '<div class="card">'+kv([('Makine','Fersah PZP-400, 64×80×95, 170 kg, 3,5 kW 220 V, zeminde'),('Plaka','üst Ø29 ısıtmalı (Ø40 → Ø29 kesildi), alt ısıtmalı'),('Üst bölge (v8)','sol yarı kova 30 L + 14 cm kol boşluğu; sağ yarı boş 35×59×84'),('Alt bölge','uç yuvaları 14 (pençe · çatal 50 derinlemesine · boş) + tepsi rafı 8 (2 yan yana + 1 kolda)'),('Açık','Fersah cevabı: CP-330 36 cm açar, PLC olur; Ø30 yuvarlak taban tekrar sorulacak')])+'</div>',
 fig('ist2_pres_detay_v8.png','PRESS v8 — kova + kol boşluğu, uç yuvaları, tepsi rafı')+thumbs([('ist2_pres_detay_v6.png','v6'),('ist2_pres_detay_v5.png','v5')]),
 '<div class="card">'+sup([('Fersah PZP-400','pide/pizza presi, PLC uyumlu','teklif/PDF alındı (26 Ağu)'),('Fersah CP-330','alternatif, max 36 cm','sorulacak'),('Fersah PZR-250','konveyör pres (reddedildi)','—')])+'</div>',
 '<div class="card">'+problems([('P1','Top sıcak plakaya yapışırsa','ÖNERİ VAR','teflon plaka + un/yağ; tepsi kaymaz'),('P2','Top ortalanmadan bırakılırsa','ÖNERİ VAR','tepsi çukur merkezi + kamera'),('P3','Şekil bozuk (yırtık/kalın kenar)','ÇÖZÜLDÜ','ısı + süre reçetesi'),('P4','Rezistans arızası','ÖNERİ VAR','termokupl izleme, alarm'),('P5','Uç takılamazsa (kilit arızası)','AÇIK','yedek yuva + manuel'),('⑤','Fersah Ø30 taban','AÇIK','tekrar sorulacak')])+'</div>',
 ver(['v8 (4 Eyl): sol kova + kol boşluğu, sağ boş, altta uç yuvaları ve tepsi rafı','v5–v6: uç cepleri, çöp çekmecesi','v1–v4 (Ağu): Fersah yerleşimi']))

unit('topping.html','3 · TOPPING — malzeme dozajı','70 × 84 × 197',COL['topping'],'Picnic tipi kaplar: POM helezon + çubuk tarak, şeffaf PC gövde, kapalı boru ucu ve menteşeli kapak. 3 kat × 2 kap, altta 8 kap yedek/çözülme rafı, dipte soğutma.',
 '<div class="card">'+steps(['Tepsi robot tarafından katın 14 cm\'lik dozaj boşluğuna sürülür (tepsi düzlemleri 158 / 117 / 76). Her tarif tek düzlemde: kat 1 kaşar A + sucuk küp, kat 2 kaşar B + park, kat 3 kıyma kavurma + kuşbaşı sote.','Kap helezonu döner (gramaj = devir; 123 cm³/dev), malzeme kapalı boru ucundaki tek ağızdan (5×4,5) tepsiye düşer; helezon durunca akış durur (vidalı besleyici mantığı). Tarak köprülenmeyi kırar.','Kap ALT rafta soğuk bekler (2 sıra × 4 L raf, dipte 1/12 HP grup, plint ızgara). Robot ÇATAL ile kabı kızaklarından önden alır, forklift gibi taşır: gir 50 → kaldır 0,5 → çek 70.','Ağız altındaki menteşeli kapak taşıma sırasında kapalıdır; yalnız TOPPING katındaki raf pimi kapağı 90° açar.','Eleman haftada 1: dolu kapları STORE kaset katına ve ALT rafa sürer, boşları alır. Robot haftada ≈ 14 kap değişimi yapar.'])+'</div>',
 '<div class="card">'+kv([('Kap (v27)','dış 14×68×24 (+kızak 2), PC 5 mm şeffaf; daire duvar R 6,5 göbek z 14, boğaz 7,6, yalak R 3,8; POM helezon Ø70 hatve 50 boy 66 + tırtıllı topuz → yaylı soket'),('Tarak','göbek + omurga + 4 çubuk Ø6 (r 57/43/29/14), tarak-duvar payı ≥ 0,45'),('Ağız','kapalı boru y 62–67, tek ağız 5×4,5 altta; menteşeli PC kapak + burulma yayı; raf pimi Ø8 yalnız TOPPING katında'),('Kızaklar','±5 (çatal aralığı 10), cep 2×1,4; ön çekme dudağı 1,5×3'),('Kapasite','12,5 L: kaşar 5,1 kg 1,1 gün (2 kap 2,3) · kıyma 7,5 kg 2,6 gün · sucuk 6,9 kg 5,7 gün · kuşbaşı 4,3 kg 3 gün; boş kap 5,7 kg'),('Yerleşim (v25)','3 kat × 2 kap (x 20–34 / 36–50), kat 27 + boşluk 14; ALT 74 = soğutma 20 + 2 × 27 raf; evaporatör sol kanal; derinlik 10+68+2+4 = 84'),('Bant kuralı','ağız merkezi yan duvara ≥ 27 (tepsi 16 + spiral 11), arka duvara ≥ 31')])+'</div>',
 fig('ist3_topping_detay_v27.png','TOPPING v27 — kapalı boru ucu, menteşeli kapak, raf pimi, eleman/robot dizileri')+fig('ist3_topping_detay_v26.png','v26 — Picnic tipi kap: daire duvar, POM helezon, çubuk tarak')+thumbs([('ist3_topping_detay_v25.png','v25 yerleşim (çatal, L raf, STORE kaset katı)'),('ist3_topping_detay_v24.png','v24 tek kap tipi'),('kap_geometri_v1.png','kap geometrisi'),('picnic_kap_helezon.webp','Picnic: helezonlu kap'),('picnic_kap_tarak.webp','Picnic: tarak'),('picnic_tarak_detay.png','Picnic: tarak detayı'),('picnic_reload_pepp.png','Picnic: yeniden dolum ekranı')]),
 '<div class="card">'+sup([('Picnic Works (referans)','otomatik topping istasyonu, helezon + tarak kapları','model referansı, satın alma yok'),('POM helezon','Ø70 hatve 50, işleme','yerli torna/CNC'),('PC gövde','5 mm polikarbonat, bükme/yapıştırma','yerli'),('Soğutma','1/12 HP yatay grup + evaporatör','entegratör')])+'</div>',
 '<div class="card">'+problems([('T1','Sucuk batonu pide ortasında biterse','ÖNERİ VAR','KÜP sucuk, dilimleme yok'),('T2','Kaşar rendesi köprülenir','ÖNERİ VAR','tarak + prototip'),('T3','Kavurma yağlanıp vidaya yapışır','ÖNERİ VAR','soğuk kap + PARÇA kavurma'),('T4','Gramaj sapması','ÖNERİ VAR','devir sayacı + tartı kalibrasyonu'),('T7','Kuşbaşı çiğ pişmez','ÖNERİ VAR','sote/kavrulmuş vakumlu'),('T11','Kaşar topaklanma','ÖNERİ VAR','2 pozisyon 2,3 gün'),('T12','Robot kap takası — kobot yükü, kulp','AÇIK','çatal + 16–20 kg kobot'),('v27','Yayıcı plaka mı spiral süpürme mi · gramaj prototipi · PC çizilme · 2 soket mi tek motor mu','AÇIK','prototip')])+'</div>',
 ver(['v27 (5 Eyl): kapalı boru ucu + tek ağız + menteşeli kapak + raf pimi, kızak ±5, kapasite 12,5 L','v26 (5 Eyl): Picnic tipi kap (daire duvar, POM helezon, tarak, PC)','v25 (5 Eyl): çatal + cepli kızak + L raf + STORE −18 kaset katı','v24 (4 Eyl): tek kap tipi, 3 kat, üst görünüm','v12–v23 (Ağu–Eyl): revolver (reddedildi), sabit dizilim, kaset formları, dozaj v1–v5','v1–v11: hazne kulesi ve kaset kurguları']))

unit('oven.html','4 · OVEN — fırın · kesme · sadeyağ','70 × 84 × 197',COL['oven'],'Omake FPZ01.E21 çift katlı taş fırın, motorlu cam kapaklar; altta sadeyağ spreyi (tek standart kap, pompa arka duvarda) ve kesme presi.',
 '<div class="card">'+steps(['Fırın gece KAPALI; açılış −20 dk ÖN ISITMA; servis boyunca BEKLEME 340 °C, 20 dk sipariş yoksa EKO 250 (→340 ≈ 3 dk = pide hazırlık süresi). "Kat hazır" = taş ≥ set −15 °C; 2. kat yalnız pik.','Robot tepsiyi sprey nişine sokar (altı boş), 90° koni nozül 4 ml sadeyağ (0,5 sn), çeker.','Motorlu kapak açılır, tepsi taşa konur (kulp 6 → 38 ≤ 40), 3–4 dk sabit sıcaklık/süre; kapak açılır, robot alır.','Kesme presi: tepsi zemin plakasına dayanır, bıçak yıldızı (2 × 28, 4 parça) 24 V aktüatörle iner (0,85–1,1 kN), robot yalnız kulpu tutar.','Sadeyağ: tek standart kap (yağ versiyonu, helezonsuz) sol slotta, 12 L = 30 gün; pompa arka duvarda; şamandıra 4 gün kala uyarır; eleman ayda 1 kapanışta değiştirir (dolapta sabaha erir).'])+'</div>',
 '<div class="card">'+kv([('Fırın','Omake FPZ01.E21: 64×60×56, 57 kg, 4,8 kW 400 V, 2 hazne 40×40×10, 400 °C, 2 camlı kapak + ayrı termostatlar'),('Kapak motoru','24 V lineer aktüatör + 2 switch + akım limiti; SSR + termokupl retrofit'),('Zonlar (v5, zeminden)','plint 12 / pano 20 / KESME 50 / YAĞ+SPREY 30 (kap 15 | tepsi 34 | boş 15, sıcak dolap 42 °C) / fırın 56 / plenum+fan 12 / filtre 5 / yedek 12 = 197'),('Havalandırma','plint girişi → yan/arka kanal → plenum → fan 140 m³/h → yağ filtresi + aktif karbon → üst ızgara (bacasız); yan 3 cm yalıtım (sol TOPPING +3, sağ PACK karton)'),('Yağ','4 ml/pide, 0,4 L/gün; tek kap 12 L = 30 gün, dolu 14,1 kg; 24 V dişli pompa 0,5 L/dk, ısıtmalı hat Ø6, çek valf'),('Kapasite','tek kavite 12–15/saat, iki kavite 25–30')])+'</div>',
 fig('ist4_oven_detay_v5.png','OVEN v5 — tek yağ kabı, sprey ortada, kesme presi (6 Eyl 2026)')+thumbs([('ist4_oven_detay_v4.png','v4 iki kap + kesme presi'),('ist4_oven_detay_v3.png','v3 kartuş + havalandırma'),('ist4_oven_detay_v2.png','v2 Omake seçimi + tank')]),
 '<div class="card">'+sup([('Omake FPZ01.E21 (Cafemarkt)','çift katlı taş fırın 64×60×56','40.169 TL'),('Atalay APF-40-2 / APF-40-1','çift / tek katlı','49.077 / 35.526 TL'),('Empero EMP.4','tek katlı 52×52','37.830 TL'),('Karacasan dijital 30×4','7" LCD 99 program','55.656 TL'),('Konveyör (Senoven SM-1100, Empero, Moretti T64E)','bant fırın','283–371 bin TL — reddedildi'),('Effeuno P134H · Zanolli · TurboChef · Ovention','yurt dışı seçenekler','€799 – ithalat'),('Sadeyağ ünitesi','24 V dişli pompa + ısıtmalı hat + nozül (entegratör)','8–12 bin TL'),('Gold Medal 2496 / Alibaba dispenser','hazır ısıtmalı yağ pompası','~1.300 $ / 185 $')])+'</div>',
 '<div class="card">'+problems([('O1','Pide yanarsa / az pişerse','ÖNERİ VAR','reçeteli süre + kamera renk kontrolü'),('O2','Motorlu kapak açılmazsa','ÖNERİ VAR','switch + 2. deneme + alarm'),('O3','Peş peşe pişirmede taş soğur','DÜZELTİLDİ','3 kW fırın 4 dk döngüde kendini yeniler'),('O6','Gece açık kalmasın','ÖNERİ VAR','KAPALI / ÖN ISITMA / BEKLEME / EKO / PİŞİRME'),('O4','Nozül tıkanması','ÇÖZÜLDÜ','gün sonu mini-CIP'),('O5','Koku/duman','ÇÖZÜLDÜ','fan + yağ filtresi + karbon'),('F-T2','Delikli tepside alt kabuk taş kadar çıtır mı','ÖNERİ VAR','pilot'),('F-T3','Tepsi malzemesi ısı döngüsü','AÇIK','paslanmaz/alu pilot'),('O8–O10','Yağ kabı: eleman değiştirir, tek kap, kuru bağlantı tipi','KARAR','CPC gıda tipi kaplin seçilecek')])+'</div>',
 ver(['v5 (6 Eyl): tek standart yağ kabı, sağ slot boş','v4 (6 Eyl): 2 standart kap + pompa arka duvarda + sprey ortada + KESME presi OVEN\'e','v3 (6 Eyl): kartuş 4 L, niş altı boş, plenum/fan/filtre, yan yalıtım, kolon 70','v2 (6 Eyl): Omake seçimi, kontrol mantığı, sprey ünitesi, stok, satın alma','v1 (Ağu): fırın kabini + tank']))

unit('pack.html','5 · PACK — kutu açıcı','70 × 84 × 197',COL['pack'],'Üstten beslemeli kutu açıcı: açık kutu yığını üstte (84 cm = 525 kutu), alttan vakumla çekilir, kalıptan 1 vuruşta açılır, plakaya yükselir; pide kayar, kapak kapanır, robot alır.',
 '<div class="card">'+steps(['AL: plunger 48 cm yukarı çıkar, 6 vantuz yığının en alt kutusuna yapışır.','İN: eksen aşağı; blank tutucu raylardan bükülerek sıyrılır, plakaya yatar.','KATLA: taban 4 cm pencereden çekilir; 4 duvar kırımdan kalkar, köşe tırnakları plowla yan duvarın içine kıvrılır. Kapak plakada düz kalır.','YÜKSEL: eksen 4 cm yukarı; kutu plakaya oturur (z 60). HAZIR.','PİDE: robot tepsiyi ön duvarın üstünde eğer, 4 parça kutuya kayar.','KAPAK: 3 flap parmağı flapları 90° kaldırır; U kol kapağı 180° çevirir; flaplar ve ön dil içeri girer.','VER: eksen 6 cm daha kalkar; robot pençe yanlardan tutar, teslim dolabına götürür. Çevrim ≈ 15 sn.'])+'</div>',
 '<div class="card">'+kv([('Kutu','32×32×4 köşe tırnaklı tepsi tipi; blank 40×76, E-dalga 1,6 mm, 115 g (TR standart 24–40 kare; 33\'lük kalıp da olur: 41×78)'),('Şarjör','84 cm (z 104–188) = 525 kutu; 80 pide: 3 gün 38 cm garanti · 5 gün 64 hedef · dolu 6,6 gün; 7 gün 90 sığmaz'),('Dikey eksen','bilyalı vida 1605 + 2 ray, NEMA 23, strok 48, 25 cm/s, ≥ 500 N; plunger 31,6 + 6 vantuz Ø40; vakum pompası 24 V 30 L/dk (kompresör yok)'),('Kalıp','pencere 32,5, duvar 4,5, köşe plowları; arka: orta ray + 3 flap parmağı (servo) + U kol (24 V redüktör)'),('Zonlar','plint 12 / pano 18 / step+vakum 15 / boyunduruk 10 / kalıp 5 / yükleme 44 / şarjör 84 / üst 9 = 197'),('Vantuz payı','dolu yığın 60 kg: gerek 257 N, vantuz 528 N → pilot 40 cm ile başlar')])+'</div>',
 fig('kutu_istasyonu_teknik_v4.png','PACK v4 — üstten beslemeli kutu açıcı (6 Eyl 2026)')+thumbs([('kutu_istasyonu_teknik_v3.png','v3 şarjör 116 (eleman katlar)')]),
 '<div class="card">'+sup([('Kutu üreticisi','özel bıçak kalıbı, köşe tırnaklı, baskılı','yerli oluklu mukavva'),('Vantuz + vakum pompası','6 × Ø40 körüklü, 24 V diyafram','Schmalz / Çin'),('Lineer eksen','bilyalı vida 1605 + NEMA 23','yerli'),('Kutu açma makinesi (referans)','Çin pnömatik pizza kutusu makinesi','video referansı')])+'</div>',
 '<div class="card">'+problems([('K5','Kutular üstte, altta katlansın, 3–7 gün','ÖNERİ VAR','v4 tasarımı'),('K2','Şarjörden kutu gelmezse / çift','ÖNERİ VAR','blank sensörü, 2. çekme, kalınlık sensörü'),('K3','Kapak tam kapanmazsa','ÖNERİ VAR','sensör + robot pençe yedek'),('P-T1','İtici dilimleri dağıtır','ÇÖZÜLDÜ','tepsi eğilir, kesim izli iner'),('—','Blank bıçak kalıbı · flap kapanma güvenilirliği · vantuz pilotu','AÇIK','pilot')])+'</div>',
 ver(['v4 (6 Eyl): üstten beslemeli kutu açıcı, vakum plunger + kalıp','v3 (4 Eyl): şarjör 116 (eleman katlar), bıçak yıldızı yatay','v1–v2 (Ağu): kesim + kutu istasyonu']))

unit('robot.html','ROBOT — ray + kol + uçlar','16–20 kg · menzil ≥ 142',COL['robot'],'Tek kol, 300 cm ray, üç uç: tepsi eli, pençe, çatal. Pideye dokunmaz; pide press\'ten kutuya kadar tepsidedir.',
 '<div class="card">'+steps(['Ray koridor boyunca 300 cm (x 60–360), eksen ince duvara 14, hat önüne 76; robot koridoru kapalı, tek kilitli kapı.','TEPSİ ELİ: kulplu tepsi Ø32 (kulp 6) robotun kilitli aksesuar ucu; tepsi PRESS, TOPPING katları, sprey nişi, fırın, kesme presi, PACK plakası arasında taşınır.','PENÇE: hamur topu, kutu (yanlardan), içecek ve tatlı.','ÇATAL: 2 lama 16×12 mm × 50 cm + sırt plakası ≈ 2 kg; kabı kızaklarından önden alır: gir 50 → kaldır 0,5 → çek 70 (5° yatık taşıma).','Uç değiştirici PRESS kabininin altında (yatay yuvalar). Haftalık: ≈ 14 kap değişimi + 4 STORE→ALT taşıma (gece).'])+'</div>',
 '<div class="card">'+kv([('Sınıf','16–20 kg kobot; en ağır yük kıyma kabı 7,5 + kap 5,7 + çatal 2,0 = 15,2 kg'),('Menzil','dükkan v7: dolap dibi 119/132, TOPPING kap dibi çatalla 113, STORE/PACK 111 → ≥ 142'),('Adaylar','Fanuc CRX-20iA/L 142 · Doosan H2017 170 · Techman TM20 130 (sınırda) · UR16e 90 ✗'),('Doluluk','≈ %85 (103 sn/pide)'),('Güvenlik','kapalı koridor, kapı açılınca durur; müşteri hiçbir noktadan ulaşamaz')])+'</div>',
 fig('robot_tepsi_el_v1.png','Robot tepsi ucu v1 — pide press\'ten kutuya kadar tepside')+fig('tepsi_hareket_analizi_v2.png','Tepsi hareket analizi v2')+thumbs([('kombine_el_detay.png','kombine el detayı (eski)')]),
 '<div class="card">'+sup([('Fanuc CRX-20iA/L','20 kg, 1418 mm','teklif alınacak'),('Doosan H2017','20 kg, 1700 mm','teklif alınacak'),('Techman TM20','20 kg, 1300 mm','sınırda'),('7. eksen','lineer ray 3 m','entegratör'),('Uç değiştirici','pnömatiksiz mekanik kilit','Schunk / yerli')])+'</div>',
 '<div class="card">'+problems([('⑦','Kol yükü + menzil — kobot seçimi','AÇIK','CRX-20iA/L ya da H2017'),('⑫','Tepsi eli v2 (kulp 6 + çatal)','AÇIK','çizilecek'),('R-T1','Pideye doğrudan temas / hizalama','ÇÖZÜLDÜ','tepsi'),('R-T2','Sıcak tepsi ile uç','ÖNERİ VAR','ısı köprüsü kesik'),('R-T3','Tepsi havuzu / yıkama','AÇIK','8–10 tepsi'),('R-T4','Kol doluluğu %85','AÇIK','çevrim optimizasyonu')])+'</div>',
 ver(['Dükkan v7 (7 Eyl): ray 300, erişim kontrolü CRX ile ✓','v25/v27 (5 Eyl): ÇATAL ucu + kızak ±5','4 Eyl: tepsi eli v1, tepsi hareket analizi v2','Ağu: kombine el, ray üstünde tek kol kararı']))

unit('dolap.html','TESLİM DOLABI — PICKUP','124 × 52 × 165 · 12 dolap',COL['dolap'],'Cephede 12 dolap (2 × 6). Ön kapı müşteri: yaylı gizli menteşe + amortisör, kendiliğinden kapanır. Arka klape robot. Isıtıcı yok.',
 '<div class="card">'+steps(['Pide hazır olunca BEYİN boş dolap seçer, arka mıknatıs kilit açılır; robot içecek/tatlıyı sol bölmeye, kutuyu pençeyle iterek koyar; klape yayla kapanır; IR "kutu var".','Kod aktif olur: kendi app müşterisine SMS/QR, platform müşterisi ve kuryeye sipariş numarasının son 4 hanesi.','Müşteri kod ünitesine girer; kilit açılır, LED yeşil, kapı açılır; alır; kapı 3 sn\'de kendiliğinden kapanır ve kilitlenir; IR boş → dolap serbest.','20 dk geçince "soğuyor" SMS, 45 dk geç listesi; gün sonu eleman boşaltır.'])+'</div>',
 '<div class="card">'+kv([('Sayı','20 sipariş/saat pik × 12 dk bekleme = 4 ort., %95 8, +2 geç = 10 gerek → 12 (150 pide/güne kadar)'),('Dolap içi','56×36×16: sağ 3 pide üst üste (13,2), sol 20: 1 L şişe yatık + tatlı 12×12 ya da 2 kutu; 4+ pide → 2 dolap tek kod'),('Kabin','124×165×52: plint 15 + pano 25 (BEYİN PC, kilit kartı) + 6 × 20 + üst 5; derinlik kapı 2 + PU 2 + iç 36 + klape 8 + çerçeve 2 + pay 2'),('Ön kapı','58×18, 2 mm 304, gizli yaylı menteşe ×3 + amortisör, yaylı elektrikli dil 5 kN, 10 mm bindirme, tutamak oyuk, reed sensör, LED; cam yok'),('Arka klape','üst menteşe, içeri açılır, yay + mıknatıs kilit; ön kapıyla interlock'),('İç','PU 20 mm, çıkarılabilir taban tepsisi, IR sensör, Ø8 buhar deliği ×3; ısıtıcı yok (15 dk kuralı)')])+'</div>',
 fig('teslim_dolabi_teknik_v2.png','Teslim dolabı v2 — ön / yan kesit / üst (7 Eyl 2026)')+thumbs([('pickup_dolap_teknik_v1.png','v1 hesap + kod akışı')]),
 '<div class="card">'+sup([('pudo · Easy Point · Kargopark · Zelfbox · Emanetmatik · Fitekno · kutu.tech','TR kargo dolabı (tek taraflı)','özel yapım için kilit kartı/kiosk'),('Apex OrderHQ Array · Hatco Minnow Pod','yurt dışı yemek dolabı (pass-through, ısıtmalı seçenek)','ithalat, pahalı'),('Öneri','kabin entegratörden + 12 × 12 V kilit + 16 kanal kilit kartı (KR-CU16) + IR','60–90 bin TL')])+'</div>',
 '<div class="card">'+problems([('D1–D3','sayı, boyut, arka kapak/ısıtıcı','ÖNERİ VAR','v2'),('D4','Platform kodu, kurye','ÖNERİ VAR','kod BEYİN üretir; entegratör API\'de sipariş no doğrulanacak'),('D5','Robot adresleme','ÖNERİ VAR','tablo + 12 sabit XYZ + IR'),('D7','Kapak açık / çöp','AÇIK','sensör 20 sn, eleman haftalık'),('D10','Kendiliğinden kapanma, vandalizm','ÖNERİ VAR','v2 kapı')])+'</div>',
 ver(['v2 (7 Eyl): 124×165×52, kendiliğinden kapanan kapı, vandalizm','v1 (7 Eyl): 140×197×60, hesap, kod akışı, satın alma']),parent=('Dükkan','index.html'))

unit('ekran.html','SİPARİŞ EKRANI — kiosk','45 × 104 × 14 · duvar tipi',COL['ekran'],'32" dokunmatik, ÖKC entegre POS, 80 mm fiş, 2D okuyucu. SERVICE dolabının sokak yüzüne asılı, BEYİN yok (LAN istemci).',
 '<div class="card">'+steps(['MENÜ: kaşarlı · sucuklu · kıymalı · kuşbaşılı · karışık (foto + fiyat).','ÜRÜN: adet, ekstra; içecek ve tatlı önerisi.','SEPET: tutar, hazır süresi 5–8 dk, yerinde al / kurye ile.','TELEFON (isteğe bağlı): SMS için; vermezse kod fişte.','ÖDEME: temassız kart, yemek kartı, QR ödeme; nakit yok.','FİŞ + KOD: sipariş no + 4 haneli dolap kodu + süre; hazır olunca dolap no ekranda yanar.'])+'</div>',
 '<div class="card">'+kv([('Gövde','2 mm 304, 45×104×14, duvara asılı, z 85–189; ön yüzde vida yok; cam 6 mm temperli IK10'),('Ekran','32" portre PCAP, 40×71, 1080×1920, merkez z 150'),('POS','ÖKC entegre (Ingenico Move 2500 / PAX A920 tipi) çelik yuvada 20° eğik, z 93–107'),('Yazıcı','80 mm termal kiosk yazıcısı, kesici; rulo servis kapağından'),('Diğer','2D okuyucu, kamera, hoparlör, mini PC i5/8 GB, LAN + 220 V duvar içinden'),('Fiş','perakende satışta ÖKC zorunlu; kağıtsız e-Arşiv seçeneği mali müşavire')])+'</div>',
 fig('siparis_ekrani_teknik_v2.png','Sipariş ekranı v2 — ön / yan / üst (7 Eyl 2026)')+thumbs([('kiosk_siparis_ekrani_v1.png','v1 cephe + akış')]),
 '<div class="card">'+sup([('KioSelf','yerli üretim self servis kiosk','teklif'),('Onega Zenyo KSK-3200','32", i5, 2D okuyucu, 80 mm yazıcı','teklif'),('İnnova · Kardo POS · Novem · PandaX · Menulux · Posgo · robotPOS','kiosk + yazılım','50–120 bin TL'),('Ingenico / PAX / Hugin','ÖKC entegre POS','banka')])+'</div>',
 '<div class="card">'+problems([('D8','Sipariş ekranı ayrı, kuryeyi bloke etmesin','ÖNERİ VAR','ayrı birim, SERVICE sırtında'),('D9','ÖKC / fiş, kağıtsız','AÇIK','mali müşavir'),('—','Yazılım–BEYİN API','AÇIK','sipariş JSON, dolap no geri')])+'</div>',
 ver(['v2 (7 Eyl): duvar tipi 45×104×14, gövde yok','v1 (7 Eyl): 40×197 gövdeli kiosk (reddedildi)']),parent=('Dükkan','index.html'))

unit('kod.html','KOD ÜNİTESİ — dolap açma','20 × 34 × 8 · duvar tipi',COL['kod'],'7" ekran + metal PIN pad + 2D okuyucu + kamera. Yalnız kod girişi, 3 saniyelik iş. SERVICE sırtında, dolabın yanında.',
 '<div class="card">'+steps(['MÜŞTERİ: SMS kodu ya da fişteki 4 hane → dolap açılır, LED yanar, ekranda "Dolap 7".','KURYE: "Kurye" tuşu → sipariş numarasının son 4 hanesi → dolap açılır.','Yanlış 3 deneme → 2 dk kilit; kamera her açılışta 10 sn kayıt.'])+'</div>',
 '<div class="card">'+kv([('Gövde','2 mm 304, 20×34×8, z 110–144; cam 6 mm IK10; tuşlar paslanmaz IK09, IP65'),('İç','RPi tipi kontrolcü, LAN ile BEYİN\'e; kilit kartı dolabın panosunda'),('Yerleşim','SERVICE sırtında, ekranın sağında; ekran merkezi z 130, tuşlar z 115–126')])+'</div>',
 fig('kod_unitesi_teknik_v1.png','Kod ünitesi v1 — ön / yan / üst'),
 '<div class="card">'+sup([('Vandal-proof metal PIN pad','IK09 IP65','Çin / Storm Interface'),('2D okuyucu modülü','cam arkası','Honeywell / Çin'),('RPi + 7" ekran','kontrolcü','—')])+'</div>',
 '<div class="card">'+problems([('D4','Kod kaynağı (platformlar üretmiyor)','ÖNERİ VAR','BEYİN üretir')])+'</div>',
 ver(['v1 (7 Eyl)']),parent=('Dükkan','index.html'))

unit('service.html','SERVICE + TEZGAH','70 × 84 × 197 · tezgah 140 × 30',COL['service'],'Elemanın dolabı: UPS, yangın tüpü, ambalaj demetleri, temizlik. Sırtı sokağa (ekran ve kod ünitesini taşır), kapısı tezgah zonuna. Tezgah sokağa bakan sürme camlı pencere.',
 '<div class="card">'+steps(['SERVICE: üst raf teknik (mini UPS yalnız BEYİN, yangın tüpü, priz); orta raflar ambalaj (kutu demetleri ≈ 5 gün); alt bölme temizlik (kilitli, mop); poşet ve çöp poşeti çekmecesi.','Tezgah: eleman kaldırımdaki müşteriye yardım eder, iade/şikâyet, büyük sipariş; nakit yok.','Eleman haftalık ziyaret: kaplar (TOPPING/STORE), kutu demetleri (PACK), yağ kabı (OVEN); günlük kova ve tepsi yıkama (bulaşık listesi).'])+'</div>',
 '<div class="card">'+kv([('Dolap','70×84×197, sırtı sokağa: 32" sipariş ekranı + kod ünitesi bu yüzde; kapısı batıya (tezgah zonu)'),('Tezgah','140×30, pencere 130×100 (eşik 100, sürme cam); eleman şeridi 54 (dar; ön zon 100 önerisi)'),('Ön zon','84 derin = SERVICE; kapı 75 solda (eleman, kurye, ikmal); robot koridoruna kilitli kapı 70')])+'</div>',
 fig('dukkan_plani_v7.png','Dükkan planı v7 — SERVICE ve tezgah cephe hattında'),
 '<div class="card">'+sup([('Paslanmaz dolap','70×84×197 raflı, kilitli alt bölme','yerli'),('Mini UPS','yalnız BEYİN için','—')])+'</div>',
 '<div class="card">'+problems([('—','Eleman şeridi 54 cm dar','AÇIK','ön zon 100 → 11,8 m²'),('R-T3','Tepsi yıkama','AÇIK','bulaşık listesi')])+'</div>',
 ver(['Dükkan v7 (7 Eyl): SERVICE cephe hattında, ekran + kod sırtında','Dükkan v1–v6: konum denemeleri']),parent=('Dükkan','index.html'))
print('OK')
