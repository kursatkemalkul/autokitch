# -*- coding: utf-8 -*-
"""kusbasi_cad_v2.py → sucuk_cad_v1.py · KÜP SUCUK KASETİ = KUŞBAŞI KASETİ (bütün parçalar birebir aynı). Değişen yalnız ÜRÜN: yoğunluk, 2 günlük stok,
porsiyon (70 g), devir ve görseldeki küpler. Hesap: sucuk_akis_model_v1.py (aynı model, sucuğun sabitleriyle)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kusbasi_cad_v2.py"), encoding="utf-8").read(); n = [0]
def rep(a, b):
    global s
    assert a in s, "BULUNAMADI: " + a[:110]
    s = s.replace(a, b, 1); n[0] += 1

for a, b in (("kusbasi_kaseti_v2", "sucuk_kaseti_v1"), ("KUSBASI_KASETI_v2", "SUCUK_KASETI_v1"), ("kusbasi_v2", "sucuk_v1"), ("kusbasi_cad_v2", "sucuk_cad_v1"),
             ("kusbasi_akis_model_v2 as AM", "sucuk_akis_model_v1 as AM"), ("import kusbasi_akis_model_v2 as KM", "import sucuk_akis_model_v1 as KM")):
    s = s.replace(a, b)
i = s.index('"""'); j = s.index('"""', i + 3) + 3
s = s[:i] + '''"""AUTOKITCH · KÜP SUCUK KASETİ v1 — (22 Eyl 2026) · kusbasi_cad_v2'den türetildi (yap_sucuk_v1.py)
Kemal: "sucuk için de küp sucuk kullanalım, ona da hazne yap, ortak olursa ne güzel; ama tüm matematiği yeniden kur."
PARÇALAR KUŞBAŞI KASETİ v2 İLE BİREBİR AYNI (kontrol listesi hacimle doğrular) → aynı STEP/STL'den basılır. Ayrı olan yalnız ÜRÜN ve HESABI:
  küp 8 mm (VARSAYIM; pizzalık küp pepperoni 5–10 mm, MIL-DTL-32541) · 70 g / pide · 20 pide/gün → 2 gün 2,8 kg · dökme 0,60 g/mL (VARSAYIM)
  doluluk 0,60 → ≈ 53 g/tur · 70 g = 1,3 tur · ≈ 8 dev/dk. Dilimleyici (14 çubuk + bıçak) yerine geçer: bıçak yok, sayma yok, hazne ortak.
ÇIKTI: otonom/kaset3d/sucuk_v1.glb/.usdz + sucuk_v1_dozaj.glb · arastirma/3_TOPPING/sucuk_kaseti_v1/
"""''' + s[j:]
rep("RHO = 0.80", "RHO = 0.60")
rep("KG2 = 5.8 ", "KG2 = 2.8 ")
rep("MALZEME.setdefault('kusbasi', dict(renk=(0.55, 0.17, 0.16, 1.0)", "MALZEME.setdefault('sucuk', dict(renk=(0.66, 0.20, 0.10, 1.0)")
rep("MALZEME.setdefault('kusbasi_dolgu', dict(renk=(0.55, 0.17, 0.16, 1.0)", "MALZEME.setdefault('sucuk_dolgu', dict(renk=(0.66, 0.20, 0.10, 1.0)")
rep("aci=lambda t: -2.1 * min(t, T_DOK) / T_DOK)", "aci=lambda t: -1.3 * min(t, T_DOK) / T_DOK)")                      # 70 g = 1,3 tur
rep('print("MODEL = CAD · on uc %.1f mL/tur (Roberts) · doluluk 0,60 VARSAYIM → %.0f g/tur · 145 g = %.2f tur · %.0f dev/dk" % (q_on, g_tur, 145.0 / g_tur, 145.0 / g_tur * 6.0))',
    'print("MODEL = CAD · on uc %.1f mL/tur (Roberts) · doluluk 0,60 VARSAYIM → %.0f g/tur · 70 g = %.2f tur · %.0f dev/dk" % (q_on, g_tur, 70.0 / g_tur, 70.0 / g_tur * 6.0))')
rep('doku_ad("KUŞBAŞI KASETİ",', 'doku_ad("KÜP SUCUK KASETİ",')
rep("rnd = random.Random(11); ks = Mesh(); d_k = 10.0", "rnd = random.Random(11); ks = Mesh(); d_k = 8.0")
rep("# pide üstünde 137 küp (145 g · d 10)", "# pide üstünde 137 küp (70 g · d 8)")
s = s.replace('"kusbasi_pide_ustu", ks, "kusbasi", "tabla"', '"sucuk_pide_ustu", ks, "sucuk", "tabla"').replace('("kusbasi_dusen", dk, "kusbasi", None)', '("sucuk_dusen", dk, "sucuk", None)').replace('("kusbasi_dolgu", dolgu, "kusbasi_dolgu", None)', '("sucuk_dolgu", dolgu, "sucuk_dolgu", None)')
assert '"sucuk_dolgu", dolgu' in s and "kusbasi" not in s.replace("kusbasi_cad_v2'den", "").replace("KUŞBAŞI", ""), [x for x in s.split() if "kusbasi" in x][:5]
io.open(os.path.join(U, "sucuk_cad_v1.py"), "w", encoding="utf-8").write(s); print("sucuk_cad_v1.py yazildi ·", n[0], "yama")
