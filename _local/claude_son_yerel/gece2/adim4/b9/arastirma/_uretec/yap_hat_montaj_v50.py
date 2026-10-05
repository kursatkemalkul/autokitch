# -*- coding: utf-8 -*-
"""hat_montaj_v49 → hat_montaj_v50 (26 Eyl 2026 gece): v49 itici denetimi 17 bulgu verdi →
 1 · itici_cad_v2: makara + kaldırma pimi −w tarafına (link uzantısı/makara sucuk iniş borusunun altına giriyordu, makara sensöre değiyordu,
     pim braketi fitili kesiyordu).
 2 · topping_uno_cad_v8: ön fitilin alt şeridinde 130 mm boşluk (itici gövdesi/kirişi ön düzlemi keser; ön kapak yok — Kemal).
 3 · Animasyon: çubuğun inişi 0,2 s, dönüşte temasa kadar 0,5 s + son 17,5 mm 0,25 s (kalkış 7 kare) → SAPMA 27 mm → küçük; tabla parka
     T_AKT + 1,0'da döner. Çıktılar hat_v50 · durum.json pafta HAT v50."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v49.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
degis('"""v49 (26 Eyl 2026 gece): AKTARMA İTİCİSİ (itici_cad_v1:', '"""v50 (26 Eyl 2026 gece): v49 + itici_cad_v2 (makara/kaldırma pimi −w) + topping_uno_cad_v8 (fitil boşluğu) + yavaş çubuk kalkışı' + NL + 'v49 (26 Eyl 2026 gece): AKTARMA İTİCİSİ (itici_cad_v1:')
degis('import itici_cad_v1 as IT', 'import itici_cad_v2 as IT')
degis('_sp = _ilu.spec_from_file_location("TU7", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v7.py"))',
      '_sp = _ilu.spec_from_file_location("TU8", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v8.py"))   # v50: fitil boşluğu')
degis('"topping_uno_cad_v7.py + topping_cad_v24.py", "hat/topping_v2.html")', '"topping_uno_cad_v8.py + topping_cad_v24.py", "hat/topping_v2.html")')
degis('(-420.0, -40.0), "sac", "topping_uno_cad_v7.py", "hat/topping_v2.html")', '(-420.0, -40.0), "sac", "topping_uno_cad_v8.py", "hat/topping_v2.html")')
degis('"sac", "itici_cad_v1.py", "hat/oven.html#itici")', '"sac", "itici_cad_v2.py", "hat/oven.html#itici")')
# zamanlama
degis('''    T_IT0, T_IT1 = T_AKT + 0.1, T_AKT + 0.7                                                      # v49: çubuk iner (T_AKT…+0,1), itme (+0,1…+0,7), bekleme, dönüş (+0,9…+1,5), son 17,5 mm'de kalkar
    X.git(T_AKT + 0.9, T_AKT + 0.9 + gecis(TH2.X_AKTARMA, TH2.X_PARK), TH2.X_PARK)''',
      '''    T_IT0, T_IT1 = T_AKT + 0.2, T_AKT + 0.8                                                      # v50: çubuk iner (T_AKT…+0,2), itme (+0,2…+0,8), bekleme +1,0, dönüş temasa +1,5, eve +1,75 (son 17,5 mm'de kalkar)
    X.git(T_AKT + 1.0, T_AKT + 1.0 + gecis(TH2.X_AKTARMA, TH2.X_PARK), TH2.X_PARK)''')
degis('''    def it_s(t):
        if t < T_IT0: return IT.S_HOME
        if t < T_IT1: return IT.S_HOME + (IT.S_END - IT.S_HOME) * (t - T_IT0) / (T_IT1 - T_IT0)
        if t < T_AKT + 0.9: return IT.S_END
        if t < T_AKT + 1.5: return IT.S_END + (IT.S_HOME - IT.S_END) * (t - T_AKT - 0.9) / 0.6
        return IT.S_HOME
    def it_aci(t):
        if t < T_AKT: return 90.0
        if t < T_IT0: return 90.0 * (1.0 - (t - T_AKT) / (T_IT0 - T_AKT))
        s_ = it_s(t)
        if t > T_AKT + 0.9 and s_ < IT.S_TEMAS: return 90.0 * (IT.S_TEMAS - s_) / (IT.S_TEMAS - IT.S_HOME)
        return 0.0''',
      '''    def it_s(t):
        if t < T_IT0: return IT.S_HOME
        if t < T_IT1: return IT.S_HOME + (IT.S_END - IT.S_HOME) * (t - T_IT0) / (T_IT1 - T_IT0)
        if t < T_AKT + 1.0: return IT.S_END
        if t < T_AKT + 1.5: return IT.S_END + (IT.S_TEMAS - IT.S_END) * (t - T_AKT - 1.0) / 0.5                 # dönüş temasa kadar
        if t < T_AKT + 1.75: return IT.S_TEMAS + (IT.S_HOME - IT.S_TEMAS) * (t - T_AKT - 1.5) / 0.25            # son 17,5 mm yavaş (kalkış)
        return IT.S_HOME
    def it_aci(t):
        if t < T_AKT: return 90.0
        if t < T_IT0: return 90.0 * (1.0 - (t - T_AKT) / (T_IT0 - T_AKT))
        s_ = it_s(t)
        if t > T_AKT + 1.0 and s_ < IT.S_TEMAS: return 90.0 * (IT.S_TEMAS - s_) / (IT.S_TEMAS - IT.S_HOME)
        return 0.0''')
s = s.replace('hat_v49.glb', 'hat_v50.glb').replace('hat_v49.usdz', 'hat_v50.usdz').replace('"hat_v49"', '"hat_v50"')
degis('pafta="HAT v49 (26 Eyl gece) · AKTARMA ITICISI itici_cad_v1 (SMC MY1B16-250 capraz 24,9°, pivotlu cubuk, destek plakasi) · F = TP10 kesitli 1500 firin v4 (havalandirmali raf) · kompresor firin ustunde · kutu yedegi 505 + 55 · TOPPING v24 + v2 v7 (katalog yay/pim, hac 7,0)',
      'pafta="HAT v50 (26 Eyl gece) · AKTARMA ITICISI itici_cad_v2 (SMC MY1B16-250 capraz 24,9°, pivotlu cubuk, sabit pimle kalkar, destek plakasi) · F = TP10 kesitli 1500 firin v4 (havalandirmali raf) · kompresor firin ustunde · kutu yedegi 505 + 55 · TOPPING v24 + v2 v8 (katalog yay/pim, hac 7,0, fitil boslugu)')
degis('print("ANA MONTAJ ANIMASYONU (v49):', 'print("ANA MONTAJ ANIMASYONU (v50):')
io.open(os.path.join(U, "hat_montaj_v50.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v50.py yazildi")
