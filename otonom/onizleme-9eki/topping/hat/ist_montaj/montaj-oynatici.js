/* MONTAJ OYNATICI (ortak) — B v4 · A v3 · tek çekmece v3 · TOPPING: aynı oynatıcı · 4 Eki 2026 · yerel
   Kemal geri bildirimi (4 Eki): RENK ANAHTARI sabit lejant — SARI = yalıtım (PU levha) · TURUNCU = şu an takılan parça · KIRMIZI = kaynak (dikiş / punta,
   birleşimden sonra da KALICI kırmızı) · MAVİ = vida / cıvata / perçin / PEM bağlantısı · YEŞİL = yapıştırıcı / silikon. Kablolar: koyu kırmızı güç ·
   koyu mavi bilgi (lejantta ayrı). Sayfa: <body data-ist="b"> + veri ../hat3d/v3/<ist>_montaj/<ist>_montaj.(json|glb) · montaj sehpası yalnız D.sehpa.
   Kaynak: b3-montaj.js (B v3 / tek çekmece v3 oynatıcısı; aynı hareket / morph / vurgu modeli). */
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const IST = document.body.dataset.ist;
const V = new URL(import.meta.url).search || '?v=1';
const $ = id => document.getElementById(id);
const sayi = (x, n = 1) => x.toFixed(n).replace('.', ',');
const KOK = `../hat3d/v3/${IST}_montaj/${IST}_montaj`;
const D = await (await fetch(KOK + '.json' + V)).json();
const T_SON = D.toplam;
const Z = D.zarf, ZM = [(Z[0][0] + Z[1][0]) / 2, (Z[0][1] + Z[1][1]) / 2, (Z[0][2] + Z[1][2]) / 2];

// ---------------------------------------------------------------- sahne
if (new URLSearchParams(location.search).has('foto')) document.body.classList.add('foto');
const kap = $('km');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.localClippingEnabled = true;
kap.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xe9edf2);
const camera = new THREE.PerspectiveCamera(32, 1, 0.03, 60);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; controls.dampingFactor = 0.12;
scene.add(new THREE.HemisphereLight(0xffffff, 0x8a939e, 1.15));
const gun = new THREE.DirectionalLight(0xffffff, 1.6); gun.position.set(ZM[0] - 1.7, 5, 4); scene.add(gun);
const gun2 = new THREE.DirectionalLight(0xffffff, 0.6); gun2.position.set(ZM[0] + 3, 3, -4); scene.add(gun2);
const ZB = Math.max(10, (Z[1][0] - Z[0][0]) + 6);
const zemin = new THREE.Mesh(new THREE.PlaneGeometry(ZB, 10), new THREE.MeshStandardMaterial({ color: 0xd9dee5, roughness: 0.95 }));
zemin.rotation.x = -Math.PI / 2; zemin.position.set(ZM[0], 0, 0); scene.add(zemin);
const izgara = new THREE.GridHelper(ZB, Math.round(ZB * 2), 0xb9c1cc, 0xc9d0d9); izgara.position.set(ZM[0], 0.001, 0); scene.add(izgara);

function resize() {
  const w = kap.clientWidth, h = kap.clientHeight;
  renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(kap); resize();

// ---------------------------------------------------------------- malzemeler + kesit
const kesitDuz = new THREE.Plane(new THREE.Vector3(0, 0, -1), 0);
const kesitler = [];
const MAL = {
  sac: { color: 0xcfd4da, metalness: 0.45, roughness: 0.42 },
  kapak: { color: 0xdfe4ea, metalness: 0.4, roughness: 0.38 },
  profil: { color: 0xb3bac3, metalness: 0.5, roughness: 0.38 },
  kaynak: { color: 0xe3151b, emissive: 0x8a0000, emissiveIntensity: 0.55, metalness: 0.2, roughness: 0.5 },
  punta: { color: 0xe3151b, emissive: 0x8a0000, emissiveIntensity: 0.7, metalness: 0.2, roughness: 0.5 },
  yapistirici: { color: 0x3ccf6a, emissive: 0x0d5a25, emissiveIntensity: 0.35, metalness: 0.0, roughness: 0.7 },
  baglanti: { color: 0x2f7bff, emissive: 0x0a2a6b, emissiveIntensity: 0.35, metalness: 0.4, roughness: 0.35 },
  arayuz: { color: 0x3d4652, metalness: 0.6, roughness: 0.35 },
  pu: { color: 0xf2c94c, metalness: 0.0, roughness: 0.85 },
  yalitim: { color: 0xe4d29a, metalness: 0.0, roughness: 0.95 },
  mekanizma: { color: 0x9aa3ad, metalness: 0.5, roughness: 0.4 },
  motor: { color: 0x2f3640, metalness: 0.5, roughness: 0.45 },
  alu: { color: 0xc3cad2, metalness: 0.55, roughness: 0.35 },
  koyu: { color: 0x454d57, metalness: 0.2, roughness: 0.6 },
  sensor: { color: 0xe0a31c, metalness: 0.2, roughness: 0.5 },
  elektrik: { color: 0xa9b1ba, metalness: 0.35, roughness: 0.5 },
  kanal: { color: 0xd7dbe0, metalness: 0.1, roughness: 0.6 },
  fis: { color: 0x3a3f47, metalness: 0.5, roughness: 0.4 },
  guc: { color: 0x8e1f22, metalness: 0.1, roughness: 0.6 },
  bilgi: { color: 0x1d3f7a, metalness: 0.1, roughness: 0.6 },
  hava: { color: 0x1f9d55, metalness: 0.1, roughness: 0.6 },
  kapak_s: { color: 0xb9d3ea, metalness: 0.1, roughness: 0.2, transparent: true, opacity: 0.45, depthWrite: false },
  urun: { color: 0xd9a35b, metalness: 0.0, roughness: 0.8 },
  silik: { color: 0x8b98aa, metalness: 0.0, roughness: 0.9, transparent: true, opacity: 0.13, depthWrite: false },
  tezgah: { color: 0x9a7b52, metalness: 0.0, roughness: 0.85 },
  tepsi: { color: 0xc96a4a, metalness: 0.0, roughness: 0.7 }
};
const CIZGI_ESIK = { guc: 70, bilgi: 70, hava: 70, kanal: 40, urun: 50, silik: 30, tepsi: 60 };
const malz = {};
for (const k in MAL) malz[k] = new THREE.MeshStandardMaterial(Object.assign({ side: THREE.DoubleSide, clippingPlanes: kesitler, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 }, MAL[k]));
const kirmizi = new THREE.MeshBasicMaterial({ color: 0xd0262b, side: THREE.BackSide, clippingPlanes: kesitler });
const cizgiM = new THREE.LineBasicMaterial({ color: 0x111111, clippingPlanes: kesitler });
const cizgiSilik = new THREE.LineBasicMaterial({ color: 0x5d6b7c, transparent: true, opacity: 0.35, depthWrite: false, clippingPlanes: kesitler });
// bağlantı vurgusu (4 Eki): sac oturduğu anda kendisi + değdiği komşu / vida / kaynak kısa süre turuncu
const vurguM = new THREE.MeshStandardMaterial({ color: 0xff8a1c, emissive: 0xff6a00, emissiveIntensity: 0.55, side: THREE.DoubleSide, clippingPlanes: kesitler, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });

// ---------------------------------------------------------------- yardımcı gövdeler (sehpa + silik komşular)
function kutu(x0, x1, y0, y1, z0, z1, renk, op) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, y1 - y0, z1 - z0),
    new THREE.MeshStandardMaterial({ color: renk, transparent: op < 1, opacity: op, roughness: 0.8, depthWrite: op >= 1 }));
  m.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2); scene.add(m); return m;
}
const sehpa = D.sehpa && Z[0][1] > 0.06 ? kutu(Z[0][0] + 0.06, Z[1][0] - 0.06, 0, Z[0][1] - 0.002, Z[0][2] + 0.06, Z[1][2] - 0.06, 0x8a6f4a, 1) : null;   // montaj sehpası
const golgeler = (D.ghost || []).map(g => kutu(g[0], g[1], g[2], g[3], g[4], g[5], 0x7a8796, 0.18));

// ---------------------------------------------------------------- model
const parts = [];
function morfKenar(geo, esik) {
  // EdgesGeometry kenarlarını ağın köşe indislerine eşle → çizgiler morph ile birlikte bükülür
  const eg = new THREE.EdgesGeometry(geo, esik), pos = geo.attributes.position, ep = eg.attributes.position;
  const k = (x, y, z) => Math.round(x * 1e5) + ',' + Math.round(y * 1e5) + ',' + Math.round(z * 1e5);
  const m = new Map(); for (let i = 0; i < pos.count; i++) { const kk = k(pos.getX(i), pos.getY(i), pos.getZ(i)); if (!m.has(kk)) m.set(kk, i); }
  const idx = []; for (let i = 0; i < ep.count; i++) { const j = m.get(k(ep.getX(i), ep.getY(i), ep.getZ(i))); idx.push(j === undefined ? 0 : j); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', pos); g.morphAttributes.position = geo.morphAttributes.position; g.morphTargetsRelative = geo.morphTargetsRelative; g.setIndex(idx); return g;
}
function morfAgirlik(p, w, t) {
  // p.mf: [t0, t1, k0, k1] — k0 → k1 arası kareler sırayla (bir büküm 6 kare); segment dışında son ulaşılan kare; hepsi bitince taban (son konum)
  w.fill(0); const S = p.mf;
  if (t < S[0][0]) { w[S[0][2]] = 1; return; }
  for (const g of S) if (t >= g[0] && t <= g[1]) {
    const f = e(uu(t, g)) * (g[3] - g[2]), i = Math.min(Math.floor(f), g[3] - g[2] - 1), r = f - i;
    w[g[2] + i] += 1 - r; w[g[2] + i + 1] += r; return;
  }
  let son = null; for (const g of S) if (g[1] < t) son = g;
  if (son && son !== S[S.length - 1]) w[son[3]] = 1;
}
const gltf = await new GLTFLoader().loadAsync(KOK + '.glb' + V);
const kok = gltf.scene; scene.add(kok);
const mesler = [];
kok.traverse(o => { if (o.isMesh) mesler.push(o); });
for (const o of mesler) {
  const ad = o.name in D.parcalar ? o.name : (o.parent && o.parent.name in D.parcalar ? o.parent.name : null);
  if (!ad) { console.warn('JSON\'da yok', o.name); continue; }
  const p = D.parcalar[ad];
  const node = o.parent && o.parent.name === ad && o.parent !== kok ? o.parent : o;
  o.material = malz[p.m] || malz.sac;
  o.geometry.computeVertexNormals();
  const morf = !!(o.geometry.morphAttributes && o.geometry.morphAttributes.position && o.geometry.morphAttributes.position.length);
  const cz = new THREE.LineSegments(morf ? morfKenar(o.geometry, CIZGI_ESIK[p.m] || 30) : new THREE.EdgesGeometry(o.geometry, CIZGI_ESIK[p.m] || 30), p.m === 'silik' ? cizgiSilik : cizgiM); cz.raycast = () => {}; o.add(cz);
  const kz = new THREE.Mesh(o.geometry, kirmizi); kz.visible = false; kz.raycast = () => {}; o.add(kz);
  if (morf) { if (!o.morphTargetInfluences) o.updateMorphTargets(); cz.morphTargetInfluences = o.morphTargetInfluences; kz.morphTargetInfluences = o.morphTargetInfluences; }
  if (p.m === 'kapak_s') { o.renderOrder = 2; cz.visible = true; }
  if (p.m === 'silik') { o.renderOrder = 3; cz.renderOrder = 3; }
  parts.push({ ad, p, node, mesh: o, cz, kz, m0: o.material, c: new THREE.Vector3(...p.c) });
}
$('yuk').remove();
// ---------------------------------------------------------------- renk anahtarı (sabit lejant, sağ üst · kamera tuşunun altında)
{
  const st = document.createElement('style');
  st.textContent = `.km .lej{position:absolute;right:12px;top:52px;background:rgba(255,255,255,.93);border:1px solid #c9d2de;border-radius:10px;padding:7px 10px;font:600 11.5px/1.55 system-ui,sans-serif;color:#2b3542;pointer-events:none;max-width:46%}
  .km .lej i{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:6px;vertical-align:-1px;border:1px solid rgba(0,0,0,.25)}
  .km .lej .k{color:#68758a;font-weight:500}
  @media (max-width:640px){.km .lej{font-size:10.5px;padding:5px 7px;top:48px}}`;
  document.head.appendChild(st);
  const lj = document.createElement('div'); lj.className = 'lej';
  lj.innerHTML = '<div><i style="background:#f2c94c"></i>Sarı = yalıtım (PU levha)</div><div><i style="background:#ff8a1c"></i>Turuncu = şu an takılan parça</div>' +
    '<div><i style="background:#e3151b"></i>Kırmızı = kaynak (dikiş / punta, kalıcı)</div><div><i style="background:#2f7bff"></i>Mavi = vida / cıvata / perçin / PEM</div>' +
    '<div><i style="background:#3ccf6a"></i>Yeşil = yapıştırıcı / silikon</div><div class="k"><i style="background:#8e1f22"></i>güç kablosu · <i style="background:#1d3f7a"></i>bilgi kablosu</div>';
  kap.appendChild(lj);
}
const Y = new THREE.Vector3(0, 1, 0);
const e = u => { u = Math.min(Math.max(u, 0), 1); return u * u * (3 - 2 * u); };
const uu = (t, h) => t >= h[1] ? 1 : (t <= h[0] ? 0 : (t - h[0]) / (h[1] - h[0]));

function uygula(t) {
  for (const q of parts) {
    const p = q.p, n = q.node, vis = t >= p.g - 1e-9;
    n.visible = vis; if (!vis) continue;
    let ox = 0, oy = 0, oz = 0;
    for (const h of p.h) { const k = 1 - e(uu(t, h)); ox += h[2] * k; oy += h[3] * k; oz += h[4] * k; }
    let a = 0, px = 0, pz = 0; if (p.r) for (const r of p.r) { a += r[2] * e(uu(t, r)); px = r[3]; pz = r[4]; }
    if (Math.abs(a) > 1e-9) {
      const rad = a * Math.PI / 180, cs = Math.cos(rad), sn = Math.sin(rad), dx = q.c.x - px, dz = q.c.z - pz;
      n.position.set(px + cs * dx + sn * dz + ox, q.c.y + oy, pz - sn * dx + cs * dz + oz);
      n.quaternion.setFromAxisAngle(Y, rad);
    } else { n.position.set(q.c.x + ox, q.c.y + oy, q.c.z + oz); n.quaternion.identity(); }
    if (p.vu) q.mesh.material = p.vu.some(v => t >= v[0] && t <= v[1]) ? vurguM : q.m0;
    if (p.mf && q.mesh.morphTargetInfluences) morfAgirlik(p, q.mesh.morphTargetInfluences, t);
    if (p.buyu) n.scale.setScalar(Math.max(1e-3, e(uu(t, p.buyu))));
    else if (p.k && p.h.length) n.scale.setScalar(Math.max(1e-3, e(uu(t, p.h[0]))));
    else n.scale.setScalar(1);
  }
  const gh = D.ghost_t != null && t >= D.ghost_t;
  if (sehpa) sehpa.visible = !gh;
  for (const g of golgeler) g.visible = gh;
}

// ---------------------------------------------------------------- son kare doğrulaması (≤ 0,01 mm)
const _v = new THREE.Vector3();
function sonKareDenetim() {
  uygula(T_SON + 1e-6); kok.updateMatrixWorld(true);
  let enb = 0, kotu = 0; const b = new THREE.Box3();
  for (const q of parts) {
    // taban köşeleri (morph hedefleri hariç — computeBoundingBox morph uçlarını da katar)
    const pos = q.mesh.geometry.attributes.position; b.makeEmpty();
    for (let i = 0; i < pos.count; i++) b.expandByPoint(_v.fromBufferAttribute(pos, i).applyMatrix4(q.mesh.matrixWorld));
    const f = Math.max(Math.abs(b.min.x - q.p.bb[0][0]), Math.abs(b.min.y - q.p.bb[0][1]), Math.abs(b.min.z - q.p.bb[0][2]),
      Math.abs(b.max.x - q.p.bb[1][0]), Math.abs(b.max.y - q.p.bb[1][1]), Math.abs(b.max.z - q.p.bb[1][2])) * 1000;
    enb = Math.max(enb, f); if (f > 0.01) kotu++;
  }
  return { enb, kotu, n: parts.length };
}
const SK = sonKareDenetim();
console.log(`${IST.toUpperCase()} montaj · son kare: ${SK.n} parça · en büyük bbox farkı ${SK.enb.toFixed(4)} mm · eşik üstü ${SK.kotu}`);

// ---------------------------------------------------------------- arayüz
const A = D.adimlar;
const QS = new URLSearchParams(location.search);
let acn2B = false;
let t = QS.has('t') ? +QS.get('t') : 0, oyna = !QS.has('t'), hiz = 1, kamOto = true, sonAdim = -1, acnSecim = null, acnElle = false;
$('adim').innerHTML = A.map((a, i) => `<button data-i="${i}">${a.no} · ${a.ad}</button>`).join('');
$('adim').onclick = ev => { const b = ev.target.closest('button'); if (!b) return; git(A[+b.dataset.i].t0 + 0.001); };
$('tz').max = T_SON;
$('sira').innerHTML = A.map(a => `<li><b>${a.ad}</b> — ${a.liste}</li>`).join('');
const ds = D.sayim, dn = D.denetim;
$('dis').textContent = D.aciklama || `Animasyonda ${ds.gosterilen} öğe var: ${ds.sac || ds.uretilen} sac (açınım → büküm kareleriyle), ${ds.baglanti} bağlantı elemanı (vida, cıvata, perçin, PEM, pul, somun — her biri kendi ekseninde), ${ds.kaynak} kaynak dikişi / punta grubu (kırmızı, kalıcı); satın alınan ürünler tek parça. Toplam ${ds.ucgen.toLocaleString('tr-TR')} üçgen.`;
function git(tt) { t = Math.min(Math.max(tt, 0), T_SON); }
$('tz').oninput = () => { t = +$('tz').value; };
$('oy').onclick = () => { if (!oyna && t >= T_SON - 1e-3) t = 0; oyna = !oyna; $('oy').innerHTML = oyna ? '&#10074;&#10074;' : '&#9654;'; };
const adimNo = tt => { let k = 0; for (let i = 0; i < A.length; i++) if (tt >= A[i].t0 - 1e-6) k = i; return k; };
$('ileri').onclick = () => { const k = adimNo(t); if (k < A.length - 1) git(A[k + 1].t0 + 0.001); };
$('geri').onclick = () => { const k = adimNo(t); git(t - A[k].t0 > 0.8 || k === 0 ? A[k].t0 + 0.001 : A[k - 1].t0 + 0.001); };
$('hz').onclick = ev => { const b = ev.target.closest('button[data-h]'); if (!b) return; hiz = +b.dataset.h; $('hz').querySelectorAll('button[data-h]').forEach(x => x.classList.toggle('ak', x === b)); };
$('kam').onclick = () => { kamOto = !kamOto; kamYaz(); };
function kamYaz() { $('kam').setAttribute('aria-pressed', kamOto); $('kam').textContent = kamOto ? 'Kamera: otomatik' : 'Kamera: serbest'; }
controls.addEventListener('start', () => { if (kamOto) { kamOto = false; kamYaz(); } });
let kenarAcik = true;
$('kenar').onclick = () => { kenarAcik = !kenarAcik; $('kenar').setAttribute('aria-pressed', kenarAcik); for (const q of parts) q.cz.visible = kenarAcik; };
// kesit
const KB = [[Z[0][0] - 0.01, Z[1][0] + 0.01], [Z[0][1] - 0.01, Z[1][1] + 0.01], [Z[0][2] - 0.01, Z[1][2] + 0.01]];
function kesitYaz() {
  const ac = $('kesit').getAttribute('aria-pressed') === 'true', ex = $('kesx').value, i = 'xyz'.indexOf(ex), d = +$('kesd').value;
  kesitler.length = 0;
  if (ac) { const n = new THREE.Vector3(); n.setComponent(i, -1); kesitDuz.normal.copy(n); kesitDuz.constant = KB[i][0] + (KB[i][1] - KB[i][0]) * d; kesitler.push(kesitDuz); }
  for (const q of parts) q.kz.visible = ac && q.p.m !== 'kapak_s' && q.p.m !== 'silik';
  for (const k in malz) malz[k].needsUpdate = true; kirmizi.needsUpdate = true; cizgiM.needsUpdate = true; cizgiSilik.needsUpdate = true; vurguM.needsUpdate = true;
}
$('kesit').onclick = () => { $('kesit').setAttribute('aria-pressed', $('kesit').getAttribute('aria-pressed') !== 'true'); kesitYaz(); };
$('kesx').onchange = kesitYaz; $('kesd').oninput = kesitYaz;
const ACIK = (dn.cakismalar || []).map(c => `${c.a} ↔ ${c.b} (t ${sayi(c.t, 1)} s)`);
const MA = Object.entries(dn.haric || {}).filter(([k, v]) => v.startsWith('MODEL AÇIĞI')).map(([k]) => k);
$('dog').innerHTML = `<b class="${SK.kotu ? 'k' : ''}">Son kare:</b> ${SK.n} öğe kaynak modelle aynı yerde — en büyük bbox farkı ${sayi(SK.enb, 4)} mm (eşik 0,01 mm).<br>` +
  `<b class="${dn.cakisma ? 'k' : ''}">Yol denetimi:</b> ${dn.cift} parça çifti, ${sayi(dn.adim_mm, 0)} mm adım, üçgen düzeyinde — çakışma <b class="${dn.cakisma ? 'k' : ''}">${dn.cakisma}</b> · büküm karelerinde sorun ${(dn.uretim_kare_sorun || []).length} · yerinde belirme ${dn.belirme} · havada ${(dn.havada || []).length}` +
  (dn.model_acigi != null ? ` · model açığı <b class="${dn.model_acigi ? 'k' : ''}">${dn.model_acigi}</b>` : '') + '. ' + (D.istisna_metin || 'Kablolar, kayış ve hortumlar kanal / kasnak boyunca uzar; kaynak dikişleri, puntalar, yapıştırıcı ve silikon birleşme anında belirir ve kalır.') +
  (ACIK.length ? `<br><b class="k">YOL ÇAKIŞMASI:</b> ${ACIK.slice(0, 12).join(' · ')}${ACIK.length > 12 ? ' …' : ''}` : '') +
  (MA.length ? `<br><b class="k">MODEL AÇIKLARI:</b> ${MA.length} parça çifti (${MA.slice(0, 6).join(' · ')}${MA.length > 6 ? ' …' : ''}).` : '');

let acnSon = '';

// ---------------------------------------------------------------- açınım kartı (üretim sırasında köşede)
let acnSonAd = null;
function acnKart(tt) {
  const A2 = (D.acinim || []).find(x => tt >= x.t0 && tt <= x.t1 + 0.6);
  const el = $('acnk'); if (!el) return;
  if (!A2) { el.style.display = 'none'; acnSonAd = null; return; }
  el.style.display = 'block';
  if (acnSonAd === A2.ad) return; acnSonAd = A2.ad;
  const bk = A2.bukum.length ? A2.bukum.map(b => `<li>${b.no} · ${b.ack} · ${sayi(b.aci, 0)}°</li>`).join('') : '<li>büküm yok (düz parça)</li>';
  el.innerHTML = `<div class="t">AÇINIM · LAZER → ABKANT</div><div class="a">${A2.ac}</div><div class="o">${A2.ac.startsWith('on_cerceve') ? 'AISI 430' : 'AISI 304'} · t ${sayi(A2.t, 1)} mm · düz levha ${sayi(A2.levha[0], 1)} × ${sayi(A2.levha[1], 1)} mm</div><ol>${bk}</ol>`;
}

// ---------------------------------------------------------------- kamera
const K = D.kamera;
const _p = new THREE.Vector3(), _q = new THREE.Vector3(), _h0 = new THREE.Vector3(), _h1 = new THREE.Vector3();
function kamera(tt) {
  let k = 0; for (let i = 0; i < K.length; i++) if (tt >= K[i][0]) k = i;
  const b = K[k], a = K[Math.max(0, k - 1)], f = e((tt - b[0]) / 1.6);
  _p.set(...a[1]).lerp(_q.set(...b[1]), f); _h0.set(...a[2]).lerp(_h1.set(...b[2]), f);
  camera.position.copy(_p); controls.target.copy(_h0);
}
function kamOlcek() { const r = kap.clientWidth / kap.clientHeight; return r < 1 ? 1.45 : (r < 1.4 ? 1.15 : 1); }

// ---------------------------------------------------------------- döngü
let onceki = performance.now();
function kare(now) {
  const dt = Math.min(0.1, (now - onceki) / 1000); onceki = now;
  if (oyna) { t += dt * hiz; if (t >= T_SON) { t = T_SON; oyna = false; $('oy').innerHTML = '&#9654;'; } }
  uygula(t);
  if (kamOto) {
    kamera(t);
    const s = kamOlcek(); if (s !== 1) camera.position.sub(controls.target).multiplyScalar(s).add(controls.target);
  }
  controls.update();
  const k = adimNo(t), a = A[k];
  if (k !== sonAdim) {
    sonAdim = k; acnElle = false; acnSon = '';
    $('adim').querySelectorAll('button').forEach((b, j) => b.classList.toggle('ak', j === k));
    $('bas').textContent = `${a.no} · ${a.ad}`; $('met').textContent = a.metin; $('lis').textContent = a.liste;
    $('no').textContent = `ADIM ${a.no} / ${A.length}`;
  }
  { let m = ''; for (const o of D.olaylar) if (t >= o[0] - 1e-6) m = o[1]; $('olay').textContent = m; }
  acnKart(t);
  if (document.activeElement !== $('tz')) $('tz').value = t;
  $('sn').textContent = `${sayi(t)} / ${sayi(T_SON, 0)} sn`;
  renderer.render(scene, camera);
  requestAnimationFrame(kare);
}
requestAnimationFrame(kare);
let _kareSay = 0; (function say() { if (++_kareSay < 5) requestAnimationFrame(say); else window.__hazir = true; })();
window.__km = { scene, camera, parts, kok, THREE, D, SK, git: x => { t = x; oyna = false; }, oynat: () => { oyna = true; }, hiz: h => { hiz = h; } };
