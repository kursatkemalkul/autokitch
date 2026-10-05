"""v81 -> v82. E v9 only; local main model, with explicit manufacturing caveats."""
from pathlib import Path
U=Path(__file__).resolve().parent
s=(U/'hat_montaj_v81.py').read_text(encoding='utf-8-sig')
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a),n)
    s=s.replace(a,b)
rep('import kutu_cad_v8 as KC','import kutu_cad_v9 as KC')
rep('"kutu_cad_v8.py", "hat/pack.html"','"kutu_cad_v9.py", "hat/pack.html"')
s=s.replace('hat_v81','hat_v82')
rep('pafta="HAT v81 (29 Eyl · YEREL) ·', 'pafta="HAT v82 (29 Eyl · YEREL) · E: MOTOR GOVDE ICINDE, ORTA AYAKLAR HIZALI, DUZ YAN KAPAK. KUTU KATLAMA URETIME HAZIR DEGIL: KOSE KIVIRICI EKSIK, ACINIM/KARTON KATLANMA PAYLARI ONAYSIZ, YAN KAPAK ACILMA/DOLUM VE SON 43 BLANK ICIN REVIZYON GEREKLI. v81:')
rep('print("ALCAK HAT SOZLESMESI (v81 ·','print("ALCAK HAT SOZLESMESI (v82 ·')
# Correct the inherited console capacity note; this does not change geometry.
rep('"pizza kutusu (E sarjoru)"', '"pizza kutusu (GEOMETRIK)"')
rep("kullanilabilir ≈ 432 + %d = %d (asansor somunu 935'te durur, v4'ten miras, karar Kemal'de)",
    "beslenebilir UST SINIR 419 + %d = %d (ray stroku671.3; son43 kalir; URETIM ONAYI DEGIL)")
rep('PIZZA_UST_KUTU, 432 + PIZZA_UST_KUTU))]', 'PIZZA_UST_KUTU, 419 + PIZZA_UST_KUTU))]')
rep('E KUTU MODULU (kutu_cad_v8)', 'E KUTU MODULU (kutu_cad_v9)')
rep('"E_SARJOR", "Şarjör + asansör: 462 kutu (1,6 mm · yığın 240–980; kullanılabilir ≈ 432: asansör somunu 935\'te durur, v4\'ten miras — karar Kemal\'de) · Tr16×4 · 2 HGR15 · NEMA 23 · 2:1 GT3"',
    '"E_SARJOR", "Şarjör + asansör: motor taban ÜSTÜNDE; 462 geometrik / en çok 419 beslenebilir (ray hareket sınırı; son 43 kalır). Sağ dolum için en az 804 mm yan boşluk; menteşe açılması doğrulanmadı. Tr16×4 · NEMA23 · 2:1 GT3"')
rep('if __name__ == "__main__":', '''# v82: the E floor stays continuous. The drive and frame are measured from solids.
_ep82={p["ad"]:p for p in KC.PARCALAR}
_emb82=_ep82["asansor_motoru"]["wp"].val().BoundingBox()
assert _emb82.ymin >= 126.0 and _emb82.xmax < KC.W and _emb82.zmax < -350.0
assert set(z for x,z in KC.AYAK_XZ)=={-110.0,-770.0}
_ef82=[p for p in MODULER_YENI if p["module"]=="E"]
assert max(p["shape"].BoundingBox().zmax for p in _ef82)<=-90.0+1e-6
assert not any("baglanti" in p["name"] for p in _ef82)
KUTU_DENETIM_V82=dict(ready_for_manufacture=False, geometry="E v9: internal drive, aligned supports, flush side door",
    regression="288 solids; changed parts0, machine201 samples0, box-machine46 samples0, pizza25 samples0; elevator8 heights0",
    open=["804x404 assumed die line, no supplier drawing", "corner-tab folding actuator missing",
          "cardboard panels intersect in prescribed folding animation", "side hinge motion/refill is not validated; >=804 mm right clearance",
          "rail travel671.3 mm; usable stock upper bound419 of462"])
print("v82 E: motor y %.3f..%.3f; floor126; aligned frame zmax %.1f; MANUFACTURING AUDIT OPEN" %
      (_emb82.ymin,_emb82.ymax,max(p["shape"].BoundingBox().zmax for p in _ef82)),flush=True)

if __name__ == "__main__":''')
rep('json.dump(dict(hat=dict(', 'json.dump(dict(kutu_denetim=KUTU_DENETIM_V82, hat=dict(')
compile(s,'hat_montaj_v82.py','exec')
(U/'hat_montaj_v82.py').write_text(s,encoding='utf-8')
for name in ('makine.html','index.html'):
    p=U.parent.parent/'otonom'/'hat'/name
    data=p.read_bytes()
    data=data.replace(b'hat_v81',b'hat_v82').replace(b'?v=81',b'?v=82')
    p.write_bytes(data)
print('v82 generator and main-model references updated; no page text or secondary page changes')
