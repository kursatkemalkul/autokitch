# -*- coding: utf-8 -*-
# AUTOKITCH — 2 · PRESS v2: ortak alt montajlar (TEPSI Ø320 ×3, UC_YUVASI ×3) + kasa parçaları → PRESS.SLDASM (7 Eyl 2026)
# fazlar: ortak → asm   (kasa parçaları sw_all.press() ile üretilmiş, 2_PRESS/parca'da)
import sys, os
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "2_PRESS"); ORTAK = os.path.join(ARA, "_ortak")

def tepsi():
    """ortak pide tepsisi Ø320: alüminyum 1,5 disk + kulp 40×6×80 (öne, robot tutar) — yerel: disk merkezi (0,0,0), kalınlık +Y"""
    st = Station(os.path.join(ORTAK, "TEPSI_D320"), "TEPSI_D320"); p = "TEPSI_"
    st.cyl_y(p+"disk_D320_alu_1.5", 0, 0, 160, 0, 6); st.box(p+"kulp_40x6x80", -20, 20, 0, 6, 160, 240)
    st.assemble("TEPSI_D320"); c = st.center(); print("  TEPSI merkez (mm): %.1f %.1f %.1f" % (c[0]/M, c[1]/M, c[2]/M)); return c

def uc_yuvasi():
    """ortak robot ucu yuvası: taban 180×20×340 + kilit pimi Ø12 ×40 — yerel: taban ön-orta (0,0,0), arkaya −Z"""
    st = Station(os.path.join(ORTAK, "UC_YUVASI"), "UC_YUVASI"); p = "UCY_"
    st.box(p+"taban_180x20x340", -90, 90, 0, 20, -340, 0); st.box(p+"kilit_pimi_12x40", -6, 6, 20, 60, -180, -168)
    st.assemble("UC_YUVASI"); c = st.center(); print("  UC_YUVASI merkez (mm): %.1f %.1f %.1f" % (c[0]/M, c[1]/M, c[2]/M)); return c

if __name__ == "__main__":
    faz = sys.argv[1]
    if faz == "ortak":
        sw.CloseAllDocuments(True); tepsi(); uc_yuvasi(); Station(ROOT, "x").exit_sw()
    elif faz == "asm":
        sw.CloseAllDocuments(True); st = Station(ROOT, "PRESS")
        for f in os.listdir(st.pdir):      # eski tekil tepsi / yuva parçaları → örneklerle değişiyor
            if f.startswith(("PRESS_tepsi_D320", "PRESS_tepsi_kulpu", "PRESS_uc_yuvasi", "PRESS_uc_kilit_pimi")): os.remove(os.path.join(st.pdir, f))
        st.load_dir(); print("kasa parca:", len(st.parts))
        ct = [0, 3*M, 40*M]                # TEPSI yerel bbox merkezi (x −160..160, y 0..6, z −160..240)
        for (cx, cy, cz) in ((190, 1080, -300), (510, 1080, -300), (350, 910, -280)):   # raf ×2 + preste ×1 (disk merkezi)
            st.add_instance(os.path.join(ORTAK, "TEPSI_D320", "TEPSI_D320.SLDASM"), [cx*M + ct[0], cy*M + ct[1], cz*M + ct[2]])
        cy_ = [0, 30*M, -170*M]            # UC_YUVASI yerel bbox merkezi (x −90..90, y 0..60, z −340..0)
        for xx in (130, 350, 570):
            st.add_instance(os.path.join(ORTAK, "UC_YUVASI", "UC_YUVASI.SLDASM"), [xx*M + cy_[0], 1154*M + cy_[1], -60*M + cy_[2]])
        st.assemble("PRESS")
        e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w_ = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        d = sw.OpenDoc6(os.path.join(ROOT, "PRESS.SLDASM"), 2, 1, "", e, w_)
        for cpt in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
            if cpt.Name2.startswith(("TEPSI", "UC_")): t = cpt.Transform2.ArrayData; print("  %-16s x=%5.0f y=%5.0f z=%5.0f" % (cpt.Name2, t[9]/M, t[10]/M, t[11]/M))
        d.ShowNamedView2("*Isometric", 7); mcall(d, "ViewZoomtofit2"); sw.FrameState = 2                      # 2 = maximize (1 = minimize idi)
