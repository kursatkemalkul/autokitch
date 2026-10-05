# -*- coding: utf-8 -*-
"""HAT v3.9 · YAMA ZİNCİRİ (gece 2 · adım 4 · 4 Eki 2026 · Claude · YEREL)
2–4 Ekim'de modele DOĞRUDAN GLB betikleriyle yapılan bütün değişiklikler burada, ÖZGÜN betiklerle ve ÖZGÜN sırayla yeniden uygulanır.
Taban: montaj v7'nin GLB'si (hat3_v7.glb · montaj v7 deterministik, iki ayrı derlemede bayt bayt aynı). Çıkış: adım 31 = hat3_v8zq ile aynı model;
4 Eki adım 5-entegrasyon 1. tur: adım 33–36 (A, B, E, U üretim sacı · yama_v9/33_a_sac.py … 36_u_sac.py + sac_ent.py) → hat3_v9d.glb; 2. tur adım 37–38 (TOPPING, F) → hat3_v9f.glb (= v9 çıkışı).

Nasıl çalışır: kaynak/ klasörü (scratchpad'deki düzen AYNEN) iş klasörüne kopyalanır; dosyalardaki yer tutucular (@@KOK_W@@ …) iş klasörünün
yoluyla doldurulur; ara GLB'ler özgün adlarıyla (hat3_v8.glb, hat3_v8c.glb … hat3_v8zq.glb, t1.glb, e1.glb …) aynı klasörlerde üretilir.
Her adımın betiği, girdisi, çıktısı ve ne yaptığı: SIRA.md.

Kullanım:
  python zincir.py --is <iş_klasörü> --taban <hat3_v7.glb> --cikis <hat3_v9.glb> --uretec <arastirma/_uretec> [--h3 <arastirma/_uretec/h3>]
  python zincir.py ... --adim 05 --girdi-dizin <kayıtlı GLB'lerin klasörü>   (tek adım doğrulama: girdiler kayıtlı GLB'lerden bağlanır)
  python zincir.py --is <iş> --uretec <arastirma/_uretec> --adim 34-38 --girdi-dizin <klasör>   (aralık: --girdi-dizin YALNIZ ilk adımın girdisini bağlar;
        sonraki adımlar iş klasöründe üretilenleri kullanır · 37 / 38 ayrıca iş kökünde hat3_v8zq.glb ister (DEGISEN kutuları) → elle bağla)

Ortam değişkenleri (calis() kurar / adım betikleri kurar):
  YAMA_URETEC   = --uretec (derleme ağacının _uretec'i) · adım 33+ üreteçleri <uretec>/h3/h3_<ist>_sac_v1.py'den import eder (sac_ent.py sys.path'e ekler)
  YAMA_IS_KOK   = iş klasörü (sac_ent.KOK: m8kit, tg/glb_sikistir, govde_denetim_dogru, hat3_v8zq.glb oradan)
  AUTOKITCH_SAC_STANDART = zincir.py KURMAZ — adım 00–31 onsuz koşmuştu (kurulursa çıktıları değişir); adım 33+ sac_ent.py setdefault ile
                  yama_v9/sac_standart'a kurar (dışarıdan verilmişse o kullanılır → bayt aynılık için verme)
  ADIM5         = sac_ent.py kurar: yama_v9/veri (E / U üreteci _bilesen_v8zq.pkl kutularından mekanizma FHP saplamalarını kurar; yalnız okunur)
  PYTHONIOENCODING=utf-8 · PYTHONDONTWRITEBYTECODE=1 (calis) · --iz: YAMA_IZ_KOK / YAMA_IZ_DOSYA + _iz/sitecustomize.py
"""
import argparse, io, os, shutil, subprocess, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
KAYNAK = os.path.join(HERE, "kaynak")

A_SIL = ('"A_GOVDE:a_govde_ust,a_ust_kusak_arka,a_ust_kusak_sol,a_ust_kusak_sag,onyuz_cerceve_ust_kayit" '
         '"U_A_GOVDE:ust_a_taban_sac,onyuz_ust_a_alt_kayit"')
# (no, kısa ad, girdiler (iş köküne göre), çıktı, [(cwd, komut), ...])
ADIMLAR = [
    ("00", "A ↔ U_A ara çerçevesi sil (v3.8)", ["hat3_v7.glb"], "hat3_v8.glb",
     [(".", "python glb_parca_sil.py hat3_v7.glb _v7/parca_kutulari.json hat3_v8.glb " + A_SIL)]),
    ("01", "A dikmeler/arka/sol sac tavana, perde + emniyet kalkar, alt kayıt (v8b+c)", ["hat3_v8.glb"], "hat3_v8c.glb",
     [(".", "python glb_duzenle.py hat3_v8.glb _v7/parca_kutulari.json hat3_v8c.glb islem_v38bc.json")]),
    ("02", "A gövdesi yeniden (kapalı ürün, tabla geçişi ağzı)", ["hat3_v8c.glb"], "hat3_v8k.glb",
     [(".", "python a_govde_yeni.py hat3_v8c.glb hat3_v8k.glb")]),
    ("03", "B ön çerçeve sacı gövde malzemesine", ["hat3_v8k.glb"], "hat3_v8l.glb",
     [(".", "python b_cerceve_govde.py hat3_v8k.glb hat3_v8l.glb")]),
    ("04", "B gövdesi yeniden", ["hat3_v8l.glb"], "hat3_v8n.glb",
     [(".", "python b_govde_yeni.py hat3_v8l.glb hat3_v8n.glb")]),
    ("05", "TOPPING gövdesi yeniden + sıkıştır", ["hat3_v8n.glb"], "hat3_v8o.glb",
     [(".", "python -u topping_govde_yeni.py hat3_v8n.glb hat3_v8o.glb"),
      (".", "python tg/glb_sikistir.py hat3_v8o.glb hat3_v8o_s.glb && mv -f hat3_v8o_s.glb hat3_v8o.glb"),
      (".", "python v9yama/pu_sira.py hat3_v8o.glb v9yama/pu_sira_v8o.json")]),   # v9: PU köşe SIRASI kayıtlı v8o'ya (geometri aynı; OCC yüz sırası)
    ("06", "B fitil + TOPPING baş açı altı + U gövdesi", ["hat3_v8o.glb"], "hat3_v8p.glb",
     [(".", "python b_fitil_duzelt.py hat3_v8o.glb _m1.glb"),
      (".", "python topping_basac_alt.py _m1.glb _m2.glb"),
      (".", "python ug/u_govde_yeni_v8o.py _m2.glb hat3_v8p.glb ug/u_parca_kutulari_v8p.json")]),   # v8p'deki U sürümü (21:45'te değiştirilmeden önce ug/'ye yedeklenen)
    ("07", "E gövdesi yeniden", ["hat3_v8p.glb"], "hat3_v8r.glb",
     [(".", "python e_govde_yeni.py hat3_v8p.glb hat3_v8r.glb")]),
    ("08", "E düzeltmeleri", ["hat3_v8r.glb"], "hat3_v8s.glb",
     [(".", "python e_duzelt.py hat3_v8r.glb hat3_v8s.glb")]),
    ("09", "pano fiş etiketleri", ["hat3_v8s.glb"], "hat3_v8t.glb",
     [(".", "python pano_fis_etiket.py hat3_v8s.glb hat3_v8t.glb _v7/parca_kutulari.json")]),
    ("10", "U gövdesi (v8u)", ["hat3_v8t.glb"], "hat3_v8u.glb",
     [(".", "python u_govde_yeni.py hat3_v8t.glb hat3_v8u.glb ug/u_parca_kutulari_v8u.json")]),
    ("11", "F üst kabin yeniden", ["hat3_v8u.glb"], "hat3_v8v.glb",
     [(".", "python f_kabin_yeni.py hat3_v8u.glb hat3_v8v.glb")]),
    ("12", "gece madde 1–6 (K ara raf, tabla geçişi, sağ kablo, E kaide, zemin, kpk)", ["hat3_v8v.glb"], "hat3_v8w.glb",
     [(".", "python gece/m1_k_ara_taban_sil.py hat3_v8v.glb hat3_v8w1.glb"),
      (".", "python gece/m2_tabla_gecis.py hat3_v8w1.glb hat3_v8w2.glb"),
      (".", "python gece/m3_topping_sag_kablo.py hat3_v8w2.glb hat3_v8w3.glb"),
      (".", "python gece/m4_e_kaide_hiza.py hat3_v8w3.glb hat3_v8w4.glb"),
      (".", "python gece/m5_zemin_duz.py hat3_v8w4.glb hat3_v8w5.glb"),
      (".", "python gece/m6_kapak_parcalari_kpk.py hat3_v8w5.glb hat3_v8w6.glb && cp hat3_v8w6.glb hat3_v8w.glb")]),
    ("13", "madde 7 TOPPING UNO/kaset yerleşimi (7a/7b/7c) + sıkıştır", ["hat3_v8w.glb"], "hat3_v8x.glb",
     [("gece", "mkdir -p m7 && python m7a_birim_tasi.py ../hat3_v8w.glb m7/v8x_a.glb"),
      ("gece", "python m7b_kabuk.py m7/v8x_a.glb m7/v8x_b.glb"),
      ("gece", "python m7c_mandal_kablo.py m7/v8x_b.glb m7/v8x_c.glb"),
      (".", "cp gece/m7/v8x_c.glb hat3_v8x.glb && python tg/glb_sikistir.py hat3_v8x.glb gece/m7/v8x_sik.glb && cp gece/m7/v8x_sik.glb hat3_v8x.glb")]),
    ("14", "madde 8 çakışma/kablo/pnömatik/delik/havada + sıkıştır", ["hat3_v8x.glb"], "hat3_v8y.glb",
     [("gece", "python m8_fix_1_cakisma.py ../hat3_v8x.glb ../hat3_v8y1.glb"),
      ("gece", "python m8_fix_2_kablo.py ../hat3_v8y1.glb ../hat3_v8y2.glb"),
      ("gece", "python m8_fix_3_pnomatik.py ../hat3_v8y2.glb ../hat3_v8y3.glb"),
      ("gece", "python m8_fix_4_delik.py ../hat3_v8y3.glb ../hat3_v8y4.glb"),
      ("gece", "python m8_fix_5_havada.py ../hat3_v8y4.glb ../hat3_v8y5.glb"),
      (".", "python tg/glb_sikistir.py hat3_v8y5.glb hat3_v8y.glb")]),
    ("15", "madde 8 tur 2 ana hat kablo şeritleme + madde 3 + sıkıştır", ["hat3_v8y.glb"], "hat3_v8z.glb",
     [("gece", "python m8t2_yaz.py ../hat3_v8y.glb m8t2/yollar_z2.json ../hat3_v8z1.glb --oluk"),
      ("gece", "python m8t2_madde3.py ../hat3_v8z1.glb ../hat3_v8z2.glb"),
      ("gece", "python ../tg/glb_sikistir.py ../hat3_v8z2.glb ../hat3_v8z.glb")]),
    ("16", "madde 8 tur 3 davlumbaz derzi + sıkıştır", ["hat3_v8z.glb"], "hat3_v8za.glb",
     [("gece", "mkdir -p m8t3 && python m8t3_derz.py ../hat3_v8z.glb m8t3/hat3_v8za1.glb"),
      ("gece/m8t3", "python ../../tg/glb_sikistir.py hat3_v8za1.glb hat3_v8za.glb && cp hat3_v8za.glb ../../hat3_v8za.glb")]),
    ("17", "gruplama: montaj ağacı + disiplin etiketleri", ["hat3_v8za.glb"], "hat3_v8zb.glb",
     [("grup", "python grup_duzen.py ../hat3_v8za.glb ../hat3_v8zb.glb")]),
    ("18", "TOPPING cep geri + evaporatör ikiye + A boş (t1–t6) + sıkıştır", ["hat3_v8zb.glb"], "hat3_v8zc.glb",
     [("topfix", "python t1_sil.py ../hat3_v8zb.glb t1.glb"),
      ("topfix", "python t2_tasi.py t1.glb t2.glb"),
      ("topfix", "python t3_kabuk.py t2.glb t3.glb"),
      ("topfix", "python t4_evap.py t3.glb t4.glb"),
      ("topfix", "python t5_bagli.py t4.glb t5.glb"),
      ("topfix", "python t6_duzelt.py t5.glb t6.glb"),
      ("topfix", "python ../tg/glb_sikistir.py t6.glb ../hat3_v8zc.glb")]),
    ("19", "robot kalktı + 3 kademe + E oluk + perde (p1, p2) + sıkıştır", ["hat3_v8zc.glb"], "hat3_v8zd.glb",
     [("paket", "mkdir -p zc"),
      ("paket/zc", "python ../../gece/m8/m8_yukle.py ../../hat3_v8zc.glb"),
      ("paket", "python p1_glb.py ../hat3_v8zc.glb zc p1.glb"),
      ("paket", "python p2_dugum.py p1.glb p2.glb"),
      ("paket", "python ../tg/glb_sikistir.py p2.glb hat3_v8zd.glb && cp hat3_v8zd.glb ../hat3_v8zd.glb")]),
    ("20", "K alt yeniden (istasyon rafı + 6 destek)", ["hat3_v8zd.glb"], "hat3_v8ze.glb",
     [("kalt", "python k_alt.py ../hat3_v8zd.glb ../hat3_v8ze.glb")]),
    ("21", "TOPPING paketi (tp1 duvar, tp2 evaporatör, tp3 pnömatik, tp4 motor) + sıkıştır", ["hat3_v8ze.glb"], "hat3_v8zf.glb",
     [("tpaket", "bash zincir.sh ../hat3_v8ze.glb ../hat3_v8zf.glb")]),
    ("22", "QR + tezgâh + kablo paketi (q1–q6, birlesim) + sıkıştır", ["hat3_v8zf.glb"], "hat3_v8zh.glb",
     [("birlesim", "bash calistir.sh ../hat3_v8zf.glb ../hat3_v8zh.glb")]),
    ("23", "KD3 kör tapalar + sıkıştır", ["hat3_v8zh.glb"], "hat3_v8zi.glb",
     [("kalanlar", "python t3_tapa.py ../hat3_v8zh.glb t3.glb"),
      (".", "python tg/glb_sikistir.py kalanlar/t3.glb hat3_v8zi.glb")]),
    ("24", "elektrik zinciri (e1 sil, e2 zincir, e3 renk) + sıkıştır", ["hat3_v8zi.glb"], "hat3_v8zj.glb",
     [("elk2", "python e1_sil.py ../hat3_v8zi.glb e1.glb"),
      ("elk2", "mkdir -p e1c"),
      ("elk2/e1c", "python ../../gece/m8/m8_yukle.py ../e1.glb"),
      ("elk2", "python -u e2_zincir.py e1.glb e1c/m8_onbellek.npz e2.glb"),
      ("elk2", "python e3_renk.py e2.glb e3.glb"),
      ("elk2", "python ../tg/glb_sikistir.py e3.glb ../hat3_v8zj.glb")]),
    ("25", "elektrik içeriden (e4) + sıkıştır", ["hat3_v8zj.glb"], "hat3_v8zk.glb",
     [("elk3", "python e4.py ../hat3_v8zj.glb e4.glb"),
      (".", "python tg/glb_sikistir.py elk3/e4.glb hat3_v8zk.glb")]),
    ("26", "iç kablolama temizliği (b4: ts ks fs us bs) + sıkıştır", ["hat3_v8zk.glb"], "hat3_v8zl.glb",
     [(".", "python elk4/cikar.py hat3_v8zk.glb"),
      ("elk4", "python b4.py ../hat3_v8zk.glb e5.glb ts ks fs us bs"),
      (".", "python tg/glb_sikistir.py elk4/e5.glb hat3_v8zl.glb")]),
    ("27", "panodaki eski ana şalter kalktı", ["hat3_v8zl.glb"], "hat3_v8zm.glb",
     [("salt", "python yap.py")]),
    ("28", "iç kablolama son tur + pano arka çıkışı (b5: qr5 k5 b5 p5) + sıkıştır", ["hat3_v8zm.glb"], "hat3_v8zn.glb",
     [("elk5", "python cikar.py ../hat3_v8zm.glb"),
      ("elk5", "python b5run.py ../hat3_v8zm.glb e6.glb qr5 k5 b5 p5"),
      ("elk5", "python ../tg/glb_sikistir.py e6.glb ../hat3_v8zn.glb")]),
    ("29", "ön yüz derz hizası (gece 2 adım 0)", ["hat3_v8zn.glb"], "hat3_v8zo.glb",
     [("derz", "python derz_hiza.py ../hat3_v8zn.glb ../hat3_v8zo.glb")]),
    ("30", "QR hizası + tezgâh 180° + B kanal köşeleri + teyit + hava kanalları (gece 2 adım 2) + sıkıştır", ["hat3_v8zo.glb"], "hat3_v8zp.glb",
     [("gece2/adim2/hava", "python cikar_h.py ../../../hat3_v8zo.glb"),
      ("gece2/adim2", "python a1_qr_tezgah.py ../../hat3_v8zo.glb a1.glb"),
      ("gece2/adim2", "python a2_b_kose.py a1.glb a2.glb"),
      ("gece2/adim2", "python a3_teyit.py a2.glb a3.glb"),
      ("gece2/adim2", "python a4_hava.py a3.glb a4.glb"),
      ("gece2/adim2", "python ../../tg/glb_sikistir.py a4.glb ../../hat3_v8zp.glb")]),
    ("31", "kaşar v15 + sucuk v9 kaset iç çakışmaları (gece 2 adım 3) + sıkıştır", ["hat3_v8zp.glb"], "hat3_v8zq.glb",
     [("gece2/adim3", 'python a1_kaset.py "{KOK}/hat3_v8zp.glb" "{KOK}/gece2/adim3/a1.glb"'),   # betik os.chdir(üreteç) yapar → mutlak yol
      ("gece2/adim3", "python ../../tg/glb_sikistir.py a1.glb ../../hat3_v8zq.glb")]),
    # --- gece 2 · adım 5-entegrasyon 1. tur (üretim sacı gövdeleri; betikler yama_v9/ altında, ortak araç sac_ent.py · 32 boş: TOPPING + F 2. turda) ---
    ("33", "A üretim sacı gövdesi (h3_a_sac_v1) + karşı taraf delik / PEM", ["hat3_v8zq.glb"], "hat3_v9a.glb",
     [(".", 'python "{YAMA}/33_a_sac.py" hat3_v8zq.glb hat3_v9a.glb')]),
    ("34", "B üretim sacı gövdesi (h3_b_sac_v1) + ray havşa delikleri + perçin somunlar", ["hat3_v9a.glb"], "hat3_v9b.glb",
     [(".", 'python "{YAMA}/34_b_sac.py" hat3_v9a.glb hat3_v9b.glb')]),
    ("35", "E üretim sacı gövdesi (h3_e_sac_v1) + mekanizma FHP delikleri", ["hat3_v9b.glb"], "hat3_v9c.glb",
     [(".", 'python "{YAMA}/35_e_sac.py" hat3_v9b.glb hat3_v9c.glb')]),
    ("36", "U_F + U_KE + F üst kabin üretim sacı (h3_u_sac_v1) + mekanizma FHP delikleri + K üst sacı PEM", ["hat3_v9c.glb"], "hat3_v9d.glb",
     [(".", 'python "{YAMA}/36_u_sac.py" hat3_v9c.glb hat3_v9d.glb')]),
    # --- adım 5-entegrasyon 2. tur: TOPPING + F (adım 5c üreteçleri) ---
    ("37", "TOPPING üretim sacı gövdesi (h3_topping_sac_v2: dimple, bükümlü iç sac + perçin + PU levha, evaporatör ayakları, kanal deliği) + F sol yan Ø9 + B perçin somunları + FHP delikleri", ["hat3_v9d.glb"], "hat3_v9e.glb",
     [(".", 'python "{YAMA}/37_topping_sac.py" hat3_v9d.glb hat3_v9e.glb')]),
    ("38", "F üretim sacı (h3_f_sac_v1: ön kapaklar, atış kanalı, baca) + U_F tavanı Ø6,6", ["hat3_v9e.glb"], "hat3_v9f.glb",
     [(".", 'python "{YAMA}/38_f_sac.py" hat3_v9e.glb hat3_v9f.glb')]),
    # --- gece 2 · adım 8: servis düzeltmeleri + acil stop ---
    ("39", "servis D2–D4: üst kayıt sağ yarısı cıvatalı, yağ lansı kaplinleri + M12, kompresör spiral halka + fişli besleme", ["hat3_v9f.glb"], "hat3_v9g.glb",
     [(".", 'python "{YAMA}/39_servis.py" hat3_v9f.glb hat3_v9g.glb')]),
    ("40", "6 acil stop butonu (Schneider XB4BS8442) — TOPPING, B, F, K, E, QR servis yüzü", ["hat3_v9g.glb"], "hat3_v9h.glb",
     [(".", 'python "{YAMA}/40_acil_stop.py" hat3_v9g.glb hat3_v9h.glb')]),
    ("41", "TOPPING iç geçişler (piston kovanı, bakır soket, hortum yatağı, valf yuvası) + QR Cat6A ayrı şerit + B ön çerçeve derz dolgusu", ["hat3_v9h.glb"], "hat3_v9i.glb",
     [(".", 'python "{YAMA}/41_gecis_kablo.py" hat3_v9h.glb hat3_v9i.glb')]),
    ("42", "havada kalan 9 grup (ELK_IC kanal, DOLAP / K kablosu, RevPi DIO / AIO) en yakın taşıyıcıya oturtuldu", ["hat3_v9i.glb"], "hat3_v9j.glb",
     [(".", 'python "{YAMA}/42_havada_oturt.py" hat3_v9i.glb hat3_v9j.glb')]),
    ("43", "B çekmece ray vidaları DIN 7991 M5 × 10 → M5 × 6 (126 adet, uç başa doğru 4 mm)", ["hat3_v9j.glb"], "hat3_v9k.glb",
     [(".", 'python "{YAMA}/43_ray_vida.py" hat3_v9j.glb hat3_v9k.glb')]),
    ("44", "B 21 çekmece düzeltmesi: ayrı kayış çenesi + tabla + mıknatıs kulağı, reed plakası + vidalar, sensör plakası sil, avara mili +1 + E segman, motor braketi delik/vida/PEM, köşebent + M4, braket saplamaları, kapak PU, köpük kapağı 1 mm derin", ["hat3_v9k.glb"], "hat3_v9l.glb",
     [(".", 'python "{YAMA}/44_cekmece_duzeltme.py" hat3_v9k.glb hat3_v9l.glb')]),
    ("45", "6 acil stop butonu kaldırıldı (adım 40 geri alındı: düğümler silindi, kapak / PU cepleri v9g bileşeniyle kapandı)", ["hat3_v9l.glb", "hat3_v9g.glb"], "hat3_v9m.glb",
     [(".", 'python "{YAMA}/45_acil_stop_kaldir.py" hat3_v9l.glb hat3_v9g.glb hat3_v9m.glb')]),
    ("46", "B PU levhaları yeniden kesildi: arka 2 katman, sol ana levha + arka şerit + 6 köşe dolgu şeridi, teknik depo PU köşe şeritleri (hacim aynı)", ["hat3_v9m.glb"], "hat3_v9n.glb",
     [(".", 'python "{YAMA}/46_b_pu_levha.py" hat3_v9m.glb hat3_v9n.glb')]),
    ("47", "B bağlantı elemanları: dikme ayakları, evaporatör braketleri, soğutma grubu, elektrik plakası, istasyon kutusu, zincir kanalı, ışınım sacı, iç kanallar; kapalı uçlu M8 perçin somun + M8 × 16; fan kablosu kanal deliklerinden", ["hat3_v9n.glb"], "hat3_v9o.glb",
     [(".", 'python "{YAMA}/47_b_baglanti.py" hat3_v9n.glb hat3_v9o.glb')]),
    ("48", "A bağlantı açıkları (A montaj animasyonu v3): A–B pulu ISO 7092, açıcı cıvatasına DIN 125, tabla rayı M6 5 mm aşağı, açıcı flanşı 120 × 155, A–TOPPING M8 × 16 → × 10", ["hat3_v9o.glb"], "hat3_v9p.glb",
     [(".", 'python "{YAMA}/48_a_tamamla.py" hat3_v9o.glb _48.glb && python tg/glb_sikistir.py _48.glb hat3_v9p.glb && rm -f _48.glb')]),
    ("49", "B iç kabuk: iç sac kenarlarında bükümlü flanş (taban / tavan / arka / sol / bölme) + DIN 7337 Ø4 kör perçin; açık bölme PU levhaları kapatıldı", ["hat3_v9p.glb"], "hat3_v9q.glb",
     [(".", 'python "{YAMA}/49_b_ic_kabuk.py" hat3_v9p.glb hat3_v9q.glb')]),
    ("50", "GLB sıkılaştırma: silinmiş (dejenere) üçgenler ve kullanılmayan köşeler atıldı, kat / mek / kpk aralıkları taşındı (geometri aynı)", ["hat3_v9q.glb"], "hat3_v9r.glb",
     [(".", 'python "{YAMA}/50_sikilastir.py" hat3_v9q.glb hat3_v9r.glb')]),
    ("51", "B taşıyıcı üst kirişte perçin somun deliği içindeki 2 hayalet disk (Ø8 × 2, hiçbir parçaya değmiyor, delik kesicisinin çekirdeği) silindi", ["hat3_v9r.glb"], "hat3_v9s.glb",
     [(".", 'python "{YAMA}/51_b_hayalet_disk.py" hat3_v9r.glb hat3_v9s.glb')]),
    ("52", "ana pano U (üst depo) istasyonuna ait: 'Elektrik/Ana pano' → 'U/Elektrik' (U arka düzleminin gerisindeki bina kablosu ucu → 'Elektrik/Ana hat'), boş ünite listeden çıktı · geometri aynı", ["hat3_v9s.glb"], "hat3_v9t.glb",
     [(".", 'python "{YAMA}/52_pano_u.py" hat3_v9s.glb hat3_v9t.glb')]),
    ("53", "TOPPING yeni menü (menu7): Lahmacun harcı / Kıyma (YENİ orta UNO, paslanmaz dirsek + dik D32 hortum + yeni düşme kovanı) / Patates (eski sos) / Tavuk / Kuşbaşı (ön-sağ köşe cebi) · 5 hazne R25 · harç +30 · sağ evaporatörde yalıtımlı silindir cebi · 2 yeni hava hortumu · ünite 55 → 56", ["hat3_v9t.glb"], "hat3_v9u.glb",
     [(".", 'python "{YAMA}/53_menu7.py" hat3_v9t.glb hat3_v9u.glb')]),
    ("54", "kuşbaşı hunisi tam dik kenar: sağ (kıyma hortumu tarafı) duvar önden arkaya düz x 1880 (boyun dış yüzüne teğet) · ön-sağ köşe cebi kalktı · hortum ↔ hazne sürekli boşluk", ["hat3_v9u.glb"], "hat3_v9v.glb",
     [(".", 'python "{YAMA}/54_kusbasi_dik.py" hat3_v9u.glb hat3_v9v.glb')]),
    ("55", "standart uyum · pul tek standart: M5 DIN 9021 → ISO 7089 (A, K, E) · M8 DIN 9021 / DIN 125 → ISO 7092 (A, TOPPING, B şase, U_F, K) · baş / somun Δ kalınlık kadar sac tarafına (sac_standart/sac_uyum_v1.json)", ["hat3_v9v.glb"], "hat3_v9w.glb",
     [(".", 'python "{YAMA}/55_uyum.py" hat3_v9v.glb hat3_v9w.glb')]),
    ("56", "sol evaporatör 2. ayağı 3 mm dar (x 1620 → 1623, 30 → 27 mm): tavuk UNO silindirinin duvar flanşı arkadan geçerken ayağın dik kolunu 2 mm sıyırıyordu (TOPPING montaj v5 yol denetimi)", ["hat3_v9w.glb"], "hat3_v9x.glb",
     [(".", 'python "{YAMA}/56_evap_ayak.py" hat3_v9w.glb hat3_v9x.glb')]),
    ("57", "servis sacı yatay kablo kanalı 4 evaporatör ayağı hizasından 2 mm boşlukla kesik (4 parça: servis sacı arkadan kapanırken / bakımda çıkarken kanal ayakların içinden geçiyordu) · boş rakor 1476 → 1608", ["hat3_v9x.glb"], "hat3_v9y.glb",
     [(".", 'python "{YAMA}/57_kanal_kesik.py" hat3_v9x.glb hat3_v9y.glb')]),
    ("58", "TEK acil stop (Kemal 5 Eki): ana şalterin önündeki kapakta — F sağ üst kapağı (3625, 1600, z 79) · Schneider XB4BS8442 Ø40 + ZBY9330T Ø60 · kapakla döner", ["hat3_v9y.glb"], "hat3_v9z.glb",
     [(".", 'python "{YAMA}/58_acil_stop.py" hat3_v9y.glb hat3_v9z.glb')]),
    ("59", "kapı emniyet anahtarları (STANDART_DURUM madde 3): 10 ön kapak — Schmersal RSS36 kodlu sensör + aktüatör (K: AZM40 kilitli), mandal tarafında kapak arkası, gerekirse 2 mm braket", ["hat3_v9z.glb"], "hat3_v10a.glb",
     [(".", 'python "{YAMA}/59_kapi_emniyet.py" hat3_v9z.glb hat3_v10a.glb')]),
    ("60", "hava hattı emniyet valfi (STANDART_DURUM madde 8): kompresör çıkış hortumuna Festo MS6-SV-E (yumuşak başlatma + hızlı boşaltma) + bobin + susturucu · hortum iki parçaya", ["hat3_v10a.glb"], "hat3_v10b.glb",
     [(".", 'python "{YAMA}/60_hava_emniyet.py" hat3_v10a.glb hat3_v10b.glb')]),
]
SON = "hat3_v10b.glb"


def kur(is_dizin, h3, uretec):
    """kaynak/ → iş klasörü (yer tutucular doldurulur)"""
    kok_w = os.path.abspath(is_dizin)
    yer = {"@@PK_V7_F@@": os.path.join(kok_w, "_v7", "parca_kutulari.json").replace("\\", "/"),
           "@@PK_V7_W@@": os.path.join(kok_w, "_v7", "parca_kutulari.json"),
           "@@PK_V7_M@@": "/" + os.path.join(kok_w, "_v7", "parca_kutulari.json").replace("\\", "/").replace(":", "", 1),
           "@@MEK_V3_W@@": os.path.join(kok_w, "_v7", "mekanizma_v3.json"),
           "@@H3_W@@": os.path.abspath(h3),
           "@@KOK_WW@@": kok_w.replace("\\", "\\\\"),
           "@@KOK_W@@": kok_w,
           "@@KOK_F@@": kok_w.replace("\\", "/"),
           "@@KOK_M@@": "/" + kok_w.replace("\\", "/").replace(":", "", 1)}
    for r, ds, fs in os.walk(KAYNAK):
        for f in fs:
            a = os.path.join(r, f); b = os.path.join(kok_w, os.path.relpath(a, KAYNAK))
            os.makedirs(os.path.dirname(b), exist_ok=True)
            if f.endswith((".py", ".sh")):
                s = io.open(a, encoding="utf-8", errors="surrogateescape").read()
                for k, v in yer.items(): s = s.replace(k, v)
                io.open(b, "w", encoding="utf-8", errors="surrogateescape", newline="").write(s)
            else:
                shutil.copy2(a, b)


def baglan(kaynak, hedef):
    if os.path.exists(hedef): os.remove(hedef)
    try: os.link(kaynak, hedef)
    except OSError: shutil.copy2(kaynak, hedef)


IZ_KOD = r"""
import sys, os
_K = os.environ.get("YAMA_IZ_KOK", "").lower().replace("\\", "/")
_D = os.environ.get("YAMA_IZ_DOSYA")
_A = set()
def _h(ev, args):
    if ev == "open" and args and isinstance(args[0], str):
        try:
            p = os.path.abspath(args[0]).lower().replace("\\", "/")
        except Exception:
            return
        if p.startswith(_K) and p not in _A and not p.endswith("acilan.txt"):
            _A.add(p)
            with open(_D, "a", encoding="utf-8") as f_: f_.write(p + chr(10))   # anında yaz (cadquery'li betikler çıkışta çökebiliyor)
if sys.argv and sys.argv[0]: _h("open", (sys.argv[0],))
sys.addaudithook(_h)
"""


def calis(is_dizin, adimlar, uretec, gunluk, iz=False):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", YAMA_URETEC=os.path.abspath(uretec), PYTHONDONTWRITEBYTECODE="1", YAMA_IS_KOK=os.path.abspath(is_dizin))
    # not: AUTOKITCH_SAC_STANDART burada KURULMAZ (adım 00–31 onsuz koşmuştu; kurulursa çıktı değişir) — adım 33+ sac_ent.py kendi kurar
    # not: ADIM5 de burada kurulmaz — sac_ent.py import edilirken yama_v9/veri'ye kurar (E / U üreteçleri _bilesen_v8zq.pkl'yi oradan okur)
    if iz:                                                                   # kullanılan kaynak dosyaların izi (sitecustomize + audit hook)
        d = os.path.join(is_dizin, "_iz"); os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "sitecustomize.py"), "w", encoding="utf-8").write(IZ_KOD)
        env["PYTHONPATH"] = d + os.pathsep + env.get("PYTHONPATH", "")
        env["YAMA_IZ_KOK"] = os.path.abspath(is_dizin); env["YAMA_IZ_DOSYA"] = os.path.join(d, "acilan.txt")
    for no, ad, gir, cik, komutlar in adimlar:
        t0 = time.time(); print("ADIM %s · %s" % (no, ad), flush=True)
        if os.path.exists(os.path.join(is_dizin, cik)) and cik not in gir: os.remove(os.path.join(is_dizin, cik))   # eski çıktı başarısız adımı gizlemesin
        for cwd, k in komutlar:
            d = os.path.join(is_dizin, cwd)
            with open(gunluk, "a", encoding="utf-8") as L:
                L.write("\n===== ADIM %s · %s $ %s\n" % (no, cwd, k)); L.flush()
                r = subprocess.run(["bash", "-c", k.replace("{KOK}", os.path.abspath(is_dizin).replace("\\", "/")).replace("{YAMA}", HERE.replace("\\", "/"))],
                                   cwd=d, env=env, stdout=L, stderr=subprocess.STDOUT)
            if r.returncode != 0 and not os.path.exists(os.path.join(is_dizin, cik)):
                # not: cadquery'li bazı betikler dosyayı yazdıktan sonra 127/139 ile çıkabiliyor (birlesim/calistir.sh notu) → çıktı varlığı esas
                print("   komut çıkış kodu %d: %s" % (r.returncode, k), flush=True)
        if not os.path.exists(os.path.join(is_dizin, cik)):
            raise SystemExit("ADIM %s ÇIKTI YOK: %s (günlük: %s)" % (no, cik, gunluk))
        print("   → %s · %.0f sn" % (cik, time.time() - t0), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--is", dest="is_dizin", required=True)
    ap.add_argument("--taban"); ap.add_argument("--cikis")
    ap.add_argument("--uretec", required=True); ap.add_argument("--h3")
    ap.add_argument("--adim", help="yalnız bu adım(lar): 05 ya da 05-09")
    ap.add_argument("--girdi-dizin", help="tek adım doğrulama: adımın girdi GLB'leri bu klasörden bağlanır")
    ap.add_argument("--kurma", action="store_true", help="iş klasörü zaten kurulu")
    ap.add_argument("--iz", action="store_true", help="kullanılan kaynak dosyaları _iz/acilan.txt'ye yaz")
    a = ap.parse_args()
    h3 = a.h3 or os.path.join(a.uretec, "h3")
    os.makedirs(a.is_dizin, exist_ok=True)
    if not a.kurma: kur(a.is_dizin, h3, a.uretec)
    sec = ADIMLAR
    if a.adim:
        b, _, s = a.adim.partition("-"); s = s or b
        sec = [x for x in ADIMLAR if b <= x[0] <= s]
    if a.girdi_dizin:
        for x in sec[:1]:
            for g in x[2]: baglan(os.path.join(a.girdi_dizin, os.path.basename(g)), os.path.join(a.is_dizin, g))
    elif a.taban:
        baglan(a.taban, os.path.join(a.is_dizin, "hat3_v7.glb"))
    gunluk = os.path.join(a.is_dizin, "_zincir_gunluk.txt")
    t0 = time.time(); calis(a.is_dizin, sec, a.uretec, gunluk, a.iz)
    if a.cikis and sec[-1][3] == SON:
        shutil.copy2(os.path.join(a.is_dizin, SON), a.cikis); print("ÇIKIŞ", a.cikis)
    print("ZİNCİR BİTTİ · %d adım · %.0f sn" % (len(sec), time.time() - t0))


if __name__ == "__main__":
    main()
