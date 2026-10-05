# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 53 · TOPPING YENİ MENÜ YERLEŞİMİ (menu7 · 4 Eki 2026 · Claude · YEREL · Kemal onayı)
python 53_menu7.py girdi.glb cikti.glb      (zincir: hat3_v9t.glb → hat3_v9u.glb)

Menü yalnız pide + lahmacun. Analiz: scratchpad gece2/menu7/ANALIZ.md (ölçüler v9t'den). ONAYLI KARARLAR:
  1. Ürün → hazne: üst sol 380 = LAHMACUN HARCI (hazne üstü +30 → 2129, tavana 11 mm) · üst ORTA (YENİ 3. UNO, 200 genişlik, iki yanda 19 mm) = KIYMA ·
     üst sağ (eski sos UNO'su, yeri aynı) = PATATES PÜRESİ (sos yayıcısı patates yayıcısı olarak kalır — yalnız ad) · alt 1. UNO = TAVUK (eski kıyma) ·
     alt 2. UNO = KUŞBAŞI (hunisinde yalnız ÖN-SAĞ KÖŞE CEBİ) · kaşar + sucuk kasetleri aynı.
     Ünite adları: TOPPING/Lahmacun harcı · /Kıyma (yeni orta) · /Patates · /Tavuk · /Kuşbaşı · /Kaşar · /Sucuk (Sos kalktı) — liste 55 → 56.
  2. 3. UNO: mevcut (sos) UNO'nun birebir kopyası x 2259,5 → 2031 (döner vana + aktüatör, valf bloğu, ürün silindiri, piston, POM burç, pnömatik silindir,
     çıkış flanşları) · VALF / PISTON hareketli düğümleri yeni düğüm (…_KIYMA_ORTA, statik — sipariş animasyonları eski menüde, yeniden üretilmedi) ·
     dar-yüksek huni 200 × 440, üst 2099 · gıda hattı: çıkış → rafın üstünde PASLANMAZ DİRSEK (Ø35,6 × 1,8; 2 × 90°: +z → −x R50, −x → −y R36) → x 1911,5
     z −170'te raftan DİK iner → D32 gıda hortumu (sos hortumu kopyası, kuşbaşı cebi ↔ kaşar kılavuzu arası 64,9) → hortum ucu + boru Ø29,8 →
     yeni düşme kovanı (raf deliği Ø39,6 + raf contası, taban: soğuk oda tabanı Ø37 / PU Ø38 / alt sac Ø31 + kovan sacı kopyası, taban contası) → boru
     ucu y 1048 (tabla yolu, z −170) · pnömatik: silindir bağlantıları (kopya) + valf adasının sağ yüzüne 2 yeni rakor + 2 yeni Ø6 yeşil hava
     hortumu (ada → y 1276 → x 2124'te 1335 / 1347'ye çıkar → soğutma emiş ve sıvı boruları arasından (z −678 / −668) → x 2302'de (hava kanalının
     arkası, z −688 / −703) 1850'ye → evaporatör üstünden cebe iner). Silindirde sensör / kablo yok (sos UNO'sunda da yok).
  3. Sağ evaporatör (R) kasetinde 3. UNO silindiri için YALITIMLI CEP: kasetin dış sacı / PU / iç kutu / fan bölmesi tabanı / ayırma sacı / ön conta
     x 1973–2089, y ≥ 1568 aralığında kesilir (serpantin y ≤ 1565 — bobin yüzü KÜÇÜLMEZ) · cep: 1 mm sac + 20 mm PU + 1 mm sac yan duvarlar,
     1 + 10 + 1 taban (iç taban y 1580) · ön yüzde cep çevresi conta 10 mm · iç genişlik 72 (silindir Ø37,4 → iki yanda 17,3; tabana 14,6) ·
     silindir tutucu plakası + ara plaka (sos'ta y 1533,9–1594,6) cep tabanının üstüne alınır (y 1580–1594,6) · POM burç üfleme ağzından geçtiği
     için burç kılıfı (paslanmaz boru + alt ayak, ağız tabanına).
  4. Bütün hazneler (5) yeniden: kare-yuvarlak geçiş hunisi = Ø64 boyun ↔ üst kesit dışbükey zarfı (açınımlı sac geçiş parçasıyla aynı yüzey),
     DİKEY KÖŞELER R25 (iç R23,5), et 1,5 · kuşbaşı: ön-sağ köşe cebi (x ≥ 1879,1 · z ≥ −201, dik yüzler, et 1,5).
  5. Kaşar: patatesli / tavuklu pidede kaşar yok varsayıldı (model değişikliği yok).
Denetimler bu betikte: her bileşen bulunur (kutuyla, tol 0,3) · boolean sonuçları kapalı · hazne hacimleri _ent.json'a."""
import os, sys, time, json, struct, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb, tup
import manifold3d as mf

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ sabitler
DX_UNO = 2031.0 - 2259.5          # sos UNO → orta UNO
X_DUS = 1911.5                    # yeni düşme ekseni (kuşbaşı cebi 1879,1 ↔ kaşar kılavuzu 1944 ortası)
DX_DUS = X_DUS - 2259.5
Z_DUS = -169.8                    # kovan ekseni (sos kovanı sac 84 ile aynı)
Z_RAF = -172.45                   # raf deliği ekseni (raf contası ile aynı)
YENI_KOD = "TOPPING/Kıyma*"       # geçici (sonda yeniden sıralanır)

UNO = [
    ('TOPPING_MODUL__aluminyum', (2168.5, 1591.0, -415.0), (2218.5, 1635.0, -359.0)),   # döner vana aktüatörü
    ('TOPPING_MODUL__aluminyum', (2247.5, 1601.5, -827.0), (2271.5, 1625.5, -811.0)),   # pnömatik arka mafsal
    ('TOPPING_MODUL__aluminyum', (2240.5, 1594.6, -811.0), (2277.9, 1632.4, -672.0)),   # pnömatik silindir D32
    ('TOPPING_MODUL__aluminyum', (2247.5, 1601.6, -672.0), (2271.2, 1625.4, -662.0)),   # ön boğaz
    ('TOPPING_MODUL__paslanmaz', (2241.5, 1595.6, -346.0), (2277.0, 1631.4, -250.7)),
    ('TOPPING_MODUL__paslanmaz', (2234.3, 1588.4, -240.8), (2284.0, 1638.6, -235.2)),
    ('TOPPING_MODUL__paslanmaz', (2230.0, 1584.2, -248.6), (2288.1, 1642.8, -227.4)),
    ('TOPPING_MODUL__paslanmaz', (2226.5, 1580.7, -436.0), (2291.5, 1646.3, -428.0)),
    ('TOPPING_MODUL__paslanmaz', (2226.5, 1580.7, -559.0), (2291.5, 1646.3, -552.0)),
    ('TOPPING_MODUL__paslanmaz', (2234.6, 1588.1, -250.7), (2285.1, 1638.9, -240.8)),
    ('TOPPING_MODUL__paslanmaz', (2228.7, 1647.6, -418.5), (2291.2, 1707.0, -355.5)),   # hazne boynu
    ('TOPPING_MODUL__paslanmaz', (2215.3, 1665.0, -432.2), (2305.0, 1683.0, -341.8)),   # TC kelepçe
    ('TOPPING_MODUL__paslanmaz', (2255.5, 1642.9, -242.0), (2263.5, 1658.8, -234.0)),
    ('TOPPING_MODUL__paslanmaz', (2218.5, 1575.4, -428.0), (2300.5, 1647.6, -346.0)),   # valf bloğu
    ('TOPPING_MODUL__pom', (2244.9, 1598.6, -635.0), (2274.5, 1628.4, -565.0)),         # POM burç (arka duvar)
    ('TOPPING_MODUL__saydam_celik', (2230.5, 1584.7, -552.0), (2287.7, 1642.3, -436.0)),
]
DUS = [
    ('TOPPING_MODUL__conta', (2239.7, 1572.0, -192.5), (2279.3, 1575.0, -152.4)),      # raf geçiş contası
    ('TOPPING_MODUL__paslanmaz', (2230.2, 1539.0, -198.6), (2288.8, 1551.0, -140.5)),  # raf altı flanş
    ('TOPPING_MODUL__hortum_gida', (2238.7, 1216.0, -191.0), (2280.3, 1539.0, -149.6)),  # D32 gıda hortumu
    ('TOPPING_MODUL__paslanmaz', (2234.7, 1204.0, -195.0), (2284.3, 1216.0, -145.7)),  # hortum kelepçesi
    ('TOPPING_MODUL__paslanmaz', (2255.5, 1206.0, -210.0), (2263.5, 1214.0, -195.0)),  # kelepçe vidası
    ('TOPPING_MODUL__paslanmaz', (2241.6, 1182.0, -188.0), (2277.4, 1205.5, -152.5)),
    ('TOPPING_MODUL__paslanmaz', (2238.7, 1184.5, -191.0), (2280.3, 1203.5, -149.6)),  # hortum ucu
    ('TOPPING_MODUL__paslanmaz', (2244.6, 1108.0, -184.6), (2274.4, 1182.0, -155.0)),  # boru Ø29,8 (→ y 1048'e uzar)
    ('TOPPING_MODUL__conta', (2241.6, 1149.0, -187.5), (2277.4, 1152.0, -152.0)),      # taban contası
    ('TOPPING_GOVDE__sac', (2240.5, 1110.5, -188.8), (2278.5, 1149.0, -150.8)),        # taban kovanı
]
TUTUCU = [
    ('TOPPING_MODUL__paslanmaz', (2233.5, 1533.9, -692.0), (2285.5, 1576.9, -630.0)),  # silindir tutucu plakası
    ('TOPPING_MODUL__fircali', (2234.5, 1576.9, -680.0), (2284.5, 1594.6, -674.0)),    # ara plaka
]
HAVA_RAKOR = [
    ('TOPPING_MODUL__hava_ana', (2252.5, 1632.5, -692.0), (2260.5, 1637.5, -684.0)),
    ('TOPPING_MODUL__hava_ana', (2252.0, 1637.5, -692.5), (2261.0, 1640.5, -683.5)),
    ('TOPPING_MODUL__hava_ana', (2258.5, 1632.5, -799.0), (2266.5, 1637.5, -791.0)),
    ('TOPPING_MODUL__hava_ana', (2258.0, 1637.5, -799.5), (2267.0, 1640.5, -790.5)),
]
ADA_RAKOR = ('TOPPING_MODUL__hava_ana', (1998.0, 1297.0, -675.0), (2008.0, 1307.0, -665.0))   # valf adası sağ yüz rakoru (sos)
HAZ = {  # eski hazne kutusu → yeni hazne (boyun x, boyun y, kutu başı y, üst y, x0, x1)
    "harc":    (('TOPPING_MODUL__paslanmaz', (1532.0, 1707.0, -560.0), (1912.0, 2099.0, -120.0)), (1722.0, 1707.0, 1887.0, 2129.0, 1532.0, 1912.0)),
    "patates": (('TOPPING_MODUL__paslanmaz', (2149.5, 1707.0, -560.0), (2369.5, 1992.0, -120.0)), (2259.5, 1707.0, 1887.0, 1992.0, 2149.5, 2369.5)),
    "tavuk":   (('TOPPING_MODUL__paslanmaz', (1501.0, 1284.0, -560.0), (1691.0, 1499.0, -120.0)), (1596.0, 1284.0, 1464.0, 1499.0, 1501.0, 1691.0)),
    "kusbasi": (('TOPPING_MODUL__paslanmaz', (1753.0, 1284.0, -560.0), (1943.0, 1499.0, -120.0)), (1848.0, 1284.0, 1464.0, 1499.0, 1753.0, 1943.0)),
}
ORTA_HAZNE = (2031.0, 1707.0, 1887.0, 2099.0, 1931.0, 2131.0)
NECK_Z, NECK_R, ET, KOSE_R = -387.0, 32.0, 1.5, 25.0
HZ0, HZ1 = -560.0, -120.0
CEP_KB = (1879.1, -201.0)          # kuşbaşı ön-sağ köşe cebi: x ≥ 1879,1 · z ≥ −201
# evaporatör cebi
EV_X0, EV_X1 = 2031.0 - 58.0, 2031.0 + 58.0      # 1973 … 2089 (dış)
EV_IX0, EV_IX1 = 2031.0 - 36.0, 2031.0 + 36.0    # 1995 … 2067 (iç)
EV_Y0, EV_IY0, EV_YT = 1568.0, 1580.0, 1838.0    # dış taban · iç taban · kesim üstü (kaset üstü 1835, kablo kanalı 1840)
EV_Z0, EV_Z1 = -826.0, -640.0
EVAP = [('TOPPING_MODUL__sac', 17), ('TOPPING_MODUL__pu', 0), ('TOPPING_MODUL__sac', 18), ('TOPPING_MODUL__sac', 19), ('TOPPING_MODUL__sac', 20),
        ('TOPPING_MODUL__pom', 37)]
EVAP_KUTU = {('TOPPING_MODUL__sac', 17): ((1758.0, 1383.0, -826.0), (2223.0, 1835.0, -640.0)),
             ('TOPPING_MODUL__pu', 0): ((1759.0, 1384.0, -825.0), (2222.0, 1834.0, -640.0)),
             ('TOPPING_MODUL__sac', 18): ((1798.0, 1423.0, -786.0), (2183.0, 1795.0, -631.0)),
             ('TOPPING_MODUL__sac', 19): ((1799.0, 1569.0, -731.0), (2182.0, 1570.0, -631.0)),
             ('TOPPING_MODUL__sac', 20): ((1799.0, 1570.0, -701.5), (2182.0, 1794.0, -700.0)),
             ('TOPPING_MODUL__pom', 37): ((1758.0, 1383.0, -640.0), (2223.0, 1835.0, -630.0))}
DELIK = [  # (düğüm, kutu, merkez x, merkez z, r) — raf / taban sandviçi
    ('TOPPING_GOVDE__sac', ((1496.0, 1534.0, -570.0), (2440.0, 1575.0, -50.0)), X_DUS, -170.0, 19.45),  # raf (raf contası dış r 19,44 — dirsek dik ekseniyle eş merkezli)
    ('TOPPING_GOVDE__sac', ((1496.0, 1110.5, -570.0), (2440.0, 1152.0, 23.0)), X_DUS, Z_DUS, 18.5),     # soğuk oda tabanı (sos: r 18,5)
    ('TOPPING_GOVDE__pu', ((1496.0, 1110.5, -567.0), (2440.0, 1150.8, 36.8)), X_DUS, Z_DUS, 19.0),      # taban PU (sos: r 19)
    ('TOPPING_GOVDE__sac', ((1437.5, 1109.0, -628.5), (2498.5, 1110.5, 38.0)), X_DUS, Z_DUS, 15.5),     # alt sac (sos: r 15,5)
]


# ------------------------------------------------------------------ yardımcılar
def ucg(b):
    return np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])


def bul(g, d, lo, hi):
    return g.bilesen(d, lo=np.array(lo), hi=np.array(hi), tol=0.3)


def mf_den(P):
    V = P.reshape(-1, 3); R = np.round(V, 4); u, inv = np.unique(R, axis=0, return_inverse=True)
    m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=inv.reshape(-1, 3).astype(np.uint32)))
    assert m.status() == mf.Error.NoError and not m.is_empty(), "manifold kurulamadı"
    return m


def mf_ucg(m):
    M = m.to_mesh(); V = np.asarray(M.vert_properties)[:, :3].astype(float); T = np.asarray(M.tri_verts).astype(np.int64)
    return V[T]


def kutu_mf(lo, hi):
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    return mf.Manifold.cube(hi - lo).translate(lo)


def silindir_y(cx, cz, r, y0, y1, n=48):
    return mf.Manifold.cylinder(y1 - y0, r, r, n).rotate([-90.0, 0.0, 0.0]).translate([cx, y0, cz])


def rrect(x0, x1, z0, z1, r, k=10):
    P = []
    for cx, cz, a0 in [(x1 - r, z0 + r, -90), (x1 - r, z1 - r, 0), (x0 + r, z1 - r, 90), (x0 + r, z0 + r, 180)]:
        for a in np.linspace(a0, a0 + 90, k): P.append((cx + r * np.cos(np.radians(a)), cz + r * np.sin(np.radians(a))))
    return np.array(P)


def kat_y(P2, y):
    return np.c_[P2[:, 0], np.full(len(P2), y), P2[:, 1]]


def daire(cx, cz, r, n=64):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False); return np.c_[cx + r * np.cos(t), cz + r * np.sin(t)]


def hazne(nx, y0, y1, yt, x0, x1, cep=None):
    """kare-yuvarlak geçiş hunisi (dışbükey zarf) + düz kutu, dikey köşe R25, et 1,5, üstü açık. Dönüş: (kabuk, iç boşluk y0…yt)"""
    dis = mf.Manifold.hull_points(np.r_[kat_y(daire(nx, NECK_Z, NECK_R), y0), kat_y(rrect(x0, x1, HZ0, HZ1, KOSE_R), y1)].tolist()) + \
        mf.Manifold.hull_points(np.r_[kat_y(rrect(x0, x1, HZ0, HZ1, KOSE_R), y1), kat_y(rrect(x0, x1, HZ0, HZ1, KOSE_R), yt)].tolist())
    ri = rrect(x0 + ET, x1 - ET, HZ0 + ET, HZ1 - ET, KOSE_R - ET)
    ic = mf.Manifold.hull_points(np.r_[kat_y(daire(nx, NECK_Z, NECK_R - ET), y0), kat_y(ri, y1)].tolist()) + \
        mf.Manifold.hull_points(np.r_[kat_y(ri, y1), kat_y(ri, yt + 5.0)].tolist()) + \
        mf.Manifold.hull_points(np.r_[kat_y(daire(nx, NECK_Z, NECK_R - ET), y0 - 5.0), kat_y(daire(nx, NECK_Z, NECK_R - ET), y0)].tolist())
    if cep is not None:
        cx, cz = cep
        dis = dis - kutu_mf((cx, y0 - 10, cz), (x1 + 50, yt + 50, HZ1 + 50))
        ic = ic - kutu_mf((cx - ET, y0 - 20, cz - ET), (x1 + 60, yt + 60, HZ1 + 60))
    kab = dis - ic
    bosluk = ic ^ kutu_mf((x0 - 50, y0, HZ0 - 50), (x1 + 50, yt, HZ1 + 50))
    assert kab.status() == mf.Error.NoError and kab.genus() >= 0
    return kab, bosluk


def boru_yolu(noktalar):
    """kırık çizgi + yay noktaları → halka çerçeveleri (paralel taşıma)"""
    Q = [np.asarray(q, float) for q in noktalar]
    T = []
    for i in range(len(Q)):
        if i == 0: t = Q[1] - Q[0]
        elif i == len(Q) - 1: t = Q[-1] - Q[-2]
        else: t = (Q[i + 1] - Q[i - 1])
        T.append(t / np.linalg.norm(t))
    u = np.cross(T[0], [0, 1, 0]) if abs(T[0][1]) < 0.9 else np.cross(T[0], [1, 0, 0]); u /= np.linalg.norm(u)
    U = [u]
    for i in range(1, len(Q)):
        v = U[-1] - (U[-1] @ T[i]) * T[i]; U.append(v / np.linalg.norm(v))
    return Q, T, U


def boru_ucgen(noktalar, ro, ri, n=32):
    Q, T, U = boru_yolu(noktalar)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    def halka(i, r):
        w = np.cross(T[i], U[i]); return [Q[i] + r * (np.cos(a) * U[i] + np.sin(a) * w) for a in th]
    O = [halka(i, ro) for i in range(len(Q))]; I = [halka(i, ri) for i in range(len(Q))]
    out = []
    for i in range(len(Q) - 1):
        for j in range(n):
            k = (j + 1) % n
            out += [(O[i][j], O[i][k], O[i + 1][k]), (O[i][j], O[i + 1][k], O[i + 1][j])]
            out += [(I[i][j], I[i + 1][k], I[i][k]), (I[i][j], I[i + 1][j], I[i + 1][k])]
    for i, s in ((0, 1), (len(Q) - 1, -1)):
        for j in range(n):
            k = (j + 1) % n
            a = [(O[i][j], I[i][j], I[i][k]), (O[i][j], I[i][k], O[i][k])]
            out += a if s > 0 else [(t[0], t[2], t[1]) for t in a]     # baş kapağı kenarı yan yüzle ters yönlü (kapalı ağ)
    P = np.array(out)
    # dışa bakan yön denetimi: kapalı ağın işaretli hacmi > 0 olmalı
    vol = np.einsum("ij,ij->i", P[:, 0], np.cross(P[:, 1], P[:, 2])).sum() / 6.0
    if vol < 0: P = P[:, [0, 2, 1]]
    return P


def yay(c, a, b, R, k=12):
    """merkez c, başlangıç yönü a (merkezden), bitiş yönü b — çeyrek yay noktaları"""
    c = np.asarray(c, float); a = np.asarray(a, float); b = np.asarray(b, float)
    return [c + R * (np.cos(t) * a + np.sin(t) * b) for t in np.linspace(0, np.pi / 2, k + 1)]


def dugum_klonla(J, BIN_ekle, oku, ad, yeni_ad, dx_m, mek_yeni):
    """hareketli (TRS'li) düğümü yeni adla klonla: ağ verisi kopyalanır (paylaşım yok), öteleme + dx, bütün üçgenler yeni mek"""
    ni = [i for i, n in enumerate(J["nodes"]) if n.get("name") == ad]; assert len(ni) == 1, ad
    nd = J["nodes"][ni[0]]; ms = J["meshes"][nd["mesh"]]
    prs = []
    for pr in ms["primitives"]:
        q = json.loads(json.dumps({k: v for k, v in pr.items() if k not in ("attributes", "indices")}))
        q["attributes"] = {}
        for k, a in pr["attributes"].items():
            arr = oku(a); q["attributes"][k] = BIN_ekle(arr.astype(np.float32), "VEC3" if arr.ndim == 2 and arr.shape[1] == 3 else "VEC2", 34962)
        ind = oku(pr["indices"]).astype(np.uint32); q["indices"] = BIN_ekle(ind, "SCALAR", 34963)
        n = len(ind)
        if (q.get("extras") or {}).get("mek"): q["extras"]["mek"] = [mek_yeni, 0, n]
        prs.append(q)
    J["meshes"].append({"name": yeni_ad, "primitives": prs})
    yn = {k: json.loads(json.dumps(v)) for k, v in nd.items() if k not in ("children",)}
    yn["name"] = yeni_ad; yn["mesh"] = len(J["meshes"]) - 1
    yn["translation"] = [nd.get("translation", [0, 0, 0])[0] + dx_m] + list(nd.get("translation", [0, 0, 0])[1:])
    J["nodes"].append(yn); yi = len(J["nodes"]) - 1
    ebeveyn = [i for i, n in enumerate(J["nodes"]) if ni[0] in n.get("children", [])]
    if ebeveyn: J["nodes"][ebeveyn[0]]["children"].append(yi)
    else: J["scenes"][J.get("scene", 0)]["nodes"].append(yi)
    return yi


# ================================================================== 1 · GLB (m8kit)
g = Glb(gi)
EX = g.J["scenes"][0]["extras"]; KOD = [m["kod"] for m in EX["mekanizmalar"]]
for k in ("TOPPING/Sos", "TOPPING/Harç", "TOPPING/Kıyma", "TOPPING/Kuşbaşı", "TOPPING/Hava", "TOPPING/Soğutma", "TOPPING/Gövde"):
    assert k in KOD, "ADIM 53 DUR: ünite yok %s" % k
M_YENI = len(KOD)
EX["mekanizmalar"].append({"kod": YENI_KOD, "istasyon": "TOPPING", "ad": "Kıyma*"})
M_HAVA, M_SOG = KOD.index("TOPPING/Hava"), KOD.index("TOPPING/Soğutma")
KAYIT = dict(adim=53, ad="TOPPING yeni menü yerleşimi (menu7)", kopya=[], hazne={}, delik=[], evaporator=[], yeni=[])

# 1a · hazneler: eskiyi sil, yenisini ekle (etiket eskiden)
LOG("1a · hazneler")
H_YENI = {}
for ad, ((d, lo, hi), (nx, y0, y1, yt, x0, x1)) in HAZ.items():
    b = bul(g, d, lo, hi); kat, mek, kpk = g.etiket_b(b)
    kab, bos = hazne(nx, y0, y1, yt, x0, x1, cep=CEP_KB if ad == "kusbasi" else None)
    eski_hacim = None
    g.sil_b(b); g.ekle_dugum(d, mf_ucg(kab), kat=kat, mek=mek, kpk=kpk)
    H_YENI[ad] = (kab, bos)
    KAYIT["hazne"][ad] = dict(kutu=[round(v, 2) for v in list(kab.bounding_box())], ust=yt, ic_hacim_L=round(bos.volume() / 1e6, 3), et=ET, kose_R=KOSE_R,
                              cep=ad == "kusbasi")
    LOG("  %-8s eski %s … %s → yeni üst %.0f · iç hacim %.2f L" % (ad, lo, hi, yt, bos.volume() / 1e6))
kab, bos = hazne(*ORTA_HAZNE)
g.ekle_dugum("TOPPING_MODUL__paslanmaz", mf_ucg(kab), kat=8, mek=M_YENI, kpk=False)
H_YENI["kiyma_orta"] = (kab, bos)
KAYIT["hazne"]["kiyma_orta"] = dict(kutu=[round(v, 2) for v in list(kab.bounding_box())], ust=ORTA_HAZNE[3], ic_hacim_L=round(bos.volume() / 1e6, 3), et=ET, kose_R=KOSE_R)
LOG("  orta     yeni x %.0f–%.0f üst %.0f · iç hacim %.2f L" % (ORTA_HAZNE[4], ORTA_HAZNE[5], ORTA_HAZNE[3], bos.volume() / 1e6))

# 1b · orta UNO: sos UNO'sunun statik parçaları x −228,5 (etiket → yeni Kıyma)
LOG("1b · orta UNO kopyası (dx %.1f)" % DX_UNO)
for d, lo, hi in UNO:
    b = bul(g, d, lo, hi); n = g.kopya_b(b, (DX_UNO, 0, 0), mek=M_YENI)
    KAYIT["kopya"].append(dict(dugum=d, kaynak=[lo, hi], dx=DX_UNO, ucgen=n))
# silindir tutucu + ara plaka: cep tabanının üstüne (y 1533,9…1594,6 → 1580…1594,6), x −228,5
YA, YB, YA2 = 1533.9, 1594.6, EV_IY0
for d, lo, hi in TUTUCU:
    b = bul(g, d, lo, hi); kat, mek, kpk = g.etiket_b(b)
    P = ucg(b).copy(); P[..., 0] += DX_UNO
    yb = b["hi"][1]; P[..., 1] = YA2 + (P[..., 1] - YA) * (YB - YA2) / (YB - YA)
    g.ekle_dugum(d, P, kat=kat, mek=M_YENI, kpk=kpk)
    KAYIT["kopya"].append(dict(dugum=d, kaynak=[lo, hi], dx=DX_UNO, y_esle=[YA, YB, YA2, YB], ucgen=len(P)))
# hareketli düğümler: yeni düğüm (statik)
YD = []
for ad, yad in (("TOPPING_DONER__VALF_SOS", "TOPPING_DONER__VALF_KIYMA_ORTA"),
                ("TOPPING_MODUL__paslanmaz__PISTON_SOS", "TOPPING_MODUL__paslanmaz__PISTON_KIYMA_ORTA"),
                ("TOPPING_MODUL__pom__PISTON_SOS", "TOPPING_MODUL__pom__PISTON_KIYMA_ORTA")):
    yi = dugum_klonla(g.J, g._ekle_arr, g._oku, ad, yad, DX_UNO / 1000.0, M_YENI); YD.append(yad)
    KAYIT["yeni"].append(dict(dugum=yad, kaynak=ad, dx=DX_UNO))
LOG("  yeni düğümler: %s" % ", ".join(YD))

# 1c · ürün çıkışı: paslanmaz dirsek (rafın üstünde) + düşme hattı kopyası x −348
LOG("1c · ürün hattı")
R_B = 50.0
yol = [(2031.0, 1613.5, -235.2), (2031.0, 1613.5, -220.0)]
yol += yay((1981.0, 1613.5, -220.0), (1, 0, 0), (0, 0, 1), R_B)[1:]
R_B2 = 36.0                       # 2. büküm (aşağı): eksen 1613,5 − 36 = 1577,5 → raf üstü 1575'ten önce dik (raf deliğinden düz geçer)
yol += [(X_DUS + R_B2, 1613.5, -170.0)]
yol += yay((X_DUS + R_B2, 1613.5 - R_B2, -170.0), (0, 1, 0), (-1, 0, 0), R_B2)[1:]
yol += [(X_DUS, 1551.0, -170.0)]
P_dirsek = boru_ucgen(yol, 35.6 / 2, 35.6 / 2 - 1.8)
g.ekle_dugum("TOPPING_MODUL__paslanmaz", P_dirsek, kat=8, mek=M_YENI, kpk=False)
KAYIT["yeni"].append(dict(parca="cikis_dirsegi_paslanmaz_D35.6x1.8_2x90_R50_R36", yol=[list(map(float, q)) for q in (yol[0], yol[-1])]))
DZ_DUS = {(2239.7, 1572.0): 2.2, (2230.2, 1539.0): -0.45}     # raf contası / raf altı flanş eksenini dirseğin dik ekseni z −170'e getir
for d, lo, hi in DUS:
    b = bul(g, d, lo, hi); dz = DZ_DUS.get((lo[0], lo[1]), 0.0)
    if lo[1] == 1108.0:                       # boru Ø29,8: alt ucu 1108 → 1048 (tabla yolu, kıyma alt UNO'su gibi)
        kat, mek, kpk = g.etiket_b(b)
        P = ucg(b).copy(); P[..., 0] += DX_DUS; m = P[..., 1] < 1108.5; P[..., 1][m] = 1048.0
        g.ekle_dugum(d, P, kat=kat, mek=M_YENI, kpk=kpk); n = len(P)
    else:
        n = g.kopya_b(b, (DX_DUS, 0, dz), mek=None if d.startswith("TOPPING_GOVDE") else M_YENI)
    KAYIT["kopya"].append(dict(dugum=d, kaynak=[lo, hi], dx=DX_DUS, dz=dz, ucgen=n))

# 1d · delikler (manifold fark) — raf + taban sandviçi
LOG("1d · delikler")
bc3 = bul(g, *DUS[0]); Pc = ucg(bc3).reshape(-1, 3) + np.array([DX_DUS, 0.0, DZ_DUS[(2239.7, 1572.0)]])
CONTA_ZARF = mf.Manifold.hull_points(np.r_[np.c_[Pc[:, 0], np.full(len(Pc), 1525.0), Pc[:, 2]], np.c_[Pc[:, 0], np.full(len(Pc), 1585.0), Pc[:, 2]]].tolist())
for d, (lo, hi), cx, cz, r in DELIK:
    b = bul(g, d, lo, hi); assert b["kapali"], d
    kat, mek, kpk = g.etiket_b(b)
    kesici = silindir_y(cx, cz, r, lo[1] - 5, hi[1] + 5)
    if lo[1] == 1534.0: kesici = kesici + CONTA_ZARF                 # raf: conta dış zarfı kadar
    m0 = mf_den(ucg(b)); m1 = m0 - kesici
    assert m1.status() == mf.Error.NoError and m1.volume() < m0.volume()
    g.sil_b(b); g.ekle_dugum(d, mf_ucg(m1), kat=kat, mek=mek, kpk=kpk)
    KAYIT["delik"].append(dict(dugum=d, kutu=[lo, hi], merkez=[cx, cz], r=r, hacim_farki_mm3=round(m0.volume() - m1.volume(), 1)))
    LOG("  %-22s r %.1f · −%.0f mm³" % (d, r, m0.volume() - m1.volume()))

# 1d2 · soğuk oda arka iç sacı (z −571…−570): POM burç deliği (sos burcunda r 14,3–15,2 delik var)
BURC_C = (2259.75 + DX_UNO, 1613.5)
b = bul(g, "TOPPING_GOVDE__sac", (1496.8, 1110.5, -571.0), (2439.2, 2139.0, -570.0)); kat, mek, kpk = g.etiket_b(b)
m0 = mf_den(ucg(b)); m1 = m0 - mf.Manifold.cylinder(20.0, 15.25, 15.25, 48).translate([BURC_C[0], BURC_C[1], -580.0])
assert m1.status() == mf.Error.NoError and m1.volume() < m0.volume()
g.sil_b(b); g.ekle_dugum("TOPPING_GOVDE__sac", mf_ucg(m1), kat=kat, mek=mek, kpk=kpk)
KAYIT["delik"].append(dict(dugum="TOPPING_GOVDE__sac (arka iç sac)", merkez=list(BURC_C), r=15.25, hacim_farki_mm3=round(m0.volume() - m1.volume(), 1)))
LOG("  arka iç sac burç deliği r 15,25 · −%.0f mm³" % (m0.volume() - m1.volume()))

# 1e · evaporatör cebi
LOG("1e · evaporatör cebi")
yarik = kutu_mf((EV_X0, EV_Y0, -900.0), (EV_X1, EV_YT, -600.0))
for d, no in EVAP:
    lo, hi = EVAP_KUTU[(d, no)]
    b = bul(g, d, lo, hi); assert b["kapali"], d
    kat, mek, kpk = g.etiket_b(b)
    m0 = mf_den(ucg(b)); m1 = m0 - yarik
    assert m1.status() == mf.Error.NoError
    g.sil_b(b)
    if not m1.is_empty(): g.ekle_dugum(d, mf_ucg(m1), kat=kat, mek=mek, kpk=kpk)
    KAYIT["evaporator"].append(dict(dugum=d, kutu=[lo, hi], kesilen_mm3=round(m0.volume() - m1.volume(), 1)))
    LOG("  %-22s −%.0f mm³" % (d, m0.volume() - m1.volume()))
Z = (EV_Z0, EV_Z1)
EV_LT = 1835.0                                   # cep duvarı üstü = kaset üstü
def U(a_x, a_y, top=EV_LT, ez=0.0):
    return kutu_mf((EV_X0 + a_x, EV_Y0 + a_y, Z[0] - ez), (EV_X1 - a_x, top, Z[1] + ez))
def ICB(b_):
    return kutu_mf((EV_IX0 - b_, EV_IY0 - b_, Z[0] - 1), (EV_IX1 + b_, EV_YT + 10, Z[1] + 1))
pu = U(1, 1, EV_LT - 1.0) - ICB(1)                 # PU: yan 20 · taban 10 · üstte 1 mm sac kapak altında biter
sac_cep = (U(0, 0) - ICB(0)) - pu                  # dış + iç + üst kenar kapağı tek bükümlü sac (PU'yu her yandan örter; ön: conta, arka: gövde arka sacı)
g.ekle_dugum("TOPPING_MODUL__sac", mf_ucg(sac_cep), kat=5, mek=M_SOG, kpk=False)
g.ekle_dugum("TOPPING_MODUL__pu", mf_ucg(pu), kat=5, mek=M_SOG, kpk=False)
conta = kutu_mf((EV_X0, EV_Y0, -640.0), (EV_X1, 1835.0, -630.0)) - kutu_mf((EV_IX0, EV_IY0, -650.0), (EV_IX1, 1900.0, -620.0))
g.ekle_dugum("TOPPING_MODUL__conta", mf_ucg(conta), kat=5, mek=M_SOG, kpk=False)
KAYIT["yeni"].append(dict(parca="evaporator_cebi", dis=[EV_X0, EV_X1, EV_Y0, EV_YT], ic=[EV_IX0, EV_IX1, EV_IY0], z=list(Z),
                          duvar="1 sac + 20 PU + 1 sac", taban="1 sac + 10 PU + 1 sac", conta="z −640…−630"))
# burç kılıfı: üfleme ağzı (GOVDE sac 12/13, z −630…−571) içinde POM burcun çevresi + alt ayak (ağız tabanına)
burc = bul(g, "TOPPING_MODUL__pom", (2244.9, 1598.6, -635.0), (2274.5, 1628.4, -565.0))     # sos burcu (kopya ekX'te görünmez) + dx
Pb = ucg(burc).reshape(-1, 3) + np.array([DX_UNO, 0.0, 0.0]); bc = np.array([(Pb[:, 0].min() + Pb[:, 0].max()) / 2, (Pb[:, 1].min() + Pb[:, 1].max()) / 2])
rb = max(np.hypot(Pb[:, 0] - bc[0], Pb[:, 1] - bc[1]).max(), 0.0)
ALT = []
for lo_, hi_ in (((1807.0, 1582.0, -630.0), (2173.0, 1785.0, -571.0)), ((1808.0, 1583.0, -630.0), (2174.0, 1786.0, -571.0))):
    Pd = ucg(bul(g, "TOPPING_GOVDE__sac", lo_, hi_)).reshape(-1, 3)
    m = Pd[:, 1] < bc[1] - rb                      # ağız tabanı düz levha (köşeleri uçlarda)
    if m.any(): ALT.append(Pd[m][:, 1].max())
assert ALT, "üfleme ağzı tabanı bulunamadı"
y_taban = max(ALT)
kilif = mf.Manifold.cylinder(59.0, rb + 2.0 + 0.1, rb + 2.0 + 0.1, 48).translate([bc[0], bc[1], -630.0]) - \
    mf.Manifold.cylinder(61.0, rb + 0.1, rb + 0.1, 48).translate([bc[0], bc[1], -631.0])
ayak = kutu_mf((bc[0] - 1.0, y_taban, -625.0), (bc[0] + 1.0, bc[1] - rb - 1.0, -576.0))
g.ekle_dugum("TOPPING_MODUL__paslanmaz", mf_ucg(kilif + ayak), kat=8, mek=M_YENI, kpk=False)
KAYIT["yeni"].append(dict(parca="burc_kilifi", merkez=bc.round(2).tolist(), r_ic=round(rb + 0.1, 2), r_dis=round(rb + 2.1, 2), ayak_taban_y=round(y_taban, 2)))
LOG("  burç kılıfı: merkez %s r %.1f · ayak ağız tabanına y %.2f" % (bc.round(1), rb, y_taban))

# 1f · hava: silindir rakorları (kopya) + ada rakorları + 2 hortum Ø6
LOG("1f · hava")
for d, lo, hi in HAVA_RAKOR:
    b = bul(g, d, lo, hi); g.kopya_b(b, (DX_UNO, 0, 0))
b = bul(g, *ADA_RAKOR)
for dy, dz in ((-26.0, -18.0), (-26.0, -33.0)): g.kopya_b(b, (0, dy, dz))
XA, XB = 2256.5 + DX_UNO, 2262.5 + DX_UNO       # 2028 / 2034
# yol: kaşar motoru (x ≤ 2117,1) ile soğutma sıvı borusu (x ≥ 2130,8, y 1320–1383) arasından x 2124'te çıkar; emiş borusunun (x 2140–2171,
# z −715…−684,5) ve sıvı borusunun (z −663…−657) arasından (z −678 / −668) geçer; x 2302'de hava kanalının arkasında (z −688 / −703) 1850'ye çıkar
HA = [(2008.0, 1276.0, -688.0), (2124.0, 1276.0, -688.0), (2124.0, 1335.0, -688.0), (2124.0, 1335.0, -678.0), (2285.0, 1335.0, -678.0),
      (2285.0, 1335.0, -688.0), (2302.0, 1335.0, -688.0), (2302.0, 1850.0, -688.0), (XA, 1850.0, -688.0), (XA, 1640.5, -688.0)]
HB = [(2008.0, 1276.0, -703.0), (2124.0, 1276.0, -703.0), (2124.0, 1347.0, -703.0), (2124.0, 1347.0, -668.0), (2285.0, 1347.0, -668.0),
      (2285.0, 1347.0, -703.0), (2302.0, 1347.0, -703.0), (2302.0, 1850.0, -703.0), (XB, 1850.0, -703.0), (XB, 1700.0, -703.0),
      (XB, 1700.0, -795.0), (XB, 1640.5, -795.0)]
for H in (HA, HB): g.ekle_dugum("TOPPING_MODUL__hava_ana", tup(H, 3.0, 12), kat=4, mek=M_HAVA, kpk=False)
KAYIT["yeni"].append(dict(parca="hava_hortumu_D6_x2", A=HA, B=HB))

tmp = go + ".d53.glb"; g.kaydet(tmp); del g
LOG("1 bitti · %.0f sn" % (time.time() - t0))

# ================================================================== 2 · ünite adları / sırası (BIN değişmez)
raw = open(tmp, "rb").read(); jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
EX = J["scenes"][0]["extras"]; KOD2 = [m["kod"] for m in EX["mekanizmalar"]]
assert KOD2[-1] == YENI_KOD and KOD2[:-1] == KOD
YENI = {"TOPPING/Harç": "TOPPING/Lahmacun harcı", "TOPPING/Sos": "TOPPING/Patates", "TOPPING/Kıyma": "TOPPING/Tavuk", YENI_KOD: "TOPPING/Kıyma"}
SIRA = ["TOPPING/Harç", YENI_KOD, "TOPPING/Sos", "TOPPING/Kıyma", "TOPPING/Kuşbaşı"]
i9 = KOD.index("TOPPING/Sos")
yeni_sira = [k for k in KOD2[:i9]] + SIRA + [k for k in KOD2[i9:-1] if k not in SIRA]
assert sorted(yeni_sira) == sorted(KOD2), "sıra"
ESLE = np.array([yeni_sira.index(k) for k in KOD2], np.int64)
EM = {m["kod"]: m for m in EX["mekanizmalar"]}
liste = []
for k in yeni_sira:
    m = dict(EM[k]); kk = YENI.get(k, k); m["kod"] = kk; m["ad"] = kk.split("/", 1)[1]; liste.append(m)
EX["mekanizmalar"] = liste
EX["gruplama"] = EX.get("gruplama", "") + " · v4 4 Eki 2026 (menu7): pide + lahmacun menüsü — TOPPING/Lahmacun harcı (eski Harç) · Kıyma (YENİ orta UNO) · Patates (eski Sos) · Tavuk (eski alt Kıyma) · Kuşbaşı · Kaşar · Sucuk; Sos kalktı"
say0 = np.zeros(len(KOD2), np.int64); say1 = np.zeros(len(KOD2), np.int64); islenen = set()
for nd in J["nodes"]:
    if "mesh" not in nd: continue
    for pi, pr in enumerate(J["meshes"][nd["mesh"]]["primitives"]):
        ex = pr.get("extras") or {}; L = ex.get("mek")
        if not L or (nd["mesh"], pi) in islenen: continue
        islenen.add((nd["mesh"], pi))
        L2 = []
        for k in range(0, len(L) - 2, 3):
            say0[L[k]] += L[k + 2] // 3; L2 += [int(ESLE[L[k]]), L[k + 1], L[k + 2]]; say1[ESLE[L[k]]] += L[k + 2] // 3
        ex["mek"] = L2
for i in range(len(KOD2)): assert say0[i] == say1[ESLE[i]], KOD2[i]
js = json.dumps(J, ensure_ascii=False, separators=(",", ":")).encode("utf-8"); js += b" " * ((4 - len(js) % 4) % 4)
binc = raw[bo:]
tmp2 = go + ".d53b.glb"
open(tmp2, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + len(binc)) + struct.pack("<II", len(js), 0x4E4F534A) + js + binc)
os.remove(tmp)
r = subprocess.run([sys.executable, os.path.join(HERE, "50_sikilastir.py"), tmp2, go]); assert r.returncode == 0
os.remove(tmp2)
KAYIT["mekanizmalar"] = [m["kod"] for m in liste]
KAYIT["ucgen_mek"] = {liste[i]["kod"]: int(say1[i]) for i in range(len(liste))}
KAYIT["log"] = SE.LOG
json.dump(KAYIT, open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=float)
LOG("ADIM 53 bitti · ünite %d → %d · %s · %.0f sn" % (len(KOD), len(liste), go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
