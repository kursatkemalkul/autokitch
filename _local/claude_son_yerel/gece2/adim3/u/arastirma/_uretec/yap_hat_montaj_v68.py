# -*- coding: utf-8 -*-
"""hat_montaj_v67 → hat_montaj_v68 (28 Eyl 2026) — ÇIPLAK SÜZGEÇ KALKTI (Kemal: "çekmecelerin bazı yerinde yalıtım malzemesi görünmüyor ya da eksik,
tam dönmüyor, temiz olmalı" · v67'de: "ön kapaklar dışında her şey normal olsun").
  · v51'in görsel süzgeci (CIPLAK: "önce sistemleri görelim") GLB/USDZ'den 22 GERÇEK parçayı düşürüyordu: dolabın arka PU'su (arka_pu_37.5 · arka_pu_F),
    sol yan PU'su (yan_pu_sol · yan_pu_sol_on), arka dış/iç sacları, sol iç sacı; K ve E'nin yan / arka / üst sacları; E şarjör yan kapısı; fırın taş yünü.
    Üst, alt ve bölme PU'ları görünürken arka ve sol yok → yalıtım "tam dönmüyor" görünüyordu. v68: süzgeç KAPALI, bütün gerçek parçalar modelde.
  · "kabuk" malzemesi (K ve E'nin dış sacı · 304 1,5) opak paslanmaz: kutu_cad_v7 / TU'da yarı saydam tanımlıydı (0,14 / 0,06) — süzgeç yüzünden görünmüyordu.
  · Kabin / etek ZARF kutuları (A_KABIN, TOPPING_MODUL, B_KASA, *_KABIN yer tutucuları) yine çizilmez (süzgeçten bağımsız) — şu an 0 adet.
  · Denetimler v67 ile aynı (zaten gerçek parçalarla koşuyordu). Çıktılar hat_v68. Tesisat + raf yükleri ayrı sürümü artık v69."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v67.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""v67 (28 Eyl 2026):',
      '"""v68 (28 Eyl 2026): ÇIPLAK SÜZGEÇ KALKTI — dolabın arka + sol yalıtımı/sacları, K ve E yan-arka-üst sacları, E şarjör kapısı, fırın taş yünü modelde; '
      '"kabuk" opak · çıktılar hat_v68.' + NL + 'v67 (28 Eyl 2026):')
degis('pafta="HAT v67 (28 Eyl) ·',
      'pafta="HAT v68 (28 Eyl) · CIPLAK SUZGEC KALKTI (dolap arka + sol yalitim ve saclar, K / E yan-arka-ust saclari, sarjor kapisi, firin tas yunu modelde; kabuk opak) · v67:')
degis('print("ALCAK HAT SOZLESMESI (v67 ·', 'print("ALCAK HAT SOZLESMESI (v68 ·')
for a_ in ("hat_v67.glb", "hat_v67.usdz", '"hat_v67"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v67", "v68"))

# çıplak süzgeç kapalı · zarf kutuları süzgeçten bağımsız atlanır
degis("CIPLAK = True", "CIPLAK = False                                                                   # v68: süzgeç KAPALI (Kemal: yalıtım tam dönmeli, her şey normal)")
degis('            if CIPLAK and (b["kod"] in CIPLAK_KUTU or b["kod"].endswith("_KABIN")):',
      '            if b["kod"] in CIPLAK_KUTU or b["kod"].endswith("_KABIN"):                      # v68: zarf kutusu süzgeçten bağımsız çizilmez')
# "kabuk" (K / E dış sacı 304 1,5) opak — TU ve kutu_cad_v7'deki yarı saydam tanımın önüne geçer (sonraki setdefault'lar ezmez)
degis('MALZEME["ayirma_saci"] = dict(renk=(0.18, 0.36, 0.92, 1.0), met=0.3, ruf=0.4, saydam=False)',
      'MALZEME["kabuk"] = dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32, saydam=False)            # v68: dış sac 304 1,5 opak (süzgeç kalkınca görünür)' + NL +
      'MALZEME["ayirma_saci"] = dict(renk=(0.18, 0.36, 0.92, 1.0), met=0.3, ruf=0.4, saydam=False)')
compile(s, "hat_montaj_v68.py", "exec")
io.open(os.path.join(U, "hat_montaj_v68.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v68.py yazildi · %d satir" % s.count(NL))
