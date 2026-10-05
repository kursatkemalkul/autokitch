# -*- coding: utf-8 -*-
# STORE v2: 24 V kablolari kasanin arkasina tasmisti -> 65 mm one al
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
S2 = os.path.join(ARA, "1_STORE_v2", "STORE_v2.SLDASM")
KAB = os.path.join(ARA, "_ortak", "KABLO_24V_D5", "KABLO_24V_D5.SLDASM")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
sw.CloseAllDocuments(True)
d = sw.OpenDoc6(S2, 2, 1, "", e, w); sw.FrameState = 2
mcall(d, "EditRebuild3"); time.sleep(2)
yer = []
d.ClearSelection2(True)
for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
    if c.Name2.startswith("KABLO_24V_D5"):
        b = c.GetBox(False, False); yer.append([(b[i]+b[i+3])/2 for i in range(3)])
        d.Extension.SelectByID2(c.Name2 + "@STORE_v2", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0)
if yer: d.Extension.DeleteSelection2(0)
d.ClearSelection2(True); print("cikarilan kablo:", len(yer))
dd = sw.OpenDoc6(KAB, 2, 1, "", e, w); n = 0
for c in yer:
    if d.AddComponent5(KAB, 0, "", False, "", c[0], c[1], c[2] - 0.030) is not None: n += 1
sw.CloseDoc(dd.GetTitle)
d.ClearSelection2(True)
for cp in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
    if cp.Name2.startswith("KABLO_24V_D5"): cp.Select4(True, NUL, False)
mcall(d, "FixComponent"); d.ClearSelection2(True)
mcall(d, "EditRebuild3"); time.sleep(2)
zmin = 1e9
def gez(c):
    global zmin
    ch = list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: zmin = min(zmin, c.GetBox(False, False)[2]/M)
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
e2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
print("yeniden eklenen: %d | en arka nokta z=%.1f | kayit=%s" % (n, zmin, bool(d.Save3(1, e2, w2))))
