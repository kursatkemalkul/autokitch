# -*- coding: utf-8 -*-
# SILMEDEN ONCE: 7 montajin TUM bilesen adlarini topla, olu liste ile karsilastir.
# Bir formun adi herhangi bir montajda geciyorsa SILINMEZ.
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
MONTAJ = [("1_STORE_v3","STORE_v3"), ("2_PRESS_v5","PRESS_v5"), ("3_TOPPING","TOPPING"),
          ("4_OVEN_v3","OVEN_v3"), ("5_PACK_v3","PACK_v3"), ("6_PICKUP_v1","PICKUP_v1"),
          ("7_SERVICE_v1","SERVICE_v1")]
OLU = ["COP_KUTUSU_70L","FIRIN_KAPAK_CAM","HAMUR_TOPU_220g","KAP_YAG_14x68x24","KLAPE_KAT_TOPPING",
       "KUTU_BLANK_40x76","KUTU_KOLA_330ml","TEPSI_HAMUR_GN21","UC_YUVASI","YUVA_1L","YUVA_icecek",
       "KAP_14x68x24","KLAPE_H270","KLAPE_H410","L_RAF_CIFTI","L_RAF_CIFTI_PIMLI","SOKET_MOTOR",
       "PZP_ayak"]
e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
sw.CloseAllDocuments(True); sw.FrameState = 2
gecen = {}
for dd, ad in MONTAJ:
    d = sw.OpenDoc6(os.path.join(ARA, dd, ad + ".SLDASM"), 2, 1, "", e, w)
    mcall(d, "EditRebuild3"); adlar = []
    def gez(c):
        adlar.append(c.Name2)
        for k in (c.GetChildren or []): gez(k)
    gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
    for o in OLU:
        # KUTU_KOLA_330ml, KUTU_KOLA_330ml_DIK i ic ermemeli -> tam ad kontrolu
        for a in adlar:
            kok = a.split("-")[0]
            if kok == o or kok.startswith(o + "_") or ("/" + o) in a or a.startswith(o + "/"):
                gecen.setdefault(o, set()).add(ad); break
            if o == "PZP_ayak" and "PZP_ayak" in a:
                gecen.setdefault(o, set()).add(ad); break
    print("%-12s %4d bilesen" % (ad, len(adlar)))
    sw.CloseDoc(d.GetTitle)
print("\n===== SONUC =====")
for o in OLU:
    if o in gecen: print("  KULLANILIYOR  %-22s -> %s" % (o, ", ".join(sorted(gecen[o]))))
    else:          print("  olu           %-22s" % o)
try: sw.ExitApp()
except Exception: pass
