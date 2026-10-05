# -*- coding: utf-8 -*-
"""topping_cad_v14 -> v15 : SAHTE KUTLELER TEMIZLENIYOR

Modul 825,3 kg cikiyordu; bunun 518 kg'i BES YER TUTUCU BLOKTAN geliyordu. Hepsi
masif kutu olarak modellenmisti, hacim x yogunluk sacma sayi veriyordu:
    pano_kutusu    189,6 kg   (1,5 mm sac kabin, ~20 kg olmali)
    sogutma_grubu  114,7 kg   (1/5 HP hermetik grup, ~26 kg)
    evaporator      90,3 kg   (MASIF BAKIR! unit cooler ~7 kg)
    on_kapak        74,4 kg   (1,5 sac + 17 PU + 1,5 sac sandvic, ~12 kg)
    ups             49,5 kg   (500 VA UPS, ~8,5 kg)

BU DOSYA IKISINI GEOMETRIDEN DUZELTIYOR (bizim imal ettigimiz parcalar):
  on_kapak    -> SAC KABUK + PU CEKIRDEK (BOM zaten boyle yaziyordu, geometri tutmuyordu)
  pano_kutusu -> 1,5 mm SAC KABUK (ici bos kabin)
Satin alinan uc birim (sogutma grubu, evaporator, UPS) ZARF olarak kalir — yerleri dogru,
kutleleri topping_fizik_ihrac'taki KATALOG_KUTLE tablosundan verilir.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v14.py"), encoding="utf-8").read()

# ---------------- ON KAPAK: masif blok -> sac kabuk + PU cekirdek
eski = '''    ekle("on_kapak", kut(84.0, W - 84.0, KAS[0] - 26.0, KAS[1] + 26.0, ZKAP[0], ZKAP[1] + 6.0), "sac",
         bom=("Ön kapak · sandviç", 1, "1,5 sac + 17 PU + 1,5 sac · 2 menteşe + mıknatıslı kilit", "kaset ağzını kapatır; açılınca 6 kaset önden çekilir"))'''
yeni = '''    # v15: masif blok degil GERCEK SANDVIC. Disi 1,5 mm sac kabuk, ici PU.
    # (Masif modellenince 74,4 kg cikiyordu; gercegi ~12 kg.)
    _kx0, _kx1 = 84.0, W - 84.0
    _ky0, _ky1 = KAS[0] - 26.0, KAS[1] + 26.0
    _kz0, _kz1 = ZKAP[0], ZKAP[1] + 6.0
    _dis = kut(_kx0, _kx1, _ky0, _ky1, _kz0, _kz1)
    _ic = kut(_kx0 + 1.5, _kx1 - 1.5, _ky0 + 1.5, _ky1 - 1.5,
              min(_kz0, _kz1) + 1.5, max(_kz0, _kz1) - 1.5)
    ekle("on_kapak", _dis.cut(_ic), "sac",
         bom=("Ön kapak sacı · sandviç kabuğu", 1, "1,5 mm 304 · 2 menteşe + mıknatıslı kilit", "kaset ağzını kapatır; açılınca 6 kaset önden çekilir"))
    ekle("on_kapak_pu", _ic, "pu",
         bom=("Ön kapak PU dolgusu", 1, "poliüretan köpük 40 kg/m³", "sandviçin yalıtım çekirdeği"))'''
assert eski in s
s = s.replace(eski, yeni, 1)

# ---------------- PANO KUTUSU: masif blok -> 1,5 mm sac kabuk
eski = '''    ekle("pano_kutusu", kut(1100.0, 1500.0, TEK[0] + 6.0, TEK[0] + 246.0, -40.0, -290.0), "sac",'''
yeni = '''    # v15: masif degil 1,5 mm SAC KABIN (masifken 189,6 kg cikiyordu, gercegi ~20 kg)
    _pd = kut(1100.0, 1500.0, TEK[0] + 6.0, TEK[0] + 246.0, -40.0, -290.0)
    _pi = kut(1101.5, 1498.5, TEK[0] + 7.5, TEK[0] + 244.5, -41.5, -288.5)
    ekle("pano_kutusu", _pd.cut(_pi), "sac",'''
assert eski in s
s = s.replace(eski, yeni, 1)

io.open(os.path.join(U, "topping_cad_v15.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v15.py yazildi")
