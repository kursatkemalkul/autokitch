# -*- coding: utf-8 -*-
"""AUTOKITCH · TOPPING v2 (UNO'lu) SİMÜLASYON TANIMI v7 (25 Eyl 2026) → otonom/hat3d/sim_makine_v7.json

Kemal: "toppingi de tam hesapla ... sağda da panel yap, seçim yapınca çalışmaya başlasın; diğer kasetler, UNO'lar için de yap;
karışıkta seçebileyim."

Tarayıcıdaki kontrol yazılımı (otonom/hat/makine_kodu_v2.js) bu dosyayı okur; tek sayı elle yazılmaz:
  · dozaj hesabı ............ topping_v2_hesap_v1 (reçeteler, yoğunluk, UNO strokları, tabla devri, yarık profili, spiral yasası)
  · döner grup pivotları .... topping_uno_cad_v5 → topping_uno_v5.json "grup" (UNO pistonu/valfi, kaset helezonu/karıştırıcısı)
  · tabla / açıcı / bant .... topping_cad_v22 + topping_hesap_v6 (v1 simülasyonundaki değerler)
ÇERÇEVE: modül C yereli — x modülün sol ucundan, y İSTASYON TABANINDAN (1060), z ön yüzden. Sahne +ofset ile hatta taşır
(ofset hat_montaj'ın yazdığı durum.json'dan okunur: TOPPING_MODUL x0, y0).
"""
import io, json, os, sys

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
OUT = os.path.join(KOK, "otonom", "hat3d")
import topping_v2_hesap_v1 as TH2
import topping_hesap_v6 as H
import topping_cad_v22 as TC

Y0 = 1060.0
RENK = {"SOS": "0xc0392b", "HARC": "0xa8402f", "KIYMA": "0x9c4a3a", "KUSBASI": "0x8c3f34", "KASAR": "0xf2d98a", "SUCUK": "0x8f2f2f"}


def ofset():
    with io.open(os.path.join(OUT, "durum.json"), encoding="utf-8") as f:
        d = json.load(f)
    b = [x for x in d["birim"] if x["durum"] == "GERCEK_MODUL"]
    assert len(b) == 1
    return [b[0]["x"][0], b[0]["y"][0], 0.0]


def kur():
    G = json.load(io.open(os.path.join(OUT, "topping_uno_v5.json"), encoding="utf-8"))["grup"]
    yer = lambda p: [p[0], p[1] - Y0, p[2]]
    ist = []
    for i in TH2.IST:
        k = i["kod"]
        e = dict(kod=k, ad=i["ad"], tip=i["tip"], x=i["x"], renk=RENK[k], taraf=TH2.TARAF.get(k, 0))
        if i["tip"] in ("YAYICI", "NOKTA"):
            e.update(sil=i["sil"], strok_max=TH2.STROK_MAX[i["sil"]], grup_piston="PISTON_" + k, grup_valf="VALF_" + k,
                     piston=yer(G["PISTON_" + k]), valf=yer(G["VALF_" + k]))
        if i["tip"] == "YAYICI":
            e.update(bar_r=list(TH2.YARIK_R), bar_alt=TH2.PIDE_UST + TH2.BICAK_YUKSEK - Y0, agiz_z=TH2.ZT,
                     yarik=[[r, TH2.yarik_genisligi(k, r)] for r in (10.0, 30.0, 60.0, 90.0, 121.0)], parca_mm=6.0)
        else:
            e.update(ic=i["ic"], agiz_y=TH2.AGIZ_Y_NOKTA - Y0, agiz_z=TH2.AGIZ_Z[i["tip"]], parca_mm=round(i["ic"] / TH2.KOPRU, 1))
        if i["tip"] == "KASET":
            e.update(g_tur=i["g_tur"], rpm=i["rpm"], grup_helezon="HELEZON_" + k, grup_karis="KARISTIRICI_" + k,
                     helezon=yer(G["HELEZON_" + k]), karis=yer(G["KARISTIRICI_" + k]))
        ist.append(e)
    O = TH2.ozet()
    tanim = dict(
        surum="sim_makine_v7 · TOPPING v2 (UNO'lu) · topping_uno_cad_v5 · topping_v2_hesap_v1",
        ofset=ofset(),
        hesap=dict(pide_r=TH2.PIDE_R, r_kap=TH2.R_KAP, a_kap=TH2.A_KAP, pide_ust=TH2.PIDE_UST - Y0, yog=TH2.YOG, rpm_yayici=TH2.RPM_YAYICI,
                   rampa_sn=TH2.RAMPA_SN, rpm_nokta=TH2.RPM_NOKTA, r_ic=TH2.R_IC, serit=TH2.SERIT, tur_uno=TH2.TUR_UNO, hava_sil=TH2.HAVA_SIL,
                   hava_bar=TH2.HAVA_BAR, valf_sn=TH2.VALF_SN, kesme_valf_sn=TH2.KESME_VALF_SN, piston_min=TH2.PISTON_MIN_HIZ, akis_n=TH2.AKIS_N),
        istasyon=ist,
        recete={k: dict(ad=v["ad"], doz=v["doz"], kaynak=v["kaynak"]) for k, v in TH2.RECETE.items()},
        karisik=dict(et=TH2.KARISIK_ET, kasar=list(TH2.KARISIK_KASAR), sos=TH2.KARISIK_SOS,
                     kural="seçilen etler tek porsiyonu paylaşır (her biri dozunun 1/n'i) · kaşar etle 90 g, yalnız 130 g · sos 80 g [V — Kemal onayına]"),
        kontrol={k: dict(sure=round(u["sure"], 2), sira=u["sira"], hesap={s: {a: (round(b, 3) if isinstance(b, float) else b) for a, b in h.items() if not isinstance(b, list)} for s, h in u["hesap"].items()})
                 for k, u in O["urun"].items()},
        tabla=dict(cap=340.0, eksen_z=TC.ZK[0] + 30.0, pivot=[TC.XC_TABLA, 0.0, TC.ZK[0] + 30.0], baslangic_x=TC.XC_TABLA,
                   x_gecis_hiz=TH2.X_HIZ, rampa_x=TH2.RAMPA_X, acici_x=H.X_PARK, aktarma_x=H.X_AKTARMA),
        x=dict(motor="NEMA23 kapalı çevrim step 1,2 N·m", tahrik="GT3 20 diş kasnak", mm_tur=60.0, cozunurluk_mm=0.01875,
               home_x=H.X_PARK, limit=[H.X_LIMIT_SOL, H.X_LIMIT_SAG]),
        pide=dict(yaricap=140.0, disk_ust=108.0, ust_y=108.0 + H.HAMUR_K, hamur_k=H.HAMUR_K, top_r=49.0),
        acici=dict(x=H.X_PARK, tepe_y=116.0, boy=140.0, taban_r=45.0, yarim_aci=17.82, kalkis=60.0, in_sn=0.8, ac_sn=3.0, kalk_sn=0.6,
                   koni_rpm=round(35.0 / __import__("math").sin(__import__("math").radians(17.82)), 1)),
        aktarma=dict(x=H.X_AKTARMA, bant_burun_x=1815.0, bant_son_x=2195.0, bant_y=106.0, bant_hiz=120.0, burun_r=10.0, tahrik_r=30.0),
    )
    with io.open(os.path.join(OUT, "sim_makine_v7.json"), "w", encoding="utf-8") as f:
        json.dump(tanim, f, ensure_ascii=False, indent=1)
    print("sim_makine_v7.json yazildi · %d istasyon · %d recete · ofset %s" % (len(ist), len(tanim["recete"]), tanim["ofset"]))


if __name__ == "__main__":
    kur(); sys.stdout.flush(); os._exit(0)
