/* v1 · kenar çizgileri (SolidWorks "gölgeli + kenarlar" görünümü) — Kemal 29 Eyl 2026.
   GLB değişmez. Sayfa açılınca her ağın KESKİN kenarları (iki yüz arası > 30°) ve açık kenarları hesaplanır,
   ağın çocuğu olarak siyah çizgi eklenir → animasyonla birlikte hareket eder, "Sadece dış kabuk" gizleyince gizlenir,
   kesit düzlemiyle birlikte kırpılır, şeffaflaşan ön kapaklarda kaybolur. Model-viewer'ın kendi three.js sınıfları kullanılır. */
(function () {
  const mv = document.getElementById('mv'), btn = document.getElementById('kenar'), dur = document.getElementById('kenar-durum');
  if (!mv || !btn) return;
  const ESIK = Math.cos(30 * Math.PI / 180), Q = 1e4;   // 30° · konum kaynaştırma 0,1 mm (GLB metre)
  let cizgiler = [], acik = true, kuruldu = false, kuruluyor = false, malz = null;
  const sahne = () => mv[Object.getOwnPropertySymbols(mv).find(s => s.description === 'scene')];

  function kenarlar(geo) {
    const P = geo.attributes.position, idx = geo.index, n = idx ? idx.count : P.count;
    const anahtar = new Array(P.count), harita = new Map(), out = [];
    for (let i = 0; i < P.count; i++) anahtar[i] = Math.round(P.getX(i) * Q) + ',' + Math.round(P.getY(i) * Q) + ',' + Math.round(P.getZ(i) * Q);
    const v = i => idx ? idx.getX(i) : i;
    for (let f = 0; f < n; f += 3) {
      const a = v(f), b = v(f + 1), c = v(f + 2);
      const ax = P.getX(a), ay = P.getY(a), az = P.getZ(a), ux = P.getX(b) - ax, uy = P.getY(b) - ay, uz = P.getZ(b) - az,
            wx = P.getX(c) - ax, wy = P.getY(c) - ay, wz = P.getZ(c) - az;
      let nx = uy * wz - uz * wy, ny = uz * wx - ux * wz, nz = ux * wy - uy * wx; const L = Math.hypot(nx, ny, nz);
      if (L < 1e-12) continue; nx /= L; ny /= L; nz /= L;
      const k = [anahtar[a], anahtar[b], anahtar[c]], iv = [a, b, c];
      for (let e = 0; e < 3; e++) {
        const i0 = iv[e], i1 = iv[(e + 1) % 3], k0 = k[e], k1 = k[(e + 1) % 3];
        if (k0 === k1) continue;
        const h = k0 < k1 ? k0 + '|' + k1 : k1 + '|' + k0, s = harita.get(h);
        if (s === undefined) harita.set(h, [i0, i1, nx, ny, nz]);
        else if (s !== null) {
          if (s[2] * nx + s[3] * ny + s[4] * nz < ESIK) out.push(P.getX(s[0]), P.getY(s[0]), P.getZ(s[0]), P.getX(s[1]), P.getY(s[1]), P.getZ(s[1]));
          harita.set(h, null);
        }
      }
    }
    for (const s of harita.values()) if (s) out.push(P.getX(s[0]), P.getY(s[0]), P.getZ(s[0]), P.getX(s[1]), P.getY(s[1]), P.getZ(s[1]));   // açık kenar
    return out;
  }

  async function kur() {
    const sc = sahne(); if (!sc || kuruluyor) return; kuruluyor = true;
    const aglar = []; sc.traverse(o => { if (o.isMesh && o.geometry && o.geometry.attributes.position && !o.userData.yalitimKesit && !o.userData.kenarCizgi) aglar.push(o); });
    if (!aglar.length) { kuruluyor = false; return; }
    malz = aglar[0].material.clone();
    Object.assign(malz, { transparent: false, opacity: 1, depthWrite: true, map: null, normalMap: null, roughnessMap: null, metalnessMap: null, emissiveMap: null, aoMap: null, envMapIntensity: 0, metalness: 0, roughness: 1 });
    malz.color.setRGB(0.02, 0.02, 0.025); if (malz.emissive) malz.emissive.setRGB(0, 0, 0); malz.name = 'KENAR_CIZGI'; malz.needsUpdate = true;
    const t0 = performance.now();
    for (let i = 0; i < aglar.length; i++) {
      const m = aglar[i];
      (Array.isArray(m.material) ? m.material : [m.material]).forEach(x => { x.polygonOffset = true; x.polygonOffsetFactor = 1; x.polygonOffsetUnits = 1; x.needsUpdate = true; });
      const d = kenarlar(m.geometry);
      if (d.length) {
        const g = new m.geometry.constructor(), A = m.geometry.attributes.position.constructor;
        g.setAttribute('position', new A(new Float32Array(d), 3));
        const nrm = new Float32Array(d.length); for (let j = 1; j < nrm.length; j += 3) nrm[j] = 1; g.setAttribute('normal', new A(nrm, 3));
        g.computeBoundingSphere();
        const l = new m.constructor(g, malz);                  // aynı three.js örneği: çizgi olarak çizilir
        l.isMesh = false; l.isLine = true; l.isLineSegments = true; l.type = 'LineSegments';
        l.raycast = () => {}; l.userData.kenarCizgi = true; l.name = 'KENAR_' + (m.name || i); l.renderOrder = 1;
        m.add(l); cizgiler.push(l);
      }
      if (i % 12 === 11) { dur.textContent = 'kenar çizgileri hazırlanıyor · %' + Math.round(100 * i / aglar.length); await new Promise(r => setTimeout(r, 0)); }
    }
    kuruldu = true; kuruluyor = false;
    dur.textContent = acik ? '' : 'kapalı';
    console.log('kenar çizgileri', cizgiler.length, 'ağ', Math.round(performance.now() - t0), 'ms');
    esitle(true);
  }

  function esitle(zorla) {
    if (!kuruldu) return;
    let P = null, degisti = !!zorla;
    for (const l of cizgiler) {
      const pm = Array.isArray(l.parent.material) ? l.parent.material[0] : l.parent.material;
      if (pm && pm.clippingPlanes && pm.clippingPlanes.length) P = pm.clippingPlanes;
      const g = acik && !(pm && pm.transparent && pm.opacity < 0.35);
      if (l.visible !== g) { l.visible = g; degisti = true; }
    }
    if (malz.clippingPlanes !== P) { malz.clippingPlanes = P; malz.needsUpdate = true; degisti = true; }
    if (degisti) { const sc = sahne(); if (sc && sc.queueRender) sc.queueRender(); }
  }

  btn.onclick = () => { acik = !acik; btn.setAttribute('aria-pressed', acik); dur.textContent = acik ? '' : 'kapalı'; if (acik && !kuruldu) kur(); esitle(true); };
  const basla = () => {                                       // model sahneye girene kadar dene (yükleme olayı ağlardan önce gelebiliyor)
    if (!acik || kuruldu || kuruluyor) return;
    const sc = mv.loaded && sahne(); let var_ = false;
    if (sc) sc.traverse(o => { if (o.isMesh && !o.userData.kenarCizgi) var_ = true; });
    if (var_) kur(); else setTimeout(basla, 1000);
  };
  mv.addEventListener('load', () => setTimeout(basla, 300));
  basla();
  setInterval(() => esitle(false), 250);                     // kesit / kapak saydamlığı / dış kabuk değişince eşitle
})();
