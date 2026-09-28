"""
BANTLI TABLA · HESAP v1 (28 Eyl 2026) — Kemal: "kare bantlı kasete odaklanalım … full detaylı, tam üretilebilir ama
basitleştir; önce her detayıyla modelle, simülasyon olsun".

SAYI TEK YERDE: bu dosya hesabı tutar → bantli_tabla_hesap_v1.json; bantli_tabla_cad_v1.py buradan OKUR.
Bağlam ölçüleri (tabla yığını, yarık, ray sonu, limit) arastirma/BANTLI_TABLA_v1/baglam/baglam_ozet_tc_v26.json'dan
(TOPPING v26 + hesap v6, ana klasörden SALT OKUNUR çıkarıldı). Fırın ağzı fırın v8'den (ana klasör, izlenmiyor) elle.

KURULUŞ (sade):
  · KASET (tablayla döner, elle takılıp çıkar): taban sacı 6 (bugünkü göbeğin yerine, ayar bileziğine oturur)
    + 2 yan sac 4 + yatak sacı 6 (açıcı baskısını taşır) + bant (Forbo Siegling Transilon E 3/1 U0/U2, 1,15 mm)
    + 2 eş rulo Ø12 (burun = TAHRİKLİ, kuyruk = yay gergili) + arka yanda GT2 kayış → tahrik rotoru
    (20T kasnak + mıknatıs kabı, sabit mile 2 rulmanla) + kilit plakası (mıknatıs tutucu).  Kasette motor/kablo YOK.
  · SABİT TAHRİK (TOPPING içinde, sağ-arka, dönüş dairesinin DIŞINDA): paslanmaz kapalı kutu, pencereli (1 mm 316);
    içinde mıknatıs diski + mil + 2 rulman; arkasında NEMA23 (katalog STEP). Kaset 0°'de gelince diskler 4,5 mm'den kavranır.
  · YÜKLEME BANDI (fırın girişi, B kavramı): Ø12 burun + Ø30 tahrik, PTFE-cam bant; aktarmada kasetle eş hız.
"""
import json, math, os, io

U = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(U)
BAGLAM = os.path.join(KOK, "BANTLI_TABLA_v1", "baglam", "baglam_ozet_tc_v26.json")
B = json.load(io.open(BAGLAM, encoding="utf-8"))
S = {"surum": "bantli_tabla_hesap_v1", "kaynaklar": {}, "varsayimlar": [], "denetim": []}
def kay(k, v): S["kaynaklar"][k] = v
def var(s): S["varsayimlar"].append(s)
def den(ad, deger, sart, ok): S["denetim"].append(dict(ad=ad, deger=round(deger, 3) if isinstance(deger, float) else deger, sart=sart, gecti=bool(ok)))

# ================================================================ 1 · SÜREÇ KOTLARI / EKSEN
ZE = B["ZT"]                         # −170 tabla ekseni z (dünya)
UST = 1000.0                         # bant üstü = bugünkü disk üstü (SÜREÇ KOTU, değişmez)
AYAR_UST = B["bb_ayar_bilezigi"][3]  # 978,0 ayar bileziği üstü → kaset tabanı buna oturur
SUCUK_X = 2293.0                     # sucuk kaseti ağzı (fırına en yakın dönüş)
KIYMA_X = 1595.0
SOS_X = 910.0
PARK = B["X_PARK"]                   # 350
AKT_ESKI = B["X_AKTARMA"]            # 2337
kay("tabla_yigini", "TOPPING v26: ayar bileziği 972,77–978 · göbek 978–989 · Ø340 tabla 989–992 · disk 992–1000 (baglam_ozet)")

# ================================================================ 2 · BANT (katalog)
BANT = dict(ad="Forbo Siegling Transilon E 3/1 U0/U2 MT HACCP white FDA", t=1.15, k1=3.0, kg_m2=1.1, r_bicak_min=3.0,
            mu_celik=0.18, T=(-30.0, 100.0))
kay("bant", "Forbo Siegling ürün föyü TR-906726 (E 3/1 U0/U2 ailesi): kalınlık 1,15 · k1% gevşemiş 3 N/mm · 1,1 kg/m² · "
             "bıçak kenar r ≥ 3 mm · −30…+100 °C · FDA+AB · alt yüz üretan emdirilmiş kumaş; sürtünme çelik 0,18 (Forbo arama özeti)")
var("MT (mat) + HACCP varyantının kendi föyü okunamadı; aile değerleri (906726) kullanıldı — bayiden teyit")
W_BANT = 296.0                        # bant genişliği → pideye her yanda 8 mm
PIDE_D = 280.0
S["pide_payi"] = (W_BANT - PIDE_D) / 2.0

# ================================================================ 3 · KASET GEOMETRİSİ (yerel: x fırına, z öne; y dünya)
D_R = 12.0                           # burun = kuyruk rulosu (aynı parça)
Y_R = UST - BANT["t"] - D_R / 2.0    # 992,85 rulo ekseni
X_UC = 153.5                         # burun ucu (bant dış yüzü) — tablanın aktarma konumunu bu belirler
X_N = X_UC - BANT["t"] - D_R / 2.0   # 146,35 burun rulosu ekseni
X_K = -X_N                           # kuyruk rulosu (gergi ±3)
Z_KILAVUZ = (148.5, 151.0)           # UHMW kenar kılavuzu (yatak üstünde)
Z_YAN = (151.0, 155.0)               # yan sac 4 mm (iç 151 · dış 155)
T_YATAK = 6.0
Y_YATAK = (UST - BANT["t"] - T_YATAK, UST - BANT["t"])      # 992,85 … 998,85
X_YATAK = (X_K + D_R / 2.0 + 1.0, X_N - D_R / 2.0 - 1.0)   # rulolara 1 mm
T_TABAN = 6.0
Y_TABAN = (AYAR_UST, AYAR_UST + T_TABAN)                   # 978 … 984
DONUS_IC = Y_R - D_R / 2.0                                   # dönüş kolu iç yüzü 986,85
DONUS_DIS = DONUS_IC - BANT["t"]                             # 985,70
S["kaset"] = dict(D_R=D_R, Y_R=Y_R, X_N=X_N, X_K=X_K, X_UC=X_UC, W_BANT=W_BANT, Z_KILAVUZ=Z_KILAVUZ, Z_YAN=Z_YAN,
                  Y_YATAK=Y_YATAK, X_YATAK=X_YATAK, Y_TABAN=Y_TABAN, DONUS_IC=DONUS_IC, DONUS_DIS=DONUS_DIS)

# bant boyu (hatve çizgisi = bant ortası)
C_R = X_N - X_K
L_BANT = 2.0 * C_R + math.pi * (D_R + BANT["t"])
S["bant_boyu"] = dict(merkezler=C_R, L=L_BANT, not_="sonsuz sıcak ek (Forbo Z-ek); kuyruk kızağı ±3 mm")

# dönüş kolu sarkması (gerginlikte)
YAY = dict(ad="Century Spring 62266SCS · 316 · dış Ø9,14 · tel 1,27 · serbest 12,7 · 13,45 N/mm · en çok 44,75 N (3,33 mm)",
           D=9.14, tel=1.27, L0=12.7, k=13.45, s_max=3.33, on_sikma=2.5)
kay("yay", "centuryspring.com/shop/62266scs (ürün sayfası): 316 paslanmaz basma yayı, uçlar kapalı-taşlanmış, 5,41 sarım")
F_YAY = YAY["k"] * YAY["on_sikma"]      # yay başına (kuyruk kızağı başına)
T_KOL = F_YAY                           # 2 yay × F = 2 kol × T  →  T = F
eps = T_KOL / (BANT["k1"] * W_BANT)     # % uzama (sonuç)
w_bant = BANT["kg_m2"] * 9.81 * W_BANT / 1000.0          # N/m
sarkma = w_bant * (C_R / 1000.0) ** 2 / (8.0 * T_KOL) * 1000.0
S["gerginlik"] = dict(eps_yuzde=eps, T_kol_N=T_KOL, mil_yuku_N=2.0 * T_KOL, sarkma_mm=sarkma, yay=YAY, F_yay=F_YAY,
                      calisma_boyu=YAY["L0"] - YAY["on_sikma"], F_aralik=(YAY["k"] * (YAY["on_sikma"] - 0.8), YAY["k"] * min(YAY["s_max"], YAY["on_sikma"] + 0.8)),
                      not_="kuyruk rulosu 2 kızakta; her kızağı 1 yay dışa iter (sabit kuvvet, bant uzasa da gerginlik ~aynı)")
den("yay çalışma sıkışması en çok sınırının altında", YAY["on_sikma"] + 0.8, "< 3,33 mm", YAY["on_sikma"] + 0.8 < YAY["s_max"])
den("dönüş kolu tabana değmez (sarkma dahil)", DONUS_DIS - sarkma - Y_TABAN[1], "> 0,5 mm", DONUS_DIS - sarkma - Y_TABAN[1] > 0.5)

# rulo eğilmesi (Ø12 dolu 316, yataklar arası)
E_CELIK = 193000.0
I12 = math.pi * D_R ** 4 / 64.0
L_RULO = 2.0 * Z_YAN[0]
q = 2.0 * T_KOL / W_BANT
sehim_rulo = 5.0 * q * L_RULO ** 4 / (384.0 * E_CELIK * I12)
S["rulo"] = dict(I=I12, L=L_RULO, q_N_mm=q, sehim_mm=sehim_rulo)
den("rulo sehimi 2T altında", sehim_rulo, "< 0,25 mm", sehim_rulo < 0.25)

# ================================================================ 4 · AÇICI BASKISI → YATAK SEHİMİ
F_ACICI = 482.0
kay("acici", "konili döner açıcı baskısı 482 N (pnömatik; TOPPING v21 açıcı hesabı)")
Lz = 2.0 * Z_YAN[0]                        # iki yan sac arası açıklık
bx = X_YATAK[1] - X_YATAK[0]
for ad_, b_eff in (("en_kotu_serit_120", 120.0), ("tam_genislik", bx)):
    I_ = b_eff * T_YATAK ** 3 / 12.0
    w_ = F_ACICI / PIDE_D                   # çizgi yük N/mm (koni hattı z boyunca)
    # 280 mm'ye yayılı yük, 302 açıklık — orta sehim ≈ düzgün yayılı yük formülü (güvenli yan)
    d_ = 5.0 * w_ * Lz ** 4 / (384.0 * E_CELIK * I_)
    S.setdefault("yatak", {})[ad_] = dict(b=b_eff, I=I_, sehim_mm=d_)
den("yatak sehimi (en kötü şerit)", S["yatak"]["en_kotu_serit_120"]["sehim_mm"], "< 0,5 mm (hamur kalınlığı 5–8)", S["yatak"]["en_kotu_serit_120"]["sehim_mm"] < 0.5)
var("yatak sehiminde koni hattı z boyunca düzgün yayılı yük + 120 mm etkin şerit (güvenli yan); plaka etkisi tam genişlikte %s mm" % round(S["yatak"]["tam_genislik"]["sehim_mm"], 2))

# ================================================================ 5 · TAHRİK ZİNCİRİ (kaset tarafı)
GT2 = dict(dis=20, dis_rotor=28, hatve=2.0)
D_KASNAK = GT2["dis"] * GT2["hatve"] / math.pi              # 12,73 burun kasnağı hatve çapı
D_KASNAK_R = GT2["dis_rotor"] * GT2["hatve"] / math.pi      # 17,83 rotor kasnağı (içine 686 rulman sığar)
ORAN = GT2["dis_rotor"] / float(GT2["dis"])                 # 1,4 (burun rotordan hızlı döner)
L_GT2 = 140.0                                               # kapalı GT2 halkası (70 diş) — katalog boyu (130 ile tahrik kutusu yarık contasına 0,8 mm giriyordu)
C_GT2 = 40.0
for _ in range(50):                                         # L = 2C + π(D1+D2)/2 + (D2−D1)²/(4C)
    C_GT2 = (L_GT2 - math.pi * (D_KASNAK + D_KASNAK_R) / 2.0 - (D_KASNAK_R - D_KASNAK) ** 2 / (4.0 * C_GT2)) / 2.0
X_ROTOR = X_N - C_GT2                                       # tahrik rotoru ekseni (yerel x)
Y_ROTOR = 988.0                                             # sabit tahrik kutusu enerji kanalının üstünde kalsın diye
Z_KASNAK = (-163.0, -156.0)                                 # GT2 düzlemi (yan sacın 1 mm dışı)
D_MIKNATIS = 36.0
Z_ROTOR_YATAK = (-176.0, -164.0)                            # 2 × 686-2RS (6×13×5) rotor gövdesinde
Z_MIKNATIS = (-184.0, -176.5)                               # mıknatıs kabı (dışa bakar) · kasnak + yatak + kap TEK gövde (316)
HAVA = 2.0                                                  # rotor kapağı ↔ pencere (tabla konum toleransı ±0,5 + pay)
BOSLUK_KAVRAMA = 0.55 + HAVA + 1.0 + 0.5 + 0.55             # mıknatıs yüzü ↔ mıknatıs yüzü: kap 0,5 + hava + pencere 1 + iç hava 0,5 + deri 0,5 = 4,6
Z_SURUCU_YUZ = Z_MIKNATIS[0] - HAVA                         # pencere dış yüzü (yerel)
S["tahrik_kaset"] = dict(GT2=GT2, D_kasnak=D_KASNAK, D_kasnak_rotor=D_KASNAK_R, oran=ORAN, L_GT2=L_GT2, C_GT2=C_GT2, X_ROTOR=X_ROTOR, Y_ROTOR=Y_ROTOR,
                         Z_KASNAK=Z_KASNAK, Z_ROTOR_YATAK=Z_ROTOR_YATAK, D_MIKNATIS=D_MIKNATIS, Z_MIKNATIS=Z_MIKNATIS, bosluk=BOSLUK_KAVRAMA,
                         mil="sabit mil Ø6 × 34 (316) arka yan saca kaynaklı · dış ucu DIN 6799 RS5 segman (kabın ortasındaki Ø14 cepte)")
kay("gt2", "GT2 2 mm hatve · burun 20 diş (Ø12,73) · rotor 28 diş (Ø17,83) · kapalı halka Gates 140-2GT-6 (70 diş, 6 mm)")

# yükler / tork
m_pide = 0.45                                                # kg (hamur 250 + sos + kaşar + sucuk ≈ 450 g)
m_bant = BANT["kg_m2"] * W_BANT / 1000.0 * L_BANT / 1000.0
v_akt, a_akt = 300.0, 1200.0                                 # mm/s, mm/s²
F_yatak = m_pide * 9.81 * BANT["mu_celik"]
F_ivme = (m_pide + m_bant) * a_akt / 1000.0
F_bukme = 1.0                                                 # iki rulo sarımı + rulman sürtünmesi (bilyalı, VARSAYIM)
F_u = F_yatak + F_ivme + F_bukme
r_tahrik = D_R / 2.0 + BANT["t"] / 2.0
T_rulo = F_u * r_tahrik / 1000.0
T_rotor = T_rulo * ORAN / 0.95
T_tasarim = 3.0 * T_rotor
var("bükme + rulman direnci 1 N (bilyalı paslanmaz rulmanlar, düşük gerginlik)")
# kayma sınırı (burun rulosu 180° sarım, µ 0,18)
F_kayma = T_KOL * (math.exp(BANT["mu_celik"] * math.pi) - 1.0)
S["tork"] = dict(m_pide=m_pide, m_bant=m_bant, v=v_akt, a=a_akt, F_yatak=F_yatak, F_ivme=F_ivme, F_bukme=F_bukme, F_u=F_u,
                 T_rulo_Nm=T_rulo, T_rotor_Nm=T_rotor, T_tasarim_Nm=T_tasarim, F_kayma_siniri=F_kayma)
den("burun rulosunda bant kaymaz", F_kayma / F_u, "> 3 kat", F_kayma / F_u > 3.0)

# mıknatıslı kavrama (dipol modeli — VARSAYIM, deneme ile doğrulanacak)
MIK = dict(ad="supermagnete S-10-05-N · Ø10 × 5 N42 nikel · ~2,6 kg tutma", adet=6, d=10.0, h=5.0, Br=1.30, r_hatve=12.5)
kay("miknatis", "supermagnete S-10-05-N (Ø10×5, N42, ~2,6 kg) ürün sayfası; 316 kaba lazer kaynaklı kapakla GÖMÜLÜ (gıda teması yok)")
mu0 = 4e-7 * math.pi
V = math.pi * (MIK["d"] / 2000.0) ** 2 * (MIK["h"] / 1000.0)
m_ = MIK["Br"] / mu0 * V
r_cc = (MIK["h"] + BOSLUK_KAVRAMA) / 1000.0
F_eks = 3.0 * mu0 * m_ ** 2 / (2.0 * math.pi * r_cc ** 4)
F_kes = 0.45 * F_eks
T_kavrama = MIK["adet"] * F_kes * MIK["r_hatve"] / 1000.0
var("kavrama torku: eksenel dipol modeli, kesme = 0,45 × çekme, %d çift × r %.1f — gerçek değer ±%%50; masa denemesi (2 disk + tork anahtarı)" % (MIK["adet"], MIK["r_hatve"]))
S["kavrama"] = dict(miknatis=MIK, F_cekme_cift_N=F_eks, F_kesme_cift_N=F_kes, T_Nm=T_kavrama, eksenel_cekme_N=MIK["adet"] * F_eks,
                    pay=T_kavrama / T_tasarim)
den("mıknatıslı kavrama torku / tasarım torku", T_kavrama / T_tasarim, "> 1,5", T_kavrama / T_tasarim > 1.5)

# motor
MOTOR = dict(ad="NEMA23 kapalı çevrim step · STP-MTR-23079 (katalog STEP)", tutma_Nm=1.0)
kay("motor", "katalog/step/stp-mtr-23079.step (projede mevcut GERÇEK CAD); tutma ~1,0 N·m [V: föy]")
n_rotor = v_akt / (math.pi * (D_R + BANT["t"])) * 60.0 / ORAN
S["motor"] = dict(MOTOR, n_dev_dk=n_rotor, pay=MOTOR["tutma_Nm"] / T_tasarim)

# ================================================================ 6 · DÖNÜŞ DAİRESİ → AKTARMA KONUMU
# dönen en uç noktalar (yerel x, z): köşe yan sac, burun kasnağı, rotor
noktalar = {"yan_sac_kosesi": (X_N + 8.0, Z_YAN[1]), "burun_kasnagi": (X_N + (D_KASNAK / 2.0 + 0.8), -Z_KASNAK[0]),
            "rotor_miknatis": (X_ROTOR + D_MIKNATIS / 2.0, -Z_MIKNATIS[0]), "rotor_kasnagi": (X_ROTOR + D_KASNAK_R / 2.0 + 1.0, -Z_KASNAK[0] + 0.5),
            "kuyruk_kizagi": (X_K - 9.0, Z_YAN[1]), "yay_kutusu": (-142.0, 167.0)}
R_SUP = max(math.hypot(x, z) for x, z in noktalar.values())
S["donus"] = dict(noktalar={k: round(math.hypot(*v), 2) for k, v in noktalar.items()}, R=R_SUP, cap=2.0 * R_SUP)
PAY = 5.0
LB_SOL = SUCUK_X + R_SUP + PAY                  # yükleme bandı burnunun en sol yüzü
AKT = LB_SOL - 3.0 - X_UC                        # kaset burun ucu banda 3 mm
S["aktarma"] = dict(LB_sol=LB_SOL, AKT=AKT, fark_eski=AKT - AKT_ESKI, bosluk_bant=3.0)

# sabit tahrik konumu (dünya)
X_SUR = AKT + X_ROTOR
Z_SUR_YUZ = ZE + Z_SURUCU_YUZ
KUTU_DAR = dict(x=(X_SUR - 21.0, X_SUR + 21.0), y=(Y_ROTOR - 28.0, Y_ROTOR + 28.0), z=(-420.0, Z_SUR_YUZ))
KUTU_MOTOR = dict(x=(X_SUR - 31.0, X_SUR + 31.0), y=(Y_ROTOR - 31.0, Y_ROTOR + 31.0), z=(-508.0, -420.0))
S["sabit_tahrik"] = dict(X=X_SUR, Y=Y_ROTOR, Z_yuz=Z_SUR_YUZ, kutu_dar=KUTU_DAR, kutu_motor=KUTU_MOTOR)

# ================================================================ 7 · AÇIKLIKLAR (hesap; CAD denetimi gerçek katıyla ayrıca ölçer)
KAPI_Z, DIKME_Z = B["KAPI_Z"], 39.0
YARIK = B["YARIK_V2"][1]           # iç açıklık x 2491–2499,5 · y 987–1038 · z −409…−13
AGIZ = dict(x=2500.0, y=(984.0, 1042.0), z=(-341.0, -10.0))
ROTOR_ALT = Y_ROTOR - D_MIKNATIS / 2.0                        # 970: sucukta dönerken fırın tarafına süpüren EN ALÇAK parça (r > 198)
YARIK_YENI_ALT = ROTOR_ALT - 5.0                              # 965 (TOPPING v27: yarık contasının alt kenarı)
AGIZ_YENI_ALT = ROTOR_ALT - 5.0                               # 965 (fırın v9: ön kabuk ağzının alt kenarı)
kay("firin_agzi", "fırın v8 (ana klasör, izlenmiyor): kabuk 2500–2501,5 · ağız y 984–1042 · z −341…−10")
d_sur = math.hypot(KUTU_DAR["x"][0] - SUCUK_X, KUTU_DAR["z"][1] - ZE) - R_SUP
A = {
    "on_kapak (z 59)": KAPI_Z - (ZE + R_SUP),
    "orta_dikme (z 39) — BOŞLUK AÇILMAZSA": DIKME_Z - (ZE + R_SUP),
    "yukleme_bandi (sucukta dönüş)": LB_SOL - (SUCUK_X + R_SUP),
    "sabit_tahrik (sucukta dönüş)": d_sur,
    "sabit_tahrik ↔ yarık contası (x 2491)": 2491.0 - KUTU_DAR["x"][1],
    "yarık alt (987) ↔ dönüş kolu": DONUS_DIS - YARIK[2],
    "fırın ağzı alt (984) ↔ dönüş kolu": DONUS_DIS - AGIZ["y"][0],
    "sucukta dönen rotor kabı alt (970) ↔ BUGÜNKÜ yarık alt (987)": ROTOR_ALT - YARIK[2],
    "sucukta dönen rotor kabı alt (970) ↔ YENİ yarık / ağız alt (965)": ROTOR_ALT - YARIK_YENI_ALT,
    "yarık ön (−13) ↔ kaset ön yan sac": YARIK[5] - (ZE + Z_YAN[1]),
    "fırın ağzı ön (−10) ↔ kaset ön yan sac": AGIZ["z"][1] - (ZE + Z_YAN[1]),
    "fırın ağzı arka (−341) ↔ burun kasnağı": (ZE + Z_KASNAK[0]) - AGIZ["z"][0],
}
S["acikliklar"] = {k: round(v, 2) for k, v in A.items()}
AYAR = [
    dict(kod="a", ne="orta dikme: tabla hizasında (y 965–1012) 47 mm boşluk (kapaklar yine dikmenin kalanına dayanır)", neden="dönen köşe %.1f mm giriyor" % -A["orta_dikme (z 39) — BOŞLUK AÇILMAZSA"]),
    dict(kod="b", ne="fırın: yükleme bandı burnu x %.1f'den başlar (eski giriş bandı 2520,5) · ön kabuk ağzının alt kenarı 984 → %.0f" % (LB_SOL, AGIZ_YENI_ALT), neden="sucukta dönüşe %.0f mm pay · rotor kabı sucukta dönerken ağzın altından 970'e iner" % PAY),
    dict(kod="c", ne="TOPPING çıkış yarığı: alt kenar 987 → %.0f, ön kenar −13 → −8" % YARIK_YENI_ALT, neden="sucukta dönen rotor kabı 970'e iner (5 mm pay) · ön yan sac %.1f mm pay" % A["yarık ön (−13) ↔ kaset ön yan sac"]),
    dict(kod="d", ne="aktarma x %.0f → %.1f (+%.1f): ray sağ ucu 2485 → 2498, limit+ ve tampon +%.0f, araba plakası sağ kenarı −20" % (AKT_ESKI, AKT, AKT - AKT_ESKI, AKT - AKT_ESKI), neden="burun ucu yükleme bandına 3 mm"),
    dict(kod="e", ne="göbek + Ø340 tabla + çalışma diski + disk pimleri KALKAR; ayar bileziğine 2 × Ø8 konum pimi; tahrik lokması pimleri 958–966 → 958–983", neden="kaset doğrudan ayar bileziğine oturur"),
    dict(kod="f", ne="sabit tahrik kutusu TOPPING sağ-arka (x %.0f–%.0f, z %.0f…%.0f), braketi kayış kirişine" % (KUTU_MOTOR["x"][0], KUTU_MOTOR["x"][1], KUTU_MOTOR["z"][0], KUTU_DAR["z"][1]), neden="dönüş dairesinin dışı"),
]
S["ayarlar"] = AYAR

# ================================================================ 8 · AKTARMA ZAMANI
yol = (LB_SOL + PIDE_D / 2.0 + 5.0) - AKT            # pide merkezi kaset ortasından bandın tamamen üstüne
t_ivme = v_akt / a_akt
s_ivme = 0.5 * a_akt * t_ivme ** 2
t_akt = 2.0 * t_ivme + max(0.0, yol - 2.0 * s_ivme) / v_akt
S["zaman"] = dict(yol_mm=yol, t_aktarma_s=t_akt, t_ivme_s=t_ivme, yaklasma_mm=AKT - SUCUK_X)
den("aktarma süresi", t_akt, "< 1,6 s", t_akt < 1.6)

with io.open(os.path.join(U, "bantli_tabla_hesap_v1.json"), "w", encoding="utf-8") as f:
    json.dump(S, f, ensure_ascii=False, indent=1)
if __name__ == "__main__":
    print("dönüş Ø%.1f (R %.1f) · AKT %.1f (+%.1f) · LB sol %.1f · sabit tahrik x %.1f" % (2 * R_SUP, R_SUP, AKT, AKT - AKT_ESKI, LB_SOL, X_SUR))
    print("bant boyu %.1f · T/kol %.1f N · sarkma %.2f · rulo sehim %.3f · yatak sehim %.3f / %.3f" % (L_BANT, T_KOL, sarkma, sehim_rulo, S["yatak"]["en_kotu_serit_120"]["sehim_mm"], S["yatak"]["tam_genislik"]["sehim_mm"]))
    print("F_u %.2f N · T_rotor %.4f N·m · tasarım %.3f · kavrama %.3f N·m (pay %.1f) · kayma sınırı %.1f N · motor %.0f dev/dk" % (F_u, T_rotor, T_tasarim, T_kavrama, T_kavrama / T_tasarim, F_kayma, n_rotor))
    for k, v in S["acikliklar"].items(): print("  %-45s %7.2f" % (k, v))
    for d in S["denetim"]: print("  [%s] %s = %s (%s)" % ("OK" if d["gecti"] else "XX", d["ad"], d["deger"], d["sart"]))
    print("aktarma %.2f s · yol %.0f mm" % (t_akt, yol))
