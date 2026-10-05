# -*- coding: utf-8 -*-
# STORE ÇAKIŞMA DÜZELTMELERİ (tarama bulguları):
#  1) Evaporatör + fanlar çekmecelerin içindeydi → tavan/taban bandına alındı (+3: y 1612–1666 · −18: y 124–178)
#  2) Orta dikey bölme yatay ayırıcının içinden geçiyordu → 766'dan başlatıldı
#  3) Kasa rayları PU/bölme içindeydi → açıklık kenarına alındı (x0+1 · x1−15)
#  4) Motor grubu çekmecenin arkasına 30 mm daha itildi (z −730) · kayış uzatıldı
#  5) Yatay kablo kanalı PU tavanın içindeydi → teknik bölmeye (y 1690–1730) alındı
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
ZI = -757.5
ACIKLIK = ([("icecek_%d" % i, 66, 690, y, 124, 4.0) for i, y in enumerate((1484, 1354, 1224, 1094), 1)] +
           [("1L", 66, 690, 772, 316, 4.0)] +
           [("taze_%d" % i, 714, 1338, y, 99, 8.0) for i, y in enumerate((1509, 1404, 1299, 1194, 1089, 984, 879, 774), 1)] +
           [("donmus_1", 66, 690, 297, 94, 8.0), ("donmus_2", 66, 690, 197, 94, 8.0),
            ("donmus_3", 714, 1338, 297, 94, 8.0), ("donmus_4", 714, 1338, 197, 94, 8.0)])

def parcalari_duzelt():
    st = Station(ROOT, "STORE"); p = "STORE_"
    # 1) evaporatör + fan: tavan (+3) ve taban (−18) bandına
    for f in os.listdir(st.pdir):
        if f.startswith(p+"evaporator") or f.startswith(p+"evap_fan") or f.startswith(p+"orta_bolme") or f.startswith(p+"kablo_kanali_yatay"):
            os.remove(os.path.join(st.pdir, f))
    st.box(p+"evaporator_1_ust_bant", 200, 1200, 1612, 1666, ZI, ZI+95)      # +3 hücre tavanı altı
    st.cyl_z(p+"evap_fan_1", 700, 1639, 25, ZI+95, ZI+135)
    st.box(p+"evaporator_2_alt_bant", 200, 1200, 124, 178, ZI, ZI+95)        # −18 hücre tabanı üstü
    st.cyl_z(p+"evap_fan_2", 700, 151, 25, ZI+95, ZI+135)
    # 2) orta dikey bölme: yatay ayırıcının üstünden başlar (766 → 1610)
    st.box(p+"orta_bolme_sac_sol", 690, 691, 766, 1610, ZI, 0)
    st.box(p+"orta_bolme_pu", 691, 713, 766, 1610, ZI, 0)
    st.box(p+"orta_bolme_sac_sag", 713, 714, 766, 1610, ZI, 0)
    # 5) yatay kablo kanalı: teknik bölmeye
    st.box(p+"kablo_kanali_yatay_40x25", 700, 1330, 1690, 1730, -752, -727)
    print("  kasa parcalari duzeltildi")
    return st

def montaji_guncelle(st):
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(2)
    comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    var = set(c.Name2.rsplit("-", 1)[0] for c in comps)
    # eski evaporator/fan bileşenleri montajda kalmışsa sil
    d.ClearSelection2(True); sil = 0
    for c in comps:
        k = c.Name2.rsplit("-", 1)[0]
        if k in (
            "STORE_evaporator_1", "STORE_evaporator_2") or (k.startswith("RAY_DIS_PROFIL") or k.startswith("MOTOR_TAHRIK_GRUBU") or k.startswith("KAYIS_GT3")):
            d.Extension.SelectByID2(c.Name2 + "@STORE", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0); sil += 1
    if sil: d.Extension.DeleteSelection2(0)
    d.ClearSelection2(True); print("  montajdan cikarilan (eski evaporator + ray/motor/kayis):", sil)
    # yeni evaporatör parçalarını ekle
    acik = []; n = 0
    for ad in ("evaporator_1_ust_bant", "evap_fan_1", "evaporator_2_alt_bant", "evap_fan_2"):
        yol = os.path.join(st.pdir, "STORE_" + ad + ".SLDPRT")
        if "STORE_" + ad in var: continue
        dd = sw.OpenDoc6(yol, 1, 1, "", e, w); acik.append(dd.GetTitle); bb = bbox_of(dd)
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        if d.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2]) is not None: n += 1
    # ray + motor + kayış: DÜZELTİLMİŞ konumlarla yeniden ekle
    def merkez(yol):
        dd = sw.OpenDoc6(yol, 2, 1, "", e, w); acik.append(dd.GetTitle); bb = [1e9]*3 + [-1e9]*3
        for cp in dd.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
            g = cp.GetBox(False, False)
            for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
        return [(bb[i]+bb[i+3])/2 for i in range(3)]
    RAY = os.path.join(ORTAK, "RAY_DIS_PROFIL", "RAY_DIS_PROFIL.SLDASM")
    KAY = os.path.join(ORTAK, "KAYIS_GT3_6mm", "KAYIS_GT3_6mm.SLDASM")
    MTG = os.path.join(ORTAK, "MOTOR_TAHRIK_GRUBU", "MOTOR_TAHRIK_GRUBU.SLDASM")
    c_ray, c_kay, c_mtg = merkez(RAY), merkez(KAY), merkez(MTG)
    for ad, x0, x1, ya, h, kc in ACIKLIK:
        yr = ya + 3 + kc + 10
        for xs in (x0 + 1, x1 - 15):                                  # açıklık kenarında, PU'nun içinde değil
            if d.AddComponent5(RAY, 0, "", False, "", c_ray[0] + xs*M, c_ray[1] + yr*M, c_ray[2]) is not None: n += 1
        if d.AddComponent5(KAY, 0, "", False, "", c_kay[0] + (x0 + 6)*M, c_kay[1] + (yr + 20)*M, c_kay[2] - 40*M) is not None: n += 1
        if d.AddComponent5(MTG, 0, "", False, "", c_mtg[0] + (x0 + 6)*M, c_mtg[1] + (yr + 21)*M, c_mtg[2] - 730*M) is not None: n += 1
    for t_ in acik:
        try: sw.CloseDoc(t_)
        except Exception: pass
    comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith(("STORE_evaporator", "STORE_evap_fan", "RAY_DIS_PROFIL", "KAYIS_GT3", "MOTOR_TAHRIK_GRUBU")): c.Select4(True, NUL_, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(2)
    print("  eklenen: %d | STORE toplam: %d" % (n, d.GetComponentCount(True)))
    png(d, os.path.join(ROOT, "STORE_duzeltilmis.png"), "*Isometric", 1400, 830)
    print("  kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    st = parcalari_duzelt(); montaji_guncelle(st)
    print("BITTI")
