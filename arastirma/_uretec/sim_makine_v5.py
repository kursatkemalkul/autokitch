# -*- coding: utf-8 -*-
"""AUTOKITCH · TOPPING SIMULASYON SAHNESI v1 (22 Eyl 2026)
Kemal: "bu tepsiye animasyon verebiliyor musun? Sagda bir pencere acalim, ordan kontrol edelim, kodunu da
test edelim. Hersey gercekmis gibi dusun — motorlar, kablolar, bir sisteme/PC'ye bagli diyelim, burdaki kod
ile yonetiyoruz. Yarin oburgun birine verirken 'bak kod bu, bu kod bunu aktif ediyor, tepsi ilerliyor, sonra
kasetin ust motorunu aktif ediyor' diyebileyim. Kasarli pide deyince tepsi kasarin altina donup x'te
hareketini kasarin dokulusune gore ayarlasin. Gercek hayattaki gibi olucak."

BU DOSYA NE YAPAR: uretim modelini (topping_cad_v10 + kasetler) alir, HAREKET EDEN paketleri AYRI GRUPLARA
bolup tek bir GLB'ye yazar; yaninda makinenin eksen/motor tanimini JSON olarak verir. Tarayicidaki
kontrol yazilimi (otonom/hat/makine_kodu.js) bu JSON'u okuyup GLB'deki gruplari gercek hiz ve devirlerle
hareket ettirir. Sim, CAD'den TURETILIR — ayri bir model degil, ayni kati.

GRUPLAR
  SABIT ................ kabin, yalitim, kovanlar, raylar, kayis zinciri, X motoru, sensorler, kaset govdeleri
  ARABA ................ x'te kayan paket (bloklar, plaka, yatak, ayar bilezigi, donus motoru, apron, kol)
  TABLA ................ arabanin icinde DONEN paket (gobek, tabla, merkezleme pimleri) · pivot: tabla ekseni
  HELEZON_<yuva> ....... kasetin dozaj mili (z ekseninde doner)
  KARISTIRICI_<yuva> ... kasetin karistirici/rotor mili (z ekseninde doner)
  TEPSI · PIDE ......... tablanin ustunde tasinan tepsi ve hamur (sim icin cizilir)
"""
import io, json, math, os, struct, sys
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, U)
import topping_cad_v21 as TC
import topping_hesap_v5 as H
from kaset_3d_v3 import Mesh, MM, MALZEME

KOK = os.path.dirname(os.path.dirname(U))
OUT = os.path.join(KOK, "otonom", "hat3d")

ARABA_P = ("kizak_blogu_", "araba_plakasi", "doner_yatak", "ayar_bilezigi", "donus_motoru", "tahrik_lokmasi",
           "siyirici_apron", "kayis_kolu", "kayis_kelepcesi_", "tabla_home_sensoru", "tabla_home_bayragi", "x_bayragi")
TABLA_P = ("tabla_gobegi", "tabla", "merkezleme_pimi_")


def modul_ofseti():
    """modul_C.glb makine koordinatlarinda yaziliyor; buradaki olculer modul-yereli.
    Farki UYDURMUYORUZ — hat_montaj'in yazdigi durum.json'dan okuyoruz."""
    with io.open(os.path.join(OUT, "durum.json"), encoding="utf-8") as f:
        d = json.load(f)
    b = [x for x in d["birim"] if x["durum"] == "GERCEK_MODUL"]
    assert len(b) == 1, "durum.json'da tek GERCEK_MODUL bekleniyordu, %d var" % len(b)
    return [b[0]["x"][0], b[0]["y"][0], 0.0]


def kur():
    import importlib
    TC.PARCALAR[:] = []; TC.modul()
    MIL_KOT = {}
    for ad, x0, x1, gen in TC.YUVA:                       # kaset mil kotlari kasetin KENDI CAD'inden
        mod = importlib.import_module(TC.KASET_CAD[ad])
        mod.PARCALAR[:] = []; mod.kap()
        MIL_KOT[ad] = dict(helezon=TC.KAS[0] + mod.CY, karistirici=TC.KAS[0] + mod.YC, x=(x0 + x1) / 2.0,
                           cap=mod.BORU_D)                        # cikis borusunun IC capi (kasetin kendi degeri)
    AGZ_Z = {}                                                    # dozaj kovaninin z merkezi — agzin gercek yeri
    for p in TC.PARCALAR:
        if p["ad"].startswith("dozaj_kovani_"):
            b = p["wp"].val().BoundingBox()
            AGZ_Z[p["ad"][len("dozaj_kovani_"):]] = (b.zmin + b.zmax) / 2.0
    AGIZ_Y = TC.AGZ[1] + H.DUSME                                  # kovanin alt ucu = urunun serbest kaldigi kot
    TB = H.S["tabla"]
    # v4: tabla artik PARK KONUMUNDA ciziliyor (acicinin alti). Sayiyi burada
    # tekrar yazmiyoruz — CAD'in cizdigi yerden okunuyor ki ikisi ayrilmasin.
    Xc, ZT = TC.XC_TABLA, TC.ZK[0] + 30.0
    ofs = modul_ofseti()

    # --- MAKINE TANIMI (kontrol yazilimi bunu okur) ---
    DEV = {"KAŞAR KABI": 42.0, "KIYMA": 14.0, "KUŞBAŞI": 13.0, "KÜP SUCUK": 8.0, "HARÇ 1": 26.0, "HARÇ 2": 26.0}
    DOZ = {"KAŞAR KABI": 100.0, "KIYMA": 160.0, "KUŞBAŞI": 145.0, "KÜP SUCUK": 70.0, "HARÇ 1": 110.0, "HARÇ 2": 80.0}
    URUN = {"KAŞAR KABI": "Kaşar", "KIYMA": "Kıyma", "KUŞBAŞI": "Kuşbaşı", "KÜP SUCUK": "Küp sucuk",
            "HARÇ 1": "Lahmacun harcı", "HARÇ 2": "Pizza sosu"}
    yuvalar = []
    for ad, x0, x1, gen in TC.YUVA:
        k = ad.replace(" ", "_")
        pmp = TC.KASET_CAD[ad].startswith("harc")
        yuvalar.append(dict(ad=ad, kod=k, urun=URUN[ad], x=MIL_KOT[ad]["x"], genislik=gen,
                            helezon_rpm=DEV[ad], doz_g=DOZ[ad], cad=TC.KASET_CAD[ad],
                            mil_helezon_y=MIL_KOT[ad]["helezon"], mil_karistirici_y=MIL_KOT[ad]["karistirici"],
                            pompa=pmp,
                            # POMPALI kasette ust mil (YC) pompa rotoru, alt mil (CY) hazne paleti.
                            # VIDALI kasette alt mil (CY) dozaj helezonu, ust mil (YC) karistirici.
                            grup_doz="KARISTIRICI" if pmp else "HELEZON",
                            grup_karis="HELEZON" if pmp else "KARISTIRICI",
                            agiz_y=AGIZ_Y, agiz_z=AGZ_Z[k], cikis_cap=MIL_KOT[ad]["cap"],
                            # dokulme hizi: debi / kesit. rho 1,05 g/cm3 [V]
                            cikis_hiz=(DOZ[ad] / 10.0 / 1.05e-3) / (3.14159 * (MIL_KOT[ad]["cap"] / 2.0) ** 2),
                            # en buyuk parca: kopruleme kurali D >= 3 x parca -> parca = D/3
                            parca_mm=MIL_KOT[ad]["cap"] / 3.0))
    tanim = dict(
        modul=dict(w=TC.W, y=TC.Y, d=TC.D, agz=list(TC.AGZ), kas=list(TC.KAS)),
        tabla=dict(cap=TB["cap"], rpm=TB["rpm"], doz_sn=TB["doz_sn"], r_dis=TB["r_dis"], r_ic=TB["r_ic"],
                   t_dis=2.5, t_ic=0.3, x_doz_hiz=TB["x_doz_hiz"], x_gecis_hiz=TB["x_gecis_hiz"],
                   # v4 · TEPSISIZ KURGU: strok iki ucta da uzadi.
                   #  -350 : ACICI — robot hamur topunu buraya birakir, konili kafa acar
                   #  1627 : BANDA AKTARMA — pidenin on kenari kopruye ciker, bant ceker
                   strok=[-350.0, 1637.0], istasyon_x=-350.0, acici_x=-350.0, aktarma_x=1637.0,
                   eksen_z=ZT, pivot=[Xc, 0.0, ZT], baslangic_x=Xc),
        x=dict(motor="NEMA23 kapalı çevrim step 1,2 N·m", tahrik="GT3 20 diş kasnak", mm_tur=60.0,
               cozunurluk_mm=0.01875, home_x=-350.0, limit=[-380.0, 1660.0]),
        donus=dict(motor="NEMA23 pancake 57×57×41 · i=1", tork_nm=0.9, gereken_nm=0.169),
        yuvalar=yuvalar,
        ofset=ofs,                                            # modul_C.glb makine koordinatlarinda
        # v4 · TEPSI YOK. Hamur dogrudan CALISMA DISKININ ustunde (disk ust yuzu y 108).
        # Top yaricapi UYDURMA DEGIL: acilmis pidenin hacminden geliyor (V = pi r^2 h).
        pide=dict(yaricap=140.0, kenar=0.0, disk_ust=108.0, ust_y=108.0 + H.HAMUR_K,
                  tepsi_k=0.0, hamur_k=H.HAMUR_K, top_r=49.0),
        acici=dict(x=-350.0, park_y=1200.0, calisma_y=1128.0, in_sn=0.8, ac_sn=3.0, kalk_sn=0.6,
                   not_="konili doner acici · olculer VARSAYIM, tedarikciden gelecek"),
        aktarma=dict(x=1637.0, bant_burun_x=1815.0, bant_y=106.0, bant_hiz=120.0),
    )
    with io.open(os.path.join(OUT, "sim_makine.json"), "w", encoding="utf-8") as f:
        json.dump(tanim, f, ensure_ascii=False, indent=1)
    print("sim_makine.json yazildi · %d yuva" % len(yuvalar))


if __name__ == "__main__":
    kur()
