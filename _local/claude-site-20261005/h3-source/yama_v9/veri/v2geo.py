# -*- coding: utf-8 -*-
"""çekmece montaj v2 · geometri araçları (mm): manifold3d katıları, katalog bağlantı elemanları, sac açınım/büküm motoru, morph'lu GLB yazıcı"""
import json, struct, math
import numpy as np
import manifold3d as mf

# ---------------------------------------------------------------- temel katılar
def kutu(lo, hi):
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    return mf.Manifold.cube((hi - lo).tolist()).translate(lo.tolist())


def _hiza(m, eksen):
    """+z ekseninde kurulmuş katıyı 'eksen' yönüne çevir (birim vektör)"""
    a = np.asarray(eksen, float); a = a / np.linalg.norm(a)
    z = np.array([0, 0, 1.0])
    if np.allclose(a, z): return m
    if np.allclose(a, -z): return m.rotate([180.0, 0, 0])
    v = np.cross(z, a); s = np.linalg.norm(v); c = float(np.dot(z, a))
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R = np.eye(3) + K + K @ K * ((1 - c) / s ** 2)
    M = np.hstack([R, np.zeros((3, 1))])
    return m.transform(M.tolist())


def silindir(p0, eksen, r, L, n=32, r2=None):
    """p0'dan eksen yönünde L boyunda silindir / koni (r → r2)"""
    m = mf.Manifold.cylinder(L, r, r if r2 is None else r2, n)
    return _hiza(m, eksen).translate(list(map(float, p0)))


def altigen(p0, eksen, s, L):
    m = mf.Manifold.cylinder(L, s / math.sqrt(3), s / math.sqrt(3), 6)
    return _hiza(m, eksen).translate(list(map(float, p0)))


def mesh(m):
    me = m.to_mesh(); V = np.asarray(me.vert_properties, float)[:, :3]; F = np.asarray(me.tri_verts, np.int64)
    return V, F


def birlesim(L):
    out = None
    for m in L: out = m if out is None else out + m
    return out


def fark(m, L):
    for k in L: m = m - k
    return m


# ---------------------------------------------------------------- katalog elemanları (h3_sac_v1 tabloları ile aynı)
DIN7991 = {"M3": (6.0, 1.7), "M4": (8.0, 2.3), "M5": (10.0, 2.8)}            # dk, k
ISO7380 = {"M3": (5.7, 1.65), "M4": (7.6, 2.2), "M5": (9.5, 2.75)}
ISO4032 = {"M3": (5.5, 2.4), "M4": (7.0, 3.2), "M5": (8.0, 4.7)}              # s, m
DIN125 = {"M3": (3.2, 7.0, 0.5), "M4": (4.3, 9.0, 0.8), "M5": (5.3, 10.0, 1.0)}
PEM_SOMUN = {"M4": dict(delik=5.41, E=7.87, T=2.0, A=0.97), "M5": dict(delik=6.40, E=8.89, T=2.0, A=0.97)}
PEM_SAPLAMA = {"M5": dict(delik=5.0, H=6.9, h=1.0)}
KOR_PERCIN = {3.2: dict(delik=3.3, dk=6.5, k=1.1)}
D_NOM = {"M3": 3.0, "M4": 4.0, "M5": 5.0}
GECIS = {"M3": 3.4, "M4": 4.5, "M5": 5.5}


def din7991(p, a, d, L):
    """havşa başlı: p = baş üst yüzü merkezi, a = vida ekseni (uca doğru), L = toplam boy (baş dahil)"""
    dk, k = DIN7991[d]; r = D_NOM[d] / 2 - 0.05
    a = np.asarray(a, float)
    return silindir(p, a, dk / 2, k, 40, r) + silindir(np.asarray(p) + a * (k - 0.01), a, r, L - k + 0.01, 24)


def iso7380(p, a, d, L):
    """yuvarlak başlı (baş altı yüzü p'de), L = gövde boyu"""
    dk, k = ISO7380[d]; r = D_NOM[d] / 2 - 0.05; a = np.asarray(a, float)
    bas = silindir(np.asarray(p) - a * k, a, dk / 2 * 0.62, k * 0.45, 32, dk / 2) + silindir(np.asarray(p) - a * k * 0.55, a, dk / 2, k * 0.55, 32)
    bas = silindir(np.asarray(p) - a * k, a, dk / 2 * 0.62, k * 0.5, 32, dk / 2 * 0.95) + silindir(np.asarray(p) - a * k * 0.5, a, dk / 2 * 0.95, k * 0.5, 32, dk / 2)
    return bas + silindir(p, a, r, L, 24)


def somun(p, a, d):
    """ISO 4032: p = alt yüz (karşı parçaya değen), a = dışa doğru eksen"""
    s, m = ISO4032[d]
    return altigen(p, a, s, m) - silindir(np.asarray(p) - np.asarray(a) * 0.1, a, D_NOM[d] / 2, m + 0.2, 24)


def pul(p, a, d):
    d1, d2, h = DIN125[d]
    return silindir(p, a, d2 / 2, h, 32) - silindir(np.asarray(p) - np.asarray(a) * 0.1, a, d1 / 2, h + 0.2, 24)


def pem_somun(p, a, d, sac_t):
    """PEM SP: p = sacın düz (flush) yüzü merkezi, a = gövde tarafına (sacın içinden dışarı); sap sacın içinde"""
    c = PEM_SOMUN[d]; a = np.asarray(a, float); p = np.asarray(p, float)
    sap = silindir(p, a, c["delik"] / 2 - 0.01, sac_t, 32)
    gov = silindir(p + a * sac_t, a, c["E"] / 2, c["T"] - sac_t if c["T"] > sac_t else 0.9, 32)
    return (sap + gov) - silindir(p - a * 0.1, a, D_NOM[d] / 2, c["T"] + 1.0, 24)


def pem_saplama(p, a, d, L):
    """PEM FHS gömme başlı saplama: p = başın sac yüzündeki merkezi (baş sacın içinde, flush), a = saplamanın çıktığı yön"""
    c = PEM_SAPLAMA[d]; a = np.asarray(a, float); p = np.asarray(p, float)
    return silindir(p, a, c["H"] / 2, c["h"], 32) + silindir(p, a, D_NOM[d] / 2 - 0.05, L, 24)     # baş sacın içinde (p yüzünden a yönünde h), boy L baş yüzünden


def kor_percin(p, a, d=3.2, kavrama=3.0):
    """ISO 15983 kör perçin: p = baş altı (sac yüzü), a = deliğe giriş yönü; gövde kavrama + 2"""
    c = KOR_PERCIN[d]; a = np.asarray(a, float); p = np.asarray(p, float)
    return silindir(p - a * c["k"], a, c["dk"] / 2, c["k"], 32) + silindir(p, a, d / 2 - 0.02, kavrama + 1.5, 24)


def setskur(p, a, d="M3", L=4.0):
    return silindir(p, a, D_NOM[d] / 2 - 0.05, L, 20)


def havsa_delik(p, a, d, t):
    """p = havşalı yüz merkezi, a = sacın içine doğru · havşa + geçiş"""
    dk, k = DIN7991[d]; a = np.asarray(a, float)
    return silindir(np.asarray(p) - a * 0.01, a, dk / 2 + 0.1, min(k, t) + 0.02, 40, dk / 2 + 0.1 - min(k, t) + 0.02) + \
        silindir(np.asarray(p) - a * 0.5, a, GECIS[d] / 2, t + 1.0, 24)


def delik(p, a, cap, t):
    a = np.asarray(a, float)
    return silindir(np.asarray(p) - a * 0.5, a, cap / 2, t + 1.0, 32)


def kaynak_noktasi(c, r=1.4):
    return mf.Manifold.sphere(r, 12).translate(list(map(float, c)))


def kaynak_dikisi(p0, p1, r=0.9):
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float); L = np.linalg.norm(p1 - p0)
    return silindir(p0, (p1 - p0) / L, r, L, 8)


# ---------------------------------------------------------------- dönüşüm
def rot(eksen, aci_deg):
    a = np.asarray(eksen, float); a = a / np.linalg.norm(a); t = math.radians(aci_deg)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(t) * K + (1 - math.cos(t)) * K @ K


def slerp_R(R0, R1, s):
    """iki dönüş matrisi arası (eksen-açı)"""
    Rd = R1 @ R0.T
    ang = math.acos(max(-1.0, min(1.0, (np.trace(Rd) - 1) / 2)))
    if ang < 1e-9: return R0.copy()
    ax = np.array([Rd[2, 1] - Rd[1, 2], Rd[0, 2] - Rd[2, 0], Rd[1, 0] - Rd[0, 1]]) / (2 * math.sin(ang))
    return rot(ax, math.degrees(ang) * s) @ R0


# ---------------------------------------------------------------- SAC: panel ağacı + büküm sırası
class Sac:
    """paneller SON konumda (dünya mm) kurulur; her bükümlü panel: ebeveyn, büküm ekseni (nokta + yön), açı (işaret otomatik).
    açınım: bükümler tersine açılır (yaprak → kök). Kare üretimi: u_b ∈ [0,1] (1 = düz)."""
    def __init__(s, ad, t, malzeme="AISI 304 2B"):
        s.ad, s.t, s.mal = ad, t, malzeme
        s.panel = []          # dict(ad, m (manifold), ebeveyn, bukum)
        s.bukum = []          # dict(no, panel, p, a, aci, R, aciklama)
        s.delikler = []       # (panel, p, a, cap, tip)

    def ekle(s, ad, m, ebeveyn=None, p=None, a=None, aci=90.0, aciklama=""):
        i = len(s.panel)
        s.panel.append(dict(ad=ad, m=m, eb=ebeveyn, b=None))
        if ebeveyn is not None:
            b = dict(no=len(s.bukum) + 1, panel=i, p=np.asarray(p, float), a=np.asarray(a, float) / np.linalg.norm(a), aci=float(aci), aciklama=aciklama)
            # açı işareti: açınımda panel ebeveynden UZAKLAŞMALI
            V, F = mesh(m); c = V.mean(0)
            Vp, _ = mesh(s.panel[ebeveyn]["m"]); cp = Vp.mean(0)
            best = None
            for sg in (1, -1):
                R = rot(b["a"], -sg * aci); cf = (c - b["p"]) @ R.T + b["p"]
                d = np.linalg.norm(cf - cp)
                if best is None or d > best[0]: best = (d, sg)
            b["sg"] = best[1]
            s.bukum.append(b); s.panel[i]["b"] = len(s.bukum) - 1
        return i

    def zincir(s, i):
        L = []
        while s.panel[i]["eb"] is not None:
            L.append(s.panel[i]["b"]); i = s.panel[i]["eb"]
        return L                       # yaprak → kök sırası

    def donusum(s, i, u):
        """panel i için 4×4 (son → u durumundaki konum). u: büküm no → açıklık (1 düz)"""
        M = np.eye(4)
        for bi in s.zincir(i):         # önce panelin kendi bükümü, sonra atalar
            b = s.bukum[bi]; R = rot(b["a"], -b["sg"] * b["aci"] * u.get(bi, 0.0))
            T = np.eye(4); T[:3, :3] = R; T[:3, 3] = b["p"] - R @ b["p"]
            M = T @ M
        return M

    def ag(s):
        """birleşik ağ (paneller ayrı kabuklar) + köşe → panel indisi"""
        VV, FF, PI = [], [], []; n = 0
        for i, p in enumerate(s.panel):
            V, F = mesh(p["m"]); VV.append(V); FF.append(F + n); PI.append(np.full(len(V), i)); n += len(V)
        return np.vstack(VV), np.vstack(FF), np.concatenate(PI)

    def kare(s, V, PI, u):
        out = V.copy()
        for i in range(len(s.panel)):
            m = PI == i; M = s.donusum(i, u)
            out[m] = V[m] @ M[:3, :3].T + M[:3, 3]
        return out

    def katı(s):
        return birlesim([p["m"] for p in s.panel])


def bukum_acinim_boyu(t, R=None, K=0.45, aci=90.0):
    """keskin köşeli ölçüden (dış ölçü) kesim boyuna düşülecek BD (büküm kesintisi)"""
    R = t if R is None else R
    BA = math.radians(aci) * (R + K * t); OSSB = (R + t) * math.tan(math.radians(aci) / 2)
    return 2 * OSSB - BA


# ---------------------------------------------------------------- GLB (morph hedefli)
def glb_yaz(yol, dugumler, malzemeler):
    """dugumler: dict(ad, V (n×3 float, yerel m), F, mat, translation, targets [n×3 delta, ...])"""
    J = {'asset': {'version': '2.0', 'generator': 'cekmece_montaj_v2'}, 'scene': 0, 'scenes': [{'nodes': list(range(len(dugumler)))}],
         'nodes': [], 'meshes': [], 'accessors': [], 'bufferViews': [], 'buffers': [], 'materials': malzemeler}
    buf = bytearray()

    def ekle(arr, typ, ct, target=None, minmax=False):
        arr = np.ascontiguousarray(arr)
        while len(buf) % 4: buf.append(0)
        off = len(buf); buf.extend(arr.tobytes())
        bv = {'buffer': 0, 'byteOffset': off, 'byteLength': arr.nbytes}
        if target: bv['target'] = target
        J['bufferViews'].append(bv)
        a = {'bufferView': len(J['bufferViews']) - 1, 'componentType': ct, 'count': int(arr.shape[0]), 'type': typ}
        if minmax: a['min'] = arr.min(0).tolist(); a['max'] = arr.max(0).tolist()
        J['accessors'].append(a); return len(J['accessors']) - 1
    for i, d in enumerate(dugumler):
        V = np.asarray(d['V'], np.float32); F = np.asarray(d['F'], np.uint32).reshape(-1)
        pr = {'attributes': {'POSITION': ekle(V, 'VEC3', 5126, 34962, True)}, 'indices': ekle(F, 'SCALAR', 5125, 34963), 'material': d['mat']}
        me = {'name': d['ad'], 'primitives': [pr]}
        if d.get('targets'):
            pr['targets'] = [{'POSITION': ekle(np.asarray(T, np.float32), 'VEC3', 5126, 34962, True)} for T in d['targets']]
            me['weights'] = [0.0] * len(d['targets'])
        J['meshes'].append(me)
        J['nodes'].append({'name': d['ad'], 'mesh': i, 'translation': [float(x) for x in d['translation']]})
    while len(buf) % 4: buf.append(0)
    J['buffers'].append({'byteLength': len(buf)})
    js = json.dumps(J, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    while len(js) % 4: js += b' '
    out = struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(buf)) + struct.pack('<II', len(js), 0x4E4F534A) + js + struct.pack('<II', len(buf), 0x004E4942) + bytes(buf)
    open(yol, 'wb').write(out); return len(out)
