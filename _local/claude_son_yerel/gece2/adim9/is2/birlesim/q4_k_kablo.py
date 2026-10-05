# -*- coding: utf-8 -*-
"""q4 · K ARKA 4 SENSÖR/MOTOR KABLOSU TEK KANALDA + K havada kelepçeler (iş 3a + 3c-K).
K alt yeniden kurulunca (v8ze) arka duvarın ortası boşaldı (eski 'yağ sacı + motor' engeli yağ panosu y ≥ 1472'de kaldı).
Kablolar (klemens altı → arka → aşağı): A r2,5 (x 4176 → y 1219,6 → x 4025 → öne) · B r2 (x 4185 → itici sol sensör) ·
C r2 (x 4238 → itici sağ sensör) · D r3 EC5000 bant motoru (x 4254). Eski dağınık yollar (8 ayrı dikey/yatay parça, 4 kelepçe, 2'si havada) silindi.
YENİ: ters T KABLO KANALI (paslanmaz 1,5, kapaklı) z −765…−735 · DİKEY x 4166–4264 · y 1240–1575 (klemensin hemen altı) +
  YATAY x 4036–4364 · y 1198–1242 (iki köşe dikmesinin arası, açık uçlar dikme önünde). Kablolar kanal içinde z −750 düzleminde, x sırası
  korunur (kesişme yok): sol A üst 1219,6 / B alt 1207 · sağ D üst 1222 / C alt 1207. Kanal arka duvara 4 ayaklı braketle (2 mm, 63,5 mm).
  Kanal uçlarından inişler dikme önündeki sac kulaklarına (z −756,2) P-kelepçeyle bağlı: sol B · sağ C + D (çift kelepçe).
  K giriş alıcı kablosunun havadaki kelepçesi → bant ön POM kılavuzuna (y 1001,3) L dilli kelepçe.
python q4_k_kablo.py giris.glb cikis.glb"""
import sys
from qlib import *
import cadquery as cq
gi, go = sys.argv[1:3]
G = m8kit.Glb(gi); R = []
ZC = -750.0
ESKI = {"A": (2.5, [(4176, 1642.5, -745), (4176, 1219.6, -745), (4025, 1219.6, -745)]),
        "B": (2.0, [(4185, 1644, -739.3), (4185, 1534, -739.3), (4185, 1534, -735.3), (4185, 1210, -735.3), (4029, 1210, -735.3), (4029, 1038, -735.3)]),
        "C": (2.0, [(4238, 1644, -739.3), (4238, 1534, -739.3), (4238, 1534, -735.3), (4318, 1534, -735.3), (4318, 1398, -735.3), (4370, 1398, -735.3), (4370, 1038, -735.3)]),
        "D": (3.0, [(4254, 1644, -746.6), (4254, 1525, -746.6), (4254, 1525, -726.6), (4298, 1525, -726.6), (4298, 1389, -726.6), (4374, 1389, -726.6), (4374, 1029, -726.6)])}
YENI = {"A": [(4176, 1642.5, -745), (4176, 1590, -745), (4176, 1590, ZC), (4176, 1219.6, ZC), (4025, 1219.6, ZC), (4025, 1219.6, -745)],
        "B": [(4185, 1644, -739.3), (4185, 1590, -739.3), (4185, 1590, ZC), (4185, 1207, ZC), (4029, 1207, ZC), (4029, 1038, ZC), (4029, 1038, -735.3)],
        "C": [(4238, 1644, -739.3), (4238, 1590, -739.3), (4238, 1590, ZC), (4238, 1207, ZC), (4370, 1207, ZC), (4370, 1038, ZC), (4370, 1038, -735.3)],
        "D": [(4254, 1644, -746.6), (4254, 1590, -746.6), (4254, 1590, ZC), (4254, 1222, ZC), (4378, 1222, ZC), (4378, 1029, ZC), (4378, 1029, -726.6), (4374, 1029, -726.6)]}


def pl_mesafe(V, L):
    L = np.asarray(L, float); d = np.full(len(V), 1e9)
    for a, b in zip(L[:-1], L[1:]):
        ab = b - a; t = np.clip(((V - a) @ ab) / max(ab @ ab, 1e-9), 0, 1)
        d = np.minimum(d, np.linalg.norm(V - (a + t[:, None] * ab), axis=1))
    return d


pk = prim(G, "ELK_K__kablo"); vis = G.gorunur(pk)
etk = None
for k, (r, L) in ESKI.items():
    d = pl_mesafe(pk["X"], L)
    m = vis & np.all(d[pk["T"]] < r + 1.0, axis=1)
    # bukum dirsekleri (bukum yaricapi > r): eski ic koselerin 2r+4 komsulugu, yeni yoldan uzak olanlar
    dn = pl_mesafe(pk["X"], YENI[k])
    for q in L[1:-1]:
        dq = np.linalg.norm(pk["X"] - np.asarray(q, float), axis=1)
        m |= vis & np.all(dq[pk["T"]] < 2 * r + 4, axis=1) & np.all(dn[pk["T"]] > r + 0.5, axis=1)
    if etk is None: etk = G._etiketler(pk, int(np.where(m)[0][0]))
    R.append(("eski yol sil " + k, G.sil(pk, m)))
    vis = G.gorunur(pk)
for k, L in YENI.items():
    r = ESKI[k][0]
    Pw = [tup(L, r, 12)]
    for q in (L[0], L[-1]): Pw.append(m8kit.kure_ucgen(q, r, 12, 6))
    R.append(("yeni yol " + k, ekle(G, "ELK_K__kablo", np.concatenate(Pw), etk)))
# eski kelepceler (tasinan yollarin) -- c2/c3 sol dikey, EC5000 c17 + c18
for lo, hi in (((4168.0, 1423.8, -828.5), (4184.0, 1435.8, -741.5)), ((4177.0, 1366.0, -828.5), (4193.0, 1378.0, -732.3)),
               ((4366.0, 1183.0, -732.6), (4382.0, 1195.0, -722.6)), ((4367.0, 1212.0, -743.3), (4398.5, 1224.0, -727.3))):
    p, m, et_c = bilesen(G, "ELK_K__celik", lo, hi, tol=0.3); R.append(("eski kelepce sil", G.sil(p, m)))

# ---------------------------------------------------------------- KANAL (ters T)
def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
t = 1.5; Z0, Z1 = -765.0, -735.0
dis = kutu(4036, 4364, 1198, 1242, Z0, Z1).union(kutu(4166, 4264, 1198, 1575, Z0, Z1))
ic = kutu(4030, 4370, 1198 + t, 1242 - t, Z0 + t, Z1 - t).union(kutu(4166 + t, 4264 - t, 1198 + t, 1580, Z0 + t, Z1 - t))
kanal = dis.cut(ic)
P, I = glbkit.Glb.ag([kanal.val()], 0.05, 0.2)
et_s = G._etiketler(prim(G, "K_ELEKTRIK__sac"), 0)
R.append(("kanal (ters T) -> K_ELEKTRIK__sac", ekle(G, "K_ELEKTRIK__sac", P[I], et_s)))
et_c = G._etiketler(prim(G, "ELK_K__celik"), 0)
# braketler: arka duvar (-828.5) -> kanal sirti (-765)
br = []
for xc, yc in ((4100.0, 1220.0), (4300.0, 1220.0), (4215.0, 1300.0), (4215.0, 1440.0)):
    br += [kutu_ucgen((xc - 1, yc - 10, -826.5), (xc + 1, yc + 10, -767.0)),
           kutu_ucgen((xc - 1, yc - 10, -828.5), (xc + 19, yc + 10, -826.5)),
           kutu_ucgen((xc - 19, yc - 10, -767.0), (xc + 1, yc + 10, -765.0))]
R.append(("4 kanal braketi", ekle(G, "ELK_K__celik", np.concatenate(br), et_c)))


def halka(x, z, ri, y0, y1, zb=None):
    """dikey kablo icin kare P-kelepce halkasi (1 mm), ic yari genislik ri; zb: arka yuz (z) zorla"""
    a = ri + 1.0; zb0 = z - a if zb is None else zb
    return [kutu_ucgen((x - a, y0, zb0), (x + a, y1, zb0 + 1.0)), kutu_ucgen((x - a, y0, z + ri), (x + a, y1, z + a)),
            kutu_ucgen((x - a, y0, zb0 + 1.0), (x - ri, y1, z + ri)), kutu_ucgen((x + ri, y0, zb0 + 1.0), (x + a, y1, z + ri))]
kl = []
kl += halka(4029, ZC, 2.2, 1144, 1156) + [kutu_ucgen((4010, 1144, -756.2), (4025.8, 1156, -753.2))]           # sol: B -> c60 kulak
kl += halka(4370, ZC, 2.2, 1144, 1156, zb=-754.2) + halka(4378, ZC, 3.2, 1144, 1156, zb=-754.2)             # sag: C + D
kl += [kutu_ucgen((4366.8, 1144, -756.2), (4396.0, 1156, -754.2))]                                           # sag dil -> c1359 kulak
R.append(("inis P-kelepceleri (sol B, sag C+D)", ekle(G, "ELK_K__celik", np.concatenate(kl), et_c)))

# ---------------------------------------------------------------- K giris alici kelepcesi: havada -> POM kilavuz
p, m, et_g = bilesen(G, "ELK_K__celik", (4185.0, 1104.0, -44.6), (4201.0, 1116.0, -33.7), tol=0.3)
R.append(("giris alici havada kelepce sil", G.sil(p, m)))
xg, zg = 4193.0, -36.7
gk = halka(xg, zg, 2.2, 1030, 1042) + [kutu_ucgen((4188.0, 1030, -50.0), (4199.0, 1042, -39.9)),          # kopru
                                        kutu_ucgen((4188.0, 1001.3, -53.0), (4199.0, 1002.8, -48.5)),          # ayak (POM kilavuz ustu)
                                        kutu_ucgen((4188.0, 1002.8, -50.0), (4199.0, 1030.0, -48.5))]          # dik dil
R.append(("giris alici L dilli kelepce", ekle(G, "ELK_K__celik", np.concatenate(gk), et_c)))
for r_ in R: print("  %-40s %d" % r_)
G.kaydet(go); print("yazildi", go)
