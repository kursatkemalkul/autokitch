# -*- coding: utf-8 -*-
# STORE v2: tum cekmeceler kizak baglantisi (0-600) + 2 klape mentese baglantisi
import os, time, pythoncom
from sw_lib import *
import sw_store_v2 as V
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
def sec(d, ad, tur, mark=0, ekle=False): return d.Extension.SelectByID2(ad, tur, 0.0, 0.0, 0.0, ekle, mark, NUL_, 0)
def refd(d, kaynak, ofs):
    d.ClearSelection2(True); sec(d, kaynak, "PLANE")
    f = d.FeatureManager.InsertRefPlane(8, ofs*M, 0, 0, 0, 0); d.ClearSelection2(True); return f
def mate(d, a, b, tip, ust=0.0):
    d.ClearSelection2(True)
    if not sec(d, a, "PLANE", 1, False): return None
    if not sec(d, b, "PLANE", 1, True): return None
    h = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4, 0)
    m = d.AddMate5(tip, 2, False, 0.0, ust*M, 0.0, 0, 0, 0, 0, 0, False, False, 0, h)
    d.ClearSelection2(True); return m

sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(os.path.join(V.ROOT, "STORE_v2.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
mcall(d, "EditRebuild3"); time.sleep(2)
comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
# --- cekmeceler ---
n = 0
for c in comps:
    if not c.Name2.startswith("CEKMECE2_"): continue
    ad = c.Name2 + "@STORE_v2"; t = c.Transform2.ArrayData; tx, ty = t[9]/M, t[10]/M
    d.ClearSelection2(True); sec(d, ad, "COMPONENT"); mcall(d, "UnfixComponent"); d.ClearSelection2(True)
    px = refd(d, "Right Plane", tx); py = refd(d, "Top Plane", ty)
    m1 = mate(d, px.Name, "Right Plane@" + ad, 0); m2 = mate(d, py.Name, "Top Plane@" + ad, 0)
    m3 = mate(d, "Front Plane", "Front Plane@" + ad, 5, 600.0)
    n += 1 if (m1 and m2 and m3) else 0
    print("  %-22s x=%6.1f y=%7.1f %s%s%s" % (c.Name2, tx, ty, "1" if m1 else "-", "1" if m2 else "-", "1" if m3 else "-"))
# --- klapeler ---
for c in comps:
    if not c.Name2.startswith("KLAPE2_"): continue
    ad = c.Name2 + "@STORE_v2"; t = c.Transform2.ArrayData; x0, y0 = t[9]/M, t[10]/M
    d.ClearSelection2(True); sec(d, ad, "COMPONENT"); mcall(d, "UnfixComponent"); d.ClearSelection2(True)
    o1 = d.Extension.SelectByRay((x0+300)*M, (y0+2)*M, -0.004, 0.0, 1.0, 0.0, 0.002, 2, False, 1, 0)
    o2 = d.Extension.SelectByRay((x0+28)*M, (y0+2)*M, -0.004, 0.0, 1.0, 0.0, 0.002, 2, True, 1, 0)
    h = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4, 0)
    m1 = d.AddMate5(1, 0, False, 0.0,0.0,0.0, 0,0,0,0,0, False, False, 0, h); d.ClearSelection2(True)
    px = refd(d, "Right Plane", x0)
    m2 = mate(d, px.Name, "Right Plane@" + ad, 0)
    print("  %-22s x=%6.1f y=%7.1f secim=%s/%s esmerkez=%s cakisik=%s" % (c.Name2, x0, y0, o1, o2, "OK" if m1 else "HATA", "OK" if m2 else "HATA"))
mcall(d, "EditRebuild3"); time.sleep(3)
hr = [c.Name2 for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren if not c.IsFixed]
print("  hareketli: %d" % len(hr))
e2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
print("  kayit:", bool(d.Save3(1, e2, w2)))
