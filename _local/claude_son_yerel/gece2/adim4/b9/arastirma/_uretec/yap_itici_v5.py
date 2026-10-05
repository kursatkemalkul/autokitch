# -*- coding: utf-8 -*-
"""itici_cad_v4 → itici_cad_v5 (28 Eyl 2026 gece) · ÖN DÜZLEM v63 — HAVADA PARÇA (SPEC_on_duzlem_v63 §2.3, C ajanı)
Tek değişiklik: SMC AS1201F-M5-06 hız ayar valfleri (hiz_ayar_0/1) gövdenin 4 mm ALTINDA havadaydı (M5 portları gövdenin uç kapaklarında) →
valf ekseni gövdenin içine (alt yüzün 6 mm üstü) alındı: yan yüzdeki M5 portuna vidalı, gövdeye değer. Kinematik, kotlar, strok, x/z AYNI.
Montaj notu: hat_montaj_v63 'import itici_cad_v4 as IT' → itici_cad_v5 (sözleşme aynı: kur() · PARCALAR · dunya() · BIRIMLER · kontrol_hepsi()).
Çalıştır: python yap_itici_v5.py [çıkış_adı.py]"""
import io, os, sys
U = os.path.dirname(os.path.abspath(__file__))
CIKIS = sys.argv[1] if len(sys.argv) > 1 else "itici_cad_v5.py"
s = io.open(os.path.join(U, "itici_cad_v4.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


d('"""AKTARMA İTİCİSİ v4 · itici_cad_v4 · 27 Eyl 2026',
  '"""AKTARMA İTİCİSİ v5 · itici_cad_v5 · 28 Eyl 2026 gece (v4 + ÖN DÜZLEM v63 havada parça: hız ayar valfleri gövdeye vidalı — gövdenin 4 mm altında havadaydı; başka değişiklik YOK).\n'
  'Önceki: itici_cad_v4.py (yap_itici_v5.py)\n'
  'v4 · itici_cad_v4 · 27 Eyl 2026')
d('        ekle("hiz_ayar_%d" % i, yerel(silz(s_, TAVAN - 6.0 - MY["NE"] - 8.0, 4.0, wa + MY["NW"] / 2.0, wa + MY["NW"] / 2.0 + 14.0)), "siyah", "C_ITICI", kaynak="K",',
  '        ekle("hiz_ayar_%d" % i, yerel(silz(s_, TAVAN - 6.0 - MY["NE"] + 6.0, 4.0, wa + MY["NW"] / 2.0, wa + MY["NW"] / 2.0 + 14.0)), "siyah", "C_ITICI", kaynak="K",   # v5: M5 portu gövdenin yan yüzünde (v4: 4 mm altında, havada)')
d('''    sonuc.append(("ALÇAK HAT (SPEC v57) · disk üstü %.0f = 1000''',
  '''    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    P = kur(S_HOME, True); _g = [dunya(p) for p in P if p["ad"] == "my1b16_govde"][0]
    for p in [p for p in P if p["ad"].startswith("hiz_ayar_")]:
        _d = _DSS(dunya(p).wrapped, _g.wrapped); _d = _d.Value() if _d.IsDone() else 99.0
        sonuc.append(("v5 · %s silindir gövdesine vidalı (mesafe %.3f ≤ 0,05)" % (p["ad"], _d), _d <= 0.05, ""))
    sonuc.append(("ALÇAK HAT (SPEC v57) · disk üstü %.0f = 1000''')
d('    print("İTİCİ v4 · %d parça', '    print("İTİCİ v5 · %d parça')
io.open(os.path.join(U, CIKIS), "w", encoding="utf-8").write(s)
compile(s, CIKIS, "exec")
print("%s yazildi" % CIKIS)
