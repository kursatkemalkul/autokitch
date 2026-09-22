# -*- coding: utf-8 -*-
# TOPPING klape animasyonu: klape her kare için AÇILI parça olarak üretilir (menteşe ekseni etrafında döndürülmüş kesit),
# kesit montaja takılır, görüntü alınır, çıkarılır → GIF. (SolidWorks MathUtility erişilemediği için transform yerine bu yol.)
import os, math, time, pythoncom
from sw_lib import *
from PIL import Image
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "3_TOPPING"); DETAY = os.path.join(ROOT, "detay"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
X0, X1, Y0_, Y1_ = 30.0, 670.0, 1560.0, 1950.0
PY, PZ = 1566.0, 30.0                 # menteşe ekseni (y, z)
KAP = os.path.join(ROOT, "alt_montaj", "KAP_14x68x24", "KAP_14x68x24.SLDASM")
KARE = os.path.join(DETAY, "kare"); os.makedirs(KARE, exist_ok=True)

def don(y, z, a):
    """menteşe ekseni (PY,PZ) etrafında +a derece döndür (klape öne-aşağı açılır)"""
    r = math.radians(a); c, s = math.cos(r), math.sin(r)
    return (PY + (y-PY)*c - (z-PZ)*s, PZ + (y-PY)*s + (z-PZ)*c)

def klape_parcasi(st, ad, a):
    """klape kesiti (YZ düzleminde dönmüş dikdörtgen) X boyunca ekstrüzyon — Right Plane: u=−z, v=y"""
    kose = [(PY, 20.0), (Y1_-6, 20.0), (Y1_-6, 40.0), (PY, 40.0)]
    pts = [don(y, z, a) for y, z in kose]
    return st.part(ad, [(RT, 'poly', [(-z, y) for y, z in pts], X0+3, X1-3, False)])

def montaj_kur():
    st = Station(DETAY, "KLAPE_ANIM"); p = "KLD_"
    # kasa kesiti (yoksa üret)
    if not os.path.exists(os.path.join(st.pdir, p+"raf_alt.SLDPRT")):
        ZI = -797.5
        st.box(p+"yan_sac_sol", X0-14, X0, Y0_-30, Y1_+30, ZI, 0)
        st.box(p+"raf_alt", X0, X1, Y0_-14, Y0_, ZI, 0)
        st.box(p+"raf_ust", X0, X1, Y1_, Y1_+14, ZI, 0)
        st.box(p+"arka_ic_sac", X0-14, X1+14, Y0_-30, Y1_+30, ZI-1, ZI)
        st.box(p+"PU_dilimi", X0-14, X1+14, Y0_-30, Y1_+30, ZI-40, ZI-1)
        st.box(p+"L_raf_sol", 216, 220, 1710, 1730, ZI, -20); st.box(p+"L_raf_sag", 320, 324, 1710, 1730, ZI, -20)
        for i, xx in enumerate((X0+40, X1-58), 1): st.box(p+"gazli_amortisor_%d" % i, xx, xx+18, Y0_+40, Y0_+240, -34, -16)
        st.cyl_z(p+"motor_kablosu_D5", X0-20, PY+20, 2.5, -140, 0)
        st.box(p+"kablo_kanali_dilimi", X1-40, X1, Y0_-30, Y1_+30, ZI+20, ZI+45)
    # gabari işaretleri: kadraj tüm salınım hacmini kapsasın (2 mm küpler, görüntüde fark edilmez)
    if not os.path.exists(os.path.join(st.pdir, p+"gabari_1.SLDPRT")):
        st.box(p+"gabari_1", X0-45, X0-43, Y0_-40, Y0_-38, -800, -798)
        st.box(p+"gabari_2", X1+20, X1+22, Y1_+40, Y1_+42, 440, 442)
    st.load_dir()
    st.add_instance(os.path.join(ORTAK, "KLAPE_MOTOR_GRUBU", "KLAPE_MOTOR_GRUBU.SLDASM"), offset_mm=(X0-40, PY, PZ-4))
    st.add_instance(os.path.join(ORTAK, "SENSOR_REED_D12", "SENSOR_REED_D12.SLDASM"), offset_mm=(X1-25, Y0_+12, 0))
    st.add_instance(os.path.join(ORTAK, "SENSOR_REED_D12", "SENSOR_REED_D12.SLDASM"), offset_mm=(X1-25, Y0_+60, -120))
    if os.path.exists(KAP): st.add_instance(KAP, offset_mm=(270, 1710, 0))
    return st.assemble("KLAPE_ANIM")

def animasyon(yol, adim=15):
    ps = Station(KARE, "kareler")                       # açılı klape parçaları buraya
    aci = [90.0*i/adim for i in range(adim+1)]
    for i, a in enumerate(aci):
        if not os.path.exists(os.path.join(ps.pdir, "KLAPE_a%02d.SLDPRT" % i)): klape_parcasi(ps, "KLAPE_a%02d" % i, a)
    print("  %d acili klape parcasi hazir" % len(aci))
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(yol, 2, 1, "", e, w); sw.FrameState = 2
    d.ShowNamedView2("*Isometric", 7); mcall(d, "ViewZoomtofit2"); time.sleep(1)
    tmp = os.path.join(DETAY, "_png"); os.makedirs(tmp, exist_ok=True); frames = []
    for i in range(len(aci)):
        pyol = os.path.join(ps.pdir, "KLAPE_a%02d.SLDPRT" % i)
        dd = sw.OpenDoc6(pyol, 1, 1, "", e, w); bb = bbox_of(dd)
        c = [(bb[k]+bb[k+3])/2 for k in range(3)]
        comp = d.AddComponent5(pyol, 0, "", False, "", c[0], c[1], c[2]); mcall(d, "EditRebuild3")
        f = os.path.join(tmp, "f%02d.png" % i); d.SaveBMP(f, 1400, 830)
        frames.append(Image.open(f).convert("P", palette=Image.ADAPTIVE, colors=128))
        if i == 9: d.SaveBMP(os.path.join(ROOT, "KLAPE_tahrik_detay.png"), 1400, 830); Image.open(os.path.join(ROOT, "KLAPE_tahrik_detay.png")).save(os.path.join(ROOT, "KLAPE_tahrik_detay.png"))   # yarı açık kare (kadraj sabit)
        d.ClearSelection2(True); d.Extension.SelectByID2(comp.Name2 + "@KLAPE_ANIM", "COMPONENT", 0.0, 0.0, 0.0, False, 0, NUL_, 0)
        d.Extension.DeleteSelection2(0); sw.CloseDoc(dd.GetTitle)
    tam = frames + frames[::-1][1:]
    gif = os.path.join(ROOT, "KLAPE_animasyon.gif")
    tam[0].save(gif, save_all=True, append_images=tam[1:], duration=80, loop=0, optimize=True)
    print("  animasyon:", gif, "(%d kare)" % len(tam))
    # son kare: klape kapalı kalsın, kaydet
    pyol = os.path.join(ps.pdir, "KLAPE_a00.SLDPRT")
    dd = sw.OpenDoc6(pyol, 1, 1, "", e, w); bb = bbox_of(dd); c = [(bb[k]+bb[k+3])/2 for k in range(3)]
    d.AddComponent5(pyol, 0, "", False, "", c[0], c[1], c[2]); sw.CloseDoc(dd.GetTitle); mcall(d, "EditRebuild3")
    print("  kayit:", saveas(d, yol))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    yol = montaj_kur(); animasyon(yol)
    print("BITTI")
