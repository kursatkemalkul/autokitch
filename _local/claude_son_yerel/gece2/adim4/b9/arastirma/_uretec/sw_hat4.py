# -*- coding: utf-8 -*-
# AUTOKITCH — HAT v4 (10 Eyl 2026): GUNCEL bes istasyonun toplu montaji.
# Eski FULL_MAKINE/HAT.SLDASM (9 Eyl) hala PRESS v2 / OVEN v2 / PACK v2 yi gosteriyordu.
#
# Hat dizilimi (x, mm) — dukkan planindaki "HAT 420" ile birebir:
#   STORE v3  1400 geniş   x    0 .. 1400
#   PRESS v5   700         x 1400 .. 2100
#   TOPPING    700         x 2100 .. 2800
#   OVEN v3    700         x 2800 .. 3500
#   PACK v3    700         x 3500 .. 4200
# PICKUP ve SERVICE hatta DEGIL (ayri uniteler) — bu montaja girmiyorlar.
import sys, os
from sw_lib import *

ARA  = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "FULL_MAKINE")

HAT = [("1_STORE_v3",  "STORE_v3",  0.0),
       ("2_PRESS_v5",  "PRESS_v5",  1400.0),
       ("3_TOPPING",   "TOPPING",   2100.0),
       ("4_OVEN_v3",   "OVEN_v3",   2800.0),
       ("5_PACK_v3",   "PACK_v3",   3500.0)]

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    st = Station(ROOT, "HAT_v4")
    for kls, ad, dx in HAT:
        st.add_instance(os.path.join(ARA, kls, ad + ".SLDASM"), offset_mm=(dx, 0.0, 0.0))
    st.assemble("HAT_v4")
