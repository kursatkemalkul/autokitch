# -*- coding: utf-8 -*-
# AUTOKITCH — 5 · PACK v3 (10 Eyl 2026) — TEMIZ BASIT KURGU   (v2 = 5_PACK, dokunulmadi)
#
# KUTU: _ortak/KUTU_KATLI_32x32 — taban 320x320, duvar 40, arkada MENTESELI KAPAK 320 (dik durur),
#       onde dil 40.  Acilmis blank = 400 x 760 (_ortak/KUTU_BLANK_40x76), E-dalga 1,6.
#
# CEVRIM (tek dogrusal hareket, tek step motor):
#   1. Plunger 6 vantuzla sarjorun en alt blankini ALTTAN tutar (vantuz yuzu y 1090)
#   2. Asagi iner; y 951..1000 deki FORM KALIBI ndan gecerken 4 duvar yukari katlanir,
#      arka kapak KAPAK PLOWU ile dik konumda tutulur
#   3. y 720 de kutuyu KUTU DAYAMA LEDGELERINE (y 718..720) birakir, vakum kesilir
#   4. Robot pideyi koyar -> KAPAK KOLU (U cubuk, 24 V) kapagi one devirir -> robot kutuyu alir
#   5. Plunger yukari doner (kutu alinmadan donmez).  STROK = 1072 - 702 = 370 mm
#      MODELDEKI AN: plunger ALT konumda, kutu ledgelerin uzerinde, kapak dik.
#
# 6 BANT — her biri TEK islev:
#   plint          0    - 120   izgarali
#   PANO           123  - 420   duz kapak
#   VAKUM+TAHRIK   423  - 695   duz kapak (pompa, tank, selenoid, step motor)
#   KUTULAMA AGZI  698  - 948   ACIK  <- kutu burada dolar, robot alir
#   KALIP+SARJOR   951  - 1880  duz kapak (form kalibi + 506 blank)
#   UST SERIT      1883 - 1968  duz panel
#
# CEPHE STANDARDI (sogutmasiz): bukme sac 1,5, 20 mm donus, on yuz z 38,5..40, fuga 3, KULP YOK.
import sys, os
from sw_lib import *

ARA  = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "5_PACK_v3"); ORTAK = os.path.join(ARA, "_ortak")
P    = "P3_"
W, T, FUGA, SOVE, TIC = 700.0, 1.5, 3.0, 30.0, 1.0
XI0, XI1 = 22.5, 677.5                      # ic sac yuzeyleri (yanlarda 20 mm kablo boslugu)
ZC = -20.0                                  # hucre on yuzu
ZI0 = ZK + T + TIC                          # ic hacim arka yuzu -817,5
XP0, XP1 = SOVE + FUGA, W - SOVE - FUGA     # cephe paneli 33..667 -> dusey fuga da 3 mm
KOR0, KOR1 = 14.0, 15.5                     # fuga kor lamasi z araligi
LAMA_Y = ((114.0, 129.0), (411.0, 432.0), (1871.0, 1892.0))   # plint · pano/tahrik · sarjor/ust

PANO   = (123.0, 420.0)
TAHRIK = (423.0, 695.0)
AGIZ   = (698.0, 948.0)                     # ACIK kutulama agzi
SARJOR = (951.0, 1880.0)
UST    = (1883.0, 1968.0)

# ---- kutu / kalip / sarjor kotlari
KX0, KX1 = 190.0, 510.0                     # kutu tabani x (320)
KZ0, KZ1 = -440.0, -120.0                   # kutu tabani z (320); arka kapak z -441,6 dik durur
OX0, OX1 = 188.0, 512.0                     # kalip agzi x (324 = kutu + 2 mm pay)
OZ0, OZ1 = -442.0, -118.0                   # kalip agzi z (324)
Y_TABLA  = 720.0                            # ledge ust yuzu = kutu taban kotu (dik kapak tepesi 1081,6)
Y_KALIP  = 951.0                            # form kalibi plakasi (951..1000)
Y_UST    = 1072.0                           # plunger plakasi UST konum (vantuz yuzu 1090 = yigin alti)
Y_ALT    = 702.0                            # plunger plakasi ALT konum (vantuz yuzu 720 = kutu tabani)
Y_YIGIN  = 1090.0                           # blank yigini alt kotu (dik kapak tepesi + 8,4 pay)
BX0, BX1 = 150.0, 550.0                     # blank 400 x 760
BZ0, BZ1 = -815.5, -55.5
VNT_X, VNT_Z = (250.0, 350.0, 450.0), (-400.0, -160.0)   # 6 vantuz — merkez kolonun disinda
ZR       = -785.0                           # dikey tahrik ekseni z (2 ray + vida arkada)
KAPILAR = (("pano",   PANO,   True,  (PANO[0]+60.0,   PANO[1]-100.0)),
           ("tahrik", TAHRIK, True,  (TAHRIK[0]+50.0, TAHRIK[1]-90.0)),
           ("sarjor", SARJOR, True,  (SARJOR[0]+80.0, SARJOR[1]-120.0)),
           ("ust",    UST,    False, ()))


def panel(ad, y0, y1, kapi, mentese=()):
    st_ = panel.st
    st_.prism_y(P+ad, [(XP0, ZF1), (XP0, 20.0), (XP0+T, 20.0), (XP0+T, ZF0),
                       (XP1-T, ZF0), (XP1-T, 20.0), (XP1, 20.0), (XP1, ZF1)], y0, y1)
    st_.box(P+ad+"_donus_alt", XP0+T, XP1-T, y0, y0+T, 20.0, ZF0)
    st_.box(P+ad+"_donus_ust", XP0+T, XP1-T, y1-T, y1, 20.0, ZF0)
    # mentese ve mandal ORTAK PARCA (_ortak/MENTESE_GIZLI_34 · MANDAL_BAS_AC) -> asm() de ornek


# =========================== 1 · ALT GRUPLAR ===========================
def vantuz_yukari():
    """VANTUZ D40 — EMME YUZU YUKARI bakan tip (plunger blanki alttan tutar).
       Yerel: emme yuzu merkezi (0,0,0), govde -Y.  (_ortak/VANTUZ_D40 asagi bakan tiptir.)"""
    ad = "VANTUZ_D40_YUKARI"; st = Station(os.path.join(ORTAK, ad), ad); p = "VNU_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.cyl_y(p+"koruk_dudak_D40", 0, 0, 20, -18, 0)
    st.cyl_y(p+"govde_D24",       0, 0, 12, -30, -18)
    st.cyl_y(p+"nipel_M8",        0, 0,  4, -44, -30)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])



def plunger_grubu():
    """PLUNGER — vantuz plakasi + merkez kolon (kalip agzindan gecer) + arka kol + araba.
       Yerel: PLAKA UST YUZU y = 0. Montajda offset y = Y_UST (ust konum)."""
    ad = "PLUNGER_6VANTUZ"; st = Station(os.path.join(ORTAK, ad), ad); p = "PLG_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.box(p+"vantuz_plakasi_296x316x2", 202.0, 498.0, -2.0, 0.0, -438.0, -122.0)
    st.box(p+"merkez_kolon_80x80",       310.0, 390.0, -440.0, -2.0, -380.0, -300.0)   # kalip agzindan gecer
    st.box(p+"kol_profil_80x60",         310.0, 390.0, -440.0, -380.0, -760.0, -380.0) # agiz tabaninin ALTINDA
    for nm, x0, x1 in (("sol", 220.0, 310.0), ("sag", 390.0, 480.0)):    # kol profilinin YANINDA
        st.box(p+"araba_dikey_kanadi_"+nm, x0, x1, -440.0, -380.0, -755.0, -745.0)
    st.box(p+"araba_plakasi_10mm",       220.0, 480.0, -460.0, -440.0, -800.0, -740.0,
           [(xx-20, xx+20, -461.0, -439.0, -805.0, -765.0) for xx in (250.0, 350.0, 450.0)])  # ray yariklari
    for i, xx in enumerate((250.0, 450.0), 1):
        st.box(p+"lineer_rulman_%d" % i, xx-20, xx+20, -500.0, -460.0, ZR-15, ZR+15)
    st.box(p+"vida_somunu_1605",         330.0, 370.0, -500.0, -460.0, ZR-12, ZR+12)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


# =========================== 2 · KASA ===========================
def kasa(st):
    panel.st = st
    # plint izgarasi artik plint sacinin KENDI yarigi (ayri panel = sahte izgara idi)
    shell(st, P, W, "plint", izgara=[(80+i*40, 100+i*40, 40, 100, 17, 21) for i in range(14)])
    sove_L(st, P, W, Y0, H, SOVE)
    # ---- ic sac kaplama 1,0 (yanlarda 20 mm kablo boslugu)
    st.box(P+"ic_yan_sol", XI0-TIC, XI0, Y0+T, 1968.5, ZI0, ZC)
    st.box(P+"ic_yan_sag", XI1, XI1+TIC, Y0+T, 1968.5, ZI0, ZC)
    st.box(P+"ic_arka",    XI0, XI1, Y0+T, 1968.5, ZK+T, ZI0)
    st.box(P+"ic_taban",   XI0, XI1, Y0+T, Y0+T+TIC, ZI0, ZC)
    st.box(P+"ic_tavan",   XI0, XI1, 1967.5, 1968.5, ZI0, ZC)
    # =============== CEPHE ===============
    for ad, (y0, y1), kapi, ment in KAPILAR: panel("panel_"+ad, y0, y1, kapi, ment)
    # ---- UST CEPHE SERIDI: en ust panelin ustu (1968) ile kabin tepesi (1970) arasindaki 2 mm band
    st.part(P+"ust_cephe_seridi_1.5", [(RT, 'poly',
             [(-ZF1, 1968.0), (-ZF1, 1970.0), (-ZF0, 1970.0), (-ZF0, 1969.5), (0.0, 1969.5), (0.0, 1968.0)],
             SOVE, W-SOVE, False)])
    # ---- FUGA KOR LAMALARI: disaridan kabin icine gorus hatti kalmiyor
    for i, (l0, l1) in enumerate(LAMA_Y, 1):
        st.box(P+"fuga_kor_lamasi_%d" % i, 34.0, 666.0, l0, l1, KOR0, KOR1)
    for nm, x0, x1 in (("sol", 30.0, 34.0), ("sag", 666.0, 670.0)):     # dusey fuga arkasi
        st.box(P+"fuga_kor_dusey_%s_alt" % nm, x0, x1, Y0, AGIZ[0]-3.0, KOR0, KOR1)
        st.box(P+"fuga_kor_dusey_%s_ust" % nm, x0, x1, AGIZ[1], H, KOR0, KOR1)
    # ---- KUTULAMA AGZI CERCEVESI: dort kenar da cephe duzleminde biter
    a0, a1 = AGIZ
    st.prism_y(P+"agiz_cerceve_sol", [(XP0, ZF1), (40.0, ZF1), (40.0, ZC), (38.5, ZC), (38.5, ZF0), (XP0, ZF0)], a0-3.0, a1)
    st.prism_y(P+"agiz_cerceve_sag", [(XP1, ZF1), (660.0, ZF1), (660.0, ZC), (661.5, ZC), (661.5, ZF0), (XP1, ZF0)], a0-3.0, a1)
    # agiz tabani/tavani yalniz GORUNEN derinlikte; arkasi plunger kolunun ve tahrikin gecis hacmi
    st.box(P+"agiz_tabani", 40.0, 660.0, a0-3.0, a0, -370.0, ZF1, [(300.0, 400.0, a0-4.0, a0+1.0, -375.0, -290.0)])
    st.box(P+"agiz_tavani", 40.0, 660.0, a1-2.0, a1, -430.0, ZC,  [(300.0, 400.0, a1-3.0, a1+1.0, -395.0, -290.0)])
    for yn, ya, yb in (("alt", a0-3.0, a0-1.5), ("ust", a1-1.5, a1)):
        st.box(P+"agiz_cep_kapagi_sol_"+yn, XP0, 38.5, ya, yb, ZC, ZF0)
        st.box(P+"agiz_cep_kapagi_sag_"+yn, 661.5, XP1, ya, yb, ZC, ZF0)
    # =============== PANO ===============
    zb = -250.0
    st.box(P+"pano_plakasi_2mm", 60, 640, 150.0, PANO[1]-15, zb-2, zb)
    st.box(P+"pano_plc", 80, 190, 180, 300, zb, zb+75); st.box(P+"pano_guc_kaynagi_24V", 210, 310, 180, 300, zb, zb+110)
    st.box(P+"pano_step_surucu", 330, 385, 180, 300, zb, zb+120)
    for i in range(2): st.box(P+"pano_motor_surucu_%d" % (i+1), 405+i*60, 450+i*60, 180, 300, zb, zb+100)
    for i in range(3): st.box(P+"pano_servo_surucu_%d" % (i+1), 530+i*35, 555+i*35, 180, 280, zb, zb+60)
    st.box(P+"pano_klemens_rayi", 80, 620, 330, 337.5, zb, zb+35)
    # =============== VAKUM ===============
    st.box(P+"vakum_pompasi_24V_30Ldk", 430, 570, TAHRIK[0]+20, TAHRIK[1]-120, -700.0, -560.0)
    st.cyl_y(P+"vakum_tanki_1L_D100", 150.0, -650.0, 50.0, TAHRIK[0]+20, TAHRIK[0]+160)
    for i, nm in enumerate(("taban", "kapak"), 1):
        st.box(P+"vakum_selenoid_"+nm, 230+(i-1)*55, 270+(i-1)*55, TAHRIK[0]+30, TAHRIK[0]+80, -680.0, -620.0)
    st.box(P+"vakum_sensoru", 360, 400, TAHRIK[0]+30, TAHRIK[0]+60, -680.0, -640.0)
    # =============== DIKEY TAHRIK (arkada, z -785) ===============
    st.box(P+"step_motor_NEMA23_3Nm", 322, 379, 123.0, 183.0, ZR-28, ZR+28)
    st.cyl_y(P+"bilyali_vida_1605", 350.0, ZR, 8.0, 195.0, 660.0)
    st.box(P+"vida_ayagi_alt", 325.0, 375.0, 183.0, 195.0, ZR-25, ZR+25)
    for i, xx in enumerate((250.0, 450.0), 1):
        st.cyl_y(P+"lineer_ray_D16_%d" % i, xx, ZR, 8.0, 195.0, 660.0)
        st.box(P+"ray_ayagi_alt_%d" % i, xx-25, xx+25, 183.0, 195.0, ZR-25, ZR+25)
        st.box(P+"ray_ayagi_ust_%d" % i, xx-25, xx+25, 660.0, 672.0, ZR-25, ZR+25)
    # =============== KUTULAMA AGZI ICI ===============
    for nm, x0, x1, k0, k1 in (("sol", 160.0, 200.0, XI0, 200.0), ("sag", 500.0, 540.0, 500.0, XI1)):
        st.box(P+"kutu_dayama_ledgesi_"+nm, x0, x1, Y_TABLA-2.0, Y_TABLA, -450.0, -110.0)
        st.box(P+"ledge_konsolu_"+nm, k0, k1, Y_TABLA-42.0, Y_TABLA-2.0, -450.0, -444.0)
    # KAPAK KOLU: pivot ekseni kapak mentesesi hizasinda (z -451 / y 744); U cubuk kapagi one devirir
    st.part(P+"kapak_kolu_pivot_mili_D10", [(RT, 'circ', (451.0, 764.0, 5.0), 180.0, 520.0, False)])
    st.part(P+"kapak_kolu_ust_cubuk_D8",   [(RT, 'circ', (451.0, 936.0, 4.0), 200.0, 500.0, False)])
    for i, xx in enumerate((200.0, 492.0), 1):
        st.box(P+"kapak_kolu_dikey_%d" % i, xx, xx+8.0, 768.0, 932.0, -455.0, -447.0)
    st.box(P+"kapak_kolu_motoru_24V_5Nm", 96.0, 176.0, 734.0, 814.0, -491.0, -411.0)
    for i, xx in enumerate((191.0, 491.0), 1):
        st.box(P+"kutu_varlik_sensoru_%d" % i, xx, xx+18.0, 726.0, 744.0, -110.0, -92.0)
    # =============== FORM KALIBI + KAPAK PLOWU ===============
    st.box(P+"form_kalibi_plakasi", XI0, XI1, Y_KALIP, 1000.0, ZI0, ZC,
           [(OX0, OX1, Y_KALIP-1, 1001.0, OZ0, OZ1)])                       # 324 x 324 agiz
    for nm, x0, x1, z0, z1 in (("on", OX0-8, OX1+8, OZ1, OZ1+8), ("arka", OX0-8, OX1+8, OZ0-8, OZ0),
                               ("sol", OX0-8, OX0, OZ0, OZ1), ("sag", OX1, OX1+8, OZ0, OZ1)):
        st.box(P+"kalip_katlama_lamasi_"+nm, x0, x1, 1000.0, 1008.0, z0, z1)
    for i, xx in enumerate((195.0, 497.0), 1):
        st.box(P+"kapak_plowu_%d" % i, xx, xx+8.0, 1008.0, 1060.0, -470.0, -445.0)
    # =============== SARJOR (506 blank) ===============
    for i, xx in enumerate((BX0-20.0, BX1), 1):
        st.prism_y(P+"sarjor_L_kilavuz_%d" % i,
                   [(xx, BZ0), (xx+20.0, BZ0), (xx+20.0, BZ0+2.0), (xx+2.0, BZ0+2.0),
                    (xx+2.0, BZ1-2.0), (xx+20.0, BZ1-2.0), (xx+20.0, BZ1), (xx, BZ1)],
                   Y_YIGIN, SARJOR[1]-10.0)
    st.box(P+"sarjor_arka_kilavuzu_2mm", BX0, BX1, Y_YIGIN, SARJOR[1]-10.0, BZ0-2.0, BZ0)
    st.box(P+"sarjor_on_kilavuzu_2mm",    BX0, BX1, Y_YIGIN, SARJOR[1]-10.0, BZ1, BZ1+2.0)
    for i, (x0, x1, z0, z1) in enumerate(((BX0, BX1, BZ0, BZ0+25.0), (BX0, BX1, BZ1-25.0, BZ1),
                                          (BX0, BX0+25.0, BZ0+25.0, BZ1-25.0),
                                          (BX1-25.0, BX1, BZ0+25.0, BZ1-25.0)), 1):
        st.box(P+"sarjor_tutucu_dili_%d" % i, x0, x1, Y_YIGIN-2.0, Y_YIGIN, z0, z1)
    st.box(P+"blank_yigini_506_adet", BX0, BX1, Y_YIGIN, SARJOR[1]-10.0, BZ0, BZ1)
    for i, yy in enumerate((Y_YIGIN+200.0, Y_YIGIN+500.0, SARJOR[1]-40.0), 1):
        st.box(P+"sarjor_foto_sensoru_%d" % i, 106.0, 124.0, yy, yy+18.0, -420.0, -402.0)
    st.box(P+"kablo_kanali_sag", XI1-45, XI1-5, 150.0, 1800.0, -700.0, -660.0)


# =========================== 3 · MONTAJ ===========================
def asm():
    st = Station(ROOT, "PACK_v3"); st.load_dir(); print("kasa parca:", len(st.parts))
    O = lambda g: os.path.join(ORTAK, g, g + ".SLDASM")
    # modellenen an: plunger kutuyu ledgelere birakmis (ALT konum). Ust konum = Y_UST (strok 370).
    st.add_instance(O("PLUNGER_6VANTUZ"), offset_mm=(0.0, Y_ALT, 0.0))
    for dx in VNT_X:
        for dz in VNT_Z:
            st.add_instance(O("VANTUZ_D40_YUKARI"), offset_mm=(dx, Y_TABLA, dz))
    st.add_instance(O("KUTU_KATLI_32x32"), offset_mm=(KX0, Y_TABLA, KZ1))
    for ax, az in AYAK_YERI(W):                       # ORTAK: ayar ayagi (eski 4+4 yerel parca)
        st.add_instance(O("AYAK_AYAR_M12"), offset_mm=(ax, 0.0, az))
    for ad, (y0, y1), kapi, ment in KAPILAR:          # ORTAK: gizli mentese + bas-ac mandali
        for yy in ment: st.add_instance(O("MENTESE_GIZLI_34"), offset_mm=(XP0+2.0, yy, 0.0))
        if kapi: st.add_instance(O("MANDAL_BAS_AC"), offset_mm=(XP1-90.0, (y0+y1)/2-10.0, 0.0))
    st.assemble("PACK_v3")


if __name__ == "__main__":
    faz = sys.argv[1]; sw.CloseAllDocuments(True)
    if faz == "alt":
        vantuz_yukari(); plunger_grubu(); Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        st = Station(ROOT, "PACK_v3")
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
        kasa(st); print("PACK v3 kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "parca":
        import re
        pat = re.compile(sys.argv[2]); st = Station(ROOT, "PACK_v3"); n = [0]
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
