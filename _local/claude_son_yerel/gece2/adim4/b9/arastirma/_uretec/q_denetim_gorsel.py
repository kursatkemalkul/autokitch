# -*- coding: utf-8 -*-
# 6 istasyon: ic gorunum (on panel/kapak/sove gizli) + kapali on gorunus PNG.
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
OUT = os.path.join(ARA, "_denetim_10eyl")
os.makedirs(OUT, exist_ok=True)
GIZ = ("on_dis_sac", "on_pu", "on_ic_sac", "sove_", "cam_", "panel_pres", "panel_uc", "panel_cop",
       "panel_atma", "panel_sag_bos", "panel_pano", "panel_yag", "panel_mekanizma", "panel_egzoz",
       "panel_vakum", "panel_kalip", "panel_temizlik", "panel_ambalaj", "panel_teknik", "panel_cop",
       "KPK_", "FIRIN_KAPAK", "alin_saci", "dis_on")
HEDEF = [("2_PRESS_v5", "PRESS_v5"), ("3_TOPPING", "TOPPING"), ("4_OVEN_v3", "OVEN_v3"),
         ("5_PACK_v3", "PACK_v3"), ("6_PICKUP_v1", "PICKUP_v1"), ("7_SERVICE_v1", "SERVICE_v1")]
e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
sw.CloseAllDocuments(True); sw.FrameState = 2
for dd, ad in HEDEF:
    d = sw.OpenDoc6(os.path.join(ARA, dd, ad + ".SLDASM"), 2, 1, "", e, w)
    mcall(d, "EditRebuild3"); time.sleep(2)
    png(d, os.path.join(OUT, ad + "_kapali_iso.png"), "*Isometric", 1200, 1400)
    d.ClearSelection2(True); n = [0]
    def gez(c):
        for k in (c.GetChildren or []): gez(k)
        if any(g in c.Name2 for g in GIZ): c.Select4(True, NUL, False); n[0] += 1
    gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
    if n[0]: mcall(d, "HideComponent")
    d.ClearSelection2(True)
    png(d, os.path.join(OUT, ad + "_ic_on.png"), "*Front", 1200, 1500)
    png(d, os.path.join(OUT, ad + "_ic_iso.png"), "*Isometric", 1300, 1450)
    print("%-12s gizlenen %d" % (ad, n[0]))
    sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
print("bitti ->", OUT)
