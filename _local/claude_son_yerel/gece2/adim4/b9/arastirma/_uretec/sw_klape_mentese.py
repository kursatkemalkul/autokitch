# -*- coding: utf-8 -*-
# STORE kaset kati KLAPESI: 3 on yuz parcasi tek alt montaja alinir + gercek mentese baglantisi
#   pivot mil kutu yerine Ø8 SILINDIR (x 59..697, y 397, z 0)
#   klape uzerinde 2 mentese kulagi Ø12 / delik Ø8,4 (x 60..76 ve 680..696)
#   mate: es merkezli (mil <-> kulak) + cakisik (Right Plane <-> Right Plane) -> yalniz X ekseninde doner
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); PD = os.path.join(ROOT, "parca")
GRP = os.path.join(ROOT, "alt_montaj", "KLAPE_KASET_KATI")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
YM, ZM, RM = 397.0, 0.0, 4.0                     # mentese ekseni + mil yaricapi
ON = ("STORE_klape_kaset_kati_on_dis_sac_bukme_1.5", "STORE_klape_kaset_kati_on_pu_37.5", "STORE_klape_kaset_kati_on_ic_sac_1.0")
KULAK = "STORE_klape_kaset_kati_mentese_kulagi"
MIL = "STORE_klape_kaset_kati_pivot_mil"

def parcalar():
    st = Station(ROOT, "STORE")
    for f in (MIL + ".SLDPRT",):
        p = os.path.join(PD, f)
        if os.path.exists(p): os.remove(p)
    st.part(MIL, [(RT, 'circ', (-ZM, YM, RM), 59.0, 697.0, False)])                       # Ø8 mil, kasaya sabit
    st.part(KULAK, [(RT, 'circ', (-ZM, YM, 6.0), 60.0, 76.0, False),                      # kulak 1 Ø12
                    (RT, 'circ', (-ZM, YM, 6.0), 680.0, 696.0, False),                    # kulak 2
                    (RT, 'circ', (-ZM, YM, 4.2), 58.0, 78.0, True),                       # delik Ø8,4
                    (RT, 'circ', (-ZM, YM, 4.2), 678.0, 698.0, True)])
    print("  mil + mentese kulagi uretildi")

def grup():
    """3 on yuz parcasi + mentese kulagi -> KLAPE_KASET_KATI.SLDASM"""
    os.makedirs(GRP, exist_ok=True)
    sw.NewDocument(TPL_ASM, 0, 0, 0); asm = sw.ActiveDoc
    for ad in ON + (KULAK,):
        yol = os.path.join(PD, ad + ".SLDPRT")
        e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
        d = sw.OpenDoc6(yol, 1, 1, "", e, w); bb = bbox_of(d)
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        if asm.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2]) is None: raise RuntimeError("eklenemedi " + ad)
        sw.CloseDoc(d.GetTitle)
    comps = list(asm.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren)
    asm.ClearSelection2(True)
    for c in comps: c.Select4(True, NUL, False)
    mcall(asm, "FixComponent"); asm.ClearSelection2(True)
    yol = os.path.join(GRP, "KLAPE_KASET_KATI.SLDASM")
    print("  grup kayit:", saveas(asm, yol), "| parca:", len(comps))
    sw.CloseDoc(asm.GetTitle); return yol

def store(grup_yolu):
    e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(2)
    # 1) eski on yuz + eski mil bilesenlerini cikar
    d.ClearSelection2(True); n = 0
    for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        if c.Name2.rsplit("-", 1)[0] in ON + (MIL,):
            d.Extension.SelectByID2(c.Name2 + "@STORE", "COMPONENT", 0.0, 0.0, 0.0, True, 0, NUL_, 0); n += 1
    if n: d.Extension.DeleteSelection2(0)
    d.ClearSelection2(True); print("  cikarilan eski bilesen:", n)
    # 2) yeni mil (sabit) + klape grubu (serbest)
    acik = []
    for yol, tur in ((os.path.join(PD, MIL + ".SLDPRT"), 1), (grup_yolu, 2)):
        dd = sw.OpenDoc6(yol, tur, 1, "", e, w); acik.append(dd.GetTitle)
        if tur == 1: bb = bbox_of(dd)
        else:
            bb = [1e9]*3 + [-1e9]*3
            for cp in dd.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
                g = cp.GetBox(False, False)
                for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        if d.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2]) is None: raise RuntimeError("eklenemedi " + yol)
    for t_ in acik:
        try: sw.CloseDoc(t_)
        except Exception: pass
    d.ClearSelection2(True)
    for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        if c.Name2.startswith(MIL): c.Select4(True, NUL, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True)
    mcall(d, "EditRebuild3"); time.sleep(2)
    # 3) mate: es merkezli (mil <-> kulak) + cakisik (Right Plane)
    def ray(x, y, z, ekle, mark):
        return d.Extension.SelectByRay(x*M, y*M, z*M, 0.0, 1.0, 0.0, 0.002, 2, ekle, mark, 0)
    ok1 = ray(400.0, 390.0, -3.0, False, 1)          # mil yuzeyi (kulaklarin disinda)
    ok2 = ray(64.0, 390.0, -3.0, True, 1)            # kulak dis yuzeyi
    print("  yuzey secimi: mil=%s kulak=%s" % (ok1, ok2))
    h = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4, 0)
    m1 = d.AddMate5(1, 0, False, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, False, False, 0, h)   # 1 = es merkezli
    print("  es merkezli mate:", "OK" if m1 is not None else "BASARISIZ", "hata", h.value)
    d.ClearSelection2(True)
    gr = "KLAPE_KASET_KATI-1@STORE"
    d.Extension.SelectByID2("Right Plane", "PLANE", 0.0, 0.0, 0.0, False, 1, NUL_, 0)
    d.Extension.SelectByID2("Right Plane@" + gr, "PLANE", 0.0, 0.0, 0.0, True, 1, NUL_, 0)
    h2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4, 0)
    m2 = d.AddMate5(0, 0, False, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, False, False, 0, h2)  # 0 = cakisik
    print("  cakisik mate:", "OK" if m2 is not None else "BASARISIZ", "hata", h2.value)
    d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(2)
    hr = [c.Name2 for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren if not c.IsFixed]
    print("  hareketli bilesenler:", hr)
    e2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    print("  STORE kayit:", bool(d.Save3(1, e2, w2)))
    return d

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    parcalar(); g = grup(); sw.CloseAllDocuments(True); store(g)
    print("BITTI")
