# -*- coding: utf-8 -*-
"""topping_cad_v31 → v32 (30 Eyl 2026 · YEREL · Claude).
Kemal 30 Eyl (ekran görüntüsü, TOPPING ray yarığı): "bu rayın üstü kapanmalı, arasına hamur sos küp sucuk girmemeli · ilerlediği yerlerde belki süpürge gibi fırça"
→ "paslanmaz örtü bandı yap / yap işte ya doğru olanları hadi".
  · v31: HGH15CA (H 28) bloğun üstü = araba plakasının altı (y 48,5) · raylar 36 mm yarıklı iki L şeritle örtülüydü, blok yarıktan geçiyordu → düşen her şey
    doğrudan raya iniyordu. Örtü bandı ya da kapalı çatı bloğun üstünden geçemezdi (tabla yükselirse aktarma kotu 1000 bozulur).
  · v32: ALÇAK KIZAK HIWIN MGN15H (H 16, paslanmaz, katalog ölçüsüyle) → blok üstü 36,5 · plaka 48,5 YERİNDE (tabla, disk, aktarma kotu aynı) ·
    KAPALI RAY ÇATISI (304 1,5 tek parça bükme, üstte YARIK YOK, 3° dışa eğim) · KIZAK AYAĞI çatının altından yana çıkar, iç eteğin içinden iner,
    eteğin ALTINDAN dışarı geçip plakaya çıkar (ters kap labirent: düşen hiçbir şey giremez; örtü bandının kaldırma makarası / mıknatısı / gergisi / sıyırıcısı yok)
  · raylar −540…1793,5 (eşleştirilmiş ek · sert duruşlarda bloklar rayda) · blok hatvesi 160 · uçlar kapaklı
  · dönüş motoru plakaya oturdu (v31: plakayla 3 mm boşluk, tekne tabanına sürtüyordu) → tekne tabanından 3 mm
Yalnız okur: topping_cad_v31.py · yazar: topping_cad_v32.py"""
import io, os, sys

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v31.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a), n)
    s = s.replace(a, b)


def dilim(bas, son, yeni):
    """bas işaretinden (dahil) son işaretine (hariç) kadar olan bloğu değiştirir · iki işaret de tek olmalı"""
    global s
    assert s.count(bas) == 1 and s.count(son) == 1, (bas[:60], s.count(bas), son[:60], s.count(son))
    i, j = s.index(bas), s.index(son)
    assert i < j
    s = s[:i] + yeni + s[j:]


# ---------------------------------------------------------------- 0 · başlık
degis('"""topping_cad_v31 (30 Eyl 2026 · YEREL · yap_topping_cad_v31.py): ',
      '"""topping_cad_v32 (30 Eyl 2026 · YEREL · yap_topping_cad_v32.py): RAYIN ÜSTÜ TAMAMEN KAPALI — alçak kızak HIWIN MGN15H + kapalı paslanmaz ray çatısı + yandan dolanan kızak ayakları\n'
      'v32: Kemal 30 Eyl "bu rayın üstü kapanmalı, arasına hamur sos küp sucuk girmemeli" → "paslanmaz örtü bandı yap / doğru olanları yap": HGH15CA (H 28) bloğun üstü plakanın\n'
      '     altıydı → örtü de çatı da geçemezdi · MGN15H (H 16) → çatı bloğun üstünden geçer, ÜSTTE YARIK YOK · ayak eteğin altından dolanır (ters kap labirent) · plaka 48,5,\n'
      '     tabla, disk, aktarma kotu AYNI · raylar −540…1793,5 (ek 650 / 770) · blok hatvesi 160 · uç kapakları · dönüş motoru plakaya oturdu (tekne tabanından 3 mm)\n'
      'v31: topping_cad_v31 (30 Eyl 2026 · YEREL · yap_topping_cad_v31.py): ')

# ---------------------------------------------------------------- 1 · sabitler + yardımcılar (MOTOR_STEP satırından önce)
SABIT = r'''# ======================= v32 · ALÇAK KIZAK HIWIN MGN15H + KAPALI RAY ÇATISI (Kemal 30 Eyl) =======================
# "bu rayın üstü kapanmalı, arasına hamur sos küp sucuk girmemeli" → "paslanmaz örtü bandı yap / yap işte doğru olanları"
# v31: HGH15CA (H 28) → blok üstü = araba plakası altı (y 48,5) · 36 mm yarıklı iki L şerit, blok yarıktan geçiyordu → düşen her şey raya iniyordu.
#      Örtü bandı da kapalı çatı da bloğun üstünden geçemiyordu (tabla yükselir → aktarma kotu 1000 bozulur).
# v32: MGN15H (H 16) → blok üstü 36,5 · aradaki 12 mm'de ayak tabanı 3 + çatı (1,5, 3° eğim) + boşluklar · çatının ÜSTÜNDE YARIK YOK ·
#      ayak çatının ALTINDAN yana çıkar, iç eteğin içinden iner, eteğin ALTINDAN dışarı geçip plakaya çıkar (ters kap labirent: içeri girmek için
#      yukarı doğru gitmek gerekir, düşen hiçbir şey giremez) · örtü bandının istediği kaldırma makarası, mıknatıs, gergi, sıyırıcı YOK, aşınan örtü parçası yok.
MGN = dict(ad="HIWIN MGN15HZ0HM", H=16.0, H1=4.0, W=32.0, B=25.0, C=25.0, L1=43.4, L=58.8, dis="M3 × 4", kg=0.092, C_din=6370.0, C0=9110.0, M0X=73.5, M0Y=57.82, M0Z=57.82,
           kaynak="HIWIN MG serisi katalog G99TE17-1306 s. 80 (MGN15H) + hiwin.de ürün 5-001047: H 16 · H1 4 · W 32 · B 25 · C 25 · L1 43,4 · L 58,8 · M3 × 4 · "
                  "C 6,37 kN · C0 9,11 kN · M0X 73,5 · M0Y/M0Z 57,8 N·m · 0,09 kg · kod sonu M = paslanmaz (blok, ray, bilye, tutucu)")
MGNR = dict(ad="HIWIN MGNR15R…HM", WR=15.0, HR=10.0, D=6.0, h=4.5, d=3.5, P=40.0, E=15.0, E_min=6.0, E_max=34.0, civata="DIN 912 M3 × 10", kg_m=1.06, Lmax=1960.0,
            kaynak="HIWIN MG katalog s. 80 + hiwin.de 5-001090: WR 15 · HR 10 · D 6 · h 4,5 · d 3,5 · P 40 · E 15 (uç payı 6–34) · cıvata M3 × 10 · 1,06 kg/m · tek parça ≤ 1960 mm")
Y_KIRIS = 20.5                                              # ray kirişi üstü (kaynaktan sonra frezelenir)
Y_RAY = Y_KIRIS + MGNR["HR"]                                # 30,5
Y_BLOK = (Y_KIRIS + MGN["H1"], Y_KIRIS + MGN["H"])          # 24,5 … 36,5
Y_PLAKA = 48.5                                              # araba plakası altı · v31 ile AYNI (tabla, disk, aktarma kotu değişmez)
KIZAK_DX = 80.0                                             # blok ekseni Xc ± 80 (v31 ± 100): sert duruşlarda bloklar rayın üstünde kalır
RAY2_X = (-540.0, 1793.5)                                   # v31 H.RAY_X0/X1 −500…1798: sol sert duruşta blok raydan 51 mm taşıyordu · sağ uç kiriş / tekne ucunu (1795) 3 mm aşıyordu
RAY_EK = {"on": 650.0, "arka": 770.0}                       # eşleştirilmiş ray eki (tek parça ≤ 1960) · iki rayda şaşırtmalı
X_SERT = (-395.0, 1645.4 + 30.0)                          # sert duruş (tabla ekseni): SOL −395 = limit −380 + 15 aşım (v32 tampon takozu plakaya) · SAĞ tampon 1645,4 ↔ kayış kolunun sağ ucu (Xc − 30) = 1675,4
#   v31 sol tampon (x −580, Ø20, y 43,5–63,5) plakaya −420'de değecekti ama önce APRON (y 58,5–60,5, plakadan 40 mm solda) −380'de tampona giriyordu ve −420'de kayış kelepçesi
#   X kasnağına giriyordu (v32 X süpürmesi buldu) → v32: PU takoz 20 × 9 × 15 plakanın kalınlığında (y 49–58), apron 1 mm üstünden geçer, kelepçe kasnağa 5,5 mm kalır
AYAK_DX = 20.0                                              # kızak ayağı x boyu 40
AYAK = dict(taban=(-16.0, 23.0), ic=(19.0, 23.0), kol=(19.0, 39.0), dis=(35.0, 39.0), flans=(35.0, 47.0), y_kol=(22.0, 26.0), t_taban=3.0, t_flans=4.0)   # u = s·(z − zc), s: iç yön (rayların arası)
CATI = dict(t=1.5, egim=3.0, y_alt=40.0, u_dis=(-30.0, -28.5), u_ic=(28.0, 29.5), u_ayak=-20.0, y_etek=29.0)   # dış etek kirişin dış kenarında · iç etek iç kenarından 0,5 içeride
CATI_X = (RAY2_X[0] - 1.5, 1795.0)                          # uç kapakları dahil (sağda kiriş / tekne ucu 1795)
ACICI_F = 482.0                                             # N · açıcı silindiri Festo DSBC-32 × 6 bar (π/4 · 32² · 0,6) — kafa tablaya en çok bu kadar bastırır (yük denetimi, en kötü durum)
X_HAREKETLI_P = ("kizak_blogu_", "araba_plakasi", "doner_yatak", "ayar_bilezigi", "donus_motoru", "tahrik_lokmasi", "siyirici_apron", "kayis_kolu", "kayis_kelepcesi_",
                 "tabla_home_sensoru", "tabla_home_bayragi", "x_bayragi", "kilit_burcu_", "tabla_gobegi", "calisma_diski", "disk_pimi_", "bk_", "ayar_konum_pimi_", "merkezleme_pimi_")   # = montaj ARABA + TABLA
RAY_E, RAY_CIVATA = {}, {}                                  # modul() doldurur: ray parçası uç delik payları · cıvata sayısı (denetim okur)


def x_hareketli(ad):
    return ad == "tabla" or ad.startswith(X_HAREKETLI_P)


def _us(zc):
    return -1.0 if zc > -170.0 else 1.0                     # iç yön: iki rayın arasına (tabla ekseni z −170)


def _uk(x0, x1, zc, u0, u1, y0, y1):
    s_ = _us(zc); za, zb = zc + s_ * u0, zc + s_ * u1
    return kut(x0, x1, y0, y1, min(za, zb), max(za, zb))


def mgn_ray(x0, x1, zc, x_ek):
    """MGNR15R · 15 × 10 · iki yanda bilye yolu (gösterim oluğu 2,4 × 1) · iki parça, x_ek'te EŞLEŞTİRİLMİŞ EK · her parçada uçtan E 15, hatve 40 ·
    havşa Ø6 × 4,5 + geçme Ø3,5 · DIN 912 M3 × 10 (baş havşanın dibinde, üstü ray üstünün 1,5 altında; diş kirişte, çizilmedi)"""
    r_ = None; cv_ = None; n_ = 0; E_ = []
    for a_, b_ in ((x0, x_ek), (x_ek, x1)):
        p_ = kut(a_, b_, Y_KIRIS, Y_RAY, zc - MGNR["WR"] / 2.0, zc + MGNR["WR"] / 2.0)
        for s_ in (-1.0, 1.0):
            p_ = p_.cut(kut(a_ - 1.0, b_ + 1.0, Y_RAY - 3.7, Y_RAY - 1.3, zc + s_ * MGNR["WR"] / 2.0 - 1.0, zc + s_ * MGNR["WR"] / 2.0 + 1.0))
        xd_ = a_ + MGNR["E"]; son_ = xd_
        while xd_ <= b_ - MGNR["E_min"] + 1e-6:
            p_ = p_.cut(sily(xd_, zc, MGNR["D"] / 2.0, Y_RAY - MGNR["h"], Y_RAY + 1.0)).cut(sily(xd_, zc, MGNR["d"] / 2.0, Y_KIRIS - 1.0, Y_RAY))
            _alyan = cq.Workplane("XZ").center(xd_, zc).polygon(6, 2.5 / math.cos(math.radians(30.0))).extrude(-1.5).translate((0, Y_RAY - MGNR["h"] + 3.0 - 1.5, 0))
            b2_ = sily(xd_, zc, 2.75, Y_RAY - MGNR["h"], Y_RAY - MGNR["h"] + 3.0).cut(_alyan).union(sily(xd_, zc, 1.5, Y_KIRIS, Y_RAY - MGNR["h"]))
            cv_ = b2_ if cv_ is None else cv_.union(b2_); n_ += 1; son_ = xd_
            xd_ += MGNR["P"]
        E_.append((round(MGNR["E"], 2), round(b_ - son_, 2), round(b_ - a_, 2)))
        r_ = p_ if r_ is None else r_.union(p_)
    return r_, cv_, n_, E_


def mgn_blok(xb, zc):
    """MGN15H katalog ölçüsüyle (STEP indirilmedi · HIWIN 3B dosyası gelirse aynı ölçüde yerine konur): çelik gövde L1 43,4 · iki plastik uç kapağı + conta
    (L 58,8'e tamamlar) · W 32 · H1 4 · H 16 · rayı saran kanal (tavanı ray üstüne, yanları ray yanına değer)"""
    y0, y1 = Y_BLOK; w2 = MGN["W"] / 2.0
    kanal = kut(xb - 40.0, xb + 40.0, y0 - 1.0, Y_RAY, zc - MGNR["WR"] / 2.0, zc + MGNR["WR"] / 2.0)
    g_ = kut(xb - MGN["L1"] / 2.0, xb + MGN["L1"] / 2.0, y0, y1, zc - w2, zc + w2).cut(kanal)
    uc_ = []
    for s_ in (-1.0, 1.0):
        xa_, xe_ = sorted((xb + s_ * MGN["L1"] / 2.0, xb + s_ * MGN["L"] / 2.0))
        uc_.append(kut(xa_, xe_, y0 + 0.5, y1 - 0.5, zc - w2 + 0.5, zc + w2 - 0.5).cut(kanal))
    return g_, uc_


def kizak_ayagi(xb, zc):
    """v32 · KIZAK AYAĞI · 304, 4 mm (tel erozyon), 40 mm boy · blok üstü → çatının ALTINDA iç yana → iç eteğin İÇİNDEN aşağı →
    eteğin ALTINDAN dışarı (alt kol, kirişin 1,5 üstünde) → eteğin DIŞINDA yukarı → üst flanş araba plakasının altına"""
    x0, x1 = xb - AYAK_DX, xb + AYAK_DX; A_ = AYAK; yb = Y_BLOK[1]
    a_ = _uk(x0, x1, zc, A_["taban"][0], A_["taban"][1], yb, yb + A_["t_taban"])
    a_ = a_.union(_uk(x0, x1, zc, A_["ic"][0], A_["ic"][1], A_["y_kol"][0], yb + A_["t_taban"]))
    a_ = a_.union(_uk(x0, x1, zc, A_["kol"][0], A_["kol"][1], A_["y_kol"][0], A_["y_kol"][1]))
    a_ = a_.union(_uk(x0, x1, zc, A_["dis"][0], A_["dis"][1], A_["y_kol"][0], Y_PLAKA))
    a_ = a_.union(_uk(x0, x1, zc, A_["flans"][0], A_["flans"][1], Y_PLAKA - A_["t_flans"], Y_PLAKA))
    return a_


def _cati_y(u, ust=False):
    C_ = CATI; y_ = C_["y_alt"] + (u - C_["u_dis"][1]) * math.tan(math.radians(C_["egim"]))
    return y_ + (C_["t"] / math.cos(math.radians(C_["egim"])) if ust else 0.0)


def ray_catisi(zc):
    """v32 · RAY ÇATISI · 304 1,5 tek parça bükme: kirişe vidalı ayak + dış etek + 3° dışa eğimli üst (su dışa akar, labirentten uzağa) + iç damlama eteği (y 29) ·
    ÜSTTE YARIK YOK"""
    C_ = CATI; s_ = _us(zc)
    P_ = [(C_["u_ayak"], Y_KIRIS), (C_["u_ayak"], Y_KIRIS + C_["t"]), (C_["u_dis"][1], Y_KIRIS + C_["t"]), (C_["u_dis"][1], _cati_y(C_["u_dis"][1])),
          (C_["u_ic"][0], _cati_y(C_["u_ic"][0])), (C_["u_ic"][0], C_["y_etek"]), (C_["u_ic"][1], C_["y_etek"]), (C_["u_ic"][1], _cati_y(C_["u_ic"][1], True)),
          (C_["u_dis"][0], _cati_y(C_["u_dis"][0], True)), (C_["u_dis"][0], Y_KIRIS)]
    return cq.Workplane("YZ").polyline([(y_, zc + s_ * u_) for u_, y_ in P_]).close().extrude(CATI_X[1] - CATI_X[0]).translate((CATI_X[0], 0.0, 0.0))


def ray_catisi_kapagi(zc, x0, x1):
    """v32 · çatının uç kapağı: çatının iç kesitini (etek altı dahil) kapatır"""
    C_ = CATI; s_ = _us(zc)
    P_ = [(C_["u_ayak"], Y_KIRIS), (C_["u_ic"][1], Y_KIRIS), (C_["u_ic"][1], C_["y_etek"]), (C_["u_ic"][0], C_["y_etek"]), (C_["u_ic"][0], _cati_y(C_["u_ic"][0])),
          (C_["u_dis"][1], _cati_y(C_["u_dis"][1])), (C_["u_dis"][1], Y_KIRIS + C_["t"]), (C_["u_ayak"], Y_KIRIS + C_["t"])]
    return cq.Workplane("YZ").polyline([(y_, zc + s_ * u_) for u_, y_ in P_]).close().extrude(x1 - x0).translate((x0, 0.0, 0.0))


'''
degis('MOTOR_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "stp-mtr-23079.step")\n',
      SABIT + 'MOTOR_STEP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "katalog", "step", "stp-mtr-23079.step")\n')

# ---------------------------------------------------------------- 2 · ray kirişi notu
degis('"kaynaktan SONRA üç üst yüzey TEK BAĞLAMADA frezelenir (düzlemlik 0,1 mm/m — HGR15 şartı)"',
      '"kaynaktan SONRA üç üst yüzey TEK BAĞLAMADA frezelenir (düzlemlik 0,1 mm/m · v32: MGN15 raylar — HIWIN MG montaj toleransıyla teyit [V])"')

# ---------------------------------------------------------------- 3 · 8b.2 LİNEER KIZAK → MGN15H + ayaklar
KIZAK = r'''    # --- 8b.2 LİNEER KIZAK · v32: ALÇAK HIWIN MGN15H (Kemal 30 Eyl: "rayın üstü kapanmalı, arasına hamur sos küp sucuk girmemeli") ---
    # v31 HGH15CA (H 28) bloğun üstü plakanın altıydı → örtü de çatı da geçemiyordu. MGN15H (H 16): blok üstü 36,5 · plaka 48,5 YERİNDE (tabla kotu aynı).
    _RY = {ad_: mgn_ray(RAY2_X[0], RAY2_X[1], zc_, RAY_EK[ad_]) for ad_, zc_ in (("on", -65.0), ("arka", -275.0))}
    RAY_E.clear(); RAY_CIVATA.clear()
    for ad_ in ("on", "arka"):
        _r, _cv, _say, _E = _RY[ad_]
        RAY_E[ad_] = _E; RAY_CIVATA[ad_] = _say
        ekle("lineer_ray_%s" % ad_, _r, "celik",
             bom=("Lineer ray %s × %.1f (iki parça, eşleştirilmiş ek)" % (MGNR["ad"], RAY2_X[1] - RAY2_X[0]), 2,
                  "paslanmaz · ön %.0f + %.1f · arka %.0f + %.1f mm (tek parça ≤ %.0f, ekler şaşırtmalı) · %s"
                  % (RAY_EK["on"] - RAY2_X[0], RAY2_X[1] - RAY_EK["on"], RAY_EK["arka"] - RAY2_X[0], RAY2_X[1] - RAY_EK["arka"], MGNR["Lmax"], MGNR["kaynak"]),
                  "v32 · HGR15 yerine (12 mm alçak blok için) · ray kirişine %s · sol sert duruşta blok raydan taşmaz (v31: 51 mm taşıyordu)" % MGNR["civata"]) if ad_ == "on" else None)
        ekle("lineer_ray_%s_civatalari" % ad_, _cv, "celik",
             bom=("Cıvata %s · A2 paslanmaz (ray bağlantısı)" % MGNR["civata"], sum(v_[2] for v_ in _RY.values()), "havşa Ø6 × 4,5 dibinde · hatve 40 · uçtan 15",
                  "ray kirişine (dişli) · v32") if ad_ == "on" else None)
    for i_, (xb, zc_) in enumerate([(Xc - KIZAK_DX, -65.0), (Xc + KIZAK_DX, -65.0), (Xc - KIZAK_DX, -275.0), (Xc + KIZAK_DX, -275.0)]):
        _g, _uc = mgn_blok(xb, zc_)
        ekle("kizak_blogu_%d" % i_, _g, "celik",
             bom=("Kızak bloğu %s" % MGN["ad"], 4, "paslanmaz · katalog ölçüsüyle modellendi (STEP indirilmedi) · %s" % MGN["kaynak"],
                  "v32 · HGH15CA yerine (H 28 → 16) · hatve %.0f (v31: 200) · uçta çift dudaklı conta + alt conta · Z0 ön yük" % (2.0 * KIZAK_DX)) if i_ == 0 else None)
        for j_, u_ in enumerate(_uc):
            ekle("kizak_blogu_%d_uc_%s" % (i_, "ab"[j_]), u_, "koyu",
                 bom=("Blok uç kapağı + conta (bloğun parçası)", 8, "plastik uç kapağı + conta · bilye dönüş kanalı", "v32 · MGN15H'nin kendi parçası (ayrı sipariş yok)") if i_ == 0 and j_ == 0 else None)
        ekle("kizak_blogu_%d_ayagi" % i_, kizak_ayagi(xb, zc_), "celik",
             bom=("Kızak ayağı · AISI 304 4 mm · 40 boy", 4, "tel erozyon · bloğa 4 × M3 × 6 havşa (DIN 7991, bloğun M3 × 4 dişine) · plakadan 2 × M4 × 12 havşa",
                  "v32 · blok ↔ araba plakası: çatının altından yana → iç eteğin içinden aşağı → eteğin altından dışarı → yukarı plakaya (ters kap labirent) · "
                  "yükseklik 12 = plaka 48,5 − blok üstü 36,5 → tabla kotu aynı") if i_ == 0 else None)
'''
dilim("    # --- 8b.2 LİNEER KIZAK ---\n", "    apl = kut(Xc - 150.0, Xc + 130.0, 48.5, 58.5, -25.0, -315.0)", KIZAK)

# ---------------------------------------------------------------- 4 · dönüş motoru plakaya · lokma
degis('    ekle("donus_motoru", kut(Xc - 28.5, Xc + 28.5, 4.5, 45.5, ZT - 28.5, ZT + 28.5), "motor",',
      '    ekle("donus_motoru", kut(Xc - 28.5, Xc + 28.5, Y_PLAKA - 41.0, Y_PLAKA, ZT - 28.5, ZT + 28.5), "motor",   # v32: plakaya oturur (v31 4,5–45,5: plakayla 3 mm boşluk, tekne tabanına sürtüyordu)')
degis('    lk = sily(Xc, ZT, 15.0, 45.5, 66.0).cut(sily(Xc, ZT, 4.1, 45.0, 67.0))',
      '    lk = sily(Xc, ZT, 15.0, Y_PLAKA, 66.0).cut(sily(Xc, ZT, 4.1, Y_PLAKA - 0.5, 67.0))   # v32: motor 3 yukarı → lokma 48,5–66')
degis('bom=("Tahrik lokması Ø30 × 20", 1,', 'bom=("Tahrik lokması Ø30 × 17,5", 1,')

# ---------------------------------------------------------------- 4b · sol uç tamponu (v32 X süpürmesi: v31'de apron −380'de tampona, kelepçe −420'de kasnağa giriyordu)
degis('''    ekle("uc_tamponu_0", silz(H.X_LIMIT_SOL - 200.0, 53.5, 10.0, -80.0, -65.0), "silikon",
         bom=("Uç tamponu Ø20 × 15 (sol)", 1, "poliüretan + 304 braket", "ARABA PLAKASINA çarpar, bloklara değil"))
    ekle("uc_tamponu_0_braketi", kut(H.X_LIMIT_SOL - 210.0, H.X_LIMIT_SOL - 190.0, 20.5, 43.5, -82.0, -63.0), "celik",
         bom=("Uç tamponu braketi 304", 1, "20 × 23 × 19 · ön ray kirişinin üstüne 2 × M5", "v25 · tampon v24'te havadaydı"))''',
      '''    ekle("uc_tamponu_0", kut(X_SERT[0] - 170.0, X_SERT[0] - 150.0, 49.0, 58.0, -80.0, -65.0), "silikon",   # v32: PU takoz plakanın kalınlığında (v31 Ø20 y 43,5–63,5 · x −580)
         bom=("Uç tamponu PU takoz 20 × 9 × 15 (sol)", 1, "poliüretan 90 ShA + 304 braket",
              "ARABA PLAKASINA çarpar: tabla ekseni %.0f = limit %.0f + %.0f aşım · apron (y 58,5) 0,5 mm üstünden geçer · kayış kelepçesi X kasnağına 5,5 mm kalır (v31: apron −380'de tampona, kelepçe −420'de kasnağa giriyordu)"
              % (X_SERT[0], H.X_LIMIT_SOL, H.X_LIMIT_SOL - X_SERT[0])))
    ekle("uc_tamponu_0_braketi", kut(X_SERT[0] - 170.0, X_SERT[0] - 150.0, 20.5, 49.0, -82.0, -63.0), "celik",
         bom=("Uç tamponu braketi 304", 1, "20 × 28,5 × 19 · ön ray kirişinin üstüne 2 × M5", "v32 · takozla birlikte 25 sağa (ray çatısının uç kapağından 3,5 solda)"))''')

# ---------------------------------------------------------------- 5 · 8b.6 ray örtü şeritleri → KAPALI ÇATI + uç kapakları
CATI_KOD = r'''    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):          # v32 · KAPALI RAY ÇATISI (v25–v31: 36 mm yarıklı iki L şerit, araba bloğu yarıktan geçiyordu)
        ekle("ray_ortu_catisi_%s" % ad_, ray_catisi(zc_), "sac",
             bom=("Ray çatısı · AISI 304 1,5 tek parça bükme", 2, "boy %.1f · kirişe vidalı ayak (12 × M3 × 6 ISO 7380) + dış etek · üst 3° dışa eğimli · iç damlama eteği y %.0f'a iner"
                  % (CATI_X[1] - CATI_X[0], CATI["y_etek"]),
                  "v32 · Kemal 30 Eyl \"rayın üstü kapanmalı, arasına hamur sos küp sucuk girmemeli\": ÜSTTE YARIK YOK · kızak ayakları iç eteğin ALTINDAN dolanır "
                  "(ters kap labirent: düşen hiçbir şey giremez) · temizlik: 12 vida sökülür, çatı kalkar") if ad_ == "on" else None)
        for u_, (xa_, xe_) in (("sol", (CATI_X[0], RAY2_X[0])), ("sag", (RAY2_X[1], CATI_X[1]))):
            ekle("ray_ortu_kapagi_%s_%s" % (ad_, u_), ray_catisi_kapagi(zc_, xa_, xe_), "sac",
                 bom=("Ray çatısı uç kapağı · AISI 304 1,5", 4, "çatının iç kesitini (etek altı dahil) kapatır · 2 × M3 çatıya", "v32 · ray ucu kapalı · blok sert duruşta kapaktan ≥ 8 mm")
                 if (ad_, u_) == ("on", "sol") else None)
'''
dilim('    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):\n        ct = kut(-520.0, 1790.0, 20.5, 44.0,', '    ekle("kirinti_cekmecesi"', CATI_KOD)

# ---------------------------------------------------------------- 6 · bağlantı elemanları listesi
degis('("_bom_civata", "Bağlantı elemanları (tümü A4/A2 paslanmaz)", 180,', '("_bom_civata", "Bağlantı elemanları (tümü A4/A2 paslanmaz)", 260,')
degis('"ray 54 × M4×16 · blok 16 × M4×20 · ', '"v32: ray 118 × M3×10 · kızak ayağı 16 × M3×6 havşa (bloğa) + 8 × M4×12 havşa (plakadan) · ')
degis(' · çatı 24 × M4×8 · ', ' · ray çatısı 24 × M3×6 ISO 7380 + uç kapağı 8 × M3 · ')

# ---------------------------------------------------------------- 7 · kinematik denetim: referans v31 · raylar ayrı denetimde
degis('        V24 = importlib.import_module("topping_cad_v30"); V24.PARCALAR[:] = []; V24.modul()      # v31: referans v30',
      '        V24 = importlib.import_module("topping_cad_v31"); V24.PARCALAR[:] = []; V24.modul()      # v32: referans v31 (raylar MGN15 → ayrı denetim)      # v31: referans v30')
degis('        for ad in ("acici_konisi_on", "acici_konisi_arka", "lineer_ray_on", "lineer_ray_arka", "araba_plakasi", "doner_yatak", "ayar_bilezigi", "st_tahrik_diski", "st_tahrik_kutusu", "st_tahrik_motoru"):',
      '        for ad in ("acici_konisi_on", "acici_konisi_arka", "araba_plakasi", "doner_yatak", "ayar_bilezigi", "st_tahrik_diski", "st_tahrik_kutusu", "st_tahrik_motoru") + tuple(p_["ad"] for p_ in PARCALAR if p_["ad"].startswith("bk_")):   # v32: + bantlı tabla kaseti (gıda yüzeyi) · raylar 9b denetiminde')
degis('        k("v31 · kinematik v30 ile aynı (koniler, 2 ray, araba, döner yatak, ayar bileziği, sabit tahrik diski / kutusu / motoru)',
      '        k("v32 · kinematik v31 ile aynı (koniler, araba plakası, döner yatak, ayar bileziği, sabit tahrik diski / kutusu / motoru + bantlı tabla kasetinin %d parçası = gıda yüzeyi · raylar MGN15 → 9b)" % sum(1 for p_ in PARCALAR if p_["ad"].startswith("bk_")) + "')

# ---------------------------------------------------------------- 8 · 9b · X EKSENİ DENETİMİ (yerel TC ölçüleri)
DENETIM = r'''

def x_ekseni_denetimi(k):
    """v32 · X EKSENİ: alçak kızak + kapalı ray çatısı + kızak ayakları (yerel TC ölçüleri · modul() çalışmış olmalı)"""
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as DSS
    t0_ = time.time()
    P_ = {p["ad"]: _tek(p["wp"]) for p in PARCALAR if not p["ad"].startswith("_bom") and not eski(p["ad"])}
    B_ = {a: sh.BoundingBox() for a, sh in P_.items()}
    def mes(a, b, dx=0.0):
        sa = P_[a] if not dx else P_[a].translate(cq.Vector(dx, 0.0, 0.0))
        d_ = DSS(sa.wrapped, P_[b].wrapped); d_.Perform(); return d_.Value()
    # 1 · katalog
    g0, ua, ub, r0 = B_["kizak_blogu_0"], B_["kizak_blogu_0_uc_a"], B_["kizak_blogu_0_uc_b"], B_["lineer_ray_on"]
    L_ = max(ua.xmax, ub.xmax) - min(ua.xmin, ub.xmin)
    parca = [e_[2] for v_ in RAY_E.values() for e_ in v_]
    Eler = [e_[j_] for v_ in RAY_E.values() for e_ in v_ for j_ in (0, 1)]
    ok_ = (abs(g0.ymin - Y_BLOK[0]) < 0.01 and abs(g0.ymax - Y_BLOK[1]) < 0.01 and abs(g0.zlen - MGN["W"]) < 0.01 and abs(g0.xlen - MGN["L1"]) < 0.01 and abs(L_ - MGN["L"]) < 0.01
           and abs(r0.ylen - MGNR["HR"]) < 0.01 and abs(r0.zlen - MGNR["WR"]) < 0.01 and max(parca) <= MGNR["Lmax"] and MGNR["E_min"] <= min(Eler) and max(Eler) <= MGNR["E_max"])
    k("v32 · KIZAK KATALOG: %s blok y %.1f–%.1f (H %.0f · v31 HGH15CA 28) · W %.0f · L1 %.1f · L %.1f · ray %s %.0f × %.0f · parçalar %s mm (≤ %.0f) · uç delik payı %.1f–%.1f (%.0f–%.0f) · %d × %s"
      % (MGN["ad"], g0.ymin, g0.ymax, g0.ymax - Y_KIRIS, g0.zlen, g0.xlen, L_, MGNR["ad"], r0.zlen, r0.ylen, " / ".join("%.1f" % p_ for p_ in parca), MGNR["Lmax"],
         min(Eler), max(Eler), MGNR["E_min"], MGNR["E_max"], sum(RAY_CIVATA.values()), MGNR["civata"]), ok_)
    # 2 · tabla kotu
    ap, dm = B_["araba_plakasi"], B_["donus_motoru"]
    bk_y = max(B_[a].ymax for a in B_ if a.startswith("bk_"))                     # bantlı tabla kaseti (gıda yüzeyi) · v31 ile birebir: kinematik denetimi
    tk_y = B_["mekanizma_teknesi"].ymin + 3.0                                   # tekne tabanı üstü (1,5 + 3)
    k("v32 · TABLA KOTU DEĞİŞMEDİ: araba plakası y %.1f–%.1f · bantlı tabla kaseti en üst y %.1f (dünya %.1f · 50 parça v31 ile birebir → kinematik) · ayak yüksekliği %.1f = plaka %.1f − blok üstü %.1f · dönüş motoru plakaya oturur (y %.1f–%.1f), tekne tabanından %.1f mm (v31: 0, sürtüyordu)"
      % (ap.ymin, ap.ymax, bk_y, bk_y + DY_D, Y_PLAKA - Y_BLOK[1], Y_PLAKA, Y_BLOK[1], dm.ymin, dm.ymax, dm.ymin - tk_y),
      abs(ap.ymin - 48.5) < 0.001 and abs(ap.ymax - 58.5) < 0.001 and abs(dm.ymax - Y_PLAKA) < 0.001 and dm.ymin - tk_y >= 2.99)
    # 3 · bağlantılar (temas ≤ 0,05)
    CIFT = []
    for i_ in range(4):
        r_ = "lineer_ray_on" if i_ < 2 else "lineer_ray_arka"
        CIFT += [("kizak_blogu_%d_ayagi" % i_, "kizak_blogu_%d" % i_), ("kizak_blogu_%d_ayagi" % i_, "araba_plakasi"), ("kizak_blogu_%d" % i_, r_),
                 ("kizak_blogu_%d_uc_a" % i_, "kizak_blogu_%d" % i_), ("kizak_blogu_%d_uc_b" % i_, "kizak_blogu_%d" % i_)]
    for ad_ in ("on", "arka"):
        CIFT += [("lineer_ray_%s" % ad_, "ray_kirisi_%s" % ad_), ("lineer_ray_%s_civatalari" % ad_, "lineer_ray_%s" % ad_), ("ray_ortu_catisi_%s" % ad_, "ray_kirisi_%s" % ad_),
                 ("ray_ortu_kapagi_%s_sol" % ad_, "ray_ortu_catisi_%s" % ad_), ("ray_ortu_kapagi_%s_sag" % ad_, "ray_ortu_catisi_%s" % ad_)]
    CIFT += [("donus_motoru", "araba_plakasi"), ("tahrik_lokmasi", "donus_motoru")]
    bd_ = [(a, b, round(mes(a, b), 3)) for a, b in CIFT]
    k("v32 · BAĞLANTILAR (%d çift ≤ 0,05 mm): ayak ↔ blok üstü · ayak flanşı ↔ plaka · blok ↔ ray · uç kapağı ↔ blok · ray ↔ kiriş · cıvata ↔ ray · çatı ayağı ↔ kiriş · uç kapağı ↔ çatı · motor ↔ plaka · lokma ↔ motor"
      % len(bd_), all(d_ <= 0.05 for a, b, d_ in bd_), str([x for x in bd_ if x[2] > 0.05][:6]))
    # 4 · ÜSTTEN KAPALI: rayın + bloğun + ayak tabanının üstünden inen düşey ışınlar çatıya çarpar
    acik = []; n_ = 0
    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):
        s_ = _us(zc_); cati = P_["ray_ortu_catisi_%s" % ad_]
        xs_ = [RAY2_X[0] + 0.5] + [RAY2_X[0] + 100.0 * i_ for i_ in range(1, 24)] + [RAY2_X[1] - 0.5]
        for x_ in xs_:
            for j_ in range(0, 91):
                u_ = -16.0 + 0.5 * j_                                                # u −16 … +29 (blok + ayak tabanı + iç etek)
                e_ = cq.Edge.makeLine(cq.Vector(x_, 70.0, zc_ + s_ * u_), cq.Vector(x_, Y_RAY + 0.1, zc_ + s_ * u_))
                d_ = DSS(cati.wrapped, e_.wrapped); d_.Perform(); n_ += 1
                if d_.Value() > 1e-6: acik.append((ad_, round(x_, 1), u_))
    k("v32 · ÜSTTEN KAPALI: rayın, bloğun ve ayak tabanının üstü (u −16…+29, 2 ray × 25 kesit × 91 = %d düşey ışın, x %.1f…%.1f) çatıya çarpar · açık ışın %d (v31: 36 mm yarık boydan boya)"
      % (n_, RAY2_X[0], RAY2_X[1], len(acik)), not acik, str(acik[:6]))
    # 5 · labirent ölçüleri (park konumu)
    d_cati = min(mes("kizak_blogu_%d_ayagi" % i_, "ray_ortu_catisi_%s" % ("on" if i_ < 2 else "arka")) for i_ in range(4))
    d_blok = min(mes("kizak_blogu_%d" % i_, "ray_ortu_catisi_%s" % ("on" if i_ < 2 else "arka")) for i_ in range(4))
    d_plk = min(mes("araba_plakasi", "ray_ortu_catisi_%s" % a_) for a_ in ("on", "arka"))
    d_kir = min(mes("kizak_blogu_%d_ayagi" % i_, "ray_kirisi_%s" % ("on" if i_ < 2 else "arka")) for i_ in range(4))
    k("v32 · LABİRENT: iç etek altı y %.1f · ayak alt kolu y %.1f–%.1f (etekten %.1f · kirişten %.1f) · ayak ↔ çatı en az %.2f mm · blok ↔ çatı %.2f · plaka ↔ çatı %.2f · çatı üstü en yüksek y %.2f (plaka %.1f) · "
      "dış etek kirişin dış kenarında, iç etek iç kenarından 0,5 içeride (kiriş üstünde açık raf yok) · su dışa akar (3°)"
      % (CATI["y_etek"], AYAK["y_kol"][0], AYAK["y_kol"][1], CATI["y_etek"] - AYAK["y_kol"][1], AYAK["y_kol"][0] - Y_KIRIS, d_cati, d_blok, d_plk, max(B_["ray_ortu_catisi_on"].ymax, B_["ray_ortu_catisi_arka"].ymax), Y_PLAKA),
      d_cati >= 1.0 and d_blok >= 1.0 and d_plk >= 3.0 and d_kir >= 1.0)
    # 6 · X SÜPÜRME (sol sert duruş → sağ sert duruş) · hareketli = montajın ARABA + TABLA grubu, alt bölge (y < 70)
    HAR = [a for a in P_ if x_hareketli(a) and B_[a].ymin < 70.0]
    SAB = [a for a in P_ if not x_hareketli(a) and B_[a].ymin < 70.0 and B_[a].zmax > -430.0 and B_[a].zmin < 5.0 and B_[a].xmax > -620.0 and B_[a].xmin < 1810.0]
    UZUN = [a for a in SAB if B_[a].xlen >= 1500.0]                             # x boyunca prizmatik uzun sabitler (tekne, kirişler, raylar, çatılar, kayış...) → anahtar konumlarda
    ANAHTAR = sorted({round(X_SERT[0], 1), round(H.X_LIMIT_SOL, 1), round(H.X_PARK, 1), 650.0, 770.0, round(H.X_AKTARMA, 1), 1675.0, round(X_SERT[1], 1)})
    KONUM = sorted(set(ANAHTAR) | {round(X_SERT[0] + 20.0 * i_, 1) for i_ in range(int((X_SERT[1] - X_SERT[0]) / 20.0) + 1)})
    RAYCIFT = {(("kizak_blogu_%d" % i_) if j_ == "" else ("kizak_blogu_%d_uc_%s" % (i_, j_)), "lineer_ray_%s" % ("on" if i_ < 2 else "arka")) for i_ in range(4) for j_ in ("", "a", "b")}
    bulgu = []; n_cift = 0
    for X_ in KONUM:
        dx = X_ - XC_TABLA
        for a in HAR:
            ba = B_[a]
            for c in (SAB if X_ in ANAHTAR else [c_ for c_ in SAB if c_ not in UZUN]):
                bc = B_[c]
                if (a, c) in RAYCIFT: continue                                        # blok ↔ kendi rayı: kayar temas (kanal = ray kesiti) → ayrıca ray bandı denetimi
                if ba.xmax + dx < bc.xmin or bc.xmax < ba.xmin + dx or ba.ymax < bc.ymin or bc.ymax < ba.ymin or ba.zmax < bc.zmin or bc.zmax < ba.zmin: continue
                n_cift += 1
                try: v_ = P_[a].translate(cq.Vector(dx, 0.0, 0.0)).intersect(P_[c]).Volume()
                except Exception: v_ = -1.0
                if v_ > 0.5 or v_ < 0: bulgu.append((X_, a, c, round(v_, 1)))
    # ray bandı (u ±7,5 · y < 30,5): hareketli hiçbir şey girmez → ray cıvataları ve ray kesiti bütün strokta serbest (x'ten bağımsız)
    bant = []
    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):
        sl_ = kut(-700.0, 1900.0, Y_KIRIS - 1.0, Y_RAY, zc_ - MGNR["WR"] / 2.0, zc_ + MGNR["WR"] / 2.0).val()
        for a in HAR:
            if B_[a].ymin >= Y_RAY or B_[a].zmax < zc_ - 7.5 or B_[a].zmin > zc_ + 7.5: continue
            v_ = P_[a].intersect(sl_).Volume()
            if v_ > 0.01: bant.append((a, round(v_, 2)))
    k("v32 · X SÜPÜRME: %d hareketli (ARABA + TABLA, y < 70) · %d konum (sert duruş %.1f … %.1f, adım 20 + limit / park / ek / aktarma) · %d sabit (%d uzun prizmatik anahtar konumlarda) · %d çift ölçüldü · çakışma %d · ray bandı (u ±7,5, y < 30,5) hareketliden boş: %s"
      % (len(HAR), len(KONUM), X_SERT[0], X_SERT[1], len(SAB), len(UZUN), n_cift, len(bulgu), "EVET" if not bant else bant[:4]), not bulgu and not bant, str(bulgu[:8]))
    # 7 · sert duruşlarda bloklar rayda · yeni parçaların en küçük açıklığı
    sol_ = X_SERT[0] - KIZAK_DX - MGN["L"] / 2.0; sag_ = X_SERT[1] + KIZAK_DX + MGN["L"] / 2.0
    YENI = [a for a in HAR if a.startswith("kizak_blogu_")] + ["donus_motoru"]
    acik_ = []
    for X_ in (X_SERT[0], H.X_PARK, 650.0, 770.0, H.X_AKTARMA, X_SERT[1]):
        dx = X_ - XC_TABLA
        for a in YENI:
            ba = B_[a]
            for c in SAB:
                if (a, c) in RAYCIFT: continue
                bc = B_[c]
                if ba.xmax + dx < bc.xmin - 5.0 or bc.xmax + 5.0 < ba.xmin + dx or ba.ymax < bc.ymin - 5.0 or bc.ymax + 5.0 < ba.ymin or ba.zmax < bc.zmin - 5.0 or bc.zmax + 5.0 < ba.zmin: continue
                acik_.append((round(mes(a, c, dx), 2), X_, a, c))
    acik_.sort()
    k("v32 · SERT DURUŞLARDA BLOK RAYDA: sol (tabla %.1f) blok ucu %.1f ≥ ray başı %.1f (%.1f) · sağ (tabla %.1f) %.1f ≤ ray sonu %.1f (%.1f) · yeni parçalar (blok, uç kapağı, ayak, motor) ↔ sabitler en küçük açıklık %.2f mm (%s ↔ %s, x %.1f) ≥ 1"
      % (X_SERT[0], sol_, RAY2_X[0], sol_ - RAY2_X[0], X_SERT[1], sag_, RAY2_X[1], RAY2_X[1] - sag_, acik_[0][0], acik_[0][2], acik_[0][3], acik_[0][1]),
      sol_ >= RAY2_X[0] + 5.0 and sag_ <= RAY2_X[1] - 5.0 and acik_[0][0] >= 1.0, str(acik_[:4]))
    # 8 · yük (en kötü: açıcı silindirinin tüm itişi disk kenarında)
    m_ = H.X_HAREKET_KUTLE + 0.5                                                 # v32: + ayaklar (4 × 0,12) − blok farkı (4 × 0,09) ≈ +0,12 → 0,5 pay
    Fz_ = m_ * 9.81 + ACICI_F
    dF_ = ACICI_F * 170.0 / (4.0 * KIZAK_DX)                                     # disk kenarı (r 170) x yönünde: blok çiftleri ± 80
    P1_ = Fz_ / 4.0 + dF_
    L_km = (MGN["C_din"] / (m_ * 9.81 / 4.0)) ** 3 * 50.0                        # HIWIN MG: L = (C / P)³ × 50 km (yalnız hareket yükü; açıcı basarken araba durur)
    k("v32 · YÜK: hareketli %.1f kg + açıcı itişi %.0f N (Festo DSBC-32 × 6 bar, disk kenarında r 170) → en yüklü blok %.0f N · statik emniyet C0/P = %.1f (≥ 4) · ömür (hareket yükü) %.1e km"
      % (m_, ACICI_F, P1_, MGN["C0"] / P1_, L_km), MGN["C0"] / P1_ >= 4.0)
    print("  X EKSENİ DENETİMİ %.0f sn" % (time.time() - t0_))


def dunya_denetimi(kaset_adim=10.0):'''
degis('\n\ndef dunya_denetimi(kaset_adim=10.0):', DENETIM)
degis('    # 10 · v30 · KAİDE v4 (soğutma grubu cebi + hava pencereleri) ↔ C istasyonu: GERÇEK DENETİM · A kabini BİLGİ\n',
      '    # 9b · v32 · X EKSENİ: alçak kızak + kapalı ray çatısı + ayaklar (yerel ölçüler)\n'
      '    try:\n'
      '        x_ekseni_denetimi(k)\n'
      '    except Exception as e_:\n'
      '        import traceback; traceback.print_exc()\n'
      '        k("v32 · X ekseni denetimi yapılamadı: %s" % str(e_)[:200], False)\n'
      '    # 10 · v30 · KAİDE v4 (soğutma grubu cebi + hava pencereleri) ↔ C istasyonu: GERÇEK DENETİM · A kabini BİLGİ\n')
degis('print("TOPPING MODULU v31 · %d parca', 'print("TOPPING MODULU v32 · %d parca')

io.open(os.path.join(U, "topping_cad_v32.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v32.py yazıldı · %d satır" % s.count("\n"))
