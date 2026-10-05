# -*- coding: utf-8 -*-
"""ZİNCİR ADIMI ÖNERİSİ · TOPPING BAĞLANTI AÇIKLARI (4 Eki 2026 · Claude · yerel) — ajan zincirinin son GLB'si sonrası
Kullanım: python zincir_T_tamamla.py giris.glb cikis.glb
Yöntem zincir_A_tamamla.py ile aynı (düğüm adı tabanlı; mevcut üçgen sırası korunur, ent indisleri değişmez; yeni üçgenler primitif sonuna;
beklenen bileşen bulunamazsa DURUR, çıktı yazmaz).

Bulunan açıklar (TOPPING montaj animasyonu v3 planı sırasında ölçüldü):
  T1 · TOPPING → B 4 × ISO 4762 M8 × 25 (arayuz_kb_*): başın altındaki DIN 9021 pul Ø24, kaide plakasındaki ve kaide borusunun üst duvarındaki
       Ø16 servis deliğinden GEÇEMEZ (boru kapalı, kaynaklı; A1 ile aynı açık). → ISO 7092 M8 küçük seri pul (8,4 / 15 × 1,6); cıvata 0,4 aşağı.
  T2 · Soğuk oda yalıtımı modelde YERİNDE KÖPÜK tek blok (pu_soguk_duvar); dış tavanın yan dönüşlerini ve arka dönüşünü sarıyor (≈ 3,5 cm³ bindirme)
       → kesilmiş levha olarak takılamaz. Kemal 4 Eki: yalıtım yüzey yüzey kesilmiş levha + dış saca yapıştırma. → blok 4 levhaya bölünür
       (arka / sol / sağ / tavan; birleşimi = blok), sacla bindiren hacim levhadan çıkarılır (flanş yarığı), dış sac yüzüne 0,5 mm yapıştırıcı
       katmanı (arka yüzde levha 0,3 mm incelir), gıda tarafı iç köşelere 3 × 3 silikon derz fitili (7). Köpük üçgenleri dejenere edilir
       (ent indisleri korunur), levhalar TOPPING_GOVDE__pu sonuna, yapıştırıcı + silikon TOPPING_GOVDE__conta sonuna eklenir.
"""
import json, struct, sys
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

KB_M8 = [(1456.0, -706.0), (1456.0, -110.0), (2120.0, -110.0), (2480.0, -110.0)]
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




# ------------------------------------------------------------------ T2 · yerinde köpük → kesilmiş PU levhalar + yapıştırıcı + derz silikonu
import manifold3d as mf
PU_KES = [('arka', [((-1e4, -1e4, -1e4), (1e4, 1e4, -571.0))]),
          ('sol', [((-1e4, -1e4, -571.0), (1495.0, 1e4, 1e4)), ((1495.0, -1e4, -571.0), (1968.0, 2140.5, 1e4))]),
          ('sag', [((2441.0, -1e4, -571.0), (1e4, 1e4, 1e4)), ((1968.0, -1e4, -571.0), (2441.0, 2140.5, 1e4))]),
          ('tavan', [((1495.0, 2140.5, -571.0), (2441.0, 1e4, 1e4))])]
# yapıştırıcı katmanı: levhanın dış sac yüzü (dış sac ile levha arasındaki 0,5 mm aralıkta; arka yüzde aralık yok → levhadan 0,3 mm)
YAP = {'sol': (0, 1438.0, 1437.5), 'sag': (0, 2498.0, 2498.5), 'tavan': (1, 2198.0, 2198.5), 'arka': (2, -628.0, -627.7)}


def _kaynak(X, T):
    u, inv = np.unique(np.round(X[T.reshape(-1)], 4), axis=0, return_inverse=True); return u, inv.reshape(-1, 3)


def _man(V, F):
    m = mf.Manifold(mf.Mesh(vert_properties=np.asarray(V, np.float32), tri_verts=np.asarray(F, np.uint32)))
    return m if m.status() == mf.Error.NoError else None


def _kutu(lo, hi): return mf.Manifold.cube(list(np.subtract(hi, lo))).translate(list(lo))


def _mesh(m):
    me = m.to_mesh(); return np.asarray(me.vert_properties, float)[:, :3], np.asarray(me.tri_verts, np.int64)


def _fitil(p0, p1, u, v, a=3.0):
    """iç köşe silikon fitili: p0 → p1 doğrusu, iki duvar yönü u, v (köşeden içeri) · dik üçgen kesit a × a"""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); u = np.asarray(u, float) * a; v = np.asarray(v, float) * a
    V = np.array([p0, p0 + u, p0 + v, p1, p1 + u, p1 + v])
    F = np.array([[0, 2, 1], [3, 4, 5], [0, 1, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2], [1, 2, 5], [1, 5, 4]])
    m = _man(V, F)
    if m is None or m.volume() < 0: F = F[:, ::-1]
    return V, F


def t2(g, rapor):
    U = g.dugum('TOPPING_GOVDE__pu')
    kom = [k for k in range(len(U.lo)) if U.hi[k][1] > 2190 and U.hi[k][0] - U.lo[k][0] > 1000]
    assert len(kom) == 1, ('pu_soguk_duvar bileşeni', len(kom))
    vs = np.where(U.cl == kom[0])[0]; tm = np.all(np.isin(U.T, vs), 1)
    M = _man(*_kaynak(U.Xw, U.T[tm])); assert M is not None, 'köpük bloğu kapalı değil'
    hac0 = M.volume()
    # köpükle bindiren gövde sacları (köpük modeli flanşları sarıyor) → levhadan çıkarılır (yarık / cep)
    cik = []
    for dn in ('TOPPING_GOVDE__kabuk', 'TOPPING_GOVDE__sac', 'TOPPING_GOVDE__cerceve'):
        S = g.dugum(dn)
        for k in range(len(S.lo)):
            if np.any(S.lo[k] > U.hi[kom[0]] + 1) or np.any(S.hi[k] < U.lo[kom[0]] - 1): continue
            vk = np.where(S.cl == k)[0]; tk = np.all(np.isin(S.T, vk), 1)
            m = _man(*_kaynak(S.Xw, S.T[tk]))
            if m is not None and (m ^ M).volume() > 0.01: cik.append(m)
    S_ = mf.Manifold.batch_boolean(cik, mf.OpType.Add) if cik else None
    yeniV, yeniF, conV, conF = [], [], [], []
    n = 0
    for ad, kutular in PU_KES:
        L = M ^ mf.Manifold.batch_boolean([_kutu(lo, hi) for lo, hi in kutular], mf.OpType.Add)
        if S_ is not None: L = L - S_
        e, a0, a1 = YAP[ad]
        if ad == 'arka':                                     # levha 0,3 mm incelir, yapıştırıcı o katmanda
            lo2 = [-1e4] * 3; hi2 = [1e4] * 3; lo2[e] = a0; hi2[e] = a1
            Y_ = L ^ _kutu(lo2, hi2); L = L - _kutu(lo2, hi2)
        else:                                                # dış sac ile levha arasındaki 0,5 mm aralık
            lo2 = [-1e4] * 3; hi2 = [1e4] * 3; o_ = 2 * a0 - a1; lo2[e] = min(a0, o_); hi2[e] = max(a0, o_)
            ince = L ^ _kutu(lo2, hi2); tr = [0.0, 0.0, 0.0]; tr[e] = a1 - a0; Y_ = ince.translate(tr)
        V, F = _mesh(L); yeniV.append(V); yeniF.append(F + n); n += len(V)
        V, F = _mesh(Y_); conV.append(V); conF.append(F)
        rapor.append('T2 PU levha %-5s %.0f cm³ · yapıştırıcı %.1f cm³' % (ad, L.volume() / 1000, Y_.volume() / 1000))
    # derz silikonu (gıda tarafı iç köşeler)
    fit = [((1496.0, 1153.0, -570.0), (1496.0, 1533.0, -570.0), (1, 0, 0), (0, 0, 1)), ((1496.0, 1576.0, -570.0), (1496.0, 2140.0, -570.0), (1, 0, 0), (0, 0, 1)),
           ((2440.0, 1153.0, -570.0), (2440.0, 1533.0, -570.0), (-1, 0, 0), (0, 0, 1)), ((2440.0, 1576.0, -570.0), (2440.0, 2140.0, -570.0), (-1, 0, 0), (0, 0, 1)),
           ((1496.0, 2140.0, -570.0), (2440.0, 2140.0, -570.0), (0, -1, 0), (0, 0, 1)),
           ((1496.0, 2140.0, -570.0), (1496.0, 2140.0, 37.5), (1, 0, 0), (0, -1, 0)), ((2440.0, 2140.0, -570.0), (2440.0, 2140.0, 37.5), (-1, 0, 0), (0, -1, 0))]
    for p0, p1, u, v in fit:
        V, F = _fitil(p0, p1, u, v); conV.append(V); conF.append(F)
    rapor.append('T2 derz silikonu: %d iç köşe fitili (3 × 3)' % len(fit))
    # köpük bloğu üçgenleri dejenere (ent indisleri korunur), levhalar sona
    I = U.I.reshape(-1, 3).copy(); I[tm] = I[tm][0, 0]; U.I = I.reshape(-1).astype(U.I.dtype)
    Vn = np.vstack(yeniV); Fn = np.vstack(yeniF)
    P_, N_, F_ = duz_kati(Vn, Fn); U.ucgen_ekle(P_, N_, F_)
    n_u = U.kapat()
    C = g.dugum('TOPPING_GOVDE__conta')
    for V, F in zip(conV, conF):
        P_, N_, F_ = duz_kati(V, F); C.ucgen_ekle(P_, N_, F_)
    n_c = C.kapat()
    rapor.append('T2 köpük hacmi %.0f cm³ → levhalar + yapıştırıcı (sac bindirmesi çıkarıldı) · PU +%d üçgen · conta +%d üçgen' % (hac0 / 1000, n_u, n_c))


def main(gi, go):
    g = GLB(gi); rapor = []
    T = g.dugum('TOPPING_GOVDE__paslanmaz')
    for xw, z in KB_M8:                                                    # T1
        vp = T.bul(xw, z, 789.9, 792.1, 12.0, 'KB pul'); vv = T.bul(xw, z, 766.9, 800.1, 6.5, 'KB cıvata')
        P = T.Xw[vp]; rr = np.hypot(P[:, 0] - xw, P[:, 2] - z)
        rn = np.where(rr > 4.25, 4.2 + (rr - 4.2) * (7.5 - 4.2) / (12.0 - 4.2), rr)
        sc = np.where(rr > 1e-9, rn / np.maximum(rr, 1e-9), 1.0)
        P2 = P.copy(); P2[:, 0] = xw + (P[:, 0] - xw) * sc; P2[:, 2] = z + (P[:, 2] - z) * sc; P2[:, 1] = 790.0 + (P[:, 1] - 790.0) * 0.8
        T.Xw[vp] = P2; T.Xw[vv, 1] -= 0.4
        rapor.append('T1 %s: pul DIN 9021 Ø24×2 → ISO 7092 Ø15×1,6 · cıvata −0,4' % ((xw, z),))
    n1 = T.kapat()
    t2(g, rapor)
    n = g.yaz(go)
    for s in rapor: print(s)
    print('yazıldı %s · TOPPING_GOVDE__paslanmaz +%d üçgen · %.1f MB' % (go, n1, n / 1e6))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main(sys.argv[1], sys.argv[2])
