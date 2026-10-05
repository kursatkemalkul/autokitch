# -*- coding: utf-8 -*-
"""topping_cad_v30 → v31 (30 Eyl 2026 · YEREL · Claude).
Kemal: "tamam önerdiğini yap toppinge": evaporatör soğuk odadan çıkar → KURU BÖLMEDE, soğutma grubunun TAM ÜSTÜNDE yalıtımlı KASET (sanayi dolabı monoblok düzeni).
  · kaset 540 × 382 × 196 (dünya x 1470–2010 · y 1473–1855 · z −826…−630): dış sac 1,0 + PU 40 + iç sac 1,0 · önde POM ısı kesici çerçeve · soğuk kutunun arka
    duvarına TAKILIR (topping_uno_cad_v19: arka dış sac kasetin önünde kesik, kutunun PU'su kasetin ön yalıtımı → metal köprü yok)
  · içi: alt bölge (dönüş kanalı → 16 mm ön aralık → lamel paketi öne→arkaya → 53 mm arka baca) · ara sac · üst bölge (emiş odası → 2 fan → üfleme odası → üst kanal)
  · damlama tavası → Ø8 sifonlu tahliye DÜMDÜZ aşağı → ünitenin ATIŞ havasındaki SICAK GAZ döngülü yoğuşma tavası (v18'in elektrikli kabı kalktı)
  · soğutma hatları ünitenin üstünden DİKİNE kasetin altına (≈ 39 cm; v18 ≈ 70 cm) · kaset ek ısı kaybı KLF6.6CND pay denetimine eklendi
Yalnız okur: topping_cad_v30.py · yazar: topping_cad_v31.py"""
import io, os, sys

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v30.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a), n)
    s = s.replace(a, b)


# ---------------------------------------------------------------- 0 · başlık + TU dosyası
degis('"""topping_cad_v30 (29 Eyl 2026 gece · YEREL · yap_topping_cad_v30.py): ',
      '"""topping_cad_v31 (30 Eyl 2026 · YEREL · yap_topping_cad_v31.py): EVAPORATÖR KASETİ KURU BÖLMEDE (soğutma grubunun tam üstü) · SICAK GAZLI YOĞUŞMA TAVASI · soğuk kutu topping_uno_cad_v19\n'
      'v31: Kemal 30 Eyl "tamam önerdiğini yap toppinge": evaporatör soğuk odadan çıktı → kuru bölmede 40 mm PU\'lu kaset, soğuk kutunun arka duvarına takılı (arka dış sac kesik,\n'
      '     kutunun PU\'su kasetin ön yalıtımı) · alt kanaldan emer → lamel paketi → arka baca → 2 fan → üst kanaldan tavan boyunca kapağa üfler · tahliye sifonlu, dümdüz\n'
      '     aşağı → ünitenin atış havasındaki sıcak gaz döngülü tavaya · hatlar ünitenin üstünden dikine kasete (≈ 39 cm)\n'
      'v30: topping_cad_v30 (29 Eyl 2026 gece · YEREL · yap_topping_cad_v30.py): ')
degis('TU_DOSYA = os.environ.get("TOPPING_TU", "topping_uno_cad_v18.py")   # v30: dikdörtgen soğuk kutu + eşit kapaklar',
      'TU_DOSYA = os.environ.get("TOPPING_TU", "topping_uno_cad_v19.py")   # v31: evaporatör kuru bölmede (arka duvarda 2 kanal + kaset yuvası)   # v30: dikdörtgen soğuk kutu + eşit kapaklar')

# ---------------------------------------------------------------- 1 · sabitler (DÜNYA ölçüleri)
SABIT = r'''
# v31 · EVAPORATÖR KASETİ (Kemal 30 Eyl: "tamam önerdiğini yap"): soğuk odadaki evaporatör (TU v18) → KURU BÖLMEDE, soğutma grubunun TAM ÜSTÜNDE · DÜNYA ölçüleri
#       yer: pano (x ≤ 1450) ile DIN plakası (x ≥ 2020) arası · hava hattının (y ≤ 1467) üstü · servis kapağının (y 1860,5) altı · grup x 1633–2013 tam altında
KSET = dict(x=(1470.0, 2010.0), y=(1473.0, 1855.0), z=(-826.0, -630.0))            # dış zarf 540 × 382 × 196 (önü kutunun arka duvarında: TU v19 KASET_KESIK 1492–1988 × 1495–1833)
KSET_CER = 10.0                                                                     # POM-C ısı kesici çerçeve (z −640…−630): sacların ön kenarı buna, çerçeve kutunun arka dış sacına + ABS yüzüne basar (conta dudağı)
KSET_DIS, KSET_PU, KSET_IC = 1.0, 40.0, 1.0                                         # dış sac 304 1,0 · PU 40 (λ 0,022 · 40 kg/m³) · iç sac 304 1,0
KSET_BOS = (1512.0, 1968.0, 1515.0, 1813.0, -784.0, -630.0)                         # iç boşluk (ön yüzü kutunun ABS yüzü · TU v19 arka_duvar_kaset_yuzu)
KSET_BOBIN = (1513.0, 1910.0, 1533.0, 1670.0, -731.0, -646.0)                       # lamel paketi (hava öne→arkaya, z boyunca 85) · ön aralık 16 · arka baca 53 · sağında kollektör bölmesi
KSET_ARA_Y = (1670.0, 1671.5)                                                       # ara sac: alt bölge (dönüş + bobin) | üst bölge (fanlar + üfleme)
KSET_KOL_X = (1910.0, 1911.5)                                                       # kollektör ayırma sacı (dağıtıcı + genleşme valfi bölmesi hava yolunun dışında)
KSET_FAN_Z = (-701.5, -700.0)                                                       # fan plakası: önü üfleme odası (−700…−630), arkası emiş odası (−784…−701,5)
KSET_TAVA = (1513.0, 1910.0, 1515.0, 1533.0, -783.0, -631.0)                        # damlama tavası 304 1,0 (bobin + baca altı) · çıkış sağ-arka köşe
KSET_TAHLIYE = [(1895.0, 1515.0, -775.0), (1895.0, 1440.0, -775.0), (1895.0, 1440.0, -805.0), (1895.0, 1462.0, -805.0), (1895.0, 1462.0, -815.0),
                (1895.0, 1115.0, -815.0), (2120.0, 1115.0, -815.0), (2120.0, 950.0, -815.0), (2120.0, 950.0, -770.0), (2120.0, 940.0, -770.0)]   # Ø8 · sifon 1440 → 1462 (22 mm su) · uç yoğuşma tavasının üstünde (hava boşluklu)
KSET_HAT = {"sogutma_emis_hatti": (1950.0, -700.0, 15.5, 6.35), "sogutma_sivi_hatti": (1928.0, -700.0, 3.175, 3.175)}   # x, z, dış r (emiş Cu Ø12,7 + Armaflex 9), çıplak Cu r
KSET_HAT_Y = (1087.0, 1473.0, 1540.0)                                               # ünitenin üstü · kasetin altı (POM geçiş bloğu) · kollektör bölmesi (dağıtıcı / TXV zarfı altı)
YT = (2098.0, 2142.0, 893.5, 933.5, -780.0, -490.0)                                 # yoğuşma tavası (teknik bölme, ünitenin ATIŞ havasında · cep kenarı 2095 ↔ taban açıklığı 2145 arası dolu sac)
SICAK_GAZ = [(2013.0, 980.0, -700.0), (2120.0, 980.0, -700.0), (2120.0, 905.0, -700.0), (2120.0, 905.0, -560.0), (2120.0, 980.0, -560.0), (2013.0, 980.0, -560.0)]   # Cu Ø6,35 basma hattı döngüsü
# v31 · FANLAR (katalog ölçüsüyle; STEP indirilmedi) · hava debisi + kanal hızları + bobin UA denetimi dünya denetiminde
FAN = dict(ad="Sanyo Denki San Ace 120W", kod="9WPA1224P4G001", a=120.0, t=25.0, r_bogaz=57.5, r_gobek=21.0, merkez=((1620.0, 1742.0), (1800.0, 1742.0)),
           q_serbest=198.0, q_isletme=110.0, p_isletme=40.0, P=7.4,
           kaynak="Sanyo Denki TR59 (05-2025) s. 11–13: IP68 · 24 V · 6,0 W · 4250 d/dk · 198 m³/h serbest · 135 Pa · −20…+70 °C · PWM hız girişi · 240 g")
#       işletme: tam hızda ≈ 130–145 m³/h @ 55–60 Pa (eğri okuması ±%15) · sistem ≈ 55 Pa @ 2 × 130 → %85 hızda 2 × 110 m³/h @ ≈ 40 Pa (fan yasaları: Q ∝ n, p ∝ n², P ∝ n³ → 2 × 3,7 W)
BOBIN_ALAN_YOG = 400.0                                                              # m²/m³ · lamel adımı 4,5 mm (ASHRAE 2018 Refr. Ch. 14: 0 °C altı yüzey 4–8 mm), Ø9,52 boru (dış yüzey yoğunluğu, [V] — soğutmacı firma kesinleştirir)
U_BOBIN = (25.0, 35.0)                                                              # W/m²K · küçük dolap evaporatörü, ıslak, 1–2 m/s (dış yüzeye göre, [V]; kıyas: Kelvion Küba FMA 011D 1,2 m² · 85 m³/h)
FAN_EV_ESKI = 10.0                                                                  # W · GEREKEN_DIK içindeki fan ısısı varsayımı (sogutma_topping_v1 FAN_EV)
YOGUSMA_GUN = 576.0                                                                 # g/gün · kapak açılışı + dolum (sogutma_topping_v1 · S2 dolum günü) + defrost suyu
EK_T_KURU = 8.0                                                                     # K · kuru bölme ortamın üstünde (sogutma_topping_v1 varsayımı)
EK_PSI = 0.03                                                                       # W/mK · POM ısı kesici çerçeve (sac ön kenarları ↔ soğuk iç), [V]


def ek_kaset(t_ortam):
    """v31 · kasetin getirdiği EK ısı (W) · ortam t_ortam °C: 5 yüz U·A·ΔT (h dış 10 · PU 40 · h iç 20) + çerçeve ψ·L·ΔT − kasetin örttüğü duvarın artık kaybetmediği
    ısı (kutu duvarı U 0,36 · kesik alanı) + (fan gücü − eski varsayım 10 W) · kaset içi ≈ 0 °C · oda +3 °C"""
    (x0, x1), (y0, y1), (z0, z1) = KSET["x"], KSET["y"], KSET["z"]
    a_, b_, c_ = (x1 - x0) / 1000.0, (y1 - y0) / 1000.0, (z1 - KSET_CER - z0) / 1000.0
    A = 2.0 * a_ * c_ + 2.0 * b_ * c_ + a_ * b_
    U_ = 1.0 / (1.0 / 10.0 + KSET_PU / 1000.0 / 0.022 + 1.0 / 20.0)
    dT = t_ortam + EK_T_KURU - 0.0
    L_ = 2.0 * ((KSET_BOS[1] - KSET_BOS[0]) + (KSET_BOS[3] - KSET_BOS[2])) / 1000.0
    U_duv = 1.0 / (1.0 / 10.0 + 0.0575 / 0.022 + 1.0 / 20.0)
    A_kesik = (1988.0 - 1492.0) * (1833.0 - 1495.0) * 1e-6
    return A * U_ * dT + EK_PSI * L_ * dT - U_duv * A_kesik * (t_ortam + EK_T_KURU - 3.0) + (FAN["P"] - FAN_EV_ESKI)
'''
degis("GEREKEN_DIK = {32: 340.0, 35: 368.0, 38: 393.0, 40: 410.0}                         # W · dikdörtgen kutu, dolum + ılık gün (dikdortgen_sogutma_v1 = sogutma_topping_v1 yöntemi, TU v16/v18 geometrisi)\n",
      "GEREKEN_DIK = {32: 340.0, 35: 368.0, 38: 393.0, 40: 410.0}                         # W · dikdörtgen kutu, dolum + ılık gün (dikdortgen_sogutma_v1 = sogutma_topping_v1 yöntemi, TU v16/v18 geometrisi)\n" + SABIT)

# ---------------------------------------------------------------- 2 · kuru bölme tabanı: yeni hat + tahliye delikleri
degis('    for _hx, _hr in ((1990.0, 15.5), (1950.0, 3.2)):                                                       # soğutma hatları (TU v18 HAT_X_INIS · z −660)\n'
      '        _kt = _kt.cut(sily(_xl(_hx), -660.0, _hr + 1.0, _yl(1106.0), _yl(1110.0)))\n',
      '    for _ha, (_hx, _hz, _hr, _hri) in KSET_HAT.items():                                                    # v31 · soğutma hatları (ünite → kaset, dikine)\n'
      '        _kt = _kt.cut(sily(_xl(_hx), _hz, _hr + 1.0, _yl(1106.0), _yl(1110.0)))\n'
      '    _kt = _kt.cut(sily(_xl(KSET_TAHLIYE[6][0]), KSET_TAHLIYE[6][2], 5.0, _yl(1106.0), _yl(1110.0)))        # v31 · kaset tahliyesi (Ø8 hortum, lastik rakor)\n')
degis('bom=("Kuru bölme tabanı AISI 304 1,5", 1, "hat + şartlandırıcı delikleri (lastik rakor)",',
      'bom=("Kuru bölme tabanı AISI 304 1,5", 1, "hat + şartlandırıcı + kaset tahliyesi delikleri (lastik rakor)",')

# ---------------------------------------------------------------- 3 · kaset parçaları (modul() içinde, kuru bölme sürücülerinden sonra)
KASET = r'''
    # ---------------- 7c · v31 · EVAPORATÖR KASETİ (kuru bölme · soğutma grubunun TAM ÜSTÜ) ----------------
    #   Kemal 30 Eyl: "tamam önerdiğini yap" · sanayi dolabı MONOBLOK düzeni: kaset soğuk kutunun arka duvarına TAKILIR (TU v19: arka dış sac kesik, kutunun PU'su kasetin
    #   ön yalıtımı, iki POM kanal) · hava: ALT kanaldan girer → 16 mm ön aralık → lamel paketi (öne→arkaya) → 53 mm arka baca → üst oda → 2 fan → üfleme odası → ÜST
    #   kanaldan tavan boyunca kapağa · bobin + genleşme valfi + dağıtıcı SOĞUTMACI FİRMA (zarf) · fanlar katalog ölçüsüyle · yoğuşma suyu Ø8 sifonlu hortumla dümdüz
    #   aşağı → ünitenin atış havasındaki SICAK GAZ döngülü tava (v18'in elektrikli kabı + hazne üstündeki hortumu kalktı) · servis: kuru bölmenin üst kapağı + kasetin üst paneli
    def _kw(x0, x1, y0, y1, z0, z1):
        return kut(_xl(x0), _xl(x1), _yl(y0), _yl(y1), z0, z1)
    (KX0, KX1), (KY0, KY1), (KZ0, KZ1) = KSET["x"], KSET["y"], KSET["z"]
    ZC = KZ1 - KSET_CER                                                          # −640 · sacların ön kenarı
    _d1 = KSET_DIS; _p1 = KSET_DIS + KSET_PU; _i1 = KSET_DIS + KSET_PU + KSET_IC
    assert abs(KX0 + _i1 - KSET_BOS[0]) < 0.01 and abs(KX1 - _i1 - KSET_BOS[1]) < 0.01 and abs(KY0 + _i1 - KSET_BOS[2]) < 0.01 and abs(KY1 - _i1 - KSET_BOS[3]) < 0.01 and abs(KZ0 + _i1 - KSET_BOS[4]) < 0.01
    _dl = _kw(KX0 + _d1, KX1 - _d1, KY0 + _d1, KY1 - _d1, KZ0 + _d1, ZC + 1.0)              # dış sacın içi (önü açık)
    _ic_ic = _kw(KSET_BOS[0], KSET_BOS[1], KSET_BOS[2], KSET_BOS[3], KSET_BOS[4], ZC + 1.0)
    _ic_dis = _kw(KX0 + _p1, KX1 - _p1, KY0 + _p1, KY1 - _p1, KZ0 + _p1, ZC)
    _ic_dis_c = _kw(KX0 + _p1, KX1 - _p1, KY0 + _p1, KY1 - _p1, KZ0 + _p1, ZC + 1.0)
    _tx, _ty, _tz = KSET_TAHLIYE[0]
    _tdl = sily(_xl(_tx), _tz, 4.0, _yl(KY0 - 1.0), _yl(KY0 + _i1 + 1.0))                     # tahliye deliği (alt duvar)
    _gec = _kw(1915.0, 1965.0, KY0, KY0 + _i1, -720.0, -680.0)                                 # hat geçiş bloğunun yeri (alt duvar)
    _dsac = _kw(KX0, KX1, KY0, KY1, KZ0, ZC).cut(_dl).cut(_gec).cut(_tdl)
    ekle("evap_kaseti_dis_sac", _dsac, "sac",
         bom=("Evaporatör kaseti dış sacı AISI 304 1,0", 1, "%.0f × %.0f × %.0f · 5 yüz (önü açık, POM çerçeveye oturur) · üst panel 4 × M5 contalı sökülür (fan servisi)" % (KX1 - KX0, KY1 - KY0, ZC - KZ0),
              "v31 · kuru bölmede, soğutma grubunun TAM ÜSTÜNDE · alttan 2 askıya oturur, önden kutunun arka dış sacına 8 × M5 (perçin somun)"))
    _pu = _kw(KX0 + _d1, KX1 - _d1, KY0 + _d1, KY1 - _d1, KZ0 + _d1, ZC).cut(_ic_dis_c).cut(_gec).cut(_tdl)
    ekle("evap_kaseti_PU", _pu, "pu",
         bom=("Evaporatör kaseti PU yalıtımı 40 mm", 1, "poliüretan 40 kg/m³ · λ 0,022 · yerinde köpük (iki sac arası)", "v31 · kuru bölme (ortam + 8 K) ↔ kaset içi (≈ 0 °C) · ek kayıp dünya denetiminde"))
    _isac = _ic_dis.cut(_ic_ic).cut(_gec).cut(_tdl)
    ekle("evap_kaseti_ic_sac", _isac, "sac",
         bom=("Evaporatör kaseti iç sacı AISI 304 1,0", 1, "%.0f × %.0f × %.0f iç · köşeler kaynaklı · tahliye + hat geçişi delikli" % (KSET_BOS[1] - KSET_BOS[0], KSET_BOS[3] - KSET_BOS[2], ZC - KSET_BOS[4]),
              "v31 · hava yolunun dış duvarı (yoğuşma suyu tavaya akar)"))
    _cer = _kw(KX0, KX1, KY0, KY1, ZC, KZ1).cut(_kw(KSET_BOS[0], KSET_BOS[1], KSET_BOS[2], KSET_BOS[3], ZC - 1.0, KZ1 + 1.0))
    ekle("evap_kaseti_isi_kesici_cerceve", _cer, "pom",
         bom=("Kaset ısı kesici çerçevesi POM-C", 1, "%.0f × %.0f dış · %.0f bant · %.0f derin · ön yüzde conta dudağı (EPDM, TPE-V)" % (KX1 - KX0, KY1 - KY0, _i1, KSET_CER),
              "v31 · dış sac (sıcak) ile soğuk iç arasında metal yok (ψ ≈ 0,03 W/mK [V]) · kutunun arka dış sacına ve ABS kaset yüzüne basar → hava sızdırmaz"))
    ekle("evap_kaseti_hat_gecis_blogu", _gec.cut(sily(_xl(KSET_HAT["sogutma_emis_hatti"][0]), KSET_HAT["sogutma_emis_hatti"][1], KSET_HAT["sogutma_emis_hatti"][3], _yl(KY0 - 1.0), _yl(KY0 + _i1 + 1.0)))
                                          .cut(sily(_xl(KSET_HAT["sogutma_sivi_hatti"][0]), KSET_HAT["sogutma_sivi_hatti"][1], KSET_HAT["sogutma_sivi_hatti"][3], _yl(KY0 - 1.0), _yl(KY0 + _i1 + 1.0))), "pom",
         bom=("Kaset hat geçiş bloğu POM-C", 1, "50 × 42 × 40 · 2 delik hat çapında (silikonla sızdırmaz)", "v31 · emiş + sıvı hattı kasetin altından kollektör bölmesine"))
    for _i, _x0 in enumerate((1485.0, 1970.0)):                                               # emiş hattının (x ≤ 1965,5) sağında
        _as = _kw(_x0, _x0 + 30.0, KY0 - 3.0, KY0, KZ0, KZ1).union(_kw(_x0, _x0 + 30.0, KY0 - 33.0, KY0, KZ1 - 3.0, KZ1))
        ekle("evap_kaseti_askisi_%d" % _i, _as, "sac",
             bom=("Kaset askısı L 30 × 3 AISI 304", 2, "yatay kol kasetin altında (196) · dik kol kutunun arka dış sacına 2 × M6 (perçin somun)", "v31 · kaset + bobin ≈ 21 kg [V]: 2 askı + önde 8 × M5") if _i == 0 else None)
    _tv = _kw(*KSET_TAVA).cut(_kw(KSET_TAVA[0] + 1.0, KSET_TAVA[1] - 1.0, KSET_TAVA[2] + 1.0, KSET_TAVA[3] + 1.0, KSET_TAVA[4] + 1.0, KSET_TAVA[5] - 1.0))
    _tv = _tv.cut(sily(_xl(_tx), _tz, 4.0, _yl(_ty - 1.0), _yl(_ty + 2.0)))
    ekle("evap_kaseti_damlama_tavasi", _tv, "sac",
         bom=("Kaset damlama tavası AISI 304 1,0", 1, "%.0f × %.0f × %.0f · %%1 eğim sağ-arka köşedeki Ø8 çıkışa" % (KSET_TAVA[1] - KSET_TAVA[0], KSET_TAVA[5] - KSET_TAVA[4], KSET_TAVA[3] - KSET_TAVA[2]),
              "v31 · bobinin + arka bacanın altı · defrost suyu da buraya"))
    ekle("evap_kaseti_lamel_paketi", _kw(*KSET_BOBIN), "celik",
         bom=("Evaporatör lamel paketi (Al lamel 4,5 mm adım / Cu boru Ø9,52) · YAPTIRILACAK", 1,
              "%.0f × %.0f × %.0f (hava yönü %.0f) · yüzey ≈ %.1f m² [V]" % (KSET_BOBIN[1] - KSET_BOBIN[0], KSET_BOBIN[3] - KSET_BOBIN[2], KSET_BOBIN[5] - KSET_BOBIN[4], KSET_BOBIN[5] - KSET_BOBIN[4],
                                                                          BOBIN_ALAN_YOG * (KSET_BOBIN[1] - KSET_BOBIN[0]) * (KSET_BOBIN[3] - KSET_BOBIN[2]) * (KSET_BOBIN[5] - KSET_BOBIN[4]) * 1e-9),
              "v31 · soğutmacı firma: −10 °C buharlaşma, +3 °C oda, gereken UA dünya denetiminde · tava kenarlarına oturur, üstü ara saca"))
    ekle("evap_kaseti_alt_conta_lamasi", _kw(KSET_TAVA[0] + 1.0, KSET_TAVA[1] - 1.0, KSET_TAVA[2] + 1.0, KSET_BOBIN[2], KSET_BOBIN[5] - 1.0, KSET_BOBIN[5]), "sac",
         bom=("Bobin altı sızdırmazlık laması AISI 304 1,0", 1, "bobinin ön alt kenarı · altında 1 mm su çentikleri", "v31 · hava bobinin altından arka bacaya kaçmaz"))
    ekle("evap_kaseti_kollektor_ayirma_saci", _kw(KSET_KOL_X[0], KSET_KOL_X[1], KSET_BOS[2], KSET_ARA_Y[0], KSET_BOS[4], KSET_BOS[5]), "sac",
         bom=("Kollektör ayırma sacı AISI 304 1,0", 1, "bobin uç plakasının devamı", "v31 · dağıtıcı + genleşme valfi bölmesi hava yolunun dışında"))
    ekle("evap_kaseti_kollektor_TXV_zarfi", _kw(KSET_KOL_X[1], 1960.0, KSET_HAT_Y[2], 1640.0, -760.0, -660.0), "koyu",
         bom=("Dağıtıcı + termostatik genleşme valfi (R290) · YER ZARFI", 1, "48,5 × 100 × 100 [V]", "v31 · soğutmacı firma (hat uçları buraya)"))
    _ara = _kw(KSET_BOS[0], KSET_KOL_X[0], KSET_ARA_Y[0], KSET_ARA_Y[1], KSET_BOBIN[4], KSET_BOS[5]).union(_kw(KSET_KOL_X[0], KSET_BOS[1], KSET_ARA_Y[0], KSET_ARA_Y[1], KSET_BOS[4], KSET_BOS[5]))
    ekle("evap_kaseti_ara_saci", _ara, "sac",
         bom=("Kaset ara sacı AISI 304 1,0", 1, "bobin üstünden öne (arka baca açık)", "v31 · alt bölge (dönüş + bobin) ile üst bölgeyi (fanlar + üfleme) ayırır"))
    _fp = _kw(KSET_BOS[0], KSET_BOS[1], KSET_ARA_Y[1], KSET_BOS[3], KSET_FAN_Z[0], KSET_FAN_Z[1])
    for _fx, _fy in FAN["merkez"]:
        _fp = _fp.cut(silz(_xl(_fx), _yl(_fy), FAN["r_bogaz"], KSET_FAN_Z[0] - 1.0, KSET_FAN_Z[1] + 1.0))
    ekle("evap_kaseti_fan_plakasi", _fp, "sac",
         bom=("Kaset fan plakası AISI 304 1,5", 1, "2 fan boğazı Ø%.0f" % (2 * FAN["r_bogaz"]), "v31 · önü üfleme odası, arkası emiş odası"))
    for _i, (_fx, _fy) in enumerate(FAN["merkez"]):
        _a2 = FAN["a"] / 2.0; _z0 = KSET_FAN_Z[0] - FAN["t"]; _z1 = KSET_FAN_Z[0]
        _fr = _kw(_fx - _a2, _fx + _a2, _fy - _a2, _fy + _a2, _z0, _z1).cut(silz(_xl(_fx), _yl(_fy), FAN["r_bogaz"], _z0 - 1.0, _z1 + 1.0))
        _fr = _fr.union(silz(_xl(_fx), _yl(_fy), FAN["r_gobek"], _z0 + 4.0, _z1 - 4.0))
        for _k in range(5):                                                                   # 5 kanat (düz levha, gösterim)
            _kn = kut(_xl(_fx) + FAN["r_gobek"] - 1.0, _xl(_fx) + FAN["r_bogaz"] - 2.0, _yl(_fy) - 12.0, _yl(_fy) + 12.0, (_z0 + _z1) / 2.0 - 1.5, (_z0 + _z1) / 2.0 + 1.5)
            _fr = _fr.union(_kn.rotate((_xl(_fx), _yl(_fy), 0.0), (_xl(_fx), _yl(_fy), 1.0), 72.0 * _k + 15.0))
        ekle("evap_kaseti_fani_%d" % _i, _fr, "motor",
             bom=("Eksenel fan %s %s" % (FAN["ad"], FAN["kod"]), 2, "%.0f × %.0f × %.0f · %s" % (FAN["a"], FAN["a"], FAN["t"], FAN["kaynak"]),
                  "v31 · fan plakasının arkasına 4 × M4 · emiş odasından çekip üfleme odasına basar · %%85 hız (PWM): %.0f m³/h @ ≈ %.0f Pa · fırçasız DC (R290 bölmesinde kıvılcım yapmaz [V])"
                  % (FAN["q_isletme"], FAN["p_isletme"])) if _i == 0 else None)
    for _ha, (_hx, _hz, _hr, _hri) in KSET_HAT.items():
        ekle(_ha, sily(_xl(_hx), _hz, _hr, _yl(KSET_HAT_Y[0]), _yl(KSET_HAT_Y[1])), "koyu" if "emis" in _ha else "celik",
             bom=(("Emiş hattı Cu Ø12,7 + Armaflex 9 mm (dış Ø31)" if "emis" in _ha else "Sıvı hattı Cu Ø6,35"), 1, "ünitenin üstünden (y %.0f) DİKİNE kasetin altına (y %.0f) · %.0f mm" % (KSET_HAT_Y[0], KSET_HAT_Y[1], KSET_HAT_Y[1] - KSET_HAT_Y[0]),
                  "v31 · kuru bölme tabanından geçer (lastik rakor) · v18: ≈ 700 mm, arka duvar bloğundan · montaj + gaz dolumu soğutmacı firma"))
        ekle(_ha + "_ic", sily(_xl(_hx), _hz, _hri, _yl(KSET_HAT_Y[1]), _yl(KSET_HAT_Y[2])), "celik",
             bom=("Hat ucu Cu (kaset içi)", 1, "geçiş bloğundan kollektör bölmesine", "v31") if "emis" in _ha else None)
    _th = [(_xl(p_[0]), _yl(p_[1]), p_[2]) for p_ in KSET_TAHLIYE]
    ekle("evap_kaseti_tahliye_hortumu", TU_BORU(_th, 4.0), "silikon",
         bom=("Kaset tahliye hortumu silikon Ø8 · SİFONLU", 1, "tava çıkışı → sifon (%.0f → %.0f, %.0f mm su) → dümdüz aşağı → kuru bölme tabanı → yoğuşma tavasının üstünde hava boşluklu biter"
              % (KSET_TAHLIYE[1][1], KSET_TAHLIYE[3][1], KSET_TAHLIYE[3][1] - KSET_TAHLIYE[1][1]),
              "v31 · sifon: kasetin alt bölgesi fan emişinde (eksi basınç) → teknik bölmenin sıcak havası tahliyeden kasete çekilmez"))
    _yt = _kw(*YT).cut(_kw(YT[0] + 1.0, YT[1] - 1.0, YT[2] + 1.0, YT[3] + 1.0, YT[4] + 1.0, YT[5] - 1.0))
    ekle("yogusma_tavasi_sicak_gazli", _yt, "sac",
         bom=("Yoğuşma buharlaştırma tavası AISI 304 1,0 · SICAK GAZ döngülü", 1, "%.0f × %.0f × %.0f (%.2f L) · TC tabanına 2 × M5" % (YT[1] - YT[0], YT[5] - YT[4], YT[3] - YT[2], (YT[1] - YT[0] - 2) * (YT[5] - YT[4] - 2) * (YT[3] - YT[2] - 1) * 1e-6),
              "v31 · ünitenin ATIŞ havasında (x 2098–2142, cep kenarı ile taban açıklığı arası) · kompresör basma hattının döngüsü suyu ısıtır · v18'in 30 W elektrikli kabı kalktı"))
    ekle("sicak_gaz_dongusu", TU_BORU([(_xl(p_[0]), _yl(p_[1]), p_[2]) for p_ in SICAK_GAZ], 3.175), "celik",
         bom=("Sıcak gaz döngüsü Cu Ø6,35", 1, "kompresör basma hattından tavaya U döngü · soğutmacı firma", "v31 · yoğuşma suyunu buharlaştırır (kondenser öncesi gazı da biraz soğutur)"))
'''
degis('    # ---------------- 8b · DÖNER TABLA — TAM ÜRETİM MODELİ (v10) ----------------', KASET + '\n    # ---------------- 8b · DÖNER TABLA — TAM ÜRETİM MODELİ (v10) ----------------')

# boru yardımcısı (TU.boru ile aynı: silindir + küre eklemler) — modul() TU'yu içe almaz
degis("def ekle(ad, wp, mal, bom=None):\n",
      "def TU_BORU(pts, r):\n"
      "    \"\"\"v31 · boru hattı (silindir + küre eklemler) · topping_uno_cad.boru ile aynı\"\"\"\n"
      "    ss = []\n"
      "    for a, b in zip(pts[:-1], pts[1:]):\n"
      "        v = cq.Vector(*b) - cq.Vector(*a)\n"
      "        if v.Length > 1e-6: ss.append(cq.Solid.makeCylinder(r, v.Length, cq.Vector(*a), v.normalized()))\n"
      "    for p in pts[1:-1]: ss.append(cq.Solid.makeSphere(r, cq.Vector(*p), angleDegrees1=-90, angleDegrees2=90))\n"
      "    return cq.Workplane(obj=cq.Compound.makeCompound(ss))\n\n\n"
      "def ekle(ad, wp, mal, bom=None):\n")

# ---------------------------------------------------------------- 4 · dünya denetimi: pay + kaset + bağlantılar
degis("    _pay = {t_: KLF66[t_] / GEREKEN_DIK[t_] - 1.0 for t_ in KLF66}\n",
      "    _ek = {t_: ek_kaset(t_) for t_ in KLF66}                                           # v31 · kasetin ek ısısı (W)\n"
      "    _pay = {t_: KLF66[t_] / (GEREKEN_DIK[t_] + _ek[t_]) - 1.0 for t_ in KLF66}\n")
degis('    k("v30 · KLF6.6CND (dikdörtgen kutu, dolum + ılık gün) pay: %s · kondenser yüzünün %%%.0f\'i taban üstünde açık (alt %.0f mm cepte) → %%5 kayıp sayılsa 40 °C\'de %+.0f%% (≥ 0)"\n'
      '      % (" · ".join("%d °C %+.0f%%" % (t_, 100.0 * p_) for t_, p_ in sorted(_pay.items())), 100.0 * _yuz, DY_D + SAC - CU_Y[0], 100.0 * (0.95 * KLF66[40] / GEREKEN_DIK[40] - 1.0)),\n'
      '      min(_pay.values()) >= 0.05 and 0.95 * KLF66[40] >= GEREKEN_DIK[40] and _yuz >= 0.65)\n',
      '    k("v31 · KLF6.6CND (dikdörtgen kutu, dolum + ılık gün + KASET EK ISISI %s W) pay: %s · kondenser yüzünün %%%.0f\'i taban üstünde açık (alt %.0f mm cepte) → %%5 kayıp sayılsa 40 °C\'de %+.1f%% (≥ 0)"\n'
      '      % (" / ".join("%.1f" % _ek[t_] for t_ in sorted(_ek)), " · ".join("%d °C %+.1f%%" % (t_, 100.0 * p_) for t_, p_ in sorted(_pay.items())), 100.0 * _yuz, DY_D + SAC - CU_Y[0],\n'
      '         100.0 * (0.95 * KLF66[40] / (GEREKEN_DIK[40] + _ek[40]) - 1.0)),\n'
      '      min(_pay.values()) >= 0.05 and 0.95 * KLF66[40] >= GEREKEN_DIK[40] + _ek[40] and _yuz >= 0.65)\n'
      + r'''    # v31 · EVAPORATÖR KASETİ: yer · kanallar · hava · bobin · yoğuşma suyu
    _ks = B_["TC:evap_kaseti_dis_sac"]; _pnk = B_["TC:kuru_pano_kutusu"]; _dn = B_["TC:kuru_din_plakasi"]; _hh = B_["TU:hava_hatti_sartlandirici_ada"]; _sk = B_["TC:kuru_bolme_servis_kapagi"]
    _ort = max(0.0, min(_ks.xmax, _cu.xmax) - max(_ks.xmin, _cu.xmin)) / (_cu.xmax - _cu.xmin)
    k("v31 · KASET YERİ: kuru bölmede x %.0f–%.0f (pano %.0f ↔ DIN plakası %.0f arası: %.0f / %.0f mm) · y %.0f–%.0f (hava hattı üstü %.0f ↔ servis kapağı %.1f: %.1f / %.1f mm) · z %.0f…%.0f · soğutma grubunun %%%.0f'inin TAM ÜSTÜNDE"
      % (_ks.xmin, _ks.xmax, _pnk.xmax, _dn.xmin, _ks.xmin - _pnk.xmax, _dn.xmin - _ks.xmax, _ks.ymin, _ks.ymax, _hh.ymax, _sk.ymin, _ks.ymin - _hh.ymax - 3.0, _sk.ymin - _ks.ymax, _ks.zmin, _ks.zmax, 100.0 * _ort),
      _ks.xmin - _pnk.xmax >= 15.0 and _dn.xmin - _ks.xmax >= 5.0 and _ks.ymin - 3.0 - _hh.ymax >= 2.9 and _sk.ymin - _ks.ymax >= 5.0 and _ort >= 0.9)
    _gk = {k_: (a_[0] + TU.KANAL_ET + DX_D, a_[1] - TU.KANAL_ET + DX_D, a_[2] + TU.KANAL_ET - 168.0, a_[3] - TU.KANAL_ET - 168.0) for k_, a_ in TU.AGIZ.items()}
    _bt = KSET_BOBIN
    k("v31 · KANALLAR ↔ KASET: alt kanal geçidi (x %.0f–%.0f · y %.0f–%.0f) bobinin önünde (bobin x %.0f–%.0f · y %.0f–%.0f) · üst kanal geçidi (y %.0f–%.0f) ara sacın (%.1f) üstünde, fan plakasının önünde · ikisi de kaset boşluğunda (x %.0f–%.0f · y %.0f–%.0f) · kesik %s"
      % (_gk["alt"][0], _gk["alt"][1], _gk["alt"][2], _gk["alt"][3], _bt[0], _bt[1], _bt[2], _bt[3], _gk["ust"][2], _gk["ust"][3], KSET_ARA_Y[1], KSET_BOS[0], KSET_BOS[1], KSET_BOS[2], KSET_BOS[3],
         "x %.0f–%.0f · y %.0f–%.0f" % (TU.KASET_KESIK[0] + DX_D, TU.KASET_KESIK[1] + DX_D, TU.KASET_KESIK[2] - 168.0, TU.KASET_KESIK[3] - 168.0)),
      _gk["alt"][0] >= _bt[0] and _gk["alt"][1] <= _bt[1] and _gk["alt"][2] >= _bt[2] and _gk["alt"][3] <= _bt[3] and _gk["ust"][2] >= KSET_ARA_Y[1] and _gk["ust"][3] <= KSET_BOS[3]
      and _gk["ust"][0] >= KSET_BOS[0] and _gk["ust"][1] <= KSET_BOS[1] and KSET_BOS[0] >= TU.KASET_KESIK[0] + DX_D + 19.9 and KSET_BOS[1] <= TU.KASET_KESIK[1] + DX_D - 19.9
      and abs(KSET["x"][0] - (TU.KASET_KESIK[0] + DX_D) + 22.0) < 0.01 and abs(KSET["x"][1] - (TU.KASET_KESIK[1] + DX_D) - 22.0) < 0.01)
    _Q = FAN["q_isletme"] * 2.0 / 3600.0                                                # m³/s · 2 fan işletme noktası
    _Aust, _Aalt = TU.IZGARA_ACIK["ust"] * 1e-6, TU.IZGARA_ACIK["alt"] * 1e-6
    _Abob = (_bt[1] - _bt[0]) * (_bt[3] - _bt[2]) * 1e-6
    _Abaca = (_bt[1] - _bt[0]) * (_bt[4] - KSET_BOS[4]) * 1e-6
    _Qn = GEREKEN_DIK[40] + _ek[40]
    _dTh = _Qn / (1.2 * 1006.0 * _Q)                                                   # K · havanın bobinde soğuması
    _lmtd = (13.0 - (13.0 - _dTh)) / __import__("math").log(13.0 / (13.0 - _dTh))    # oda +3 → bobin çıkışı +3 − ΔT · buharlaşma −10
    _UA = _Qn / _lmtd
    _Aex = BOBIN_ALAN_YOG * _Abob * (_bt[5] - _bt[4]) / 1000.0
    k("v31 · KASET HAVASI: 2 × %s işletme %.0f m³/h @ %.0f Pa (toplam %.0f m³/h = %.3f m³/s) · üst ızgara %.1f m/s · alt ızgara %.1f m/s (≤ 4) · bobin yüzü %.2f m/s (0,8–2,5) · arka baca %.1f m/s (≤ 4,5) · "
      "40 °C'de %.0f W → hava %.1f K soğur · LMTD %.1f K · gereken UA %.0f W/K · bobin dış yüzeyi ≈ %.2f m² → gereken U %.1f W/m²K (tipik %.0f–%.0f [V])"
      % (FAN["ad"], FAN["q_isletme"], FAN["p_isletme"], 2 * FAN["q_isletme"], _Q, _Q / _Aust, _Q / _Aalt, _Q / _Abob, _Q / _Abaca, _Qn, _dTh, _lmtd, _UA, _Aex, _UA / _Aex, U_BOBIN[0], U_BOBIN[1]),
      _Q > 0.0 and _Q / _Aust <= 4.0 and _Q / _Aalt <= 4.0 and 0.8 <= _Q / _Abob <= 2.5 and _Q / _Abaca <= 4.5 and _dTh < 9.0 and _UA / _Aex <= U_BOBIN[0])
    _th = KSET_TAHLIYE; _sf = min(range(len(_th)), key=lambda i_: _th[i_][1] if i_ < 4 else 1e9)
    _dus = all(_th[i_ + 1][1] <= _th[i_][1] + 1e-6 for i_ in range(3, len(_th) - 1))
    _yv = (YT[1] - YT[0] - 2) * (YT[5] - YT[4] - 2) * (YT[3] - YT[2] - 1) * 1e-6
    _uc = B_["TC:evap_kaseti_tahliye_hortumu"]; _ytb = B_["TC:yogusma_tavasi_sicak_gazli"]
    k("v31 · YOĞUŞMA SUYU: tava → Ø8 hortum · sifon %.0f → %.0f (%.0f mm su ≥ 10: fan emişi kasete sıcak hava çekemez) · sifondan sonra hep iner: %s · uç y %.0f tavanın (üstü %.1f) üstünde hava boşluklu · tava %.2f L · günde ≈ %.0f g (sogutma_topping_v1) · ünitenin atış havasında sıcak gaz döngülü (elektrikli kap yok)"
      % (_th[1][1], _th[3][1], _th[3][1] - _th[1][1], "evet" if _dus else "HAYIR", _uc.ymin, _ytb.ymax, _yv, YOGUSMA_GUN),
      _th[3][1] - _th[1][1] >= 10.0 and _dus and _uc.ymin > _ytb.ymax and _ytb.xmin >= CU_CEP[1] and _ytb.xmax <= TABAN_ATIS[0][0] and _yv >= 0.3)
''')
degis('      _pn.ymin - _cu.ymax >= 400.0 and _kz.ymax <= _ua.ymin + 0.01 and B_["TC:kuru_bolme_servis_kapagi"].ymin - max(B_[a].ymax for a in ("TC:kuru_pano_kutusu", "TC:kuru_ups", "TC:kuru_guc_kaynagi")) >= 5.0)',
      '      _pn.ymin - _cu.ymax >= 400.0 and _kz.ymax <= _ua.ymin + 0.01 and B_["TC:kuru_bolme_servis_kapagi"].ymin - max(B_[a].ymax for a in ("TC:kuru_pano_kutusu", "TC:kuru_ups", "TC:kuru_guc_kaynagi", "TC:evap_kaseti_dis_sac")) >= 5.0)')
degis('           ("TU:sogutma_emis_hatti", "TC:sogutma_grubu_KLF66"), ("TU:sogutma_sivi_hatti", "TC:sogutma_grubu_KLF66"),\n',
      '           ("TC:sogutma_emis_hatti", "TC:sogutma_grubu_KLF66"), ("TC:sogutma_sivi_hatti", "TC:sogutma_grubu_KLF66"),\n'
      '           ("TC:sogutma_emis_hatti", "TC:evap_kaseti_hat_gecis_blogu"), ("TC:sogutma_sivi_hatti", "TC:evap_kaseti_hat_gecis_blogu"), ("TC:sogutma_emis_hatti_ic", "TC:evap_kaseti_kollektor_TXV_zarfi"),\n'
      '           ("TC:sogutma_sivi_hatti_ic", "TC:evap_kaseti_kollektor_TXV_zarfi"), ("TC:sogutma_emis_hatti_ic", "TC:evap_kaseti_hat_gecis_blogu"),\n'
      '           ("TC:evap_kaseti_dis_sac", "TC:evap_kaseti_PU"), ("TC:evap_kaseti_ic_sac", "TC:evap_kaseti_PU"), ("TC:evap_kaseti_isi_kesici_cerceve", "TC:evap_kaseti_dis_sac"),\n'
      '           ("TC:evap_kaseti_isi_kesici_cerceve", "TU:soguk_arka_dis_sac"), ("TC:evap_kaseti_isi_kesici_cerceve", "TU:arka_duvar_kaset_yuzu"), ("TC:evap_kaseti_hat_gecis_blogu", "TC:evap_kaseti_PU"),\n'
      '           ("TC:evap_kaseti_askisi_0", "TC:evap_kaseti_dis_sac"), ("TC:evap_kaseti_askisi_1", "TC:evap_kaseti_dis_sac"), ("TC:evap_kaseti_askisi_0", "TU:soguk_arka_dis_sac"), ("TC:evap_kaseti_askisi_1", "TU:soguk_arka_dis_sac"),\n'
      '           ("TC:evap_kaseti_damlama_tavasi", "TC:evap_kaseti_ic_sac"), ("TC:evap_kaseti_lamel_paketi", "TC:evap_kaseti_damlama_tavasi"), ("TC:evap_kaseti_lamel_paketi", "TC:evap_kaseti_ara_saci"),\n'
      '           ("TC:evap_kaseti_alt_conta_lamasi", "TC:evap_kaseti_damlama_tavasi"), ("TC:evap_kaseti_ara_saci", "TC:evap_kaseti_ic_sac"), ("TC:evap_kaseti_kollektor_ayirma_saci", "TC:evap_kaseti_ic_sac"),\n'
      '           ("TC:evap_kaseti_kollektor_TXV_zarfi", "TC:evap_kaseti_kollektor_ayirma_saci"), ("TC:evap_kaseti_fan_plakasi", "TC:evap_kaseti_ara_saci"), ("TC:evap_kaseti_fan_plakasi", "TC:evap_kaseti_ic_sac"),\n'
      '           ("TC:evap_kaseti_fani_0", "TC:evap_kaseti_fan_plakasi"), ("TC:evap_kaseti_fani_1", "TC:evap_kaseti_fan_plakasi"), ("TC:evap_kaseti_tahliye_hortumu", "TC:evap_kaseti_damlama_tavasi"),\n'
      '           ("TC:yogusma_tavasi_sicak_gazli", "TC:dis_taban"), ("TC:sicak_gaz_dongusu", "TC:sogutma_grubu_KLF66"),\n')
degis('        V24 = importlib.import_module("topping_cad_v29"); V24.PARCALAR[:] = []; V24.modul()      # v30: referans v29',
      '        V24 = importlib.import_module("topping_cad_v30"); V24.PARCALAR[:] = []; V24.modul()      # v31: referans v30      # v30: referans v29')
degis('        k("v30 · kinematik v29 ile aynı', '        k("v31 · kinematik v30 ile aynı')
degis('print("TOPPING MODULU v30 · %d parca', 'print("TOPPING MODULU v31 · %d parca')

compile(s, "topping_cad_v31.py", "exec")
io.open(os.path.join(U, "topping_cad_v31.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v31.py yazıldı · %d satır" % s.count("\n"))
