# -*- coding: utf-8 -*-
# AUTOKITCH — 5 · PACK v2 (kutu_istasyonu_teknik_v4): ALT MONTAJLI — VANTUZ_D40 ×6, KUTU_BLANK ×1, KUTU_KATLI ×1, ortak TEPSI_D320 ×1 + kasa
# zonlar (zeminden cm): plint 12 · PANO 18 · step+vakum 15 · BOYUNDURUK 10 (36×72 profil) · KALIP 5 (plaka 3 mm 66×79, pencere 32,5) · YÜKLEME 44 · ŞARJÖR 84 (525 blank 40×76) · üst pay 9 = 197
# çevrim: plunger 48 yukarı → 6 vantuz en alt kutuya yapışır → 44 iner → kalıptan geçer (katlanır) → plakaya oturur → pide → kapak → robot alır
import sys, os
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "5_PACK"); ORTAK = os.path.join(ARA, "_ortak")
W = 700.0

def vantuz():
    """körüklü vakum vantuzu Ø40 + M8 nipel — yerel: emme yüzeyi merkezi (0,0,0), gövde +Y"""
    st = Station(os.path.join(ORTAK, "VANTUZ_D40"), "VANTUZ_D40"); p = "VNT_"
    st.cyl_y(p+"koruk_dudak_D40", 0, 0, 20, 0, 18); st.cyl_y(p+"govde_D24", 0, 0, 12, 18, 30); st.cyl_y(p+"nipel_M8", 0, 0, 4, 30, 44)
    st.assemble("VANTUZ_D40"); print("  VANTUZ merkez (mm): %.1f %.1f %.1f" % tuple(v/M for v in st.center()))

def kutu_blank():
    """AÇILMIŞ KUTU (blank) 40×76 — E-dalga 1,6 mm, 115 g; kırım çizgileri kalıpta katlanır. Yerel: sol-arka köşe (0,0), düzlem yatay"""
    st = Station(os.path.join(ORTAK, "KUTU_BLANK_40x76"), "KUTU_BLANK_40x76"); p = "BLANK_"
    st.prism_y(p+"karton_E_dalga_1.6", [(0, 0), (400, 0), (400, -760), (0, -760)], 0, 1.6)
    st.assemble("KUTU_BLANK_40x76"); print("  BLANK merkez (mm): %.1f %.1f %.1f" % tuple(v/M for v in st.center()))

def kutu_katli():
    """KATLANMIŞ KUTU 32×32×4 (kapak açık, arkada dik) — taban + 4 duvar + kapak. Yerel: taban sol-arka köşe (0,0,0)"""
    st = Station(os.path.join(ORTAK, "KUTU_KATLI_32x32"), "KUTU_KATLI_32x32"); p = "KUTU_"
    st.box(p+"taban_320x320", 0, 320, 0, 1.6, -320, 0)
    st.box(p+"duvar_on", 0, 320, 1.6, 41.6, -1.6, 0); st.box(p+"duvar_arka", 0, 320, 1.6, 41.6, -320, -318.4)
    st.box(p+"duvar_sol", 0, 1.6, 1.6, 41.6, -320, 0); st.box(p+"duvar_sag", 318.4, 320, 1.6, 41.6, -320, 0)
    st.box(p+"kapak_320x320_dik", 0, 320, 41.6, 361.6, -321.6, -320)      # menteşe arka duvarda, açık (dik) konumda
    st.box(p+"on_dil", 0, 320, 41.6, 81.6, 0, 1.6)
    st.assemble("KUTU_KATLI_32x32"); print("  KUTU_KATLI merkez (mm): %.1f %.1f %.1f" % tuple(v/M for v in st.center()))

def kasa(st):
    p = "PACK_"
    shell(st, p, W, "plint"); sove_L(st, p, W, Y0, H)
    st.box(p+"plint_izgara_paneli", 60, 640, 30, 110, 18.5, 20, [(80+i*40, 100+i*40, 40, 100, 17, 21) for i in range(14)])
    # PANO 18 (120–300): PLC I/O · step sürücü · 2 motor sürücü · 3 servo sürücü · 24 V PSU
    door_C(st, p+"pano_kapagi_", 30, 670, Y0, 300)
    st.box(p+"pano_plakasi", 50, 650, 130, 290, -250, -248); zb = -248
    st.box(p+"pano_plc_IO", 60, 180, 180, 280, zb, zb+75); st.box(p+"pano_psu_24V", 200, 300, 180, 280, zb, zb+110)
    st.box(p+"pano_step_surucu", 320, 370, 180, 280, zb, zb+120)
    for i in range(2): st.box(p+"pano_motor_surucu_%d" % (i+1), 390+i*60, 435+i*60, 180, 280, zb, zb+100)
    for i in range(3): st.box(p+"pano_servo_surucu_%d" % (i+1), 520+i*45, 555+i*45, 180, 280, zb, zb+60)
    st.box(p+"pano_klemens_rayi", 60, 640, 140, 147.5, zb, zb+35)
    # STEP + VAKUM 15 (300–450): NEMA 23 (3 N·m) + bilyalı vida 1605 + 2 lineer ray Ø16 · diyafram pompa 30 L/dk + 1 L tank + 2 selenoid + vakum sensörü
    st.box(p+"panel_mekanizma", 30, 670, 300, 600, ZF0, ZF1)
    st.box(p+"step_motor_NEMA23_3Nm", 322, 379, 300, 380, -430, -373); st.cyl_y(p+"bilyali_vida_1605", 350, -400, 8, 380, 900); st.box(p+"vida_somunu_1605", 330, 370, 480, 520, -420, -380)
    for i, xx in enumerate((150, 550), 1): st.cyl_y(p+"lineer_ray_D16_%d" % i, xx, -400, 8, 300, 900); st.box(p+"lineer_rulman_%d" % i, xx-15, xx+15, 470, 530, -415, -385)
    st.box(p+"vakum_pompasi_24V_30Ldk", 440, 580, 300, 440, -700, -560); st.cyl_y(p+"vakum_tanki_1L_D100", 150, -650, 50, 300, 440)
    for i, nm in enumerate(("taban", "kapak"), 1): st.box(p+"vakum_selenoid_%s" % nm, 220+(i-1)*50, 260+(i-1)*50, 320, 370, -680, -620)
    st.box(p+"vakum_sensoru", 300, 340, 320, 350, -680, -640); st.cyl_z(p+"vakum_hortumu_D8", 500, 420, 4, -560, -420)
    # BOYUNDURUK 10 (450–550): alu profil 36×72 + plunger plakası 31,6×31,6×2 (vantuzlar alt montaj)
    st.box(p+"boyunduruk_profil_36x72", 120, 580, 470, 506, -436, -364); st.box(p+"plunger_plakasi_316x316x2", 192, 508, 506, 508, -558, -242)
    st.box(p+"kapak_postu_dikey", 330, 370, 508, 700, -420, -380)          # 2 kapak vantuzunu taşır
    # KALIP 5 (550–600): paslanmaz plaka 3 mm 66×79 · pencere 32,5 · kalıp duvarı 4,5 derin · 4 köşe plowu · yan duvar 5 alçak
    st.box(p+"kalip_plakasi_3mm_66x79", 20, 680, 597, 600, -790, 0, [(187.5, 512.5, 596, 601, -562.5, -237.5)])
    # kalıp duvarı: pencere çevresinde 4 parça (yan duvarlar 5 mm alçak → önce tırnak, sonra duvar kıvrılır)
    st.box(p+"kalip_duvari_arka", 185, 515, 552, 597, -565, -562.5); st.box(p+"kalip_duvari_on", 185, 515, 552, 597, -237.5, -235)
    st.box(p+"kalip_duvari_sol", 185, 187.5, 552, 592, -565, -235); st.box(p+"kalip_duvari_sag", 512.5, 515, 552, 592, -565, -235)
    for i, (xx, zz) in enumerate(((187.5, -562.5), (512.5, -562.5), (187.5, -237.5), (512.5, -237.5)), 1): st.box(p+"kose_plowu_%d" % i, xx-10, xx+10, 552, 597, zz-10, zz+10)
    st.box(p+"orta_ray_yarikli", 330, 370, 597, 600, -790, -570)
    # YÜKLEME 44 (600–1040): kapak kolu U Ø8 + redüktörlü 24 V motor + 2 switch · 3 flap parmağı (servo) · robot klapesi önde
    st.box(p+"panel_kutulama", 30, 670, 600, 1040, ZF0, ZF1, [(60, 640, 620, 1020, ZF0-1, ZF1+1)])
    st.cyl_z(p+"kapak_kolu_U_yatay_D8", 130, 980, 4, -600, -520); st.box(p+"kapak_kolu_dikey_1", 126, 134, 640, 980, -604, -596); st.box(p+"kapak_kolu_dikey_2", 566, 574, 640, 980, -604, -596)
    st.box(p+"kapak_kolu_motoru_24V_5Nm", 40, 120, 610, 690, -640, -560)
    for i in range(2): st.box(p+"kapak_switch_%d" % (i+1), 100+i*450, 130+i*450, 700+i*200, 720+i*200, -640, -620)
    for i, xx in enumerate((150, 350, 550), 1): st.box(p+"flap_servo_25kgcm_%d" % i, xx-25, xx+25, 640, 700, -230, -170); st.box(p+"flap_parmagi_%d" % i, xx-4, xx+4, 700, 760, -215, -185)
    # ŞARJÖR 84 (1040–1880): 2 L kılavuz (iç 40) · alt tutucu ray 2×76 + 4 köşe parmağı · 525 blank yığını · foto sensör ×3
    door_C(st, p+"sarjor_kapisi_", 30, 670, 1040, 1950)
    for i, (xx, sx) in enumerate(((140, 1), (560, -1)), 1): st.prism_y(p+"sarjor_L_kilavuz_%d" % i, [(xx, -800), (xx+sx*10, -800), (xx+sx*10, -798), (xx+sx*2, -798), (xx+sx*2, -20), (xx, -20)], 1040, 1880)
    for i, zz in enumerate((-790, -30), 1): st.box(p+"sarjor_alt_tutucu_ray_%d" % i, 150, 550, 1040, 1044, zz-10, zz+10)
    for i, (xx, zz) in enumerate(((155, -785), (545, -785), (155, -35), (545, -35)), 1): st.box(p+"sarjor_kose_parmagi_%d" % i, xx-8, xx+8, 1044, 1060, zz-8, zz+8)
    st.box(p+"blank_yigini_525_adet", 150, 550, 1044, 1880, -790, -30)
    for i, yy in enumerate((1100, 1400, 1860), 1): st.box(p+"sarjor_foto_sensoru_%d" % i, 120, 140, yy, yy+20, -420, -400)
    st.box(p+"panel_ust_pay", 30, 670, 1950, H, ZF0, ZF1)

if __name__ == "__main__":
    faz = sys.argv[1]
    if faz == "alt":
        sw.CloseAllDocuments(True); vantuz(); kutu_blank(); kutu_katli(); Station(ROOT, "x").exit_sw()
    elif faz == "kasa":
        sw.CloseAllDocuments(True); st = Station(ROOT, "PACK"); kasa(st); print("kasa parca:", len(st.parts)); st.exit_sw()
    elif faz == "asm":
        sw.CloseAllDocuments(True); st = Station(ROOT, "PACK"); st.load_dir(); print("kasa parca yuklendi:", len(st.parts))
        V = os.path.join(ORTAK, "VANTUZ_D40", "VANTUZ_D40.SLDASM")
        for xx, zz in ((230, -520), (470, -520), (230, -280), (470, -280)):     # plunger plakasında 4 taban vantuzu (emme yüzü y=508)
            st.add_instance(V, offset_mm=(xx, 508, zz))
        for xx in (330, 370):                                                    # kapak postunda 2 vantuz
            st.add_instance(V, offset_mm=(xx, 700, -400))
        st.add_instance(os.path.join(ORTAK, "KUTU_KATLI_32x32", "KUTU_KATLI_32x32.SLDASM"), offset_mm=(190, 600, -240))   # kalıp plakasında hazır kutu
        st.add_instance(os.path.join(ORTAK, "KUTU_BLANK_40x76", "KUTU_BLANK_40x76.SLDASM"), offset_mm=(150, 1042, -30))   # şarjörün en alt blank'i
        st.add_instance(os.path.join(ORTAK, "TEPSI_D320", "TEPSI_D320.SLDASM"), offset_mm=(350, 620, -400))               # robotun getirdiği tepsi (yükleme)
        st.assemble("PACK")
        e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w_ = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        d = sw.OpenDoc6(os.path.join(ROOT, "PACK.SLDASM"), 2, 1, "", e, w_)
        for cpt in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
            if cpt.Name2.startswith(("VANTUZ", "KUTU", "TEPSI")): t = cpt.Transform2.ArrayData; print("  %-20s x=%4.0f y=%5.0f z=%5.0f" % (cpt.Name2, t[9]/M, t[10]/M, t[11]/M))
        d.ShowNamedView2("*Isometric", 7); mcall(d, "ViewZoomtofit2"); sw.FrameState = 2
