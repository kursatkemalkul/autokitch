# -*- coding: utf-8 -*-
"""MADDE 5 ("zemini kaldir, duz surface koy") · ZEMIN_DOSEME: 60 × 60 karo kutulari (y −10…0, kenar cizgili, kesitte kirmizi) + sap katmani
(y −30…−10) SILINIR; yerine tek duz, cizgisiz yuzey: y = 0 duzleminde 2 ucgen (x −864…6336 · z −830…2170, ayni zemin alani).
Malzeme (MR_ZEMIN_DOSEME__zemin_karo, acik gri, cift yuzlu) ve kat/mek etiketi (Cevre) korunur. Golge sayfada model-viewer
golge duzlemi — dokunulmadi.
Kullanim: python m5_zemin_duz.py giris.glb cikis.glb"""
import sys, numpy as np
sys.path.insert(0, r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\t3\is_A\gece")
import glbkit

gi, go = sys.argv[1:3]
G = glbkit.Glb(gi)
for nm in ("ZEMIN_DOSEME__zemin_karo", "ZEMIN_DOSEME__zemin_sap"):
    p = G.bul(nm); print("  %s sil %d ucgen" % (nm, G.sil(p, G.gorunur(p))))
p = G.bul("ZEMIN_DOSEME__zemin_karo")
X = np.array([[-864.0, 0.0, -830.0], [6336.0, 0.0, -830.0], [6336.0, 0.0, 2170.0], [-864.0, 0.0, 2170.0]])
T = np.array([[0, 2, 1], [0, 3, 2]])                                        # normal +y (yukari)
print("  duz zemin ucgen", G.ekle(p, X, T))
G.kaydet(go); print("yazildi", go)
