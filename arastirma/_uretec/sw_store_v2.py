# -*- coding: utf-8 -*-
# AUTOKITCH — 1 · STORE v2 : CONTALI (üretime yönelik) — 8 Eyl 2026
# v1 (arastirma/1_STORE) DEĞİŞMEDİ; bu sürüm arastirma/1_STORE_v2 altında.
#
# SIZDIRMAZLIK KURGUSU (endüstriyel standart geçmeli manyetik conta 21 × 18,5 · kanal 6,3 · diş 8,3):
#   · kasa ön yüzünde ÇERÇEVE SACI z −16…−15 (açıklıklar kesilmiş) = contanın bastığı alın
#   · çekmece/klape ön yüzü açıklığa 15 mm BİNDİRİR, arkasında 15 mm genişliğinde manyetik conta halkası (z −15…0)
#   · komşu ön yüzler arası fuga 3 → açıklıklar arası alın 15 + 3 + 15 = 33 mm
#   · ön yüzler z 0…40 (1,0 iç sac + 37,5 PU + 1,5 dış sac), söve ve sabit panellerle aynı düzlemde
#   · kulp/girinti YOK (Kemal kuralı); çekmeceyi robot çeker, klapeyi motor açar
# YERLEŞİM SONUCU: 33 mm alın zorunluluğu açıklık sayısını 19 → 14'e indirdi (bkz. mesajdaki kapasite tablosu)
import sys, os, io, json, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE_v2"); CEKD = os.path.join(ROOT, "cekmece")
W, PU = 1400.0, 60.0
SOVE = 45.0                      # söve genişliği (v1: 66) — bindirmeli ön yüze yer açmak için daraltıldı
BIND, FUGA = 15.0, 3.0           # ön yüz bindirmesi · fuga  → alın = 15+3+15 = 33
CZ0, CZ1 = -15.0, 0.0            # conta bölgesi (sıkışmış yükseklik 15; profil 18,5)
FRZ0, FRZ1 = -16.0, -15.0        # çerçeve sacı 1,0
WO = 620.0                       # açıklık genişliği (her iki modül)
XL, XR = 63.0, 716.0             # sol / sağ modül açıklık sol kenarı
CELL0, CELL1 = 182.5, 1610.0     # yalıtımlı hücre alt/üst
# tip: açıklık yüksekliği
TIP = {"1L": 316.0, "icecek": 133.0, "taze": 108.0, "donmus": 160.0}
KLAPE_H = 284.0
# örnekler: (tip, x0, y0)
ORNEK = ([("1L", XL, 781.0)] + [("icecek", XL, y) for y in (1130.0, 1296.0, 1462.0)] +
         [("taze", XR, y) for y in (781.0, 922.0, 1063.0, 1204.0, 1345.0, 1486.0)] +
         [("donmus", XL, 198.0), ("donmus", XR, 198.0)])
KLAPE_ORNEK = [(XL, 391.0), (XR, 391.0)]
ACIKLIKLAR = [(x0, x0+WO, y0, y0+TIP[t]) for t, x0, y0 in ORNEK] + [(x0, x0+WO, y0, y0+KLAPE_H) for x0, y0 in KLAPE_ORNEK]

def on_yuz(st, p, h):
    """bindirmeli ön yüz + manyetik conta halkası — yerel: açıklık sol-alt köşesi (0,0), ön yüz z 0..40"""
    a, b = -BIND, WO+BIND; c, d = -BIND, h+BIND
    st.box(p+"on_ic_sac_1.0", a, b, c, d, 0.0, 1.0)
    st.box(p+"on_pu_37.5",    a, b, c, d, 1.0, 38.5)
    st.box(p+"on_dis_sac_1.5", a, b, c, d, 38.5, 40.0)
    st.box(p+"conta_manyetik_21x18.5", a, b, c, d, CZ0, CZ1, [(0.0, WO, 0.0, h, CZ0-1, CZ1+1)])   # 15 mm genişlik halka

ICERIK = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cekmece_icerik.json"), encoding="utf-8"))

def cekmece(tip):
    """çekmece alt montajı: bindirmeli contalı ön yüz + U kutu 1,0 + arka + iç ray + tepsi tabanı +
       kayış pabucu + reed mıknatısı + İÇERİK (yuva/tepsi + ürün) — kulp YOK"""
    h = TIP[tip]; st = Station(os.path.join(CEKD, "CEKMECE2_" + tip), "CEKMECE2_" + tip); p = "CEK2_%s_" % tip
    on_yuz(st, p, h)
    ka, kb, kc, kd = 16.0, WO-16.0, 8.0, h-10.0                      # kutu dış ölçüleri
    st.prism_z(p+"kutu_U_1.0", [(ka, kd), (ka, kc), (kb, kc), (kb, kd), (kb-1, kd), (kb-1, kc+1), (ka+1, kc+1), (ka+1, kd)], -700.0, 0.0)
    st.box(p+"kutu_arka_1.0", ka+1, kb-1, kc+1, kd, -700.0, -699.0)
    st.box(p+"tepsi_taban_saci_1.5", ka+1, kb-1, kc+1, kc+2.5, -698.0, -3.0)        # ürünlerin oturduğu delikli taban
    st.box(p+"ray_ic_profil_sol_45x12.7", 0.0, 12.7, kc+8, kc+53, -660.0, 0.0)
    st.box(p+"ray_ic_profil_sag_45x12.7", WO-12.7, WO, kc+8, kc+53, -660.0, 0.0)
    st.box(p+"kayis_pabucu_alt", 13.0, 21.0, kc-5.0, kc+1.0, -80.0, -40.0)         # kutu tabanı → alttaki kayış
    st.box(p+"kayis_pabucu_yan", 13.0, 17.0, 72.0, 80.0, -80.0, -40.0)              # kutu yanı → yandaki kayış (sıranın en alt çekmecesi)
    st.box(p+"miknatis_15x8x3", WO-16.0, WO-8.0, 72.0, 80.0, -32.0, -27.0)          # reed sensörünün mıknatısı (kutu dış yüzünde)
    for yol, c in ICERIK[tip]:                                                       # v1 yerleşimi birebir (x +1: açıklık 618→620)
        if os.path.exists(yol): st.add_instance(yol, center_m=[(c[0]+1)*M, c[1]*M, (c[2]+3)*M])
    st.assemble("CEKMECE2_" + tip); print("  CEKMECE2_%s: %d icerik | bbox:" % (tip, len(ICERIK[tip])), ["%.1f" % (v/M) for v in st.bb])

def klape():
    """kaset katı klapesi: contalı ön yüz + alt menteşe kulakları (mil kasada) — 2 örnek (sol + sağ modül)"""
    st = Station(os.path.join(CEKD, "KLAPE2_KASET"), "KLAPE2_KASET"); p = "KLP2_"
    on_yuz(st, p, KLAPE_H)
    # menteşe ekseni AÇIKLIĞIN İÇİNDE (y +12, z −4) — conta halkasının iç boşluğunda, contaya değmez.
    # ÜRETİMDE: telafili (4 kollu) klape menteşesi — kapak açılırken önce öne çıkıp contadan ayrılır.
    st.part(p+"mentese_kulagi", [(RT, 'circ', (4.0, 12.0, 6.0), 20.0, 36.0, False),
                                (RT, 'circ', (4.0, 12.0, 6.0), WO-36.0, WO-20.0, False),
                                (RT, 'circ', (4.0, 12.0, 4.2), 18.0, 38.0, True),
                                (RT, 'circ', (4.0, 12.0, 4.2), WO-38.0, WO-18.0, True)])
    st.assemble("KLAPE2_KASET"); print("  KLAPE2_KASET bbox:", ["%.1f" % (v/M) for v in st.bb])

def hucre_v2(st, p, ycell0, ycell1, pu, ytek):
    """yalitimli hucre — v1'den tek farki: HER SEY on cerceve sacinin ARKASINDA (z FRZ0) biter,
       boylece conta bolgesi (z -15..0) ve bindirmeli on yuz PU'ya girmez"""
    xi0, xi1 = T_DIS+pu+T_IC, W-T_DIS-pu-T_IC; zi = ZK+T_DIS+pu+T_IC; ZE = FRZ0
    st.box(p+"pu_yan_sol", T_DIS, T_DIS+pu, Y0+T_DIS, ytek, ZK+T_DIS, ZE)
    st.box(p+"pu_yan_sag", W-T_DIS-pu, W-T_DIS, Y0+T_DIS, ytek, ZK+T_DIS, ZE)
    st.box(p+"pu_arka", T_DIS+pu, W-T_DIS-pu, Y0+T_DIS, ytek, ZK+T_DIS, ZK+T_DIS+pu)
    st.box(p+"pu_alt", T_DIS+pu, W-T_DIS-pu, Y0+T_DIS, ycell0-T_IC, zi-T_IC, ZE)
    st.box(p+"ic_yan_sol", xi0-T_IC, xi0, ycell0-T_IC, ycell1+T_IC, zi-T_IC, ZE)
    st.box(p+"ic_yan_sag", xi1, xi1+T_IC, ycell0-T_IC, ycell1+T_IC, zi-T_IC, ZE)
    st.box(p+"ic_arka", xi0, xi1, ycell0-T_IC, ycell1+T_IC, zi-T_IC, zi)
    st.box(p+"ic_alt", xi0, xi1, ycell0-T_IC, ycell0, zi, ZE)
    st.box(p+"ic_tavan", xi0, xi1, ycell1, ycell1+T_IC, zi, ZE)
    st.box(p+"pu_tavan", T_DIS+pu, W-T_DIS-pu, ycell1+T_IC, ytek-T_IC, zi-T_IC, ZE)
    st.box(p+"teknik_taban", T_DIS+pu, W-T_DIS-pu, ytek-T_IC, ytek, zi-T_IC, ZE)
    return xi0, xi1, zi

def kasa(st):
    p = "S2_"
    shell(st, p, W, "feet")
    xi0, xi1, zi = hucre_v2(st, p, CELL0, CELL1, PU, 1670.0)
    for nm, a, b in (("sol", xi0, 683.0), ("sag", 716.0, xi1)):     # yatay ayirici, dikey bolmenin iki yaninda ayri
        st.box(p+"ayirici_sac_alt_"+nm, a, b, 690, 691, zi, FRZ0)
        st.box(p+"ayirici_pu_"+nm, a, b, 691, 765, zi, FRZ0)
        st.box(p+"ayirici_sac_ust_"+nm, a, b, 765, 766, zi, FRZ0)
    st.box(p+"orta_bolme_sac_sol", 683, 684, CELL0, CELL1, zi, FRZ0)                      # orta bölme 33 geniş (v1: 24)
    st.box(p+"orta_bolme_pu", 684, 715, CELL0, CELL1, zi, FRZ0)
    st.box(p+"orta_bolme_sac_sag", 715, 716, CELL0, CELL1, zi, FRZ0)
    # ---- ÖN ÇERÇEVE SACI 1,0 (contanın bastığı alın) — tek parça, 14 açıklık kesilmiş
    st.box(p+"on_cerceve_saci", SOVE, W-SOVE, CELL0, CELL1, FRZ0, FRZ1,
           [(a, b, c, d, FRZ0-1, FRZ1+1) for a, b, c, d in ACIKLIKLAR])
    # ---- SÖVE ve SABİT PANELLER: 40 mm sandviç (arkası açık kalmıyor), çerçeve düzleminden ön yüze kadar dolu
    def sandvic(ad, x0, x1, y0, y1, ic=True):
        if ic: st.box(p+ad+"_ic_sac_1.0", x0, x1, y0, y1, FRZ0, FRZ1)
        st.box(p+ad+"_pu_37.5",    x0, x1, y0, y1, FRZ1, ZF0)
        st.box(p+ad+"_dis_sac_1.5", x0, x1, y0, y1, ZF0, ZF1)
    sandvic("sove_sol", T_DIS, SOVE, Y0+T_DIS, H-T_DIS); sandvic("sove_sag", W-SOVE, W-T_DIS, Y0+T_DIS, H-T_DIS)
    st.box(p+"dis_yan_on_donus_sol", 0.0, T_DIS, Y0, H, 0.0, ZF1)          # dış kabuk ön dönüşü (köşe kapalı)
    st.box(p+"dis_yan_on_donus_sag", W-T_DIS, W, Y0, H, 0.0, ZF1)
    st.box(p+"dis_ust_on_donus", 0.0, W, H-T_DIS, H, 0.0, ZF1)
    sandvic("panel_bant_ust", SOVE, W-SOVE, CELL1, 1670.0)
    sandvic("panel_ayirici_on", SOVE, W-SOVE, 690.0, 766.0, ic=False)      # iç sacı ön çerçeve sacı zaten veriyor
    sandvic("panel_bant_alt", SOVE, W-SOVE, Y0+T_DIS, CELL0)
    # teknik bölme servis paneli: bükme 1,5 sac (kenarları kapalı, sökülebilir)
    st.prism_y(p+"panel_sogutma_bukme_1.5", [(SOVE, ZF1), (SOVE, 0), (SOVE+1.5, 0), (SOVE+1.5, ZF0),
                                             (W-SOVE-1.5, ZF0), (W-SOVE-1.5, 0), (W-SOVE, 0), (W-SOVE, ZF1)], 1670.0, H)
    st.box(p+"panel_sogutma_alt_donus", SOVE+1.5, W-SOVE-1.5, 1670.0, 1671.5, 0.0, ZF0)
    st.box(p+"panel_sogutma_ust_donus", SOVE+1.5, W-SOVE-1.5, H-1.5, H, 0.0, ZF0)
    # ---- ELEKTRİK PANOSU (teknik bölme, soğutma grubunun arkasında)
    st.box(p+"pano_montaj_plakasi", 300, 1100, 1700, 1940, -502, -500)
    st.box(p+"pano_plc_modbus", 320, 420, 1820, 1930, -500, -440)
    st.box(p+"pano_guc_kaynagi_24V_20A", 440, 560, 1820, 1930, -500, -430)
    for i in range(14):                                                     # 12 çekmece + 2 klape sürücüsü
        st.box(p+"pano_surucu_%02d" % (i+1), 320+ (i%7)*55, 365+(i%7)*55, 1700+(i//7)*55, 1750+(i//7)*55, -500, -460)
    st.box(p+"pano_klemens_rayi", 720, 1080, 1700, 1707.5, -500, -465)
    st.box(p+"pano_kablo_kanali", 720, 1080, 1730, 1770, -500, -460)
    cooling_unit(st, p+"sog1_", 80, 1680, -100); cooling_unit(st, p+"sog2_", 720, 1680, -100)
    # arka plenum (57,5 mm): evaporatör + fan üst üste; motor kolonu (x 65–238 / 718–891) serbest bırakıldı
    for i, (x0, x1, y0, y1, xf) in enumerate(((250, 680, 1400, 1500, 465), (900, 1180, 1400, 1500, 1040),
                                              (250, 680, 500, 600, 465), (900, 1180, 500, 600, 1040)), 1):
        st.box(p+"evaporator_%d" % i, x0, x1, y0, y1, -757, -737)
        st.cyl_z(p+"evap_fan_%d" % i, xf, (y0+y1)/2, 90, -737, -712)
    st.box(p+"dis_alt_on_donus", T_DIS, W-T_DIS, Y0, Y0+T_DIS, 0.0, ZF1)
    # klape menteşe mili (kasaya sabit) + raf + amortisör
    for i, (x0, y0) in enumerate(KLAPE_ORNEK, 1):
        st.part(p+"klape_mentese_mili_%d" % i, [(RT, 'circ', (4.0, y0+12.0, 4.0), x0+10, x0+WO-10, False)])
        st.box(p+"klape_raf_%d" % i, x0+4, x0+WO-4, y0+6, y0+7.5, zi, FRZ0)
        for j, xx in enumerate((x0+30, x0+WO-48), 1):
            st.box(p+"klape_gazli_amortisor_%d_%d" % (i, j), xx, xx+18, y0+40, y0+240, -60, -42)

def asm():
    st = Station(ROOT, "STORE_v2"); st.load_dir(); print("kasa parca yuklendi:", len(st.parts))
    for tip, x0, y0 in ORNEK:
        st.add_instance(os.path.join(CEKD, "CEKMECE2_" + tip, "CEKMECE2_" + tip + ".SLDASM"), offset_mm=(x0, y0, 0))
    for x0, y0 in KLAPE_ORNEK:
        st.add_instance(os.path.join(CEKD, "KLAPE2_KASET", "KLAPE2_KASET.SLDASM"), offset_mm=(x0, y0, 0))
    # ---- TAHRİK SİSTEMİ (v1'deki ortak gruplar): çekmece başına 2 dış ray + kayış + 24 V motor + kablo + reed sensör
    O = lambda g: os.path.join(ARA, "_ortak", g, g + ".SLDASM")
    # her 33 mm'lik alın boşluğuna BİR motor: çekmecenin ALTINDAKİ boşluğa; sıranın en altındaki için ÜSTTEKİ boşluğa (x kaydırmalı)
    ENALT = {}
    for tip, x0, y0 in ORNEK:
        k = (x0, y0 < 700); ENALT[k] = min(ENALT.get(k, 1e9), y0)
    for tip, x0, y0 in ORNEK:
        st.add_instance(O("RAY_DIS_PROFIL"), offset_mm=(x0+1, y0+16, 0))
        st.add_instance(O("RAY_DIS_PROFIL"), offset_mm=(x0+WO-15, y0+16, 0))
        # kayış kutunun ALTINDA; sıranın en alt çekmecesinde motor braketi hücre tabanına çarptığı için YANDA
        dy = 73.0 if y0 == ENALT[(x0, y0 < 700)] else 3.0
        st.add_instance(O("KAYIS_GT3_6mm"),  offset_mm=(x0+14, y0+dy, -40))
        st.add_instance(O("MOTOR_TAHRIK_GRUBU"), offset_mm=(x0+17, y0+dy+1.5, -727))
        st.add_instance(O("KABLO_24V_D5"),   offset_mm=(x0+180, y0+dy+1.5, -735))
        st.add_instance(O("SENSOR_REED_D12"), offset_mm=(x0+612, y0+80, -25))       # çekmecedeki mıknatısı görür
    for x0, y0 in KLAPE_ORNEK:                                   # klape motoru (v1 TOPPING ile aynı grup)
        st.add_instance(O("KLAPE_MOTOR_GRUBU"), offset_mm=(x0+60, y0+40, -160))
        st.add_instance(O("SENSOR_REED_D12"), offset_mm=(x0+8, y0+80, -25))
    st.assemble("STORE_v2")

if __name__ == "__main__":
    faz = sys.argv[1]; sw.CloseAllDocuments(True)
    if faz == "cekmece":
        for t in TIP: cekmece(t)
        klape(); Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        st = Station(ROOT, "STORE_v2")
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
        kasa(st); print("kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "asm":
        asm(); Station(ROOT, "x").exit_sw()
