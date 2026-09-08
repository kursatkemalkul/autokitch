# -*- coding: utf-8 -*-
# İÇECEK + 1 L çekmeceleri: ÇUKURLU HİZALAMA TEPSİSİ (hamur tepsisi mantığı) — kanal/ayırıcı yok, ön sıra boş değil.
#   · kola tepsisi: 70 çukur Ø70 × 12 derin · x adım 82 (robot parmak boşluğu 16) · z adım 74 → 7 × 10 = 70 kutu
#     4 içecek çekmecesi = 280 kutu (haftalık ihtiyaç 264 ✓)
#   · 1 L tepsisi: 40 çukur Ø92 × 15 derin · x adım 118 (boşluk 30) · z adım 90 → 5 × 8 = 40 şişe (teknik resim ✓)
#   · kutu tabanı 4 mm'ye indirildi: kola 115 + tepsi → açıklık 124 içinde kalıyor
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); CEKD = os.path.join(ROOT, "cekmece"); ORTAK = os.path.join(ARA, "_ortak")
DERIN, KA, KB = 740.0, 13.7, 604.3
KC = 4.0                                   # kutu tabanı (kola dik sığsın diye 8 → 4)
# (ad, kanal/adım x, adım z, sütun, sıra, çukur R, tepsi kalınlığı, çukur derinliği, ürün yolu, ürün yarıçapı)
TIP = {
 "icecek": dict(h_on=118.0, ax=82.0, az=74.0, nx=7, nz=10, r=35.0, kal=13.0, cd=12.0,
                urun=os.path.join(ORTAK, "KUTU_KOLA_330ml", "KUTU_KOLA_330ml.SLDASM")),
 "1L":     dict(h_on=310.0, ax=118.0, az=90.0, nx=5, nz=8, r=46.0, kal=20.0, cd=15.0,
                urun=os.path.join(ORTAK, "SISE_KOLA_1L", "SISE_KOLA_1L.SLDASM")),
}

def merkezler(t):
    genis = KB - KA
    x0 = KA + (genis - ((t["nx"]-1)*t["ax"] + 2*t["r"]))/2 + t["r"]
    z0 = -(2 + t["r"])
    return [x0 + i*t["ax"] for i in range(t["nx"])], [z0 - j*t["az"] for j in range(t["nz"])]

def cekmece(tip):
    t = TIP[tip]; st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip; kd = t["h_on"] - 12.0
    # eski kanal ayırıcı / delikli sac / kutu parçalarını temizle
    for f in os.listdir(st.pdir):
        if any(k in f for k in ("kanal_ayirici", "hizalama_saci", "kutu_U", "kutu_arka", "ray_teleskopik")): os.remove(os.path.join(st.pdir, f))
    st.prism_z(p+"kutu_U_1.0", [(KA, kd), (KA, KC), (KB, KC), (KB, kd), (KB-1, kd), (KB-1, KC+1), (KA+1, KC+1), (KA+1, kd)], -DERIN, 0)
    st.box(p+"kutu_arka_1.0", KA, KB, KC, kd, -DERIN, -DERIN+1)
    st.box(p+"ray_teleskopik_sol_45x12.7", 0, 12.7, KC+10, KC+55, -DERIN+50, 0)
    st.box(p+"ray_teleskopik_sag_45x12.7", 618.0-12.7, 618.0, KC+10, KC+55, -DERIN+50, 0)
    # ÇUKURLU HİZALAMA TEPSİSİ: düz taban sacı + her ürün için halka yuva (tek parça, 70 kez örneklenir)
    X, Z = merkezler(t); y0 = KC + 1; y1 = y0 + t["kal"]
    st.box(p+"tepsi_taban_saci_1.5", KA+3, KB-3, y0, y0+1.5, Z[-1]-t["r"]-8, min(Z[0]+t["r"]+8, -3))
    halka = os.path.join(ORTAK, "YUVA_%s" % tip)
    hs = Station(halka, "YUVA_%s" % tip)
    if not os.path.exists(os.path.join(halka, "YUVA_%s.SLDASM" % tip)):
        hs.part("YUVA_%s_halka" % tip, [(TP, 'circ', (0, 0, t["r"]+5.5), y0+1.5, y1, False),
                                        (TP, 'circ', (0, 0, t["r"]+2), y1 - t["cd"], y1 + 1, True)])
        hs.assemble("YUVA_%s" % tip)
    st.load_dir(); n = 0
    for cx in X:
        for cz in Z:
            st.add_instance(os.path.join(halka, "YUVA_%s.SLDASM" % tip), offset_mm=(cx, 0, cz))
            st.add_instance(t["urun"], offset_mm=(cx, y1 - t["cd"], cz)); n += 1
    st.assemble("CEKMECE_" + tip)
    print("  CEKMECE_%s: %d cukur dolu (%d x %d) · cukur araligi x %.0f (bosluk %.0f) · z %.0f" %
          (tip, n, t["nx"], t["nz"], t["ax"], t["ax"]-2*t["r"], t["az"]))
    return n

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    a = cekmece("icecek"); b = cekmece("1L")
    print("TOPLAM: %d kutu (4 cekmece) · %d sise" % (4*a, b))
    # STORE'u yenile + görüntü
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(3)
    for nm in ("LimitDistance1", "LimitDistance2", "LimitDistance3", "LimitDistance4"):
        p2 = d.Parameter("D1@" + nm)
        if p2 is not None: p2.SystemValue = 0.55
    mcall(d, "EditRebuild3"); time.sleep(2)
    png(d, os.path.join(ROOT, "STORE_kola_tepsi.png"), "*Isometric")
    print("kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))
