# -*- coding: utf-8 -*-
import os, pythoncom
from sw_lib import *
ASM = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\4_OVEN\OVEN.SLDASM"
sw.CloseAllDocuments(True)
e=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(ASM, 2, 1, "", e, w); mcall(d,"EditRebuild3")
print("acilis hata=%d uyari=%d" % (e.value, w.value))
o=[]
def gez(c):
    ch=list(c.GetChildren)
    if ch:
        for k in ch: gez(k)
    else: o.append(c)
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
bb=[1e9]*3+[-1e9]*3
sat=[]
for c in o:
    b=c.GetBox(False,False)
    if not b: continue
    for i in range(3): bb[i]=min(bb[i],b[i]); bb[i+3]=max(bb[i+3],b[i+3])
    b=[v*1000 for v in b]; sat.append((b[1], c.Name2.rsplit('-',1)[0].split('/')[-1], b))
print("bilesen: %d | dis olcu x %.0f..%.0f y %.0f..%.0f z %.0f..%.0f" % tuple([len(o)]+[v*1000 for v in bb]))
sat.sort()
print("%-40s %15s %17s %15s" % ("parca","x","y","z"))
for y,ad,b in sat:
    print("%-40s %6.1f..%-6.1f %7.1f..%-7.1f %6.1f..%-6.1f" % (ad,b[0],b[3],b[1],b[4],b[2],b[5]))
sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
