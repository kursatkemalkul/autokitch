# -*- coding: utf-8 -*-
"""topping_cad_v18 -> v19 : SOGUTMA PAKETI "YAPTIRILACAK" OLARAK ISARETLENDI

Kemal: "sogutmalara gerek yok onlar zaten yaptirilicak."

Sogutma grubu, evaporator ve fani raftan alinan katalog urunu degil; sogutmaci
firmaya yaptirilacak / yerinde kurulacak paket. O yuzden bunlar icin uretici STEP'i
aranmiyor. Modelde YER ZARFI olarak duruyorlar: olculeri ve kutleleri sinif degeri,
kesin model firma secince belli olacak.

Bu dosya yalniz BOM metinlerini ve notlari duzeltiyor — GEOMETRI DEGISMIYOR.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v18.py"), encoding="utf-8").read()

eski = '''         bom=("Soğutma grubu ⅕ HP", 1, "hermetik, hava soğutmalı", "teknik bantta, önden servis; +3 °C'de 250–350 W verir"))'''
yeni = '''         bom=("Soğutma grubu ⅕ HP · YAPTIRILACAK", 1, "hermetik, hava soğutmalı · soğutmacı firma kurar",
              "teknik bantta, önden servis; +3 °C'de 250–350 W verir. RAFTAN ALINAN PARÇA DEĞİL: "
              "modelde YER ZARFI, kesin marka/model firma seçince belli olacak (300 × 220 × 220)"))'''
assert eski in s; s = s.replace(eski, yeni, 1)

eski = '''         bom=("Fanlı evaporatör (unit cooler)", 1, "400 × 180 × 190 (lamel 140 + fan 50) · standart sınıf", "KURU BÖLMEDE, motorların üstünde; soğuğu arka yalıtımdaki iki boşluktan hücreye verir · yük %.0f W, seçim %.0f W" % (H.S["soguk"]["q_toplam"], H.S["soguk"]["q_secim"])))'''
yeni = '''         bom=("Fanlı evaporatör (unit cooler) · YAPTIRILACAK", 1,
              "400 × 180 × 190 (lamel 140 + fan 50) · soğutmacı firma kurar",
              "KURU BÖLMEDE, motorların üstünde; soğuğu arka yalıtımdaki iki boşluktan hücreye verir · "
              "yük %.0f W, seçim %.0f W. RAFTAN ALINAN PARÇA DEĞİL: modelde YER ZARFI" % (H.S["soguk"]["q_toplam"], H.S["soguk"]["q_secim"])))'''
assert eski in s; s = s.replace(eski, yeni, 1)

eski = '''         bom=("Evaporatör fanı Ø200", 1, "24 V eksenel · evaporatörle birlikte gelir", "havayı evaporatörden çekip yalıtımdaki üfleme boşluğuna basar"))'''
yeni = '''         bom=("Evaporatör fanı Ø200", 1, "eksenel · EVAPORATÖRLE BİRLİKTE GELİR, ayrı alınmaz",
              "havayı evaporatörden çekip yalıtımdaki üfleme boşluğuna basar. Soğutma paketi "
              "yaptırılacağı için fan da o pakete dahil; modelde YER ZARFI"))'''
assert eski in s; s = s.replace(eski, yeni, 1)

# HATA DUZELTMESI: parca adi "ups_rayi" idi; katalog kutle tablosu ad BASINA bakiyor,
# "ups" ile basladigi icin raya UPS'in 0,65 kg'ini veriyordu (gercegi 0,15 kg sac).
s = s.replace('ekle("ups_rayi"', 'ekle("din_ray_ups"')

io.open(os.path.join(U, "topping_cad_v19.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v19.py yazildi")
