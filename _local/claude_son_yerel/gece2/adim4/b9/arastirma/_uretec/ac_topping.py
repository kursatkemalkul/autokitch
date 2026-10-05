# -*- coding: utf-8 -*-
# TOPPING montajini SolidWorks'te acik birak (Kemal kendi bakacak)
import os, pythoncom
from sw_lib import *
ASM = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\TOPPING.SLDASM"
sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(ASM, 2, 0, "", e, w)          # 0 = normal (salt-okunur degil), Kemal uzerinde calisabilsin
print("acilis hata=%d uyari=%d" % (e.value, w.value))
mcall(d, "EditRebuild3")
# referans duzlemlerini gizle
f = mcall(d, "FirstFeature"); dl = []
while f is not None:
    if mcall(f, "GetTypeName2") == "RefPlane": dl.append(f)
    f = mcall(f, "GetNextFeature")
d.ClearSelection2(True)
for x in dl: x.Select2(True, 0)
try: mcall(d, "BlankRefGeom")
except Exception: pass
d.ClearSelection2(True)
d.ShowNamedView2("*Isometric", 7); mcall(d, "ViewZoomtofit2")
n = 0
def gez(c):
    global n
    ch = list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: n += 1
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
print("TOPPING acik | bilesen: %d | hata=%d uyari=%d" % (n, e.value, w.value))
sw.Visible = True
