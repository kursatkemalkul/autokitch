# -*- coding: utf-8 -*-
# STORE ÇAKIŞMA DÜZELTME · 3. tur
#  1) Evaporatörler yalıtımın içindeydi → ARKA DUVARA ince panel (44 mm) olarak alındı; çekmece arkasındaki 57,5 mm boşluğun ortası
#     (motorlar modül kenarlarında, evaporatör ortada — çakışma yok). Fanlar evaporatör yüzeyinde, aynı derinlikte.
#  2) Pano kutuları üst üste binmişti (iki ayrı turda eklenmiş) → eski klemens + PLC giriş modülü yeni yerlere taşındı
#  3) Kaset klapesi amortisörleri kapların önündeydi → modül kenarlarındaki boş şeritlere alındı (12 mm genişlik)
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)

def parcalar():
    st = Station(ROOT, "STORE"); p = "STORE_"
    sil = ("evaporator_1_ust_bant", "evap_fan_1", "evaporator_2_alt_bant", "evap_fan_2",
           "PLC_giris_modulu_16_kanal", "klemens_kutusu_150x100x60", "klape_kaset_kati_gazli_amortisor")
    for f in os.listdir(st.pdir):
        if any(k in f for k in sil): os.remove(os.path.join(st.pdir, f))
    # 1) arka duvar evaporatörleri (44 derin: z −756…−712) — çekmece 700'de bitiyor, 12 mm hava payı
    st.box(p+"evaporator_1_arka_+3", 250, 1150, 800, 1560, -756, -712)
    st.box(p+"evaporator_2_arka_-18", 250, 1150, 220, 660, -756, -712)
    for i, (xx, yy) in enumerate(((450, 1500), (900, 1500)), 1): st.cyl_z(p+"evap_fan_ust_%d" % i, xx, yy, 60, -752, -714)
    for i, (xx, yy) in enumerate(((450, 600), (900, 600)), 1): st.cyl_z(p+"evap_fan_alt_%d" % i, xx, yy, 60, -752, -714)
    # 2) pano: klemens + giriş modülü teknik bölmede boş yere
    st.box(p+"klemens_kutusu_150x100x60", 560, 690, 1830, 1930, -700, -640)
    st.box(p+"PLC_giris_modulu_16_kanal", 700, 870, 1830, 1930, -700, -660)
    # 3) amortisörler: modül kenarındaki boş şeritlerde (kapların dışında)
    for i, xx in enumerate((68, 672), 1): st.box(p+"klape_kaset_kati_gazli_amortisor_%d" % i, xx, xx+12, 436, 636, -18, 0)
    print("  parcalar yenilendi")
    return st

def montaj(st):
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(2)
    # silinen adlara ait bileşenleri montajdan çıkar
    d.ClearSelection2(True); sil = 0
    for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        k = c.Name2.rsplit("-", 1)[0]
        if k in ("STORE_evaporator_1_ust_bant", "STORE_evap_fan_1", "STORE_evaporator_2_alt_bant", "STORE_evap_fan_2"):
            d.Extension.SelectByID2(c.Name2 + "@STORE", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0); sil += 1
    if sil: d.Extension.DeleteSelection2(0)
    d.ClearSelection2(True)
    var = set(c.Name2.rsplit("-", 1)[0] for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    acik = []; n = 0
    for ad in ("evaporator_1_arka_+3", "evaporator_2_arka_-18", "evap_fan_ust_1", "evap_fan_ust_2", "evap_fan_alt_1", "evap_fan_alt_2"):
        yol = os.path.join(st.pdir, "STORE_" + ad + ".SLDPRT")
        if "STORE_" + ad in var or not os.path.exists(yol): continue
        dd = sw.OpenDoc6(yol, 1, 1, "", e, w); acik.append(dd.GetTitle); bb = bbox_of(dd)
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        if d.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2]) is not None: n += 1
    for t_ in acik:
        try: sw.CloseDoc(t_)
        except Exception: pass
    comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith(("STORE_evaporator", "STORE_evap_fan")): c.Select4(True, NUL_, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(2)
    for i in range(1, 9):
        p2 = d.Parameter("D1@LimitDistance%d" % i)
        if p2 is not None: p2.SystemValue = 0.0
    mcall(d, "EditRebuild3"); time.sleep(1)
    print("  eklenen: %d | bilesen: %d" % (n, d.GetComponentCount(True)))
    png(d, os.path.join(ROOT, "STORE_son.png"), "*Isometric", 1400, 830)
    print("  kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    montaj(parcalar()); print("BITTI")
