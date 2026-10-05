# -*- coding: utf-8 -*-
"""hat_montaj_v68 → hat_montaj_v69 (28 Eyl 2026) — ÜRETİM DÜZELTMELERİ (katı denetimi denetim_kati_v1.py · Kemal: "düzelt, onaylıyorum yap").
  · B = store_cad_v9: kapak iç sacı tek parça (kanal dışı halka = dış sacın arka dönüşü) · ısı kalkanı sol sacı tek parça (x 2534)
  · C = topping_uno_cad_v15 (TOPPING kapak iç sacı tek parça · sucuk_cad_v8) + topping_cad_v26 (açıcı kolonu 120 × 50 × 4 kutu profil · ray örtüsü 4 ayrı L şerit)
  · E = kutu_cad_v8: kapak masası açıkça iki levha (kol yarığı boydan boya; kol β 0…144°)
  · kaset = sucuk_cad_v8 (örümcek kaynak yakaları kola bitişik) · Codex STEP'lerindeki ayrık kırıntılar (< binde 1 hacim) atılır
Montajın kendisi (yerleşim, kotlar, animasyonlar, denetimler) v68 ile aynı. Çıktılar hat_v69. Tesisat + raf yükleri ayrı sürümü artık v70."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v68.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""v68 (28 Eyl 2026):',
      '"""v69 (28 Eyl 2026): ÜRETİM DÜZELTMELERİ — store_cad_v9 · topping_uno_cad_v15 · topping_cad_v26 · kutu_cad_v8 · sucuk_cad_v8 · Codex STEP kırıntıları atılır · '
      'bütün parçalar tek gövde / gerçek profil (denetim_kati) · çıktılar hat_v69.' + NL + 'v68 (28 Eyl 2026):')
degis('pafta="HAT v68 (28 Eyl) ·',
      'pafta="HAT v69 (28 Eyl) · URETIM DUZELTMELERI (kapak ic saclari tek parca, isi kalkani saci tek parca, acici kolonu kutu profil, ray ortusu 4 serit, kapak masasi 2 levha, '
      'sucuk orumcegi tek parca) · v68:')
degis('print("ALCAK HAT SOZLESMESI (v68 ·', 'print("ALCAK HAT SOZLESMESI (v69 ·')
for a_ in ("hat_v68.glb", "hat_v68.usdz", '"hat_v68"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v68", "v69"))
# yeni modül sürümleri (kod + birim kaynak etiketleri)
for eski, yeni, n in (("store_cad_v8", "store_cad_v9", 16), ("kutu_cad_v7", "kutu_cad_v8", 13), ("topping_uno_cad_v14", "topping_uno_cad_v15", 7),
                      ("topping_cad_v25", "topping_cad_v26", 3), ("sucuk_cad_v7", "sucuk_cad_v8", 1)):
    c = s.count(eski); assert c == n, (eski, c)
    s = s.replace(eski, yeni)
# Codex STEP kırıntıları
degis('        yeni_sh = cq.importers.importStep(os.path.join(KOK, "arastirma", "3_TOPPING", yol))',
      '        yeni_sh = cq.importers.importStep(os.path.join(KOK, "arastirma", "3_TOPPING", yol))\n'
      '        _ss69 = sorted(yeni_sh.solids().vals(), key=lambda s_: -s_.Volume())                               # v69: STEP\'teki ayrık kırıntılar (< binde 1) atılır\n'
      '        if len(_ss69) > 1 and all(s_.Volume() < 1e-3 * _ss69[0].Volume() for s_ in _ss69[1:]):\n'
      '            yeni_sh = cq.Workplane(obj=_ss69[0])')
compile(s, "hat_montaj_v69.py", "exec")
io.open(os.path.join(U, "hat_montaj_v69.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v69.py yazildi · %d satir" % s.count(NL))
