# -*- coding: utf-8 -*-
# AUTOKITCH — 4 · OVEN v2 (ist4_oven_detay_v5): ALT MONTAJLI — KAP_YAG ×1, FIRIN_KAPAK_CAM ×2, ortak TEPSI_D320 ×2 + kasa (7 Eyl 2026)
# zonlar (zeminden cm): plint 12 · PANO 20 · KESME 50 · YAĞ+SPREY 30 (sıcak dolap 42 °C) · FIRIN 56 (OMAKE 64×60×56, 2 kat) · PLENUM+FAN 12 · filtre 5 · yedek 12 = 197
# plan: fırın 60 derin + arka kanal 24 (hava/kablo/buhar, pompa arkada) · yan taş yünü 3+3 · baca YOK (egzoz mekâna)
import sys, os
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "4_OVEN"); ORTAK = os.path.join(ARA, "_ortak")
W = 700.0

def kap_yag():
    """STANDART KAP — YAĞ VERSİYONU 14×68×24 (v5 C): gövde/kızak/dudak aynı kalıp; helezon+tarak YOK,
       taban kapalı, geçmeli kapak + dolum ağzı Ø60, şamandıra, arka kuru bağlantı. Yerel: kap merkezi x=0, raf üstü y=0"""
    st = Station(os.path.join(ORTAK, "KAP_YAG_14x68x24"), "KAP_YAG_14x68x24"); p = "KAPYAG_"; yb, yt = 20, 260
    st.prism_z(p+"PC_govde_5mm", [(-70, yt-5), (70, yt-5), (70, yt-105), (38, yb+10), (-38, yb+10), (-70, yt-105)], -700, -20)
    st.box(p+"taban_plakasi_kapali", -38, 38, yb+5, yb+10, -700, -20)
    st.box(p+"PC_kapak_gecmeli", -70, 70, yt-5, yt, -700, -20); st.cyl_y(p+"dolum_agzi_D60", 0, -360, 30, yt, yt+12)
    st.cyl_z(p+"samandira_D30", 0, yb+120, 15, -400, -300); st.cyl_z(p+"kuru_baglanti_D12", 0, yb+30, 6, -740, -700)
    st.box(p+"kizak_sol_30x20", -65, -35, 0, 20, -700, -20); st.box(p+"kizak_sag_30x20", 35, 65, 0, 20, -700, -20)
    st.box(p+"on_cekme_dudagi", -70, 70, yt-15, yt, -20, -5)
    st.assemble("KAP_YAG_14x68x24"); c = st.center(); print("  KAP_YAG merkez (mm): %.1f %.1f %.1f" % (c[0]/M, c[1]/M, c[2]/M)); return c

def firin_kapak():
    """FIRIN CAM KAPAK (aşağı açılır, motorlu) — çerçeve 1,5 bükme C + çift cam 4+4, alt pivot mili, menteşe motoru Ø28
       Yerel: kapak sol alt köşesi (0,0); genişlik 640, yükseklik 280, z 20..40"""
    st = Station(os.path.join(ORTAK, "FIRIN_KAPAK_CAM"), "FIRIN_KAPAK_CAM"); p = "FKAP_"; w, h = 640.0, 280.0
    st.prism_y(p+"cerceve_sol", [(0, ZF1), (0, 20), (25, 20), (25, ZF1)], 0, h); st.prism_y(p+"cerceve_sag", [(w-25, ZF1), (w-25, 20), (w, 20), (w, ZF1)], 0, h)
    st.box(p+"cerceve_ust", 25, w-25, h-25, h, 20, ZF1); st.box(p+"cerceve_alt", 25, w-25, 0, 25, 20, ZF1)
    st.box(p+"cam_dis_4mm", 25, w-25, 25, h-25, 34, 38); st.box(p+"cam_ic_4mm", 25, w-25, 25, h-25, 22, 26)
    st.box(p+"pivot_mili_D8", -10, w+10, 2, 10, 26, 34); st.cyl_z(p+"mentese_motoru_D28", w+15, 14, 14, -60, 40)
    st.assemble("FIRIN_KAPAK_CAM"); c = st.center(); print("  FIRIN_KAPAK merkez (mm): %.1f %.1f %.1f" % (c[0]/M, c[1]/M, c[2]/M)); return c

def kasa(st):
    p = "OVEN_"
    shell(st, p, W, "plint"); sove_L(st, p, W, Y0, H)
    st.box(p+"plint_izgara_paneli", 60, 640, 30, 110, 18.5, 20, [(80+i*40, 100+i*40, 40, 100, 17, 21) for i in range(14)])
    st.box(p+"yalitim_tasyunu_sol", T_DIS, 31.5, Y0, 1850, ZK+T_DIS, -20); st.box(p+"yalitim_tasyunu_sag", 668.5, W-T_DIS, Y0, 1850, ZK+T_DIS, -20)
    st.box(p+"arka_kanal_bolme_saci", 31.5, 668.5, Y0, 1850, -581, -580)
    # PANO 20 (120–320)
    door_C(st, p+"pano_kapagi_", 30, 670, Y0, 320)
    st.box(p+"pano_plakasi", 50, 650, 130, 310, -250, -248); zb = -248
    st.box(p+"pano_plc", 60, 160, 200, 300, zb, zb+75); st.box(p+"pano_psu_24V", 180, 280, 200, 300, zb, zb+110)
    for i, nm in enumerate(("mentese_1", "mentese_2", "pres")): st.box(p+"pano_surucu_%s" % nm, 300+i*70, 350+i*70, 200, 300, zb, zb+120)
    for i in range(2): st.box(p+"pano_SSR_%d" % (i+1), 520+i*60, 565+i*60, 220, 300, zb, zb+40)
    st.box(p+"pano_pompa_rolesi", 60, 110, 140, 190, zb, zb+60); st.box(p+"pano_klemens_rayi", 130, 640, 140, 147.5, zb, zb+35)
    # KESME 50 (320–820): tepsi zemine dayanır, bıçak yıldızı 2×28 + göbek, aktüatör 24 V 1500 N strok 100
    st.box(p+"panel_kesme", 30, 670, 320, 820, ZF0, ZF1, [(60, 640, 340, 800, ZF0-1, ZF1+1)])
    st.box(p+"kesme_zemin_plakasi", 60, 640, 330, 340, -580, -30); st.cyl_y(p+"kesme_tepsi_halkasi_D330", 350, -300, 165, 340, 346)
    st.box(p+"kesme_ust_travers", 100, 600, 780, 800, -400, -200)
    for i, xx in enumerate((150, 550), 1): st.cyl_y(p+"kesme_kilavuz_mili_D12_%d" % i, xx, -300, 6, 400, 780)
    st.box(p+"kesme_aktuator_24V_1500N", 320, 380, 560, 780, -330, -270); st.cyl_y(p+"kesme_aktuator_mili", 350, -300, 8, 470, 560)
    st.box(p+"kesme_kizak_plakasi", 130, 570, 460, 470, -340, -260); st.cyl_y(p+"kesme_gobek_D28", 350, -300, 14, 400, 460)
    st.box(p+"kesme_bicak_1_2x28_t1.2", 210, 490, 360, 400, -301, -299); st.box(p+"kesme_bicak_2_2x28_t1.2", 349, 351, 360, 400, -440, -160)
    # YAĞ + SPREY 30 (820–1120): sıcak dolap 42 °C; yağ kabı solda (L raf çifti), pompa arkada, nozül ortada, tepsi nişi
    door_C(st, p+"yag_kabi_kapagi_", 30, 180, 820, 1120)
    st.box(p+"panel_sprey", 180, 670, 820, 1120, ZF0, ZF1, [(200, 650, 840, 1100, ZF0-1, ZF1+1)])
    st.box(p+"sicak_dolap_pu_alt", 60, 640, 822, 862, -580, -30); st.box(p+"sicak_dolap_pu_ust", 60, 640, 1080, 1118, -580, -30)
    st.box(p+"sicak_dolap_isitici_100W", 200, 400, 862, 872, -400, -300); st.box(p+"sicak_dolap_termostat", 420, 460, 862, 892, -380, -340)
    for side, sx in (("sol", -1), ("sag", 1)):
        xe = 110 + sx*54; st.prism_z(p+"yag_kabi_L_raf_%s" % side, [(xe, 870), (xe+sx*2, 870), (xe+sx*2, 890), (xe-sx*6, 890), (xe-sx*6, 888), (xe, 888)], -580, -30)
    st.box(p+"yag_pompasi_24V", 60, 160, 900, 1000, -780, -640); st.cyl_z(p+"yag_hatti_D6", 350, 1060, 3, -640, -240)
    st.cyl_y(p+"sprey_nozulu_D8", 350, -240, 4, 1040, 1080); st.box(p+"sprey_nozul_tutucu", 330, 370, 1080, 1090, -260, -220)
    st.cyl_y(p+"tepsi_nisi_halkasi_D330", 350, -300, 165, 872, 878); st.box(p+"damlalik_tavasi", 200, 500, 862, 870, -450, -150)
    # FIRIN 56 (1120–1680): OMAKE satın alınan blok + 2 hazne düzlemi (tepsi 117 / 145)
    st.box(p+"OMAKE_firin_SATIN_ALINAN_64x60x56", 30, 670, 1120, 1680, -600, 0, [(100, 600, 1160, 1260, -420, 1), (100, 600, 1440, 1540, -420, 1)])
    st.box(p+"OMAKE_hazne_1_tepsi_duzlemi_117", 150, 550, 1166, 1170, -560, -60); st.box(p+"OMAKE_hazne_2_tepsi_duzlemi_145", 150, 550, 1446, 1450, -560, -60)
    st.box(p+"firin_arka_kanal_kablo", 620, 660, Y0, 1800, -800, -760); st.box(p+"firin_buhar_kanali", 300, 400, 1120, 1690, -760, -600)
    # PLENUM + FAN 12 (1680–1800) · karbon filtre 5 (1800–1850) · üst yedek 12 · egzoz mekâna (baca yok)
    st.box(p+"plenum_kutusu", 40, 660, 1690, 1800, -580, -40); st.cyl_y(p+"egzoz_fani_D120", 500, -300, 60, 1700, 1790)
    st.box(p+"karbon_filtre_40x40x5_opsiyon", 150, 550, 1800, 1850, -500, -100); st.box(p+"egzoz_izgarasi_ust", 400, 600, 1958, 1968.5, -500, -300)
    door_C(st, p+"fan_filtre_kapagi_", 30, 670, 1680, 1950); st.box(p+"panel_ust_serit", 30, 670, 1950, H, ZF0, ZF1)

if __name__ == "__main__":
    faz = sys.argv[1]
    if faz == "alt":
        sw.CloseAllDocuments(True); kap_yag(); firin_kapak(); Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        sw.CloseAllDocuments(True); st = Station(ROOT, "OVEN"); kasa(st); print("kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "asm":
        sw.CloseAllDocuments(True); st = Station(ROOT, "OVEN"); st.load_dir(); print("kasa parca yuklendi:", len(st.parts))
        C_TEPSI = [0, 3*M, 40*M]                 # TEPSI_D320 yerel merkez (disk 0,0 · kulp öne)
        for (cx, cy, cz) in ((350, 352, -300), (350, 884, -300)):    # kesme zemininde · sprey nişinde
            st.add_instance(os.path.join(ORTAK, "TEPSI_D320", "TEPSI_D320.SLDASM"), [cx*M + C_TEPSI[0], cy*M + C_TEPSI[1], cz*M + C_TEPSI[2]])
        st.add_instance(os.path.join(ORTAK, "KAP_YAG_14x68x24", "KAP_YAG_14x68x24.SLDASM"), offset_mm=(110, 890, 0))   # yağ kabı: kap merkezi x=110, raf üstü y=890
        for y0 in (1120, 1400):                  # cam kapak ×2: sol kenar x=30, alt kenar y=y0
            st.add_instance(os.path.join(ORTAK, "FIRIN_KAPAK_CAM", "FIRIN_KAPAK_CAM.SLDASM"), offset_mm=(30, y0, 0))
        st.assemble("OVEN")
        e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w_ = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        d = sw.OpenDoc6(os.path.join(ROOT, "OVEN.SLDASM"), 2, 1, "", e, w_)
        for cpt in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
            if cpt.Name2.startswith(("TEPSI", "KAP_YAG", "FIRIN_KAPAK")): t = cpt.Transform2.ArrayData; print("  %-20s x=%4.0f y=%5.0f z=%4.0f" % (cpt.Name2, t[9]/M, t[10]/M, t[11]/M))
        d.ShowNamedView2("*Isometric", 7); mcall(d, "ViewZoomtofit2"); sw.FrameState = 2
