# -*- coding: utf-8 -*-
"""hat_montaj_v77 → hat_montaj_v78 (29 Eyl 2026 · YEREL) — B = store_cad_v12: K4 emiş pencereleri açık (fırın altı ilk ayak 2530) · sağ uçta tek enine
· K1 kablo kanalı köşesi birleşik. Çıktılar hat_v78."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v77.py"), encoding="utf-8").read()
def degis(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100]); s = s.replace(a, b)
degis('pafta="HAT v77 (29 Eyl · YEREL) ·', 'pafta="HAT v78 (29 Eyl · YEREL) · STORE v12: K4 EMIS PENCERELERI ACIK (ayak 2530) · SAG UC TEK ENINE · K1 KABLO KANALI KOSESI · v77:')
degis('print("ALCAK HAT SOZLESMESI (v77 ·', 'print("ALCAK HAT SOZLESMESI (v78 ·')
for a_ in ("hat_v77.glb", "hat_v77.usdz", '"hat_v77"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v77", "v78"))
print("store_cad_v11 -> v12:", s.count("store_cad_v11"))
s = s.replace("store_cad_v11", "store_cad_v12")
s = s.replace('"""', '"""hat_montaj_v78 (29 Eyl 2026 · YEREL): STORE v12 (K4 emiş pencereleri açık, sağ uç tek enine, K1 kablo köşesi) — yap_hat_montaj_v78.py.\n', 1)
compile(s, "hat_montaj_v78.py", "exec")
io.open(os.path.join(U, "hat_montaj_v78.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v78.py yazildi")
