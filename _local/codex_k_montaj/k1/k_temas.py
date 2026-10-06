# -*- coding: utf-8 -*-
"""K bağlantı işi (Claude, 6 Eki 2026) · 1. adım: her açık parçanın oturduğu yüzey ve aralık.
Girdi: plan_k_clip_full.pkl (Codex devri, parça üçgenleri dünya mm) + baglanti_claude.json (bağlantı denetimi: ACIK listesi)
Çıktı: k_temas.json — parça → [(komşu, en yakın uzaklık mm, temas noktası sayısı, temas normali)] (en çok temas eden ilk)"""
import json, pickle, sys
import numpy as np
import trimesh
D = pickle.load(open('plan_k_clip_full.pkl', 'rb')); P = D['P']
B = json.load(open('baglanti_claude.json'))
ACIK = sorted(a for a, v in B.items() if v['sinif'] == 'BAGLANTISIZ' and v.get('kategori') == 'ACIK')
ADAY = [a for a in P if P[a]['tur'] not in ('kaynak', 'kablo', 'silikon') and not a.startswith('cevre')]
LO = {a: P[a]['V'].min(0) for a in P}; HI = {a: P[a]['V'].max(0) for a in P}
TM = {}
def tm(a):
    if a not in TM: TM[a] = trimesh.Trimesh(P[a]['V'], P[a]['F'], process=False)
    return TM[a]
OUT = {}
for i, a in enumerate(ACIK):
    S, fi = trimesh.sample.sample_surface_even(tm(a), 3000, seed=1) if len(P[a]['F']) else (np.zeros((0, 3)), None)
    S = np.vstack([S, P[a]['V']])
    L = []
    for b in ADAY:
        if b == a or np.any(LO[b] > HI[a] + 3) or np.any(HI[b] < LO[a] - 3): continue
        cp, d, tri = trimesh.proximity.closest_point(tm(b), S)
        m = d < 0.3
        n = tm(b).face_normals[tri[m]].mean(0) if m.any() else np.zeros(3)
        L.append((b, round(float(d.min()), 3), int(m.sum()), [round(float(x), 3) for x in n]))
    L.sort(key=lambda x: (-x[2], x[1]))
    OUT[a] = L[:6]
    if i % 20 == 0: print(i, len(ACIK), flush=True)
json.dump(OUT, open('k_temas.json', 'w'), ensure_ascii=False, indent=0)
for a in ACIK:
    L = OUT[a]
    print('%-40s %s' % (a, ' | '.join('%s %.2f %d' % (b[:26], d, n) for b, d, n, _ in L[:3])))
