# -*- coding: utf-8 -*-
"""hat_montaj_v59 → hat_montaj_v60 (27 Eyl 2026 gece) — TOPPING YALITIMI TAM (Kemal: "toppingin yan izolasyonları nerede, neden alt izolasyonunu
koymadın" · "yap dediğini, altına da az da olsa yalıtım yap"):
  · HATA DÜZELTMESİ: V3_CIKAN "kabin_" öneki TOPPING'in yan PU duvarlarını da (kabin_sol_duvar_PU · kabin_sag_duvar_PU) modelden düşürüyordu
    (v56'daki "yan PU duvarlar da görünür" satırı hiç çalışmadı) → yalnız dış kabuk sacları (taban · arka · üst · sağ teknik) dışarıda kalır.
  · TOPPING = topping_uno_cad_v12: soğuk odanın ALTINA alt sac 1 + PU 39 (rafın altı, bükümlerin arası; kotlar aynı).
  · sözleşmeye 1 eşitlik (yan PU 2 + alt yalıtım 2 modelde) · pafta metni · çıktılar hat_v60. Başka davranış DEĞİŞMEZ."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v59.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""v59 (27 Eyl 2026 gece):',
      '"""v60 (27 Eyl 2026 gece): TOPPING YALITIMI TAM — yan PU duvarları modele girdi (V3_CIKAN "kabin_" öneki onları da düşürüyordu) +' + NL +
      '  topping_uno_cad_v12: soğuk odanın altına alt sac 1 + PU 39 (Kemal: "altına da az da olsa yalıtım yap") · çıktılar hat_v60.' + NL +
      'v59 (27 Eyl 2026 gece):')
i = s.index('\nimport importlib, io')
assert s[i:].count("topping_uno_cad_v11") >= 3
s = s[:i] + s[i:].replace("topping_uno_cad_v11", "topping_uno_cad_v12")
degis('V3_CIKAN = ("kabin_", "tabla_diski",',
      'V3_CIKAN = ("kabin_taban_saci", "kabin_arka_saci", "kabin_ust_saci", "kabin_sag_teknik_sac", "tabla_diski",   # v60: yan PU duvarlar ARTIK girer (eski "kabin_" öneki onları da düşürüyordu)\n           ')
degis('''    elif _q["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU"):                       # v56: yan PU duvarlar da görünür
        _q["mal"] = "yalitim_gorunur"''',
      '''    elif _q["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU", "alt_yalitim_PU"):     # v56: yan PU duvarlar da görünür · v60: + alt yalıtım (v12)
        _q["mal"] = "yalitim_gorunur"''')
degis('''    ("v59 · B lamelli evaporator''',
      '''    ("v60 · TOPPING yalitimi modelde: yan PU 2 + alt sac + alt PU = 4 (topping_uno_cad_v12)", (float(len([q for q in TU.P if q["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU", "alt_yalitim_PU", "alt_yalitim_saci") and not q["ad"].startswith(V3_CIKAN)])), 4.0)),
    ("v59 · B lamelli evaporator''')
degis('print("ALCAK HAT SOZLESMESI (v59 ·', 'print("ALCAK HAT SOZLESMESI (v60 ·')
degis('pafta="HAT v59 (27 Eyl gece) ·',
      'pafta="HAT v60 (27 Eyl gece) · TOPPING YALITIMI TAM (Kemal: toppingin yan izolasyonlari nerede, alt izolasyonu neden yok): yan PU duvarlari modele girdi '
      '(eski filtre dusuruyordu) + topping_uno_cad_v12 soguk odanin altina alt sac 1 + PU 39 (kotlar ayni) · v59:')
for a_ in ("hat_v59.glb", "hat_v59.usdz", '"hat_v59"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v59", "v60"))
_kod = s[s.index('\nimport importlib, io'):]
for _eski in ("topping_uno_cad_v11", "hat_v59.glb", 'V3_CIKAN = ("kabin_",'):
    assert _eski not in _kod, "v60: eski kaldi: %s" % _eski
compile(s, "hat_montaj_v60.py", "exec")
io.open(os.path.join(U, "hat_montaj_v60.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v60.py yazildi · %d satir" % s.count(NL))
