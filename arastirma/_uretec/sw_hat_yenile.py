# -*- coding: utf-8 -*-
# HAT.SLDASM: guncel istasyonlarla yeniden olustur -> gorseller
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
HAT = os.path.join(ARA, "FULL_MAKINE", "HAT.SLDASM")
e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
sw.CloseAllDocuments(True)
d = sw.OpenDoc6(HAT, 2, 1, "", e, w); sw.FrameState = 2
print("acildi, hata=%s uyari=%s" % (e.value, w.value))
mcall(d, "EditRebuild3"); time.sleep(4)
kok = d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True)
for c in kok.GetChildren:
    t = c.Transform2.ArrayData; b = c.GetBox(False, False)
    print("  %-28s x=%6.0f  |  x %.0f..%.0f  y %.0f..%.0f  z %.0f..%.0f" %
          (c.Name2, t[9]/M, b[0]/M, b[3]/M, b[1]/M, b[4]/M, b[2]/M, b[5]/M))
print("toplam bilesen:", d.GetComponentCount(True))
for v, ad in (("*Isometric", "HAT_son_iso"), ("*Front", "HAT_son_on")):
    png(d, os.path.join(ARA, "FULL_MAKINE", ad + ".png"), v, 1800, 900)
print("kayit:", saveas(d, HAT))
