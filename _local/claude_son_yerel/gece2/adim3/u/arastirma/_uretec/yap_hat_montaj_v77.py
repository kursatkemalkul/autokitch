# -*- coding: utf-8 -*-
"""hat_montaj_v76 → hat_montaj_v77 (29 Eyl 2026 · YEREL) — B = store_cad_v11: fırın altı ayakları + alt şase kenarda (soldaki gibi) · K4|K5 bölmesinin önü kapalı.
Çıktılar hat_v77."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v76.py"), encoding="utf-8").read()
def degis(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100]); s = s.replace(a, b)
degis('pafta="HAT v76 (29 Eyl · YEREL) ·', 'pafta="HAT v77 (29 Eyl · YEREL) · STORE v11: FIRIN ALTI AYAKLAR + ALT SASE KENARDA (soldaki gibi) · K4|K5 BOLME ONU KAPALI · v76:')
degis('print("ALCAK HAT SOZLESMESI (v76 ·', 'print("ALCAK HAT SOZLESMESI (v77 ·')
for a_ in ("hat_v76.glb", "hat_v76.usdz", '"hat_v76"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v76", "v77"))
print("store_cad_v10 -> v11:", s.count("store_cad_v10"))
s = s.replace("store_cad_v10", "store_cad_v11")
s = s.replace('"""', '"""hat_montaj_v77 (29 Eyl 2026 · YEREL): STORE v11 (ayaklar kenarda, K4|K5 önü kapalı) — yap_hat_montaj_v77.py.\n', 1)
compile(s, "hat_montaj_v77.py", "exec")
io.open(os.path.join(U, "hat_montaj_v77.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v77.py yazildi")
