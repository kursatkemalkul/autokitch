# -*- coding: utf-8 -*-
# TOPPING — KLAPE OTOMASYONU (ana PC / BEYİN kontrolünde kendi açılıp kapanan kapaklar)
#   her klapede: 24 V redüktörlü menteşe motoru (5 N·m, sonsuz vida = kendinden kilitli) + kol + 2 reed sensör (açık/kapalı)
#   gazlı amortisör ×2 klapenin ağırlığını dengeler (zaten modelde) → motora ≈ 3 N·m kalır
#   pano: TOPPING arka duvarında 8 kanal röle + PLC (ana PC'ye Modbus TCP)
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "3_TOPPING"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
KLAPE = [("kat1", 1560.0, 1950.0), ("kat2", 1150.0, 1560.0), ("kat3", 740.0, 1150.0), ("alt1", 460.0, 740.0), ("alt2", 200.0, 460.0)]
X0, X1 = 30.0, 670.0          # klape genişliği (kabin ön yüzü)

def klape_motoru():
    """KLAPE_MOTOR_GRUBU: 24 V redüktörlü menteşe motoru + kol + braket + M12 soket
       Yerel: menteşe ekseni (0,0,0); motor +X yönünde, kol öne uzanır"""
    kok = os.path.join(ORTAK, "KLAPE_MOTOR_GRUBU")
    if os.path.exists(os.path.join(kok, "KLAPE_MOTOR_GRUBU.SLDASM")): print("  klape motoru zaten var"); return
    st = Station(kok, "KLAPE_MOTOR_GRUBU"); p = "KLM_"
    st.box(p+"reduktor_govde_40x40x45", 0, 45, -20, 20, -20, 20)        # sonsuz vida redüktör (menteşe ekseninde)
    st.box(p+"motor_24V_37x37x75", 45, 120, -18.5, 18.5, -18.5, 18.5)   # DC motor
    st.box(p+"M12_soket", 120, 135, -8, 8, -8, 8)
    st.box(p+"montaj_braketi_3mm", -5, 50, -28, -20, -25, 25)           # kabine vidalanır
    st.box(p+"tahrik_kolu_120", -6, 6, -8, 8, 0, 120)                   # menteşeden klapeye giden kol
    st.assemble("KLAPE_MOTOR_GRUBU"); print("  KLAPE_MOTOR_GRUBU: 24 V reduktorlu mentese motoru + kol")

def sensor_ve_pano(st):
    """klape başına 2 reed sensör yuvası + TOPPING panosu (röle kartı + PLC)"""
    p = "TOPPING_"; yeni = []
    for ad, x0, x1, y0, y1, z0, z1 in (
        ("pano_role_karti_8kanal", 150, 260, 300, 390, -776, -746),
        ("pano_PLC_ModbusTCP", 280, 400, 300, 400, -776, -740),
        ("pano_guc_kaynagi_24V_5A", 420, 530, 300, 400, -776, -736),
        ("klape_kablo_kanali_dikey", 620, 660, 200, 1900, -776, -750)):
        yol = os.path.join(st.pdir, p + ad + ".SLDPRT")
        if not os.path.exists(yol): st.box(p + ad, x0, x1, y0, y1, z0, z1)
        yeni.append(yol)
    # klape başına 2 reed sensör (kapalı: ön sövede · açık: yan duvarda) — tek parça, örneklenecek
    return yeni

def topping_ekle(kasa_parcalari):
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "TOPPING.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    print("  TOPPING acildi, bilesen:", d.GetComponentCount(True))
    var = set(c.Name2.rsplit("-", 1)[0] for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    acik = []; n = 0
    for yol in kasa_parcalari:
        ad = os.path.splitext(os.path.basename(yol))[0]
        if ad in var: continue
        dd = sw.OpenDoc6(yol, 1, 1, "", e, w); bb = bbox_of(dd); acik.append(dd.GetTitle)
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        if d.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2]) is not None: n += 1
    def merkez(yol):
        dd = sw.OpenDoc6(yol, 2, 1, "", e, w); acik.append(dd.GetTitle); bb = [1e9]*3 + [-1e9]*3
        for cp in dd.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
            g = cp.GetBox(False, False)
            for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
        return [(bb[i]+bb[i+3])/2 for i in range(3)]
    MTR = os.path.join(ORTAK, "KLAPE_MOTOR_GRUBU", "KLAPE_MOTOR_GRUBU.SLDASM")
    SNS = os.path.join(ORTAK, "SENSOR_REED_D12", "SENSOR_REED_D12.SLDASM")
    c_m, c_s = merkez(MTR), merkez(SNS)
    for ad, y0, y1 in KLAPE:                       # motor sol menteşe ucunda; sensörler kapalı/açık
        if d.AddComponent5(MTR, 0, "", False, "", c_m[0] + (X0 - 40)*M, c_m[1] + (y0 + 6)*M, c_m[2] + 26*M) is not None: n += 1
        if d.AddComponent5(SNS, 0, "", False, "", c_s[0] + (X1 - 25)*M, c_s[1] + (y0 + 12)*M, c_s[2]) is not None: n += 1
        if d.AddComponent5(SNS, 0, "", False, "", c_s[0] + (X1 - 25)*M, c_s[1] + (y0 + 60)*M, c_s[2] - 120*M) is not None: n += 1
    for t_ in acik:
        try: sw.CloseDoc(t_)
        except Exception: pass
    comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith(("KLAPE_MOTOR_GRUBU", "SENSOR_REED", "TOPPING_pano_", "TOPPING_klape_kablo")): c.Select4(True, NUL_, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(2)
    print("  eklenen: %d | TOPPING toplam: %d" % (n, d.GetComponentCount(True)))
    png(d, os.path.join(ROOT, "TOPPING_klape_otomasyon.png"), "*Isometric")
    print("  kayit:", saveas(d, os.path.join(ROOT, "TOPPING.SLDASM")))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    klape_motoru()
    st = Station(ROOT, "TOPPING")
    topping_ekle(sensor_ve_pano(st))
    print("BITTI — 5 klape motoru + 10 reed sensor + pano TOPPING'de")
