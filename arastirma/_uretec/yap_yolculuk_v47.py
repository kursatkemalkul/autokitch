# -*- coding: utf-8 -*-
"""yolculuk_v46 → v47: hamur topu tablaya OTURUR (görsel denetim: 6,4–7,98 s arası top tablanın 5,7 mm üstünde asılıydı).
Sebep: yükseklik hesabı yarı yüksekliği TOP_R × TOP_K = 40,2 mm alıyordu; modeldeki top 49 × 34,8 mm (yarı yükseklik 34,8).
Artık yarı yükseklik topun kendi ağından OKUNUR (TOP_H) ve açma sırasında alt yüzü diskte kalır (0,95 katsayısı kalktı)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "yolculuk_v46.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


d('''    TOP_R, TOP_K = 49.0, 0.82
    top_x, top_y0, top_z0 = (_cb["x"][0] + _cb["x"][1]) / 2.0, _cb["y"][0] + 5.0 + TOP_R * TOP_K, (_cb["z"][0] + _cb["z"][1]) / 2.0''',
  '''    TOP_R, TOP_K = 49.0, 0.82
    _tm = [m_ for a_, m_, _x in parcalar if a_ == "URUN__top"]
    TOP_H = (-min(q[1] for q in _tm[0].P) / MM) if _tm else TOP_R * TOP_K   # v47: topun GERÇEK yarı yüksekliği (ağdan · 34,8)
    top_x, top_y0, top_z0 = (_cb["x"][0] + _cb["x"][1]) / 2.0, _cb["y"][0] + 5.0 + TOP_H, (_cb["z"][0] + _cb["z"][1]) / 2.0''')
d('TOPY.git(6.4, 6.9, H_B + 108.0 + TOP_R * TOP_K + 0.5, "ss")', 'TOPY.git(6.4, 6.9, H_B + 108.0 + TOP_H + 0.5, "ss")')
d('kanal("URUN__top", lambda t: (TOPX(t) * MM, (TOPY(t) - (TOP_R * TOP_K) * ACMA(t) * 0.95) * MM, TOPZ(t) * MM))',
  'kanal("URUN__top", lambda t: (TOPX(t) * MM, (TOPY(t) - TOP_H * ACMA(t)) * MM, TOPZ(t) * MM))   # v47: açılırken alt yüzü diskte')
io.open(os.path.join(U, "yolculuk_v47.py"), "w", encoding="utf-8").write(s)
print("yolculuk_v47.py yazildi")
