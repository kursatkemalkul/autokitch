import {GLTFLoader} from './vendor/GLTFLoader.js';
import {MeshoptDecoder} from './vendor/meshopt_decoder.module.js';
export async function yukle(IKIZ){
const MODEL='./model/', $=id=>document.getElementById(id);
const parts=await fetch(MODEL+'parts.json').then(r=>r.json());
async function modelFetch(url){const n=url.slice(MODEL.length).split('?')[0];const chunks=[];let len=0;for(const p of parts[n]){const r=await fetch(MODEL+p);if(!r.ok)throw Error(p+' HTTP '+r.status);const b=new Uint8Array(await r.arrayBuffer());chunks.push(b);len+=b.length;$('yukleMetin').textContent='3B parçalar yükleniyor: '+Math.round(len/1048576)+' MB';}const bytes=new Uint8Array(len);let o=0;for(const c of chunks){bytes.set(c,o);o+=c.length;}const stream=new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));return new Response(stream);}
async function modelYukle() {
  const [E, ENT] = await Promise.all([fetch(MODEL + 'ikiz_esleme.json').then(r => r.json()), import(MODEL + 'ikiz-esleme.js')]);
  const yanit = await modelFetch(MODEL + E.glb + '?v=' + E.glb_sha256.slice(0, 12));          // köprü Content-Encoding: gzip → tarayıcı açar
  if (!yanit.ok) throw new Error('GLB HTTP ' + yanit.status);
  const tahmin = 305e6, kovan = [];
  let oku = 0; const rd = yanit.body.getReader();
  for (;;) {
    const { done, value } = await rd.read(); if (done) break; kovan.push(value); oku += value.length;
    $('yukleCubuk').style.width = Math.min(99, oku / tahmin * 100) + '%'; $('yukleMetin').textContent = `3B dükkân indiriliyor… ${(oku / 1048576).toFixed(0)} MB`;
  }
  const buf = new Uint8Array(oku); let o = 0; for (const k of kovan) { buf.set(k, o); o += k.length; } kovan.length = 0;
  $('yukleMetin').textContent = '3B dükkân çözülüyor…';
  const loader = new GLTFLoader(); loader.setMeshoptDecoder(MeshoptDecoder);
  const gltf = await new Promise((coz, red) => loader.parse(buf.buffer, '', coz, red));
  /* EK GLB (ENT tur 6+: web paketine girmeyen B100+ — robot kapakları, QR kabloları, tablet, duvar panosu): ENT'in ikizEkYukle kuralı aynen
     (gizle_web listesi gizlenir + adı '__web_gizli' olur, ek sahne aynı köke eklenir); dosya köprüden Content-Encoding: gzip ile gelir (tarayıcı açar). */
  /* TOPPING düzeltme (11 Eki akşam, S3): ek GLB bir düğümün YALNIZ kendi ağını değiştirir — gizlenen web düğümünün ekte bulunmayan çocukları (ör. TOPPING_DONER__TABLA__BANT)
     ekteki yeni düğümün altına dünya konumu korunarak taşınır (yoksa bant da gizleniyordu, pide boşlukta duruyordu). */
  const cocukTasi = (adlar, ekSahne) => { gltf.scene.updateMatrixWorld(true); let n = 0;
    for (const a of adlar) { const eski = gltf.scene.getObjectByName(a + '__web_gizli'), yeni = ekSahne.getObjectByName(a); if (!eski || !yeni) continue;
      for (const c of [...eski.children]) { if (!c.name || ekSahne.getObjectByName(c.name)) continue; yeni.attach(c); c.visible = true; n++; } }
    return n; };
  let ek = null;
  if (E.ek_glb && E.ek_glb.dosya) {
    $('yukleMetin').textContent = '3B ek parçalar indiriliyor…';
    const ey = await modelFetch(MODEL + E.ek_glb.dosya + '?v=' + (E.ek_glb.glb_sha256 || '').slice(0, 12));
    if (!ey.ok) throw new Error('ek GLB HTTP ' + ey.status);
    const eb = await ey.arrayBuffer();
    ek = await new Promise((coz, red) => loader.parse(eb, '', coz, red));
    const gz = new Set(E.ek_glb.gizle_web || []);
    gltf.scene.traverse(o => { if (gz.has(o.name)) o.visible = false; });
    for (const n of gz) { const o = gltf.scene.getObjectByName(n); if (o) o.name = n + '__web_gizli'; }
    ek.scene.name = 'IKIZ_EK'; gltf.scene.add(ek.scene);
    const tak = []; ek.scene.traverse(o => { if (o.userData && o.userData.ebeveyn) tak.push(o); });                // ENT GOVDE-4 kuralı (ikizEkYukle): extras.ebeveyn → web ebeveyninin altına, yerel TRS
    for (const o of tak) { const p = gltf.scene.getObjectByName(o.userData.ebeveyn); if (p) p.add(o); }
    IKIZ.ekCocukTasinan = cocukTasi(gz, ek.scene);
  }
  /* TUTUCU GLB (ENT ikiz-v2, ROBOT-TUTUCU-2): kök 'Tool' → extras ebeveyn (UR10E_body_06) altına birim dönüşümle; ürün şablonları gizli (elde ürünü sürücü çizer). ENT ikizTutucuYukle kuralı. */
  IKIZ.tutucu = null; IKIZ.gltfListe = [gltf].concat(ek ? [ek] : []);          // KABUL-C: GLB'deki özgün düğüm adı (parser.associations)
  if (E.tutucu_glb && E.tutucu_glb.dosya) {
    $('yukleMetin').textContent = '3B tutucu indiriliyor…';
    const r = await modelFetch(MODEL + E.tutucu_glb.dosya + '?v=' + (E.tutucu_glb.glb_sha256 || '').slice(0, 12)); if (!r.ok) throw new Error('tutucu GLB HTTP ' + r.status);
    const t = await new Promise(async (coz, red) => loader.parse(await r.arrayBuffer(), '', coz, red));
    const tool = t.scene.getObjectByName(E.tutucu_glb.kok || 'Tool'), p = gltf.scene.getObjectByName(E.tutucu_glb.ebeveyn);
    if (tool) tool.traverse(o => { if (o.userData && o.userData.urun_sablon) { o.visible = false; o.userData.urun = true; } });
    if (tool && p) p.add(tool);
    IKIZ.tutucu = { dosya: E.tutucu_glb.dosya, bagli: !!(tool && p) }; IKIZ.gltfListe.push(t);
  }
  IKIZ.ekGlb = ek ? { dugum: E.ek_glb.dugum_sayisi, gizlenen: (E.ek_glb.gizle_web || []).length } : null;
  /* EK GLB LİSTESİ (`E.ek_glb_ekler`, başlatıcı --ek-ekle): ENT final paketinden önce deneme ekleri (ör. 142 perde). Aynı kural: gizle_web adları bütün sahnede
     (web + önceki ekler) gizlenir ve yeniden adlanır, sonra ek sahne köke eklenir — sürücü adı yalnız yeni (görünür) kopyada bulur. */
  IKIZ.ekGlbler = [];
  for (const x of (E.ek_glb_ekler || [])) {
    $('yukleMetin').textContent = '3B ek parçalar indiriliyor… ' + x.dosya;
    const r = await modelFetch(MODEL + x.dosya + '?v=' + (x.glb_sha256 || '').slice(0, 12)); if (!r.ok) throw new Error('ek GLB HTTP ' + r.status + ' ' + x.dosya);
    const e2 = await new Promise(async (coz, red) => loader.parse(await r.arrayBuffer(), '', coz, red));
    const gz = new Set(x.gizle_web || []); let gizlenen = 0;
    gltf.scene.traverse(o => { if (gz.has(o.name)) { o.visible = false; o.name = o.name + '__web_gizli'; gizlenen++; } });
    e2.scene.name = 'IKIZ_EK_' + IKIZ.ekGlbler.length; gltf.scene.add(e2.scene);
    IKIZ.ekGlbler.push({ dosya: x.dosya, gizlenen, cocuk_tasinan: cocukTasi(gz, e2.scene) }); IKIZ.gltfListe.push(e2);
  }
  return { gltf, E, ENT };
}

return modelYukle();
}
