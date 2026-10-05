# -*- coding: utf-8 -*-
"""hat_montaj_v72 → hat_montaj_v74 (29 Eyl 2026) — Kemal: "vazgeçtim, ayakları geri koy". v73'ün ayak/etek silmesi GERİ ALINDI; içerik v72 ile aynı. Çıktılar hat_v74."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v72.py"), encoding="utf-8").read()
def degis(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100]); s = s.replace(a, b)
degis('pafta="HAT v72 (29 Eyl) ·', 'pafta="HAT v74 (29 Eyl) · v73 GERI ALINDI: ayaklar + etekler yerinde (Kemal) · v72:')
degis('print("ALCAK HAT SOZLESMESI (v72 ·', 'print("ALCAK HAT SOZLESMESI (v74 ·')
for a_ in ("hat_v72.glb", "hat_v72.usdz", '"hat_v72"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v72", "v74"))
s = s.replace('"""', '"""hat_montaj_v74 (29 Eyl 2026): v72 ile aynı (ayaklar geri) — yap_hat_montaj_v74.py.\n', 1)
compile(s, "hat_montaj_v74.py", "exec")
io.open(os.path.join(U, "hat_montaj_v74.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v74.py yazildi")
