# -*- coding: utf-8 -*-
"""hat_montaj_v70 → hat_montaj_v71 (29 Eyl 2026) — FIRIN KAPASİTESİ KORUNDU (Kemal: "kapasiteyi düşürme; pişirme alanı aynı; içeri alan bant hızlı, sonrası yavaş").
  · F = firin_tp10_cad_v10: ısıtılan 2624–3940 = 1316, aynı anda 4 ürün (v8 ile aynı) · yükleme bandı ön odadan ısıtılan bölgenin başına girer (2522–2845)
  · ürün yolu / animasyon v70 ile aynı (kasetten hızlı alır 1,25 s, sonra fırın bandı hızında) · çıktılar hat_v71."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v70.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120])
    s = s.replace(a, b)


degis('pafta="HAT v70 (29 Eyl) ·', 'pafta="HAT v71 (29 Eyl) · FIRIN KAPASITESI KORUNDU (isitilan 2624-3940 = 1316, ayni anda 4 urun · yukleme bandi on odadan isitilan bolgenin basina girer: kasetten hizli alir, sonra firin bandi hizinda) · v70:')
degis('print("ALCAK HAT SOZLESMESI (v70 ·', 'print("ALCAK HAT SOZLESMESI (v71 ·')
for a_ in ("hat_v70.glb", "hat_v70.usdz", '"hat_v70"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v70", "v71"))
degis('import firin_tp10_cad_v9 as FT ', 'import firin_tp10_cad_v10 as FT ')
degis('"sac", "firin_tp10_cad_v9.py", "hat/oven.html")', '"sac", "firin_tp10_cad_v10.py", "hat/oven.html")')
degis('    ("v70 · firin isitilan: FT.ODA = 1028 · FT.N_URUN = 3", (FT.ODA, 1028.0)),', '    ("v71 · firin isitilan korunur: FT.ODA = 1316", (FT.ODA, 1316.0)),')
degis('    ("v70 · firin ayni anda urun", (float(FT.N_URUN), 3.0)),', '    ("v71 · firin ayni anda urun = 4", (float(FT.N_URUN), 4.0)),' + NL +
      '    ("v71 · yukleme bandi isitilan bolgenin basinda: FT.X_TUN0 < FT.YB_SON (1 = evet)", (float(FT.X_TUN0 < FT.YB_SON), 1.0)),')
degis('"Yükleme bandı pideyi fırının ısıtılmayan ön odasından fırın bandına verir (fırın bandı hızıyla, hiç durmadan).',
      '"Yükleme bandı ısıtılan bölgenin başındadır: pideyi kasetten hızlı alır, sonra fırın bandı hızında taşıyıp fırın bandına verir (fırın bandı hiç durmaz, hızı değişmez).')
s = s.replace('"""', '"""hat_montaj_v71 (29 Eyl 2026): fırın kapasitesi korundu — yap_hat_montaj_v71.py.\n', 1)
compile(s, "hat_montaj_v71.py", "exec")
io.open(os.path.join(U, "hat_montaj_v71.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v71.py yazildi")
