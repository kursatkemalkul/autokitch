# -*- coding: utf-8 -*-
# STORE_v3 montaj agaci: ust seviye bilesenler ve her birinin yaprak sayisi.
import os, pythoncom, collections
from sw_lib import *
R = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE_v3"
sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
d = sw.OpenDoc6(os.path.join(R, "STORE_v3.SLDASM"), 2, 1, "", e, w)
mcall(d, "EditRebuild3")

def yaprak(c):
    ch = list(c.GetChildren)
    if not ch: return 1
    return sum(yaprak(k) for k in ch)

kok = d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True)
say = collections.Counter(); yap = collections.Counter()
for c in kok.GetChildren:
    ad = c.Name2.split("-")[0]
    say[ad] += 1; yap[ad] += yaprak(c)
top = 0
for ad in sorted(say, key=lambda k: -yap[k]):
    if yap[ad] < 6 and say[ad] < 3: continue
    print("  %-28s ornek %3d   yaprak %5d" % (ad, say[ad], yap[ad]))
    top += yap[ad]
print("  ... listelenen yaprak: %d / toplam %d" % (top, sum(yap.values())))
print("  ust seviye bilesen: %d · toplam yaprak: %d" % (sum(say.values()), sum(yap.values())))
sw.CloseDoc(d.GetTitle)
try: sw.ExitApp()
except Exception: pass
