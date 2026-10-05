# -*- coding: utf-8 -*-
"""hareketli düğümlerin süpürme kutuları (animasyon öteleme aralığı) ∩ yeni elektrik parçaları · A içi boş mu"""
import json, struct, numpy as np, re, sys
S=r"C:SERSKEMALAPPDATAocaltempaudec--users-kemal-desktop-kemal-webs-te3ef876a-f062-4b29-bb81-775cc8a1a6d8scratchpad"
G = sys.argv[1]; d = sys.argv[2]
raw = open(G, 'rb').read(); jl = struct.unpack('<I', raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); BIN = raw[28 + jl:]
def acc(i):
    a = J['accessors'][i]; v = J['bufferViews'][a['bufferView']]; n = {'SCALAR': 1, 'VEC3': 3, 'VEC4': 4}[a['type']]
    off = v.get('byteOffset', 0) + a.get('byteOffset', 0); return np.frombuffer(BIN[off:off + a['count'] * n * 4], np.float32).reshape(-1, n)
rng = {}
for an in J['animations']:
    for c in an['channels']:
        if c['target']['path'] != 'translation': continue
        nd = c['target']['node']; o = acc(an['samplers'][c['sampler']]['output']) * 1000; t0 = np.array(J['nodes'][nd].get('translation', [0, 0, 0])) * 1000
        dd = o - t0; lo, hi = dd.min(0), dd.max(0)
        if nd in rng: lo = np.minimum(lo, rng[nd][0]); hi = np.maximum(hi, rng[nd][1])
        rng[nd] = (lo, hi)
D = np.load(d + r"\m8_onbellek.npz"); PJ = json.load(open(d + r"\m8_parca.json", encoding="utf-8"))
ad = np.array([p["ad"] for p in PJ["parca"]]); A, B, C, P = D["A"], D["B"], D["C"], D["P"]
lo = np.minimum(np.minimum(A, B), C); hi = np.maximum(np.maximum(A, B), C); nm = ad[P]
yeni = np.array([bool(re.match(r"ELK_IC|TOPPING_MODUL__yayici|ELK_ANA_PANO_UF__salter", s)) for s in nm])
NL, NH = lo[yeni], hi[yeni]
sor = 0
for nd, (dl, dh) in rng.items():
    name = J['nodes'][nd]['name']; m = nm == name
    if not m.any(): continue
    a = lo[m].min(0) + np.minimum(dl, 0); b = hi[m].max(0) + np.maximum(dh, 0)
    hit = np.all(NH > a + 0.3, 1) & np.all(NL < b - 0.3, 1)
    if hit.any():
        sor += 1; print("SÜPÜRME ∩ YENİ:", name, np.round(a).tolist(), np.round(b).tolist(), int(hit.sum()))
print("hareketli düğüm", len(rng), "· süpürme kutusu yeni parçaya değen:", sor)
Ab = (np.array([736.5, 788.5, -829.0]), np.array([1435.5, 2199.5, 58.0]))
iA = yeni & np.all(hi > Ab[0], 1) & np.all(lo < Ab[1], 1)
print("A içinde yeni parça üçgeni:", int(iA.sum()))
