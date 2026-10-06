# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 82 · E KUTU KAPAĞI KATLAMA MEKANİZMASI VİDALI (6 Eki 2026 · Claude · 2. oturum · E mekanizma montajı · KURALLAR §1.2 / §2.2 / §5)
python 82_e_kapak.py girdi.glb cikti.glb      (zincir: hat3_v10m.glb → hat3_v10n.glb)

E_KAPAK (43 bileşen: şasi, 3 motor, 2 yatak ayağı, tahrik mili + kol, dik mil + göbek, katlayıcı kol + palet (3 mm bıçak), 2 kılavuz direk + mil,
2 dik rod + üst plakalar, 2 sensör) — envanterde bağlantı elemanı 0. Üreteç yapısı: şasi = 6 mm üst kiriş + 4 ayak 20 × 20 (kalıp tabanının
4 mm plakasında) · motor bloğu = 6 mm flanş plakası + 10 mm duvar · yatak plakası duvarın yarığında · dişli kutusu + üst motor fabrikada birleşik
hazır ürün (giriş flanşı 38 × 38, NEMA 23 deseni yok → tek parça sayılır) · palet 3 mm L bıçak, kolun −x yüzü üstünde köşe temasıyla duruyordu → kademeli 6 mm BRAKET (yeni).
  şasi ayakları: kirişe üstten M6 · kalıp taban plakasına (4 mm) alttan M6 (baş tepsinin içinde) · motor dik plakası kirişe alttan 2 × M5 · motor plakası
  (4 mm) dik plakaya 2 × M4 · dişli kutulu motor plakaya 4 × M4 (gövde eksen noktalarından) · yatak ayakları kirişe alttan 2 × M5 · yataklar ayaklara 2 × M5×50 · tahrik mili kol göbeğine setskur, ön yatakta
  segman · sensör L braketleri M3 (yatak ayağına / kirişe) + M8 sensör somunları · motor bloğu duvarı kirişe üstten 2 × M5 · alt motor 4 × M5 ·
  yatak plakası duvara 2 × M4 · kaplin motor miline + mil muylusuna setskur · dik mil segman (y 732) · göbek dik mile 2 × setskur · katlayıcı
  plakası göbeğe 2 × M5 · katlayıcı kolu arka bloğa 2 × M5, ön bloğa dişli ara pim üzerinden M5 (pim kanal duvarına geçme) · 2 palet braketi kola 2 × M5, bıçağa 2 × havşa M4 + somun ·
  kılavuz direkleri kirişe alttan M5, kılavuz milleri kirişten alttan M5 ve üst kapağa havşa M3, ayak plakaları 2 × M3 · dik rodlar kirişe alttan M6, üst plakalara havşa M5.
Hazır ürün (motor / dişli kutusu / sensör): ürüne dokunulmaz, bizim parça dişli; vida ürünün kendi deliğinden geçer (KURALLAR §3).
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
M = MB.Mek(g, (4830, 560, -400), (5240, 1000, 20))
Y, YM, X, XM, Z, ZM = (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)

# ---------------------------------------------------------------- 1 · şasi: 4 ayak kirişe üstten M6 · kalıp taban plakasına alttan M6
AYAK = [(4850.0, -358.0), (4850.0, -36.0), (5190.0, -358.0), (5190.0, -36.0)]
M.vida("kapak_sasi_kiris_vida", "kapak_sasi", "kapak_sasi", dis="M6", yon=YM, duzlem=826.0, pts=AYAK, kavrama=9.0, not_="kirişten (6 mm) ayağın üst ucuna (20 × 20, dişli)")
M.vida("kapak_sasi_taban_vida", "kalip_taban", "kapak_sasi", dis="M6", yon=Y, duzlem=622.0, pts=AYAK, kavrama=9.0, not_="kalıp tabanının 4 mm plakasından (baş tepsinin içinde, alttan) ayağın alt ucuna")
# ---------------------------------------------------------------- 2 · üst tahrik: dik plaka · motor plakası · dişli kutusu · adaptör · üst motor
M.vida("kapak_motor_dik_plaka_vida", "kapak_sasi", "kapak_motor_dik_plaka", dis="M5", yon=Y, duzlem=832.0, pts=[(4940.0, -145.0), (4980.0, -145.0)])
M.vida("kapak_motor_plakasi_vida", "kapak_motor_plakasi", "kapak_motor_dik_plaka", dis="M4", yon=Z, duzlem=-150.0, pts=[(4940.0, 876.5), (4980.0, 876.5)])
EKS = [(4960.0 + fx * 20.0, 911.5 + fy * 20.0) for fx, fy in ((-1, 0), (1, 0), (0, -1), (0, 1))]
M.vida("kapak_disli_motor_vida", "kapak_motor_plakasi", "kapak_disli_motor", dis="M4", yon=Z, duzlem=-150.0, pts=EKS, kavrama=8.0,
       not_="hazır ürün (planet dişli kutulu motor, fabrikada birleşik): dişli kutusu ön yüzünde 4 × M4 dişli delik (eksen noktaları, 40 mm kare)")
# yatak ayakları (10 mm plaka) kirişe alttan · yataklar (36 mm çelik) ayaklara üstten M5×50 · tahrik mili kol göbeğine setskur · ön yatakta segman
for i, z_ in ((0, -231.0), (1, -165.0)):
    M.vida("kapak_yatak_ayak_%d_vida" % i, "kapak_sasi", "kapak_yatak_ayak_%d" % i, dis="M5", yon=Y, duzlem=832.0, pts=[(4950.0, z_), (4970.0, z_)])
    M.vida("kapak_yatak_%d_vida" % i, "kapak_yatak_%d" % i, "kapak_yatak_ayak_%d" % i, dis="M5", yon=YM, duzlem=894.0, pts=[(4947.0, z_), (4973.0, z_)], kavrama=14.0)
M.setskur("kapak_kol_setskur", "kapak_kol", "kapak_tahrik_mili", yon=YM, pts=[(4960.0, -206.0)])
M.segman("kapak_tahrik_mili_segman", "kapak_tahrik_mili", -160.0, Z)
# sensör L braketleri (3 mm): 0 → yatak ayağı 1'in +x yüzüne 2 × M3 · 1 → kirişe ayağından 2 × M4 (üstten) · M8 sensör somunları
M.vida("kapak_sensor_blogu_0_vida", "kapak_sensor_blogu_0", "kapak_yatak_ayak_1", dis="M3", yon=XM, duzlem=4978.0, pts=[(866.0, -162.0), (878.0, -162.0)])
M.somun_mil("kapak_sensor_0_somun", "kapak_sensor_0", "kapak_sensor_blogu_0", yon=ZM, dis="M8")
M.vida("kapak_sensor_blogu_1_vida", "kapak_sensor_blogu_1", "kapak_sasi", dis="M4", yon=YM, duzlem=832.0, pts=[(5120.0, -306.0), (5120.0, -294.0)], kavrama=5.0)
M.somun_mil("kapak_sensor_1_somun", "kapak_sensor_1", "kapak_sensor_blogu_1", yon=Y, dis="M8")
# ---------------------------------------------------------------- 3 · alt tahrik: motor bloğu (6 mm flanş + 10 mm duvar) · alt motor · yatak plakası · kaplin · dik mil · göbek
M.vida("kapak_motor_blogu_vida", "kapak_sasi", "kapak_motor_blogu", dis="M5", yon=YM, duzlem=826.0, pts=[(5185.0, -312.0), (5185.0, -288.0)])
M.motor("kapak_motor_alt_vida", "kapak_motor_alt", "kapak_motor_blogu", yon=Y, flans=685.5, boy_flans=8.0, kav=5.5, dis="M5", kare=47.14, merkez=(5150.0, -300.5))
M.vida("kapak_yatak_plakasi_vida", "kapak_motor_blogu", "kapak_yatak_plakasi", dis="M4", yon=XM, duzlem=5180.0, pts=[(728.0, -325.0), (728.0, -275.0)])
M.setskur("kapak_kaplin_setskur_0", "kapak_kaplin", "kapak_motor_alt", yon=Z, pts=[(5150.0, 703.0)])
M.setskur("kapak_kaplin_setskur_1", "kapak_kaplin", "kapak_motor_mili", yon=Z, pts=[(5150.0, 716.0)])
M.segman("kapak_dik_mil_segman", "kapak_dik_mil", 732.0, Y)
M.setskur("kapak_katlayici_gobek_setskur", "kapak_katlayici_gobek", "kapak_dik_mil", yon=X, pts=[(850.0, -299.5), (875.0, -299.5)], dis="M5")
# ---------------------------------------------------------------- 4 · katlayıcı: plaka göbeğe · kol arka bloğa · ön blok pim üzerinden somunlu · palet braketi (yeni) · bıçak
M.vida("kapak_katlayici_plaka_vida", "kapak_katlayici_plaka", "kapak_katlayici_gobek", dis="M5", yon=YM, duzlem=890.0, pts=[(5164.0, -310.0), (5164.0, -282.0)])
M.vida("kapak_katlayici_kol_vida", "kapak_katlayici_kol", "kapak_katlayici_blok_arka", dis="M5", yon=X, duzlem=5151.6, pts=[(895.0, -337.5)], not_="bloğun kulağından (8,4 mm)")
M.vida("kapak_katlayici_kol_vida_2", "kapak_katlayici_kol", "kapak_katlayici_blok_arka", dis="M4", yon=X, duzlem=5151.6, pts=[(912.0, -342.5)], not_="8,4 mm boşluktan blok gövdesine (kızak burcunun arkasından, z −342,5)")
M.vida("kapak_katlayici_blok_on_vida", "kapak_katlayici_kol", "kapak_katlayici_pim", dis="M5", yon=X, duzlem=5151.6, pts=[(895.0, -75.0)], kavrama=5.0,
       not_="koldan dişli ara pime (Ø10 × 8,4, M5 iç dişli, tutuş 5 = 1×d; uç pim içinde kalır); pimin öbür ucu ön bloğun kanal duvarındaki deliğe sıkı geçme (kanal içinde kızak burcu: somun / uzun vida yeri yok)")
# palet braketi × 2 (kademeli lama 6 × 50; kolun ucu z −218…−194 arasında süpürdüğü için arka 135 + ön 125 mm iki parça): alt 25 mm (6 kalın) kola, üst 25 mm (3 kalın) bıçağa
for i, (z0, z1, zz) in enumerate(((-360.0, -225.0, (-340.0, -245.0)), (-187.0, -62.0, (-167.0, -82.0)))):
    BRK = (cq.Workplane("XY").box(6.0, 25.0, z1 - z0, centered=False).translate((5130.6, 919.0, z0))
           .union(cq.Workplane("XY").box(3.0, 25.0, z1 - z0, centered=False).translate((5130.6, 944.0, z0))).val())
    ad = "kapak_palet_braketi_%d" % i
    M.yeni(ad, BRK, ["Palet braketi AISI 304 kademeli lama 6 × 50 × %g (alt 25 mm 6 kalın kola, üst 25 mm 3 kalın bıçağa)" % (z1 - z0), 1, "6 × 50 × %g" % (z1 - z0), "lama + freze · 0.25 kg", "ÜRETİM"],
           "E_MEK_BAG__paslanmaz", aile="kapak_katlayici", kontrol=[((5130.6, 919.0, z0), (5136.6, 944.0, z1)), ((5130.6, 944.0, z0), (5133.6, 969.0, z1))])
    M.vida("%s_vida" % ad, ad, "kapak_katlayici_kol", dis="M5", yon=X, duzlem=5136.6, pts=[(931.5, zz[0]), (931.5, zz[1])])
    M.somunlu("%s_bicak_vida" % ad, ad, "kapak_katlayici_paleti", dis="M4", std="DIN7991", yon=X, duzlem=5133.6, pts=[(956.5, zz[0]), (956.5, zz[1])],
              not_="havşa başlı, braket + 3 mm bıçak, bıçağın arkasında pul + fiberli somun")
# ---------------------------------------------------------------- 5 · kılavuz direkleri + milleri · dik rodlar + üst plakalar
for i, z_ in ((0, -330.0), (1, -75.0)):
    M.vida("kapak_profil_%d_vida" % i, "kapak_sasi", "kapak_profil_%d" % i, dis="M5", yon=Y, duzlem=832.0, pts=[(5194.5, z_ - 6.0)])   # baş motor bloğu duvarının (x ≤ 5190 · z ≥ −330) dışında
    M.vida("kapak_kilavuz_mil_%d_alt_vida" % i, "kapak_sasi", "kapak_kilavuz_mil_%d" % i, dis="M5", yon=Y, duzlem=832.0, pts=[(5175.0, z_)], kavrama=7.5,
           not_="kirişten (6), ayak plakasının deliğinden milin alt ucuna")
    M.vida("kapak_profil_ayak_%d_vida" % i, "kapak_sasi", "kapak_profil_ayak_%d" % i, dis="M3", yon=Y, duzlem=832.0, pts=[(5166.0, z_ + 9.0), (5184.0, z_ - 9.0)], kavrama=4.5)   # çapraz: başlar motor bloğu duvarının (x 5180–5190 · z ≥ −330) dışında
    M.vida("kapak_kilavuz_mil_%d_ust_vida" % i, "kapak_profil_kapak_%d" % i, "kapak_kilavuz_mil_%d" % i, dis="M3", std="DIN7991", yon=YM, duzlem=974.0, pts=[(5177.5, z_)], kavrama=6.0,
           not_="direğin üst kapağındaki tapadan milin üst ucuna (havşa)")
for i, z_ in ((0, -316.0), (1, -96.0)):
    M.vida("kapak_dik_rod_%d_alt_vida" % i, "kapak_sasi", "kapak_dik_rod_%d" % i, dis="M6", yon=Y, duzlem=832.0, pts=[(5000.0, z_)], kavrama=9.0)
    M.vida("kapak_dik_rod_%d_ust_vida" % i, "kapak_ust_plaka_%d" % i, "kapak_dik_rod_%d" % i, dis="M5", std="DIN7991", yon=YM, duzlem=977.0, pts=[(5000.0, z_)], kavrama=9.0)

M.bitir(go, "E_MEK_BAG__vida", "82", mek=36, mek_kod="E/Kutu katlama", ek=dict(aile=["kapak", "kapak_katlayici"]),
        ek_dugum={"_sablon": {"E_MEK_BAG__paslanmaz": "E_GOVDE__sac"}})
LOG("%.0f sn" % (time.time() - t0))
sys.stdout.flush(); os._exit(0)
