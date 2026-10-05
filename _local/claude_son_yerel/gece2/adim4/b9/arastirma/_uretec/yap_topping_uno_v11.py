# -*- coding: utf-8 -*-
"""topping_uno_cad_v10 → v11 (27 Eyl 2026): YALITIM YALNIZ SOĞUK HACMİ SARAR (Kemal: "tamam yalıtım sadece hacmi sarsın").
Teknik cep (soğutma grubu · pano · güç · UPS) yalıtımın DIŞINDA: x 820–1800 · y 1720–2028, kabuğu saç (sağ üst yan saç + üst saç, havalandırma
ızgaralı), arkası açık. Soğuk hacim ↔ teknik cep: 30 mm PU (L: yatay y 1690–1720 · dikey x 790–820) + teknik tarafta 1,5 mm saç.
Yalıtım parçaları: A tavanı 1968–2028 · L PU 30 · arka bölme (A 1277–1968 · B 1277–1690) · sağ yan PU yalnız 1277–1720 (üstü teknik cep).
Isı kaçağı soğuk ↔ teknik: PU 30 (λ 0,024) U ≈ 0,8 W/m²K · 0,55 m² · ΔT 32 K ≈ 14 W (ince saçla ≈ 65 W idi). Teknik zarflar 1731,5'ten."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v10.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
d('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v10 · 27 Eyl 2026 (v9 + YALITIM TEK DİKDÖRTGEN: B tavanı 1680 dilimi kalktı, teknik cep ince saçla ayrıldı — Kemal)',
  '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v11 · 27 Eyl 2026 (v10 + YALITIM YALNIZ SOĞUK HACMİ SARAR, teknik cep dışarıda — Kemal)' + NL +
  'v11: yalıtım A tavanı + L PU 30 (soğuk ↔ teknik) + arka bölme + sağ yan 1277–1720; teknik cep x 820–1800 · y 1720–2028 saç kabuklu, havalandırmalı, arkası açık. Önceki: topping_uno_cad_v10.py' + NL +
  'v10 (27 Eyl):')
d('SAC_T = 1.5; TEK_Y0 = TAVAN_B + SAC_T + 10.0                                      # v10: ince ayırma saçı · teknik bant zarflarının altı 1701,5',
  'SAC_T = 1.5; PU_L = 30.0                                                            # v11: soğuk ↔ teknik PU levha 30' + NL +
  'Y_TEK = TAVAN_B + PU_L; X_TEK = BAY_A[1] + PU_L                                    # v11: teknik cep tabanı 1720 · sol duvarı 820' + NL +
  'TEK_Y0 = Y_TEK + SAC_T + 10.0                                                      # v11: teknik bant zarflarının altı 1731,5')
d('ekle("kabin_sag_duvar_PU", kut(W - 90, W, 1277.0, YUST, 0, -D), "pu", "V", not_="v7: 1277\'den başlar (disk aktarmada 2507\'ye kadar çıkar)")',
  'ekle("kabin_sag_duvar_PU", kut(W - 90, W, 1277.0, Y_TEK, 0, -D), "pu", "V", not_="v11: yalnız soğuk hacim yüksekliği 1277–1720 (üstü teknik cep, yalıtımsız)")' + NL +
  'ekle("kabin_sag_teknik_sac", kut(W - 1.5, W, Y_TEK, YUST, 0, -D), "kabuk", "V", not_="v11: teknik cebin sağ yan saçı · havalandırma ızgaralı (kondenser havası)")')
d('''_yal = kut(BAY_A[0], BAY_B[1], YAL_Y0, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1])
_yal = _yal.cut(kut(BAY_A[0] - 1, BAY_A[1], YAL_Y0 - 1, TAVAN_A, Z_KAPAK[1] + 1, Z_BOLME[0]))          # soğuk oda A
_yal = _yal.cut(kut(BAY_B[0], BAY_B[1] + 1, YAL_Y0 - 1, TAVAN_B, Z_KAPAK[1] + 1, Z_BOLME[0]))          # soğuk oda B
_yal = _yal.cut(kut(CEP_TEKNIK[0], CEP_TEKNIK[1] + 1, CEP_TEKNIK[2], CEP_TEKNIK[3], CEP_TEKNIK[4], CEP_TEKNIK[5] - 1))   # teknik cep (arkaya açık)''',
  '''# v11 · YALITIM YALNIZ SOĞUK HACMİ SARAR (Kemal): A tavanı · L PU 30 (soğuk ↔ teknik) · arka bölme — teknik cep yalıtımın DIŞINDA
_yal = kut(BAY_A[0], BAY_A[1], TAVAN_A, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1])                             # A tavanı 60
_yal = _yal.union(kut(BAY_A[1], X_TEK, TAVAN_B, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1]))                   # L dikey PU 30 (A | teknik)
_yal = _yal.union(kut(X_TEK, BAY_B[1], TAVAN_B, Y_TEK, Z_KAPAK[1], Z_BOLME[1]))                        # L yatay PU 30 (B tavanı)
_yal = _yal.union(kut(BAY_A[0], BAY_A[1], YAL_Y0, TAVAN_A, Z_BOLME[0], Z_BOLME[1]))                    # arka bölme A
_yal = _yal.union(kut(BAY_A[1], BAY_B[1], YAL_Y0, TAVAN_B, Z_BOLME[0], Z_BOLME[1]))                    # arka bölme B''')
d('CEP_TEKNIK = (BAY_A[1], W - 90, TAVAN_B, TAVAN_A, -110.0, Z_BOLME[1])              # v10: 790–1710 × 1690–1968 · soğuk hacme ince saçla açılır · arkadan servis',
  'CEP_TEKNIK = (X_TEK, W, Y_TEK, YUST, Z_KAPAK[1], -D)                                # v11: yalıtımın dışında · 820–1800 × 1720–2030 · arkası açık')
d('"zarf", "Ö", not_="v10 teknik cep (ince saçın üstü) · ZARF")', '"zarf", "Ö", not_="v11 teknik cep (yalıtımın dışında) · ZARF")')
d('''ekle("teknik_ayirma_saci_yatay", kut(BAY_A[1], BAY_B[1], TAVAN_B, TAVAN_B + SAC_T, -110.0, Z_BOLME[0]), "paslanmaz", "Ö",
     not_="1,5 mm AISI 304 · 920 × 455 · soğuk hacmin (B) tavanı · üstünde soğutma grubu / pano / güç / UPS (Kemal: ince saçla ayır)")
ekle("teknik_ayirma_saci_dikey", kut(BAY_A[1], BAY_A[1] + SAC_T, TAVAN_B + SAC_T, TAVAN_A, -110.0, Z_BOLME[0]), "paslanmaz", "Ö",
     not_="1,5 mm AISI 304 · 276,5 × 455 · soğuk oda A ile teknik cep arası")''',
  '''ekle("teknik_ayirma_saci_yatay", kut(X_TEK, W - 1.5, Y_TEK, Y_TEK + SAC_T, Z_KAPAK[1], Z_BOLME[1]), "paslanmaz", "Ö",
     not_="v11: 1,5 mm AISI 304 · teknik cebin tabanı, PU 30'un üstünde · üstünde soğutma grubu / pano / güç / UPS")
ekle("teknik_ayirma_saci_dikey", kut(X_TEK, X_TEK + SAC_T, Y_TEK + SAC_T, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1]), "paslanmaz", "Ö",
     not_="v11: 1,5 mm AISI 304 · teknik cebin sol duvarı, PU 30'un sağında")''')
d('     not_="v10 TEK DİKDÖRTGEN PU 60 (sac kaplı) · dışı 1620 × 751 × 526 düz · soğuk hacim tek parça: A tavan 1968 / B 1690 (ince saç) · teknik cep 790–1710 × 1690–1968 arkaya açık',
  '     not_="v11 YALNIZ SOĞUK HACMİ SARAR · PU (sac kaplı): A tavanı 60 · L 30 (soğuk ↔ teknik) · arka bölme 65 · soğuk hacim A tavan 1968 / B 1690 · teknik cep yalıtımın dışında')
s = s.replace('"generator": "AUTOKITCH topping_uno_cad_v10"', '"generator": "AUTOKITCH topping_uno_cad_v11"')
s = s.replace('"topping_uno_v10.glb"', '"topping_uno_v11.glb"').replace('"topping_uno_v10.json"', '"topping_uno_v11.json"').replace('surum="topping_uno_cad_v10 ·', 'surum="topping_uno_cad_v11 ·')
io.open(os.path.join(U, "topping_uno_cad_v11.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v11.py yazildi")
