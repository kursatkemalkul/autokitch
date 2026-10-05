# -*- coding: utf-8 -*-
# STORE ÇAKIŞMA DÜZELTME · 2. tur
#  1) MOTOR_TAHRIK_GRUBU braketi inceltildi (grup derinliği 60 → 40) ve motorlar 12 mm içeri alındı → yan PU'ya girmiyor
#  2) Motor z −730 → −737 (çekmece arkası 700 ile arka sac 757,5 arasına tam oturur)
#  3) Kaset katı klapesinin gazlı amortisörleri kapların içindeydi → öne alındı (z −18…0)
#  4) Dikey kablo kanalı tavan PU'sunu deliyordu → y 200–1605'te bitiyor
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
ACIKLIK = ([("icecek_%d" % i, 66, 690, y, 124, 4.0) for i, y in enumerate((1484, 1354, 1224, 1094), 1)] +
           [("1L", 66, 690, 772, 316, 4.0)] +
           [("taze_%d" % i, 714, 1338, y, 99, 8.0) for i, y in enumerate((1509, 1404, 1299, 1194, 1089, 984, 879, 774), 1)] +
           [("donmus_1", 66, 690, 297, 94, 8.0), ("donmus_2", 66, 690, 197, 94, 8.0),
            ("donmus_3", 714, 1338, 297, 94, 8.0), ("donmus_4", 714, 1338, 197, 94, 8.0)])

def motor_incelt():
    """braket ve gövde z yönünde daralt: grup derinliği 40 mm (57,5 mm'lik arka boşluğa rahat sığar)"""
    kok = os.path.join(ORTAK, "MOTOR_TAHRIK_GRUBU"); st = Station(kok, "MOTOR_TAHRIK_GRUBU"); p = "MTG_"
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    st.cyl_z(p+"kasnak_D30_kayis", 0, 0, 15, -6, 6)
    st.box(p+"reduktor_govde_37x37x40", 8, 48, -18.5, 18.5, -18, 18)
    st.box(p+"motor_24V_37x37x80", 48, 128, -18.5, 18.5, -18, 18)
    st.box(p+"enkoder_kapagi", 128, 143, -15, 15, -15, 15)
    st.box(p+"M12_soket", 143, 158, -8, 8, -8, 8)
    st.box(p+"montaj_braketi_3mm", 0, 60, -25, -18.5, -18, 18)          # braket artık z ±18 (önce ±30)
    st.load_dir(); st.assemble("MOTOR_TAHRIK_GRUBU"); print("  motor grubu inceltildi (derinlik 40 mm)")

def kasa_parcalari():
    st = Station(ROOT, "STORE"); p = "STORE_"
    for f in os.listdir(st.pdir):
        if "klape_kaset_kati_gazli_amortisor" in f or f.startswith(p+"kablo_kanali_dikey"): os.remove(os.path.join(st.pdir, f))
    for i, xx in enumerate((84, 654), 1):                                # amortisörler önde, kapların dışında
        st.box(p+"klape_kaset_kati_gazli_amortisor_%d" % i, xx, xx+18, 436, 636, -18, 0)
    st.box(p+"kablo_kanali_dikey_40x25", 1290, 1330, 200, 1605, -752, -727)
    print("  amortisorler one alindi, kablo kanali kisaltildi")
    return st

def montaji_guncelle():
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(2)
    # motorları çıkar, yeni konumla ekle
    d.ClearSelection2(True); sil = 0
    for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        if c.Name2.startswith("MOTOR_TAHRIK_GRUBU"):
            d.Extension.SelectByID2(c.Name2 + "@STORE", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0); sil += 1
    if sil: d.Extension.DeleteSelection2(0)
    d.ClearSelection2(True)
    MTG = os.path.join(ORTAK, "MOTOR_TAHRIK_GRUBU", "MOTOR_TAHRIK_GRUBU.SLDASM")
    dd = sw.OpenDoc6(MTG, 2, 1, "", e, w); bb = [1e9]*3 + [-1e9]*3
    for cp in dd.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        g = cp.GetBox(False, False)
        for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
    c_m = [(bb[i]+bb[i+3])/2 for i in range(3)]; n = 0
    for ad, x0, x1, ya, h, kc in ACIKLIK:
        yr = ya + 3 + kc + 10
        if d.AddComponent5(MTG, 0, "", False, "", c_m[0] + (x0 + 18)*M, c_m[1] + (yr + 21)*M, c_m[2] - 737*M) is not None: n += 1
    sw.CloseDoc(dd.GetTitle)
    comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith("MOTOR_TAHRIK_GRUBU"): c.Select4(True, NUL_, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(2)
    print("  motor yeniden konumlandi: %d | STORE toplam: %d" % (n, d.GetComponentCount(True)))
    png(d, os.path.join(ROOT, "STORE_duzeltilmis.png"), "*Isometric", 1400, 830)
    print("  kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    motor_incelt(); kasa_parcalari(); montaji_guncelle()
    print("BITTI")
