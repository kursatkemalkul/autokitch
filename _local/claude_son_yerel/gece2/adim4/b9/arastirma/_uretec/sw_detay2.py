# -*- coding: utf-8 -*-
# TEK ÇEKMECE TAHRİK DETAYI (kesit) — MOTOR VE KABLO ZİNCİRİ GÖRÜNÜR + animasyon
#   ana PC ─Ethernet→ PLC ─röle→ 24 V kablo → MOTOR (ray arkasında, kasada sabit) → kayış → çekmece
#   geri bildirim: reed sensör (kapalı) + motor enkoderi
# Yakın taraftaki yan sac ÇİZİLMEZ (kesit) → motor, kayış, kablo, sensör açıkta görünür.
import os, time, pythoncom
from sw_lib import *
from PIL import Image
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); DETAY = os.path.join(ROOT, "detay2"); CEKD = os.path.join(ROOT, "cekmece"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
X0, X1, YA, H = 714.0, 1338.0, 1509.0, 99.0          # taze_1 açıklığı (STORE koordinatı)
ZB = -757.5                                           # iç hücre arka sacı
CEK = os.path.join(CEKD, "CEKMECE_taze", "CEKMECE_taze.SLDASM")
MTG = os.path.join(ORTAK, "MOTOR_TAHRIK_GRUBU", "MOTOR_TAHRIK_GRUBU.SLDASM")
YR = YA + 3 + 18                                      # ray ekseni (çekmece yereli 8+10 → kasa kotu)

def kasa(st):
    p = "DET2_"
    st.box(p+"bolme_saci_sol", X0-12, X0, YA-40, YA+H+40, ZB, 0)          # SOL yan (arka planda kalır)
    st.box(p+"raf_alt", X0, X1, YA-12, YA, ZB, 0)
    st.box(p+"raf_ust", X0, X1, YA+H, YA+H+12, ZB, 0)
    st.box(p+"arka_ic_sac", X0-12, X1+12, YA-40, YA+H+40, ZB-1, ZB)
    st.box(p+"PU_dilimi_arka", X0-12, X1+12, YA-40, YA+H+40, ZB-40, ZB-1)
    st.box(p+"on_sove_dilimi", X0-12, X0, YA-40, YA+H+40, 38.5, 40)
    # RAY: kasa tarafı dış profiller (sol motorlu hat, sağ pasif)
    st.box(p+"ray_dis_profil_sol", X0, X0+14, YR-2, YR+47, -660, 0)
    st.box(p+"ray_dis_profil_sag", X1-14, X1, YR-2, YR+47, -660, 0)
    # KAYIŞ: motor kasnağından çekmecedeki pabuca (görünür ince şerit)
    st.box(p+"kayis_GT3_6mm", X0+3, X0+9, YR+20, YR+23, -690, -40)
    st.box(p+"gergi_makarasi_braketi", X0, X0+14, YR+10, YR+35, -70, -55)
    # KABLO ZİNCİRİ: motor soketi → dikey kanal → üstte klemens → PLC → Ethernet
    st.cyl_z(p+"kablo_24V_motor_D5", X0+30, YR+20, 2.5, -800, -690)
    st.box(p+"kablo_kanali_40x25", X1-40, X1, YA-40, YA+H+40, -800, -775)
    st.box(p+"klemens_kutusu_dilimi", X1-120, X1-40, YA+H+20, YA+H+40, -800, -760)
    st.box(p+"PLC_dilimi", X1-260, X1-130, YA+H+16, YA+H+40, -800, -770)
    st.cyl_z(p+"ethernet_kablosu_ana_PC", X1-190, YA+H+28, 3, -900, -800)
    st.box(p+"reed_sensor_braketi", X0+16, X0+34, YA+H-24, YA+H-8, -8, 2)

def montaj():
    st = Station(DETAY, "CEKMECE_TAHRIK_DETAY"); kasa(st); st.load_dir()
    st.add_instance(CEK, offset_mm=(X0+3, YA+3, 0))                                  # çekmece (içeriğiyle)
    st.add_instance(MTG, offset_mm=(X0+3, YR+21, -690))                              # MOTOR: ray arkasında, ekseni X
    st.add_instance(os.path.join(ORTAK, "SENSOR_REED_D12", "SENSOR_REED_D12.SLDASM"), offset_mm=(X0+25, YA+H-16, 0))
    yol = st.assemble("CEKMECE_TAHRIK_DETAY")
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(yol, 2, 1, "", e, w); sw.FrameState = 2
    hedef = [c.Name2 for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren if c.Name2.startswith("CEKMECE_taze")][0]
    d.ClearSelection2(True); d.Extension.SelectByID2(hedef+"@CEKMECE_TAHRIK_DETAY", "COMPONENT", 0.0, 0.0, 0.0, False, 0, NUL_, 0)
    mcall(d, "UnfixComponent"); d.ClearSelection2(True)
    d.Extension.SelectByID2("Right Plane", "PLANE", 0.0, 0.0, 0.0, False, 0, NUL_, 0); px = d.FeatureManager.InsertRefPlane(8, (X0+3)*M, 0, 0, 0, 0); d.ClearSelection2(True)
    d.Extension.SelectByID2("Top Plane", "PLANE", 0.0, 0.0, 0.0, False, 0, NUL_, 0); py = d.FeatureManager.InsertRefPlane(8, (YA+3)*M, 0, 0, 0, 0); d.ClearSelection2(True)
    for a, b, tip, ust in ((px.Name, "Right Plane@"+hedef+"@CEKMECE_TAHRIK_DETAY", 0, 0.0), (py.Name, "Top Plane@"+hedef+"@CEKMECE_TAHRIK_DETAY", 0, 0.0),
                           ("Front Plane", "Front Plane@"+hedef+"@CEKMECE_TAHRIK_DETAY", 5, 600.0)):
        d.ClearSelection2(True); d.Extension.SelectByID2(a, "PLANE", 0.0, 0.0, 0.0, False, 1, NUL_, 0); d.Extension.SelectByID2(b, "PLANE", 0.0, 0.0, 0.0, True, 1, NUL_, 0)
        h = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); d.AddMate5(tip, 2, False, 0.0, ust*M, 0.0, 0, 0, 0, 0, 0, False, False, 0, h); d.ClearSelection2(True)
    for ad in (px.Name, py.Name): d.Extension.SelectByID2(ad, "PLANE", 0.0, 0.0, 0.0, True, 0, NUL_, 0)
    mcall(d, "BlankRefGeom"); d.ClearSelection2(True); mcall(d, "EditRebuild3")
    return d, yol

def kayit_ve_animasyon(d, yol):
    d.ShowNamedView2("*Isometric", 7); mcall(d, "ViewZoomtofit2"); time.sleep(1)
    tmp = os.path.join(DETAY, "_kare"); os.makedirs(tmp, exist_ok=True)
    kare = 16; dizi = [600.0*i/kare for i in range(kare+1)] + [600.0*(kare-i)/kare for i in range(1, kare+1)]
    frames = []
    for i, mm in enumerate(dizi):
        d.Parameter("D1@LimitDistance1").SystemValue = mm/1000.0; mcall(d, "EditRebuild3")
        f = os.path.join(tmp, "k%03d.png" % i); d.SaveBMP(f, 1100, 750)
        frames.append(Image.open(f).convert("P", palette=Image.ADAPTIVE, colors=128))
    gif = os.path.join(ROOT, "CEKMECE_tahrik_animasyon.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)
    d.Parameter("D1@LimitDistance1").SystemValue = 0.30; mcall(d, "EditRebuild3"); time.sleep(1)
    png(d, os.path.join(ROOT, "CEKMECE_tahrik_detay.png"), "*Isometric", 1700, 1150)
    print("  animasyon:", gif); print("  kayit:", saveas(d, yol))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    d, yol = montaj(); kayit_ve_animasyon(d, yol)
