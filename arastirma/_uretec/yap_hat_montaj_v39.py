# -*- coding: utf-8 -*-
"""hat_montaj_v38 -> v39 : B ÇEKMECE RAYI ÜÇ ELEMANLI TELESKOP (store_cad_v3)

Kemal (25 Eyl 2026): "çekmeceler açılıyor ama havada kalıyor, çekmece rayından çıkıp havada kalıyor; onu düzelt."
  · B = store_cad_v3: ray dış (kasa, sabit) · ara (strok/2) · iç (çekmece, strok). Tam açıkta en az bindirme dış–ara 384,
    ara–iç 380 mm; kutu iç elemana 527 mm boyunca bağlı. Çakışma: kapalı 0 · açılma yolunda 4 konum 0.
  · Animasyon: çekmece düğümü (…__CEKMECE) strok kadar, ara ray düğümü (…__CEKMECE_ARA) aynı zamanlamayla yarısı kadar.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v38.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, "YOK/COK (%d): %s" % (s.count(a), a[:90])
    s = s.replace(a, b)


degis('"""v38 (25 Eyl 2026):', '''"""v39 (25 Eyl 2026): B = store_cad_v3 — çekmece rayı ÜÇ ELEMANLI teleskop (açık çekmece artık rayda taşınıyor, havada değil).
v38 (25 Eyl 2026):''')
degis("ÇIKTI: otonom/hat3d/hat_v38.glb + .usdz", "ÇIKTI: otonom/hat3d/hat_v39.glb + .usdz")
degis("import store_cad_v2 as SC", "import store_cad_v3 as SC                                  # v39: 3 elemanlı ray")
degis('''birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v1.py", "")''',
      '''birim(_kod, _ad, "B", "GERCEK_STORE", _x, _y, _z, "sac", "store_cad_v3.py", "")''')
degis('''print("B CEKMECE MODULU (store_cad_v2): %d birim''', '''print("B CEKMECE MODULU (store_cad_v3 · 3 elemanli ray): %d birim''')
degis('''        for a_, _m, _x in parcalar:
            if a_.startswith(kod_ + "__") and a_.endswith("__CEKMECE"):
                ANIM.append((a_, T, V))''',
      '''        for a_, _m, _x in parcalar:
            if a_.startswith(kod_ + "__") and a_.endswith("__CEKMECE"):
                ANIM.append((a_, T, V))
            elif a_.startswith(kod_ + "__") and a_.endswith("__CEKMECE_ARA"):            # v39: ray ara elemanı aynı anda yarı yol
                ANIM.append((a_, T, [(x_, y_, z_ * SC.RAY_ARA_ORAN) for x_, y_, z_ in V]))''')
degis('''    print("ANIMASYON: %d cekmece sirayla · acilma %.1f sn · cekmece turu %.1f sn · %d hareketli dugum" % (len(_sira), _ac, _T_top, len(ANIM)))''',
      '''    print("ANIMASYON: %d cekmece sirayla · acilma %.1f sn · cekmece turu %.1f sn · %d hareketli dugum (%d ara ray)"
          % (len(_sira), _ac, _T_top, len(ANIM), sum(1 for x_ in ANIM if x_[0].endswith("__CEKMECE_ARA"))))
    assert sum(1 for x_ in ANIM if x_[0].endswith("__CEKMECE_ARA")) == len(_sira), "her acilan cekmecenin ara ray dugumu olmali"''')
degis('''os.path.join(OUT, "hat_v38.glb")''', '''os.path.join(OUT, "hat_v39.glb")''')
degis('''print("hat_v38.glb · %d birim''', '''print("hat_v39.glb · %d birim''')
degis('''usdz_yaz([os.path.join(OUT, "hat_v38.usdz")], "hat_v38",''', '''usdz_yaz([os.path.join(OUT, "hat_v39.usdz")], "hat_v39",''')
degis('''print("hat_v38.usdz · %.0f KB''', '''print("hat_v39.usdz · %.0f KB''')
degis('''· v38 · E = kutu_cad_v2 · B = store_cad_v2 ·''', '''· v39 · E = kutu_cad_v2 · B = store_cad_v3 (3 elemanli ray) ·''')
io.open(os.path.join(U, "hat_montaj_v39.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v39.py yazildi")
