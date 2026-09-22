# -*- coding: utf-8 -*-
# ÖN YÜZLER: BÜKME SAC KENARLI + EN İNCE FUGA
#  · dış sac 1,5 dört kenardan bükülür (kenarlar kapalı, PU görünmez) — tek parça
#  · PU 37,5 ve iç sac 1,0 bükümün içinde kalır
#  · fuga 6 → 3 mm (her kenarda 1,5): imalat toleransı + kaplama + ısıl genleşme için pratik alt sınır
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); CEKD = os.path.join(ROOT, "cekmece")
W_KUTU = 618.0            # çekmece gövde genişliği (içerik bu koordinata göre)
T_D, T_I, FUGA = 1.5, 1.0, 3.0
# tip: açıklık yüksekliği (mm)
TIP = {"icecek": 124.0, "1L": 316.0, "taze": 99.0, "donmus": 94.0}

def on_yuz(st, p, w_kutu, h_acik, x0=0.0, y0=0.0):
    """bükme sac ön yüz: dış sac (ön + 4 kenar dönüşü) · PU · iç sac
       ön panel = açıklık − 3 mm; gövdeye göre −1,5 kayık (her kenarda 1,5 fuga)"""
    a, b = x0 - T_D, x0 + w_kutu + T_D                  # panel dış sınırları (621 geniş)
    h_pu = h_acik - 2*FUGA                              # gövde yüksekliği (eski h_on)
    c, d = y0 - T_D, y0 + h_pu + T_D                    # panel alt/üst (açıklık − 3)
    ops = [(FR, 'rect', (a, b, c, d), 38.5, 40.0, False),          # ön yüz sacı
           (FR, 'rect', (a, a + T_D, c, d), 1.0, 40.0, False),     # sol kenar dönüşü
           (FR, 'rect', (b - T_D, b, c, d), 1.0, 40.0, False),     # sağ kenar dönüşü
           (FR, 'rect', (a, b, c, c + T_D), 1.0, 40.0, False),     # alt kenar dönüşü
           (FR, 'rect', (a, b, d - T_D, d), 1.0, 40.0, False)]     # üst kenar dönüşü
    st.part(p + "on_dis_sac_bukme_1.5", ops)
    st.box(p + "on_pu_37.5", x0, x0 + w_kutu, y0, y0 + h_pu, 1.0, 38.5)
    st.box(p + "on_ic_sac_1.0", x0, x0 + w_kutu, y0, y0 + h_pu, 0.0, 1.0)

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    for tip, h_acik in TIP.items():
        st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip
        for f in os.listdir(st.pdir):
            if "on_ic_sac" in f or "on_pu" in f or "on_dis_sac" in f: os.remove(os.path.join(st.pdir, f))
        on_yuz(st, p, W_KUTU, h_acik)
        print("  %s: panel %.0f x %.0f (aciklik %.0f, fuga %.1f)" % (tip, W_KUTU + 2*T_D, h_acik - FUGA, h_acik, FUGA))
    # kaset katı klapesi (STORE parçası, global koordinat): açıklık x 66–690, y 403–687
    st = Station(ROOT, "STORE"); p = "STORE_klape_kaset_kati_"
    for f in os.listdir(st.pdir):
        if f.startswith(p) and ("on_ic_sac" in f or "on_pu" in f or "on_dis_sac" in f): os.remove(os.path.join(st.pdir, f))
    on_yuz(st, p, 618.0, 284.0, x0=69.0, y0=406.0)
    print("  kaset klapesi: panel 621 x 281")
    # STORE'u yenile
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(3)
    for i in range(1, 9):
        p2 = d.Parameter("D1@LimitDistance%d" % i)
        if p2 is not None: p2.SystemValue = 0.0
    mcall(d, "EditRebuild3"); time.sleep(1)
    png(d, os.path.join(ROOT, "STORE_bukme_kenar.png"), "*Front", 1400, 830)
    png(d, os.path.join(ROOT, "STORE_bukme_kenar_iso.png"), "*Isometric", 1400, 830)
    print("  bilesen:", d.GetComponentCount(True), "| kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))
