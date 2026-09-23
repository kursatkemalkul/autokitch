// AUTOKITCH · TOPPING — CANLI SİMÜLASYON (sayfa içinde, sağdan açılan panel)
// Kemal: "neden başka bir sayfaya gidiyor? Tüm detayları ilk sayfada istiyorum; sadece sağda bir pop-up
// sayfa olsun, ona basınca animasyon açılsın ve ordan seçeyim. Kasetin de parçaları çalışsın, aktif olsun,
// kapansın vs." → TOPPING sayfasından ayrılmıyoruz: aynı görüntüleyici kutusunun içinde three.js sahnesi
// açılıyor, sağdan panel kayıyor. Kasetin helezonu, karıştırıcısı ve pompası gerçekten dönüyor; dozlanan
// ürün pidenin üstünde spiral iz olarak birikiyor.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as K from './makine_kodu.js?v=6';

const MM = 0.001;
const URUN_RENK = {                                   // dozlanan ürünün pide üstündeki rengi
  'KAŞAR_KABI': 0xf2d98a, 'KIYMA': 0x9c4a3a, 'KUŞBAŞI': 0x8c3f34,
  'KÜP_SUCUK': 0x8f2f2f, 'HARÇ_1': 0xa8402f, 'HARÇ_2': 0xc0392b,
};

let S = null;                                          // sahne durumu (bir kez kurulur)

export async function ac(kutu, dugme) {
  if (S) { S.goster(!S.acik); return; }
  dugme.textContent = 'yükleniyor…'; dugme.disabled = true;
  S = await kur(kutu);
  dugme.disabled = false;
  dugme.textContent = '■ SİMÜLASYONU KAPAT';
  S.goster(true);
}

async function kur(kutu) {
  // ---------- panel ----------
  const panel = document.createElement('div');
  panel.className = 'simp';
  panel.innerHTML = `
    <div class="simp-b">
      <h4>1 · Ürün seç</h4><div class="simp-u"></div>
      <div class="simp-c"><button class="bas">BAŞLAT</button><button class="dur">DUR</button></div>
      <h4>2 · Makine durumu</h4><div class="simp-d"></div><div class="simp-m"></div>
      <h4>3 · Çalışan kod — makine_kodu.js</h4><div class="simp-k"><pre></pre></div>
      <div class="simp-l"></div>
    </div>`;
  kutu.appendChild(panel);
  const q = s => panel.querySelector(s);
  const log = (t, c) => { const d = document.createElement('div'); if (c) d.className = c; d.textContent = t; q('.simp-l').appendChild(d); q('.simp-l').scrollTop = 1e6; };

  // ---------- sahne ----------
  const yer = document.createElement('div'); yer.className = 'simv'; kutu.appendChild(yer);
  const sahne = new THREE.Scene(); sahne.background = new THREE.Color(0x15181d);
  const kam = new THREE.PerspectiveCamera(38, 1, 0.05, 60);
  const ren = new THREE.WebGLRenderer({ antialias: true });
  ren.setPixelRatio(Math.min(2, devicePixelRatio));
  yer.appendChild(ren.domElement);
  const kon = new OrbitControls(kam, ren.domElement);
  sahne.add(new THREE.HemisphereLight(0xdfe7f2, 0x2a2f38, 1.15));
  const g1 = new THREE.DirectionalLight(0xffffff, 1.0); g1.position.set(1.4, 2.2, 1.6); sahne.add(g1);
  const g2 = new THREE.DirectionalLight(0xffffff, 0.35); g2.position.set(-1.2, 1.0, -1.4); sahne.add(g2);

  const M = await (await fetch('../hat3d/sim_makine.json?v=4')).json();
  K.kur(M, izle);

  // ASIL ÜRETİM MODELİ — sayfanın gösterdiği dosyanın ta kendisi (aynı URL → tarayıcı önbelleğinden
  // gelir, ikinci indirme yok). Kemal: "neden başka bir model geliyor, direkt modeli çalıştır."
  // Ayrı/kaba sim modeli KALDIRILDI. hat_montaj_v17 hareket eden paketleri AYRI DÜĞÜM yazıyor:
  //     TOPPING_MODUL__celik__ARABA · TOPPING_MODUL__sac__TABLA · KASET_KIYMA__pom__HELEZON
  // Malzeme adları değişmedi, o yüzden model-viewer sayfası bundan etkilenmiyor.
  const glb = await new GLTFLoader().loadAsync('../hat3d/modul_C.glb?v=30');
  const kok = glb.scene;
  const OFS = M.ofset;                                  // JSON ölçüleri modül-yerel, GLB makine koordinatında
  const mak = p => [p[0] + OFS[0], p[1] + OFS[1], p[2] + OFS[2]];

  const HAREKETLI = new Set(['ARABA', 'TABLA', 'HELEZON', 'KARISTIRICI']);
  const G = {};
  const agalar = []; kok.traverse(o => { if (o.isMesh) agalar.push(o); });
  for (const o of agalar) {
    const s = (o.name || '').split('__');
    if (s.length < 3) continue;                         // 2 parçalı ad = sabit gövde, etiket vb.
    const g = s[2];
    if (!HAREKETLI.has(g)) continue;                    // tanımadığın eki SABİT say (yoksa etiket düğümü
                                                        //  sahte gruba düşüp sahneden kayboluyordu)
    const ad = (g === 'HELEZON' || g === 'KARISTIRICI') ? g + '_' + s[0].replace(/^KASET_/, '') : g;
    (G[ad] = G[ad] || new THREE.Group()).add(o);        // .add eski ebeveynden çıkarır; ağlar dünya koordinatında
  }
  if (!G.ARABA || !G.TABLA) throw new Error('modul_C.glb hareketli paket taşımıyor — hat_montaj_v17 ile üretilmeli');

  function pivotla(obj, p) {
    const t = new THREE.Group();
    t.position.set(p[0] * MM, p[1] * MM, p[2] * MM);
    obj.position.set(-p[0] * MM, -p[1] * MM, -p[2] * MM);
    kok.add(t); t.add(obj); return t;
  }
  const ARABA = new THREE.Group(); kok.add(ARABA);
  const P = mak(M.tabla.pivot);

  // TEPSİ + PİDE modülün parçası değil (robot getirir) — ölçüleri sim_makine.json'dan, uydurma yok:
  // tabla Ø340 · tepsi 12 mm · hamur 8 mm · pide üst yüzü y=120 (ağız zonunun tavanı).
  // DİKKAT: pivotla() nesnenin position'ını EZİYOR (GLB ağları 0'da durur, dünya koordinatı geometrinin
  // içindedir). O yüzden diskin yerini de GEOMETRİYE gömüyoruz — yoksa pide tablanın altına düşer.
  function disk(r, kal, ym, renk, ruf) {
    const g = new THREE.CylinderGeometry(r * MM, r * MM, kal * MM, 72);
    g.translate(P[0] * MM, ym * MM, P[2] * MM);
    const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: renk, roughness: ruf, metalness: ruf < 0.5 ? 0.75 : 0.05 }));
    kok.add(m); return m;
  }
  // v20 · TEPSİ YOK. Hamur doğrudan ÇALIŞMA DİSKİNİN üstünde. Robot TOP halinde bırakır,
  // açıcı Ø280'e açar. Topun yarıçapı uydurma değil: açılmış pidenin hacminden geliyor
  // (V = π r² h → aynı hacimli küre), sim_makine.json · pide.top_r.
  const yDisk = M.pide.disk_ust + OFS[1];                 // çalışma diskinin üst yüzü
  const yPide = M.pide.ust_y + OFS[1];
  const pideAg  = disk(M.pide.yaricap, M.pide.hamur_k, yPide - M.pide.hamur_k / 2, 0xe8d6ad, 0.9);
  const topG = new THREE.SphereGeometry(M.pide.top_r * MM, 32, 24);
  topG.scale(1, 0.82, 1);                                  // top tezgâhta hafif yayılır
  topG.translate(P[0] * MM, (yDisk + M.pide.top_r * 0.82) * MM, P[2] * MM);
  const topAg = new THREE.Mesh(topG, new THREE.MeshStandardMaterial({ color: 0xead9b4, roughness: 0.95 }));
  kok.add(topAg);

  const TABLA = pivotla(G.TABLA, P), PIDE = pivotla(pideAg, P), TOP = pivotla(topAg, P);
  ARABA.add(TABLA, PIDE, TOP, G.ARABA);
  PIDE.visible = false;                                    // açılana kadar ortada yalnız top var

  // MOTOR ADI -> döndürülecek grup. Pompalı kasette ÜST mil (YC) pompa rotoru, ALT mil (CY) hazne paleti;
  // vidalı kasette tam tersi. Eskiden ikisi de "helezon = dozaj" sayılıyordu → pompa hiç dönmüyor, hazne
  // paleti doz hızıyla dönüyordu (Kemal: "sos kasetlerinin parçaları eksenleri kayık, bir yerlerde dönüyor").
  const MILLER = {};
  for (const y of M.yuvalar) {
    const KOT = { HELEZON: y.mil_helezon_y, KARISTIRICI: y.mil_karistirici_y };
    for (const [gAd, motor] of [[y.grup_doz, (y.pompa ? 'POMPA_' : 'HELEZON_') + y.kod],
                                [y.grup_karis, 'KARISTIRICI_' + y.kod]]) {
      const g = G[gAd + '_' + y.kod];
      if (g) MILLER[motor] = pivotla(g, mak([y.x, KOT[gAd], 0]));
    }
  }
  sahne.add(kok);

  // ---------- GERÇEKÇİ DÖKÜLME ----------
  // Ürün ağızdan çıkar, SERBEST DÜŞER, pideye çarpınca durur ve orada YIĞILIR. Uydurma sayı yok:
  //   çıkış hızı = debi / kesit  (sim_makine.json · cikis_hiz — sos 52 · kıyma 19 · kuşbaşı 7 mm/s)
  //   parça boyu = köprüleme kuralı D >= 3 x parça -> parça = D/3  (kuşbaşı 17,3 · küp sucuk 14,0 mm)
  //   düşme yolu = ağız y 160 -> pide üstü y 120 = 40 mm,  yerçekimi 9810 mm/s²
  const YER = 9810, YOGUNLUK = 1.05e-3;                 // mm/s² · g/mm³ [V]
  const UCAN_N = 1200, YIGIN_N = 14000;
  const HB_A = 72, HB_R = 20;                           // yığın yükseklik haritası: açı x yarıçap gözü
  const hMap = new Float32Array(HB_A * HB_R);
  const DR = M.pide.yaricap / HB_R, DA = 2 * Math.PI / HB_A;

  function parcaKur(n) {
    const g = new THREE.BoxGeometry(1, 0.62, 1);        // yassı tane: ürün pideye yayılır, bilye gibi durmaz
    const im = new THREE.InstancedMesh(g, new THREE.MeshStandardMaterial({ roughness: 0.82, metalness: 0.02 }), n);
    im.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    im.frustumCulled = false; im.count = 0;
    return im;
  }
  const ucanAg = parcaKur(UCAN_N); kok.add(ucanAg);     // havadakiler — dünya uzayında düşer
  const yiginAg = parcaKur(YIGIN_N); PIDE.add(yiginAg); // pideye konanlar — pide ile birlikte döner
  const ucanlar = [];
  let yiginAdet = 0, birikim = 0;
  const MT = new THREE.Matrix4(), MQ = new THREE.Quaternion(), MV = new THREE.Vector3(), MS = new THREE.Vector3();
  const YEKS = new THREE.Vector3(0, 1, 0), RENK = new THREE.Color();

  function dokumTemizle() {
    ucanlar.length = 0; yiginAdet = 0; birikim = 0;
    hMap.fill(0); ucanAg.count = 0; yiginAg.count = 0;
  }

  function tane(m, i, x, y, z, d, aci, renk) {
    MV.set(x, y, z); MQ.setFromAxisAngle(YEKS, aci); MS.set(d, d, d);
    m.setMatrixAt(i, MT.compose(MV, MQ, MS));
    m.setColorAt(i, RENK.setHex(renk));
  }

  function dokumKare(dt, y) {
    // --- ağızdan yeni parça çıkar (kütle korunur: g/s bölü parça kütlesi = parça/s)
    if (y) {
      const d = y.parca_mm, mp = d * d * d * 0.62 * YOGUNLUK;        // g/parça
      birikim += (y.doz_g / M.tabla.doz_sn) * dt / mp;
      const rA = Math.max(1, y.cikis_cap / 2 - d / 2);
      while (birikim >= 1 && ucanlar.length < UCAN_N) {
        birikim--;
        const t = Math.random() * 2 * Math.PI, rr = rA * Math.sqrt(Math.random());
        ucanlar.push({ x: y.x + OFS[0] + rr * Math.cos(t), y: y.agiz_y + OFS[1], z: y.agiz_z + rr * Math.sin(t),
                       vx: (Math.random() - 0.5) * 6, vy: -y.cikis_hiz, vz: (Math.random() - 0.5) * 6,
                       d: d * (0.8 + 0.4 * Math.random()), a: Math.random() * 6.28, renk: dozRenk });
      }
      if (birikim > 60) birikim = 60;                                 // kare atlarsa kuyruk şişmesin
    }
    // --- düşüş + pideye konma
    const cx = K.EKSEN.X + OFS[0];
    const ac = THREE.MathUtils.degToRad(K.EKSEN.TABLA), ct = Math.cos(ac), st = Math.sin(ac);
    for (let i = ucanlar.length - 1; i >= 0; i--) {
      const p = ucanlar[i];
      p.vy -= YER * dt; p.x += p.vx * dt; p.y += p.vy * dt; p.z += p.vz * dt;
      const ox = p.x - cx, oz = p.z - P[2];
      const u = ox * ct - oz * st, w = ox * st + oz * ct;             // pide yereli (yığın pideye sabit)
      const rr = Math.hypot(u, w);
      const ri = Math.min(HB_R - 1, Math.floor(rr / DR));
      const ai = ((Math.floor((Math.atan2(w, u) + Math.PI) / DA) % HB_A) + HB_A) % HB_A;
      const gz = ai * HB_R + ri;
      const yuzey = rr <= M.pide.yaricap ? yPide + hMap[gz] : -1e6;   // pidenin dışına düşen kaybolur
      if (p.y - p.d / 2 > yuzey) continue;
      ucanlar.splice(i, 1);
      if (rr > M.pide.yaricap || yiginAdet >= YIGIN_N) continue;
      tane(yiginAg, yiginAdet, u * MM, (yuzey + p.d * 0.31 - P[1]) * MM, w * MM, p.d * MM, p.a, p.renk);
      yiginAdet++; yiginAg.count = yiginAdet;
      yiginAg.instanceMatrix.needsUpdate = true;
      if (yiginAg.instanceColor) yiginAg.instanceColor.needsUpdate = true;
      hMap[gz] = Math.min(28, hMap[gz] + (p.d * p.d * p.d * 0.62) / (DA * (ri * DR + DR / 2) * DR));
    }
    // --- havadakileri çiz
    for (let i = 0; i < ucanlar.length; i++) {
      const p = ucanlar[i];
      tane(ucanAg, i, p.x * MM, p.y * MM, p.z * MM, p.d * MM, p.a, p.renk);
    }
    ucanAg.count = ucanlar.length;
    ucanAg.instanceMatrix.needsUpdate = true;
    if (ucanAg.instanceColor) ucanAg.instanceColor.needsUpdate = true;
  }

  // ---------- kamera ----------
  const TBY = (M.pide.ust_y + OFS[1]) * MM, TBZ = M.tabla.eksen_z * MM, TBX = (M.tabla.baslangic_x + OFS[0]) * MM;
  kon.target.set(TBX, TBY + 0.20, TBZ - 0.10);
  kam.position.set(TBX + 0.75, TBY + 0.95, TBZ + 2.30);
  let TAKIP = true;
  function boyut() {
    const r = yer.getBoundingClientRect();
    if (!r.width) return;
    kam.aspect = r.width / r.height; kam.updateProjectionMatrix(); ren.setSize(r.width, r.height);
  }
  addEventListener('resize', boyut);

  // ---------- kod paneli ----------
  const kaynak = await (await fetch('./makine_kodu.js?v=6')).text();
  const sat = kaynak.split('\n'), ISARET = {};
  sat.forEach((s, i) => { const m = s.match(/\/\*@(\w+)\*\//); if (m) ISARET[m[1]] = i; });
  q('.simp-k pre').innerHTML = sat.map((s, i) =>
    `<span class="l" data-i="${i}">${s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])) || ' '}</span>`).join('');
  let sonS = null;
  function vurgula(ad) {
    const i = ISARET[ad]; if (i === undefined) return;
    if (sonS !== null) q(`.simp-k [data-i="${sonS}"]`)?.classList.remove('ak');
    const e = q(`.simp-k [data-i="${i + 1}"]`) || q(`.simp-k [data-i="${i}"]`);
    if (e) {                                            // DİKKAT: scrollIntoView SAYFANIN kendisini kaydırıyordu
      e.classList.add('ak'); sonS = +e.dataset.i;       // (Kemal: "beni sürekli sayfada aşağı kaydırıyor").
      const kk = q('.simp-k');                          // yalnız kod kutusunun kendi kaydırmasını oynat.
      kk.scrollTop = e.offsetTop - kk.clientHeight / 2 + e.offsetHeight / 2;
    }
  }

  let dozRenk = 0xf2d98a, dozlaniyor = false;
  let dozT0 = 0, dozY = null;
  let acilma = -1;                                         // -1 kapalı · 0..1 açılma ilerlemesi
  function izle(o) {
    if (o.satir) vurgula(o.satir);
    if (o.kod) dozRenk = URUN_RENK[o.kod] || 0xf2d98a;
    if (o.faz === 'doz') {
      dozlaniyor = true;
      dozT0 = performance.now(); dozY = M.yuvalar.find(v => v.kod === o.kod) || null;
    }
    if (o.faz === 'bitti' || o.faz === 'basla') dozlaniyor = false;
    // v20 · HAMUR: yeni çevrimde TOP gelir, açıcı onu Ø280 pideye çevirir,
    // aktarmada pide banda geçer ve tabla boş kalır.
    if (o.yeniTepsi) { dokumTemizle(); dozY = null; acilma = -1; TOP.visible = true; TOP.scale.setScalar(1); PIDE.visible = false; }
    if (o.acildi) acilma = 0;
    if (o.aktarildi) { PIDE.visible = false; TOP.visible = false; dokumTemizle(); }
    if (o.mesaj) log(o.mesaj, o.faz === 'bitti' ? 'y' : (o.faz === 'basla' ? 'b' : ''));
  }

  // ---------- ürün düğmeleri ----------
  let secili = [];
  for (const [k, r] of Object.entries(K.RECETE)) {
    const b = document.createElement('button'); b.textContent = r.ad;
    b.onclick = () => {
      secili = r.adim.slice();
      panel.querySelectorAll('.simp-u button').forEach(x => x.classList.toggle('on', x === b));
      log('seçildi: ' + r.ad + ' → ' + r.adim.join(' + '), 'b');
    };
    q('.simp-u').appendChild(b);
  }
  q('.simp-u button').click();
  q('.bas').onclick = async () => {
    if (!secili.length) return;
    q('.bas').disabled = true; dokumTemizle();
    try { await K.urunYap(secili); } finally { q('.bas').disabled = false; }
  };
  q('.dur').onclick = () => { K.durdur(); log('DUR basıldı', 'b'); };

  const MOTADLAR = ['X', 'TABLA', ...M.yuvalar.flatMap(y => [(y.pompa ? 'POMPA_' : 'HELEZON_') + y.kod, 'KARISTIRICI_' + y.kod])];
  q('.simp-m').innerHTML = MOTADLAR.map(a => `<span data-m="${a}">${a.replace(/_/g, ' ')}</span>`).join('');

  // dozlanan miktar: helezon sabit devirde döndüğü için gram, geçen doz süresiyle doğru orantılı
  function dozGram() {
    if (!dozY) return 0;
    const u = Math.min(1, (performance.now() - dozT0) / 1000 / M.tabla.doz_sn);
    return dozY.doz_g * (dozlaniyor ? u : 1);
  }

  // ---------- kare ----------
  let onceki = performance.now(), acik = false;
  function kare() {
    requestAnimationFrame(kare);
    if (!acik) return;
    const t = performance.now(), dt = Math.min(0.05, (t - onceki) / 1000); onceki = t;
    K.kareIsle(dt);

    ARABA.position.x = (K.EKSEN.X - M.tabla.baslangic_x) * MM;
    const a = THREE.MathUtils.degToRad(K.EKSEN.TABLA);
    TABLA.rotation.y = PIDE.rotation.y = TOP.rotation.y = a;

    // AÇILMA: top yassılaşıp kaybolurken pide diski büyür (koniler yuvarlayarak açıyor)
    if (acilma >= 0 && acilma < 1) {
      acilma = Math.min(1, acilma + dt / M.acici.ac_sn);
      const u = acilma;
      PIDE.visible = true;
      PIDE.scale.set(0.18 + 0.82 * u, 1, 0.18 + 0.82 * u);
      TOP.scale.set(1 + 1.4 * u, Math.max(0.02, 1 - u), 1 + 1.4 * u);
      if (u >= 1) TOP.visible = false;
    }
    for (const ad in MILLER) {
      const m = K.MOTOR[ad] || K.MOTOR[ad.replace('HELEZON_', 'POMPA_')];
      if (m) MILLER[ad].rotation.z = THREE.MathUtils.degToRad(m.aci || 0);
    }

    // Dökülen yuvayı MAKİNE KODU söyler. Eskiden "en yakın yuva" alınıyordu; araba dozaj boyunca kaydığı
    // için yarı yolda komşu kaset daha yakın kalıyor ve ürün ÖBÜR kasetten dökülüyordu
    // (Kemal: "yan yana olan iki kasetten biri bitince öbüründen döküldü").
    const dok = K.DOZ_YUVA ? M.yuvalar.find(v => v.kod === K.DOZ_YUVA) : null;
    const y = dok || M.yuvalar.reduce((p, v) => Math.abs(v.x - K.EKSEN.X) < Math.abs(p.x - K.EKSEN.X) ? v : p);
    const r = Math.hypot(y.x - K.EKSEN.X, M.tabla.r_ic);
    dokumKare(dt, dok);

    if (TAKIP) {
      const hx = (K.EKSEN.X + OFS[0]) * MM, dx = hx - kon.target.x;
      if (Math.abs(dx) > 1e-5) { const u = Math.min(1, dt * 6); kon.target.x += dx * u; kam.position.x += dx * u; }
    }
    q('.simp-d').innerHTML =
      `<div class="sat"><span>X ekseni</span><b>${K.EKSEN.X.toFixed(1)} mm</b></div>` +
      `<div class="sat"><span>tabla açısı</span><b>${K.EKSEN.TABLA.toFixed(0)}°</b></div>` +
      `<div class="sat"><span>ağız → pide merkezi</span><b>${r.toFixed(1)} mm</b></div>` +
      `<div class="sat"><span>${dozlaniyor ? 'dozlanan yuva' : 'en yakın yuva'}</span><b>${(dozlaniyor && dozY ? dozY : y).urun}</b></div>` +
      `<div class="sat"><span>dozlanan</span><b>${dozGram().toFixed(0)} g</b></div>` +
      `<div class="sat"><span>tabla devri · doz</span><b>${M.tabla.rpm} dev/dk · ${M.tabla.doz_sn} s</b></div>`;
    panel.querySelectorAll('.simp-m span').forEach(s => s.classList.toggle('on', !!K.MOTOR[s.dataset.m]));

    kon.update(); ren.render(sahne, kam);
  }
  kare();
  log('hazır — ürün seç ve BAŞLAT', 'y');

  return {
    get acik() { return acik; },
    goster(v) {
      acik = v;
      yer.style.display = panel.style.display = v ? 'block' : 'none';
      kutu.classList.toggle('sim-on', v);
      if (v) { setTimeout(boyut, 30); onceki = performance.now(); }
    },
  };
}
