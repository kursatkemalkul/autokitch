# -*- coding: utf-8 -*-
"""hat_montaj_v45 → v46: ana animasyonda dönen parçalar kendi ekseninde (pivot-yerel düğüm) · tabla_bos_sensoru sabit · 30 kare/s · öz-denetim."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v45.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


degis('"""v45 (26 Eyl 2026):', '"""v46 (26 Eyl 2026): ANİMASYON DÜZELTMESİ (Kemal: "bir şeyler eksen kaçık dönüp duruyor, fırında, TOPPING\'de, her yerde").\n'
      '  Sebep 1: dönen parçalar dünya ağıyla "dönüş + telafi ötelemesi" alıyordu; glTF kareler arasında ötelemeyi doğrusal, dönüşü yay\n'
      '  boyunca ara değerlediği için parça ekseninden savruluyordu (bant burun makarası 350 mm, koniler 96, valf 94). Artık her dönen\n'
      '  TOPPING grubu kendi ekseninde duran düğüm (ağ pivota göre yerel). Sebep 2: sabit "tabla_bos_sensoru" adı "tabla" ile başladığı\n'
      '  için tablanın dönen grubuna düşmüş, 2 m yarıçapla dönüyordu → SABİT. 30 kare/s. Montaj her çalışmada sapmayı ölçer.\n'
      'v45 (26 Eyl 2026):')
degis('def grup_modul(ad):\n', 'def grup_modul(ad):\n    if ad == "tabla_bos_sensoru": return "SABIT"                 # v46: aktarma ucundaki sabit sensör (adı "tabla" ile başlıyor)\n')
degis('    ANIM_HAT, ADIM_HAT, T_J = yolculuk(parcalar)\n    print("ANA MONTAJ ANIMASYONU (v45): tek tam dongu %.0f sn · %d kanal · %d adim" % (T_J, len(ANIM_HAT), len(ADIM_HAT)))\n',
      '    ANIM_HAT, ADIM_HAT, T_J, OZEL_T, HARIC_T, SAPMA = yolculuk(parcalar)\n'
      '    print("ANA MONTAJ ANIMASYONU (v46): tek tam dongu %.0f sn · %d kanal · %d adim · %d eksenli doner dugum" % (T_J, len(ANIM_HAT), len(ADIM_HAT), len(OZEL_T)))\n'
      '    print("SAPMA DENETIMI (kareler arasi, glTF ara degerleme <-> tam kinematik): en kotu 15 / %d dugum" % len(SAPMA))\n'
      '    for e_, t_, a_ in SAPMA[:15]: print("   %8.2f mm  t=%6.2f  %s" % (e_, t_, a_))\n'
      '    _kotu = [r for r in SAPMA if r[2].startswith("TOPPING_DONER__") and r[0] > 3.0]   # 3 mm: spiral sonundaki x hızı sıçraması (eksen değil)\n'
      '    assert not _kotu, "TOPPING donen dugumu ekseninden kayiyor: %s" % _kotu[:3]\n')
degis('    b1 = glb_yaz(os.path.join(OUT, "hat_v45.glb"), parcalar, dokular, liste=ANIM_HAT)   # v45: 1 tam animasyon (Kemal 25 Eyl)\n    print("hat_v45.glb · %d dugum · %.0f KB · animasyon %.0f sn" % (len(parcalar), b1 / 1024.0, T_J))\n',
      '    b1 = glb_yaz(os.path.join(OUT, "hat_v46.glb"), [x for x in parcalar if x[0] not in HARIC_T], dokular, ozel=OZEL + OZEL_T, liste=ANIM_HAT)   # v46: donenler kendi ekseninde\n'
      '    print("hat_v46.glb · %d dugum · %.0f KB · animasyon %.0f sn" % (len(parcalar), b1 / 1024.0, T_J))\n')
degis('usdz_yaz([os.path.join(OUT, "hat_v45.usdz")], "hat_v45", _usd + E_USDZ, dokular)', 'usdz_yaz([os.path.join(OUT, "hat_v46.usdz")], "hat_v46", _usd + E_USDZ, dokular)')
degis('print("hat_v45.usdz · %.0f KB', 'print("hat_v46.usdz · %.0f KB')
degis('pafta="HAT_ATOSA_TABLALI v12 · v45 ·', 'pafta="HAT_ATOSA_TABLALI v12 · v46 (animasyon duzeltmesi, geometri v45 ile ayni) ·')
i = s.index("# ---------------------------------------------------------------- v45 · 1 TAM ANİMASYON")
j = s.index('\n\nif __name__ == "__main__":\n')
s = s[:i] + io.open(os.path.join(U, "yolculuk_v46.py"), encoding="utf-8").read() + s[j:]
io.open(os.path.join(U, "hat_montaj_v46.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v46.py yazildi")
