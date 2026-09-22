# -*- coding: utf-8 -*-
# HAT: STORE v1 -> STORE_v3 (contali) degisimi
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
HAT = os.path.join(ARA, "FULL_MAKINE", "HAT.SLDASM")
V2 = os.path.join(ARA, "1_STORE_v3", "STORE_v3.SLDASM")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
sw.CloseAllDocuments(True)
d = sw.OpenDoc6(HAT, 2, 1, "", e, w); sw.FrameState = 2
mcall(d, "EditRebuild3"); time.sleep(3)
print("acilis hata=%d uyari=%d" % (e.value, w.value))
d.ClearSelection2(True); n = 0
for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
    if c.Name2.rsplit("-", 1)[0] in ("STORE", "STORE_v2"):
        d.Extension.SelectByID2(c.Name2 + "@HAT", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0); n += 1
if n: d.Extension.DeleteSelection2(0)
d.ClearSelection2(True); print("cikarilan STORE v1:", n)
dd = sw.OpenDoc6(V2, 2, 1, "", e, w)
bb = [1e9]*3 + [-1e9]*3
for cp in dd.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
    g = cp.GetBox(False, False)
    for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
c = [(bb[i]+bb[i+3])/2 for i in range(3)]
ok = d.AddComponent5(V2, 0, "", False, "", c[0], c[1], c[2])
sw.CloseDoc(dd.GetTitle)
print("STORE_v3 eklendi:", ok is not None)
d.ClearSelection2(True)
for cp in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
    if cp.Name2.startswith("STORE_v3"): cp.Select4(True, NUL, False)
mcall(d, "FixComponent"); d.ClearSelection2(True)
mcall(d, "EditRebuild3"); time.sleep(3)
for cp in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
    t = cp.Transform2.ArrayData; b = cp.GetBox(False, False)
    print("  %-14s x %6.0f..%-6.0f y %5.0f..%-5.0f z %6.0f..%-6.0f" % (cp.Name2, b[0]/M, b[3]/M, b[1]/M, b[4]/M, b[2]/M, b[5]/M))
e2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
print("toplam bilesen: %d | kayit: %s" % (d.GetComponentCount(False), bool(d.Save3(1, e2, w2))))
png(d, os.path.join(ARA, "FULL_MAKINE", "HAT_v3_iso.png"), "*Isometric", 2000, 1150)
