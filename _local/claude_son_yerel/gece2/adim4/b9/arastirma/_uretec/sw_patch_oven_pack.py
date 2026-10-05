# -*- coding: utf-8 -*-
# sw_all.py: oven() ve pack() bloklarını teknik resimlere (OVEN v5 / PACK v4) göre değiştirir; PRESS çatal düzeltmesi
import io
P = 'sw_all.py'
a = io.open(P, encoding='utf-8').read()
# --- PRESS çatal lamaları öne taşıyordu (z +170) → yuva içinde 500 uzun, arkaya doğru
a = a.replace('st.box(p+"uc_catal_sirt", 280, 420, 1174, 1254, -380, -330); st.box(p+"uc_catal_lama_1", 290, 306, 1176, 1188, -330, 170); st.box(p+"uc_catal_lama_2", 394, 410, 1176, 1188, -330, 170)',
              'st.box(p+"uc_catal_sirt", 280, 420, 1174, 1254, -600, -550); st.box(p+"uc_catal_lama_1", 290, 306, 1176, 1188, -550, -50); st.box(p+"uc_catal_lama_2", 394, 410, 1176, 1188, -550, -50)')
a = a.replace('st.box(p+"uc_catal_flans_ISO9409", 320, 380, 1254, 1266, -380, -330)', 'st.box(p+"uc_catal_flans_ISO9409", 320, 380, 1254, 1266, -600, -550)')
i0 = a.index('# ============================== 4 · OVEN 70'); i1 = a.index('# ============================== HAT üst montajı')
new = r'''# ============================== 4 · OVEN 70 (ist4_oven_detay_v5) ==============================
# dikey (cm): plint 12 (hava giriş ızgarası) · PANO 20 (12–32) · KESME 50 (32–82) · YAĞ+SPREY 30 (82–112, sıcak dolap 42 °C) · FIRIN 56 (112–168, OMAKE 64×60×56 2 kat) · PLENUM 12 + fan Ø120 (168–180) · karbon filtre 5 (180–185) · üst boşluk 12 (185–197)
# plan: fırın 60 derin + arka 24 (kanal 20 hava+kablo+buhar, pompa arkada); yan yalıtım 3+3
def oven():
    st = Station(os.path.join(ROOT, "4_OVEN"), "OVEN"); p = "OVEN_"; W = 700.0
    shell(st, p, W, "plint"); sove_L(st, p, W, Y0, H)
    st.box(p+"plint_izgara_paneli", 60, 640, 30, 110, 18.5, 20, [(80+i*40, 100+i*40, 40, 100, 17, 21) for i in range(14)])
    st.box(p+"yalitim_tasyunu_sol", T_DIS, 31.5, Y0, 1850, ZK+T_DIS, -20); st.box(p+"yalitim_tasyunu_sag", 668.5, W-T_DIS, Y0, 1850, ZK+T_DIS, -20)
    st.box(p+"arka_kanal_bolme_saci", 31.5, 668.5, Y0, 1850, -581, -580)     # fırın 60 + arka kanal 24 (hava + kablo + buhar)
    # --- PANO 20 (12–32): servis kapağı önde; PLC, 2 menteşe sürücüsü, 1 pres sürücüsü, 2 SSR, pompa rölesi, 24 V PSU
    door_C(st, p+"pano_kapagi_", 30, 670, Y0, 320)
    st.box(p+"pano_plakasi", 50, 650, 130, 310, -250, -248); zb = -248
    st.box(p+"pano_plc", 60, 160, 200, 300, zb, zb+75); st.box(p+"pano_psu_24V", 180, 280, 200, 300, zb, zb+110)
    for i, nm in enumerate(("mentese_1", "mentese_2", "pres")): st.box(p+"pano_surucu_%s" % nm, 300+i*70, 350+i*70, 200, 300, zb, zb+120)
    for i in range(2): st.box(p+"pano_SSR_%d" % (i+1), 520+i*60, 565+i*60, 220, 300, zb, zb+40)
    st.box(p+"pano_pompa_rolesi", 60, 110, 140, 190, zb, zb+60); st.box(p+"pano_klemens_rayi", 130, 640, 140, 147.5, zb, zb+35)
    # --- KESME 50 (32–82): zemin plakası + tepsi halkası Ø330, aktüatör 24 V 1500 N strok 100 dikey, 2 kılavuz Ø12, kızak plakası, bıçak 2×28 + 4 tırnak
    panel(st, p+"panel_kesme", 30, 670, 320, 820, cuts=[(60, 640, 340, 800)])
    st.box(p+"kesme_zemin_plakasi", 60, 640, 330, 340, -580, -30); st.cyl_y(p+"kesme_tepsi_halkasi_D330", 350, -300, 165, 340, 346)
    st.cyl_y(p+"tepsi_D320_kesmede", 350, -300, 160, 346, 352); st.box(p+"tepsi_kulpu_kesmede", 330, 370, 346, 352, -140, -60)
    st.box(p+"kesme_ust_travers", 100, 600, 780, 800, -400, -200)
    for i, xx in enumerate((150, 550), 1): st.cyl_y(p+"kesme_kilavuz_mili_D12_%d" % i, xx, -300, 6, 400, 780)
    st.box(p+"kesme_aktuator_24V_1500N", 320, 380, 560, 780, -330, -270); st.cyl_y(p+"kesme_aktuator_mili", 350, -300, 8, 470, 560)
    st.box(p+"kesme_kizak_plakasi", 130, 570, 460, 470, -340, -260); st.box(p+"kesme_gobek_D28", 336, 364, 400, 460, -314, -286)
    for i, (x0, x1, z0, z1) in enumerate(((210, 490, -301, -299), (349, 351, -440, -160)), 1): st.box(p+"kesme_bicak_%d_2x28_t1.2" % i, x0, x1, 360, 400, z0, z1)
    # --- YAĞ + SPREY 30 (82–112): sıcak dolap PU 40 + ısıtıcı; yağ kabı 14×68×24 solda (L raflar), pompa arkada, nozül ortada 20 derin, tepsi nişi Ø32, damlalık tavası, klape 4 önde
    door_C(st, p+"yag_kabi_kapagi_", 30, 180, 820, 1120)                    # eleman: ayda 1 kap
    panel(st, p+"panel_sprey", 180, 670, 820, 1120, cuts=[(200, 650, 840, 1100)])  # robot: tepsi nişi
    st.box(p+"sicak_dolap_pu_alt", 60, 640, 822, 862, -580, -30); st.box(p+"sicak_dolap_pu_ust", 60, 640, 1080, 1118, -580, -30)
    st.box(p+"sicak_dolap_isitici_100W", 200, 400, 862, 872, -400, -300); st.box(p+"sicak_dolap_termostat", 420, 460, 862, 892, -380, -340)
    for side, sx in (("sol", -1), ("sag", 1)):
        xe = 110 + sx*54; st.prism_z(p+"yag_kabi_L_raf_%s" % side, [(xe, 870), (xe+sx*2, 870), (xe+sx*2, 890), (xe-sx*6, 890), (xe-sx*6, 888), (xe, 888)], -580, -30)
    xc, yb, yt = 110, 890, 1130
    st.prism_z(p+"yag_kabi_PC_govde", [(xc-70, yt-5-20), (xc+70, yt-5-20), (xc+70, yt-125), (xc+38, yb+10), (xc-38, yb+10), (xc-70, yt-125)], -560, -40)
    st.box(p+"yag_kabi_PC_kapak", xc-70, xc+70, yt-25, yt-20, -560, -40); st.cyl_y(p+"yag_kabi_dolum_agzi_D60", xc, -300, 30, yt-20, yt-8)
    for side, sx in (("sol", -1), ("sag", 1)): st.box(p+"yag_kabi_kizak_%s" % side, xc+sx*50-15, xc+sx*50+15, yb-20, yb, -560, -40)
    st.cyl_z(p+"yag_kabi_samandira", xc, yb+60, 8, -300, -200); st.cyl_z(p+"yag_kabi_kuru_baglanti_D12", xc, yb+30, 6, -600, -560)
    st.box(p+"yag_pompasi_24V", 60, 160, 900, 1000, -780, -640); st.cyl_z(p+"yag_hatti_D6", 350, 1060, 3, -640, -240)
    st.cyl_y(p+"sprey_nozulu_D8", 350, -240, 4, 1040, 1080); st.box(p+"sprey_nozul_tutucu", 330, 370, 1080, 1090, -260, -220)
    st.cyl_y(p+"tepsi_nisi_halkasi_D330", 350, -300, 165, 872, 878); st.cyl_y(p+"tepsi_D320_nisde", 350, -300, 160, 878, 884); st.box(p+"tepsi_kulpu_nisde", 330, 370, 878, 884, -140, -60)
    st.box(p+"damlalik_tavasi", 200, 500, 862, 870, -450, -150)
    # --- FIRIN 56 (112–168): OMAKE 64×60×56 (satın alınan) 2 kat, hazne 40×40×10, tepsi düzlemleri 117 / 145; cam kapaklar + menteşe motorları Ø28
    st.box(p+"OMAKE_firin_SATIN_ALINAN_64x60x56", 30, 670, 1120, 1680, -600, 0, [(100, 600, 1160, 1260, -420, 1), (100, 600, 1440, 1540, -420, 1)])
    st.box(p+"OMAKE_hazne_1_tepsi_duzlemi_117", 150, 550, 1166, 1170, -560, -60); st.box(p+"OMAKE_hazne_2_tepsi_duzlemi_145", 150, 550, 1446, 1450, -560, -60)
    glass_door(st, p+"kapak1_", 30, 670, 1120, 1400); glass_door(st, p+"kapak2_", 30, 670, 1400, 1680)
    for i, yy in enumerate((1120, 1400), 1): st.cyl_z(p+"kapak_mentese_motoru_D28_%d" % i, 655, yy+14, 14, -600, -500)
    st.box(p+"firin_arka_kanal_kablo", 620, 660, Y0, 1800, -800, -760); st.box(p+"firin_buhar_kanali", 300, 400, 1120, 1690, -760, -600)
    # --- PLENUM 12 + FAN Ø120 (168–180) · karbon filtre 5 (180–185) · üst boşluk 12 (185–197) · egzoz mekâna (baca yok)
    st.box(p+"plenum_kutusu", 40, 660, 1690, 1800, -580, -40); st.cyl_y(p+"egzoz_fani_D120", 500, -300, 60, 1700, 1790)
    st.box(p+"karbon_filtre_40x40x5_opsiyon", 150, 550, 1800, 1850, -500, -100); st.box(p+"egzoz_izgarasi_ust", 400, 600, 1958, 1968.5, -500, -300)
    door_C(st, p+"fan_filtre_kapagi_", 30, 670, 1680, 1950); panel(st, p+"panel_ust_serit", 30, 670, 1950, H)
    return st.assemble("OVEN")

# ============================== 5 · PACK 70 (kutu_istasyonu_teknik_v4) ==============================
# dikey (cm): plint 12 · PANO 18 (12–30) · step + vakum pompası 15 (30–45) · BOYUNDURUK 10 (45–55, 36×72 profil) · KALIP 5 (55–60, plaka 3 mm 66×79, pencere 32,5) · YÜKLEME 44 (60–104) · ŞARJÖR 84 (104–188, 525 blank 40×76) · üst pay 9
def pack():
    st = Station(os.path.join(ROOT, "5_PACK"), "PACK"); p = "PACK_"; W = 700.0
    shell(st, p, W, "plint"); sove_L(st, p, W, Y0, H)
    # --- PANO 18 (12–30): PLC, step sürücü, 2 motor sürücü, 3 servo sürücü, 24 V
    door_C(st, p+"pano_kapagi_", 30, 670, Y0, 300)
    st.box(p+"pano_plakasi", 50, 650, 130, 290, -250, -248); zb = -248
    st.box(p+"pano_plc_IO", 60, 180, 180, 280, zb, zb+75); st.box(p+"pano_psu_24V", 200, 300, 180, 280, zb, zb+110)
    st.box(p+"pano_step_surucu", 320, 370, 180, 280, zb, zb+120)
    for i in range(2): st.box(p+"pano_motor_surucu_%d" % (i+1), 390+i*60, 435+i*60, 180, 280, zb, zb+100)
    for i in range(3): st.box(p+"pano_servo_surucu_%d" % (i+1), 520+i*45, 555+i*45, 180, 280, zb, zb+60)
    st.box(p+"pano_klemens_rayi", 60, 640, 140, 147.5, zb, zb+35)
    # --- STEP + VAKUM 15 (30–45): NEMA23 + bilyalı vida 1605 + 2 lineer ray Ø16; vakum pompası diyafram 30 L/dk + tank 1 L + 2 selenoid
    panel(st, p+"panel_mekanizma", 30, 670, 300, 600)
    st.box(p+"step_motor_NEMA23", 322, 379, 300, 380, -430, -373); st.cyl_y(p+"bilyali_vida_1605", 350, -400, 8, 380, 900); st.box(p+"vida_somunu_1605", 330, 370, 480, 520, -420, -380)
    for i, xx in enumerate((150, 550), 1): st.cyl_y(p+"lineer_ray_D16_%d" % i, xx, -400, 8, 300, 900); st.box(p+"lineer_rulman_%d" % i, xx-15, xx+15, 470, 530, -415, -385)
    st.box(p+"vakum_pompasi_30Ldk", 440, 580, 300, 440, -700, -560); st.box(p+"vakum_tanki_1L", 100, 200, 300, 440, -700, -600)
    for i in range(2): st.box(p+"vakum_selenoid_%d" % (i+1), 220+i*50, 260+i*50, 320, 370, -680, -620)
    st.cyl_z(p+"vakum_hortumu_D8", 500, 420, 4, -560, -420)
    # --- BOYUNDURUK 10 (45–55): 36×72 alüminyum profil, plunger plakası 31,6×31,6×2, 6 vantuz Ø40 (4 taban + 2 kapak)
    st.box(p+"boyunduruk_profil_36x72", 120, 580, 470, 506, -436, -364); st.box(p+"plunger_plakasi_316x316x2", 192, 508, 506, 508, -558, -242)
    for i, (xx, zz) in enumerate(((230, -520), (470, -520), (230, -280), (470, -280), (300, -400), (400, -400)), 1):
        st.cyl_y(p+"vantuz_D40_%s_%d" % ("taban" if i <= 4 else "kapak", i), xx, zz, 20, 508, 538)
    # --- KALIP 5 (55–60): paslanmaz plaka 3 mm 66×79, pencere 32,5 + kalıp duvarı 4,5 derin + 4 köşe plowu
    st.box(p+"kalip_plakasi_3mm_66x79", 20, 680, 597, 600, -790, 0, [(187.5, 512.5, 596, 601, -562.5, -237.5)])
    st.prism_y(p+"kalip_duvari_45", [(185, -565), (515, -565), (515, -235), (185, -235), (185, -237.5), (512.5, -237.5), (512.5, -562.5), (187.5, -562.5), (187.5, -237.5), (185, -237.5)], 552, 597)
    for i, (xx, zz) in enumerate(((187.5, -562.5), (512.5, -562.5), (187.5, -237.5), (512.5, -237.5)), 1): st.box(p+"kose_plowu_%d" % i, xx-10, xx+10, 552, 597, zz-10, zz+10)
    # --- YÜKLEME 44 (60–104): kutu plakada (açık, kapak arkada dik), kapak kolu U Ø8 + redüktörlü 24 V motor, 3 flap parmağı (servo), robot klapesi önde
    panel(st, p+"panel_kutulama", 30, 670, 600, 1040, cuts=[(60, 640, 620, 1020)])
    st.box(p+"kutu_taban_32x32_ornek", 190, 510, 600, 640, -560, -240); st.box(p+"kutu_kapak_32x32_ornek_dik", 190, 510, 640, 960, -562, -558)
    st.cyl_z(p+"kapak_kolu_U_D8_yatay", 130, 980, 4, -600, -520); st.box(p+"kapak_kolu_U_dikey_1", 126, 134, 640, 980, -604, -596); st.box(p+"kapak_kolu_U_dikey_2", 566, 574, 640, 980, -604, -596)
    st.box(p+"kapak_kolu_motoru_24V_reduktor", 40, 120, 610, 690, -640, -560)
    for i, xx in enumerate((150, 350, 550), 1): st.box(p+"flap_parmagi_servo_%d" % i, xx-25, xx+25, 640, 700, -230, -170); st.box(p+"flap_parmagi_%d" % i, xx-4, xx+4, 700, 760, -215, -185)
    # --- ŞARJÖR 84 (104–188): 2 L kılavuz (iç 40), alt tutucu raylar 2×76 + 4 köşe parmağı, 525 blank yığını, ön kapı (eleman)
    door_C(st, p+"sarjor_kapisi_", 30, 670, 1040, 1950)
    for i, (xx, sx) in enumerate(((140, 1), (560, -1)), 1): st.prism_y(p+"sarjor_L_kilavuz_%d" % i, [(xx, -800), (xx+sx*10, -800), (xx+sx*10, -798), (xx+sx*2, -798), (xx+sx*2, -20), (xx, -20)], 1040, 1880)
    for i, zz in enumerate((-790, -30), 1): st.box(p+"sarjor_alt_tutucu_ray_%d" % i, 150, 550, 1040, 1044, zz-10, zz+10)
    for i, (xx, zz) in enumerate(((155, -785), (545, -785), (155, -35), (545, -35)), 1): st.box(p+"sarjor_kose_parmagi_%d" % i, xx-8, xx+8, 1044, 1060, zz-8, zz+8)
    st.box(p+"blank_yigini_525_adet_40x76", 150, 550, 1044, 1880, -790, -30)
    st.box(p+"sarjor_foto_sensoru_1_gun", 120, 140, 1160, 1180, -420, -400); panel(st, p+"panel_ust_pay", 30, 670, 1950, H)
    return st.assemble("PACK")

'''
a = a[:i0] + new + a[i1:]
io.open(P, 'w', encoding='utf-8').write(a); print("sw_all ok")
