# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 83 · E KÖŞE KALDIRICI (4 köşe tutucu) + KÖŞE PİSTONU MEKANİZMALARI VİDALI (6 Eki 2026 · Claude · 2. oturum · E mekanizma montajı · KURALLAR §1.2 / §2.2 / §5)
python 83_e_kose.py girdi.glb cikti.glb      (zincir: hat3_v10n.glb → hat3_v10o.glb)

E_KOSE (63 bileşen: çerçeve, 4 NEMA 23 motor, 4 × 2 kılavuz bloğu, 4 köşe tutucu linkajı (göbek · mil · bayrak bileziği · mafsal bileziği · çene · parmak),
4 endüktif sensör + 3 mm braketleri, 2 uç blok + LM12 burçları + sağ kapak, bronz somun; piston: kızak kolu (4 × 9 direkler), 10 mm plaka + çelik somun,
motor plakası, NEMA 23 motor, kaplin, vida mili, 2 × Ø12 kılavuz çubuğu, M8 sensör + ürün ince somunları) — envanterde bağlantı elemanı 0.
ÖLÇÜLEN GERÇEK: 4 köşe tutucu (motor + göbek + mil + linkaj) çerçeveye göre x ekseni etrafında 2,7688° EĞİK (arka köşeler yukarı giderken −z, ön köşeler +z);
çerçevenin motor plakası da aynı eğimde 6 mm plaka. Bu yüzden köşe vidaları / pimleri eğik eksende (3B nokta) tanımlanır; x yönündeki pimler eksen hizalıdır.
  motor: 4 × M5 NEMA köşelerinden eğik plakaya (dişli, tutuş 5,5) · göbek → motor mili: setskur M4 (+x) · göbek ↔ mil: Ø3 pim (x) · mafsal bileziği ↔ mil: Ø3 pim (x) ·
  bayrak bileziği (kol) → göbek: 2 × havşa M3 (±z′, 2 mm bilezik duvarından göbeğe dişli) · çene → parmak: havşa M3 (çene üstünden parmağa dişli) ·
  çene kolu ucu ↔ mafsal bileziği: TIG köşe dikişi (gerçekte tek parça krank olarak işlenebilir) · kılavuz blokları: çerçevenin 3 mm dudaklarından 2 × havşa M4 ·
  sensörler: braket + 6 mm perde M8 sensör gövdesiyle delinmiş → dışta ISO 4032, içte ISO 4035 ince somun (braketi perdeye sıkar; braket vidası gerekmez) ·
  uç bloklar: perdeden bloğun iç duvarına 4 × havşa M5 (sol perde 32 mm → M5×40 · sağ 9 mm → M5×16) · sağ kapak: 2 × havşa M3 · LM12 burçlar sıkı geçme (GEÇME) ·
  bronz somun: yeni alüminyum kelepçe bileziği (Ø36/Ø20,2 × 8) 2 × setskur M5 + plakaya 4 × M4 ·
  piston: motor 4 × M5 plakaya (dişli) · motor plakası 2 yeni L köşebent (2 mm) ile direklere (M4 + somun) ve plakaya (M3) · 10 mm plaka direklere direğin dış yüzünden M4 ·
  çelik somun plakaya 2 × setskur M4 · kaplin 2 × setskur M4 · vida mili altında segman · Ø12 çubuklar kola setskur M5 + üstte segman.
Hazır ürün (motor / sensör / burç / somun): ürüne dokunulmaz, bizim parça dişli (KURALLAR §3). Denetim (betikte): baş / somun / segman / yeni parça hacmi boş ·
her vida tam olarak A + B'yi deliyor · diş tutuşu ≥ 1 × d · boy katalogdan."""
import os, sys, time, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import cadquery as cq
import e_mek_bag as MB

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
g = Glb(gi)
M = MB.Mek(g, (4400, 1300, -420), (4900, 1630, 0))
Y, YM, X, XM, Z, ZM = (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)
U = np.array([1.0, 0.0, 0.0])

# ---------------------------------------------------------------- köşe tutucu geometrisi (mil ekseni PCA ile ölçüldü: 2,7688°)
S_, C_ = 0.048306, 0.998833
ACI = math.degrees(math.atan2(S_, C_))                                      # 2.7688°
KOSE = [  # ad, x merkez, mil ekseninin y=1378'deki z'si, eğim işareti (yukarı giderken z yönü), motor, sensör, braket, perde dış/iç yüzü x, somun dış yönü
    ("sol_arka", 4501.6, -369.289, -1, "kose_motor_sol_arka", "kose_sensor_sol_arka", "kose_sensor_braket_0", (4468.6, 4477.6), XM),
    ("sol_on",   4501.6,  -42.711, +1, "kose_motor_sol_on",   "kose_sensor_sol_on",   "kose_sensor_braket_1", (4534.6, 4525.6), X),
    ("sag_arka", 4818.4, -369.289, -1, "kose_motor_sag_arka", "kose_sensor_sag_arka", "kose_sensor_braket_2", (4851.4, 4842.4), X),
    ("sag_on",   4818.4,  -42.711, +1, "kose_motor_sag_on",   "kose_sensor_sag_on",   "kose_sensor_braket_3", (4851.4, 4842.4), X),
]
CENE_PARMAK = {"sol_arka": (4471.0, -378.0), "sol_on": (4473.0, -34.0), "sag_arka": (4848.0, -378.0), "sag_on": (4846.0, -34.0)}   # çene üstünden parmağa vida (x, z) · temas y 1342.5


def eksen(xc, zc, sg):
    e_up = MB.vek((0.0, C_, sg * S_)); w = MB.vek((0.0, -sg * S_, C_))          # e_up: mil ekseni (yukarı) · w: eğik +z
    A0 = np.array([xc, 1378.0, zc])
    nokta = lambda y: A0 + ((y - 1378.0) / C_) * e_up                           # eksen üstünde y yüksekliğindeki nokta
    return e_up, w, A0, nokta


for ad, xc, zc, sg, MOT, SEN, BRK, (yuz_dis, yuz_ic), yon_dis in KOSE:
    e_up, w, A0, P = eksen(xc, zc, sg); e_dn = -e_up
    T = "kose_tutucu_%s_" % ad
    # motor: NEMA 23 flanşı eğik plakanın üstünde (eksen noktası y 1425,83) · 4 × M5×14, flanş 8, tutuş 5,5 (6 mm plaka)
    M.motor("%smotor_vida" % T, MOT, "kose_sasi", yon=e_dn, merkez3=P(1425.83), u_vec=U, kare=47.14, dis="M5", boy_flans=8.0, kav=5.5,
            not_="NEMA 23 flanş deliklerinden çerçevenin 2,77° eğik 6 mm motor plakasına (dişli); motor eksenine paralel")
    # göbek → motor mili: setskur M4 +x (y 1419: göbek duvarı 4,8 · mil Ø6,35) · göbek ↔ mil ve mafsal ↔ mil: Ø3 × 15 pim (x, her iki duvardan 1 mm içeride biter)
    M.setskur("%sgobek_setskur" % T, T + "gobek", MOT, yon=X, pts=[(1419.0, float(P(1419.0)[2]))], dis="M4")
    M.pim("%sgobek_pim" % T, T + "gobek", T + "mil", yon=X, pts=[(1399.5, float(P(1399.5)[2]))], boy=14.0, giris=0.5,
          not_="DIN 7 pim; mil göbeğe yalnız 4,6 mm giriyor (y 1397,5–1402,1) → pim bu bindirmenin ortasında; uçları göbek yüzeyinden 0,5 / 1 mm içeride (çerçeve deliğine sürtmesin)")
    M.pim("%smafsal_pim" % T, T + "mafsal", T + "mil", yon=X, pts=[(1359.0, float(P(1359.0)[2]))], boy=15.0)
    # bayrak bileziği (kol: iç Ø16 / dış Ø20 × 8) → göbek: 2 × havşa M3, ±z′ yönünde bilezik duvarından göbek duvarına (4,8) dişli; delik motor miline ulaşmaz
    c = P(1409.5)
    M.vida("%skol_vida_0" % T, T + "kol", T + "gobek", dis="M3", std="DIN7991", yon=w, duzlem=0.0, pts=[tuple((c - 7.9 * w).tolist())], kavrama=3.0,
           not_="bayrak bileziğinin −z′ duvarından göbeğe (havşa; bilezik 2 mm)")
    M.vida("%skol_vida_1" % T, T + "kol", T + "gobek", dis="M3", std="DIN7991", yon=-w, duzlem=0.0, pts=[tuple((c + 7.9 * w).tolist())], kavrama=3.0,
           not_="bayrak bileziğinin +z′ duvarından göbeğe (havşa)")
    # çene → parmak: havşa M3 çenenin üst yüzünden (eğik) parmağa dişli
    px, pz = CENE_PARMAK[ad]
    M.vida("%scene_parmak_vida" % T, T + "cene", T + "parmak", dis="M3", std="DIN7991", yon=e_dn, duzlem=0.0, pts=[(px, 1342.5, pz)],
           not_="çene kolunun dik bacağı üstünden parmağa (parmak 10 × 5,6 kesit, dişli)")
    # çene kolu ucu ↔ mafsal bileziği: TIG köşe dikişi (yeni 'kaynak' katısı: kol üstü + bilezik yüzeyi arasında, eğik çerçevede kurulur)
    yarm = float(e_up @ np.array([xc, 1359.7, zc + sg * 4.7]))                     # kol üst düzlemi (e_up · P): kolun üstü y 1359,7 (eksenden 4,7 dışarıda: arka −z, ön +z)
    zax = float(w @ A0)                                                             # bilezik ekseninin z′ koordinatı
    x0, x1 = (xc - 8.6, xc - 3.6) if xc < 4600 else (xc + 3.6, xc + 8.6)
    zp0, zp1 = (zax - 8.7, zax - 2.7) if sg < 0 else (zax + 2.7, zax + 8.7)
    kutu = cq.Workplane("XY").box(x1 - x0, 2.2, zp1 - zp0, centered=False).translate((x0, yarm, zp0)).val()
    kutu = kutu.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), sg * ACI)
    sil = cq.Solid.makeCylinder(8.0, 80.0, cq.Vector(*(A0 - 40.0 * e_up).tolist()), cq.Vector(*e_up.tolist()))
    M.yeni("%scene_kaynak" % T, kutu.cut(sil), ["TIG 141 köşe dikişi a 2 · ER308LSi · ~12 mm · çene kolu ucu ↔ mafsal bileziği (gerçekte tek parça krank olarak da işlenebilir)", 1, "a 2 × ~12", "TIG 141", "ÜRETİM"],
           "E_MEK_BAG__kaynak", aile="kose_tutucu", rol="kaynak", kontrol=[], tur="kaynak")
    # kılavuz blokları (7 mm, 21,7 × 22; çerçevenin C yatağında dudak–blok 0–perde 9–blok 1–dudak): alt dudaktan 2 × havşa M4×25 (köşegen ±7)
    # blok 0 + perde geçiş deliği, blok 1 dişli → paket tek vidayla sıkılır (üst dudaktan vida göbeğe çarpıyordu: dudak 5,7 kalın yerde baş göbek deliğine giriyor)
    q = A0 - 7.12 * e_up
    M.vida("kose_kilavuz_%s_vida" % ad, "kose_sasi", "kose_kilavuz_%s_1" % ad, dis="M4", std="DIN7991", yon=e_up, duzlem=0.0,
           pts=[tuple((q - 7.0 * U - 7.0 * w).tolist()), tuple((q + 7.0 * U + 7.0 * w).tolist())], kavrama=5.0, hedef_ek=["kose_kilavuz_%s_0" % ad],
           not_="alt dudaktan (3 mm, havşa) blok 0 (7, geçiş) + perde (9, geçiş) üstünden blok 1'e dişli (eğik eksen)")
    # sensör (M8 endüktif, braket 3 + perde 6'dan geçer): dışta ISO 4032 somun braket yüzünde, içte ISO 4035 ince somun perdenin iç yüzünde → braket perdeye sıkışır
    M.somun_mil("%ssensor_somun_dis" % T, SEN, BRK, yon=yon_dis, dis="M8", yuz=yuz_dis)
    M.somun_mil("%ssensor_somun_ic" % T, SEN, "kose_sasi", yon=tuple(-np.asarray(yon_dis, float)), dis="M8", yuz=yuz_ic, ince=True)

# ---------------------------------------------------------------- uç bloklar · LM12 burçlar · sağ kapak · bronz somun kelepçesi
# uç bloklar çerçevenin 6 mm yan rayının 28 × 28 çentiğinde oturur (3 yüz temas; ray kenarına vida olmaz) → rayın altına 2 mm L köşebent:
# yatay bacak rayın altında (2 × M4 yukarı, dişli ray), dik bacak bloğun iç yüzünde (2 × M4 bloğun 9 mm iç duvarına; burç deliğine 2 mm kala)
for ad, xr0, xr1, xb, yon_b, dz in (("sol", 4444.0, 4466.0, 4444.0, XM, -1), ("sag", 4813.0, 4822.0, 4822.0, X, +1)):
    xa, xb2 = (xb, xb + 2.0) if dz < 0 else (xb - 2.0, xb)                  # dik bacak (bloğun iç yüzünden rayın altındaki boşluğa)
    L = (cq.Workplane("XY").box(xr1 - xr0, 2.0, 26.0, centered=False).translate((xr0, 1392.0, -219.0))
         .union(cq.Workplane("XY").box(2.0, 20.0, 26.0, centered=False).translate((xa, 1374.0, -219.0))).val())
    br = "kose_uc_blok_%s_braket" % ad
    M.yeni(br, L, ["Uç blok L köşebenti AISI 304 2 × %g × 20 × 26 (rayın altı ↔ bloğun iç yüzü)" % (xr1 - xr0 + 2), 1, "2 × %g × 20 × 26" % (xr1 - xr0 + 2), "lazer + büküm · 0.02 kg", "ÜRETİM"],
           "E_MEK_BAG__celik", aile="kose", kontrol=[((xr0, 1392.0, -219.0), (xr1, 1394.0, -193.0)), ((xa, 1374.0, -219.0), (xb2, 1392.0, -193.0))])
    xm = (xr0 + xr1) / 2
    M.vida("%s_ray_vida" % br, br, "kose_sasi", dis="M4", yon=Y, duzlem=1394.0, pts=[(xm, -213.0), (xm, -199.0)], not_="köşebent yatay bacağından rayın altına (6 mm, dişli)")
    M.vida("%s_blok_vida" % br, br, "kose_uc_blok_%s" % ad, dis="M4", yon=yon_b, duzlem=xb, pts=[(1384.0, -213.0), (1384.0, -199.0)], kavrama=4.0,
           not_="köşebent dik bacağından bloğun iç duvarına (dişli; LM12 burç deliğine 2 mm kala biter)")
M.vida("kose_uc_kapak_sag_vida", "kose_uc_kapak_sag", "kose_uc_blok_sag", dis="M3", std="DIN7991", yon=XM, duzlem=4850.0, pts=[(1384.0, -212.0), (1396.0, -200.0)],
       not_="2 mm kapaktan bloğun dış duvarına (5,7 mm) · havşa")
KLP = cq.Solid.makeCylinder(18.0, 8.0, cq.Vector(4660.0, 1400.0, -35.0), cq.Vector(0, 1, 0)).cut(cq.Solid.makeCylinder(10.1, 10.0, cq.Vector(4660.0, 1399.0, -35.0), cq.Vector(0, 1, 0)))
M.yeni("kose_somun_kelepce", KLP, ["Bronz somun kelepçe bileziği Al 6082 Ø36 / Ø20,2 × 8 (bronz somunu çerçeve plakasına tutar; 2 × M5 setskur yuvası, 4 × Ø4,5 delik)", 1, "Ø36/Ø20,2 × 8", "torna · 0.02 kg", "ÜRETİM"],
       "E_MEK_BAG__aluminyum", aile="kose", kontrol=[((4642.0, 1400.0, -53.0), (4650.0, 1408.0, -17.0)), ((4670.0, 1400.0, -53.0), (4678.0, 1408.0, -17.0)),
                                                     ((4650.0, 1400.0, -53.0), (4670.0, 1408.0, -45.0)), ((4650.0, 1400.0, -25.0), (4670.0, 1408.0, -17.0))])
R2 = 18.0 / math.sqrt(2.0)                                                     # setskurlar köşegenlerde (bilezik yüzeyinden radyal), vidalar eksenlerde
M.setskur("kose_somun_setskur_0", "kose_somun_kelepce", "kose_somun", yon=(-1.0, 0.0, -1.0), pts=[(4660.0 + R2, 1404.0, -35.0 + R2)], dis="M5")
M.setskur("kose_somun_setskur_1", "kose_somun_kelepce", "kose_somun", yon=(1.0, 0.0, -1.0), pts=[(4660.0 - R2, 1404.0, -35.0 + R2)], dis="M5")
M.vida("kose_somun_kelepce_vida", "kose_somun_kelepce", "kose_sasi", dis="M4", yon=YM, duzlem=1400.0, pts=[(4674.0, -35.0), (4646.0, -35.0), (4660.0, -21.0), (4660.0, -49.0)],
       not_="kelepçe bileziğinden çerçeve plakasına (6 mm, dişli)")

# ---------------------------------------------------------------- köşe pistonu (kızak kolu): motor · plakalar · kaplin · vida mili · çubuklar
M.motor("kose_piston_motor_vida", "kose_piston_motor", "kose_piston_motor_plakasi", yon=YM, flans=1540.0, boy_flans=8.0, kav=5.5, dis="M5", kare=47.14, merkez=(4660.0, -35.0))
for i, (xp, sgn) in enumerate(((4634.0, +1), (4686.0, -1))):            # direk iç yüzü x · köşebent direğin iç tarafında
    xa, xb = (xp, xp + 2.0) if sgn > 0 else (xp - 2.0, xp)               # dik bacak
    xh0, xh1 = (xp, xp + 18.0) if sgn > 0 else (xp - 18.0, xp)           # yatay bacak (plaka altında)
    L = (cq.Workplane("XY").box(2.0, 20.0, 9.0, centered=False).translate((xa, 1514.0, -16.0))
         .union(cq.Workplane("XY").box(18.0, 2.0, 9.0, centered=False).translate((xh0, 1532.0, -16.0))).val())
    ad = "kose_piston_braket_%d" % i
    M.yeni(ad, L, ["Motor plakası L köşebenti AISI 304 2 × 20 × 20 × 9 (direk iç yüzü ↔ plaka altı)", 1, "2 × 20 × 20 × 9", "lazer + büküm · 0.01 kg", "ÜRETİM"],
           "E_MEK_BAG__celik", aile="kose_piston", kontrol=[((xa, 1514.0, -16.0), (xb, 1534.0, -7.0)), ((xh0, 1532.0, -16.0), (xh1, 1534.0, -7.0))])
    M.somunlu("%s_direk_vida" % ad, ad, "kose_piston_kol", dis="M4", yon=(XM if sgn > 0 else X), duzlem=xp, pts=[(1518.0, -11.5), (1527.0, -11.5)],
              not_="köşebent dik bacağı + 4 mm direk; pul + fiberli somun direğin dış yüzünde")
    M.vida("%s_plaka_vida" % ad, ad, "kose_piston_motor_plakasi", dis="M3", yon=Y, duzlem=1534.0, pts=[(xp + sgn * 6.0, -11.5), (xp + sgn * 13.0, -11.5)],
           not_="köşebent yatay bacağından motor plakasına (6 mm, dişli)")
    M.vida("kose_piston_plaka_vida_%d" % i, "kose_piston_kol", "kose_piston_plaka", dis="M4", yon=(X if sgn > 0 else XM), duzlem=xp, pts=[(1493.0, -11.5)],
           not_="direğin dış yüzünden (4 mm) 10 mm plakanın çentik yüzüne (dişli)")
M.setskur("kose_piston_somun_setskur", "kose_piston_plaka", "kose_piston_somun", yon=Z, pts=[(4655.0, 1493.0), (4665.0, 1493.0)], dis="M4")
M.setskur("kose_piston_kaplin_setskur_0", "kose_piston_kaplin", "kose_piston_vida_mili", yon=Z, pts=[(4660.0, 1508.0)], dis="M3",
          not_="vida mili kaplinin içine yalnız 4 mm giriyor (y 1506–1510, üreteç geometrisi) → M3 setskur y 1508; açık madde: milin boyu +10 mm")
M.setskur("kose_piston_kaplin_setskur_1", "kose_piston_kaplin", "kose_piston_motor", yon=Z, pts=[(4660.0, 1526.0)])
M.segman("kose_piston_vida_mili_segman", "kose_piston_vida_mili", 1488.0, YM)
for ad_, xr in (("sol", 4430.1), ("sag", 4836.1)):
    M.setskur("kose_piston_mil_%s_setskur" % ad_, "kose_piston_kol", "kose_piston_mil_%s" % ad_, yon=Z, pts=[(xr, 1493.0)], dis="M5")
    M.segman("kose_piston_mil_%s_segman" % ad_, "kose_piston_mil_%s" % ad_, 1496.0, Y)

M.bitir(go, "E_MEK_BAG__vida", "83", mek=36, mek_kod="E/Kutu katlama", ek=dict(aile=["kose", "kose_tutucu", "kose_piston"], egim_derece=ACI),
        ek_dugum={"_sablon": {"E_MEK_BAG__kaynak": "E_GOVDE__sac", "E_MEK_BAG__celik": "E_GOVDE__celik"}})
LOG("%.0f sn" % (time.time() - t0))
sys.stdout.flush(); os._exit(0)
