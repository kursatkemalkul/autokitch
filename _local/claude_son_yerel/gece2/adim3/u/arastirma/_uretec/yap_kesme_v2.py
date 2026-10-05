# -*- coding: utf-8 -*-
"""kesme_cad_v1 → kesme_cad_v2 (27 Eyl 2026): ÖN KAPAKLAR YOK (Kemal: "kesme kısmına kapak koymuşsun, kapak vs yok şu anda").
Kaldırılan: taban kapısı + kulpu, PC pencereli üst kapı çerçevesi + pencere + kulp, AZM kapı kilidi, ön acil stop (kapaksız ön yüze
takılacak yeri yok; kapak istenirse kilit + acil stop birlikte gelir). Gerisi (bant, kesici + sprey kafası, çit, itici, tank, pano) aynı."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "kesme_cad_v1.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


d('"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v1 (25 Eyl 2026)',
  '"""AUTOKITCH · K · KESME + TEREYAĞI SPREYİ İSTASYONU — ÜRETİM MODELİ v2 (27 Eyl 2026): ÖN KAPAKLAR YOK (Kemal) — taban kapısı, PC pencereli\n'
  'üst kapı, kulplar, AZM kilidi ve ön acil stop kaldırıldı; ön yüz açık (TOPPING gibi: "kapaklar en son"). Önceki: kesme_cad_v1.py\n'
  'v1 (25 Eyl 2026):')
i0 = s.index("    # ön: taban kapısı + üst kapı (PC pencereli, kilitli)")
i1 = s.index("# ---------------------------------------------------------------- 2 · K BANDI")
s = s[:i0] + "    # v2: ÖN KAPAK YOK (Kemal 27 Eyl) — taban kapısı, PC pencereli üst kapı, kulplar, AZM kilit, acil stop kaldırıldı\n\n\n" + s[i1:]
d('print("DENETİM (kesme_cad_v1)")', 'print("DENETİM (kesme_cad_v2)")')
d('print("K KESME + SPREY v1: %d parca', 'print("K KESME + SPREY v2 (on kapak yok): %d parca')
d('"generator": "AUTOKITCH kesme_cad_v1"', '"generator": "AUTOKITCH kesme_cad_v2"')
d('surum="kesme_cad_v1 · %s"', 'surum="kesme_cad_v2 · %s"')
d('"otonom", "hat3d", "kesme_v1.glb")', '"otonom", "hat3d", "kesme_v2.glb")')
d('"arastirma", "4_KESME_v1")', '"arastirma", "4_KESME_v2")')
d('"otonom", "hat3d", "kesme_v1.json")', '"otonom", "hat3d", "kesme_v2.json")')
io.open(os.path.join(U, "kesme_cad_v2.py"), "w", encoding="utf-8").write(s)
print("kesme_cad_v2.py yazildi")
