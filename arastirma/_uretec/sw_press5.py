# -*- coding: utf-8 -*-
# AUTOKITCH — 2 · PRESS v5 (9 Eyl 2026) — DUZ KAPALI CEPHE   (v4 = 2_PRESS, dokunulmadi)
# Kemal: "Fersah bizim makineye mebled olmus gibi dursun; one duz kapak koy, acinca makine gozuksun.
#         Pres yerini makinenin ucu girip hamuru birakacak kadar yap. Ustundeki kisimda makine uclari
#         neye takili nasil duracak, ama cok kucuk alanda. Onunla fersah arasi raf olsun.
#         Gerisini dumduz kapat, temiz goruntu onemli. Ustundeki cop solda, sagdaki alan simdilik bos
#         -> duz kapak, full kapali. Copun ustunde robot kolun hamurla girip birakacagi bosluk olsun."
#
# DIKEY ZON (mm)
#   plint      0      - 120
#   takoz      121,5  - 141,5   (4 x titresim takozu 20)
#   FERSAH     141,5  - 1091,5  (PZP-400  640 x 950 x 800)
#   raf 1      1091,5 - 1093,5
#   UC         1093,5 - 1393,5  (300)
#   raf 2      1393,5 - 1395,5
#   COP        1395,5 - 1675,5  (280)
#   ATMA       1675,5 - 1968,5  (293)
# CEPHE: 5 duz panel + fuga 3, kulp/girinti YOK (bas-ac mandali). Uc aciklik, ucu de tam ihtiyac kadar:
#   O1 PRES 564 x 260  panel genisligince (iki yanda 20 alin) | pence 190 + 70 bilek
#   O2 UC   564 x 250  panel genisligince                     | pence 190 + 2x30
#   O3 ATMA 364 x 250  YALNIZ cop kolonu genisligince         | pence 190 + 60  (motorlu klape)
import sys, os, time, pythoncom
from sw_lib import *

ARA  = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "2_PRESS_v5")
P    = "P5_"
W, T, FUGA, SOVE = 700.0, 1.5, 3.0, 30.0    # sove 45 -> 30: hattaki 700 lik istasyonlarla AYNI
XP0, XP1 = 33.0, 667.0                      # cephe panel bandi (634)
XC1, XR0 = 437.0, 440.0                     # cop kolonu sagi / bos kolon solu (kolon genisligi 404 sabit)

TAKOZ  = (121.5, 141.5)
PRES   = (141.5, 1091.5)                    # PZP-400 Fersah
RAF1   = (1091.5, 1093.5)
UC     = (1093.5, 1393.5)                   # uc (takim) bolmesi 300
RAF2   = (1393.5, 1395.5)
COP    = (1395.5, 1675.5)                   # cop bolmesi 280
ATMA   = (1675.5, 1968.5)                   # atma bolmesi 293

O1 = ( 53.0, 647.0,  760.0, 1020.0)         # pres agzi  594 x 260  (tam genislik — sove 30 ile +30)
O2 = ( 53.0, 647.0, 1120.0, 1370.0)         # uc bolmesi 594 x 250  (tam genislik)
O3 = ( 53.0, 417.0, 1697.0, 1947.0)         # atma agzi  364 x 250  (yalniz cop kolonu, saga tasmaz)
# (ad, x0, x1, y0, y1, aciklik|None, kapi mi, mentese y konumlari)
PANEL = [("panel_pres",    XP0, XP1, TAKOZ[0], 1091.5,  O1,   True,  (200.0, 480.0, 1030.0)),
         ("panel_uc",      XP0, XP1, 1094.5,   1392.5,  O2,   False, ()),
         ("panel_cop",     XP0, XC1, COP[0],   1672.5,  None, True,  (1455.0, 1600.0)),
         ("panel_atma",    XP0, XC1, ATMA[0],  1968.5,  O3,   False, ()),
         ("panel_sag_bos", XR0, XP1, COP[0],   1968.5,  None, False, ())]
# uc yuvalari: (ad, slot x0, slot x1, takim x0, takim x1)
YUVA = [("catal", 150.0, 266.0), ("pence", 300.0, 416.0), ("vantuz", 450.0, 566.0)]
RAY_Y, RAY_Z0, RAY_Z1 = 1372.0, -280.0, -20.0        # uc aski plakasi 8 mm (dock tabani ustune oturur)
COPK = (60.0, 440.0, 1397.0, 1657.0, -680.0, -80.0)  # cop kutusu 380 x 260 x 600 = 59 L


def cephe_paneli(st, ad, x0, x1, y0, y1, acik, kapi, nm):
    """bukme 1,5 duz panel: on plaka ZF0..ZF1 + 20 mm kenar donusleri; aciklik cevresi de bukulu.
       KULP / GIRINTI YOK — kapilar bas-ac mandaliyla acilir (Kemal kurali)"""
    kes = [(acik[0], acik[1], acik[2], acik[3], ZF0-1, ZF1+1)] if acik else []
    st.prism_y(P+ad, [(x0, ZF1), (x0, 20.0), (x0+T, 20.0), (x0+T, ZF0),
                      (x1-T, ZF0), (x1-T, 20.0), (x1, 20.0), (x1, ZF1)], y0, y1, kes)
    st.box(P+ad+"_donus_alt", x0+T, x1-T, y0, y0+T, 20.0, ZF0)
    st.box(P+ad+"_donus_ust", x0+T, x1-T, y1-T, y1, 20.0, ZF0)
    if acik:                                       # aciklik cevresi ice bukum — kesik kenar gorunmez
        a, b, c, d = acik
        st.box(P+ad+"_agiz_sol", a-T, a, c-T, d+T, 20.5, ZF0)
        st.box(P+ad+"_agiz_sag", b, b+T, c-T, d+T, 20.5, ZF0)
        st.box(P+ad+"_agiz_alt", a, b, c-T, c, 20.5, ZF0)
        st.box(P+ad+"_agiz_ust", a, b, d, d+T, 20.5, ZF0)
    # mentese ve mandal ORTAK PARCA (_ortak/MENTESE_GIZLI_34 · MANDAL_BAS_AC) -> asm() de ornek


def kasa(st):
    shell(st, P, W, "plint")                       # dis kabuk 1,5 + plint (temiz, kapali taban)
    sove_L(st, P, W, Y0, H, SOVE)                  # sol/sag duz sove 45
    xi0, xi1, zi = T, W-T, ZK+T
    # ---- yatay raflar (bolme ayirici) 2 mm + on/arka bukum
    for ad, (a, b) in (("raf_uc", RAF1), ("raf_cop", RAF2)):
        st.box(P+ad+"_sac_2mm", xi0, xi1, a, b, zi, 0.0)
        st.box(P+ad+"_on_bukum", xi0, xi1, a-25, a, -T, 0.0)
        st.box(P+ad+"_arka_bukum", xi0, xi1, a-25, a, zi, zi+T)
    # ---- ON CERCEVE ISKELETI (sabit panel + mentese baglantisi), kutu profil 20 x 16
    st.box(P+"on_cerceve_alt",   SOVE+4, W-SOVE-4, 121.5,  141.5,  4.0, 20.0)
    st.box(P+"on_cerceve_raf1",  SOVE+4, W-SOVE-4, 1081.5, 1101.5, 4.0, 20.0)
    st.box(P+"on_cerceve_raf2",  SOVE+4, W-SOVE-4, 1383.5, 1403.5, 4.0, 20.0)
    st.box(P+"on_cerceve_cop",   SOVE+4, 428.0,    1663.0, 1685.0, 4.0, 20.0)   # dikmeye dayanir
    st.box(P+"on_cerceve_ust",   SOVE+4, W-SOVE-4, 1948.5, 1968.5, 4.0, 20.0)
    # DIKMELER: dusey fuganin (x 45..48) arkasini korlestirir; gizli mentese z 18..32 de oldugu
    # icin dikme z 4..17,5 te kaliyor.
    for nm, x0, x1 in (("sol", SOVE, SOVE+4), ("sag", W-SOVE-4, W-SOVE)):
        st.box(P+"on_cerceve_dikme_"+nm, x0, x1, 121.5, 1968.5, 4.0, 17.5)
    st.box(P+"on_cerceve_dikme", 428.0, 448.0, 1403.5, 1948.5, 4.0, 20.0)
    # ---- cephe
    for ad, x0, x1, y0, y1, acik, kapi, nm in PANEL: cephe_paneli(st, ad, x0, x1, y0, y1, acik, kapi, nm)
    # ---- PRES bolmesi: 4 titresim takozu + makine ankraj plakasi
    st.box(P+"pres_ankraj_plakasi_4mm", 20.0, W-20.0, TAKOZ[1]-4, TAKOZ[1], zi, -10.0)
    for i, (ax, az) in enumerate([(50, -60), (610, -60), (50, -740), (610, -740)], 1):
        st.box(P+"pres_titresim_takozu_%d" % i, ax, ax+40, TAKOZ[0], TAKOZ[1]-4, az-40, az)
    # ---- UC bolmesi: 2 yan tasiyici + U yuvali aski plakasi 8 + 3 varlik sensoru
    for ad, xx in (("sol", 110.0), ("sag", 602.0)):
        st.box(P+"uc_tasiyici_"+ad, xx, xx+8, UC[0]+2, RAY_Y, RAY_Z0, RAY_Z1)
    st.box(P+"uc_aski_plakasi_8mm", 110.0, 610.0, RAY_Y, RAY_Y+8, RAY_Z0, RAY_Z1,
           [(a, b, RAY_Y-1, RAY_Y+9, RAY_Z0+60, RAY_Z1+10) for _, a, b in YUVA])
    # varlik sensoru UC_DOCK_PLAKASI grubunun kendi icinde var, ayrica konmadi
    # ---- COP bolmesi: 59 L bukme kutu + tam cekmece rayi + torba kelepcesi
    cx0, cx1, cy0, cy1, cz0, cz1 = COPK
    st.prism_z(P+"cop_kutusu_59L_U", [(cx0, cy1), (cx0, cy0), (cx1, cy0), (cx1, cy1),
                                      (cx1-T, cy1), (cx1-T, cy0+T), (cx0+T, cy0+T), (cx0+T, cy1)], cz0, cz1)
    st.box(P+"cop_kutusu_arka", cx0+T, cx1-T, cy0+T, cy1, cz0, cz0+T)
    st.box(P+"cop_kutusu_on", cx0+T, cx1-T, cy0+T, cy1, cz1-T, cz1)
    for i, xx in enumerate((cx0-13.7, cx1+1.0), 1):
        st.box(P+"cop_rayi_%d" % i, xx, xx+12.7, cy0+30, cy0+75, cz0, cz1+40)
    st.box(P+"cop_torba_kelepcesi", cx0+T, cx1-T, cy1-18, cy1-10, cz1-18, cz1-3)
    # ---- ATMA bolmesi: AGIZ TAMAMEN ACIK (klape yok — robot kolun kovaya erisimi engellenmeyecek)
    #      yalniz kisa bir esik saci: agiz alt kenari (z -20) ile kova agzi arasindaki 40 mm olu bosluk
    #      koprulenir, cop arkaya/one kacmaz. Kova agzinin yalniz 20 mm on seridini orter.
    a, b, c, d = O3
    st.part(P+"atma_esik_saci", [(RT, 'poly', [(20.0, c+2.5), (100.0, cy1+11), (100.0, cy1+9.5), (20.0, c+1.0)],
                                 a-2, b+2, False)])
    for ad, xx in (("sol", a-3.5), ("sag", b+2)):
        st.part(P+"atma_esik_yan_"+ad, [(RT, 'poly', [(20.0, c+2.5), (100.0, cy1+11), (100.0, c+2.5)], xx, xx+T, False)])
    # ---- ELEKTRIK PANOSU: uc bolmesinin arka olu alani (catal -495'te bitiyor, arkasi bos)
    st.box(P+"pano_plakasi_2mm", 90.0, 610.0, UC[0]+20, UC[1]-30, zi, zi+2)
    st.box(P+"pano_plc", 110.0, 210.0, 1250.0, 1360.0, zi+2, zi+77)
    st.box(P+"pano_guc_kaynagi_24V", 230.0, 330.0, 1250.0, 1360.0, zi+2, zi+112)
    for i in range(2): st.box(P+"pano_surucu_%d" % (i+1), 350.0+i*90, 420.0+i*90, 1230.0, 1360.0, zi+2, zi+132)
    st.box(P+"pano_kontaktor", 110.0, 190.0, 1140.0, 1220.0, zi+2, zi+82)
    st.box(P+"pano_klemens_rayi", 210.0, 590.0, 1125.0, 1132.5, zi+2, zi+37)
    st.box(P+"pano_kablo_kanali", 210.0, 590.0, 1170.0, 1210.0, zi+2, zi+42)


def asm():
    st = Station(ROOT, "PRESS_v5"); st.load_dir(); print("kasa parca:", len(st.parts))
    O = lambda g: os.path.join(ARA, "_ortak", g, g + ".SLDASM")
    st.add_instance(O("PZP400_PRES"),     center_m=(0.349, 0.6165, -0.418))  # x29..669 y141,5..1091,5 z-818..-18
    st.add_instance(O("ROBOT_UCU_CATAL"), center_m=(0.200, 1.323, -0.260))   # yuva 1  x130..270, flans 1348..1360
    st.add_instance(O("ROBOT_UCU_PENCE"), center_m=(0.350, 1.265, -0.111))   # yuva 2  x300..400, flans 1348..1360
    st.add_instance(O("VANTUZ_D40"),      center_m=(0.500, 1.338, -0.100))   # yuva 3  x480..520, nipel 1346..1360
    for x in (0.200, 0.350, 0.500):
        st.add_instance(O("UC_DOCK_PLAKASI"), center_m=(x, 1.373, -0.140))   # ISO 9409 takim degistirici plakasi
    for ax, az in AYAK_YERI(W):                       # ORTAK: ayar ayagi (eski 4+4 yerel parca)
        st.add_instance(O("AYAK_AYAR_M12"), offset_mm=(ax, 0.0, az))
    for ad, x0, x1, y0, y1, acik, kapi, nm in PANEL:  # ORTAK: gizli mentese + bas-ac mandali
        for yy in nm: st.add_instance(O("MENTESE_GIZLI_34"), offset_mm=(x0+2.0, yy, 0.0))
        if kapi: st.add_instance(O("MANDAL_BAS_AC"), offset_mm=(x1-90.0, (y0+y1)/2-10.0, 0.0))
    st.assemble("PRESS_v5")


if __name__ == "__main__":
    faz = sys.argv[1]; sw.CloseAllDocuments(True)
    if faz == "kasa":
        st = Station(ROOT, "PRESS_v5")
        for f in os.listdir(st.pdir):
            if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
        kasa(st); print("PRESS v5 kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "parca":                       # ornek: python sw_press5.py parca "panel_atma|atma_"
        import re
        pat = re.compile(sys.argv[2]); st = Station(ROOT, "PRESS_v5"); n = [0]
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
