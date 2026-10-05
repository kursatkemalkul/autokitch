# -*- coding: utf-8 -*-
# kat1 robot agzinin SOL KOSESI: bolge disindaki her sey gizlenip tam kadraj
import os, time, pythoncom
from sw_lib import *
R = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING"
sw.CloseAllDocuments(True)
e=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(os.path.join(R,"TOPPING.SLDASM"), 2, 0, "", e, w); mcall(d,"EditRebuild3")
f = mcall(d,"FirstFeature"); dl=[]
while f is not None:
    if mcall(f,"GetTypeName2")=="RefPlane": dl.append(f)
    f = mcall(f,"GetNextFeature")
d.ClearSelection2(True)
for x in dl: x.Select2(True,0)
try: mcall(d,"BlankRefGeom")
except Exception: pass
d.ClearSelection2(True)
o=[]
def gez(c):
    ch=list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: o.append(c)
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
# ilgi bolgesi: sol yarim, kat1 agzi ve alt/ust kapak kenarlari
X0,X1,Y0_,Y1_,Z0,Z1 = -10.0, 260.0, 1500.0, 1760.0, -140.0, 45.0
d.ClearSelection2(True); giz=0
for c in o:
    b=c.GetBox(False,False)
    if not b: continue
    b=[v*1000 for v in b]
    if not (b[0]<X1 and b[3]>X0 and b[1]<Y1_ and b[4]>Y0_ and b[2]<Z1 and b[5]>Z0):
        c.Select4(True,NUL,False); giz+=1
if giz: mcall(d,"HideComponent")
d.ClearSelection2(True)
png(d, os.path.join(R,"AGIZ_kose_iso.png"), "*Isometric", 1700, 1150)
png(d, os.path.join(R,"AGIZ_kose_on.png"), "*Front", 1700, 1150)
print("gizlenen:", giz, "| gorunen:", len(o)-giz)
sw.Visible = True
