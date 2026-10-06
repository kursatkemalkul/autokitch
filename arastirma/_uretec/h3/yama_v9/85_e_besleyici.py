# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 85 · E BESLEYİCİ (kutu besleme kızağı) + BESLEYİCİ İTİCİSİ + VAKUM BARI MEKANİZMALARI VİDALI (6 Eki 2026 · Claude · yerel oturum · E mekanizma montajı · KURALLAR §1.2 / §2.2 / §5)
python 85_e_besleyici.py girdi.glb cikti.glb      (zincir: hat3_v10p.glb → hat3_v10q.glb)

E_BESLEYICI (5 mm plaka · 4 × 20 × 20 dolu alüminyum dikme (üst saca önceki adımlarda bağlı) · 2 MGN15 ray (plakanın altında) · mil yatağı + kasnak mili + 2 kasnak + kayış ·
NEMA 23 motor + L motor yuvası · sensör tutucusu + M8 sensör) · İTİCİ (2 kızak plakası + 2 MGN15H araba · 2 kol 8 × 20 · kiriş 6 × 43 · 2 kılavuz blok + burç ·
orta blok · itici pedi · kayış kelepçesi) · VAKUM (5 mm bar · 12 mm vakum bloğu · 2 Ø12 + 1 Ø10 mil · 4 vantuz flanşı + vantuz) — envanterde bağlantı elemanı 0.
  dikmeler ↔ plaka: dikmenin alt ucu plakaya oturur, altında ray olduğundan alttan vida yok → 4 yeni 3 mm L köşebent (AISI 304): dik bacak dikmenin yan yüzüne 2 × M4
  (dolu çubukta dişli), ayak plakaya M4 (5 mm, dişli) · raylar plakaya kendi havşa yuvalarından 8 × M4 (gömme 5) · arabalar kızak plakalarının altından 4 × M4 ·
  kollar ↔ kızak plakası ve kollar ↔ kiriş: TIG köşe dikişi (alüminyum, ER5356) · kılavuz blokları kirişin üstünden 2 × M4 · orta blok kirişin altından 2 × M4 ·
  ped kirişin altından 2 × M4 (plastik: dişli) · kayış kelepçesi kızak plakasının altından 2 × M3 · vakum mili orta: bar altından eksenel M5 ·
  Ø12 miller bara iki yandan DIN 471 segman · vakum bloğu bar altından 2 × M4 · vantuzlar ürün sapıyla (M5) bara.
Hazır ürün (motor / ray / araba / sensör / vantuz): ürüne dokunulmaz, bizim parça dişli (KURALLAR §3).
Denetim (betikte): baş / somun / segman / yeni parça hacmi boş · her vida tam olarak A + B'yi deliyor · diş tutuşu ≥ 1 × d · boy katalogdan."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq
import e_mek_bag as MB

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
g = Glb(gi)
M = MB.Mek(g, (4490, 990, -840), (5240, 1400, -300))
Y, YM, X, XM, Z, ZM = (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)


def kutu(x0, y0, z0, x1, y1, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


# ---------------------------------------------------------------- dikmeler ↔ plaka: L köşebent (sol dikmelerde +x yanda, sağ dikmelerde −x yanda)
for i, (xd, zc, sg) in enumerate(((4560.0, -590.0, 1), (4560.0, -410.0, 1), (5040.0, -590.0, -1), (5040.0, -410.0, -1))):
    ad = "besleyici_dikme_braketi_%d" % i
    xa, xb = (xd, xd + 3.0) if sg > 0 else (xd - 3.0, xd)                  # dik bacak (dikmenin yan yüzünde)
    xf0, xf1 = (xd, xd + 20.0) if sg > 0 else (xd - 20.0, xd)             # ayak (plakanın üstünde)
    sh = kutu(xa, 1337.0, zc - 8.0, xb, 1367.0, zc + 8.0).union(kutu(xf0, 1337.0, zc - 8.0, xf1, 1340.0, zc + 8.0)).val()
    M.yeni(ad, sh, ["L köşebent AISI 304 3 mm · 16 × 30 × 20 (dikme yan yüzü ↔ besleyici plakası)", 1, "3 × 16 × 30 / 20", "lazer + 1 büküm · 0.02 kg", "ÜRETİM"],
           "E_MEK_BAG__celik", aile="besleyici")
    D = "besleyici_profil_%d" % i
    M.vida("%s_dikme_vida" % ad, ad, D, dis="M4", yon=XM if sg > 0 else X, duzlem=xd, pts=[(1350.0, zc), (1360.0, zc)], kavrama=6.0,
           not_="köşebentin dik bacağından 20 × 20 dolu dikmenin yan yüzüne (dişli)")
    M.vida("%s_plaka_vida" % ad, ad, "besleyici_plaka", dis="M4", yon=YM, duzlem=1337.0, pts=[(xd + sg * 13.0, zc)], kavrama=5.0,
           not_="köşebent ayağından 5 mm besleyici plakasına (dişli)")
# ---------------------------------------------------------------- raylar ↔ plaka (ray plakanın altında; vida raydan yukarı)
RAY_Z = [-810.5, -750.5, -690.5, -510.5, -450.5, -390.5]          # rayın ölçülen 6 havşalı deliği (0,25 mm tarama; ortadaki düz delikler havşasız)
for i, xr in ((0, 4550.0), (1, 5050.0)):
    M.vida("besleyici_ray_%d_vida" % i, "besleyici_ray_%d" % i, "besleyici_plaka", dis="M4", yon=Y, duzlem=1332.0, pts=[(xr, z) for z in RAY_Z],
           urun="A", bas_bos=False, not_="MGN15 rayı kendi havşa yuvalarından (60 mm aralık; baş yuvanın tabanında) 5 mm plakaya (dişli)")
# ---------------------------------------------------------------- itici: arabalar ↔ kızak plakaları · kollar · kiriş · bloklar · ped · kelepçe
for i, xc in ((0, 4550.0), (1, 5050.0)):
    M.vida("bitici_araba_%d_vida" % i, "bitici_kizak_plakasi_%d" % i, "bitici_araba_%d" % i, dis="M4", yon=Y, duzlem=1304.0,
           pts=[(xc + fx * 13.0, -797.0 + fz * 15.0) for fx in (-1, 1) for fz in (-1, 1)], kavrama=5.0,
           not_="6 mm kızak plakasının altından MGN15H arabasının 4 dişli deliğine (ürün)")
    # kol ↔ kızak plakası alt yüzü ve kol ↔ kiriş üst kenarı: TIG köşe dikişi (iki yan)
    for k, (xa, xb) in enumerate(((xc - 14.0, xc - 10.0), (xc + 10.0, xc + 14.0))):
        M.yeni("bitici_kol_%d_ust_kaynak_%d" % (i, k), kutu(xa, 1294.0, -826.0, xb, 1298.0, -818.0).val(),
               ["TIG 141 köşe dikişi a 3 · ER5356 · 8 mm · kol yan yüzü ↔ kızak plakası alt yüzü", 1, "a 3 × 8", "TIG 141", "ÜRETİM"],
               "E_MEK_BAG__kaynak", aile="itici_b", rol="kaynak", tur="kaynak")
    M.yeni("bitici_kol_%d_alt_kaynak" % i, kutu(xc - 10.0, 1080.0, -818.0, xc + 10.0, 1084.0, -814.0).val(),
           ["TIG 141 köşe dikişi a 3 · ER5356 · 20 mm · kol +z yüzü ↔ kiriş üst yüzü", 1, "a 3 × 20", "TIG 141", "ÜRETİM"],
           "E_MEK_BAG__kaynak", aile="itici_b", rol="kaynak", tur="kaynak")
for i, (xa, xb) in ((0, (4570.0, 4590.0)), (1, (5060.0, 5080.0))):
    M.vida("bitici_kilavuz_blok_%d_vida" % i, "bitici_kiris", "bitici_kilavuz_blok_%d" % i, dis="M4", yon=YM, duzlem=1074.0, pts=[(xa - 2.0, -803.0), (xb + 2.0, -781.0)],
           kavrama=6.0, not_="6 mm kirişin üstünden kılavuz bloğuna (dişli)")
M.vida("bitici_orta_blok_vida", "bitici_kiris", "bitici_orta_blok", dis="M4", yon=Y, duzlem=1080.0, pts=[(4800.0, -792.0), (4820.0, -792.0)], kavrama=6.0,
       not_="kirişin altından orta bloğa (dişli; mil halkasının dışında)")
M.vida("bitici_pad_vida", "bitici_kiris", "bitici_pad", dis="M4", yon=Y, duzlem=1080.0, pts=[(4870.0, -807.5), (4950.0, -807.5)], kavrama=6.0,
       not_="kirişin altından itici pedine (POM, dişli)")
M.vida("bitici_kayis_kelepcesi_vida", "bitici_kizak_plakasi_1", "bitici_kayis_kelepcesi", dis="M3", yon=Y, duzlem=1304.0, pts=[(5123.5, -799.0), (5123.5, -787.0)],
       kavrama=4.5, not_="kızak plakasının altından kayış kelepçesine (dişli)")
# ---------------------------------------------------------------- vakum bar · miller · blok · vantuzlar
M.vida("vakum_mil_orta_vida", "vakum_bar", "vakum_mil_orta", dis="M5", yon=Y, duzlem=1018.0, pts=[(4810.0, -792.0)], kavrama=10.0,
       not_="5 mm barın altından Ø10 milin alt ucundaki eksenel dişli deliğe")
for i, xm in ((0, 4580.0), (1, 5070.0)):
    M.segman("vakum_mil_%d_segman_alt" % i, "vakum_mil_%d" % i, 1013.0, YM)
    M.segman("vakum_mil_%d_segman_ust" % i, "vakum_mil_%d" % i, 1018.0, Y)
M.vida("vakum_blok_vida", "vakum_bar", "vakum_blok", dis="M4", yon=Y, duzlem=1018.0, pts=[(4885.0, -795.0), (4915.0, -795.0)], kavrama=6.0,
       not_="barın altından 12 mm vakum bloğuna (dişli)")
for i in range(4):
    M.sap_vida("vantuz_%d_sap" % i, "vantuz_flans_%d" % i, "vakum_bar", yon=Y, dis="M5", boy=5.0)

# ---------------------------------------------------------------- kasnak mili yatağı · kasnaklar · motor · motor yuvası (yan saca)
M.vida("besleyici_mil_yatagi_vida", "besleyici_plaka", "besleyici_mil_yatagi", dis="M4", yon=Y, duzlem=1337.0, pts=[(5105.0, -822.5), (5116.0, -807.5)], kavrama=6.0,
       not_="5 mm plakanın altından 36 mm mil yatağına (dişli; mil deliğinin iki yanında)")
M.segman("besleyici_kasnak_mili_segman", "besleyici_kasnak_mili", 5121.0, X)
M.setskur("besleyici_kasnak_0_setskur", "besleyici_kasnak_0", "besleyici_kasnak_mili", yon=ZM, pts=[(5130.5, 1357.0)], dis="M4", gomulu=True,
          not_="göbeksiz kasnak: diş dibinin altında kalan kısa setskur (kayış takılmadan sıkılır, kayış üstünden geçer)")
M.setskur("besleyici_kasnak_1_setskur", "besleyici_kasnak_1", "besleyici_motor", yon=Z, pts=[(5130.5, 1356.5)], dis="M4", gomulu=True,
          not_="göbeksiz kasnak: diş dibinin altında kalan kısa setskur, motor milinin düz yüzüne (kayış takılmadan sıkılır)")
M.motor("besleyici_motor_vida", "besleyici_motor", "besleyici_motor_yuvasi", yon=XM, flans=5142.0, boy_flans=8.0, kav=4.0, dis="M4", kare=47.14, merkez=(1356.5, -345.0),
        not_="NEMA 23 flanşından motor yuvasının 4 mm flanşına (dişli; tutuş 4 = 1 × d)")
M.yeni("besleyici_motor_yuvasi_kaynak", kutu(5135.0, 1321.0, -376.0, 5138.0, 1324.0, -314.0).val(),
       ["TIG 141 köşe dikişi a 3 · ER5356 · 62 mm · motor yuvası flanşı ↔ tabanı (dış köşe)", 1, "a 3 × 62", "TIG 141", "ÜRETİM"],
       "E_MEK_BAG__kaynak", aile="besleyici", rol="kaynak", tur="kaynak")
M.V["e_sag_sac"] = dict(dug="E_GOVDE__kabuk", lo=[5213.5, 123.0, -828.5], hi=[5230.0, 1862.0, 59.0], aile="govde", rol="sac", tip="E sağ yan sac", ek=[])
sh = kutu(5225.5, 1295.0, -355.0, 5228.5, 1321.0, -335.0).union(kutu(5200.0, 1318.0, -355.0, 5228.5, 1321.0, -335.0)).val()
M.yeni("besleyici_motor_yuvasi_braketi", sh, ["L köşebent AISI 304 3 mm · 20 × 26 × 28,5 (motor yuvası tabanı ↔ E sağ yan sacı)", 1, "3 × 20 × 26 / 28,5", "lazer + 1 büküm · 0.03 kg", "ÜRETİM"],
       "E_MEK_BAG__celik", aile="besleyici")
M.vida("besleyici_motor_yuvasi_braketi_vida", "besleyici_motor_yuvasi_braketi", "besleyici_motor_yuvasi", dis="M4", yon=Y, duzlem=1321.0, pts=[(5210.0, -345.0)], kavrama=5.0,
       not_="köşebent ayağının altından 6 mm motor yuvası tabanına (dişli)")
M.saplamali("besleyici_motor_yuvasi_braketi_saplama", "e_sag_sac", "besleyici_motor_yuvasi_braketi", dis="M4", yon=XM, duzlem=5228.5, pts=[(1303.0, -345.0)],
            not_="sağ yan sacın dışından preslenmiş PEM FHP gömme saplama (dışta yüzle aynı) · içte pul + fiberli somun")
# ---------------------------------------------------------------- sensörler
M.vida("besleyici_sensor_tutucu_vida", "besleyici_sensor_tutucu", "besleyici_plaka", dis="M3", yon=Y, duzlem=1332.0, pts=[(4994.0, -800.0), (5006.0, -800.0)],
       not_="3 mm tutucunun üst ayağından plakaya (dişli)")
M.somun_mil("besleyici_sensor_somun_dis", "besleyici_sensor", "besleyici_sensor_tutucu", yon=ZM, dis="M8", yuz=-812.0)
M.somun_mil("besleyici_sensor_somun_ic", "besleyici_sensor", "besleyici_sensor_tutucu", yon=Z, dis="M8", yuz=-809.0, ince=True)
# E3Z sensör tutucuları (yan saca önceki adımın PEM M5 saplamasıyla; somun eksikti) + E3Z gövdesi 4 mm dile kendi 2 × Ø3,2 deliğinden (25,4 aralık)
for ad, tut, sap, (lo, hi), zc, xs in (("asansor", "asansor_sensor_tutucu", "e_saplama_asansor", ((5218.0, 1063.1, -793.4), (5230.0, 1069.9, -786.5)), -790.0, 5180.8),
                                       ("besleyici_uc", "besleyici_uc_sensor_tutucu", "e_saplama_besleyici_uc", ((5218.0, 1063.1, -209.5), (5230.0, 1069.9, -202.5)), -206.0, 5200.8)):
    M.V[sap] = dict(dug="E_GOVDE__celik", lo=list(lo), hi=list(hi), aile="govde", rol="saplama", tip="PEM M5 saplama (sağ yan sac)", ek=[])
    M.somun_mil("%s_tutucu_somun" % ad, sap, tut, yon=XM, dis="M5", yuz=5225.5)
    sen = "%s_sensor" % ad
    M.yeni("%s_sensor_dili" % ad, kutu(xs, 1022.0, zc - 10.0, xs + 4.0, 1053.0, zc + 10.0).val(),
           ["Sensör dili EN AW-5754 4 mm · 31 × 20 · 2 × M3 dişli (E3Z yan delikleri)", 1, "4 × 31 × 20", "lazer + kılavuz · 0.01 kg", "ÜRETİM"], "E_MEK_BAG__celik", aile="besleyici")
    M.yeni("%s_sensor_dili_kaynak" % ad, kutu(xs + 4.0, 1050.0, zc - 10.0, xs + 7.0, 1053.0, zc + 10.0).val(),
           ["TIG 141 köşe dikişi a 3 · ER5356 · 20 mm · sensör dili ↔ tutucunun alt yüzü", 1, "a 3 × 20", "TIG 141", "ÜRETİM"], "E_MEK_BAG__kaynak", aile="besleyici", rol="kaynak", tur="kaynak")
    M.vida("%s_sensor_vida" % ad, sen, "%s_sensor_dili" % ad, dis="M3", yon=X, duzlem=xs, pts=[(1024.4, zc), (1049.8, zc)], urun="A",
           not_="Omron E3Z kendi 2 × Ø3,2 montaj deliğinden (25,4 aralık) 4 mm dile (dişli)")
M.V["e_saplama_katlama"] = dict(dug="E_GOVDE__celik", lo=[4400.0, 1111.1, -243.5], hi=[4412.0, 1117.9, -236.6], aile="govde", rol="saplama", tip="PEM M5 saplama (sol yan sac)", ek=[])
M.somun_mil("katlama_tutucu_somun", "e_saplama_katlama", "katlama_sensor_tutucu", yon=X, dis="M5", yuz=4404.5)

# ---------------------------------------------------------------- 81 / 82 açıkları (E montaj v3 bağlantı denetimi, yerel 6 Eki): yalnız dayanan parçalar
# kalıp duvarları + ön kılavuzlar üst plakanın üstünde duruyordu (vidasız) → 6 mm üst plakanın altından kenarlarına
for ad, x, dis_ in (("kalip_duvar_arka", None, "M3"), ("kalip_duvar_sol", 4495.65, "M3"), ("kalip_duvar_sag", 4825.1, "M4")):
    pts = [(x_, -370.85) for x_ in (4540.0, 4652.0, 4765.0)] if x is None else [(x, z_) for z_ in (-270.0, -206.0, -140.0)]
    M.vida("%s_vida" % ad, "kalip_ust_plaka", ad, dis=dis_, yon=Y, duzlem=918.0, pts=pts, not_="6 mm üst plakanın altından duvarın alt kenarına (dişli)")
for i, (x0, x1) in enumerate(((4500.0, 4555.0), (4585.0, 4645.0), (4675.0, 4735.0), (4765.0, 4805.0))):
    xm = (x0 + x1) / 2.0; d_ = (x1 - x0) / 2.0 - 8.0
    M.vida("kalip_on_kilavuz_%d_vida" % i, "kalip_ust_plaka", "kalip_on_kilavuz_%d" % i, dis="M4", yon=Y, duzlem=918.0, pts=[(xm - d_, -40.9), (xm + d_, -40.9)],
           not_="6 mm üst plakanın altından ön kılavuzun alt kenarına (dişli)")
# kapak katlayıcı ön bloğu: kolun pimine yalnız 3 mm şeritte değiyordu (vidasız) → pim ↔ blok iç köşesine TIG dikişi (ikisi de alüminyum)
M.yeni("kapak_katlayici_blok_on_kaynak", kutu(5157.0, 900.0, -88.0, 5160.0, 903.0, -62.0).val(),
       ["TIG 141 köşe dikişi a 3 · ER5356 · 26 mm · pim üst yüzü ↔ ön blok yan yüzü", 1, "a 3 × 26", "TIG 141", "ÜRETİM"],
       "E_MEK_BAG__kaynak", aile="kapak_katlayici", rol="kaynak", tur="kaynak")

M.bitir(go, "E_MEK_BAG__vida", "85", mek=36, mek_kod="E/Kutu katlama", ek=dict(aile=["besleyici", "itici_b", "vakum"]),
        ek_dugum={"_sablon": {"E_MEK_BAG__kaynak": "E_GOVDE__sac", "E_MEK_BAG__celik": "E_GOVDE__celik"}})
LOG("%.0f sn" % (time.time() - t0))
sys.stdout.flush(); os._exit(0)
