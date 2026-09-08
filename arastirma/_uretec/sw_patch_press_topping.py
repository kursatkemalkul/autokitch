# -*- coding: utf-8 -*-
# sw_all.py içindeki press() ve topping() bloklarını teknik resimlere (v8 / v25-v27) göre değiştirir
import io
P = 'sw_all.py'
a = io.open(P, encoding='utf-8').read()
i0 = a.index('# ============================== 2 · PRESS 70'); i1 = a.index('# ============================== 4 · OVEN 70')
new = r'''# ============================== 2 · PRESS 70 (ist2_pres_detay_v8) ==============================
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
    st.box(p+"uc_catal_sirt", 280, 420, 1174, 1254, -380, -330); st.box(p+"uc_catal_lama_1", 290, 306, 1176, 1188, -330, 170); st.box(p+"uc_catal_lama_2", 394, 410, 1176, 1188, -330, 170)
    st.box(p+"uc_catal_flans_ISO9409", 320, 380, 1254, 1266, -380, -330)
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

'''
a = a[:i0] + new + a[i1:]
io.open(P, 'w', encoding='utf-8').write(a); print("sw_all ok")
