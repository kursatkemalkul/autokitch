# -*- coding: utf-8 -*-
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
T = os.path.join(ARA, "3_TOPPING", "TOPPING.SLDASM")
def ac(etiket):
    e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    d = sw.OpenDoc6(T, 2, 1, "", e, w); print("%-12s hata=%d uyari=%d" % (etiket, e.value, w.value)); return d
sw.CloseAllDocuments(True)
d = ac("acilis")
# once cocuklarin yollarini kontrol et
kok = d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True)
yok = [c.Name2 for c in kok.GetChildren if c.GetPathName and not os.path.exists(c.GetPathName)]
print("olu referans:", yok)
mcall(d, "ForceRebuild3", True); time.sleep(3)
e2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
print("zorla olustur + kayit:", bool(d.Save3(1, e2, w2)), "hata=", e2.value, "uyari=", w2.value)
sw.CloseAllDocuments(True); time.sleep(2)
d = ac("2. acilis")
sw.CloseAllDocuments(True)
