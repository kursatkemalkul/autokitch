# -*- coding: utf-8 -*-
# STORE — içecek çekmeceleri: teneke kutu 330 ml (Ø66 × 115, yatık) ve 1 L PET şişe (Ø88 × 280, ayakta)
# İçecek çekmecesi ×4 → her birinde 40 kutu (8 × 5 yatık) = 160 kutu · 1 L çekmecesi ×1 → 30 şişe (5 × 6 ayakta)
# Alt montaja eklenir → aynı tipteki bütün çekmeceler birden değişir.
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
CEKD = os.path.join(ARA, "1_STORE", "cekmece"); ORTAK = os.path.join(ARA, "_ortak")
DERIN = 700.0                                        # kutu derinliği (taze çekmecede de 700 yapıldı)
KA, KB, KC = 13.7, 618.0-13.7, 8.0                   # kutu iç sınırları (x sol/sağ, taban üstü)
# kutu 330 ml: 8 sıra (x pitch 70) × 5 derin (z pitch 130) = 40 · şişe 1 L: 5 (x pitch 110) × 6 (z pitch 100) = 30
KUTU_X = [64.0 + i*70.0 for i in range(8)]; KUTU_Z = [-145.0 - j*130.0 for j in range(5)]
SISE_X = [89.0 + i*110.0 for i in range(5)]; SISE_Z = [-101.0 - j*100.0 for j in range(6)]

def kutu_derinlestir(tip, h_on):
    """çekmece kutusunu/rayını 700 mm derinlikte yeniden üret (tepsi/şişe sığsın)"""
    st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip; kd = h_on - 12.0
    for ad in ("kutu_U_1.0", "kutu_arka_1.0", "ray_teleskopik_sol_45x12.7", "ray_teleskopik_sag_45x12.7"):
        yol = os.path.join(st.pdir, p + ad + ".SLDPRT")
        if os.path.exists(yol): os.remove(yol)
    st.prism_z(p+"kutu_U_1.0", [(KA, kd), (KA, KC), (KB, KC), (KB, kd), (KB-1, kd), (KB-1, KC+1), (KA+1, KC+1), (KA+1, kd)], -DERIN, 0)
    st.box(p+"kutu_arka_1.0", KA, KB, KC, kd, -DERIN, -DERIN+1)
    st.box(p+"ray_teleskopik_sol_45x12.7", 0, 12.7, KC+10, KC+55, -DERIN+50, 0)
    st.box(p+"ray_teleskopik_sag_45x12.7", 618.0-12.7, 618.0, KC+10, KC+55, -DERIN+50, 0)
    print("  %s kutusu %d mm" % (tip, DERIN))

def teneke_kutu():
    """330 ml teneke kutu Ø66 × 115 — yerel: ekseni Z boyunca, z 0..115, merkez (0,0)"""
    st = Station(os.path.join(ORTAK, "KUTU_KOLA_330ml"), "KUTU_KOLA_330ml"); p = "KOLA330_"
    st.cyl_z(p+"govde_D66", 0, 0, 33, 3, 112); st.cyl_z(p+"alt_bilezik_D60", 0, 0, 30, 0, 3); st.cyl_z(p+"ust_kapak_D60", 0, 0, 30, 112, 115)
    st.assemble("KUTU_KOLA_330ml"); print("  teneke kutu 330 ml: D66 x 115")

def sise_1L():
    """1 L PET şişe Ø88 × 280 (≤28 cm — çekmeceye ayakta girer) — yerel: taban merkezi (0,0,0), +Y yukarı"""
    st = Station(os.path.join(ORTAK, "SISE_KOLA_1L"), "SISE_KOLA_1L"); p = "KOLA1L_"
    st.cyl_y(p+"govde_D88", 0, 0, 44, 0, 190); st.cyl_y(p+"omuz_D70", 0, 0, 35, 190, 225)
    st.cyl_y(p+"boyun_D30", 0, 0, 15, 225, 265); st.cyl_y(p+"kapak_D32", 0, 0, 16, 265, 280)
    st.assemble("SISE_KOLA_1L"); print("  1 L sise: D88 x 280")

def cekmece_kur(tip, icerik):
    st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); st.load_dir()
    n = 0
    if icerik == "kutu":
        for cx in KUTU_X:
            for cz in KUTU_Z: st.add_instance(os.path.join(ORTAK, "KUTU_KOLA_330ml", "KUTU_KOLA_330ml.SLDASM"), offset_mm=(cx, KC+1+33, cz)); n += 1
    else:
        for cx in SISE_X:
            for cz in SISE_Z: st.add_instance(os.path.join(ORTAK, "SISE_KOLA_1L", "SISE_KOLA_1L.SLDASM"), offset_mm=(cx, KC+1, cz)); n += 1
    st.assemble("CEKMECE_" + tip); print("  CEKMECE_%s: %d adet %s" % (tip, n, icerik))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    kutu_derinlestir("icecek", 118.0); kutu_derinlestir("1L", 310.0)
    teneke_kutu(); sise_1L()
    cekmece_kur("icecek", "kutu"); cekmece_kur("1L", "sise")
    print("BITTI — 4 icecek cekmecesi x 40 = 160 teneke kutu · 1 L cekmecesi 30 sise")
