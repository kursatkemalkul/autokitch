# -*- coding: utf-8 -*-
import os, sys, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
TIP = {0:"Coincident",1:"Concentric",2:"Perpendicular",3:"Parallel",4:"Tangent",5:"Distance",6:"Angle",13:"Symmetric",14:"Cam",15:"Width",16:"Gear",17:"Hinge",25:"Slot"}
yol = sys.argv[1]
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
sw.CloseAllDocuments(True)
d = sw.OpenDoc6(yol, 2, 1, "", e, w); mcall(d, "EditRebuild3"); time.sleep(2)
kok = d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True)
sabit = hareketli = 0; ornek = []
for c in kok.GetChildren:
    if c.IsFixed: sabit += 1
    else:
        hareketli += 1
        if len(ornek) < 12: ornek.append(c.Name2)
print("%s: sabit=%d  hareketli=%d" % (os.path.basename(yol), sabit, hareketli))
if ornek: print("  hareketli ornekler:", ", ".join(ornek))
# mate listesi
f = mcall(d, "FirstFeature"); n = 0; lim = []
while f is not None:
    tn = mcall(f, "GetTypeName2")
    if tn == "MateGroup":
        sf = mcall(f, "GetFirstSubFeature")
        while sf is not None:
            m = mcall(sf, "GetSpecificFeature2")
            try:
                t = m.Type; mn = sf.Name
                n += 1
                if t == 5:
                    lim.append((mn, m.MinimumVariation*1000 if m.CanBeFlipped is not None else 0, m.MaximumVariation*1000, m.DisplayDimension2(0).GetDimension2(0).SystemValue*1000 if m.DisplayDimension2(0) else 0))
            except Exception: pass
            sf = mcall(sf, "GetNextSubFeature")
    f = mcall(f, "GetNextFeature")
print("  toplam mate: %d | mesafe(limit) mate: %d" % (n, len(lim)))
for mn, a, b, v in lim[:20]: print("    %-24s min=%.0f max=%.0f su an=%.0f mm" % (mn, a, b, v))
sw.CloseAllDocuments(True)
