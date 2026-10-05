# -*- coding: utf-8 -*-
# STORE TEMİZLİK: (1) çekmece/klape ön yüzlerinden KULP GİRİNTİSİ kaldırılır → dümdüz yüzey
#                 (2) kulp_cukuru parçaları montajdan çıkarılır
#                 (3) SolidWorks girişim (interference) analizi → iç içe geçen parçalar raporlanır
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); CEKD = os.path.join(ROOT, "cekmece"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
W_CEK = 618.0
TIP = {"icecek": 118.0, "1L": 310.0, "taze": 93.0, "donmus": 94.0}

def duz_on_yuz(tip, h):
    """çekmece ön sandviçini kulpsuz (dümdüz) yeniden üret: iç sac 1,0 + PU 37,5 + dış sac 1,5"""
    st = Station(os.path.join(CEKD, "CEKMECE_" + tip), "CEKMECE_" + tip); p = "CEK_%s_" % tip
    for f in os.listdir(st.pdir):
        if "on_ic_sac" in f or "on_pu" in f or "on_dis_sac" in f or "kulp_cukuru" in f: os.remove(os.path.join(st.pdir, f))
    st.box(p+"on_ic_sac_1.0", 0, W_CEK, 0, h, 0, 1)
    st.box(p+"on_pu_37.5", 0, W_CEK, 0, h, 1, 38.5)
    st.box(p+"on_dis_sac_1.5", 0, W_CEK, 0, h, 38.5, 40)
    print("  %s: on yuz duz (kulp yok)" % tip)

def klape_duz(st):
    """STORE −18 kaset katı klapesi: kulpsuz"""
    p = "STORE_klape_kaset_kati_"; a, b, c, d = 69.0, 687.0, 406.0, 684.0
    for f in os.listdir(st.pdir):
        if f.startswith(p) and ("on_ic_sac" in f or "on_pu" in f or "on_dis_sac" in f or "kulp_cukuru" in f): os.remove(os.path.join(st.pdir, f))
    st.box(p+"on_ic_sac", a, b, c, d, 0, 1); st.box(p+"on_pu", a, b, c, d, 1, 38.5); st.box(p+"on_dis_sac", a, b, c, d, 38.5, 40)
    print("  kaset katı klapesi: duz")

def montajlari_yenile():
    """çekmece alt montajlarını içerikleriyle yeniden kur (kulp_cukuru bileşeni düşer)"""
    import sw_motor_gorunur as mg
    for tip in ("icecek", "1L"): mg.yuvali_tepsi(tip)
    for tip, h, kc in (("taze", 93.0, 8.0), ("donmus", 94.0, 8.0)): mg.hamur_tepsi(tip, h, kc)

def kulp_bilesenlerini_sil(d):
    d.ClearSelection2(True); n = 0
    for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        if "kulp_cukuru" in c.Name2:
            d.Extension.SelectByID2(c.Name2 + "@STORE", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0); n += 1
    if n: d.Extension.DeleteSelection2(0)
    d.ClearSelection2(True); print("  montajdan silinen kulp parcasi:", n)

def girisim_analizi(d):
    """SolidWorks girişim analizi: iç içe geçen bileşen çiftleri + hacimleri"""
    mgr = mcall(d.Extension, "GetInterferenceDetectionManager")
    mgr.TreatCoincidenceAsInterference = False        # yüzey teması girişim sayılmasın
    mgr.IncludeMultibodyPartInterferences = True
    mgr.MakeInterferingPartsTransparent = False
    mgr.UseTransform = False if hasattr(mgr, "UseTransform") else None
    liste = mcall(mgr, "GetInterferences")
    say = mcall(mgr, "GetInterferenceCount") if liste is None else len(liste)
    print("  GIRISIM SAYISI:", say)
    kayit = []
    if liste:
        for it in liste:
            try:
                hac = it.Volume * 1e9                    # m³ → mm³
                cmp_ = mcall(it, "GetComponents")
                adlar = [c.Name2 for c in cmp_] if cmp_ else []
                kayit.append((hac, adlar))
            except Exception as e: kayit.append((0.0, ["okunamadi: %s" % str(e)[:40]]))
    kayit.sort(key=lambda x: -x[0])
    for hac, adlar in kayit[:40]:
        print("   %10.0f mm3  %s" % (hac, " ↔ ".join(a.rsplit('-',1)[0] for a in adlar)))
    return kayit

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    for tip, h in TIP.items(): duz_on_yuz(tip, h)
    st = Station(ROOT, "STORE"); klape_duz(st)
    montajlari_yenile()
    # STORE'u aç, kulp bileşenlerini sil, girişim analizi
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(3)
    kulp_bilesenlerini_sil(d)
    print("  bilesen:", d.GetComponentCount(True))
    girisim_analizi(d)
    for nm in ("LimitDistance1", "LimitDistance2", "LimitDistance3", "LimitDistance4"):
        p2 = d.Parameter("D1@" + nm)
        if p2 is not None: p2.SystemValue = 0.0
    mcall(d, "EditRebuild3"); time.sleep(1)
    png(d, os.path.join(ROOT, "STORE_duz_yuzey.png"), "*Isometric", 1400, 830)
    print("  kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))
