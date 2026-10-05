# -*- coding: utf-8 -*-
import os, pythoncom
from sw_lib import *
ASM = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\2_PRESS_v5\PRESS_v5.SLDASM"
sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(ASM, 2, 1, "", e, w); mcall(d, "EditRebuild3")
out=[]
def gez(c):
    ch=list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: out.append(c)
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
print("=== COP KUTUSU PARCALARI ===")
for c in out:
    b=c.GetBox(False,False)
    if not b: continue
    b=[v*1000 for v in b]
    if "cop_" in c.Name2:
        print("  %-34s x %6.1f..%-6.1f y %7.1f..%-7.1f z %7.1f..%-7.1f" % (c.Name2.rsplit('-',1)[0],b[0],b[3],b[1],b[4],b[2],b[5]))
print("=== KOVA AGZININ USTUNDEKI HACIMDE (x 60..440, y 1657..1700, z -680..-80) NE VAR ===")
n=0
for c in out:
    b=c.GetBox(False,False)
    if not b: continue
    b=[v*1000 for v in b]
    if b[0]<440 and b[3]>60 and b[1]<1700 and b[4]>1657 and b[2]<-80 and b[5]>-680:
        n+=1; print("  %-34s x %6.1f..%-6.1f y %7.1f..%-7.1f z %7.1f..%-7.1f" % (c.Name2.rsplit('-',1)[0],b[0],b[3],b[1],b[4],b[2],b[5]))
print("  toplam:", n)
sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
