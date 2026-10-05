# -*- coding: utf-8 -*-
"""h3/hat3_montaj_v3.py (v3.3) → h3/hat3_montaj_v4.py (HAT v3.4 · 1 Eki 2026 · Claude · YEREL) — metin yaması, her değişiklik sayısı denetlenir.
Kemal 1 Eki ("v3 ile devam · eksikleri bitir · açıcı motorunun kablosu vs kaldır, üstteki rafı kaldır, bu kutu temiz kalsın ki satın alıp içine koyacağız ·
harç borusu düz insin, sola taşı · alt kısım ayaklıkların içinden geçsin, zemine gömme yok · E'nin sağından yukarı giden kanalı sil · her şey kendi istasyonunda mı"):
  · A: açıcı GÖRSEL KALIR (Kemal: "açıcıya dokunma") · hava hortumu + rakorları kalkar · A tavan sacı + U_A taban sacı ortası açılır (çerçeve içi, 40'lık kenar) → A + U_A tek kutu 788–2200
  · TOPPING harç UNO'su 87 sola (h3_topping_v1 içinde) · robot kablosu zemin üstünde (h3_ray_ek_v2) · elektrik katmanı h3/_elk önbelleğinden (zemin üstü, iç güzergâh)
  · ELK_GECICI=1 ortam değişkeni: eski elektrik önbelleğiyle ara montaj (silinen parçalara düşen delikler atlanır) — yalnız yeni dünya dökümü için."""
import io, os, runpy
H3 = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(H3, "yap_hat3_montaj_v3.py"))                     # önce v3.3 (hat3_montaj_v3.py)
s = io.open(os.path.join(H3, "hat3_montaj_v3.py"), encoding="utf-8").read()
N = [0]


def rep(a, b, n=None):
    global s
    c = s.count(a)
    assert c >= 1 and (n is None or c == n), (a[:100], c)
    s = s.replace(a, b); N[0] += 1


rep("hat3_v3", "hat3_v4")
rep('surum="v3.3"', 'surum="v3.4"', 1)
# ---- açıcı mekanizması modelden çıkar (hazır satın alınır, A boş kutu) ----
rep('V1_CIKAN = ("pu_", ', 'V1_CIKAN = ("hava_hatti_acici", "rakor_hava_acici", "pu_", ', 1)        # Kemal: açıcıya dokunma (görsel kalır) · yalnız hava hortumu + rakorları kalkar
# ---- A tavan sacı + U_A taban sacı: çerçeve içi açılır (raf kalkar) ----
_AC = '''
def _v34_ac(PL_, ad_, x0_=770.0, x1_=1402.0, z0_=-796.0, z1_=7.0):           # v3.4 · Kemal: "üstteki rafı kaldır, bu kutu temiz kalsın"
    for p_ in PL_:
        if p_["ad"] == ad_:
            s_ = p_["wp"].val() if hasattr(p_["wp"], "val") else p_["wp"]; b_ = s_.BoundingBox()
            p_["wp"] = cq.Workplane(obj=s_.cut(cq.Solid.makeBox(x1_ - x0_, b_.ylen + 2.0, z1_ - z0_, cq.Vector(x0_, b_.ymin - 1.0, z0_))))
            return True
    raise AssertionError("v3.4 · açılacak sac yok: " + ad_)
'''
rep("AK.kur()\n", "AK.kur()\n" + _AC + 'AK.PARCALAR[:] = [p_ for p_ in AK.PARCALAR if p_["ad"] != "a_govde_ust_omega"]; _v34_ac(AK.PARCALAR, "a_govde_ust")   # v3.4 · A tek temiz kutu\n', 1)
rep("UD.kur()\n", 'UD.kur()\n_v34_ac(UD.PARCALAR, "ust_a_taban_sac")                                          # v3.4 · U_A rafı kalktı (A ile tek kutu)\n', 1)
# ---- elektrik delikleri: C kaidesi de kesilir (ana besleme kaideden geçer) ----
rep('"FT": ("F_TP10",)}', '"FT": ("F_TP10",), "KD": ("KAIDE_",)}', 1)
# ---- QR alt servis kapağı + alt menteşesi düşer (yerine h3_elk_qr_v1'de kısa kapak + alt ön bant · ara montajda eski önbellek düşürmüyordu) ----
rep("_ELK_DUS = set(_a32 for _m32, _a32 in EL.DUSUR)", '_ELK_DUS = set(_a32 for _m32, _a32 in EL.DUSUR) | {"servis_kapagi_alt", "servis_mentesesi_0"}', 1)
# ---- robot kablosu zemin üstünde (gömme kanal yok) ----
rep("h3_ray_ek_v1 as RE", "h3_ray_ek_v2 as RE", 1)
rep('_dis_birim(RE, "GERCEK_RAY", "ray_ek_cad_v1.py"', '_dis_birim(RE, "GERCEK_RAY", "h3_ray_ek_v2.py"', 1)
# ---- ara montaj (eski elektrik önbelleği): silinen parçalara düşen delikler atlanır ----
rep('    assert not _eksik32, _eksik32', '    assert not _eksik32 or os.environ.get("ELK_GECICI"), _eksik32', 1)
rep('pafta="HAT v3.3 (1 Eki · Claude · YEREL): ', 'pafta="' + os.environ.get("V34_PAFTA", "HAT v3.4 (1 Eki · Claude · YEREL): ARA") + ' || HAT v3.3 (1 Eki · Claude · YEREL): ', 1)
assert "import os" in s or "\nimport os" in s or "import io, os" in s or ", os" in s
io.open(os.path.join(H3, "hat3_montaj_v4.py"), "w", encoding="utf-8").write(s)
print("hat3_montaj_v4.py yazıldı · %d yama" % N[0])
