# -*- coding: utf-8 -*-
import pickle, json, collections
R = pickle.load(open("m8_k123.pkl", "rb"))


def sade(r, tur, oneri):
    ist = sorted(set(m.split("/")[0] for m in r["mek"]))
    return dict(tur=tur, istasyon=",".join(ist), dugum=", ".join(r["dugumler"]), mek=list(r["mek"]),
                konum_mm=dict(x=r["x"], y=r["y"], z=r["z"]), boyut_mm=r["boyut"], parca_sayisi=r["parca_sayisi"],
                en_yakin_mm=r["en_yakin_mm"], en_yakin_parca=r["en_yakin_parca"],
                tam_modelde_degdigi=r.get("tam_modelde_degdigi"), oneri=oneri)


ONERI_K1 = {
    "TOPPING_MODUL__motor": "Tabla motoru baglanti civata/pimleri delikte bosta (0,5-1,35 mm), hicbir yere degmiyor: civata basi motor flansina oturacak sekilde uzat ya da delik capini civataya esitle.",
    "ELK_TOPPING__kanal": "Yatay kablo kanali (556 mm) 1,5 mm havada: arka saca yasla ya da klips ekle.",
    "K_BANT__aluminyum": "Bant yan profilleri PU banttan 0,9-1,1 mm ayrik, baska hicbir seye degmiyor: saseye/uc plakasina koseben ile bagla.",
    "K_ITICI__aluminyum__ITICI_ARABA": "BILINEN: K itici arabasindaki 2 aluminyum parca 4,0 mm bosta; araba plakasina 4 mm kaydir ya da ara burc ekle.",
    "E_GOVDE__sac": "E govde sag yan sac parcasi (11,5x745x389) 1,5 mm havada: komsu sac kenarina kaydir / bukumle birlestir.",
    "TEZGAH_EVYE__krom": "Evye sensorlu batarya kafasi (krom + sensor cami) govdesinden 0,58 mm ayrik: kafayi 0,6 mm govdeye yaklastir.",
    "TEZGAH_EVYE__sensor_cam": "Evye kafasi ile ayni: kafa duzelince cozulur.",
    "TEZGAH_SARF__poset": "Poset rulosu askisindan 1,0 mm havada: ruloyu aski cubuguna oturt.",
    "ELK_ANA_PANO_UF__cihaz_koyu": "Ana pano UF icinde 2x2 dar modul (7,8 mm) DIN rayina degmiyor, komsu cihaza 1,78 mm: modulleri raya oturt.",
    "TOPPING_DONER__TABLA": "Doner tabla dugumunde kucuk parca (19,8x8,2x33) 1,0 mm havada: tabla gobegine bagla (donerken de bagli kalsin).",
}
k1 = []
for r in R["tum"]:
    n0 = list(r["dugumler"])[0]
    if r["haric"]:
        k1.append(sade(r, "havada - HARIC (insan figuru, gorsel)", "Insan figuru uzuvlari ayrik; gorsel, duzeltme gerekmez."))
    else:
        k1.append(sade(r, "havada", ONERI_K1.get(n0, "parcayi komsusuna bagla")))

ONERI_K2 = {
    "ELK_ISTASYON__cihaz": "B/Elektrik kutusunun ARKA montaj saci (z -700..-698, 160x120x2) kpk etiketli; kapak gizlenince ustundeki cihaz/DIN/rakor havada. Arka sactan kpk kaldir (yalniz on kapak z -612..-610 kpk kalsin).",
    "ELK_ISTASYON__rakor": "Ayni kutu: rakorlar kpk'li saca bagli; arka sacin kpk'si kalkinca cozulur.",
    "DUZ_E_OLUK__paslanmaz": "E robot copu (E_COP sac + DUZ_E_OLUK) yalniz E on kapagina (E_GOVDE__on_seffaf, kpk) degiyor; kapak gizlenince 26,9 mm havada. Kapakla aciliyorsa kpk ekle, degilse govdeye/kaliba tasiyici braket.",
    "QR_MUSTERI_PANELI__ekran_cam": "BILINEN: QR musteri paneli (ekran cami + paslanmaz okuyucu + plastik) yalniz QR on paneline (QR_GOVDE__on_seffaf, kpk) bagli. Panel sabitse on panelden kpk kaldir; aciliyorsa musteri paneli 3 parcasina kpk ekle.",
    "QR_MUSTERI_PANELI__paslanmaz": "Musteri paneli ile ayni karar.",
    "QR_MUSTERI_PANELI__plastik": "Musteri paneli ile ayni karar.",
    "QR_HAVALANDIRMA__plastik": "QR pano havalandirma izgarasi (150x150) yalniz kpk'li panele degiyor: izgaraya kpk ekle.",
    "TEZGAH_BULASIK__ekran_cam": "Bulasik kapagindaki ekran cami kpk'siz: kpk ekle.",
    "TEZGAH_BULASIK__kulp_isik": "BILINEN: bulasik kulp isigi kapaga bagli ama kpk'siz: kpk ekle.",
    "TEZGAH_CEKMECE__celik": "Tezgah cekmece celik parcalari (kulp/ray) yalniz cekmece onune degiyor: kulpsa kpk ekle, raysa govdeye bagla (4-18 mm).",
}
k2 = [sade(r, "kapak gizli -> havada", ONERI_K2.get(list(r["dugumler"])[0], "kpk etiketini kontrol et")) for r in R["kapak_gizli"]]


def tt(t, tur, oneri):
    return dict(tur=tur, istasyon=t["istasyon"], dugum=t["dugum"], mek=t["mek"],
                konum_mm=dict(x=[float(v) for v in t["x"]], y=[float(v) for v in t["y"]], z=[float(v) for v in t["z"]]),
                boyut_mm=t["boyut"], komsular=t.get("komsular"), oneri=oneri)


ters = []
for t in R["kpk_ters"]:
    if t["dugum"] == "ELK_ISTASYON__pano" and float(t["z"][0]) in (-730.0, -700.0):
        ters.append(tt(t, "govdeye ait olup kpk'li (TERS)", "Kutunun arka montaj saci kpk'li: kpk kaldir (cihazlar bu saca bagli)."))
    else:
        ters.append(tt(t, "kpk'li, kpk komsusu yok (bilgi)", "Kapak paneli tek parca; mentese/kilit modellenmemis ya da kpk'siz. Dogruysa sorun yok."))
yalniz = [tt(t, "kpk'siz ama yalniz kapaga bagli", "kpk ekle (kapakla birlikte gizlenmeli)") for t in R["kpksiz_yalniz_kpk_degen"]]

ONERI_K3 = {
    "Elektrik": "Elektrik ana hat/ana pano kablo, kanal ve rakorlari baska istasyonun sacina bagli; Elektrik gorunumunde havada. Bilgi: ya ait oldugu istasyonun Elektrik mekanizmasina alin ya da kabul edin.",
    "F": "F/Elektrik rakoru B kasasi sacina + ana hatta bagli, firin sacina 2,5 mm: rakoru firin sacina oturt ya da etiketi Elektrik/Ana hat yap.",
    "QR": "ELK_QR_MONTAJ paslanmaz braketi QR govdesine 0,6 mm; yalniz robot kontrol kutusu / kablo koprusune degiyor: braketi 0,6 mm QR govdesine yaklastir ya da Robot/Kontrol kutusu etiketine al.",
    "TOPPING": "(1) ELK_TOPPING__celik klips yalniz KAIDE_A sacina degiyor: A/Govde etiketi ya da TOPPING sacina tasi. (2) ELK_TOPPING dikey kablo kanali (25x932) yalniz Elektrik ana hattina degiyor, TOPPING sacina 1,5 mm: kanali TOPPING arka sacina yasla.",
}
k3 = {}
for k, v in R.items():
    if k.startswith("ist:") and isinstance(v, list) and v:
        s = k[4:]
        k3[s] = [sade(r, "istasyon gorunumunde havada", ONERI_K3.get(s, "")) for r in v]
ana = {k[4:-4]: v for k, v in R.items() if k.endswith("|ana")}

pu1 = json.load(open("m8_pu.json", encoding="utf-8"))
pu05 = json.load(open("m8_pu_0.5.json", encoding="utf-8"))
k4 = dict(
    cozunurluk_1mm=dict(is_sayisi=24, bulgu_sayisi=len(pu1), not_="6 yon x kapali/acik x hat/karsi grup: 4 mm2 ustu acik PU YOK"),
    cozunurluk_05mm=dict(is_sayisi=12, bulgu=[dict(
        tur="acikta PU (ince yarik)", istasyon="TOPPING", dugum=r["dugum"], durum="kapaklar acik (kpk gizli)", yon=r["yon"],
        konum_mm=dict(x=r["u"], y=r["v"], z=r["derinlik"]), alan_mm2=r["alan_mm2"],
        oneri="TOPPING on PU yuzu (z 20) 63 mm x <=0,5 mm yariktan gorunuyor (y 1142,5-1143): komsu sac kenarini 0,5 mm uzat ya da PU on yuzunu 1 mm geri cek.") for r in pu05]))

derz = json.load(open("m8_derz.json", encoding="utf-8"))
grp = collections.defaultdict(list)
for d in derz:
    grp[(d["tur"], d["a"]["dugum"], d["b"]["dugum"], d["aralik_mm"])].append(d["nokta"])
k5 = [dict(tur=tur, aralik_mm=g, a=a, b=b, adet=len(p), noktalar=p[:6]) for (tur, a, b, g), p in sorted(grp.items(), key=lambda x: (x[0][0], x[0][3]))]

OUT = dict(model="hat3_v8x.glb", tarih="2026-10-03", yontem=dict(
    temas="dugum ici bagli bilesen + (mek,kpk) etiketi = PARCA (4432); kose->ucgen kesin uzaklik <=0,5 mm; havada gorunen kumelerde kenar ornegi 0,7 mm ile ikinci tur; tam dunya donusumu (TRS + hiyerarsi; olcek 0,0001 urunler gizli sayildi)",
    topraklama="kume y_alt <= 1 mm olmali; istasyon gorunumunde en buyuk kume = istasyon govdesi (A/F/K/TOPPING/U modulleri tasarim geregi 788/1862'de baska modulun ustunde)",
    pu="ortografik z-tampon raster 1 mm (24 is) + 0,5 mm (hat grubu, 12 is); kapali = on_seffaf opak, acik = kpk gizli; cam saydam; ZEMIN/INSAN/ROBOT/URUN ortmez",
    derz="GOVDE kat. sac malzemeleri (sac/paslanmaz/on_seffaf/kabuk/qr_govde/on_cerceve); hic degmeyen ciftlerin en yakin uzakligi 0,2-15 mm"),
    k1_havada=k1, k2_kapak_gizli=dict(havada=k2, kpk_ters=ters, kpksiz_yalniz_kapaga_bagli=yalniz),
    k3_istasyon=dict(havada=k3, ana_govde=ana), k4_pu=k4, k5_derz=k5)
json.dump(OUT, open("havada_pu_kapak.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(k1), len(k2), len(ters), len(yalniz), sum(len(v) for v in k3.values()), len(k5))
print(collections.Counter(x["tur"] for x in k5))
for x in k5:
    if x["tur"].startswith("ayn"):
        print(x["aralik_mm"], x["adet"], x["a"], "|", x["b"], x["noktalar"][:2])
