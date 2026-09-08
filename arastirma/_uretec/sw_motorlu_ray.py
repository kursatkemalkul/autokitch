# -*- coding: utf-8 -*-
# STORE — ÇEKMECE OTOMASYONU · BASİT KURGU: hazır MOTORLU TELESKOPİK RAY (motor + kontrol rayın içinde)
#   · sol ray = motorlu (arka ucunda motor kutusu 40×40×120 + M12 soket) · sağ ray = pasif teleskopik ray
#   · kasada ek motor/kremayer/braket YOK → temiz iç hacim, tek katalog parçası
#   · pano (üst teknik bölme): 24 V 10 A güç kaynağı + PLC (Modbus TCP) + 2 × 8 kanal röle kartı
#   · geri bildirim: rayın kendi uç anahtarları (açık/kapalı) + çekmecede reed "kapalı" doğrulaması
# Not: ray parça DOSYASI aynı adla yeniden üretilir → tüm çekmece montajları kendiliğinden güncellenir (içerik korunur).
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); CEKD = os.path.join(ROOT, "cekmece")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
TIPLER = (("icecek", 118.0, 4.0), ("1L", 310.0, 4.0), ("taze", 93.0, 8.0), ("donmus", 94.0, 8.0))

def motorlu_ray(tip, h_on, kc):
    """sol rayı MOTORLU sürümle değiştir (aynı dosya adı → montajlar otomatik güncellenir)"""
    st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip
    yol = os.path.join(st.pdir, p + "ray_teleskopik_sol_45x12.7.SLDPRT")
    if os.path.exists(yol): os.remove(yol)
    y0 = kc + 10; y1 = y0 + 45
    ops = [(FR, 'rect', (0, 12.7, y0, y1), -690, 0, False),                      # ray gövdesi (tam açılım 700)
           (FR, 'rect', (0, 40, y0 - 5, y0 + 45), -740, -690, False),            # arka uçta motor kutusu 40×50×120
           (FR, 'rect', (12, 28, y0 + 12, y0 + 28), -750, -740, False)]          # M12 soket (kablo sabit uçta)
    st.part(p + "ray_MOTORLU_sol_45x12.7", ops)
    # dosya adını montajın beklediği ada çevir
    yeni = os.path.join(st.pdir, p + "ray_MOTORLU_sol_45x12.7.SLDPRT")
    if os.path.exists(yeni):
        if os.path.exists(yol): os.remove(yol)
        os.rename(yeni, yol)
    print("  %s: sol ray MOTORLU (motor kutusu arka uçta)" % tip)

def pano(st):
    """basit pano: 24 V güç kaynağı + PLC + 2 röle kartı (17 çekmece için 16+ kanal)"""
    p = "STORE_"; yeni = []
    for ad, x0, x1, y0, y1, z0, z1 in (
        ("pano_guc_kaynagi_24V_10A", 700, 830, 1690, 1815, -700, -640),
        ("pano_PLC_ModbusTCP", 850, 970, 1690, 1800, -700, -650),
        ("pano_role_karti_1_8kanal", 990, 1100, 1690, 1780, -700, -670),
        ("pano_role_karti_2_8kanal", 1120, 1230, 1690, 1780, -700, -670)):
        yol = os.path.join(st.pdir, p + ad + ".SLDPRT")
        if not os.path.exists(yol): st.box(p + ad, x0, x1, y0, y1, z0, z1)
        yeni.append(yol)
    return yeni

def store_ekle(parcalar):
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    var = set(c.Name2.rsplit("-", 1)[0] for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    n = 0
    for yol in parcalar:
        ad = os.path.splitext(os.path.basename(yol))[0]
        if ad in var: continue
        dd = sw.OpenDoc6(yol, 1, 1, "", e, w); bb = bbox_of(dd)
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        if d.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2]) is not None: n += 1
        sw.CloseDoc(dd.GetTitle)
    comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith("STORE_pano_"): c.Select4(True, NUL_, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(3)
    print("  pano parcasi eklendi: %d | STORE toplam: %d" % (n, d.GetComponentCount(True)))
    for nm in ("LimitDistance1", "LimitDistance2", "LimitDistance3", "LimitDistance4"):
        p2 = d.Parameter("D1@" + nm)
        if p2 is not None: p2.SystemValue = 0.45
    mcall(d, "EditRebuild3"); time.sleep(2)
    png(d, os.path.join(ROOT, "STORE_motorlu_ray.png"), "*Isometric")
    print("  kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    for tip, h, kc in TIPLER: motorlu_ray(tip, h, kc)
    store_ekle(pano(Station(ROOT, "STORE")))
    print("BITTI — 17 motorlu ray · 1 guc kaynagi · 1 PLC · 2 role karti")
