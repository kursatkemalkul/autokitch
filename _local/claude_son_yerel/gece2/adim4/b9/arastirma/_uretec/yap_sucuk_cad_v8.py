# -*- coding: utf-8 -*-
"""sucuk_cad_v7 → sucuk_cad_v8 (28 Eyl 2026) — ÖRÜMCEK KAYNAK YAKALARI KOLA BİTİŞİK (katı denetimi: denetim_kati_v1.py · Kemal: "düzelt, onaylıyorum").
v7'de kaynak yakaları örümcek GÖBEĞİNİN uçlarına (z0 − 3 … z0 · z1 … z1 + 3) konuyordu. Kol göbekten 3,5 mm kısa (14 / 17,5) → arka ve ön örümcekte yakalar
kolun yüzünden 1,75 mm uzakta, HAVADA (her örümcek 5 ayrık gövde). v8: yaka KOLUN YÜZÜNE bitişik ve yalnız sıyırıcı lamanın DEVAM ETTİĞİ yüzde
(lama −146…146: arka örümcekte yalnız iç yüz, ön örümcekte yalnız iç yüz, orta örümcekte iki yüz — orta v7 ile aynı). Başka hiçbir parça değişmez.
Çıktılar _v8 adlarıyla (sucuk_v8.glb / .usdz / _dozaj.glb · 3_TOPPING/sucuk_kaseti_v8/)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "sucuk_cad_v7.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""KAPAK YOK', '"""v8 (28 Eyl 2026): ÖRÜMCEK KAYNAK YAKALARI KOLUN YÜZÜNE BİTİŞİK (v7: göbek ucuna göre → arka/ön örümcekte 1,75 mm havada, 5 ayrık gövde) · '
                    'yalnız lamanın devam ettiği yüzde · başka değişiklik yok · çıktılar sucuk_v8 (yap_sucuk_cad_v8.py).' + NL + 'KAPAK YOK')
degis('            for za_, zb_ in ((z0 - 3.0, z0), (z1, z1 + 3.0)):',
      '            for za_, zb_ in yaka_z(zo):                                                   # v8: kolun yüzüne bitişik (v7: göbek ucuna göre, havada)')
degis('    def orumcek(z0, z1):',
      '    LAMA_Z = (-146.0, 146.0)                                                         # sıyırıcı lama boyu (cubuk_*)\n'
      '    def yaka_z(zo):                                                                  # v8: kaynak yakası kolun iki yüzünden yalnız lamanın geçtiği yüze\n'
      '        L = []\n'
      '        if zo - 7.0 > LAMA_Z[0] + 3.0: L.append((zo - 7.0 - 3.0, zo - 7.0))\n'
      '        if zo + 7.0 < LAMA_Z[1] - 3.0: L.append((zo + 7.0, zo + 7.0 + 3.0))\n'
      '        return L\n'
      '    def orumcek(z0, z1):')
for a_, n_ in (("sucuk_v7", 9), ("sucuk_kaseti_v7", 2)):
    assert s.count(a_) == n_, (a_, s.count(a_))
s = s.replace("sucuk_kaseti_v7", "sucuk_kaseti_v8").replace("sucuk_v7", "sucuk_v8")
compile(s, "sucuk_cad_v8.py", "exec")
io.open(os.path.join(U, "sucuk_cad_v8.py"), "w", encoding="utf-8").write(s)
print("sucuk_cad_v8.py yazildi · %d satir" % s.count(NL))
