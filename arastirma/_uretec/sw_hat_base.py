# -*- coding: utf-8 -*-
# AUTOKITCH — BASE HAT MONTAJI (12 Eyl 2026)
#
# BASE = tek robotlu hat. Istasyonlar yan yana, hepsi 1970 yuksek x 840 derin:
#     STORE v4   2800   x    0.. 2800   4 kapi · K1 bolmeli (-18/+3) · 40 cekmece
#     PRESS v5    700   x 2800.. 3500   Fersah PZP-400
#     TOPPING v4  700   x 3500.. 4200   14 yuva · kaset celigi BORU (bos 7,54 kg)
#     OVEN v4     700   x 4200.. 4900   3 tas hazne · ortak havuz · camsiz sac kapak
#     PACK v3     700   x 4900.. 5600   sarjor 487 kutu
#   TOPLAM 5600 mm
#
# PICKUP ve SERVICE hatta DAHIL DEGIL — musteri tarafinda, ayri kabinler.
# ROBOT RAYI henuz modellenmedi (acik madde: robot turu / uc yeri / ray kotu).
#
# NOT: her istasyon kendi yerel koordinatinda x 0..W olarak modellenmistir;
# add_instance(offset_mm=(dx,0,0)) ile hat uzerine kaydirilir.
import os, sys, time
from sw_lib import *

ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma".replace("WEBSITE", "WEBS\u0130TE")
ROOT = os.path.join(ARA, "FULL_MAKINE")

# (klasor, montaj dosyasi, genislik mm, etiket)
HAT = (("1_STORE_v4",   "STORE_v4",   2800.0, "STORE"),
       ("2_PRESS_v5",   "PRESS_v5",    700.0, "PRESS"),
       ("3_TOPPING_v4", "TOPPING",     700.0, "TOPPING"),
       ("4_OVEN_v4",    "OVEN_v4",     700.0, "OVEN"),
       ("5_PACK_v3",    "PACK_v3",     700.0, "PACK"))


def kur():
    st = Station(ROOT, "HAT_BASE")
    x = 0.0
    print("BASE HAT — istasyon yerlesimi:")
    for klasor, asm, w, etiket in HAT:
        yol = os.path.join(ARA, klasor, asm + ".SLDASM")
        if not os.path.exists(yol):
            raise SystemExit("BULUNAMADI: " + yol)
        st.add_instance(yol, offset_mm=(x, 0.0, 0.0))
        print("  %-8s %-12s %6.0f mm   x %6.0f .. %-6.0f" % (etiket, asm, w, x, x + w))
        x += w
    print("  TOPLAM HAT UZUNLUGU: %.0f mm = %.2f m" % (x, x / 1000.0))
    st.assemble("HAT_BASE")
    return x


if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    kur()
    Station(ROOT, "x").exit_sw()
