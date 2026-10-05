# -*- coding: utf-8 -*-
"""hat_montaj_v61 → hat_montaj_v62 (27 Eyl 2026 gece) — Kemal: "mausla üstüne gelip biraz beklediğimde o parçanın ne olduğu yazar mı, mouse yanında küçük etiket gibi".
GLB parçaları birim + malzemeye göre birleşik (binlerce düğüm telefonu yorar) → parça adı GLB'de yok. v62: ağ kurulurken her parçanın ADI + BİRİMİ + dünya
sınır kutusu (mm) otonom/hat3d/parca_kutulari.json'a yazılır; sayfa (model3d.js v17) farenin değdiği noktayı bu kutularda arar, şeffaf kapağa değerse
ışın boyunca arkasındaki ilk parçaya geçer. Model ve denetimler DEĞİŞMEZ; çıktılar hat_v62."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v61.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""v61 (27 Eyl 2026 gece):',
      '"""v62 (27 Eyl 2026 gece): PARÇA ETİKETİ — her parçanın adı + birimi + sınır kutusu parca_kutulari.json\'a (sayfada fare etiketi) · çıktılar hat_v62.' + NL +
      'v61 (27 Eyl 2026 gece):')
degis('\nif __name__ == "__main__":\n', '''
# ---- v62 · PARÇA KUTULARI (sayfadaki fare etiketi): her TC_AG çağrısında çağıran satırın parçası (p / q) ve birimi (b) kaydedilir
import linecache as _lc62
PARCA_KUTU = {}
_TC_AG_ASIL = TC_AG


def TC_AG(wp, *a, **k):
    try:
        f_ = sys._getframe(1); L_ = f_.f_locals; sat_ = _lc62.getline(f_.f_code.co_filename, f_.f_lineno)
        pv_ = L_.get("q") if 'q["' in sat_ else (L_.get("p") if 'p["' in sat_ else None)
        bv_ = L_.get("b")
        if isinstance(pv_, dict) and "ad" in pv_ and isinstance(bv_, dict) and "kod" in bv_:
            sh_ = wp.val() if hasattr(wp, "val") else wp; bb_ = sh_.BoundingBox()
            PARCA_KUTU.setdefault(bv_["kod"], []).append([pv_["ad"], 1 if pv_.get("mal") == "on_seffaf" else 0]
                                                        + [round(v_, 1) for v_ in (bb_.xmin, bb_.xmax, bb_.ymin, bb_.ymax, bb_.zmin, bb_.zmax)])
    except Exception:
        pass
    return _TC_AG_ASIL(wp, *a, **k)


if __name__ == "__main__":
''')
degis('''    parcalar.append(("INSAN_180cm__insan_180", _im, "insan_180"))''',
      '''    parcalar.append(("INSAN_180cm__insan_180", _im, "insan_180"))
    PARCA_KUTU["INSAN_180cm"] = [["insan figuru 180 cm (olcek)", 0] + [round(v_, 1) for v_ in (_ib.xmin, _ib.xmax, _ib.ymin, _ib.ymax, _ib.zmin, _ib.zmax)]]''')
degis('''    g_ = sum(v for k, v in sayac.items() if k.startswith("GERCEK"))
    print("durum.json yazildi''',
      '''    with io.open(os.path.join(OUT, "parca_kutulari.json"), "w", encoding="utf-8") as f:
        json.dump(dict(birim={b["kod"]: dict(ad=b["ad"], mal=mal_ad(b)) for b in B}, parca=PARCA_KUTU), f, ensure_ascii=False, separators=(",", ":"))
    print("v62 · parca_kutulari.json: %d birim · %d parca kutusu" % (len(PARCA_KUTU), sum(len(v) for v in PARCA_KUTU.values())))
    assert sum(len(v) for v in PARCA_KUTU.values()) > 1000, "v62: parca kutulari eksik"
    g_ = sum(v for k, v in sayac.items() if k.startswith("GERCEK"))
    print("durum.json yazildi''')
degis('pafta="HAT v61 (27 Eyl gece) ·', 'pafta="HAT v62 (27 Eyl gece) · PARCA ETIKETI (parca_kutulari.json · fare durunca parca adi) · v61:')
degis('print("ALCAK HAT SOZLESMESI (v61 ·', 'print("ALCAK HAT SOZLESMESI (v62 ·')
for a_ in ("hat_v61.glb", "hat_v61.usdz", '"hat_v61"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v61", "v62"))
compile(s, "hat_montaj_v62.py", "exec")
io.open(os.path.join(U, "hat_montaj_v62.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v62.py yazildi")
