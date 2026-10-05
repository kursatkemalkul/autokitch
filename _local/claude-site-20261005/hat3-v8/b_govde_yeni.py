# -*- coding: utf-8 -*-
"""B ÇEKMECE DOLABI GÖVDESİ — BAŞTAN, BASİT, ÜRETİME YÖNELİK (Kemal 2 Eki: "karışık kurmuşsun; basit bir düzende yap; her şey tam otursun;
altı üstü basit bir çekmece dolabı" · "yalıtım hiçbir yerde görünmesin, sac ile yalıtım arası boşluk olmasın" · "üretime yönelik").

DEĞİŞMEYEN ARAYÜZLER (GLB'den / h3_store_v1'den): dış zarf x 736–4400 · y 123–788 (üst DÜZ 788: A kaidesi, TOPPING kaidesi, fırın, K bunun üstünde) ·
z −830 (arka dış) … +39 (kabuk önü) · kapaklar +39…+79 · fitil arkası z 24 · ayaklar (B_KASA__celik, dokunulmaz) · çekmece açıklıkları (CEK listesi) ·
taşıyıcı (B_TASIYICI) · soğutma (B_SOGUTMA) · depo (B_DEPO) · elektrik · kablo kanalı (B_KABLO) · gider hattı.

KURGU (tek kural, her yerde aynı):
  1. SANDVİÇ KASA = DIŞ 304 1,5 + yerinde köpük PU (40 kg/m³) + İÇ 304 1,2 (sac_kararlar_v1: ic_panel_t 1,2). İç yüzler (soğuk hacim) sabit:
     sol 798,5 · taban 164,5 · arka −790 · tavan 728 (K1–K2) / 668 (K3–K6) · bölme yüzleri = kolon kenarları.
  2. ÖN ÇERÇEVE (430 ferritik 1,0, manyetik fitil) z 23–24 TEK PARÇA, dış sacların arasında köşeden köşeye (x 737,5–4398,5 · y 124,5–786,5);
     bütün PU'ların önü z 23'te biter → hiçbir PU ön yüzü açıkta değil. Dış sacların ön kenarı +39'a kadar uzar (kapak arkası) = 15 mm etek,
     etekle çerçeve arasında yalnız fitil bandı (hava, metal).
  3. KÖPÜKLEME KALIBI MANTIĞI: her PU bloğu dış sac + iç sac + ön çerçeve + komşu blok/bölme sacıyla KAPALI bir hacim; köpük yerinde
     (enjeksiyon) dolar → PU şekli = boşluğun kendisi (geçen profil / kılıf / kanal tam oturur, arada boşluk yok).
  4. BÖLMELER B1–B5 AYNI KESİT: sac 1,2 + PU 32,6 + sac 1,2 = 35 · z −790…+23 (arka iç sacın önü → çerçevenin arkası) · y 164,5 → tavan iç sacı
     (taban ve tavan iç sacları sürekli, bölmeler aralarına tam oturur; yarım bölme / basamak / ek parça yok). B5 (soğuk ↔ teknik sütun) aynı
     kesit + teknik tarafta tam boy kapama sacı (dış kabuğun parçası: 124,5–786,5 · −828,5…+23).
  5. GEÇİŞLER: hava geçişleri ve kablo kanalı geçişleri bölmelerde 1,2 sac KOVANLA kaplı (PU görünmez); gider hattı Ø24 kılıfta (B_SOGUTMA);
     taşıyıcı / modüler dikmeler ve elektrik kanalı PU'ya gömülü (köpük üstüne dolar).
  6. FIRIN ALTI ISI KALKANI (store_cad_v14 kurgusu korunur): x 2500–3994,7 · tavan PU 669,2–728 üstünde ayırma sacı → HAVA BOŞLUĞU 729,2–786,5
     (iki yanda kapama sacı, önü çerçeve, arkası arka dış sacın 7 yarığı) · içinde parlak paslanmaz ışınım sacı 0,8 (12 takoz üstünde) · taşıyıcı
     kirişler boşlukta.
  7. TEKNİK SÜTUN (4028,5–4398,5, K'nin altı): Secop bölmesi PU'suz (sıcak) · ara PU katmanı (sacları B_SOGUTMA'da; arkası 1,2 kapama sacı YENİ) ·
     soğuk depo: sağ PU 60, tavan PU, arka PU panel (sacları B_DEPO'da, değişmedi) — PU'lar bu saclara birebir oturur (eski 1 mm boşluklar yok).
  8. MODÜLER İSKELET (B_MODULER, A + TOPPING yükü): alt şase 60×60×3 (y 63–123: zemin elektrik kanalı kapağı y ≤ 51,5 altta serbest; 2 boyuna
     + 7 enine, ayak saplamaları boyunalardan Ø13 delikle geçer) · PU içinde 30×30×2 dikmeler (sol duvar, B1, B2 · ön + arka) + iki üst kiriş
     (ön z −125…−95 x 737,5–2731 → taşıyıcı ön kirişine alın alına · arka z −721…−691 x 737,5–2106 → B2 dikmesinde biter: elektrik ana hat
     kanalı x 2421–2451 yolunu keser) · dış saca 3 mm GFRP ısı köprüsü kesici (alt + üst).
  9. ELEKTRİK GEÇİŞİ (ELK_* değişmez): TOPPING altında ana hat kanalının ucu + kabloları PU içinde 1,2 sac kovanda (x 2419,8–2500) · ısı kalkanı
     boşluğundaki yatay tava ısı kalkanı yan saclarından, B5 üst PU'sundan (kovanlı) ve teknik duvardan delikle geçer · dış tavanda 2, dış
     tabanda 1 kablo geçiş deliği.
Birleşim: dış sac kenarları büküm + iç yüzden rivnut/PEM (görünür vida yok) · iç saclar köşelerde TIG, gıda bölgesinde bindirme yok ·
  çerçeve dış saca iç yüzden punta + silikon · köpük öncesi bütün dikişler sızdırmaz bant.
Kullanım: python b_govde_yeni.py giris.glb cikis.glb"""
import json, struct, sys
import numpy as np
import cadquery as cq

T_D, T_I, T_C = 1.5, 1.2, 1.0                     # dış · iç · çerçeve (430)
X0, X1 = 736.0, 4400.0
YB, YT = 123.0, 788.0
ZA, ZF = -830.0, 39.0
ZC0, ZC1 = 23.0, 24.0                             # çerçeve
XDi, XDs = X0 + T_D, X1 - T_D                     # 737,5 · 4398,5
YDi, YDs = YB + T_D, YT - T_D                     # 124,5 · 786,5
ZDa = ZA + T_D                                    # −828,5
XL = 798.5                                        # sol soğuk yüz
YF, YCH, YCL = 164.5, 728.0, 668.0                # taban · tavan yüksek · tavan alçak
ZB = -790.0                                       # arka soğuk yüz
X_ALCAK = 2108.5                                  # K3 sol kenarı (tavan basamağı)
XFIR = 2500.0                                     # fırın sol ucu (ısı kalkanı)
BOLME = [1418.5, 2073.5, 2728.5, 3383.5, 3993.5]  # B1..B5 sol yüzleri · 35
BW = 35.0
T0 = 4028.5                                       # teknik sütun sol iç yüzü
XKS = BOLME[4] + T_I                              # 3994,7 · ısı kalkanı sağ sacı / B5 PU başı
XB5b = T0 - T_I                                   # 4027,3


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def boru(x0, x1, y0, y1, z0, z1, et=2.0):        # dikdörtgen boru, uzun ekseni boyunca içi boş
    d = [x1 - x0, y1 - y0, z1 - z0]; ax = int(np.argmax(d)); a = [x0, x1, y0, y1, z0, z1]
    ic = [x0 + et, x1 - et, y0 + et, y1 - et, z0 + et, z1 - et]; ic[2 * ax], ic[2 * ax + 1] = a[2 * ax] - 1, a[2 * ax + 1] + 1
    return kutu(*a).cut(kutu(*ic))


def kes(s, *aletler):
    al = [a for a in aletler if a is not None]
    if not al: return s
    r = s.cut(*al)
    return r.clean() if hasattr(r, "clean") else r


# ---------------------------------------------------------------- değişmeyen arayüz verileri
CEK = [("K1", 798.5, 620.0, [200.5, 308.5, 416.5, 524.5, 632.5], [75.0] * 5),
       ("K2", 1453.5, 620.0, [200.5, 308.5, 416.5, 524.5, 632.5], [75.0] * 5),
       ("K3", 2108.5, 620.0, [200.5, 308.5, 416.5, 524.5], [75.0] * 4),
       ("K5", 2763.5, 620.0, [200.5, 308.5, 416.5, 524.5], [75.0, 75.0, 75.0, 126.0]),
       ("K6", 3418.5, 575.0, [200.5, 308.5, 471.5], [75.0, 130.0, 130.0])]
ACIKLIK = [(k, x, x + w, y, y + h) for k, x, w, ys, hs in CEK for y, h in zip(ys, hs)]
DEPO_ACIK = (4028.5, 4337.5, 463.5, 707.5)                       # depo çekmecesi açıklığı (h3 DEPO_ACIK)
SERVIS_ACIK = (4030.5, 4369.5, 126.0, 431.0)                     # Secop atış açıklığı (servis paneli klipsleri çerçeveye oturur)
EMIS_T = [(4033.0, 4140.0), (4160.0, 4267.0), (4287.0, 4394.0)]  # taban dış sacında emiş pencereleri · z −695…−565
ARKA_YARIK = [(2540.0 + 205.0 * i, 2725.0 + 205.0 * i) for i in range(7)]   # ısı kalkanı boşluğu arka yarıkları · y 748–778
TAKOZ_XZ = [(x, z) for x in (2650.0, 3050.0, 3350.0, 3700.0) for z in (-700.0, -250.0, 10.0)]
TASIYICI = [(2731.0, 4026.0, 746.5, 786.5, -130.0, -90.0), (2502.5, 4026.0, 746.5, 786.5, -640.0, -600.0),
            (2502.5, 2532.5, 746.5, 786.5, -600.0, -125.0)] + \
           [(x - 15.0, x + 15.0, 746.5, 786.5, -600.0, -130.0) for x in (2746.0, 3401.0, 4011.0)] + \
           [(x - 15.0, x + 15.0, 124.5, 746.5, z - 15.0, z + 15.0) for x in (2746.0, 3401.0, 4011.0) for z in (-110.0, -620.0)]
KANAL = [(988.5, 1028.5, 164.5, 703.0), (1643.5, 1683.5, 164.5, 703.0), (2298.5, 2338.5, 164.5, 643.0), (2953.5, 2993.5, 164.5, 643.0),
         (3608.5, 3648.5, 164.5, 643.0), (988.5, 2072.5, 703.0, 728.0), (2032.5, 2072.5, 668.0, 703.0), (2072.5, 4032.5, 643.0, 668.0)]
KAN_Z = (-790.0, -765.0)
GID_A, GID_B, GID_R = (2023.5, 200.5, -738.0), (4073.5, 177.95, -738.0), 12.0   # gider ana hattı ekseni · kılıf Ø24
# bölme hava geçişleri (arkada, plenum hizasında; arka iç sac kapatır) · B5'te depo geçişleri (soğuk K6 ↔ depo, ikisi de 668 altında)
HAVA = {0: [(190.0, 290.0), (560.0, 660.0)], 1: [(190.0, 290.0), (560.0, 660.0)], 3: [(190.0, 290.0), (400.0, 490.0)]}
HAVA_Z = (-790.0, -760.0)
DEPO_HAVA, DEPO_HAVA_Z = [(550.0, 600.0), (610.0, 660.0)], (-430.0, -380.0)
# modüler iskelet (A + TOPPING yükü) · ayak x'leri (B_KASA__celik ile aynı)
AYAK_X = [796.0, 1436.0, 2091.0, 2746.0, 3401.0, 4011.0, 4340.0]
MZ = [(-721.0, -691.0), (-125.0, -95.0)]                         # arka · ön dikme/kiriş hattı
M_DIKME_X = [(XDi, XDi + 30.0), (1421.0, 1451.0), (2076.0, 2106.0)]  # sol duvar (sol dış saca dayalı) · B1 · B2 (B3 arka: 2731–2761)
YG0, YG1 = YDi, YDi + 3.0                                         # alt GFRP 124,5–127,5
YK0, YK1 = YDs - 3.0 - 30.0, YDs - 3.0
YS0 = YB - 60.0                                                   # alt şase 60 × 60 × 3 (y 63–123): zemin elektrik kanalının kapağı (y ≤ 51,5) altta serbest
# ELEKTRİK ANA HAT GEÇİŞLERİ (ELK_ANA_HAT / ELK_ISTASYON değişmez → gövdede gömme sac kovan + sac delikleri)
E1 = (2421.0, XFIR, 742.5, YDs, -761.5, -558.5)                   # TOPPING altı: dikey kanalın ucu + kablolar (PU içinde, 1,2 sac kovanlı)
E2 = (XFIR, 4141.5, 742.5, YDs, -761.5, -640.5)                   # ısı kalkanı boşluğunda yatay tava → teknik sütun (B5 üstünde kovanlı)
DELIK_TAVAN = [(2421.0, 2451.0, -699.5, -558.5), (2971.6, 3008.4, -690.0, -653.5)]   # dış tavan sacı: dikey kanal · istasyon rakoru
DELIK_TABAN = [(4092.0, 4148.0, -704.0, -638.0)]                 # dış taban sacı: zemin rakoru (kablolar zemin kanalına iner)                            # üst kiriş 753,5–783,5 · üst GFRP 783,5–786,5


def bolme_kutusu(i):
    x = BOLME[i]; tav = YCH if i <= 1 else YCL
    return x, tav


def yap():
    S, P, C, M, G, KY = {}, {}, {}, {}, {}, {}     # sac · pu · çerçeve · modüler paslanmaz · gfrp · koyu (takoz)
    # ---------------- dış kabuk 1,5
    em = [kutu(a, b, YB - 1, YDi + 1, -695.0, -565.0) for a, b in EMIS_T] + [kutu(a, b, YB - 1, YDi + 1, c, d) for a, b, c, d in DELIK_TABAN]
    ay = [kutu(a, b, 748.0, 778.0, ZA - 1, ZDa + 1) for a, b in ARKA_YARIK]
    S["dis_sol_yan"] = kutu(X0, XDi, YB, YT, ZA, ZF)
    S["dis_sag_yan"] = kutu(XDs, X1, YB, YT, ZA, ZF)
    S["dis_tavan"] = kes(kutu(XDi, XDs, YDs, YT, ZA, ZF), *[kutu(a, b, YDs - 1, YT + 1, c, d) for a, b, c, d in DELIK_TAVAN])
    S["dis_taban"] = kes(kutu(XDi, XDs, YB, YDi, ZA, ZF), *em)
    S["dis_arka"] = kes(kutu(XDi, XDs, YDi, YDs, ZA, ZDa), *ay)
    # ---------------- ön çerçeve 430 · 1,0 · tek parça
    ac = [kutu(a, b, c, d, ZC0 - 1, ZC1 + 1) for _k, a, b, c, d in ACIKLIK]
    ac += [kutu(DEPO_ACIK[0], DEPO_ACIK[1], DEPO_ACIK[2], DEPO_ACIK[3], ZC0 - 1, ZC1 + 1),
           kutu(SERVIS_ACIK[0], SERVIS_ACIK[1], SERVIS_ACIK[2], SERVIS_ACIK[3], ZC0 - 1, ZC1 + 1),
           kutu(T0, 4338.5, 728.0, 729.0, ZC0 - 1, ZC1 + 1)]          # depo tavan iç sacının (B_DEPO, +37,5'e uzanır) yuvası
    C["on_cerceve"] = kes(kutu(XDi, XDs, YDi, YDs, ZC0, ZC1), *ac)
    # ---------------- iç kabuk 1,2 (soğuk hacmin sürekli yüzleri)
    S["ic_sol_yan"] = kutu(XL - T_I, XL, YF, YCH, ZB, ZC0)
    S["ic_taban"] = kutu(XL - T_I, XB5b, YF - T_I, YF, ZB - T_I, ZC0)
    S["ic_arka_yuksek"] = kutu(XL - T_I, X_ALCAK, YF, YCH, ZB - T_I, ZB)
    S["ic_arka_alcak"] = kutu(X_ALCAK, XB5b, YF, YCL, ZB - T_I, ZB)
    S["ic_tavan_yuksek"] = kutu(XL - T_I, X_ALCAK, YCH, YCH + T_I, ZB - T_I, ZC0)
    S["ic_tavan_alcak"] = kutu(X_ALCAK, XB5b, YCL, YCL + T_I, ZB - T_I, ZC0)
    # ---------------- bölmeler B1–B5 aynı kesit · hava / kanal geçişleri kovanlı
    kanal = [kutu(a, b, c, d, KAN_Z[0], KAN_Z[1]) for a, b, c, d in KANAL]
    gid = cq.Solid.makeCylinder(GID_R, float(np.linalg.norm(np.subtract(GID_B, GID_A))) + 200.0,
                                cq.Vector(*GID_A) - cq.Vector(*np.subtract(GID_B, GID_A)) * (100.0 / np.linalg.norm(np.subtract(GID_B, GID_A))),
                                cq.Vector(*np.subtract(GID_B, GID_A)))
    for i in range(5):
        x, tav = bolme_kutusu(i)
        env = (x, x + BW, YF, tav, ZB, ZC0)
        bosluk, kovan = [], []                                                    # hava/kanal geçiş hacmi (+1,2 kovan payı)
        hv = [(y0, y1, HAVA_Z[0], HAVA_Z[1]) for y0, y1 in HAVA.get(i, [])]
        if i == 4: hv += [(y0, y1, DEPO_HAVA_Z[0], DEPO_HAVA_Z[1]) for y0, y1 in DEPO_HAVA]
        kn = [(max(c, YF), min(d, tav), KAN_Z[0], KAN_Z[1]) for a, b, c, d in KANAL if a < x + BW and b > x and c < tav and d > YF]
        gec = [list(g) for g in hv + kn]                                          # üst üste binen geçişler tek açıklık (B2: hava + kanal)
        birlesti = True
        while birlesti:
            birlesti = False
            for a_ in range(len(gec)):
                for b_ in range(a_ + 1, len(gec)):
                    u, v = gec[a_], gec[b_]
                    if u[0] < v[1] + 2 * T_I and v[0] < u[1] + 2 * T_I and u[2] < v[3] + 2 * T_I and v[2] < u[3] + 2 * T_I:
                        gec[a_] = [min(u[0], v[0]), max(u[1], v[1]), min(u[2], v[2]), max(u[3], v[3])]; gec.pop(b_); birlesti = True; break
                if birlesti: break
        for y0, y1, z0, z1 in gec:
            dis = (x, x + BW, max(y0 - T_I, YF), min(y1 + T_I, tav), max(z0 - T_I, ZB), min(z1 + T_I, ZC0))
            ic_ = (x - 1, x + BW + 1, y0, y1, z0 - (1 if z0 <= ZB else 0), z1)
            bosluk.append(kutu(*dis)); kovan.append(kutu(*dis).cut(kutu(*ic_)))
        ek = bosluk + [gid]
        S["bolme_%d_sac_a" % (i + 1)] = kes(kutu(x, x + T_I, YF, tav, ZB, ZC0), *ek)
        S["bolme_%d_sac_b" % (i + 1)] = kes(kutu(x + BW - T_I, x + BW, YF, tav, ZB, ZC0), *ek) if i < 4 else None
        P["bolme_%d_pu" % (i + 1)] = kes(kutu(x + T_I, x + BW - T_I, YF, tav, ZB, ZC0), *ek)
        for j, k in enumerate(kovan):
            S["bolme_%d_kovan_%d" % (i + 1, j)] = k
        if i == 4: B5_DELIK = bosluk
    S.pop("bolme_5_sac_b")
    S["teknik_sol_duvar"] = kes(kutu(XB5b, T0, YDi, YDs, ZDa, ZC0), gid, *B5_DELIK)   # B5 teknik tarafı tam boy kapama sacı
    # ---------------- fırın altı ısı kalkanı
    S["isi_kalkani_ayirma"] = kutu(XFIR + T_I, BOLME[4], YCH, YCH + T_I, ZDa, ZC0)
    S["isi_kalkani_sol"] = kutu(XFIR, XFIR + T_I, YCH, YDs, ZDa, ZC0)
    S["isi_kalkani_sag"] = kutu(BOLME[4], XKS, YCH, YDs, ZDa, ZC0)
    S["isi_kalkani_isinim_0.8"] = kutu(XFIR + T_I + 1.0, BOLME[4] - 1.0, 740.0, 740.8, ZDa + 2.0, ZC0 - 2.0)
    for i, (x, z) in enumerate(TAKOZ_XZ):
        KY["isi_kalkani_takozu_%d" % i] = kutu(x - 10.0, x + 10.0, YCH + T_I, 740.0, z - 10.0, z + 10.0)
    # ---------------- PU (soğuk kasa) — bloklar sac/komşu blok yüzlerine tam oturur
    P["pu_sol"] = kutu(XDi, XL - T_I, YDi, YDs, ZDa, ZC0)
    P["pu_taban"] = kutu(XL - T_I, XB5b, YDi, YF - T_I, ZB - T_I, ZC0)
    P["pu_arka_yuksek"] = kutu(XL - T_I, XFIR, YDi, YDs, ZDa, ZB - T_I)
    P["pu_arka_alcak"] = kutu(XFIR, XB5b, YDi, YCH, ZDa, ZB - T_I)
    P["pu_tavan_yuksek"] = kutu(XL - T_I, X_ALCAK, YCH + T_I, YDs, ZB - T_I, ZC0)
    P["pu_tavan_topping"] = kutu(X_ALCAK, XFIR, YCL + T_I, YDs, ZB - T_I, ZC0)
    P["pu_tavan_firin"] = kutu(XFIR, XB5b, YCL + T_I, YCH, ZB - T_I, ZC0)
    P["pu_b5_ust"] = kutu(XKS, XB5b, YCH, YDs, ZDa, ZC0)
    # ---------------- teknik sütun: ara katman + depo PU'ları (sacları B_SOGUTMA / B_DEPO'da, değişmedi)
    S["tk_ara_arka_sac"] = kutu(T0, XDs, 433.5, 463.5, -494.0 - T_I, -494.0)
    P["tk_ara_pu"] = kutu(T0, XDs, 434.5, 462.5, -494.0, ZC0)
    P["tk_depo_arka_pu"] = kutu(T0, XDs, 463.5, YDs, -469.0, -441.0)
    P["tk_depo_sag_pu"] = kutu(4338.5, XDs, 463.5, YDs, -441.0, ZC0)
    P["tk_depo_tavan_pu"] = kutu(T0, 4338.5, 729.0, YDs, -441.0, ZC0).fuse(kutu(T0, 4338.5, 728.0, 729.0, -441.0, -440.0)).clean()
    # ---------------- modüler iskelet
    for zi, (z0, z1) in enumerate(MZ):
        ad = "arka" if zi == 0 else "on"
        M["sase_boyuna_%s" % ad] = None
        xs = M_DIKME_X
        for j, (a, b) in enumerate(xs):
            M["dikme_%s_%d" % (ad, j)] = boru(a, b, YG1, YK0, z0, z1)
            G["gfrp_alt_%s_%d" % (ad, j)] = kutu(a, b, YG0, YG1, z0, z1)
        xe = M_DIKME_X[-1][1] if zi == 0 else 2731.0               # arka: B2 dikmesinde biter (elektrik ana hat kanalı x 2421–2451 yolu keser) · ön: taşıyıcı ön kirişine alın alına
        M["ust_kiris_%s" % ad] = boru(XDi, xe, YK0, YK1, z0, z1)
        G["gfrp_ust_%s" % ad] = kutu(XDi, xe, YK1, YDs, z0, z1)
    del M["sase_boyuna_arka"], M["sase_boyuna_on"]
    M["sase_boyuna_arka"] = boru(XDi, XDs, YS0, YB, -790.0, -730.0, 3.0)
    M["sase_boyuna_on"] = boru(XDi, XDs, YS0, YB, -140.0, -80.0, 3.0)
    for j, x in enumerate(AYAK_X):
        xe_ = x - 2.0 if j == 5 else x                                            # B5 altındaki enine 2 mm sola: zemin elektrik kanalı x 4040'tan başlar
        M["sase_enine_%d" % j] = boru(xe_ - 30.0, xe_ + 30.0, YS0, YB, -730.0, -140.0, 3.0)
    ayak_delik = [cq.Solid.makeCylinder(6.5, 100.0, cq.Vector(x, 30.0, z), cq.Vector(0, 1, 0)) for x in AYAK_X for z in (-760.0, -110.0)]
    for k in ("sase_boyuna_arka", "sase_boyuna_on"):
        M[k] = kes(M[k], *ayak_delik)                                             # ayar ayağı M12 saplaması (Ø13 delik, üstte kaynak somunu)
    # ---------------- elektrik ana hat geçişi: gömme sac kovan (PU kovanın dışına dolar) + saclarda tava deliği
    S["elk_kovan_topping"] = kutu(E1[0] - T_I, E1[1], E1[2] - T_I, E1[3], E1[4] - T_I, E1[5] + T_I).cut(kutu(E1[0], E1[1] + 1, E1[2], E1[3] + 1, E1[4], E1[5]))
    S["elk_kovan_b5_alt"] = kutu(XKS, XB5b, E2[2] - T_I, E2[2], E2[4] - T_I, -640.0)
    S["elk_kovan_b5_arka"] = kutu(XKS, XB5b, E2[2], E2[3], E2[4] - T_I, E2[4])
    S["elk_kovan_b5_on"] = kutu(XKS, XB5b, E2[2] - T_I, 746.5, -640.0, -640.0 + T_I).fuse(kutu(4026.0, XB5b, 746.5, E2[3], -640.0, -640.0 + T_I)).clean()
    #   üstü (746,5–786,5) taşıyıcı arka kirişi kapatır · kiriş ucu (4026) ile teknik duvar arasındaki 1,3 mm şerit kovanın büküm dudağı
    tava = kutu(E2[0] - 1, E2[1], E2[2], E2[3], E2[4], E2[5])
    for k in ("isi_kalkani_sol", "isi_kalkani_sag", "teknik_sol_duvar"):
        S[k] = kes(S[k], tava)
    P["pu_tavan_topping"] = kes(P["pu_tavan_topping"], kutu(E1[0] - T_I, E1[1], E1[2] - T_I, E1[3], E1[4] - T_I, E1[5] + T_I))
    P["pu_b5_ust"] = kes(P["pu_b5_ust"], kutu(XKS, XB5b, E2[2] - T_I, E2[3], E2[4] - T_I, -640.0 + T_I))
    # ---------------- gömülü elemanlar PU'dan / saclardan düşülür (köpük etrafına dolar · sacta geçiş deliği)
    zarf = lambda s_: (lambda b: kutu(b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))(s_.BoundingBox())
    gomulu = [kutu(*t) for t in TASIYICI] + [zarf(m) for k, m in M.items() if not k.startswith("sase")] + [g for g in G.values()]
    for d in (P, S):
        for k in list(d):
            bb = d[k].BoundingBox()
            al = [g for g in gomulu if _kesisir(bb, g.BoundingBox())]
            if d is P: al += [s for s in S.values() if _kesisir(bb, s.BoundingBox())] + [gid] + [kk for kk in kanal if _kesisir(bb, kk.BoundingBox())]
            if al: d[k] = kes(d[k], *al)
    return dict(sac=S, pu=P, cerceve=C, moduler=M, gfrp=G, koyu=KY)


def yabanci():
    """GLB'deki DEĞİŞMEYEN komşu katılar (PU sarım denetiminde örtücü): depo + ara katman sacları, taşıyıcı, kablo kanalı, gider kılıfı"""
    Y = {"tk_depo_arka_sac_on": kutu(T0, 4338.5, 463.5, 728.0, -441.0, -440.0), "tk_depo_arka_sac_arka": kutu(T0, XDs, 463.5, YDs, -470.0, -469.0),
         "tk_depo_sag_ic_sac": kutu(4337.5, 4338.5, 463.5, 728.0, -440.0, ZC0), "tk_depo_tavan_ic_sac": kutu(T0, 4338.5, 728.0, 729.0, -440.0, 37.5),
         "tk_ara_sac_alt": kutu(T0, XDs, 433.5, 434.5, -494.0, ZC0), "tk_ara_sac_ust": kutu(T0, XDs, 462.5, 463.5, -494.0, ZC0)}
    for i, t in enumerate(TASIYICI): Y["tasiyici_%d" % i] = kutu(*t)
    for i, (a, b, c, d) in enumerate(KANAL): Y["kablo_kanali_%d" % i] = kutu(a, b, c, d, KAN_Z[0], KAN_Z[1])
    v = np.subtract(GID_B, GID_A); L = float(np.linalg.norm(v))
    Y["gider_kilifi"] = cq.Solid.makeCylinder(GID_R, L, cq.Vector(*GID_A), cq.Vector(*v))
    return Y


def _kesisir(a, b, e=0.01):
    return a.xmin < b.xmax - e and b.xmin < a.xmax - e and a.ymin < b.ymax - e and b.ymin < a.ymax - e and a.zmin < b.zmax - e and b.zmin < a.zmax - e


if __name__ == "__main__" and len(sys.argv) >= 2 and sys.argv[1] == "--kuru":
    import time; t = time.time(); R = yap()
    for g, d in R.items():
        print(g, len(d), round(sum(s.Volume() for s in d.values()) / 1e6, 2), "dm³")
    print("%.1f s" % (time.time() - t))


# ================================================================ GLB yazımı (a_govde_yeni.py ile aynı yöntem)
def ag(solidler):
    P, I = [], []
    for s in solidler:
        for f in s.Faces():
            v, t = f.tessellate(0.1, 0.2)
            o = sum(len(p) for p in P)
            P.append(np.array([[q.x, q.y, q.z] for q in v], float))
            I.append(np.array(t, np.int64) + o if len(t) else np.zeros((0, 3), np.int64))
    X = np.vstack(P); T = np.vstack(I)
    Xf = X[T.reshape(-1)]; n = np.cross(Xf[1::3] - Xf[0::3], Xf[2::3] - Xf[0::3])
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return (Xf / 1000.0).astype(np.float32), np.repeat(n, 3, axis=0).astype(np.float32), np.arange(len(Xf), dtype=np.uint32)


def glb_yaz(gi, go, R):
    raw = open(gi, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]; J = json.loads(raw[20:20 + jl]); bo = 20 + jl
    bl = struct.unpack("<I", raw[bo:bo + 4])[0]; BIN = bytearray(raw[bo + 8:bo + 8 + bl])

    def ekle(arr, tip, hedef):
        while len(BIN) % 4: BIN.extend(b"\0")
        off = len(BIN); BIN.extend(arr.tobytes())
        J["bufferViews"].append({"buffer": 0, "byteOffset": off, "byteLength": arr.nbytes, "target": hedef})
        a = {"bufferView": len(J["bufferViews"]) - 1, "componentType": 5126 if arr.dtype == np.float32 else 5125, "count": int(len(arr)), "type": tip}
        if tip == "VEC3": a["min"] = arr.min(axis=0).tolist(); a["max"] = arr.max(axis=0).tolist()
        J["accessors"].append(a); return len(J["accessors"]) - 1

    def koy(dugum, solidler):
        X, N, I = ag(solidler)
        nd = [n for n in J["nodes"] if n.get("name") == dugum][0]
        assert not any(k in nd for k in ("translation", "rotation", "scale", "matrix")), dugum
        pr = J["meshes"][nd["mesh"]]["primitives"][0]
        pr["attributes"] = {"POSITION": ekle(X, "VEC3", 34962), "NORMAL": ekle(N, "VEC3", 34962)}
        pr["indices"] = ekle(I, "SCALAR", 34963)
        nt = len(I); ex = pr.setdefault("extras", {})                       # 'kat'/'mek' aralıkları İNDİS sayısıyla (üçgen × 3)
        ex["kat"] = [ex.get("kat", [0])[0], 0, nt]; ex["mek"] = [ex.get("mek", [13])[0], 0, nt]; ex["kpk"] = []
        print("  %-24s %4d parça  %6d üçgen" % (dugum, len(solidler), nt // 3))

    koy("B_KASA__sac", list(R["sac"].values()))
    koy("B_KASA__pu", list(R["pu"].values()))
    koy("B_KASA__on_cerceve", list(R["cerceve"].values()))
    koy("B_KASA__koyu", list(R["koyu"].values()))
    koy("B_MODULER__paslanmaz", list(R["moduler"].values()))
    koy("B_MODULER__gfrp", list(R["gfrp"].values()))
    for n in J["nodes"]:                                                    # ön çerçeve: gövde malzemesi, opak, kapak değil
        if n.get("name") == "B_KASA__on_cerceve":
            p = J["meshes"][n["mesh"]]["primitives"][0]; m = J["materials"][p["material"]]
            m["pbrMetallicRoughness"] = {"baseColorFactor": [0.74, 0.77, 0.80, 1.0], "metallicFactor": 0.85, "roughnessFactor": 0.32}
            m.pop("alphaMode", None); m["doubleSided"] = True; p["extras"]["kpk"] = []
    J["buffers"][0]["byteLength"] = len(BIN)
    jb = json.dumps(J, separators=(",", ":")).encode(); jb += b" " * ((4 - len(jb) % 4) % 4)
    while len(BIN) % 4: BIN.extend(b"\0")
    open(go, "wb").write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(jb) + 8 + len(BIN)) + struct.pack("<II", len(jb), 0x4E4F534A) + jb
                         + struct.pack("<II", len(BIN), 0x004E4942) + bytes(BIN))
    print("yazıldı", go)


if __name__ == "__main__" and len(sys.argv) == 3:
    R = yap()
    for g, d in R.items():
        print("%-9s %3d parça  %8.2f dm³" % (g, len(d), sum(s.Volume() for s in d.values()) / 1e6))
    glb_yaz(sys.argv[1], sys.argv[2], R)
