# -*- coding: utf-8 -*-
"""hızlı tasarım denetimi: python kontrol.py spec_modulu"""
import sys, importlib, re, numpy as np
S = r"@@KOK_W@@"
sys.path.insert(0, S + r"\elk5"); sys.path.insert(0, S + r"\elk4")
from b5lib import *
from ortam4 import Ortam as _O, bolge
def Ortam(): return _O(S + r"\elk5\c0")
IST = dict(TOPPING=((1434, 788, -832), (2500, 2200, 80)), F=((2500, 788, -832), (4000, 1862, 80)), U=((2500, 1840, -832), (4000, 2200, 80)), K=((4000, 788, -832), (4400, 2200, 80)), E=((4400, 788, -832), (5232, 2200, 80)), B=((736, 0, -832), (4400, 788, 80)), QR=((4560, 0, 660), (5440, 2060, 1200)))
sp = importlib.import_module(sys.argv[1])
O0 = Ortam(); lo, hi = IST[sp.IST]
O = bolge(O0, np.array(lo) - 150, np.array(hi) + 150)
istc = [ci for ci, d in enumerate(KAY) if d["ist"] == sp.IST and d["S"] and re.search(r"kablo", d["prim"])] + list(getattr(sp, "EK_KABLO", []))
SEG = {ci: seg_list(ci, sp.YOL) for ci in istc}
# engel: yapı (kablo ve kelepçe hariç)
M = O.yapi.copy()
haric = getattr(sp, "HARIC_RE", None)
if haric: M &= ~np.array([bool(re.search(haric, a)) for a in O.nm])
tum = [s for ci in istc for s in SEG[ci]]
print("== KANAL ÇAKIŞMA")
for k in sp.KAN:
    c = O.kutu_kesis(k["lo"], k["hi"], M, e=0.1)
    nm = {}
    for i in c:
        a = nm.setdefault(O.nm[i], [0, O.lo[i].copy(), O.hi[i].copy()]); a[0] += 1; a[1] = np.minimum(a[1], O.lo[i]); a[2] = np.maximum(a[2], O.hi[i])
    print("  %-12s %s %s -> %s" % (k["ad"], np.round(k["lo"], 1).tolist(), np.round(k["hi"], 1).tolist(), "TEMİZ" if not nm else ""))
    for n_, (cnt, l_, h_) in nm.items(): print("        %-32s %4d  %s %s" % (n_, cnt, np.round(l_, 1).tolist(), np.round(h_, 1).tolist()))
print("== YENİ KABLO ÇAKIŞMA (kutu yaklaşık)")
for ci in sp.YOL:
    nm = {}
    for a, b, r in SEG[ci]:
        L0 = np.minimum(a, b) - r * 0.7; H0 = np.maximum(a, b) + r * 0.7
        for i in O.kutu_kesis(L0, H0, M, e=0.0):
            a_ = nm.setdefault(O.nm[i], [0, O.lo[i].copy(), O.hi[i].copy()]); a_[0] += 1; a_[1] = np.minimum(a_[1], O.lo[i]); a_[2] = np.maximum(a_[2], O.hi[i])
    print("  #%d -> %s" % (ci, "TEMİZ" if not nm else ""))
    for n_, (cnt, l_, h_) in nm.items(): print("        %-32s %4d  %s %s" % (n_, cnt, np.round(l_, 1).tolist(), np.round(h_, 1).tolist()))
print("== KABLO-KABLO")
ks = list(SEG)
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        if ks[i] not in sp.YOL and ks[j] not in sp.YOL: continue
        h = kesisim(SEG[ks[i]], SEG[ks[j]])
        if h: print("  #%d x #%d" % (ks[i], ks[j]), h[:3])
print("== AÇIK UZUNLUK (kanal dışı / 150 sonrası)")
KK = list(sp.KAN) + list(getattr(sp, "VAR_KANAL", []))
for ci in istc:
    z = zincir(SEG[ci]) if ci not in sp.YOL else SEG[ci]
    if not z: continue
    def kanalda(P, r):
        return any(np.all(P >= np.asarray(k["lo"]) - r - 3) and np.all(P <= np.asarray(k["hi"]) + r - 0 + 3) for k in KK)
    u0 = not kanalda(z[0][0], z[0][2]); u1 = not kanalda(z[-1][1], z[-1][2]) if len(z) else True
    if not (u0 or u1): u0 = u1 = True
    t, f = acik_uzunluk(z, KK, getattr(sp, "UC", {}).get(ci, (u0, u1)))
    print("  #%-4d %-28s açık %6.0f  fazla %6.0f %s" % (ci, KAY[ci]["prim"].split("__")[1], t, f, "<-- !" if f > 5 else ""))
