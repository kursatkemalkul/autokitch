# -*- coding: utf-8 -*-
# Bes istasyonun EN ON YUZEY kotunu ve on yuz sandvic yapisini modelden oku
import os, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
IST = [("STORE v3", "1_STORE_v3", "STORE_v3.SLDASM"),
       ("PRESS v5", "2_PRESS_v5", "PRESS_v5.SLDASM"),
       ("TOPPING",  "3_TOPPING",  "TOPPING.SLDASM"),
       ("OVEN",     "4_OVEN",     "OVEN.SLDASM"),
       ("PACK",     "5_PACK",     "PACK.SLDASM")]
sw.CloseAllDocuments(True)
def leafs(c, o):
    ch = list(c.GetChildren)
    if ch:
        for k in ch: leafs(k, o)
    else: o.append(c)
print("%-10s | %8s | %8s | on yuz parcasi (en ondeki)" % ("istasyon", "max z", "sove z1"))
print("-"*78)
for ad, kls, dosya in IST:
    yol = os.path.join(ARA, kls, dosya)
    if not os.path.exists(yol): print("%-10s | dosya yok" % ad); continue
    e=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w=VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    d = sw.OpenDoc6(yol, 2, 1, "", e, w)
    o=[]; leafs(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True), o)
    mz = -1e9; onde = []; sovez = None
    for c in o:
        b = c.GetBox(False, False)
        if not b: continue
        z1 = b[5]*1000
        if z1 > mz + 0.01: mz = z1; onde = [c.Name2.rsplit('-',1)[0].split('/')[-1]]
        elif abs(z1 - mz) < 0.01 and len(onde) < 4: onde.append(c.Name2.rsplit('-',1)[0].split('/')[-1])
        if "sove" in c.Name2 and sovez is None: sovez = z1
    print("%-10s | %8.1f | %8s | %s" % (ad, mz, ("%.1f" % sovez) if sovez else "-", ", ".join(sorted(set(onde))[:3])))
    sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
