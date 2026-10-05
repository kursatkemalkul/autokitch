# -*- coding: utf-8 -*-
"""ADIM 3 · uretec yamalari: kaset_birlesim_v1 -> v2, kasar_cad_v14 -> v15, sucuk_cad_v8 -> v9 (eski dosyalar DEGISMEZ). python yama_uret.py <_uretec klasoru>"""
import io, os, sys
U = sys.argv[1]
def oku(a): return io.open(os.path.join(U, a), encoding="utf-8").read()
def yaz(a, s): io.open(os.path.join(U, a), "w", encoding="utf-8").write(s); print("yazildi", a)
def deg(s, a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); return s.replace(a, b)
NL = "\n"
# ---- kaset_birlesim_v2
s = oku("kaset_birlesim_v1.py")
s = deg(s, '"""AUTOKITCH · KASET BİRLEŞİM DETAYLARI v1 (22 Eyl 2026)',
        '"""v2 (3 Eki 2026 · HAT v3 gece 2 adım 3): (1) yatak_kapagi(..., z_arka) — kapağın arka alın yüzü parametre (varsayılan 236 = v1 ile AYNI);' + NL +
        'kaşar v15 238 kullanır: çıkış borusunun ön dış yüzü (BZ 212,5 + r 25 = 237,5) kapağın bayonet dudağına 1,5 mm giriyordu.' + NL +
        '(2) web_ag: GEÇME yüzeyli parçalar + yuvalarındaki iki O-ring (INCE) web/montaj modeline İNCE ağla (0,02 mm / 0,1 rad) gider — kaba ağın' + NL +
        '(0,12 / 0,35 rad; O-ring 0,4 / 0,8) kirişleri 0,2–0,3 mm geçme boşluklarından büyük (r 39 deliğin kirişi 0,6 mm içeri sarkar) → montajda sahte' + NL +
        'çakışma: sucuk kapak ↔ tüp 0,92, gövde ↔ plaka kanalı 0,22, kapak ↔ O-ring 0,33.' + NL +
        'AUTOKITCH · KASET BİRLEŞİM DETAYLARI v1 (22 Eyl 2026)')
s = deg(s, "def yatak_kapagi(RT, CY, TUP_Z1):", "def yatak_kapagi(RT, CY, TUP_Z1, z_arka=236.0):")
s = deg(s, "kp = silz(0, CY, RD + 4.0, 236.0, 254.5)",
        'assert z_arka <= Z_HALKA - 2.0, "bayonet dudagi en az 2 mm kalmali"' + NL + "    kp = silz(0, CY, RD + 4.0, z_arka, 254.5)")
s = deg(s, 'KABA = ("saplama_",',
        'INCE = ("govde", "plaka_on", "plaka_arka", "conta_on", "conta_arka", "cikis_tupu", "yatak_kapagi", "oring_tup", "oring_kapak")   # v2: geçme yüzeyli parçalar + yuvalarındaki O-ringler · ince web ağı' + NL +
        'KABA = ("saplama_",')
s = deg(s, '    if p["ad"].startswith(KABA): return ag(cq.Workplane(obj=p["wp"].val().copy()), 0.4, 0.8)',
        '    if p["ad"] in INCE: return ag(cq.Workplane(obj=p["wp"].val().copy()), 0.02, 0.1)        # v2: geçme yüzeyleri (kiriş sarkması < 0,05) · KABA\'dan ÖNCE (O-ringler ikisinde de)' + NL +
        '    if p["ad"].startswith(KABA): return ag(cq.Workplane(obj=p["wp"].val().copy()), 0.4, 0.8)')
yaz("kaset_birlesim_v2.py", s)
# ---- kasar_cad_v15
s = oku("kasar_cad_v14.py")
s = deg(s, '# -*- coding: utf-8 -*-' + NL + '"""', '# -*- coding: utf-8 -*-' + NL +
        '"""v15 (3 Eki 2026 · HAT v3 gece 2 adım 3) — v14\'ten FARK, YALNIZ: (1) YATAK KAPAĞI arka alın yüzü z 236 → 238 (bayonet dudağı 4,3 → 2,3 mm):' + NL +
        'çıkış borusu (eksen z 212,5 · dış r 25 → ön dış yüzü z 237,5) kapağın dudağına 1,5 mm giriyordu (üretecin kendi taraması: cikis_tupu × yatak_kapagi 62,4 mm³;' + NL +
        'montaj taraması x 2088 · y 1165 · z −125); şimdi 0,5 mm boşluk. Boru ekseni / çapı, tüp boyu, tırnaklar, cep / tümsek / dayama kotları, kapağın ön yüzü (z 266)' + NL +
        've kasetin dış ölçüsü DEĞİŞMEDİ. (2) birleşim kodu kaset_birlesim_v2 (geçme yüzeyli 7 parça + 2 O-ring web ağı ince). Önceki sürüm: kasar_cad_v14.py' + NL)
s = deg(s, "import kaset_birlesim_v1 as BR", "import kaset_birlesim_v2 as BR")
s = deg(s, "kp = BR.yatak_kapagi(RT, CY, TUP_Z1)", "kp = BR.yatak_kapagi(RT, CY, TUP_Z1, z_arka=KAPAK_Z_ARKA)")
s = deg(s, "TUP_Z1 = 246.5" + NL, "TUP_Z1 = 246.5" + NL +
        "KAPAK_Z_ARKA = 238.0                                                 # v15: yatak kapağı arka alın yüzü (v14: 236 → boruya 1,5 mm giriyordu) · boru ön dış yüzü 237,5 + 0,5 boşluk" + NL)
s = s.replace("kasar_kabi_v14", "kasar_kabi_v15").replace("kasar_v14", "kasar_v15")
yaz("kasar_cad_v15.py", s)
# ---- sucuk_cad_v9
s = oku("sucuk_cad_v8.py")
s = deg(s, '# -*- coding: utf-8 -*-' + NL + '"""', '# -*- coding: utf-8 -*-' + NL +
        '"""v9 (3 Eki 2026 · HAT v3 gece 2 adım 3) — v8\'den FARK: (1) ÇIKIŞ TÜPÜNDE koni geçiş tüpün ön ucunda kırpılır — v8\'de koninin üst ucu tüp ucunun 2,5 mm' + NL +
        'önüne gaga gibi çıkıyordu → ön muylu ∩ tüp 16 mm³, kapak ∩ tüp 2,5 mm³ (üretecin kendi taraması "2 BULGU" yazıyordu). (2) birleşim kodu kaset_birlesim_v2:' + NL +
        'geçme yüzeyli 7 parça + 2 O-ring web/montaj modeline İNCE ağla (kaba ağın kirişleri montajda sahte çakışma veriyordu — kapak deliği Ø78,6 ↔ tüp Ø78 0,92 mm,' + NL +
        'gövde ↔ plaka kanalı 0,22 mm). Diğer katılar v8 ile AYNI. Önceki sürüm: sucuk_cad_v8.py' + NL)
s = deg(s, "import kaset_birlesim_v1 as BR", "import kaset_birlesim_v2 as BR")
_e = "    boru = koni_y(BZ, RB_, RT + 3.0, YG_, CY).union(sily(0, BZ, RB_, BORU_ALT, YG_))                      # tüp çapında başlar, konik daralır, düz iner" + NL
s = deg(s, _e, _e + "    boru = boru.intersect(kut(-RD - 20.0, RD + 20.0, BORU_ALT - 1.0, CY, ZF, TUP_Z1))                      # v9: koni tüp boyunca (ZF … TUP_Z1) kırpılır — v8'de koninin üst ucu" + NL +
        "    #   (y 60'ta r 39, eksen z 210 → z 249'a kadar) tüpün ÖN UCUNU 2,5 mm aşıyordu: tüp ucunun önünde gaga → ön muylu ∩ tüp 16 mm³ + yatak kapağı ∩ tüp 2,5 mm³" + NL)
s = s.replace("sucuk_kaseti_v8", "sucuk_kaseti_v9").replace("sucuk_v8", "sucuk_v9")
yaz("sucuk_cad_v9.py", s)
