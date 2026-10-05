// GLB → EXT_meshopt_compression (KAYIPSIZ: filtre yok, nicemleme yok, köşe/üçgen sırası aynı)
// node meshopt_kucult.mjs gir.glb cik.glb [--idx tri|seq|ham] [--u16]
//   --idx tri : indisler TRIANGLES kodeği (en küçük; üçgen sırası korunur, üçgen içi köşe döndürülebilir → doğrulamada bakılır)
//   --idx seq : indisler INDICES kodeği (bayt bayt aynı)
//   --idx ham : indisler sıkıştırılmaz
//   --u16     : köşe sayısı ≤ 65535 olan primitive'lerde UINT32 indis → UINT16 (değerler aynı, yalnız tip)
// Sıkıştırılmış her bufferView açılıp özgün baytlarla karşılaştırılır (tri modunda üçgen dizisi + dönüş denetimi).
import fs from 'fs';
import { MeshoptEncoder } from './package/meshopt_encoder.js';
import { MeshoptDecoder } from './package/meshopt_decoder.mjs';

const [gi, go, ...arg] = process.argv.slice(2);
const IDX = arg.includes('--idx') ? arg[arg.indexOf('--idx') + 1] : 'tri';
const U16 = arg.includes('--u16');
await MeshoptEncoder.ready; await MeshoptDecoder.ready;

const raw = fs.readFileSync(gi);
const jl = raw.readUInt32LE(12); const J = JSON.parse(raw.subarray(20, 20 + jl).toString('utf8'));
const bo = 20 + jl, bl = raw.readUInt32LE(bo), BIN = raw.subarray(bo + 8, bo + 8 + bl);
if (J.buffers.length !== 1) throw Error('tek buffer bekleniyor');

const acc = J.accessors, bvs = J.bufferViews;
// bufferView → rol
const rol = new Map();   // bv -> {mod, stride, count, accs:[]}
const set = (bvi, r) => { const o = rol.get(bvi); if (o && (o.mod !== r.mod || o.stride !== r.stride)) throw Error('bv çakışan rol ' + bvi); rol.set(bvi, r); };
const BYTES = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}, NC = {SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16};
const u16Acc = new Set();
for (const m of J.meshes) for (const p of m.primitives) {
  for (const a of Object.values(p.attributes)) { const A = acc[a]; set(A.bufferView, {mod: 'ATTRIBUTES', stride: BYTES[A.componentType] * NC[A.type], count: A.count, acc: a}); }
  if ('indices' in p) {
    const A = acc[p.indices], nv = acc[p.attributes.POSITION].count;
    if ((p.mode ?? 4) !== 4) throw Error('mode != 4');
    if (U16 && A.componentType === 5125 && nv <= 65535) u16Acc.add(p.indices);
    set(A.bufferView, {mod: IDX === 'tri' ? 'TRIANGLES' : IDX === 'seq' ? 'INDICES' : 'HAM', stride: (u16Acc.has(p.indices) || A.componentType === 5123) ? 2 : 4, count: A.count, acc: p.indices});
  }
}
for (const a of (J.animations || [])) for (const s of a.samplers) for (const x of [s.input, s.output]) {
  const A = acc[x]; set(A.bufferView, {mod: 'ATTRIBUTES', stride: BYTES[A.componentType] * NC[A.type], count: A.count, acc: x});
}
// her bv tek accessor + byteOffset 0 + sıkı paket mi?
for (const [bvi, r] of rol) {
  const A = acc[r.acc], bv = bvs[bvi];
  if ((A.byteOffset || 0) !== 0 || bv.byteStride) throw Error('ofsetli/stride bv ' + bvi);
  const srcStride = BYTES[A.componentType] * NC[A.type];
  if (bv.byteLength !== srcStride * A.count) throw Error('boy uyuşmuyor ' + bvi);
}

const out = [], fallback = { len: 0 };
let comp = 0, ham = 0, dogru = 0, donmus = 0, hata = 0;
const pad4 = n => (n + 3) & ~3;
const yeniBV = [];
for (let i = 0; i < bvs.length; i++) {
  const bv = bvs[i], r = rol.get(i);
  let src = BIN.subarray(bv.byteOffset || 0, (bv.byteOffset || 0) + bv.byteLength);
  if (!r) { // görüntü vb. ham kalır (ana tamponda)
    yeniBV.push({_ham: src, ...bv}); continue;
  }
  let srcStride = BYTES[acc[r.acc].componentType] * NC[acc[r.acc].type];
  let data = new Uint8Array(src.buffer, src.byteOffset, src.byteLength);
  if (r.stride === 2 && srcStride === 4) { // UINT32 → UINT16
    const u32 = new Uint32Array(data.slice().buffer), u16 = new Uint16Array(u32.length);
    for (let k = 0; k < u32.length; k++) { if (u32[k] > 65535) throw Error('u16 taşma'); u16[k] = u32[k]; }
    data = new Uint8Array(u16.buffer); acc[r.acc].componentType = 5123;
  }
  if (r.mod === 'HAM') { yeniBV.push({_ham: Buffer.from(data), ...bv, byteLength: data.length}); ham += data.length; continue; }
  const enc = MeshoptEncoder.encodeGltfBuffer(data, r.count, r.stride, r.mod);
  // doğrula: aç → karşılaştır
  const dec = new Uint8Array(r.count * r.stride);
  MeshoptDecoder.decodeGltfBuffer(dec, r.count, r.stride, enc, r.mod, 'NONE');
  if (Buffer.compare(Buffer.from(dec), Buffer.from(data)) === 0) dogru++;
  else if (r.mod === 'TRIANGLES') {
    // üçgen sırası aynı mı, üçgen içi döndürme mi?
    if (r.count * r.stride !== dec.length || data.length !== dec.length) console.log("UYUSMAZ", i, r.stride, r.count, data.length, dec.length, acc[r.acc].componentType);
    const T = r.stride === 1 ? Uint8Array : r.stride === 2 ? Uint16Array : Uint32Array;
    const nb = r.count * r.stride, a = new T(Uint8Array.from(data.subarray(0, nb)).buffer), b = new T(dec.buffer); let ok = true, rot = 0;
    for (let t = 0; t < a.length; t += 3) {
      const x = [a[t], a[t + 1], a[t + 2]], y = [b[t], b[t + 1], b[t + 2]];
      if (x[0] === y[0] && x[1] === y[1] && x[2] === y[2]) continue;
      if ((x[0] === y[1] && x[1] === y[2] && x[2] === y[0]) || (x[0] === y[2] && x[1] === y[0] && x[2] === y[1])) { rot++; continue; }
      ok = false; break;
    }
    if (ok) donmus++; else hata++;
  } else hata++;
  comp += enc.length; fallback.len = pad4(fallback.len);
  const fOff = fallback.len; fallback.len += data.length;
  yeniBV.push({_enc: Buffer.from(enc), buffer: 1, byteOffset: fOff, byteLength: data.length,
    extensions: {EXT_meshopt_compression: {buffer: 0, byteStride: r.stride, count: r.count, mode: r.mod}}});
}
// ana tamponu yeniden kur
const parcalar = []; let off = 0;
J.bufferViews = yeniBV.map(v => {
  const veri = v._enc || v._ham; const nv = {...v}; delete nv._enc; delete nv._ham;
  while (off % 4) { parcalar.push(Buffer.alloc(1)); off++; }
  if (v._enc) { nv.extensions.EXT_meshopt_compression.byteOffset = off; nv.extensions.EXT_meshopt_compression.byteLength = veri.length; }
  else { nv.buffer = 0; nv.byteOffset = off; nv.byteLength = veri.length; }
  parcalar.push(veri); off += veri.length; return nv;
});
while (off % 4) { parcalar.push(Buffer.alloc(1)); off++; }
J.buffers = [{byteLength: off}, {byteLength: pad4(fallback.len), extensions: {EXT_meshopt_compression: {fallback: true}}}];
J.extensionsUsed = [...new Set([...(J.extensionsUsed || []), 'EXT_meshopt_compression'])];
J.extensionsRequired = [...new Set([...(J.extensionsRequired || []), 'EXT_meshopt_compression'])];
let jb = Buffer.from(JSON.stringify(J), 'utf8'); jb = Buffer.concat([jb, Buffer.alloc((4 - jb.length % 4) % 4, 0x20)]);
const binb = Buffer.concat(parcalar);
const head = Buffer.alloc(20); head.writeUInt32LE(0x46546C67, 0); head.writeUInt32LE(2, 4); head.writeUInt32LE(12 + 8 + jb.length + 8 + binb.length, 8);
head.writeUInt32LE(jb.length, 12); head.writeUInt32LE(0x4E4F534A, 16);
const bh = Buffer.alloc(8); bh.writeUInt32LE(binb.length, 0); bh.writeUInt32LE(0x004E4942, 4);
fs.writeFileSync(go, Buffer.concat([head, jb, bh, binb]));
console.log(JSON.stringify({girdi: raw.length, cikti: 28 + jb.length + binb.length, idx: IDX, u16: U16, u16_prim: u16Acc.size,
  bayt_ayni_bv: dogru, ucgen_sirasi_ayni_donmus_bv: donmus, HATA_bv: hata, sikistirilmis_MB: +(comp / 1e6).toFixed(1), ham_indis_MB: +(ham / 1e6).toFixed(1)}));
