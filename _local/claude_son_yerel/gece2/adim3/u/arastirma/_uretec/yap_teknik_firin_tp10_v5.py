# -*- coding: utf-8 -*-
"""teknik_firin_tp10_v4 → v5 (27 Eyl 2026): model firin_tp10_cad_v6 — kutu yedeği TEK YERDE fırın üstü sol 320, raf 4 mm + 10 takoz; dolap pizza gözü boş."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_firin_tp10_v4.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


d('TEKNİK RESİM v4 (27 Eyl 2026): FIRIN 79 mm ÖNE (firin_tp10_cad_v5)', 'TEKNİK RESİM v5 (27 Eyl 2026): KUTU YEDEĞİ TEK YERDE fırın üstü sol 320, raf 4 mm + 10 takoz (firin_tp10_cad_v6) · v4: FIRIN 79 mm ÖNE')
d('import firin_tp10_cad_v5 as FT', 'import firin_tp10_cad_v6 as FT')
d('"içerik v47 ile aynı · üstü %s · pizza kutusu yedeği 505"', '"içerik v47 ile aynı · üstü %s · pizza gözü BOŞ (v52: yedek fırın üstünde)"')
d('("14", "F taban dolabı (bizim) · üst 956", "pizza yedeği 505", "hesap"),', '("14", "F taban dolabı (bizim) · üst 956", "pizza gözü boş", "v52"),')
d('("15", "Egzoz davlumbazı (bizim)", "1483–2028", "v47"),',
  '("15", "Egzoz davlumbazı (bizim) · arka yarı", "1483–2028", "v47"),\n'
  '        ("16", "Üst raf 4 mm · 10 takoz Ø16 · SOL kutu yedeği 320 · SAĞ kompresör", "1512–1516 · yığın 1516–2028", "hesap · 99 kg"),')
d('"pizza kutusu 4 gün: dolap 505 + raf 55 + şarjör 567"', '"pizza kutusu 887 = 3,1 gün: şarjör 567 + fırın üstü sol 320 (Kemal)"')
d('TEKNİK RESİM v4", f30, INK)', 'TEKNİK RESİM v5", f30, INK)')
d('"3B model firin_tp10_cad_v5 (tek kaynak)', '"3B model firin_tp10_cad_v6 (tek kaynak)')
s = s.replace("FIRIN_TP10_v4_teknik", "FIRIN_TP10_v5_teknik")
s = s.replace("ana makine v51", "ana makine v52")
io.open(os.path.join(U, "teknik_firin_tp10_v5.py"), "w", encoding="utf-8").write(s)
print("teknik_firin_tp10_v5.py yazildi")
