# -*- coding: utf-8 -*-
# 7 SERVICE v1 ic gorunumu: cephe panelleri + sag yan duvar gizlenir, banttaki her sey gorunur
import os, pythoncom
from sw_lib import *
R = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\6_PICKUP_v1"
sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4, 0)
d = sw.OpenDoc6(os.path.join(R, "PICKUP_v1.SLDASM"), 2, 1, "", e, w); mcall(d, "EditRebuild3")
out = []
def gez(c):
    ch = list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: out.append(c)
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
f = mcall(d, "FirstFeature"); dl = []
while f is not None:
    if mcall(f, "GetTypeName2") == "RefPlane": dl.append(f)
    f = mcall(f, "GetNextFeature")
d.ClearSelection2(True)
for x in dl: x.Select2(True, 0)
try: mcall(d, "BlankRefGeom")
except Exception: pass

def kes(giz, adlar):
    d.ClearSelection2(True); n = 0
    for c in out:
        if any(k in c.Name2 for k in giz): c.Select4(True, NUL, False); n += 1
    if n: mcall(d, "HideComponent")
    d.ClearSelection2(True)
    for ad, gor in adlar: png(d, os.path.join(R, ad), gor)
    return n

# 1) yalnizca cephe gizli -> raflar, bidonlar, tup, kova, cekmece gorunur
n1 = kes(("on_cerceve_2mm", "on_kapi_dis", "pano_kapagi"),
         [("PICKUP_v1_ic_iso.png", "*Isometric"), ("PICKUP_v1_ic_on.png", "*Front")])
# 2) ayrica sag yan duvar + sove gizli -> yandan kesit gibi bakis
n2 = kes(("dis_yan_sag", "yan_ic_2mm_sag", "yan_pu_sag", "dis_ust", "ust_pu", "ust_ic"),
         [("PICKUP_v1_ic_yan.png", "*Right")])
print("gizlenen: %d + %d" % (n1, n2))
sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
