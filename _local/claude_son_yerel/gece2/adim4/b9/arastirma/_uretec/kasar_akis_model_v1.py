# -*- coding: utf-8 -*-
"""AUTOKITCH · KAŞAR AKIŞ MODELİ v1 (20 Eyl 2026)
Rende kaşarın kaset içindeki akışı için HESAP ÇEKİRDEĞİ. Sayfadaki (otonom/kaset3d/akis.html) sabit sayılar buradan gelir.

KAYNAKLI (ölçülmüş / yayınlanmış):
  · dökme yoğunluk 0,48 g/mL  — USDA SR (1 cup rende LMPS mozzarella = 113 g) + King Arthur ağırlık tablosu (113 g/cup)
    alt sınır 0,36 g/mL (USDA FDC 170900, 86 g/cup — DOĞRULANMADI) · küp 0,56 g/mL
  · katı yoğunluk 1,10 g/cm3 (USDA: 18 g / in3)
  · helezon hacim verimi: A.W. Roberts, "Design considerations and performance evaluation of screw conveyors"
      Vt   = (pi/4) [(D+2C)^2 - Dc^2] (p - ts)
      Re   = (2/3)(Ro^3-Ri^3)/(Ro^2-Ri^2) ,  alfa_e = atan(p / (2 pi Re))
      etaVR = 1 / (1 + tan(alfa_e) tan(fi_s + alfa_e))          (yatay, düşük devir)
      Q    = Vt · etaVR · etaF
  · sıcaklık: Banville 2013 (J. Dairy Sci.) — 4 °C kek "kolayca dağılıyor", 13 / 22 °C'de kohezyon artıyor
VARSAYIM (kaynak YOK — prototipte ölçülecek): fi_s (peynir–POM sürtünme açısı), etaF (kanat arası doluluk), yığın açısı.
"""
import math

RHO, RHO_ALT, RHO_KUP, RHO_KATI = 0.48, 0.36, 0.56, 1.10      # g/mL
GUN_KASAR_KG, PIDE_GUN = 4.4, 80                               # günlük tüketim (stok kurgusu 16 Eyl) → 55 g / pide
PORSIYON = GUN_KASAR_KG * 1000.0 / PIDE_GUN


def roberts(D, Dc, p, ts=3.0, C=3.0, fi_s=30.0):
    """mm girer → (Vt mL/tur, etaVR, alfa_e derece)"""
    Ro, Ri = D / 2.0, Dc / 2.0
    Vt = math.pi / 4.0 * ((D + 2 * C) ** 2 - Dc ** 2) * (p - ts) / 1000.0
    Re = (2.0 / 3.0) * (Ro ** 3 - Ri ** 3) / (Ro ** 2 - Ri ** 2)
    a = math.atan(p / (2 * math.pi * Re))
    eta = 1.0 / (1.0 + math.tan(a) * math.tan(math.radians(fi_s) + a))
    return Vt, eta, math.degrees(a)


# ---------------- v4 KESİT (iç ölçüler, mm) ----------------
V4 = dict(hw=134.0, rt=31.0, cy=56.0, Rb=134.0, yc=217.0, y_dolum=332.0, boy=390.0, Rs=129.0)
V3 = dict(hw=134.0, rt=31.0, cy=72.0, y1=158.0, y_dolum=332.0, boy=390.0, ykar=245.0, Rs=92.0)


def yari_v4(y, g=V4):
    if y < g["cy"] - g["rt"]: return 0.0
    if y < g["cy"]: return math.sqrt(max(0.0, g["rt"] ** 2 - (y - g["cy"]) ** 2))
    yj = g["yc"] - math.sqrt(g["Rb"] ** 2 - g["rt"] ** 2)                 # boğaz–kadeh birleşimi
    if y < yj: return g["rt"]
    if y < g["yc"]: return math.sqrt(max(0.0, g["Rb"] ** 2 - (y - g["yc"]) ** 2))
    return g["hw"]


def yari_v3(y, g=V3):
    if y < g["cy"] - g["rt"]: return 0.0
    if y < g["cy"]: return math.sqrt(max(0.0, g["rt"] ** 2 - (y - g["cy"]) ** 2))
    if y < g["y1"]:
        t = (g["y1"] - y) / (g["y1"] - g["cy"]); s = t * t * (3 - 2 * t)
        return g["hw"] - (g["hw"] - g["rt"]) * s
    return g["hw"]


def hacim(yari, g):
    a, dy, y = 0.0, 0.25, g["cy"] - g["rt"]
    while y < g["y_dolum"]:
        a += 2 * yari(y + dy / 2) * dy; y += dy
    return a * g["boy"] / 1e6                                              # L


def olu_bolge(yari, g, ymerk, Rs, egim_min=60.0):
    """Kesitte KENDİ AKMAYAN alan: duvar eğimi < egim_min (yataydan) olan yerin üstündeki malzeme,
    karıştırıcının süpürdüğü daire (merkez ymerk, yarıçap Rs) DIŞINDA kalıyorsa ölü sayılır.
    Basit ölçü: duvara yapışık 1 mm'lik şeritleri tara; şerit süpürülmüyorsa ve duvar yatıksa, o şeridin
    üstündeki yığın açısı kamasını (45°) ölü say."""
    dy, y, alan = 0.5, g["cy"], 0.0
    while y < g["y_dolum"] - dy:
        x0, x1 = yari(y), yari(y + dy)
        if x1 - x0 > 1e-6:
            egim = math.degrees(math.atan2(dy, x1 - x0))
            xm, ym = (x0 + x1) / 2, y + dy / 2
            supuruluyor = math.hypot(xm, ym - ymerk) <= Rs + 6.0          # tel + sıyırıcı payı
            if egim < egim_min and not supuruluyor:
                # bu duvar parçasının üstünde duran kama: yükseklik = kalan yatay mesafe * tan(45) ile sınırlı
                alan += (x1 - x0) * min(g["y_dolum"] - ym, (g["hw"] - xm) * 1.0 + 25.0)
        y += dy
    return 2 * alan * g["boy"] / 1e6                                       # L (iki yan)


# ---------------- HATVE DİZİSİ: eşit çekiş ----------------
def cekis(dizi, fi_s=30.0):
    """dizi = [(hatve, mil çapı)] akış yönünde. Her kanadın kapasitesi ve hazneden ALDIĞI pay."""
    q = [roberts(56.0, dc, p, fi_s=fi_s)[0] * roberts(56.0, dc, p, fi_s=fi_s)[1] for p, dc in dizi]
    pay = [q[0]] + [max(0.0, q[i] - q[i - 1]) for i in range(1, len(q))]
    return q, pay


if __name__ == "__main__":
    print("PORSIYON %.0f g/pide · 2 gunluk %.1f kg" % (PORSIYON, 2 * GUN_KASAR_KG))
    for ad, yari, g in (("v3", yari_v3, V3), ("v4", yari_v4, V4)):
        print("%s kesit hacmi %.1f L" % (ad, hacim(yari, g)))
    H4 = hacim(yari_v4, V4) - 0.35                                         # helezon + köprü + karıştırıcı payı
    for rho in (RHO_ALT, 0.41, RHO):
        print("  yogunluk %.2f → 2 gunluk kasar %.1f L · doluluk %%%.0f · tam dolu %.1f kg" % (rho, 8.8 / rho, 100 * 8.8 / rho / H4, H4 * rho))
    print("OLU BOLGE v3: %.2f L   v4: %.2f L" % (olu_bolge(yari_v3, V3, V3["ykar"], V3["Rs"]), olu_bolge(yari_v4, V4, V4["yc"], V4["Rs"])))
    print("\nROBERTS · D56 Dc20 p48 ts3 C3")
    for fi in (20, 30, 40, 45):
        Vt, eta, a = roberts(56, 20, 48, fi_s=fi)
        print("  fi_s %2d°  Vt %.1f mL  alfa_e %.1f°  etaVR %.3f  → %.1f mL/tur (tam dolu)" % (fi, Vt, a, eta, Vt * eta))
    print("\nHATVE DIZILERI (tek yan, giris 122 mm):")
    for ad, dizi in (("sabit 48 / mil 20", [(40.7, 20)] * 3), ("artan 34-40-48 / mil 20", [(34, 20), (40, 20), (48, 20)]),
                     ("artan 32-40-50 / konik mil 38-30-20", [(32, 38), (40, 30), (50, 20)]),
                     ("artan 30-40-52 / konik mil 40-32-20", [(30, 40), (40, 32), (52, 20)])):
        q, pay = cekis(dizi); top = sum(pay)
        print("  %-38s kapasite %s  → hazneden pay %s" % (ad, " / ".join("%.0f" % x for x in q), " / ".join("%%%.0f" % (100 * x / top) for x in pay)))
    print("\nDOZAJ (iki yan birlikte, son kanat p52 mil20, bogaz p52):")
    Vt, eta, a = roberts(56, 20, 52)
    for etaF in (0.3, 0.45, 0.6, 0.75):
        for rho in (RHO_ALT, RHO):
            g_tur = 2 * Vt * eta * etaF * rho
            print("  etaF %.2f  rho %.2f → %.1f g/tur · %.2f tur/porsiyon · 10 sn'de dokmek icin %.1f dev/dk" % (etaF, rho, g_tur, PORSIYON / g_tur, PORSIYON / g_tur / 10 * 60))
