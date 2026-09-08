# -*- coding: utf-8 -*-
# STORE — bir çekmeceyi HAREKETLİ yap: sabitlemeyi kaldır + kızak bağlantısı (yalnız öne-arkaya, 0–600 mm sınırlı)
# Sonuç: Kemal çekmece önünü fareyle tutup çekince açılır, 600 mm'de durur. Kapanınca 0'a oturur.
import os, time, pythoncom
from sw_lib import *
ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE"
HEDEF, X0, Y0_, STROK = "CEKMECE_taze-1", 717.0, 1512.0, 600.0     # konumlar STORE montaj kaydından

NUL_ = VARIANT(pythoncom.VT_DISPATCH, None)
def sec(doc, ad, tur, mark=0, ekle=False):
    ok = doc.Extension.SelectByID2(ad, tur, 0.0, 0.0, 0.0, ekle, mark, NUL_, 0)
    if not ok: raise RuntimeError("secilemedi: " + ad)

def ref_duzlem(doc, kaynak, ofset):
    """kaynak düzlemden 'ofset' mm uzakta yeni referans düzlem"""
    doc.ClearSelection2(True); sec(doc, kaynak, "PLANE")
    f = doc.FeatureManager.InsertRefPlane(8, ofset*M, 0, 0, 0, 0)      # 8 = mesafe kısıtı
    if f is None: raise RuntimeError("duzlem olusmadi: " + kaynak)
    doc.ClearSelection2(True); return f

def mate(doc, a, b, tip, mesafe=0.0, ust=0.0, alt=0.0):
    doc.ClearSelection2(True)
    sec(doc, a, "PLANE", 1, False); sec(doc, b, "PLANE", 1, True)
    hata = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    m = doc.AddMate5(tip, 2, False, mesafe*M, ust*M, alt*M, 0, 0, 0, 0, 0, False, False, 0, hata)
    doc.ClearSelection2(True)
    print("    mate tip=%d hata=%s -> %s" % (tip, hata.value, "OK" if m is not None else "BASARISIZ"))
    return m

if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    doc = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
    print("STORE acildi, bilesen:", doc.GetComponentCount(True))
    # 1) hedef çekmeceyi serbest bırak
    doc.ClearSelection2(True); sec(doc, HEDEF + "@STORE", "COMPONENT")
    mcall(doc, "UnfixComponent"); doc.ClearSelection2(True); print("  sabitleme kaldirildi:", HEDEF)
    # 2) çekmecenin bulunduğu x ve y'de yardımcı düzlemler
    px = ref_duzlem(doc, "Right Plane", X0); py = ref_duzlem(doc, "Top Plane", Y0_)
    print("  duzlemler:", px.Name, py.Name)
    # 3) kızak bağlantısı: x ve y kilitli, z serbest (0–600 sınırlı)
    mate(doc, px.Name, "Right Plane@" + HEDEF + "@STORE", 0)                      # 0 = çakışık
    mate(doc, py.Name, "Top Plane@" + HEDEF + "@STORE", 0)
    mate(doc, "Front Plane", "Front Plane@" + HEDEF + "@STORE", 5, 0.0, STROK, 0.0)   # 5 = mesafe (sınırlı)
    mcall(doc, "EditRebuild3")
    # 4) kanıt: çekmeceyi 400 mm açıp görüntü al, sonra kapat
    for ac in (400.0, 0.0):
        try:
            p = doc.Parameter("D1@Distance1"); p.SystemValue = ac*M; mcall(doc, "EditRebuild3"); time.sleep(1)
            png(doc, os.path.join(ROOT, "STORE_cekmece_%s.png" % ("acik" if ac else "kapali")), "*Isometric")
            print("  cekmece %.0f mm -> goruntu alindi" % ac)
        except Exception as ex: print("  olcu ayari:", ex)
    if not saveas(doc, os.path.join(ROOT, "STORE.SLDASM")): print("  UYARI: kayit basarisiz")
    print("BITTI — cekmeceyi fareyle tutup cekebilirsin (0-600 mm)")
