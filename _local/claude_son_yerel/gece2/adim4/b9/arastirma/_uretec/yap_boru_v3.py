# -*- coding: utf-8 -*-
"""Kaset cikis borusunu YALITIMIN UST YUZUNDE keser (boru v2 -> v3).
Kemal (22 Eyl): "yuvarlak parcalar neden yalitim parcasindan da assagiya gidip sacma sapan uzun kaliyor?
Kirmizi yere kadar yap. Hatta soyle yap: kasetlerin o yuvarlak parca uzunlugu SADECE YALITIMIN UST KISMINA
kadar gelsin, orda kes; yalitimin icine de AYNI CAPTA yuvarlak bosluk ac, kaset takilinca ucu oraya denk gelsin,
malzeme assaga aksin. Bu sayede etrafi kapanir, yalitimda sadece BIR DELIK olur."

OLCU: yalitim (pu_taban) y 190-250 · ic kabuk tabani y 250-251 · kaset tabani y 260.
  -> boru alt ucu y 250 = kaset yerelinde BORU_ALT = 250 - 260 = -10  (onceki: -100, yani 90 mm fazla sarkiyordu)

NE KAZANILIYOR:
  · Boru yalitimin ALTINA inmiyor; tabandaki uzun YARIK yerine her yuvada tek YUVARLAK DELIK kaliyor
    -> soguk kacagi cok azaliyor, etrafi kapaniyor.
  · Kaset one cekilirken boru yalitimin USTUNDE kaliyor, hicbir seye takilmiyor (eski uzun boru
    yarigin icinden gecmek zorundaydi).
  · Urunu yalitim deliginin icindeki PASLANMAZ KOVAN asagi indiriyor (modulun parcasi, topping_cad_v9).

  kasar_cad_v12 -> v13 · kiyma_cad_v7 -> v8 · kusbasi_cad_v6 -> v7 · sucuk_cad_v5 -> v6 · harc_cad_v2 -> v3
"""
import io, os, re

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
YENI_ALT = -10.0

ISLER = [("kasar_cad_v12", "kasar_cad_v13"), ("kiyma_cad_v7", "kiyma_cad_v8"),
         ("kusbasi_cad_v6", "kusbasi_cad_v7"), ("sucuk_cad_v5", "sucuk_cad_v6"),
         ("harc_cad_v2", "harc_cad_v3")]


def don(eski, yeni):
    s = io.open(os.path.join(U, eski + ".py"), encoding="utf-8").read()
    s = s.replace(eski, yeni)
    ur = eski.split("_")[0]
    ev, yv = eski.rsplit("_v", 1)[1], yeni.rsplit("_v", 1)[1]
    for ek in ("", "_kabi", "_kaseti", "_dozaj", "_adimlar", "_montaj"):
        s = s.replace("%s%s_v%s" % (ur, ek, ev), "%s%s_v%s" % (ur, ek, yv))
    i = s.index('"""', s.index('"""') + 3)
    s = s[:i] + ("BORU BOYU: alt uc artik YALITIMIN UST YUZUNDE bitiyor (kaset yerel y %.0f; modulde 250).\n"
                 "Onceki surumde 90 mm daha asagi sarkiyordu. Urunu yalitim deligindeki paslanmaz kovan indiriyor.\n" % YENI_ALT) + s[i:]

    yeni_satir = re.sub(r"(BORU_D, BORU_ET, BORU_ALT(?:, BORU_GECIS)?\s*=\s*[\d.]+,\s*[\d.]+,\s*)-?[\d.]+",
                        r"\g<1>%.1f" % YENI_ALT, s, count=1, flags=re.M)
    assert yeni_satir != s, eski + " — BORU_ALT satiri bulunamadi"
    s = yeni_satir
    s = s.replace("alt uç (kaset tabanının altında)", "alt uç (YALITIMIN ÜST YÜZÜ: kaset tabanının 10 mm altı)")
    s = re.sub(r"kaset tabanının \d+ mm altına iner", "yalıtımın üst yüzünde biter, ürünü yalıtımdaki kovan indirir", s)
    io.open(os.path.join(U, yeni + ".py"), "w", encoding="utf-8").write(s)
    print("%s -> %s  ·  BORU_ALT %.0f" % (eski, yeni, YENI_ALT))


for e, y in ISLER:
    don(e, y)
