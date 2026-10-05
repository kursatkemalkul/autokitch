# -*- coding: utf-8 -*-
"""h3/hat3_montaj_v7.py (v3.7) → h3/hat3_montaj_v8.py (HAT v3.8 TASLAK · 2 Eki 2026 · Claude · YEREL) — metin yaması, her değişiklik sayısı denetlenir.
Kemal 2 Eki (resim 48): "bu ne, bunu kaldır dememiş miydik; burası boş olmalı, burada çıtalara gerek yok, boş tutacaktık"
  · A ile U_A arasındaki (y 1830–1894) bütün ara çerçeve kalkar: A üst kuşakları (arka/sol/sağ), ön üst kayıt, A tavan sacının kalan çerçevesi,
    U_A taban sacının kalan çerçevesi, U_A ön alt kayıt → A + U_A 788–2200 tek boş kutu (v3.4'te yalnız sacların ortası açılmıştı).
TASLAK (Kemal 2 Eki kuralı): elektrik / havada / boşluk / envanter denetimleri bu turda ÇALIŞMAZ (taslak_zincir.sh, ELK_GECICI=1)."""
import io, os, runpy, sys
H3 = os.path.dirname(os.path.abspath(__file__))
if H3 not in sys.path: sys.path.insert(0, H3)
runpy.run_path(os.path.join(H3, "yap_hat3_montaj_v7.py"), run_name="__yap__")     # önce v3.7 (hat3_montaj_v7.py)
s = io.open(os.path.join(H3, "hat3_montaj_v7.py"), encoding="utf-8").read()
N = [0]


def rep(a, b, n=None):
    global s
    c = s.count(a)
    assert c >= 1 and (n is None or c == n), (a[:100], c)
    s = s.replace(a, b); N[0] += 1


rep("hat3_v7", "hat3_v8")
rep('surum="v3.7"', 'surum="v3.8"', 1)
# ---- A ↔ U_A ara çerçevesi kalkar (A + U_A tek boş kutu) ----
_A38 = ("a_govde_ust", "a_ust_kusak_arka", "a_ust_kusak_sol", "a_ust_kusak_sag", "onyuz_cerceve_ust_kayit")
_U38 = ("ust_a_taban_sac", "onyuz_ust_a_alt_kayit")
rep('_v34_ac(AK.PARCALAR, "a_govde_ust")   # v3.4 · A tek temiz kutu\n',
    '_v34_ac(AK.PARCALAR, "a_govde_ust")   # v3.4 · A tek temiz kutu\n'
    '_n38 = len(AK.PARCALAR); AK.PARCALAR[:] = [p_ for p_ in AK.PARCALAR if p_["ad"] not in %r]; assert _n38 - len(AK.PARCALAR) == %d, ("v3.8 A ara çerçeve", _n38 - len(AK.PARCALAR))   # v3.8 · Kemal: A–U_A arası boş (çıtalar kalktı)\n' % (_A38, len(_A38)), 1)
rep('_v34_ac(UD.PARCALAR, "ust_a_taban_sac")',
    '_v34_ac(UD.PARCALAR, "ust_a_taban_sac"); _n38 = len(UD.PARCALAR); UD.PARCALAR[:] = [p_ for p_ in UD.PARCALAR if p_["ad"] not in %r]; assert _n38 - len(UD.PARCALAR) == %d, ("v3.8 U_A ara çerçeve", _n38 - len(UD.PARCALAR))   # v3.8 · Kemal: A–U_A arası boş' % (_U38, len(_U38)), 1)
# ---- v3.8b (Kemal 2 Eki, resim 49–50): A + U_A tek kutu · dikmeler ve sol/arka sac tavana · açıcı elektriği yok · perde kaydı + U_A tavan kirişi kalkar · omega hizası ----
_B38 = '''
def _v38_uzat(PL_, ad_, y1_):                                                           # v3.8b · parçayı üst yüzünden y1_'e uzatır (aynı x/z kesiti)
    for p_ in PL_:
        if p_["ad"] == ad_:
            s_ = p_["wp"].val() if hasattr(p_["wp"], "val") else p_["wp"]; b_ = s_.BoundingBox()
            p_["wp"] = cq.Workplane(obj=s_.fuse(cq.Solid.makeBox(b_.xlen, y1_ - b_.ymax + 0.01, b_.zlen, cq.Vector(b_.xmin, b_.ymax - 0.01, b_.zmin))).clean())
            return
    raise AssertionError("v3.8b · uzatılacak parça yok: " + ad_)
for _a38, _y38 in (("a_govde_sol_yan", 2178.5), ("a_govde_arka", 2200.0), ("a_kose_dikmesi_arka_sol", 2178.5), ("a_kose_dikmesi_arka_sag", 2178.5),
                   ("onyuz_cerceve_sol_dikme", 2168.5), ("onyuz_cerceve_sag_dikme", 2168.5)):
    _v38_uzat(AK.PARCALAR, _a38, _y38)
for p_ in AK.PARCALAR:                                                                   # v3.8b · sol yan omega arka omegayla aynı hizaya (1325 → 1280)
    if p_["ad"] == "a_govde_sol_yan_omega":
        p_["wp"] = cq.Workplane(obj=(p_["wp"].val() if hasattr(p_["wp"], "val") else p_["wp"]).translate(cq.Vector(0, -45.0, 0)))
_n38 = len(AK.PARCALAR); AK.PARCALAR[:] = [p_ for p_ in AK.PARCALAR if not (p_["ad"] == "onyuz_cerceve_perde_kayit" or p_["ad"].startswith(("onyuz_isik_perdesi", "onyuz_emniyet")))]
def _v38_boy(PL_, ad_, y0_, y1_):                                                       # v3.8c · parçayı aynı x/z kesitiyle y0_–y1_ boyuna getirir (aşağı/yukarı uzatma)
    for p_ in PL_:
        if p_["ad"] == ad_:
            s_ = p_["wp"].val() if hasattr(p_["wp"], "val") else p_["wp"]; b_ = s_.BoundingBox()
            p_["wp"] = cq.Workplane(obj=s_.fuse(cq.Solid.makeBox(b_.xlen, y1_ - y0_, b_.zlen, cq.Vector(b_.xmin, y0_, b_.zmin))).clean())
            return
    raise AssertionError("v3.8c · parça yok: " + ad_)
AK.PARCALAR[:] = [p_ for p_ in AK.PARCALAR if p_["ad"] not in ("onyuz_cerceve_sol_alt_dikme", "onyuz_cerceve_sag_alt_dikme", "onyuz_cerceve_ara_lama_sol", "onyuz_cerceve_ara_lama_sag", "onyuz_cerceve_ara_lama_orta")]
_v38_boy(AK.PARCALAR, "onyuz_cerceve_sol_dikme", 788.0, 2168.5); _v38_boy(AK.PARCALAR, "onyuz_cerceve_sag_dikme", 788.0, 2168.5)   # v3.8c · ön dikmeler kesintisiz 788–2168,5 (basamak yok)
_v38_boy(AK.PARCALAR, "onyuz_cerceve_alt_kayit", 788.0, 893.5)                       # v3.8c · alt kayıt kaide yüksekliği boyunca düz ön bant (z 39–59, dikmeler arası)
print("v3.8b · A: perde kaydı + ışık perdesi + emniyet sensörü/hedefi kalktı: %d parça" % (_n38 - len(AK.PARCALAR)))
'''
rep('# v3.8 · Kemal: A–U_A arası boş (çıtalar kalktı)\n', '# v3.8 · Kemal: A–U_A arası boş (çıtalar kalktı)\n' + _B38, 1)
rep('_n38 - len(UD.PARCALAR))   # v3.8 · Kemal: A–U_A arası boş',
    '_n38 - len(UD.PARCALAR))   # v3.8 · Kemal: A–U_A arası boş\nUD.PARCALAR[:] = [p_ for p_ in UD.PARCALAR if p_["ad"] not in ("ust_a_yan_sol", "ust_a_arka_sac", "ust_a_tavan_kirisi_0")]   # v3.8b · A sol/arka sacı tavana çıktı, U_A kirişi kalktı', 1)
# not: açıcı elektriği (A istasyon kutusu + Harting + TOPPING x sol limit / x sıfır kabloları) h3_elk_* kaynaklarından FİNAL elektrik turunda kaldırılacak (Kemal 2 Eki: elektrik final)
V38 = ("HAT v3.8 TASLAK (2 Eki · Claude · YEREL): A ↔ U_A ara çerçevesi (üst kuşaklar, ön kayıtlar, tavan/taban sac çerçeveleri) KALKTI — A + U_A 788–2200 tek boş kutu (Kemal) · "
       "elektrik/havada/boşluk denetimleri bu turda ÇALIŞMADI (taslak) || ")
rep('pafta="HAT v3.7 (', 'pafta="' + V38 + 'HAT v3.7 (', 1)
compile(s, "hat3_montaj_v8", "exec")
io.open(os.path.join(H3, "hat3_montaj_v8.py"), "w", encoding="utf-8").write(s)
print("hat3_montaj_v8.py yazıldı · %d yama" % N[0])
