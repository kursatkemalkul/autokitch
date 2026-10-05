# -*- coding: utf-8 -*-
"""m8t2 · MADDE 3: boş rakorlara kör tapa (Lapp SKINTOP kör tapa başlığı, rakor dış yüzüne oturur) + 4 havada kelepçeye yapıya bağlanan dil.
python m8t2_madde3.py giris.glb cikis.glb"""
import sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from m8kit import Glb, kutu_ucgen, silindir_ucgen, Yuzey
g = Glb(sys.argv[1]); LOG = []
def log(*a): LOG.append(" ".join(str(x) for x in a)); print(*a, flush=True)

# ---------- kör tapa: (düğüm, bileşen içi nokta, eksen, dış yüz koordinatı, yön, tapa r) ----------
TAPA = [("ELK_QR_KUTU__rakor", (4880.0, 1996.0, 790.3), 1, 2005.0, +1, 12.0, "QR kutusu Harting rakoru M32 (Harting kullanılmıyor)"),
        ("ELK_ANA_HAT__rakor", (5491.0, 1301.0, 950.3), 1, 1312.0, +1, 12.0, "ana ayırıcı üst rakoru M32"),
        ("F_UST_KABIN__plastik", (2600.2, 1825.0, -821.0), 2, -812.0, +1, 8.0, "F üst kabin davlumbaz fanı rakoru M20"),
        ("F_UST_KABIN__plastik", (2630.2, 830.0, -821.0), 2, -812.0, +1, 8.0, "F üst kabin fırın sinyal rakoru M20"),
        ("F_UST_KABIN__plastik", (3689.2, 1825.0, -821.0), 2, -812.0, +1, 8.0, "F üst kabin kompresör rakoru M20")]
for d, q, ax, yuz, sg, r, ad in TAPA:
    try:
        b = g.bul_nokta(d, q, tol=1.0)
    except KeyError as e:
        log("tapa: bileşen yok", d, q); continue
    c = (b["lo"] + b["hi"]) / 2.0
    # dış yüz: bileşen kutusunun o eksendeki ucu
    yz = b["hi"][ax] if sg > 0 else b["lo"][ax]
    p0 = c.copy(); p0[ax] = yz; p1 = c.copy(); p1[ax] = yz + sg * 3.0
    g.ekle_dugum(d, silindir_ucgen(p0, p1, r, 24), ornek=b)
    log("kör tapa:", ad, "merkez", c.round(1), "yüz", round(yz, 2), "r", r)

# ---------- havada kelepçe dilleri ----------
YS = Yuzey(g)
YAPI_DISI = r"kablo|__hava|hortum|rakor|__conta|__on_seffaf"
def dil(lo, hi, dugum, ornek, genis=12.0, kal=2.0, maxd=60.0):
    c = (lo + hi) / 2
    icinde = lambda P: np.all((P.mean(1) >= lo - 0.5) & (P.mean(1) <= hi + 0.5), axis=1)
    best = None
    for ax in range(3):
        u, w = [i for i in range(3) if i != ax]
        gu = min(genis, hi[u] - lo[u]); gw = min(kal, hi[w] - lo[w])
        for sg in (-1, 1):
            d = np.zeros(3); d[ax] = sg
            o = c.copy(); o[ax] = hi[ax] if sg > 0 else lo[ax]
            t = YS.isin(o, d, maxd, atla=icinde, haric_ad=YAPI_DISI + "|^" + dugum + "$")
            if t is None or t < 0.3: continue
            ok = True
            for du in (-gu / 2 - 0.3, 0, gu / 2 + 0.3):
                for dw in (-gw / 2 - 0.3, 0, gw / 2 + 0.3):
                    qq = o.copy(); qq[u] += du; qq[w] += dw
                    ta = YS.isin(qq, d, t + 0.5, atla=icinde, haric_ad="^" + dugum + "$")
                    if ta is not None and ta < t - 0.05: ok = False
            if ok and (best is None or t < best[0]): best = (t, ax, sg, o)
    if best is None: return None
    t, ax, sg, o = best
    a = o.copy(); e = o.copy(); e[ax] = o[ax] + sg * t
    u, w = [i for i in range(3) if i != ax]
    lo2 = np.minimum(a, e); hi2 = np.maximum(a, e)
    gu = min(genis, hi[u] - lo[u]); gw = min(kal, hi[w] - lo[w])
    lo2[u] = c[u] - gu / 2; hi2[u] = c[u] + gu / 2
    lo2[w] = c[w] - gw / 2; hi2[w] = c[w] + gw / 2
    g.ekle_dugum(dugum, kutu_ucgen(lo2, hi2), ornek=ornek)
    return round(t, 1), "xyz"[ax], sg
KEL = [("ELK_QR_KABLO__celik", (4956.0, 1960.0, 783.0)), ("ELK_QR_KABLO__celik", (4955.2, 1960.0, 797.0)),
       ("ELK_K__celik", (4193.0, 1110.0, -39.1))]
# K EC5000 kelepçesi: tek uygun yön (−z 52 mm) K duruş verici kablosunu kesiyor (tam tarama 1,0 mm) -> dil eklenmedi
for d, q in KEL:
    try:
        b = g.bul_nokta(d, q, tol=0.5)
    except KeyError:
        log("kelepçe yok", d, q); continue
    log("kelepçe dili", d, q, dil(b["lo"], b["hi"], d, b))

# ---------- MADDE 2 (kısmi): F üst kabin kompresör hava ana hattı (Ø9,9, 0 kelepçe) -> P-kelepçe + tavana askı lamı, ~250 mm ara ----------
pf = [q for q in g.dprims("F_UST_KABIN__paslanmaz") if not q.get("gizli")][0]
ex = pf["pr"].get("extras", {}); KAT_F = (ex.get("kat") or [None])[0]; MEK_F = (ex.get("mek") or [None])[0]
RH = 4.96; GEN = 12.0; KAL = 1.5; IC = RH + 0.4
def p_kelepce(x, y, z):
    T = []
    # kare bant (dört lama) hortum çevresinde, iç yarı genişlik IC
    T.append(kutu_ucgen((x - GEN / 2, y + IC, z - IC - KAL), (x + GEN / 2, y + IC + KAL, z + IC + KAL)))     # üst
    T.append(kutu_ucgen((x - GEN / 2, y - IC - KAL, z - IC - KAL), (x + GEN / 2, y - IC, z + IC + KAL)))   # alt
    T.append(kutu_ucgen((x - GEN / 2, y - IC, z - IC - KAL), (x + GEN / 2, y + IC, z - IC)))               # arka
    T.append(kutu_ucgen((x - GEN / 2, y - IC, z + IC), (x + GEN / 2, y + IC, z + IC + KAL)))               # ön
    yu = y + IC + KAL
    t = YS.isin((x, yu + 0.01, z), (0, 1, 0), 80.0)
    if t is None: return None
    for dx in (-GEN / 2 + 0.5, GEN / 2 - 0.5):
        for dz in (-0.6, 0.6):
            t2 = YS.isin((x + dx, yu + 0.01, z + dz), (0, 1, 0), t + 1.0)
            if t2 is None or t2 < t - 0.3: return None
    T.append(kutu_ucgen((x - GEN / 2, yu, z - 1.0), (x + GEN / 2, yu + t, z + 1.0)))                       # askı lamı (2 mm)
    g.ucgen_ekle("F_UST_KABIN__paslanmaz", np.concatenate(T), kat=KAT_F, mek=MEK_F)
    return round(t, 1)
for x in (2620.0, 2870.0, 3120.0, 3370.0):
    log("F hava hattı P-kelepçe x", x, "askı", p_kelepce(x, 1809.0, -740.1))
for x in (3720.0, 3950.0):
    log("K dalı P-kelepçe x", x, "askı", p_kelepce(x, 1809.0, -769.9))
g.kaydet(sys.argv[2]); log("kaydedildi", sys.argv[2])
open(os.path.join(HERE, "m8t2", "madde3.log"), "w", encoding="utf-8").write("\n".join(LOG))
