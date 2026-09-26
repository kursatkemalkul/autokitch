# -*- coding: utf-8 -*-
"""topping_uno_cad_v5 → topping_uno_cad_v6 (26 Eyl 2026 gece, Kemal):
 1 · KASET YUVALARI tam mühendislik: kaset raf üstünde havada duruyordu (gövde altı 1335 / 1341, raf 1320). Her kasete
     2 KIZAK (304 · gövde altını taşır, dış dudakla 0,5 mm yanal kılavuz, önde 30 mm 10° giriş pahı) · ARKA DAYAMA ×2 (kaset
     gövdesinin arka yüzü dayanır → z konumu) · ÖN MANDAL (POM yaylı dil: takarken kasetin altına kalkar, geçince önüne düşer =
     KLİK; kolu bastırınca çıkar) · her tahrik miline KAVRAMA (yaylı kayar kovan, kare yuva 8,4 × 6 derin: kasetin 5,5 mm'lik kare
     mil ucunu alır; PLC yavaş çevirip oturtur). VİDA YOK — aletsiz tak-çıkar. Raf deliği ÖNE AÇIK U-yarık (çıkış tüpü öne
     kayarken raftan sıyrılır), raf ön bükümünde 60'lık çentik. Sucuk kaseti 10 mm sağa: kaşar–sucuk boşluğu 20 → 30, sucuk–duvar 36.
 2 · YALITIM TAM KUTU: soguk_hucre_A/B_tavan + basamak + arka_yalitim_A/B → tek dikdörtgen PU blok (90–1710 × 1277–2028,5 ×
     −104…−630); içinde soğuk oda (A 1968, B 1680 tavan), arkaya açık teknik cep (soğutma grubu · pano · güç · UPS, 850–1710 ×
     1740–2012), kovan/mil/geçiş bloğu delikleri. ÖN FİTİL (çekmecelerdeki gibi manyetik profil 21 × 18,5) soğuk odanın L
     ağzının çevresinde; ön kapaklar SONRA (Kemal).
 3 · Kaset çıkış yolu taraması (__main__): kaset 10 mm adımlarla öne çekilir (mandal kalkık), hiçbir parçaya değmemeli."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v5.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


d('"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v5 · 25 Eyl 2026',
  '"""TOPPING v2 (UNO\'lu) · 3B MODEL · topping_uno_cad_v6 · 26 Eyl 2026 gece\n'
  'v6 (Kemal: "kasetlerin yerlerini tam mühendislik yap — vidalanacak mı, nasıl çıkacak, hizalama, aralarında boşluk; yalıtım tam\n'
  'kare olsun, önünde çekmecelerdeki gibi conta"): KASET YUVALARI (kılavuz köşebentler · arka dayama · SOLDA yaylı KAYAR mandal ·\n'
  'her milde yaylı HAÇ yuvası: Ø48 POM kovan + 4 yay + boydan pim + segmanlı yay tablası · raf U-yarığı · iniş hunisi) · sucuk 13 mm sağa\n'
  '(boşluklar: kuşbaşı–kaşar mandalı 25 · kaşar kılavuzu–sucuk mandalı 10,5 · sucuk–duvar 25,5) · YALITIM TEK BLOK (teknik cep arkaya\n'
  'açık) + ÖN FİTİL. Önceki: topping_uno_cad_v5.py\nv5:')
d('KASET = [("KAŞAR KABI", "kasar_cad_v14", 1220.0, 1502.0), ("KÜP SUCUK", "sucuk_cad_v7", 1522.0, 1664.0)]',
  'KASET = [("KAŞAR KABI", "kasar_cad_v14", 1220.0, 1502.0), ("KÜP SUCUK", "sucuk_cad_v7", 1539.0, 1681.0)]   # v6: sucuk +13 (kaşar–sucuk plakaları 30, sağ duvar 25,5)')
# ---- raf: U-yarık + ön büküm çentiği ----
d('''ekle("tasiyici_raf_3mm", _raf, "paslanmaz", "H", not_="AISI 304 · 3 mm · yük 154 kg · sehim 3,4 mm · emniyet 2,3 · ağız delikleri")
ekle("raf_on_bukumu", kut(90, W - 90, SOGUK_TABAN - RAF_T - RAF_BUKUM, SOGUK_TABAN - RAF_T, Z_KAPAK[1] - RAF_T, Z_KAPAK[1]), "paslanmaz", "H", not_="40 mm aşağı büküm (rafın kirişi)")''',
  '''_rob = kut(90, W - 90, SOGUK_TABAN - RAF_T - RAF_BUKUM, SOGUK_TABAN - RAF_T, Z_KAPAK[1] - RAF_T, Z_KAPAK[1])
for _ad, _mod, _x0, _x1 in KASET:                                                       # v6: kaset çıkış tüpü öne kayarken raftan sıyrılsın: U-yarık + çentik
    _xc = (_x0 + _x1) / 2.0; _r = KAS_R[_mod][0]
    _raf = _raf.cut(kut(_xc - _r, _xc + _r, SOGUK_TABAN - RAF_T - 1, SOGUK_TABAN + 1, KAS_Z, Z_KAPAK[1] + 1))
    _rob = _rob.cut(kut(_xc - _r, _xc + _r, SOGUK_TABAN - RAF_T - RAF_BUKUM - 1, SOGUK_TABAN - RAF_T + 1, Z_KAPAK[1] - RAF_T - 1, Z_KAPAK[1] + 1))
ekle("tasiyici_raf_3mm", _raf, "paslanmaz", "H", not_="AISI 304 · 3 mm · yük 154 kg · sehim 3,4 mm · emniyet 2,3 · ağız delikleri · v6: kaset delikleri öne açık U-yarık (Ø60)")
ekle("raf_on_bukumu", _rob, "paslanmaz", "H", not_="40 mm aşağı büküm (rafın kirişi) · v6: kaset yarıklarında 60 çentik")''')
# ---- yalıtım: 5 parça → tek blok + fitil ----
d('''ekle("soguk_hucre_A_tavan", kut(BAY_A[0], BAY_A[1], TAVAN_A, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1]), "pu", "Ö", not_="sos + harç üstünde tavan 1968")
ekle("soguk_hucre_B_tavan", kut(BAY_B[0], BAY_B[1], TAVAN_B, TAVAN_B + 60, Z_KAPAK[1], Z_BOLME[1]), "pu", "Ö")
ekle("soguk_hucre_basamak", kut(BAY_B[0], BAY_B[0] + 60, TAVAN_B + 60, TAVAN_A, Z_KAPAK[1], Z_BOLME[1]), "pu", "Ö")
ekle("arka_yalitim_A", kut(BAY_A[0], BAY_A[1], SOGUK_TABAN - 43, TAVAN_A, Z_BOLME[0], Z_BOLME[1]), "pu", "Ö")
ekle("arka_yalitim_B", kut(BAY_B[0], BAY_B[1], SOGUK_TABAN - 43, TAVAN_B + 60, Z_BOLME[0], Z_BOLME[1]), "pu", "Ö")
''', '''# v6 · YALITIM TEK BLOK ("tam kare"): dışı düz dikdörtgen; içinde soğuk oda (A tavan 1968 · B tavan 1680), arkaya açık TEKNİK CEP,
#      kaset kovanı / UNO mil kovanı / geçiş bloğu delikleri. Fitil ve kaset yuvaları aşağıda (kasetlerden sonra).
YAL_Y0 = SOGUK_TABAN - 43                                                             # 1277 (raf bükümünün altı)
CEP_TEKNIK = (850.0, W - 90, TAVAN_B + 60, 2012.0, -110.0, Z_BOLME[1])               # soğutma grubu · pano · güç · UPS (zarflar) — arkadan servis
_yal = kut(BAY_A[0], BAY_B[1], YAL_Y0, YUST - 1.5, Z_KAPAK[1], Z_BOLME[1])
_yal = _yal.cut(kut(BAY_A[0] - 1, BAY_A[1], YAL_Y0 - 1, TAVAN_A, Z_KAPAK[1] + 1, Z_BOLME[0]))          # soğuk oda A
_yal = _yal.cut(kut(BAY_B[0], BAY_B[1] + 1, YAL_Y0 - 1, TAVAN_B, Z_KAPAK[1] + 1, Z_BOLME[0]))          # soğuk oda B
_yal = _yal.cut(kut(CEP_TEKNIK[0], CEP_TEKNIK[1] + 1, CEP_TEKNIK[2], CEP_TEKNIK[3], CEP_TEKNIK[4], CEP_TEKNIK[5] - 1))   # teknik cep (arkaya açık)
_yal = _yal.cut(kut(89, 1201, 1439, 1471, Z_BOLME[1] - 1, Z_BOLME[0] + 1))                              # geçiş bloğu yuvası
for _ad, _cx, *_r in UNO:
    _yal = _yal.cut(silz(_cx, V_EKSEN, 15.5, Z_BOLME[1] - 1, Z_BOLME[0] + 1))                         # UNO mil geçiş kovanı
YAL_BLOK = [_yal]                                                                     # kaset kovan delikleri kasetlerden sonra açılır (ekle orada)
''')
# ---- kasetler: mil kısalır (kavrama kovanı miline biner) ----
d('''        ekle("mil_" + tag, silz(xc, yy, 11, -670, -525), "celik", "Ö", grup=("HELEZON_" if kk == "helezon" else "KARISTIRICI_") + KOD)''',
  '''        _mil = silz(xc, yy, 11, -670, -545).cut(kut(xc - 1.6, xc + 1.6, yy - 12.0, yy + 12.0, -560.5, -546.5))   # v6: −545'e kadar · haç yuvası pim kanalı 3,2 × 14 BOYDAN BOYA (−560,5…−546,5; uçta 1,5 köprü)
        _mil = _mil.cut(silz(xc, yy, 11.5, -564.7, -563.5).cut(silz(xc, yy, 10.3, -565.0, -563.0)))                # segman kanalı (DIN 471 22 × 1,2): yay tablasının dayandığı yer
        ekle("mil_" + tag, _mil, "celik", "Ö", grup=("HELEZON_" if kk == "helezon" else "KARISTIRICI_") + KOD,
             not_="Ø22 · kovanda keçeli · ucunda boydan boya pim kanalı 3,2 × 14 (haç yuvası 10,5 kayar) + segman kanalı (v6)")
        YAL_BLOK[0] = YAL_BLOK[0].cut(silz(xc, yy, 30.5, Z_BOLME[1] - 1, Z_BOLME[0] + 1))            # v6: yalıtım bloğunda kovan deliği''')
# ---- iniş borusu: kaset borusuyla iç içe geçmesin (v5'te 1312–1317 arası 5 mm geçiyordu → kaset öne çekilemezdi) ----
d('''    ekle("%s_inis_borusu" % _mod.split("_")[0], sily(_x, KAS_Z, ro, 1216.0, SOGUK_TABAN - RAF_T).cut(sily(_x, KAS_Z, ri, 1215.0, SOGUK_TABAN)), "paslanmaz", "H",
         not_="kaset borusunun devamı: raftan pideye 40 mm kalana iner (v1'de yalıtımdaki dozaj kovanıydı)")''',
  '''    HUNI_Y = (1305.0, 1311.0)                                                                          # v6: boru üstü 1305 · huni 1305–1311 · kaset borusunun altı 1312 → 1 mm, iç içe DEĞİL
    ekle("%s_inis_borusu" % _mod.split("_")[0], sily(_x, KAS_Z, ro, 1216.0, HUNI_Y[0]).cut(sily(_x, KAS_Z, ri, 1215.0, HUNI_Y[0] + 1.0)), "paslanmaz", "H",
         not_="kaset borusunun devamı: üstü 1305 — kaset borusu (dış Ø%.0f) 1312'de biter, iç içe geçmez (v5'te 5 mm geçiyordu, kaset öne çekilemezdi) · pideye 40 mm kalana iner" % (2 * ro))
    _hn = cq.Solid.makeCone(ro, 32.0, HUNI_Y[1] - HUNI_Y[0], V(_x, HUNI_Y[0], KAS_Z), V(0, 1, 0))
    _hn = _hn.cut(cq.Solid.makeCone(ri, 29.0, HUNI_Y[1] - HUNI_Y[0], V(_x, HUNI_Y[0], KAS_Z), V(0, 1, 0))).cut(sily(_x, KAS_Z, ri, HUNI_Y[0] - 1.0, HUNI_Y[0] + 0.5).val())
    ekle("%s_inis_hunisi" % _mod.split("_")[0], _hn, "paslanmaz", "H",
         not_="huni iç Ø%.0f→Ø58 · 1305–1311 · kaset borusunun altındaki 1 mm boşluğu ve 4 mm yanal payı örter → kaset öne çekilirken boruya takılmaz" % (2 * ri))''')
# ---- kasetlerden sonra: yuva parçaları + yalıtım bloğu + fitil ----
d('''# ================================================================ 4 · HAVA TESİSATI''',
  '''# ================================================================ 3b · KASET YUVALARI (v6) — kaset gövdesine DOKUNULMADI, yuva kasete uyar
# Ölçüldü (26 Eyl): kaset ÖN/ARKA PLAKALARI (280 / 140 × 352 × 8) raf üstüne (1320) oturur — kasetin ayağı plakalardır, gövde 15/21 mm yukarıda.
# Kasetin arkasında kendi HAÇ KAVRAMASI var (kasar_cad_v14: Ø26 disk + 36 × 8 haç, z −543,5…−533,5) — "makinedeki yaylı yuvaya oturur".
# Plakaların arkasında kör somunlar (z −538,6), önünde somunlar / topuz / tüp yatak kapağı (−96,5'e kadar).
def prizma_xz(pts, y0, y1):
    return cq.Workplane("XZ", origin=(0.0, y1, 0.0)).polyline(pts).close().extrude(y1 - y0)
def _bbx(ad): return [p for p in P if p["ad"] == ad][0]["sh"].BoundingBox()
YUVA = {}
for ad, mod, x0, x1 in KASET:
    KOD = "KASAR" if mod.startswith("kasar") else "SUCUK"; k = KOD.lower()
    pb = _bbx("%s__plaka_on" % mod); px0, px1, pz1 = pb.xmin, pb.xmax, pb.zmax                          # plaka: x · ön yüz (−200)
    pz0 = _bbx("%s__plaka_arka" % mod).zmin                                                             # arka plaka arka yüzü (−525)
    hb = _bbx("%s__kavrama_helezon" % mod)                                                              # haç kavrama: z −543,5…−525,5
    xc = (x0 + x1) / 2.0; ST = SOGUK_TABAN
    YUVA[KOD] = dict(px0=px0, px1=px1, pz0=pz0, pz1=pz1, xc=xc, hac_arka=hb.zmin)
    dz_stop = 20.0 if KOD == "KASAR" else 9.0                                                           # arka dayama genişliği (kör somunlara 15 / 2 mm)
    mz = pz1 + 0.5                                                                                      # mandal dili: plakanın ön yüzünün 0,5 önünde
    for yon, xa, sgn in (("sol", px0, 1.0), ("sag", px1, -1.0)):
        # kılavuz dudak: L köşebent 4 × 20, plakaya 0,5 boşluk, plakaların tüm boyu + önde 20 giriş; önde 30 mm boyunca 3 mm dışa açılır (10°)
        dud = kut(xa - sgn * 0.5, xa - sgn * 4.5, ST, ST + 20.0, pz0 - 20.0, pz1 + 20.0)
        pah = prizma_xz([(xa - sgn * 0.5, pz1 - 10.0), (xa - sgn * 0.5, pz1 + 21.0), (xa - sgn * 3.5, pz1 + 21.0)], ST - 1.0, ST + 21.0)
        dud = dud.cut(pah)
        if yon == "sol": dud = dud.cut(kut(xa - 6.0, xa + 1.0, ST + 1.0, ST + 11.0, mz - 1.0, mz + 7.0))        # mandal dili penceresi 10 × 8
        ekle("yuva_%s_kilavuz_%s" % (k, yon), dud, "paslanmaz", "H",
             not_="304 köşebent 4 × 20 · kaset plakalarını yanal 0,5 mm boşlukla güder · önde 30 mm 10° giriş pahı · rafa 3 × M4 havşa" + (" · önde mandal dili penceresi" if yon == "sol" else ""))
        ekle("yuva_%s_arka_dayama_%s" % (k, yon), kut(xa, xa + sgn * dz_stop, ST, ST + 30.0, pz0 - 20.0, pz0), "paslanmaz", "H",
             not_="arka plaka alt köşesi buna dayanır (z %.0f) → kavrama derinliği sabit · kılavuzla tek parça bükme · kör somunlara değmez" % pz0)
    # ÖN MANDAL — SOL kılavuzun önünde, plakanın dışında. X'TE KAYAR DİL: POM dil plakanın ön-alt köşesinin ÖNÜNDE durur (plakayı 6 mm örter).
    # Takarken plakanın alt köşesi dilin 45° rampasına basar → dil sola kayar → plaka geçince yay dili geri iter (KLİK).
    # Çıkarmak: kol sola bastırılır (6,5 mm), kaset kulpundan çekilir. (Sağda yer yoktu: sucuk mandalı sağ duvara 10 mm kalıyordu.)
    gov = kut(px0 - 24.0, px0 - 5.0, ST, ST + 34.0, mz - 8.0, mz + 24.0)
    gov = gov.cut(kut(px0 - 21.5, px0 - 7.5, ST + 1.5, ST + 35.0, mz - 9.0, mz + 8.0))                  # dil + kol kanalı (üstü açık, duvarlar 2,5)
    gov = gov.cut(kut(px0 - 8.0, px0 - 4.0, ST + 1.5, ST + 11.0, mz - 1.0, mz + 7.0))                    # iç duvarda dil penceresi
    gov = gov.cut(silx(ST + 18.0, mz + 3.0, 1.6, px0 - 25.0, px0 - 4.0))                                 # pim deliği
    ekle("yuva_%s_mandal_govdesi" % k, gov, "pom", "H", not_="mandal yuvası POM 19 × 34 × 32 · U kanal (duvar 2,5) · kılavuza 2 × M4 · pim iki yan duvarda")
    dil = kut(px0 - 14.0, px0 + 6.0, ST + 2.0, ST + 10.0, mz, mz + 6.0).cut(prizma_xz([(px0 + 6.0, mz + 6.0), (px0 + 6.0, mz + 0.5), (px0 + 0.5, mz + 6.0)], ST + 1.0, ST + 11.0))
    dil = dil.union(kut(px0 - 14.0, px0 - 10.0, ST + 2.0, ST + 44.0, mz, mz + 6.0))                     # dik kol: pim üstünde kayar, üstü baş parmak (gövdenin 10 üstünde)
    dil = dil.cut(silx(ST + 6.0, mz + 3.0, 1.75, px0 - 14.5, px0 - 2.0)).cut(silx(ST + 18.0, mz + 3.0, 1.6, px0 - 15.0, px0 - 9.0))   # yay deliği Ø3,5 × 12 · pim deliği
    ekle("yuva_%s_mandal_dili" % k, dil, "pom", "H",
         not_="kayar dil POM 20 × 8 × 6 + kol 4 × 42 · plakayı 6 mm örter · ucu 45° rampa (takarken plaka dili sola iter) · yay geri iter · kol 6,5 mm sola basılınca kaset serbest")
    ekle("yuva_%s_mandal_yayi" % k, silx(ST + 6.0, mz + 3.0, 1.5, px0 - 21.5, px0 - 2.0).cut(silx(ST + 6.0, mz + 3.0, 1.1, px0 - 22.0, px0 - 1.5)), "celik", "V",
         not_="baskı yayı Ø3 × 19,5 (tel 0,4) · dilin deliğinde, gövdenin dış duvarına dayanır · ≈2 N")
    ekle("yuva_%s_mandal_pimi" % k, silx(ST + 18.0, mz + 3.0, 1.5, px0 - 24.0, px0 - 5.0), "celik", "V", not_="Ø3 × 19 kılavuz pimi: iki yan duvara sıkı geçme, dil üstünde kayar")
    # HAÇ YUVASI (kasetin haç kavraması buna oturur): her tahrik milinde YAYLI KAYAR POM KOVAN Ø48 × 18; önünde haç yarığı 10,5 derin (çubuklar
    # 9,5 girer, dipte 1 mm). 4 baskı yayı (Ø5 × 24,5, 45°'lerde r 18) kovanın arka ceplerinde; yaylar milin segmanına oturan yay tablasına dayanır
    # (kovan · yaylar · tabla · pim = hepsi milyle döner; sürtünen yüzey yok). Tork + strok sınırı: boydan boya Ø3 pim, mildeki 3,2 × 14 kanalda.
    # Kaset takılırken haç hizalı değilse çubuklar kovanı 9,5 geri iter (tabla 10,5'te durdurur), PLC mili yavaş çevirir, yarık hizalanınca
    # yaylar kovanı öne iter → haç oturur (KLİK). Bakım: kovan segman sökülmeden çıkar (pim çekilir).
    Vm = importlib.import_module(mod)
    for ey, kk in zip(TC.eksen(mod), ("helezon", "rotor")):
        yy = ST + ey; tag = "%s_%s" % (k, kk); gr = ("HELEZON_" if kk == "helezon" else "KARISTIRICI_") + KOD
        z_agiz = hb.zmax - 18.0 + 10.0 - 0.5                                                            # haç çubuklarının ön yüzü −533,5 → yuva ağzı −534
        YAYC = [(xc + 18.0 * math.cos(math.radians(45 + 90 * i)), yy + 18.0 * math.sin(math.radians(45 + 90 * i))) for i in range(4)]
        kv = silz(xc, yy, 24.0, z_agiz - 18.0, z_agiz)                                                  # POM Ø48 × 18 (−552…−534)
        kv = kv.cut(silz(xc, yy, 13.5, z_agiz - 10.5, z_agiz + 1.0))                                    # disk boşluğu Ø27 × 10,5 (kavrama Ø26 · dipte 1 mm)
        kv = kv.cut(kut(xc - 18.25, xc + 18.25, yy - 4.25, yy + 4.25, z_agiz - 10.5, z_agiz + 1.0))    # haç yarığı 36,5 × 8,5 × 10,5
        kv = kv.cut(kut(xc - 4.25, xc + 4.25, yy - 18.25, yy + 18.25, z_agiz - 10.5, z_agiz + 1.0))
        kv = kv.cut(silz(xc, yy, 11.1, z_agiz - 18.5, z_agiz - 10.0))                                   # mil deliği Ø22,2 (mil ucu −545, dipten 0,5 geride)
        kv = kv.cut(kut(xc - 1.6, xc + 1.6, yy - 25.0, yy + 25.0, z_agiz - 15.6, z_agiz - 12.4))       # pim deliği Ø3,2 boydan boya (pim −549,5…−546,5)
        for cxi, cyi in YAYC: kv = kv.cut(silz(cxi, cyi, 3.0, z_agiz - 18.5, z_agiz - 3.5))            # 4 yay cebi Ø6 × 14,5 (yarıkların arasında, r 18)
        ekle("yuva_%s_hac_yuvasi" % tag, kv, "pom", "H", grup=gr,
             not_="POM Ø48 × 18 · önünde 36,5 × 8,5 haç yarığı 10,5 derin (kaset haçı 9,5 girer) · milde pimle kayar (strok 10,5; kaset en çok 9,5 iter) · 4 yay öne iter · PLC yavaş çevirir, haç oturur (KLİK)")
        for i, (cxi, cyi) in enumerate(YAYC):
            ekle("yuva_%s_yay_%d" % (tag, i), silz(cxi, cyi, 2.5, z_agiz - 28.5, z_agiz - 4.0).cut(silz(cxi, cyi, 2.0, z_agiz - 29.0, z_agiz - 3.5)), "celik", "V", grup=gr,
                 not_="baskı yayı Ø5 × 24,5 (tel 0,4 · serbest 28) — gösterim: kovan · kovan 9,5 geri çekilince 15'e sıkışır · 4'ü birden ≈3–12 N")
        tb = silz(xc, yy, 24.0, z_agiz - 29.5, z_agiz - 28.5).cut(silz(xc, yy, 11.5, z_agiz - 30.0, z_agiz - 28.0))
        for cxi, cyi in YAYC: tb = tb.union(silz(cxi, cyi, 1.8, z_agiz - 28.5, z_agiz - 24.5))
        ekle("yuva_%s_yay_tablasi" % tag, tb, "paslanmaz", "H", grup=gr, not_="yay tablası 304 · Ø48 × 1 · milin segmanına oturur, milyle döner · 4 yay pilotu Ø3,6 × 4 · kovan 10,5'te buna dayanır")
        ekle("yuva_%s_segmani" % tag, silz(xc, yy, 12.3, z_agiz - 30.7, z_agiz - 29.5).cut(silz(xc, yy, 10.3, z_agiz - 31.0, z_agiz - 29.0)), "celik", "V", grup=gr,
             not_="segman DIN 471 22 × 1,2 · mil kanalında · kovan yüzüne 0,3")
        ekle("yuva_%s_kavrama_pimi" % tag, kut(xc - 1.5, xc + 1.5, yy - 24.0, yy + 24.0, z_agiz - 15.5, z_agiz - 12.5), "celik", "V", grup=gr,
             not_="Ø3 × 48 sertleştirilmiş pim (ISO 8734): kovanı mile bağlar (tork), mildeki 3,2 × 14 kanalda kayar (strok 10,5)")
ekle("yalitim_blogu", YAL_BLOK[0], "pu", "Ö",
     not_="v6 TEK BLOK PU 60 (sac kaplı) · dışı 1620 × 751 × 526 düz · soğuk oda A tavan 1968 / B 1680 · teknik cep arkaya açık · 4 kaset kovanı + 4 UNO kovanı + geçiş bloğu delikleri")
# ön fitil: soğuk odanın L ağzının çevresi (A 90–790 × 1277–1968 · B 790–1710 × 1277–1680), manyetik profil 21 × 18,5 (çekmecelerle aynı) · ön kapak SONRA
FITIL_W, FITIL_T = 21.0, 6.0
_agiz = [(BAY_A[0], YAL_Y0), (BAY_B[1], YAL_Y0), (BAY_B[1], TAVAN_B), (BAY_A[1], TAVAN_B), (BAY_A[1], TAVAN_A), (BAY_A[0], TAVAN_A)]
_dis = cq.Workplane("XY", origin=(0, 0, Z_KAPAK[1])).polyline([(x + (-FITIL_W if x == BAY_A[0] else FITIL_W), y + (-FITIL_W if y == YAL_Y0 else (FITIL_W if y in (TAVAN_A,) or (y == TAVAN_B and x == BAY_B[1]) else 0.0))) for x, y in _agiz]).close().extrude(FITIL_T)
_ic = cq.Workplane("XY", origin=(0, 0, Z_KAPAK[1] - 1)).polyline(_agiz).close().extrude(FITIL_T + 2)
ekle("on_fitil", _dis.cut(_ic), "silikon", "H",
     not_="manyetik fitil 21 × 18,5 (sıkışınca 15) kanallı alüminyum profilde · L ağzın çevresi · ön kapak kapanınca buna basar · çekmece fitiliyle aynı profil")

# ================================================================ 4 · HAVA TESİSATI''')
# ---- denetimler: yuva ----
d('''kontrol("hortumlar kaset motorlarına değmiyor", cak == 0, "%d çakışma" % cak)
''', '''kontrol("hortumlar kaset motorlarına değmiyor", cak == 0, "%d çakışma" % cak)
# v6 · kaset yuvaları
for KOD, Y_ in YUVA.items():
    k = KOD.lower(); mod = "kasar_cad_v14" if KOD == "KASAR" else "sucuk_cad_v7"
    kas = cq.Compound.makeCompound([p["sh"] for p in P if p["ad"].startswith(mod)])
    yuva = [p for p in P if p["ad"].startswith("yuva_%s_" % k)]
    _kes = 0
    for p in yuva:
        try:
            if kas.intersect(p["sh"]).Volume() > 1.0: _kes += 1; print("   yuva parçası kasete giriyor:", p["ad"])
        except Exception: _kes += 1
    kontrol("%s yuvası kasete girmiyor (%d parça)" % (KOD, len(yuva)), _kes == 0, "%d" % _kes)
    pb_ = bb("%s__plaka_on" % mod); kontrol("%s kaseti plakalarıyla rafa oturuyor (plaka altı %.0f = raf %.0f)" % (KOD, pb_.ymin, SOGUK_TABAN), abs(pb_.ymin - SOGUK_TABAN) < 0.01)
    kl = bb("yuva_%s_kilavuz_sol" % k); kr = bb("yuva_%s_kilavuz_sag" % k)
    kontrol("%s kılavuz dudakları plakaya 0,5 mm (%.1f / %.1f)" % (KOD, Y_["px0"] - kl.xmax, kr.xmin - Y_["px1"]), abs(Y_["px0"] - kl.xmax - 0.5) < 0.01 and abs(kr.xmin - Y_["px1"] - 0.5) < 0.01)
    dl = bb("yuva_%s_mandal_dili" % k); gv = bb("yuva_%s_mandal_govdesi" % k)
    kontrol("%s mandal dili plakanın ÖNÜNDE (z %.1f ≥ plaka önü %.0f), plakayı %.1f mm örtüyor ≥ 5,5" % (KOD, dl.zmin, Y_["pz1"], dl.xmax - Y_["px0"]), dl.zmin >= Y_["pz1"] and dl.xmax - Y_["px0"] >= 5.5)
    kontrol("%s mandal kolu sola %.1f mm kayabilir ≥ 6,5 (dil plakadan çıkar)" % (KOD, dl.xmin - (gv.xmin + 2.5)), dl.xmin - (gv.xmin + 2.5) >= 6.5)
    ad_ = bb("yuva_%s_arka_dayama_sol" % k); kontrol("%s arka dayama plakanın arka yüzünde (z %.0f)" % (KOD, ad_.zmax), abs(ad_.zmax - Y_["pz0"]) < 0.01)
    hy = bb("yuva_%s_helezon_hac_yuvasi" % k); hk = bb("%s__kavrama_helezon" % mod); ty = bb("yuva_%s_helezon_yay_tablasi" % k)
    kontrol("%s haç yuvası ağzı haç çubuklarının önünde 0,5 mm, çubuklar yuvada %.1f mm" % (KOD, hy.zmax - hk.zmin), hy.zmax > hk.zmin and abs((hy.zmax - hk.zmin) - 9.5) < 0.6)
    kontrol("%s haç yuvası geri çekilebilir: yay tablasına %.1f mm ≥ 10,5 (kaset en çok 9,5 iter)" % (KOD, hy.zmin - (ty.zmin + 1.0)), hy.zmin - (ty.zmin + 1.0) >= 10.49)   # tabla plakası 1 mm; pilotlar sayılmaz
    kontrol("%s mil ucu (−545) haç kavramasının arkasında ≥ 1 mm" % KOD, hk.zmin - bb("mil_%s_helezon" % mod).zmax >= 1.0)
    # yuva parçaları birbirine ve makinenin öbür sabit parçalarına girmiyor (gerçek katı; kaset ayrı sayıldı)
    _oth = [p for p in P if not p["ad"].startswith((mod, "yuva_%s_" % k, "baglam", "kompresor", "hava_ana", "pide", "tabla_diski", "teknik_bant"))]
    _kes2 = []
    for p in yuva:
        b1 = p["sh"].BoundingBox()
        for q in yuva + _oth:
            if q is p: continue
            b2 = q["sh"].BoundingBox()
            if not (b1.xmin < b2.xmax and b2.xmin < b1.xmax and b1.ymin < b2.ymax and b2.ymin < b1.ymax and b1.zmin < b2.zmax and b2.zmin < b1.zmax): continue
            try: v_ = p["sh"].intersect(q["sh"]).Volume()
            except Exception: v_ = -1.0
            if v_ > 1.0 or v_ < 0: _kes2.append((p["ad"], q["ad"], round(v_, 1)))
    kontrol("%s yuva parçaları birbirine / makineye girmiyor (%d parça)" % (KOD, len(yuva)), not _kes2, "%s" % _kes2[:6])
kontrol("kaşar sağ kılavuzu–sucuk mandalı boşluğu %.1f ≥ 10 · kaşar plakası–sucuk plakası %.0f ≥ 30" % (bb("yuva_sucuk_mandal_govdesi").xmin - bb("yuva_kasar_kilavuz_sag").xmax, bb("sucuk_cad_v7__plaka_on").xmin - bb("kasar_cad_v14__plaka_on").xmax),
        bb("yuva_sucuk_mandal_govdesi").xmin - bb("yuva_kasar_kilavuz_sag").xmax >= 10.0 and bb("sucuk_cad_v7__plaka_on").xmin - bb("kasar_cad_v14__plaka_on").xmax >= 30.0)
kontrol("sucuk sağ kılavuzu–sağ duvar boşluğu %.1f ≥ 20" % (BAY_B[1] - bb("yuva_sucuk_kilavuz_sag").xmax), BAY_B[1] - bb("yuva_sucuk_kilavuz_sag").xmax >= 20.0)
kontrol("kuşbaşı valf topuzu–kaşar mandalı boşluğu %.0f ≥ 20" % (bb("yuva_kasar_mandal_govdesi").xmin - bb("kusbasi__valf_topuzu").xmax), bb("yuva_kasar_mandal_govdesi").xmin - bb("kusbasi__valf_topuzu").xmax >= 20.0)
for _ad, _mod, _x0, _x1 in KASET:
    _kb_ = bb("%s__cikis_tupu" % _mod); _hn_ = bb("%s_inis_hunisi" % _mod.split("_")[0])
    kontrol("%s çıkış borusu altı (%.0f) iniş hunisinin üstünde (%.0f), iç içe DEĞİL" % (_ad, _kb_.ymin, _hn_.ymax), _kb_.ymin > _hn_.ymax)
_yb = bb("yalitim_blogu"); kontrol("yalıtım tek blok, dışı düz (x %.0f…%.0f · y %.0f…%.0f · z %.0f…%.0f)" % (_yb.xmin, _yb.xmax, _yb.ymin, _yb.ymax, _yb.zmin, _yb.zmax), _yb.xmin == BAY_A[0] and _yb.xmax == BAY_B[1] and _yb.zmax == Z_KAPAK[1] and _yb.zmin == Z_BOLME[1])
_yv = [p for p in P if p["ad"].startswith(("soguk_hucre", "arka_yalitim"))]; kontrol("eski parçalı yalıtım kalktı", not _yv)
_kb = 0; _ybs = [q for q in P if q["ad"] == "yalitim_blogu"][0]["sh"]
for p in P:
    if p["ad"].startswith(("yalitim_blogu", "on_fitil", "teknik_bant", "kabin_", "baglam", "kompresor", "hava_ana")): continue
    try:
        if p["sh"].intersect(_ybs).Volume() > 1.0: _kb += 1; print("   yalıtım bloğuna giren:", p["ad"])
    except Exception: pass
kontrol("yalıtım bloğuna hiçbir parça girmiyor (kovanlar deliklerinde)", _kb == 0, "%d" % _kb)
''')
# ---- __main__: çıkış yolu taraması + v6 dosya adları ----
d('''if __name__ == "__main__":
    kal = [d for d in DEN if not d[1]]
    assert not kal, kal
    glb_yaz(os.path.join(OUT, "topping_uno_v5.glb"))
    with open(os.path.join(OUT, "topping_uno_v5.json"), "w", encoding="utf-8") as f:
        json.dump(dict(surum="topping_uno_cad_v5 · %s" % time.strftime("%d.%m.%Y %H:%M"),''',
  '''if __name__ == "__main__":
    # v6 · KASET ÇIKIŞ YOLU: kaset (mandal kalkık) 10 mm adımlarla öne çekilir; hiçbir sabit parçaya değmemeli
    for KOD in YUVA:
        k = KOD.lower(); mod = "kasar_cad_v14" if KOD == "KASAR" else "sucuk_cad_v7"
        kas = [p["sh"] for p in P if p["ad"].startswith(mod)]
        sabit = [p for p in P if not p["ad"].startswith((mod, "yuva_%s_mandal_dili" % k, "baglam", "kompresor", "hava_ana", "pide", "tabla_diski"))]
        bul = []
        for dz in range(10, 431, 10):
            kc = cq.Compound.makeCompound([q.translate(V(0, 0, dz)) for q in kas]); kb_ = kc.BoundingBox()
            for p in sabit:
                b_ = p["sh"].BoundingBox()
                if not (kb_.xmin < b_.xmax and b_.xmin < kb_.xmax and kb_.ymin < b_.ymax and b_.ymin < kb_.ymax and kb_.zmin < b_.zmax and b_.zmin < kb_.zmax): continue
                try: v_ = kc.intersect(p["sh"]).Volume()
                except Exception: v_ = -1.0
                if v_ > 1.0 or v_ < 0: bul.append((dz, p["ad"], round(v_, 1)))
        kontrol("%s kaseti öne çekilirken (0–430 mm) hiçbir parçaya değmiyor" % KOD, not bul, "%d bulgu %s" % (len(bul), bul[:6]))
    kal = [d for d in DEN if not d[1]]
    assert not kal, kal
    glb_yaz(os.path.join(OUT, "topping_uno_v6.glb"))
    with open(os.path.join(OUT, "topping_uno_v6.json"), "w", encoding="utf-8") as f:
        json.dump(dict(surum="topping_uno_cad_v6 · %s" % time.strftime("%d.%m.%Y %H:%M"),''')
d('"generator": "AUTOKITCH topping_uno_cad_v5"', '"generator": "AUTOKITCH topping_uno_cad_v6"')
io.open(os.path.join(U, "topping_uno_cad_v6.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v6.py yazildi")
