# -*- coding: utf-8 -*-
# 6 istasyonu TEK oturumda cakisma taramasi (STORE_v3 zaten tarandi).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sw_cakisma as C
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
HEDEF = [("2_PRESS_v5",   "PRESS_v5"),
         ("3_TOPPING",    "TOPPING"),
         ("4_OVEN_v3",    "OVEN_v3"),
         ("5_PACK_v3",    "PACK_v3"),
         ("6_PICKUP_v1",  "PICKUP_v1"),
         ("7_SERVICE_v1", "SERVICE_v1")]
ozet = []
for d, ad in HEDEF:
    yol = os.path.join(ARA, d, ad + ".SLDASM")
    print("\n" + "="*70); print(ad); print("="*70)
    try:
        b = C.tara(yol, ad)
        ozet.append((ad, len(b)))
    except Exception as e:
        print("  HATA:", e); ozet.append((ad, -1))
print("\n\n===== OZET =====")
for ad, n in ozet: print("  %-12s cakisma %s" % (ad, n if n >= 0 else "HATA"))
try: sw.ExitApp()
except Exception: pass
