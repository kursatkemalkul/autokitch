# -*- coding: utf-8 -*-
# TEK ÇEKMECE DETAY MONTAJI (kesit) + AÇILMA ANİMASYONU
#   içerik: kasa kesiti (yan söveler, alt/üst raf, arka panel, PU dilimi) + MOTORLU RAY (kasada sabit: gövde + motor kutusu + M12 soket)
#           + pasif ray karşılığı + çekmece (içeriğiyle) + reed sensör + mıknatıs
#   animasyon: kızak bağlantısının ölçüsü 0 → 600 → 0 adım adım değiştirilip kare kare görüntü alınır, GIF üretilir
import os, time, pythoncom
from sw_lib import *
from PIL import Image
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); DETAY = os.path.join(ROOT, "detay"); CEKD = os.path.join(ROOT, "cekmece"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
# taze_1 çekmecesi çevresi (STORE koordinatı): açıklık x 714..1338, y 1509..1608
X0, X1, YA, H = 714.0, 1338.0, 1509.0, 99.0
ZB, ZK_ = -757.5, 0.0            # iç hücre arka sacı · ön yüz
CEK = os.path.join(CEKD, "CEKMECE_taze", "CEKMECE_taze.SLDASM")

def kasa_kesiti():
    """çekmecenin çevresinden ince bir kasa dilimi — detay görünümü için"""
    st = Station(DETAY, "CEKMECE_DETAY"); p = "DET_"
    st.box(p+"bolme_saci_sol", X0-12, X0, YA-40, YA+H+40, ZB, ZK_)
    st.box(p+"bolme_saci_sag", X1, X1+12, YA-40, YA+H+40, ZB, ZK_)
    st.box(p+"raf_alt", X0, X1, YA-12, YA, ZB, ZK_)
    st.box(p+"raf_ust", X0, X1, YA+H, YA+H+12, ZB, ZK_)
    st.box(p+"arka_ic_sac", X0-12, X1+12, YA-40, YA+H+40, ZB-1, ZB)
    st.box(p+"PU_dilimi_arka", X0-12, X1+12, YA-40, YA+H+40, ZB-40, ZB-1)
    st.box(p+"on_sove_dilimi", X0-12, X0, YA-40, YA+H+40, 38.5, 40)
    # KASADA SABİT MOTORLU RAY: gövde + motor kutusu + M12 soket + kablo
    yr = YA + 18
    st.box(p+"MOTORLU_RAY_govde_45x12.7", X0, X0+12.7, yr, yr+45, -700, 0)
    st.box(p+"MOTORLU_RAY_motor_kutusu", X0, X0+40, yr-5, yr+50, -740, -700)
    st.box(p+"MOTORLU_RAY_M12_soket", X0+12, X0+28, yr+12, yr+28, -752, -740)
    st.cyl_z(p+"MOTORLU_RAY_kablo_D5", X0+20, yr+20, 2.5, -830, -752)
    st.box(p+"PASIF_RAY_govde_45x12.7", X1-12.7, X1, yr, yr+45, -700, 0)
    # kablo kanalı dilimi + klemens ucu
    st.box(p+"kablo_kanali_dilimi_40x25", X1-40, X1, YA-40, YA+H+40, -790, -765)
    return st

def detay_montaj(st):
    """kasa kesiti + çekmece + sensör → CEKMECE_DETAY.SLDASM (çekmece kızak bağlantısıyla hareketli)"""
    st.load_dir()
    st.add_instance(CEK, offset_mm=(X0+3, YA+3, 0))                                   # çekmece (içerik dahil)
    st.add_instance(os.path.join(ORTAK, "SENSOR_REED_D12", "SENSOR_REED_D12.SLDASM"), offset_mm=(X0+26, YA+H-18, 0))
    yol = st.assemble("CEKMECE_DETAY")
    # kızak bağlantısı: x/y kilitli, z serbest 0–600
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(yol, 2, 1, "", e, w); sw.FrameState = 2
    hedef = [c.Name2 for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren if c.Name2.startswith("CEKMECE_taze")][0]
    d.ClearSelection2(True); d.Extension.SelectByID2(hedef+"@CEKMECE_DETAY", "COMPONENT", 0.0, 0.0, 0.0, False, 0, NUL_, 0)
    mcall(d, "UnfixComponent"); d.ClearSelection2(True)
    d.Extension.SelectByID2("Right Plane", "PLANE", 0.0, 0.0, 0.0, False, 0, NUL_, 0); px = d.FeatureManager.InsertRefPlane(8, (X0+3)*M, 0, 0, 0, 0); d.ClearSelection2(True)
    d.Extension.SelectByID2("Top Plane", "PLANE", 0.0, 0.0, 0.0, False, 0, NUL_, 0); py = d.FeatureManager.InsertRefPlane(8, (YA+3)*M, 0, 0, 0, 0); d.ClearSelection2(True)
    for a, b, tip, ust in ((px.Name, "Right Plane@"+hedef+"@CEKMECE_DETAY", 0, 0.0), (py.Name, "Top Plane@"+hedef+"@CEKMECE_DETAY", 0, 0.0),
                           ("Front Plane", "Front Plane@"+hedef+"@CEKMECE_DETAY", 5, 600.0)):
        d.ClearSelection2(True); d.Extension.SelectByID2(a, "PLANE", 0.0, 0.0, 0.0, False, 1, NUL_, 0); d.Extension.SelectByID2(b, "PLANE", 0.0, 0.0, 0.0, True, 1, NUL_, 0)
        h = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); d.AddMate5(tip, 2, False, 0.0, ust*M, 0.0, 0, 0, 0, 0, 0, False, False, 0, h); d.ClearSelection2(True)
    for ad in (px.Name, py.Name): d.Extension.SelectByID2(ad, "PLANE", 0.0, 0.0, 0.0, True, 0, NUL_, 0)
    mcall(d, "BlankRefGeom"); d.ClearSelection2(True); mcall(d, "EditRebuild3")
    print("  detay montaj hazir, kizak bagli")
    return d, yol

def animasyon(d, kare=18, acilim=600.0):
    """ölçüyü adım adım değiştirip kare kare görüntü al → GIF"""
    d.ShowNamedView2("*Isometric", 7); mcall(d, "ViewZoomtofit2"); time.sleep(1)
    kareler = []; tmp = os.path.join(DETAY, "_kare")
    os.makedirs(tmp, exist_ok=True)
    diziler = [acilim*i/kare for i in range(kare+1)] + [acilim*(kare-i)/kare for i in range(1, kare+1)]
    for i, mm in enumerate(diziler):
        d.Parameter("D1@LimitDistance1").SystemValue = mm/1000.0; mcall(d, "EditRebuild3")
        yol = os.path.join(tmp, "k%03d.png" % i); d.SaveBMP(yol, 1000, 700)
        im = Image.open(yol).convert("P", palette=Image.ADAPTIVE, colors=128); kareler.append(im)
    gif = os.path.join(ROOT, "CEKMECE_animasyon.gif")
    kareler[0].save(gif, save_all=True, append_images=kareler[1:], duration=70, loop=0, optimize=True)
    print("  animasyon:", gif, "(%d kare)" % len(kareler))
    d.Parameter("D1@LimitDistance1").SystemValue = 0.35; mcall(d, "EditRebuild3")
    png(d, os.path.join(ROOT, "CEKMECE_detay.png"), "*Isometric", 1600, 1100)
    return gif

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    st = kasa_kesiti(); d, yol = detay_montaj(st)
    g = animasyon(d)
    print("kayit:", saveas(d, yol))
