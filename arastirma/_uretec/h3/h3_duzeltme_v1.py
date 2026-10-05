# -*- coding: utf-8 -*-
"""HAT v3.2 · HAVADA KALAN PARÇALARIN MONTAJI v1 (1 Eki 2026 · Claude · YEREL) — bütün makine döküm denetimi (h3_havada_v1) sonrası kalanlar:
  1 TEZGÂH: sabunluk + havluluk (sokak duvarı) ve askı rayı (ince duvar) bina duvarına asılıydı, modelde duvar yok → ikisine PASLANMAZ DUVAR KAPLAMA
    SACI (sıçrama paneli, 1,2 mm 304, alt ucu tabla eteğine bindirmeli + silikon) · cihazlar sacın yüzüne vidalı (duvara dübel aynı delikten).
  2 B soğutma: sıcak gaz serpantini buharlaştırma tavasının tabanından 3,3 mm yukarıda boşta → PA SERPANTİN TUTUCULARI (her düz kolda 2, boruya oturan eyer).
  3 E çöp: şerit düşme oluğu ön alt kanattan 1,5 mm kısa → OLUK FLANŞI (oluğun kesiti 1,5 mm uzatılır, kanada perçin).
SÖZLEŞME (h3_ust_depo_v2 gibi): kur() · PARCALAR [ad, wp, mal, birim, grup, kaynak, bom] (DÜNYA) · dunya(p) · BIRIMLER · BIRIM_MODUL · MALZEME."""
import os, sys
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_elk_ortak as EO
from h3_elk_ortak import kut

PARCALAR = []
BIRIMLER = [("DUZ_TEZGAH_DUVAR", "Tezgâh duvar kaplama sacları (sokak + ince duvar · 304 1,2 · alt ucu tabla eteğine bindirmeli) — sabunluk · havluluk · askı rayı bunlara vidalı"),
            ("DUZ_B_SERPANTIN", "Sıcak gaz serpantini tutucuları (PA66 eyer · buharlaştırma tavası tabanına perçin)"),
            ("DUZ_E_OLUK", "Robot çöpü şerit düşme oluğu flanşı (oluk kesiti → ön alt kanat, perçin)")]
BIRIM_MODUL = {"DUZ_TEZGAH_DUVAR": "S", "DUZ_B_SERPANTIN": "B", "DUZ_E_OLUK": "E"}
MALZEME = {"paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30), "plastik": dict(renk=(0.92, 0.92, 0.90, 1.0), met=0.0, ruf=0.6)}


def ekle(ad, sh, mal, birim, bom=None):
    PARCALAR.append(dict(ad=ad, wp=cq.Workplane(obj=sh), mal=mal, birim=birim, grup="SABIT", kaynak="h3_duzeltme_v1", bom=bom))


def dunya(p):
    v = p["wp"].vals()
    return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])


def _d(ad):
    for a, s, b in EO.dokum():
        if a == ad: return s, b
    raise KeyError(ad)


def kur():
    PARCALAR[:] = []
    # 1 · TEZGÂH duvar kaplama sacları (tabla x 3842 – arka panel 4503,8 · etek üstü 1000 → 1700)
    X0, X1, Y0, Y1, T = 3842.0, 4503.8, 1000.0, 1700.0, 1.2
    sok = kut(X0, X1, Y0 + T, Y1, 1879.0, 1879.0 + T).fuse(kut(X0, X1, Y0, Y0 + T, 1872.8, 1879.0 + T))          # yüz + alt dudak (eteğe biner)
    ekle("duvar_kaplama_sokak", sok, "paslanmaz", "DUZ_TEZGAH_DUVAR",
         ("Duvar kaplama sacı 304 1,2 · 662 × 700 · alt dudak tabla eteğine (silikon)", 2, "sokak + ince duvar", "sabunluk / havluluk / askı rayı bu saca vidalı"))
    inc = kut(X0, X1, Y0 + T, Y1, 1039.0 - T, 1039.0).fuse(kut(X0, X1, Y0, Y0 + T, 1039.0 - T, 1045.2))
    ekle("duvar_kaplama_ince", inc, "paslanmaz", "DUZ_TEZGAH_DUVAR")
    # 2 · serpantin tutucuları: borunun alt çizgisine oturan 3 eyer (x ≈ 4080 · 4213 · 4345), tava tabanı (y 126) → boru ekseni, boru şekli çıkarılır
    sp, sb = _d("B_SOGUTMA|sicak_gaz_serpantini")
    yc = (sb[2] + sb[3]) / 2.0
    n = 0
    for xh in (4080.0, 4213.0, 4345.0):
        yer = None
        for dx in (0, 6, -6, 12, -12, 18, -18, 24, -24):
            for zi in range(int(sb[4]) + 4, int(sb[5]) - 3, 2):
                if sp.intersect(kut(xh + dx - 1.0, xh + dx + 1.0, sb[2], sb[2] + 1.0, zi - 1.0, zi + 1.0)).Volume() > 0.05:
                    yer = (xh + dx, float(zi)); break
            if yer: break
        if yer is None: continue
        xc, zc = yer
        e = kut(xc - 6.0, xc + 6.0, 126.0, yc, zc - 5.0, zc + 5.0).cut(sp)
        ekle("serpantin_tutucu_%d" % n, e, "plastik", "DUZ_B_SERPANTIN",
             ("Serpantin tutucu PA66 eyer 12 × 10 (tava tabanına perçin)", 3, "", "") if n == 0 else None)
        n += 1
    kollar = [0] * n
    # 3 · E oluk flanşı: oluk kesiti (z 56–57,5) 1,5 mm öne kaydırılır → 57,5–59 (kanada değer)
    ol, ob = _d("E_COP|ecop_serit_dusme_olugu")
    kesit = ol.intersect(kut(ob[0] - 1, ob[1] + 1, ob[2] - 1, ob[3] + 1, ob[5] - 1.5, ob[5]))
    ekle("ecop_oluk_flansi", kesit.translate(cq.Vector(0, 0, 1.5)), "paslanmaz", "DUZ_E_OLUK",
         ("Oluk flanşı 304 1,5 (oluk kesiti) · ön alt kanada 4 perçin", 1, "", ""))
    print("h3_duzeltme_v1 · %d parça (serpantin kolu %d)" % (len(PARCALAR), len(kollar)))
    return PARCALAR


if __name__ == "__main__":
    kur()
    for p in PARCALAR:
        s = dunya(p); bad = [(a, round(v, 2)) for a, v in EO.cakisma(s)]
        print("  %-28s hacim %8.0f  çakışma %s" % (p["ad"], s.Volume(), bad[:4]))
    sys.stdout.flush(); os._exit(0)
