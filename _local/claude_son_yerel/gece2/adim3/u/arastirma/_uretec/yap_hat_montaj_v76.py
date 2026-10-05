# -*- coding: utf-8 -*-
"""hat_montaj_v75 → hat_montaj_v76 (29 Eyl 2026 · YEREL) — Kemal: "kolaları normal hamurlar gibi yap, parmaklarıyla robot alsın" · "simetri, basit görünsün".
B = store_cad_v10: strok 700 · her şey tepside (itici yok) · 21 çekmece (lahmacun 10 × 42 · pide 7 × 25 · içecek 3 × 48 · tatlı 12) · K1–K3 / K5–K6 ön çizgileri hizalı.
Çekmece 3,7 s'de açılır → robot topu 3,8 s'de alır. Çıktılar hat_v76."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v75.py"), encoding="utf-8").read()
NL = chr(10)
def degis(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100]); s = s.replace(a, b)
degis('pafta="HAT v75 (29 Eyl) ·', 'pafta="HAT v76 (29 Eyl · YEREL) · STORE v10: STROK 700 · HER SEY TEPSIDE (robot parmakla, itici yok) · 21 CEKMECE (lahmacun 10 × 42 · pide 7 × 25 · icecek 3 × 48 · tatli 12) · K1-K3 / K5-K6 on cizgileri hizali · v75:')
degis('print("ALCAK HAT SOZLESMESI (v75 ·', 'print("ALCAK HAT SOZLESMESI (v76 ·')
for a_ in ("hat_v75.glb", "hat_v75.usdz", '"hat_v75"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v75", "v76"))
n9 = s.count("store_cad_v9")
s = s.replace("store_cad_v9", "store_cad_v10")
print("store_cad_v9 -> v10:", n9)
degis('("lahmacun", "Lahmacun", "CEK_K2_lahm_6")', '("lahmacun", "Lahmacun", "CEK_K2_lahm_5")')
degis('("pide (dolap K3 + K5)", _kap.get("hamur", 0), 160, "2 gun 160"), ("lahmacun (K1 + K2)", _kap.get("lahm", 0), 432, "2 gun 400")',
      '("pide (dolap K3 + K5)", _kap.get("hamur", 0), 175, "2 gun 160 · v76: 7 × 25"), ("lahmacun (K1 + K2)", _kap.get("lahm", 0), 420, "2 gun 400 · v76: 10 × 42")')
degis('("icecek (dolap K6)", _kap.get("ic1", 0), 144, "2 gun 139")', '("icecek (dolap K6)", _kap.get("ic1", 0), 144, "2 gun 139 · v76: 3 × 48 tepside")')
# strok 700 → çekmece 3,67 s'de açılır: robot 3,8 s'de alır (v75: 3,5 — çekmece 3,3 s'de açılıyordu)
degis('    TOPZ.git(CEK_T, 3.5, top_z0 + SC.STROK, "l")' + NL + '    TOPY.git(3.5, 4.2, 650.0);',
      '    T_AL = max(3.5, CEK_T + 0.1)                                        # v76: strok 700 → 3,7 s' + NL +
      '    TOPZ.git(CEK_T, T_AL, top_z0 + SC.STROK, "l")' + NL + '    TOPY.git(T_AL, 4.2, 650.0);')
degis('             (3.5, "ROBOT", "FR5 hamur topunu alır,', '             (T_AL, "ROBOT", "FR5 hamur topunu alır,')
s = s.replace('"""', '"""hat_montaj_v76 (29 Eyl 2026 · YEREL): STORE v10 (tepsiler, 21 çekmece, simetri) — yap_hat_montaj_v76.py.\n', 1)
compile(s, "hat_montaj_v76.py", "exec")
io.open(os.path.join(U, "hat_montaj_v76.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v76.py yazildi")
