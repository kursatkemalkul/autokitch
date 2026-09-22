# -*- coding: utf-8 -*-
"""topping_hesap_v3 + topping_cad_v7  ->  v4 / v8   ·   DÖNER TABLA
Kemal (22 Eyl): "simdi altina Atosa gibi tabla yapicaz ama nasil olucak? Her kasetin cikis yerine denk
gelicek, ona gore kendini ayarlayip donerken ilerliyecek vs."

SISTEM — iki eksen, kasetlerin akis modelleri ZATEN buna gore kurulmus:
  X EKSENI  : tabla arabasi kasetler boyunca kayar. Iki isi var —
              (a) kasetten kasete gecis, (b) DOZAJ SIRASINDA agzin pide merkezine uzakligini degistirmek.
  THETA EKSENI: tabla kendi ekseninde doner (35 dev/dk).
  Nozzle SABIT. Tabla donerken x'te kaydigi icin nozzle pide uzerinde SPIRAL ciziyor — Atosa'nin
  "baslik radyal kayar" duzeninin tersi ama ayni sonuc.

AKIS MODELLERINDEN GELEN (kasar_akis_model_v2 · kusbasi_akis_model_v2 — uydurma degil, hesap oradan):
  pide yaricapi 140 · kenar 15 -> kaplanan 125
  doz suresi T_DOK = 10 s
  tabla yasasi r(t): 105 mm'de 2,5 s bekle -> r^2 dogrusal azalarak ICERI -> 20 mm'de 0,3 s bekle
  tabla devri n_tabla = 35 dev/dk
  -> dozajda x stroku 105 - 20 = 85 mm · 10 s'de 5,83 tur · tur basina 85/5,83 = 14,6 mm iceri
     (serit araligi 14,6 mm; kaset serit genisligi bunun uzerinde olmali — kasar/kusbasi modelinde oyle)

MEKANIZMA:
  X: lineer kizak + GT3 kayis, NEMA23. Strok = yuvalar arasi 1075 + dozaj salinimi 105 + yukleme payi
     -> 1300 mm. Dozajda 8,5 mm/s (hassas), gecislerde 200 mm/s.
  THETA: tabla altinda NEMA17 + planet i=10 -> 35 dev/dk cikis icin motor 350 dev/dk.
  Tabla O360 (tepsi O340 + 20). Robot tepsiyi tablaya birakir, dozaj biter, robot alir firina goturur.

DIKEY DIZILIM (AGZ + BAS zonu; huni kalktigi icin BAS bosaldi):
  nozzle ucu 160 -> dusme 40 -> pide ustu 120 -> hamur 8 -> tepsi 12 -> tabla 14 -> govde/motor -> ray
"""
import io, os

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
n = [0]


def yama(s, a, b):
    assert a in s, "BULUNAMADI: " + a[:110]
    n[0] += 1
    return s.replace(a, b, 1)


# ================================================================ 1 · HESAP v4
h = io.open(os.path.join(U, "topping_hesap_v3.py"), encoding="utf-8").read()
h = h.replace("topping_hesap_v3", "topping_hesap_v4").replace("topping_cad_v3.py", "topping_cad_v8.py")
i = h.index('"""', h.index('"""') + 3)
h = h[:i] + ("v4 (22 Eyl 2026): DONER TABLA hesabi eklendi — x ekseni stroku/hizi, tabla devri, dikey dizilim.\n") + h[i:]

h = yama(h, "# ---------------------------------------------------------------- 3 · SOĞUTMA YÜKÜ ----------------------------------------------------------------",
         '''# ---------------------------------------------------------------- 2d · DÖNER TABLA (v4) ----------------------------------------------------------------
# Kemal: "altına Atosa gibi tabla yapacağız; her kasetin çıkış yerine denk gelecek, ona göre kendini
# ayarlayıp dönerken ilerleyecek." Kasetlerin akış modelleri ZATEN tablalı düzene göre çözülmüştü.
PIDE_R, KENAR = 140.0, 15.0        # [kasar_akis_model_v2] pide yarıçapı · kaplanmayan kenar
T_DOZ = 10.0                       # [kasar_akis_model_v2 · T_DOK] bir dozun süresi
TABLA_RPM = 35.0                   # [kusbasi_akis_model_v2 · dagilim(n_tabla=35)] tabla devri
R_DIS, R_IC = 105.0, 20.0          # [kasar_akis_model_v2 · YASA] ağzın pide merkezine uzaklığı: dıştan içeri
TABLA_D = 340.0                    # tepsi Ø340 ile aynı; merkezleme 3 pimle (bilezik modülün ön yüzünden taşıyordu)
TEPSI_K, TABLA_K, HAMUR_K = 12.0, 14.0, 8.0                                  # tepsi · tabla · hamur kalınlıkları [V]

DOZ_STROK = R_DIS - R_IC                                                     # dozaj sırasında x'te kayma = 85 mm
TUR_DOZ = TABLA_RPM * T_DOZ / 60.0                                           # bir dozda tabla kaç tur döner = 5,83
SERIT_ARA = DOZ_STROK / TUR_DOZ                                              # her turda içeri kayma = 14,6 mm
X_DOZ_HIZ = DOZ_STROK / T_DOZ                                                # dozajda araba hızı = 8,5 mm/s
X_GECIS_HIZ = 200.0                                                          # yuvadan yuvaya [V: lineer kızakta rahat]
# Strok: ilk ve son yuva merkezi arası + dozaj salınımı + robotun tepsiyi bıraktığı yükleme noktası
YUVA_ACIKLIK = 1075.0                                                        # topping_cad YUVA merkezlerinden ölçüldü
X_STROK = YUVA_ACIKLIK + R_DIS + 120.0                                       # 1300 mm

# ---------------------------------------------------------------- 3 · SOĞUTMA YÜKÜ ----------------------------------------------------------------''')

h = yama(h, '                  kuru_gerek=KURU_D, on_nis=ON_NIS, sogutulan_z=IC["z"], dusme=DUSME, kaset_alti=KASET_ALTI),',
         '                  kuru_gerek=KURU_D, on_nis=ON_NIS, sogutulan_z=IC["z"], dusme=DUSME, kaset_alti=KASET_ALTI),\n'
         '    tabla=dict(cap=TABLA_D, rpm=TABLA_RPM, doz_sn=T_DOZ, r_dis=R_DIS, r_ic=R_IC, doz_strok=DOZ_STROK,\n'
         '               tur_doz=round(TUR_DOZ, 2), serit_ara=round(SERIT_ARA, 1), x_doz_hiz=round(X_DOZ_HIZ, 1),\n'
         '               x_gecis_hiz=X_GECIS_HIZ, x_strok=X_STROK),')

h = h.replace('    print("=== 3 · SOGUTMA ===")',
              '''    print("=== 2d · DONER TABLA ===")
    print("   pide yaricapi %.0f · kaplanan %.0f · doz %.0f s · tabla %.0f dev/dk  [akis modellerinden]" % (PIDE_R, PIDE_R - KENAR, T_DOZ, TABLA_RPM))
    print("   agiz pide merkezine %.0f -> %.0f mm  =>  dozajda x stroku %.0f mm" % (R_DIS, R_IC, DOZ_STROK))
    print("   bir dozda %.2f tur -> her turda %.1f mm iceri (serit araligi)" % (TUR_DOZ, SERIT_ARA))
    print("   araba hizi: dozajda %.1f mm/s · yuvadan yuvaya %.0f mm/s · toplam strok %.0f mm" % (X_DOZ_HIZ, X_GECIS_HIZ, X_STROK))
    print("=== 3 · SOGUTMA ===")''', 1)

io.open(os.path.join(U, "topping_hesap_v4.py"), "w", encoding="utf-8").write(h)
print("topping_hesap_v4.py yazildi")

# ================================================================ 2 · CAD v8
c = io.open(os.path.join(U, "topping_cad_v7.py"), encoding="utf-8").read()
c = c.replace("topping_hesap_v3", "topping_hesap_v4").replace("topping_cad_v7", "topping_cad_v8").replace("topping_modul_v7", "topping_modul_v8")
i = c.index('"""', c.index('"""') + 3)
c = c[:i] + ("v8 (22 Eyl 2026): DONER TABLA — x arabasi (lineer kizak + kayis) + tabla (O360, 35 dev/dk).\n"
             "Nozzle sabit; tabla donerken x'te kaydigi icin agiz pide uzerinde spiral ciziyor.\n") + c[i:]
c = yama(c, '"TOPPING MODULU v7', '"TOPPING MODULU v8')

c = yama(c, '    # ---------------- 9 · AĞIZ ve DAMLAMA ----------------',
         '''    # ---------------- 8b · DÖNER TABLA (v8) ----------------
    # İki eksen: ARABA x'te kayar (hem yuvadan yuvaya, hem dozaj sırasında ağzın pide merkezine
    # uzaklığını 105 → 20 mm değiştirir), TABLA kendi ekseninde 35 dev/dk döner. Nozzle sabit.
    TB = H.S["tabla"]
    TY = AGZ[1] - HAMUR_ - TEPSI_ - TB["cap"] * 0.0                                     # tabla üst yüzü
    # Tabla ekseni nozzle'dan z'de 20 mm GERİDE: dozaj r = √(dx² + 20²) olduğu için dx = 0'da
    # r tam olarak yasanın r_ic'sine (20 mm) iniyor. Aynı zamanda Ø340 tabla modülün ön yüzünü aşmıyor.
    ZT = ZK[0] + 30.0
    ray_y = (AGZ[0] + 6.0, AGZ[0] + 26.0)
    for s_, zz in (("on", ZT + 150.0), ("arka", ZT - 150.0)):
        ekle("tabla_rayi_%s" % s_, kut(160.0, 160.0 + TB["x_strok"], ray_y[0], ray_y[1], zz - 10.0, zz + 10.0), "celik",
             bom=("Lineer kızak rayı 20 × %.0f" % TB["x_strok"], 2, "HGR20 sınıfı · paslanmaz", "tabla arabası bunun üstünde kayar; strok %.0f mm" % TB["x_strok"]) if s_ == "on" else None)
    ekle("tabla_arabasi", kut(-150.0, 150.0, ray_y[1], ray_y[1] + 20.0, ZT - 250.0, ZT + 170.0).translate((900.0, 0, 0)), "sac",
         bom=("Tabla arabası", 1, "304 kaynaklı şasi · 4 kızak arabası", "x ekseni: dozajda %.1f mm/s, yuvadan yuvaya %.0f mm/s" % (TB["x_doz_hiz"], TB["x_gecis_hiz"])))
    ekle("tabla_x_motoru", kut(60.0, 117.0, ray_y[0] + 4.0, ray_y[0] + 61.0, ZT - 28.0, ZT + 28.0), "motor",
         bom=("X ekseni motoru NEMA23 + GT3 kayış", 1, "kapalı çevrim step · kasnak Ø30", "dozajda 5 dev/dk, geçişte 128 dev/dk"))
    # Motor tablanın ALTINA sığmıyor (orada yalnız 36 mm var): arabanın ARKA ucuna, tablanın dışına
    # kondu; torku kayışla tabla miline taşıyor. Kaset bölgesinin altında kalıyor, hiçbir şeye değmiyor.
    ekle("tabla_donus_motoru", kut(879.0, 921.0, ray_y[1] + 22.0, ray_y[1] + 64.0, ZT - 240.0, ZT - 198.0), "motor",
         bom=("Tabla motoru NEMA17 + planet i=10", 1, "35 dev/dk çıkış · motor 350 dev/dk", "arabanın arka ucunda; torku kayışla tabla miline taşır · doz boyunca %.2f tur" % TB["tur_doz"]))
    ekle("tabla_kayisi", kut(894.0, 906.0, ray_y[1] + 38.0, ray_y[1] + 48.0, ZT - 196.0, ZT - 14.0), "koyu",
         bom=("Tabla kayışı GT3 · 9 mm", 1, "poliüretan çelik takviyeli", "motordan tabla miline"))
    ekle("tabla_mili", sily(900.0, ZT, 12.0, ray_y[1] + 30.0, TY - TABLA_ - 1.0), "celik", bom=("Tabla mili Ø24", 1, "304", "redüktörden tablaya"))
    ekle("tabla", sily(900.0, ZT, TB["cap"] / 2, TY - TABLA_, TY), "sac",
         bom=("Döner tabla Ø%.0f" % TB["cap"], 1, "304 · tepsi merkezleme bileziği", "tepsi Ø340 buraya oturur · %.0f dev/dk · doz %.0f s" % (TB["rpm"], TB["doz_sn"])))
    for _i in range(3):
        _a = math.radians(120.0 * _i + 30.0)
        ekle("tabla_pimi_%s" % "ABC"[_i], sily(900.0 + 158.0 * math.cos(_a), ZT + 158.0 * math.sin(_a), 4.0, TY, TY + 9.0), "celik",
             bom=("Tepsi merkezleme pimi Ø8", 3, "304 · tablaya preslenir", "tepsi dönerken kaymasın; bilezik yerine pim — bilezik modülün ön yüzünü aşıyordu") if _i == 0 else None)
    for a_, ad_, n_, malz_, gor_ in (("_bom_tabla", "Tabla yasası", 1, "yazılım", "ağız pide merkezine %.0f mm'de %.1f s bekler, r² doğrusal azalarak %.0f mm'ye iner, %.1f s bekler [kasar_akis_model_v2]" % (TB["r_dis"], 2.5, TB["r_ic"], 0.3)),):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "celik", bom=(ad_, n_, malz_, gor_))

    # ---------------- 9 · AĞIZ ve DAMLAMA ----------------''')

c = c.replace('def silz(x, y, r, z0, z1):', 'def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1):', 1)
c = yama(c, "    hy0, hy1 = KAS[0] - H.KASET_ALTI, KAS[1] + 20.0",
         "    HAMUR_, TEPSI_, TABLA_ = H.HAMUR_K, H.TEPSI_K, H.TABLA_K\n"
         "    hy0, hy1 = KAS[0] - H.KASET_ALTI, KAS[1] + 20.0")

io.open(os.path.join(U, "topping_cad_v8.py"), "w", encoding="utf-8").write(c)
print("topping_cad_v8.py yazildi ·", n[0], "yama")
