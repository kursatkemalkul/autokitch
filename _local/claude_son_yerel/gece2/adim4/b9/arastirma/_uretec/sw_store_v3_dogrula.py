# -*- coding: utf-8 -*-
# STORE v3 — YENI PARCALARIN GERCEKTEN DOGRU URETILDIGINI OLCER (varsayim yok).
#  · delikli hizalama saci: yuz sayisi = 6 + delik + bukum bacaklari
#  · plenum ayirici saci: yuz sayisi = 6 + 4 x yarik  (yariklarin acildiginin kaniti)
#  · klape mentese kulagi: Ø8,4 kertigi olusmus mu (silindirik yuz var mi)
#  · klape 90 derece kinematigi: supurme hacmi sabit parcalara giriyor mu (matematik)
import os, sys, glob, math, pythoncom
from sw_lib import *
import sw_store_v3 as V

def ac(yol):
    e = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0); w = VARIANT(pythoncom.VT_BYREF|pythoncom.VT_I4,0)
    return sw.OpenDoc6(yol, 1, 0, "", e, w)

def olc(yol):
    d = ac(yol)
    if d is None: return None
    yuz = sum(mcall(b, "GetFaceCount") for b in d.GetBodies2(0, True))
    sil = 0
    for b in d.GetBodies2(0, True):
        f = mcall(b, "GetFirstFace")
        while f is not None:
            s = mcall(f, "GetSurface")
            try:
                if s is not None and mcall(s, "IsCylinder"): sil += 1
            except Exception: pass
            f = mcall(f, "GetNextFace")
    bb = bbox_of(d); sw.CloseDoc(d.GetTitle)
    return yuz, sil, [v/M for v in bb]

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    P = os.path.join(V.ROOT, "parca")
    print("== DELIKLI HIZALAMA SACI (delik sayisi = silindirik yuz sayisi) ==")
    for tip, bek in (("1L", 42), ("icecek", 63)):
        c = glob.glob(os.path.join(V.CEKD, "CEKMECE3_%s" % tip, "parca", "*hizalama_saci*.SLDPRT"))
        if not c: print("  %-8s DOSYA YOK" % tip); continue
        yuz, sil, bb = olc(c[0])
        print("  %-8s yuz=%3d  silindirik=%3d (beklenen %d)  %s" % (tip, yuz, sil, bek, "OK" if sil == bek else "EKSIK"))
    print("== PLENUM AYIRICI SACI (yarik sayisi = 4 x yarik -> dik yuz) ==")
    for f in sorted(glob.glob(os.path.join(P, "*plenum_ayirici*.SLDPRT"))):
        yuz, sil, bb = olc(f)
        yar = (yuz - 6) / 4.0
        print("  %-34s yuz=%3d -> %.0f yarik  z %.1f..%.1f" % (os.path.basename(f)[:34], yuz, yar, bb[2], bb[5]))
    print("== KLAPE MENTESE KULAGI (Ø8,4 kertik) ==")
    for f in sorted(glob.glob(os.path.join(V.CEKD, "KLAPE3_KASET", "parca", "*mentese_kulagi*.SLDPRT"))):
        yuz, sil, bb = olc(f)
        print("  %-30s yuz=%2d silindirik=%d  y %.1f..%.1f  z %.1f..%.1f  %s"
              % (os.path.basename(f)[:30], yuz, sil, bb[1], bb[4], bb[2], bb[5], "OK" if sil >= 1 else "KERTIK YOK"))
    print("== KLAPE 90 DERECE — SUPURME HACMI ==")
    MY, MZ, Y0K, H = V.MENT_Y, V.MENT_Z, V.KLAPE_ORNEK[0][1], V.KLAPE_H
    kose = [(y-MY, z-MZ) for y in (Y0K, Y0K+H+V.BIND) for z in (0.0, 40.0)]
    kose += [(y-MY, z-MZ) for y in (Y0K, Y0K+15.0) for z in (V.CZ0, 0.0)]
    ymin, zmin = 1e9, 1e9
    for dy, dz in kose:
        for k in range(0, 91):
            th = math.radians(k)
            ymin = min(ymin, MY + dy*math.cos(th) - dz*math.sin(th))
            zmin = min(zmin, MZ + dz*math.cos(th) + dy*math.sin(th))
    print("  mentese ekseni y=%.0f z=%.0f | 90 derecede ic yuz y=%.1f | kaset rafi KAP_Y=%.1f -> KOT FARKI %.1f mm"
          % (MY, MZ, MY+40.0, V.KAP_Y, MY+40.0-V.KAP_Y))
    print("  supurme y >= %.1f (alt panel ust kenari %.1f -> %s)" % (ymin, MY-2.0, "OK" if ymin >= MY-2.0 else "CARPIYOR"))
    print("  supurme z >= %.1f (cerceve saci -15 -> %s)" % (zmin, "OK" if zmin >= V.CZ0 else "CARPIYOR"))
    try: sw.ExitApp()
    except Exception: pass
