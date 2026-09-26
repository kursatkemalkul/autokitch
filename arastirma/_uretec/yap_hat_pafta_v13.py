# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v12 → v13: pafta = montaj v47 (kural 6.5: model değiştiği gün pafta eşitlenir).
Değişen: TOPPING topping_cad_v23 — aktarma bandının motoru bandın ARKASINDA (tahrik silindiriyle eş eksenli; v22'de ön yüzün
78 mm önündeydi), ön yan sac + mil uçları + fire sileceği ön yüzün içinde, çıkış yarığı 294 × 44. Çizimin geri kalanı v12 ile aynı."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v12.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


degis("TEKNİK RESİM  v12  ·  MONTAJ = hat_montaj_v45  ·", "TEKNİK RESİM  v13  ·  MONTAJ = hat_montaj_v47  ·")
degis("+ topping_cad_v22 tabla ·", "+ topping_cad_v23 tabla ·")
degis('"itici ve köprü YOK · Ø60 kauçuk tahrik silindiri + PTFE kaplı cam elyaf bant"',
      '"itici ve köprü YOK · Ø60 kauçuk tahrik silindiri + PTFE kaplı cam elyaf bant · v13: bant motoru ARKADA, tahrik silindiriyle eş eksenli · ön sac + mil uçları ön yüzün içinde · çıkış yarığı 294 × 44"')
degis('    yol = KLASOR + r"\\HAT_ATOSA_TABLALI_v12_HD.png"', '    yol = KLASOR + r"\\HAT_ATOSA_TABLALI_v13_HD.png"')
degis('k.save(KLASOR + r"\\HAT_ATOSA_TABLALI_v12_EKRAN.png", optimize=True)', 'k.save(KLASOR + r"\\HAT_ATOSA_TABLALI_v13_EKRAN.png", optimize=True)')
io.open(os.path.join(U, "teknik_hat_atosa_tablali_v13.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v13.py yazildi")
