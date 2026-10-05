# -*- coding: utf-8 -*-
"""topping_cad_v25 → topping_cad_v26 (28 Eyl 2026) — ÜRETİM DÜZELTMELERİ (katı denetimi denetim_kati_v1.py · Kemal: "düzelt, onaylıyorum yap").
1 · AÇICI KOLONU gerçek KUTU PROFİL: v25'te 120 × 50 × 612 DOLU blok çiziliydi (BOM zaten "304 kutu profil 120 × 50" diyordu; dolu hali ≈ 29 kg çelik).
    v26: 304 kutu profil 120 × 50 × 4 (et 4 VARSAYIM — katalogdan teyit), uçları açık + içeride 10 mm alt uç plakası (kaynaklı, 4 × M10 dişli: kaide A'ya
    alttan) + üst kol 90 × 30 × 155 (kaynaklı, v25 ile aynı). Dış ölçüler, yeri, rayların oturduğu ön yüz AYNI. Z rayları ön duvara M4 perçin somunla (VARSAYIM).
2 · RAY ÖRTÜ ÇATISI açıkça 2 ŞERİT: v25'te çatıdaki 36 mm araba yarığı boydan boya kesiyor, "tek parça" çatı iki ayrık L şeride düşüyordu (BOM 2 derken 4 şerit).
    Uçlara köprü konamaz: kızak blokları örtünün uçlarına 9–39 mm yaklaşıyor (park / limit+). v26: her örtü 2 ayrı L şerit (a · b), BOM 4. Geometri AYNI.
3 · DÜNYA DENETİMİ montaj v69'un soğuk paketiyle: topping_uno_cad_v15 + sucuk_cad_v8 (v25: v14 + v7).
Başka hiçbir parça değişmez. Önceki: topping_cad_v25.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v25.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""v25 (28 Eyl 2026 gece): ÖN DÜZLEM +79',
      '"""v26 (28 Eyl 2026 akşam · yap_topping_cad_v26.py): AÇICI KOLONU kutu profil 120 × 50 × 4 (v25 dolu blok) · RAY ÖRTÜ ÇATISI 2 ayrı L şerit (yarık boydan boya) · '
      'başka değişiklik yok. Önceki: topping_cad_v25.py' + NL + 'v25 (28 Eyl 2026 gece): ÖN DÜZLEM +79')
degis('print("TOPPING MODULU v25 ·', 'print("TOPPING MODULU v26 ·')
degis('''        ekle("ray_ortu_catisi_%s" % ad_, ct, "sac",
             bom=("Ray örtü çatısı", 2, "304 1,0 mm · 90 geniş, tepe y 44, ortada 36 yarık", "arabanın olmadığı yerde rayı örter; 24 × M4 havşa") if ad_ == "on" else None)''',
      '''        for _y26, (_za, _zb) in (("a", (zc_ - 31.0, zc_ - 18.0)), ("b", (zc_ + 18.0, zc_ + 31.0))):     # v26: yarık boydan boya → 2 ayrı L şerit (v25: tek parça sanılıyordu)
            ekle("ray_ortu_catisi_%s_%s" % (ad_, _y26), ct.intersect(kut(-525.0, 1795.0, 19.0, 45.0, _za, _zb)), "sac",
                 bom=("Ray örtü şeridi · L 12 × 23,5", 4, "304 1,0 mm bükme · boy 2310 · iki şerit arası 36 yarık (araba geçer) · uçları açık (kızaklar örtünün ucuna 9 mm yaklaşır)",
                      "arabanın olmadığı yerde rayı örter; şerit başına 12 × M4 havşa") if (ad_, _y26) == ("on", "a") else None)''')
degis('''    ekle("acici_kolonu", kut(AC_X - 60.0, AC_X + 60.0, 0.0, 612.0, -660.0, -610.0)
         .union(kut(AC_X - 45.0, AC_X + 45.0, 582.0, 612.0, -660.0, -505.0)), "sac",''',
      '''    _t26 = 4.0                                                                                   # v26: kutu profil et kalınlığı [VARSAYIM · katalog]
    _kol26 = kut(AC_X - 60.0, AC_X + 60.0, 0.0, 612.0, -660.0, -610.0).cut(kut(AC_X - 60.0 + _t26, AC_X + 60.0 - _t26, -1.0, 613.0, -660.0 + _t26, -610.0 - _t26))
    _kol26 = _kol26.union(kut(AC_X - 60.0 + _t26, AC_X + 60.0 - _t26, 0.0, 10.0, -660.0 + _t26, -610.0 - _t26))     # alt uç plakası 10 (içeride, kaynaklı, 4 × M10 dişli)
    ekle("acici_kolonu", _kol26
         .union(kut(AC_X - 45.0, AC_X + 45.0, 582.0, 612.0, -660.0, -505.0)), "sac",''')
degis('bom=("Açıcı kolonu", 1, "304 kutu profil 120 × 50 · boy 612 + üst kol 90 × 30 × 155 · tabana (kaide A) 4 × M10",',
      'bom=("Açıcı kolonu", 1, "304 kutu profil 120 × 50 × 4 (et VARSAYIM) · boy 612 · içte 10 mm alt uç plakası (4 × M10 dişli) + üst kol 90 × 30 × 155 kaynaklı · tabana (kaide A) alttan 4 × M10 · Z rayları ön duvara M4 perçin somunla",')
# dünya denetimi montaj v69'un gördüğü soğuk paketle: topping_uno_cad_v15 (sucuk_cad_v8) — adlar TU:sucuk_cad_v8__… (kaset çekme taraması boş kalmasın)
degis('TU_DOSYA = os.environ.get("TOPPING_TU", "topping_uno_cad_v14.py")', 'TU_DOSYA = os.environ.get("TOPPING_TU", "topping_uno_cad_v15.py")')
n7 = s.count("sucuk_cad_v7"); assert n7 == 5, n7
s = s.replace("sucuk_cad_v7", "sucuk_cad_v8")
degis('"""(ad, geçti, değer) listesi · TU v14 + TC v25 + itici v5 dünyada"""', '"""(ad, geçti, değer) listesi · TU v15 + TC v26 + itici v5 dünyada"""')
degis('# v25 · DÜNYA DENETİMİ (montajın gördüğü C istasyonu: TC v25 + TU v14 + itici)', '# v26 · DÜNYA DENETİMİ (montajın gördüğü C istasyonu: TC v26 + TU v15 + itici)')
compile(s, "topping_cad_v26.py", "exec")
io.open(os.path.join(U, "topping_cad_v26.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v26.py yazildi · %d satir" % s.count(NL))
