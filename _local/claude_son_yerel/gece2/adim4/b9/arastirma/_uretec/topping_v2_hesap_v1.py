# -*- coding: utf-8 -*-
"""AUTOKITCH · TOPPING v2 (UNO'lu) — DOZAJ HESABI v1 (25 Eyl 2026)

Kemal: "toppingi de tam hesapla: pizza gelip sos geniş ağızlının altına geliyor — o ne kadar dökecek, alt tabla ne kadar
dönecek; sağda da panel yap, seçim yapınca çalışmaya başlasın; diğer kasetler, UNO'lar için de yap; karışıkta seçebileyim."

TEK KAYNAK: model (topping_uno_cad_v5 → yayıcı yarık profili) ve simülasyon (sim_makine_v7 → makine_kodu_v2.js) sayıları
BURADAN okur; hiçbir sayı iki yerde yazılmaz. [K] kaynaklı · [H] hesap · [V] varsayım (pilotta ölçülecek).

ÜÇ DOZAJ TİPİ
  YAYICI  (SOS, HARÇ)          UNO + Beldos spreader: yarıklı boru tabla ekseninde, merkezden kenara. Tabla ağzın iç ucunu
                               merkeze getirir, x'te durur, TAM 1 TUR döner; piston o 1 turda strokunu bitirir.
  NOKTA   (KIYMA, KUŞBAŞI)     UNO + yuvarlak ağız (iç Ø33, pideden 40 mm). Tabla 35 dev/dk döner, araba x'te kayar,
                               ağız pide üstünde spiral çizer (eşit alan yasası: r² zamanla doğrusal).
  KASET   (KAŞAR, KÜP SUCUK)   bizim kaset (helezon sabit devirde) + iniş borusu; yasa NOKTA ile aynı.
"""
import json, math

PI = math.pi

# ---------------------------------------------------------------- 1 · ÜRÜN, ALAN, YOĞUNLUK ----------------------------------------------------------------
PIDE_R = 140.0                    # açıcının açtığı hamur Ø280 [K: sim_makine · açıcı]
KENAR = 15.0                      # dozlanmayan kenar [K: topping_uno_cad_v4 BICAK notu "sos kenarı 15 mm boş"]
R_KAP = PIDE_R - KENAR            # 125 · kaplanan yarıçap
A_KAP = PI * R_KAP ** 2           # 49 087 mm²
PIDE_UST = 1176.0                 # pide üst yüzü (yerden) [K: topping_uno_cad_v4 PIDE_UST · disk 1168 + hamur 8]

# yoğunluk g/ml — UNO pistonu HACİM iter; gram → ml buradan
YOG = {"SOS": 1.05,               # [V] domates bazlı pizza sosu
       "HARC": 110.0 / 105.0,     # [K: topping_uno_cad_v4 · 110 g harç ≈ 105 ml]
       "KIYMA": 160.0 / 152.0,    # [K: topping_uno_cad_v4 · 160 g ≈ 152 ml]
       "KUSBASI": 145.0 / 170.0,  # [K: topping_uno_cad_v4 · 145 g ≈ 170 ml, silindirde parça arası boşluk dahil]
       "KASAR": 0.40,             # [K: hazne hesabı 14 Eyl · rende kaşar yığın yoğunluğu]
       "SUCUK": 0.59}             # [K: hazne hesabı 14 Eyl · küp sucuk yığın yoğunluğu]

# ---------------------------------------------------------------- 2 · REÇETELER (gram) ----------------------------------------------------------------
# Kemal'in stok kurgusu (14 Eyl, teknik_atosa_modul_v3 HEDEF): 80 pide = 20 kıymalı (160 g) + 20 kuşbaşılı (145 g)
# + 20 kaşarlı (130 g) + 20 sucuklu (70 g sucuk + 90 g kaşar) · 200 lahmacun × 110 g harç.
# Pizza adedi belirsiz (kural kitabı 2.1); pizza dozları sim v1'den [V].
RECETE = {
    "pizza":     dict(ad="Pizza",           doz={"SOS": 80.0, "KASAR": 100.0, "SUCUK": 70.0}, kaynak="V · sim v1"),
    "lahmacun":  dict(ad="Lahmacun",        doz={"HARC": 110.0}, kaynak="K · stok 14 Eyl"),
    "kasarli":   dict(ad="Kaşarlı pide",    doz={"KASAR": 130.0}, kaynak="K · stok 14 Eyl"),
    "kiymali":   dict(ad="Kıymalı pide",    doz={"KIYMA": 160.0}, kaynak="K · stok 14 Eyl"),
    "kusbasili": dict(ad="Kuşbaşılı pide",  doz={"KUSBASI": 145.0}, kaynak="K · stok 14 Eyl"),
    "sucuklu":   dict(ad="Sucuklu pide",    doz={"KASAR": 90.0, "SUCUK": 70.0}, kaynak="K · stok 14 Eyl"),
}
# KARIŞIK (Kemal seçer): seçilen ETLER tek porsiyonu paylaşır (her biri kendi dozunun 1/n'i); kaşar etle 90, tek başına 130;
# sos seçilirse 80 (pizza tabanı). Harç karışığa girmez: lahmacun ayrı ürün. [V — Kemal'in onayına]
KARISIK_ET = {"KIYMA": 160.0, "KUSBASI": 145.0, "SUCUK": 70.0}
KARISIK_KASAR = (130.0, 90.0)
KARISIK_SOS = 80.0


def karisik_doz(secim):
    """secim: {'SOS','KIYMA','KUSBASI','KASAR','SUCUK'} alt kümesi → {istasyon: gram}"""
    et = [k for k in KARISIK_ET if k in secim]
    d = {}
    if "SOS" in secim: d["SOS"] = KARISIK_SOS
    for k in et: d[k] = round(KARISIK_ET[k] / len(et), 1)
    if "KASAR" in secim: d["KASAR"] = KARISIK_KASAR[1] if et else KARISIK_KASAR[0]
    return d


# ---------------------------------------------------------------- 3 · İSTASYONLAR (modül C yereli x, yerden y) ----------------------------------------------------------------
# x'ler topping_uno_cad_v4'ten (UNO çekirdeği ve kaset yuvası merkezleri) [K]
IST = [
    dict(kod="SOS",     ad="Pizza sosu",      tip="YAYICI", x=210.0,  sil=52.0),
    dict(kod="HARC",    ad="Lahmacun harcı",  tip="YAYICI", x=560.0,  sil=52.0),
    dict(kod="KIYMA",   ad="Kıyma",           tip="NOKTA",  x=895.0,  sil=70.0, ic=33.0),
    dict(kod="KUSBASI", ad="Kuşbaşı",         tip="NOKTA",  x=1105.0, sil=70.0, ic=33.0),
    dict(kod="KASAR",   ad="Kaşar (rende)",   tip="KASET",  x=1361.0, ic=45.0, g_tur=100.0 / (42.0 / 60.0 * 10.0), rpm=42.0),
    dict(kod="SUCUK",   ad="Küp sucuk",       tip="KASET",  x=1593.0, ic=42.0, g_tur=70.0 / (8.0 / 60.0 * 10.0), rpm=8.0),
]
# kaset g/tur: sim v1 (kaşar 100 g / 10 s / 42 dev/dk · sucuk 70 g / 10 s / 8 dev/dk) — kaset akış modellerinden [K]
AGIZ_Y_NOKTA = 1216.0             # yuvarlak ağız ucu ve kaset iniş borusu ucu: pideden 40 mm [K: topping_uno_cad_v4]
AGIZ_Z = {"NOKTA": -170.0, "KASET": -150.0}   # UNO ağzı tabla ekseninde, kaset borusu 20 mm önde [K]
ZT = -170.0

# ---------------------------------------------------------------- 4 · UNO (Beldos Beltop UNO çekirdeği) ----------------------------------------------------------------
HAVA_SIL = 32.0                   # UNO pnömatik silindiri Ø32 [K: beldos_cad_v1 · hava tüketiminden]
HAVA_BAR = 6.0                    # şartlandırıcı çıkışı [V]
STROK_MAX = {52.0: 71.1, 70.0: 71.5}   # Ø52 151 ml → 71,1 · Ø70 275 ml → 71,5 [K: Beldos broşürü · beldos_cad_v1]
VALF_SN = 0.20                    # döner valf (emiş ↔ ağız) çevirme süresi [V]
KESME_VALF_SN = 0.05              # yayıcı kesme valfi açma/kapama [V]
PISTON_MIN_HIZ = 10.0             # standart pnömatik silindirde takılma-kaymasız en düşük hız, mm/s [V: genel katalog bilgisi]


def uno(kod, sil, gram):
    A = PI / 4.0 * sil ** 2
    ml = gram / YOG[kod]
    s = ml * 1000.0 / A
    F = HAVA_BAR * 0.1 * PI / 4.0 * HAVA_SIL ** 2          # N
    return dict(ml=ml, alan=A, strok=s, strok_orani=s / STROK_MAX[sil], hava_N=F, urun_bar=F / A * 10.0)


# ---------------------------------------------------------------- 5 · YAYICI (sos, harç) ----------------------------------------------------------------
RPM_YAYICI = 30.0                 # 1 tur = 2,0 s [H: kenar ivmesi aşağıda, ≤ 0,2 g]
RAMPA_SN = 0.25                   # tabla hızlanır/yavaşlar — valf KAPALI, ürün akmaz [V]
YARIK_R = (10.0, 121.0)           # yarığın açık olduğu yarıçap aralığı (boru 133, iki uçta tapa payı) [K: topping_uno_cad_v4]
AKIS_N = 0.30                     # akış davranış indeksi (power-law) — domates sosu / et harcı 0,2–0,4 [V: pilotta ölçülecek]
YARIK_MIN = {"SOS": 2.0, "HARC": 6.0}   # yarığın merkezdeki genişliği: sos 2 mm · harçta 5 mm parça geçmeli → 6 [V]
BICAK_YUKSEK = 6.0                # yayıcı borunun altı pideden 6 mm yukarıda [K: topping_uno_cad_v4]


def yarik_genisligi(kod, r):
    """KAPLAMA DÜZGÜN OLSUN DİYE: dönen tablada r yarıçapındaki halka turda 2πr·dr alan geçirir → borunun birim boyundan
    çıkan debi r ile ORANTILI olmalı (q ∝ r). Yarık akışı q ∝ w^(2+1/n) (power-law akışkan) → w ∝ r^(1/(2+1/n))."""
    r = max(YARIK_R[0], r)
    return YARIK_MIN[kod] * (r / YARIK_R[0]) ** (1.0 / (2.0 + 1.0 / AKIS_N))


def yayici(kod, gram, sil=52.0):
    u = uno(kod, sil, gram)
    T = 60.0 / RPM_YAYICI                                   # dozaj = 1 tam tur
    w = 2 * PI * RPM_YAYICI / 60.0
    return dict(u, sure=T, tur=1.0, aci=360.0, rampa_aci=2 * 0.5 * RAMPA_SN * 360.0 / T,   # ramplarda dönülen (valf kapalı)
                debi=u["ml"] / T, piston_hiz=u["strok"] / T, katman=u["ml"] * 1000.0 / A_KAP,
                kenar_ivme_g=w * w * PIDE_R / 1000.0 / 9.81,
                yarik=[(r, yarik_genisligi(kod, r)) for r in (10.0, 20.0, 40.0, 60.0, 80.0, 100.0, 121.0)],
                duz_yarik_oran=R_KAP / YARIK_R[0])          # düz yarıkla merkez / kenar kalınlık oranı (h ∝ 1/r)


# ---------------------------------------------------------------- 6 · NOKTA AĞIZ + KASET (spiral) ----------------------------------------------------------------
RPM_NOKTA = 35.0                  # [K: sucuk_v2_hesap · r 125'te küp sucuğun kaymaması için μ ≥ 0,17]
R_IC = 20.0                       # spiral bu yarıçapta biter: kaset borusu tabla ekseninin 20 mm önünde → tam üstü [K: v1]
SERIT = 0.80                      # ürün şeridi genişliği = ağız iç çapı × 0,8 [V]
TUR_UNO = 6.0                     # UNO nokta ağızda spiral tur sayısı [H: seyrek merkez r ≤ 40]
KOPRU = 3.0                       # köprüleme kuralı: ağız ≥ 3 × parça [K: v1 sim_makine · kaset hesapları]


def spiral(ist, gram):
    b = SERIT * ist["ic"]
    r_dis = R_KAP - b / 2.0
    if ist["tip"] == "NOKTA":
        N = TUR_UNO
        T = N / RPM_NOKTA * 60.0
        u = uno(ist["kod"], ist["sil"], gram)
        ml = u["ml"]
    else:
        T = gram / (ist["g_tur"] * ist["rpm"] / 60.0)             # helezon kendi devrinde, süre dozdan çıkar
        N = T * RPM_NOKTA / 60.0
        u = {}
        ml = gram / YOG[ist["kod"]]
    C = (r_dis ** 2 - R_IC ** 2) / (2.0 * N)                      # hatve p(r) = C / r
    w = 2 * PI * RPM_NOKTA / 60.0
    d = dict(u, sure=T, tur=N, aci=N * 360.0, r_dis=r_dis, r_ic=R_IC, serit=b,
             hatve_dis=C / r_dis, hatve_ic=C / R_IC, seyrek_r=C / b,          # r < seyrek_r'de şeritler birbirine değmez
             debi=ml / T, katman=ml * 1000.0 / A_KAP, cikis_hiz=ml * 1000.0 / T / (PI / 4 * ist["ic"] ** 2),
             parca_max=ist["ic"] / KOPRU, kenar_ivme_g=w * w * R_KAP / 1000.0 / 9.81,
             yuzey_hiz_dis=w * r_dis, x_hiz_max=(r_dis ** 2 - R_IC ** 2) / T / (2 * R_IC))
    if ist["tip"] == "NOKTA":
        d["piston_hiz"] = u["strok"] / T
    else:
        d["helezon_rpm"] = ist["rpm"]; d["helezon_tur"] = ist["rpm"] * T / 60.0
    return d


def r_yasa(d, t):
    """spiral: r² zamanla doğrusal (eşit alan hızı) — dıştan içe"""
    u = min(1.0, max(0.0, t / d["sure"]))
    return math.sqrt(d["r_dis"] ** 2 + (d["r_ic"] ** 2 - d["r_dis"] ** 2) * u)


# ---------------------------------------------------------------- 7 · TARAF + ENGEL DENETİMİ ----------------------------------------------------------------
# Tabla ağzın solunda (−1) ya da sağında (+1) durabilir. Dökülen ürün tabla dönerken YAYICI BORULARIN (pideden 6 mm)
# altına girmemeli. Kıymada sol tarafta pidenin kenarı harç borusunun altına giriyor (kıyma şeridi ~4–7 mm) → SAĞ.
TARAF = {"KIYMA": 1, "KUSBASI": -1, "KASAR": -1, "SUCUK": -1}
BORU_X = {k: (i["x"] - 8.0 - 6.0, i["x"] + 125.0 + 10.0) for k, i in ((j["kod"], j) for j in IST) if i["tip"] == "YAYICI"}   # tapalar dahil


def tabla_x(ist, r):
    dz = 0.0 if ist["tip"] == "NOKTA" else abs(AGIZ_Z["KASET"] - ZT)
    return ist["x"] + TARAF[ist["kod"]] * math.sqrt(max(0.0, r * r - dz * dz))


def engel_denetimi():
    """her nokta istasyonu için: dozaj boyunca pidenin dökülen halkası (merkez ± 125) yayıcı boruların x aralığına girmesin"""
    sonuc = []
    for ist in IST:
        if ist["tip"] == "YAYICI":
            continue
        d = spiral(ist, 100.0)
        xs = [tabla_x(ist, r_yasa(d, d["sure"] * i / 50.0)) for i in range(51)]
        lo, hi = min(xs) - R_KAP, max(xs) + R_KAP
        for kod, (b0, b1) in BORU_X.items():
            cak = lo < b1 and b0 < hi
            sonuc.append((ist["kod"], kod, lo, hi, b0, b1, not cak))
    return sonuc


# ---------------------------------------------------------------- 8 · ÇEVRİM SÜRESİ (araba + tabla) ----------------------------------------------------------------
X_PARK, X_AKTARMA = -350.0, 1637.0     # açıcının altı · banda aktarma [K: topping_hesap_v6]
X_HIZ = 200.0                          # x geçiş hızı mm/s [K: topping_hesap_v6]
RAMPA_X = 0.3                          # [K: makine_kodu.js rampali()]
ACICI_SN = 0.8 + 3.0 + 0.6             # in + aç + kalk [K: sim_makine]
AKTARMA_SN = 2.0                       # pide banda geçer [V: v1 sim ölçümü ~2 s]


def gecis(x0, x1):
    return abs(x1 - x0) / X_HIZ + RAMPA_X


def cevrim(doz):
    """doz: {istasyon: gram} → sıralı adımlar + toplam süre (tabla açıcıdan çıkar → aktarır → açıcıya döner)"""
    sira = sorted(doz, key=lambda k: [i["x"] for i in IST if i["kod"] == k][0])
    ad = []; x = X_PARK; t = ACICI_SN
    ad.append(("AÇICI", ACICI_SN))
    for k in sira:
        ist = [i for i in IST if i["kod"] == k][0]
        if ist["tip"] == "YAYICI":
            d = yayici(k, doz[k]); x0 = ist["x"]
            t_g = gecis(x, x0); t_d = VALF_SN + 2 * RAMPA_SN + d["sure"] + KESME_VALF_SN; x = x0
        else:
            d = spiral(ist, doz[k]); x0 = tabla_x(ist, d["r_dis"])
            t_g = gecis(x, x0); t_d = (VALF_SN if ist["tip"] == "NOKTA" else 0.0) + d["sure"] + 0.35; x = tabla_x(ist, d["r_ic"])
        ad.append(("→ " + k, t_g)); ad.append((k, t_d)); t += t_g + t_d
    t_a = gecis(x, X_AKTARMA) + AKTARMA_SN; t_d = gecis(X_AKTARMA, X_PARK)
    ad += [("→ AKTARMA", t_a), ("→ AÇICI (dönüş)", t_d)]
    t += t_a + t_d
    return sira, ad, t


# ---------------------------------------------------------------- 9 · ÖZET (sim_makine_v7 ve sayfa bunu okur) ----------------------------------------------------------------
def istasyon_hesabi(kod, gram):
    ist = [i for i in IST if i["kod"] == kod][0]
    return yayici(kod, gram, ist["sil"]) if ist["tip"] == "YAYICI" else spiral(ist, gram)


def ozet():
    out = dict(pide_r=PIDE_R, kenar=KENAR, r_kap=R_KAP, a_kap=A_KAP, rpm_yayici=RPM_YAYICI, rpm_nokta=RPM_NOKTA,
               rampa_sn=RAMPA_SN, valf_sn=VALF_SN, kesme_valf_sn=KESME_VALF_SN, akis_n=AKIS_N, yarik_r=list(YARIK_R),
               yarik_min=YARIK_MIN, bicak_yuksek=BICAK_YUKSEK, serit=SERIT, tur_uno=TUR_UNO, r_ic=R_IC, taraf=TARAF,
               yog=YOG, karisik=dict(et=KARISIK_ET, kasar=list(KARISIK_KASAR), sos=KARISIK_SOS),
               recete={k: dict(ad=v["ad"], doz=v["doz"], kaynak=v["kaynak"]) for k, v in RECETE.items()},
               istasyon=[], urun={})
    for ist in IST:
        g = {"SOS": 80.0, "HARC": 110.0, "KIYMA": 160.0, "KUSBASI": 145.0, "KASAR": 130.0, "SUCUK": 70.0}[ist["kod"]]
        out["istasyon"].append(dict(ist, ornek_g=g, hesap=istasyon_hesabi(ist["kod"], g)))
    for k, r in RECETE.items():
        sira, ad, t = cevrim(r["doz"])
        out["urun"][k] = dict(sira=sira, adim=ad, sure=t, saat=3600.0 / t,
                              hesap={s: istasyon_hesabi(s, r["doz"][s]) for s in sira})
    return out


if __name__ == "__main__":
    O = ozet()
    print("TOPPING v2 DOZAJ HESABI v1 — kaplanan alan Ø%.0f = %.0f mm² (kenar %.0f boş)" % (2 * R_KAP, A_KAP, KENAR))
    for i in O["istasyon"]:
        h = i["hesap"]
        if i["tip"] == "YAYICI":
            print("  %-8s YAYICI %5.0f g = %5.1f ml · Ø%.0f strok %.1f mm (%%%.0f) · 1 tur %.1f s @ %.0f dev/dk · piston %.1f mm/s · debi %.1f ml/s · katman %.2f mm"
                  % (i["kod"], i["ornek_g"], h["ml"], i["sil"], h["strok"], 100 * h["strok_orani"], h["sure"], RPM_YAYICI, h["piston_hiz"], h["debi"], h["katman"]))
            print("           yarık (r → w): " + " · ".join("%.0f→%.2f" % rw for rw in h["yarik"]) + "  · düz yarıkla merkez/kenar kalınlık %.1f kat" % h["duz_yarik_oran"])
        else:
            print("  %-8s %-6s %5.0f g · %4.1f s · %.2f tur (%.0f°) · şerit %.1f · hatve dış %.1f / iç %.1f · seyrek r < %.0f · katman %.2f mm · parça ≤ %.1f mm%s"
                  % (i["kod"], i["tip"], i["ornek_g"], h["sure"], h["tur"], h["aci"], h["serit"], h["hatve_dis"], h["hatve_ic"], h["seyrek_r"], h["katman"], h["parca_max"],
                     (" · piston %.2f mm/s (strok %.1f)" % (h["piston_hiz"], h["strok"])) if "piston_hiz" in h else (" · helezon %.0f dev/dk %.1f tur" % (h["helezon_rpm"], h["helezon_tur"]))))
    print("KENAR İVMESİ: yayıcı %.2f g · nokta %.2f g (küp sucuk için μ ≥ %.2f yeter)" % (O["istasyon"][0]["hesap"]["kenar_ivme_g"], O["istasyon"][2]["hesap"]["kenar_ivme_g"], O["istasyon"][2]["hesap"]["kenar_ivme_g"]))
    print("ENGEL DENETİMİ (dökülen halka ↔ yayıcı borular, 6 mm):")
    for a, b, lo, hi, b0, b1, ok in engel_denetimi():
        print("  %-8s ↔ %-5s boru  pide %.0f…%.0f · boru %.0f…%.0f  %s" % (a, b, lo, hi, b0, b1, "GEÇTİ" if ok else "** ÇAKIŞIR **"))
    assert all(x[-1] for x in engel_denetimi())
    for k, u in O["urun"].items():
        print("  %-15s %5.1f s · saatte %3.0f · %s" % (RECETE[k]["ad"], u["sure"], u["saat"], " · ".join("%s %.1f" % (a, t) for a, t in u["adim"])))
    print("KARIŞIK örnek (kıyma + kuşbaşı + kaşar + sucuk):", karisik_doz({"KIYMA", "KUSBASI", "KASAR", "SUCUK"}))
    for kod in ("KIYMA", "KUSBASI"):
        h = istasyon_hesabi(kod, 160.0 if kod == "KIYMA" else 145.0)
        if h["piston_hiz"] < PISTON_MIN_HIZ:
            print("  UYARI %s: piston %.1f mm/s < %.0f mm/s — pnömatikte takılma-kayma riski (pilot; gerekirse servo sürüm)" % (kod, h["piston_hiz"], PISTON_MIN_HIZ))
