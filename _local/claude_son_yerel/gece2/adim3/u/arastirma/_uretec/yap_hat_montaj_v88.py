# -*- coding: utf-8 -*-
"""hat_montaj_v87 → v88 (30 Eyl 2026 · Claude · base 33b600b = v87 yayında). Yalnız kayıtlı montaj worktree'sinde çalıştır.
Kemal (30 Eyl): "yap işte ne lazımsa" → v87 raporunun açık listesi:
1 · K v9: gıda sınıfı tereyağı sistemi (PulsaJet 104210-VIFC + PWMD yassı uç girişte SABİT · MDG 3 6 bar + karıştırıcı + manşet · LMT121 · Kletti hortum)
2 · E v13: 7 sıfır sensörü · Beckhoff CX9240 + 7 × EL7062 (13 eksen) · frenli kafa motoru PKP268D28M2 · gerçek vakum parçaları (kinematik v12 ile aynı)
3 · FR5 TCP rampası 0,4 → 0,5 s: Fairino kılavuzu ivmeyi hızın ≈ 2 katı önerir (800 mm/s → 1,6 m/s²) · yer rayı 0,8 s (1 m/s²) Güdel CMF (2 m/s · 2 m/s²) /
    Rollon SEV160 (2 m/s · 4 m/s²) sınıfının içinde
4 · sayfa bağlantıları v87 → v88 (yalnız model bağlantıları + K/E veri dosyası)"""
import re
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / "hat_montaj_v87.py").read_text(encoding="utf-8-sig")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:110], s.count(a), n)
    s = s.replace(a, b)


# ---------------------------------------------------------------- 0 · başlık + sürüm ----------------------------------------------------------------
rep('"""hat_montaj_v87 (30 Eyl 2026 · Claude · base 4ae5cd0)',
    '"""hat_montaj_v88 (30 Eyl 2026 · Claude · base 33b600b): K v9 GIDA SINIFI TEREYAĞI (PulsaJet 104210-VIFC + PWMD girişte sabit · MDG 3 6 bar · LMT121) +\n'
    'E v13 (7 sıfır sensörü · Beckhoff CX9240 + 7 × EL7062 · frenli kafa motoru · SMC vakum) + FR5 rampası 0,5 s (Fairino kılavuzu) — yap_hat_montaj_v88.py\n'
    'hat_montaj_v87 (30 Eyl 2026 · Claude · base 4ae5cd0)')
rep('pafta="HAT v87 (30 Eyl · Claude · YEREL)',
    'pafta="HAT v88 (30 Eyl · Claude · YEREL): K v9 GIDA SINIFI TEREYAGI (PULSAJET 104210-VIFC + PWMD GIRISTE SABIT) + E v13 (SIFIR SENSORLERI, BECKHOFF 13 EKSEN, FRENLI KAFA, SMC VAKUM) + FR5 RAMPA 0,5 s; HAT 5230 · v87 (30 Eyl · Claude · YEREL)')

# ---------------------------------------------------------------- 1 · istasyon sürümleri ----------------------------------------------------------------
n8 = s.count("kesme_cad_v8"); assert n8 >= 5, n8
s = s.replace("kesme_cad_v8", "kesme_cad_v9")
n12 = s.count("kutu_cad_v12"); assert n12 >= 2, n12
s = s.replace("kutu_cad_v12", "kutu_cad_v13")
# K v9 ↔ E v13 saat arayüzü: K v9, K v8'in E v12 bağını kullanır; E v13 kinematiği v12 ile BİREBİR olmalı
rep('''import kutu_cad_v13 as KC ''', '''import kutu_cad_v12 as _KC12_saat                            # v88: E v13 kinematiği v12 ile aynı mı (K v9 → K v8 → E v12 saat bağı)
import kutu_cad_v13 as KC ''')
rep('''KC.modul()
_ION = KC.icecek_on_olcum()''', '''KC.modul()
assert (KC.DONGU_GERCEK, KC.E_HAZIR_GERCEK, tuple(KC.Z_CATAL_GERCEK)) == (_KC12_saat.DONGU_GERCEK, _KC12_saat.E_HAZIR_GERCEK, tuple(_KC12_saat.Z_CATAL_GERCEK)), \\
    "v88: E v13 saati v12'den farkli (K v9 saat bagi v12'ye kurulu)"
_ION = KC.icecek_on_olcum()''')

# ---------------------------------------------------------------- 2 · K birimleri (v9) ----------------------------------------------------------------
rep('''    ("K_KESICI", "Kesici + sprey kafası: Festo DGRF-C-GF-63-125-PPV-A-R (6 bar 1870 N · 16,5 mm bağlantı plakası arka kirişe) · yıldız bıçak Ø296 × 6 · koruma halkası · göbekte PulsaJet AAB10000AUH-03 + UniJet TG-W 2.8W (dik)",
     ("kopru_kirisi", "DGRF", "kafa_adaptoru", "ara_dikme", "kafa_plakasi", "bicak_", "koruma_", "kelebek_", "PulsaJet", "isitmali_hortum_kafa", "hortum_baglantisi_")),''',
    '''    ("K_KESICI", "Kesici: Festo DGRF-C-GF-63-125-PPV-A-R (6 bar 1870 N · 16,5 mm bağlantı plakası arka kirişe) · yıldız bıçak Ø296 × 6 · koruma halkası (v88: sprey kafadan alındı)",
     ("kopru_kirisi", "DGRF", "kafa_adaptoru", "ara_dikme", "kafa_plakasi", "bicak_", "koruma_", "kelebek_")),''')
rep('''    ("K_YAG", "Tereyağı sistemi (ALT dolap): Walther Pilot MDG 3 paslanmaz basınçlı tank 3,2 L (2 gün 1,41 L) + ısıtıcı ceket + regülatör + seviye sensörü · ısıtmalı hortum arkadan kafaya", ("yag_", "isitmali_hortum_", "hava_hortumu_tank")),''',
    '''    ("K_YAG", "Tereyağı sistemi GIDA SINIFI (v88): Spraying Systems PulsaJet AAB10000AUH-104210-VIFC + TPU11002 PWMD yassı uç ÜRÜN GİRİŞİNDE SABİT (x 25 · 130 mm · 110°: ürün altından geçer) + ısıtıcı blok · "
     "ALT dolapta Walther Pilot MDG 3 6 bar + karıştırıcı 46-200 + ısıtma manşeti + SSCo 11438-45S · ifm LMT121 · Kletti DN6 ısıtmalı hortum sağ duvardan",
     ("yag_", "isitmali_hortum_", "hava_hortumu_tank", "PulsaJet", "nozul_", "taban_hortum_gecisi")),''')
rep('''    ("K_ELEKTRIK", "Pano (arka üst): Siemens S7-1200 1214C · Mean Well NDR-240-24 · 2 × E5DC + 2 × G3PE (tank + hortum ısısı) · SMC SS5Y3-20-04 + 3 × SY3120 · AW20-F02-A şartlandırıcı · hortumlar",''',
    '''    ("K_ELEKTRIK", "Pano (arka üst): Siemens S7-1200 1214C · Mean Well NDR-240-24 · 3 × E5DC + 2 × G3PE + DC SSR (tank manşeti · hortum · nozül) · SMC SS5Y3-20-04 + 3 × SY3120 · AW20-F02-A şartlandırıcı · hortumlar",''')

# ---------------------------------------------------------------- 3 · E birimleri (v13) ----------------------------------------------------------------
rep('''    ("E_BESLEYICI", "Vakumlu alma/bırakma: 4 vantuz + 20 mm Z kaldırma + mevcut 411 mm ray; itici çubuk yok", ("besleyici_", "itici_", "vakum_")),''',
    '''    ("E_BESLEYICI", "Vakumlu alma/bırakma (v88 gerçek parça): SMC CDQ2B16-20DZ · 4 × ZP3C-T32CFS-MF-A8 (karton için) · ZK2G15K5RWA-08 vakum ünitesi · 411 mm ray", ("besleyici_", "itici_", "vakum_")),''')
rep('''    ("E_PISTON", "Piston: 296 × 296 kafa · SFU1610 (üstten BK12) · 2 HGR15 · NEMA 23 · taban / kilit / kapak", ("piston_",)),''',
    '''    ("E_PISTON", "Piston: 296 × 296 kafa · SFU1610 (üstten BK12) · 2 HGR15 · FRENLİ motor Oriental PKP268D28M2 (0,8 N·m · kafa düşmez) · taban / kilit / kapak", ("piston_",)),''')
rep('''    ("E_ELEKTRIK", "Pano: S7-1200 1214C + SM1221 + SM1222 · 13 × STP-DRV-4830; hareket denetleyicisi/I-O seçimi AÇIK · Mean Well 24/48 V · sensörler", ("pano_", "din_rayi", "plc_", "guc_", "surucu_", "klemens_", "kablo_kanali", "sensor_")),''',
    '''    ("E_ELEKTRIK", "Pano (v88): S7-1200 1214C + SM1221 + SM1222 (istasyon denetçisi) · Beckhoff CX9240 + EL6631-0010 PROFINET + 7 × EL7062 (13 step ekseni) · Mean Well 24/48 V · sensörler",
     ("pano_", "din_rayi", "plc_", "guc_", "surucu_", "klemens_", "kablo_kanali", "sensor_", "beckhoff_")),''')

# ---------------------------------------------------------------- 4 · FR5 rampası (Fairino kılavuzu) ----------------------------------------------------------------
rep('''    V_TCP, TA_TCP = 800.0, 0.4                     # Fairino FR5 TCP ≤ 1 m/s (%80) · 0,4 s rampa ≈ 2 m/s² [V: Fairino veri sayfası teyit]''',
    '''    V_TCP, TA_TCP = 800.0, 0.5                     # v88: Fairino FR5 katalog EV4.4 — tipik/azami TCP 1 m/s, eklemler 180°/s · kılavuz §9.5.2: ivme ≈ 2 × hız → 1,6 m/s² = 0,5 s rampa (v87 0,4 s = 2 m/s²)''')
rep('''    V_RAY, TA_RAY = 800.0, 0.8                     # FR5 yer rayı ≤ 1 m/s (%80) · 0,8 s rampa ≈ 1 m/s² [V]''',
    '''    V_RAY, TA_RAY = 800.0, 0.8                     # yer rayı 0,8 m/s · 1 m/s² — Fairino ray satmıyor; Güdel CoboMover CMF (2 m/s · 2 m/s²) / Rollon SEV160-1S (2 m/s · 4 m/s²) sınıfı [ürün V]''')
rep('''    ADIM += [(0.0, "ÇEKMECE",''', '''    ADIM += [(0.0, "ÇEKMECE",''')
s = s.replace("TCP ≤ 800 mm/s [V]", "TCP ≤ 800 mm/s · rampa 0,5 s (Fairino kılavuzu)")

# ---------------------------------------------------------------- 5 · K adım metni (sprey artık girişte) ----------------------------------------------------------------
rep('''"K bandı (Interroll EC5000, ≤ 0,37 m/s) ürünü fırın bandından alır, 2 s'de kesme merkezine getirir (E3Z ışını durdurur). Pidede kafanın göbeğindeki PulsaJet 1,2 s tereyağı püskürtür. Festo DGRF-C-63 kafayı 1,4 s'de indirir, 6 dilim keser (bıçak bandın 0,5 mm üstünde durur), 0,8 s'de kaldırır."''',
    '''"Ürün K girişindeki SABİT gıda nozülünün (PulsaJet 104210-VIFC · 110° yassı yelpaze, 130 mm yukarıda) altından geçerken tereyağı alır: son 65 mm fırın bandında, kalanı K bandında (PWM ürün hızıyla orantılı · ≈ 8 g). K bandı (Interroll EC5000, ≤ 0,37 m/s) ürünü 2 s'de kesme merkezine getirir (E3Z ışını durdurur). Festo DGRF-C-63 kafayı 1,4 s'de indirir, 6 dilim keser (bıçak bandın 0,5 mm üstünde durur), 0,8 s'de kaldırır."''')

# ---------------------------------------------------------------- 6 · çıktı adları ----------------------------------------------------------------
n_ = s.count('os.path.join(OUT, "hat_v87.glb")') + s.count('os.path.join(OUT, "hat_v87.usdz")')
assert n_ == 2, n_
s = s.replace('os.path.join(OUT, "hat_v87.glb")', 'os.path.join(OUT, "hat_v88.glb")').replace('os.path.join(OUT, "hat_v87.usdz")', 'os.path.join(OUT, "hat_v88.usdz")')
rep('"hat_v87", _usd', '"hat_v88", _usd')
rep('print("hat_v87.glb · %d dugum', 'print("hat_v88.glb · %d dugum')
rep('print("hat_v87.usdz · %.0f KB', 'print("hat_v88.usdz · %.0f KB')
assert "hat_v87." not in s.replace("hat_v87.py", ""), [l for l in s.splitlines() if "hat_v87." in l][:3]

compile(s, "hat_montaj_v88.py", "exec")
(U / "hat_montaj_v88.py").write_text(s, encoding="utf-8")
# sayfa bağlantısı (makine.html / index.html): v87 → v88
for name in ("makine.html", "index.html"):
    p = U.parent.parent / "otonom" / "hat" / name
    data = p.read_bytes()
    if b"hat_v88" in data:
        continue
    assert b"hat_v87" in data, name
    data = re.sub(rb"hat_v87\.(glb|usdz)\?v=87[\w-]*", rb"hat_v88.\1?v=88", data)
    assert b"hat_v87" not in data, name
    p.write_bytes(data)
print("v88 montaj üreteci yazıldı (v87 + K v9 + E v13 + FR5 rampa) · makine.html / index.html model bağlantısı v88")
