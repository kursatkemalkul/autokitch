# -*- coding: utf-8 -*-
import io, os
D = os.path.dirname(os.path.abspath(__file__))
def yama(ad, R):
    P = os.path.join(D, ad); s = io.open(P, encoding="utf-8").read()
    for a, b in R:
        assert s.count(a) == 1, (ad, a[:80]); s = s.replace(a, b)
    io.open(P, "w", encoding="utf-8").write(s)
yama("h3_ist_v1.py", [
 ('"""HAT v2 · TOPPING DOZAJ HESABI ADAPTÖRÜ', '"""HAT v3 (v2 adaptörünün kopyası) · TOPPING DOZAJ HESABI ADAPTÖRÜ'),
 ('IST_DUNYA = {"SOS": 1396.0, "HARC": 1466.0, "KIYMA": 1596.0, "KUSBASI": 1806.0, "KASAR": 2062.0, "SUCUK": 2311.0}',
  'IST_DUNYA = dict(HS.IST_V3)                    # v3 · sos 1645 · harç 2160 (yayıcılar alt kat dozajlayıcılarının arasında)'),
 ('X_PARK = _m.X_PARK + HS.DXL                                                           # −350 → 157,5 (açıcının altı)',
  'X_PARK = _m.X_PARK + HS.DXL                                                           # −350 → 386 (dünya 1086 · açıcının altı)'),
 ('_ENGEL = _m.engel_denetimi()\nassert all(r[-1] for r in _ENGEL), [r for r in _ENGEL if not r[-1]]                 # pidenin dökülen halkası yayıcı borularının altına girmez',
  '# v3: yayıcı ağzı kaset iniş borularıyla aynı kotta (1047) → pide + malzeme koridorunun (1033) üstünde; dökülen halka her ağzın altından geçer ·\n'
  '#     v2\'nin engel denetimi (yayıcı borusu alçaktaydı, halka altına giremezdi) yerine KORİDOR denetimi\n'
  '_ENGEL = [(k, HS.Y_AGIZ - 1.0, HS.Y_KORIDOR, HS.Y_AGIZ - 1.0 - HS.Y_KORIDOR >= 10.0) for k in BORU_X]\n'
  'assert all(r[-1] for r in _ENGEL), _ENGEL'),
])
print("ok")
