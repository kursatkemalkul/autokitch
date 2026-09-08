# -*- coding: utf-8 -*-
# AUTOKITCH — 3 · TOPPING v2 (ist3_topping_detay_v25/v27): ALT MONTAJLI — KAP ×12, L_RAF_CIFTI ×14, SOKET_MOTOR ×6 + kasa → TOPPING.SLDASM (7 Eyl 2026)
# fazlar: alt → kasa → asm (her biri temiz SolidWorks oturumu)
# dikey (cm): soğutma 0–20 (plint) · ALT sıra 2 20–47 · ALT sıra 1 47–74 · kat 3 74–115 · kat 2 115–156 · kat 1 156–197 (boşluk 14 + kap 27)
# plan: sol kanal 20 (evaporatör) · kaplar x 27/43 · sağ kanal 20 (hava dönüş + kablo) · arka duvar 10 (motor + pano) · klape önde
import sys, os
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "3_TOPPING"); ALT = os.path.join(ROOT, "alt_montaj")
W, PU, PUB, YB = 700.0, 40.0, 20.0, 200.0
ZI = ZK + T_DIS + PUB + T_IC                     # iç arka sac önü −797,5
LAYOUT = [("kat1", 1710, [(270, "kasar_A"), (430, "sucuk")]), ("kat2", 1300, [(270, "kasar_B"), (430, "kavurma")]), ("kat3", 890, [(270, "kiyma"), (430, "kusbasi")]),
          ("alt1", 480, [(115, "kasar_yedek_1"), (272, "kasar_yedek_2"), (428, "kasar_yedek_3"), (585, "kasar_yedek_4")]),
          ("alt2", 210, [(428, "cozulme_kiyma"), (585, "cozulme_kusbasi")])]
RAF_X = {"kat": (270, 430), "alt": (115, 272, 428, 585)}

def kap():
    """KAP 14×68×24 Picnic tipi — yerel: kap merkezi x=0, raf üstü y=0 (kızak 0..20, gövde 20..260), z −720..−20"""
    st = Station(os.path.join(ALT, "KAP_14x68x24"), "KAP_14x68x24"); p = "KAP_"; yb, yt = 20, 260
    st.prism_z(p+"PC_govde_5mm", [(-70, yt-5), (70, yt-5), (70, yt-105), (38, yb+10), (-38, yb+10), (-70, yt-105)], -700, -20)
    st.box(p+"PC_kapak_gecmeli", -70, 70, yt-5, yt, -700, -20)
    st.cyl_z(p+"helezon_POM_D70", 0, yb+48, 35, -700, -100); st.cyl_z(p+"helezon_topuz_D50", 0, yb+48, 25, -720, -700)
    st.cyl_z(p+"tarak_mili_D12", 0, yb+150, 6, -700, -40); st.cyl_z(p+"tarak_topuz_D30", 0, yb+150, 15, -720, -700)
    st.box(p+"kizak_sol_30x20", -65, -35, 0, 20, -700, -20); st.box(p+"kizak_sag_30x20", 35, 65, 0, 20, -700, -20)
    st.box(p+"on_cekme_dudagi", -70, 70, yt-15, yt, -20, -5); st.box(p+"agiz_kapagi_PC", -30, 30, yb+10, yb+15, -90, -25)
    st.assemble("KAP_14x68x24"); c = st.center(); print("  KAP merkez (mm): %.1f %.1f %.1f" % (c[0]/M, c[1]/M, c[2]/M)); return c

def raf_cifti():
    """kabin L raf çifti 20×8×2 (dik kenar dışta) + ön çapraz çubuk — yerel: kap merkezi x=0, raf üstü y=0"""
    st = Station(os.path.join(ALT, "L_RAF_CIFTI"), "L_RAF_CIFTI"); p = "LRAF_"
    for side, sx in (("sol", -1), ("sag", 1)):
        xe = sx*54; st.prism_z(p+side+"_20x8x2", [(xe, 0), (xe+sx*2, 0), (xe+sx*2, 20), (xe-sx*6, 20), (xe-sx*6, 18), (xe, 18)], ZI, -20)
    st.box(p+"capraz_cubuk_8x8", -58, 58, 22, 30, -60, -52)
    st.assemble("L_RAF_CIFTI"); c = st.center(); print("  L_RAF merkez (mm): %.1f %.1f %.1f" % (c[0]/M, c[1]/M, c[2]/M)); return c

def soket_motor():
    """arka duvar: kap başına 2 yaylı soket + 2 yassı step motor 57×57×40 — yerel: kap merkezi x=0, raf üstü y=0"""
    st = Station(os.path.join(ALT, "SOKET_MOTOR"), "SOKET_MOTOR"); p = "SM_"; yb = 20
    st.cyl_z(p+"soket_helezon_yayli", 0, yb+48, 15, -740, -720); st.cyl_z(p+"soket_tarak_yayli", 0, yb+150, 15, -740, -720)
    st.box(p+"motor_helezon_57x57x40", -28, 28, yb+20, yb+76, -780, -740); st.box(p+"motor_tarak_57x57x40", -28, 28, yb+122, yb+178, -780, -740)
    st.assemble("SOKET_MOTOR"); c = st.center(); print("  SOKET_MOTOR merkez (mm): %.1f %.1f %.1f" % (c[0]/M, c[1]/M, c[2]/M)); return c

def kasa(st):
    p = "TOPPING_"
    shell(st, p, W, "plint", y0=YB); sove_L(st, p, W, YB, H)
    xi0, xi1, zi = insulated_cell(st, p, W, YB+42.5, 1968.5-T_IC, PU, pu_back=PUB, y0=YB, top_pu=False)
    st.cyl_z(p+"sog_kompresor_yatik_D100", 200, 105, 50, -600, -400); st.box(p+"sog_kondenser", 300, 600, 30, 180, -300, -240); st.cyl_z(p+"sog_kondenser_fan_D140", 450, 105, 70, -240, -200)
    st.box(p+"plint_izgara_paneli", 60, 640, 40, 170, 18.5, 20, [(80+i*40, 100+i*40, 50, 160, 17, 21) for i in range(14)])
    st.box(p+"evaporator_sol_kanal", xi0+5, xi0+130, 400, 1500, -600, -200)
    for i, yy in enumerate((550, 1250), 1): st.box(p+"evap_fan_%d" % i, xi0+130, xi0+160, yy-70, yy+70, -470, -330)
    st.box(p+"sag_kanal_kablo_kanali", xi1-45, xi1-5, YB+50, 1900, -700, -660); st.box(p+"sag_kanal_hava_donus_izgarasi", xi1-160, xi1-50, 300, 1500, -20, -18)
    st.box(p+"arka_duvar_pano_plakasi", 100, 600, 300, 700, -778, -776); st.box(p+"arka_duvar_pano_plc", 120, 220, 560, 670, -776, -736)
    st.box(p+"arka_duvar_pano_guc_kaynagi", 240, 340, 560, 670, -776, -736)
    for i in range(6): st.box(p+"arka_duvar_pano_surucu_%d" % (i+1), 120+i*80, 170+i*80, 330, 530, -776, -736)
    st.box(p+"arka_duvar_kapak_saci", xi0, xi1, YB+42.5, 1960, -722, -720)
    for zone, yr, kaps in LAYOUT:          # kapak açma pimi Ø8 yalnız katlarda (v27)
        if zone.startswith("kat"):
            for j, xc in enumerate(RAF_X["kat"], 1): st.cyl_z(p+zone+"_kapak_pimi_D8_%d" % j, xc+30, yr+34, 4, -60, -40)
    for nm, y0, y1 in (("kat1", 1560, 1950), ("kat2", 1150, 1560), ("kat3", 740, 1150), ("alt1", 460, 740), ("alt2", YB, 460)): door_C(st, p+"klape_"+nm+"_", 30, 670, y0, y1, hinge="bottom")
    st.box(p+"panel_ust_serit", 30, 670, 1950, H, ZF0, ZF1)

if __name__ == "__main__":
    faz = sys.argv[1]
    if faz == "alt":
        sw.CloseAllDocuments(True); kap(); raf_cifti(); soket_motor(); Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        sw.CloseAllDocuments(True); st = Station(ROOT, "TOPPING"); kasa(st); print("kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "asm":
        sw.CloseAllDocuments(True); st = Station(ROOT, "TOPPING"); st.load_dir(); print("kasa parca yuklendi:", len(st.parts))
        for zone, yr, kaps in LAYOUT:
            for xc in (RAF_X["kat"] if zone.startswith("kat") else RAF_X["alt"]):
                st.add_instance(os.path.join(ALT, "L_RAF_CIFTI", "L_RAF_CIFTI.SLDASM"), offset_mm=(xc, yr, 0))
                if zone.startswith("kat"): st.add_instance(os.path.join(ALT, "SOKET_MOTOR", "SOKET_MOTOR.SLDASM"), offset_mm=(xc, yr, 0))
            for xc, nm in kaps: st.add_instance(os.path.join(ALT, "KAP_14x68x24", "KAP_14x68x24.SLDASM"), offset_mm=(xc, yr, 0))
        st.assemble("TOPPING")
        e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w_ = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        d = sw.OpenDoc6(os.path.join(ROOT, "TOPPING.SLDASM"), 2, 1, "", e, w_)
        for cpt in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
            if cpt.Name2.startswith(("KAP", "L_RAF", "SOKET")): t = cpt.Transform2.ArrayData; print("  %-16s x=%4.0f y=%5.0f z=%3.0f" % (cpt.Name2, t[9]/M, t[10]/M, t[11]/M))
        d.ShowNamedView2("*Isometric", 7); mcall(d, "ViewZoomtofit2"); sw.FrameState = 2                      # 2 = maximize (1 = minimize idi)
