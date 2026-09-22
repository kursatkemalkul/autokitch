# -*- coding: utf-8 -*-
"""Cikis borusunun TUPLE BIRLESIMINI duzeltir (boru v1 -> v2).
Kemal (22 Eyl): "assagi inen boru capinin disi yataydaki boru capiyla ayni degil, birlesimleri duzgun olmadi,
birlesim duzgun olsun."

OLCULEN SORUN:
  kasar  : yatay tup disi O50 (RT 22 + et 3), dikey boru disi O58 -> BORU TUPTEN KALIN, tupu yutuyordu.
           Ustelik urun zaten tupun IC capindan (O44) geciyor; borunun O52 olmasinin bir anlami yoktu.
           -> kasar borusu O44 (tupun ic capiyla AYNI, daralma yok, dis O50 = tup disi: tam hizali).
  digerleri: tup disi O78, boru disi O38-O58 -> boru ince ama birlesim KESKIN basamakti.
           -> her boruda 22 mm KONIK GECIS: boru tupun disinda tup capiyla basliyor, konik daralip
              kendi capina iniyor, sonra duz devam ediyor. Ici de ayni sekilde konik.

  kasar_cad_v11 -> v12 · kiyma_cad_v6 -> v7 · kusbasi_cad_v5 -> v6 · sucuk_cad_v4 -> v5
"""
import io, os, re

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")

# (eski, yeni, yeni boru IC capi)
ISLER = [("kasar_cad_v11", "kasar_cad_v12", 44.0),      # = tupun ic capi (2 x RT 22): daralma yok
         ("kiyma_cad_v6", "kiyma_cad_v7", 32.0),
         ("kusbasi_cad_v5", "kusbasi_cad_v6", 52.0),
         ("sucuk_cad_v4", "sucuk_cad_v5", 42.0)]


def don(eski, yeni, D):
    s = io.open(os.path.join(U, eski + ".py"), encoding="utf-8").read()
    s = s.replace(eski, yeni)
    ur = eski.split("_")[0]
    ev, yv = eski.rsplit("_v", 1)[1], yeni.rsplit("_v", 1)[1]
    for ek in ("", "_kabi", "_kaseti", "_dozaj", "_adimlar", "_montaj"):
        s = s.replace("%s%s_v%s" % (ur, ek, ev), "%s%s_v%s" % (ur, ek, yv))
    i = s.index('"""', s.index('"""') + 3)
    s = s[:i] + ("BIRLESIM: boru artik tupun disinda TUP CAPIYLA basliyor, 22 mm konik daralip kendi capina\n"
                 "iniyor (ic D %.0f) ve duz devam ediyor — basamak yok. Onceki surumde boru tupe basamakla oturuyordu.\n" % D) + s[i:]

    # 1 · boru capi
    s = re.sub(r"^BORU_D, BORU_ET, BORU_ALT = [\d.]+, ([\d.]+), (-?[\d.]+)",
               "BORU_D, BORU_ET, BORU_ALT, BORU_GECIS = %.1f, \\1, \\2, 22.0" % D, s, count=1, flags=re.M)
    s = s.replace("# yuvarlak çıkış borusu: iç çap · et · alt uç (kaset tabanının altında)",
                  "# yuvarlak çıkış borusu: iç çap · et · alt uç · tüpten boruya konik geçiş boyu", 1)

    # 2 · koni yardimcisi
    assert "def sily(" in s
    s = s.replace("def kut(x0, x1, y0, y1, z0, z1):",
                  'def koni_y(z, r_alt, r_ust, y0, y1):\n'
                  '    """y ekseninde konik: y0 (alt, r_alt) → y1 (üst, r_ust). Tüpten boruya geçişi basamaksız yapar."""\n'
                  '    if abs(r_alt - r_ust) < 0.01: return sily(0, z, r_alt, y0, y1)   # esit yaricap: makeCone hata verir
'
                  '    return cq.Workplane(obj=cq.Solid.makeCone(r_alt, r_ust, y1 - y0, cq.Vector(0, y0, z), cq.Vector(0, 1, 0)))\n\n\n'
                  'def kut(x0, x1, y0, y1, z0, z1):', 1)

    # 3 · boru govdesi: koni + duz
    a = "    boru = sily(0, BZ, BORU_D / 2 + BORU_ET, BORU_ALT, CY)                                                # YUVARLAK ÇIKIŞ BORUSU (tüple tek parça)"
    assert a in s, eski + " — boru satiri yok"
    s = s.replace(a,
                  "    RB_ = BORU_D / 2 + BORU_ET                                                                            # boru dış yarıçapı\n"
                  "    YG_ = CY - BORU_GECIS                                                                                 # konik geçişin alt kotu\n"
                  "    boru = koni_y(BZ, RB_, RT + 3.0, YG_, CY).union(sily(0, BZ, RB_, BORU_ALT, YG_))                      # tüp çapında başlar, konik daralır, düz iner", 1)

    b = "    tup = tup.union(flans).union(boru).cut(silz(0, CY, RT, ZF - 4, TUP_Z1 + 1)).cut(sily(0, BZ, BORU_D / 2, BORU_ALT - 1.0, CY))"
    assert b in s, eski + " — tup birlestirme satiri yok"
    s = s.replace(b,
                  "    bic_ = koni_y(BZ, BORU_D / 2, RT, YG_, CY + 1.0).union(sily(0, BZ, BORU_D / 2, BORU_ALT - 1.0, YG_))   # iç boşluk da konik\n"
                  "    tup = tup.union(flans).union(boru).cut(silz(0, CY, RT, ZF - 4, TUP_Z1 + 1)).cut(bic_)", 1)

    s = re.sub(r"yuvarlak çıkış borusu iç Ø\d+", "yuvarlak çıkış borusu iç Ø%.0f (tüpten 22 mm konik geçişle)" % D, s)
    io.open(os.path.join(U, yeni + ".py"), "w", encoding="utf-8").write(s)
    print("%s -> %s  ·  boru ic D %.0f · dis D %.0f" % (eski, yeni, D, D + 6))


for e, y, d in ISLER:
    don(e, y, d)
