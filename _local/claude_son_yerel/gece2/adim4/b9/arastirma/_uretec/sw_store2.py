# -*- coding: utf-8 -*-
# AUTOKITCH — 1 · STORE v3: ÇEKMECELER ALT MONTAJ (grup) — 4 tip birer kez modellenir, STORE'a örnek olarak yerleşir (7 Eyl 2026)
# fazlar (her biri temiz SolidWorks oturumu): cekmece → kasa → asm
#   cekmece: 1_STORE/cekmece/CEKMECE_<tip>/parca/*.SLDPRT + CEKMECE_<tip>.SLDASM (yerel koordinat: ön sol alt köşe 0,0; z 0..40 ön, kutu −600..0)
#   kasa   : 1_STORE/parca/*.SLDPRT (kasa, yalıtım, söveler, paneller, soğutma, klape)
#   asm    : 1_STORE/STORE.SLDASM = kasa parçaları + 17 çekmece örneği (içecek ×4, 1L ×1, taze ×8, donmuş ×4)
import sys, os
from sw_lib import *

ROOT = os.path.join(r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma", "1_STORE")
W, PU = 1400.0, 60.0
# çekmece tipleri: (tip, açıklık genişliği, açıklık yüksekliği) — fuga 6 düşülmüş parça ölçüsü w=x1-x0-6, h=y1-y0-6
TIPLER = {"icecek": (624-6, 124-6), "1L": (624-6, 316-6), "taze": (624-6, 99-6), "donmus": (624-6, 94-6)}
# örnek yerleri: (tip, x0, y0) açıklık sol-alt köşesi (mm)
ORNEKLER = [("icecek", 66, 1484), ("icecek", 66, 1354), ("icecek", 66, 1224), ("icecek", 66, 1094), ("1L", 66, 772),
            ("taze", 714, 1509), ("taze", 714, 1404), ("taze", 714, 1299), ("taze", 714, 1194), ("taze", 714, 1089), ("taze", 714, 984), ("taze", 714, 879), ("taze", 714, 774),
            ("donmus", 66, 297), ("donmus", 66, 197), ("donmus", 714, 297), ("donmus", 714, 197)]

def cekmece(tip):
    """bir çekmece tipi = alt montaj: sandviç ön 40 (1,5 dış + 37,5 PU + 1,0 iç) + kulp oyuğu + kutu U 1,0 + arka + teleskopik ray çifti"""
    w, h = TIPLER[tip]; st = Station(os.path.join(ROOT, "cekmece", "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip
    kw = 300.0; kx = w/2 - kw/2; ky = h - 60; kul = [(kx, kx+kw, ky, ky+34, 27, 41)]
    st.box(p+"on_ic_sac_1.0", 0, w, 0, h, 0, 1); st.box(p+"on_pu_37.5", 0, w, 0, h, 1, 38.5, kul); st.box(p+"on_dis_sac_1.5", 0, w, 0, h, 38.5, 40, kul)
    st.box(p+"kulp_cukuru_1.0", kx-1, kx+kw+1, ky-1, ky+35, 26, 27)
    ka, kb, kc, kd = 13.7, w-13.7, 8, h-12
    st.prism_z(p+"kutu_U_1.0", [(ka, kd), (ka, kc), (kb, kc), (kb, kd), (kb-1, kd), (kb-1, kc+1), (ka+1, kc+1), (ka+1, kd)], -600, 0)
    st.box(p+"kutu_arka_1.0", ka, kb, kc, kd, -600, -599)
    st.box(p+"ray_teleskopik_sol_45x12.7", 0, 12.7, kc+10, kc+55, -500, 0); st.box(p+"ray_teleskopik_sag_45x12.7", w-12.7, w, kc+10, kc+55, -500, 0)
    path = st.assemble("CEKMECE_" + tip); c = st.center(); print("  %s merkez (mm): %.1f %.1f %.1f" % (tip, c[0]/M, c[1]/M, c[2]/M))
    return path, c

def kasa(st):
    """kasa parçaları (çekmece hariç) — sw_all.store() ile aynı kurgu"""
    p = "STORE_"
    shell(st, p, W, "feet")
    xi0, xi1, zi = insulated_cell(st, p, W, 182.5, 1610.0, PU, ytop_single=1670.0)
    st.box(p+"ayirici_sac_alt", xi0, xi1, 690, 691, zi, 0); st.box(p+"ayirici_pu", xi0, xi1, 691, 765, zi, 0); st.box(p+"ayirici_sac_ust", xi0, xi1, 765, 766, zi, 0)
    st.box(p+"orta_bolme_sac_sol", 690, 691, 182.5, 1610, zi, 0); st.box(p+"orta_bolme_pu", 691, 713, 182.5, 1610, zi, 0); st.box(p+"orta_bolme_sac_sag", 713, 714, 182.5, 1610, zi, 0)
    sove_L(st, p, W, Y0, H, side=66.0)
    xm = 702.0; st.prism_y(p+"sove_orta", [(690, ZF1), (690, ZF0), (xm-0.75, ZF0), (xm-0.75, 0), (xm+0.75, 0), (xm+0.75, ZF0), (714, ZF0), (714, ZF1)], 182.5, 1610)
    for nm, x0, x1, y0, y1 in (("panel_sogutma", 66, W-66, 1670, H), ("panel_bant_ust", 66, W-66, 1610, 1670), ("panel_ayirici_on", 66, W-66, 690, 766), ("panel_bos_bant", 714, 1338, 403, 687), ("panel_bant_alt", 66, W-66, Y0, 182.5)):
        st.box(p+nm, x0, x1, y0, y1, ZF0, ZF1)
    cooling_unit(st, p+"sog1_", 80, 1680, -100); cooling_unit(st, p+"sog2_", 720, 1680, -100)
    for i, (y0, y1) in enumerate(((1400, 1500), (500, 600)), 1):
        st.box(p+"evaporator_%d" % i, 200, 1200, y0, y1, -750, -650); st.cyl_z(p+"evap_fan_%d" % i, 700, (y0+y1)/2, 90, -790, -750)
    # −18 kaset katı klapesi (tek, alt montaj değil) + raf + 4 donmuş kap
    a, b, c, d = 69, 687, 406, 684; q = p + "klape_kaset_kati_"; kw = 180; kx = (a+b)/2 - kw/2; ky = d - 60; kul = [(kx, kx+kw, ky, ky+34, 27, 41)]
    st.box(q+"on_ic_sac", a, b, c, d, 0, 1); st.box(q+"on_pu", a, b, c, d, 1, 38.5, kul); st.box(q+"on_dis_sac", a, b, c, d, 38.5, 40, kul); st.box(q+"kulp_cukuru", kx-1, kx+kw+1, ky-1, ky+35, 26, 27)
    st.box(q+"pivot_mil", a-10, b+10, c+2, c+10, -8, 0)
    for i, xx in enumerate((a+15, b-33), 1): st.box(q+"gazli_amortisor_%d" % i, xx, xx+18, c+30, c+230, -30, -12)
    st.box(q+"raf", xi0, 690, 403, 404.5, zi, 0)
    for i in range(4): st.box(q+"donmus_kap_%d" % (i+1), 80+i*150, 80+i*150+140, 405, 555, -400, -100)

if __name__ == "__main__":
    faz = sys.argv[1]
    if faz == "cekmece":
        sw.CloseAllDocuments(True)
        for tip in TIPLER: cekmece(tip)
        Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        sw.CloseAllDocuments(True); st = Station(ROOT, "STORE"); kasa(st); print("kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "asm":
        sw.CloseAllDocuments(True); st = Station(ROOT, "STORE"); st.load_dir(); print("kasa parca yuklendi:", len(st.parts))
        for tip, x0, y0 in ORNEKLER:     # alt montaj örneği: yerel bbox merkezi + (x0+3, y0+3, 0) kaydırma
            w, h = TIPLER[tip]; loc = [(w/2)*M, (h/2)*M, (-600+40)/2*M]
            st.add_instance(os.path.join(ROOT, "cekmece", "CEKMECE_" + tip, "CEKMECE_" + tip + ".SLDASM"), [loc[0] + (x0+3)*M, loc[1] + (y0+3)*M, loc[2]])
        st.assemble("STORE")
        # kontrol: örnek konumları (alt montajın yerel orijini = açıklık sol-alt köşesi olmalı)
        e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w_ = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w_)
        for cpt in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
            if cpt.Name2.startswith("CEKMECE"): t = cpt.Transform2.ArrayData; print("  %-18s x=%5.0f y=%5.0f z=%4.0f" % (cpt.Name2, t[9]/M, t[10]/M, t[11]/M))
        d.ShowNamedView2("*Isometric", 7); mcall(d, "ViewZoomtofit2"); sw.FrameState = 2                      # 2 = maximize (1 = minimize idi)     # açık bırak: Kemal bakacak
