# -*- coding: utf-8 -*-
"""h3/hat3_montaj_v2.py (v3.2) → h3/hat3_montaj_v3.py (HAT v3.3 · 1 Eki 2026 · Claude · YEREL) — çıktı adı + sürüm + pafta notu.
v3.3: cihaz envanteri denetiminde kablosuz kalan X ekseni motoru bağlandı (A arka duvarı boyunca → G9 rakoru → TOPPING panosu) · açıcı hazır alınır, yalnız görsel ·
yükleme bandı kablosu motor yüzüne tam dayalı. Elektrik katmanı h3_elektrik_v1 önbelleğinden (h3/_elk)."""
import io, os, runpy
H3 = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(H3, "yap_hat3_montaj_v2.py"))                     # önce v3.2 yaması (hat3_montaj_v2.py)
s = io.open(os.path.join(H3, "hat3_montaj_v2.py"), encoding="utf-8").read()
N = [0]


def rep(a, b, n=None):
    global s
    c = s.count(a)
    assert c >= 1 and (n is None or c == n), (a[:100], c)
    s = s.replace(a, b); N[0] += 1


rep("hat3_v2", "hat3_v3")
rep('surum="v3.2"', 'surum="v3.3"', 1)
rep('pafta="HAT v3.2 (1 Eki · Claude · YEREL): ', 'pafta="HAT v3.3 (1 Eki · Claude · YEREL): X EKSENİ MOTORU BAĞLANDI (A arka duvarı → G9 rakoru → TOPPING panosu) · AÇICI HAZIR ALINIR: yalnız görsel, motor kablosu yok · cihaz envanteri: tüm cihazlar kablolu (araba üstündekiler enerji zincirinden) || HAT v3.2: ', 1)
io.open(os.path.join(H3, "hat3_montaj_v3.py"), "w", encoding="utf-8").write(s)
print("hat3_montaj_v3.py yazıldı · %d yama" % N[0])
