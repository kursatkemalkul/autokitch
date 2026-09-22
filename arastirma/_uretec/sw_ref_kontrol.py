# -*- coding: utf-8 -*-
# KONTROL: kaydetmeden ac, uyari bayraklarini yaz (1=ID uyusmazligi, 32=yeniden olusturma gerekli)
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
AD = {1: "ID uyusmazligi", 2: "surum farki", 4: "salt okunur", 8: "paylasimda", 16: "referans yok", 32: "yeniden olusturma gerekli", 128: "kaydedilmemis"}
sw.CloseAllDocuments(True)
import sys
if len(sys.argv) > 1 and sys.argv[1] == "alt":
    A = os.path.join(ARA, "3_TOPPING", "alt_montaj"); HEDEF = [os.path.join(A, d, d + ".SLDASM") for d in sorted(os.listdir(A))]
else:
    HEDEF = [os.path.join(ARA, x) for x in ("1_STORE/STORE.SLDASM", "1_STORE_v2/STORE_v2.SLDASM", "1_STORE_v3/STORE_v3.SLDASM", "2_PRESS/PRESS.SLDASM", "3_TOPPING/TOPPING.SLDASM",
                                            "4_OVEN/OVEN.SLDASM", "5_PACK/PACK.SLDASM", "FULL_MAKINE/HAT.SLDASM")]
for yol in HEDEF:
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(yol, 2, 1, "", e, w); time.sleep(1)
    b = [AD[k] for k in AD if w.value & k]
    print("  %-16s hata=%d uyari=%d %s" % (os.path.basename(yol), e.value, w.value, ("-> " + ", ".join(b)) if b else "TEMIZ"))
    sw.CloseAllDocuments(True)
