# -*- coding: utf-8 -*-
"""Kalem 5 (dış zarf) + 6 (A içi): python d56_zarf_a.py [meta.json]  (meta: cak/c8a_meta9.py çıktısı; bileşen kutuları)"""
import sys, json, re, numpy as np
from collections import defaultdict
M = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "cak/meta.json", encoding="utf-8"))["bil"]
TOL = 0.5
HARIC = re.compile(r"^ACIL_STOP__|^TEZGAH|^DUZ_TEZGAH|^ROBOT|^INSAN|^ZEMIN")
KOL = re.compile(r"kol|kulp|tutamak|tutamac|el_?yeri", re.I)
def ic(lo, hi, z):  # z = (x0,x1,y0,y1,z0,z1)
    return all(lo[i] >= z[2 * i] - TOL and hi[i] <= z[2 * i + 1] + TOL for i in range(3))
ANA = (736, 5230, 0, 2200, -830, 79); QR = (4370, 5230, 0, 2200, -830, 1190)
tas = defaultdict(list)
for b in M:
    if HARIC.search(b["dugum"]): continue
    lo, hi = b["lo"], b["hi"]
    if ic(lo, hi, ANA): continue
    # QR bölgesi: x 4370–5230 içinde kalan, z +1190'a kadar izinli
    if lo[0] >= QR[0] - TOL and ic(lo, hi, QR): continue
    adn = (b["ad"] or "") + " " + b["dugum"]
    hariç = bool(KOL.search(adn))
    if b["dugum"].startswith("ELK_ZEMIN"): tas["ZEMİN ALTI KANAL ELK_ZEMIN (kasıtlı, y<0)"].append((0, b["dugum"], b["ad"], b["no"], lo, hi)); continue
    if b["dugum"].startswith(("URUN", "E_PIZZA", "D_PIZZA")) and max(h - l for l, h in zip(lo, hi)) < 0.01: tas["SIFIR BOYUTLU ÜRÜN (animasyon yer tutucu)"].append((0, b["dugum"], b["ad"], b["no"], lo, hi)); continue
    asim = [max(0, ANA[0] - lo[0]), max(0, hi[0] - ANA[1]), max(0, ANA[2] - lo[1]), max(0, hi[1] - ANA[3]), max(0, ANA[4] - lo[2]), max(0, hi[2] - (QR[5] if lo[0] >= QR[0] - TOL else ANA[5]))]
    tas[("KOL/KULP (hariç)" if hariç else "TAŞAN")].append((round(max(asim), 1), b["dugum"], b["ad"], b["no"], lo, hi))
print("=== KALEM 5 · DIŞ ZARF (x 736–5230, y 0–2200, z −830…+79; QR x≥4370 z≤1190; tol 0,5; ACIL_STOP/TEZGAH/ROBOT hariç)")
for k in list(tas):
    L = sorted(tas[k], key=lambda x: -x[0]); print(k, len(L))
    if k != "TAŞAN": continue
    for a, d, ad, no, lo, hi in L[:60]: print("   %7.1f mm  %s[%d] %s  lo %s hi %s" % (a, d, no, ad or "-", lo, hi))
# acil stop kendi kontrolü (ne kadar taşıyor)
AS = [b for b in M if b["dugum"].startswith("ACIL_STOP__")]
print("ACIL_STOP bileşen", len(AS), "· en büyük z", max(b["hi"][2] for b in AS) if AS else None)
print("\n=== KALEM 6 · A İÇİ (x 737,5–1434,5 iç; A gövde/kapak/açıcı/tabla geçişi dışı parça)")
IZIN = re.compile(r"^A_|^KAIDE_A|^U_A_|^TOPPING_MODUL__.*ARABA|^TOPPING_DONER__TABLA|^ACIL_STOP")
say = defaultdict(list)
for b in M:
    lo, hi = b["lo"], b["hi"]
    if not (lo[0] >= 737.5 - TOL and hi[0] <= 1434.5 + TOL and lo[1] >= 788 and hi[1] <= 2200 and lo[2] >= -830 and hi[2] <= 79): continue
    if IZIN.search(b["dugum"]): continue
    tabla = lo[1] >= 893 and hi[1] <= 1006.5 and lo[2] >= -416 and hi[2] <= -3
    say["tabla geçişi (x 836–1434, y 893,5–1006, z −415…−3,8)" if tabla else "DİĞER"].append((b["dugum"], b["no"], b["ad"], lo, hi, b["mek"]))
for k, L in say.items():
    print(k, len(L))
    dd = defaultdict(list)
    for x in L: dd[x[0]].append(x)
    for d, xs in sorted(dd.items()): print("   %-40s %3d  ör. %s lo %s hi %s mek %s" % (d, len(xs), xs[0][2], xs[0][3], xs[0][4], xs[0][5]))
