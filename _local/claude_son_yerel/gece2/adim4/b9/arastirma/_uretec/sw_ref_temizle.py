# -*- coding: utf-8 -*-
# REFERANS TEMIZLIGI: montajlari ALTTAN USTE acip kaydeder -> "non-matching internal ID" uyarisi biter.
# Sebep: parca uretiminde eski dosya silinip ayni isimle yazildigi icin SolidWorks ic kimligi degisiyor;
#        ust montaj eski kimligi hatirliyor. Bir kez yeniden kaydetmek kimligi tazeler.
import os, sys, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
KAT = {
 "1": [os.path.join(ARA, "_ortak", d, d + ".SLDASM") for d in sorted(os.listdir(os.path.join(ARA, "_ortak")))]
      + [os.path.join(ARA, "3_TOPPING", "alt_montaj", d, d + ".SLDASM") for d in sorted(os.listdir(os.path.join(ARA, "3_TOPPING", "alt_montaj")))]
      + [os.path.join(ARA, "1_STORE", "cekmece", d, d + ".SLDASM") for d in sorted(os.listdir(os.path.join(ARA, "1_STORE", "cekmece")))],
 "2": [os.path.join(ARA, x) for x in ("2_PRESS/PRESS.SLDASM", "3_TOPPING/TOPPING.SLDASM", "4_OVEN/OVEN.SLDASM", "5_PACK/PACK.SLDASM")],
 "3": [os.path.join(ARA, "1_STORE", "STORE.SLDASM")],
 "4": [os.path.join(ARA, "FULL_MAKINE", "HAT.SLDASM")],
}
def coz(doc):
    """bastirilmis (suppressed) bileseni geri ac"""
    n = 0
    def gez(c):
        nonlocal n
        for k in c.GetChildren:
            try:
                if k.GetSuppression2() != 2: k.SetSuppression2(2); n += 1
            except Exception: pass
            gez(k)
    gez(doc.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True))
    return n

faz = sys.argv[1]
sw.CloseAllDocuments(True)
for yol in KAT[faz]:
    if not os.path.exists(yol): print("  yok:", os.path.basename(yol)); continue
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(yol, 2, 1, "", e, w)
    if d is None: print("  ACILAMADI:", os.path.basename(yol), "hata", e.value); continue
    ns = coz(d); mcall(d, "EditRebuild3"); time.sleep(1)
    ok = False
    try:
        e2 = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w2 = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        ok = bool(d.Save3(1, e2, w2))
    except Exception as ex: print("   kayit hatasi:", ex)
    print("  %-28s uyari=%-3s cozulen=%d kayit=%s" % (os.path.basename(yol), w.value, ns, ok))
    sw.CloseAllDocuments(True)
print("faz %s bitti" % faz)
