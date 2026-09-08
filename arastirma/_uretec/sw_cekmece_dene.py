# -*- coding: utf-8 -*-
# kızak bağlantısı eklenmiş çekmeceyi ölçüsünden açıp kapatarak dene + kaydet
import os, time, pythoncom
from sw_lib import *
ROOT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\1_STORE"
sw.CloseAllDocuments(True)
e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
doc = sw.OpenDoc6(os.path.join(ROOT, "STORE.SLDASM"), 2, 1, "", e, w); sw.FrameState = 2
f = mcall(doc, "FirstFeature"); mates = []
while f is not None:
    t = mcall(f, "GetTypeName2")
    if t == "MateGroup":
        c = mcall(f, "GetFirstSubFeature")
        while c is not None:
            mates.append((c.Name, mcall(c, "GetTypeName2"))); c = mcall(c, "GetNextSubFeature")
    f = mcall(f, "GetNextFeature")
print("mate listesi:", mates)
for ad, tip in mates:
    for kalip in ("D1@%s" % ad, "D1@%s@STORE.SLDASM" % ad):
        p = doc.Parameter(kalip)
        if p is not None: print("  olcu bulundu:", kalip, "deger =", p.SystemValue*1000); ad_olcu = kalip; break
    else: continue
    break
else:
    ad_olcu = None; print("  olcu bulunamadi")
if ad_olcu:
    for mm, etiket in ((450.0, "acik"), (0.0, "kapali")):
        doc.Parameter(ad_olcu).SystemValue = mm/1000.0; mcall(doc, "EditRebuild3"); time.sleep(1)
        png(doc, os.path.join(ROOT, "STORE_cekmece_%s.png" % etiket), "*Isometric"); print("  %s (%.0f mm) goruntu alindi" % (etiket, mm))
print("kayit:", saveas(doc, os.path.join(ROOT, "STORE.SLDASM")))
