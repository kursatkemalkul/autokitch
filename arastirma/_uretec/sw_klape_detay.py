# -*- coding: utf-8 -*-
# TOPPING — TEK KLAPE TAHRİK DETAYI (kesit) + AÇILMA ANİMASYONU
#   ana PC ─Ethernet→ PLC ─röle→ 24 V ─→ menteşe motoru (redüktörlü, kendinden kilitli) ─→ klape 90° aşağı açılır
#   gazlı amortisör ×2 ağırlığı dengeler · 2 reed sensör (kapalı / açık) durumu PC'ye bildirir
# Animasyon: klape bileşeni menteşe ekseni etrafında kare kare döndürülür (Transform2), GIF üretilir.
import os, math, time, pythoncom
from sw_lib import *
from PIL import Image
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "3_TOPPING"); DETAY = os.path.join(ROOT, "detay"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
# kat 1 klapesi: açıklık y 1560..1950, x 30..670 · menteşe alt ön kenarda (y 1566, z 30)
X0, X1, Y0_, Y1_ = 30.0, 670.0, 1560.0, 1950.0
PIVOT_Y, PIVOT_Z = 1566.0, 30.0
ZI = -797.5                      # TOPPING iç arka sacı
KAP = os.path.join(ORTAK if False else os.path.join(ROOT, "alt_montaj"), "KAP_14x68x24", "KAP_14x68x24.SLDASM")

def klape_alt_montaj():
    """KLAPE_KAT: bükme sac kapak 1,5 + PU + gömme kulp — tek bileşen (animasyonda bu döner)"""
    kok = os.path.join(ORTAK, "KLAPE_KAT_TOPPING")
    if os.path.exists(os.path.join(kok, "KLAPE_KAT_TOPPING.SLDASM")): print("  klape alt montaji zaten var"); return kok
    st = Station(kok, "KLAPE_KAT_TOPPING"); p = "KLP_"
    a, b, c, d_ = X0+3, X1-3, Y0_+6, Y1_-6
    st.prism_y(p+"kapak_dis_sac_1.5", [(a, 40), (a, 20), (a+1.5, 20), (a+1.5, 38.5), (b-1.5, 38.5), (b-1.5, 20), (b, 20), (b, 40)], c, d_)
    st.box(p+"kapak_ic_sac_1.0", a+1.5, b-1.5, c, d_, 20, 21)
    st.box(p+"PU_dolgu", a+1.5, b-1.5, c, d_, 21, 38.5)
    kw = 180.0; kx = (a+b)/2 - kw/2; ky = d_ - 60
    st.box(p+"kulp_cukuru", kx, kx+kw, ky, ky+34, 26, 27)
    st.box(p+"mentese_mili_D8", a-10, b+10, c-4, c+4, 26, 34)
    st.assemble("KLAPE_KAT_TOPPING"); print("  KLAPE_KAT_TOPPING hazir"); return kok

def kasa_kesiti(st):
    p = "KLD_"
    st.box(p+"yan_sac_sol", X0-14, X0, Y0_-30, Y1_+30, ZI, 0)
    st.box(p+"raf_alt", X0, X1, Y0_-14, Y0_, ZI, 0)
    st.box(p+"raf_ust", X0, X1, Y1_, Y1_+14, ZI, 0)
    st.box(p+"arka_ic_sac", X0-14, X1+14, Y0_-30, Y1_+30, ZI-1, ZI)
    st.box(p+"PU_dilimi", X0-14, X1+14, Y0_-30, Y1_+30, ZI-40, ZI-1)
    st.box(p+"L_raf_sol", 216, 220, 1710, 1730, ZI, -20); st.box(p+"L_raf_sag", 320, 324, 1710, 1730, ZI, -20)
    # gazlı amortisör ×2 (klape ağırlığını dengeler) + kablo + klemens
    for i, xx in enumerate((X0+40, X1-58), 1): st.box(p+"gazli_amortisor_%d" % i, xx, xx+18, Y0_+40, Y0_+240, -34, -16)
    st.cyl_z(p+"motor_kablosu_D5", X0-20, PIVOT_Y+20, 2.5, -140, 0)
    st.box(p+"kablo_kanali_dilimi", X1-40, X1, Y0_-30, Y1_+30, ZI+20, ZI+45)
    st.box(p+"klemens_ucu", X1-120, X1-40, Y0_-30, Y0_-10, ZI+20, ZI+60)

def montaj():
    kok = klape_alt_montaj()
    st = Station(DETAY, "KLAPE_TAHRIK_DETAY"); kasa_kesiti(st); st.load_dir()
    st.add_instance(os.path.join(kok, "KLAPE_KAT_TOPPING.SLDASM"), offset_mm=(0, 0, 0))
    st.add_instance(os.path.join(ORTAK, "KLAPE_MOTOR_GRUBU", "KLAPE_MOTOR_GRUBU.SLDASM"), offset_mm=(X0-40, PIVOT_Y, PIVOT_Z-4))
    st.add_instance(os.path.join(ORTAK, "SENSOR_REED_D12", "SENSOR_REED_D12.SLDASM"), offset_mm=(X1-25, Y0_+12, 0))
    st.add_instance(os.path.join(ORTAK, "SENSOR_REED_D12", "SENSOR_REED_D12.SLDASM"), offset_mm=(X1-25, Y0_+60, -120))
    if os.path.exists(KAP): st.add_instance(KAP, offset_mm=(270, 1710, 0))
    return st.assemble("KLAPE_TAHRIK_DETAY")

def animasyon(yol, kare=14):
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(yol, 2, 1, "", e, w); sw.FrameState = 2
    mu = mcall(sw, "IGetMathUtility")     # matematik yardımcısı (arayüz sürümü — düz ad yazma-özel)
    klape = [c for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren if c.Name2.startswith("KLAPE_KAT")][0]
    d.ClearSelection2(True); klape.Select4(True, NUL_, False); mcall(d, "UnfixComponent"); d.ClearSelection2(True)
    d.ShowNamedView2("*Isometric", 7); mcall(d, "ViewZoomtofit2"); time.sleep(1)
    tmp = os.path.join(DETAY, "_kare"); os.makedirs(tmp, exist_ok=True)
    aci = [90.0*i/kare for i in range(kare+1)] + [90.0*(kare-i)/kare for i in range(1, kare+1)]
    frames = []
    for i, a in enumerate(aci):
        t = math.radians(-a); cs, sn = math.cos(t), math.sin(t)
        py, pz = PIVOT_Y*M, PIVOT_Z*M
        ty = py - (cs*py - sn*pz); tz = pz - (sn*py + cs*pz)      # p - R·p  (X ekseni etrafında)
        veri = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [1, 0, 0, 0, cs, -sn, 0, sn, cs, 0.0, ty, tz, 1, 0, 0, 0])
        klape.Transform2 = mcall(mu, 'CreateTransform', veri)
        mcall(d, "EditRebuild3")
        f = os.path.join(tmp, "k%03d.png" % i); d.SaveBMP(f, 1100, 780)
        frames.append(Image.open(f).convert("P", palette=Image.ADAPTIVE, colors=128))
    gif = os.path.join(ROOT, "KLAPE_animasyon.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)
    # yarı açık kare (kapak görünsün) + kayıt
    t = math.radians(-55); cs, sn = math.cos(t), math.sin(t); py, pz = PIVOT_Y*M, PIVOT_Z*M
    veri = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [1, 0, 0, 0, cs, -sn, 0, sn, cs, 0.0, py-(cs*py-sn*pz), pz-(sn*py+cs*pz), 1, 0, 0, 0])
    klape.Transform2 = mcall(mu, 'CreateTransform', veri); mcall(d, "EditRebuild3"); time.sleep(1)
    png(d, os.path.join(ROOT, "KLAPE_tahrik_detay.png"), "*Isometric", 1700, 1150)
    print("  animasyon:", gif)
    print("  kayit:", saveas(d, yol))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    yol = montaj(); animasyon(yol)
    print("BITTI")
