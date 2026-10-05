

# ------------------------------------------------------------------ T2 · yerinde köpük → kesilmiş PU levhalar + yapıştırıcı + derz silikonu
import manifold3d as mf
PU_KES = [('arka', (-1e4, -1e4, -1e4), (1e4, 1e4, -571.0)), ('sol', (-1e4, -1e4, -571.0), (1495.0, 1e4, 1e4)),
          ('sag', (2441.0, -1e4, -571.0), (1e4, 1e4, 1e4)), ('tavan', (1495.0, -1e4, -571.0), (2441.0, 1e4, 1e4))]
# yapıştırıcı katmanı: levhanın dış sac yüzü (dış sac ile levha arasındaki 0,5 mm aralıkta; arka yüzde aralık yok → levhadan 0,3 mm)
YAP = {'sol': (0, 1438.0, 1437.5), 'sag': (0, 2498.0, 2498.5), 'tavan': (1, 2198.0, 2198.5), 'arka': (2, -628.0, -627.7)}


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
    Tk = U.T[tm]; uq, inv = np.unique(Tk.reshape(-1), return_inverse=True)
    M = _man(U.Xw[uq], inv.reshape(-1, 3)); assert M is not None, 'köpük bloğu kapalı değil'
    hac0 = M.volume()
    # köpükle bindiren gövde sacları (köpük modeli flanşları sarıyor) → levhadan çıkarılır (yarık / cep)
    cik = []
    for dn in ('TOPPING_GOVDE__kabuk', 'TOPPING_GOVDE__sac', 'TOPPING_GOVDE__cerceve'):
        S = g.dugum(dn)
        for k in range(len(S.lo)):
            if np.any(S.lo[k] > U.hi[kom[0]] + 1) or np.any(S.hi[k] < U.lo[kom[0]] - 1): continue
            vk = np.where(S.cl == k)[0]; tk = np.all(np.isin(S.T, vk), 1)
            u2, i2 = np.unique(S.T[tk].reshape(-1), return_inverse=True)
            m = _man(S.Xw[u2], i2.reshape(-1, 3))
            if m is not None and (m ^ M).volume() > 0.01: cik.append(m)
    S_ = mf.Manifold.batch_boolean(cik, mf.OpType.Add) if cik else None
    yeniV, yeniF, conV, conF = [], [], [], []
    n = 0
    for ad, lo, hi in PU_KES:
        L = M ^ _kutu(lo, hi)
        if S_ is not None: L = L - S_
        e, a0, a1 = YAP[ad]
        if a1 > a0 and ad != 'arka' or (ad == 'sag' or ad == 'tavan'):
            pass
        if ad == 'arka':                                     # levha 0,3 mm incelir, yapıştırıcı o katmanda
            lo2 = [-1e4] * 3; hi2 = [1e4] * 3; lo2[e] = a0; hi2[e] = a1
            Y_ = L ^ _kutu(lo2, hi2); L = L - _kutu(lo2, hi2)
        else:                                                # dış sac ile levha arasındaki 0,5 mm aralık
            lo2 = [-1e4] * 3; hi2 = [1e4] * 3; lo2[e] = min(a0, a0 + (a0 - a1) * -1); hi2[e] = max(a0, a0 + (a0 - a1) * -1)
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
