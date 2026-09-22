// AUTOKITCH · TOPPING — CANLI SİMÜLASYON (sayfa içinde, sağdan açılan panel)
// Kemal: "neden başka bir sayfaya gidiyor? Tüm detayları ilk sayfada istiyorum; sadece sağda bir pop-up
// sayfa olsun, ona basınca animasyon açılsın ve ordan seçeyim. Kasetin de parçaları çalışsın, aktif olsun,
// kapansın vs." → TOPPING sayfasından ayrılmıyoruz: aynı görüntüleyici kutusunun içinde three.js sahnesi
// açılıyor, sağdan panel kayıyor. Kasetin helezonu, karıştırıcısı ve pompası gerçekten dönüyor; dozlanan
// ürün pidenin üstünde spiral iz olarak birikiyor.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as K from './makine_kodu.js?v=3';

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

  const M = await (await fetch('../hat3d/sim_makine.json?v=1')).json();
  K.kur(M, izle);
  const glb = await new GLTFLoader().loadAsync('../hat3d/sim_topping_v1.glb?v=1');
  const kok = glb.scene, G = {};
  kok.traverse(o => { if (o.name && !o.name.includes('.')) G[o.name] = o; });

  function pivotla(obj, p) {
    const t = new THREE.Group();
    t.position.set(p[0] * MM, p[1] * MM, p[2] * MM);
    obj.position.set(-p[0] * MM, -p[1] * MM, -p[2] * MM);
    kok.add(t); t.add(obj); return t;
  }
  const ARABA = new THREE.Group(); kok.add(ARABA);
  const P = M.tabla.pivot;
  const TABLA = pivotla(G.TABLA, P), TEPSI = pivotla(G.TEPSI, P), PIDE = pivotla(G.PIDE, P);
  ARABA.add(TABLA, TEPSI, PIDE, G.ARABA);

  const MILLER = {};
  for (const y of M.yuvalar)
    for (const [ad, kot] of [['HELEZON', y.mil_helezon_y], ['KARISTIRICI', y.mil_karistirici_y]]) {
      const g = G[ad + '_' + y.kod];
      if (g) MILLER[ad + '_' + y.kod] = pivotla(g, [y.x, kot, 0]);
    }
  sahne.add(kok);

  // ---------- dozlanan ürün: pidenin üstünde biriken spiral iz ----------
  const IZ_N = 6000;
  const izGeo = new THREE.BufferGeometry();
  izGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(IZ_N * 3), 3));
  izGeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(IZ_N * 3), 3));
  izGeo.setDrawRange(0, 0);
  const iz = new THREE.Points(izGeo, new THREE.PointsMaterial({ size: 0.009, vertexColors: true, sizeAttenuation: true }));
  iz.position.copy(G.PIDE.position);                    // pide ile birlikte döner
  PIDE.add(iz);
  let izAdet = 0;
  const izTemizle = () => { izAdet = 0; izGeo.setDrawRange(0, 0); };
  function izEkle(r, aciDer, renk) {
    if (izAdet >= IZ_N) return;
    const a = THREE.MathUtils.degToRad(-aciDer);        // pide döndüğü için iz ters yönde birikir
    const py = (M.pide.ust_y + 1.5) * MM;
    const p = izGeo.attributes.position.array, c = izGeo.attributes.color.array, i = izAdet * 3;
    p[i] = (P[0] + r * Math.cos(a)) * MM; p[i + 1] = py; p[i + 2] = (P[2] + r * Math.sin(a)) * MM;
    const col = new THREE.Color(renk); c[i] = col.r; c[i + 1] = col.g; c[i + 2] = col.b;
    izAdet++; izGeo.setDrawRange(0, izAdet);
    izGeo.attributes.position.needsUpdate = izGeo.attributes.color.needsUpdate = true;
  }

  // ---------- dozlanırken memeden inen ürün ipi ----------
  const ipGeo = new THREE.CylinderGeometry(0.008, 0.008, 1, 10);
  const ip = new THREE.Mesh(ipGeo, new THREE.MeshStandardMaterial({ color: 0xf2d98a, roughness: 0.85 }));
  ip.visible = false; kok.add(ip);

  // ---------- kamera ----------
  const TBY = M.pide.ust_y * MM, TBZ = M.tabla.eksen_z * MM;
  kon.target.set(M.tabla.baslangic_x * MM, TBY + 0.20, TBZ - 0.10);
  kam.position.set(M.tabla.baslangic_x * MM + 0.75, TBY + 0.95, TBZ + 2.30);
  let TAKIP = true;
  function boyut() {
    const r = yer.getBoundingClientRect();
    if (!r.width) return;
    kam.aspect = r.width / r.height; kam.updateProjectionMatrix(); ren.setSize(r.width, r.height);
  }
  addEventListener('resize', boyut);

  // ---------- kod paneli ----------
  const kaynak = await (await fetch('./makine_kodu.js?v=3')).text();
  const sat = kaynak.split('\n'), ISARET = {};
  sat.forEach((s, i) => { const m = s.match(/\/\*@(\w+)\*\//); if (m) ISARET[m[1]] = i; });
  q('.simp-k pre').innerHTML = sat.map((s, i) =>
    `<span class="l" data-i="${i}">${s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])) || ' '}</span>`).join('');
  let sonS = null;
  function vurgula(ad) {
    const i = ISARET[ad]; if (i === undefined) return;
    if (sonS !== null) q(`.simp-k [data-i="${sonS}"]`)?.classList.remove('ak');
    const e = q(`.simp-k [data-i="${i + 1}"]`) || q(`.simp-k [data-i="${i}"]`);
    if (e) { e.classList.add('ak'); sonS = +e.dataset.i; e.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
  }

  let dozRenk = 0xf2d98a, dozlaniyor = false;
  let dozT0 = 0, dozY = null;
  function izle(o) {
    if (o.satir) vurgula(o.satir);
    if (o.kod) dozRenk = URUN_RENK[o.kod] || 0xf2d98a;
    if (o.faz === 'doz') {
      dozlaniyor = true; ip.material.color.setHex(dozRenk);
      dozT0 = performance.now(); dozY = M.yuvalar.find(v => v.kod === o.kod) || null;
    }
    if (o.faz === 'bitti' || o.faz === 'basla') dozlaniyor = false;
    if (o.yeniTepsi) { izTemizle(); dozY = null; }
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
    q('.bas').disabled = true; izTemizle();
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
    TABLA.rotation.y = TEPSI.rotation.y = PIDE.rotation.y = a;
    for (const ad in MILLER) {
      const m = K.MOTOR[ad] || K.MOTOR[ad.replace('HELEZON_', 'POMPA_')];
      if (m) MILLER[ad].rotation.z = THREE.MathUtils.degToRad(m.aci || 0);
    }

    const y = M.yuvalar.reduce((p, v) => Math.abs(v.x - K.EKSEN.X) < Math.abs(p.x - K.EKSEN.X) ? v : p);
    const r = Math.hypot(y.x - K.EKSEN.X, M.tabla.r_ic);

    // dozlanırken: memeden inen ip + pide üstünde biriken iz
    ip.visible = dozlaniyor;
    if (dozlaniyor) {
      const ust = 252 * MM, alt = (M.pide.ust_y + 2) * MM;
      ip.position.set(y.x * MM, (ust + alt) / 2, M.tabla.eksen_z * MM + M.tabla.r_ic * MM);
      ip.scale.y = (ust - alt) / 1;
      izEkle(r, K.EKSEN.TABLA, dozRenk);
    }

    if (TAKIP) {
      const hx = K.EKSEN.X * MM, dx = hx - kon.target.x;
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
