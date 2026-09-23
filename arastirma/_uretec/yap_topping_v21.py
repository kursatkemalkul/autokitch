# -*- coding: utf-8 -*-
"""topping_cad_v20 -> v21 : ACICI ve FIRIN BANDI TAM URETIM MODELI

Kemal: "soldaki bolumu tamamen detayli modellesene, o donen parcanin seklini fln,
birde tum detaylariyla" + "sag taraftaki firin bandini da gercek firin banti gibi
yap, donsun, pidenin nasil dusecegini goster" + "uretime gidicek sekilde".

────────────────────────────────────────────────────────────────────────────────
KONI NEDEN KONI — tasarimin kalbi
  Kemal'in gonderdigi Cin makinesinin fotografinda iki koninin UCLARI ORTADA
  BULUSUYOR. Sebebi geometrik: donen tablada cizgisel hiz v = w*r, merkezden
  uzaklastikca artar. KONI'nin yaricapi da tepesinden uzaklastikca DOGRUSAL artar.
  Koninin TEPESI tablanin EKSENINE konursa koninin her noktasindaki cevresel hizi
  tablanin o yaricaptaki hizina BIREBIR esit olur; koni hicbir yerde KAYMADAN
  yuvarlanir. Silindir olsa yalniz tek yaricapta uyar, kalan her yerde hamuru surter.
  Sonuc: tabla acma sirasinda DONER. v20'deki kilit artik gerekmiyor; burclari
  servis/ayar icin birakiyorum.

  tepe        tabla ekseninde, calisma diskinin 8 mm ustunde (y 116) = pide kalinligi
  boy         140 mm = pidenin yaricapi (Ø280)
  yarim aci   arctan(45/140) = 17,82 derece · taban yaricapi 45
  alt cizgi   YATAY y 116 — temas cizgisi hamurun ust yuzu
  iki koni    180 derece, uclari eksende bulusuyor; ters yonde donerler, teget
              kuvvetler birbirini goturur, hamur kendi etrafinda donmez

Z YERLESIMI (tabla ekseni ZT = -170; her seyin kendi bandi var, ic ice girmiyor)
  ON  koni -170..-30 · yatak -12..12 · reduktor 20..80  · motor 85..165
  ARKA koni -170..-310 · yatak -352..-328 · reduktor -400..-340 · motor -465..-385
  aski  on 0 · arka -340   (yatak hizasinda, reduktorun disinda)
  kafa plakasi y 250..262, z -500..200
  Z kizaklari z -560 ve -520 · pnomatik z -585 · kolon z -620..-590

────────────────────────────────────────────────────────────────────────────────
FIRIN BANDI — KOPRU KALKTI, USTELIK CAKISIYORDU
  Kopru plakasinin alti y 105,3'te idi; calisma diskinin kenari 106-108'de. Disk
  banda dogru ilerlerken kopruye CARPIYORDU (statik taramada gorunmedi, cunku
  modelde tabla park konumunda duruyor).
  Yerine sanayi standardi BICAK BURUNLU AKTARMA: bant Ø20'lik ince burun
  silindirine doluyor, ust yuzu y 106 (diskin 2 mm alti). Diskin kenari burna
  8 mm kala duruyor; pide o bosluğu kendi govdesiyle kopruler, 2 mm asagi banda
  iner, bant cekip firina goturur. Ø280'lik pide icin 8 mm hicbir sey.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v20.py"), encoding="utf-8").read()
D = []

# ============================================================ 1 · FIRIN BANDI
D.append((
    """    AKT_Y = 108.3                                               # diskin 0,3 mm ustu
    AKT_X0, AKT_X1 = 1700.0, 1800.0                             # koprü: tabla ucu … modül yüzü""",
    """    AKT_Y = 106.0                                               # BANDIN UST YUZU (diskin 2 mm alti)
    AKT_X0, AKT_X1 = 1815.0, 2195.0                             # burun silindiri … tahrik silindiri
    # burun x 1815: modulun cikis yarigi cercevesi 1792-1798,5'te bitiyor, bant onun
    # DISINDA duruyor. Tabla aktarma konumunda (x 1637) diskin kenari 1807'de —
    # burna 8 mm kala duruyor, pide o bosluğu kendi govdesiyle kopruluyor."""))

D.append((
    """    # UST yuzu AKT_Y (108,3) — pide bunun USTUNE cikacak, plaka asagi dogru kalin.
    _kpr = kut(AKT_X0, AKT_X1, AKT_Y - 3.0, AKT_Y, AKT_Z0, AKT_Z1)
    # giris agzi: 10 mm'de 1,5 mm'lik pah — pide 0,3 mm'lik basamaga carpmaz, tirmanir
    _pah = (cq.Workplane("XY").box(12.0, AKT_Z1 - AKT_Z0 + 4.0, 3.0, centered=False)
            .translate((AKT_X0 - 1.0, AKT_Z0 - 2.0, AKT_Y - 1.5))
            .rotate(cq.Vector(AKT_X0 + 10.0, 0.0, AKT_Y), cq.Vector(AKT_X0 + 10.0, 1.0, AKT_Y), 8.5))
    _kpr = _kpr.cut(_pah)
    ekle("aktarma_koprusu", _kpr, "celik",
         bom=("Aktarma köprüsü 100 × 360 × 3", 1, "304 · üst yüzü taşlanmış, ağzı 15° pah",
              "pide tabladan buna çıkar, fırın bandı buradan çeker. Üst yüzü çalışma diskinin "
              "0,3 mm üstünde. FIRIN BANDI ŞARTI: bıçak burunlu, yüzeyi y 108,3 ± 1, burnu "
              "modül yüzünden en çok 5 mm içeride [bant seçilince doğrulanacak]"))
    # KOPRU DUVARA CIVATALI: aski gerekmiyor. Kopru x 1700-1800 arasinda ve sag yan
    # sac 1798,5'te — koprunun 360 mm'lik arka kenari bastan basa duvara baglanir.
    # Askilar denenmisti ama arkadaki aski X TAHRIK MOTORUNUN z bandina (-400..-320)
    # giriyordu; motor da sag uctan tasinamiyor cunku tablanin PARK YERI sol uc.
    ekle("kopru_lamasi", kut(1780.0, 1798.5, AKT_Y - 3.0, AKT_Y + 45.0, AKT_Z0, AKT_Z1), "sac",
         bom=("Köprü bağlama laması 360 × 48 × 5", 1, "304 · sağ yan saca 8 × M6",
              "köprüyü duvara bağlar; askı yok — altta destek koyacak yer yok, araba oradan geçiyor"))""",
    """    # ---- FIRIN BANDI · BICAK BURUNLU AKTARMA (v21) ----
    BR_R, BT_R, BANT_K = 10.0, 30.0, 1.5
    BR_Y = AKT_Y - BANT_K - BR_R
    BT_Y = AKT_Y - BANT_K - BT_R
    BZ0, BZ1 = AKT_Z0, AKT_Z1
    ekle("bant_burun_silindiri", silz(AKT_X0, BR_Y, BR_R, BZ0 - 8.0, BZ1 + 8.0), "celik",
         bom=("Bant burun silindiri Ø20 × 376", 1, "304 · iki uçta flanşlı rulman",
              "BIÇAK BURUN: çapı küçük tutuldu ki bant yüzeyi tablanın kenarına 8 mm kala "
              "başlasın — pide o boşluğu kendi gövdesiyle köprüler ve 2 mm aşağı banda iner"))
    ekle("bant_tahrik_silindiri", silz(AKT_X1, BT_Y, BT_R, BZ0 - 8.0, BZ1 + 8.0), "celik",
         bom=("Bant tahrik silindiri Ø60 × 376", 1, "304 · kauçuk kaplı",
              "bandı çeker; devri fırındaki pişirme süresini belirler"))
    _dis = (silz(AKT_X0, BR_Y, BR_R + BANT_K, BZ0, BZ1)
            .union(silz(AKT_X1, BT_Y, BT_R + BANT_K, BZ0, BZ1))
            .union(kut(AKT_X0, AKT_X1, AKT_Y - BANT_K, AKT_Y, BZ0, BZ1))
            .union(cq.Workplane("XY").polyline([(AKT_X0, BR_Y - BR_R - BANT_K),
                                                (AKT_X1, BT_Y - BT_R - BANT_K),
                                                (AKT_X1, BT_Y - BT_R),
                                                (AKT_X0, BR_Y - BR_R)]).close()
              .extrude(BZ1 - BZ0).translate((0.0, BZ0, 0.0))))
    _ic = (silz(AKT_X0, BR_Y, BR_R, BZ0 - 1.0, BZ1 + 1.0)
           .union(silz(AKT_X1, BT_Y, BT_R, BZ0 - 1.0, BZ1 + 1.0))
           .union(kut(AKT_X0, AKT_X1, BR_Y - BR_R, AKT_Y - BANT_K, BZ0 - 1.0, BZ1 + 1.0)))
    ekle("bant", _dis.cut(_ic), "koyu",
         bom=("Fırın bandı · 290 geniş · kapalı çevrim", 1,
              "gıda onaylı PTFE kaplı cam elyaf örgü · 1,5 mm",
              "fırın içinden geçer; PTFE örgü 300 °C'ye dayanır ve hamur yapışmaz. "
              "Üst koşu y 106 — çalışma diskinin 2 mm altında"))
    ekle("bant_tasiyici_saci", kut(AKT_X0 + 20.0, AKT_X1 - 40.0, AKT_Y - BANT_K - 4.0,
                                   AKT_Y - BANT_K - 1.0, BZ0 + 5.0, BZ1 - 5.0), "sac",
         bom=("Bant taşıyıcı sacı", 1, "304 3 mm · üstü taşlanmış",
              "üst koşunun altında; pide ve malzeme yükü altında bant sarkmasın"))
    for i_, zb in enumerate((BZ0 - 30.0, BZ1 + 10.0)):
        # yan sac MODULUN DISINDA baslar (1800): x_motor_kaidesi 1690-1780'de duruyor
        ekle("bant_yan_saci_%d" % i_, kut(1802.0, AKT_X1 + 45.0, 20.0, AKT_Y + 18.0, zb, zb + 20.0), "sac",
             bom=("Bant yan sacı", 2, "304 5 mm · lazer",
                  "iki silindirin yataklarını taşır; burun ucu modül yüzüne cıvatalı") if i_ == 0 else None)
    _bm = nema23()["govde"].rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90.0)
    ekle("bant_motoru", cq.Workplane(obj=_bm.translate(cq.Vector(AKT_X1, BT_Y, BZ1 + 75.0))), "motor",
         bom=("Bant motoru · NEMA23 + planet i = 20", 1, "STP-MTR-23079 (GERÇEK CAD)",
              "bant hızı = fırın pişirme süresi; reçeteye göre değişir"))
    ekle("bant_ayagi", kut(AKT_X1 - 70.0, AKT_X1 + 10.0, 0.0, BT_Y - BT_R - BANT_K - 2.0, BZ0 + 30.0, BZ1 - 30.0), "sac",
         bom=("Bant ayağı", 1, "304 kutu profil · ayarlı taban",
              "bandın fırın tarafındaki ucunu taşır; TOPPING'e bağlı değil, bağımsız durur"))"""))

# ============================================================ 2 · ACICI
D.append((
    """    # ---------------- 8c · BANDA AKTARMA (v20) ----------------""",
    """    # ---------------- 8d · ACICI — KONILI DONER ACICI (v21) ----------------
    import math as _m
    AC_X, AC_Z = XC_TABLA, ZT
    AC_TEPE = 108.0 + 8.0                       # tepe: disk ustu + pide kalinligi
    AC_L, AC_RB = 140.0, 45.0                   # boy = pide yaricapi · taban yaricapi
    AC_ACI = _m.degrees(_m.atan2(AC_RB, AC_L))  # 17,82 derece

    def _koni(yon):
        \"\"\"tepesi tabla ekseninde, alt cizgisi YATAY koni. yon=+1 one, -1 arkaya\"\"\"
        p0 = cq.Vector(AC_X, AC_TEPE, AC_Z)
        p1 = cq.Vector(AC_X, AC_TEPE + AC_RB, AC_Z + yon * AC_L)
        v = p1 - p0
        k = (cq.Workplane("XY").circle(0.4).workplane(offset=v.Length)
             .circle(AC_RB).loft(ruled=True).val())
        eks = cq.Vector(0, 0, 1).cross(v)
        aci = _m.degrees(_m.acos(max(-1.0, min(1.0, cq.Vector(0, 0, 1).dot(v) / v.Length))))
        if eks.Length > 1e-9:
            k = k.rotate(cq.Vector(0, 0, 0), eks, aci)
        return cq.Workplane(obj=k.translate(p0)), p1

    # z bantlari: her parcanin kendi yeri var, ic ice girmiyorlar
    # her parca KENDI bandinda; komsusuyla en az 6 mm bosluk (kavrama payi)
    YER = {1.0: dict(yatak=(-12.0, 12.0), red=(20.0, 80.0), mot=125.0, aski=0.0, mil=(-42.0, 20.0)),
           -1.0: dict(yatak=(-352.0, -328.0), red=(-420.0, -360.0), mot=-455.0, aski=-340.0, mil=(-298.0, -360.0))}
    for i_, yon in enumerate((1.0, -1.0)):
        ad_ = "on" if yon > 0 else "arka"
        Y_ = YER[yon]
        _k, _p1 = _koni(yon)
        ekle("acici_konisi_" + ad_, _k, "celik",
             bom=("Açıcı konisi · boy 140 · taban Ø90", 2,
                  "304 taşlanmış, mat kumlu · yarım açı 17,82°",
                  "TEPESİ TABLA EKSENİNDE: koninin yarıçapı boyla doğrusal arttığı için dönen "
                  "tablanın her yarıçaptaki hızıyla birebir eşleşir; hamuru hiç sürtmeden "
                  "yuvarlayarak açar. Alt çizgisi y 116'da yatay = pide kalınlığı 8 mm") if i_ == 0 else None)
        _my = _p1.y
        ekle("acici_mili_" + ad_, silz(AC_X, _my, 9.0, Y_["mil"][0], Y_["mil"][1]), "celik",
             bom=("Açıcı mili Ø18", 2, "304 taşlanmış", "koniyi yatağa ve redüktöre bağlar") if i_ == 0 else None)
        ekle("acici_yatagi_" + ad_, silz(AC_X, _my, 24.0, Y_["yatak"][0], Y_["yatak"][1])
             .cut(silz(AC_X, _my, 9.1, Y_["yatak"][0] - 1.0, Y_["yatak"][1] + 1.0)), "celik",
             bom=("Açıcı yatağı · flanşlı Ø18", 2, "paslanmaz gövdeli rulman · gıda gresi",
                  "koninin DIŞ ucunu tutar; iç uç (tepe) serbesttir, yük taşımaz") if i_ == 0 else None)
        ekle("acici_reduktoru_" + ad_, kut(AC_X - 30.0, AC_X + 30.0, _my - 30.0, _my + 30.0,
                                           Y_["red"][0], Y_["red"][1]), "motor",
             bom=("Açıcı redüktörü · planet i = 5", 2, "SureGear sınıfı 60 × 60",
                  "mil devri = tabla devri / sin 17,82° — kayma olmaması şartı") if i_ == 0 else None)
        _mg = nema23()["govde"].rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 90.0 if yon > 0 else -90.0)
        ekle("acici_motoru_" + ad_, cq.Workplane(obj=_mg.translate(cq.Vector(AC_X, _my, Y_["mot"]))), "motor",
             bom=("Açıcı motoru · NEMA23 STP-MTR-23079", 2, "1,95 N·m · 2,8 A (GERÇEK CAD)",
                  "iki koni TERS YÖNDE döner — teğet kuvvetler birbirini götürür, hamur "
                  "kendi etrafında dönmez") if i_ == 0 else None)
        ekle("acici_askisi_" + ad_, kut(AC_X - 26.0, AC_X + 26.0, _my + 20.0, 250.0,
                                        Y_["aski"] - 12.0, Y_["aski"] + 12.0), "celik",
             bom=("Açıcı askısı", 2, "304 lama 52 × 12",
                  "yatağı kafa plakasına bağlar; redüktör ve motorun z bandının DIŞINDA") if i_ == 0 else None)

    ekle("acici_kafa_plakasi", kut(AC_X - 80.0, AC_X + 80.0, 250.0, 262.0, AC_Z - 330.0, AC_Z + 350.0), "sac",
         bom=("Açıcı kafa plakası 160 × 680 × 12", 1, "304 lama · frezelenmiş",
              "iki koni takımı buna asılı; iki dikey kızakta 60 mm iner-kalkar"))
    for i_, zb in enumerate((-575.0, -550.0)):
        ekle("acici_z_kizagi_%d" % i_, kut(AC_X - 10.0, AC_X + 10.0, 150.0, 340.0, zb, zb + 20.0), "celik",
             bom=("Açıcı Z kızağı · HGR15 · strok 60", 2, "HIWIN sınıfı",
                  "kafa iniş-kalkış ekseni; koni ancak hamurun üstüne indiğinde çalışır") if i_ == 0 else None)
    ekle("acici_pnomatigi", silz(AC_X, 320.0, 20.0, -520.0, -500.0)
         .union(kut(AC_X - 12.0, AC_X + 12.0, 262.0, 320.0, -521.0, -499.0)), "koyu",
         bom=("Açıcı pnömatiği Ø32 · strok 60", 1, "ISO 6432 paslanmaz · 6 bar",
              "kafayı indirir. 6 bar × Ø32 = 480 N; koninin istediği 40-160 N'un üstünde "
              "ama yük hamuru EZMİYOR — koni yuvarlanıyor, basmıyor"))
    ekle("acici_kolonu", kut(AC_X - 60.0, AC_X + 60.0, 0.0, 380.0, -660.0, -610.0)
         .union(kut(AC_X - 60.0, AC_X + 60.0, 350.0, 380.0, -660.0, -490.0)), "sac",
         bom=("Açıcı kolonu", 1, "304 kutu profil 120 × 40 · tabana cıvatalı",
              "kafayı taşır; rayın ARKASINDA durur, arabanın yolunu kesmez"))

    # ---------------- 8c · BANDA AKTARMA (v20) ----------------"""))

for e, y in D:
    assert e in s, "BULUNAMADI -> " + e[:70]
    s = s.replace(e, y, 1)

io.open(os.path.join(U, "topping_cad_v21.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v21.py yazildi ·", len(D), "donusum")
