# -*- coding: utf-8 -*-
# STORE v3: tum cekmeceler kizak baglantisi (0-600) + klape mentese baglantisi
#
# NOT: Station.assemble() her bileseni FixComponent yapar. Montaj her yeniden kuruldugunda
#      bu betik TEKRAR calistirilmalidir, aksi halde hicbir sey hareket etmez.
#
# KLAPE (10 Eyl 2026): mentese ekseni cephe duzlemine (y=160 / z=40) alindi. Klape kulagi artik
# CEYREK KERTIK (kulak koseinde Ø8,4 kesik) — eski SelectByRay yontemi bu yuzeyi tutturamiyor.
# Bunun yerine yuzey YARICAPINDAN bulunuyor: kesin ve tekrarlanabilir.
import os, time, math, pythoncom
from sw_lib import *
import sw_store_v3 as V
NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
def sec(d, ad, tur, mark=0, ekle=False): return d.Extension.SelectByID2(ad, tur, 0.0, 0.0, 0.0, ekle, mark, NUL_, 0)
def refd(d, kaynak, ofs):
    d.ClearSelection2(True); sec(d, kaynak, "PLANE")
    f = d.FeatureManager.InsertRefPlane(8, ofs*M, 0, 0, 0, 0); d.ClearSelection2(True); return f
def mate(d, a, b, tip, ust=0.0):
    d.ClearSelection2(True)
    if not sec(d, a, "PLANE", 1, False): return None
    if not sec(d, b, "PLANE", 1, True): return None
    h = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4, 0)
    m = d.AddMate5(tip, 2, False, 0.0, ust*M, 0.0, 0, 0, 0, 0, 0, False, False, 0, h)
    d.ClearSelection2(True); return m

def yapraklar(c, out):
    """bilesen agacinin YAPRAK (parca) bilesenlerini toplar"""
    ch = list(c.GetChildren)
    if ch:
        for k in ch: yapraklar(k, out)
    else: out.append(c)
    return out

def silindir_yuz(comp, r_mm, tol=0.05):
    """comp parca bilesenindeki r_mm yaricapli silindirik yuzu dondurur (montaj baglaminda)"""
    b = mcall(comp, "GetBody")
    if b is None: return None
    f = mcall(b, "GetFirstFace")
    while f is not None:
        s = mcall(f, "GetSurface")
        try:
            if s is not None and mcall(s, "IsCylinder"):
                p = list(s.CylinderParams)
                if abs(p[6]/M - r_mm) < tol: return f
        except Exception: pass
        f = mcall(f, "GetNextFace")
    return None

sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
d = sw.OpenDoc6(os.path.join(V.ROOT, "STORE_v3.SLDASM"), 2, 0, "", e, w); sw.FrameState = 2
# ZORUNLU: bilesenler LIGHTWEIGHT acilirsa Component2.GetBody() None doner ve mentese
# yuzeyi bulunamaz (klape es-merkez mate'i sessizce kurulmaz).
mcall(d, "ResolveAllLightWeightComponents", False)
mcall(d, "EditRebuild3"); time.sleep(3)
kok = d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True)
comps = list(kok.GetChildren)
# --- cekmeceler: 2 cakisik duzlem + 1 sinirli mesafe (0..600) ---
n = 0
for c in comps:
    if not c.Name2.startswith("CEKMECE3_"): continue
    ad = c.Name2 + "@STORE_v3"; t = c.Transform2.ArrayData; tx, ty = t[9]/M, t[10]/M
    d.ClearSelection2(True); sec(d, ad, "COMPONENT"); mcall(d, "UnfixComponent"); d.ClearSelection2(True)
    px = refd(d, "Right Plane", tx); py = refd(d, "Top Plane", ty)
    m1 = mate(d, px.Name, "Right Plane@" + ad, 0); m2 = mate(d, py.Name, "Top Plane@" + ad, 0)
    m3 = mate(d, "Front Plane", "Front Plane@" + ad, 5, 600.0)
    n += 1 if (m1 and m2 and m3) else 0
    print("  %-22s x=%6.1f y=%7.1f %s%s%s" % (c.Name2, tx, ty, "1" if m1 else "-", "1" if m2 else "-", "1" if m3 else "-"))
# --- klape: mentese kulagi Ø8,4 kertigi <-> mil Ø8 (es merkez) + eksenel kilit ---
mil = None
for c in comps:
    if "klape_mentese_mili" in c.Name2: mil = c; break
mily = silindir_yuz(mil, 4.0) if mil is not None else None
print("  mil bileseni=%s  yuz=%s" % (mil.Name2 if mil else "YOK", "OK" if mily else "YOK"))
for c in comps:
    if not c.Name2.startswith("KLAPE3_"): continue
    ad = c.Name2 + "@STORE_v3"; t = c.Transform2.ArrayData; x0 = t[9]/M
    d.ClearSelection2(True); sec(d, ad, "COMPONENT"); mcall(d, "UnfixComponent"); d.ClearSelection2(True)
    kulak = [k for k in yapraklar(c, []) if "mentese_kulagi" in k.Name2]
    m1 = None
    for k in kulak:
        ky = silindir_yuz(k, 4.2)
        if ky is None or mily is None: continue
        d.ClearSelection2(True)
        if not mcall(ky, "Select4", False, NUL_): continue
        if not mcall(mily, "Select4", True, NUL_): continue
        h = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4, 0)
        m1 = d.AddMate5(1, 0, False, 0.0, 0.0, 0.0, 0, 0, 0, 0, 0, False, False, 0, h)
        d.ClearSelection2(True)
        if m1: break
    px = refd(d, "Right Plane", x0)
    m2 = mate(d, px.Name, "Right Plane@" + ad, 0)
    # SINIRLI ACI 0..90: klape TAM 90 derecede durur (kasetler icin dumduz kot) ve daha fazla acilmaz
    d.ClearSelection2(True); m3 = None
    if sec(d, "Top Plane", "PLANE", 1, False) and sec(d, "Top Plane@" + ad, "PLANE", 1, True):
        h = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4, 0)
        # flip=True ZORUNLU: False ile klape KABIN ICINE donuyor (deneyle olculdu:
        #   flip=False -> klape z -296,5..40 (ters) · flip=True -> z 40..376,5 (dogru))
        m3 = d.AddMate5(6, 0, True, 0.0, 0.0, 0.0, 0, 0, 0.0, math.radians(90.0), 0.0, False, False, 0, h)
    d.ClearSelection2(True)
    print("  %-22s x=%6.1f kulak=%d  esmerkez=%s  eksenel=%s  aci0-90=%s"
          % (c.Name2, x0, len(kulak), "OK" if m1 else "HATA", "OK" if m2 else "HATA", "OK" if m3 else "HATA"))
mcall(d, "EditRebuild3"); time.sleep(3)
hr = [c.Name2 for c in d.ConfigurationManager.ActiveConfiguration.GetRootComponent3(True).GetChildren if not c.IsFixed]
print("  hareketli: %d" % len(hr))
e2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w2 = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
print("  kayit:", bool(d.Save3(1, e2, w2)))
