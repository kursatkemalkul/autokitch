# -*- coding: utf-8 -*-
"""Adim 7 servis erisimi: parca_kutulari.json (v8zq duzeyi) uzerinden
her servis parcasi icin on yuzden derinlik + onunu kapatan parcalar. SALT OKUMA."""
import json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat3d\v3\parca_kutulari.json"
d = json.load(open(PK, encoding="utf-8"))
P = []
for b, L in d["parca"].items():
    for r in L:
        P.append((b, r[0], r[2:8]))
ON = 59.0   # on kapak ic yuzu (kapak 59..79)
# gozardi: kabuk/kapak/kaplama/zarf/kablo/kanal (sokulmeyen ya da esnek)
GOZ = re.compile(r"(^onyuz_|kapak|_sac$|_sac_|saci|kabuk|govde_kabugu|yalitim|_pu|PU$|fitil|conta|kablo|kelepce|hortum|tel_|zemin|INSAN|dis_taban|tunel|kaplama|etiket|kanal|cerceve|_pem|vida|pul|somun|perde|tapa|omega|kayit|dikme|kulak|kiris|profil|ayak)", re.I)
HEDEF = [
 # (istasyon, etiket, desen)
 ("A", "Açıcı ön motoru", r"^acici_motoru_on$"), ("A", "Açıcı arka motoru", r"^acici_motoru_arka$"),
 ("A", "Açıcı pnömatiği", r"^acici_pnomatigi"), ("A", "Emniyet sensörü RSS36", r"^onyuz_emniyet_sensoru$"),
 ("A", "Işık perdesi", r"^onyuz_isik_perdesi_(alt|ust)$"), ("A", "A istasyon kutusu (U_A içinde)", r"^A_istasyon_kutusu"),
 ("TOPPING", "Kuru bölme pano kutusu", r"^kuru_pano_kutusu$"), ("TOPPING", "DIN plakası (UPS/güç)", r"^kuru_din_plakasi$"),
 ("TOPPING", "Sürücüler (4)", r"^kuru_surucu_\d$"), ("TOPPING", "Valf adası 12×5/2", r"^valf_adasi_12x5_2$"),
 ("TOPPING", "Hava şartlandırıcı (filtre-reg.)", r"^sartlandirici_filtre_regulator$"),
 ("TOPPING", "Kaşar helezon motoru", r"^motor_kasar_cad_v14_helezon$"), ("TOPPING", "Kaşar rotor motoru", r"^motor_kasar_cad_v14_rotor$"),
 ("TOPPING", "Sucuk helezon motoru", r"^motor_sucuk_cad_v8_helezon$"), ("TOPPING", "Sucuk rotor motoru", r"^motor_sucuk_cad_v8_rotor$"),
 ("TOPPING", "Evaporatör fanları (kaset)", r"^evap_kaseti_fani_\d$"), ("TOPPING", "Soğutma grubu KLF6.6 (kaide cebi)", r"^sogutma_grubu_KLF66$"),
 ("TOPPING", "Teknik bölme arka emiş filtresi", r"^teknik_bolme_arka_emis_filtresi$"), ("TOPPING", "Ön kanat filtresi", r"^onyuz_mekanizma_kanadi_sol_filtre$"),
 ("TOPPING", "Tabla X motoru", r"^x_motoru$"), ("TOPPING", "Sabit tahrik motoru (bant kaseti)", r"^st_tahrik_motoru$"),
 ("TOPPING", "Dönüş motoru", r"^donus_motoru$"), ("TOPPING", "X home / limit sensörleri", r"^x_(home|limit_sol|limit_sag)_sensoru$"),
 ("TOPPING", "Tabla boş sensörü", r"^tabla_bos_sensoru$"), ("TOPPING", "Tabla home sensörü", r"^tabla_home_sensoru$"),
 ("TOPPING", "UNO valf blokları (kıyma/kuşbaşı)", r"^(kiyma|kusbasi)__valf_blogu$"), ("TOPPING", "UNO valf blokları (sos/harç)", r"^(sos|harc)__valf_blogu$"),
 ("TOPPING", "Yayıcı kesme valfleri", r"^(sos|harc)_spreader_kesme_valfi_govde$"),
 ("TOPPING", "Evap. kaseti tahliye hortumu", r"^evap_kaseti_tahliye_hortumu$"),
 ("B", "Soğutma grubu (Secop) kondenser", r"^sogutma_grubu_kondenser$"), ("B", "Soğutma grubu kompresör", r"^sogutma_grubu_kompresor$"),
 ("B", "Buharlaştırma tavası", r"^buharlastirma_tavasi$"), ("B", "B panosu PLC", r"^plc_S7-1200_1214C$"),
 ("B", "B panosu güç kaynağı", r"^guc_kaynagi_NDR-240-24$"), ("B", "DOLAP istasyon kutusu", r"^DOLAP_istasyon_kutusu_160x120x90$"),
 ("B", "Evaporatör fanı sol", r"^fan_sol_\d$"), ("B", "Evaporatör fanı sağ", r"^fan_sag_\d$"),
 ("F", "TP10 teknik bölme fanı", r"^fan_[01]$"), ("F", "TP10 ana şalter", r"^ana_salter$"), ("F", "TP10 ekran", r"^ekran_cami$"),
 ("F", "TP10 servis plakası", r"^servis_plakasi$"), ("F", "TP10 CEE priz", r"^cee_priz$"), ("F", "F istasyon kutusu", r"^F_istasyon_kutusu"),
 ("F", "Yükleme bandı motoru", r"^yb_motoru$"), ("F", "Davlumbaz fanı RS30-15", r"^f_davlumbaz_fani"),
 ("F", "Davlumbaz yağ filtresi EN16282", r"^f_davlumbaz_yag_filtresi"), ("F", "Davlumbaz karbon filtresi", r"^f_davlumbaz_karbon_filtre$"),
 ("F", "Kompresör JUN-AIR", r"^kompresor_JUNAIR_OF302_15B_tank$"), ("F", "Kompresör çıkış vanası", r"^kompresor_cikis_vanasi$"),
 ("F", "Yağ tenekesi 18 L", r"^yag_tenekesi_18L$"), ("F", "Yağ tartısı yük hücresi", r"^yag_tarti_yuk_hucresi"),
 ("U", "ANA PANO kapağı", r"^ana_pano_kapagi$"), ("U", "Ana şalter kolu", r"^ana_salter_kolu_OHYS2AJ$"),
 ("U", "U_F emiş fanı + G3 keçe", r"^ust_f_fan_filtre_kecesi_emis_\d$"), ("U", "U_F atış fanı + G3 keçe", r"^ust_f_fan_filtre_kecesi_atis_\d$"),
 ("U", "STEGO termostat", r"^ust_f_fan_termostati"),
 ("K", "K panosu PLC", r"^plc_S7-1200_1214C$"), ("K", "K valf adası SS5Y3", r"^valf_adasi_SS5Y3"),
 ("K", "K şartlandırıcı AW20 (filtre)", r"^sartlandirici_AW20"), ("K", "Yağ emiş filtresi 10 µm", r"^yag_emis_filtresi$"),
 ("K", "Yağ pompası GJ-N21", r"^yag_pompasi_GJ-N21"), ("K", "Yağ basınç sensörü PM1704", r"^yag_basinc_sensoru_PM1704$"),
 ("K", "PulsaJet nozül", r"^PulsaJet_AAB10000"), ("K", "Kesici DGRF", r"^DGRF-C-63-125_govde$"), ("K", "Bıçak (yıldız)", r"^bicak_koruma_halkasi$"),
 ("K", "EC5000 tahrik rulosu", r"^tahrik_rulosu_EC5000_354$"), ("K", "Ürün sensörü verici (arka)", r"^urun_sensoru_(giris|durus)_verici$"),
 ("K", "İtici X (MY1B 250)", r"^itici_X_MY1B10G-250_profil$"), ("K", "İtici Z (MY1B 350)", r"^itici_Z_MY1B10G-350_profil$"),
 ("K", "İtici Z sensörü D-M9N arka", r"^itici_Z_MY1B10G-350_D-M9N_0$"),
 ("E", "E panosu PLC / Beckhoff", r"^(plc_S7-1200_1214C|beckhoff_CX9240)$"), ("E", "E 24/48 V güç", r"^guc_(24V_NDR-240-24|48V_NDR-240-48_a)$"),
 ("E", "Asansör motoru", r"^asansor_motoru$"), ("E", "Besleyici motoru", r"^besleyici_motoru$"), ("E", "Besleyici arka sensörü", r"^besleyici_arka_sensor$"),
 ("E", "Vakum Z silindiri", r"^vakum_Z_silindir$"), ("E", "Köşe motorları (arka MF/MB)", r"^kose_CNR_M[FB]_motor$"),
 ("E", "Piston motoru (frenli)", r"^piston_motoru$"), ("E", "Kalıp destek motoru", r"^destek_motoru$"), ("E", "Köprü motoru", r"^kopru_motoru$"),
 ("E", "Flap katlayıcı motoru", r"^flap_katlayici_motoru$"), ("E", "Yığın üstü sensörü (arka)", r"^sensor_yigin_ustu$"),
 ("E", "Robot çöp kovası 15 L", r"^ecop_robot_cop_kovasi_15L$"),
]
GECIS = {"A": (736, 1436), "TOPPING": (1436, 2500), "B": (736, 4400), "F": (2500, 4000), "U": (2500, 4000), "K": (4000, 4400), "E": (4400, 5230)}
def bul(desen, ist):
    lo, hi = GECIS[ist]
    out = [p for p in P if re.search(desen, p[1]) and p[2][0] >= lo - 1 and p[2][1] <= hi + 1]
    return out
def onunde(k, ist):
    x0, x1, y0, y1, z0, z1 = k
    m = 5
    R = []
    for b, ad, q in P:
        if GOZ.search(ad) or b.startswith(("ELK_", "HAVA_IC", "ZEMIN", "INSAN", "E_KUTU", "E_PIZZA", "ROBOT")): continue
        if q[4] < z1 - 1 or q[4] > ON: continue            # parcanin arka yuzu hedefin onunde olmali
        if q[1] <= x0 + m or q[0] >= x1 - m or q[3] <= y0 + m or q[2] >= y1 - m: continue
        R.append((ad, b, q))
    return R
satir = []
for ist, et, des in HEDEF:
    L = bul(des, ist)
    if not L:
        print("YOK", ist, et, des); continue
    for b, ad, k in L[:2]:
        der = ON + 20 - k[5]                                # on duzlem 79'dan hedefin on yuzune
        R = onunde(k, ist)
        R.sort(key=lambda r: -r[2][5])
        engel = ", ".join(sorted({r[0] for r in R}))[:300]
        print("%-8s %-36s %-34s x %4.0f-%4.0f y %4.0f-%4.0f z %5.0f..%5.0f | ön düzlemden %4.0f mm | önünde: %s" % (
            ist, et, ad, k[0], k[1], k[2], k[3], k[4], k[5], der, engel or "-"))
        satir.append(dict(ist=ist, et=et, ad=ad, k=k, derinlik=der, engel=sorted({r[0] for r in R})))
json.dump(satir, open(r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\adim7\erisim.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
