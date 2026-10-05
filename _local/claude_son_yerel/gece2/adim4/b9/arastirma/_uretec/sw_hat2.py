# -*- coding: utf-8 -*-
# AUTOKITCH — HAT üst montajı: hazır istasyon alt montajlarını yan yana dizer (ön yüzler aynı düzlem, x ofsetleri) (7 Eyl 2026)
# kullanım: python sw_hat2.py STORE PRESS [TOPPING OVEN PACK]
import sys, os
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
SIRA = [("STORE", "1_STORE", 1400), ("PRESS", "2_PRESS", 700), ("TOPPING", "3_TOPPING", 700), ("OVEN", "4_OVEN", 700), ("PACK", "5_PACK", 700)]

sw.CloseAllDocuments(True)
istenen = sys.argv[1:] or [s[0] for s in SIRA]
sw.NewDocument(TPL_ASM, 0, 0, 0); asm = sw.ActiveDoc; x = 0.0
for name, folder, W in SIRA:
    if name not in istenen: x += W; continue
    path = os.path.join(ARA, folder, name + ".SLDASM")
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(path, 2, 1, "", e, w); bb = [1e9]*3 + [-1e9]*3
    for cpt in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        g = cpt.GetBox(False, False)
        for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
    c = [(bb[i]+bb[i+3])/2 for i in range(3)]
    if asm.AddComponent5(path, 0, "", False, "", c[0] + x*M, c[1], c[2]) is None: raise RuntimeError("alt montaj eklenemedi " + name)
    sw.CloseDoc(d.GetTitle); print("  %-8s bbox x %.0f..%.0f y %.0f..%.0f z %.0f..%.0f → ofset %.0f" % (name, bb[0]/M, bb[3]/M, bb[1]/M, bb[4]/M, bb[2]/M, bb[5]/M, x)); x += W
comps = list(asm.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
asm.ClearSelection2(True)
for cpt in comps: cpt.Select4(True, NUL, False)
mcall(asm, "FixComponent"); asm.ClearSelection2(True)
for cpt in comps: t = cpt.Transform2.ArrayData; print("  %-12s konum x=%5.0f y=%3.0f z=%3.0f" % (cpt.Name2, t[9]/M, t[10]/M, t[11]/M))
out = os.path.join(ARA, "FULL_MAKINE"); ok = saveas(asm, os.path.join(out, "HAT.SLDASM"))
png(asm, os.path.join(out, "HAT_asm_iso.png"), "*Isometric", 2000, 1000); png(asm, os.path.join(out, "HAT_asm_on.png"), "*Front", 2000, 900)
print("HAT.SLDASM kayit=%s, alt montaj=%d" % (ok, len(comps)))
asm.ShowNamedView2("*Isometric", 7); mcall(asm, "ViewZoomtofit2"); sw.FrameState = 2                      # 2 = maximize (1 = minimize idi)
