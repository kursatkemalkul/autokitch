# -*- coding: utf-8 -*-
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
sw.CloseAllDocuments(True)
d = sw.OpenDoc6(os.path.join(ARA, "FULL_MAKINE", "HAT.SLDASM"), 2, 1, "", e, w)
mcall(d, "EditRebuild3"); time.sleep(3)
top = [0]; par = set()
def gez(c, lv):
    for k in c.GetChildren:
        top[0] += 1
        if k.GetPathName: par.add(os.path.basename(k.GetPathName).lower())
        gez(k, lv+1)
kok = d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True)
for st in kok.GetChildren:
    n = [0]
    def g2(c):
        for k in c.GetChildren: n[0] += 1; g2(k)
    g2(st); print("  %-12s %4d bilesen" % (st.Name2.rsplit('-',1)[0], n[0]))
gez(kok, 0)
print("HAT toplam bilesen: %d | benzersiz dosya: %d" % (top[0], len(par)))
sw.CloseDoc(d.GetTitle)
