# -*- coding: utf-8 -*-
# TOPPING gorselleri: iso · on · yan · ic (cephe gizli)
import os, pythoncom
from sw_lib import *
R = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING"
d = sw.ActiveDoc
if d is None or "TOPPING" not in (d.GetTitle or ""):
    e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    d = sw.OpenDoc6(os.path.join(R,"TOPPING.SLDASM"), 2, 0, "", e, w)
mcall(d, "EditRebuild3")
f = mcall(d,"FirstFeature"); dl=[]
while f is not None:
    if mcall(f,"GetTypeName2")=="RefPlane": dl.append(f)
    f = mcall(f,"GetNextFeature")
d.ClearSelection2(True)
for x in dl: x.Select2(True,0)
try: mcall(d,"BlankRefGeom")
except Exception: pass
d.ClearSelection2(True)
png(d, os.path.join(R,"TOPPING_v28_iso.png"), "*Isometric")
png(d, os.path.join(R,"TOPPING_v28_on.png"), "*Front")
png(d, os.path.join(R,"TOPPING_v28_yan.png"), "*Right")
# ic gorunum: cephe/kapak/klape gizle
out=[]
def gez(c):
    ch=list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: out.append(c)
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
adlar = sorted(set(c.Name2.rsplit('-',1)[0] for c in out))
print("=== PARCA ADLARI (ilk 60) ===")
for a in adlar[:60]: print("  ", a)
print("toplam farkli ad:", len(adlar))
sw.Visible = True
