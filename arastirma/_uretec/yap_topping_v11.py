# -*- coding: utf-8 -*-
"""topping_cad_v10 -> v11 : YUVA ETIKET PLAKALARI.

Kemal: "birde onune etiket koy kasetlerin hangi urun oldugunu, yada kasete koy — ama eger makinenin
biyerine mi koymak lazim, cunku cogu kaset ORTAK, sadece vidalari farkli degil mi? Belkide YUVALARIN
ONUNE etiket koymak lazim."

Hakli: govde ortak (ORTAK GOVDE 140 karari), ayirt eden sey icindeki vida. O yuzden urun adi MAKINEYE,
yuvanin onune yaziliyor: operator hangi yuvaya ne girdigini kasete bakmadan goruyor.

YER: ic kabugun on rimi, kasetin USTUNDE (kaset tavani y 620, hucre tavani y 640) -> plaka y 621..637,
z -106,5..-105 (hucre agzinin on rimi). On kapak -84..-104 arasinda, arada 1 mm bosluk; kaset -200'de.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "topping_cad_v10.py"), encoding="utf-8").read()

anc = """    for a_, ad_, n_, malz_, gor_ in (("_bom_kovan", "Dozaj kovanı", 6,"""
assert anc in s, "kovan BOM bulunamadi"

yeni = '''    # v11 · YUVA ETİKET PLAKASI: ürün adı KASETE değil MAKİNEYE yazılıyor. Kaset gövdeleri ortak
    # (ORTAK GÖVDE 140), ayırt eden şey içindeki vida — o yüzden "bu yuvaya ne girer" bilgisi yuvanın
    # kendisine ait. Plaka iç kabuğun ön rimine, kasetin ÜSTÜNE oturuyor; kaset takılıyken de okunur.
    for ad, x0, x1, gen in YUVA:
        pl = kut(x0 + 15.0, x1 - 15.0, ET_Y0, ET_Y1, ET_Z0, ET_Z1)
        ekle("yuva_etiketi_%s" % ad.replace(" ", "_"), pl, "sac", bom=None)
    for a_, ad_, n_, malz_, gor_ in (("_bom_yuva_etiket", "Yuva etiket plakası", 6,
            "304 1,5 mm · baskılı ya da lazer kazıma", "ürün adı yuvanın üstünde; kaset gövdeleri ortak olduğu için ürün bilgisi makinede durur"),):
        ekle(a_, kut(0, 0.1, 0, 0.1, 0, -0.1), "sac", bom=(ad_, n_, malz_, gor_))
'''
s = s.replace(anc, yeni + anc, 1)

# etiket kotlari: modul() disinda, hat_montaj da bunlari OKUYACAK (tek yerde dursun)
anc2 = "def ekle(ad, wp, mal, bom=None):"
kot = """# v11 · yuva etiketi kotlari — hat_montaj dokuyu BU kotlara yapistiriyor, iki yerde ayri sayi olmasin
ET_Y0, ET_Y1 = KAS[1] + 1.0, KAS[1] + 17.0          # kaset tavaninin (620) 1 mm ustu, 16 mm yuksek
ET_Z0, ET_Z1 = ZKAP[1] - 2.5, ZKAP[1] - 1.0        # hucrenin ON RIMINDE, on kapagin 1 mm gerisinde
# Yuvaya giren urunun adi — etiketin yazisi ve simulasyon bunu OKUR (iki yerde ayri liste olmasin)
URUN = {"HARÇ 1": "LAHMACUN HARCI", "HARÇ 2": "PİZZA SOSU", "KIYMA": "KIYMA",
        "KUŞBAŞI": "KUŞBAŞI", "KAŞAR KABI": "KAŞAR", "KÜP SUCUK": "KÜP SUCUK"}

"""
assert anc2 in s
s = s.replace(anc2, kot + anc2, 1)

io.open(os.path.join(U, "topping_cad_v11.py"), "w", encoding="utf-8").write(s)
print("topping_cad_v11.py yazildi")
