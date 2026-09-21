# -*- coding: utf-8 -*-
"""KAPAK YOK + ROTOR KAYNAKLI + KOVANDA SAVURMA DİSKİ → dört kasetin yeni sürümü (eskilere dokunmaz):
   kasar_cad_v9→v10 · kiyma_cad_v4→v5 · kusbasi_cad_v3→v4 · sucuk_cad_v2→v3
Kemal (22 Eyl): "Kapak olmasın, TOPPING'de de yok."  +  1 numaralı kural gereği benim bulduğum iki eksik:
 1 KAPAK KALDIRILDI (kaset +3 °C kapalı kabinin içinde; Atosa'nın dozaj haznelerinde de kapak yok).
   Yerine gövdenin ağzı boyunca İÇE 8 mm bükme DUDAK: kenar keskin kalmaz, ağız açıklığı esnemez (kapak çıtasının işiydi),
   elle taşırken tutulacak yer olur. İÇE bükülüyor çünkü kaset dış ölçüsü (140 / 280) dolu — dışa 8 mm yer yok.
 2 SIYIRICI LAMA artık POZİTİF TUTULUYOR: lama koldan 4 mm taşıyor ve çentiğin ucu AÇIKTI → lamayı dışa doğru tutan hiçbir şey yoktu.
   Çözüm: rotor KAYNAKLI TEK PARÇA. Her lama-kol birleşimine 3 mm KAYNAK YAKASI modellendi (6 yaka/kaset). Yaka lamanın kendi
   dış yarıçapıyla SINIRLI — duvar boşluğu (kıymada 2,4 mm) bozulmuyor; üreteç bunu ölçerek doğruluyor.
   Vida/pim ile tutturmadım: çiğ ette aralık = bakteri yuvası. Kaynaklı rotor tek parça çıkar, tek parça yıkanır.
   Baskı deneme parçasında yakalar zaten basılıyor (tek parça çıkar).
 3 ÖN KOVANDA SAVURMA DİSKİ Ø26 × 2: ürün kare milin çevresinden kovana sürünebiliyordu. Disk mile geçer, kovanın 6 mm önünde
   durur, mil dönerken geleni merkezkaçla geri atar. NOT: SIZDIRMAZLIK DEĞİL, sürünmeyi kesen savurucu. Denemede sızarsa
   çözüm: milin kovandan geçen bölümünü Ø8 yuvarlağa tornalayıp 8 × 2 O-ring koymak.
"""
import io, os, re
U = os.path.dirname(os.path.abspath(__file__))
ISLER = [("kasar_cad_v9", "kasar_cad_v10", [("kasar_kabi_v9", "kasar_kabi_v10"), ("KASAR_KABI_v9", "KASAR_KABI_v10"), ("kasar_v9", "kasar_v10")], False),
         ("kiyma_cad_v4", "kiyma_cad_v5", [("kiyma_kaseti_v4", "kiyma_kaseti_v5"), ("KIYMA_KASETI_v4", "KIYMA_KASETI_v5"), ("kiyma_v4", "kiyma_v5")], True),
         ("kusbasi_cad_v3", "kusbasi_cad_v4", [("kusbasi_kaseti_v3", "kusbasi_kaseti_v4"), ("KUSBASI_KASETI_v3", "KUSBASI_KASETI_v4"), ("kusbasi_v3", "kusbasi_v4")], True),
         ("sucuk_cad_v2", "sucuk_cad_v3", [("sucuk_kaseti_v2", "sucuk_kaseti_v3"), ("SUCUK_KASETI_v2", "SUCUK_KASETI_v3"), ("sucuk_v2", "sucuk_v3")], True)]

DUDAK = '''    # ---- 8 AĞIZ DUDAĞI (KAPAK YOK — Kemal, 22 Eyl) ----
    # Gövdenin üst ağzı boyunca İÇE 8 mm bükme dudak (gövdeyle AYNI parça). Dışa bükülemez: kaset dış ölçüsü dolu.
    AD_ = {p["ad"]: p for p in PARCALAR}
    for s_ in (1, -1):
        dudak = kut(min(s_ * (RB - 8.0), s_ * RB), max(s_ * (RB - 8.0), s_ * RB), Y_UST - 1.5, Y_UST, ZBI, ZFI)
        v0_ = AD_["govde"]["wp"].val().Volume(); AD_["govde"]["wp"] = AD_["govde"]["wp"].union(dudak)
        assert AD_["govde"]["wp"].val().isValid() and AD_["govde"]["wp"].val().Volume() > v0_ + 3000.0, "agiz dudagi birlesmedi"
    AD_["govde"]["bom"] = ("Gövde · kadeh kesit + ağız dudağı", 1, AD_["govde"]["bom"][2], "iki plakanın 4 mm kanalına oturur · üst ağız boyunca İÇE 8 mm bükme dudak (KAPAK YOK: kenar keskin kalmaz, ağız esnemez)")
'''

KAYNAK = '''            # KAYNAK YAKASI: lama ile kolun birleşimi, kolun iki yanında 3 mm. Lamanın kendi dış yarıçapıyla sınırlı → duvar boşluğu bozulmaz.
            ac_ = math.radians(LAMA_ACI); R_DIS_ = R_LAMA + LAMA_G / 2.0 * math.cos(ac_) + LAMA_K / 2.0 * math.sin(ac_)   # lamanın EN DIŞ köşesi: yaka bundan dışarı çıkmaz
            for za_, zb_ in ((z0 - 3.0, z0), (z1, z1 + 3.0)):
                yaka = lama(LAMA_G + 6.0, LAMA_K + 6.0, za_, zb_).cut(lama(LAMA_G + 0.3, LAMA_K + 0.3, za_ - 1, zb_ + 1)).intersect(
                    cq.Workplane("XY").circle(R_DIS_).extrude(zb_ - za_ + 2).translate((0, 0, za_ - 1)))
                kol = kol.union(yaka)
'''


for eski, yeni, adlar, rotorlu in ISLER:
    s = io.open(os.path.join(U, eski + ".py"), encoding="utf-8").read(); n = 0
    for a, b in adlar: assert a in s, (eski, a); s = s.replace(a, b)
    def tek(desen, yerine, ad, bayrak=0):
        global s, n
        s2, k = re.subn(desen, lambda m_: m_.expand(yerine), s, count=1, flags=bayrak)      # m_.expand: geri basvuru calissin
        assert k == 1, "%s: BULUNAMADI: %s" % (eski, ad)
        s = s2; n += 1

    i = s.index('"""')
    s = s[:i + 3] + ("KAPAK YOK (Kemal, 22 Eyl: \"kapak olmasın, TOPPING'de de yok\") → gövde ağzında İÇE 8 mm bükme dudak · ROTOR KAYNAKLI (lama-kol kaynak yakaları) · "
                     "ön kovanda SAVURMA DİSKİ. Üreteç: yap_kapaksiz_v1.py · önceki sürüm: %s.py\n" % eski) + s[i + 3:]

    # ---- 1 · KAPAK → AĞIZ DUDAĞI ----
    tek(r"    # ---- 8 KAPAK ----\n.*?(?=    BR\.uygula)", DUDAK, "kapak blogu", re.S)
    tek(r', \("kapak", "govde", "kapak çıtası ↔ gövde \(0,5\)"\)', "", "kapak boslugu satiri")

    # ---- 2 · ROTOR KAYNAKLI ----
    if rotorlu:
        tek(r"(            kol = kut\(6\.0, R_KOL, -7\.0, 7\.0, zo - 7, zo \+ 7\)\.cut\(lama\(LAMA_G \+ 0\.3, LAMA_K \+ 0\.3, z0 - 1, z1 \+ 1\)\)[^\n]*\n)", "\\1" + KAYNAK, "kaynak yakasi")
        tek(r"(kol: lamaları r \d+'t?d?a?e? 20° eğik(?: KAPALI CEPTE)? tutar)", "\\1 · her birleşimde 3 mm KAYNAK YAKASI", "orumcek bom")
        tek(r'"çentiklere sıkı geçer · duvar[^"]*"', '"kola KAYNAKLI (rotor tek parça: vida/pim yok, aralık yok, bakteri tutmaz) · duvarı sıyırıp eti boğaza iter"', "lama bom")
        tek(r'\("Rotor göbeği · 2 kollu", 3, "DENEME: PETG / PA12 baskı · ÜRETİM: POM-C ya da kaynaklı 304"',
            '("Rotor göbeği · 2 kollu", 3, "DENEME: PETG / PA12 baskı (yakalarla tek parça çıkar) · ÜRETİM: 304, lamalarla KAYNAKLI"', "orumcek malzeme")

    # ---- 3 · LABİRENT: ön örümcek göbeği ↔ kovan havşası (ayrı parça YOK) ----
    # Ürün kare milin çevresinden kovana sürünebiliyordu. Önce ayrı savurma diski denendi: çakışma taraması ön örümceğin içine
    # girdiğini gösterdi, oraya 2 mm'lik parça sığmıyor (örümcek 150,5'te bitiyor, kovan 151,5'te başlıyor).
    # Çözüm parça istemiyor: kovanın arka yüzüne Ø28,4 × 2 HAVŞA açıldı, ön örümceğin Ø28 göbeği 1,7 mm içine giriyor.
    # Radyal aralık 0,2 mm × 1,7 mm boy = LABİRENT; dönen göbek geleni geri savurur, ürün mile ulaşamaz. Sökünce ikisi de yıkanır.
    tek(r"(    kovan = silz\(0, YC, 16\.0, ZFI - 3\.0, ZFI\)[^\n]*\n)",
        "\\1    kovan = kovan.cut(silz(0, YC, 14.2, ZFI - 3.0, ZFI - 1.0))                    # LABİRENT havşası Ø28,4 × 2 (ön örümcek göbeği girer)\n",
        "kovan havsasi")
    tek(r'(\("Ön kovan", 1, "POM / baskı", ")', "\\1arka yüzünde Ø28,4 × 2 LABİRENT havşası (ön örümcek göbeği girer → ürün mile sürünemez) · ", "kovan bom")
    # Göbek uzantısı YALNIZ göbeğe eklenir (kolları uzatmak kaynak yakasını ön plakanın içine sokuyordu — çakışma taraması yakaladı).
    tek(r'(        ekle\("orumcek_" \+ ad, )orumcek\(z0, z1\)(, "pom", Kg,)',
        "\\1(orumcek(z0, z1).union(silz(0, YC, 14.0, z1, 153.2).cut(karez(0, YC, KARE + 0.3, z1 - 1, 154.0))) if ad == \"on\" else orumcek(z0, z1))\\2",
        "on gobek uzantisi")
    io.open(os.path.join(U, yeni + ".py"), "w", encoding="utf-8").write(s); print("%s.py yazildi · %d yama" % (yeni, n))
