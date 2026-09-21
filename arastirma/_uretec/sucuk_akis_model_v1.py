# -*- coding: utf-8 -*-
"""AUTOKITCH · KÜP SUCUK AKIŞ MODELİ v1 (22 Eyl 2026) — Kemal: "sucuk için de küp sucuk kullanalım, ona da hazne yap, ortak olursa ne güzel;
ama tüm matematiği yeniden kur." → GÖVDE, VİDA, TÜP, ROTOR kuşbaşı kasetiyle BİREBİR AYNI; yeniden kurulan şey HESAP: ürün sabitleri başka.
KAYNAKLI: porsiyon 70 g (sucuklu pide = 90 g kaşar + 70 g sucuk; tedarikçi yazışması) · 20 pide/gün → 1,4 kg/gün → 2 gün 2,8 kg
          pizzalık küp pepperoni 5–10 mm (MIL-DTL-32541) · Hormel küp pepperoni 1/4" = 6,35 mm
VARSAYIM (ölçülecek): küp 8 mm · katı yoğunluk 1,00 · dökme 0,60 g/mL (sert küp gevşek istiflenir) · duvar sürtünmesi 0,25 (yağlı yüzey) · doluluk 0,60
Taban model kusbasi_akis_model_v2.py'nin AYRI BİR KOPYASI olarak yüklenir (kuşbaşı modeliyle aynı süreçte çakışmasın diye)."""
import importlib.util, math, os
_y = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kusbasi_akis_model_v2.py")
_s = importlib.util.spec_from_file_location("_sucuk_taban", _y); M = importlib.util.module_from_spec(_s); _s.loader.exec_module(M)
M.URUN, M.JSON_ADI = "KUP SUCUK", "sucuk_model.json"
M.PORS, M.KG2 = 70.0, 2.8
M.RHO_KATI, M.RHO_DOKME = 1.00, 0.60
M.MU = 0.25; M.FI_S = math.degrees(math.atan(M.MU))
M.D_NOM, M.D_ARALIK = 8.0, (6.0, 8.0, 10.0, 12.0, 15.0)
PORS, KG2, RHO_DOKME, G = M.PORS, M.KG2, M.RHO_DOKME, M.G
kapasite, kup, r_t_k, tabla_tur, dagilim, D_NOM = M.kapasite, M.kup, M.r_t_k, M.tabla_tur, M.dagilim, M.D_NOM
if __name__ == "__main__":
    M.calistir()
