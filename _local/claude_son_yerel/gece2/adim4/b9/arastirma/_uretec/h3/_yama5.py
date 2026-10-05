# -*- coding: utf-8 -*-
import io, os
D = os.path.dirname(os.path.abspath(__file__))
def yama(ad, R):
    P = os.path.join(D, ad); s = io.open(P, encoding="utf-8").read()
    for a, b in R:
        assert s.count(a) == 1, (ad, a[:80]); s = s.replace(a, b)
    io.open(P, "w", encoding="utf-8").write(s)
yama("h3_moduler_v1.py", [
 ("# h3_moduler_v1 (30 Eyl 2026 · Claude, YEREL): HAT VERSİYON 2 · moduler_montaj_v4'ün v2 KOPYASI",
  "# h3_moduler_v1 (30 Eyl 2026 · Claude, YEREL): HAT VERSİYON 3 · h2_moduler_v1'in kopyası — B/AC dikmeleri v3 dolabının bölmelerinde (h3_hesap_v1.BOLME_V3):\n"
  "#   753 (sol duvar PU) · 1436 (B1) · 2091 (B2) · 2746 (B3 = fırın taşıyıcı dikmeleri TD, ön hatta ORTAK) · kiriş sağ ucu 2731 (TD sol yüzü) · dolap 736–4400.\n"
  "# ESKİ BAŞLIK (v2): HAT VERSİYON 2 · moduler_montaj_v4'ün v2 KOPYASI"),
 ('''def v2x(x_v1):
    """v1 dünya x → v2 (h3_hesap_v1): dolabın / A'nın sol grubu (x < B_DILIM[0]) + DXL · dilimin içi YOK · x ≥ B_DILIM[1] yerinde"""
    if x_v1 < H.B_DILIM[0]: return x_v1 + DXL
    if x_v1 >= H.B_DILIM[1]: return x_v1
    raise ValueError("v1 x %.1f dolaptan çıkan dilimde (%.1f–%.1f)" % (x_v1, H.B_DILIM[0], H.B_DILIM[1]))
''', ""),
 ("TD_X0 = H.B_DILIM[1] + BOLME / 2.0                       # 2517,5 · B4 (K3|K5, eski K4|K5) bölmesinin ortası = store_cad_v14 TD_X[0] (fırın taşıyıcı dikmeleri)",
  "TD_X0 = H.BOLME_V3[2] + BOLME / 2.0                      # v3 · 2746 · B3 (K3|K5) bölmesinin ortası = h3_store_v1 fırın taşıyıcı dikmeleri (TD) ilk ekseni"),
 ("TK_X0 = TD_X0 - 15.0                                     # 2502,5 = store_cad_v14 TK_X[0] (fırın taşıyıcı kirişleri + TD dikmesinin sol yüzü) = v1 kiriş sağ ucu",
  "TK_X0 = TD_X0 - 15.0                                     # v3 · 2731 = TD dikmesinin sol yüzü = h3_store_v1 fırın ön taşıyıcı kirişinin sol ucu"),
 ('''                v2x(682.5 + BOLME / 2.0),                # 1207,5 (v1 700) · B1 bölmesi (store_cad_v14 BOLME_X[0] 682,5)
                v2x(1337.5 + BOLME / 2.0),               # 1862,5 (v1 1355) · B2 bölmesi (BOLME_X[1] 1337,5)
                TD_X0)                                   # 2517,5 (v1 2010 = B3 ortası · B3 dilimle çıktı) · K3'ün yeni sağ bölmesi B4''',
  '''                H.BOLME_V3[0] + BOLME / 2.0,             # v3 · 1436 · B1 bölmesi (K1|K2)
                H.BOLME_V3[1] + BOLME / 2.0,             # v3 · 2091 · B2 bölmesi (K2|K3)
                TD_X0)                                   # v3 · 2746 · B3 bölmesi (K3|K5) · ön hatta fırın TD dikmesi ORTAK'''),
])
print("ok")
