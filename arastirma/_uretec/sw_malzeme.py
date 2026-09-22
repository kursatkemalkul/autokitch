# -*- coding: utf-8 -*-
# AUTOKITCH — MALZEME ATAMA (10 Eyl 2026)
#
# Parca adina gore SOLIDWORKS malzeme kutuphanesinden malzeme atar.
# Malzeme atanınca RENK DE KENDILIGINDEN gelir (kutuphane malzemesinin kendi gorunumu).
# Renk yalnizca kutuphanede karsiligi OLMAYAN kalemlerde elle veriliyor (satin alma bilesenleri).
#
# Kullanim:  python sw_malzeme.py 1_STORE_v3          (tek unite)
#            python sw_malzeme.py 1_STORE_v3 3_TOPPING ...
#
# Malzeme adlari "solidworks materials.sldmat" dosyasindan OKUNARAK dogrulandi — uydurma yok.
import sys, os, re, io, pythoncom
from sw_lib import *

ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
DB  = "SOLIDWORKS Materials"

# (isim kalibi, malzeme, elle renk|None)  — SIRA ONEMLI, ilk eslesen kazanir
KURAL = [
    # ---- kutuphanede karsiligi OLMAYAN satin alma bilesenleri: renk elle, koyu antrasit
    (r"kompresor|kondenser|evap_fan|evaporator|fan_D|pano_plc|pano_surucu|pano_guc|"
     r"psu|router|kilit_kontrol|step_motor|servo|reduktor|aktuator|pompa|selenoid|"
     r"sensor|reed|foto|ir_sensor|kamera|ekran|okuyucu|kontrolcu|ups_|priz_|"
     r"motor|surucu|klemens|amortisor|led_",           None, (0.16, 0.17, 0.19)),
    # ---- yalitim
    (r"_pu_|^pu_|pu_yan|pu_arka|pu_alt|pu_tavan|pu_dolgu|teknik_taban",
                                                       "Polyurethane Foam Rigid", None),
    (r"tasyunu",                                       "Polyurethane Foam Rigid", None),
    # ---- conta / kaucuk
    (r"conta_|kece|burulma_yayi|silikon",              "EPDM",                    None),
    # ---- cam
    (r"cam_",                                          "Glass",                   None),
    # ---- plastikler
    (r"_PC_|PC_5mm|burun_PC|govde_profil_PC|arka_kapak_PC",
                                                       "PC High Viscosity",       None),
    (r"helezon|POM|_yatak_POM|tarak_gobek",            "POM Acetal Copolymer",    None),
    (r"govde_HDPE|bidon|boyun_D40|kapak_D48",          "PE High Density",         None),
    (r"kutu_U|kutu_arka|blank|KUTU_|kutu_kapak|karton","Corrugated Paper",        None),
    # ---- miknatis / bakir
    (r"miknatis",                                      "Rubber",                  (0.12, 0.12, 0.14)),
    # ---- geri kalan her sey: PASLANMAZ SAC (gövde, panel, söve, plint, raf, ray, lama, tepsi...)
    (r".",                                             "AISI 304",                None),
]
DERLI = [(re.compile(p, re.I), m, c) for p, m, c in KURAL]


def esle(ad):
    for rx, m, c in DERLI:
        if rx.search(ad): return m, c
    return "AISI 304", None


LIMIT = 40          # bir calistirmada en fazla kac parca (SolidWorks tek oturumda 138 i kaldiramiyor)
IZ = ".malzeme_yapildi.txt"

def unite(kls):
    kok = os.path.join(ARA, kls)
    izy = os.path.join(kok, IZ)
    yapildi = set(io.open(izy, encoding="utf-8").read().splitlines()) if os.path.exists(izy) else set()
    dosyalar = [os.path.join(d, f) for d, _, fs in os.walk(kok) for f in fs if f.lower().endswith(".sldprt")]
    kalan = [y for y in dosyalar if y not in yapildi]
    print("%s — %d parca, %d kalan" % (kls, len(dosyalar), len(kalan)))
    if not kalan:
        print("KALAN: 0"); return
    e = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0); w = VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)
    say = {}; hata = 0; iz = io.open(izy, "a", encoding="utf-8")
    for i, yol in enumerate(kalan[:LIMIT], 1):
        ad = os.path.splitext(os.path.basename(yol))[0]
        mal, renk = esle(ad)
        try:
            d = sw.OpenDoc6(yol, 1, 0, "", e, w)
            if mal: mcall(d, "SetMaterialPropertyName2", "", DB, mal)
            if renk:
                d.MaterialPropertyValues = VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8,
                                                   list(renk) + [1.0, 1.0, 0.35, 0.30, 0.0, 0.0])
            saveas(d, yol); sw.CloseDoc(d.GetTitle)
            iz.write(yol + chr(10)); iz.flush()
            k = mal or "ELLE RENK"; say[k] = say.get(k, 0) + 1
        except Exception as ex:
            hata += 1; print("   HATA %s: %s" % (ad, ex)); break
    iz.close()
    for k, v in sorted(say.items(), key=lambda x: -x[1]): print("   %-28s %3d parca" % (k, v))
    if hata: print("   HATALI: %d" % hata)
    print("KALAN: %d" % (len(kalan) - len(say and [1]*sum(say.values()) or [])))


if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    for kls in sys.argv[1:]: unite(kls)
    try: sw.ExitApp()
    except Exception: pass
