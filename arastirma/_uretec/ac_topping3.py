# -*- coding: utf-8 -*-
# TOPPING v29 gorselleri: iso · on · klapesiz ic
import os, pythoncom
from sw_lib import *
R = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING"
sw.CloseAllDocuments(True)
e=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(os.path.join(R,"TOPPING.SLDASM"), 2, 0, "", e, w); mcall(d,"EditRebuild3")
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
png(d, os.path.join(R,"TOPPING_v29_iso.png"), "*Isometric")
png(d, os.path.join(R,"TOPPING_v29_on.png"), "*Front")
out=[]
def gez(c):
    ch=list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: out.append(c)
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
print("toplam bilesen:", len(out))
# klapeler + sag sove gizli -> ic gorunum
d.ClearSelection2(True); n=0
for c in out:
    if c.Name2.startswith(("KLAPE_H270","BORU_MOTOR","TOPPING_sove_sag","TOPPING_dis_yan_sag")):
        c.Select4(True,NUL,False); n+=1
if n: mcall(d,"HideComponent")
d.ClearSelection2(True)
png(d, os.path.join(R,"TOPPING_v29_klapesiz_iso.png"), "*Isometric")
print("gizlenen:", n)
sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
