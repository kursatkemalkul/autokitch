# -*- coding: utf-8 -*-
"""ELEKTRİK v2 (zincir) · TEK ÖLÇÜ KAYNAĞI (mm, dünya: x hat boyu, y yukarı, z ön +). Kaynaklı katalog ölçüleri + VARSAYIMLAR."""
Z_ARKA = -830.0          # istasyon arka düzlemi
Z_DUVAR = -940.0         # VARSAYIM: dükkân duvarı (makine duvardan 110 mm açık: fiş başlığı ~70 + kanal 60; soğutma kondenser havası da ister)
# --- katalog (kaynak: harting.com 09300100301 Han 10B-HBM: 93 × 43,4 × 28,9 · Eaton P3-63/I4/SVB: 160 × 240 × 170 (eaton.com))
HAN_GOV = (43.4, 93.0, 28.9)      # Han 10B gövde (taban, sac üstü) x, y, yükseklik
HAN_KAP = (43.0, 75.0, 38.0)      # Han 10B kapak (hood) yandan çıkışlı, M32 — VARSAYIM ölçü (föyden teyit)
HAN_RAKOR_R, HAN_RAKOR_L = 15.0, 20.0
M12_FLANS = (26.0, 26.0, 3.0)     # M12 X-kodlu panel soketi (Phoenix SACC-DSI-M12FSX-8CON-L180) — flanş VARSAYIM
M12_FIS_R, M12_FIS_L = 10.0, 39.0 # M12 X fiş (dik) Ø20 × 43 — VARSAYIM
HAVA_R, HAVA_L = 8.0, 28.0        # Festo QSSF-8 duvar geçişli itme-tak rakor (Ø8 hortum) — VARSAYIM ölçü
SALTER = (160.0, 240.0, 170.0)    # Eaton P3-63/I4/SVB (63 A, 3P, kilitlenebilir kırmızı-sarı kol, IP65)
# --- kablolar
R_GUC = 7.5       # H07RN-F 5G2,5 Ø15 (zincir ara kablosu, 16 A / 400 V 3F+N+PE) — Lapp ÖLFLEX/H07RN-F föyü Ø 14–16
R_VERI = 4.35     # Cat6A endüstriyel PUR Ø8,7 (Lapp ETHERLINE Cat.6A)
R_BINA = 10.0     # H07RN-F 5G6 Ø20 (bina besleme)
R_HAVA = 4.0      # PU Ø8 hortum
# --- fiş paneli (her istasyonda AYNI): 280 × 120 · 304 2 mm · bağlantılar (x merkez = c + dx)
PANEL_W, PANEL_H, PANEL_T = 280.0, 120.0, 2.0
DX = dict(HAVA_GIRIS=-125.0, GUC_GIRIS=-85.0, VERI_GIRIS=-40.0, VERI_CIKIS=40.0, GUC_CIKIS=85.0, HAVA_CIKIS=125.0)
Y_UST = 920.0     # üst sıra istasyonlarda bağlantı merkez yüksekliği (panel 860–980)
Y_B = 360.0       # B (alt modül): panel 300–420 — B'nin arka yüzü yalnız 0–788; B elektrik plakasının (455–745) hemen altı
Y_QR = 120.0      # QR: arka yüz altı (panel 60–180), kanal başlığının hemen üstü
# istasyon panel merkezleri (x)
C = dict(TOPPING=1720.0, F=2855.0, K=4200.0, B=4200.0, E=4815.0, QR=5250.0)
# her panel istasyonun KENDİ elektrik kutusunun sırtında (bağlantılar arka sactan doğrudan kutuya): bağlantı merkez yüksekliği
YC = dict(TOPPING=2010.0, F=920.0, K=1500.0, E=1500.0, B=360.0, QR=120.0)
HAVALI = ("TOPPING", "F", "K", "E")
# --- ana kanal (duvarda, makinenin arkasında): x 2160–5160 · y 740–840 · z −938…−866
KANAL = dict(x=(1570.0, 5160.0), y=(740.0, 840.0), z=(-938.0, -866.0), t=1.5)
YUKSELIS = dict(x=(3925.0, 3995.0), y=(840.0, 2080.0))            # pano iniş (dik) kanalı, aynı z
DIRSEK = dict(x=(3925.0, 3995.0), y=(2080.0, 2168.0), z=(-940.0, -830.0))   # duvar ↔ U arka sacı bağlantı kutusu
INIS = dict(x=(5060.0, 5140.0), y=(50.0, 740.0))                  # E ucu zemine iniş (aynı z)
ZEMIN = dict(x=(5060.0, 5140.0), y=(0.0, 50.0), z=(-938.0, 560.0))   # zemin kanalı (E altı + koridor)
ZEMIN_BAS = dict(x=(5060.0, 5400.0), y=(0.0, 50.0), z=(560.0, 668.0))  # QR önü başlık
ROBOT_KUTU = dict(x=(4930.0, 5060.0), y=(0.0, 130.0), z=(300.0, 420.0))
