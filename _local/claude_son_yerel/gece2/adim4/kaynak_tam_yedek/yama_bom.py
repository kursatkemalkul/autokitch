# -*- coding: utf-8 -*-
import io
H = r"@@KOK_W@@\b3\arastirma\_uretec\h3\\"
def yama(f, R):
    P = H + f; s = io.open(P, encoding="utf-8").read()
    for a, b in R:
        assert s.count(a) == 1, (f, a[:70], s.count(a)); s = s.replace(a, b)
    compile(s, P, "exec"); io.open(P, "w", encoding="utf-8").write(s); print("ok", f, len(R))
yama("h3_elk_ist_v1.py", [
 ('"Soğutma grubu besleme + kontrol 5 × 1,5 (Secop KLF6.6 → pano)", 1, "", ""', '"Soğutma grubu besleme + kontrol 5G1,5 (Secop KLF6.6 → pano)", 1, "Lapp ÖLFLEX CLASSIC 110 5G1,5 1119305", "Ø 8,1"'),
 ('"Motor kablosu ekranlı 4 × 0,75 + fren (M23 → sürücü)", 4, "", ""', '"Step motor uzatma kablosu 6,1 m (STP-MTR-23079 kendi soketi → sürücü)", 4, "AutomationDirect STP-EXT-020", "kaset motorları step (TOPPING CAD) · fren yok"'),
 ('"Sürücü güç + kontrol kablosu 7 × 0,5 ekranlı (sürücü → pano)", 4, "", ""', '"Sürücü güç + kontrol kablosu 7G0,5 ekranlı (sürücü → pano)", 4, "Lapp ÖLFLEX CLASSIC 110 CY 7G0,5 1135007", "Ø 8,9 (modelde gerçek çap)"'),
 ('''        sabit("TOPPING_surucu_%d_pano" % i, [(xs, 1477.0, -730.0), (xs, yj, -730.0), (xl, yj, -730.0), (xl, yj, -815.0), (xl, 1879.8, -815.0)], 3.0, "C",''',
  '''        sabit("TOPPING_surucu_%d_pano" % i, [(xs, 1477.0, -730.0), (xs, yj, -730.0), (xl, yj, -730.0), (xl, yj, -815.0), (xl, 1879.8, -815.0)], 4.45, "C",'''),
 ('"Fan kablosu 3 × 0,5 (EC fan → pano)", 2, "", ""', '"Fan kablosu 4 × 0,5 (San Ace 9WPA 24 V PWM + hız → pano)", 2, "Lapp ÖLFLEX CLASSIC 110 4X0,5 1119754", "Ø 5,7 · 4 damar VARSAYIM (fan föyü)"'),
 ('"Valf adası çok damarlı kablo 25 × 0,34 (D-sub → KD1 → pano)", 1, "", ""', '"Valf adası çok damarlı kablo 25 × 0,3 (D-sub → KD1 → pano)", 1, "SMC AXT100-DS25-050", "VARSAYIM: ada SMC D-sub tipi ise"'),
 ('"Motor kablosu 4 × 1 + fren (sabit tahrik → KD1)", 1, "", ""', '"Motor kablosu 4 × 1 + fren (sabit tahrik → KD1)", 1, "", "VARSAYIM: motor üreticisi seçilince (NEMA23 kapalı çevrim step)"'),
 ('"Sensör kablosu M8 3 × 0,25 PUR", 4, "", "tabla boş', '"Sensör kablosu M8 3 kutup PUR 5 m (Murrelektronik 7000-08041-6300500, Ø 4,1)", 4, "", "tabla boş'),
 ('"Motor kablosu 4 × 1 (yükleme bandı → fırın gövdesi arkası → TOPPING KD1)", 1, "", ""', '"Step motor uzatma kablosu 6,1 m (yükleme bandı STP-MTR-23079 → TOPPING)", 1, "AutomationDirect STP-EXT-020", "yol ≤ 6,1 m"'),
 ('"Motor kablosu esnek PUR 4 × 0,75 + fren (X ekseni)", 1, "", "sürücüsü TOPPING panosunda"', '"Motor kablosu esnek PUR 4 × 0,75 + fren (X ekseni)", 1, "", "VARSAYIM: motor üreticisi seçilince · sürücüsü TOPPING panosunda"'),
 ('"Cihaz kabloları K (motor 4 × 0,75 · sensör M8/M12 PUR · PulsaJet M8)", len(kk) + 1, "", ""', '"Cihaz kabloları K (step motor · sensör M8/M12 PUR · PulsaJet M8)", len(kk) + 1, "STP-EXT-020 · Murrelektronik 7000-08041-6300500 / 7000-12221-6340500", ""'),
 ('"Yük hücresi kablosu 6 × 0,25 ekranlı (PW15AH → SIWAREX WP231)", 1, "", ""', '"Yük hücresi kendi kablosu 6 m (PW15AH → SIWAREX WP231)", 1, "HBM PW15AH (6 m kablo seçeneği)", "ayrı kablo yok"'),
 ('"Kompresör kablosu 3 × 1,5 + termik (Secop NLE8.8CN → dolap panosu)", 1, "", "kondenser', '"Kompresör kablosu 3G1,5 (Secop NLE8.8CN → dolap panosu · termik koruma kompresörün içinde)", 1, "Lapp ÖLFLEX CLASSIC 110 3G1,5 1119303", "kondenser'),
 ('"Fan kablosu 3 × 0,5 (4414 FL → kolon kanalı)", 4, "", ""', '"Fan kablosu 2 × 0,5 (4414 FL 24 V DC → kolon kanalı)", 4, "Lapp ÖLFLEX CLASSIC 110 2X0,5 1119752", "Ø 4,8"'),
 ('''RK_BOM = lambda n: ("Kablo rakoru IP68 PA (M16/M20) + kontra somun", n, "sac geçişi", "delik montajda açılır")''',
  '''RK_BOM = lambda n: ("Kablo rakoru IP68 PA M16 / M20 + kontra somun (kalın duvarda kovan + iç sacta rakor)", n, "Lapp SKINTOP ST-M 53111010 / 53111020 + GMP-GL-M 53119010 / 53119020", "delik montajda açılır")'''),
 ('''KB = ("Kablo kanalı PVC kapaklı (parmak yuvalı) · 28 × 40 / 38 × 40", 2,''', '''KB = ("Kablo kanalı PVC kapaklı (parmak yuvalı) · 30 × 40 / 40 × 40 (model KD1 28 geniş: AÇIK +2 mm)", 2,'''),
])
yama("h3_elk_hat_v1.py", [
 ('"Taban rakoru M25 (güç 3G2,5 + Cat6A)", 1, "Lapp SKINTOP MS-M"', '"Taban rakoru M32 + 2 delikli conta (güç 3G2,5 + Cat6A)", 1, "Lapp SKINTOP MS-M 32 + DIX-M (VARSAYIM conta no.)"'),
 ('"Dikey kablo kanalı PVC 30 × 34 (teknik sütun arka-sol köşe) + kapak", 1, "arka sacına perçin"', '"Dikey kablo kanalı PVC 30 × 40 (teknik sütun arka-sol köşe) + kapak", 1, "Hager tehalit BA7A40030 (model 34 derin: AÇIK)"'),
 ('"Pano altı kablo kanalı PVC 35 × 34 (+ kapak) · teknik sütun", 1, "arka sacına perçin"', '"Pano altı kablo kanalı PVC 40 × 40 (+ kapak) · teknik sütun", 1, "Hager tehalit BA7A40040 (model 35 × 34: AÇIK)"'),
 ('"Üst hat kablo kanalı PVC 60 × 40 + kapak (U_KE)", 1, "arka / yan saca konsollu", ""', '"Üst hat kablo kanalı PVC 60 × 40 + kapak (U_KE)", 1, "Hager tehalit BA7A40060 / OBO LK4 40060 6178014", ""') if False else ('"Rakor M25 çift delikli conta (güç + veri) · U tabanı + istasyon tavanı", 3, "Lapp SKINTOP"', '"Rakor M32 + 2 delikli conta (güç 3G2,5 + Cat6A) · U tabanı + istasyon tavanı", 3, "Lapp SKINTOP MS-M 32 + DIX-M (VARSAYIM conta no.)"'),
 ('"İstasyon besleme demeti (3G2,5 H07RN-F + Cat6A S/FTP, spiral sargılı)" if nm == "E" else None, 3, "", ""', '"İstasyon besleme demeti (3G2,5 H07RN-F + Cat6A S/FTP, spiral sargılı)" if nm == "E" else None, 3, "Lapp H07RN-F 3G2,5 1600118 + ETHERLINE Cat.6A 2170465", "Ø 12,5 + 8,7"'),
])
