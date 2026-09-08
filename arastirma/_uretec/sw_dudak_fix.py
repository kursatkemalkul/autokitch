# -*- coding: utf-8 -*-
# DÜZELTME: kabın ön çekme dudağı yukarı taşıyordu (kat 1'de 1985 > 1970). v27: dudak ÖNE çıkar (kap 68 + 1,5 = 69,5 ≤ STORE 70).
# KAP ve KAP_YAG alt montajlarındaki dudak parçası yeniden üretilir; TOPPING · OVEN · HAT montajları yenilenir.
import os, io, sys
from sw_lib import *
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
HEDEF = [(os.path.join(ARA, "3_TOPPING", "alt_montaj", "KAP_14x68x24"), "KAP_14x68x24", "KAP_"),
         (os.path.join(ARA, "_ortak", "KAP_YAG_14x68x24"), "KAP_YAG_14x68x24", "KAPYAG_")]

if __name__ == "__main__":
    # 1) kaynak scriptlerdeki dudak satırlarını kalıcı düzelt
    for f in ("sw_topping2.py", "sw_oven2.py"):
        s = io.open(f, encoding="utf-8").read()
        s2 = s.replace('"on_cekme_dudagi", -70, 70, yt, yt+15, -35, -20', '"on_cekme_dudagi", -70, 70, yt-15, yt, -20, -5')
        if s2 != s: io.open(f, "w", encoding="utf-8").write(s2); print("duzeltildi:", f)
    # 2) alt montajlardaki dudak parçasını yeniden üret + montajı yenile
    sw.CloseAllDocuments(True)
    for kok, ad, p in HEDEF:
        st = Station(kok, ad); yt = 260
        eski = os.path.join(st.pdir, p + "on_cekme_dudagi.SLDPRT")
        if os.path.exists(eski): os.remove(eski)
        st.box(p + "on_cekme_dudagi", -70, 70, yt-15, yt, -20, -5)     # üstte değil, ÖNDE (z −20 → −5)
        st.load_dir(); st.assemble(ad)
