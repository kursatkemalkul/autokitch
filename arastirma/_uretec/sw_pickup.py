# -*- coding: utf-8 -*-
# AUTOKITCH — 6 · PICKUP v1 (10 Eyl 2026) — QR / KOD ILE ACILAN TESLIM DOLABI
#
# AYRI UNITE: hatta bagli DEGIL. Dukkanin ON DUVARI ICINE gomulu; on yuzu sokaga (musteri),
# arka yuzu robot koridoruna bakar. Kendi montaji: 6_PICKUP_v1/PICKUP_v1.SLDASM
#
# KAYNAK: 6_PICKUP/teslim_dolabi_teknik_v2.svg  +  kod_unitesi_teknik_v1.svg (birebir)
#   TESLIM DOLABI  1240 x 1650 x 520 · 12 goz (2 sutun x 6 sira) · goz ici 560 x 360 x 160
#     yukseklik  : plint 150 + PANO 250 + 6 x 200 + ust 50 = 1650
#     genislik   : 20 + 600 + 600 + 20 = 1240
#     derinlik   : kapi 20 + PU 20 + ic 360 + klape 80 + cerceve 20 + pay 20 = 520
#     kapi 580 x 180 x 2 (304) — gizli yayli mentese x3 SOLDA, elektrikli kilit SAGDA,
#     kasa icine 10 mm bindirme kenari, TUTAMAK OYUK (cikinti yok — vandalizm),
#     soft-close amortisor 3 sn, PU 20 alt/ust/yan, ISITICI YOK (15 dk sicak kalir),
#     arka klape: UST mentese, ICERI acilir, yay + miknatis kilit (yalniz BEYIN acar),
#     IR sensor "kutu var", buhar deligi Ø8 x3 arka ust, cikarilabilir taban tepsisi,
#     LED serit kapi ustu, cam YOK, dis yuzde vida YOK (guvenlik torx iceriden).
#     Interlock: on kapi ile arka klape ASLA ayni anda acilmaz.
#   KOD UNITESI  200 x 340 x 80 · zeminden 1100..1440 · dolabin hemen SAGINDA
#     7" ekran · metal PIN pad 4x3 (IK09/IP65) · 2D QR okuyucu · kamera · LED serit
#     kontrolcu (RPi tipi) + PSU; kilit karti dolabin panosunda, bu kutuda kilit YOK
#
# Z KONVANSIYONU: musteri yuzu z = 40 (hat istasyonlariyla ayni on duzlem).
#   kapi 20..40 · bindirme saci 18..20 · PU/ic kabuk -360..18 · klape -362..-360
#   klape zonu -440..-360 · arka cerceve -460..-440 · pay -480..-460
#   (NOT: sw_lib._ext kesikte yonu ters cevirdigi icin bir kesigin z araligi z=0 i GECMEMELI.)
import sys, os
from sw_lib import *

ARA  = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "6_PICKUP_v1"); ORTAK = os.path.join(ARA, "_ortak")
P    = "PK_"
W, H = 1240.0, 1650.0
T2   = 2.0                                  # dis kasa 2 mm 304
GX   = (20.0, 620.0)                        # iki sutunun sol kenarlari (modul 600 genis)
SIRA, SY0, SH = 6, 400.0, 200.0             # 6 sira, ilk sira 400, adim 200
PLINT, PANO, UST = (0.0, 150.0), (150.0, 400.0), (1600.0, 1650.0)
ZF   = 40.0                                 # MUSTERI YUZU
ZB0, ZB1 = 18.0, 20.0                       # bindirme saci (kapi buna kapanir)
ZI0  = -360.0                               # goz ici arkasi
ZK1  = -360.0                               # arka klape duzlemi
DZ0  = -480.0                               # kasa arkasi
KX0, KX1, KY0, KY1, KZ0 = 1290.0, 1490.0, 1100.0, 1440.0, -40.0   # kod unitesi
MENT_Y = (25.0, 90.0, 155.0)                # gizli yayli mentese kotlari (modul yereli)


# =========================== 1 · ALT GRUP ===========================
def teslim_gozu():
    """TESLIM GOZU — TEK FORM, 12 ornek. Yerel: modul sol alt kose x=0 / y=0.
       Modul 600 x 200; goz ici 560 x 160 x 360. Moduller yan yana / ust uste TEGET."""
    ad = "TESLIM_GOZU"; st = Station(os.path.join(ORTAK, ad), ad); p = "TG_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    # ---- PU 20 alt/ust/yan (isitici YOK)
    st.box(p+"pu_sol",  0.0,   20.0,  0.0,   200.0, ZI0, ZB0)
    st.box(p+"pu_sag",  580.0, 600.0, 0.0,   200.0, ZI0, ZB0)
    st.box(p+"pu_alt",  20.0,  580.0, 0.0,   20.0,  ZI0, ZB0)
    st.box(p+"pu_ust",  20.0,  580.0, 180.0, 200.0, ZI0, ZB0)
    # ---- ic kabuk 1,0 paslanmaz (yikanabilir)
    st.box(p+"ic_yan_sol_1.0", 20.0,  21.0,  20.0,  180.0, ZI0, ZB0)
    st.box(p+"ic_yan_sag_1.0", 579.0, 580.0, 20.0,  180.0, ZI0, ZB0)
    st.box(p+"ic_taban_1.0",   21.0,  579.0, 20.0,  21.0,  ZI0, ZB0)
    st.box(p+"ic_tavan_1.0",   21.0,  579.0, 179.0, 180.0, ZI0, ZB0)
    st.box(p+"taban_tepsisi_1.0", 26.0, 574.0, 21.0, 23.0, ZI0+5.0, 10.0)    # cikarilabilir, yikanir
    # ---- ON KAPI 580 x 180 x 20 : 2 mm 304 + PU 16 + 2 mm; TUTAMAK OYUK (cikinti yok)
    st.box(p+"on_kapi_dis_2mm", 10.0, 590.0, 10.0, 190.0, ZF-2.0, ZF,
           [(535.0, 585.0, 80.0, 120.0, ZF-3.0, ZF+1.0)])
    st.box(p+"on_kapi_pu_16",   12.0, 588.0, 12.0, 188.0, 22.0, ZF-2.0,
           [(535.0, 585.0, 80.0, 120.0, 21.0, 35.0)]
           + [(6.0, 28.0, yy-1.0, yy+31.0, 21.0, 37.0) for yy in MENT_Y])    # mentese yuvalari
    st.box(p+"on_kapi_ic_2mm",  10.0, 590.0, 10.0, 190.0, 20.0, 22.0)
    st.box(p+"tutamak_oyugu_1.0", 535.0, 585.0, 80.0, 120.0, 33.0, 34.0)     # oyuk tabani
    for i, yy in enumerate(MENT_Y, 1):        # gizli yayli mentese SOLDA — disaridan sokulmez
        st.box(p+"gizli_yayli_mentese_%d" % i, 6.0, 28.0, yy, yy+30.0, 22.0, 34.0)
    st.box(p+"soft_close_amortisor", 30.0, 50.0, 22.0, 32.0, 2.0, 16.0)      # 3 sn, goz tabaninda
    # ---- KILIT: 12 V elektrikli dil, fail-secure (enerji kesilince KILITLI kalir), 5 kN
    st.box(p+"elektrikli_kilit_12V", 560.0, 578.0, 86.0, 114.0, 0.0, 16.0)
    st.box(p+"kilit_dili",           566.0, 588.0, 94.0, 106.0, 24.0, 32.0)
    st.box(p+"reed_sensoru_kapi",    545.0, 563.0, 160.0, 174.0, 2.0, 14.0)
    # ---- ARKA KLAPE: ust mentese, ICERI acilir, yay kapatir, miknatis kilit (yalniz BEYIN)
    st.box(p+"arka_klape_2mm", 20.0, 580.0, 20.0, 180.0, ZK1-2.0, ZK1,
           [(230.0+i*70.0, 238.0+i*70.0, 158.0, 166.0, ZK1-3.0, ZK1-1.0) for i in range(3)])  # buhar Ø8 x3
    st.box(p+"klape_mentese_mili_D6", 30.0, 570.0, 180.0, 186.0, ZK1-6.0, ZK1)   # klapenin USTUNDE
    for i, xx in enumerate((60.0, 520.0), 1):
        st.box(p+"klape_burulma_yayi_%d" % i, xx, xx+20.0, 176.0, 186.0, ZK1-8.0, ZK1-6.0)
    st.box(p+"klape_miknatis_kilit_12V", 275.0, 325.0, 22.0, 34.0, ZK1-14.0, ZK1-2.0)
    # ---- SENSOR + AYDINLATMA
    st.box(p+"ir_sensoru_kutu_var", 28.0, 48.0, 150.0, 170.0, -22.0, -2.0)
    st.box(p+"led_serit_kapi_ustu", 30.0, 570.0, 172.0, 178.0, -20.0, -14.0)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


# =========================== 2 · KASA ===========================
def _goz_yerleri():
    for i in range(SIRA):
        y0 = SY0 + i * SH
        for j, x0 in enumerate(GX):
            yield i, j, x0, y0


def kasa(st):
    # ---- DIS KASA 2 mm 304 (duvar acikligina gomulu, dis yuzde vida YOK — guvenlik torx iceriden)
    st.box(P+"dis_yan_sol_2mm", 0.0,  T2,   PLINT[1], H, DZ0, ZF)
    st.box(P+"dis_yan_sag_2mm", W-T2, W,    PLINT[1], H, DZ0, ZF)
    st.box(P+"dis_ust_2mm",     T2,   W-T2, H-T2,     H, DZ0, ZF)
    st.box(P+"dis_alt_2mm",     T2,   W-T2, PLINT[1], PLINT[1]+T2, DZ0, ZF)
    st.box(P+"dis_arka_2mm",    T2,   W-T2, PLINT[1]+T2, H-T2, DZ0, DZ0+T2)
    # 20 mm cidar: 2 dis + 16 PU + 2 ic
    st.box(P+"yan_pu_sol",     T2,     18.0,   PLINT[1]+T2, H-T2, DZ0+T2, ZB0)
    st.box(P+"yan_ic_2mm_sol", 18.0,   20.0,   PLINT[1]+T2, H-T2, DZ0+T2, ZB0)
    st.box(P+"yan_pu_sag",     W-18.0, W-T2,   PLINT[1]+T2, H-T2, DZ0+T2, ZB0)
    st.box(P+"yan_ic_2mm_sag", W-20.0, W-18.0, PLINT[1]+T2, H-T2, DZ0+T2, ZB0)
    st.box(P+"ust_pu",         20.0,   W-20.0, H-18.0, H-T2,  DZ0+T2, ZB0)
    st.box(P+"ust_ic_2mm",     20.0,   W-20.0, H-20.0, H-18.0, DZ0+T2, ZB0)
    # ---- PLINT (bukme sac U, 20 iceride) + 4 ayar ayagi
    st.prism_y(P+"plint_U", [(20.0, -460.0), (20.0, 20.0), (W-20.0, 20.0), (W-20.0, -460.0),
                             (W-21.5, -460.0), (W-21.5, 18.5), (21.5, 18.5), (21.5, -460.0)], 10.0, PLINT[1])
    # ayar ayaklari ORTAK PARCA (_ortak/AYAK_AYAR_M12) -> asm() de 4 ornek
    # ---- ON CERCEVE: TEK lazer kesim 2 mm 304 levha — 12 goz agzi + pano agzi
    kes = [(x0+9.0, x0+591.0, y0+9.0, y0+191.0, ZF-3.0, ZF+1.0) for _, _, x0, y0 in _goz_yerleri()]
    kes.append((29.0, W-29.0, PANO[0]+9.0, PANO[1]-9.0, ZF-3.0, ZF+1.0))
    st.box(P+"on_cerceve_2mm", T2, W-T2, PLINT[1]+T2, H-T2, ZF-T2, ZF, kes)
    # ---- BINDIRME SACI: kapi bunun uzerine kapanir (kasa icine 10 mm bindirme kenari)
    kes2 = [(x0+20.0, x0+580.0, y0+20.0, y0+180.0, ZB0-1.0, ZB1+1.0) for _, _, x0, y0 in _goz_yerleri()]
    st.box(P+"bindirme_saci_2mm", 20.0, W-20.0, SY0-10.0, SY0+SIRA*SH+10.0, ZB0, ZB1, kes2)
    # ---- PANO 150..400 : kilit kartlari, 12 V PSU, router  (BEYIN PC hat panosunda)
    st.box(P+"pano_kapagi_2mm", 30.0, W-30.0, PANO[0]+10.0, PANO[1]-10.0, ZF-2.0, ZF,
           [(W-100.0, W-80.0, 265.0, 285.0, ZF-3.0, ZF+1.0)])     # anahtarli kilit deligi
    st.cyl_z(P+"pano_anahtarli_kilit_D20", W-90.0, 275.0, 10.0, 26.0, ZF)
    st.box(P+"pano_plakasi_2mm", 40.0, W-40.0, PANO[0]+20.0, PANO[1]-20.0, -212.0, -210.0)
    for i in range(2):
        st.box(P+"kilit_kontrol_karti_%d" % (i+1), 70.0+i*220.0, 260.0+i*220.0, 200.0, 310.0, -210.0, -175.0)
    st.box(P+"psu_12V_150W", 520.0, 660.0, 200.0, 310.0, -210.0, -155.0)
    st.box(P+"router_LAN",   700.0, 860.0, 200.0, 300.0, -210.0, -175.0)
    st.box(P+"klemens_rayi", 70.0, W-70.0, 340.0, 347.5, -210.0, -175.0)
    st.box(P+"kablo_kanali_arka", W-120.0, W-60.0, PANO[1], H-60.0, -476.0, -444.0)   # klape zonunun arkasi
    st.box(P+"ust_kablo_rafi_2mm", 20.0, W-20.0, UST[0], UST[0]+2.0, -440.0, ZB0)
    # =============== KOD UNITESI (dolabin hemen saginda, duvara gomme) ===============
    st.box(P+"kod_govde_2mm_sol",  KX0, KX0+T2, KY0, KY1, KZ0, ZF)
    st.box(P+"kod_govde_2mm_sag",  KX1-T2, KX1, KY0, KY1, KZ0, ZF)
    st.box(P+"kod_govde_2mm_alt",  KX0+T2, KX1-T2, KY0, KY0+T2, KZ0, ZF)
    st.box(P+"kod_govde_2mm_ust",  KX0+T2, KX1-T2, KY1-T2, KY1, KZ0, ZF)
    st.box(P+"kod_govde_2mm_arka", KX0+T2, KX1-T2, KY0+T2, KY1-T2, KZ0, KZ0+T2)
    st.box(P+"kod_cam_6mm_IK10",   KX0+T2, KX1-T2, 1270.0, KY1-T2, 34.0, ZF)   # ekran + kamera + LED onu
    st.box(P+"kod_led_serit",      KX0+20.0, KX1-20.0, 1410.0, 1424.0, 26.0, 32.0)
    st.box(P+"kod_ekran_7inc",     KX0+20.0, KX1-20.0, 1300.0, 1400.0, 18.0, 32.0)
    st.box(P+"kod_kamera",         KX1-50.0, KX1-30.0, 1276.0, 1296.0, 18.0, 32.0)
    for r in range(4):                                   # metal PIN pad 4 x 3 (IK09, IP65)
        for c in range(3):
            st.box(P+"kod_tus_%d%d" % (r+1, c+1), KX0+40.0+c*40.0, KX0+70.0+c*40.0,
                   1240.0-r*30.0, 1265.0-r*30.0, 28.0, 34.0)
    st.box(P+"kod_2D_okuyucu_QR",  KX0+40.0, KX0+110.0, 1105.0, 1140.0, 16.0, 32.0)
    st.box(P+"kod_kontrolcu_RPi",  KX0+30.0, KX1-30.0, KY0+40.0, KY0+110.0, -32.0, -15.0)
    st.box(P+"kod_psu_12V",        KX0+30.0, KX0+110.0, KY0+130.0, KY0+200.0, -32.0, -15.0)


# =========================== 3 · MONTAJ ===========================
def asm():
    st = Station(ROOT, "PICKUP_v1"); st.load_dir(); print("kasa parca:", len(st.parts))
    O = lambda g: os.path.join(ORTAK, g, g + ".SLDASM")
    for i, j, x0, y0 in _goz_yerleri():
        st.add_instance(O("TESLIM_GOZU"), offset_mm=(x0, y0, 0.0))
    for ax, az in ((60.0, -40.0), (W-60.0, -40.0), (60.0, -400.0), (W-60.0, -400.0)):
        st.add_instance(O("AYAK_AYAR_M12"), offset_mm=(ax, 0.0, az))
    st.assemble("PICKUP_v1")


if __name__ == "__main__":
    faz = sys.argv[1]; sw.CloseAllDocuments(True)
    if faz == "alt":
        teslim_gozu(); Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        st = Station(ROOT, "PICKUP_v1")
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
        kasa(st); print("PICKUP v1 kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "parca":
        import re
        pat = re.compile(sys.argv[2]); st = Station(ROOT, "PICKUP_v1"); n = [0]
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
