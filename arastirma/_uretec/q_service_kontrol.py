# -*- coding: utf-8 -*-
import os, sys, pythoncom
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sw_cakisma as C
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
yol = os.path.join(ARA, "7_SERVICE_v1", "SERVICE_v1.SLDASM")
sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
d = sw.OpenDoc6(yol, 2, 1, "", e, w)
print("acilis: hata=%d uyari=%d" % (e.value, w.value))
# uyari kodunu coz
BIT = {1:"IdMismatch", 2:"ReadOnly", 4:"SharingViolation", 8:"DrawingShapeChanged",
       16:"DrawingSFSymbolNotFound", 32:"ViewMissingRefConfig", 64:"ViewOnlyRestrictions",
       128:"MissingExternalRefs", 256:"ModelOutOfDate", 512:"AlreadyOpen", 1024:"BasePartNotLoaded"}
print("  cozum:", " + ".join(v for k, v in BIT.items() if w.value & k) or "-")
mcall(d, "EditRebuild3")
n = [0]; hatali = []
def gez(c):
    n[0] += 1
    try:
        if c.GetSuppression2 == 2 and not c.IsSuppressed(): pass
    except Exception: pass
    for k in (c.GetChildren or []): gez(k)
gez(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
print("  bilesen dugumu:", n[0])
sw.CloseDoc(d.GetTitle)
C.tara(yol, "SERVICE_v1")
try: sw.ExitApp()
except Exception: pass
