# -*- coding: utf-8 -*-
# kat1 robot agzinin SOL UST kosesindeki her parcayi listele
import os, pythoncom
from sw_lib import *
ASM = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\TOPPING.SLDASM"
sw.CloseAllDocuments(True)
e=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(ASM, 2, 1, "", e, w); mcall(d,"EditRebuild3")
o=[]
def gez(c):
    ch=list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: o.append(c)
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
# ilgi kutusu: sol kenar, kat1 robot agzi (1572..1689) ve hemen etrafi, on bolge
X0,X1, Y0_,Y1_, Z0,Z1 = -5.0, 130.0, 1540.0, 1720.0, -70.0, 45.0
sat=[]
for c in o:
    b=c.GetBox(False,False)
    if not b: continue
    b=[v*1000 for v in b]
    if b[0]<X1 and b[3]>X0 and b[1]<Y1_ and b[4]>Y0_ and b[2]<Z1 and b[5]>Z0:
        sat.append((b[5], c.Name2.rsplit('-',1)[0].split('/')[-1], b))
sat.sort(key=lambda t:-t[0])
print("kat1 ROBOT AGZI = y 1572..1689 | sove x 0..30 | hucre ici x 42,5")
print("%-34s %16s %18s %16s" % ("parca","x","y","z"))
print("-"*92)
for z1, ad, b in sat:
    print("%-34s %7.1f..%-7.1f %8.1f..%-8.1f %7.1f..%-7.1f" % (ad,b[0],b[3],b[1],b[4],b[2],b[5]))
sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
