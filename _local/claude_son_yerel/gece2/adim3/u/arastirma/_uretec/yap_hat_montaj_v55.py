# -*- coding: utf-8 -*-
"""hat_montaj_v54 → hat_montaj_v55 (27 Eyl 2026) · YALNIZ GÖRSEL (Kemal: "nerede, 3D'de göremedim"):
yalıtım bloğu görünür (yarı saydam krem; v51'den beri çıplak modelde gizliydi) · teknik ayırma saçı mavi · pizza + içecek yedeği yığınları opak karton
(v54'te %30 saydam gri "henüz kutu" rengindeydi). Geometri ve denetimler v54 ile aynı."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v54.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
degis('"""v54 (27 Eyl 2026):', '"""v55 (27 Eyl 2026): GÖRSEL — yalıtım yarı saydam krem görünür, teknik ayırma saçı mavi, pizza + içecek yığınları opak karton (Kemal: 3D\'de göremedim)' + NL + 'v54 (27 Eyl 2026):')
degis('''for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))''', '''for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))
# v55 · görünürlük: yalıtım yarı saydam krem · ayırma saçı mavi · yedek yığınları karton
MALZEME["yalitim_gorunur"] = dict(renk=(0.95, 0.84, 0.52, 0.38), met=0.0, ruf=0.8, saydam=True)
MALZEME["ayirma_saci"] = dict(renk=(0.18, 0.36, 0.92, 1.0), met=0.3, ruf=0.4, saydam=False)
MALZEME["karton"] = dict(renk=(0.80, 0.64, 0.42, 1.0), met=0.0, ruf=0.85, saydam=False)
for _q in TU.P:
    if _q["ad"] == "yalitim_blogu":
        _q["mal"] = "yalitim_gorunur"
    elif _q["ad"].startswith("teknik_ayirma_saci"):
        _q["mal"] = "ayirma_saci"''')
degis('"yalitim_blogu", "on_fitil", "yalitim_tasyunu",', '"on_fitil", "yalitim_tasyunu",')
degis('(3328.0, 3595.0), (1516.0, 2008.0), (-422.0, -22.0), "kutu", "v54 ·', '(3328.0, 3595.0), (1516.0, 2008.0), (-422.0, -22.0), "karton", "v54 ·')
degis('(3170.0, 3570.0), (130.0, 253.0), (-287.0, -20.0), "kutu", "v54 ·', '(3170.0, 3570.0), (130.0, 253.0), (-287.0, -20.0), "karton", "v54 ·')
degis('(X_D + 20.0, X_D + 824.0), (1516.0, 2028.0), (-424.0, -20.0), "kutu", "v48 ·', '(X_D + 20.0, X_D + 824.0), (1516.0, 2028.0), (-424.0, -20.0), "karton", "v48 ·')
degis('pafta="HAT v54 (27 Eyl) ·', 'pafta="HAT v55 (27 Eyl) · GORSEL: yalitim gorunur (yari saydam), ayirma saci mavi, yedek yiginlari karton · v54:')
degis('print("ANA MONTAJ ANIMASYONU (v54):', 'print("ANA MONTAJ ANIMASYONU (v55):')
s = s.replace('hat_v54.glb', 'hat_v55.glb').replace('hat_v54.usdz', 'hat_v55.usdz').replace('"hat_v54"', '"hat_v55"')
io.open(os.path.join(U, "hat_montaj_v55.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v55.py yazildi")
