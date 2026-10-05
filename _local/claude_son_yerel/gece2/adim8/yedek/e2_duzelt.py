# -*- coding: utf-8 -*-
# ADIM 8 · E + U + TOPPING üreteçlerine saplama düzeltmesi (sonradan kaldır yöntemi) — yedekten yeniden uygular
import io, os, sys, shutil
H3 = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3"
Y = os.path.dirname(os.path.abspath(__file__))


def oku(f): return io.open(f, encoding="utf-8").read()


def yaz(f, s): io.open(f, "w", encoding="utf-8", newline="").write(s)


def rep(s, a, b):
    assert s.count(a) == 1, a[:80]
    return s.replace(a, b)


# ------------------------------------------------------------------ E
s = oku(os.path.join(Y, "h3_e_sac_v1.py"))
a = '''MEK_HARIC = re.compile(r"^(E_GOVDE|E_MODULER|K_|U_KE|U_ICECEK|ELK_ZEMIN|ZEMIN|QR)|karton|poset|E_KUTU|kablo|__hava|conta|yigin|plastik$")
'''
s = rep(s, a, a + '''# ADIM 8 (4 Eki 2026) · entegrasyonda (zincir 35, sac_ent saplama boyu denetimi) engel yüzünden çıkarılan FHP saplamalar: kur() SONUNDA
# saplama_duzelt() ile kaldırılır — saplama (ARAYÜZ) + sacdaki PEM deliği (kesik) birlikte gider, boş delik kalmaz. Sonda yapılır ki diğer saplamaların
# yer seçimi (guvenli: mevcut deliklere uzaklık) ve ad numaraları birebir aynı kalsın. Taşınamadılar: karşı parçanın tüm yüzü engelin altında / karşı parça yok.
SAPLAMA_CIKAR = {
    "arayuz_j3_burc_1476_669": "J3 üst burç · 23,5 mm'de ELK_ZINCIR etiketi (burç yeri elektrik modelinde sabit; panel alt 2 burçla tutulur)",
    "arayuz_j3_burc_1594_669": "J3 üst burç · 23,5 mm'de Harting (burç yeri elektrik modelinde sabit; panel alt 2 burçla tutulur)",
    "arayuz_mek_sol_2": "şarjör UHMW yan astarı (5 mm) · karton yığını 8 mm'de, astar yüzünün tamamı yığının arkasında",
    "arayuz_mek_sol_3": "şarjör UHMW yan astarı (5 mm) · karton yığını 8 mm'de, astar yüzünün tamamı yığının arkasında",
    "arayuz_mek_arka_19": "şarjör UHMW arka astarı (8 mm) · karton yığını 11 mm'de, astar yüzünün tamamı yığının arkasında",
    "arayuz_mek_arka_20": "şarjör UHMW arka astarı (8 mm) · karton yığını 11 mm'de, astar yüzünün tamamı yığının arkasında",
    "arayuz_mek_taban_38": "karşı parça yok (alüminyum + motor 3,4 mm'de)",
    "arayuz_mek_taban_39": "karşı parça yok (çöp kovası 4,5 mm'de)",
    "arayuz_mek_taban_40": "karşı parça yok (çöp kovası 4,5 mm'de)",
}
''')
s = rep(s, '''    P.delik(ya[0], ya[1], c["delik"], tip="pem_saplama", parca=sp["meta"]["parca"], pem_tip="FHP", kenar_min=c["kenar"], min_sac=c["min_sac"])
    g.arayuz(sp, karsi, gerek, tip_not)
    return sp
''', '''    k = P.delik(ya[0], ya[1], c["delik"], tip="pem_saplama", parca=sp["meta"]["parca"], pem_tip="FHP", kenar_min=c["kenar"], min_sac=c["min_sac"])
    g.arayuz(sp, karsi, gerek, tip_not)
    g.__dict__.setdefault("_FHP", {})[sp["ad"]] = (P, k, dict(nokta=np.asarray(nokta, float), yon=yon, karsi=karsi, gerek=gerek, dis=dis, boy=boy, tip_not=tip_not))
    return sp


def saplama_duzelt(g, cikar, tasi=None, log=print):
    """ADIM 8: cikar {ad: gerekçe} → saplama + sacdaki PEM deliği kaldırılır · tasi {ad: [(eksen, değer), ...]} → kaldırılır ve aynı duvarda yeni
    nokta(lar)a (ad, ad + 'b', …) yeniden konur (yer güvenli değilse atlanır, rapora) · fhp_arayuz'un g._FHP kaydını kullanır · kur() SONUNDA çağrılır"""
    F = getattr(g, "_FHP", {}); cik, tas = [], []
    for ad in list(cikar) + list(tasi or {}):
        if ad not in F: continue
        P, k, a = F.pop(ad)
        P.kesikler.remove(k); P.sac._gecersiz()
        g.ARAYUZ[:] = [e for e in g.ARAYUZ if e["ad"] != ad]
        if ad in cikar: cik.append((ad, cikar[ad])); continue
        for j, (eks, deg) in enumerate(tasi[ad]):
            q = a["nokta"].copy(); q[eks] = deg; yq = P.yerel(q)
            if not guvenli(P, yq[0], yq[1], kenar=12.0, delik=9.0): tas.append((ad, "yer güvenli değil %s" % np.round(q, 1).tolist())); continue
            ad_q = ad + "b" * j
            fhp_arayuz(g, P, q, a["yon"], a["karsi"], a["gerek"], dis=a["dis"], boy=a["boy"], ad=ad_q, tip_not=a["tip_not"])
            tas.append((ad_q, np.round(q, 1).tolist()))
    g.SAPLAMA_CIKAR, g.SAPLAMA_TASI = cik, tas
    log("%s · ADIM 8 saplama düzeltmesi: çıkarılan %d · taşınan %s" % (g.birim, len(cik), tas))
    return cik, tas
''')
s = rep(s, '''    mekanizma_saplamalari(g, log)
    g.doner_guncelle()''', '''    mekanizma_saplamalari(g, log)
    saplama_duzelt(g, SAPLAMA_CIKAR, log=log)                      # ADIM 8
    g.doner_guncelle()''')
yaz(os.path.join(H3, "h3_e_sac_v1.py"), s)

# ------------------------------------------------------------------ U
s = oku(os.path.join(Y, "h3_u_sac_v1.py"))
a = '''                       r"|karton|__hava|kablo|conta|yigin")
'''
s = rep(s, a, a + '''# ADIM 8 (4 Eki 2026) · entegrasyonda (zincir 36, sac_ent saplama boyu denetimi) engel yüzünden çıkarılan FHP saplamalar: kur() SONUNDA
# E.saplama_duzelt() ile kaldırılır (saplama + sacdaki PEM deliği) · diğer saplamaların yeri ve adları birebir aynı kalır.
SAPLAMA_CIKAR = {
    "arayuz_mek_ust_f_taban_sac_0": "ana pano ayak lamasının (4 mm) tamamı pano kutusunun altında (pano 4,5 mm'de)",
    "arayuz_mek_ust_f_taban_sac_1": "ana pano ayak lamasının (4 mm) tamamı pano kutusunun altında (pano 4,5 mm'de)",
    "arayuz_mek_ust_f_taban_sac_2": "ana pano ayak lamasının (4 mm) tamamı pano kutusunun altında (pano 4,5 mm'de)",
    "arayuz_mek_ust_f_taban_sac_3": "ana pano ayak lamasının (4 mm) tamamı pano kutusunun altında (pano 4,5 mm'de)",
    "arayuz_baca_flansi_2935_620": "eski v8zq baca flanşı (yalıtım 4,5 mm'de) · zincir 38'de F üreteci bacayı yeniler, flanşı U_F tavanına 8 × M6 ile kendisi bağlar",
    "arayuz_baca_flansi_3265_620": "eski v8zq baca flanşı · F üreteci 8 × M6 ile bağlar",
    "arayuz_baca_flansi_3100_505": "eski v8zq baca flanşı · F üreteci 8 × M6 ile bağlar",
    "arayuz_baca_flansi_3100_735": "eski v8zq baca flanşı · F üreteci 8 × M6 ile bağlar",
    "arayuz_j1_burc_1476_769": "J1 üst burç · 23,5 mm'de ELK_ZINCIR etiketi (burç yeri elektrik modelinde sabit; panel alt 2 burçla tutulur)",
    "arayuz_j1_burc_1594_769": "J1 üst burç · 23,5 mm'de Harting (panel alt 2 burçla tutulur)",
    "arayuz_j2_burc_1476_669": "J2 üst burç · 23,5 mm'de ELK_ZINCIR etiketi (panel alt 2 burçla tutulur)",
    "arayuz_j2_burc_1594_669": "J2 üst burç · 23,5 mm'de Harting (panel alt 2 burçla tutulur)",
    "arayuz_mek_f_ust_tavan_sac_8": "hava hortumu askısı tepe tablası 14 × 14 · ortasından askı laması iniyor (3,5 mm'de), taşınacak serbest yer yok",
    "arayuz_mek_f_ust_tavan_sac_9": "hava hortumu askısı tepe tablası 14 × 14 · ortasından askı laması iniyor (3,5 mm'de), taşınacak serbest yer yok",
    "arayuz_mek_f_ust_taban_levhasi_18": "davlumbaz taşıyıcı lamasının tamamı davlumbaz gövdesinin altında (6 mm'de)",
    "arayuz_mek_f_ust_taban_levhasi_19": "davlumbaz taşıyıcı lamasının tamamı davlumbaz gövdesinin altında (6 mm'de)",
    "arayuz_mek_f_ust_taban_levhasi_22": "davlumbaz taşıyıcı lamasının tamamı davlumbaz gövdesinin altında (6 mm'de)",
    "arayuz_mek_f_ust_taban_levhasi_23": "davlumbaz taşıyıcı lamasının tamamı davlumbaz gövdesinin altında (6 mm'de)",
}
# taşınan: fan braketi (U_F_HAVALANDIRMA__celik 70 × 34) ortasında plastik gövde (x 3343–3376) → iki uçtaki serbest banda ikiye bölünür
# (braket başka saplamayla tutulmuyordu) · (dünya ekseni, yeni değer) · aynı duvar düzlemi
SAPLAMA_TASI = {"arayuz_mek_ust_f_arka_sac_6": ((0, 3334.0), (0, 3386.0))}
''')
s = rep(s, '''    for g in (gF, gK, gFU): g.doner_guncelle()''', '''    for g in (gF, gK, gFU): E.saplama_duzelt(g, SAPLAMA_CIKAR, SAPLAMA_TASI, log=log)      # ADIM 8 (adlar birim içinde tekil)
    for g in (gF, gK, gFU): g.doner_guncelle()''')
yaz(os.path.join(H3, "h3_u_sac_v1.py"), s)

# ------------------------------------------------------------------ TOPPING (RAY_M6 = [] zaten uygulandı → yedekten yeniden)
s = oku(os.path.join(Y, "h3_topping_sac_v1.py"))
s = rep(s, '''RAY_M6 = [(1750.0, -320.0), (1750.0, -20.0), (2250.0, -320.0), (2250.0, -20.0)]
''', '''# ADIM 8 (4 Eki 2026): tabla rayı → kaide M6 (x 1750 / 2250 · z −320 / −20) KALDIRILDI — bu eksenlerde ray tabanı yok (cıvata hiçbir parçaya değmiyordu,
# zincir 37 atlıyordu). Ray tabanı A tarafında h3_a_sac_v1.RAY_M6 (4 × M6) ile bağlı. Kaide plakasında PEM SP-M6 ve gövde tabanında Ø6,6 da açılmaz.
RAY_M6 = []
# ADIM 8 · entegrasyonda (zincir 37, sac_ent saplama boyu denetimi) engel yüzünden çıkarılan FHP saplamalar: kur() SONUNDA saplama_duzelt() ile
# kaldırılır (saplama + sacdaki PEM deliği) · diğer saplamaların yeri ve adları birebir aynı kalır.
SAPLAMA_CIKAR = {
    "arayuz_j1_burc_1476_769": "J1 üst burç · 23,5 mm'de ELK_ZINCIR etiketi (burç yeri elektrik modelinde sabit; panel alt 2 burçla tutulur)",
    "arayuz_j1_burc_1594_769": "J1 üst burç · 23,5 mm'de Harting (panel alt 2 burçla tutulur)",
    "arayuz_mek_yan_sag_0": "ELK_IC kablo kanalı tabanı · kablolar 4 mm'de (kanal boyunca dolu, taşınacak yer yok)",
    "arayuz_mek_yan_sag_1": "ELK_IC kablo kanalı tabanı · kablolar 4 mm'de (kanal boyunca dolu, taşınacak yer yok)",
    "arayuz_mek_arka_19": "evaporatör ayağı 30 × 20 × 2,5 · tamamı evaporatör gövdesinin (PU + sac) altında, 4 mm'de",
    "arayuz_mek_arka_20": "evaporatör ayağı 30 × 20 × 2,5 · tamamı evaporatör gövdesinin altında, 4 mm'de",
    "arayuz_mek_arka_21": "evaporatör ayağı 30 × 20 × 2,5 · tamamı evaporatör gövdesinin altında, 4 mm'de",
    "arayuz_mek_arka_22": "evaporatör ayağı 30 × 20 × 2,5 · tamamı evaporatör gövdesinin altında, 4 mm'de",
}
''')
s = rep(s, '''    P.delik(ya[0], ya[1], c["delik"], tip="pem_saplama", parca=sp["meta"]["parca"], pem_tip="FHP", kenar_min=c["kenar"], min_sac=c["min_sac"])
    _arayuz(sp, karsi, gerek, "mekanizma")
    return sp
''', '''    k = P.delik(ya[0], ya[1], c["delik"], tip="pem_saplama", parca=sp["meta"]["parca"], pem_tip="FHP", kenar_min=c["kenar"], min_sac=c["min_sac"])
    _arayuz(sp, karsi, gerek, "mekanizma")
    _FHP[sp["ad"]] = (P, k)
    return sp


_FHP = {}


def saplama_duzelt(log=print):
    """ADIM 8: SAPLAMA_CIKAR → saplama (ARAYÜZ) + sacdaki PEM deliği kaldırılır · kur() SONUNDA (diğer saplamaların yeri / adı değişmez)"""
    cik = []
    for ad in SAPLAMA_CIKAR:
        if ad not in _FHP: continue
        P, k = _FHP.pop(ad)
        P.kesikler.remove(k); P.sac._gecersiz()
        G.ARAYUZ[:] = [e for e in G.ARAYUZ if e["ad"] != ad]
        cik.append(ad)
    G.NOT.append("ADIM 8 · çıkarılan FHP saplama (saplama + PEM deliği): %d → %s" % (len(cik), cik))
    log("TOPPING · ADIM 8 saplama düzeltmesi: çıkarılan %d" % len(cik))
    return cik
''')
s = rep(s, "kaideye 2 × M6 + tabla rayı 4 × M6 (cıvata yukarıdan, kaide plakasında PEM SP-M6).",
        "kaideye 2 × M6 (cıvata yukarıdan, kaide plakasında PEM SP-M6) · tabla rayı M6'sı ADIM 8'de kalktı (ray tabanı A'da bağlı).")
yaz(os.path.join(H3, "h3_topping_sac_v1.py"), s)
print("ok")
