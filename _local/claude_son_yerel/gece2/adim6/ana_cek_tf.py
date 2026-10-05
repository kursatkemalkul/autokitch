# -*- coding: utf-8 -*-
"""adım 6 (devam) · TOPPING + F: ana GLB'den (hat3_v8zq, SALT OKUNUR) gövde-dışı parçalar.
ana_cek.py ile aynı (mek / kpk etiketi + zarf) + üretim sacının YERİNE GEÇTİĞİ v8zq bileşenleri çıkarılır
(adim5 denetimindeki DEGISEN: düğüm + bileşen no · bil_hepsi.pkl; F'de ayrıca U sacının yerine geçtiği F_UST_KABIN parçaları).
Çıktı: ana_TOPPING.pkl, ana_F.pkl"""
import json, struct, sys, pickle, os
import numpy as np
from scipy.spatial import cKDTree
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
GLB = sys.argv[1]
BIL = os.path.join(os.path.dirname(HERE), 'adim5', '_is', 'bil_hepsi.pkl')
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
raw = open(GLB, 'rb').read(); jl = struct.unpack('<I', raw[12:16])[0]
J = json.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack('<I', raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]

# ---- yerine geçen bileşenler (h3_topping_sac_v1.DEGISEN · h3_f_sac_v1.DEGISEN · h3_u_sac_v1 F_UST_KABIN)
DEG = {'TOPPING': {"TOPPING_MODUL__sac": sorted(set([30, 17, 20, 19, 18, 21, 22, 23, 24, 25, 26, 27, 28, 98, 99] + list(range(31, 82)))),
                   "TOPPING_MODUL__paslanmaz": list(range(105, 156)), "TOPPING_MODUL__pu": [0, 1, 2, 3, 4, 5, 6, 7, 10, 11], "KAIDE_C__paslanmaz": "hepsi"},
       'F': {"F_UST_KAPAK__on_seffaf__KAPAK_F_SOL": [0, 1, 2, 3, 5, 8], "F_UST_KAPAK__on_seffaf__KAPAK_F_SAG": [0, 1, 2, 3, 5, 8], "F_DAVLUMBAZ__sac": [1],
             "U_F_BACA__sac": "hepsi", "U_F_BACA__yalitim_gorunur": "hepsi", "U_F_BACA__paslanmaz": "hepsi",
             "F_UST_KABIN__sac": "hepsi", "F_UST_KABIN__yalitim": "hepsi"}}
KISMI = {'F': {"F_DAVLUMBAZ__sac": [((2501, 1347, -442), (3999, 1861, -439.9))],
               "F_UST_KABIN__paslanmaz": [((2501, 1316, -829), (3999, 1347, 58)), ((3325, 1347, -828), (3357, 1861, 58)), ((2502, 1830, 26), (3998, 1861, 58))]}}
t_ = __import__('time').time()
TUM = pickle.load(open(BIL, 'rb'))
print('bil_hepsi', len(TUM), round(__import__('time').time() - t_, 1), 's')
AGAC, SIL_SAY = {}, {}
for s in DEG:
    C = []
    for b in TUM:
        d = DEG[s].get(b['ad']); sil = d == 'hepsi' or (d is not None and b['no'] in d)
        for lo, hi in KISMI.get(s, {}).get(b['ad'], []):
            if np.all(b['lo'] >= np.array(lo) - 0.5) and np.all(b['hi'] <= np.array(hi) + 0.5): sil = True
        if sil:
            C.append(b['P'].mean(1)); SIL_SAY[(s, b['ad'])] = SIL_SAY.get((s, b['ad']), 0) + 1
    AGAC[s] = cKDTree(np.vstack(C))
    print(s, 'silinecek bileşen', {k[1]: v for k, v in SIL_SAY.items() if k[0] == s})
del TUM


def acc(i):
    a = J['accessors'][i]; v = J['bufferViews'][a['bufferView']]
    n = {'SCALAR': 1, 'VEC3': 3, 'VEC2': 2, 'VEC4': 4}[a['type']]; dt = TD[a['componentType']]
    off = v.get('byteOffset', 0) + a.get('byteOffset', 0)
    r = np.frombuffer(BIN[off:off + a['count'] * n * np.dtype(dt).itemsize], dt)
    return r.reshape(-1, n) if n > 1 else r


def trs(nd):
    M = np.eye(4)
    if 'matrix' in nd: return np.array(nd['matrix']).reshape(4, 4).T
    t = nd.get('translation', [0, 0, 0]); q = nd.get('rotation', [0, 0, 0, 1]); s = nd.get('scale', [1, 1, 1])
    x, y, z, w = q
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    M[:3, :3] = R * np.array(s)[None, :]; M[:3, 3] = t; return M


W = {}
def gez(i, P):
    M = P @ trs(J['nodes'][i]); W[i] = M
    for c in J['nodes'][i].get('children', []): gez(c, M)
for r in J['scenes'][0]['nodes']: gez(r, np.eye(4))

IST = {
    'TOPPING': dict(mek=set(range(7, 18)), zarf=((0.70, 0.70, -0.86), (2.56, 2.30, 0.11))),
    'F': dict(mek=set(range(18, 24)), zarf=((2.44, 0.70, -0.86), (4.06, 2.40, 0.11))),
}
OUT = {k: {} for k in IST}
SILINEN = {k: 0 for k in IST}
for ni, nd in enumerate(J['nodes']):
    if 'mesh' not in nd or ni not in W: continue
    M = W[ni]; sc = abs(np.linalg.det(M[:3, :3])) ** (1 / 3)
    if sc < 0.01: continue
    ad = nd['name']
    for pi, pr in enumerate(J['meshes'][nd['mesh']]['primitives']):
        ex = pr.get('extras', {})
        T = acc(pr['indices']).reshape(-1, 3).astype(np.int64); n = len(T)
        mek = np.full(n, -1, int); kpk = np.zeros(n, bool)
        L = ex.get('mek') or []
        for k in range(0, len(L) - 2, 3): mek[L[k + 1] // 3:(L[k + 1] + L[k + 2]) // 3] = L[k]
        L = ex.get('kpk') or []
        for k in range(0, len(L) - 1, 2): kpk[L[k] // 3:(L[k] + L[k + 1]) // 3] = True
        um = set(np.unique(mek).tolist())
        ilgili = [s for s, d in IST.items() if um & d['mek']]
        if not ilgili: continue
        X = acc(pr['attributes']['POSITION']).astype(np.float64)
        X = X @ M[:3, :3].T + M[:3, 3]
        P = X[T]; cen = P.mean(1)
        ok = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2]) & (T[:, 0] != T[:, 2])
        for s in ilgili:
            d = IST[s]
            sec = np.isin(mek, list(d['mek']))
            lo = np.array(d['zarf'][0]); hi = np.array(d['zarf'][1])
            sec &= ok & np.all((cen >= lo) & (cen <= hi), axis=1)
            if not sec.any(): continue
            if ad in DEG[s] or ad in KISMI.get(s, {}):
                dd, _ = AGAC[s].query(cen[sec] * 1000.0, distance_upper_bound=0.05)
                sil = np.zeros(n, bool); sil[np.where(sec)[0][np.isfinite(dd)]] = True
                SILINEN[s] += int(sil.sum()); sec &= ~sil
                if not sec.any(): continue
            for m_ in np.unique(mek[sec]):
                for kp in (False, True):
                    q = sec & (mek == m_) & (kpk == kp)
                    if not q.any(): continue
                    key = (ad, int(m_), kp)
                    Tq = T[q]
                    u, inv = np.unique(Tq.reshape(-1), return_inverse=True)
                    g = OUT[s].setdefault(key, dict(V=[], F=[], base=0))
                    g['V'].append(X[u].astype(np.float32)); g['F'].append(inv.reshape(-1, 3) + g['base']); g['base'] += len(u)
MEK = J['scenes'][0]['extras']['mekanizmalar']
for s, gs in OUT.items():
    lst = []
    for (ad, m_, kp), g in gs.items():
        V = np.vstack(g['V']); F = np.vstack(g['F']).astype(np.uint32)
        mat = ad.split('__')[1] if '__' in ad else ad
        lst.append(dict(dugum=ad, mek=m_, mek_kod=MEK[m_]['kod'] if m_ >= 0 else '', kpk=kp, mat=mat, V=V, F=F))
    pickle.dump(lst, open(os.path.join(HERE, 'ana_%s.pkl' % s), 'wb'))
    print(s, len(lst), 'grup', sum(len(x['F']) for x in lst), 'üçgen · yerine geçen (silinen) üçgen', SILINEN[s])
    for x in sorted(lst, key=lambda x: (x['mek'], x['dugum'])):
        lo = x['V'].min(0); hi = x['V'].max(0)
        print('   %-48s %-22s %s %6d  x %.3f–%.3f y %.3f–%.3f z %.3f–%.3f' % (x['dugum'], x['mek_kod'], 'K' if x['kpk'] else ' ', len(x['F']), lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
