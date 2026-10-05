# -*- coding: utf-8 -*-
"""FIRIN ÜSTÜ DOLAP (F üst kabin, y 1305–1862 · x 2500–4000) — Kemal çizimi images/86.webp (2 Eki): taban + çerçeve + yalıtım + orta bölme.
Taban hat3_v8u.glb → hat3_v8v.glb. Montaj / elektrik ÇALIŞTIRILMAZ: GLB düğüm geometrisi yerinde değişir.

KURGU
  1 ÇERÇEVE: altta 3 kare profil 304 30 × 30 × 2 (mevcut ön üst kayıtla AYNI kesit) — ÖN (z 27–57, eski ön alt kayıtın yerinde ve aynı kesitte;
    yalnız 8,5 yukarıda), ORTA (bölme duvarının tam altında, z −455,75…−425,75), ARKA (sağ alt köşe, z −828,5…−798,5, arka saca dayalı) ·
    y 1316,5–1346,5 · yan saclar arası x 2501,5–3998,5 (yan saclara kaynaklı; yük yan saclardan kaideye). Eski ön alt kayıt + 3 ara takozu kalkar.
  2 TABAN: TEK DÜZ LEVHA 304 1,5 · y 1346,5–1348 · x 2501,5–3998,5 · z −828,5…+57 (duvardan duvara; iki bölmede aynı kot 1348 = eski raf üstü,
    böylece kompresör / yağ tankı / pizza yığını YERİNDE kalır, hortum ve kablo bağları bozulmaz) · 3 profilin üstüne oturur.
    Kalkan: ısı kalkanlı raf (F_UST_RAF: 0,8 kalkan + 4 mm raf + 20 takoz) · davlumbaz kutusunun tabanı / yanları / arkası / üstü + 2 askı köşebendi.
  3 ISI: taban levhasının ALTINDA 20 mm taş yünü levha (A1, ≥ 100 kg/m³) · iki gözde, profiller ve yan saclar arasında (y 1326,5–1346,5) ·
    altı 0,5 mm 304 kılıfla kapalı (baca yalıtımıyla aynı kurgu; lif açıkta kalmaz) · dışarıdan görünmez. Gerekçe raporda.
  4 ORTA BÖLME: davlumbaz ön duvarı TEK PARÇA 304 1,5 · y 1348 → 1860,5 (taban üstünden tavan altına) · z −441,5…−440 · orta profilin üstünde ·
    9 emiş yarığı 160 × 10 (eski yerinde) · içinden geçen boru / hortumlara delik (otomatik, +1 mm).
    Davlumbaz içi: fan + 2 fan konsolu ve kanal konsolları +31,5 (taban 1348'e) · filtre çerçevesi + filtre +13 · iç kanal + atış kanalı TEK KANAL
    300 × 200 · 1361,5 → 1860,5.
  5 HAVA BORUSU: boru zaten eksenlere paralel (ölçüldü; "eğik" görünen = TOPPING kolunun x boyunca uzaklaşan perspektifi). KOPUK UÇ: iki kol F yan
    saclarından DELİKSİZ geçiyordu (sol delik + conta z −432'de boştaydı, boru −740'ta · sağ delik −780, boru −770) → delikler + contalar boru eksenine.
  Elektrik: davlumbaz fanı kablo rakoru +31,5 (eski taban deliği yerine yeni taban deliğinde, aynı göreli konum) · arka saçtaki kablo kelepçesi
    +20,5 (arka profil + rakorla çakışıyordu) · F kapak menteşe plakaları +8,5 (yeni ön profilin yüzüne).
Kullanım: python f_kabin_yeni.py giris.glb cikis.glb"""
import json, struct, sys, os
import numpy as np
import cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tg")); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "ug"))
import bilesen
from u_ortak import ornekle

TD = {5126: np.float32, 5125: np.uint32, 5123: np.uint16}
X0, X1 = 2501.5, 3998.5
ZAI = -828.5
YP0, YP1 = 1316.5, 1346.5                  # alt profiller
YT0, YT1 = 1346.5, 1348.0                  # taban levhası
YAL = 20.0                                 # taş yünü
YTAV = 1860.5                              # kabin tavan sacının altı
ZW0, ZW1 = -441.5, -440.0                  # bölme duvarı
PROF = {"f_ust_alt_profil_on": (27.0, 57.0), "f_ust_alt_profil_orta": (-455.75, -425.75), "f_ust_alt_profil_arka": (ZAI, ZAI + 30.0)}
KANAL = (2952.0, 3248.0, -718.0, -522.0)          # eski iç kanalın kesiti (fana x 3248'de dayanır)
RAKOR = (3460.0, -780.15, 8.25)            # davlumbaz fanı kablo rakoru ekseni (x, z) + delik yarıçapı (eski taban deliğiyle aynı)
DY_DAV = YT1 - 1316.5                      # +31,5 (eski davlumbaz tabanı üstü 1316,5 → 1348)


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def boru_x(x0, x1, y0, y1, z0, z1, et=2.0):
    return kutu(x0, x1, y0, y1, z0, z1).cut(kutu(x0 - 1, x1 + 1, y0 + et, y1 - et, z0 + et, z1 - et))


def sily(x, z, r, y0, y1):
    return cq.Solid.makeCylinder(r, y1 - y0, cq.Vector(x, y0, z), cq.Vector(0, 1, 0))


def silz(x, y, r, z0, z1):
    return cq.Solid.makeCylinder(r, z1 - z0, cq.Vector(x, y, z0), cq.Vector(0, 0, 1))


raw = open(sys.argv[1], "rb").read()
jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])
NI = {n.get("name"): i for i, n in enumerate(J["nodes"])}


def oku(i):
    a = J["accessors"][i]; v = J["bufferViews"][a["bufferView"]]; n = {"SCALAR": 1, "VEC3": 3}[a["type"]]; dt = TD[a["componentType"]]
    off = v.get("byteOffset", 0) + a.get("byteOffset", 0)
    r = np.frombuffer(bytes(BIN[off:off + a["count"] * n * np.dtype(dt).itemsize]), dt).copy()
    return r.reshape(-1, n) if n > 1 else r


def ekle_buf(arr, tip, hedef):
    global BIN
    while len(BIN) % 4: BIN += b"\0"
    off = len(BIN); BIN += arr.tobytes()
    J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
    a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
    if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
    J["accessors"].append(a); return len(J["accessors"]) - 1


class Dugum:
    def __init__(self, ad):
        self.ad = ad; nd = J["nodes"][NI[ad]]
        assert not any(k in nd for k in ("translation", "rotation", "scale", "matrix")), ad
        self.pr = J["meshes"][nd["mesh"]]["primitives"][0]
        self.X = oku(self.pr["attributes"]["POSITION"]).astype(np.float64) * 1000.0
        self.N = oku(self.pr["attributes"]["NORMAL"]).astype(np.float32)
        self.T = oku(self.pr["indices"]).astype(np.int64).reshape(-1, 3)
        self.ek = []                                                      # yeni katılar

    def ok(self):
        return (self.T[:, 0] != self.T[:, 1]) | (self.T[:, 1] != self.T[:, 2])

    def sec(self, kosul):
        """bağlı bileşenlerden kutusu kosul(mn, mx) olanların üçgen maskesi"""
        ok = self.ok(); idx = np.where(ok)[0]
        P = np.round(self.X, 2); u, inv = np.unique(P, axis=0, return_inverse=True); inv = inv.reshape(-1)
        from scipy.sparse import coo_matrix
        from scipy.sparse.csgraph import connected_components
        Ti = inv[self.T[idx]]
        g = coo_matrix((np.ones(2 * len(idx)), (np.concatenate([Ti[:, 0], Ti[:, 1]]), np.concatenate([Ti[:, 1], Ti[:, 2]]))), shape=(len(u), len(u)))
        _, lab = connected_components(g, directed=False)
        tl = lab[Ti[:, 0]]; m = np.zeros(len(self.T), bool)
        for c in np.unique(tl):
            tt = idx[tl == c]; Q = self.X[self.T[tt]].reshape(-1, 3)
            if kosul(Q.min(0), Q.max(0)): m[tt] = True
        return m

    def sil(self, m):
        self.T[m, 1] = self.T[m, 0]; self.T[m, 2] = self.T[m, 0]; return int(m.sum())

    def tasi(self, m, dv):
        v = np.unique(self.T[m].ravel())
        diger = np.unique(self.T[(~m) & self.ok()].ravel())
        assert not len(np.intersect1d(v, diger)), (self.ad, "paylaşılan köşe")
        self.X[v] += np.array(dv); return len(v)

    def yaz(self):
        Xa = [(self.X / 1000.0).astype(np.float32)]; Na = [self.N]; Ia = [self.T.reshape(-1).astype(np.uint32)]
        say = len(self.X)
        for s in self.ek:
            Xf, Nf = ag([s]); Xa.append((Xf / 1000.0).astype(np.float32)); Na.append(Nf); Ia.append(np.arange(say, say + len(Xf), dtype=np.uint32)); say += len(Xf)
        X = np.vstack(Xa); N = np.vstack(Na); I = np.concatenate(Ia)
        self.pr["attributes"] = {"POSITION": ekle_buf(X, "VEC3", 34962), "NORMAL": ekle_buf(N, "VEC3", 34962)}
        self.pr["indices"] = ekle_buf(I, "SCALAR", 34963)
        ex = self.pr.setdefault("extras", {})
        for k in ("kat", "mek"):
            if k in ex and self.ek:
                assert len(ex[k]) == 3, (self.ad, k)
                ex[k] = [ex[k][0], 0, len(I)]


def ag(solidler):
    P, I = [], []
    for s in solidler:
        for f in s.Faces():
            v, t = f.tessellate(0.1, 0.2)
            o = sum(len(p) for p in P)
            P.append(np.array([[q.x, q.y, q.z] for q in v], float))
            I.append(np.array(t, np.int64) + o if len(t) else np.zeros((0, 3), np.int64))
    X = np.vstack(P); T = np.vstack(I)
    Xf = X[T.reshape(-1)]; n = np.cross(Xf[1::3] - Xf[0::3], Xf[2::3] - Xf[0::3])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return Xf, np.repeat(n, 3, axis=0).astype(np.float32)


def icinde(mn, mx, k, e=0.6):
    return (mn >= np.array(k[0::2]) - e).all() and (mx <= np.array(k[1::2]) + e).all()


R = {}
G = {n: Dugum(n) for n in ["F_UST_KABIN__sac", "F_UST_KABIN__paslanmaz", "F_UST_RAF__sac", "F_UST_RAF__paslanmaz", "F_DAVLUMBAZ__sac", "F_DAVLUMBAZ__paslanmaz",
                           "F_DAVLUMBAZ__celik", "F_DAVLUMBAZ__koyu", "ELK_ISTASYON__rakor", "ELK_ISTASYON__celik", "F_UST_KAPAK__celik", "F_UST_KABIN__conta"]}
# ---------------- SİL ----------------
R["sil F_UST_RAF (kalkan + raf + takozlar)"] = G["F_UST_RAF__sac"].sil(G["F_UST_RAF__sac"].ok()) + G["F_UST_RAF__paslanmaz"].sil(G["F_UST_RAF__paslanmaz"].ok())
g = G["F_UST_KABIN__paslanmaz"]
R["sil eski ön alt kayıt + 3 ara takoz"] = g.sil(g.sec(lambda mn, mx: mx[1] <= 1338.6 and mn[2] >= 26.5))
g = G["F_DAVLUMBAZ__sac"]
R["sil davlumbaz kutusu + iç kanal + atış kanalı (tek kanal + bölme duvarı olarak yeniden)"] = g.sil(g.ok())
g = G["F_DAVLUMBAZ__paslanmaz"]
R["sil davlumbaz askı köşebentleri"] = g.sil(g.sec(lambda mn, mx: mx[1] <= 1315.6 and mn[1] <= 1276))
# ---------------- TAŞI ----------------
R["taşı fan +31,5"] = G["F_DAVLUMBAZ__celik"].tasi(G["F_DAVLUMBAZ__celik"].ok(), (0, DY_DAV, 0))
g = G["F_DAVLUMBAZ__paslanmaz"]
R["taşı fan + kanal konsolları +31,5"] = g.tasi(g.sec(lambda mn, mx: mn[1] >= 1316.0 and mx[1] <= 1330.6), (0, DY_DAV, 0))
R["taşı filtre çerçevesi +13"] = g.tasi(g.sec(lambda mn, mx: icinde(mn, mx, (3385, 3955, 1335, 1765, -496.5, -441.5))), (0, YT1 - 1335.0, 0))
R["taşı filtre +13"] = G["F_DAVLUMBAZ__koyu"].tasi(G["F_DAVLUMBAZ__koyu"].ok(), (0, YT1 - 1335.0, 0))
g = G["ELK_ISTASYON__rakor"]
R["taşı fan kablosu rakoru +31,5"] = g.tasi(g.sec(lambda mn, mx: icinde(mn, mx, (3448.6, 3471.4, 1303.0, 1324.5, -791.5, -768.8))), (0, DY_DAV, 0))
g = G["ELK_ISTASYON__celik"]
R["taşı arka kablo kelepçesi +30,5"] = g.tasi(g.sec(lambda mn, mx: icinde(mn, mx, (3452, 3468, 1336.5, 1348.5, -828.5, -775))), (0, 30.5, 0))
R["taşı F kapak menteşe plakaları +8,5"] = G["F_UST_KAPAK__celik"].tasi(G["F_UST_KAPAK__celik"].ok(), (0, 8.5, 0))
# yan sac hava borusu delikleri boru eksenine: sol (TOPPING kolu) z −432 → −740 · sağ (K kolu) z −780 → −770 (contalarıyla)
def delik_tasi(g, xs, zr, dz):
    X = g.X; m = np.zeros(len(X), bool)
    for xv in xs: m |= np.abs(X[:, 0] - xv) < 0.01
    m &= (X[:, 1] > 1795) & (X[:, 1] < 1823) & (X[:, 2] > zr[0]) & (X[:, 2] < zr[1])
    v = np.where(m)[0]; X[v, 2] += dz; return len(v)
def alan(g, xs):
    ok = g.ok(); P = g.X[g.T[ok]]; c = P.mean(1); m = np.zeros(len(P), bool)
    for xv in xs: m |= np.abs(c[:, 0] - xv) < 0.01
    n = np.cross(P[m, 1] - P[m, 0], P[m, 2] - P[m, 0]); return round(float(np.abs(n[:, 0]).sum() / 2), 1), int((np.sign(n[:, 0]) > 0).sum())
for xs, zr, dz in (((2500.0, 2501.5), (-441.0, -423.0), -308.0), ((3998.5, 4000.0), (-789.0, -771.0), 10.0)):
    a0 = alan(G["F_UST_KABIN__sac"], xs)
    R["yan sac boru deliği x %.0f kaydır %+.0f (köşe)" % (xs[0], dz)] = delik_tasi(G["F_UST_KABIN__sac"], xs, zr, dz)
    a1 = alan(G["F_UST_KABIN__sac"], xs); assert a0 == a1, ("yüz alanı / yönü bozuldu", a0, a1)
    R["   yan yüz alanı + yön korundu"] = a1
    gc = G["F_UST_KABIN__conta"]
    if dz > 0:                                             # sağ: K'nın geçiş rakoru (K_ELEKTRIK, Ø13,8) yan sacdan kendisi geçer → conta gereksiz, rakorla çakışıyordu
        R["   sağ conta kalktı (geçiş rakoru var)"] = gc.sil(gc.sec(lambda mn, mx, xs=xs, zr=zr: mn[0] >= xs[0] - 2.6 and mx[0] <= xs[1] + 2.6 and mn[2] > zr[0] - 3 and mx[2] < zr[1] + 3)); continue
    R["   conta kaydır %+.0f" % dz] = gc.tasi(gc.sec(lambda mn, mx, xs=xs, zr=zr: mn[0] >= xs[0] - 2.6 and mx[0] <= xs[1] + 2.6 and mn[2] > zr[0] - 3 and mx[2] < zr[1] + 3), (0, 0, dz))
# ön orta dikme (tavan kirişiyle tek parça) eski kayıt üstünden (1338) yeni ön profil üstüne (1346,5)
g = G["F_UST_KABIN__paslanmaz"]; m = g.sec(lambda mn, mx: icinde(mn, mx, (3326, 3356, 1338, 1860.5, -827, 57)))
v = np.unique(g.T[m].ravel()); vv = v[np.abs(g.X[v, 1] - 1338.0) < 0.02]; g.X[vv, 1] = YT1; R["ön orta dikme alt ucu 1338 → 1348 (taban üstü, köşe)"] = len(vv)

# ---------------- YENİ KATILAR ----------------
YENI = {}
FLC = [kutu(X0 - 1, X0 + 15.0, YP0 - 1, YT1 + 1, ZAI - 1, ZAI + 1.5), kutu(X1 - 15.0, X1 + 1, YP0 - 1, YT1 + 1, ZAI - 1, ZAI + 1.5)]   # yan sac arka bükümleri (15 × 1,5) çentiği
for ad, (z0, z1) in PROF.items():
    pr_ = boru_x(X0, X1, YP0, YP1, z0, z1)
    if z0 < ZAI + 1.6: pr_ = pr_.cut(FLC[0]).cut(FLC[1])
    YENI[ad] = ("F_UST_KABIN__paslanmaz", pr_)
taban = kutu(X0, X1, YT0, YT1, ZAI, 57.0).cut(sily(RAKOR[0], RAKOR[1], RAKOR[2], YT0 - 1, YT1 + 1)).cut(FLC[0]).cut(FLC[1])
YENI["f_ust_taban_levhasi"] = ("F_UST_KABIN__sac", taban)
ZC = [(PROF["f_ust_alt_profil_orta"][1], PROF["f_ust_alt_profil_on"][0]), (PROF["f_ust_alt_profil_arka"][1], PROF["f_ust_alt_profil_orta"][0])]
for i, (z0, z1) in enumerate(ZC):
    y = kutu(X0, X1, YP1 - YAL, YP1, z0, z1)
    if z0 < RAKOR[1] < z1: y = y.cut(sily(RAKOR[0], RAKOR[1], 12.7, YP1 - YAL - 1, YP1 + 1))     # rakor gövdesi + somunu (Ø 22,8) için
    YENI["f_ust_taban_yalitimi_%s" % ("on" if i == 0 else "arka")] = ("F_UST_KABIN__yalitim", y)
    k = kutu(X0, X1, YP1 - YAL - 0.5, YP1 - YAL, z0, z1)                                          # 0,5 mm 304 alt kılıf (taş yünü lifi açıkta kalmaz)
    if z0 < RAKOR[1] < z1: k = k.cut(sily(RAKOR[0], RAKOR[1], 12.7, YP1 - YAL - 2, YP1 - YAL + 1))
    YENI["f_ust_taban_yalitim_kilifi_%s" % ("on" if i == 0 else "arka")] = ("F_UST_KABIN__sac", k)
    if z0 < RAKOR[1] < z1:                                                                       # rakor kovanı 304 Ø25,4 × 1 (kılıf → taban levhası): yalıtım rakora açılmaz
        YENI["f_ust_taban_rakor_kovani"] = ("F_UST_KABIN__sac", sily(RAKOR[0], RAKOR[1], 12.7, YP1 - YAL - 0.5, YP1).cut(sily(RAKOR[0], RAKOR[1], 11.7, YP1 - YAL - 1.5, YP1 + 1)))
# bölme duvarı: emiş yarıkları (eski yerinde) + hava borusu deliği Ø12 (boru Ø9,8) + tavan kirişi (30 × 30, x 3326–3356) çentiği +
# üst köşelerde tavan sacının 20 mm yan bükümü çentiği (1,5 × 20) → duvar yan saclara, tavana ve kirişe tam oturur
duvar = kutu(X0, X1, YT1, YTAV, ZW0, ZW1)
for yr in (1520.0, 1620.0, 1720.0):
    for xa in (3390.0, 3590.0, 3790.0):
        duvar = duvar.cut(kutu(xa, xa + 160.0, yr, yr + 10.0, ZW0 - 1, ZW1 + 1))
duvar = duvar.cut(silz(3548.9, 1809.0, 6.0, ZW0 - 1, ZW1 + 1))
duvar = duvar.cut(kutu(3326.0, 3356.0, 1830.5, YTAV + 1, ZW0 - 1, ZW1 + 1))
duvar = duvar.cut(kutu(X0 - 1, 2503.0, 1840.5, YTAV + 1, ZW0 - 1, ZW1 + 1)).cut(kutu(3997.0, X1 + 1, 1840.5, YTAV + 1, ZW0 - 1, ZW1 + 1))
GECIS = ["hava borusu Ø12 (3548,9 · 1809)", "tavan kirişi çentiği 30 × 30", "tavan yan bükümü çentikleri 1,5 × 20"]
YENI["f_davlumbaz_bolme_duvari"] = ("F_DAVLUMBAZ__sac", duvar)
k0, k1, k2, k3 = KANAL; ykb = 1330.0 + DY_DAV
YENI["f_davlumbaz_atis_kanali"] = ("F_DAVLUMBAZ__sac", kutu(k0, k1, ykb, YTAV, k2, k3).cut(kutu(k0 + 1.5, k1 - 1.5, ykb - 1, YTAV + 1, k2 + 1.5, k3 - 1.5)))

for ad, (nd, s) in YENI.items():
    if nd in G: G[nd].ek.append(s)
for g in G.values(): g.yaz()
# yalıtım: yeni düğüm (F_UST_KABIN birimi · kategori / mekanizma F_UST_KABIN__sac ile aynı)
yal = [s for ad, (nd, s) in YENI.items() if nd == "F_UST_KABIN__yalitim"]
Xf, Nf = ag(yal)
ref = J["meshes"][J["nodes"][NI["F_UST_KABIN__sac"]]["mesh"]]["primitives"][0]["extras"]
mat = dict(J["materials"][J["meshes"][J["nodes"][NI["U_F_BACA__yalitim_gorunur"]]["mesh"]]["primitives"][0]["material"]]); mat["name"] = "MU_F_UST_KABIN__yalitim"
J["materials"].append(mat)
pr = {"attributes": {"POSITION": ekle_buf((Xf / 1000.0).astype(np.float32), "VEC3", 34962), "NORMAL": ekle_buf(Nf, "VEC3", 34962)},
      "indices": ekle_buf(np.arange(len(Xf), dtype=np.uint32), "SCALAR", 34963), "material": len(J["materials"]) - 1,
      "extras": {"kat": [ref["kat"][0], 0, len(Xf)], "mek": [ref["mek"][0], 0, len(Xf)], "kpk": []}}
J["meshes"].append({"name": "F_UST_KABIN__yalitim", "primitives": [pr]})
J["nodes"].append({"name": "F_UST_KABIN__yalitim", "mesh": len(J["meshes"]) - 1})
J["scenes"][0]["nodes"].append(len(J["nodes"]) - 1)

J["buffers"][0]["byteLength"] = len(BIN)
jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
while len(BIN) % 4: BIN += b"\0"
open(sys.argv[2], "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
                              + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
for k, v in R.items(): print("  %-70s %s" % (k, v))
print("  bölme duvarı geçişleri:", GECIS)
for ad, (nd, s) in YENI.items():
    b = s.BoundingBox(); print("  + %-32s %-26s x %.1f–%.1f y %.1f–%.1f z %.1f…%.1f" % (ad, nd, b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))
cq.Compound.makeCompound([s for _a, (_n, s) in YENI.items()]).exportBrep(os.path.join(HERE, "ug", "f_yeni_katilar.brep"))
json.dump([[a, n] for a, (n, s) in YENI.items()], open(os.path.join(HERE, "ug", "f_yeni_dizin.json"), "w"), ensure_ascii=False)
print("yazıldı", sys.argv[2])
sys.stdout.flush(); os._exit(0)
