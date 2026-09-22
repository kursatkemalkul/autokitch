# -*- coding: utf-8 -*-
import os, pythoncom
from sw_lib import *
R = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\4_OVEN_v3"
sw.CloseAllDocuments(True)
e=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(os.path.join(R,"OVEN_v3.SLDASM"), 2, 0, "", e, w); mcall(d,"EditRebuild3")
print("acilis hata=%d uyari=%d" % (e.value, w.value))
f = mcall(d,"FirstFeature"); dl=[]
while f is not None:
    if mcall(f,"GetTypeName2")=="RefPlane": dl.append(f)
    f = mcall(f,"GetNextFeature")
d.ClearSelection2(True)
for x in dl: x.Select2(True,0)
try: mcall(d,"BlankRefGeom")
except Exception: pass
d.ClearSelection2(True)
png(d, os.path.join(R,"OVEN_v3_iso.png"), "*Isometric")
png(d, os.path.join(R,"OVEN_v3_on.png"), "*Front")
n=0
def gez(c):
    global n
    ch=list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: n+=1
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
print("OVEN v3 acik | bilesen: %d | hata=%d uyari=%d" % (n, e.value, w.value))
sw.Visible = True
