# -*- coding: utf-8 -*-
"""adım 6 · ana GLB'den (hat3_v8zq, SALT OKUNUR) istasyonların gövde-dışı parçalarını çeker.
Üçgen etiketi (mek / kpk) + istasyon zarfı (+pay) ile süzer; grup = (düğüm, mek, kpk).
Çıktı: ana_<IST>.pkl  [dict(ad, dugum, mat, mek, kpk, V (n×3 m), F)]"""
import json, struct, sys, pickle, os, re
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
GLB = sys.argv[1]
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
raw = open(GLB, 'rb').read(); jl = struct.unpack('<I', raw[12:16])[0]
J = json.loads(raw[20:20 + jl]); bo = 20 + jl; bl = struct.unpack('<I', raw[bo:bo + 4])[0]; BIN = raw[bo + 8:bo + 8 + bl]


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

# istasyon tanımı: mek kümesi · Gövde mek'inden KALAN düğümler · zarf (m) + pay
IST = {
    'A': dict(mek={1}, govde=set(), govde_kalan=(), zarf=((0.736, 0.0, -0.83), (1.449, 2.2, 0.079)), pay=0.15),
    'B': dict(mek={3, 4, 5, 6}, govde={2}, govde_kalan=('B_TASIYICI__', 'B_KASA__celik', 'B_MODULER__'),
              zarf=((0.736, 0.0, -0.83), (4.4, 0.788, 0.08)), pay=0.03),
    'E': dict(mek=set(range(32, 39)), govde={31}, govde_kalan=(), zarf=((4.4, 0.0, -0.83), (5.23, 2.2, 0.08)), pay=0.05),
    'U': dict(mek={40, 41, 50}, govde={39}, govde_kalan=('U_F_GOVDE__on_seffaf', 'U_ICECEK_YEDEK', 'U_KUTU_YEDEK'),
              zarf=((2.5, 0.788, -0.83), (5.23, 2.2, 0.08)), pay=0.03),
}
OUT = {k: {} for k in IST}
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
        ilgili = [s for s, d in IST.items() if um & (d['mek'] | d['govde'])]
        if not ilgili: continue
        X = acc(pr['attributes']['POSITION']).astype(np.float64)
        X = X @ M[:3, :3].T + M[:3, 3]
        P = X[T]; cen = P.mean(1)
        ok = (T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2]) & (T[:, 0] != T[:, 2])
        for s in ilgili:
            d = IST[s]
            sec = np.isin(mek, list(d['mek']))
            if d['govde'] and ad.startswith(tuple(d['govde_kalan'])):
                sec |= np.isin(mek, list(d['govde']))
            lo = np.array(d['zarf'][0]) - d['pay']; hi = np.array(d['zarf'][1]) + d['pay']
            sec &= ok & np.all((cen >= lo) & (cen <= hi), axis=1)
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
    print(s, len(lst), 'grup', sum(len(x['F']) for x in lst), 'üçgen')
    for x in sorted(lst, key=lambda x: -len(x['F']))[:8]: print('   ', x['dugum'], x['mek_kod'], x['kpk'], len(x['F']))
