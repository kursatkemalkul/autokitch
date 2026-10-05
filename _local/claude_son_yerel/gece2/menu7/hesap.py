# -*- coding: utf-8 -*-
"""menu7 hesap: hazne hacimleri (loft integrali), 2 gunluk ihtiyac, sekil karsilastirmasi, evaporator tablosu. SALT OKUMA (modele dokunmaz)."""
import numpy as np, json, math
from scipy.spatial import ConvexHull

N = 720
def daire(cx, cz, d):
    t = np.linspace(0, 2 * np.pi, N, endpoint=False); return np.c_[cx + d / 2 * np.cos(t), cz + d / 2 * np.sin(t)]
def ray_poly(poly, cx, cz):
    """poligonu merkezden aci ile yeniden ornekle (yildiz-sekil varsayimi)"""
    t = np.linspace(0, 2 * np.pi, N, endpoint=False); out = []
    P = np.asarray(poly); n = len(P)
    for a in t:
        d = np.array([np.cos(a), np.sin(a)]); best = None
        for i in range(n):
            p, q = P[i], P[(i + 1) % n]; e = q - p
            M = np.array([[d[0], -e[0]], [d[1], -e[1]]])
            if abs(np.linalg.det(M)) < 1e-12: continue
            s, u = np.linalg.solve(M, p - np.array([cx, cz]))
            if s > 0 and -1e-9 <= u <= 1 + 1e-9: best = s if best is None else min(best, s)
        out.append([cx + best * d[0], cz + best * d[1]])
    return np.array(out)
def rect(x0, x1, z0, z1, r=0.0, k=24):
    if r <= 0: return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]
    P = []
    for (cx, cz, a0) in [(x1 - r, z0 + r, -90), (x1 - r, z1 - r, 0), (x0 + r, z1 - r, 90), (x0 + r, z0 + r, 180)]:
        for a in np.linspace(a0, a0 + 90, k): P.append((cx + r * math.cos(math.radians(a)), cz + r * math.sin(math.radians(a))))
    return P
def alan(P):
    x, z = P[:, 0], P[:, 1]; return 0.5 * abs(np.dot(x, np.roll(z, -1)) - np.dot(z, np.roll(x, -1)))
def loft_hacim(A, B, h, n=60):
    """A alt kesit, B ust kesit (ayni acida eslenmis noktalar), duz cizgili yuzey; Simpson"""
    ts = np.linspace(0, 1, 2 * n + 1); ar = np.array([alan(A + (B - A) * t) for t in ts])
    w = np.ones_like(ts); w[1:-1:2] = 4; w[2:-1:2] = 2
    return h / (6 * n) * np.dot(w, ar)
NECK_D, NECK_Z = 64.0, -387.0
Z0, Z1 = -560.0, -120.0
def hazne(xc, x0, x1, h_huni, h_kutu, top=None, neck_x=None):
    nx = xc if neck_x is None else neck_x
    A = daire(nx, NECK_Z, NECK_D)
    top = rect(x0, x1, Z0, Z1) if top is None else top
    B = ray_poly(top, nx, NECK_Z)
    Vh = loft_hacim(A, B, h_huni); Vk = alan(B) * h_kutu
    return (Vh + Vk) / 1e6, Vh / 1e6, Vk / 1e6
def aci(dx, h): return math.degrees(math.atan2(abs(dx), h))   # duseyden
def vadi(t1, t2): return math.degrees(math.atan(math.sqrt(math.tan(math.radians(t1)) ** 2 + math.tan(math.radians(t2)) ** 2)))

R = {}
# ---- 1 · MEVCUT HAZNELER (v9t olculeri)
R["mevcut"] = {
    "alt1_190 (kiyma yeri)": hazne(1596, 1501, 1691, 180, 35),
    "alt2_190 (kusbasi yeri)": hazne(1848, 1753, 1943, 180, 35),
    "ust_sol_380 (harc)": hazne(1722, 1532, 1912, 180, 212),
    "ust_sag_220 (sos yeri)": hazne(2259.5, 2149.5, 2369.5, 180, 105),
}
# kontrol: convex hull ile (mesh tepe noktalari yerine geometrik)
# ---- 2 · ONERILENLER
C3 = 2031.0
R["oneri"] = {
    "alt2_EKSANTRIK_dik_sag (sag kenar 1879)": hazne(1848, 1753, 1879.1, 180, 35),
    "alt2_ON_SAG_CEP (sadece y>1410, z>-201 x>1879 kesik)": None,
    "ust_orta_190 (x 1936-2126)": hazne(C3, C3 - 95, C3 + 95, 180, 212),
    "ust_orta_200 (x 1931-2131)": hazne(C3, C3 - 100, C3 + 100, 180, 212),
    "ust_orta_210 (x 1926-2136)": hazne(C3, C3 - 105, C3 + 105, 180, 212),
    "ust_orta_217 (10 mm pay)": hazne(C3, 1922, 2139.5, 180, 212),
    "ust_sag_220_YUKSELTILMIS (ust 2099)": hazne(2259.5, 2149.5, 2369.5, 180, 212),
}
# on-sag cep: alt2 hacminden cep hacmi dus (cep: x 1879-1943, z -201..-120, y 1410..1499; hunide kesitin icinde kalan kisim)
def cep_hacmi():
    v = 0.0; ys = np.linspace(1410, 1499, 90); dy = ys[1] - ys[0]
    for y in ys:
        if y >= 1464: xr, zf = 1943.0, -120.0
        else:
            t = (y - 1284) / 180.0; xr = 1879.1 + (1943 - 1879.1) * t; zf = -355 + (235) * t
        w = max(0.0, xr - 1879.1); d = max(0.0, zf - (-201.0)); v += w * d * dy
    return v / 1e6
full = R["mevcut"]["alt2_190 (kusbasi yeri)"][0]; cv = cep_hacmi()
R["oneri"]["alt2_ON_SAG_CEP (sadece y>1410, z>-201 x>1879 kesik)"] = (full - cv, None, None)

# ---- 3 · SEKIL KARSILASTIRMASI (ayni zarf: genislik w x derinlik 440 x huni 180 + kutu hk)
def sekil(w, hk, xc=0.0):
    x0, x1 = xc - w / 2, xc + w / 2
    out = {}
    out["A kare-yuvarlak gecis (mevcut, keskin kose)"] = hazne(xc, x0, x1, 180, hk)[0]
    out["A' ayni, kose R25 (hijyen)"] = hazne(xc, x0, x1, 180, hk, top=rect(x0, x1, Z0, Z1, 25))[0]
    out["B yuvarlak konik (O = dar kenar)"] = None
    # konik: ust daire O=min(w,440) merkez (xc, -340); boyun O64 (xc,-387)
    d = min(w, 440.0); A = daire(xc, NECK_Z, NECK_D); B = daire(xc, -340.0, d)
    out["B yuvarlak konik (O = dar kenar)"] = (loft_hacim(A, B, 180) + alan(B) * hk) / 1e6
    out["C oval (stadyum, uclar yarim daire)"] = hazne(xc, x0, x1, 180, hk, top=rect(x0, x1, Z0, Z1, w / 2 - 0.01))[0]
    out["D eksantrik (bir kenar dik)"] = hazne(xc, x0, xc + 32, 180, hk)[0] if True else None
    return out
R["sekil_190x440_h215"] = sekil(190, 35)
R["sekil_200x440_h392"] = sekil(200, 212)
R["sekil_380x440_h392"] = sekil(380, 212)

# ---- 4 · DUVAR ACILARI (duseyden) mevcut
def acilar(w):
    sx = aci(w / 2 - 32, 180); on = aci(-120 - (-355.0), 180); ark = aci(-560 - (-418.7), 180)
    return dict(yan=round(sx, 1), on=round(on, 1), arka=round(ark, 1), vadi_on=round(vadi(sx, on), 1), vadi_arka=round(vadi(sx, ark), 1))
R["acilar"] = {"190": acilar(190), "200": acilar(200), "220": acilar(220), "380": acilar(380),
               "eksantrik_sol_190": dict(sol=round(aci(1816.9 - 1753, 180), 1), sag=0.0)}

# ---- 5 · 2 GUNLUK IHTIYAC
URUN = {  # gram/adet, yogunluk g/ml, kaynak
    "harc":    dict(g=110, rho=110 / 105, k="K hesap_v2 · 110 g ≈ 105 ml"),
    "patates": dict(g=150, rho=1.05, k="V · doz + yogunluk pilotta tartilacak"),
    "kiyma":   dict(g=160, rho=160 / 152, k="K hesap_v2"),
    "tavuk":   dict(g=145, rho=145 / 170, k="V · kusbasi ile ayni alindi"),
    "kusbasi": dict(g=145, rho=145 / 170, k="K hesap_v2"),
}
ADET = dict(lahmacun=200, patatesli=20, tavuklu=20, kiymali=10, kusbasili=10, kasarli=10, sucuklu=10)   # V · 80 pide dagilimi
gun = {"harc": ADET["lahmacun"] * 110, "patates": ADET["patatesli"] * 150, "kiyma": ADET["kiymali"] * 160, "tavuk": ADET["tavuklu"] * 145,
       "kusbasi": ADET["kusbasili"] * 145, "kasar": ADET["kasarli"] * 130 + ADET["sucuklu"] * 90, "sucuk": ADET["sucuklu"] * 70}
ih = {}
for k, g in gun.items():
    kg2 = 2 * g / 1000.0
    L2 = kg2 / URUN[k]["rho"] if k in URUN else None
    ih[k] = dict(gun_kg=round(g / 1000, 2), iki_gun_kg=round(kg2, 2), iki_gun_L=None if L2 is None else round(L2, 2))
R["ihtiyac"] = ih
json.dump(R, open("hesap_sonuc.json", "w"), ensure_ascii=False, indent=1, default=lambda o: o)
for k, v in R.items():
    print("==", k)
    if isinstance(v, dict):
        for a, b in v.items(): print("   ", a, b if not isinstance(b, tuple) else tuple(None if q is None else round(q, 2) for q in b))
print("cep hacmi L", round(cv, 3))
# evaporator tablosu (tpaket tp_olcu / tp2 log)
E = {"eski tek kaset (TC v31)": (397, 137, 85), "L (mevcut)": (142, 176, 85), "R (mevcut)": (327, 140, 85)}
for k, (a, b, c) in E.items(): print("EVAP", k, "yuz", a * b, "mm2 · hacim", round(a * b * c / 1e6, 2), "L")
