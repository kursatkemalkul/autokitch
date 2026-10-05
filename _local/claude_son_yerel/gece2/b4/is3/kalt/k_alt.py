# -*- coding: utf-8 -*-
"""K ALT YENİDEN (Kemal 3 Eki, 99.png: "bu alt kısım olmadı, burayı tekrar kur; yanda neden profil var; direkt temiz bir şekilde üstteki rafı
tutacak destekleri olsun ama düzgün yap, temiz, basit").
Taban v8zd → v8ze. Dünya mm (x hat boyunca, y yukarı, z koridora; K = x 4000–4400).

KALKAN (dağınık alt)
  · 2 orta yan kuşak (istasyon_tabani_tasiyici_20 / _380 · 30 × 32 kutu, y 860–892, duvar boyunca z −785…27) = Kemal'in "yandaki profil"
  · 6 orta panel kulağı (y 826/833–862, kuşağın altında, z −680 / −350 / −20) + üstlerindeki 18 bağlantı elemanı (saplama, pul, somun)
  · bant ayaklarının 791–892 uzatması (m1'de tabana uzatılmıştı → yine kısa ayak: 892–932,5)
YENİ (tek, düz raf + 6 eş dik destek)
  · İSTASYON RAFI 304 3 mm, üst yüz y 892 (bant ayakları ve itici taban plakaları DOĞRUDAN üstünde; bant 932,5 · itici 958 DEĞİŞMEDİ)
    x 4005–4395 · z −785…27 (köşe dikmelerinin arasında) · 4 kenar 30 mm aşağı büküm (y 862–892): yan bükümlerde K↔F (z −720) ve K↔E (z −100)
    M8 perçin somunları (eski kuşaktaki yerinde, Ø13,6 delik) · üstte 2 × Ø16,4 K→B lokma servis deliği + silikon tapa (tapa −3) ·
    bant ayağı 4 × PEM SP-M6 · itici tabanı 8 × PEM SP-M5 (rafa gömülü, eski ara raftaki yerlerinde)
  · 6 DİK DESTEK: 304 kutu 40 × 40 × 1,5, iki sıra (x 4040–4080 / 4320–4360, x 4200'e simetrik) × 3 (z −700 / −379 / −58: 321 eşit aralık,
    raf ortasına simetrik) · üst: 40 × 40 × 4 kapak plakası (kaynaklı, raf altına 2 × M6 havşa vida, raf üstü düz) · alt: 40 × 90 × 4 taban flanşı
    (kaynaklı) + 2 × M6 altıgen başlı vida tabana (taban sacında PEM) · altta boş hacim (kablo yok)
Kullanım: python k_alt.py giris.glb cikis.glb"""
import sys, os, numpy as np
import cadquery as cq
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\b4\is3"
sys.path.insert(0, S + r"\gece"); sys.path.insert(0, S)
import m8kit, glbkit

gi, go = sys.argv[1:3]
G = m8kit.Glb(gi)
R = []

# ---------------------------------------------------------------- ölçüler
X0, X1 = 4005.0, 4395.0          # raf dış (eski kuşakların dış yüzleri)
Z0, Z1 = -785.0, 27.0            # köşe dikmeleri arası
YU, T, BUK = 892.0, 3.0, 30.0    # raf üst yüzü · sac · büküm
YA = YU - BUK                    # 862 büküm alt kenarı
PX = (4060.0, 4340.0)            # destek sıraları (x 4200'e simetrik)
PZ = (-700.0, -379.0, -58.0)     # 321 eşit aralık, raf ortası (−379) simetrik
PA, PT = 40.0, 1.5               # kutu profil
YT = 791.0                       # asıl taban sacı üstü
FT = 4.0                         # flanş / kapak kalınlığı
FL = 90.0                        # taban flanşı boyu (z)
TAPA = ((4016.5, -569.86), (4016.5, -479.86))
RIV = ((X0, -720.0, 1), (X1, -100.0, -1))      # perçin somunu (yan büküm) · y 877,1
PEM6 = [(4065.0, -421.0), (4065.0, -3.0), (4335.0, -421.0), (4335.0, -3.0)]
PEM5 = [(x, z) for x in (4054.0, 4346.0) for z in (-741.0, -769.0, -631.0, -659.0)]


def komp(ad):
    p = [q for q in G.prims if q["name"] == ad and not q.get("gizli")][0]
    tl, kut = glbkit.Glb.komp(p); return p, tl, kut


def sec(kut, f):
    return [i for i, (a, b, n) in kut.items() if f(a, b)]


# ---------------------------------------------------------------- 1 · K_GOVDE__sac: kuşaklar + orta kulaklar
p, tl, kut = komp("K_GOVDE__sac")
kus = sec(kut, lambda a, b: a[1] > 859.5 and b[1] < 892.5 and b[2] - a[2] > 800 and (b[0] < 4036 or a[0] > 4364))
kul = sec(kut, lambda a, b: a[1] > 825 and b[1] < 862.5 and (b[0] < 4027 or a[0] > 4373) and -700 < (a[2] + b[2]) / 2 < -1 and b[2] - a[2] < 32)
kul = [i for i in kul if min(abs((kut[i][0][2] + kut[i][1][2]) / 2 - z) for z in (-680, -350, -20)) < 2]
assert len(kus) == 2 and len(kul) == 6, (kus, kul)
tri0 = int(np.where(tl == kus[0])[0][0])
KAT_SAC, MEK_SAC = G.etiket_of(p, tri0, "kat"), G.etiket_of(p, tri0, "mek")
R.append(("kuşak sil", len(kus), G.sil(p, np.isin(tl, kus + kul))))
R.append(("orta kulak sil", len(kul), 0))

# ---------------------------------------------------------------- 2 · K_GOVDE__celik: orta kulak elemanları (18)
p, tl, kut = komp("K_GOVDE__celik")
ck = sec(kut, lambda a, b: 833 < a[1] and b[1] < 851 and (b[0] < 4016 or a[0] > 4384)
         and min(abs((a[2] + b[2]) / 2 - z) for z in (-680, -350, -20)) < 2)
assert len(ck) == 18, ck
riv = sec(kut, lambda a, b: 869 < a[1] and b[1] < 885 and abs((a[2] + b[2]) / 2 + 720) < 1 and b[0] < 4021)
KAT_CEL, MEK_CEL = G.etiket_of(p, int(np.where(tl == riv[0])[0][0]), "kat"), G.etiket_of(p, int(np.where(tl == riv[0])[0][0]), "mek")
R.append(("kulak elemanı sil", len(ck), G.sil(p, np.isin(tl, ck))))

# ---------------------------------------------------------------- 3 · tapalar −3 (raf üstü 892)
p, tl, kut = komp("K_GOVDE__conta")
tp = sec(kut, lambda a, b: a[1] > 891.9 and b[1] < 896.1)
assert len(tp) == 2
R.append(("tapa −3", len(tp), G.tasi(p, np.isin(tl, tp) & G.gorunur(p), lambda V: V + [0, -3.0, 0])))

# ---------------------------------------------------------------- 4 · bant ayakları 791 → 892
p, tl, kut = komp("K_BANT__sac")
ay = sec(kut, lambda a, b: abs(a[1] - 791) < 0.1 and abs(b[1] - 932.5) < 0.1 and b[0] - a[0] < 21)
assert len(ay) == 4, ay
def kisalt(V):
    V[np.abs(V[:, 1] - 791.0) < 0.05, 1] = YU; return V
R.append(("bant ayağı 791→892", len(ay), G.tasi(p, np.isin(tl, ay) & G.gorunur(p), kisalt)))

# ---------------------------------------------------------------- 5 · RAF (CadQuery)
def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def sil_y(x, z, r, y0, y1):          # dikey silindir
    return cq.Workplane("XY").add(cq.Solid.makeCylinder(r, y1 - y0, cq.Vector(x, y0, z), cq.Vector(0, 1, 0)))


def alti_y(x, z, ak, y0, y1):        # dikey altıgen (köşeden köşeye ak)
    w = cq.Workplane(cq.Plane(origin=(x, y0, z), xDir=(1, 0, 0), normal=(0, 1, 0))).polygon(6, ak).extrude(y1 - y0)
    return w


raf = kutu(X0, X1, YU - T, YU, Z0, Z1)
raf = raf.union(kutu(X0, X0 + T, YA, YU - T, Z0, Z1)).union(kutu(X1 - T, X1, YA, YU - T, Z0, Z1))
raf = raf.union(kutu(X0 + T, X1 - T, YA, YU - T, Z0, Z0 + T)).union(kutu(X0 + T, X1 - T, YA, YU - T, Z1 - T, Z1))
for x, z in TAPA: raf = raf.cut(sil_y(x, z, 8.2, YU - T - 1, YU + 1))
for x, z in PEM6: raf = raf.cut(sil_y(x, z, 4.35, YU - T - 1, YU + 1))
for x, z in PEM5: raf = raf.cut(sil_y(x, z, 3.95, YU - T - 1, YU + 1))
for x, z, s in RIV:
    xa = x - 1 if s > 0 else x - T - 1
    raf = raf.cut(cq.Workplane("XY").add(cq.Solid.makeCylinder(6.8, T + 2, cq.Vector(xa, 877.1, z), cq.Vector(1, 0, 0))))
cel = []
for x, z in PEM6: cel.append(sil_y(x, z, 4.35, YU - T - 2.1, YU - 0.6))
for x, z in PEM5: cel.append(sil_y(x, z, 3.95, YU - T - 2.1, YU - 0.6))
# ---------------------------------------------------------------- 6 · DESTEKLER
des = []
h = PA / 2
for x in PX:
    for z in PZ:
        y0, y1 = YT + FT, YU - T - FT                      # kutu 795–885
        k = kutu(x - h, x + h, y0, y1, z - h, z + h)       # kutu profil uçları kapalı (kaynaklı kapak + flanş) → ağda dolu gösterilir
        k = k.union(kutu(x - h, x + h, y1, YU - T, z - h, z + h))                 # üst kapak 885–889
        k = k.union(kutu(x - h, x + h, YT, YT + FT, z - FL / 2, z + FL / 2))     # taban flanşı 791–795
        des.append(k)
        for dz in (-32.0, 32.0):                                                 # M6 altıgen baş (Ø10 × 4)
            cel.append(alti_y(x, z + dz, 11.5, YT + FT, YT + FT + 4.0))

def ekle(ad, solidler, kat, mek):
    P, I = glbkit.Glb.ag([s.val() for s in solidler], 0.05, 0.2)
    p = [q for q in G.prims if q["name"] == ad and not q.get("gizli")][0]
    return G._ekle_dunya(p, P[I], kat, mek, False)

R.append(("raf + 6 destek → K_GOVDE__sac", 7, ekle("K_GOVDE__sac", [raf] + des, KAT_SAC, MEK_SAC)))
R.append(("PEM 12 + vida 12 → K_GOVDE__celik", 24, ekle("K_GOVDE__celik", cel, KAT_CEL, MEK_CEL)))
for r in R: print("  %-36s %3d · %d" % r)
print("etiket sac kat %s mek %s · celik kat %s mek %s" % (KAT_SAC, MEK_SAC, KAT_CEL, MEK_CEL))
G.kaydet(go); print("yazildi", go)
