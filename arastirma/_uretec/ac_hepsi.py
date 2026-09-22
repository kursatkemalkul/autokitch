# -*- coding: utf-8 -*-
# Yedi unitenin montajini SIRAYLA acar, ref duzlemlerini gizler, on + izometrik goruntu alir
# ve ACIK BIRAKIR. (Butun istasyonlar ayni SolidWorks oturumunda kalir.)
import os, pythoncom
from sw_lib import *

ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
UNITE = [("1_STORE_v3",   "STORE_v3"),
         ("2_PRESS_v5",   "PRESS_v5"),
         ("3_TOPPING",    "TOPPING"),
         ("4_OVEN_v3",    "OVEN_v3"),
         ("5_PACK_v3",    "PACK_v3"),
         ("6_PICKUP_v1",  "PICKUP_v1"),
         ("7_SERVICE_v1", "SERVICE_v1")]

sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
for kls, ad in UNITE:
    R = os.path.join(ARA, kls)
    d = sw.OpenDoc6(os.path.join(R, ad + ".SLDASM"), 2, 0, "", e, w)
    mcall(d, "EditRebuild3")
    f = mcall(d, "FirstFeature"); dl = []
    while f is not None:
        if mcall(f, "GetTypeName2") == "RefPlane": dl.append(f)
        f = mcall(f, "GetNextFeature")
    d.ClearSelection2(True)
    for x in dl: x.Select2(True, 0)
    try: mcall(d, "BlankRefGeom")
    except Exception: pass
    d.ClearSelection2(True)
    png(d, os.path.join(R, ad + "_on.png"),  "*Front")
    png(d, os.path.join(R, ad + "_iso.png"), "*Isometric")
    n = 0
    def gez(c):
        global n
        ch = list(c.GetChildren)
        if ch:
            for k in ch: gez(k)
        else: n += 1
    gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
    print("%-12s acik | bilesen %5d | hata=%d uyari=%d" % (ad, n, e.value, w.value))
sw.Visible = True
print("YEDI UNITE DE ACIK")
