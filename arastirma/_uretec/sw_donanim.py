# -*- coding: utf-8 -*-
# AUTOKITCH — ORTAK DONANIM (10 Eyl 2026)
# Her istasyonun kendi kopyasini urettigi KATALOG parcalari tek forma indirildi:
#   AYAK_AYAR_M12    : 6 istasyon x 4 adet — onceden 48 ayri parca dosyasi
#   MENTESE_GIZLI_34 : 5 istasyon, kapi basina 2-3 adet — onceden 27 dosya
#   MANDAL_BAS_AC    : 5 istasyon, kapi basina 1 adet — onceden 13 dosya
# Tek yerden degisir: mentese markasi degisirse yalnizca bu dosya guncellenir.
import sys, os
from sw_lib import *

ORTAK = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_ortak"


def _yeni(ad):
    st = Station(os.path.join(ORTAK, ad), ad)
    for f in os.listdir(st.pdir):
        if f.lower().endswith(".sldprt"): os.remove(os.path.join(st.pdir, f))
    return st


def ayak_ayar():
    """AYAR AYAGI M12 — Ø50 taban + M12 mil, 0..40 ayar. Yerel: eksen x=0 / z=0, zemin y=0"""
    ad = "AYAK_AYAR_M12"; st = _yeni(ad); p = "AY_"
    st.cyl_y(p+"taban_D50", 0.0, 0.0, 25.0, 0.0, 12.0)
    st.cyl_y(p+"mil_M12",   0.0, 0.0,  6.0, 12.0, 40.0)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


def mentese_gizli():
    """GIZLI MENTESE 34 x 40 x 14 — kapak kenarina gomulu, disaridan gorunmez.
       Yerel: sol yuz x=0, alt y=0, z 18..32 (kapak ic sacinin arkasi)"""
    ad = "MENTESE_GIZLI_34"; st = _yeni(ad); p = "MG_"
    st.box(p+"govde_34x40x14", 0.0, 34.0, 0.0, 40.0, 18.0, 32.0)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


def mandal_bas_ac():
    """BAS-AC MANDALI 60 x 20 x 11 — kulp yok kuralinin karsiligi; itince acilir.
       Yerel: sol yuz x=0, alt y=0, z 8..19 (kapak ic sacina 1 mm pay)"""
    ad = "MANDAL_BAS_AC"; st = _yeni(ad); p = "MB_"
    st.box(p+"govde_60x20x11", 0.0, 60.0, 0.0, 20.0, 8.0, 19.0)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


def kola_kutusu_dik():
    """KOLA KUTUSU 330 ml — DIK duran tip (Ø66 x 115). Mevcut KUTU_KOLA_330ml YATAY eksende
       modellenmis; delikli hizalama sacina dik duran kutu gerekiyor. Yerel: taban y = 0."""
    ad = "KUTU_KOLA_330ml_DIK"; st = _yeni(ad); p = "KLD_"
    st.cyl_y(p+"alt_bilezik_D60", 0.0, 0.0, 30.0,   0.0,   3.0)
    st.cyl_y(p+"govde_D66",       0.0, 0.0, 33.0,   3.0, 112.0)
    st.cyl_y(p+"ust_kapak_D60",   0.0, 0.0, 30.0, 112.0, 115.0)
    st.assemble(ad); print("  %s bbox:" % ad, ["%.1f" % (v/M) for v in st.bb])


if __name__ == "__main__":
    sw.CloseAllDocuments(True)
    if len(sys.argv) > 1 and sys.argv[1] == "kola":
        kola_kutusu_dik(); Station(ORTAK, "x").exit_sw(); raise SystemExit
    ayak_ayar(); mentese_gizli(); mandal_bas_ac(); kola_kutusu_dik()
    Station(ORTAK, "x").exit_sw()
