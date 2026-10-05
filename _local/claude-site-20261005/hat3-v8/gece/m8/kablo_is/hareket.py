# -*- coding: utf-8 -*-
"""m8c adım 3: kablo ↔ hareketli parça (animasyonlu düğüm süpürmesi, kapak açılma süpürmesi, kaset / UNO çekme yolu, TOPPING araba zarfı, robot alanı). SALT OKUMA.
Girdi: _bulgu.pkl · Çıktı: _hareket.pkl"""
import sys, os, pickle, struct, json, re, math, collections
import numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); GECE = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, GECE)
import glbkit, m7_etiket
G = glbkit.Glb(os.path.join(os.path.dirname(GECE), "hat3_v8x.glb"))
R = pickle.load(open(os.path.join(HERE, '_bulgu.pkl'), 'rb'))
KAY = [d for d in R['KAY'] if d.get('tup')]
J = G.J
PK = m7_etiket.pk_yeni([os.path.join(GECE, "m7", f) for f in ("v8x_b_rapor.txt", "v8x_c_rapor.txt")])


def P2(v): return [round(float(x), 1) for x in v]


def acc(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]
    n = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}[a["type"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    r = np.frombuffer(bytes(G.BIN[off:off + a["count"] * n * 4]), np.float32).copy()
    return r.reshape(-1, n) if n > 1 else r


# ---------- kablo örnek noktaları
NOK = []   # (kablo_idx, nokta, r)
for k, d in enumerate(KAY):
    for q in d['S']:
        L = np.linalg.norm(q['b'] - q['a']); n = max(1, int(L / 8))
        for j in range(n + 1): NOK.append((k, q['a'] + (q['b'] - q['a']) * j / n, q['r']))
NP = np.array([p for _, p, _ in NOK]); NK = np.array([k for k, _, _ in NOK]); NR = np.array([r for _, _, r in NOK])
print('nokta', len(NP))
B = []


def bul(tur, d, konum, aciklama, oneri, agirlik=2, **ek):
    B.append(dict(tur=tur, dugum=d['prim'], parca=d['ad'] or d['id'], bilesen=d['id'], istasyon=d['ist'], konum_mm=P2(konum),
                  aciklama=aciklama, oneri=oneri, agirlik=agirlik, **ek))


def yuzey_ornek(X, T, ad=4.0):
    """üçgen yüzeyinden ~ad mm aralıkla nokta"""
    V0, V1, V2 = X[T[:, 0]], X[T[:, 1]], X[T[:, 2]]
    A = 0.5 * np.linalg.norm(np.cross(V1 - V0, V2 - V0), axis=1)
    n = np.maximum(1, np.ceil(A / (ad * ad)).astype(int)); n = np.minimum(n, 4000)
    idx = np.repeat(np.arange(len(T)), n)
    u = np.random.default_rng(1).random((len(idx), 2)); m = u.sum(1) > 1; u[m] = 1 - u[m]
    P = V0[idx] + u[:, :1] * (V1[idx] - V0[idx]) + u[:, 1:] * (V2[idx] - V0[idx])
    return np.vstack([P, V0, V1, V2])


# ---------- 5a · animasyonlu düğümler (öteleme)
YOL = collections.defaultdict(list)
for an in J.get("animations", []):
    for c in an["channels"]:
        if c["target"]["path"] != "translation": continue
        YOL[c["target"]["node"]].append(acc(an["samplers"][c["sampler"]]["output"]))
nd_ad = {i: n.get('name', '') for i, n in enumerate(J['nodes'])}
say = 0
for ni, outs in YOL.items():
    nd = J['nodes'][ni]; ad = nd_ad[ni]
    if ad.startswith(('URUN', 'E_KUTU', 'E_PIZZA')): continue
    t0 = np.array(nd.get('translation', [0, 0, 0]), float)
    D = np.vstack(outs) - t0
    D = np.unique(np.round(D * 1000.0, 1), axis=0)                     # mm ötelemeler
    if np.abs(D).max() < 1.0: continue
    pr = [p for p in G.prims if p['nd'] is nd]
    if not pr: continue
    Xs = [];
    for p in pr:
        v = G.gorunur(p)
        if v.any(): Xs.append(yuzey_ornek(p['X'], p['T'][v]))
    if not Xs: continue
    S = np.vstack(Xs); lo, hi = S.min(0), S.max(0)
    slo, shi = lo + D.min(0) - 15, hi + D.max(0) + 15
    m = np.all((NP >= slo) & (NP <= shi), axis=1)
    if not m.any(): continue
    tr = cKDTree(S)
    # yol üzerinde ara örnekler (ardışık anahtar kareler arası 5 mm)
    Dp = [D[0]]
    for a in D[1:]:
        n = max(1, int(np.linalg.norm(a - Dp[-1]) / 5.0))
        for j in range(1, n + 1): Dp.append(Dp[-1] + (a - Dp[-1]) * j / n)
    Dp = np.unique(np.round(np.array(Dp), 1), axis=0)
    ii = np.where(m)[0]
    vur = {}
    for dlt in Dp:
        dd, _ = tr.query(NP[ii] - dlt)
        h = dd < NR[ii] + 1.5
        for j in ii[h]:
            k = NK[j]
            if k not in vur or np.linalg.norm(dlt) > np.linalg.norm(vur[k][1]): vur[k] = (NP[j], dlt)
    for k, (p, dlt) in vur.items():
        d = KAY[k]; say += 1
        bul('hareket/animasyon', d, p, "%s hareket ederken (öteleme %s mm) kabloya değiyor / r+1,5 mm'den yakın geçiyor" % (ad, P2(dlt)),
            "kabloyu süpürme kutusunun dışına al (süpürme x %.0f–%.0f · y %.0f–%.0f · z %.0f–%.0f) ya da hareketli parçaya enerji zinciri / spiral ile bağla" % (slo[0] + 15, shi[0] - 15, slo[1] + 15, shi[1] - 15, slo[2] + 15, shi[2] - 15), 3,
            hareketli=ad)
print('animasyon temasi', say)

# ---------- 5b · kapaklar (kpk) · açılma süpürmesi (menteşe bilinmiyor: kapak düzleminden dışa W kadar kutu) + kapanma düzlemi
KAPAK = []
for p in G.prims:
    kp = G.kpk_maske(p) & G.gorunur(p)
    if not kp.any(): continue
    tl, kut = G.komp(p)
    for c in np.unique(tl[kp]):
        lo, hi, n = kut[int(c)]
        e = hi - lo
        if e.max() < 120: continue                                       # mandal / kilit / menteşe parçası
        KAPAK.append((p['name'], int(c), lo, hi))
BIRIM = {}
_acc = collections.defaultdict(list)
for p in G.prims:
    v = G.gorunur(p)
    if v.any(): _acc[p['name'].split('__')[0]].append(p['X'][np.unique(p['T'][v])])
BEXT = {}
for b_, L_ in _acc.items():
    A_ = np.vstack(L_); BIRIM[b_] = (A_.min(0) + A_.max(0)) / 2; BEXT[b_] = A_.max(0) - A_.min(0)
# aynı düzlemdeki kapak parçalarını birleştir (kanat başına bir kutu)
print('kapak parcasi', len(KAPAK))
say = 0
for nm, c, lo, hi in KAPAK:
    e = hi - lo; ta = int(np.argmin(e)); W = min(e[k] for k in range(3) if k != ta)
    if e[ta] > 25: continue
    ub = nm.split('__')[0]; bb = BIRIM.get(ub)
    if bb is not None and BEXT[ub][ta] < 60:
        al = [b_ for b_ in BIRIM if b_.split('_')[0] == ub.split('_')[0] and BEXT[b_][ta] >= 60]
        bb = BIRIM[max(al, key=lambda b_: BEXT[b_].prod())] if al else None
    yon = [1 if ((lo[ta] + hi[ta]) / 2) >= bb[ta] else -1] if bb is not None else [-1, +1]
    for sg in yon:
        blo, bhi = lo.copy(), hi.copy()
        if sg > 0: blo[ta] = hi[ta]; bhi[ta] = hi[ta] + W
        else: bhi[ta] = lo[ta]; blo[ta] = lo[ta] - W
        m = np.all((NP >= blo - NR[:, None]) & (NP <= bhi + NR[:, None]), axis=1)
        for k in np.unique(NK[m]):
            d = KAY[k]; j = np.where(m & (NK == k))[0][0]
            bul('hareket/kapak', d, NP[j], "kapak %s#%d açılma süpürmesinin içinde (kapak %s–%s, açılma yönü %s%s, kanat %.0f mm · menteşe yeri modelde yok: kanat = kısa kenar)" % (nm, c, P2(lo), P2(hi), '+' if sg > 0 else '-', 'xyz'[ta], W),
                "kabloyu kapak kanadının süpürme hacminden çıkar (kapak düzleminin iç tarafına, ≥ 20 mm geri) ya da menteşe tarafına al", 2, hareketli=nm)
            say += 1
print('kapak', say)

# ---------- 5c · kaset / UNO çekme yolu (TOPPING, +z)
say = 0
grup = collections.defaultdict(list)
for q in PK.get('TOPPING_MODUL', []):
    ad = q[0]; k = np.array(q[2:8], float)
    if not k.any(): continue
    m_ = re.match(r'^(kasar_cad|sucuk_cad|kovan_kasar|kovan_sucuk)', ad)
    if m_: grup['kaset_' + ('kasar' if 'kasar' in ad else 'sucuk')].append(k)
    m2 = re.match(r'^(kiyma|kusbasi|harc|sos)_(hazne_bizim|hazne_boynu|tc_kelepce_hazne)', ad)
    if m2: grup['UNO_' + m2.group(1)].append(k)
for g, ks in grup.items():
    ks = np.array(ks); lo = np.array([ks[:, 0].min(), ks[:, 2].min(), ks[:, 4].min()]); hi = np.array([ks[:, 1].max(), ks[:, 3].max(), ks[:, 5].max()])
    L = 300.0 if g.startswith('kaset') else max(0.0, 79.0 - hi[2]) + 50.0
    blo = np.array([lo[0], lo[1], hi[2]]); bhi = np.array([hi[0], hi[1], hi[2] + L])
    m = np.all((NP >= blo - NR[:, None]) & (NP <= bhi + NR[:, None]), axis=1)
    for k in np.unique(NK[m]):
        d = KAY[k]; j = np.where(m & (NK == k))[0][0]
        bul('hareket/kaset_cekme', d, NP[j], "%s önden çekme yolunda (x %.0f–%.0f · y %.0f–%.0f · z %.0f→%.0f)" % (g, blo[0], bhi[0], blo[1], bhi[1], blo[2], bhi[2]),
            "kabloyu kaset / hazne izdüşümünün dışına (x veya y'de ≥ 15 mm) ya da kasetin arkasına al", 3, hareketli=g)
        say += 1
    print(g, P2(blo), P2(bhi))
print('kaset', say)

# ---------- 5d · TOPPING araba / tabla zarfı (h3_elk_ist_v1) + robot alanı
ZARF = {"TOPPING araba + tabla zarfı": (890.0, 2520.0, 931.0, 1045.0, -345.0, -3.0), "TOPPING kızak zarfı": (890.0, 2520.0, 912.0, 931.0, -345.0, -35.0),
        "TOPPING dönüş motoru zarfı": (1050.0, 2400.0, 898.0, 942.0, -200.0, -140.0),
        "robot çalışma alanı (FR5 ray x 936–5100, koridor z 79–670, y ≤ 1700)": (736.0, 5300.0, 0.0, 1700.0, 79.5, 669.0)}
say = 0
for ad, z in ZARF.items():
    lo = np.array(z[0::2]); hi = np.array(z[1::2])
    m = np.all((NP > lo) & (NP < hi), axis=1)
    for k in np.unique(NK[m]):
        d = KAY[k]
        if d['base'].startswith('ROBOT') and ad.startswith('robot'): continue
        jj = np.where(m & (NK == k))[0]
        # kanal / oluk içindekiler hariç
        icerde = [any((NP[j] >= np.array(lo_) - 1).all() and (NP[j] <= np.array(hi_) + 1).all() for _, lo_, hi_ in R['KANAL']) for j in jj]
        jj = [j for j, ic in zip(jj, icerde) if not ic]
        if not jj: continue
        L = len(jj) * 8
        bul('hareket/zarf', d, NP[jj[0]], "%s içinde ~%d mm kablo (kanal dışı) · ilk nokta %s" % (ad, L, P2(NP[jj[0]])),
            "kabloyu zarfın dışına al (zarf x %.0f–%.0f · y %.0f–%.0f · z %.0f–%.0f) ya da kapaklı kanala / zincir oluğuna al" % tuple(z), 3 if 'robot' not in ad else 2, hareketli=ad)
        say += 1
print('zarf', say)
pickle.dump(B, open(os.path.join(HERE, '_hareket.pkl'), 'wb'))
print(collections.Counter(b['tur'] for b in B))
