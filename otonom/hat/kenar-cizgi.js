/* v2 · kenar çizgileri (SolidWorks "gölgeli + kenarlar") — Kemal 29 Eyl 2026: "modellemelerin hepsinde çizgi olacak".
   Sayfadaki BÜTÜN <model-viewer>'lara uygulanır. GLB değişmez: her ağın keskin (> 30°) ve açık kenarları sayfada hesaplanır,
   ağın çocuğu olarak siyah çizgi eklenir → animasyon, gizleme, kesit düzlemi ve kapak saydamlığıyla uyumlu.
   Düğme: sayfada #kenar varsa o (makine.html), yoksa her görüntüleyicinin altına küçük bir "Kenar çizgileri" düğmesi eklenir. */
(function () {
  const ESIK = Math.cos(30 * Math.PI / 180), Q = 1e4;

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
      if (L < 1e-14) continue; nx /= L; ny /= L; nz /= L;
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
    for (const s of harita.values()) if (s) out.push(P.getX(s[0]), P.getY(s[0]), P.getZ(s[0]), P.getX(s[1]), P.getY(s[1]), P.getZ(s[1]));
    return out;
  }

  function kur(mv, btn, dur) {
    let cizgiler = [], acik = true, kuruldu = false, kuruluyor = false, malz = null, src = mv.src;
    const sahne = () => mv[Object.getOwnPropertySymbols(mv).find(s => s.description === 'scene')];
    async function hesapla() {
      const sc = sahne(); if (!sc || kuruluyor) return; kuruluyor = true;
      const aglar = []; sc.traverse(o => { if (o.isMesh && o.geometry && o.geometry.attributes.position && !o.userData.yalitimKesit && !o.userData.kenarCizgi) aglar.push(o); });
      if (!aglar.length) { kuruluyor = false; return false; }
      const m0 = Array.isArray(aglar[0].material) ? aglar[0].material[0] : aglar[0].material;
      malz = m0.clone();
      Object.assign(malz, { transparent: false, opacity: 1, depthWrite: true, map: null, normalMap: null, roughnessMap: null, metalnessMap: null, emissiveMap: null, aoMap: null, envMapIntensity: 0, metalness: 0, roughness: 1 });
      if (malz.color) malz.color.setRGB(0.02, 0.02, 0.025); if (malz.emissive) malz.emissive.setRGB(0, 0, 0); malz.name = 'KENAR_CIZGI'; malz.needsUpdate = true;
      for (let i = 0; i < aglar.length; i++) {
        const m = aglar[i];
        (Array.isArray(m.material) ? m.material : [m.material]).forEach(x => { x.polygonOffset = true; x.polygonOffsetFactor = 1; x.polygonOffsetUnits = 1; x.needsUpdate = true; });
        const d = kenarlar(m.geometry);
        if (d.length) {
          const g = new m.geometry.constructor(), A = m.geometry.attributes.position.constructor;
          g.setAttribute('position', new A(new Float32Array(d), 3));
          const nrm = new Float32Array(d.length); for (let j = 1; j < nrm.length; j += 3) nrm[j] = 1; g.setAttribute('normal', new A(nrm, 3));
          g.computeBoundingSphere();
          const l = new m.constructor(g, malz);
          l.isMesh = false; l.isLine = true; l.isLineSegments = true; l.type = 'LineSegments';
          l.raycast = () => {}; l.userData.kenarCizgi = true; l.name = 'KENAR_' + (m.name || i); l.renderOrder = 1;
          m.add(l); cizgiler.push(l);
        }
        if (i % 12 === 11) { if (dur) dur.textContent = 'kenar çizgileri %' + Math.round(100 * i / aglar.length); await new Promise(r => setTimeout(r, 0)); }
      }
      kuruldu = true; kuruluyor = false; if (dur) dur.textContent = ''; esitle(true); return true;
    }
    function esitle(zorla) {
      if (!kuruldu) return;
      let P = null, degisti = !!zorla;
      for (const l of cizgiler) {
        if (!l.parent) continue;
        const pm = Array.isArray(l.parent.material) ? l.parent.material[0] : l.parent.material;
        if (pm && pm.clippingPlanes && pm.clippingPlanes.length) P = pm.clippingPlanes;
        const gor = acik && !(pm && pm.transparent && pm.opacity < 0.35);
        if (l.visible !== gor) { l.visible = gor; degisti = true; }
      }
      if (malz.clippingPlanes !== P) { malz.clippingPlanes = P; malz.needsUpdate = true; degisti = true; }
      if (degisti) { const sc = sahne(); if (sc && sc.queueRender) sc.queueRender(); }
    }
    function basla() {
      if (!acik || kuruldu || kuruluyor) return;
      const sc = mv.loaded && sahne(); let var_ = false;
      if (sc) sc.traverse(o => { if (o.isMesh && !o.userData.kenarCizgi) var_ = true; });
      if (var_) hesapla(); else setTimeout(basla, 1000);
    }
    btn.onclick = () => { acik = !acik; btn.setAttribute('aria-pressed', acik); if (dur) dur.textContent = acik ? '' : 'kapalı'; if (acik && !kuruldu) basla(); esitle(true); };
    mv.addEventListener('load', () => {                                   // model değişince (src) yeniden
      if (mv.src !== src) { src = mv.src; cizgiler = []; kuruldu = false; }
      setTimeout(basla, 300);
    });
    basla();
    setInterval(() => esitle(false), 250);
  }

  function hepsi() {
    document.querySelectorAll('model-viewer').forEach((mv, i) => {
      if (mv.dataset.kenar) return; mv.dataset.kenar = '1';
      let btn = document.getElementById('kenar'), dur = document.getElementById('kenar-durum');
      if (!btn || mv.id !== 'mv') {
        const kap = document.createElement('div'); kap.style.cssText = 'display:flex;gap:8px;align-items:center;margin:6px 0';
        btn = document.createElement('button'); btn.type = 'button'; btn.textContent = 'Kenar çizgileri'; btn.setAttribute('aria-pressed', 'true');
        btn.style.cssText = 'border:1px solid #39424f;background:#232932;color:#cfd6df;border-radius:8px;padding:5px 10px;font:600 12px system-ui,sans-serif;cursor:pointer';
        dur = document.createElement('span'); dur.style.cssText = 'color:#8d97a4;font:12px system-ui,sans-serif';
        kap.append(btn, dur); mv.insertAdjacentElement('afterend', kap);
      }
      kur(mv, btn, dur);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', hepsi); else hepsi();
})();
