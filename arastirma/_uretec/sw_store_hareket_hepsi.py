# -*- coding: utf-8 -*-
# STORE: (1) TUM cekmeceler hareketli (kizak baglantisi 0-600 mm)
#        (2) sag moduldeki bos alan -> SOL KAPAKLA AYNI grup (KLAPE_KASET_KATI ikinci ornek) + raf/mil/amortisor
import os, time, pythoncom
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
ROOT = os.path.join(ARA, "1_STORE"); PD = os.path.join(ROOT, "parca")
GRP = os.path.join(ROOT, "alt_montaj", "KLAPE_KASET_KATI", "KLAPE_KASET_KATI.SLDASM")
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
DX = 648.0                      # sol modulden sag module kayma
YM, ZM, RM = 397.0, 0.0, 4.0

def sec(doc, ad, tur, mark=0, ekle=False):
    return doc.Extension.SelectByID2(ad, tur, 0.0, 0.0, 0.0, ekle, mark, NUL_, 0)

def ref_duzlem(doc, kaynak, ofset):
    doc.ClearSelection2(True); sec(doc, kaynak, "PLANE")
    f = doc.FeatureManager.InsertRefPlane(8, ofset*M, 0, 0, 0, 0)
    doc.ClearSelection2(True); return f

def mate(doc, a, b, tip, ust=0.0):
    doc.ClearSelection2(True)
    if not sec(doc, a, "PLANE", 1, False): return None
    if not sec(doc, b, "PLANE", 1, True): return None
    h = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    m = doc.AddMate5(tip, 2, False, 0.0, ust*M, 0.0, 0, 0, 0, 0, 0, False, False, 0, h)
    doc.ClearSelection2(True); return m

def sag_kapak(d):
    """sag modul: raf + mil + amortisor + KLAPE_KASET_KATI 2. ornek"""
    st = Station(ROOT, "STORE"); p = "STORE_klape_kaset_kati_sag_"
    st.box(p+"raf", 62+DX, 690+DX, 403, 404, -758, 0)
    st.part(p+"pivot_mil", [(RT, 'circ', (-ZM, YM, RM), 59+DX, 697+DX, False)])
    for i, xx in enumerate((68+DX, 672+DX), 1): st.box(p+"gazli_amortisor_%d" % i, xx, xx+12, 436, 636, -18, 0)
    yeni = [yol for yol, _ in st.parts]
    acik = []
    for yol in yeni + [GRP]:
        tur = 2 if yol.lower().endswith(".sldasm") else 1
        e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
        dd = sw.OpenDoc6(yol, tur, 1, "", e, w); acik.append(dd.GetTitle)
        if tur == 1: bb = bbox_of(dd)
        else:
            bb = [1e9]*3 + [-1e9]*3
            for cp in dd.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
                g = cp.GetBox(False, False)
                for i in range(3): bb[i] = min(bb[i], g[i]); bb[i+3] = max(bb[i+3], g[i+3])
        c = [(bb[i]+bb[i+3])/2 for i in range(3)]
        if yol == GRP: c[0] += DX*M
        if d.AddComponent5(yol, 0, "", False, "", c[0], c[1], c[2]) is None: print("   eklenemedi:", yol)
    for t_ in acik:
        try: sw.CloseDoc(t_)
        except Exception: pass
    d.ClearSelection2(True)
    for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren:
        if c.Name2.startswith("STORE_klape_kaset_kati_sag_"): c.Select4(True, NUL, False)
    mcall(d, "FixComponent"); d.ClearSelection2(True); mcall(d, "EditRebuild3"); time.sleep(2)
    # mentese: sag mil <-> 2. klape kulagi
    o1 = d.Extension.SelectByRay((400+DX)*M, 0.390, -0.003, 0.0, 1.0, 0.0, 0.002, 2, False, 1, 0)
    o2 = d.Extension.SelectByRay((64+DX)*M, 0.390, -0.003, 0.0, 1.0, 0.0, 0.002, 2, True, 1, 0)
    h = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4, 0)
    m1 = d.AddMate5(1, 0, False, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, False, False, 0, h); d.ClearSelection2(True)
    px = ref_duzlem(d, "Right Plane", DX)
    m2 = mate(d, px.Name, "Right Plane@KLAPE_KASET_KATI-2@STORE", 0)
    print("  sag kapak: secim=%s/%s esmerkez=%s cakisik=%s" % (o1, o2, "OK" if m1 else "HATA", "OK" if m2 else "HATA"))

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    d = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    mcall(d, "EditRebuild3"); time.sleep(2)
    sag_kapak(d)
    # --- tum cekmeceleri hareketli yap ---
    sabitler = [c for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren
                if c.Name2.startswith("CEKMECE_") and c.IsFixed]
    print("  hareketlendirilecek cekmece:", len(sabitler))
    for c in sabitler:
        ad = c.Name2 + "@STORE"; t = c.Transform2.ArrayData
        tx, ty = t[9]/M, t[10]/M
        d.ClearSelection2(True); sec(d, ad, "COMPONENT"); mcall(d, "UnfixComponent"); d.ClearSelection2(True)
        px = ref_duzlem(d, "Right Plane", tx); py = ref_duzlem(d, "Top Plane", ty)
        m1 = mate(d, px.Name, "Right Plane@" + ad, 0)
        m2 = mate(d, py.Name, "Top Plane@" + ad, 0)
        m3 = mate(d, "Front Plane", "Front Plane@" + ad, 5, 600.0)
        print("   %-18s x=%6.1f y=%7.1f  %s%s%s" % (c.Name2, tx, ty, "1" if m1 else "-", "1" if m2 else "-", "1" if m3 else "-"))
    mcall(d, "EditRebuild3"); time.sleep(3)
    hr = [c.Name2 for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren if not c.IsFixed]
    print("  hareketli toplam: %d" % len(hr))
    e2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    print("  kayit:", bool(d.Save3(1, e2, w2)))
