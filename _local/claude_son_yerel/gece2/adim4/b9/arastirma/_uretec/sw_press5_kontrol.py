# -*- coding: utf-8 -*-
# PRESS v5 — modelden olcu okuma + gorsel (kapali cephe / kapaklar acik)
import os, sys, pythoncom
from sw_lib import *
ARA  = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "2_PRESS_v5")
ASM  = os.path.join(ROOT, "PRESS_v5.SLDASM")

def leafs(c, out):
    ch = list(c.GetChildren)
    if ch:
        for k in ch: leafs(k, out)
    else: out.append(c)

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(ASM, 2, 1, "", e, w); mcall(d, "EditRebuild3")
    print("acilis hata=%d uyari=%d" % (e.value, w.value))
    root = d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True)
    comps = []; leafs(root, comps)
    bb = [1e9]*3 + [-1e9]*3; kutu = {}
    for c in comps:
        g = c.GetBox(False, False)
        if not g: continue
        kutu[c.Name2] = [v*1000 for v in g]
        for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
    print("=== DIS OLCU ===  x %.0f..%.0f  y %.0f..%.0f  z %.0f..%.0f" % tuple([v*1000 for v in bb]))
    print("toplam parca: %d" % len(comps))
    print("=== CEPHE PANELLERI (on plaka) ===")
    for n in sorted(kutu):
        if "panel_" in n and "_donus" not in n and "_agiz" not in n and "_mentese" not in n and "mandal" not in n:
            b = kutu[n]; print("  %-28s x %7.1f..%-7.1f y %7.1f..%-7.1f  (%.0f x %.0f)"
                               % (n.rsplit('-',1)[0], b[0], b[3], b[1], b[4], b[3]-b[0], b[4]-b[1]))
    print("=== BOLME ICERIGI ===")
    for anah in ("PZP400", "ROBOT_UCU_CATAL", "ROBOT_UCU_PENCE", "VANTUZ_D40", "UC_DOCK",
                 "uc_aski_plakasi", "cop_kutusu_59L", "atma_klapesi", "atma_hunisi", "raf_uc_sac", "raf_cop_sac"):
        for n in sorted(kutu):
            if anah in n:
                b = kutu[n]; print("  %-30s x %7.1f..%-7.1f y %7.1f..%-7.1f z %7.1f..%-7.1f"
                                   % (n.rsplit('-',1)[0], b[0], b[3], b[1], b[4], b[2], b[5]))
    # ---- gorsel: referans duzlemleri gizle
    fs = mcall(d, "FirstFeature"); dl = []
    while fs is not None:
        if mcall(fs, "GetTypeName2") == "RefPlane": dl.append(fs)
        fs = mcall(fs, "GetNextFeature")
    d.ClearSelection2(True)
    for f in dl: f.Select2(True, 0)
    try: mcall(d, "BlankRefGeom")
    except Exception: pass
    d.ClearSelection2(True)
    png(d, os.path.join(ROOT, "PRESS_v5_on.png"), "*Front")
    png(d, os.path.join(ROOT, "PRESS_v5_iso.png"), "*Isometric")
    # kapaklar gizli -> ic gorunum
    d.ClearSelection2(True); giz = 0
    for c in comps:
        if any(k in c.Name2 for k in ("panel_pres", "panel_cop", "panel_uc", "panel_atma", "panel_sag_bos")):
            c.Select4(True, NUL, False); giz += 1
    if giz: mcall(d, "HideComponent")
    d.ClearSelection2(True)
    png(d, os.path.join(ROOT, "PRESS_v5_ic_iso.png"), "*Isometric")
    print("gizlenen cephe parcasi:", giz)
    sw.CloseDoc(d.GetTitle)
    try: sw.ExitApp()
    except Exception: pass
