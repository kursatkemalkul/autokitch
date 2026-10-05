# -*- coding: utf-8 -*-
"""topping_uno_cad_v14 → topping_uno_cad_v15 (28 Eyl 2026) — ÜRETİM DÜZELTMELERİ (katı denetimi denetim_kati_v1.py · Kemal: "düzelt, onaylıyorum yap").
1 · SOĞUK ODA KAPAKLARI (K1 · K2) İÇ SACI TEK PARÇA: v14'te 1,0 iç sac fitil kanalıyla ikiye (halka + panel) bölünüyordu. v15: kanal DIŞINDAKİ halka dış sacın
    ARKA DÖNÜŞÜ (1,5, dört kenar bükümünün devamı); iç sac yalnız kanalın İÇİNDEKİ panel (store_cad_v9 ile aynı düzen). Ölçüler, fitil, kanal AYNI.
    Temas denetiminde kapak gövdesi = dış sac + iç panel (menteşe kolu hangisine basıyorsa).
2 · KÜP SUCUK KASETİ sucuk_cad_v8 (örümcek kaynak yakaları kola bitişik — v7'de havadaydı).
3 · CODEX STEP KIRINTILARI: içe alınan STEP'te ana gövdenin binde 1'inden küçük ayrık katılar atılır (sucuk çıkış tüpünde 2 × 1,3 mm³).
Çıktılar topping_uno_v15. Önceki: topping_uno_cad_v14.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v14.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v14 · 28 Eyl 2026 gece',
      '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v15 · 28 Eyl 2026 akşam (v14 + KAPAK İÇ SACI TEK PARÇA · sucuk_cad_v8 · Codex STEP kırıntıları atılır · '
      'yap_topping_uno_cad_v15.py)' + NL + 'v14: topping_uno_cad_v14 · 28 Eyl 2026 gece')
# 1 · kapak iç sacı
degis('''    _kn_ = cevre_supur(*ac, KANAL_PROF)
    _pu, _ic = _pu.cut(_kn_), _ic.cut(_kn_)''',
      '''    _kn_ = cevre_supur(*ac, KANAL_PROF)
    _pu, _ic = _pu.cut(_kn_), _ic.cut(_kn_)
    # v15 · kanal DIŞINDAKİ halka = dış sacın ARKA DÖNÜŞÜ (1,5) · iç sac = yalnız kanalın İÇİNDEKİ panel (v14: iç sac kanalla ikiye bölünüyordu)
    _pl = kut(x0 + 1.0, x1 - 1.0, y0 + 1.0, y1 - 1.0, z0, z0 + 1.5).cut(_kn_)
    _pp = sorted(_pl.solids().vals(), key=lambda s_: -s_.BoundingBox().xlen * s_.BoundingBox().ylen)
    assert len(_pp) == 2, "%s: kanal dış halkası %d parça" % (_kn, len(_pp))
    _halka = cq.Workplane(obj=_pp[0])
    _ds = _ds.union(_halka); _pu = _pu.cut(_halka)
    _ip = sorted(_ic.solids().vals(), key=lambda s_: s_.BoundingBox().xlen * s_.BoundingBox().ylen)
    assert len(_ip) == 2, "%s: iç sac %d parça" % (_kn, len(_ip))
    _ic = cq.Workplane(obj=_ip[0])
    assert len(_ds.solids().vals()) == 1, "%s: dış sac tek parça değil" % _kn''')
degis('not_="v14 · AISI 304 1,0 · fitil geçme kanalı 6,4 × 8,4")',
      'not_="v15 · AISI 304 1,0 · kanalın İÇİNDEKİ panel (tek parça) · fitil dişi dış sacın arka dönüşü ile bu panel arasındaki 6,4 × 8,4 kanala geçer")')
degis('"v14 · soğuk kapak %s %.1f × %.1f × 40 · AISI 304 fırçalı 1,5 dört kenardan 40 bükülü (kulpsuz, bas-aç)',
      '"v15 · soğuk kapak %s %.1f × %.1f × 40 · AISI 304 fırçalı 1,5 dört kenardan 40 bükülü + arkada kanal kenarına kadar dönüş (kulpsuz, bas-aç)')
# kapak gövdesi temas denetimi: menteşe kolu iç panele ya da dış sacın dönüşüne basabilir
degis('''    _d = _mes(_a, _b_)
    kontrol("v14 · temas %s ↔ %s: %.3f mm (≤ 0,05)" % (_a, _b_, _d), _d <= 0.05)''',
      '''    _d = _mes(_a, _b_)
    if _b_ in ("onyuz_K1_ic_sac", "onyuz_K2_ic_sac"):                                                  # v15: kapak gövdesi = iç panel + dış sacın arka dönüşü
        _d = min(_d, _mes(_a, _b_.replace("_ic_sac", "_dis_sac")))
    kontrol("v14 · temas %s ↔ %s: %.3f mm (≤ 0,05)" % (_a, _b_, _d), _d <= 0.05)''')
# 3 · Codex STEP kırıntıları
degis('''        h[0]["wp"] = cq.importers.importStep(os.path.join(KOK, "arastirma", "3_TOPPING", yol))''',
      '''        _st = cq.importers.importStep(os.path.join(KOK, "arastirma", "3_TOPPING", yol))
        _ss = sorted(_st.solids().vals(), key=lambda s_: -s_.Volume())                                    # v15: Codex STEP'indeki ayrık kırıntılar atılır
        h[0]["wp"] = cq.Workplane(obj=_ss[0]) if len(_ss) > 1 and all(s_.Volume() < 1e-3 * _ss[0].Volume() for s_ in _ss[1:]) else _st''')
# 2 · sucuk_cad_v8 + çıktılar v15
n7 = s.count("sucuk_cad_v7"); assert n7 == 13, n7
s = s.replace("sucuk_cad_v7", "sucuk_cad_v8")
for a_ in ("topping_uno_v14.glb", "topping_uno_v14.json"):
    degis(a_, a_.replace("v14", "v15"))
degis('surum="topping_uno_cad_v14 · %s"', 'surum="topping_uno_cad_v15 · %s"')                       # JSON sürüm etiketi (sayfada görünür)
compile(s, "topping_uno_cad_v15.py", "exec")
io.open(os.path.join(U, "topping_uno_cad_v15.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v15.py yazildi · %d satir" % s.count(NL))
