# -*- coding: utf-8 -*-
"""hat_montaj_v78 → hat_montaj_v79 (29 Eyl 2026 · YEREL) — Kemal: "delikleri kaldır, nasıl bağlanacaklarını şu an karar vermeyeceğiz, bağlanmayla ilgili
şeyleri kaldır" + K4 depo "tek kap, bölmeli". moduler_montaj_v2 (modüller arası bağlantı parçası YOK) · B = store_cad_v13. Çıktılar hat_v79."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v78.py"), encoding="utf-8").read()
def degis(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100]); s = s.replace(a, b)
degis('pafta="HAT v78 (29 Eyl · YEREL) ·', 'pafta="HAT v79 (29 Eyl · YEREL) · MODULLER ARASI BAGLANTI PARCALARI YOK (karar sonra · A/C-B civata + delik, B-K / K-E plaka kalkti) · K4 DEPO TEK BOLMELI KAP (kasar 22,5 L + sucuk 6,6 L) · v78:')
degis('print("ALCAK HAT SOZLESMESI (v78 ·', 'print("ALCAK HAT SOZLESMESI (v79 ·')
for a_ in ("hat_v78.glb", "hat_v78.usdz", '"hat_v78"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v78", "v79"))
print("store_cad_v12 -> v13:", s.count("store_cad_v12"))
s = s.replace("store_cad_v12", "store_cad_v13")
degis('import types as _ty, moduler_montaj_v1 as MOD72', 'import types as _ty, moduler_montaj_v2 as MOD72                   # v79: v2 = bağlantı parçaları yok (Kemal)')
degis('(A cerceve −2, cepler, civata delikleri)', '(A cerceve −2, cepler · v79: baglanti parcasi / civata deligi YOK)')
s = s.replace('"""', '"""hat_montaj_v79 (29 Eyl 2026 · YEREL): bağlantı parçaları yok (moduler_montaj_v2) · STORE v13 K4 depo tek kap — yap_hat_montaj_v79.py.\n', 1)
compile(s, "hat_montaj_v79.py", "exec")
io.open(os.path.join(U, "hat_montaj_v79.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v79.py yazildi")
