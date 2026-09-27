# -*- coding: utf-8 -*-
"""topping_uno_cad_v9 → v10 (27 Eyl 2026): YALITIM KIRMIZI ÇİZGİ GİBİ (Kemal: "yalıtımı kırmızı çizdiğim gibi yap, daha düzgün olur; motor vs
teknik şeyleri de sadece ince bir saçla ayır, mavi çizdiğim gibi"). Soğuk oda B'nin 1680 tavanı (60 mm PU dilimi) KALKTI; soğuk hacim tek parça
(A 90–790 × 1277–1968 · B 790–1710 × 1277–1690). Teknik cep (soğutma grubu · pano · güç · UPS) x 790–1710 · y 1690–1968: soğuk hacimden yalnız
1,5 mm paslanmaz saçla ayrılır (yatay y 1690 + dikey x 790 = mavi L). Dış kabuk tek düz dikdörtgen: üst 1968–2028 · her yerde aynı 60 mm PU.
Teknik bant zarfları 1772 → 1701,5'e indi (pano 240 yüksek, üst 1941,5 ≤ 1968). Cep arkaya açık kalır (soğutma grubu havasını arkaya atar)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v9.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
d('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v9 · 27 Eyl 2026 (v8 − fitil boşluğu: fırın 79 öne, itici v3 düz → ön fitil yine TAM)',
  '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v10 · 27 Eyl 2026 (v9 + YALITIM TEK DİKDÖRTGEN: B tavanı 1680 dilimi kalktı, teknik cep ince saçla ayrıldı — Kemal)' + NL +
  'v10: soğuk hacim tek parça (B tavanı 1690 = ayırma saçı) · teknik cep x 790–1710 · y 1690–1968, soğuk hacimden 1,5 mm paslanmaz L saçla ayrılır · üst PU 1968–2028. Önceki: topping_uno_cad_v9.py' + NL +
  'v9 (27 Eyl): ön fitil TAM')
d("BAY_A = (90.0, 790.0); TAVAN_A = 1968.0; BAY_B = (790.0, 1710.0); TAVAN_B = 1680.0",
  "BAY_A = (90.0, 790.0); TAVAN_A = 1968.0; BAY_B = (790.0, 1710.0); TAVAN_B = 1690.0   # v10: B tavanı = teknik ayırma saçı (60 mm PU dilimi kalktı; kaset üstü 1680 + 10)" + NL +
  "SAC_T = 1.5; TEK_Y0 = TAVAN_B + SAC_T + 10.0                                      # v10: ince ayırma saçı · teknik bant zarflarının altı 1701,5")
d("CEP_TEKNIK = (850.0, W - 90, TAVAN_B + 60, 2012.0, -110.0, Z_BOLME[1])               # soğutma grubu · pano · güç · UPS (zarflar) — arkadan servis",
  "CEP_TEKNIK = (BAY_A[1], W - 90, TAVAN_B, TAVAN_A, -110.0, Z_BOLME[1])              # v10: 790–1710 × 1690–1968 · soğuk hacme ince saçla açılır · arkadan servis")
d('    ekle("teknik_bant_" + ad, kut(x0, x1, 1772, 2012 if ad == "pano_PLC" else 1992, -110, -560), "zarf", "Ö", not_="pafta v9 teknik bant · ZARF")',
  '    ekle("teknik_bant_" + ad, kut(x0, x1, TEK_Y0, TEK_Y0 + (240.0 if ad == "pano_PLC" else 220.0), -110, -560), "zarf", "Ö", not_="v10 teknik cep (ince saçın üstü) · ZARF")' + NL +
  '# v10 · TEKNİK AYIRMA SAÇI (mavi L): soğuk hacim ↔ teknik cep, 1,5 mm AISI 304 · kenarları yalıtım bloğuna silikonla' + NL +
  'ekle("teknik_ayirma_saci_yatay", kut(BAY_A[1], BAY_B[1], TAVAN_B, TAVAN_B + SAC_T, -110.0, Z_BOLME[0]), "paslanmaz", "Ö",' + NL +
  '     not_="1,5 mm AISI 304 · 920 × 455 · soğuk hacmin (B) tavanı · üstünde soğutma grubu / pano / güç / UPS (Kemal: ince saçla ayır)")' + NL +
  'ekle("teknik_ayirma_saci_dikey", kut(BAY_A[1], BAY_A[1] + SAC_T, TAVAN_B + SAC_T, TAVAN_A, -110.0, Z_BOLME[0]), "paslanmaz", "Ö",' + NL +
  '     not_="1,5 mm AISI 304 · 276,5 × 455 · soğuk oda A ile teknik cep arası")')
d('     not_="v6 TEK BLOK PU 60 (sac kaplı) · dışı 1620 × 751 × 526 düz · soğuk oda A tavan 1968 / B 1680 · teknik cep arkaya açık',
  '     not_="v10 TEK DİKDÖRTGEN PU 60 (sac kaplı) · dışı 1620 × 751 × 526 düz · soğuk hacim tek parça: A tavan 1968 / B 1690 (ince saç) · teknik cep 790–1710 × 1690–1968 arkaya açık')
s = s.replace('"generator": "AUTOKITCH topping_uno_cad_v9"', '"generator": "AUTOKITCH topping_uno_cad_v10"')
s = s.replace('"topping_uno_v9.glb"', '"topping_uno_v10.glb"').replace('"topping_uno_v9.json"', '"topping_uno_v10.json"').replace('surum="topping_uno_cad_v9 ·', 'surum="topping_uno_cad_v10 ·')
io.open(os.path.join(U, "topping_uno_cad_v10.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v10.py yazildi")
