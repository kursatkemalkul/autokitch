# -*- coding: utf-8 -*-
# STORE v2 gorseller: referans duzlemleri gizle, 3 cekmece ac, on + ic gorunum
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
R = os.path.join(ARA, "1_STORE_v2"); NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(os.path.join(R, "STORE_v2.SLDASM"), 2, 0, "", e, w); sw.Visible = True; sw.FrameState = 2
mcall(d, "EditRebuild3"); time.sleep(3)
d.ClearSelection2(True); n = 0
f = mcall(d, "FirstFeature")
while f is not None:
    if mcall(f, "GetTypeName2") == "RefPlane": d.Extension.SelectByID2(f.Name, "PLANE", 0.0,0.0,0.0, True, 0, NUL_, 0); n += 1
    f = mcall(f, "GetNextFeature")
if n: mcall(d, "BlankRefGeom")
d.ClearSelection2(True)
ad = [i for i in range(1, 20) if d.Parameter("D1@LimitDistance%d" % i) is not None]
for i in ad[:4]: d.Parameter("D1@LimitDistance%d" % i).SystemValue = 0.5
mcall(d, "EditRebuild3"); time.sleep(2)
png(d, os.path.join(R, "STORE_v2_icerik_iso.png"), "*Isometric", 1600, 1000)
for i in ad[:4]: d.Parameter("D1@LimitDistance%d" % i).SystemValue = 0.0
mcall(d, "EditRebuild3"); time.sleep(1)
png(d, os.path.join(R, "STORE_v2_on.png"), "*Front", 1100, 1400)
e2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
print("duzlem gizlendi=%d | olcu=%d | kayit=%s | hata=%d uyari=%d" % (n, len(ad), bool(d.Save3(1, e2, w2)), e.value, w.value))
