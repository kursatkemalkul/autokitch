# -*- coding: utf-8 -*-
# SILME SONRASI: 7 montaj hatasiz aciliyor mu, kayip referans var mi?
import os, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
MONTAJ = [("1_STORE_v3","STORE_v3"), ("2_PRESS_v5","PRESS_v5"), ("3_TOPPING","TOPPING"),
          ("4_OVEN_v3","OVEN_v3"), ("5_PACK_v3","PACK_v3"), ("6_PICKUP_v1","PICKUP_v1"),
          ("7_SERVICE_v1","SERVICE_v1")]
sw.CloseAllDocuments(True); sw.FrameState = 2
tum_ok = True
for dd, ad in MONTAJ:
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ARA, dd, ad + ".SLDASM"), 2, 1, "", e, w)
    hata, uyari = e.value, w.value
    mcall(d, "EditRebuild3")
    kayip = []
    def gez(c):
        try:
            if c.GetSuppression2 == 0 or c.IsSuppressed(): pass
        except Exception: pass
        try:
            if not os.path.exists(c.GetPathName()): kayip.append(c.Name2)
        except Exception: pass
        for k in (c.GetChildren or []): gez(k)
    gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
    ok = (hata == 0 and not kayip)
    tum_ok = tum_ok and ok
    print("%-12s acilis hata=%d uyari=%d · kayip referans=%d  %s" % (ad, hata, uyari, len(kayip), "OK" if ok else "!!!"))
    for k in kayip[:6]: print("     KAYIP:", k)
    sw.CloseDoc(d.GetTitle)
print("\nHEPSI TEMIZ" if tum_ok else "\nSORUN VAR")
try: sw.ExitApp()
except Exception: pass
