# -*- coding: utf-8 -*-
"""h3/hat3_montaj_v4.py (v3.4) → h3/hat3_montaj_v5.py (HAT v3.5 · 1 Eki 2026 · Claude · YEREL) — çıktı adı + sürüm + pafta.
v3.5 (Kemal "sen karar ver"): ana pano 304 paslanmaz özel imalat 400 × 350 × 250 (katalogda yok, QR üst bölmesi 395) · bina beslemesi QR sağından zemin üstü kanal +
bağlantı kutusu · TOPPING sürücü kabloları gerçek çap Ø8,9. Geometri yalnız elektrik katmanında (h3/_elk)."""
import io, os, runpy
H3 = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(H3, "yap_hat3_montaj_v4.py"))
s = io.open(os.path.join(H3, "hat3_montaj_v4.py"), encoding="utf-8").read()
for a, b in (("hat3_v4", "hat3_v5"), ('surum="v3.4"', 'surum="v3.5"')):
    assert a in s, a; s = s.replace(a, b)
a = 'pafta="HAT v3.4 (1 Eki · Claude · YEREL): ARA || '
assert s.count(a) == 1
s = s.replace(a, 'pafta="HAT v3.5 (1 Eki · Claude · YEREL): ANA PANO 304 PASLANMAZ ÖZEL İMALAT 400 × 350 × 250 (katalogda bu ölçü yok) · BİNA BESLEMESİ QR SAĞINDAN ZEMİN ÜSTÜ KANAL + BAĞLANTI KUTUSU · SÜRÜCÜ KABLOLARI GERÇEK Ø8,9 || HAT v3.4 (1 Eki · Claude · YEREL): A: açıcı görsel kalır · A|U_A rafı açıldı · TOPPING harç 2160 düz iniş · gömme kanal yok, E dış dikey kanal yok, ana besleme içeriden · QR alt bant + icotek girişleri · 5 üretici STEP · denetim temiz || ')
io.open(os.path.join(H3, "hat3_montaj_v5.py"), "w", encoding="utf-8").write(s)
print("hat3_montaj_v5.py yazıldı")
