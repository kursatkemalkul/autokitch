# -*- coding: utf-8 -*-
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
TMP = os.path.join(os.environ['TEMP'], 'sw_deney'); os.makedirs(TMP, exist_ok=True)
ALT = os.path.join(ARA, "3_TOPPING", "alt_montaj"); PD = os.path.join(ARA, "3_TOPPING", "parca")
def kur(ad, yollar):
    sw.CloseAllDocuments(True)
    sw.NewDocument(TPL_ASM, 0, 0, 0); asm = sw.ActiveDoc
    for yol in yollar:
        e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
        d = sw.OpenDoc6(yol, 2 if yol.lower().endswith('.sldasm') else 1, 1, "", e, w)
        asm.AddComponent5(yol, 0, "", False, "", 0.0, 0.0, 0.0)
        sw.CloseDoc(d.GetTitle)
    p = os.path.join(TMP, ad + ".SLDASM")
    if os.path.exists(p): os.remove(p)
    e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    asm.Extension.SaveAs3(p, 0, 1, NUL, NUL, e, w)
    sw.CloseAllDocuments(True); time.sleep(1)
    e2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    d = sw.OpenDoc6(p, 2, 1, "", e2, w2)
    print("  %-12s (%d ogesi) -> hata=%d uyari=%d %s" % (ad, len(yollar), e2.value, w2.value, "ID UYUSMAZLIGI" if w2.value & 1 else "temiz"))
    sw.CloseAllDocuments(True)
altlar = [os.path.join(ALT, d, d + ".SLDASM") for d in sorted(os.listdir(ALT))]
parcalar = [os.path.join(PD, f) for f in sorted(os.listdir(PD)) if f.lower().endswith('.sldprt')][:10]
kur("D_ALT", altlar)
kur("D_PARCA", parcalar)
for a in altlar: kur("D_" + os.path.basename(a)[:8], [a])
