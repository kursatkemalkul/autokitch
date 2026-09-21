# -*- coding: utf-8 -*-
"""AUTOKITCH · 3 · TOPPING MODÜLÜ — ÜRETİM MODELİ v1 (22 Eyl 2026)
Kemal: "bunlar niye bu kadar önde, birde arka kısımlarını o motor yerlerini — bu TOPPING'i full tasarla, üretime yönelik."

NE ÇÖZÜLDÜ
  · KASET ÖNE TAŞIYORDU: kulp z = 0'ın 48 mm önüne çıkıyordu, kabin kapanmıyordu. Kaset 80 mm içeri alındı,
    önüne yalıtımlı KAPAK kondu; kulp artık kabinin içinde (topping_hesap_v1.py · derinlik dizilimi).
  · ARKA 505 mm BOŞTU: artık KAVRAMA (40) + YALITIMLI BÖLME (65) + KURU MAKİNE BÖLMESİ (320). Motorlar soğuk hücrenin
    DIŞINDA, yalıtımın arkasında; mil bölmeden yataklı-keçeli kovanla geçiyor. Yoğuşma almıyorlar, soğutma yükü yok.
  · 12 TAHRİK (6 kaset × 2 mil): NEMA23 kapalı çevrim step + EŞ EKSENLİ planet redüktör i=10. Sonsuz vida (NMRV030)
    kullanılmadı: girişi dik olduğu için motor yana taşıyor, 140'lık kasetin arkasında komşuya giriyordu.
  · Mil eksenleri kaset üreteçlerinden OKUNUR (hardcode yok): 140 sınıfı CY 60 / YC 164 · kaşar CY 40 / YC 195.

KOORDİNAT (modül yereli): x 0..1800 soldan sağa · y 0..970 aşağıdan yukarı (makinede 1060 eklenir) · z 0 ön yüz, −830 arka.
ÇIKTI: arastirma/3_TOPPING/topping_modul_v1/ (parça başına STEP + STL, MONTAJ.step, BOM.csv) · otonom/hat3d/ (GLB/USDZ)
"""
import csv, io, json, math, os, re, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
URETIM = os.path.join(KOK, "arastirma", "3_TOPPING", "topping_modul_v1")
from kaset_3d_v3 import Mesh, MM, MALZEME, doku_ad, usdz_yaz, OUT
import topping_hesap_v1 as H

# ---------------------------------------------------------------- SABİTLER ----------------------------------------------------------------
W, Y, D = 1800.0, 970.0, 830.0                       # modül gabarisi (pafta HAT v19: modül C)
SAC, SAC_IC, PU = 1.5, 1.0, 60.0                     # dış sac · iç kabuk · poliüretan
Y0 = 1060.0                                          # modülün makinedeki taban kotu
ZK = H.Z_KASET; ZKAP = H.Z_KAPAK; ZKAV = H.Z_KAVRAMA; ZBOL = H.Z_BOLME; ZKURU = H.Z_KURU
AGZ = (10.0, 120.0); BAS = (123.0, 257.0); KAS = (260.0, 620.0); TEK = (706.0, 962.0)    # yerel y zonları
# Harç kasetleri henüz tasarlanmadı; yuvası 280 (kaşar gövdesi sınıfı) ve mil eksenleri de kaşarınki VARSAYILDI.
# PAFTA DÜZELTMESİ: HAT v19'da yuva genişlikleri kaset genişliğine BİREBİR eşitti ve yuvalar bitişikti —
# kılavuz lamasına ve geçme boşluğuna yer kalmıyordu, kaset fiziksel olarak girmezdi. Yuvalar burada
# kaset + BOSLUK, aralarında BOLME kalınlığında ayırıcı olacak şekilde YENİDEN hesaplanıyor ve ortalanıyor.
BOSLUK, BOLME = 2.0, 3.0
_ADLAR = ("HARÇ 1", "HARÇ 2", "KIYMA", "KUŞBAŞI", "KAŞAR KABI", "KÜP SUCUK")
_GEN = (280, 280, 140, 140, 280, 140)
_TOP = sum(_GEN) + len(_GEN) * BOSLUK + (len(_GEN) + 1) * BOLME
_X = round(30.0 + PU + ((W - 2 * (30.0 + PU)) - _TOP) / 2.0, 1)
YUVA = []
for _ad, _g in zip(_ADLAR, _GEN):
    _X += BOLME
    YUVA.append((_ad, _X, _X + _g + BOSLUK, _g)); _X += _g + BOSLUK
_X += BOLME
KASET_CAD = {140: "kiyma_cad_v5", 280: "kasar_cad_v10"}
MALZEME.setdefault("sac", dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32))
MALZEME.setdefault("pu", dict(renk=(0.93, 0.88, 0.72, 1.0), met=0.0, ruf=0.85))
MALZEME.setdefault("motor", dict(renk=(0.18, 0.19, 0.22, 1.0), met=0.5, ruf=0.45))
MALZEME.setdefault("bakir", dict(renk=(0.72, 0.45, 0.20, 1.0), met=0.9, ruf=0.35))
MALZEME.setdefault("kart", dict(renk=(0.10, 0.35, 0.22, 1.0), met=0.1, ruf=0.6))


def eksen(modul):
    """kaset üretecinden mil eksenlerini OKU (iki yerde yazılmasın)"""
    s = io.open(os.path.join(U, modul + ".py"), encoding="utf-8").read()
    m = re.search(r"CY, RT, YC, RB, RF, Y_UST, Y_DOLUM = ([\d.]+), ([\d.]+), ([\d.]+)", s)
    assert m, modul + ": eksen satiri bulunamadi"
    return float(m.group(1)), float(m.group(3))


EKSEN = {g: eksen(KASET_CAD[g]) for g in (140, 280)}          # {genişlik: (CY alt mil, YC üst mil)} kasetin kendi tabanından

kut = lambda x0, x1, y0, y1, z0, z1: cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
PARCALAR = []
def ekle(ad, wp, mal, bom=None): PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, bom=bom))


def modul():
    hy0, hy1 = KAS[0] - 20.0, KAS[1] + 20.0                                   # soğuk hücre iç yüksekliği (240 … 640)
    zc0, zc1 = ZKAP[1], ZBOL[1]                                               # soğuk paket derinliği (−20 … −510)
    XI0, XI1 = 30.0 + PU, W - 30.0 - PU                                       # hücre iç genişliği (90 … 1710)
    MIL = []                                                                  # (x, y, kod) — 12 tahrik mili; yalıtım ve kabuk bunlara göre delinir
    for ad, x0, x1, gen in YUVA:
        for j, ey in enumerate(EKSEN[gen]):
            MIL.append(((x0 + x1) / 2.0, KAS[0] + ey, "%s_%s" % (ad.replace(" ", "_"), "helezon" if j == 0 else "rotor")))
    # Kasetin MEMESİ hücrenin tabanından geçer: her yuvanın altına yarık açılır, ürün oradan aşağıdaki dozaj bandına düşer.
    YARIK = [(x0 + 20.0, x1 - 20.0) for ad, x0, x1, gen in YUVA]
    ZY = (ZK[0] - 5.0, ZK[0] - 120.0)                                         # yarığın derinlik aralığı (kasetin ön bölgesi)

    # ---------------- 1 · DIŞ KABUK (bükme sac 1,5 · AISI 304) ----------------
    ekle("dis_taban", kut(0, W, 0, SAC, 0, -D), "sac", bom=("Dış taban sacı", 1, "304 1,5 mm · lazer + abkant", "modülün tabanı, alttaki B modülüne oturur"))
    ekle("dis_tavan", kut(0, W, Y - SAC, Y, 0, -D), "sac", bom=("Dış tavan sacı", 1, "304 1,5 mm · lazer + abkant", "üst kapak; soğutma grubu buraya oturur"))
    for s, x in (("sol", 0.0), ("sag", W - SAC)):
        ekle("dis_yan_" + s, kut(x, x + SAC, SAC, Y - SAC, 0, -D), "sac", bom=("Dış yan sac", 2, "304 1,5 mm · lazer + abkant", "komşu modüle cıvatalanır (lego birleşim)") if s == "sol" else None)
    ekle("dis_arka", kut(SAC, W - SAC, SAC, Y - SAC, -D, -D + SAC), "sac", bom=("Dış arka sac", 1, "304 1,5 mm", "kuru bölmenin arkası; kablo rakorları burada"))

    # ---------------- 2 · ÖN ÇERÇEVE ve AĞIZLAR ----------------
    on = kut(SAC, W - SAC, SAC, Y - SAC, 0, -SAC)
    on = on.cut(kut(30.0, W - 30.0, AGZ[0], AGZ[1], 1, -2))                   # robot ağzı 1740 × 110
    on = on.cut(kut(78.0, W - 78.0, KAS[0] - 30.0, KAS[1] + 30.0, 1, -2))     # kaset kapağı açıklığı (kapak + conta buraya oturur)
    on = on.cut(kut(40.0, W - 40.0, TEK[0] + 10.0, TEK[1] - 10.0, 1, -2))     # teknik bant servis kapağı
    ekle("on_cerceve", on, "sac", bom=("Ön çerçeve sacı", 1, "304 1,5 mm · lazer", "robot ağzı 1740 × 110 · kaset kapağı açıklığı · teknik bant servis açıklığı"))

    # ---------------- 3 · SOĞUK HÜCRE: PU 60 + iç kabuk 1,0 ----------------
    PUP = (("pu_taban", 30.0, W - 30.0, hy0 - PU, hy0), ("pu_tavan", 30.0, W - 30.0, hy1, hy1 + PU),
           ("pu_sol", 30.0, 30.0 + PU, hy0, hy1), ("pu_sag", W - 30.0 - PU, W - 30.0, hy0, hy1))
    for ad, x0, x1, y0, y1 in PUP:
        w_ = kut(x0, x1, y0, y1, zc0, zc1)
        if ad == "pu_taban":
            for a_, b_ in YARIK: w_ = w_.cut(kut(a_, b_, y0 - 1, y1 + 1, ZY[0], ZY[1]))      # meme yarıkları
        ekle(ad, w_, "pu", bom=("PU yalıtım paneli 60 mm", 4, "poliüretan 60 · λ 0,022 W/mK", "soğuk hücreyi sarar; ısı kaybı hesabı topping_hesap_v1") if ad == "pu_taban" else None)
    arka = kut(XI0, XI1, hy0, hy1, ZBOL[0], ZBOL[1])
    for x_, y_, k_ in MIL: arka = arka.cut(silz(x_, y_, 31.0, ZBOL[0] + 1, ZBOL[1] - 1))     # 12 mil geçişi
    ekle("pu_arka", arka, "pu", bom=("PU arka bölme paneli 60 mm", 1, "poliüretan 60", "SOĞUK / KURU ayırıcı: motorlar bunun arkasında kalır"))

    ic = kut(XI0, XI1, hy0, hy1, zc0, ZBOL[0])
    ic = ic.cut(kut(XI0 + SAC_IC, XI1 - SAC_IC, hy0 + SAC_IC, hy1 - SAC_IC, zc0 + 1, ZBOL[0] + SAC_IC))
    for a_, b_ in YARIK: ic = ic.cut(kut(a_, b_, hy0 - 1, hy0 + 2, ZY[0], ZY[1]))
    for x_, y_, k_ in MIL: ic = ic.cut(silz(x_, y_, 31.0, ZBOL[0] - 1, ZBOL[0] + SAC_IC + 1))
    ekle("ic_kabuk", ic, "sac", bom=("İç kabuk (soğuk hücre)", 1, "304 1,0 mm · bükme, köşeler kaynaklı-taşlanmış", "gıda bölgesi: köşe R ≥ 6, yıkanabilir; 6 meme yarığı + 12 mil geçişi"))

    # ---------------- 4 · ÖN KAPAK ----------------
    ekle("on_kapak", kut(84.0, W - 84.0, KAS[0] - 26.0, KAS[1] + 26.0, ZKAP[0], ZKAP[1] + 6.0), "sac",
         bom=("Ön kapak · sandviç", 1, "1,5 sac + 17 PU + 1,5 sac · 2 menteşe + mıknatıslı kilit", "kaset ağzını kapatır; açılınca 6 kaset önden çekilir"))
    cont = kut(88.0, W - 88.0, KAS[0] - 22.0, KAS[1] + 22.0, ZKAP[1] + 6.0, ZKAP[1])
    cont = cont.cut(kut(102.0, W - 102.0, KAS[0] - 8.0, KAS[1] + 8.0, ZKAP[1] + 7.0, ZKAP[1] - 1.0))
    ekle("kapak_contasi", cont, "silikon", bom=("Kapak contası", 1, "manyetik buzdolabı contası", "kapağın arka yüzünde; yalıtım panelinin ön yüzüne basar"))
    for i, xx in enumerate((110.0, W - 140.0)):
        ekle("mentese_%d" % i, kut(xx, xx + 30.0, KAS[0] - 30.0, KAS[0] - 26.0, ZKAP[0] - 4.0, ZKAP[1] + 2.0), "celik",
             bom=("Menteşe", 2, "paslanmaz, gömme", "kapak alttan menteşeli: açılınca tezgâh gibi öne yatar") if i == 0 else None)

    # ---------------- 5 · KASET YUVALARI ----------------
    for ad, x0, x1, gen in YUVA:
        k = ad.replace(" ", "_")
        ray = kut(x0 + 6.0, x1 - 6.0, KAS[0] - 4.0, KAS[0], ZK[0], ZK[1])
        for a_, b_ in YARIK: ray = ray.cut(kut(a_, b_, KAS[0] - 5.0, KAS[0] + 1.0, ZY[0], ZY[1]))
        ekle("ray_%s" % k, ray, "sac", bom=None)
        for i, xx in enumerate((x0 + 20.0, x1 - 30.0)):
            ekle("konum_pimi_%s_%d" % (k, i), silz(xx + 5.0, KAS[0] + 20.0, 5.0, ZKAV[0], ZKAV[0] - 12.0), "celik", bom=None)
        ekle("huni_%s" % k, kut(x0 + 22.0, x1 - 22.0, hy0 - PU - 4.0, KAS[0] - 4.0, ZY[0] - 2.0, ZY[1] + 2.0)
             .cut(kut(x0 + 25.0, x1 - 25.0, hy0 - PU - 5.0, KAS[0] - 3.0, ZY[0] - 5.0, ZY[1] + 5.0)), "sac", bom=None)
    for i, xx in enumerate([YUVA[0][1] - BOLME] + [y[2] for y in YUVA]):
        ekle("bolme_%d" % i, kut(xx, xx + BOLME, KAS[0], KAS[0] + 60.0, ZK[0], ZK[1]), "sac", bom=None)
    for a_, ad_, n_, malz_, gor_ in (("_bom_kilavuz", "Yuva ayırıcı lama 3 × 60 × 325", 7, "304 lama, iç kabuğa kaynaklı", "kasetin iki yanını kılavuzlar; kaset ile arasında 2 mm boşluk"),
                                     ("_bom_ray", "Taban rayı", 6, "304 bükme, meme yarığı açık", "kaset üstünde kayar; altındaki yarıktan meme geçer"),
                                     ("_bom_pim", "Konum pimi Ø10", 12, "304 taşlanmış", "kaset arkada iki pimle merkezlenir → kavrama hizalanır"),
                                     ("_bom_huni", "Dozaj hunisi", 6, "304 1,0 mm, çekip çıkarılır", "memeden çıkanı aşağıdaki robot ağzına yönlendirir; yıkamak için sökülür")):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "sac", bom=(ad_, n_, malz_, gor_))

    # ---------------- 6 · TAHRİK ×12 (kuru bölmede) ----------------
    R = H.S["tahrik"]; MO, RE, YA, KE = R["motor"], R["reduktor"], R["yatak"], R["kece"]
    for xm, yy, k in MIL:
        sok = silz(xm, yy, 22.0, ZKAV[0], ZKAV[0] - 26.0)
        sok = sok.cut(kut(xm - 19, xm + 19, yy - 3, yy + 3, ZKAV[0] + 1, ZKAV[0] - 20.0)).cut(kut(xm - 3, xm + 3, yy - 19, yy + 19, ZKAV[0] + 1, ZKAV[0] - 20.0))
        ekle("soket_" + k, sok, "pom", bom=None)
        ekle("yay_" + k, silz(xm, yy, 16.0, ZKAV[0] - 26.0, ZKAV[1]).cut(silz(xm, yy, 12.0, ZKAV[0] - 27.0, ZKAV[1] - 1.0)), "celik", bom=None)
        ekle("mil_" + k, silz(xm, yy, 11.0, ZKAV[1], ZBOL[1] - 40.0), "celik", bom=None)
        kov = silz(xm, yy, 30.0, ZBOL[0], ZBOL[1] - 18.0)
        kov = kov.cut(silz(xm, yy, YA["cap_dis"] / 2, ZBOL[0] - 1, ZBOL[0] + YA["z"]))
        kov = kov.cut(silz(xm, yy, KE["cap_dis"] / 2, ZBOL[1] - 18.0 - KE["z"], ZBOL[1] - 17.0))
        kov = kov.cut(silz(xm, yy, 11.2, ZBOL[0] + 1, ZBOL[1] - 19.0))
        ekle("kovan_" + k, kov, "pom", bom=None)
        ekle("reduktor_" + k, silz(xm, yy, RE["cap"] / 2, ZBOL[1] - 42.0, ZBOL[1] - 42.0 - RE["z"]), "motor", bom=None)
        zm = ZBOL[1] - 42.0 - RE["z"] - 2.0
        ekle("motor_" + k, kut(xm - MO["g"] / 2, xm + MO["g"] / 2, yy - MO["y"] / 2, yy + MO["y"] / 2, zm, zm - MO["z"]), "motor", bom=None)
    for a_, ad_, n_, malz_, gor_ in (("_bom_soket", "Yaylı haç soketi", 12, "POM-C + paslanmaz yay", "kaset takılınca haç kavramaya oturur; yay kursu 14 mm, diş kaçarsa kaset zorlanmaz"),
                                     ("_bom_mil", "Tahrik mili Ø22", 12, "AISI 304 taşlanmış", "yalıtımlı bölmeden geçer; soğuk tarafta soket, kuru tarafta redüktör"),
                                     ("_bom_kovan", "Yataklı-keçeli kovan", 12, "POM-C gövde + yatak ×2 + keçe 22×35×7", "mili bölmeden SIZDIRMAZ geçirir; soğuk hücreye nem girmez"),
                                     ("_bom_red", "Planet redüktör i = 10", 12, "PLF60/PLE60 sınıfı · eş eksenli", "sonsuz vida DEĞİL: girişi dik olduğu için motor yana taşıyordu"),
                                     ("_bom_motor", "NEMA23 kapalı çevrim step 1,2 N·m", 12, "sürücüsüyle birlikte", "dozaj = mil açısı; kapalı çevrim adım kaçırmayı yakalar")):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "celik", bom=(ad_, n_, malz_, gor_))

    # ---------------- 7 · SOĞUTMA ----------------
    ekle("evaporator", kut(420.0, 1280.0, hy1 - 120.0, hy1 - 20.0, ZBOL[0] + 5.0, ZBOL[0] + 115.0), "bakir",
         bom=("Evaporatör", 1, "lamelli, paslanmaz karter", "soğuk hücrenin üst-arkasında; hesaplanan yük %.0f W, seçim %.0f W" % (H.S["soguk"]["q_toplam"], H.S["soguk"]["q_secim"])))
    for i, xx in enumerate((560.0, 1140.0)):
        ekle("fan_%d" % i, silz(xx, hy1 - 58.0, 55.0, ZBOL[0] + 118.0, ZBOL[0] + 168.0), "motor",
             bom=("Evaporatör fanı Ø150", 2, "24 V eksenel, 12 W", "havayı kasetlerin üstünden geçirir") if i == 0 else None)
    ekle("hava_kanali", kut(XI0 + SAC_IC + 2.0, XI1 - SAC_IC - 2.0, hy1 - 136.0, hy1 - 132.0, ZBOL[0] + 4.0, ZK[0]), "sac",
         bom=("Hava kanalı saci", 1, "304 1,0 mm delikli", "soğuk havayı kaset sırasının üstüne dağıtır, doğrudan üflemez"))
    ekle("sogutma_grubu", kut(60.0, 360.0, TEK[0] + 6.0, TEK[0] + 226.0, -60.0, -280.0), "motor",
         bom=("Soğutma grubu ⅕ HP", 1, "hermetik, hava soğutmalı", "teknik bantta, önden servis; +3 °C'de 250–350 W verir"))

    # ---------------- 8 · ELEKTRİK (teknik bant) ----------------
    ekle("pano_kutusu", kut(1100.0, 1500.0, TEK[0] + 6.0, TEK[0] + 246.0, -40.0, -290.0), "sac",
         bom=("Ana pano kutusu", 1, "304 · önden kapaklı, IP54", "PLC + ana şalter + röleler; ekran yok, tablet"))
    ekle("ups", kut(1520.0, 1740.0, TEK[0] + 6.0, TEK[0] + 156.0, -40.0, -230.0), "koyu", bom=("UPS 500 VA", 1, "hat içi", "elektrik kesintisinde kaset konumları ve saat korunur"))
    ekle("guc_kaynagi", kut(400.0, 560.0, TEK[0] + 6.0, TEK[0] + 106.0, -40.0, -140.0), "sac",
         bom=("Güç kaynağı 24 V %d W" % H.S["elektrik"]["guc_kaynagi_W"], 1, "DIN raya", "aynı anda en çok 2 mil döner"))
    ekle("din_ray", kut(600.0, 1060.0, TEK[0] + 26.0, TEK[0] + 41.0, -140.0, -147.0), "sac", bom=("DIN ray 35 mm", 1, "standart", "sürücü kartları burada"))
    for i in range(12):
        xx = 605.0 + i * 38.0
        ekle("surucu_%d" % i, kut(xx, xx + 34.0, TEK[0] + 6.0, TEK[0] + 81.0, -45.0, -140.0), "kart",
             bom=("Step sürücü kartı", 12, "kapalı çevrim, 24 V", "her mile bir sürücü: 6 kaset × 2") if i == 0 else None)

    # ---------------- 9 · AĞIZ ve DAMLAMA ----------------
    agz = kut(30.0, W - 30.0, AGZ[0] - 6.0, AGZ[1] + 6.0, -SAC, -30.0).cut(kut(36.0, W - 36.0, AGZ[0], AGZ[1], -SAC + 1, -31.0))
    ekle("agiz_cercevesi", agz, "sac", bom=("Robot ağzı çerçevesi", 1, "304 1,5 mm bükme", "1740 × 110 açıklık; kenarları kıvrık, robot çarparsa zarar vermez"))
    ekle("damlama_teknesi", kut(200.0, 1560.0, AGZ[1] + 14.0, AGZ[1] + 40.0, -34.0, -200.0), "sac",
         bom=("Damlama teknesi", 1, "304 1,0 mm, öne eğimli, çekmeceli", "hunilerden damlayanı toplar; öne çekilip boşaltılır"))


if __name__ == "__main__":
    t0 = time.time(); modul()
    gercek = [p for p in PARCALAR if not p["ad"].startswith("_bom")]
    print("TOPPING MODULU v1 · %d parca (%d cizili + %d yalniz listede) · %.0f sn" % (len(PARCALAR), len(gercek), len(PARCALAR) - len(gercek), time.time() - t0))
    gecersiz = [p["ad"] for p in gercek if not p["wp"].val().isValid()]
    print("KATI DENETIMI: %s" % ("hepsi gecerli" if not gecersiz else "GECERSIZ: " + ", ".join(gecersiz))); assert not gecersiz

    # ---- zarf ----
    bb = [(p["ad"], p["wp"].val().BoundingBox()) for p in gercek]
    tas = [a for a, b in bb if b.xmin < -0.01 or b.xmax > W + 0.01 or b.ymin < -0.01 or b.ymax > Y + 0.01 or b.zmax > 0.01 or b.zmin < -D - 0.01]
    print("ZARF: %s (%.0f × %.0f × %.0f)" % ("hepsi modulun icinde" if not tas else "TASAN: " + ", ".join(tas), W, Y, D)); assert not tas

    # ---- çakışma ----
    S = [(p["ad"], p["wp"].val(), p["wp"].val().BoundingBox()) for p in gercek]; bulgu = []
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            a, b = S[i][2], S[j][2]
            if a.xmax < b.xmin or b.xmax < a.xmin or a.ymax < b.ymin or b.ymax < a.ymin or a.zmax < b.zmin or b.zmax < a.zmin: continue
            try: v = S[i][1].intersect(S[j][1]).Volume()
            except Exception: v = -1.0
            if v > 1.0 or v < 0: bulgu.append((S[i][0], S[j][0], round(v, 1)))
    print("CAKISMA: %s" % ("TEMIZ" if not bulgu else "%d BULGU" % len(bulgu)))
    for x in bulgu: print("   ", x)
    assert not bulgu

    # ---- KASET YUVAYA SIĞIYOR MU + TAHRİK EKSENİ TUTUYOR MU ----
    print("YUVA DENETIMI:")
    for ad, x0, x1, gen in YUVA:
        bosluk = (x1 - x0) - gen
        alt, ust = EKSEN[gen]
        print("   %-11s yuva %.0f  kaset %.0f  bosluk %.1f mm · mil kotlari (kaset tabanindan) %.0f / %.0f" % (ad, x1 - x0, gen, bosluk, alt, ust))
        assert abs(bosluk - BOSLUK) < 0.01, "%s: yuva-kaset boslugu %.1f (olmasi gereken %.1f)" % (ad, bosluk, BOSLUK)
    ekseni = {}
    for p in gercek:
        if p["ad"].startswith("mil_"):
            b = p["wp"].val().BoundingBox(); ekseni[p["ad"]] = round((b.ymin + b.ymax) / 2.0, 1)
    bek = []
    for ad, x0, x1, gen in YUVA:
        for j, ey in enumerate(EKSEN[gen]):
            k = "mil_%s_%s" % (ad.replace(" ", "_"), "helezon" if j == 0 else "rotor")
            bek.append((k, round(KAS[0] + ey, 1), ekseni.get(k)))
    kotu = [x for x in bek if x[1] != x[2]]
    print("   tahrik mil eksenleri kasetin kendi eksenleriyle AYNI: %s" % ("EVET (12/12)" if not kotu else kotu)); assert not kotu
    print("   derinlik: kapak %.0f | kulp %.0f | kaset %.0f | kavrama %.0f | yalitim %.0f | kuru %.0f = %.0f mm"
          % (H.ON_KAPAK, H.KULP_BOS, H.KASET_D, H.KAVRAMA, H.ARKA_PU, abs(ZKURU[1] - ZKURU[0]), D))

    # ---- üretim dosyaları ----
    os.makedirs(os.path.join(URETIM, "step"), exist_ok=True); os.makedirs(os.path.join(URETIM, "stl"), exist_ok=True)
    asm = cq.Assembly(name="TOPPING_MODUL_v1"); RENK = dict(sac=(0.74, 0.77, 0.80, 1), pu=(0.93, 0.88, 0.72, 1), motor=(0.18, 0.19, 0.22, 1),
                                                            pom=(0.95, 0.95, 0.92, 1), celik=(0.75, 0.77, 0.8, 1), bakir=(0.72, 0.45, 0.2, 1), kart=(0.1, 0.35, 0.22, 1), koyu=(0.15, 0.15, 0.17, 1), silikon=(0.16, 0.5, 0.95, 1))
    bom = []
    for p in gercek:
        sh = p["wp"].val(); b = sh.BoundingBox()
        cq.exporters.export(p["wp"], os.path.join(URETIM, "step", p["ad"] + ".step"))
        cq.exporters.export(p["wp"], os.path.join(URETIM, "stl", p["ad"] + ".stl"), tolerance=0.1, angularTolerance=0.3)
        asm.add(sh, name=p["ad"], color=cq.Color(*RENK.get(p["mal"], (0.8, 0.8, 0.8, 1))))
    for p in PARCALAR:
        if p["bom"]:
            b = p["wp"].val().BoundingBox()
            bom.append((p["ad"],) + tuple(p["bom"]) + ("%.0f × %.0f × %.0f" % (b.xlen, b.ylen, b.zlen),))
    asm.save(os.path.join(URETIM, "TOPPING_MODUL_v1_MONTAJ.step"))
    with io.open(os.path.join(URETIM, "BOM.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(["dosya", "parça", "adet", "malzeme · yöntem", "görevi", "zarf mm"]); w.writerows(bom)
    with io.open(os.path.join(URETIM, "bom.json"), "w", encoding="utf-8") as f: json.dump(bom, f, ensure_ascii=False)
    print("URETIM: %d STEP + %d STL + MONTAJ.step + BOM.csv (%d kalem) → %s" % (len(gercek), len(gercek), len(bom), URETIM))
    for b in bom: print("   %-22s %-38s ×%-3s %s" % (b[0], b[1], b[2], b[5]))
    sys.stdout.flush(); os._exit(0)
