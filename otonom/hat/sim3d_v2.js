// AUTOKITCH · TOPPING v2 (UNO'lu) — CANLI SİMÜLASYON (sayfa içinde, sağdan açılan panel)
// Kemal: "toppingi de tam hesapla: pizza gelip sos geniş ağızlının altına geliyor — ne kadar dökecek, alt tabla ne kadar
// dönecek; sağda da panel yap, seçim yapınca çalışmaya başlasın; diğer kasetler, UNO'lar için de yap; karışıkta seçebileyim."
// ASIL ÜRETİM MODELİ oynar: ana montajın modul_C.glb'si (hat_montaj_v45). Hareketli paketler montajda ayrı düğüm:
//   TOPPING_MODUL__<ton>__ARABA · __TABLA · __PISTON_SOS · __VALF_SOS · __HELEZON_KASAR · __KARISTIRICI_KASAR ...
// Kontrol: makine_kodu_v2.js (makineyi süren kod). Sayılar: sim_makine_v7.json (topping_v2_hesap_v1 + topping_uno_cad_v5).
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as K from './makine_kodu_v2.js?v=1';

const MM = 0.001;
let S = null;

export async function ac(kutu, dugme) {
  if (S) { S.goster(!S.acik); return; }
  dugme.textContent = 'yükleniyor…'; dugme.disabled = true;
  S = await kur(kutu);
  dugme.disabled = false;
  dugme.textContent = '■ SİMÜLASYONU KAPAT';
  S.goster(true);
}

const f1 = v => v.toFixed(1).replace('.', ',');
const f2 = v => v.toFixed(2).replace('.', ',');

async function kur(kutu) {
  // ---------- panel ----------
  const panel = document.createElement('div');
  panel.className = 'simp';
  panel.innerHTML = `
    <div class="simp-b">
      <h4>1 · Ürün seç — seçince başlar</h4><div class="simp-u"></div>
      <div class="simp-x" style="display:none;padding:0 16px 10px;color:#c3cad3;font-size:12.5px"></div>
      <div class="simp-c"><button class="bas">▶ TEKRAR</button><button class="dur">DUR</button></div>
      <h4>2 · Hesap — bu ürün</h4><div class="simp-h" style="padding:6px 16px 10px;font-size:11.5px;color:#9aa4b2;overflow:auto;max-height:190px"></div>
      <h4>3 · Makine durumu</h4><div class="simp-d"></div><div class="simp-m"></div>
      <h4>4 · Çalışan kod — makine_kodu_v2.js</h4><div class="simp-k"><pre></pre></div>
      <div class="simp-l"></div>
    </div>`;
  kutu.appendChild(panel);
  const q = s => panel.querySelector(s);
  const log = (t, c) => { const d = document.createElement('div'); if (c) d.className = c; d.textContent = t; q('.simp-l').appendChild(d); q('.simp-l').scrollTop = 1e6; };

  // ---------- sahne ----------
  const yer = document.createElement('div'); yer.className = 'simv'; kutu.appendChild(yer);
  const sahne = new THREE.Scene(); sahne.background = new THREE.Color(0x15181d);
  const kam = new THREE.PerspectiveCamera(36, 1, 0.05, 60);
  const ren = new THREE.WebGLRenderer({ antialias: true });
  ren.setPixelRatio(Math.min(2, devicePixelRatio));
  yer.appendChild(ren.domElement);
  const kon = new OrbitControls(kam, ren.domElement);
  sahne.add(new THREE.HemisphereLight(0xdfe7f2, 0x2a2f38, 1.15));
  const g1 = new THREE.DirectionalLight(0xffffff, 1.0); g1.position.set(1.4, 2.2, 1.6); sahne.add(g1);
  const g2 = new THREE.DirectionalLight(0xffffff, 0.35); g2.position.set(-1.2, 1.0, -1.4); sahne.add(g2);

  const M = await (await fetch('../hat3d/sim_makine_v7.json?v=1')).json();
  K.kur(M, izle);
  const OFS = M.ofset, mak = p => [p[0] + OFS[0], p[1] + OFS[1], p[2] + OFS[2]];

  const glb = await new GLTFLoader().loadAsync('../hat3d/modul_C.glb?v=47');
  const kok = glb.scene;
  const G = {};
  const agalar = []; kok.traverse(o => { if (o.isMesh) agalar.push(o); });
  for (const o of agalar) {
    const s = (o.name || '').split('__');
    if (s.length < 3) continue;
    const g = s[2];
    if (!/^(ARABA|TABLA|ACICI|KONI_ON|KONI_ARKA|BANT_BURUN|BANT_TAHRIK|PISTON_\w+|VALF_\w+|HELEZON_\w+|KARISTIRICI_\w+)$/.test(g)) continue;
    (G[g] = G[g] || new THREE.Group()).add(o);
  }
  if (!G.ARABA || !G.TABLA || !G.PISTON_SOS) throw new Error('modul_C.glb hareketli paket taşımıyor — hat_montaj_v45 ile üretilmeli');

  function pivotla(obj, p) {
    const t = new THREE.Group();
    t.position.set(p[0] * MM, p[1] * MM, p[2] * MM);
    obj.position.set(-p[0] * MM, -p[1] * MM, -p[2] * MM);
    kok.add(t); t.add(obj); return t;
  }
  const ARABA = new THREE.Group(); kok.add(ARABA);
  const P = mak(M.tabla.pivot);

  function disk(r, kal, ym, renk, ruf) {
    const g = new THREE.CylinderGeometry(r * MM, r * MM, kal * MM, 72);
    g.translate(P[0] * MM, ym * MM, P[2] * MM);
    const m = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: renk, roughness: ruf, metalness: 0.05 }));
    kok.add(m); return m;
  }
  const yDisk = M.pide.disk_ust + OFS[1], yPide = M.pide.ust_y + OFS[1];
  const pideAg = disk(M.pide.yaricap, M.pide.hamur_k, yPide - M.pide.hamur_k / 2, 0xe8d6ad, 0.9);
  const topG = new THREE.SphereGeometry(M.pide.top_r * MM, 32, 24); topG.scale(1, 0.82, 1);
  topG.translate(P[0] * MM, (yDisk + M.pide.top_r * 0.82) * MM, P[2] * MM);
  const topAg = new THREE.Mesh(topG, new THREE.MeshStandardMaterial({ color: 0xead9b4, roughness: 0.95 })); kok.add(topAg);
  const TABLA = pivotla(G.TABLA, P), PIDE = pivotla(pideAg, P), TOP = pivotla(topAg, P);
  ARABA.add(TABLA, PIDE, TOP, G.ARABA);
  PIDE.visible = false;

  // ---------- AÇICI ----------
  const AC = M.acici, AKT = M.aktarma;
  const ACGRUP = new THREE.Group(); kok.add(ACGRUP); if (G.ACICI) ACGRUP.add(G.ACICI);
  const acAci = THREE.MathUtils.degToRad(AC.yarim_aci), KONI = {};
  for (const [ad, yon] of [['KONI_ON', 1], ['KONI_ARKA', -1]]) {
    if (!G[ad]) continue;
    const tepe = mak([AC.x, AC.tepe_y, M.tabla.eksen_z]);
    const t = new THREE.Group(); t.position.set(tepe[0] * MM, tepe[1] * MM, tepe[2] * MM);
    G[ad].position.set(-tepe[0] * MM, -tepe[1] * MM, -tepe[2] * MM); t.add(G[ad]); ACGRUP.add(t);
    KONI[ad] = { g: t, eks: new THREE.Vector3(0, Math.sin(acAci), yon * Math.cos(acAci)).normalize(), aci: 0, yon };
  }
  ACGRUP.position.y = AC.kalkis * MM;

  // ---------- BANT ----------
  const RULO = {};
  for (const [ad, rx, ry] of [['BANT_BURUN', AKT.bant_burun_x, AKT.bant_y - 1.5 - AKT.burun_r], ['BANT_TAHRIK', AKT.bant_son_x, AKT.bant_y - 1.5 - AKT.tahrik_r]]) {
    if (!G[ad]) continue;
    RULO[ad] = { g: pivotla(G[ad], mak([rx, ry, 0])), r: ad === 'BANT_BURUN' ? AKT.burun_r : AKT.tahrik_r, aci: 0 };
  }
  const bantPideAg = disk(M.pide.yaricap, M.pide.hamur_k, 0, 0xe8d6ad, 0.9);
  bantPideAg.geometry.translate(-P[0] * MM, 0, -P[2] * MM); bantPideAg.visible = false; kok.add(bantPideAg);
  let bantPideX = 0, bantCalisiyor = false;

  // ---------- UNO: piston (z'de kayar) + döner valf (x ekseninde 90°) · KASET: helezon + karıştırıcı (z ekseninde döner) ----------
  const PST = {}, VLF = {}, MIL = {};
  for (const i of M.istasyon) {
    if (i.grup_piston && G[i.grup_piston]) { PST[i.kod] = G[i.grup_piston]; kok.add(PST[i.kod]); }
    if (i.grup_valf && G[i.grup_valf]) VLF[i.kod] = pivotla(G[i.grup_valf], mak(i.valf));
    if (i.grup_helezon && G[i.grup_helezon]) MIL['HELEZON_' + i.kod] = pivotla(G[i.grup_helezon], mak(i.helezon));
    if (i.grup_karis && G[i.grup_karis]) MIL['KARISTIRICI_' + i.kod] = pivotla(G[i.grup_karis], mak(i.karis));
  }
  sahne.add(kok);

  // ---------- YAYICI: tabla dönerken borunun altından çıkan katman pidede SEKTÖR olarak büyür ----------
  const katmanlar = [];
  function katmanKur(i) {
    const mat = new THREE.MeshStandardMaterial({ color: +i.renk, roughness: 0.6, side: THREE.DoubleSide });
    const m = new THREE.Mesh(new THREE.BufferGeometry(), mat);
    m.userData = { i, a0: null, y: yPide + 0.8 + katmanlar.length * 0.9 };
    pideAg.add(m); katmanlar.push(m); return m;
  }
  function katmanGuncelle(m, sweep) {
    const { i, y } = m.userData;
    const g = new THREE.RingGeometry(i.bar_r[0] * MM, M.hesap.r_kap * MM, 96, 1, -m.userData.a0 - sweep, Math.max(0.001, sweep));
    g.rotateX(-Math.PI / 2); g.translate(P[0] * MM, y * MM, P[2] * MM);
    m.geometry.dispose(); m.geometry = g;
  }
  // borudan inen perde (yalnız kesme valfi açıkken)
  const perde = {};
  for (const i of M.istasyon.filter(v => v.tip === 'YAYICI')) {
    const L = i.bar_r[1] - i.bar_r[0], h = i.bar_alt - M.pide.ust_y;
    const g = new THREE.BoxGeometry(L * MM, h * MM, 3 * MM);
    g.translate((i.x + (i.bar_r[0] + i.bar_r[1]) / 2 + OFS[0]) * MM, (M.pide.ust_y + h / 2 + OFS[1]) * MM, i.agiz_z * MM);
    perde[i.kod] = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: +i.renk, transparent: true, opacity: 0.85 }));
    perde[i.kod].visible = false; sahne.add(perde[i.kod]);
  }

  // ---------- NOKTA + KASET: gerçek dökülme (serbest düşme + yığın) — v1 simülasyonundaki model ----------
  const YER = 9810, YOG = 1.05e-3, UCAN_N = 1500, YIGIN_N = 16000, HB_A = 72, HB_R = 20;
  const hMap = new Float32Array(HB_A * HB_R), DR = M.pide.yaricap / HB_R, DA = 2 * Math.PI / HB_A;
  function parcaKur(n) {
    const im = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 0.62, 1), new THREE.MeshStandardMaterial({ roughness: 0.82 }), n);
    im.instanceMatrix.setUsage(THREE.DynamicDrawUsage); im.frustumCulled = false; im.count = 0; return im;
  }
  const ucanAg = parcaKur(UCAN_N); kok.add(ucanAg);
  const yiginAg = parcaKur(YIGIN_N); PIDE.add(yiginAg);
  const ucanlar = []; let yiginAdet = 0, birikim = 0;
  const MT = new THREE.Matrix4(), MQ = new THREE.Quaternion(), MV = new THREE.Vector3(), MS = new THREE.Vector3(), YEKS = new THREE.Vector3(0, 1, 0), RENK = new THREE.Color();
  function temizle() {
    ucanlar.length = 0; yiginAdet = 0; birikim = 0; hMap.fill(0); ucanAg.count = 0; yiginAg.count = 0;
    for (const m of katmanlar) { pideAg.remove(m); m.geometry.dispose(); } katmanlar.length = 0;
  }
  function tane(m, n, x, y, z, d, a, renk) { MV.set(x, y, z); MQ.setFromAxisAngle(YEKS, a); MS.set(d, d, d); m.setMatrixAt(n, MT.compose(MV, MQ, MS)); m.setColorAt(n, RENK.setHex(renk)); }
  function dokum(dt, D) {
    if (D && D.tip !== 'YAYICI') {
      const i = M.istasyon.find(v => v.kod === D.kod), d = i.parca_mm, mp = d * d * d * 0.62 * YOG;
      birikim += (D.g / D.T) * dt / mp;
      const rA = Math.max(1, i.ic / 2 - d / 2), vy = (D.ml * 1000 / D.T) / (Math.PI / 4 * i.ic * i.ic);
      while (birikim >= 1 && ucanlar.length < UCAN_N) {
        birikim--;
        const t = Math.random() * 2 * Math.PI, rr = rA * Math.sqrt(Math.random());
        ucanlar.push({ x: i.x + OFS[0] + rr * Math.cos(t), y: i.agiz_y + OFS[1], z: i.agiz_z + rr * Math.sin(t), vx: (Math.random() - 0.5) * 6, vy: -vy, vz: (Math.random() - 0.5) * 6,
                       d: d * (0.8 + 0.4 * Math.random()), a: Math.random() * 6.28, renk: +i.renk });
      }
      if (birikim > 60) birikim = 60;
    }
    const cx = K.EKSEN.X + OFS[0], ac = THREE.MathUtils.degToRad(K.EKSEN.TABLA), ct = Math.cos(ac), st = Math.sin(ac);
    for (let n = ucanlar.length - 1; n >= 0; n--) {
      const p = ucanlar[n];
      p.vy -= YER * dt; p.x += p.vx * dt; p.y += p.vy * dt; p.z += p.vz * dt;
      const ox = p.x - cx, oz = p.z - P[2], u = ox * ct - oz * st, w = ox * st + oz * ct, rr = Math.hypot(u, w);
      const ri = Math.min(HB_R - 1, Math.floor(rr / DR)), ai = ((Math.floor((Math.atan2(w, u) + Math.PI) / DA) % HB_A) + HB_A) % HB_A, gz = ai * HB_R + ri;
      const yuzey = rr <= M.pide.yaricap ? yPide + 1.5 + hMap[gz] : -1e6;
      if (p.y - p.d / 2 > yuzey) continue;
      ucanlar.splice(n, 1);
      if (rr > M.pide.yaricap || yiginAdet >= YIGIN_N) continue;
      tane(yiginAg, yiginAdet, u * MM, (yuzey + p.d * 0.31 - P[1]) * MM, w * MM, p.d * MM, p.a, p.renk);
      yiginAdet++; yiginAg.count = yiginAdet; yiginAg.instanceMatrix.needsUpdate = true; if (yiginAg.instanceColor) yiginAg.instanceColor.needsUpdate = true;
      hMap[gz] = Math.min(28, hMap[gz] + (p.d * p.d * p.d * 0.62) / (DA * (ri * DR + DR / 2) * DR));
    }
    for (let n = 0; n < ucanlar.length; n++) { const p = ucanlar[n]; tane(ucanAg, n, p.x * MM, p.y * MM, p.z * MM, p.d * MM, p.a, p.renk); }
    ucanAg.count = ucanlar.length; ucanAg.instanceMatrix.needsUpdate = true; if (ucanAg.instanceColor) ucanAg.instanceColor.needsUpdate = true;
  }

  // ---------- kamera ----------
  const TBY = yPide * MM, TBZ = M.tabla.eksen_z * MM, TBX = (M.tabla.baslangic_x + OFS[0]) * MM;
  kon.target.set(TBX, TBY + 0.18, TBZ - 0.05);
  kam.position.set(TBX + 0.55, TBY + 0.75, TBZ + 1.85);
  let TAKIP = true;
  ren.domElement.addEventListener('pointerdown', () => { TAKIP = false; });
  function boyut() { const r = yer.getBoundingClientRect(); if (!r.width) return; kam.aspect = r.width / r.height; kam.updateProjectionMatrix(); ren.setSize(r.width, r.height); }
  addEventListener('resize', boyut);

  // ---------- kod paneli ----------
  const kaynak = await (await fetch('./makine_kodu_v2.js?v=1')).text();
  const sat = kaynak.split('\n'), ISARET = {};
  sat.forEach((s, n) => { const m = s.match(/\/\*@(\w+)\*\//); if (m) ISARET[m[1]] = n; });
  q('.simp-k pre').innerHTML = sat.map((s, n) => `<span class="l" data-i="${n}">${s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])) || ' '}</span>`).join('');
  let sonS = null;
  function vurgula(ad) {
    const n = ISARET[ad]; if (n === undefined) return;
    if (sonS !== null) q(`.simp-k [data-i="${sonS}"]`)?.classList.remove('ak');
    const e = q(`.simp-k [data-i="${n + 1}"]`) || q(`.simp-k [data-i="${n}"]`);
    if (e) { e.classList.add('ak'); sonS = +e.dataset.i; const kk = q('.simp-k'); kk.scrollTop = e.offsetTop - kk.clientHeight / 2 + e.offsetHeight / 2; }
  }

  let acilma = -1, kafa = -1, kafaU = 1, aktifKatman = null, sonSure = null;
  function izle(o) {
    if (o.satir) vurgula(o.satir);
    if (o.yeniTepsi) { temizle(); acilma = -1; TOP.visible = true; TOP.scale.setScalar(1); PIDE.visible = false; PIDE.scale.set(1, 1, 1); }
    if (o.faz === 'acma') kafa = 0;
    if (o.acildi) acilma = 0;
    if (o.satir === 'ac' && o.mesaj && o.mesaj.indexOf('kalkıyor') >= 0) kafa = 2;
    if (o.aktarildi) { PIDE.visible = false; TOP.visible = false; bantPideX = AKT.bant_burun_x; bantCalisiyor = true; bantPideAg.visible = true; }
    if (o.faz === 'bitti' && o.sure) sonSure = o.sure;
    if (o.mesaj) log(o.mesaj, o.faz === 'bitti' ? 'y' : (o.faz === 'basla' ? 'b' : ''));
  }

  // ---------- ürün düğmeleri (seçince başlar) + karışık ----------
  let secili = null, calisiyor = false, bekleyen = null;
  async function baslat(doz, ad) {
    if (calisiyor) { bekleyen = [doz, ad]; K.durdur(); return; }
    calisiyor = true; secili = [doz, ad]; hesapTablosu(doz, ad); sonSure = null;
    try { await K.urunYap(doz); } finally {
      calisiyor = false;
      if (bekleyen) { const b = bekleyen; bekleyen = null; baslat(b[0], b[1]); }
    }
  }
  const URUN = Object.entries(M.recete).map(([k, r]) => ({ k, ad: r.ad, doz: r.doz }));
  URUN.push({ k: 'karisik', ad: 'Karışık (seç)', doz: null });
  for (const u of URUN) {
    const b = document.createElement('button'); b.textContent = u.ad; b.dataset.k = u.k;
    b.onclick = () => {
      panel.querySelectorAll('.simp-u button').forEach(x => x.classList.toggle('on', x === b));
      q('.simp-x').style.display = u.doz ? 'none' : 'block';
      if (u.doz) { log('seçildi: ' + u.ad, 'b'); baslat(u.doz, u.ad); }
      else karisikGoster();
    };
    q('.simp-u').appendChild(b);
  }
  function karisikGoster() {
    const ops = [['SOS', 'Sos'], ['KIYMA', 'Kıyma'], ['KUSBASI', 'Kuşbaşı'], ['KASAR', 'Kaşar'], ['SUCUK', 'Küp sucuk']];
    q('.simp-x').innerHTML = ops.map(([k, a]) => `<label style="margin-right:10px;white-space:nowrap"><input type="checkbox" value="${k}"${['KIYMA', 'KUSBASI', 'KASAR', 'SUCUK'].includes(k) ? ' checked' : ''}> ${a}</label>`).join('') +
      `<div style="margin-top:6px;color:#8d97a4">${M.karisik.kural}</div><button class="kbas" style="margin-top:8px;padding:8px 12px;border:0;border-radius:8px;background:#2f7d4f;color:#fff;font-weight:700;cursor:pointer">▶ KARIŞIĞI YAP</button>`;
    const oku = () => [...q('.simp-x').querySelectorAll('input:checked')].map(x => x.value);
    const on = () => { const d = K.karisik(oku()); hesapTablosu(d, 'Karışık'); };
    q('.simp-x').querySelectorAll('input').forEach(x => x.onchange = on); on();
    q('.simp-x .kbas').onclick = () => { const d = K.karisik(oku()); if (!Object.keys(d).length) return; log('seçildi: karışık → ' + JSON.stringify(d), 'b'); baslat(d, 'Karışık'); };
  }
  q('.bas').onclick = () => { if (secili) baslat(secili[0], secili[1]); };
  q('.dur').onclick = () => { K.durdur(); log('DUR basıldı', 'b'); };

  function hesapTablosu(doz, ad) {
    const sira = K.sirala(doz);
    let h = `<div style="color:#e6ecf3;font-weight:600;margin-bottom:4px">${ad}</div><table style="width:100%;border-collapse:collapse">`;
    h += '<tr style="color:#6f7a87"><td>istasyon</td><td>doz</td><td>tabla</td><td>süre</td><td>katman</td></tr>';
    for (const k of sira) {
      const i = M.istasyon.find(v => v.kod === k), r = K.hesapla(k, doz[k]);
      const alt = i.tip === 'YAYICI' ? `UNO Ø${i.sil} strok ${f1(r.strok)} mm · piston ${f1(r.piston_hiz)} mm/s · kama yarık ${f1(i.yarik[0][1])}→${f1(i.yarik[i.yarik.length - 1][1])} mm`
        : i.tip === 'NOKTA' ? `UNO Ø${i.sil} strok ${f1(r.strok)} mm · piston ${f2(r.piston_hiz)} mm/s · şerit ${f1(r.serit)} · hatve ${f1(r.hatve_dis)}→${f1(r.hatve_ic)} · r<${f1(r.seyrek_r)} seyrek`
        : `helezon ${i.rpm} dev/dk × ${f1(r.helezon_tur)} tur · şerit ${f1(r.serit)} · hatve ${f1(r.hatve_dis)}→${f1(r.hatve_ic)}`;
      h += `<tr style="border-top:1px solid #222831"><td style="color:#e6ecf3">${i.ad}</td><td>${f1(doz[k])} g · ${f1(r.ml)} ml</td><td>${r.tur === 1 ? '1 tur (360°)' : f2(r.tur) + ' tur'}</td><td>${f1(r.sure)} s</td><td>${f2(r.katman)} mm</td></tr>` +
           `<tr><td colspan="5" style="color:#7d8794;padding-bottom:4px">${alt}</td></tr>`;
    }
    h += '</table>';
    const kt = Object.entries(M.recete).find(([k, r]) => JSON.stringify(r.doz) === JSON.stringify(doz));
    if (kt && M.kontrol[kt[0]]) h += `<div style="margin-top:4px">hesapta çevrim ${f1(M.kontrol[kt[0]].sure)} s (açıcı → dozlar → aktarma → açıcı)</div>`;
    q('.simp-h').innerHTML = h;
  }

  const MOTADLAR = ['X', 'TABLA', 'ACICI', ...M.istasyon.filter(i => i.grup_piston).flatMap(i => ['UNO_' + i.kod, 'VALF_' + i.kod]),
                    ...M.istasyon.filter(i => i.tip === 'YAYICI').map(i => 'KESME_' + i.kod), ...M.istasyon.filter(i => i.tip === 'KASET').flatMap(i => ['HELEZON_' + i.kod, 'KARISTIRICI_' + i.kod])];
  q('.simp-m').innerHTML = MOTADLAR.map(a => `<span data-m="${a}">${a.replace(/_/g, ' ')}</span>`).join('');
  const onceki_p = {};
  const aktifMi = (a, dt) => {
    if (a.startsWith('UNO_')) { const k = a.slice(4), v = K.PISTON[k], o = onceki_p[k]; onceki_p[k] = v; return o !== undefined && Math.abs(v - o) > 1e-4; }
    if (a.startsWith('VALF_')) { const v = K.VALF[a.slice(5)]; return v > 0.02 && v < 0.98; }
    if (a.startsWith('KESME_')) return !!K.KESME[a.slice(6)];
    return !!K.MOTOR[a];
  };

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
    // UNO pistonu (emişte −z'ye çekilir) + döner valf (x ekseninde −90°)
    for (const k in PST) PST[k].position.z = -K.PISTON[k] * MM;
    for (const k in VLF) VLF[k].rotation.x = -Math.PI / 2 * K.VALF[k];
    for (const ad in MIL) { const m = K.MOTOR[ad]; if (m) MIL[ad].rotation.z = -THREE.MathUtils.degToRad(m.aci || 0); }
    // açıcı
    if (kafa === 0) { kafaU = Math.max(0, kafaU - dt / AC.in_sn); if (kafaU <= 0) kafa = 1; }
    else if (kafa === 2) { kafaU = Math.min(1, kafaU + dt / AC.kalk_sn); if (kafaU >= 1) kafa = -1; }
    ACGRUP.position.y = AC.kalkis * kafaU * MM;
    for (const ad in KONI) { const k = KONI[ad]; if (acilma >= 0 && acilma < 1) k.aci += k.yon * AC.koni_rpm * 6 * THREE.MathUtils.DEG2RAD * dt; k.g.quaternion.setFromAxisAngle(k.eks, k.aci); }
    if (acilma >= 0 && acilma < 1) {
      acilma = Math.min(1, acilma + dt / AC.ac_sn); const u = acilma;
      PIDE.visible = true; PIDE.scale.set(0.18 + 0.82 * u, 1, 0.18 + 0.82 * u);
      TOP.scale.set(1 + 1.4 * u, Math.max(0.02, 1 - u), 1 + 1.4 * u); if (u >= 1) TOP.visible = false;
    }
    // bant
    if (bantCalisiyor) {
      bantPideX += AKT.bant_hiz * dt;
      bantPideAg.position.set((bantPideX + OFS[0]) * MM, (AKT.bant_y + M.pide.hamur_k / 2 + OFS[1]) * MM, M.tabla.eksen_z * MM);
      for (const ad in RULO) { const r = RULO[ad]; r.aci -= AKT.bant_hiz / r.r * dt; r.g.rotation.z = r.aci; }
      if (bantPideX > AKT.bant_son_x + 200) { bantCalisiyor = false; bantPideAg.visible = false; }
    }
    // yayıcı katmanı + perde
    const D = K.DOZ;
    for (const k in perde) perde[k].visible = !!K.KESME[k];
    if (D && D.tip === 'YAYICI') {
      if (!aktifKatman || aktifKatman.userData.i.kod !== D.kod) { aktifKatman = katmanKur(M.istasyon.find(v => v.kod === D.kod)); aktifKatman.userData.a0 = THREE.MathUtils.degToRad(D.a0); }
      if (K.KESME[D.kod]) katmanGuncelle(aktifKatman, Math.min(2 * Math.PI, THREE.MathUtils.degToRad(K.EKSEN.TABLA - D.a0)));
    } else aktifKatman = null;
    dokum(dt, D);
    if (TAKIP) { const hx = (K.EKSEN.X + OFS[0]) * MM, dx = hx - kon.target.x; if (Math.abs(dx) > 1e-5) { const u = Math.min(1, dt * 5); kon.target.x += dx * u; kam.position.x += dx * u; } }
    // durum
    let dozS = '—', grS = '—', turS = '—', pS = '—';
    if (D) {
      const i = M.istasyon.find(v => v.kod === D.kod), gecen = (performance.now() - D.t0) / 1000;
      dozS = i.ad;
      const gr = i.grup_piston ? D.g * (1 - K.PISTON[D.kod] / D.strok) : D.g * Math.min(1, gecen / D.T);
      grS = `${f1(Math.max(0, Math.min(D.g, gr)))} / ${f1(D.g)} g`;
      turS = D.tip === 'YAYICI' ? `${Math.min(360, K.EKSEN.TABLA - D.a0).toFixed(0)}° / 360°` : `${f2((K.EKSEN.TABLA - D.a0) / 360)} / ${f2(D.h.tur)} tur`;
      if (i.grup_piston) pS = `${f1(K.PISTON[D.kod])} mm (strok ${f1(D.strok)})`;
    }
    q('.simp-d').innerHTML =
      `<div class="sat"><span>X ekseni (araba)</span><b>${f1(K.EKSEN.X)} mm</b></div>` +
      `<div class="sat"><span>tabla</span><b>${(((K.EKSEN.TABLA % 360) + 360) % 360).toFixed(0)}° · ${K.MOTOR.TABLA ? f1(K.MOTOR.TABLA.rpm) + ' dev/dk' : 'duruyor'}</b></div>` +
      `<div class="sat"><span>dozlayan</span><b>${dozS}</b></div>` +
      `<div class="sat"><span>dökülen</span><b>${grS}</b></div>` +
      `<div class="sat"><span>bu dozda tabla</span><b>${turS}</b></div>` +
      `<div class="sat"><span>UNO pistonu</span><b>${pS}</b></div>` +
      (sonSure ? `<div class="sat"><span>son çevrim (ölçülen)</span><b>${f1(sonSure)} s · saatte ${Math.round(3600 / sonSure)}</b></div>` : '');
    panel.querySelectorAll('.simp-m span').forEach(s => s.classList.toggle('on', aktifMi(s.dataset.m, dt)));
    kon.update(); ren.render(sahne, kam);
  }
  kare();
  log('hazır — ürün seç, hemen başlar', 'y');
  return {
    get acik() { return acik; },
    goster(v) { acik = v; yer.style.display = panel.style.display = v ? 'block' : 'none'; kutu.classList.toggle('sim-on', v); if (v) { setTimeout(boyut, 30); onceki = performance.now(); } },
  };
}
