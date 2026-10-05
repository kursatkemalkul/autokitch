// Bağımsız doğrulama: node dogrula.mjs ozgun.glb sikistirilmis.glb
// Sıkıştırılmış dosyayı DOSYADAN okur, her accessor'ı (POSITION / NORMAL / indis / animasyon) açar, özgünle bayt bayt karşılaştırır;
// JSON'da bufferViews / buffers / extensionsUsed / extensionsRequired dışındaki her şey (extras kat/mek/kpk, sahne extras, düğüm, malzeme, animasyon) aynı mı bakar.
import fs from 'fs';
import { MeshoptDecoder } from './package/meshopt_decoder.mjs';
await MeshoptDecoder.ready;
function oku(f) {
  const raw = fs.readFileSync(f), jl = raw.readUInt32LE(12), J = JSON.parse(raw.subarray(20, 20 + jl).toString('utf8'));
  const bo = 20 + jl, bl = raw.readUInt32LE(bo); return {J, BIN: raw.subarray(bo + 8, bo + 8 + bl)};
}
const A = oku(process.argv[2]), B = oku(process.argv[3]);
const BYTES = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}, NC = {SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16};
const cache = new Map();
function bvVeri(G, i) {
  const bv = G.J.bufferViews[i], e = bv.extensions && bv.extensions.EXT_meshopt_compression;
  if (!e) return G.BIN.subarray(bv.byteOffset || 0, (bv.byteOffset || 0) + bv.byteLength);
  if (cache.has(i)) return cache.get(i);
  const src = G.BIN.subarray(e.byteOffset || 0, (e.byteOffset || 0) + e.byteLength), dst = new Uint8Array(e.count * e.byteStride);
  MeshoptDecoder.decodeGltfBuffer(dst, e.count, e.byteStride, new Uint8Array(src), e.mode, e.filter || 'NONE');
  const b = Buffer.from(dst.buffer, 0, bv.byteLength); cache.set(i, b); return b;
}
function accVeri(G, i) {
  const a = G.J.accessors[i], n = BYTES[a.componentType] * NC[a.type] * a.count, o = a.byteOffset || 0;
  return bvVeri(G, a.bufferView).subarray(o, o + n);
}
let ayni = 0, farkli = 0;
const sinifla = {POSITION: [0, 0], NORMAL: [0, 0], indis: [0, 0], animasyon: [0, 0]};
const ekle = (k, ok) => { sinifla[k][ok ? 0 : 1]++; ok ? ayni++ : farkli++; };
for (const m of A.J.meshes) for (const p of m.primitives) {
  for (const [k, i] of Object.entries(p.attributes)) ekle(k, Buffer.compare(accVeri(A, i), accVeri(B, i)) === 0);
  if ('indices' in p) ekle('indis', Buffer.compare(accVeri(A, p.indices), accVeri(B, p.indices)) === 0);
}
for (const an of (A.J.animations || [])) for (const s of an.samplers) for (const x of [s.input, s.output]) ekle('animasyon', Buffer.compare(accVeri(A, x), accVeri(B, x)) === 0);
const tem = J => { const c = {...J}; for (const k of ['bufferViews', 'buffers', 'extensionsUsed', 'extensionsRequired']) delete c[k]; return JSON.stringify(c); };
const jsonAyni = tem(A.J) === tem(B.J);
const ex = J => JSON.stringify(J.meshes.map(m => m.primitives.map(p => p.extras))) + JSON.stringify(J.scenes.map(s => s.extras));
const hb = A.J.bufferViews.filter(v => !v.extensions).length, ex2 = B.J.bufferViews.filter(v => v.extensions && v.extensions.EXT_meshopt_compression);
const modlar = {}; for (const v of ex2) { const m = v.extensions.EXT_meshopt_compression.mode; modlar[m] = (modlar[m] || 0) + 1; }
console.log(JSON.stringify({accessor_ayni: ayni, accessor_farkli: farkli, sinif: sinifla, json_bufferViews_disi_ayni: jsonAyni, extras_ayni: ex(A.J) === ex(B.J),
  meshopt_bv: ex2.length, modlar, extensionsRequired: B.J.extensionsRequired}));
