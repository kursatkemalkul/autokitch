# -*- coding: utf-8 -*-
# STORE — çekmece otomasyonu donanımı (MOTORSUZ kurgu: çekmeceyi ROBOT çeker/iter)
#   · her çekmecede: mıknatıs (çekmece önünün iç yüzünde) — çekmece alt montajına girer, tüm örneklerde çıkar
#   · kasada her çekmece hizasında: reed sensör Ø12×30 (kapalı doğrulama) — söve iç yüzüne
#   · arka sağ iç köşede dikey kablo kanalı 40×25 + üst teknik bölmede klemens kutusu 150×100×60
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); CEKD = os.path.join(ROOT, "cekmece"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
# çekmece açıklıkları: (ad, x0, x1, y_alt, yükseklik)
ACIKLIK = ([("icecek_%d" % i, 66, 690, y, 124) for i, y in enumerate((1484, 1354, 1224, 1094), 1)] +
           [("1L", 66, 690, 772, 316)] +
           [("taze_%d" % i, 714, 1338, y, 99) for i, y in enumerate((1509, 1404, 1299, 1194, 1089, 984, 879, 774), 1)] +
           [("donmus_1", 66, 690, 297, 94), ("donmus_2", 66, 690, 197, 94), ("donmus_3", 714, 1338, 297, 94), ("donmus_4", 714, 1338, 197, 94)] +
           [("kaset_klape", 66, 690, 403, 284)])

def miknatis(tip, h_on):
    """çekmece önünün iç yüzüne mıknatıs 15×8×3 (sensöre bakar) — çekmece alt montajına eklenir"""
    st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip
    yol = os.path.join(st.pdir, p + "miknatis_15x8x3.SLDPRT")
    if os.path.exists(yol): os.remove(yol)
    st.box(p + "miknatis_15x8x3", 596, 611, h_on - 20, h_on - 12, -3, 0)     # önün iç yüzü (z 0), üst kenara yakın
    return st

def sensor_parcasi():
    """reed sensör Ø12 × 30 + M12 soket + kablo ucu — yerel: gövde merkezi (0,0,0), ekseni Z"""
    st = Station(os.path.join(ORTAK, "SENSOR_REED_D12"), "SENSOR_REED_D12"); p = "SNS_"
    if os.path.exists(os.path.join(ORTAK, "SENSOR_REED_D12", "SENSOR_REED_D12.SLDASM")): return
    st.cyl_z(p+"govde_D12x30", 0, 0, 6, -30, 0); st.cyl_z(p+"M12_soket", 0, 0, 7.5, -40, -30); st.cyl_z(p+"kablo_D5", 0, 0, 2.5, -140, -40)
    st.assemble("SENSOR_REED_D12"); print("  sensor: reed D12 x 30 + M12 soket")

def store_donanim():
    st = Station(ROOT, "STORE"); p = "STORE_"
    # kablo kanalı + klemens kutusu (kasa parçaları)
    yeni = []
    for ad, x0, x1, y0, y1, z0, z1 in (
        ("kablo_kanali_dikey_40x25", 1290, 1330, 200, 1660, -752, -727),      # arka sağ iç köşe
        ("kablo_kanali_yatay_40x25", 700, 1330, 1620, 1660, -752, -727),
        ("klemens_kutusu_150x100x60", 1150, 1300, 1690, 1790, -700, -640),    # üst teknik bölme (soğutma yanı)
        ("PLC_giris_modulu_16_kanal", 950, 1120, 1690, 1790, -700, -660)):
        yol = os.path.join(st.pdir, p + ad + ".SLDPRT")
        if not os.path.exists(yol): st.box(p + ad, x0, x1, y0, y1, z0, z1)
        yeni.append(yol)
    print("  kanal + klemens + PLC girisi uretildi")
    return yeni

def store_ekle(kasa_parcalari):
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    var = set(c.Name2.rsplit("-", 1)[0] for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    n = 0
    for yol in kasa_parcalari:                                   # kasa parçaları kendi yerinde modellendi
        ad = os.path.splitext(os.path.basename(yol))[0]
        if ad in var: continue
        dd = sw.OpenDoc6(yol, 1, 1, "", e, w); bb = bbox_of(dd)
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        if d.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2]) is not None: n += 1
        sw.CloseDoc(dd.GetTitle)
    # sensörler: her açıklığın üst-iç köşesinde, söve yüzünde (sol modülde sağ kenar, sağ modülde sol kenar)
    yol = os.path.join(ORTAK, "SENSOR_REED_D12", "SENSOR_REED_D12.SLDASM")
    dd = sw.OpenDoc6(yol, 2, 1, "", e, w); bb = [1e9]*3 + [-1e9]*3
    for cp in dd.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        g = cp.GetBox(False, False)
        for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
    kc = [(bb[i]+bb[i+3])/2 for i in range(3)]; sw.CloseDoc(dd.GetTitle)
    for ad, x0, x1, ya, h in ACIKLIK:
        xs = x1 - 12 if x1 < 700 else x0 + 12                    # sol modül: sağ kenara · sağ modül: sol kenara
        if d.AddComponent5(yol, 0, "", False, "", kc[0] + xs*M, kc[1] + (ya + h - 18)*M, kc[2] + 0*M) is not None: n += 1
    comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith(("SENSOR_REED", "STORE_kablo_kanali", "STORE_klemens", "STORE_PLC")): c.Select4(True, NUL_, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(2)
    print("  eklenen bilesen: %d | STORE toplam: %d" % (n, d.GetComponentCount(True)))
    for nm in ("LimitDistance1", "LimitDistance2", "LimitDistance3", "LimitDistance4"):
        p2 = d.Parameter("D1@" + nm)
        if p2 is not None: p2.SystemValue = 0.35
    mcall(d, "EditRebuild3"); time.sleep(2)
    png(d, os.path.join(ROOT, "STORE_otomasyon.png"), "*Isometric")
    print("  kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    sensor_parcasi()
    for tip, h in (("icecek", 118.0), ("1L", 310.0), ("taze", 93.0), ("donmus", 94.0)):
        st = miknatis(tip, h); st.load_dir()
        # içerikleri koru: alt montajı yeniden kurmak yerine sadece mıknatısı ekleyip yeniden kur
        print("  %s: miknatis eklendi (parca %d)" % (tip, len(st.parts)))
    print("NOT: cekmece alt montajlari sw_kola_tepsi/sw_hamur ile yeniden kurulmali (icerik + miknatis)")
    store_ekle(store_donanim())
