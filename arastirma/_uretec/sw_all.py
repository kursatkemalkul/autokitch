# -*- coding: utf-8 -*-
# AUTOKITCH — 5 istasyon AYRI PARÇALI sac kasa + iç donanım + istasyon montajları + HAT üst montajı (SolidWorks 2025 COM) (7 Eyl 2026)
# kullanım: python sw_all.py store press topping oven pack hat
import sys, os, time
from sw_lib import *

ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
def panel(st, p, x0, x1, y0, y1, cuts=()):   # sabit ön sac 1,5 (ön düzlem), istenirse açıklık kesmeli
    st.box(p, x0, x1, y0, y1, ZF0, ZF1, [(c[0], c[1], c[2], c[3], ZF0-1, ZF1+1) for c in cuts])
def cm(*v): return [x*10.0 for x in v]

# ============================== 1 · STORE 140 ==============================
def store():
    st = Station(os.path.join(ROOT, "1_STORE"), "STORE"); p = "STORE_"; W = 1400.0; PU = 60.0
    shell(st, p, W, "feet")
    xi0, xi1, zi = insulated_cell(st, p, W, 182.5, 1610.0, PU, ytop_single=1670.0)
    # yatay ayırıcı PU80 + orta dikey bölme 24
    st.box(p+"ayirici_sac_alt", xi0, xi1, 690, 691, zi, 0); st.box(p+"ayirici_pu", xi0, xi1, 691, 765, zi, 0); st.box(p+"ayirici_sac_ust", xi0, xi1, 765, 766, zi, 0)
    st.box(p+"orta_bolme_sac_sol", 690, 691, 182.5, 1610, zi, 0); st.box(p+"orta_bolme_pu", 691, 713, 182.5, 1610, zi, 0); st.box(p+"orta_bolme_sac_sag", 713, 714, 182.5, 1610, zi, 0)
    # söveler L + orta T (tam boy)
    sove_L(st, p, W, Y0, H, side=66.0)
    xm = 702.0; st.prism_y(p+"sove_orta", [(690, ZF1), (690, ZF0), (xm-0.75, ZF0), (xm-0.75, 0), (xm+0.75, 0), (xm+0.75, ZF0), (714, ZF0), (714, ZF1)], 182.5, 1610)
    # sabit paneller
    panel(st, p+"panel_sogutma", 66, W-66, 1670, H); panel(st, p+"panel_bant_ust", 66, W-66, 1610, 1670)
    panel(st, p+"panel_ayirici_on", 66, W-66, 690, 766); panel(st, p+"panel_bos_bant", 714, 1338, 403, 687); panel(st, p+"panel_bant_alt", 66, W-66, Y0, 182.5)
    # soğutma: 2 kompresör grubu teknik bölmede, 2 evaporatör hücre arkasında (+3 üst, −18 alt)
    cooling_unit(st, p+"sog1_", 80, 1680, -100); cooling_unit(st, p+"sog2_", 720, 1680, -100)
    for i, (y0, y1) in enumerate(((1400, 1500), (500, 600)), 1):
        st.box(p+"evaporator_%d" % i, 200, 1200, y0, y1, -750, -650); st.cyl_z(p+"evap_fan_%d" % i, 700, (y0+y1)/2, 90, -790, -750)
    # çekmeceler: sandviç ön 40 (1,5 + 37,5 PU + 1,0) + kulp oyuğu + kutu U 1,0 + arka + teleskopik ray çifti
    FRONT = [('cekmece_icecek_1', 66, 690, 1484, 1608), ('cekmece_icecek_2', 66, 690, 1354, 1478), ('cekmece_icecek_3', 66, 690, 1224, 1348), ('cekmece_icecek_4', 66, 690, 1094, 1218), ('cekmece_1L', 66, 690, 772, 1088),
             ('cekmece_taze_1', 714, 1338, 1509, 1608), ('cekmece_taze_2', 714, 1338, 1404, 1503), ('cekmece_taze_3', 714, 1338, 1299, 1398), ('cekmece_taze_4', 714, 1338, 1194, 1293),
             ('cekmece_taze_5', 714, 1338, 1089, 1188), ('cekmece_taze_6', 714, 1338, 984, 1083), ('cekmece_taze_7', 714, 1338, 879, 978), ('cekmece_taze_8', 714, 1338, 774, 873),
             ('cekmece_donmus_1', 66, 690, 297, 391), ('cekmece_donmus_2', 66, 690, 197, 291), ('cekmece_donmus_3', 714, 1338, 297, 391), ('cekmece_donmus_4', 714, 1338, 197, 291)]
    for nm, x0, x1, y0, y1 in FRONT + [('klape_kaset_kati', 66, 690, 403, 687)]:
        a, b, c, d = x0+3, x1-3, y0+3, y1-3; q = p + nm + "_"
        kw = 300 if nm.startswith('cekmece') else 180; kx = (a+b)/2 - kw/2; ky = d - 60
        kul = [(kx, kx+kw, ky, ky+34, 27, 41)]
        st.box(q+"on_ic_sac", a, b, c, d, 0, 1); st.box(q+"on_pu", a, b, c, d, 1, 38.5, kul); st.box(q+"on_dis_sac", a, b, c, d, 38.5, 40, kul)
        st.box(q+"kulp_cukuru", kx-1, kx+kw+1, ky-1, ky+35, 26, 27)
        if nm.startswith('cekmece'):
            ka, kb, kc, kd = a+13.7, b-13.7, c+8, d-12
            st.prism_z(q+"kutu", [(ka, kd), (ka, kc), (kb, kc), (kb, kd), (kb-1, kd), (kb-1, kc+1), (ka+1, kc+1), (ka+1, kd)], -600, 0)
            st.box(q+"kutu_arka", ka, kb, kc, kd, -600, -599); rails(st, q, ka-13.7, kb+13.7, kc+10, 0)
        else:   # klape: alt pivot + gazlı amortisörler + kaset katı rafı (4 donmuş kap 200×300×150)
            st.box(q+"pivot_mil", a-10, b+10, c+2, c+10, -8, 0)
            for i, xx in enumerate((a+15, b-33), 1): st.box(q+"gazli_amortisor_%d" % i, xx, xx+18, c+30, c+230, -30, -12)
            st.box(q+"raf", xi0, 690, 403, 404.5, zi, 0)
            for i in range(4): st.box(q+"donmus_kap_%d" % (i+1), 80+i*150, 80+i*150+140, 405, 555, -400, -100)
    return st.assemble("STORE")

# ============================== 2 · PRESS 70 (ist2_pres_detay_v8) ==============================
# dikey (zeminden cm): ayak 12 · PZP-400 zeminde 95 (64×80×95, 170 kg) · tepsi rafı 8 · uç yuvaları 14 · pay 2 · kova 44 (sol 35 = 30 L kova, sağ 35 boş) · kol boşluğu 14 · üst 4 = 197
def press():
    st = Station(os.path.join(ROOT, "2_PRESS"), "PRESS"); p = "PRESS_"; W = 700.0
    shell(st, p, W, "feet"); sove_L(st, p, W, Y0, H)
    # ön yüz: pres ağzı açıklığı 72–108 (robot), sol kova kapağı 134–178 (eleman), kol boşluğu 175–189 açıklığı (robot atığı kovaya bırakır)
    panel(st, p+"panel_alt", 30, 670, Y0, 700); panel(st, p+"panel_pres_agzi", 30, 670, 700, 1340, cuts=[(100, 600, 720, 1080)])
    door_C(st, p+"kova_kapagi_", 30, 340, 1340, 1780); panel(st, p+"panel_ust_sol", 30, 340, 1780, 1950, cuts=[(50, 320, 1760, 1900)])
    panel(st, p+"panel_ust_sag", 340, 670, 1340, 1950)
    # FERSAH PZP-400 (satın alınan, zeminde): gövde 640×800×950 + ağız oyuğu; alt ısıtmalı plaka Ø340 (zeminden ~90) + üst plaka Ø290 (Fersah sorusu) + piston + motor/rezistans gövdesi
    st.box(p+"PZP400_govde_SATIN_ALINAN", 30, 670, Y0, 1070, -800, 0, [(100, 600, 720, 1080, -520, 1)])
    st.cyl_y(p+"PZP400_alt_plaka_D340", 350, -280, 170, 890, 910); st.cyl_y(p+"PZP400_ust_plaka_D290", 350, -280, 145, 1000, 1020)
    st.cyl_y(p+"PZP400_piston_mili", 350, -280, 20, 1020, 1070); st.box(p+"PZP400_motor_rezistans_govdesi", 80, 620, 150, 400, -750, -250)
    st.cyl_y(p+"tepsi_D320_preste", 350, -280, 160, 910, 916); st.box(p+"tepsi_kulpu_preste", 330, 370, 910, 916, -120, -40)
    # TEPSİ RAFI 8 (107–115): raf sacı + 2 tepsi Ø320 yan yana (kulp öne) — 3. tepsi robot kolunda
    shelf(st, p+"tepsi_rafi_", 40, 660, 1072, -800, -20)
    for i, xx in enumerate((190, 510), 1): st.cyl_y(p+"tepsi_D320_%d" % i, xx, -300, 160, 1080, 1086); st.box(p+"tepsi_kulpu_%d" % i, xx-20, xx+20, 1080, 1086, -140, -60)
    # UÇ YUVALARI 14 (115–129): yatay yan yana — PENÇE · ÇATAL · yedek (boş); kilit pimi
    shelf(st, p+"uc_rafi_", 40, 660, 1152, -800, -20)
    for nm, xx in (("pence", 130), ("catal", 350), ("yedek", 570)):
        st.box(p+"uc_yuvasi_%s" % nm, xx-90, xx+90, 1154, 1174, -400, -60); st.box(p+"uc_kilit_pimi_%s" % nm, xx-6, xx+6, 1174, 1214, -240, -228)
    st.box(p+"uc_pence_govde", 60, 200, 1174, 1254, -360, -100); st.box(p+"uc_pence_parmak_1", 70, 90, 1254, 1284, -300, -160); st.box(p+"uc_pence_parmak_2", 170, 190, 1254, 1284, -300, -160)
    st.box(p+"uc_catal_sirt", 280, 420, 1174, 1254, -600, -550); st.box(p+"uc_catal_lama_1", 290, 306, 1176, 1188, -550, -50); st.box(p+"uc_catal_lama_2", 394, 410, 1176, 1188, -550, -50)
    st.box(p+"uc_catal_flans_ISO9409", 320, 380, 1254, 1266, -600, -550)
    # KOVA 30 L (Ø30×45) sol yarı, kapaksız, poşet kelepçeli, öne çekilir (kızak) — üstünde kol boşluğu 14
    st.cyl_y(p+"cop_kovasi_30L_D300", 185, -300, 150, 1320, 1770); st.cyl_y(p+"poset_kelepcesi_D320", 185, -300, 160, 1770, 1790)
    st.box(p+"kova_kizagi_sol", 20, 40, 1300, 1320, -500, -60); st.box(p+"kova_kizagi_sag", 330, 350, 1300, 1320, -500, -60); st.box(p+"kova_tabani", 40, 330, 1300, 1310, -460, -140)
    # sağ yarı BOŞ (35×59×84, büyüme payı) — yalnız küçük kontrol panosu arkada
    st.box(p+"kontrol_panosu_kucuk", 380, 640, 1400, 1700, -300, -120)
    return st.assemble("PRESS")

# ============================== 3 · TOPPING 70 (ist3_topping_detay_v25/v27) ==============================
# dikey (cm): soğutma 0–20 (plint içi) · ALT sıra 2 20–47 (park ×2 + çözülme ×2) · ALT sıra 1 47–74 (kaşar yedek ×4) · kat 3 boşluk 74–88 + kap 88–115 · kat 2 115–156 · kat 1 156–197
# plan: sol kanal 20 (evaporatör + fan) · kaplar x 27 / 43 (14×68×24, arkaya dayalı, ara mil yok) · sağ kanal 20 (hava dönüşü + kablo) · arka duvar 10 (motor + pano) · klape önde
def topping():
    st = Station(os.path.join(ROOT, "3_TOPPING"), "TOPPING"); p = "TOPPING_"; W = 700.0; PU = 40.0; YB = 200.0
    shell(st, p, W, "plint", y0=YB); sove_L(st, p, W, YB, H)
    xi0, xi1, zi = insulated_cell(st, p, W, YB+42.5, 1968.5-T_IC, PU, pu_back=20.0, y0=YB, top_pu=False)   # üst PU yok (kat 27 tam dolu; v23: üst teknik yok)
    # SOĞUTMA GRUBU 0–20 (plint içinde, hava önden ızgaradan): yatık kompresör Ø100×200 + kondenser + fan; ön ızgara paneli
    st.cyl_z(p+"sog_kompresor_yatik_D100", 200, 105, 50, -600, -400); st.box(p+"sog_kondenser", 300, 600, 30, 180, -300, -240); st.cyl_z(p+"sog_kondenser_fan_D140", 450, 105, 70, -240, -200)
    st.box(p+"plint_izgara_paneli", 60, 640, 40, 170, 18.5, 20, [(80+i*40, 100+i*40, 50, 160, 17, 21) for i in range(14)])
    # EVAPORATÖR sol kanalda (x 0–20), fan ×2; sağ kanal hava dönüş ızgarası + kablo kanalı
    st.box(p+"evaporator_sol_kanal", xi0+5, xi0+130, 400, 1500, -600, -200)
    for i, yy in enumerate((550, 1250), 1): st.box(p+"evap_fan_%d" % i, xi0+130, xi0+160, yy-70, yy+70, -470, -330)
    st.box(p+"sag_kanal_kablo_kanali", xi1-45, xi1-5, YB+50, 1900, -700, -660); st.box(p+"sag_kanal_hava_donus_izgarasi", xi1-160, xi1-50, 300, 1500, -20, -18)
    # ARKA DUVAR 10 cm (z −800..−720): motorlar (yassı step 57×57×40) + soketler; elektrik panosu (yassı) arka duvar içinde
    st.box(p+"arka_duvar_pano_plakasi", 100, 600, 300, 700, -778, -776); st.box(p+"arka_duvar_pano_plc", 120, 220, 560, 670, -776, -736)
    st.box(p+"arka_duvar_pano_guc_kaynagi", 240, 340, 560, 670, -776, -736)
    for i in range(6): st.box(p+"arka_duvar_pano_surucu_%d" % (i+1), 120+i*80, 170+i*80, 330, 530, -776, -736)
    st.box(p+"arka_duvar_kapak_saci", xi0, xi1, YB+42.5, 1960, -722, -720)
    # KAT ve ALT yerleşimi: (ad, raf üst kotu y, kaplar (x merkez, ad)) — kap 240 yüksek + kızak 20 + raf 2 → kat 27
    KAP_X = {"kat": (270, 430), "alt": (115, 272, 428, 585)}
    LAYOUT = [("kat1", 1710, [(270, "kasar_A"), (430, "sucuk")]), ("kat2", 1300, [(270, "kasar_B"), (430, "kavurma")]), ("kat3", 890, [(270, "kiyma"), (430, "kusbasi")]),
              ("alt1", 480, [(115, "kasar_yedek_1"), (272, "kasar_yedek_2"), (428, "kasar_yedek_3"), (585, "kasar_yedek_4")]),
              ("alt2", 210, [(428, "cozulme_kiyma"), (585, "cozulme_kusbasi")])]
    for zone, yr, kaps in LAYOUT:
        q = p + zone + "_"; xs = KAP_X["kat"] if zone.startswith("kat") else KAP_X["alt"]
        for j, xc in enumerate(xs, 1):     # kabin L raf çifti 20×8×2 (dik kenar dışta) her pozisyonda + ön çapraz çubuk + kapak pimi Ø8 (v27)
            for side, sx in (("sol", -1), ("sag", 1)):
                xe = xc + sx*54
                pts = [(xe, yr), (xe+sx*2, yr), (xe+sx*2, yr+20), (xe-sx*6, yr+20), (xe-sx*6, yr+18), (xe, yr+18)]
                st.prism_z(q+"L_raf_%d_%s" % (j, side), pts, zi, -20)
            st.box(q+"capraz_cubuk_%d" % j, xc-58, xc+58, yr+22, yr+30, -60, -52)
            if zone.startswith("kat"): st.cyl_z(q+"kapak_pimi_D8_%d" % j, xc+30, yr+34, 4, -60, -40)
        for xc, nm in kaps:                 # KAP 14×68×24 Picnic tipi: PC 5 mm gövde (simetrik kama 55°, U-oluk R38), helezon POM Ø70, tarak mili, geçmeli kapak, 2 kızak
            r = q + "kap_" + nm + "_"; yb = yr + 20; yt = yb + 240
            st.prism_z(r+"PC_govde", [(xc-70, yt-5), (xc+70, yt-5), (xc+70, yt-105), (xc+38, yb+10), (xc-38, yb+10), (xc-70, yt-105)], -700, -20)
            st.box(r+"PC_kapak", xc-70, xc+70, yt-5, yt, -700, -20)
            st.cyl_z(r+"helezon_POM_D70", xc, yb+48, 35, -700, -100); st.cyl_z(r+"helezon_topuz_D50", xc, yb+48, 25, -720, -700)
            st.cyl_z(r+"tarak_mili_D12", xc, yb+150, 6, -700, -40); st.cyl_z(r+"tarak_topuz_D30", xc, yb+150, 15, -720, -700)
            for side, sx in (("sol", -1), ("sag", 1)): st.box(r+"kizak_%s" % side, xc+sx*50-15, xc+sx*50+15, yb-20, yb, -700, -20)
            st.box(r+"on_cekme_dudagi", xc-70, xc+70, yt, yt+15, -35, -20); st.box(r+"agiz_kapagi_PC", xc-30, xc+30, yb+10, yb+15, -90, -25)
            st.cyl_z(r+"soket_helezon", xc, yb+48, 15, -740, -720); st.cyl_z(r+"soket_tarak", xc, yb+150, 15, -740, -720)
            st.box(r+"motor_helezon_57x57x40", xc-28, xc+28, yb+20, yb+76, -780, -740); st.box(r+"motor_tarak_57x57x40", xc-28, xc+28, yb+122, yb+178, -780, -740)
    # KLAPELER (aşağı açılır): kat1 156–195 · kat2 115–156 · kat3 74–115 · ALT 46–74 · ALT 20–46 ; üst şerit 195–197 sabit
    for nm, y0, y1 in (("kat1", 1560, 1950), ("kat2", 1150, 1560), ("kat3", 740, 1150), ("alt1", 460, 740), ("alt2", YB, 460)): door_C(st, p+"klape_"+nm+"_", 30, 670, y0, y1, hinge="bottom")
    panel(st, p+"panel_ust_serit", 30, 670, 1950, H)
    return st.assemble("TOPPING")

# ============================== 4 · OVEN 70 (ist4_oven_detay_v5) ==============================
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

# ============================== HAT üst montajı ==============================
def hat():
    sw.NewDocument(TPL_ASM, 0, 0, 0); asm = sw.ActiveDoc; x = 0.0
    for folder, name, wcm in (("1_STORE", "STORE", 140), ("2_PRESS", "PRESS", 70), ("3_TOPPING", "TOPPING", 70), ("4_OVEN", "OVEN", 70), ("5_PACK", "PACK", 70)):
        path = os.path.join(ROOT, folder, name + ".SLDASM"); W = wcm*10.0
        e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        d = sw.OpenDoc6(path, 2, 1, "", e, w); bb = [1e9]*3 + [-1e9]*3
        for cpt in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
            g = cpt.GetBox(False, False)
            for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        if asm.AddComponent5(path, 0, "", False, "", c[0] + x*M, c[1], c[2]) is None: raise RuntimeError("alt montaj eklenemedi " + name)
        sw.CloseDoc(os.path.basename(path)); x += W
    comps = list(asm.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    for cpt in comps: cpt.Select4(True, NUL, False)
    mcall(asm, "FixComponent"); asm.ClearSelection2(True)
    for cpt in comps: t = cpt.Transform2.ArrayData; print("  %-12s x=%5.0f y=%3.0f z=%3.0f" % (cpt.Name2, t[9]/M, t[10]/M, t[11]/M))
    out = os.path.join(ROOT, "FULL_MAKINE"); ok = saveas(asm, os.path.join(out, "HAT.SLDASM"))
    png(asm, os.path.join(out, "HAT_asm_iso.png"), "*Isometric", 2000, 1000); png(asm, os.path.join(out, "HAT_asm_on.png"), "*Front", 2000, 900)
    print("HAT.SLDASM kayit=%s, alt montaj=%d, toplam %.0f mm" % (ok, len(comps), x))

if __name__ == "__main__":
    sw.CloseAllDocuments(True); t = time.time()
    for a in sys.argv[1:]: globals()[a]()
    print("TOPLAM %.0f s" % (time.time()-t))
