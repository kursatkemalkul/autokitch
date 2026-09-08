# -*- coding: utf-8 -*-
# STORE −18 BUZLUK: (1) donmuş çekmeceler ×4 → çukurlu tepsi + 20 donmuş hamur topu (pitch 10, büyümez)
#                   (2) kaset katı (klapeli) → 4 standart kap 14×68×24 (kıyma ×2 · kuşbaşı ×2) + L raf çiftleri
# STORE.SLDASM yeniden KURULMAZ; mevcut montaja bileşen eklenir (çekmece kızak bağlantıları korunsun diye).
import os, time, pythoncom
from sw_lib import *
from sw_hamur import X_CUKUR, Z_CUKUR, Y_TEPSI, TEPSI_H, CUKUR_H
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); CEKD = os.path.join(ROOT, "cekmece"); ORTAK = os.path.join(ARA, "_ortak")
KAP = os.path.join(ARA, "3_TOPPING", "alt_montaj", "KAP_14x68x24", "KAP_14x68x24.SLDASM")
DERIN, KA, KB, KC = 740.0, 13.7, 604.3, 8.0
ZI = -757.5                                   # −18 hücresinin iç arka sacı
KASET_Y = 404.5                               # kaset katı rafının üst kotu
KAP_X = [151.5, 299.5, 447.5, 595.5]          # 4 kap yan yana (sol modül 66–690 içinde, toplam 59,5 cm)
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)

def donmus_cekmece():
    """donmuş çekmece: kutu 740 + çukurlu tepsi + 20 donmuş top (taze ile aynı tepsi/kap)"""
    st = Station(os.path.join(CEKD, "CEKMECE_donmus"), "CEKMECE_donmus"); p = "CEK_donmus_"; kd = 94.0 - 12.0
    for ad in ("kutu_U_1.0", "kutu_arka_1.0", "ray_teleskopik_sol_45x12.7", "ray_teleskopik_sag_45x12.7"):
        yol = os.path.join(st.pdir, p + ad + ".SLDPRT")
        if os.path.exists(yol): os.remove(yol)
    st.prism_z(p+"kutu_U_1.0", [(KA, kd), (KA, KC), (KB, KC), (KB, kd), (KB-1, kd), (KB-1, KC+1), (KA+1, KC+1), (KA+1, kd)], -DERIN, 0)
    st.box(p+"kutu_arka_1.0", KA, KB, KC, kd, -DERIN, -DERIN+1)
    st.box(p+"ray_teleskopik_sol_45x12.7", 0, 12.7, KC+10, KC+55, -DERIN+50, 0)
    st.box(p+"ray_teleskopik_sag_45x12.7", 618.0-12.7, 618.0, KC+10, KC+55, -DERIN+50, 0)
    st.load_dir()
    st.add_instance(os.path.join(ORTAK, "TEPSI_HAMUR_GN21", "TEPSI_HAMUR_GN21.SLDASM"), offset_mm=(0, 0, 0))
    n = 0
    for cx in X_CUKUR:
        for cz in Z_CUKUR:
            st.add_instance(os.path.join(ORTAK, "HAMUR_TOPU_220g", "HAMUR_TOPU_220g.SLDASM"), offset_mm=(cx, Y_TEPSI+TEPSI_H-CUKUR_H, cz)); n += 1
    st.assemble("CEKMECE_donmus"); print("  CEKMECE_donmus: tepsi + %d donmus top (4 cekmece = %d)" % (n, 4*n))

def kaset_raflari():
    """kaset katında her kap için L raf çifti (20×8×2, dik kenar dışta) — STORE parça klasörüne"""
    st = Station(ROOT, "STORE"); p = "STORE_kaset_"; yeni = []
    for i, xc in enumerate(KAP_X, 1):
        for side, sx in (("sol", -1), ("sag", 1)):
            ad = p + "L_raf_%d_%s" % (i, side); yol = os.path.join(st.pdir, ad + ".SLDPRT")
            if os.path.exists(yol): os.remove(yol)
            xe = xc + sx*54
            pts = [(xe, KASET_Y), (xe+sx*2, KASET_Y), (xe+sx*2, KASET_Y+20), (xe-sx*6, KASET_Y+20), (xe-sx*6, KASET_Y+18), (xe, KASET_Y+18)]
            st.prism_z(ad, pts, ZI+2, -20); yeni.append(yol)
    print("  %d L raf uretildi" % len(yeni)); return yeni

def store_guncelle(raflar):
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    # 1) eski temsili kapları sil
    d.ClearSelection2(True); sil = 0
    for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        if "donmus_kap" in c.Name2: d.Extension.SelectByID2(c.Name2 + "@STORE", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0); sil += 1
    if sil: d.Extension.DeleteSelection2(0); print("  temsili kap silindi:", sil)
    d.ClearSelection2(True)
    # 2) L rafları ekle (kendi koordinatlarında modellendi → merkezine koy)
    for yol in raflar:
        dd = sw.OpenDoc6(yol, 1, 1, "", e, w); bb = bbox_of(dd); sw.CloseDoc(dd.GetTitle)
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        d.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2])
    # 3) 4 standart kap (kıyma ×2 · kuşbaşı ×2) — kap yereli: merkez x=0, raf üstü y=0
    dd = sw.OpenDoc6(KAP, 2, 1, "", e, w); bb = [1e9]*3 + [-1e9]*3
    for cp in dd.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        g = cp.GetBox(False, False)
        for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
    kc = [(bb[i]+bb[i+3])/2 for i in range(3)]; sw.CloseDoc(dd.GetTitle)
    for xc in KAP_X: d.AddComponent5(KAP, 0, "", False, "", kc[0] + xc*M, kc[1] + KASET_Y*M, kc[2])
    # 4) yeni bileşenleri sabitle
    comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith(("STORE_kaset_L_raf", "KAP_14x68x24")): c.Select4(True, NUL_, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(2)
    print("  STORE bilesen:", d.GetComponentCount(True))
    # 5) donmuş çekmeceye kızak bağlantısı (görsel için) + görüntü
    hedef, x0, y0 = "CEKMECE_donmus-1", 69.0, 300.0
    d.ClearSelection2(True); d.Extension.SelectByID2(hedef + "@STORE", "COMPONENT", 0.0, 0.0, 0.0, False, 0, NUL_, 0); mcall(d, "UnfixComponent"); d.ClearSelection2(True)
    d.Extension.SelectByID2("Right Plane", "PLANE", 0.0, 0.0, 0.0, False, 0, NUL_, 0); px = d.FeatureManager.InsertRefPlane(8, x0*M, 0, 0, 0, 0); d.ClearSelection2(True)
    d.Extension.SelectByID2("Top Plane", "PLANE", 0.0, 0.0, 0.0, False, 0, NUL_, 0); py = d.FeatureManager.InsertRefPlane(8, y0*M, 0, 0, 0, 0); d.ClearSelection2(True)
    for a, b, tip, ust in ((px.Name, "Right Plane@"+hedef+"@STORE", 0, 0.0), (py.Name, "Top Plane@"+hedef+"@STORE", 0, 0.0), ("Front Plane", "Front Plane@"+hedef+"@STORE", 5, 600.0)):
        d.ClearSelection2(True); d.Extension.SelectByID2(a, "PLANE", 0.0, 0.0, 0.0, False, 1, NUL_, 0); d.Extension.SelectByID2(b, "PLANE", 0.0, 0.0, 0.0, True, 1, NUL_, 0)
        h = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); d.AddMate5(tip, 2, False, 0.0, ust*M, 0.0, 0, 0, 0, 0, 0, False, False, 0, h); d.ClearSelection2(True)
    for ad in (px.Name, py.Name): d.Extension.SelectByID2(ad, "PLANE", 0.0, 0.0, 0.0, True, 0, NUL_, 0)
    mcall(d, "BlankRefGeom"); d.ClearSelection2(True)
    for nm in ("LimitDistance1", "LimitDistance2", "LimitDistance3", "LimitDistance4"):
        p = d.Parameter("D1@" + nm)
        if p is not None: p.SystemValue = 0.55
    mcall(d, "EditRebuild3"); time.sleep(2)
    # kaset katını göstermek için klape ön saclarını geçici gizle
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith("STORE_klape_kaset_kati_on"): d.Extension.SelectByID2(c.Name2 + "@STORE", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0)
    mcall(d, "HideComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(1)
    png(d, os.path.join(ROOT, "STORE_buzluk.png"), "*Isometric")
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith("STORE_klape_kaset_kati_on"): d.Extension.SelectByID2(c.Name2 + "@STORE", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0)
    mcall(d, "ShowComponent"); d.ClearSelection2(True)
    print("  kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    donmus_cekmece(); raflar = kaset_raflari(); store_guncelle(raflar)
    print("BITTI — 4 donmus cekmece x 20 = 80 top · kaset kati 4 kap")
