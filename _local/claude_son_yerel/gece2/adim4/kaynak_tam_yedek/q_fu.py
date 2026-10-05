import sys, os
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.join(os.getcwd(), "h3"))
import h3_hesap_v1 as HS
import firin_tp10_cad_v10 as FT
FT.KOMP_ACIKLIK = (HS.KOMP_ACIKLIK_X[0], HS.KOMP_ACIKLIK_X[1], FT.KOMP_ACIKLIK[2], FT.KOMP_ACIKLIK[3])
import h3_firin_ust_v1 as FU
FU.kur()
FT.kur(ayak=False, plaka=False, uyarla=True)
import h3_kesme_v1 as KS
KS.modul()
import cadquery as cq
V = cq.Vector
F = [("FU:" + p["ad"], FU.dunya(p)) for p in FU.PARCALAR]
F += [("FT:" + p["ad"], (p["wp"].val() if hasattr(p["wp"], "val") else p["wp"])) for p in FT.PARCALAR if p.get("birim", "").startswith(("F_UST", "F_TP10_GOVDE"))]
K = [("KS:" + p["ad"], p["wp"].val().translate(V(4000, 0, 0))) for p in KS.PARCALAR if p["grup"] not in ("URUN", "URUN_IZ", "REF", "SPREY")]
for a, s in F[:3]: print(a, s.BoundingBox().xmin)
# fırın üstü kutu yağ seti ile F parçaları + K ↔ F
def bb(s): b = s.BoundingBox(); return b
def ov(A, B, p=0.05): return A.xmin < B.xmax - p and B.xmin < A.xmax - p and A.ymin < B.ymax - p and B.ymin < A.ymax - p and A.zmin < B.zmax - p and B.zmin < A.zmax - p
bul = []
for a, sa in K:
    A = bb(sa)
    if A.xmax < 3300: pass
    for c, sc in F:
        C = bb(sc)
        if not ov(A, C): continue
        v = sa.intersect(sc).Volume()
        if v > 0.5: bul.append((round(v, 1), a, c))
for x in sorted(bul, reverse=True)[:40]: print("CAK", x)
print("toplam", len(bul))
# kompresör tavası/ayaklar ↔ raf
for c, sc in F:
    if "komp" in c or "ust_raf" in c or "kiris" in c or "dikme" in c: 
        b = bb(sc); print("F", c, round(b.xmin), round(b.xmax), round(b.ymin), round(b.ymax), round(b.zmin), round(b.zmax))
