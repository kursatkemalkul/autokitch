# -*- coding: utf-8 -*-
# HAT: on panelleri (klape / kapak / cekmece on yuzu / sove / cam kapak) gizleyip ic gorunum
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
HAT = os.path.join(ARA, "FULL_MAKINE", "HAT.SLDASM")
GIZ = ("klape", "KLAPE", "kapak", "on_dis_sac", "on_pu", "on_ic_sac", "sove", "cam_", "panel_ust", "kapi")
e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
sw.CloseAllDocuments(True)
d = sw.OpenDoc6(HAT, 2, 1, "", e, w); sw.FrameState = 2
mcall(d, "EditRebuild3"); time.sleep(4)
d.ClearSelection2(True); n = [0]
def gez(c):
    ch = c.GetChildren
    if ch:
        for k in ch: gez(k)
    if any(g in c.Name2 for g in GIZ): c.Select4(True, NUL, False); n[0] += 1
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
if n[0]: mcall(d, "HideComponent")
d.ClearSelection2(True); print("gizlenen:", n[0])
png(d, os.path.join(ARA, "FULL_MAKINE", "HAT_son_acik_iso.png"), "*Isometric", 2000, 1150)
png(d, os.path.join(ARA, "FULL_MAKINE", "HAT_son_acik_on.png"), "*Front", 2200, 1040)
sw.CloseDoc(d.GetTitle)
print("bitti")
