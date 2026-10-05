import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "h3"))
import h3_elk_hat_v1 as EH
P, D, U = [], [], []
def ekle(ad, sh, mal, birim, bom=None): P.append((ad, sh))
EH.kur(ekle, D, U)
for ad, sh in P:
    b = sh.BoundingBox(); v = sh.Volume()
    if ad.startswith(("zemin", "ana_", "ust_hat_TOPPING", "ust_hat_gecis")): print("%-32s V %10.0f  %s valid=%s" % (ad, v, [round(t) for t in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)], sh.isValid()))
print(len(P), "parça ·", len(D), "delik")
sys.stdout.flush(); os._exit(0)
