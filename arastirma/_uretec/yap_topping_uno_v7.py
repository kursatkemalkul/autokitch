# -*- coding: utf-8 -*-
"""topping_uno_cad_v6 → topping_uno_cad_v7 (26 Eyl 2026 gece, Kemal: "yay pim hepsi katalog olsun · her şeyi mühendislik gözüyle kontrol et"):
 1 · KATALOG YAY: Century Spring 66644SCS (316 paslanmaz · tel 0,41 · dış Ø4,78 · serbest 21,34 · 0,33 N/mm · en çok 9,12 mm sıkışma · kapalı uç)
     hem haç kovanının 4 yayı hem mandal yayı. Kovan buna göre: haç 7,0 mm girer (9,5 → 7,0), kovan 15,5 boy, yay cebi Ø6 × 9,7,
     ön yük 1,24 mm (4 yay 1,6 N), tam geri çekilmede (8,0) 9,2 mm → sınırın içinde; pim kanalı 11,5 → sert durak 8,5 (tabladan 1,9 önce).
     Mandal: dil plakayı 4,5 örter, 5,0 kayar, yay cebi Ø5,2 × 10,3, ön yük 4,0 mm (1,3 N), açıkta 9,0 mm.
 2 · KATALOG PİM: ISO 8734 (3 m6 × 45 kovan · 3 m6 × 18 mandal), segman DIN 471 22 × 1,2 (kanal d2 21,0 · m 1,3 — föy), kasetin pimi ISO 8752 4 × 26 (zaten).
 3 · KABİN YAN DUVARLARI 1277'den başlar: tabla/disk mekanizma bölgesi (1060–1277) tüm genişlikte serbest (disk aktarmada 2507'ye çıkar);
     alt tarafı topping_cad'in sac yan duvarları kapatır.
 4 · Denetimler: strok/yay sıkışma hesabı kataloğa göre, kanal ölçüsü, pim boyları."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_uno_cad_v6.py"), encoding="utf-8").read()


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


d("TOPPING v2 (UNO'lu) · 3B MODEL · topping_uno_cad_v6 · 26 Eyl 2026 gece",
  "TOPPING v2 (UNO'lu) · 3B MODEL · topping_uno_cad_v7 · 26 Eyl 2026 gece (katalog yay/pim · haç 7,0 · mandal 4,5 · kabin duvarı 1277'den)\nv7: yay Century Spring 66644SCS (4 kovan + mandal), pim ISO 8734 3 × 45 / 3 × 18, segman DIN 471 22 × 1,2 kanalı d2 21,0 · m 1,3; haç kovanı 15,5 (haç 7,0 girer, strok 8,0 / sert durak 8,5); mandal dili plakayı 4,5 örter, 5,0 kayar; kabin yan PU duvarları 1277–2030. Önceki: topping_uno_cad_v6.py\nv6:")
# ---- kabin yan duvarları 1277'den ----
d('''ekle("kabin_sol_duvar_PU", kut(0, 90, Y0, YUST, 0, -D), "pu", "V", not_="sac + PU 60")
ekle("kabin_sag_duvar_PU", kut(W - 90, W, Y0, YUST, 0, -D), "pu", "V")''',
  '''ekle("kabin_sol_duvar_PU", kut(0, 90, 1277.0, YUST, 0, -D), "pu", "V", not_="sac + PU 60 · v7: 1277'den başlar (altı mekanizma bölgesi: tabla park/aktarmada duvar hizasını geçer; alt yanlar topping_cad'in sacı)")
ekle("kabin_sag_duvar_PU", kut(W - 90, W, 1277.0, YUST, 0, -D), "pu", "V", not_="v7: 1277'den başlar (disk aktarmada 2507'ye kadar çıkar)")''')
# ---- mil: kanal 11,5 (sert durak 8,5) + DIN 471 kanalı d2 21,0 m 1,3 ----
d('''        _mil = silz(xc, yy, 11, -670, -545).cut(kut(xc - 1.6, xc + 1.6, yy - 12.0, yy + 12.0, -560.5, -546.5))   # v6: −545'e kadar · haç yuvası pim kanalı 3,2 × 14 BOYDAN BOYA (−560,5…−546,5; uçta 1,5 köprü)
        _mil = _mil.cut(silz(xc, yy, 11.5, -564.7, -563.5).cut(silz(xc, yy, 10.3, -565.0, -563.0)))                # segman kanalı (DIN 471 22 × 1,2): yay tablasının dayandığı yer''',
  '''        _mil = silz(xc, yy, 11, -670, -545).cut(kut(xc - 1.6, xc + 1.6, yy - 12.0, yy + 12.0, -558.0, -546.5))   # v7: pim kanalı 3,2 × 11,5 boydan boya (−558…−546,5): sert durak 8,5 (yay sınırı 9,1 · tabla 10,4)
        _mil = _mil.cut(silz(xc, yy, 11.5, -564.7, -563.4).cut(silz(xc, yy, 10.5, -565.0, -563.0)))                # segman kanalı DIN 471 (d1 22: d2 21,0 · m 1,3 · s 1,2) [föy]''')
d('''             not_="Ø22 · kovanda keçeli · ucunda boydan boya pim kanalı 3,2 × 14 (haç yuvası 10,5 kayar) + segman kanalı (v6)")''',
  '''             not_="Ø22 · kovanda keçeli · ucunda boydan boya pim kanalı 3,2 × 11,5 (haç yuvası 8,5 kayar) + segman kanalı d2 21 × 1,3 (v7)")''')
# ---- mandal: dil 10 × 8, plakayı 4,5 örter, 5,0 kayar, yay 66644SCS ----
d('''        if yon == "sol": dud = dud.cut(kut(xa - 6.0, xa + 1.0, ST + 1.0, ST + 11.0, mz - 1.0, mz + 7.0))        # mandal dili penceresi 10 × 8''',
  '''        if yon == "sol": dud = dud.cut(kut(xa - 6.0, xa + 1.0, ST + 1.0, ST + 13.0, mz - 1.0, mz + 9.0))        # mandal dili penceresi 12 × 10 (v7)''')
d('''    gov = kut(px0 - 24.0, px0 - 5.0, ST, ST + 34.0, mz - 8.0, mz + 24.0)
    gov = gov.cut(kut(px0 - 21.5, px0 - 7.5, ST + 1.5, ST + 35.0, mz - 9.0, mz + 8.0))                  # dil + kol kanalı (üstü açık, duvarlar 2,5)
    gov = gov.cut(kut(px0 - 8.0, px0 - 4.0, ST + 1.5, ST + 11.0, mz - 1.0, mz + 7.0))                    # iç duvarda dil penceresi''',
  '''    gov = kut(px0 - 24.0, px0 - 5.0, ST, ST + 34.0, mz - 8.0, mz + 26.0)
    gov = gov.cut(kut(px0 - 21.5, px0 - 7.5, ST + 1.5, ST + 35.0, mz - 9.0, mz + 10.0))                 # dil + kol kanalı (üstü açık, duvarlar 2,5) · v7 dil 8 kalın
    gov = gov.cut(kut(px0 - 8.0, px0 - 4.0, ST + 1.5, ST + 13.0, mz - 1.0, mz + 9.0))                    # iç duvarda dil penceresi 12 × 10''')
d('''    ekle("yuva_%s_mandal_govdesi" % k, gov, "pom", "H", not_="mandal yuvası POM 19 × 34 × 32 · U kanal (duvar 2,5) · kılavuza 2 × M4 · pim iki yan duvarda")
    dil = kut(px0 - 14.0, px0 + 6.0, ST + 2.0, ST + 10.0, mz, mz + 6.0).cut(prizma_xz([(px0 + 6.0, mz + 6.0), (px0 + 6.0, mz + 0.5), (px0 + 0.5, mz + 6.0)], ST + 1.0, ST + 11.0))
    dil = dil.union(kut(px0 - 14.0, px0 - 10.0, ST + 2.0, ST + 44.0, mz, mz + 6.0))                     # dik kol: pim üstünde kayar, üstü baş parmak (gövdenin 10 üstünde)
    dil = dil.cut(silx(ST + 6.0, mz + 3.0, 1.75, px0 - 14.5, px0 - 2.0)).cut(silx(ST + 18.0, mz + 3.0, 1.6, px0 - 15.0, px0 - 9.0))   # yay deliği Ø3,5 × 12 · pim deliği
    ekle("yuva_%s_mandal_dili" % k, dil, "pom", "H",
         not_="kayar dil POM 20 × 8 × 6 + kol 4 × 42 · plakayı 6 mm örter · ucu 45° rampa (takarken plaka dili sola iter) · yay geri iter · kol 6,5 mm sola basılınca kaset serbest")
    ekle("yuva_%s_mandal_yayi" % k, silx(ST + 6.0, mz + 3.0, 1.5, px0 - 21.5, px0 - 2.0).cut(silx(ST + 6.0, mz + 3.0, 1.1, px0 - 22.0, px0 - 1.5)), "celik", "V",
         not_="baskı yayı Ø3 × 19,5 (tel 0,4) · dilin deliğinde, gövdenin dış duvarına dayanır · ≈2 N")
    ekle("yuva_%s_mandal_pimi" % k, silx(ST + 18.0, mz + 3.0, 1.5, px0 - 24.0, px0 - 5.0), "celik", "V", not_="Ø3 × 19 kılavuz pimi: iki yan duvara sıkı geçme, dil üstünde kayar")''',
  '''    ekle("yuva_%s_mandal_govdesi" % k, gov, "pom", "H", not_="mandal yuvası POM 19 × 34 × 34 · U kanal (duvar 2,5) · kılavuza 2 × M4 · pim iki yan duvarda")
    dil = kut(px0 - 14.0, px0 + 4.5, ST + 2.0, ST + 12.0, mz, mz + 8.0).cut(prizma_xz([(px0 + 4.5, mz + 8.0), (px0 + 4.5, mz + 0.5), (px0 - 3.0, mz + 8.0)], ST + 1.0, ST + 13.0))
    dil = dil.union(kut(px0 - 14.0, px0 - 10.0, ST + 2.0, ST + 44.0, mz, mz + 8.0))                     # dik kol: pim üstünde kayar, üstü baş parmak (gövdenin 10 üstünde)
    dil = dil.cut(silx(ST + 7.0, mz + 4.0, 2.6, px0 - 14.5, px0 - 4.2)).cut(silx(ST + 18.0, mz + 4.0, 1.6, px0 - 15.0, px0 - 9.0))   # yay deliği Ø5,2 × 10,3 · pim deliği
    ekle("yuva_%s_mandal_dili" % k, dil, "pom", "H",
         not_="kayar dil POM 18,5 × 10 × 8 + kol 4 × 42 · plakayı 4,5 mm örter · ucu 45° rampa (takarken plaka dili sola iter) · yay geri iter · kol 5 mm sola basılınca kaset serbest (v7)")
    ekle("yuva_%s_mandal_yayi" % k, silx(ST + 7.0, mz + 4.0, 2.39, px0 - 21.5, px0 - 4.2).cut(silx(ST + 7.0, mz + 4.0, 1.98, px0 - 22.0, px0 - 3.7)), "celik", "K",
         not_="Century Spring 66644SCS · 316 · tel 0,41 · Ø4,78 · serbest 21,34 · 0,33 N/mm · en çok 9,12 sıkışma [katalog] · takılı 17,3 (ön yük 4,0 = 1,3 N) · açıkta 12,3 (9,0 sıkışma)")
    ekle("yuva_%s_mandal_pimi" % k, silx(ST + 18.0, mz + 4.0, 1.5, px0 - 23.5, px0 - 5.5), "celik", "K", not_="Pim ISO 8734 3 m6 × 18 A1: iki yan duvara sıkı geçme, dil üstünde kayar (0,5 içeride)")''')
d('''    gov = gov.cut(silx(ST + 18.0, mz + 3.0, 1.6, px0 - 25.0, px0 - 4.0))                                 # pim deliği''',
  '''    gov = gov.cut(silx(ST + 18.0, mz + 4.0, 1.6, px0 - 25.0, px0 - 4.0))                                 # pim deliği (v7: dil 8 kalın, pim mz+4)''')
# ---- haç kovanı: 15,5 boy, haç 7,0 girer, yay cebi Ø6 × 9,7, 66644SCS ----
d('''        z_agiz = hb.zmax - 18.0 + 10.0 - 0.5                                                            # haç çubuklarının ön yüzü −533,5 → yuva ağzı −534''',
  '''        z_agiz = hb.zmax - 18.0 + 10.0 - 3.0                                                            # v7: yuva ağzı −536,5 → haç çubukları (−543,5…−533,5) 7,0 mm girer''')
d('''        kv = silz(xc, yy, 24.0, z_agiz - 18.0, z_agiz)                                                  # POM Ø48 × 18 (−552…−534)
        kv = kv.cut(silz(xc, yy, 13.5, z_agiz - 10.5, z_agiz + 1.0))                                    # disk boşluğu Ø27 × 10,5 (kavrama Ø26 · dipte 1 mm)
        kv = kv.cut(kut(xc - 18.25, xc + 18.25, yy - 4.25, yy + 4.25, z_agiz - 10.5, z_agiz + 1.0))    # haç yarığı 36,5 × 8,5 × 10,5
        kv = kv.cut(kut(xc - 4.25, xc + 4.25, yy - 18.25, yy + 18.25, z_agiz - 10.5, z_agiz + 1.0))
        kv = kv.cut(silz(xc, yy, 11.1, z_agiz - 18.5, z_agiz - 10.0))                                   # mil deliği Ø22,2 (mil ucu −545, dipten 0,5 geride)
        kv = kv.cut(kut(xc - 1.6, xc + 1.6, yy - 25.0, yy + 25.0, z_agiz - 15.6, z_agiz - 12.4))       # pim deliği Ø3,2 boydan boya (pim −549,5…−546,5)
        for cxi, cyi in YAYC: kv = kv.cut(silz(cxi, cyi, 3.0, z_agiz - 18.5, z_agiz - 3.5))            # 4 yay cebi Ø6 × 14,5 (yarıkların arasında, r 18)''',
  '''        kv = silz(xc, yy, 24.0, z_agiz - 15.5, z_agiz)                                                  # POM Ø48 × 15,5 (−552…−536,5)
        kv = kv.cut(silz(xc, yy, 13.5, z_agiz - 8.0, z_agiz + 1.0))                                     # disk boşluğu Ø27 × 8 (kavrama Ø26 · dipte 1 mm)
        kv = kv.cut(kut(xc - 18.25, xc + 18.25, yy - 4.25, yy + 4.25, z_agiz - 8.0, z_agiz + 1.0))     # haç yarığı 36,5 × 8,5 × 8
        kv = kv.cut(kut(xc - 4.25, xc + 4.25, yy - 18.25, yy + 18.25, z_agiz - 8.0, z_agiz + 1.0))
        kv = kv.cut(silz(xc, yy, 11.1, z_agiz - 16.0, z_agiz - 7.5))                                    # mil deliği Ø22,2 (mil ucu −545, dipten 0,5 geride)
        kv = kv.cut(kut(xc - 1.6, xc + 1.6, yy - 25.0, yy + 25.0, z_agiz - 13.1, z_agiz - 9.9))        # pim deliği Ø3,2 boydan boya (pim −549,5…−546,5)
        for cxi, cyi in YAYC: kv = kv.cut(silz(cxi, cyi, 3.0, z_agiz - 16.0, z_agiz - 15.5 + 9.7))     # 4 yay cebi Ø6 × 9,7 (yarıkların arasında, r 18): dip −542,3''')
d('''             not_="POM Ø48 × 18 · önünde 36,5 × 8,5 haç yarığı 10,5 derin (kaset haçı 9,5 girer) · milde pimle kayar (strok 10,5; kaset en çok 9,5 iter) · 4 yay öne iter · PLC yavaş çevirir, haç oturur (KLİK)")''',
  '''             not_="POM Ø48 × 15,5 · önünde 36,5 × 8,5 haç yarığı 8 derin (kaset haçı 7,0 girer, dipte 1) · milde pimle kayar (sert durak 8,5; kaset en çok 7,0 + 0,5 iter) · 4 katalog yay öne iter · PLC yavaş çevirir, haç oturur (KLİK) · tork: 4 çubuk yüzü 7 × 4,75, 3 Nm'de 1,8 MPa (POM 20)")''')
d('''            ekle("yuva_%s_yay_%d" % (tag, i), silz(cxi, cyi, 2.5, z_agiz - 28.5, z_agiz - 4.0).cut(silz(cxi, cyi, 2.0, z_agiz - 29.0, z_agiz - 3.5)), "celik", "V", grup=gr,
                 not_="baskı yayı Ø5 × 24,5 (tel 0,4 · serbest 28) — gösterim: kovan · kovan 9,5 geri çekilince 15'e sıkışır · 4'ü birden ≈3–12 N")''',
  '''            ekle("yuva_%s_yay_%d" % (tag, i), silz(cxi, cyi, 2.39, z_agiz - 26.0 + 0.1, z_agiz - 15.5 + 9.7).cut(silz(cxi, cyi, 1.98, z_agiz - 26.5, z_agiz - 15.5 + 9.7 + 0.5)), "celik", "K", grup=gr,
                 not_="Century Spring 66644SCS · 316 · tel 0,41 · Ø4,78 · serbest 21,34 · 0,33 N/mm · en çok 9,12 mm sıkışma [katalog] · takılı 20,1 (ön yük 1,24 = 0,41 N; 4 yay 1,6 N) · 8,0 geri çekilmede 12,1 (9,2 sıkışma) — gösterim: kovan")''')
d('''        tb = silz(xc, yy, 24.0, z_agiz - 29.5, z_agiz - 28.5).cut(silz(xc, yy, 11.5, z_agiz - 30.0, z_agiz - 28.0))
        for cxi, cyi in YAYC: tb = tb.union(silz(cxi, cyi, 1.8, z_agiz - 28.5, z_agiz - 24.5))
        ekle("yuva_%s_yay_tablasi" % tag, tb, "paslanmaz", "H", grup=gr, not_="yay tablası 304 · Ø48 × 1 · milin segmanına oturur, milyle döner · 4 yay pilotu Ø3,6 × 4 · kovan 10,5'te buna dayanır")
        ekle("yuva_%s_segmani" % tag, silz(xc, yy, 12.3, z_agiz - 30.7, z_agiz - 29.5).cut(silz(xc, yy, 10.3, z_agiz - 31.0, z_agiz - 29.0)), "celik", "V", grup=gr,
             not_="segman DIN 471 22 × 1,2 · mil kanalında · kovan yüzüne 0,3")
        ekle("yuva_%s_kavrama_pimi" % tag, kut(xc - 1.5, xc + 1.5, yy - 24.0, yy + 24.0, z_agiz - 15.5, z_agiz - 12.5), "celik", "V", grup=gr,
             not_="Ø3 × 48 sertleştirilmiş pim (ISO 8734): kovanı mile bağlar (tork), mildeki 3,2 × 14 kanalda kayar (strok 10,5)")''',
  '''        tb = silz(xc, yy, 24.0, z_agiz - 26.9, z_agiz - 25.9).cut(silz(xc, yy, 11.5, z_agiz - 27.4, z_agiz - 25.4))              # −563,4…−562,4
        for cxi, cyi in YAYC: tb = tb.union(silz(cxi, cyi, 1.8, z_agiz - 25.9, z_agiz - 21.9))
        ekle("yuva_%s_yay_tablasi" % tag, tb, "paslanmaz", "H", grup=gr, not_="yay tablası 304 · Ø48 × 1 · milin segmanına oturur, milyle döner · 4 yay pilotu Ø3,6 × 4 (yay iç Ø3,96) · kovan sert durakta (8,5) buna 1,9 kala durur")
        ekle("yuva_%s_segmani" % tag, silz(xc, yy, 12.3, z_agiz - 28.1, z_agiz - 26.9).cut(silz(xc, yy, 10.5, z_agiz - 28.5, z_agiz - 26.5)), "celik", "K", grup=gr,
             not_="Segman DIN 471 A22 × 1,2 (kanal d2 21,0 · m 1,3) · kovan yüzüne 0,3")
        ekle("yuva_%s_kavrama_pimi" % tag, kut(xc - 1.5, xc + 1.5, yy - 22.5, yy + 22.5, z_agiz - 13.0, z_agiz - 10.0), "celik", "K", grup=gr,
             not_="Pim ISO 8734 3 m6 × 45 A1 (kovanda 1,5 içeride): kovanı mile bağlar (tork), mildeki 3,2 × 11,5 kanalda kayar (sert durak 8,5)")''')
# ---- denetimler ----
d('''    kontrol("%s haç yuvası ağzı haç çubuklarının önünde 0,5 mm, çubuklar yuvada %.1f mm" % (KOD, hy.zmax - hk.zmin), hy.zmax > hk.zmin and abs((hy.zmax - hk.zmin) - 9.5) < 0.6)
    kontrol("%s haç yuvası geri çekilebilir: yay tablasına %.1f mm ≥ 10,5 (kaset en çok 9,5 iter)" % (KOD, hy.zmin - (ty.zmin + 1.0)), hy.zmin - (ty.zmin + 1.0) >= 10.49)   # tabla plakası 1 mm; pilotlar sayılmaz''',
  '''    kontrol("%s haç çubukları yuvada %.1f mm (7,0 · v7 katalog yayına göre)" % (KOD, hy.zmax - hk.zmin), hy.zmax > hk.zmin and abs((hy.zmax - hk.zmin) - 7.0) < 0.6)
    kontrol("%s haç yuvası geri çekilebilir: yay tablasına %.1f mm ≥ 8,5 sert durak + 1,9" % (KOD, hy.zmin - (ty.zmin + 1.0)), hy.zmin - (ty.zmin + 1.0) >= 10.39)   # tabla plakası 1 mm; pilotlar sayılmaz
    _ys = bb("yuva_%s_helezon_yay_0" % k); _tak = _ys.zmax - _ys.zmin
    kontrol("%s yay takılı boy %.1f: ön yük %.2f ≥ 1,0 · 8,0 geri çekilmede sıkışma %.2f ≤ 9,12 (66644SCS)" % (KOD, _tak, 21.34 - _tak, 21.34 - _tak + 8.0), 21.34 - _tak >= 1.0 and 21.34 - _tak + 8.0 <= 9.12 + 0.3)
    _my = bb("yuva_%s_mandal_yayi" % k); _mt = _my.xmax - _my.xmin
    kontrol("%s mandal yayı takılı %.1f: ön yük %.1f (%.1f N) · 5 mm açılınca sıkışma %.1f ≤ 9,12" % (KOD, _mt, 21.34 - _mt, 0.33 * (21.34 - _mt), 21.34 - _mt + 5.0), 21.34 - _mt >= 3.0 and 21.34 - _mt + 5.0 <= 9.12 + 0.3)
    _mil = bb("mil_%s_helezon" % mod); _seg = bb("yuva_%s_helezon_segmani" % k)
    kontrol("%s segman kanalı DIN 471: genişlik %.1f = 1,3 · segman kanalda · kovan yüzüne %.1f" % (KOD, 1.3, _seg.zmin + 565.0), abs((_seg.zmin + 565.0) - 0.4) < 0.15)''')
d('''    kontrol("%s mandal dili plakanın ÖNÜNDE (z %.1f ≥ plaka önü %.0f), plakayı %.1f mm örtüyor ≥ 5,5" % (KOD, dl.zmin, Y_["pz1"], dl.xmax - Y_["px0"]), dl.zmin >= Y_["pz1"] and dl.xmax - Y_["px0"] >= 5.5)
    kontrol("%s mandal kolu sola %.1f mm kayabilir ≥ 6,5 (dil plakadan çıkar)" % (KOD, dl.xmin - (gv.xmin + 2.5)), dl.xmin - (gv.xmin + 2.5) >= 6.5)''',
  '''    kontrol("%s mandal dili plakanın ÖNÜNDE (z %.1f ≥ plaka önü %.0f), plakayı %.1f mm örtüyor ≥ 4,0" % (KOD, dl.zmin, Y_["pz1"], dl.xmax - Y_["px0"]), dl.zmin >= Y_["pz1"] and dl.xmax - Y_["px0"] >= 4.0)
    kontrol("%s mandal kolu sola %.1f mm kayabilir ≥ 5,0 (dil plakadan çıkar)" % (KOD, dl.xmin - (gv.xmin + 2.5)), dl.xmin - (gv.xmin + 2.5) >= 5.0)''')
d('''kontrol("kuşbaşı valf topuzu–kaşar mandalı boşluğu %.0f ≥ 20" % (bb("yuva_kasar_mandal_govdesi").xmin - bb("kusbasi__valf_topuzu").xmax), bb("yuva_kasar_mandal_govdesi").xmin - bb("kusbasi__valf_topuzu").xmax >= 20.0)''',
  '''kontrol("kuşbaşı valf topuzu–kaşar mandalı boşluğu %.0f ≥ 20" % (bb("yuva_kasar_mandal_govdesi").xmin - bb("kusbasi__valf_topuzu").xmax), bb("yuva_kasar_mandal_govdesi").xmin - bb("kusbasi__valf_topuzu").xmax >= 20.0)
_sd = [p for p in P if p["ad"] in ("kabin_sol_duvar_PU", "kabin_sag_duvar_PU")]
kontrol("kabin yan PU duvarları 1277'den başlıyor (mekanizma bölgesi serbest)", all(p["sh"].BoundingBox().ymin >= 1276.99 for p in _sd))''')
# ---- çıkış dosyaları ----
for a, b in (("topping_uno_v6.glb", "topping_uno_v7.glb"), ("topping_uno_v6.json", "topping_uno_v7.json"), ('surum="topping_uno_cad_v6', 'surum="topping_uno_cad_v7'),
             ('"generator": "AUTOKITCH topping_uno_cad_v6"', '"generator": "AUTOKITCH topping_uno_cad_v7"')):
    assert s.count(a) >= 1, a
    s = s.replace(a, b)
io.open(os.path.join(U, "topping_uno_cad_v7.py"), "w", encoding="utf-8").write(s)
print("topping_uno_cad_v7.py yazildi")
