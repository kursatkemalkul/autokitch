# -*- coding: utf-8 -*-
# AUTOKITCH — 3 · TOPPING v3 — KAP paftaya (ist3_topping_detay_v26 + v27) BİREBİR modellendi (8 Eyl 2026)
# fazlar: kap → alt → kasa → asm   (her faz temiz SolidWorks oturumu; bellek şişmesine karşı)
#
# KAP kesiti (v26 · A ÖN KESİT) — ölçüler iç tabandan (y=25) yukarı:
#   yalak R38 (3,8) 25→63 · boğaz Ø76 (4,9) 63→112,3 · daire R65 (5,3) 112,3→165 · dik duvar (9,5) 165→260
#   dış: yalak R43 · daire R70 · dik ±70  → kap dış 14 / iç 13 · kızak 0..20 → toplam 26 → kat 27
#   helezon tepesi z 7,3 (y 98) · tarak göbeği z 14,0 (y 165) · süpürme R5,7 → y 108..222
# KAP boyu (v27 · A BOY KESİT) — arka dış yüz z −700, ön dış yüz z −20 (68 cm), dudakla 69,5:
#   arka duvar 0..5 · hazne 5..620 · KAPALI BORU Ø7,6 620..670 · burun dolu PC 670..680 · dudak 680..695
#   AĞIZ 5 × 4,5 borunun altında (z −80..−30) · menteşe ön kenarda (z −30) · kapak 5,1×5×0,3 PC + burulma yayı
#   kol x +30, menteşeden pime 32 mm (paftada "kol 1,8" yazıyor — bkz. AÇIK NOT) · raf pimi Ø8 yalnız TOPPING katında
import sys, os, math, time
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "3_TOPPING"); ALT = os.path.join(ROOT, "alt_montaj")
W, PU, PUB, YB = 700.0, 40.0, 20.0, 158.0     # plint ustu 158 -> hucre ic tabani 200,5 (v25: sogutma z 0-20)
ZI = ZK + T_DIS + PUB + T_IC                      # iç arka sac önü −797,5

# ---- kap kesit sabitleri (mm, yerel: kap merkezi x=0, raf üstü y=0) ----
YT = 67.0            # yalak / helezon / boru merkezi (taban plakasi 0,4 ustunde)
YD = 169.0           # daire duvar + tarak göbeği merkezi
R_YI, R_YD = 38.0, 43.0      # yalak iç / dış
R_DI, R_DD = 65.0, 70.0      # daire iç / dış
Y_TOP = 264.0        # kap ust kenari (kizak 20 + plaka 4 + govde 240)
ZB, ZF = -700.0, -20.0       # kap arka / ön dış yüz
Z_HAZ, Z_BORU0, Z_BORU1 = -80.0, -80.0, -30.0    # hazne sonu = boru başı ; boru sonu
# ---- istasyon yerleşimi (v25 · dikey: 3 × (27 kap + 14 robot boşluğu) + ALT 74) ----
#   kat 1 kap altı 170 · kat 2 129 · kat 3 88  → tepsi düzlemleri 158 / 117 / 76 (kap altından 12 cm aşağı)
# --- v30 (9 Eyl 2026): kaset odalari CONTALI KAPALI. Kaset govdesi 240 (taban plakasi + ust kapak silindi).
#     net aciklik 249 = 240 + 9 pay · contali kapak 279 = 249 + 2x15 bindirme · fuga 3 · robot agzi 121 (ACIK)
#     5 kapak + 4 fuga + 3 agiz = 1770 = bant boslugu (198..1968), pay 0.
KAPAK_H, AGIZ_H, FUGA_B, BIND_B = 279.0, 117.0, 3.0, 15.0
CZ0, CZ1, FRZ0, FRZ1 = -15.0, 0.0, -16.0, -15.0   # STORE v3 ile BIREBIR: conta bolgesi ve on cerceve saci   # taban 210 (hucre ic tabani 200,5 + L raf)
LAYOUT = [("kat1", 1683, [(270, "kasar_A"), (430, "sucuk")]),
          ("kat2", 1284, [(270, "kasar_B")]),                       # sag poz. BOS (v25) - 3. kasar secenegi Kemal karari
          ("kat3",  885, [(270, "kiyma"),   (430, "kusbasi")]),
          ("alt1",  486, [(125, "kasar_yedek_1"), (275, "kasar_yedek_2"), (425, "kasar_yedek_3"), (575, "kasar_yedek_4")]),
          ("alt2",  204, [(125, "sucuk_yedek"), (275, "park_bos_kap"), (425, "cozulme_kiyma"), (575, "cozulme_kusbasi")])]
RAF_X = {"kat": (270, 430), "alt": (125, 275, 425, 575)}   # ALT: 4 x 140 + 3 x 10 fuga = 590, kenar payi 12,5
# KAPAK = kaset odasinin CONTALI kapisi (5 bandin hepsi 279 -> TEK FORM, bant basina 2 kanat)
KLAPE = (("kat1", 1689, 1968), ("kat2", 1290, 1569), ("kat3", 891, 1170), ("alt1", 492, 771), ("alt2", 210, 489))
# robot agzi: KAPAKSIZ ACIK, sove arasi tam genislik (30..670 = 640)
ROBOT_AGZI = (("kat1", 1572, 1689), ("kat2", 1173, 1290), ("kat3", 774, 891))
KANAT_W = 634.0                       # bant basina TEK kapak: x 33..667 (dusey fuga da 3 mm)
KANAT_X = (33.0,)
TEPSI_Y = {"kat1": 1607, "kat2": 1208, "kat3": 809}     # robot pide tepsisi (Ø320) düzlemi — agzin ortasi

def _arc(cx, cy, r, a0, a1, n):
    return [(cx + r*math.cos(math.radians(a0 + (a1-a0)*i/n)), cy + r*math.sin(math.radians(a0 + (a1-a0)*i/n))) for i in range(n+1)]

def _tek(pts):
    o = []
    for q in pts:
        if not o or abs(q[0]-o[-1][0]) > 1e-6 or abs(q[1]-o[-1][1]) > 1e-6: o.append(q)
    if abs(o[0][0]-o[-1][0]) < 1e-6 and abs(o[0][1]-o[-1][1]) < 1e-6: o.pop()
    return o

def _kesit(r_yalak, r_daire, y_ust):
    """kap ön kesiti: yalak yayı → boğaz → daire yayı → dik duvar → üst (kapalı poligon)"""
    yj = YD - math.sqrt(r_daire**2 - r_yalak**2)                 # boğaz–daire birleşimi
    aj = math.degrees(math.atan2(yj - YD, -r_yalak)) % 360.0      # daire yayı başlangıç açısı (sol)
    p  = _arc(0, YT, r_yalak, 270, 180, 18)                       # (0, YT−r) → (−r, YT)
    p += [(-r_yalak, yj)]
    p += _arc(0, YD, r_daire, aj, 180, 12)                        # → (−r_daire, YD)
    p += [(-r_daire, y_ust), (r_daire, y_ust)]
    p += _arc(0, YD, r_daire, 0, -(aj - 180), 12)                 # (r_daire, YD) → (r_yalak, yj)
    p += [(r_yalak, YT)]
    p += _arc(0, YT, r_yalak, 0, -90, 18)
    return _tek(p)

# =========================== 1 · KAP (v26 + v27) ===========================
def kap():
    kok = os.path.join(ALT, "KAP_14x68x24"); st = Station(kok, "KAP_14x68x24"); p = "KAP_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))

    dis, ic = _kesit(R_YD, R_DD, Y_TOP), _kesit(R_YI, R_DI, Y_TOP + 30)
    st.part(p+"govde_PC_5mm", [
        (FR, 'poly', dis, ZB, ZF, False),                          # tek kalıp dış kabuk
        (FR, 'poly', ic,  ZB+5, Z_HAZ, True),                      # hazne boşluğu (arka duvar 5 kalır)
        (FR, 'circ', (0, YT, R_YI), Z_BORU0, Z_BORU1, True),       # KAPALI BORU Ø7,6 · 5 cm
        (FR, 'rect', (-22.5, 22.5, 15, 35), Z_BORU0, Z_BORU1, True),# AĞIZ 5 × 4,5 (boru tabanini deler)
        (FR, 'circ', (0, YT, 12), ZB-5, ZB+10, True),              # helezon keçe yuvası Ø24
        (FR, 'circ', (0, YD, 7), ZB-5, ZB+10, True),               # tarak keçe yuvası Ø14
        (FR, 'circ', (0, YD, 16), Z_HAZ, -55.0, True)])            # tarak ön yatağı (burun içinde)
    st.box(p+"taban_plakasi_0.4", -65, 65, 20, 24, ZB, ZF, [(-22.5, 22.5, 19, 25, Z_BORU0, Z_BORU1)])
    st.box(p+"kizak_sol_3x2", -65, -35, 0, 20, ZB, ZF, [(-60, -40, 3, 17, ZB+20, ZF)])   # çatal cebi 2,0×1,4
    st.box(p+"kizak_sag_3x2",  35,  65, 0, 20, ZB, ZF, [( 40,  60, 3, 17, ZB+20, ZF)])
    st.box(p+"on_cekme_dudagi_1.5x3", -70, 70, 234, 264, ZF, ZF+15)
    st.prism_z(p+"ust_kapak_PC_gecmeli",                                                  # geçmeli, ağza gömme
               [(-65, 264), (65, 264), (65, 260), (62, 260), (62, 250), (58, 250), (58, 260),
                (-58, 260), (-58, 250), (-62, 250), (-62, 260), (-65, 260)], ZB+5, Z_HAZ)
    # --- ağız kapağı: menteşe ön kenarda, burulma yayı kapalı tutar, kol raf pimine dayanır ---
    st.box(p+"agiz_kapagi_PC_5.1x5x0.3", -25.5, 25.5, 15.5, 18.5, Z_BORU0, -32.0)   # kapali: plakanin altinda, agzi kapatir
    st.part(p+"kapak_mentese_mili_D4",  [(RT, 'circ', (30.0, 17.0, 2.0), -34.0, 32.0, False)])
    st.part(p+"kapak_burulma_yayi_D6",  [(RT, 'circ', (30.0, 17.0, 3.0), -33.0, -27.0, False),
                                         (RT, 'circ', (30.0, 17.0, 2.2), -33.0, -27.0, True)])
    st.box(p+"kapak_kolu_1.8", 28, 32, 0, 17, -32.0, -28.0)          # 2 cm bosluga sarkar; rampaya biner (alt duzlemi asmaz)
    # --- helezon (POM) Ø70 · hatve 50 · boy 600 · son hatve borunun içinde ---
    ops = [(FR, 'circ', (0, YT, 10), ZB-20, -40.0, False)]                                 # mil Ø20
    ops += [(FR, 'circ', (0, YT, 35), -640.0 + k*50, -634.0 + k*50, False) for k in range(12)]   # 12 hatve × 5
    st.part(p+"helezon_POM_D70_hatve50", ops)
    st.part(p+"helezon_topuz_D50_tirtilli", [(FR, 'circ', (0, YT, 25), ZB-20, ZB, False),
                                             (FR, 'circ', (0, YT, 10), ZB-25, ZB+5, True)])   # 2 cm dısarı, mil gecisli
    # --- tarak (kafes, 304): göbek Ø30 + omurga 6 + 4 çubuk Ø6 (r 57/43/29/14) ---
    tops = [(FR, 'circ', (0, YD, 15), ZB+10, -60.0, False),                                 # göbek Ø30 · boy 630
            (FR, 'circ', (0, YD, 5),  ZB-10, ZB+10, False),                                 # arka mil Ø10
            (FR, 'rect', (-4, 4, YD-4, YD+4), ZB-20, ZB-10, False),                         # kare uç kavrama
            (FR, 'rect', (-3, 3, YD-57, YD), ZB+10, -60.0, False)]                          # omurga 6
    tops += [(FR, 'circ', (0, YD-r, 3), ZB+8, -82.0, False) for r in (57, 43, 29, 14)]
    st.part(p+"tarak_304_4cubuk", tops)
    # --- sızdırmazlık: gıda tipi dudak keçe ×2 ---
    st.part(p+"kece_helezon_D24", [(FR, 'circ', (0, YT, 12), ZB, ZB+5, False), (FR, 'circ', (0, YT, 10), ZB, ZB+5, True)])
    st.part(p+"kece_tarak_D14",   [(FR, 'circ', (0, YD, 7),  ZB, ZB+5, False), (FR, 'circ', (0, YD, 5),  ZB, ZB+5, True)])
    st.assemble("KAP_14x68x24"); print("  KAP bbox (mm):", ["%.1f" % (v/M) for v in st.bb])

# =========================== 2 · KABİN ALT MONTAJLARI ===========================
def kap_detay():
    """KAP v2 — URETIME HAZIR DETAY (9 Eyl 2026) — 29 farkli parca / 36 ornek.
       ANA KARAR: govde TEK ENJEKSIYON DEGIL. Kesit 615 mm boyunca sabit oldugu icin
       EKSTRUZYON profil + enjeksiyon BURUN + ARKA KAPAK olarak uce bolundu (kalip maliyeti).
       TAHRIK ARAYUZU: kaset tarafi ERKEK kare 12x12 cikinti (cep yok -> yikanir),
       kabin tarafi DISI yayli kare yuva (bkz. soket_motor_detay)."""
    kok = os.path.join(ALT, "KAP_DETAY"); st = Station(kok, "KAP_DETAY"); p = "KAPD_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    dis, ic = _kesit(R_YD, R_DD, Y_TOP), _kesit(R_YI, R_DI, Y_TOP + 30)
    ZP0, ZP1 = ZB + 5, Z_HAZ                                   # ekstruzyon profil -695..-80 (615)
    # ---------------- A - GOVDE (6)
    st.part(p+"govde_profil_PC_5mm",  [(FR,'poly',dis, ZP0, ZP1, False),
                                       (FR,'poly',ic,  ZP0-1, ZP1+1, True)])
    # UC KAPAKLARI KARE (9 Eyl 2026, Kemal): dis hat dikdortgen, alt kenari DUZ -> iki uc kapak ayak
    # gorevi gorur, kaset dogrudan duz rafa oturur. Ici (yalak/daire caplari) aynen korunur.
    kare = [(-70.0, 24.0), (70.0, 24.0), (70.0, Y_TOP), (-70.0, Y_TOP)]
    st.part(p+"arka_kapak_PC_5mm",    [(FR,'poly',kare, ZB, ZP0, False),
                                       (FR,'circ',(0,YT,12), ZB-1, ZP0+1, True),
                                       (FR,'circ',(0,YD, 9), ZB-1, ZP0+1, True)])
    # burun: DOLU DEGIL. Ic profil oyulur -> yanlarda 5, ustte 4, onde 4 mm esit cidar (enjeksiyon kurali)
    ic_burun = _kesit(R_YI, R_DI, 260.0)
    st.part(p+"burun_PC_enjeksiyon",  [(FR,'poly',kare, ZP1, ZF, False),
                                       (FR,'poly',ic_burun, ZP1-1, -24.0, True),      # ici bosaltildi
                                       (FR,'circ',(0,YD,66), ZP1, -72.0, False),      # tarak on yatak PERDESI
                                       (FR,'rect',(-22.5,22.5,15,35), ZP1-1, Z_BORU1, True),   # AGIZ 45 x 48
                                       (FR,'circ',(0,YD,16), ZP1-1, -71.0, True)])    # perdedeki yatak yuvasi Ø32
    # UST KAPAK ve CONTASI SILINDI (9 Eyl 2026, Kemal): kaset odasi zaten contali kapali ve +3 C,
    # kasetin ayrica kapagi gerekmiyor. Havalandirma filtresi de kapakla birlikte kalkti.
    # ---------------- B - AGIZ (5)
    st.box(p+"agiz_kapagi_PC_51x3", -22.0, 22.0, 24.0, 27.0, Z_BORU0, -32.0)   # agiz acikliginin icinde
    # AGIZ CONTASI ayri parca DEGIL: kapagin uzerine 2K TPE dudak olarak enjekte edilir (kasetin
    # govde tabaninin altina sarkan ayri bir cerceve, oda tabanina/PU dolgusuna giriyordu).
    st.part(p+"kapak_mentese_mili_D4", [(RT,'circ',(30.0,25.5,2.0), -34.0, 32.0, False)])
    st.part(p+"kapak_burulma_yayi_D6", [(RT,'circ',(30.0,25.5,3.0), -33.0, -27.0, False),
                                        (RT,'circ',(30.0,25.5,2.2), -33.0, -27.0, True)])
    # KAPAK KOLU SILINDI (9 Eyl 2026): pimli raf kalkti. Agiz kapagi helezonun ittigi urun basinciyla
    # acilir, burulma yayi kapatir — ayrica mekanik kol/pim gerekmiyor.
    # ---------------- C - HELEZON GRUBU (6)
    # GERCEK SARMAL: 11 tur x hatve 50 = 550 boy, kanat 5 mm, Ø70 dis / Ø22 gobek / Ø20 mil deligi.
    # Her tur 15 sektore bolunur (24 derece, dz 3,33); kanat 5 mm oldugu icin sektorler ust uste binip
    # kesintisiz helis yuzeyi olusturur. (Eski model 12 DUZ DISK ti - malzeme tasimazdi.)
    HAT, TUR, ADIM, KANAT = 50.0, 11, 15, 5.0
    ops = [(FR,'circ',(0,YT,11), -645.0, -85.0, False)]                       # gobek Ø22
    for k in range(TUR*ADIM):
        a0 = 360.0*k/ADIM; a1 = a0 + 360.0/ADIM; am = (a0+a1)/2.0
        zk = -640.0 + HAT*k/ADIM
        pts  = [(35.0*math.cos(math.radians(a)), YT + 35.0*math.sin(math.radians(a))) for a in (a0, am, a1)]
        pts += [(10.5*math.cos(math.radians(a)), YT + 10.5*math.sin(math.radians(a))) for a in (a1, am, a0)]
        ops.append((FR, 'poly', pts, zk, zk + KANAT, False))
    ops.append((FR,'circ',(0,YT,10), -646.0, -84.0, True))                    # Ø20 mil gecisi
    st.part(p+"helezon_POM_D70_hatve50", ops)
    st.part(p+"helezon_mili_304_D20",   [(FR,'circ',(0,YT,10), ZB, -45.0, False)])
    st.part(p+"helezon_arka_yatak_POM", [(FR,'circ',(0,YT,17), -692.0, -676.0, False),
                                         (FR,'circ',(0,YT,10), -693.0, -675.0, True)])
    st.part(p+"helezon_on_yatak_POM",   [(FR,'circ',(0,YT,17), -62.0, -46.0, False),
                                         (FR,'circ',(0,YT,10), -63.0, -45.0, True)])
    st.box(p+"helezon_kare_ucu_12", -6, 6, YT-6, YT+6, -715.0, ZB)      # ERKEK cikinti 15
    st.part(p+"kece_helezon_D24", [(FR,'circ',(0,YT,12), ZB, ZP0, False),
                                   (FR,'circ',(0,YT,10), ZB-1, ZP0+1, True)])
    # ---------------- D - TARAK GRUBU (6)
    st.part(p+"tarak_gobek_304_D30", [(FR,'circ',(0,YD,15), -685.0, -60.0, False)])
    st.part(p+"tarak_cubugu_D6",     [(FR,'circ',(0,YD-57,3), -683.0, -82.0, False)])
    st.part(p+"tarak_omurgasi_6",    [(FR,'rect',(-3,3,YD-57,YD-15), -685.0, -60.0, False)])
    st.part(p+"tarak_mili_304_D10",  [(FR,'circ',(0,YD,5), ZB, -683.0, False)])
    st.box(p+"tarak_kare_ucu_12", -6, 6, YD-6, YD+6, -715.0, ZB)        # ERKEK cikinti 15
    st.part(p+"kece_tarak_D18", [(FR,'circ',(0,YD,9), ZB, ZP0, False),
                                 (FR,'circ',(0,YD,5), ZB-1, ZP0+1, True)])
    # ---------------- E - TASIMA / ARAYUZ (5)
    # KIZAK ve CATAL CEBI KALDIRILDI (9 Eyl 2026, Kemal): robot tutmaci ayrica tasarlanacak.
    # Kaset artik taban plakasi (y 20..24) uzerinden L raf uzerinde kayiyor. Yukseklik 264 -> 244.
    st.box(p+"on_cekme_dudagi_1.5x3", -70, 70, 234, 264, ZF, ZF+15)
    # TABAN PLAKASI SILINDI (Kemal): govde profilinin kendi 5 mm cidari zaten taban. Kaset 244 -> 240.
    # ---------------- F - TANIMA (1)
    st.box(p+"rfid_etiketi_25x40", -20, 20, YD+30, YD+55, ZB-2.0, ZB)
    # ---------------- cok ornekli parcalar
    for dy in (14.0, 28.0, 43.0):
        st.add_instance(os.path.join(st.pdir, p+"tarak_cubugu_D6.SLDPRT"), offset_mm=(0, dy, 0))
    st.assemble("KAP_DETAY"); print("  KAP_DETAY bbox (mm):", ["%.1f" % (v/M) for v in st.bb])


def soket_motor_detay():
    """KASET ARKA TAHRIK ARAYUZU - DETAY.
       KASET = ERKEK kare 12x12 cikinti  |  KABIN = DISI yayli kare yuva (8 mm strok).
       Arada arka kapak saci var (2 mm, z -724..-722, 34x34 delik) ama SIZDIRMAZLIK ORADA DEGIL:
       plenum da ayni hucrenin soguk havasi. Gercek bariyer motorun IP65 kutusunun flansindaki O14 mil kecesi.
       Kavrama boyu 17 mm; yay tam basiliyken bile 9 mm kavramada kalir."""
    st = Station(os.path.join(ALT, "SOKET_MOTOR_DETAY"), "SOKET_MOTOR_DETAY"); p = "SMD_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    ORTAK = ("yayli_kare_soket_D30", "baski_yayi_D24", "cikis_mili_kare12", "mil_kecesi_D14",
             "kutu_flansi_90x90x6", "motor_kutusu_IP65_70x70", "montaj_braketi_3mm")
    st.part(p+"yayli_kare_soket_D30", [(FR,'circ',(0,YT,15), -725.0, -701.0, False),
                                       (FR,'rect',(-6.15,6.15,YT-6.15,YT+6.15), -726.0, -700.0, True)])
    st.part(p+"baski_yayi_D24",  [(FR,'circ',(0,YT,12), -741.0, -725.0, False),      # serbest 16, strok 6
                                  (FR,'circ',(0,YT, 9), -742.0, -724.0, True)])
    st.part(p+"cikis_mili_kare12", [(FR,'circ',(0,YT,7), -749.0, -739.0, False),
                                    (FR,'rect',(-6,6,YT-6,YT+6), -741.0, -717.0, False)])
    st.part(p+"mil_kecesi_D14", [(FR,'circ',(0,YT,12), -747.0, -741.0, False),
                                 (FR,'circ',(0,YT, 7), -748.0, -740.0, True)])
    st.box(p+"kutu_flansi_90x90x6", -45, 45, YT-45, YT+45, -747.0, -741.0, [(-13,13,YT-13,YT+13,-748.0,-740.0)])
    st.box(p+"motor_kutusu_IP65_70x70", -35, 35, YT-35, YT+35, -795.0, -747.0)
    st.box(p+"montaj_braketi_3mm", -45, 45, YT-45, YT-42, -797.0, -741.0)
    st.box(p+"step_motor_NEMA17_dozaj", -21, 21, YT-21, YT+21, -789.0, -749.0)
    st.box(p+"reduktorlu_dc_motor_tarak_10W", -21, 21, YD-21, YD+21, -789.0, -749.0)
    for nm in ORTAK:
        st.add_instance(os.path.join(st.pdir, p+nm+".SLDPRT"), offset_mm=(0.0, YD-YT, 0.0))
    st.assemble("SOKET_MOTOR_DETAY"); print("  SOKET_MOTOR_DETAY bbox:", ["%.1f" % (v/M) for v in st.bb])


def raf_cifti(pimli):
    """L raf çifti (±5): yatay kanat üstü y=0 (kap kızağı buraya oturur) + dik kanat 18 dışta.
       pimli → yalnız TOPPING katı: raflar arası çapraz çubuk + kapak açma pimi Ø8 (x +3)"""
    ad = "L_RAF_CIFTI_PIMLI" if pimli else "L_RAF_CIFTI"
    st = Station(os.path.join(ALT, ad), ad)
    p = "LRAFP_" if pimli else "LRAF_"     # ONEMLI: iki grubun parca adlari FARKLI olmali,
    #                                        yoksa SolidWorks ayni isimli iki dosyayi acamaz -> "internal ID" uyarisi
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.prism_z(p+"sol_L_2mm", [(-67, 18), (-67, -2), (-37, -2), (-37, 0), (-65, 0), (-65, 18)], -722.0, ZF)
    st.prism_z(p+"sag_L_2mm", [( 67, 18), ( 67, -2), ( 37, -2), ( 37, 0), ( 65, 0), ( 65, 18)], -722.0, ZF)
    if pimli:
        st.box(p+"capraz_cubuk_8x8", -67, 67, -10, -2, -25.0, -10.0)
        # kapak acma RAMPASI: kap son 1,5 cm girerken kolu 12 mm kaldirir (~73 deg), duz tepe acik tutar
        st.part(p+"kapak_acma_rampasi", [(RT, 'poly', [(0, 0), (15, 12), (25, 12), (25, -2), (0, -2)], 27.0, 33.0, False)])
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])

def tepsi_grubu():
    """robot pide tepsisi Ø320 + uzerinde pide — kat basina 14 cm'lik bosluga giriyor (referans/gosterim)"""
    st = Station(os.path.join(ALT, "TEPSI_PIDE_D320"), "TEPSI_PIDE_D320")
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.cyl_y("TP_tepsi_D320_alu_2mm", 0, -55, 160, 0, 2)
    st.cyl_y("TP_pide_D300_h18", 0, -55, 150, 2, 20)
    st.assemble("TEPSI_PIDE_D320"); print("  TEPSI bbox:", ["%.1f" % (v/M) for v in st.bb])


def kapak_kaset():
    """kaset odasinin CONTALI kapagi — TEK FORM, 5 ornek (bant basina TEK kanat).
       STORE ile ayni conta standardi: manyetik profil 21 genis x 18,5 yuksek, bindirme 15, fuga 3.
       Yan mentese (gizli, kanadin mentese kenarinda) — kaset one cikarken onunde hicbir sey kalmiyor.
       yerel: x 0..640 · y 0..279 · sandvic z 0..40 (1,0 + 37,5 + 1,5) · conta z -15..0 · alin saci z -16..-15
       SOGUTMALI ISTASYON CEPHE STANDARDI — STORE v3 ile birebir ayni."""
    ad = "KAPAK_KASET"; st = Station(os.path.join(ALT, ad), ad); p = "KPK_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    W_, H_ = 634.0, 279.0
    st.box(p+"on_ic_sac_1.0",  0, W_, 0, H_, 0.0, 1.0)                      # STORE v3 ile BIREBIR AYNI
    st.box(p+"on_pu_37.5",     1.5, W_-1.5, 1.5, H_-1.5, 1.0, 38.5)         # kopuk tamamen sacin icinde
    # dis sac: DORT KENARDA da 90 derece geriye bukulu kabuk -> hicbir kenarda ciplak PU kesiti gorunmez
    st.prism_y(p+"on_dis_sac_1.5",
               [(0.0, 40.0), (0.0, 0.0), (1.5, 0.0), (1.5, 38.5),
                (W_-1.5, 38.5), (W_-1.5, 0.0), (W_, 0.0), (W_, 40.0)], 0.0, H_)
    st.box(p+"on_dis_sac_alt_donus", 1.5, W_-1.5, 0.0, 1.5, 0.0, 38.5)
    st.box(p+"on_dis_sac_ust_donus", 1.5, W_-1.5, H_-1.5, H_, 0.0, 38.5)
    st.box(p+"conta_manyetik_21x18.5", 0, W_, 0, H_, CZ0, CZ1, [(15.0, W_-15.0, 15.0, H_-15.0, CZ0-1, CZ1+1)])
    for i, yy in enumerate((45.0, 194.0), 1):              # gizli mentese, mentese kenarinda (22 genis)
        st.box(p+"gizli_mentese_%d" % i, 0.0, 22.0, yy, yy+40.0, 8.0, 28.0)
    st.box(p+"bas_ac_mandali", W_-70, W_-30, H_/2-10, H_/2+10, -6.0, 0.0)    # kulp YOK
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


def boru_motor():
    """klape tahrigi — STANDART TUBULER (BORU) MOTOR: panjur/tente ailesi Ø35, 24 V, 6-10 Nm,
       mentese borusunun ICINE girer, ayrica yer kaplamaz. Uc siniri motorun kendi icinde (ayrica sensor yok).
       Gerekli moment: klape 640x270x1,5 sac = 2,0 kg, agirlik merkezi 135 mm -> 2,65 Nm.
       yerel: eksen y=0 z=0, x=0 borunun sol ucu"""
    st = Station(os.path.join(ARA, "_ortak", "BORU_MOTOR_D35"), "BORU_MOTOR_D35"); p = "BM_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.part(p+"yatak_pimi_D12",      [(RT, 'circ', (0.0, 0.0,  6.0),   0.0,  40.0, False)])
    st.part(p+"motor_govde_D32x450", [(RT, 'circ', (0.0, 0.0, 16.0),  40.0, 490.0, False)])
    st.part(p+"reduktor_taci_D31",   [(RT, 'circ', (0.0, 0.0, 15.5), 490.0, 530.0, False)])
    st.box(p+"kablo_D6", 25.0, 31.0, -60.0, -16.0, -3.0, 3.0)
    st.assemble("BORU_MOTOR_D35"); print("  BORU_MOTOR_D35 bbox:", ["%.1f" % (v/M) for v in st.bb])


def soket_motor():
    """arka duvar: kap başına 2 yaylı soket (helezon y 63 · tarak y 165) + 2 motor 57×57×57"""
    st = Station(os.path.join(ALT, "SOKET_MOTOR"), "SOKET_MOTOR"); p = "SM_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.cyl_z(p+"yayli_soket_helezon", 0, YT, 15, -740.0, -720.0)
    st.cyl_z(p+"yayli_soket_tarak",   0, YD, 15, -740.0, -720.0)
    st.box(p+"adim_motoru_helezon_dozaj", -28, 28, YT-28.5, YT+28.5, -797.0, -740.0)
    st.box(p+"reduktorlu_motor_tarak_10W", -28, 28, YD-28.5, YD+28.5, -797.0, -740.0)
    st.assemble("SOKET_MOTOR"); print("  SOKET_MOTOR bbox:", ["%.1f" % (v/M) for v in st.bb])

# =========================== 3 · KASA ===========================
def kasa(st):
    p = "TOPPING_"
    # SOGUTMA GRUBU plint bolgesinde (y 15..155) -> GOVDE tabani 158 de KALIYOR.
    # Ama PLINT YUZU hattaki digerleriyle ayni: 120. Aradaki 120..158 bandi alt cephe
    # seridinin arkasinda kaliyor ve kondenser fanina hava girisi oluyor.
    shell(st, p, W, "plint", y0=YB, plint_y=Y0,
          izgara=[(80+i*40, 100+i*40, 40, 110, 17, 21) for i in range(14)]); sove_L(st, p, W, Y0, H)
    xi0, xi1, zi = insulated_cell(st, p, W, YB+42.5, 1968.5-T_IC, PU, pu_back=PUB, y0=YB, top_pu=False, ze=FRZ0)
    st.cyl_z(p+"sog_kompresor_yatik_D100", 200, 85, 50, -600, -400)              # 1/12 HP Embraco EM, yatik
    st.box(p+"sog_kondenser", 300, 600, 25, 145, -300, -240); st.cyl_z(p+"sog_kondenser_fan_D140", 450, 85, 70, -240, -200)
    # plint izgarasi artik plint sacinin KENDI yarigi degil -> ayri panel iptal; yarik plint_U ya acildi
    # ---- ARKA PLENUM (standart soğuk dolap kurgusu): evaporatör + fanlar ALTTA, hava plenumdan yukarı,
    #      kaset bandlarındaki kesiklerden hücreye çıkar, ROBOT AĞIZLARININ HİZASINDA KESİK YOK.
    #      v28 e kadar soğutma sol yan kanaldaydı — kaldırıldı, hücrede 142 mm genişlik kazanıldı.
    st.box(p+"plenum_evaporator", xi0+30, xi1-30, 250, 450, -790, -732)          # 555 × 200 × 58 slim kanatlı
    st.cyl_z(p+"plenum_fan_D120", 250, 560, 60, -790, -750)                      # tek parca, 2 ornek (bkz. asm)
    st.box(p+"sag_kanal_kablo_kanali", xi1-45, xi1-5, 800, 1900, -700, -660)
    st.box(p+"arka_duvar_pano_plakasi", 470, 650, 1200, 1900, -778, -776)         # pano SAG ARKA kolona (ALT hava plenumu bosaldi)
    st.box(p+"arka_duvar_pano_plc", 490, 590, 1780, 1890, -776, -736)
    st.box(p+"arka_duvar_pano_guc_kaynagi", 490, 590, 1640, 1750, -776, -736)
    st.box(p+"arka_duvar_pano_surucu", 490, 540, 1250, 1400, -776, -736)         # tek parca, 6 ornek (bkz. asm)
    # arka kapak sacı: yalnız kat pozisyonlarında soket delikleri
    delik = []
    for zone, yr, kaps in LAYOUT:
        if zone.startswith("kat"):
            for xc, _ in kaps: delik += [(xc-17, xc+17, yr+YT-17, yr+YT+17, -726, -720), (xc-17, xc+17, yr+YD-17, yr+YD+17, -726, -720)]
    for nm, y0, y1 in KLAPE:                    # HAVA ÇIKIŞ KESİKLERİ — yalnız kaset bandlarında
        for yy in (y0+40.0, y1-60.0):
            for k in range(10): delik.append((xi0+20+k*60, xi0+60+k*60, yy, yy+10.0, -726.0, -720.0))
    for k in range(10):                         # DÖNÜŞ IZGARASI — en altta, plenuma geri
        delik.append((xi0+20+k*60, xi0+60+k*60, 215.0, 235.0, -726.0, -720.0))
    st.box(p+"arka_duvar_kapak_saci", xi0, xi1, YB+42.5, 1960, -724, -722, delik)
    # ---- CONTANIN BASTIGI ALIN SACI (bant cevresi) + KASET ODASI TABANI + DOKUM BACASI
    KAPX = dict((nm, [xc for xc, _ in kaps]) for nm, _, kaps in LAYOUT)
    YR   = dict((nm, yr) for nm, yr, _ in LAYOUT)
    for nm, y0, y1 in KLAPE:
        # oda tabani: kaset odasini alttaki ACIK robot agzindan ayirir
        # oda tabani: ust yuzu ALIN SACI ACIKLIGININ ALT KENARIYLA SIFIR (y0+18) -> esikte basamak yok.
        # Tum genislik; sagda yalniz 45 mm kablo yarigi.
        AGZ = dict((n, (a, b)) for n, a, b in ROBOT_AGZI)
        dok = KAPX[nm] if nm in AGZ else []          # dokum deligi yalniz dozaj yapan kat bandlarinda
        st.box(p+"oda_tabani_"+nm, xi0, xi1, y0+16.0, y0+18.0, -722.0, FRZ0,
               [(xc-32.0, xc+32.0, y0+15.0, y0+19.0, -89.0, -21.0) for xc in dok]
               + [(610.0, 655.0, y0+15.0, y0+19.0, -710.0, -650.0)])
        for xc in dok:            # dokum bacasi: kap agzindan asagi, robot agzina 40 mm girer (2 mm cidar)
            yb = AGZ[nm][1] - 40.0
            st.box(p+"dokum_bacasi_%s_%d" % (nm, int(xc)), xc-32.0, xc+32.0, yb, y0+18.0, -88.0, -22.0,
                   [(xc-30.0, xc+30.0, yb-1.0, y0+19.0, -86.0, -24.0)])
    # ---- ROBOT AGZI CERCEVESI: sove (z 0..40) ile yalitim (z -16) arasindaki 56 mm derin acik kanali
    #      kapatir ve acikligin dort kenarini da CEPHE DUZLEMINE (z 38,5..40) tasir. Disaridan tek,
    #      temiz dikdortgen aciklik gorunur; katman/basamak/oyuk kalmaz.
    #      Kapaklarin conta hatti (z -15..0) ve alin saci (z -16..-15) DEGISMEZ.
    for nm, y0, y1 in ROBOT_AGZI:
        # taban: on kenari cephe duzlemine kadar gelir (3 mm goruntu = fuga cizgisi)
        st.box(p+"agiz_tabani_"+nm, xi0, xi1, y0-3.0, y0, -722.0, ZF1,
               [(610.0, 655.0, y0-4.0, y0+1.0, -710.0, -650.0)])   # tum genislik, 45 mm kablo yarigi
        # tavan: odayi ustten kapatir; on tarafi kapagin alt kenarina birakilir (kapak z -15..40)
        st.box(p+"agiz_tavani_"+nm, xi0, xi1, y1-2.0, y1, -722.0, FRZ0,
               [(xc-32.0, xc+32.0, y1-3.0, y1+1.0, -89.0, -21.0) for xc in KAPX[nm]]
               + [(610.0, 655.0, y1-3.0, y1+1.0, -710.0, -650.0)])   # baca delikleri + 45 mm kablo yarigi
        # yan cerceveler: bukme sac 1,5 — on flans z 38,5..40 (x 30..42,5) + hucreye donen etek x 41..42,5
        st.prism_y(p+"agiz_cerceve_sol_"+nm,
                   [(30.0, ZF1), (xi0, ZF1), (xi0, FRZ0), (xi0-1.5, FRZ0), (xi0-1.5, ZF0), (30.0, ZF0)],
                   y0-3.0, y1)
        st.prism_y(p+"agiz_cerceve_sag_"+nm,
                   [(670.0, ZF1), (xi1, ZF1), (xi1, FRZ0), (xi1+1.5, FRZ0), (xi1+1.5, ZF0), (670.0, ZF0)],
                   y0-3.0, y1)
        # C kesitli cerceve cebinin ALT ve UST uclari: acik kalirsa acili bakista icine gorunur ve kir birikir
        for yn, ya, yb in (("alt", y0-3.0, y0-1.5), ("ust", y1-1.5, y1)):
            st.box(p+"agiz_cep_kapagi_sol_%s_%s" % (yn, nm), 30.0, xi0-1.5, ya, yb, FRZ0, ZF0)
            st.box(p+"agiz_cep_kapagi_sag_%s_%s" % (yn, nm), xi1+1.5, 670.0, ya, yb, FRZ0, ZF0)
    # ---- CONTANIN BASTIGI ALIN SACI — TUM CEPHE ICIN TEK PARCA (Kemal: "tek temiz bir parca olmali").
    #      8 aciklik: 5 kapak (contanin bastigi alin cevrede kalir) + 3 robot agzi. Fugalarin arkasi
    #      da bu tek sacla kapali oldugu icin hicbir yerden iceri gorunmuyor.
    st.box(p+"alin_saci_1.0", 30.0, 670.0, 159.5, 1968.5, FRZ0, FRZ1,
           [(45.0, 655.0, y0+18.0, y1-BIND_B, FRZ0-1, FRZ1+1) for _, y0, y1 in KLAPE]
           + [(xi0, xi1, y0-3.0, y1-2.0, FRZ0-1, FRZ1+1) for _, y0, y1 in ROBOT_AGZI])
    # ---- YALITIM DOLGUSU: robot agzi (ortam sicakligi) ile ustundeki kaset odasi (+3 C) arasindaki
    #      16 mm bosluk PU ile doldurulur — kapaklarin altinda bos cep kalmaz.
    KY0 = dict((n, a) for n, a, _ in KLAPE)
    for nm, y0, y1 in ROBOT_AGZI:
        st.box(p+"bant_pu_dolgusu_"+nm, xi0, xi1, y1, KY0[nm]+16.0, -722.0, FRZ0,
               [(xc-32.0, xc+32.0, y1-1.0, KY0[nm]+17.0, -89.0, -21.0) for xc in KAPX[nm]]
               + [(610.0, 655.0, y1-1.0, KY0[nm]+17.0, -710.0, -650.0)])
    st.box(p+"alt_pu_dolgusu", xi0, xi1, 200.5, 226.0, -722.0, FRZ0)
    # ---- ALT CEPHE SERIDI: plint ustu (y 159,5) ile alt2 kapaginin alt kenari (y 208) arasindaki
    #      50 mm'lik band tamamen ACIKTI — disaridan kabinin icine bakiliyordu. Bukme sac 1,5:
    #      on yuzu cephe duzleminde (z 38,5..40), alt kenari geriye bukulup plinte/pu_alt a kapaniyor.
    st.part(p+"alt_cephe_seridi_1.5", [(RT, 'poly',
             [(-ZF1, 208.0), (-ZF1, 123.0), (-FRZ1, 123.0), (-FRZ1, 124.5), (-ZF0, 124.5), (-ZF0, 208.0)],
             30.0, 670.0, False)])
    # ---- UST CEPHE SERIDI: kat1 kapaginin ust kenari (1968) ile dis_ust (1968,5) arasinda
    #      0,5 mm surekli yarik vardi — z +40 tan z -820 ye kadar kabinin icine acik. Altin aynasi.
    # kapak 1968 de bitiyor, dis_ust 1968,5 te basliyor: serit YALNIZ 1968..1970 bandinda
    st.part(p+"ust_cephe_seridi_1.5", [(RT, 'poly',
             [(-ZF1, 1968.0), (-ZF1, 1970.0), (-ZF0, 1970.0), (-ZF0, 1969.5), (0.0, 1969.5), (0.0, 1968.0)],
             30.0, 670.0, False)])   # hucre tabani ile alt2 oda tabani arasi

# =========================== 4 · MONTAJ ===========================
def asm():
    st = Station(ROOT, "TOPPING"); st.load_dir(); print("kasa parca yuklendi:", len(st.parts))
    st.add_instance(os.path.join(st.pdir, "TOPPING_plenum_fan_D120.SLDPRT"), offset_mm=(200, 0, 0))   # 2. plenum fani
    for dx, dy in ((55, 0), (110, 0), (0, 170), (55, 170), (110, 170)):
        st.add_instance(os.path.join(st.pdir, "TOPPING_arka_duvar_pano_surucu.SLDPRT"), offset_mm=(dx, dy, 0))
    for zone, yr, kaps in LAYOUT:
        pimli = zone.startswith("kat")
        # L RAF SILINDI (Kemal): kaset kare uc kapaklarinin duz alt kenariyla dogrudan oda tabanina oturuyor
        if pimli:
            for xc in RAF_X["kat"]:
                st.add_instance(os.path.join(ALT, "SOKET_MOTOR_DETAY", "SOKET_MOTOR_DETAY.SLDASM"), offset_mm=(xc, yr, 0))
        for xc, nm in kaps: st.add_instance(os.path.join(ALT, "KAP_DETAY", "KAP_DETAY.SLDASM"), offset_mm=(xc, yr, 0))
    for nm, yy in TEPSI_Y.items():                                               # robot tepsisi: her katin bosluguna 1 ornek
        st.add_instance(os.path.join(ALT, "TEPSI_PIDE_D320", "TEPSI_PIDE_D320.SLDASM"), offset_mm=(350, yy, -130))
    for nm, y0, y1 in KLAPE:                          # contali kapak: TEK FORM, bant basina 1 kanat
        for kx in KANAT_X:
            st.add_instance(os.path.join(ALT, "KAPAK_KASET", "KAPAK_KASET.SLDASM"), offset_mm=(kx, y0, 0))
    # kapak tahriki — STORE ile ORTAK: KLAPE_MOTOR_GRUBU. Kat bandlarinda menteşe tarafinda yer var
    # (kaset x 200..500). ALT bandlarda 4 kaset tum genisligi doldurdugu icin motor SIGMIYOR (bkz. not).
    ORT = lambda g: os.path.join(ARA, "_ortak", g, g + ".SLDASM")
    for nm, y0, y1 in KLAPE:
        if not nm.startswith("kat"): continue
        st.add_instance(ORT("KLAPE_MOTOR_GRUBU"), center_m=(0.116, (y0+140.0)*M, -0.080))   # PU yalitimindan 3 mm acik
        st.add_instance(ORT("SENSOR_REED_D12"),   center_m=(0.170, (y0+30.0)*M, -0.072))   # kapagin ic sacindan 2 mm geride
    O = lambda g: os.path.join(ARA, "_ortak", g, g + ".SLDASM")
    for ax, az in AYAK_YERI(W):                       # ORTAK: ayar ayagi (eski 4+4 yerel parca)
        st.add_instance(O("AYAK_AYAR_M12"), offset_mm=(ax, 0.0, az))
    st.assemble("TOPPING")

def kap_gorsel():
    """kap ici: govde + ust kapak gizli -> helezon, tarak, agiz kapagi, kol gorunur"""
    yol = os.path.join(ALT, "KAP_14x68x24", "KAP_14x68x24.SLDASM")
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(yol, 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(2); d.ClearSelection2(True); n = 0
    for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        if c.Name2.startswith(("KAP_govde", "KAP_ust_kapak", "KAP_kizak_sag")): c.Select4(True, NUL, False); n += 1
    mcall(d, "HideComponent"); d.ClearSelection2(True)
    png(d, os.path.join(ROOT, "KAP_ici_iso.png"), "*Isometric", 1400, 900)
    png(d, os.path.join(ROOT, "KAP_ici_yan.png"), "*Right", 1400, 900)
    print("  kap: gizlenen", n)
    sw.CloseDoc(d.GetTitle)


def gorsel():
    """klapeler gizli: robot/tepsi bosluklari ve kaplar gorunur"""
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "TOPPING.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(2); d.ClearSelection2(True); n = 0
    for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        if c.Name2.startswith(("KLAPE_H", "TOPPING_sove", "TOPPING_dis_yan_sag")): c.Select4(True, NUL, False); n += 1
    mcall(d, "HideComponent"); d.ClearSelection2(True)
    png(d, os.path.join(ROOT, "TOPPING_klapesiz_on.png"), "*Front", 1400, 900)
    png(d, os.path.join(ROOT, "TOPPING_klapesiz_iso.png"), "*Isometric", 1400, 900)
    print("  gizlenen bilesen:", n)
    sw.CloseDoc(d.GetTitle)


def mate():
    """klapeleri serbest birak + gercek mentese baglantisi (es merkezli + cakisik)"""
    NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "TOPPING.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(2)
    kls = []
    for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        if c.Name2.startswith("KLAPE_H"):
            bb = c.GetBox(False, False); kls.append((round(bb[4]/M), c))          # ust kenar y
    kls.sort()
    d.ClearSelection2(True)
    for _, c in kls: c.Select4(True, NUL, False)
    mcall(d, "UnfixComponent"); d.ClearSelection2(True)
    print("  serbest birakilan klape:", len(kls))
    for yust, c in kls:
        ad = c.Name2 + "@TOPPING"; ya = yust - 6.0
        d.ClearSelection2(True)
        o1 = d.Extension.SelectByRay(0.350, ya*M, 0.0, 0.0, 0.0, 1.0, 0.002, 2, False, 1, 0)   # sabit mil
        o2 = d.Extension.SelectByRay(0.043, ya*M, 0.0, 0.0, 0.0, 1.0, 0.002, 2, True, 1, 0)    # klape kulagi
        h = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        m1 = d.AddMate5(1, 0, False, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, False, False, 0, h)
        d.ClearSelection2(True)
        d.Extension.SelectByID2("Right Plane", "PLANE", 0.0, 0.0, 0.0, False, 1, NUL_, 0)
        d.Extension.SelectByID2("Right Plane@" + ad, "PLANE", 0.0, 0.0, 0.0, True, 1, NUL_, 0)
        h2 = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        m2 = d.AddMate5(0, 0, False, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, False, False, 0, h2)
        d.ClearSelection2(True)
        print("  %-16s (ust y=%d) secim=%s/%s  esmerkez=%s cakisik=%s" %
              (c.Name2, yust, o1, o2, "OK" if m1 else "HATA", "OK" if m2 else "HATA"))
    mcall(d, "EditRebuild3"); time.sleep(2)
    hr = [c.Name2 for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren if not c.IsFixed]
    print("  hareketli:", hr)
    e2 = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w2 = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    print("  kayit:", bool(d.Save3(1, e2, w2)))


if __name__ == "__main__":
    faz = sys.argv[1]; sw.CloseAllDocuments(True)
    if   faz == "kap":  kap_detay(); soket_motor_detay(); Station(ROOT, "x").exit_sw()
    elif faz == "alt":
        pass   # L raf kalkti
        kapak_kaset()
        tepsi_grubu()
        Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        st = Station(ROOT, "TOPPING")
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
        kasa(st); print("kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "parca":                       # ornek: python sw_topping3.py parca "oda_tabani|agiz_tabani"
        import re
        pat = re.compile(sys.argv[2]); st = Station(ROOT, "TOPPING"); n = [0]
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt") and pat.search(f): os.remove(os.path.join(st.pdir, f))
        orij = Station.part
        def sadece(self, fname, ops, _retry=2):
            if not pat.search(fname): return None
            n[0] += 1; return orij(self, fname, ops, _retry)
        Station.part = sadece
        Station.cyl_y = Station.cyl_z = lambda self, fname, *a: None
        kasa(st); print("yeniden uretilen parca:", n[0]); st.exit_sw()
    elif faz == "asm":  asm(); Station(ROOT, "x").exit_sw()
    elif faz == "mate":   mate(); Station(ROOT, "x").exit_sw()
    elif faz == "gorsel": gorsel(); kap_gorsel(); Station(ROOT, "x").exit_sw()
