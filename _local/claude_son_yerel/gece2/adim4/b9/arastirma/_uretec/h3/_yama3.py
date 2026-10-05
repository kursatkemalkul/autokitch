# -*- coding: utf-8 -*-
import io, os
D = os.path.dirname(os.path.abspath(__file__))
def yama(ad, R):
    P = os.path.join(D, ad); s = io.open(P, encoding="utf-8").read()
    for a, b in R:
        assert s.count(a) == 1, (ad, a[:80]); s = s.replace(a, b)
    io.open(P, "w", encoding="utf-8").write(s)
yama("h3_hesap_v1.py", [
 ('"HARC": 2226.0', '"HARC": 2160.0'),
 ("(sos 1645 · harç 2226)", "(sos 1645 · harç 2160: kaşar kasetinin önü boş · sucuk mandalı 2217'de)"),
])
yama("h3_topping_v1.py", [
 ('# v3: 1645 · 2226 (alt kat dozajlayıcılarının arası)', '# v3: 1645 (kıyma | kuşbaşı arası) · 2160 (kaşar kasetinin önü: çıkış tüpü ≤ 2103 · somun 2146–2158 z ≤ −186 · kılavuz 2202)'),
 ('X_UST = {"sos": 1645.0, "harc": 2247.0}      # v3 · üst kattaki UNO eksenleri: sos yayıcısının tam üstü · harç 21 sağda (evaporatör kaseti iki UNO silindirinin arasına sığsın)',
  'X_UST = {"sos": 1645.0, "harc": 2247.0}      # v3 · üst kattaki UNO eksenleri: sos yayıcısının tam üstü · harç 87 sağda (evaporatör kaseti 1676–2216 iki UNO silindirinin arasına sığsın)'),
 ('TAHLIYE_V2 = [(2108.0, 1425.0, -775.0), (2108.0, 1350.0, -775.0), (2108.0, 1350.0, -805.0), (2108.0, 1372.0, -805.0), (2108.0, 1372.0, -815.0),\n'
  '              (2108.0, 950.0, -815.0), (2120.0, 950.0, -815.0),',
  'TAHLIYE_INIS_X = 2203.0                        # v2 ile aynı iniş (kaşar ≤ 2090 | sucuk ≥ 2283 motorlarının arası) · kasetin çıkışı v3\'te 2101 (v2 2203 − 102)\n'
  'TAHLIYE_V2 = [(2101.0, 1425.0, -775.0), (2101.0, 1350.0, -775.0), (2101.0, 1350.0, -805.0), (2101.0, 1372.0, -805.0), (2101.0, 1372.0, -815.0),\n'
  '              (TAHLIYE_INIS_X, 1372.0, -815.0), (TAHLIYE_INIS_X, 950.0, -815.0), (2120.0, 950.0, -815.0),'),
 ('(TAHLIYE_V2[0][0], -815.0, 5.0)', '(TAHLIYE_INIS_X, -815.0, 5.0)'),
 ('# v3 · UNO çıkışından ÖNE (z −90: alt kat hazneleri −120\'de biter) → DİK iner → kıyma haznesinin altında (1250) yayıcı ekseninin üstüne döner → TC girişine (1216)',
  '# v3 · UNO çıkışından ÖNE (z −90: alt kat hazneleri −120\'de biter) → DİK iner (harç 1290\'da kasetlerin önünde 87 sola) → 1250\'de yayıcı ekseninin üstüne döner → TC girişine (1216)'),
 ('(2247.0, 1290.0, -90.0), (2226.0, 1290.0, -90.0), (2226.0, 1250.0, -90.0),\n'
  '                   (2226.0, 1250.0, -170.0), (2226.0, 1216.0, -170.0)]}',
  '(2247.0, 1290.0, -90.0), (2160.0, 1290.0, -90.0), (2160.0, 1250.0, -90.0),\n'
  '                   (2160.0, 1250.0, -170.0), (2160.0, 1216.0, -170.0)]}'),
])
print("ok")
