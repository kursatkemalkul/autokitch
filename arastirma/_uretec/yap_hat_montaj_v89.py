# -*- coding: utf-8 -*-
"""hat_montaj_v88 → v89 (30 Eyl 2026 · Claude · base 34f362b = v88 yerel). Yalnız kayıtlı montaj worktree'sinde çalıştır.
Kemal (30 Eyl): "tamam önerdiğini yap toppinge · sıvı yağ · modelle"
1 · TOPPING v31 + soğuk kutu v19: evaporatör soğuk odadan çıktı → kuru bölmede soğutma grubunun TAM ÜSTÜNDE yalıtımlı kaset (arka duvara takılı · 2 POM kanal ·
    sifonlu tahliye → sıcak gaz döngülü yoğuşma tavası) · soğuk odada yalnız arka duvarda 2 yarıklı ızgara
2 · K v10: sıvı yağ · standart 18 L teneke tartıda (HBM PW15AH + SIWAREX WP231) · ProMinent emme borusu · Micropump GJ-N21 + Swagelok KBP + ifm PM1704 ·
    SMC PFA hortumlar · basınçlı tank, ısıtma, karıştırıcı kalktı
3 · sayfa bağlantıları v88 → v89 (yalnız model bağlantıları)"""
import re
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / "hat_montaj_v88.py").read_text(encoding="utf-8-sig")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:110], s.count(a), n)
    s = s.replace(a, b)


# ---------------------------------------------------------------- 0 · başlık + sürüm ----------------------------------------------------------------
rep('"""hat_montaj_v88 (30 Eyl 2026 · Claude · base 33b600b)',
    '"""hat_montaj_v89 (30 Eyl 2026 · Claude · base 34f362b): TOPPING v31 EVAPORATÖR KASETİ KURU BÖLMEDE (soğuk kutu v19: arka duvarda 2 kanal) + K v10 SIVI YAĞ TENEKESİ\n'
    '(18 L teneke tartıda · GJ-N21 pompa · KBP regülatör · PM1704) — yap_hat_montaj_v89.py\n'
    'hat_montaj_v88 (30 Eyl 2026 · Claude · base 33b600b)')
rep('pafta="HAT v88 (30 Eyl · Claude · YEREL)',
    'pafta="HAT v89 (30 Eyl · Claude · YEREL): TOPPING v31 EVAPORATOR KASETI KURU BOLMEDE GRUBUN USTUNDE (SOGUK KUTU v19: ARKA DUVARDA 2 KANAL, ICERIDE YALNIZ 2 IZGARA) + '
    'K v10 SIVI YAG TENEKESI (18 L TENEKE TARTIDA, GJ-N21 POMPA, KBP REGULATOR, PM1704); HAT 5230 · v88 (30 Eyl · Claude · YEREL)')

# ---------------------------------------------------------------- 1 · istasyon sürümleri ----------------------------------------------------------------
n9 = s.count("kesme_cad_v9"); assert n9 >= 5, n9
s = s.replace("kesme_cad_v9", "kesme_cad_v10")
n30 = s.count("topping_cad_v30"); assert n30 >= 2, n30
s = s.replace("topping_cad_v30", "topping_cad_v31")
n18 = s.count("topping_uno_cad_v18"); assert n18 >= 3, n18
s = s.replace("topping_uno_cad_v18", "topping_uno_cad_v19")
rep('"topping_uno_cad_v19.py"))   # v86: dikdörtgen soğuk kutu + eşit kapaklar',
    '"topping_uno_cad_v19.py"))   # v89: evaporatör kuru bölmede (arka duvarda 2 kanal)   # v86: dikdörtgen soğuk kutu + eşit kapaklar')

# ---------------------------------------------------------------- 2 · K birimleri (v10) ----------------------------------------------------------------
rep('3 ön kapak (tava 20, ön düzlem +79) · v87: tank ALT dolapta",', '3 ön kapak (tava 20, ön düzlem +79) · v89: yağ tenekesi + tartı + pompa grubu ALT dolapta",')
rep('''    ("K_YAG", "Tereyağı sistemi GIDA SINIFI (v88): Spraying Systems PulsaJet AAB10000AUH-104210-VIFC + TPU11002 PWMD yassı uç ÜRÜN GİRİŞİNDE SABİT (x 25 · 130 mm · 110°: ürün altından geçer) + ısıtıcı blok · "
     "ALT dolapta Walther Pilot MDG 3 6 bar + karıştırıcı 46-200 + ısıtma manşeti + SSCo 11438-45S · ifm LMT121 · Kletti DN6 ısıtmalı hortum sağ duvardan",
     ("yag_", "isitmali_hortum_", "hava_hortumu_tank", "PulsaJet", "nozul_", "taban_hortum_gecisi")),''',
    '''    ("K_YAG", "SIVI YAĞ sistemi (v89): Spraying Systems gıda PulsaJet AAB10000AUH-104210-VIFC + TPU11002 PWMD ÜRÜN GİRİŞİNDE SABİT (ısıtıcı yok) · ALT dolapta standart 18 L yağ tenekesi "
     "TARTIDA (HBM PW15AH 50 kg · kalan yağ ekranda) · ProMinent 1038304 emme borusu (seviye şalterli) · 10 µm filtre → Micropump GJ-N21 + EagleDrive → ifm PM1704 → Swagelok KBP (≈ 3,1 bar, fazlası tenekeye) · "
     "SMC PFA 10 × 8 hortum sağdan nozüle · damlama tavası",
     ("yag_", "PulsaJet", "nozul_", "taban_hortum_gecisi")),''')
rep('''    ("K_ELEKTRIK", "Pano (arka üst): Siemens S7-1200 1214C · Mean Well NDR-240-24 · 3 × E5DC + 2 × G3PE + DC SSR (tank manşeti · hortum · nozül) · SMC SS5Y3-20-04 + 3 × SY3120 · AW20-F02-A şartlandırıcı · hortumlar",''',
    '''    ("K_ELEKTRIK", "Pano (arka üst): Siemens S7-1200 1214C + SIWAREX WP231 tartı modülü · Mean Well NDR-240-24 · SMC SS5Y3-20-04 + 3 × SY3120 · AW20-F02-A şartlandırıcı · hortumlar (v89: E5DC / SSR kalktı — ısıtma yok)",''')

# ---------------------------------------------------------------- 3 · K adım metni (tereyağı → sıvı yağ) ----------------------------------------------------------------
rep('altından geçerken tereyağı alır: son 65 mm fırın bandında, kalanı K bandında (PWM ürün hızıyla orantılı · ≈ 8 g).',
    'altından geçerken sıvı yağ alır (tartıdaki 18 L tenekeden pompayla, ≈ 3,1 bar): son 65 mm fırın bandında, kalanı K bandında (PWM ürün hızıyla orantılı · ≈ 8 g).')

# ---------------------------------------------------------------- 4 · çıktı adları ----------------------------------------------------------------
n_ = s.count('os.path.join(OUT, "hat_v88.glb")') + s.count('os.path.join(OUT, "hat_v88.usdz")')
assert n_ == 2, n_
s = s.replace('os.path.join(OUT, "hat_v88.glb")', 'os.path.join(OUT, "hat_v89.glb")').replace('os.path.join(OUT, "hat_v88.usdz")', 'os.path.join(OUT, "hat_v89.usdz")')
rep('"hat_v88", _usd', '"hat_v89", _usd')
rep('print("hat_v88.glb · %d dugum', 'print("hat_v89.glb · %d dugum')
rep('print("hat_v88.usdz · %.0f KB', 'print("hat_v89.usdz · %.0f KB')
assert "hat_v88." not in s.replace("hat_v88.py", ""), [l for l in s.splitlines() if "hat_v88." in l][:3]

compile(s, "hat_montaj_v89.py", "exec")
(U / "hat_montaj_v89.py").write_text(s, encoding="utf-8")
# sayfa bağlantısı (makine.html / index.html): v88 → v89
for name in ("makine.html", "index.html"):
    p = U.parent.parent / "otonom" / "hat" / name
    data = p.read_bytes()
    if b"hat_v89" in data:
        continue
    assert b"hat_v88" in data, name
    data = re.sub(rb"hat_v88\.(glb|usdz)\?v=88[\w-]*", rb"hat_v89.\1?v=89", data)
    assert b"hat_v88" not in data, name
    p.write_bytes(data)
print("v89 montaj üreteci yazıldı (v88 + TOPPING v31 / TU v19 + K v10) · makine.html / index.html model bağlantısı v89")
