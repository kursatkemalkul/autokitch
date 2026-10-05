# -*- coding: utf-8 -*-
"""hat_montaj_v79 → hat_montaj_v80 (29 Eyl 2026 · YEREL) — Kemal: "yap yapılacakları işte". B = store_cad_v14: çekmece kutusu tabanı 2 mm · motor rampası
0,3 s · yük denetimi (ray 45 kg / motor 60 N / taban sehimi ≤ 2 mm). Animasyonda çekmece açılma süresi rampayı içerir (strok / hız + 0,3 s). Çıktılar hat_v80."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v79.py"), encoding="utf-8").read()
def degis(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100]); s = s.replace(a, b)
degis('pafta="HAT v79 (29 Eyl · YEREL) ·', 'pafta="HAT v80 (29 Eyl · YEREL) · STORE v14: CEKMECE KUTU TABANI 2 mm (sehim <= 2 mm) · MOTOR RAMPASI 0,3 s (en agir cekmece 34 kg, ray 45 kg, motor 25 / 60 N) · v79:')
degis('print("ALCAK HAT SOZLESMESI (v79 ·', 'print("ALCAK HAT SOZLESMESI (v80 ·')
for a_ in ("hat_v79.glb", "hat_v79.usdz", '"hat_v79"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v79", "v80"))
print("store_cad_v13 -> v14:", s.count("store_cad_v13"))
s = s.replace("store_cad_v13", "store_cad_v14")
degis('    CEK_T = SC.STROK / (127.0 / 60.0 * math.pi * SC.KAS_PD)           # 3,3 s (çekmece motoru)',
      '    CEK_T = SC.STROK / (127.0 / 60.0 * math.pi * SC.KAS_PD) + SC.RAMPA_SN   # v80: 3,7 s + 0,3 s yumuşak kalkış/duruş rampası (store_cad_v14)')
degis('    _ac = SC.STROK / (127.0 / 60.0 * 3.141592653589793 * SC.KAS_PD)               # 3,3 sn (motor hizi)',
      '    _ac = SC.STROK / (127.0 / 60.0 * 3.141592653589793 * SC.KAS_PD) + SC.RAMPA_SN  # v80: + rampa (store_cad_v14)')
s = s.replace('"""', '"""hat_montaj_v80 (29 Eyl 2026 · YEREL): STORE v14 (taban 2 mm, motor rampası 0,3 s) — yap_hat_montaj_v80.py.\n', 1)
compile(s, "hat_montaj_v80.py", "exec")
io.open(os.path.join(U, "hat_montaj_v80.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v80.py yazildi")
