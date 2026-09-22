# -*- coding: utf-8 -*-
"""harc_cad_v1 -> harc_cad_v2   ·   VIDA YOK: HORTUM POMPA + BORULU NOZZLE
Kemal (22 Eyl): "ya niye vidali yaptin? Sosla lahmacun harcini dedik ya, BORULU NOZZLE olacak diye."

v1'de kasar govdesini kopyalayip icine HELEZON koymustum — YANLISTI. Sivi/macun vidayla dozlanmaz;
konusulan sistem HORTUM POMPASIYDI (Atosa'da gorulen bidon + hortum duzeni).

v2'DEKI YOL — hicbir yerinde vida yok:
  HAZNE (kasetin kendi kasesi) -> DIP RAKORU -> EMIS HORTUMU (on yuzde yukari)
  -> PERISTALTIK POMPA KAFASI (ust mil ekseninde, rotor + 3 makara hortumu ezer)
  -> BASMA HORTUMU -> BORULU NOZZLE (ic O16) + 1/2" DUCKBILL VALF -> pidenin 40 mm ustu
  Urun YALNIZ hortumun icinde; pompanin hicbir parcasi urune degmiyor.

MIL GOREVLERI (modulde 12 tahrik aynen duruyor, yeni motor gerekmiyor):
  UST mil YC 195 = POMPA ROTORU   ·   ALT mil CY 40 = HAZNE KARISTIRICISI (3 duz palet)

DEBI:  hortum ic O12,7 (1/2" standart) = 127 mm2 · rotor O60 · yatak yayi ~190 mm
       -> ~24 mL/tur [V: kesit x yatak yayi, makara kaybi %5-10]
       doz 110 g @ 1,05 = 105 mL -> 4,4 tur -> 10 saniyede 26 dev/dk (tahrik 42'ye kadar veriyor)
NOZZLE: 10,5 mL/s · ic O16 = 201 mm2 -> 52 mm/s
HORTUM: sarf malzemesi, ~500 saat [V katalog] -> gunde 2 saatte ~8 ay
"""
import io, os, re

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
s = io.open(os.path.join(U, "harc_cad_v1.py"), encoding="utf-8").read()
n = [0]


def yama(a, b):
    global s
    assert a in s, "BULUNAMADI: " + a[:110]
    n[0] += 1
    s = s.replace(a, b, 1)


s = s.replace("harc_cad_v1", "harc_cad_v2").replace("harc_kaseti_v1", "harc_kaseti_v2").replace("harc_v1", "harc_v2")
i = s.index('"""')
j = s.index('"""', i + 3)
s = s[:i] + ('"""AUTOKITCH · HARÇ / SOS ÜNİTESİ v2 (22 Eyl 2026) — VİDA YOK.\n'
             'Hazne → dip rakoru → emiş hortumu → PERİSTALTİK POMPA → basma hortumu → BORULU NOZZLE Ø16 + duckbill valf.\n'
             'Ürün yalnız hortumun içinde. Üst mil pompayı, alt mil hazne karıştırıcısını döndürür.\n'
             'Hesap: yap_harc_v2.py\n"""\n') + s[j + 4:]

# ---------------------------------------------------------------- 1 · POMPA SABİTLERİ
yama("BORU_D, BORU_ET, BORU_ALT, BORU_GECIS = 25.0, 3.0, -100.0, 22.0",
     "HRT_IC, HRT_DIS = 12.7, 19.0                # peristaltik hortum 1/2\" · platin silikon [katalog]\n"
     "POM_R, POM_MAK = 30.0, 9.5                  # rotor yarıçapı · makara yarıçapı\n"
     "POM_Z0, POM_Z1 = 10.0, 36.0                  # pompa kafasının z aralığı (ön plakanın önünde)\n"
     "RAKOR_Y = 16.0                              # dip rakoru: kâse tabanından yüksekliği\n"
     "BORU_D, BORU_ET, BORU_ALT, BORU_GECIS = 16.0, 3.0, -100.0, 10.0")

# ---------------------------------------------------------------- 2 · HELEZON KALKTI, ALT MİL KARIŞTIRICI OLDU
yama("    G = \"helezon\"; BOYUN, GERI = 3.0, 0.2",
     '''    G = "helezon"; BOYUN, GERI = 3.0, 0.2
    # v2: HELEZON KALKTI (Kemal: "niye vidalı yaptın, borulu nozzle olacak diye"). Sıvı/macun vidayla
    # dozlanmaz. Alt mil artık HAZNE KARIŞTIRICISI: kâsenin dibini süpüren 3 düz palet — ürünü itmiyor,
    # yalnız ayrışmayı önlüyor. Ürünü hortum pompası veriyor.
    for _i in range(3):
        _pal = kut(-(RT - 2.0), RT - 2.0, -2.5, 2.5, -145.0, 150.0).rotate((0.0, CY, 0.0), (0.0, CY, 1.0), 120.0 * _i)
        ekle("karistirici_paleti_%s" % "ABC"[_i], _pal.translate((0, CY, 0)).cut(karez(0, CY, KARE + 0.3, -147.0, 152.0)), "pom", G,
             bom=("Karıştırıcı paleti 40 × 5 × 295", 3, "POM ya da 304 lama · kare mile geçme",
                  "kâsenin dibini süpürür; sos/harç beklerken ayrışmasın diye dozdan önce birkaç tur döner") if _i == 0 else None)''')
yama("    SEG = [(\"helezon_A\"", "    SEG = [] if 1 else [(\"helezon_A\"")

# ---------------------------------------------------------------- 3 · ÇIKIŞ TÜPÜ YERİNE POMPA + HORTUM + NOZZLE
i0 = s.index("    # ---- 6 ÇIKIŞ TÜPÜ")
i1 = s.index('    ekle("yatak_kapagi"')
s = s[:i0] + '''    # ---- 6 · HAZNE RAKORU + PERİSTALTİK POMPA + BORULU NOZZLE (v2: vida yok) ----
    ZP = (ZF + POM_Z0, ZF + POM_Z1)                                                                      # pompa kafası ön plakanın ÖNÜNDE
    ZPM = (ZP[0] + ZP[1]) / 2.0
    R_YAT = POM_R + HRT_DIS / 2.0                                                                        # hortum yatağının merkez yarıçapı
    R_DIS = R_YAT + HRT_DIS / 2.0 + 12.0                                                                 # pompa gövdesinin dış yarıçapı
    ZN = (AG_Z0 + AG_Z1) / 2.0                                                                           # nozzle ekseni (eski ağız yeri — modüldeki yarık orada)

    # 6a · dip rakoru: kâsenin en alçak noktası, ön plakada
    rk = silz(0, RAKOR_Y, 11.0, ZF + 0.6, ZF + 26.0).cut(silz(0, RAKOR_Y, HRT_IC / 2 + 0.6, ZF - 3.0, ZF + 27.0))
    rk = rk.union(silz(0, RAKOR_Y, 14.0, ZF + 18.0, ZF + 23.0)).cut(silz(0, RAKOR_Y, HRT_IC / 2 + 0.6, ZF - 1.0, ZF + 27.0))
    ekle("hazne_rakoru", rk, "celik", bom=("Hazne dip rakoru · hortum nipeli", 1, "304 torna · gıda · O-ringli",
         "kâsenin en alçak noktasında; hazne boşalınca içeride ürün kalmaz · hortum buraya kelepçelenir"))

    # 6b · emiş hortumu: rakordan pompanın emiş ağzına (ön yüzde yukarı)
    # NOT: hortumlar DOLU modelleniyor (dış çap). İçini kesince L köşesinde geçersiz katı çıkıyordu;
    # iç çap ölçüsü BOM'da ve hesapta yazılı, geometrik olarak gerekmiyor.
    ekle("emis_hortumu", sily(0, ZPM, HRT_DIS / 2, RAKOR_Y + 17.0, YC - R_YAT + 4.0), "silikon",
         bom=("Emiş hortumu 1/2\\"", 1, "platin silikon, gıda · SARF", "hazneden pompaya; ürün yalnız hortumun içinde"))

    # 6c · pompa gövdesi (yarım ay yatak) + kapak
    gv = silz(0, YC, R_DIS, ZP[0], ZP[1]).cut(silz(0, YC, R_YAT + HRT_DIS / 2 + 0.3, ZP[0] - 1.0, ZP[1] + 1.0))
    gv = gv.union(silz(0, YC, R_DIS, ZP[0], ZP[0] + 3.0))                                                # arka yanak
    gv = gv.cut(kut(-R_DIS - 1, R_DIS + 1, YC - R_DIS - 1, YC - R_YAT + 2.0, ZP[0] - 1.0, ZP[1] + 1.0))  # hortumun girip çıktığı ağız
    gv = gv.cut(silz(0, YC, 13.0, ZP[0] - 1.0, ZP[1] + 1.0))                                             # mil geçişi
    ekle("pompa_govdesi", gv, "pom", bom=("Peristaltik pompa gövdesi", 1, "POM ya da 304 · yarım ay yatak",
         "hortumu makaralara karşı tutar; ürünle TEMAS ETMEZ, yıkanması gerekmez"))
    ekle("pompa_kapagi", silz(0, YC, R_DIS, ZP[1], ZP[1] + 3.0).cut(silz(0, YC, 13.0, ZP[1] - 1.0, ZP[1] + 4.0))
         .cut(kut(-R_DIS - 1, R_DIS + 1, YC - R_DIS - 1, YC - R_YAT + 2.0, ZP[1] - 1.0, ZP[1] + 4.0)), "cam",
         bom=("Pompa kapağı · şeffaf", 1, "PC 3 mm · 3 mandal", "hortum değişimi için açılır; şeffaf olduğu için hortumun durumu görülür"))

    # 6d · rotor + 3 makara (ürüne değmez)
    rt = silz(0, YC, POM_R - 2 * POM_MAK - 1.0, ZP[0] + 10.0, ZP[1] - 1.0).cut(karez(0, YC, KARE + 0.3, ZP[0] + 3.0, ZP[1] + 1.0))
    for _i in range(3):
        _a = math.radians(120.0 * _i)
        rt = rt.union(silz((POM_R - POM_MAK) * math.cos(_a), YC + (POM_R - POM_MAK) * math.sin(_a), 3.9, ZP[0] + 10.0, ZP[1] - 2.0))
    ekle("pompa_rotoru", rt, "pom", "karistirici",
         bom=("Pompa rotoru · 3 makaralı", 1, "POM · kare mile geçme", "üst mille döner; makaralar hortumu ezerek ürünü iter"))
    for _i in range(3):
        _a = math.radians(120.0 * _i)
        ekle("makara_%s" % "ABC"[_i], silz((POM_R - POM_MAK) * math.cos(_a), YC + (POM_R - POM_MAK) * math.sin(_a), POM_MAK, ZP[0] + 11.0, ZP[1] - 3.0)
             .cut(silz((POM_R - POM_MAK) * math.cos(_a), YC + (POM_R - POM_MAK) * math.sin(_a), 4.2, ZP[0] + 4.0, ZP[1] - 1.0)), "celik", "karistirici",
             bom=("Makara Ø19 · rulmanlı", 3, "304 + 623 rulman", "hortumu yatağa doğru ezer") if _i == 0 else None)

    # 6e · pompa hortumu: yatakta yarım tur
    ph = cq.Workplane(obj=cq.Solid.makeTorus(R_YAT, HRT_DIS / 2, cq.Vector(0, YC, ZPM), cq.Vector(0, 0, 1)))
    ph = ph.cut(cq.Workplane(obj=cq.Solid.makeTorus(R_YAT, HRT_IC / 2, cq.Vector(0, YC, ZPM), cq.Vector(0, 0, 1))))
    ph = ph.cut(kut(-R_YAT - 20.0, R_YAT + 20.0, YC - R_YAT - 20.0, YC - R_YAT + HRT_DIS / 2 - 1.0, ZPM - HRT_DIS, ZPM + HRT_DIS))   # alt dilim acik: hortumun girisi/cikisi
    ekle("pompa_hortumu", ph, "silikon", bom=("Pompa hortumu 1/2\\" · SARF", 1, "platin silikon, peristaltik tip",
         "yatakta 200°; makaralar bunu ezer · ~500 saat ömür [V katalog] → günde 2 saatte ~8 ay"))

    # 6f · basma hortumu: pompa çıkışından nozzle'a
    ekle("basma_hortumu", silz(24.0, YC - R_YAT + 6.0, HRT_DIS / 2, ZP[1] + 5.0, ZN + 4.0), "silikon",
         bom=("Basma hortumu 1/2\\"", 1, "platin silikon, gıda · SARF", "pompadan nozzle borusuna"))

    # 6g · BORULU NOZZLE: ön plakaya bağlı, pidenin 40 mm üstünde biter
    BZ = ZN
    nz = sily(0, ZN, BORU_D / 2 + BORU_ET, BORU_ALT, YC - R_YAT - 18.0)
    nz = nz.union(silz(0, YC - R_YAT - 26.0, BORU_D / 2 + BORU_ET + 5.0, ZN - 16.0, ZN + 16.0))          # ön plakaya cıvatalı bilezik
    nz = nz.cut(sily(0, ZN, BORU_D / 2, BORU_ALT - 1.0, YC - R_YAT - 12.0))
    nz = nz.cut(sily(0, ZN, HRT_DIS / 2 + 0.3, YC - R_YAT - 26.0, YC - R_YAT - 12.0))                    # hortumun oturduğu ağız
    ekle("nozzle_borusu", nz, "cam", bom=("Nozzle borusu · iç Ø%.0f" % BORU_D, 1, "PC / PETG şeffaf ya da 304",
         "kasetin ön yüzüne bilezikle bağlı; pidenin %.0f mm üstünde biter · ürün burada serbest düşmez, duckbill'e kadar dolu iner" % 40))

''' + s[i1:]

# 3b · duckbill valf: yeni boru capina gore
yama('    RB_V = BORU_D / 2 + BORU_ET', '    RB_V = BORU_D / 2 + BORU_ET   # 1/2" duckbill (boru iç Ø16)')
s = s.replace('("Duckbill valf 1\\"", 1,', '("Duckbill valf 1/2\\"", 1,')

# 3c · topuz kalkti (ust mil artik pompayi dondurur, elle cevrilmiyor)
s = re.sub(r'^    ekle\("topuz".*?\n', '', s, flags=re.M)
s = re.sub(r'^    ekle\("setuskur".*?\n', '', s, flags=re.M)

s = re.sub(r"^    kp = BR\.yatak_kapagi.*?\n", "", s, flags=re.M)
s = re.sub(r'^    ekle\("yatak_kapagi".*?\n', "", s, flags=re.M)
io.open(os.path.join(U, "harc_cad_v2.py"), "w", encoding="utf-8").write(s)
print("harc_cad_v2.py yazildi ·", n[0], "yama")
