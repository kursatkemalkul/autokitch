# -*- coding: utf-8 -*-
# 2 · PRESS v3 — PZP-400 katalog ölçüsüyle (64×80×95, 170 kg, 3,5 kW/220 V) + ALTINDA robot tepsi & uç istasyonu
# Dikey (zeminden cm):
#   0–12    plint / ayaklar
#   12–107  PZP-400 PRESİ 95   → ZEMİNDE (170 kg ağırlık merkezi aşağıda, devrilme emniyeti)
#   107–117 TEPSİ RAFI 10      → 3 tepsi Ø32, 3 cm aralık
#   117–137 UÇ İSTASYONU 20    → pençe · çatal · yedek; dock plakaları üstte, uçlar aşağı asılı, robot üstten takar
#   137–181 ÇÖP KUTUSU 44      → DİKDÖRTGEN 32×52×42 = 70 L, kızakla öne çekilir, poşet kelepçeli
#   181–193 KOL BOŞLUĞU 12     → robot atığı kovanın üstünden bırakır
#   193–197 üst şerit 4
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "2_PRESS"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
W = 700.0
Z_PRES, Z_TEPSI, Z_UC, Z_KOVA, Z_KOL, Z_UST = 120.0, 1070.0, 1170.0, 1370.0, 1810.0, 1930.0   # pres zeminde
TEPSI = os.path.join(ORTAK, "TEPSI_D320", "TEPSI_D320.SLDASM")

def pzp400():
    """PZP-400 pizza açma presi — katalog: 640 × 800 × 950, 170 kg, 3,5 kW, 220 V
       Yerel: kaide sol-ön-alt köşe (0,0,0); +Y yukarı, −Z arkaya"""
    kok = os.path.join(ORTAK, "PZP400_PRES")
    if os.path.exists(os.path.join(kok, "PZP400_PRES.SLDASM")): print("  PZP-400 zaten var"); return kok
    st = Station(kok, "PZP400_PRES"); p = "PZP_"
    st.box(p+"kaide_govde_640x800x520", 0, 640, 0, 520, -800, 0)                 # motor + rezistans + şanzıman
    st.box(p+"kaide_ust_tabla", 0, 640, 520, 540, -800, 0)
    st.cyl_y(p+"alt_plaka_isitmali_D340", 320, -400, 170, 540, 560)              # tepsi bunun üstünde bekler
    for i, xx in enumerate((90, 550), 1): st.box(p+"kolon_80x80_%d" % i, xx-40, xx+40, 540, 800, -520, -440)
    st.box(p+"ust_kafa_640x260x150", 0, 640, 800, 950, -560, -400)
    st.cyl_y(p+"ust_plaka_isitmali_D290", 320, -400, 145, 760, 790)              # basma plakası (aşağı iner)
    st.cyl_y(p+"piston_mili_D40", 320, -400, 20, 790, 800)
    st.box(p+"kontrol_paneli", 430, 620, 560, 700, -60, -20)                     # ön sağda, eleman kullanır
    st.box(p+"motor_3.5kW", 60, 300, 60, 300, -700, -460)
    for i, (xx, zz) in enumerate(((60, -60), (540, -60), (60, -700), (540, -700)), 1): st.box(p+"ayak_%d" % i, xx, xx+40, 0, 0.1, zz-40, zz)
    st.assemble("PZP400_PRES"); print("  PZP400_PRES: 640x800x950 (katalog)"); return kok

def robot_uclari():
    """robot uçları: PENÇE (2 parmak) ve ÇATAL (tepsi/kap taşır) — ISO 9409-1-50 flanş + konum pimleri
       Yerel: flanş üst yüzü merkezi (0,0,0); uç aşağı doğru"""
    for ad, kur in (
        ("ROBOT_UCU_PENCE", lambda st, p: (
            st.cyl_y(p+"ISO9409_flans_D50", 0, 0, 25, -12, 0),
            st.box(p+"govde_100x80x60", -50, 50, -70, -12, -40, 40),
            st.box(p+"parmak_sol", -46, -34, -190, -70, -18, 18),
            st.box(p+"parmak_sag", 34, 46, -190, -70, -18, 18),
            st.box(p+"pnomatik_baglanti", -18, 18, -70, -50, 40, 58))),
        ("ROBOT_UCU_CATAL", lambda st, p: (
            st.cyl_y(p+"ISO9409_flans_D50", 0, 0, 25, -12, 0),
            st.box(p+"sirt_140x60x50", -70, 70, -62, -12, -25, 25),
            st.box(p+"lama_sol_16x12", -58, -42, -74, -62, -25, 475),
            st.box(p+"lama_sag_16x12", 42, 58, -74, -62, -25, 475),
            st.box(p+"tirnak_ucu_sol", -58, -42, -74, -62, 455, 475),
            st.box(p+"tirnak_ucu_sag", 42, 58, -74, -62, 455, 475))),
        ("UC_DOCK_PLAKASI", lambda st, p: (
            st.box(p+"taban_plakasi_130x8x200", -65, 65, 0, 8, -200, 0),          # platformun ALTINA vidalanır
            st.cyl_y(p+"konum_pimi_D12_1", -40, -60, 6, -18, 0),                   # pimler AŞAĞI bakar (uç alttan geçer)
            st.cyl_y(p+"konum_pimi_D12_2", 40, -60, 6, -18, 0),
            st.box(p+"kilit_dili", -20, 20, -20, 0, -40, -20),
            st.box(p+"varlik_sensoru", 44, 62, -22, -6, -150, -120)))):
        kok = os.path.join(ORTAK, ad)
        if os.path.exists(os.path.join(kok, ad + ".SLDASM")): continue
        st = Station(kok, ad); kur(st, ad.split("_")[-1][:3] + "_"); st.assemble(ad); print("  %s hazir" % ad)

def cop_kutusu():
    """DİKDÖRTGEN çöp kutusu 320 × 520 × 420 = 70 L · paslanmaz 1,0 · poşet kelepçesi · kızakta öne çekilir"""
    kok = os.path.join(ORTAK, "COP_KUTUSU_70L")
    if os.path.exists(os.path.join(kok, "COP_KUTUSU_70L.SLDASM")): print("  cop kutusu zaten var"); return kok
    st = Station(kok, "COP_KUTUSU_70L"); p = "COP_"
    st.prism_z(p+"govde_U_1.0", [(0, 420), (0, 0), (320, 0), (320, 420), (319, 420), (319, 1), (1, 1), (1, 420)], -520, 0)
    st.box(p+"arka_duvar_1.0", 0, 320, 0, 420, -520, -519)
    st.box(p+"on_duvar_1.0", 0, 320, 0, 420, -1, 0)
    st.box(p+"poset_kelepcesi_cerceve", -6, 326, 420, 432, -526, 6)
    st.box(p+"kizak_sol", -12, 0, 40, 85, -500, 0); st.box(p+"kizak_sag", 320, 332, 40, 85, -500, 0)
    st.assemble("COP_KUTUSU_70L"); print("  COP_KUTUSU_70L: 320x520x420 = 70 L"); return kok

def kasa(st):
    p = "PRESS_"
    shell(st, p, W, "feet"); sove_L(st, p, W, Y0, H)
    # ön yüz: pres ağzı açık (robot tepsiyi koyar/alır) · tepsi+uç bandı açık · kova kapağı · kol boşluğu · üst şerit
    st.box(p+"panel_pres_yan_sol", 30, 60, Z_PRES, Z_TEPSI, ZF0, ZF1)
    st.box(p+"panel_pres_yan_sag", 640, 670, Z_PRES, Z_TEPSI, ZF0, ZF1)
    st.box(p+"panel_tepsi_uc_cerceve", 30, 670, Z_TEPSI, Z_KOVA, ZF0, ZF1, [(45, 655, Z_TEPSI+15, Z_KOVA-15, ZF0-1, ZF1+1)])
    door_C(st, p+"kova_kapagi_", 30, 350, Z_KOVA, Z_KOL)
    st.box(p+"panel_kova_sag", 350, 670, Z_KOVA, Z_KOL, ZF0, ZF1)
    st.box(p+"panel_kol_bosluk_cerceve", 30, 670, Z_KOL, Z_UST, ZF0, ZF1, [(60, 640, Z_KOL+10, Z_UST-10, ZF0-1, ZF1+1)])
    st.box(p+"panel_ust_serit", 30, 670, Z_UST, H, ZF0, ZF1)
    # tepsi rafları (107–117): 3 kat, 3 cm aralık
    for i, yy in enumerate((Z_TEPSI+8, Z_TEPSI+38, Z_TEPSI+68), 1):
        st.box(p+"tepsi_raf_%d" % i, 190, 510, yy, yy+2, -700, -60)
    st.box(p+"tepsi_raf_tasiyici_sol", 180, 190, Z_TEPSI+5, Z_UC, -700, -60)
    st.box(p+"tepsi_raf_tasiyici_sag", 510, 520, Z_TEPSI+5, Z_UC, -700, -60)
    # uç istasyonu tavanı (137): dock plakaları buraya vidalanır, uçlar aşağı asılı
    st.box(p+"uc_ist_tavan_saci", 40, 660, Z_UC+190, Z_UC+200, -780, -20)
    st.box(p+"uc_ist_yan_sol", 40, 50, Z_UC, Z_UC+200, -780, -20)
    st.box(p+"uc_ist_yan_sag", 650, 660, Z_UC, Z_UC+200, -780, -20)
    # kova rafı
    st.box(p+"kova_rafi", 30, 360, Z_KOVA, Z_KOVA+10, -700, -20)
    # pano (kova sağındaki boş yarıda)
    for ad, x0, x1, y0, y1, z0, z1 in (
        ("pano_plaka", 390, 630, 1400, 1780, -350, -348), ("pano_plc", 400, 500, 1680, 1760, -348, -273),
        ("pano_guc_kaynagi_24V", 520, 620, 1680, 1760, -348, -238), ("pano_surucu_1", 400, 470, 1540, 1660, -348, -228),
        ("pano_surucu_2", 490, 560, 1540, 1660, -348, -228), ("pano_kontaktor_1", 580, 625, 1560, 1640, -348, -268),
        ("pano_klemens_rayi", 400, 620, 1480, 1488, -348, -313), ("pano_kablo_kanali", 400, 620, 1410, 1450, -348, -308)):
        st.box(p + ad, x0, x1, y0, y1, z0, z1)

def yerlestir(st, pzp, cop):
    st.add_instance(os.path.join(pzp, "PZP400_PRES.SLDASM"), offset_mm=(30, Z_PRES+1.5, -14))          # ZEMİNDE, alt sacın üstünde (12–107)
    st.add_instance(os.path.join(cop, "COP_KUTUSU_70L.SLDASM"), offset_mm=(45, Z_KOVA+10, -60))
    for i, yy in enumerate((Z_TEPSI+10, Z_TEPSI+40, Z_TEPSI+70), 1):                                    # 3 tepsi rafta
        st.add_instance(TEPSI, offset_mm=(350, yy, -380))
    st.add_instance(TEPSI, offset_mm=(350, Z_PRES+560, -420))                                          # preste bekleyen tepsi
    for xx in (120, 350, 580):                                                                          # 3 dock: pençe · çatal · yedek
        st.add_instance(os.path.join(ORTAK, "UC_DOCK_PLAKASI", "UC_DOCK_PLAKASI.SLDASM"), offset_mm=(xx, Z_UC+180, -120))     # dock plakası tavan sacının ALTINA vidalı
    st.add_instance(os.path.join(ORTAK, "ROBOT_UCU_PENCE", "ROBOT_UCU_PENCE.SLDASM"), offset_mm=(120, Z_UC+172, -180))
    st.add_instance(os.path.join(ORTAK, "ROBOT_UCU_CATAL", "ROBOT_UCU_CATAL.SLDASM"), offset_mm=(350, Z_UC+172, -640))
    return st.assemble("PRESS")

if __name__ == "__main__":
    import sys
    faz = sys.argv[1] if len(sys.argv) > 1 else "hepsi"
    sw.CloseAllDocuments(True)
    if faz in ("ortak", "hepsi"): pzp400(); robot_uclari(); cop_kutusu()
    if faz == "kasa":
        st = Station(ROOT, "PRESS")
        for f in os.listdir(st.pdir):
            if f.lower().endswith((".sldprt", ".sldasm")): os.remove(os.path.join(st.pdir, f))
        kasa(st); print("  kasa parca uretildi:", len(st.parts)); st.exit_sw()
    elif faz == "asm":
        st = Station(ROOT, "PRESS"); st.load_dir(); print("  kasa parca:", len(st.parts))
        yol = yerlestir(st, os.path.join(ORTAK, "PZP400_PRES"), os.path.join(ORTAK, "COP_KUTUSU_70L"))
        e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
        d = sw.OpenDoc6(yol, 2, 1, "", e, w); sw.FrameState = 2
        png(d, os.path.join(ROOT, "PRESS_v3_iso.png"), "*Isometric", 1400, 830)
        png(d, os.path.join(ROOT, "PRESS_v3_on.png"), "*Front", 1400, 830)
        print("  PRESS bilesen:", d.GetComponentCount(True))
