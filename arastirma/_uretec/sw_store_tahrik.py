# -*- coding: utf-8 -*-
# ANA MODELE EKLE: STORE'daki 17 çekmecenin tahrik sistemi (motor + kasa rayları + kayış + kablo)
# Alan kullanımı: çekmece 700 derin → arkada 57 mm; motor (37 kalın) tam oraya oturuyor, boşa alan yok.
# Parçalar ORTAK ve ÖRNEKLENİR (tek parça, 17/34 kopya): RAY_DIS_PROFIL · KAYIS_GT3 · MOTOR_TAHRIK_GRUBU · KABLO_24V
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); ORTAK = os.path.join(ARA, "_ortak")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
MTG = os.path.join(ORTAK, "MOTOR_TAHRIK_GRUBU", "MOTOR_TAHRIK_GRUBU.SLDASM")
# (ad, x0, x1, y_alt, yükseklik, çekmece taban kotu kc)
ACIKLIK = ([("icecek_%d" % i, 66, 690, y, 124, 4.0) for i, y in enumerate((1484, 1354, 1224, 1094), 1)] +
           [("1L", 66, 690, 772, 316, 4.0)] +
           [("taze_%d" % i, 714, 1338, y, 99, 8.0) for i, y in enumerate((1509, 1404, 1299, 1194, 1089, 984, 879, 774), 1)] +
           [("donmus_1", 66, 690, 297, 94, 8.0), ("donmus_2", 66, 690, 197, 94, 8.0),
            ("donmus_3", 714, 1338, 297, 94, 8.0), ("donmus_4", 714, 1338, 197, 94, 8.0)])

def ortak_parcalar():
    """tek kez üretilir, 17/34 kez örneklenir"""
    for ad, kur in (("RAY_DIS_PROFIL", lambda st: st.box("RAY_DIS_PROFIL_14x49x660", 0, 14, 0, 49, -660, 0)),
                    ("KAYIS_GT3_6mm",  lambda st: st.box("KAYIS_GT3_6x3x650", 0, 6, 0, 3, -690, -40)),
                    ("KABLO_24V_D5",   lambda st: st.cyl_z("KABLO_24V_D5x120", 0, 0, 2.5, -120, 0))):
        kok = os.path.join(ORTAK, ad)
        if os.path.exists(os.path.join(kok, ad + ".SLDASM")): continue
        st = Station(kok, ad); kur(st); st.assemble(ad); print("  ortak parca:", ad)

def store_ekle():
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    print("  STORE acildi, mevcut bilesen:", d.GetComponentCount(True))
    acik = []
    def merkez(yol):
        """referans belgeyi AÇIK BIRAK (AddComponent5 yüklü belge ister) ve bbox merkezini döndür"""
        dd = sw.OpenDoc6(yol, 2, 1, "", e, w); acik.append(dd.GetTitle)
        bb = [1e9]*3 + [-1e9]*3
        for cp in dd.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
            g = cp.GetBox(False, False)
            for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
        return [(bb[i]+bb[i+3])/2 for i in range(3)]
    RAY = os.path.join(ORTAK, "RAY_DIS_PROFIL", "RAY_DIS_PROFIL.SLDASM")
    KAY = os.path.join(ORTAK, "KAYIS_GT3_6mm", "KAYIS_GT3_6mm.SLDASM")
    KBL = os.path.join(ORTAK, "KABLO_24V_D5", "KABLO_24V_D5.SLDASM")
    c_ray, c_kay, c_kbl, c_mtg = merkez(RAY), merkez(KAY), merkez(KBL), merkez(MTG)
    n = 0
    for ad, x0, x1, ya, h, kc in ACIKLIK:
        yr = ya + 3 + kc + 10                                  # ray ekseni (kasa kotu)
        for xs in (x0 + 3 - 14, x1 - 3):                       # sol ve sağ kasa rayı (çekmece rayının dışında)
            if d.AddComponent5(RAY, 0, "", False, "", c_ray[0] + xs*M, c_ray[1] + yr*M, c_ray[2]) is not None: n += 1
        if d.AddComponent5(KAY, 0, "", False, "", c_kay[0] + (x0 + 6)*M, c_kay[1] + (yr + 20)*M, c_kay[2]) is not None: n += 1
        if d.AddComponent5(MTG, 0, "", False, "", c_mtg[0] + (x0 + 6)*M, c_mtg[1] + (yr + 21)*M, c_mtg[2] - 690*M) is not None: n += 1
        if d.AddComponent5(KBL, 0, "", False, "", c_kbl[0] + (x0 + 40)*M, c_kbl[1] + (yr + 21)*M, c_kbl[2] - 700*M) is not None: n += 1
    for t_ in acik:
        try: sw.CloseDoc(t_)
        except Exception: pass
    comps = list(d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    d.ClearSelection2(True)
    for c in comps:
        if c.Name2.startswith(("RAY_DIS_PROFIL", "KAYIS_GT3", "MOTOR_TAHRIK_GRUBU", "KABLO_24V")): c.Select4(True, NUL_, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(3)
    print("  eklenen: %d | STORE toplam bilesen: %d" % (n, d.GetComponentCount(True)))
    for nm in ("LimitDistance1", "LimitDistance2", "LimitDistance3", "LimitDistance4"):
        p2 = d.Parameter("D1@" + nm)
        if p2 is not None: p2.SystemValue = 0.45
    mcall(d, "EditRebuild3"); time.sleep(2)
    png(d, os.path.join(ROOT, "STORE_tahrik.png"), "*Isometric")
    print("  kayit:", saveas(d, os.path.join(ROOT, "STORE.SLDASM")))

if __name__ == "__main__":
    sw.CloseAllDocuments(True); ortak_parcalar(); store_ekle()
    print("BITTI — 17 motor + 34 kasa rayi + 17 kayis + 17 kablo ana modelde")
