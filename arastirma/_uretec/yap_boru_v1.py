# -*- coding: utf-8 -*-
"""Kasetlerin KARE agzini YUVARLAK BORUYA cevirir ve pideye kadar uzatir.
Kemal (22 Eyl): "o kasetlerden kare cikis yapmissin, bacami ne diyorsan onu yuvarlak yapsan, circle capinida
hesapla ona gore ve alta dogru uzat ... baska parca yok, direk kasetin kendi ucu pideye yaklasiyor."

  kasar_cad_v10 -> v11 · kiyma_cad_v5 -> v6 · kusbasi_cad_v4 -> v5 · sucuk_cad_v3 -> v4

CAP HESABI (granuler akista kopruleme kurali: boru capi >= 3 x en buyuk parca olcusu):
  kusbasi   kup 10 mm -> kosegen 17,3 -> 3x = 52    -> D 52
  kup sucuk kup  8 mm -> kosegen 13,9 -> 3x = 42    -> D 42
  kasar     rende 3 x 3 x 30; lif esnek, kesit 3 mm ama 30 mm uzun -> D 52 (kusbasiyla ayni, lif koprulemesin)
  kiyma     macun, parcacik <= 3 mm; kopruleme yok, capi DEBI belirler:
            doz 160 g / 10 s = 16 g/s, ro 1,0 -> 16 mL/s · D 32 -> 804 mm2 -> hiz 20 mm/s (ip gibi iner)  -> D 32

BOY: boru alt ucu kaset yerel y = -100 (kaset tabaninin 100 mm altinda). Modulde kaset tabani 260 ->
boru ucu 160; pide ust yuzu 120 -> DUSME 40 mm. Modulde ayri baca/huni parcasi KALKIYOR.

NOT — KASET ARTIK MASAYA OTURMUYOR: boru ayak duzleminin 100 mm altina iniyor. Kaset makine disinda
yatay konmali ya da ayakli sehpaya oturtulmali. Tasima tapasi borunun ucuna gecen yuvarlak kapak oldu.
"""
import io, os, re

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
BORU_ALT = -100.0

# (dosya, yeni surum, boru IC capi, agiz alt kotu degiskeni)
ISLER = [("kasar_cad_v10", "kasar_cad_v11", 52.0), ("kiyma_cad_v5", "kiyma_cad_v6", 32.0),
         ("kusbasi_cad_v4", "kusbasi_cad_v5", 42.0 + 10.0), ("sucuk_cad_v3", "sucuk_cad_v4", 42.0)]


def don(eski, yeni, D):
    s = io.open(os.path.join(U, eski + ".py"), encoding="utf-8").read()
    n = [0]

    def yama(a, b):
        nonlocal s
        assert a in s, eski + " — BULUNAMADI: " + a[:90]
        n[0] += 1
        s = s.replace(a, b, 1)

    s = s.replace(eski, yeni)
    ur = eski.split("_")[0]                                   # kasar / kiyma / kusbasi / sucuk
    ev, yv = eski.rsplit("_v", 1)[1], yeni.rsplit("_v", 1)[1]  # 10 -> 11 gibi
    for ek in ("", "_kabi", "_kaseti", "_dozaj", "_adimlar"):  # cikti adlari da yeni surume gecsin
        s = s.replace("%s%s_v%s" % (ur, ek, ev), "%s%s_v%s" % (ur, ek, yv))
    i = s.index('"""', s.index('"""') + 3)
    s = s[:i] + ("SURUM: kare agiz YUVARLAK BORU oldu (ic D %.0f, kopruleme kurali D >= 3 x en buyuk parca) ve\n"
                 "kaset tabaninin %.0f mm altina uzatildi — urun pidenin 40 mm ustunden dokuluyor, arada baska parca yok.\n"
                 "Kaset artik masaya oturmuyor (boru asagida): yatay konur ya da ayakli sehpaya oturur.\n" % (D, -BORU_ALT)) + s[i:]

    # --- boru sabitleri ---
    yama("TUP_Z1 = 246.5", "TUP_Z1 = 246.5\nBORU_D, BORU_ET, BORU_ALT = %.1f, 3.0, %.1f      # yuvarlak çıkış borusu: iç çap · et · alt uç (kaset tabanının altında)" % (D, BORU_ALT))

    # --- bilezik -> boru ---
    m = re.search(r"^(\s*)bilezik = kut\(-AG_X - 3, AG_X \+ 3, ([^,]+), CY, AG_Z0 - 3, AG_Z1 \+ 3\)(.*)$", s, re.M)
    assert m, eski + " — bilezik satiri yok"
    bosluk = m.group(1)
    s = s[:m.start()] + (
        bosluk + "BZ = (AG_Z0 + AG_Z1) / 2.0                                                                            # borunun z ekseni = ağzın ortası\n" +
        bosluk + "boru = sily(0, BZ, BORU_D / 2 + BORU_ET, BORU_ALT, CY)                                                # YUVARLAK ÇIKIŞ BORUSU (tüple tek parça)") + s[m.end():]

    m2 = re.search(r"^(\s*)tup = tup\.union\(flans\)\.union\(bilezik\)\.cut\(silz\(0, CY, RT, ZF - 4, TUP_Z1 \+ 1\)\)\.cut\(kut\(-AG_X, AG_X, [^,]+, CY, AG_Z0, AG_Z1\)\)$", s, re.M)
    assert m2, eski + " — tup birlestirme satiri yok"
    b2 = m2.group(1)
    s = s[:m2.start()] + (
        b2 + "tup = tup.union(flans).union(boru).cut(silz(0, CY, RT, ZF - 4, TUP_Z1 + 1)).cut(sily(0, BZ, BORU_D / 2, BORU_ALT - 1.0, CY))") + s[m2.end():]

    # --- tasima tapasi: boru ucuna gecen yuvarlak kapak ---
    m3 = re.search(r'^(\s*)ekle\("tasima_tapasi",.*?\n.*?\n.*?bom=\("Taşıma tapası".*?\)\)$', s, re.M | re.S)
    assert m3, eski + " — tasima tapasi blogu yok"
    b3 = m3.group(1)
    s = s[:m3.start()] + (
        b3 + 'ekle("tasima_tapasi", sily(0, BZ, BORU_D / 2 + BORU_ET + 2.0, BORU_ALT - 8.0, BORU_ALT + 14.0)\n' +
        b3 + '     .cut(sily(0, BZ, BORU_D / 2 + BORU_ET + 0.2, BORU_ALT - 6.0, BORU_ALT + 16.0)), "silikon",\n' +
        b3 + '     bom=("Taşıma tapası", 1, "TPU 95A baskı", "kap makine dışındayken çıkış borusunun ucuna geçer · makineye sürmeden çıkarılır"))') + s[m3.end():]

    s = s.replace('"tapa ↔ bilezik (0,2)"', '"tapa ↔ boru ucu (0,2)"')
    s = s.replace("alt ağız 48 × 44", "yuvarlak çıkış borusu iç Ø%.0f, kaset tabanının %.0f mm altına iner" % (D, -BORU_ALT))
    s = s.replace("alt ağız 30 × 30", "yuvarlak çıkış borusu iç Ø%.0f, kaset tabanının %.0f mm altına iner" % (D, -BORU_ALT))
    io.open(os.path.join(U, yeni + ".py"), "w", encoding="utf-8").write(s)
    print("%s -> %s  ·  boru ic D %.0f  ·  %d yama" % (eski, yeni, D, n[0]))


for e, y, d in ISLER:
    don(e, y, d)
