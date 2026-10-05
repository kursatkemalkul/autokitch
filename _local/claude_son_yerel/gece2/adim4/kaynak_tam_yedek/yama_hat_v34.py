# -*- coding: utf-8 -*-
"""h3_elk_hat_v1.py v3.4 yaması: zemine gömme yok · E dış dikey kanalı yok · ana besleme makinenin içinden (teknik sütun → fırın altı ılık boşluk → C kaidesi → TOPPING kuru bölmesi → üst hat)."""
import io
P = r"@@KOK_W@@\b3\arastirma\_uretec\h3\h3_elk_hat_v1.py"
s = io.open(P, encoding="utf-8").read()

YENI_DOC = '''"""HAT v3.4 · ELEKTRİK · ANA HAT v1 (1 Eki 2026 · Kemal: "alt kısım ayaklıkların içinden geçsin, zemine gömme yok · E'nin sağından yukarı giden kanalı sil")
QR ana panosundan makineye güç + veri omurgası — bütün kablolar kapaklı kanalda, HİÇBİR PARÇA ZEMİNİN ALTINDA DEĞİL, makinenin dışında dikey kanal YOK.
  ZEMİN ÜSTÜ KANAL (304 1,5 · 60 × 50, basılır kapak): QR alt ön bandındaki giriş (x 5395, h3_elk_qr_v1) → koridorun ray bitişinden sonraki kör ucunda
         (x 5365–5425, ray ve zincir oluğu 5100'de biter) makineye → E'nin sağ süpürgeliğinden içeri · E ve dolap ayaklarının ARASINDAN (z −70…−10, ön ayak
         sırasının önü) dolabın teknik sütununun altına → arkaya (x 4040–4130).
  DOLAP: taban rakoru (M25) → teknik sütun arka-sol köşe dikey kanalı → pano altı kanalı (v3.2 ile aynı).
  ANA BESLEME YÜKSELİŞİ (TOPPING · K · E besleme demetleri): teknik sütunun hava odasında dikey kanal (x 4100–4130 · z −698…−658, pano ile kondenser arası) →
         y 744–784'te bölme 4'ten (sıcak ↔ sıcak) FIRIN ALTI ILIK BOŞLUĞA (ısı kalkanı ışınım sacı 741 ile dolap tavanı 786 arası) → 304 kapalı kanal x boyunca →
         TOPPING altında dolap tavan PU'sunu 65 mm yatay geçer (altında 75 mm PU kalır) → C kaidesinin içinden yukarı (x 2421–2451) → TOPPING kuru bölmesinin sağ cebi →
         şartlandırıcının (FRL) üstünden arkaya → gövde kanalı (x 2452–2478 · z −828…−788) → üst hat (y 2143) · inişler: TOPPING (x 1950) · K (x 4300) · E (x 5100).
  ÜST HAT: U_KE arkası 60 × 40 → U_F arkası + TOPPING kuru bölmesi 60 × 22 (v3.2 ile aynı; U_KE'nin sağ yan kolu + dış girişi KALKTI).
  Kablo taşıma: kanal tabanı arka duvara / tabana vidalı konsollarla, kanal içindeki kablolar çizilmez (pano imalatı standardı).
  Fırın altı kanalındaki kablolar SİLİKON yalıtımlı (Lapp ÖLFLEX HEAT 180 SiF) — VARSAYIM: boşluk sıcaklığı ölçülecek (AÇIK)."""'''
i = s.index('"""HAT v3.2 · ELEKTRİK · ANA HAT v1')
j = s.index('"""', i + 3) + 3
s = s[:i] + YENI_DOC + s[j:]

# yardımcılar: zemin üstü kanal + içi boş dikdörtgen kanal
ek_yard = '''

def zu_kanal(kutular, h=50.0):
    """ZEMİN ÜSTÜ kanal (y 0…h): kutular [(x0, x1, z0, z1)] birleşik taban + yanlar (içi boş) · kapak h…h + T · döner (gövde, kapak)"""
    dis = ic = kp = None
    for x0, x1, z0, z1 in kutular:
        d = kut(x0, x1, 0.0, h, z0, z1); c = kut(x0 + T, x1 - T, T, h + 1.0, z0 + T, z1 - T); k = kut(x0, x1, h, h + T, z0, z1)
        dis = d if dis is None else dis.fuse(d); ic = c if ic is None else ic.fuse(c); kp = k if kp is None else kp.fuse(k)
    return dis.cut(ic).clean(), kp.clean()


def ici_bos(kutular, ici):
    """kapalı sac kanal: dış kutular birleşimi − iç kutular birleşimi (uçları iç kutularla açılır)"""
    dis = None
    for q in kutular:
        d = kut(*q); dis = d if dis is None else dis.fuse(d)
    for q in ici:
        dis = dis.cut(kut(*q))
    return dis.clean()


def rampa(x0, x1, z0, z1, h, yon):
    """yürünebilir kanal kenarı: üçgen kesitli rampa (x boyunca h → 0) · yon '+x' | '-x'"""
    if yon == "+x": pts = [(x0, 0.0), (x0, h), (x1, 0.0)]
    else: pts = [(x0, 0.0), (x1, h), (x1, 0.0)]
    return cq.Workplane("XY").polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0)).val()
'''
s = s.replace("\n\ndef kur(ekle, DELIKLER, DUSUR):", ek_yard + "\n\ndef kur(ekle, DELIKLER, DUSUR):", 1)

i0 = s.index("    # ---------------- 1 · ZEMİN: QR altı uzantı + makine kolu (ray altından) + DOLAP / E kolları ----------------")
i1 = s.index("    # ---------------- 2 · DOLAP: taban rakoru + arka-sol köşe dikey kanal + pano altı kanalı ----------------")
YENI_ZEMIN = '''    # ---------------- 1 · ZEMİN ÜSTÜ KANAL (gömme YOK): QR giriş (x 5395) → koridorun kör ucu → E / dolap ayakları arası → teknik sütun altı ----------------
    ZU = [(5365.0, 5425.0, -70.0, 667.0),                    # koridor kör ucu (ray + oluk 5100'de biter) · QR alt ön bandına dayalı
          (4040.0, 5425.0, -70.0, -10.0),                    # E + dolap ön süpürgeliğinin arkası, ön ayak sırasının (z ≤ −90) önü
          (4040.0, 4130.0, -829.0, -70.0)]                   # teknik sütunun altı: dolap besleme çıkışı (z −809) + ana yükseliş çıkışı (z −678)
    g, k = zu_kanal(ZU)
    CIK = [(4035.0, 4059.0, -821.0, -797.0), (4100.0, 4130.0, -698.0, -658.0)]          # dolap rakoru · ana yükseliş girişi
    for x0, x1, z0, z1 in CIK:
        k = k.cut(kut(x0, x1, 49.0, 53.0, z0, z1))
    ekle("zemin_ustu_kanal", g, "paslanmaz", B, bom=("Zemin üstü kablo kanalı 304 1,5 · 60 × 50 (koridor kör ucu + E / dolap ayakları arası) · zemine dübelli", 1,
                                                     "lazer + abkant", "gömme YOK (Kemal 1 Eki) · koridorda iki yan rampa"))
    ekle("zemin_ustu_kanal_kapak", k, "paslanmaz", B, bom=("Kanal kapağı 304 1,5 gözyaşı desenli (basılır)", 1, "", ""))
    for nm, (x0, x1, yon) in (("sol", (5335.0, 5365.0, "-x")), ("sag", (5425.0, 5455.0, "+x"))):
        ekle("zemin_ustu_kanal_rampa_%s" % nm, rampa(x0, x1, 80.0, 667.0, 51.5, yon), "paslanmaz", B,
             bom=("Kanal rampası 304 (koridor kör ucu, 30 × 51,5)", 2, "", "") if nm == "sol" else None)
    for i, (x0, x1, z0, z1) in enumerate(CIK):
        ekle("zemin_ustu_cikis_%d" % i, ici_bos([(x0 - T, x1 + T, 50.0, 123.0, z0 - T, z1 + T)], [(x0, x1, 49.0, 124.0, z0, z1)]), "paslanmaz", B,
             bom=("Kanal çıkış kutusu 304 (kanal kapağından dolap tabanına)", 2, "", "") if i == 0 else None)
    DELIKLER.append(("KC", "onyuz_plint", kut(5185.0, 5215.0, -1.0, 52.0, -71.0, -9.0), "zemin üstü kanal E sağ süpürgelik geçişi"))
    DELIKLER.append(("KC", "onyuz_plint", kut(4390.0, 4410.0, -1.0, 52.0, -71.0, -9.0), "zemin üstü kanal E sol süpürgelik geçişi"))
    DELIKLER.append(("SC", "onyuz_plint_donus_sag", kut(4344.0, 4374.0, -1.0, 52.0, -71.0, -9.0), "zemin üstü kanal dolap sağ süpürgelik geçişi"))
'''
s = s[:i0] + YENI_ZEMIN + s[i1:]
s = s.replace('''    ekle("dolap_zemin_cikis_kablosu", boru([(4052.0, -40.0, -809.0), (rx, -40.0, rz), (rx, 123.0, rz)], 7.0), "kablo", B)\n''', "", 1)

i0 = s.index("    # ---------------- 3 · E DIŞ DİKEY KANAL (60 × 60 paslanmaz) + konsollar ----------------")
i1 = s.index("    # ---------------- 4 · ÜST HAT: U_KE (60 × 40) → U_F + TOPPING (60 × 22) ----------------")
YENI_YUK = '''    # ---------------- 3 · ANA BESLEME YÜKSELİŞİ (içeriden): teknik sütun → fırın altı ılık boşluk → C kaidesi → TOPPING kuru bölmesi → gövde kanalı → üst hat ----------------
    ZA = (-698.0, -658.0)                                    # kanal z bandı (pano bileşenleri ≤ −744 · kondenser −504 · taşıyıcı kiriş ≥ −640 · FRL ≤ −700)
    YA = (744.0, 784.0)                                      # fırın altı bandı (ışınım sacı 741 · dolap tavanı 786)
    DIS = [(4100.0 - T, 4130.0 + T, 125.5, YA[1] + T, ZA[0] - T, ZA[1] + T),           # teknik sütun dikey
           (2421.0 - T, 4130.0 + T, YA[0] - T, YA[1] + T, ZA[0] - T, ZA[1] + T),       # fırın altı yatay
           (2421.0 - T, 2451.0 + T, YA[0] - T, 1300.0 + T, ZA[0] - T, ZA[1] + T),      # kaide + kuru bölme yükselişi
           (2421.0 - T, 2478.0 + T, 1260.0 - T, 1300.0 + T, ZA[0] - T, ZA[1] + T),     # FRL üstü bağlantı (ön)
           (2452.0 - T, 2478.0 + T, 1260.0 - T, 1300.0 + T, -788.0, ZA[1] + T),        # FRL üstü bağlantı (arkaya)
           (2452.0 - T, 2478.0 + T, 1260.0 - T, 2143.0, -828.0 - T, -788.0)]           # gövde kanalı → üst hat
    ICI = [(4100.0, 4130.0, 124.0, YA[1], ZA[0], ZA[1]), (2421.0, 4130.0, YA[0], YA[1], ZA[0], ZA[1]), (2421.0, 2451.0, YA[0], 1300.0, ZA[0], ZA[1]),
           (2421.0, 2478.0, 1260.0, 1300.0, ZA[0], ZA[1]), (2452.0, 2478.0, 1260.0, 1300.0, -788.0 + T, ZA[1]),
           (2452.0, 2478.0, 1260.0, 2144.0, -828.0, -788.0 - T)]
    ekle("ana_besleme_kanali", ici_bos(DIS, ICI), "paslanmaz", B,
         bom=("Ana besleme kanalı 304 1,5 kapalı (30–57 × 40, vidalı kapaklı) · teknik sütun → fırın altı → C kaidesi → TOPPING kuru bölmesi → üst hat", 1, "lazer + abkant",
              "fırın altı bölümünde kablolar silikon (Lapp ÖLFLEX HEAT 180 SiF) · VARSAYIM: boşluk sıcaklığı ölçülecek"))
    ekle("ana_besleme_taban_cercevesi", ici_bos([(4092.0, 4138.0, 125.0, 131.0, -706.0, -650.0)], [(4100.0, 4130.0, 124.0, 132.0, ZA[0], ZA[1])]), "rakor", B,
         bom=("Kablo giriş çerçevesi bölmeli conta (4 demet) · dolap tabanı", 1, "icotek KEL-DPZ 24 sınıfı", "VARSAYIM: çerçeve no. demet çaplarına göre seçilecek"))
    DELIKLER.append(("SC", "taban_dis_sac", kut(4100.0, 4130.0, 120.0, 128.0, ZA[0], ZA[1]), "ana besleme dolap tabanı girişi"))
    for a_ in ("bolme_4_sac_a", "bolme_4_pu", "bolme_4_sac_b"):
        DELIKLER.append(("SC", a_, kut(3990.0, 4032.0, YA[0] - T, YA[1] + T, ZA[0] - T, ZA[1] + T), "ana besleme bölme 4 geçişi (teknik sütun ↔ fırın altı, ikisi de sıcak)"))
    DELIKLER.append(("SC", "isi_kalkani_sol_sac", kut(2498.0, 2503.0, YA[0] - T, YA[1] + T, ZA[0] - T, ZA[1] + T), "ana besleme ısı kalkanı geçişi"))
    DELIKLER.append(("SC", "tavan_pu_T", kut(2421.0 - T, 2503.0, YA[0] - T, 788.5, ZA[0] - T, ZA[1] + T), "ana besleme dolap tavan PU geçişi (altında 75 mm PU kalır)"))
    DELIKLER.append(("SC", "tavan_dis_sac", kut(2421.0 - T, 2451.0 + T, 785.0, 789.0, ZA[0] - T, ZA[1] + T), "ana besleme dolap tavanı → C kaidesi"))
    DELIKLER.append(("KD", "kaide_C_ust_plaka_4", kut(2421.0 - T, 2451.0 + T, 887.0, 893.0, ZA[0] - T, ZA[1] + T), "ana besleme C kaidesi üst plakası"))
    DELIKLER.append(("TC", "dis_taban", kut(2421.0 - T, 2451.0 + T, 891.0, 895.0, ZA[0] - T, ZA[1] + T), "ana besleme TOPPING tabanı"))

'''
s = s[:i0] + YENI_YUK + s[i1:]
i0 = s.index("    # U_KE: girişten arkaya (sağ yan boyunca z −766'ya) + arka boyunca 4000'e")
i1 = s.index('    g, k = u_kanal_x(4016.0, 5200.0, ys0, ys1, zs0, zs1, acik="+y")')
s = s[:i0] + "    # U_KE: arka boyunca 4016–5200 (v3.4: sağ yan kolu + dış girişi kalktı)\n" + s[i0 + len("    # U_KE: girişten arkaya (sağ yan boyunca z −766'ya) + arka boyunca 4000'e\n"):i0 + len("    # U_KE: girişten arkaya (sağ yan boyunca z −766'ya) + arka boyunca 4000'e\n")] + s[i1:] if False else s[:i0] + "    ys0, ys1 = UST_KE[\"y\"]; zs0, zs1 = UST_KE[\"z\"]                     # v3.4: U_KE sağ yan kolu + dış girişi kalktı\n" + s[i1:]
# üst hat TOPPING bölümü + F_T geçişi: gövde kanalının girdiği yerde taban kesiği
a = '''        g, k = u_kanal_x(a, b, yf0, yf1, zs0, zs1, acik="+y")
        ekle("ust_hat_%s" % nm, g, "kanal", B,'''
b = '''        g, k = u_kanal_x(a, b, yf0, yf1, zs0, zs1, acik="+y")
        if nm == "TOPPING": g = g.cut(kut(2452.0, 2478.0, yf0 - 1.0, yf0 + T + 0.5, -828.0, -788.0 - T))        # v3.4 · ana besleme gövde kanalı aşağıdan girer
        ekle("ust_hat_%s" % nm, g, "kanal", B,'''
assert s.count(a) == 1; s = s.replace(a, b)
a = '''        g = kut(xa, xb, yf0, yf1, zs0, zs1).cut(kut(xa - 1.0, xb + 1.0, yf0 + T, yf1 - T, zs0 + T, zs1 - T))'''
b = '''        g = kut(xa, xb, yf0, yf1, zs0, zs1).cut(kut(xa - 1.0, xb + 1.0, yf0 + T, yf1 - T, zs0 + T, zs1 - T))
        if nm == "F_T": g = g.cut(kut(2468.0, 2478.0, yf0 - 1.0, yf0 + T + 0.5, -828.0, -788.0 - T))'''
assert s.count(a) == 1; s = s.replace(a, b)
for kalan in ("E_RISER", "zemin_kanal(", "kanal_uc_qr", "ust_ke_yan_sag", "U_KE_giris", "ust_hat_U_KE_yan"):
    print(kalan, s.count(kalan))
compile(s, P, "exec")
io.open(P, "w", encoding="utf-8").write(s)
print("yazıldı")
