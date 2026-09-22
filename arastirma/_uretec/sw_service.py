# -*- coding: utf-8 -*-
# AUTOKITCH — 7 · SERVICE v1 (10 Eyl 2026) — TEMIZ BASIT KURGU   [rev.2 — denetim duzeltmeleri]
#
# AYRI UNITE: hatta bagli DEGIL, kendi montaji (7_SERVICE_v1/SERVICE_v1.SLDASM).
# SOGUTMA YOK — kompresor / evaporator / fan hicbiri yok. Ustteki silindir YANGIN TUPU dur.
#
# KAYNAK: teknik_cizim51.py "7 · SERVICE" kolonu. Cizimde olculer TEPEDEN (d); y = 1970 - d:
#   d    0.. 300  -> y 1670..1968  TEKNIK   : mini UPS (yalniz BEYIN) + yangin tupu + priz
#   d  300.. 780  -> y 1190..1667  AMBALAJ RAFI 1 (6 bolme = 7 goz)
#   d  780..1260  -> y  710..1187  AMBALAJ RAFI 2 (6 bolme = 7 goz)
#   d 1260..1720  -> y  256.. 707  TEMIZLIK (KILITLI) : 4 bidon + yedek robot ucu rafi
#        MOP YOK — Kemal karari (10 Eyl 2026). Cizimdeki 'mop kapi icinde' notu IPTAL.
#        KOVA/SUZGEC/BEZ KUTUSU da SILINDI (rev.2): cizimde yoklar, uydurmaydilar.
#   d 1720..1820  -> y  123.. 253  poset + cop posedi CEKMECESI
#   plint 0..120  : izgara artik plint sacinin KENDI yarigi (sw_lib.shell izgara=)
#
# rev.2 DUZELTMELERI (bagimsiz denetim, 10 Eyl 2026):
#   1  fugalarin arkasi ACIKTI (5 x 3 x 640 mm gorus hatti) -> FUGA KOR LAMALARI z 14..15,5
#   2  panel-sove dusey birlesimi 0 mm idi -> XP0/XP1 33/667, 4 kenarda esit 3 mm fuga
#   3  cekmece on paneli havadaydi -> cekmece on saci z 19..20 e alindi, panel ona baglaniyor
#   4  4 bidon birbirinin icine giriyordu (beyaz liste gizlemis) -> cizimdeki 130 adima donuldu
#   5  BIDON_5L 4,05 L idi -> 95 x 270 x 200 = 5,13 L
#   6  YANGIN_TUPU_6KG uydurmaydi -> cizimdeki olcu Ø110 x 320 = 2 kg ABC (YANGIN_TUPU_2KG)
#   7  tup yataga degmiyordu, kayis bosluktaydi -> yatak tabani tupe teget, kayis yatak bacaklarina
#   8  UPS/priz havadaydi -> UPS raf ustune oturdu, priz sol ic yan saca yaslandi
#   9  raf_temizlik / raf_teknik tasiyicisizdi -> L konsollar eklendi
#   10 ambalaj bolmeleri on lamayi/arka dayamayi deliyordu -> z araligi kisaltildi
#   11 cekmece raylari havadaydi ve tekrar eden formdu -> CEKMECE_RAYI_450 alt montaji, 2 ornek
#   12 kilit silindirinin panelde deligi yoktu -> panel() e delik parametresi
#
# CEPHE STANDARDI (sogutmasiz): bukme sac 1,5 + 20 mm donus, on yuz z 38,5..40, fuga 3, KULP YOK.
import sys, os
from sw_lib import *

ARA  = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "7_SERVICE_v1"); ORTAK = os.path.join(ARA, "_ortak")
P    = "S1_"
W, T, FUGA, SOVE, TIC = 700.0, 1.5, 3.0, 30.0, 1.0
XI0, XI1 = 22.5, 677.5                      # ic sac yuzeyleri
ZC = -20.0                                  # hucre on yuzu
ZI0 = ZK + T + TIC                          # ic hacim arka yuzu -817,5
XP0, XP1 = SOVE + FUGA, W - SOVE - FUGA     # cephe paneli 33..667 -> dusey fuga da 3 mm
KOR0, KOR1 = 14.0, 15.5                     # fuga kor lamasi z araligi (kapak donusu z 20 de basliyor)

COP    = (123.0,   253.0)
TEMIZ  = (256.0,   707.0)
AMB2   = (710.0,  1187.0)
AMB1   = (1190.0, 1667.0)
TEKNIK = (1670.0, 1968.0)
# kor lamasi y araliklari — fugayi ortuyor ama cekmece govdesine (y 131..245) girmiyor
LAMA_Y = ((114.0, 129.0), (247.0, 265.0), (698.0, 719.0), (1178.0, 1199.0), (1658.0, 1679.0))
GOZ    = ((23.5, 79.0), (81.0, 174.0), (176.0, 269.0), (271.0, 364.0),
          (366.0, 459.0), (461.0, 554.0), (556.0, 676.5))     # 6 bolme -> 7 goz
BOLME_X = (80.0, 175.0, 270.0, 365.0, 460.0, 555.0)
BLANK   = 400.0                             # PACK v3 blanki 400 x 760 (_ortak/KUTU_BLANK_40x76)
RAFZ0, RAFZ1 = -803.0, -25.0                # raf derinligi (arkada kablo kanalina 3 mm pay)
YT_X, YT_Y, YT_Z = 300.0, 1825.0, -200.0    # yangin tupu: cizimdeki x 300..620 · y 1770..1880
YT_KX = (340.0, 520.0)                      # tup yataklari
BID_X = (110.0, 240.0, 370.0, 500.0)        # cizimdeki 130 mm adim
KIL_X, KIL_Y = 607.0, 481.5                 # kilit silindiri
# kapi tablosu — kasa() ve asm() AYNI kaynaktan okur (ad, band, bas-ac mandali var mi, mentese kotlari)
KAPILAR = (("cop",      COP,    True,  ()),
           ("temizlik", TEMIZ,  False, (TEMIZ[0]+60.0,  TEMIZ[1]-100.0)),
           ("ambalaj2", AMB2,   True,  (AMB2[0]+70.0,   AMB2[1]-110.0)),
           ("ambalaj1", AMB1,   True,  (AMB1[0]+70.0,   AMB1[1]-110.0)),
           ("teknik",   TEKNIK, True,  (TEKNIK[0]+50.0, TEKNIK[1]-90.0)))


def panel(ad, y0, y1, kapi, mentese=(), delik=()):
    """cephe paneli — bukme sac 1,5, 20 mm yan donus, alt/ust donus; kulp YOK, bas-ac mandali"""
    st_ = panel.st
    st_.prism_y(P+ad, [(XP0, ZF1), (XP0, 20.0), (XP0+T, 20.0), (XP0+T, ZF0),
                       (XP1-T, ZF0), (XP1-T, 20.0), (XP1, 20.0), (XP1, ZF1)], y0, y1, delik)
    st_.box(P+ad+"_donus_alt", XP0+T, XP1-T, y0, y0+T, 20.0, ZF0)
    st_.box(P+ad+"_donus_ust", XP0+T, XP1-T, y1-T, y1, 20.0, ZF0)
    # mentese ve mandal ORTAK PARCA (_ortak/MENTESE_GIZLI_34 · MANDAL_BAS_AC) -> asm() de ornek


# =========================== 1 · ALT GRUPLAR ===========================
def ambalaj_rafi():
    """AMBALAJ RAFI — TEK FORM, 2 ornek. KASA KAYNAGI sirasinda monte edilir (sokulur parca degil;
       655 x 780 x 420 govde 620 mm kapi acikligindan gecmez). Yerel: raf plakasi alt yuzu y = 0."""
    ad = "AMBALAJ_RAFI_700"; st = Station(os.path.join(ORTAK, ad), ad); p = "AMB_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.box(p+"raf_plakasi_2mm", XI0, XI1, 0.0, 2.0, RAFZ0, RAFZ1)
    st.box(p+"on_tutucu_lama_1.5", XI0, XI1, 2.0, 60.0, RAFZ1-1.5, RAFZ1)
    st.box(p+"arka_dayama_1.5",    XI0, XI1, 2.0, 60.0, RAFZ0, RAFZ0+1.5)
    for i, xx in enumerate(BOLME_X, 1):      # bolmeler lamalarin ARASINDA kaliyor
        st.box(p+"bolme_1.5_%d" % i, xx-0.75, xx+0.75, 2.0, 422.0, RAFZ0+1.5, RAFZ1-1.5)
    for i, (x0, x1) in enumerate(GOZ, 1):    # her gozde yassi kutu yigini (blank ayakta, x boyunca istif)
        st.box(p+"blank_yigini_%d" % i, x0+1.0, x1-1.0, 3.0, 3.0+BLANK, -785.0, -25.0)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


def bidon():
    """BIDON 5 L — TEK FORM, 4 ornek. 95 x 270 x 200 = 5,13 L (dar-derin bidon).
       Yerel: taban y = 0, sol on kose x = 0 / z = 0"""
    ad = "BIDON_5L"; st = Station(os.path.join(ORTAK, ad), ad); p = "BD_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.box(p+"govde_HDPE", 0.0, 95.0, 0.0, 270.0, -200.0, 0.0)
    st.cyl_y(p+"boyun_D40", 47.5, -100.0, 20.0, 270.0, 288.0)
    st.cyl_y(p+"kapak_D48", 47.5, -100.0, 24.0, 288.0, 308.0)
    st.box(p+"etiket_0.2", 5.0, 90.0, 70.0, 200.0, 0.0, 0.2)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


def yangin_tupu():
    """YANGIN TUPU 2 kg ABC — YATAY, ekseni X. Olcu teknik_cizim51.py:377 den: Ø110 x 320.
       Yerel: eksen y = 0 / z = 0, tup dibi x = 0"""
    ad = "YANGIN_TUPU_2KG"; st = Station(os.path.join(ORTAK, ad), ad); p = "YT2_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.part(p+"tup_govdesi_D110", [(RT, 'circ', (0.0,   0.0, 55.0),   0.0, 270.0, False)])
    st.part(p+"tup_omuzu_D60",    [(RT, 'circ', (0.0,   0.0, 30.0), 270.0, 300.0, False)])
    st.part(p+"vana_govdesi_D36", [(RT, 'circ', (0.0,   0.0, 18.0), 300.0, 336.0, False)])
    st.box(p+"tetik_kolu", 306.0, 350.0, 18.0, 26.0, -10.0, 10.0)
    st.part(p+"hortum_D16",       [(RT, 'circ', (0.0, -26.0,  8.0), 318.0, 336.0, False)])
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


def cekmece_rayi():
    """CEKMECE RAYI 450 tam acilim — TEK FORM, 2 ornek. Yerel: dis profil sol yuzu x = 0"""
    ad = "CEKMECE_RAYI_450"; st = Station(os.path.join(ORTAK, ad), ad); p = "CRY_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.box(p+"dis_profil_12.7", 0.0, 12.7, 0.0, 45.0, -610.0, 0.0)          # kasa ic yanagina
    st.box(p+"ara_profil",      1.2, 11.5, 2.0, 43.0, -580.0, 0.0)
    st.box(p+"ic_profil",       2.4, 10.3, 4.0, 41.0, -560.0, 0.0)          # cekmece yanagina
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


# =========================== 2 · KASA ===========================
def kasa(st):
    panel.st = st
    # plint izgarasi artik plint sacinin KENDI yarigi (ayri panel = sahte izgara idi)
    shell(st, P, W, "plint", izgara=[(80+i*40, 100+i*40, 40, 100, 17, 21) for i in range(14)])
    sove_L(st, P, W, Y0, H, SOVE)
    # ---- ic sac kaplama 1,0
    st.box(P+"ic_yan_sol", XI0-TIC, XI0, Y0+T, 1968.5, ZI0, ZC)
    st.box(P+"ic_yan_sag", XI1, XI1+TIC, Y0+T, 1968.5, ZI0, ZC)
    st.box(P+"ic_arka",    XI0, XI1, Y0+T, 1968.5, ZK+T, ZI0)
    st.box(P+"ic_taban",   XI0, XI1, Y0+T, Y0+T+TIC, ZI0, ZC)
    st.box(P+"ic_tavan",   XI0, XI1, 1967.5, 1968.5, ZI0, ZC)
    # =============== CEPHE ===============
    for ad, (y0, y1), kapi, ment in KAPILAR:
        panel("panel_"+ad, y0, y1, kapi, ment,
              [(KIL_X-10.5, KIL_X+10.5, KIL_Y-10.5, KIL_Y+10.5, 13.0, 41.0)] if ad == "temizlik" else ())
    st.cyl_z(P+"kilit_silindiri_D20", KIL_X, KIL_Y, 10.0, 14.0, 40.0)
    # ---- UST CEPHE SERIDI: en ust panelin ustu (1968) ile kabin tepesi (1970) arasindaki 2 mm band
    st.part(P+"ust_cephe_seridi_1.5", [(RT, 'poly',
             [(-ZF1, 1968.0), (-ZF1, 1970.0), (-ZF0, 1970.0), (-ZF0, 1969.5), (0.0, 1969.5), (0.0, 1968.0)],
             SOVE, W-SOVE, False)])
    # ---- FUGA KOR LAMALARI: her fuganin arkasi z 14..15,5 te kapali. Kapak donusleri z 20 de
    #      basladigi icin acilmaya engel degil; mandal z 16..20 e cekildi.
    for i, (l0, l1) in enumerate(LAMA_Y, 1):
        st.box(P+"fuga_kor_lamasi_%d" % i, 34.0, 666.0, l0, l1, KOR0, KOR1)
    st.box(P+"fuga_kor_dusey_sol", 30.0, 34.0,  Y0, H, KOR0, KOR1)     # dusey fuga 30..33 un arkasi
    st.box(P+"fuga_kor_dusey_sag", 666.0, 670.0, Y0, H, KOR0, KOR1)
    # =============== RAF PLAKALARI + TASIYICILARI ===============
    st.box(P+"raf_temizlik_2mm", XI0, XI1, TEMIZ[0],  TEMIZ[0]+2.0,  ZI0, ZC,
           [(605.0, 655.0, TEMIZ[0]-1.0,  TEMIZ[0]+3.0,  ZI0-1.0, ZI0+13.0)])
    st.box(P+"raf_teknik_2mm",   XI0, XI1, TEKNIK[0], TEKNIK[0]+2.0, ZI0, ZC,
           [(605.0, 655.0, TEKNIK[0]-1.0, TEKNIK[0]+3.0, ZI0-1.0, ZI0+13.0)])
    for y in (TEMIZ[0], AMB2[0], AMB1[0], TEKNIK[0]):
        st.prism_z(P+"raf_tasiyici_sol_%d" % int(y), [(XI0, y-40.0), (XI0+1.5, y-40.0), (XI0+1.5, y-2.0),
                   (XI0+20.0, y-2.0), (XI0+20.0, y), (XI0, y)], RAFZ0, RAFZ1)
        st.prism_z(P+"raf_tasiyici_sag_%d" % int(y), [(XI1, y-40.0), (XI1-1.5, y-40.0), (XI1-1.5, y-2.0),
                   (XI1-20.0, y-2.0), (XI1-20.0, y), (XI1, y)], RAFZ0, RAFZ1)
    # =============== TEKNIK BANDI ===============
    st.box(P+"ups_mini_1kVA",    40.0, 240.0, TEKNIK[0]+2.0, TEKNIK[0]+162.0, -420.0, -60.0)  # rafa oturur
    st.box(P+"ups_kablo_cikisi", 60.0, 220.0, TEKNIK[0]+2.0, TEKNIK[0]+34.0,  -440.0, -420.0)
    st.box(P+"priz_kutusu_6li",  XI0, 280.0, TEKNIK[0]+200.0, TEKNIK[0]+270.0, -140.0, -60.0) # yan saca yasli
    for i, xx in enumerate(YT_KX, 1):        # tup yatagi: U kanal 1,5 — tabani tupe TEGET
        uo0, uo1 = -(YT_Z+57.5), -(YT_Z-57.5); ui0, ui1 = -(YT_Z+56.0), -(YT_Z-56.0)
        st.part(P+"tup_yatagi_%d" % i, [(RT, 'poly',
                [(uo1, YT_Y+62.0), (uo1, YT_Y-56.5), (uo0, YT_Y-56.5), (uo0, YT_Y+62.0),
                 (ui0, YT_Y+62.0), (ui0, YT_Y-55.0), (ui1, YT_Y-55.0), (ui1, YT_Y+62.0)],
                xx-15.0, xx+15.0, False)])
        st.box(P+"tup_kayisi_%d" % i, xx-15.0, xx+15.0, YT_Y+55.0, YT_Y+56.5, YT_Z-56.0, YT_Z+56.0)
    st.box(P+"kablo_kanali_arka_40x12", 610.0, 650.0, 130.0, 1900.0, ZI0, ZI0+12.0)
    # =============== TEMIZLIK BANDI (KILITLI) ===============
    st.box(P+"yedek_robot_ucu_rafi_2mm", XI0, XI1, 600.0, 602.0, -500.0, -60.0)
    st.prism_z(P+"yedek_uc_rafi_konsol_sol", [(XI0, 570.0), (XI0+1.5, 570.0), (XI0+1.5, 598.0),
               (XI0+30.0, 598.0), (XI0+30.0, 600.0), (XI0, 600.0)], -500.0, -60.0)
    st.prism_z(P+"yedek_uc_rafi_konsol_sag", [(XI1, 570.0), (XI1-1.5, 570.0), (XI1-1.5, 598.0),
               (XI1-30.0, 598.0), (XI1-30.0, 600.0), (XI1, 600.0)], -500.0, -60.0)
    # =============== COP POSETI CEKMECESI ===============
    CX0, CX1 = 36.2, 663.8                   # cekmece yanaklari (raylar disinda)
    st.box(P+"cekmece_tabani_1.0", CX0, CX1, COP[0]+8.0, COP[0]+9.0, -640.0, 19.0)
    st.box(P+"cekmece_arka_1.0",   CX0, CX1, COP[0]+9.0, COP[1]-8.0, -641.0, -640.0)
    st.box(P+"cekmece_on_1.0",     CX0, CX1, COP[0]+8.0, COP[1]-8.0,  19.0,  20.0)   # panel buna baglanir
    st.box(P+"cekmece_sol_1.0", CX0-1.0, CX0, COP[0]+9.0, COP[1]-8.0, -641.0, 19.0)
    st.box(P+"cekmece_sag_1.0", CX1, CX1+1.0, COP[0]+9.0, COP[1]-8.0, -641.0, 19.0)
    st.box(P+"poset_rulosu_yatagi", CX0, CX1, COP[0]+95.0, COP[0]+112.0, -620.0, -570.0)


# =========================== 3 · MONTAJ ===========================
def asm():
    st = Station(ROOT, "SERVICE_v1"); st.load_dir(); print("kasa parca:", len(st.parts))
    O = lambda g: os.path.join(ORTAK, g, g + ".SLDASM")
    for y in (AMB2[0], AMB1[0]):
        st.add_instance(O("AMBALAJ_RAFI_700"), offset_mm=(0.0, y, 0.0))
    st.add_instance(O("YANGIN_TUPU_2KG"), offset_mm=(YT_X, YT_Y, YT_Z))
    for xx in BID_X:
        st.add_instance(O("BIDON_5L"), offset_mm=(xx, TEMIZ[0]+2.0, -120.0))
    for xx in (XI0, 664.8):                  # cekmece raylari: sol ve sag
        st.add_instance(O("CEKMECE_RAYI_450"), offset_mm=(xx, COP[0]+40.0, -40.0))
    for ax, az in AYAK_YERI(W):                       # ORTAK: ayar ayagi (eski 4+4 yerel parca)
        st.add_instance(O("AYAK_AYAR_M12"), offset_mm=(ax, 0.0, az))
    for ad, (y0, y1), kapi, ment in KAPILAR:          # ORTAK: gizli mentese + bas-ac mandali
        for yy in ment: st.add_instance(O("MENTESE_GIZLI_34"), offset_mm=(XP0+2.0, yy, 0.0))
        if kapi: st.add_instance(O("MANDAL_BAS_AC"), offset_mm=(XP1-90.0, (y0+y1)/2-10.0, 0.0))
    st.assemble("SERVICE_v1")


if __name__ == "__main__":
    faz = sys.argv[1]; sw.CloseAllDocuments(True)
    if faz == "alt":
        ambalaj_rafi(); bidon(); yangin_tupu(); cekmece_rayi(); Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        st = Station(ROOT, "SERVICE_v1")
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
        kasa(st); print("SERVICE v1 kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "parca":
        import re
        pat = re.compile(sys.argv[2]); st = Station(ROOT, "SERVICE_v1"); n = [0]
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
