# -*- coding: utf-8 -*-
# STORE — içecek çekmeceleri TEKNİK RESME GÖRE (ist1_store_detay_v4):
#   · kutu 330 ml Ø66×115 DİK · 7 kanal (8,2 cm) × 11 derin = 77 kutu/çekmece → 4 çekmece = 28 kanal = 308 kutu ✓
#   · 1 L PET Ø88×280 DİK · 5 kanal × 8 = 40 şişe ✓
#   · çekmece kutusu derinliği 740 (resimdeki "derinlik 740"), kanal ayırıcı sacları 1 mm
import os, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
CEKD = os.path.join(ARA, "1_STORE", "cekmece"); ORTAK = os.path.join(ARA, "_ortak")
DERIN = 740.0; KA, KB, KC = 13.7, 604.3, 8.0
IC_X0, IC_W = 22.0, 590.6                       # kutu içi kullanılabilir genişlik
# içecek: 7 kanal × 82 · 11 derin (pitch 67) · 1 L: 5 kanal × 118 · 8 derin (pitch 90)
KOLA_KANAL, KOLA_N, KOLA_ADIM = 82.0, 11, 67.0
SISE_KANAL, SISE_N, SISE_ADIM = 118.0, 8, 90.0

def kutu_derinlestir(tip, h_on):
    st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip; kd = h_on - 12.0
    for ad in ("kutu_U_1.0", "kutu_arka_1.0", "ray_teleskopik_sol_45x12.7", "ray_teleskopik_sag_45x12.7"):
        yol = os.path.join(st.pdir, p + ad + ".SLDPRT")
        if os.path.exists(yol): os.remove(yol)
    st.prism_z(p+"kutu_U_1.0", [(KA, kd), (KA, KC), (KB, KC), (KB, kd), (KB-1, kd), (KB-1, KC+1), (KA+1, KC+1), (KA+1, kd)], -DERIN, 0)
    st.box(p+"kutu_arka_1.0", KA, KB, KC, kd, -DERIN, -DERIN+1)
    st.box(p+"ray_teleskopik_sol_45x12.7", 0, 12.7, KC+10, KC+55, -DERIN+50, 0)
    st.box(p+"ray_teleskopik_sag_45x12.7", 618.0-12.7, 618.0, KC+10, KC+55, -DERIN+50, 0)
    return st

def kanal_ayirici(st, p, adet, kanal_w, yuk):
    """kanal ayırıcı sac 1 mm — kutuların/şişelerin devrilmesini önler"""
    x0 = IC_X0 + (IC_W - adet*kanal_w)/2 if adet*kanal_w < IC_W else IC_X0
    for k in range(1, adet):
        xx = x0 + k*kanal_w
        st.box(p+"kanal_ayirici_%d" % k, xx-0.5, xx+0.5, KC+1, KC+1+yuk, -DERIN+2, -2)
    return [x0 + kanal_w/2 + k*kanal_w for k in range(adet)]     # kanal merkezleri

def teneke_kutu_dik():
    """330 ml teneke kutu Ø66 × 115 — DİK (ekseni Y), yerel taban merkezi (0,0,0)"""
    st = Station(os.path.join(ORTAK, "KUTU_KOLA_330ml"), "KUTU_KOLA_330ml"); p = "KOLA330_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.cyl_y(p+"alt_bilezik_D60", 0, 0, 30, 0, 3); st.cyl_y(p+"govde_D66", 0, 0, 33, 3, 108)
    st.cyl_y(p+"boyun_daralma_D60", 0, 0, 30, 108, 112); st.cyl_y(p+"kapak_D60", 0, 0, 30, 112, 115)
    st.assemble("KUTU_KOLA_330ml"); print("  teneke kutu DIK: D66 x 115")

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    teneke_kutu_dik()
    # --- İÇECEK çekmecesi: 7 kanal × 11 kutu = 77
    st = kutu_derinlestir("icecek", 124.0); p = "CEK_icecek_"
    for f in os.listdir(st.pdir):
        if "kanal_ayirici" in f: os.remove(os.path.join(st.pdir, f))
    merkez = kanal_ayirici(st, p, 7, KOLA_KANAL, 60.0)
    st.load_dir(); n = 0
    z0 = -(2 + 33)
    for cx in merkez:
        for j in range(KOLA_N):
            st.add_instance(os.path.join(ORTAK, "KUTU_KOLA_330ml", "KUTU_KOLA_330ml.SLDASM"), offset_mm=(cx, KC+1, z0 - j*KOLA_ADIM)); n += 1
    st.assemble("CEKMECE_icecek"); print("  CEKMECE_icecek: 7 kanal x %d = %d kutu (4 cekmece = %d)" % (KOLA_N, n, 4*n))
    # --- 1 L çekmecesi: 5 kanal × 8 şişe = 40
    st = kutu_derinlestir("1L", 310.0); p = "CEK_1L_"
    for f in os.listdir(st.pdir):
        if "kanal_ayirici" in f: os.remove(os.path.join(st.pdir, f))
    merkez = kanal_ayirici(st, p, 5, SISE_KANAL, 120.0)
    st.load_dir(); n = 0; z0 = -(2 + 44)
    for cx in merkez:
        for j in range(SISE_N):
            st.add_instance(os.path.join(ORTAK, "SISE_KOLA_1L", "SISE_KOLA_1L.SLDASM"), offset_mm=(cx, KC+1, z0 - j*SISE_ADIM)); n += 1
    st.assemble("CEKMECE_1L"); print("  CEKMECE_1L: 5 kanal x %d = %d sise" % (SISE_N, n))
    # --- taze çekmecesi kutusunu da 740'a getir (tepsi/hamur aynı kalır)
    st = kutu_derinlestir("taze", 93.0); st.load_dir()
    from sw_hamur import X_CUKUR, Z_CUKUR, Y_TEPSI, TEPSI_H, CUKUR_H
    st.add_instance(os.path.join(ORTAK, "TEPSI_HAMUR_GN21", "TEPSI_HAMUR_GN21.SLDASM"), offset_mm=(0, 0, 0))
    for cx in X_CUKUR:
        for cz in Z_CUKUR: st.add_instance(os.path.join(ORTAK, "HAMUR_TOPU_220g", "HAMUR_TOPU_220g.SLDASM"), offset_mm=(cx, Y_TEPSI+TEPSI_H-CUKUR_H, cz))
    st.assemble("CEKMECE_taze"); print("  CEKMECE_taze: kutu 740, tepsi + 20 top")
    print("BITTI — 308 teneke kutu (dik) · 40 sise (dik) · 160 hamur topu")
