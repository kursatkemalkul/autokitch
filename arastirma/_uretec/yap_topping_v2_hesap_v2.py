# -*- coding: utf-8 -*-
"""topping_v2_hesap_v1 → topping_v2_hesap_v2 (29 Eyl 2026 · YEREL) — Kemal: "sucuk dolarken tabla fırına yanaşıyor, yeterince boş alan var mı".
Montaj v81 ölçtü: sucuk spirali r 20'de bitince tabla x 2293'e gelir, dönen bant kasetinin köşesi 2517,2'ye uzanır → yükleme bandına 4,7 mm.
v2: spiral bitiş yarıçapı istasyon başına (R_IC_IST) — SUCUK 30 (öteki istasyonlar 20, değişmez). Kaset borusu tabla ekseninin 20 mm önünde →
tabla x = istasyon x − √(r² − 20²): r 20 → 0 · r 30 → 22,4 → tabla 22,4 mm erken durur, pay ≈ 27 mm. Ürün: şerit 33,6 → merkezde Ø26 sucuksuz
(r 13–47 dolu), dozaj süresi ve gram aynı (helezon devri). Önceki: topping_v2_hesap_v1.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_v2_hesap_v1.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""AUTOKITCH · TOPPING v2 (UNO\'lu) — DOZAJ HESABI v1 (25 Eyl 2026)',
      '"""AUTOKITCH · TOPPING v2 (UNO\'lu) — DOZAJ HESABI v2 (29 Eyl 2026 · yap_topping_v2_hesap_v2.py): SUCUK spirali r 30\'da biter (R_IC_IST) → tabla 22,4 mm erken durur,' + NL +
      'dönen kaset ↔ fırın yükleme bandı payı 4,7 → ≈27 mm (Kemal: "sucuk dolarken tabla fırına yanaşıyor, yer var mı") · öteki istasyonlar v1 ile aynı' + NL +
      'v1: AUTOKITCH · TOPPING v2 (UNO\'lu) — DOZAJ HESABI v1 (25 Eyl 2026)')
degis('R_IC = 20.0                       # spiral bu yarıçapta biter: kaset borusu tabla ekseninin 20 mm önünde → tam üstü [K: v1]',
      'R_IC = 20.0                       # spiral bu yarıçapta biter: kaset borusu tabla ekseninin 20 mm önünde → tam üstü [K: v1]' + NL +
      'R_IC_IST = {"SUCUK": 30.0}        # v2: sucuk r 30\'da biter → tabla x 22,4 mm erken durur (kaset süpürmesi ↔ yükleme bandı ≈27 mm) · şerit 33,6 → merkez Ø26 sucuksuz [H · Kemal onayı 29 Eyl]' + NL +
      NL + NL +
      'def r_ic(ist):' + NL +
      '    """v2 · istasyonun spiral bitiş yarıçapı"""' + NL +
      '    return R_IC_IST.get(ist["kod"], R_IC)')
degis('''    C = (r_dis ** 2 - R_IC ** 2) / (2.0 * N)                      # hatve p(r) = C / r''',
      '''    ric = r_ic(ist)                                               # v2: istasyon başına (sucuk 30)
    C = (r_dis ** 2 - ric ** 2) / (2.0 * N)                       # hatve p(r) = C / r''')
degis('''    d = dict(u, sure=T, tur=N, aci=N * 360.0, r_dis=r_dis, r_ic=R_IC, serit=b,
             hatve_dis=C / r_dis, hatve_ic=C / R_IC, seyrek_r=C / b,          # r < seyrek_r'de şeritler birbirine değmez''',
      '''    d = dict(u, sure=T, tur=N, aci=N * 360.0, r_dis=r_dis, r_ic=ric, serit=b,
             hatve_dis=C / r_dis, hatve_ic=C / ric, seyrek_r=C / b,           # r < seyrek_r'de şeritler birbirine değmez''')
degis('''             yuzey_hiz_dis=w * r_dis, x_hiz_max=(r_dis ** 2 - R_IC ** 2) / T / (2 * R_IC))''',
      '''             yuzey_hiz_dis=w * r_dis, x_hiz_max=(r_dis ** 2 - ric ** 2) / T / (2 * ric))''')
degis('''               yarik_min=YARIK_MIN, bicak_yuksek=BICAK_YUKSEK, serit=SERIT, tur_uno=TUR_UNO, r_ic=R_IC, taraf=TARAF,''',
      '''               yarik_min=YARIK_MIN, bicak_yuksek=BICAK_YUKSEK, serit=SERIT, tur_uno=TUR_UNO, r_ic=R_IC, r_ic_ist=R_IC_IST, taraf=TARAF,''')
degis('''    print("TOPPING v2 DOZAJ HESABI v1 — kaplanan alan Ø%.0f = %.0f mm² (kenar %.0f boş)" % (2 * R_KAP, A_KAP, KENAR))''',
      '''    print("TOPPING v2 DOZAJ HESABI v2 (sucuk r_ic %.0f) — kaplanan alan Ø%.0f = %.0f mm² (kenar %.0f boş)" % (R_IC_IST["SUCUK"], 2 * R_KAP, A_KAP, KENAR))''')
compile(s, "topping_v2_hesap_v2.py", "exec")
io.open(os.path.join(U, "topping_v2_hesap_v2.py"), "w", encoding="utf-8").write(s)
print("topping_v2_hesap_v2.py yazildi")
