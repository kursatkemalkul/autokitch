# -*- coding: utf-8 -*-
# AUTOKITCH — 4 · OVEN v4 (11 Eyl 2026) — TEK KABINDE 3 HAZNE, ORTAK HAVUZ   (v3 = 4_OVEN_v3, dokunulmadi)
#
# KARAR (Kemal, 11 Eyl): iki firin istasyonu olmayacak (makine buyuyordu). Tek kabin, 3 tas tabanli hazne,
# hepsi ayni sicaklik (~370 C, usta teyidi), HER URUN HER HAZNEYE (pide + lahmacun ortak havuz).
# Simulasyon: 25 dk hedefinde 21,7 -> 24,1 urun/saat; sadece-pide gununde 12 -> 21. Hazne bagimsiz
# acilir/kapanir (sakin saatte BEYIN birini kapatir). Lahmacun kaplamasiz DELIKLI tepside tas ustunde.
#
# DIKEY BUTCE (mm) — v3'ten 280 mm yer acildi:
#   plint        0    - 120
#   YAG + PANO   123  - 370   yag kabi ONDE (v3 ile ayni), pano ARKA DUVARDA (z -790..-678) -> PANO bandi kalkti (247)
#   ISLEM AGZI   373  - 533   ACIK, tepsi duzlemi 410; sprey nozulu agzin icinde
#   MEKANIZMA    536  - 816   kesici (331 -> 280: kompakt aktuator, govde 135 — teyit)  |  bicak + sprey AYRI
#   FIRIN        819  - 1659  3 SAC KAPAK (CAM YOK — kapali mutfak karari), 3 hazne 40x40x10, dis 640x600x840 (3 katli model teyit: OMAKE/Fimak/Oztiryakiler)
#   EGZOZ        1662 - 1968  plenum + fan + karbon filtre
# CEPHE STANDARDI ayni: bukme sac 1,5, 20 mm donus, on yuz z 38,5..40, fuga 3, kulp yok.
import sys, os
from sw_lib import *

ARA  = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "4_OVEN_v4"); ORTAK = os.path.join(ARA, "_ortak")
P    = "O4_"
W, T, FUGA, SOVE = 700.0, 1.5, 3.0, 30.0
TY, TIC = 25.0, 1.0                                  # tas yunu 25 + ic sac 1,0 (hucre 645 -> OMAKE 640 sigar)
XI0, XI1 = T + TY + TIC, W - T - TY - TIC            # hucre ici 32,5 .. 667,5
ZC = -20.0                                           # hucre on yuzu (cephe sandvicinin arkasi)
XP0, XP1 = SOVE + FUGA, W - SOVE - FUGA              # cephe paneli 33..667 -> dusey fuga da 3 mm
KOR0, KOR1 = 14.0, 15.5                              # fuga kor lamasi z araligi
# kor lamasi y araliklari — fugayi ortuyor, komsu parcalara girmiyor
LAMA_Y = ((114.0, 129.0), (805.0, 821.0), (1650.0, 1672.0))   # 370-373 boslugunu agiz_tabani kapatiyor; 821: kapak pivot mili 825'te basliyor

YAG    = (123.0, 370.0)                              # yag kabi onde + PANO arka duvarda (ayni band)
PANO   = YAG
AGIZ   = (373.0, 533.0)                              # ACIK islem agzi
MEK    = (536.0, 816.0)                              # kesici, 280 (v3: 331)
FIRIN  = (819.0, 1659.0)                             # 3 hazne, 840
EGZOZ  = (1662.0, 1968.0)
N_HAZNE = 3
FKAP   = tuple((FIRIN[0]+3.0+i*280.0, FIRIN[0]+278.0+i*280.0) for i in range(N_HAZNE))   # 3 cam kapak 275
Y_TEPSI = 410.0                                      # tepsi duzlemi (islem agzinin icinde)
KAPILAR = (("yag",   YAG,   True,  (YAG[0]+50.0,   YAG[1]-90.0)),
           ("mek",   MEK,   False, ()),
           ("egzoz", EGZOZ, True,  (EGZOZ[0]+60.0, EGZOZ[1]-100.0)))


def panel(ad, y0, y1, kapi, mentese=()):
    """bukme sac 1,5 duz panel: on plaka z 38,5..40 + 20 mm kenar donusleri. KULP YOK."""
    st_ = panel.st
    st_.prism_y(P+ad, [(XP0, ZF1), (XP0, 20.0), (XP0+T, 20.0), (XP0+T, ZF0),
                       (XP1-T, ZF0), (XP1-T, 20.0), (XP1, 20.0), (XP1, ZF1)], y0, y1)
    st_.box(P+ad+"_donus_alt", XP0+T, XP1-T, y0, y0+T, 20.0, ZF0)
    st_.box(P+ad+"_donus_ust", XP0+T, XP1-T, y1-T, y1, 20.0, ZF0)
    # mentese ve mandal ORTAK PARCA (_ortak/MENTESE_GIZLI_34 · MANDAL_BAS_AC) -> asm() de ornek


def firin_kapak_v3():
    """FIRIN CAM KAPAGI — asagi acilir, alt pivotlu, motor KABIN ICINDE (v2 de sovenin icine giriyordu).
       Yerel: sol alt kose (0,0); 634 x 275; sandvic z 20..40 (cift cam 4+4 + hava)"""
    ad = "FIRIN_KAPAK_V3"; st = Station(os.path.join(ORTAK, ad), ad); p = "FK3_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    w_, h_ = 634.0, 275.0        # cephe paneli 634 (dusey fuga 3 mm)
    st.prism_y(p+"cerceve_sol", [(0.0, ZF1), (0.0, 20.0), (25.0, 20.0), (25.0, ZF1)], 0.0, h_)
    st.prism_y(p+"cerceve_sag", [(w_-25, ZF1), (w_-25, 20.0), (w_, 20.0), (w_, ZF1)], 0.0, h_)
    st.box(p+"cerceve_alt", 25.0, w_-25, 0.0, 25.0, 28.0, ZF1)
    st.box(p+"cerceve_ust", 25.0, w_-25, h_-25, h_, 20.0, ZF1)
    st.box(p+"cam_dis_4mm", 25.0, w_-25, 25.0, h_-25, 34.0, 38.0)
    st.box(p+"cam_ic_4mm",  25.0, w_-25, 25.0, h_-25, 22.0, 26.0)
    st.box(p+"pivot_mili_D8", 8.0, w_-8, 3.0, 11.0, 10.0, 18.0)
    st.box(p+"mentese_kulagi_sol", 8.0, 24.0, 0.0, 14.0, 8.0, 20.0)
    st.box(p+"mentese_kulagi_sag", w_-24, w_-8, 0.0, 14.0, 8.0, 20.0)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


def firin_kapak_v4():
    """FIRIN SAC KAPAGI — CAM YOK (Kemal, 11 Eyl: kapali mutfak, cam gorunmez). Asagi acilir, alt pivotlu.
       Yerel: sol alt kose (0,0); 634 x 275 (dusey fuga 3). Kesit z 20..40: dis sac 1,5 bukme (38,5..40) + 20 mm
       kenar donusleri, ic sac 1,0 (20..21), arada TAS YUNU 17,5 (21..38,5). Pivot mili ve mentese kulaklari
       V3 ile BIREBIR — ayni motor, ayni mil, ayni yuva; yalniz kanat degisti."""
    ad = "FIRIN_KAPAK_V4"; st = Station(os.path.join(ORTAK, ad), ad); p = "FK4_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    w_, h_ = 634.0, 275.0
    st.prism_y(p+"dis_sac_1.5_bukme", [(0.0, ZF1), (0.0, 20.0), (T, 20.0), (T, ZF0),
                                       (w_-T, ZF0), (w_-T, 20.0), (w_, 20.0), (w_, ZF1)], 0.0, h_)
    st.box(p+"donus_alt", T, w_-T, 0.0, T, 20.0, ZF0)
    st.box(p+"donus_ust", T, w_-T, h_-T, h_, 20.0, ZF0)
    st.box(p+"ic_sac_1.0", T, w_-T, T, h_-T, 20.0, 21.0)
    st.box(p+"tasyunu_17.5", T, w_-T, T, h_-T, 21.0, ZF0)
    st.box(p+"pivot_mili_D8", 8.0, w_-8, 3.0, 11.0, 10.0, 18.0)
    st.box(p+"mentese_kulagi_sol", 8.0, 24.0, 0.0, 14.0, 8.0, 20.0)
    st.box(p+"mentese_kulagi_sag", w_-24, w_-8, 0.0, 14.0, 8.0, 20.0)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


def yag_kabi_v3():
    """YAG KABI — 5 L paslanmaz, one cekilir (ray uzerinde), ustte dolum agzi, arkada kuru baglanti.
       Yerel: kap sol-alt-arka kosesi (0,0,arka)"""
    ad = "YAG_KABI_5L"; st = Station(os.path.join(ORTAK, ad), ad); p = "YK_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.prism_z(p+"govde_304_1.0", [(0.0, 0.0), (300.0, 0.0), (300.0, 180.0), (298.0, 180.0),
                                   (298.0, 2.0), (2.0, 2.0), (2.0, 180.0), (0.0, 180.0)], -400.0, 0.0)
    st.box(p+"arka_sac", 2.0, 298.0, 2.0, 180.0, -400.0, -398.0)
    st.box(p+"on_sac",   2.0, 298.0, 2.0, 180.0, -2.0, 0.0)
    st.box(p+"kapak_gecmeli", 0.0, 300.0, 180.0, 182.0, -400.0, 0.0)
    st.cyl_y(p+"dolum_agzi_D60", 150.0, -200.0, 30.0, 182.0, 194.0)
    st.cyl_z(p+"emis_borusu_D8", 150.0, 20.0, 4.0, -398.0, -340.0)
    st.cyl_z(p+"kuru_baglanti_D12", 150.0, 20.0, 6.0, -420.0, -398.0)
    st.cyl_z(p+"seviye_samandirasi_D30", 60.0, 90.0, 15.0, -300.0, -260.0)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


def kasa(st):
    panel.st = st
    # plint izgarasi artik plint sacinin KENDI yarigi (ayri panel = sahte izgara idi)
    shell(st, P, W, "plint", izgara=[(80+i*40, 100+i*40, 40, 100, 17, 21) for i in range(14)])
    sove_L(st, P, W, Y0, H, SOVE)
    # ---- yalitimli kabuk: tas yunu 30 + ic sac 1,0 (sicak istasyon)
    st.box(P+"tasyunu_sol", T, T+TY, Y0+T, 1968.5, ZK+T, ZC); st.box(P+"tasyunu_sag", W-T-TY, W-T, Y0+T, 1968.5, ZK+T, ZC)
    st.box(P+"tasyunu_arka", T+TY, W-T-TY, Y0+T, 1968.5, ZK+T, ZK+T+TY)
    st.box(P+"tasyunu_taban", T+TY, W-T-TY, Y0+T, Y0+T+TY, ZK+T+TY, ZC)
    st.box(P+"ic_yan_sol", XI0-TIC, XI0, Y0+T+TY, 1968.5, ZK+T+TY, ZC)
    st.box(P+"ic_yan_sag", XI1, XI1+TIC, Y0+T+TY, 1968.5, ZK+T+TY, ZC)
    st.box(P+"ic_arka", XI0, XI1, Y0+T+TY, 1968.5, ZK+T+TY, ZK+T+TY+TIC)
    st.box(P+"ic_taban", XI0, XI1, Y0+T+TY, Y0+T+TY+TIC, ZK+T+TY+TIC, ZC)
    # =============== CEPHE ===============
    for ad, (y0, y1), kapi, ment in KAPILAR: panel("panel_"+ad, y0, y1, kapi, ment)
    # UST CEPHE SERIDI: en ust panelin ustu (1968) ile kabin tepesi (1970) arasi — diger istasyonlarla ayni
    st.part(P+"ust_cephe_seridi_1.5", [(RT, 'poly',
             [(-ZF1, 1968.0), (-ZF1, 1970.0), (-ZF0, 1970.0), (-ZF0, 1969.5), (0.0, 1969.5), (0.0, 1968.0)],
             SOVE, W-SOVE, False)])
    # ---- FUGA KOR LAMALARI: disaridan kabin icine gorus hatti kalmiyor
    for i, (l0, l1) in enumerate(LAMA_Y, 1):
        st.box(P+"fuga_kor_lamasi_%d" % i, 34.0, 666.0, l0, l1, KOR0, KOR1)
    for nm, x0, x1 in (("sol", 30.0, 34.0), ("sag", 666.0, 670.0)):     # dusey fuga arkasi
        st.box(P+"fuga_kor_dusey_%s_alt" % nm, x0, x1, Y0, AGIZ[0]-3.0, KOR0, KOR1)
        st.box(P+"fuga_kor_dusey_%s_ust" % nm, x0, x1, AGIZ[1], H, KOR0, KOR1)
    # ---- ISLEM AGZI CERCEVESI: dort kenari da cephe duzleminde biter, katman/basamak gorunmez
    a0, a1 = AGIZ
    st.prism_y(P+"agiz_cerceve_sol", [(XP0, ZF1), (40.0, ZF1), (40.0, ZC), (38.5, ZC), (38.5, ZF0), (XP0, ZF0)], a0-3.0, a1)
    st.prism_y(P+"agiz_cerceve_sag", [(XP1, ZF1), (660.0, ZF1), (660.0, ZC), (661.5, ZC), (661.5, ZF0), (XP1, ZF0)], a0-3.0, a1)
    st.box(P+"agiz_tabani", 40.0, 660.0, a0-3.0, a0, ZK+T+TY+TIC, ZF1,
           [(625.0, 670.0, a0-4.0, a0+1.0, -710.0, -650.0)])
    st.box(P+"agiz_tavani", 40.0, 660.0, a1-2.0, a1, ZK+T+TY+TIC, ZC,
           [(625.0, 670.0, a1-3.0, a1+1.0, -710.0, -650.0),
            (333.0, 367.0, a1-3.0, a1+1.0, -318.0, -282.0)]                      # kesici gobegi
           + [(xx-8.0, xx+8.0, a1-3.0, a1+1.0, -310.0, -290.0) for xx in (180.0, 500.0)])  # kilavuz milleri
    for yn, ya, yb in (("alt", a0-3.0, a0-1.5), ("ust", a1-1.5, a1)):
        st.box(P+"agiz_cep_kapagi_sol_"+yn, XP0, 38.5, ya, yb, ZC, ZF0)
        st.box(P+"agiz_cep_kapagi_sag_"+yn, 661.5, XP1, ya, yb, ZC, ZF0)
    # =============== PANO ===============
    zb = -788.0          # ARKA DUVAR: ic sac -792,5 -> plaka -790..-788, elemanlar -788..-678 (yag pompasi -600'de biter)
    st.box(P+"pano_plakasi_2mm", 60, 600, 150.0, PANO[1]-15, zb-2, zb)
    st.box(P+"pano_plc", 80, 180, 160, 280, zb, zb+75); st.box(P+"pano_guc_kaynagi_24V", 200, 300, 160, 280, zb, zb+110)
    for i, nm in enumerate(("kapak_1", "kapak_2", "kapak_3", "kesici", "pompa")):
        st.box(P+"pano_surucu_"+nm, 320+i*56, 370+i*56, 170, 290, zb, zb+110)
    for i in range(N_HAZNE): st.box(P+"pano_SSR_hazne_%d" % (i+1), 80+i*60, 130+i*60, 300, 350, zb, zb+40)
    st.box(P+"pano_klemens_rayi", 270, 590, 300, 307.5, zb, zb+35)
    st.box(P+"pano_kablo_kanali", 270, 590, 320, 360, zb, zb+40)
    # =============== YAG KABI BANDI ===============
    for i, xx in enumerate((190.0, 497.0), 1):          # +15: ic_taban ustu 147,5 -> ray 153..168
        st.box(P+"yag_kabi_rayi_%d" % i, xx, xx+12.7, YAG[0]+30, YAG[0]+45, -430.0, -30.0)
    st.box(P+"yag_kabi_tabani", XI0, XI1, YAG[0]+26, YAG[0]+30, -440.0, ZC)
    st.box(P+"yag_pompasi_24V", 470, 600, YAG[0]+90, YAG[0]+190, -600.0, -470.0)
    st.cyl_z(P+"yag_hatti_D6", 600.0, YAG[1]+40, 3.0, -560.0, -300.0)
    # =============== ISLEM ISTASYONU (tepsi yuvasi + sprey + kesici) ===============
    st.cyl_y(P+"tepsi_yuvasi_halkasi_D336", 350.0, -300.0, 168.0, Y_TEPSI-8, Y_TEPSI)
    st.box(P+"tepsi_yuvasi_tablasi", 150, 550, Y_TEPSI-12, Y_TEPSI-8, -480.0, -120.0)
    st.box(P+"damlalik_tavasi", 120, 580, Y_TEPSI-30, Y_TEPSI-24, -500.0, -100.0)
    # sprey: nozul yandan girer, kesici ekseninden 90 mm kacik -> bicakla cakismaz
    st.cyl_y(P+"sprey_nozulu_D8", 350.0, -390.0, 4.0, Y_TEPSI+90, Y_TEPSI+108)   # kola dayanir
    st.box(P+"sprey_nozul_kolu", 340, 360, Y_TEPSI+108, Y_TEPSI+118, -400.0, -330.0)
    # kesici: gobek + 4 bicak (8 dilim), kilavuz mili x2, 24 V aktuator strok 100
    # gobek kizak plakasinin ALTINA kadar; 4 bicak gobege GECMELI (govdenin icinden gecmez)
    st.cyl_y(P+"kesici_gobegi_D30", 350.0, -300.0, 15.0, Y_TEPSI+60, MEK[0]+110)
    st.box(P+"kesici_bicak_1_sol",  200.0, 335.0, Y_TEPSI+30, Y_TEPSI+90, -301.0, -299.0)
    st.box(P+"kesici_bicak_2_sag",  365.0, 490.0, Y_TEPSI+30, Y_TEPSI+90, -301.0, -299.0)
    st.box(P+"kesici_bicak_3_arka", 349.0, 351.0, Y_TEPSI+30, Y_TEPSI+90, -450.0, -315.0)
    st.box(P+"kesici_bicak_4_on",   349.0, 351.0, Y_TEPSI+30, Y_TEPSI+90, -285.0, -150.0)
    for i, xx in enumerate((180.0, 500.0), 1):
        st.cyl_y(P+"kesici_kilavuz_mili_D12_%d" % i, xx, -300.0, 6.0, Y_TEPSI+60, MEK[1]-40)
    # kizak plakasi millerin uzerinde KAYAR -> gecis delikleri
    st.box(P+"kesici_kizak_plakasi", 150, 550, MEK[0]+110, MEK[0]+125, -360.0, -240.0,
           [(xx-7.0, xx+7.0, MEK[0]+109, MEK[0]+126, -308.0, -292.0) for xx in (180.0, 500.0)])
    st.box(P+"kesici_aktuator_24V_1500N_kompakt", 320, 380, MEK[0]+125, MEK[1]-20, -340.0, -260.0)   # govde 135, strok 100 — katalog teyidi
    st.box(P+"kesici_ust_travers", 100, 600, MEK[1]-20, MEK[1], -400.0, -200.0)
    # =============== FIRIN ===============
    # 3 KATLI TAS TABANLI DECK FIRIN (satin alinan; 3 katli model teyit edilecek): dis 640x600x840, hazne 40x40x10
    st.box(P+"FIRIN_3_HAZNE_SATIN_ALINAN_64x60x84", XI0+2.5, XI1-2.5, FIRIN[0], FIRIN[1], -600.0, ZC,
           [(100, 600, FIRIN[0]+45+i*280, FIRIN[0]+145+i*280, -420.0, ZC+1) for i in range(N_HAZNE)])
    for i in range(N_HAZNE):
        st.box(P+"firin_hazne_%d_tas_taban" % (i+1), 150, 550, FIRIN[0]+46+i*280, FIRIN[0]+50+i*280, -415.0, -60.0)
    st.box(P+"firin_buhar_kanali", 300, 400, FIRIN[0], FIRIN[1]+10, -760.0, -600.0)
    # =============== EGZOZ ===============
    st.box(P+"plenum_kutusu", 50, 650, EGZOZ[0]+10, EGZOZ[1]-120, -580.0, -60.0,
           [(60, 640, EGZOZ[0]+15, EGZOZ[1]-125, -570.0, -70.0)])
    st.cyl_y(P+"egzoz_fani_D120", 500.0, -300.0, 60.0, EGZOZ[0]+20, EGZOZ[1]-130)
    st.box(P+"karbon_filtre_400x400x50", 150, 550, EGZOZ[1]-110, EGZOZ[1]-60, -500.0, -100.0)
    st.box(P+"egzoz_izgarasi_ust", 350, 550, 1958.0, 1968.5, -500.0, -300.0)
    st.box(P+"kablo_kanali_sag", XI1-45, XI1-5, 150.0, 1800.0, -700.0, -660.0)


def asm():
    st = Station(ROOT, "OVEN_v4"); st.load_dir(); print("kasa parca:", len(st.parts))
    O = lambda g: os.path.join(ORTAK, g, g + ".SLDASM")
    st.add_instance(O("YAG_KABI_5L"), offset_mm=(200.0, YAG[0]+45.0, -30.0))   # ust 168+194 = 362 < 370
    for y0, _ in FKAP:                                # 3 SAC kapak (cam yok) — ORTAK FIRIN_KAPAK_V4, 3 ornek
        st.add_instance(O("FIRIN_KAPAK_V4"), offset_mm=(XP0, y0, 0.0))
    st.add_instance(O("TEPSI_D320"), center_m=(0.350, (Y_TEPSI+3.0)*M, -0.300))     # islem yuvasinda
    for ax, az in AYAK_YERI(W):                       # ORTAK: ayar ayagi (eski 4+4 yerel parca)
        st.add_instance(O("AYAK_AYAR_M12"), offset_mm=(ax, 0.0, az))
    for ad, (y0, y1), kapi, ment in KAPILAR:          # ORTAK: gizli mentese + bas-ac mandali
        for yy in ment: st.add_instance(O("MENTESE_GIZLI_34"), offset_mm=(XP0+2.0, yy, 0.0))
        if kapi: st.add_instance(O("MANDAL_BAS_AC"), offset_mm=(XP1-90.0, (y0+y1)/2-10.0, 0.0))
    st.assemble("OVEN_v4")


if __name__ == "__main__":
    faz = sys.argv[1]; sw.CloseAllDocuments(True)
    if faz == "alt":                                  # V4'e ozel tek yeni form; kapak V3 ve yag kabi zaten _ortak'ta
        firin_kapak_v4(); Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        st = Station(ROOT, "OVEN_v4")
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
        kasa(st); print("OVEN v4 kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "parca":
        import re
        pat = re.compile(sys.argv[2]); st = Station(ROOT, "OVEN_v4"); n = [0]
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt") and pat.search(f): os.remove(os.path.join(st.pdir, f))
        orij = Station.part
        def sadece(self, fname, ops, _retry=2):
            if not pat.search(fname): return None
            n[0] += 1; return orij(self, fname, ops, _retry)
        Station.part = sadece
        Station.cyl_y = Station.cyl_z = lambda self, fname, *a: None
        kasa(st); print("yeniden uretilen parca:", n[0]); st.exit_sw()
    elif faz == "asm":
        asm(); Station(ROOT, "x").exit_sw()
