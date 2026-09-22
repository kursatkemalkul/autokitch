# -*- coding: utf-8 -*-
"""topping_cad_v8 -> topping_cad_v9
Kemal (22 Eyl):
 1 "Yuvarlak parcalar neden yalitim parcasindan da assagiya gidip sacma sapan uzun kaliyor? Kirmizi yere kadar yap.
    Kasetlerin o yuvarlak parca uzunlugu sadece YALITIMIN UST KISMINA kadar gelsin, orda kes; yalitimin icine de
    AYNI CAPTA yuvarlak bosluk ac, kaset takilinca ucu oraya denk gelsin, malzeme assaga aksin. Bu sayede etrafi
    kapanir, yalitimda sadece BIR DELIK olur."
 2 "Yalitim parcasinin altinda bir gri parca var onu sil, ne gerek var ona."      -> damlama_teknesi
 3 "Konustuk, on yuzeyde sac parca kalmis havada ucuyor, onu da sil."             -> agiz_cercevesi

v9'DA:
 · Kaset borulari artik y 250'de (yalitimin ust yuzu) bitiyor — kaset ureteclerinde yapildi (yap_boru_v3.py:
   kasar v13 · kiyma v8 · kusbasi v7 · sucuk v6 · harc v3).
 · PU TABAN ve IC KABUK'ta uzun YARIK yerine her yuvada TEK YUVARLAK DELIK (boru disi + 2 mm).
 · Deligin icine DOZAJ KOVANI: paslanmaz boru, yalitimi bastan basa geciyor ve pidenin 40 mm ustunde bitiyor.
   Urun kasetin borusundan cikip kovana giriyor, kovan asagi indiriyor. Kaset cekilince boru kovanin USTUNDE
   kaliyor, hicbir seye takilmiyor.
 · Taban rayinda yarik KALIYOR (boru y 250-260 arasinda rayin icinden geciyor, cekme yolu acik olmali).
 · damlama_teknesi ve agiz_cercevesi silindi.
"""
import io, os, re

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
n = [0]


def yama(s, a, b):
    assert a in s, "BULUNAMADI: " + a[:110]
    n[0] += 1
    return s.replace(a, b, 1)


c = io.open(os.path.join(U, "topping_cad_v8.py"), encoding="utf-8").read()
c = c.replace("topping_cad_v8", "topping_cad_v9").replace("topping_modul_v8", "topping_modul_v9")
i = c.index('"""', c.index('"""') + 3)
c = c[:i] + ("v9 (22 Eyl 2026): kaset borulari yalitimin ust yuzunde bitiyor; yalitimda uzun yarik yerine TEK YUVARLAK\n"
             "DELIK + icinde DOZAJ KOVANI. damlama_teknesi ve agiz_cercevesi silindi.\n") + c[i:]
c = yama(c, '"TOPPING MODULU v8', '"TOPPING MODULU v9')

# ---------------------------------------------------------------- 1 · yeni kaset surumleri
c = yama(c, '''KASET_CAD = {"HARÇ 1": "harc_cad_v2", "HARÇ 2": "harc_cad_v2", "KIYMA": "kiyma_cad_v7",
             "KUŞBAŞI": "kusbasi_cad_v6", "KAŞAR KABI": "kasar_cad_v12", "KÜP SUCUK": "sucuk_cad_v5"}''',
         '''KASET_CAD = {"HARÇ 1": "harc_cad_v3", "HARÇ 2": "harc_cad_v3", "KIYMA": "kiyma_cad_v8",
             "KUŞBAŞI": "kusbasi_cad_v7", "KAŞAR KABI": "kasar_cad_v13", "KÜP SUCUK": "sucuk_cad_v6"}''')

# ---------------------------------------------------------------- 2 · YARIK -> yuvarlak DELIK (yalitim + ic kabuk)
c = yama(c, '''    # v5: yarık artık YUVA genişliğine göre değil, kasetin BORU dışına göre — soğuk kaçağı en aza insin.
    YARIK = []
    for ad, x0, x1, gen in YUVA:
        bd, be, _ = BORU[ad]
        r_ = bd / 2.0 + be + 3.0                                               # boru dışı + 3 mm pay
        YARIK.append(((x0 + x1) / 2.0 - r_, (x0 + x1) / 2.0 + r_))''',
         '''    # v9: YALITIM ve İÇ KABUKTA artık uzun yarık YOK — her yuvada TEK YUVARLAK DELİK (Kemal: "yalıtımda
    # sadece bir delik olur, etrafı kapanır"). Kaset borusu y 250'de, yani yalıtımın üst yüzünde bitiyor;
    # ürünü deliğin içindeki DOZAJ KOVANI aşağı indiriyor. Yarık yalnız TABAN RAYINDA kalıyor:
    # boru y 250–260 arasında rayın içinden geçiyor, kaset çekilirken o yol açık olmalı.
    DELIK = []                                                                 # (x merkez, z merkez, delik yarıçapı)
    for ad, x0, x1, gen in YUVA:
        bd, be, _ = BORU[ad]
        a0_, a1_, dd_ = AGIZ[ad]
        DELIK.append(((x0 + x1) / 2.0, ZK[0] + ((a0_ + a1_) / 2.0 - dd_ / 2.0), bd / 2.0 + be + 1.0))
    YARIK = [(x_ - r_ - 2.0, x_ + r_ + 2.0) for x_, z_, r_ in DELIK]           # yalnız taban rayı için''')

# pu_taban ve ic_kabuk artik YUVARLAK delik alir
c = yama(c, '''        if ad == "pu_taban":
            for a_, b_ in YARIK: w_ = w_.cut(kut(a_, b_, y0 - 1, y1 + 1, ZY[0], ZY[1]))      # meme yarıkları''',
         '''        if ad == "pu_taban":
            for x_, z_, r_ in DELIK: w_ = w_.cut(sily(x_, z_, r_, y0 - 1.0, y1 + 1.0))       # v9: yuvarlak dozaj deliği''')
c = yama(c, '    for a_, b_ in YARIK: ic = ic.cut(kut(a_, b_, hy0 - 1, hy0 + 2, ZY[0], ZY[1]))',
         '    for x_, z_, r_ in DELIK: ic = ic.cut(sily(x_, z_, r_, hy0 - 2.0, hy0 + 3.0))            # v9: yuvarlak dozaj deliği')

# ---------------------------------------------------------------- 3 · DOZAJ KOVANI
c = yama(c, '    for i, xx in enumerate([YUVA[0][1] - BOLME] + [y[2] for y in YUVA]):',
         '''    # v9 · DOZAJ KOVANI: yalıtım deliğini baştan başa geçen paslanmaz boru. Üstü kasetin borusunun
    # ucuna denk geliyor (arada 1 mm hava), altı pidenin DUSME kadar üstünde bitiyor. Yalıtımı kapatan parça bu.
    for (x_, z_, r_), (ad, x0, x1, gen) in zip(DELIK, YUVA):
        kv = sily(x_, z_, r_ - 0.2, AGZ[1] + H.DUSME, hy0)                 # üstü iç kabuğun ALT yüzünde biter
        kv = kv.cut(sily(x_, z_, r_ - 1.4, AGZ[1] + H.DUSME - 1.0, hy0 + 1.0))
        ekle("dozaj_kovani_%s" % ad.replace(" ", "_"), kv, "sac", bom=None)
    for a_, ad_, n_, malz_, gor_ in (("_bom_kovan", "Dozaj kovanı", 6, "304 boru 1,2 mm · iç kabuğa kaynaklı", "yalıtım deliğini baştan başa geçer; kasetin borusu üstüne oturur, ürünü pidenin %.0f mm üstüne indirir" % H.DUSME),):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "sac", bom=(ad_, n_, malz_, gor_))

    for i, xx in enumerate([YUVA[0][1] - BOLME] + [y[2] for y in YUVA]):''')

# ---------------------------------------------------------------- 4 · SILINEN IKI PARCA
c = re.sub(r'^    agz = .*?\n(    agz = .*?\n)*    ekle\("agiz_cercevesi".*?\n', '', c, flags=re.M)
c = re.sub(r'^    ekle\("agiz_cercevesi".*?\n(\s+bom=.*?\n)?', '', c, flags=re.M)
c = re.sub(r'^    ekle\("damlama_teknesi".*?\n(\s+bom=.*?\n)?', '', c, flags=re.M)
c = c.replace('    # ---------------- 9 · AĞIZ ve DAMLAMA ----------------',
              '    # ---------------- 9 · (v9: AĞIZ ÇERÇEVESİ ve DAMLAMA TEKNESİ SİLİNDİ) ----------------\n'
              '    # Kemal: "yalıtım parçasının altındaki gri parçayı sil, ne gerek var ona" (damlama teknesi) ·\n'
              '    # "ön yüzeyde sac parça kalmış havada uçuyor, onu da sil" (ağız çerçevesi — ön çerçeve sacı\n'
              '    # v7\'de kalkınca desteksiz kalmıştı). Damlamayı artık dozaj kovanı + duckbill valf kesiyor.', 1)

io.open(os.path.join(U, "topping_cad_v9.py"), "w", encoding="utf-8").write(c)
print("topping_cad_v9.py yazildi ·", n[0], "yama")
