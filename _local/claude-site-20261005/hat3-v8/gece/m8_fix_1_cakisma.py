# -*- coding: utf-8 -*-
"""MADDE 8 · adim 1 · 127 gercek cakismadan duzeltilebilenler (cakisma.md, v8x bilesen numaralari). python m8_fix_1_cakisma.py giris.glb cikis.glb"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m8kit import Glb, delik_ucgenler, kenetle, esle, radyal, kutu_ucgen, silindir_ucgen
g = Glb(sys.argv[1]); LOG = []
def log(*a): LOG.append(" ".join(str(x) for x in a)); print(*a)
B = lambda d, n: g.bilesen(d, n)

# ---- once tum bilesenleri cozumle (numaralar v8x taramasindan) ----
H = {}
def h(k, d, n): H[k] = B(d, n)
h("KD1o", "ELK_TOPPING__kanal", 0); h("KD1i", "ELK_TOPPING__kanal", 1); h("anabes", "ELK_ANA_HAT__paslanmaz", 3)
h("hava", "HAVA_KOMPRESOR__hava_ana", 0)
for k, n in (("sg6", 6), ("sg8", 8)): h(k, "TOPPING_MODUL__celik", n)
h("sivi", "TOPPING_MODUL__bakir", 4)
h("cerceve", "ELK_ANA_HAT__rakor", 2)
h("qra", "ELK_QR_MONTAJ__paslanmaz", 0); h("qrb", "ELK_QR_MONTAJ__paslanmaz", 1)
MAND = {59: 91, 55: 83, 43: 59, 35: 43, 47: 67, 39: 51, 31: 35, 51: 75, 15: 3, 19: 11, 27: 27, 23: 19}
for kb, br in MAND.items(): h("kab%d" % kb, "ELK_QR_KABLO__kablo", kb); h("br%d" % br, "ELK_QR_MONTAJ__celik", br)
h("kolon", "TOPPING_MODUL__sac", 20)
h("Apost", "A_GOVDE__paslanmaz", 3)
h("klf", "TOPPING_MODUL__motor", 0)
h("aski", "ELK_ANA_HAT__paslanmaz", 14)
h("UKE", "ELK_ANA_HAT__kanal", 4); h("inisK", "ELK_ANA_HAT__kanal", 25); h("inisE", "ELK_ANA_HAT__kanal", 23)
for n in (6, 8, 10, 14): h("UF%d" % n, "ELK_ANA_HAT__kanal", n)
for n in (1, 3, 2, 0): h("ayak%d" % n, "TOPPING_MODUL__fircali", n)
for n in (6, 7, 2, 3): h("conta%d" % n, "TOPPING_MODUL__conta", n)
for n in (1, 0): h("rconta%d" % n, "TOPPING_MODUL__conta", n)
h("filtre", "TOPPING_MODUL__pom", 2); h("sil15", "TOPPING_MODUL__silikon", 15)
h("Asag", "A_GOVDE__sac", 3)
h("klemens", "ELK_ISTASYON__cihaz", 7)
AVARA = ["K2_lahm_4", "K3_hamur_4", "K1_lahm_4", "K5_ic1_1", "K1_lahm_1", "K5_hamur_3", "K1_lahm_2", "K1_lahm_3", "K5_hamur_1", "K1_lahm_5", "K6_ic1_1",
         "K2_lahm_1", "K3_hamur_2", "K2_lahm_3", "K5_hamur_2", "K2_lahm_5", "K6_tatli_1", "K3_hamur_1", "K2_lahm_2", "K6_ic1_2", "K3_hamur_3"]
for a in AVARA: h("av_" + a, "CEK_%s__aluminyum" % a, 1)
h("cit", "K_BANT__pom", 4)
for n in (60, 12, 47, 30): h("keleb%d" % n, "TOPPING_MODUL__paslanmaz", n)
h("dil_s", "TOPPING_MODUL__pom", 23)
for n in (6, 3, 5, 4): h("kilif%d" % n, "B_SOGUTMA__plastik", n)
for n in (9, 8): h("kel%d" % n, "B_SOGUTMA__plastik", n)
log("bilesen cozuldu:", len(H))

# 1 . KD1 dikey kanal ana besleme kolunu (y 1253,5-1321,5) kesiyordu -> KD1 iki parca, kolun alt/ust sacinda kanal agzi (kablolar kolun icinden gecer)
for k, (a0, a1) in (("KD1o", ((905, 1253.5), (1321.5, 1840))), ("KD1i", ((906.5, 1253.5), (1321.5, 1838.5)))):
    b = H[k]
    def f(P, a0=a0, a1=a1):
        return np.concatenate([kenetle(P, 1, a0[0], a0[1]), kenetle(P, 1, a1[0], a1[1])])
    log("KD1 bol", k, g.donustur(b, f))
log("ana besleme kol agzi", g.donustur(H["anabes"], lambda P: delik_ucgenler(delik_ucgenler(P, 1, [1253.5, 1255.0], 2422.5, 2447.5, -826.8, -790.0), 1, [1320.0, 1321.5], 2422.5, 2447.5, -826.8, -790.0)))

# 2 . kompresor hava ana #0 vananin alt yuzune yarim giriyordu -> hortum y 1817'de biter + 90 derece dirsek rakor (vana alt portuna vidali)
g.donustur(H["hava"], lambda P: kenetle(P, 1, None, 1817.0))
g.ucgen_ekle("HAVA_KOMPRESOR__siyah", kutu_ucgen([3543.5, 1817.0, -386.5], [3554.5, 1832.0, -380.0]))
log("hava dirsek rakor eklendi")

# 3 . TOPPING sicak gaz dongusu dikey borulari tava borusuna giriyordu -> boru ucu tava borusunun ustunde biter (lehim T)
for k in ("sg6", "sg8"): log(k, g.donustur(H[k], lambda P: kenetle(P, 1, 908.3, None)))
# sivi hatti emis dirsegine giriyordu -> sivi hatti dirsegin onunde biter
log("sivi", g.donustur(H["sivi"], lambda P: kenetle(P, 2, -696.7, None)))

# 4 . ana besleme taban cercevesi ic agzi kanal ic olcusundeydi -> ic agiz kanal dis olcusu + 0,1
def cer(P):
    P = esle(P, 0, 4100.0, 4098.4); P = esle(P, 0, 4140.0, 4141.6); P = esle(P, 2, -700.0, -701.6); return esle(P, 2, -642.0, -640.4)
log("cerceve", g.donustur(H["cerceve"], cer))

# 5 . QR giris plakalari: dudak robot kutusuna / omurga kanal duvarina giriyordu -> dudakta kesik (delikli taban + kisaltilmis dudak)
def plaka(x0, x1, hx0, hx1, dx0, dx1):
    T = [kutu_ucgen([x0, 20.6, 670.0], [hx0, 83.6, 671.5]), kutu_ucgen([hx1, 20.6, 670.0], [x1, 83.6, 671.5]),
         kutu_ucgen([hx0, 20.6, 670.0], [hx1, 32.0, 671.5]), kutu_ucgen([hx0, 68.0, 670.0], [hx1, 83.6, 671.5]),
         kutu_ucgen([dx0, 20.6, 671.5], [dx1, 22.1, 691.5])]
    return np.concatenate(T)
g.donustur(H["qra"], lambda P: plaka(5040, 5157, 5066, 5131, 5070.2, 5157))
g.donustur(H["qrb"], lambda P: plaka(5300, 5428, 5325, 5411, 5300, 5321.9))
log("QR plakalar yeniden")

# 6 . 12 goz mandal kablosu braketi deliksiz geciyordu -> braket (z 1148-1151) 4,6 x 4,6 kablo deligi (buson yeri)
for kb, br in MAND.items():
    c = (H["kab%d" % kb]["lo"] + H["kab%d" % kb]["hi"]) / 2
    g.donustur(H["br%d" % br], lambda P, c=c: delik_ucgenler(P, 2, [1148.0, 1151.0], c[0] - 2.3, c[0] + 2.3, c[1] - 2.3, c[1] + 2.3))
log("12 braket deligi")

# 7 . acici kolonu taban sacini 1,5 mm geciyordu -> kolon sacin ustunde biter (y 893,5)
log("kolon", g.donustur(H["kolon"], lambda P: kenetle(P, 1, 893.55, None)))
# 8 . A arka-sag kose dikmesi ust hat TOPPING_A kanalini/kablolarini kesiyordu -> dikme kanalin altinda biter (y 2142,9)
log("A dikme", g.donustur(H["Apost"], lambda P: kenetle(P, 1, None, 2142.9)))
# 9 . KLF6.6 sac#36'ya 1 mm -> grup 1,05 mm geri
log("KLF", g.tasi_b(H["klf"], [0, 0, -1.05]))
# 10 . toplama kanali askisi U_F on dudagina giriyordu -> aski U_F onunde (z -689,95...-675)
log("aski", g.donustur(H["aski"], lambda P: kenetle(P, 2, -689.95, None)))
# 11 . inis K/E kanallari U_KE tabanini geciyordu -> inis taban altinda biter + tabanda kanal agzi
log("inisK", g.donustur(H["inisK"], lambda P: kenetle(P, 1, None, 2125.0)))
log("inisE", g.donustur(H["inisE"], lambda P: kenetle(P, 1, None, 2125.0)))
log("UKE agiz", g.donustur(H["UKE"], lambda P: delik_ucgenler(delik_ucgenler(P, 1, [2125.0, 2126.5], 4281.5, 4318.5, -824.5, -767.5), 1, [2125.0, 2126.5], 5081.5, 5118.5, -824.5, -767.5)))
# 12 . kesit gecis plakalari (1,6) kanal uclarinin ortasindaydi -> kanal uclari plaka yuzune
g.donustur(H["UF8"], lambda P: esle(esle(P, 0, 3280.0, 3279.15), 0, 2920.0, 2920.75))
g.donustur(H["UF6"], lambda P: esle(P, 0, 3280.0, 3280.85))
g.donustur(H["UF10"], lambda P: esle(esle(P, 0, 2920.0, 2919.25), 0, 2575.0, 2575.85))
g.donustur(H["UF14"], lambda P: esle(P, 0, 2575.0, 2574.15)); log("UF uclari")
# 13 . pnomatik on ayak ust yuzu silindire 0,9 -> ayak ust yuzu silindir alt yuzunde
for n in (1, 0): g.donustur(H["ayak%d" % n], lambda P: kenetle(P, 1, None, 1594.55))
for n in (3, 2): g.donustur(H["ayak%d" % n], lambda P: kenetle(P, 1, None, 1171.55))
log("ayaklar")
# 14 . gecis contalari ic capi dirsek/agiz dis capindan kucuktu -> ic dudak 0,8 mm acildi
for n in (6, 7, 2, 3):
    b = H["conta%d" % n]; c = ((b["lo"] + b["hi"]) / 2)[[0, 2]]
    g.donustur(b, lambda P, c=c: radyal(P, 1, c, 0.8, rmax=19.3))
def dik_ic(P, lo, hi, d):
    P = P.copy(); V = P.reshape(-1, 3); c = (lo + hi) / 2
    ic = (np.abs(V[:, 0] - c[0]) < (hi[0] - lo[0]) / 2 - 0.1) & (np.abs(V[:, 2] - c[2]) < (hi[2] - lo[2]) / 2 - 0.1)
    for ax in (0, 2):
        V[ic, ax] += np.sign(V[ic, ax] - c[ax]) * d
    return V.reshape(P.shape)
for n in (1, 0):
    b = H["rconta%d" % n]; g.donustur(b, lambda P, b=b: dik_ic(P, b["lo"], b["hi"], 1.4))
log("contalar")
# 15 . teknik bolme emis filtresi sac#38'e 0,5 -> filtre x <= 1629,45 . silikon #15 evap kaseti saclarina -> ust uc y 1382,95
g.donustur(H["filtre"], lambda P: kenetle(P, 0, None, 1629.45)); g.donustur(H["sil15"], lambda P: kenetle(P, 1, None, 1382.95)); log("filtre+silikon")
# 16 . A sag levha cep agzi alt kenari (y 894) mekanizma teknesi / enerji zinciri kanalinin tabanindan 0,5 yuksek -> agiz alt kenari y 893,4
log("A agiz", g.donustur(H["Asag"], lambda P: esle(P, 1, 894.0, 893.4, kosul=lambda V: (V[:, 2] > -510.1) & (V[:, 2] < 4.1))))
# 17 . F klemens 5 kutu rakoruna 0,4 -> klemens x <= 2950,75
g.donustur(H["klemens"], lambda P: kenetle(P, 0, None, 2950.75)); log("klemens")
# 18 . 21 cekmece avarasi GT3 kayisa 0,35 -> avara gobek yaricapi 0,45 mm kucuk (kayis ic yuzu disinda)
for a in AVARA:
    b = H["av_" + a]; c = ((b["lo"] + b["hi"]) / 2)[[1, 2]]
    g.donustur(b, lambda P, c=c: radyal(P, 0, c, -0.45, rmax=15.0, rmin=12.5))
log("avaralar")
# 19 . K bant cit_giris_1 kose dikmesine 0,31 -> cit ust kenari z 26,95
g.donustur(H["cit"], lambda P: kenetle(P, 2, None, 26.95)); log("cit")
# 20 . TC kelepce kelebek somunu kelepce govdesine 0,28 -> kelebek 0,35 disa (+y)
for n in (60, 12, 47, 30): g.tasi_b(H["keleb%d" % n], [0, 0.35, 0])
# 21 . sucuk yarik dili cikis tupune 0,34 -> dil 0,4 -y
log("kelebek (yarik dili: kaset ici, dokunulmadi)")
# 22 . gider ana hatti kiliflari/kelepceleri (egimli boru) ic capi -> 0,45 acildi
for k in ("kilif6", "kilif3", "kilif5", "kilif4"):
    b = H[k]; c = ((b["lo"] + b["hi"]) / 2)[[1, 2]]; g.donustur(b, lambda P, c=c: radyal(P, 0, c, 0.45, rmax=10.4))
for k in ("kel9", "kel8"):
    b = H[k]; c = ((b["lo"] + b["hi"]) / 2)[[1, 2]]; g.donustur(b, lambda P, c=c: radyal(P, 0, c, 0.7, rmin=9.5, rmax=11.0))
log("gider kilif")
g.kaydet(sys.argv[2]); log("kaydedildi", sys.argv[2])
open(os.path.splitext(sys.argv[2])[0] + "_log.txt", "w", encoding="utf-8").write("\n".join(LOG))
