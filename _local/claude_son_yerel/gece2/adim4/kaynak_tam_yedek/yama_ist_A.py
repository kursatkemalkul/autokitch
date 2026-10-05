import io
P = r"@@KOK_W@@\b3\arastirma\_uretec\h3\h3_elk_ist_v1.py"
s = io.open(P, encoding="utf-8").read()
a0 = s.index("    # A: emniyet sensörleri + ışık perdesi + TOPPING x sol limit / x sıfır sensörleri → A sağ ön köşede DİKEY KABLO KANALI")
a1 = s.index("    AK_BOM = (")
yeni = '''    # A (v3.4 · TEMİZ KUTU, açıcı hazır alınır): emniyet sensörleri + ışık perdesi + TOPPING x sol limit / x sıfır sensörleri → A sağ ön köşede DİKEY KABLO KANALI
    #    (y 1050–1610) → 6 kablo DEMET halinde (dağıtıcı kutusu YOK: Exact12 8 port gerçekte 150 × 50 × 17, köşeye sığmıyordu) → A|TOPPING duvarı G7 → TOPPING panosu
    kanal_kutu("kanal_A_sag_on_dikey", 1406.0, 1434.0, 1050.0, 1610.0, -40.0, -8.0, "A",
               ("Kablo kanalı PVC kapaklı 30 × 40 (A sağ ön köşe, kapak −x yönüne)", 1, "Hager tehalit BA7A40030", "A|TOPPING duvarına konsollu"))
    gecis("G7_A_TOPPING_duvari", (1436.0, 1520.0, -680.0), "x", [("TC", "dis_yan_sol")], "A", r=6.5, t=31.5, yon="-",
          bom=("Çok delikli rakor M32 + 6 delikli conta (6 sensör kablosu) · 31,5 duvarda kovan + iç sacta rakor", 1, "Lapp SKINTOP MS-M 32 + DIX-M", "VARSAYIM: conta no. kablo çaplarına göre"))
    sabit("A_sensor_demeti", [(1420.0, 1560.0, -24.0), (1420.0, 1625.0, -24.0), (1420.0, 1625.0, -680.0), (1420.0, 1520.0, -680.0), (1480.0, 1520.0, -680.0),
                              (1480.0, 1870.0, -680.0), (1480.0, 1870.0, -715.0), (1480.0, 1879.8, -715.0)], 6.5, "A", haric=("TOPPING_MODUL|dis_yan_sol",),
          bom=("Sensör kabloları demeti 6 × M12 / M8 PUR (A kanalından TOPPING panosuna, spiral sargılı)", 1, "Murrelektronik 7000-12221-6340500 / 7000-08041-6300500", ""))
    # satın alınacak açıcının bağlantısı: A sağ duvarında priz kutusu ← G10 ← TOPPING panosu (besleme + kontrol)
    parca("A_acici_baglanti_kutusu", kut(1374.0, 1434.0, 1310.0, 1380.0, -700.0, -630.0).cut(kut(1376.0, 1432.0, 1312.0, 1378.0, -698.0, -632.0)), "cihaz_koyu", "A",
          ("Açıcı bağlantı kutusu IP65 (priz 230 V 16 A + M12 kontrol soketi) · A sağ duvarı", 1, "Spelsberg / Hensel sınıfı",
           "AÇIK: satın alınacak açıcının fişi / kontrol bağlantısına göre seçilecek"))
    gecis("G10_A_TOPPING_acici", (1436.0, 1345.0, -665.0), "x", [("TC", "dis_yan_sol")], "A", r=4.5, t=31.5, yon="-",
          bom=("Rakor M20 (açıcı besleme 3G1,5 + kontrol) · A|TOPPING duvarı", 1, "Lapp SKINTOP ST-M 53111020", ""))
    cihaz("A_acici_beslemesi", (1440.0, 1345.0, -665.0), (1500.0, 1879.8, -700.0), 4.5, "A",
          via=[((1470.0, 1345.0, -665.0), ("TOPPING_MODUL|dis_yan_sol",))], on=(1500.0, 1862.0, -700.0), bolge=(1436.0, 2000.0, 1100.0, 1880.0, -828.5, -630.0), h=5.0,
          bom=("Açıcı besleme + kontrol kablosu (3G1,5 + 4 × 0,34) → TOPPING panosu", 1, "Lapp ÖLFLEX CLASSIC 110 1119303 + 7000-12221-6340500", ""))
'''
s = s[:a0] + yeni + s[a1:]
s = s.replace('''    AK_BOM = ("Sensör kablosu M12 / M8 PUR (A emniyet · ışık perdesi · x eksen sensörleri → A kanalı)", 6, "", "")''',
              '''    AK_BOM = ("Sensör kablosu M12 / M8 PUR (A emniyet · ışık perdesi · x eksen sensörleri → A kanalı)", 6, "Murrelektronik 7000-12221-6340500 (M12) / 7000-08041-6300500 (M8)", "")''', 1)
compile(s, P, "exec"); io.open(P, "w", encoding="utf-8").write(s); print("ok")
