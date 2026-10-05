# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 48 · A (AÇICI) BAĞLANTI AÇIKLARI (4 Eki 2026 · Claude · yerel) — A montaj animasyonu v3 ajanının betiği (gece2/a3/zincir_A_tamamla.py)
zincire alındı + A5 eklendi. Kullanım: python 48_a_tamamla.py hat3_v9o.glb hat3_v9p.glb
  A5 · A → TOPPING 4 × ISO 4762 M8 × 16 (yatay, TOPPING sol dış sacındaki PEM SP-M8): uç PEM'i 6,1–6,9 mm geçip köpük kapağı cebine giriyordu
       → M8 × 10 (gövde başa doğru 6 mm kısaltılır; PEM dişi tam kavranır, uç PEM'in ≤ 0,9 mm ötesinde).
Düğüm adı tabanlı: 'A_GOVDE__paslanmaz' ve 'TOPPING_MODUL__sac' (açıcı kolonu, mek A/Açıcı) düğümlerinin tek primitifine dokunur.
Parçalar konum-birleşik bileşen (0,001 mm) + eksen / kutu ile seçilir. Mevcut üçgen sırası korunur (ent indisleri değişmez); yeni üçgenler
primitifin SONUNA eklenir, mek / kat aralığı (komşu üçgenin değeriyle) eklenir. Beklenen sayıda bileşen bulunamazsa DURUR (çıktı yazmaz).

Bulunan açıklar (A montaj animasyonu v3 planı sırasında, hat3_v9l üzerinde ölçüldü):
  A1 · A → B 6 × ISO 4762 M8 × 25: başın altındaki DIN 9021 pul (Ø24) kaide borusunun üst duvarındaki / plakadaki / damlama sacındaki
       Ø16 servis deliğinden GEÇEMEZ (boru kapalı, kaynaklı). → ISO 7092 M8 küçük seri pul (8,4 / 15 × 1,6); cıvata 0,4 aşağı
       (adım 47 sonrası M8 × 16: uç y 775,6, kapalı uçlu perçin somunun iç diş dibinin 7 mm üstünde).
  A2 · Açıcı kolonu 4 × ISO 4762 M8 × 20: baş, kolon flanşının üstünden 1,5 mm havada (flanş üstü 902,0 · baş altı 903,5); arayüz metni
       "ISO 4762 M8 + DIN 125" diyor, pul modelde yok. → DIN 125-1 M8 pul (8,4 / 16 × 1,6) eklenir (902,0–903,6), cıvata 0,1 yukarı.
  A3 · Tabla rayı 4 × ISO 4762 M6 × 16: baş, ray taban sacının üstünden 5,0 mm havada (ray üstü 896,5 · baş altı 901,5) → cıvata 5,0 aşağı.
  A4 · Açıcı kolonunun modeldeki taban flanşı 120 × 50 (z −660…−610); A gövdesi açıcıyı 4 köşe Ø9 (90 × 125 eksen, z −645 / −520) bekliyor
       (satın alma şartı: h3_a_sac_v1 ACICI_M8). Öndeki 2 cıvata (z −520) flanşa değil boşluğa basıyordu. → temsili ürün flanşı şartnameye
       göre 120 × 155'e uzatılır (z −610…−505, kalınlık aynı 893,55–902,0, 2 × Ø9). Gerçek üründe flanş ya da 8,5 mm adaptör plakası doğrulanır."""
import json, struct, sys
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

X_A = 736.0
AB_M8 = [(25.0, -706.0), (25.0, -110.0), (350.0, -706.0), (350.0, -110.0), (675.0, -706.0), (675.0, -110.0)]
ACICI_M8 = [(305.0, -645.0), (395.0, -645.0), (305.0, -520.0), (395.0, -520.0)]
RAY_M6 = [(144.0, -320.0), (144.0, -20.0), (564.0, -320.0), (564.0, -20.0)]
TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}


def trs(nd):
    M = np.eye(4)
    if 'matrix' in nd: return np.array(nd['matrix']).reshape(4, 4).T
    t = nd.get('translation', [0, 0, 0]); q = nd.get('rotation', [0, 0, 0, 1]); s = nd.get('scale', [1, 1, 1])
    x, y, z, w = q
    R = np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                  [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                  [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])
    M[:3, :3] = R * np.array(s)[None, :]; M[:3, 3] = t; return M


class GLB:
    def __init__(s, gi):
        raw = open(gi, 'rb').read()
        jl = struct.unpack('<I', raw[12:16])[0]
        s.J = json.loads(raw[20:20 + jl]); bo = 20 + jl
        bl = struct.unpack('<I', raw[bo:bo + 4])[0]
        s.BIN = bytearray(raw[bo + 8:bo + 8 + bl])
        assert not s.J.get('extensionsUsed'), 'sıkıştırılmış GLB desteklenmez: %s' % s.J.get('extensionsUsed')
        s.W = {}
        for r in s.J['scenes'][0]['nodes']: s._gez(r, np.eye(4))

    def _gez(s, i, P):
        M = P @ trs(s.J['nodes'][i]); s.W[i] = M
        for c in s.J['nodes'][i].get('children', []): s._gez(c, M)

    def oku(s, i):
        a = s.J['accessors'][i]; v = s.J['bufferViews'][a['bufferView']]
        n = {'SCALAR': 1, 'VEC3': 3}[a['type']]; dt = TD[a['componentType']]
        off = v.get('byteOffset', 0) + a.get('byteOffset', 0)
        arr = np.frombuffer(bytes(s.BIN[off:off + a['count'] * n * np.dtype(dt).itemsize]), dt).copy()
        return arr.reshape(-1, n) if n > 1 else arr

    def ekle(s, arr, typ, ct, target, minmax=False):
        arr = np.ascontiguousarray(arr)
        while len(s.BIN) % 4: s.BIN.append(0)
        off = len(s.BIN); s.BIN.extend(arr.tobytes())
        s.J['bufferViews'].append({'buffer': 0, 'byteOffset': off, 'byteLength': arr.nbytes, 'target': target})
        a = {'bufferView': len(s.J['bufferViews']) - 1, 'componentType': ct, 'count': int(arr.shape[0]), 'type': typ}
        if minmax: a['min'] = arr.min(0).tolist(); a['max'] = arr.max(0).tolist()
        s.J['accessors'].append(a); return len(s.J['accessors']) - 1

    def dugum(s, ad):
        ni = [i for i, n in enumerate(s.J['nodes']) if n.get('name') == ad]
        assert len(ni) == 1, (ad, ni)
        return Dugum(s, ni[0])

    def yaz(s, go):
        while len(s.BIN) % 4: s.BIN.append(0)
        s.J['buffers'][0]['byteLength'] = len(s.BIN)
        js = json.dumps(s.J, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        while len(js) % 4: js += b' '
        out = struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(s.BIN)) + struct.pack('<II', len(js), 0x4E4F534A) + js + struct.pack('<II', len(s.BIN), 0x004E4942) + bytes(s.BIN)
        open(go, 'wb').write(out); return len(out)


class Dugum:
    """tek primitifli düğüm: dünya mm köşeleri (Xw), konum-birleşik bileşenler, köşe taşıma, üçgen ekleme"""
    def __init__(s, g, ni):
        s.g = g; s.M = g.W[ni]; s.Mi = np.linalg.inv(s.M)
        pr = g.J['meshes'][g.J['nodes'][ni]['mesh']]['primitives']
        assert len(pr) == 1; s.pr = pr[0]
        s.X = g.oku(s.pr['attributes']['POSITION']); s.N = g.oku(s.pr['attributes']['NORMAL']); s.I = g.oku(s.pr['indices'])
        s.Xw = (s.X.astype(float) @ s.M[:3, :3].T + s.M[:3, 3]) * 1000.0; s.Xw0 = s.Xw.copy()
        s.T = s.I.reshape(-1, 3).astype(np.int64)
        uq, inv = np.unique(np.round(s.Xw, 3), axis=0, return_inverse=True); inv = inv.reshape(-1); Tu = inv[s.T]
        r = np.concatenate([Tu[:, 0], Tu[:, 1]]); c = np.concatenate([Tu[:, 1], Tu[:, 2]])
        n, cl = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(len(uq), len(uq))), directed=False)
        s.cl = cl[inv]; kul = np.zeros(len(s.X), bool); kul[s.T.reshape(-1)] = True
        s.lo = np.full((n, 3), 1e9); s.hi = np.full((n, 3), -1e9)
        np.minimum.at(s.lo, s.cl[kul], s.Xw[kul]); np.maximum.at(s.hi, s.cl[kul], s.Xw[kul])
        s.yeniV, s.yeniN, s.yeniF = [], [], []

    def bul(s, x, z, ylo, yhi, rmax, ad):
        lo, hi = s.lo, s.hi
        m = (np.abs((lo[:, 0] + hi[:, 0]) / 2 - x) < 0.3) & (np.abs((lo[:, 2] + hi[:, 2]) / 2 - z) < 0.3) & \
            (lo[:, 1] > ylo - 0.05) & (hi[:, 1] < yhi + 0.05) & (hi[:, 1] - lo[:, 1] > (yhi - ylo) - 0.5) & (np.abs((hi[:, 0] - lo[:, 0]) / 2 - rmax) < 0.35)
        k = np.where(m)[0]
        assert len(k) == 1, (ad, x, z, len(k))
        return np.where(s.cl == k[0])[0]

    def ucgen_ekle(s, V, Nn, F):
        s.yeniV.append(V); s.yeniN.append(Nn); s.yeniF.append(F)

    def kapat(s, ornek_nokta=None):
        g = s.g; nv = len(s.X)
        Xl = ((s.Xw / 1000.0 - s.M[:3, 3]) @ s.Mi[:3, :3].T).astype(np.float32)
        ayni = np.all(s.Xw == s.Xw0, 1); Xl[ayni] = s.X[ayni]          # dokunulmayan köşeler bayt aynı
        n_eski = len(s.I)
        if s.yeniV:
            Vn = np.vstack(s.yeniV); Nn_ = np.vstack(s.yeniN); Fn = []; k = 0
            for V, F in zip(s.yeniV, s.yeniF): Fn.append(F + nv + k); k += len(V)
            Fn = np.vstack(Fn)
            Vl = ((Vn / 1000.0 - s.M[:3, 3]) @ s.Mi[:3, :3].T).astype(np.float32)
            Nl = Nn_ @ np.linalg.inv(s.M[:3, :3]); Nl = (Nl / np.linalg.norm(Nl, axis=1, keepdims=True)).astype(np.float32)
            XX = np.vstack([Xl, Vl]); NN = np.vstack([s.N.astype(np.float32), Nl]); II = np.concatenate([s.I.astype(np.uint32), Fn.reshape(-1).astype(np.uint32)])
        else:
            XX, NN, II = Xl, s.N.astype(np.float32), s.I.astype(np.uint32)
        s.pr['attributes']['POSITION'] = g.ekle(XX, 'VEC3', 5126, 34962, True)
        s.pr['attributes']['NORMAL'] = g.ekle(NN, 'VEC3', 5126, 34962)
        s.pr['indices'] = g.ekle(II, 'SCALAR', 5125, 34963)
        n_yeni = len(II)
        if n_yeni > n_eski:
            ex = s.pr.setdefault('extras', {})
            ti = None
            if ornek_nokta is not None:
                C = s.Xw0[s.T].mean(1); ti = int(np.argmin(np.linalg.norm(C - np.asarray(ornek_nokta), axis=1))) * 3
            for key in ('mek', 'kat'):
                L = ex.get(key) or []
                if not L: continue
                val = L[-3]
                if ti is not None:
                    for k in range(0, len(L) - 2, 3):
                        if L[k + 1] <= ti < L[k + 1] + L[k + 2]: val = L[k]
                if L[-3] == val and L[-2] + L[-1] == n_eski: L[-1] += n_yeni - n_eski
                else: L += [val, n_eski, n_yeni - n_eski]
                ex[key] = L
        return (n_yeni - n_eski) // 3


def duz_kati(V, F):
    """keskin kenarlı ağ: üçgen başına ayrı köşe + yüz normali"""
    P = V[F]; n = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True)
    return P.reshape(-1, 3), np.repeat(n, 3, axis=0), np.arange(len(F) * 3).reshape(-1, 3)


def _y_ekseni(x, y0, z):
    return [[1, 0, 0, x], [0, 0, 1, y0], [0, -1, 0, z]]                      # yerel z (silindir ekseni) → dünya +y


def halka(x, z, y0, y1, ri, ro, n=32):
    import manifold3d as mf
    m = mf.Manifold.cylinder(y1 - y0, ro, ro, n) - mf.Manifold.cylinder(y1 - y0 + 2, ri, ri, n).translate([0, 0, -1])
    me = m.transform(_y_ekseni(x, y0, z)).to_mesh()
    return duz_kati(np.asarray(me.vert_properties, float)[:, :3], np.asarray(me.tri_verts, np.int64))


def flans_uzanti():
    import manifold3d as mf
    x0, x1, y0, y1, z0, z1 = 1026.0, 1146.0, 893.55, 902.0, -610.0, -505.0
    m = mf.Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])
    for x, z in ((1041.0, -520.0), (1131.0, -520.0)):
        m = m - mf.Manifold.cylinder(y1 - y0 + 2, 4.5, 4.5, 32).transform(_y_ekseni(x, y0 - 1, z))
    me = m.to_mesh(); return duz_kati(np.asarray(me.vert_properties, float)[:, :3], np.asarray(me.tri_verts, np.int64))


def main(gi, go):
    g = GLB(gi); rapor = []
    A = g.dugum('A_GOVDE__paslanmaz')
    for x, z in AB_M8:                                                     # A1
        xw = x + X_A
        vp = A.bul(xw, z, 789.9, 792.1, 12.0, 'AB pul'); vv = A.bul(xw, z, 775.9, 800.1, 6.5, 'AB cıvata')          # adım 47: M8 × 25 → × 16 (uç 776)
        P = A.Xw[vp]; rr = np.hypot(P[:, 0] - xw, P[:, 2] - z)
        rn = np.where(rr > 4.25, 4.2 + (rr - 4.2) * (7.5 - 4.2) / (12.0 - 4.2), rr)
        sc = np.where(rr > 1e-9, rn / np.maximum(rr, 1e-9), 1.0)
        P2 = P.copy(); P2[:, 0] = xw + (P[:, 0] - xw) * sc; P2[:, 2] = z + (P[:, 2] - z) * sc; P2[:, 1] = 790.0 + (P[:, 1] - 790.0) * 0.8
        A.Xw[vp] = P2; A.Xw[vv, 1] -= 0.4
        rapor.append('A1 %s: pul DIN 9021 Ø24×2 → ISO 7092 Ø15×1,6 · cıvata −0,4' % ((xw, z),))
    for x, z in ACICI_M8:                                                  # A2
        xw = x + X_A
        vv = A.bul(xw, z, 883.4, 911.6, 6.5, 'açıcı cıvata'); A.Xw[vv, 1] += 0.1
        A.ucgen_ekle(*halka(xw, z, 902.0, 903.6, 4.2, 8.0))
        rapor.append('A2 %s: DIN 125-1 M8 pul eklendi (902,0–903,6) · cıvata +0,1' % ((xw, z),))
    for x, z in RAY_M6:                                                    # A3
        xw = x + X_A
        vv = A.bul(xw, z, 885.4, 907.6, 5.0, 'tabla M6 cıvata'); A.Xw[vv, 1] -= 5.0
        rapor.append('A3 %s: M6 cıvata −5,0 (baş ray tabanına)' % ((xw, z),))
    n1 = A.kapat(ornek_nokta=(1041.0, 905.0, -645.0))
    K = g.dugum('TOPPING_MODUL__sac')                                      # A4
    C = K.Xw0[K.T].mean(1)
    flans = np.all((C >= [1025.9, 893.4, -660.1]) & (C <= [1146.1, 902.1, -609.9]), 1)
    assert flans.sum() > 50, flans.sum()
    on = np.all((C >= [1025.9, 893.4, -609.5]) & (C <= [1146.1, 901.9, -505.0]), 1)
    assert not on.any(), 'flanş önü boş değil: %d üçgen' % on.sum()
    K.ucgen_ekle(*flans_uzanti())
    n2 = K.kapat(ornek_nokta=(1086.0, 897.0, -630.0))
    # A5 · A → TOPPING yatay M8 × 16 → × 10 (eksen x; baş x 1424,5 tarafında, uç 1448,5)
    A = g.dugum('A_GOVDE__paslanmaz')
    for yc, zc in ((1300.0, -300.0), (1300.0, -700.0), (2000.0, -300.0), (2000.0, -700.0)):
        P = A.Xw; k = (P[:, 0] > 1424.4) & (P[:, 0] < 1448.6) & (np.abs(P[:, 1] - yc) < 6.6) & (np.abs(P[:, 2] - zc) < 6.6)
        r = np.hypot(P[:, 1] - yc, P[:, 2] - zc)
        bas = k & (r > 4.5)
        assert bas.any() and k.sum() > 20, ('A5', yc, zc, k.sum())
        uh = float(P[bas, 0].max()); uc = float(P[k, 0].max())
        assert abs((uc - uh) - 16.0) < 0.6, ('A5 boy', uc - uh)
        g_ = k & (r <= 4.1) & (P[:, 0] > uh + 1e-3)
        A.Xw[g_, 0] = uh + (P[g_, 0] - uh) * (10.0 / (uc - uh))
        rapor.append('A5 (y %.0f, z %.0f): A → TOPPING M8 × %.1f → × 10 (uç x %.2f → %.2f)' % (yc, zc, uc - uh, uc, uh + 10.0))
    n1 += A.kapat(ornek_nokta=(1430.0, 1300.0, -300.0))
    rapor.append('A4 açıcı kolonu taban flanşı 120 × 50 → 120 × 155 (z −610…−505 uzantı · 2 × Ø9 @ x 1041 / 1131 z −520)')
    n = g.yaz(go)
    for s in rapor: print(s)
    print('yazıldı %s · A_GOVDE__paslanmaz +%d üçgen · TOPPING_MODUL__sac +%d üçgen · %.1f MB' % (go, n1, n2, n / 1e6))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main(sys.argv[1], sys.argv[2])
