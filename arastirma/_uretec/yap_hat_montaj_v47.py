# -*- coding: utf-8 -*-
"""hat_montaj_v46 → v47: fırının önündeki köşede DIŞARI TAŞAN PARÇALAR içeri alındı (topping_cad_v23) · yer tutucu fırın bandı
TOPPING tahrik makarasının İÇİNDEN başlamıyor · hamur topu tablaya oturuyor (yolculuk_v47) · ön yüz denetimi montajda."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v46.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


degis('"""v46 (26 Eyl 2026):', '"""v47 (26 Eyl 2026): KÖŞEDEKİ ÇIKINTILAR (Kemal: "bize bakan köşesinde çıkıntılar, fırının dışına çıkmış parçalar").\n'
      '  Görsel denetim kaynağı ölçtü: aktarma bandının motoru ön yüzün 78 mm önünde, havada ve 90° ters · ön yan sac + makara uçları\n'
      '  +10 · fire sileceği +10 → topping_cad_v23 ile hepsi z ≤ 0 (motor bandın arkasında, makarayla eş eksenli). Yer tutucu fırın\n'
      '  bandı TOPPING tahrik makarasının 30 mm içinden başlıyordu → makaranın 3,5 mm sonrasından. Hamur topu tablada 5,7 mm havada\n'
      '  duruyordu → oturur (yolculuk_v47). Montaj artık ön yüzü denetler. Açıcı kafası (+167/+180) BİLİNEN açık konu, dokunulmadı.\n'
      'v46 (26 Eyl 2026):')
degis('import topping_hesap_v6 as TH, topping_cad_v22 as TC ', 'import topping_hesap_v6 as TH, topping_cad_v23 as TC ')
degis('BANT_X0 = X_BC + 2195.0 ', 'BANT_X0 = X_BC + 2195.0 + 35.0 ')   # v47: tahrik makarası Ø60 + bant 1,5 + 3,5 boşluk
degis('"sac", "topping_uno_cad_v5.py + topping_cad_v22.py", "hat/topping_v2.html")', '"sac", "topping_uno_cad_v5.py + topping_cad_v23.py", "hat/topping_v2.html")')
degis('    print("ANA MONTAJ ANIMASYONU (v46):', '    print("ANA MONTAJ ANIMASYONU (v47):')
degis('    b1 = glb_yaz(os.path.join(OUT, "hat_v46.glb")', '    b1 = glb_yaz(os.path.join(OUT, "hat_v47.glb")')
degis('    print("hat_v46.glb · %d dugum', '''    # v47 · ÖN YÜZ DENETİMİ: sabit makine düğümleri makinenin ön yüzünü (z 0) geçemez. İstisna: açıcı kafası (bilinen açık
    # konu), koridordaki robot + ray, QR dolabı, çekmeceler (açılır) ve ürün (taşınır).
    _IST = ("ROBOT", "QR", "CEK_", "URUN__", "TOPPING_DONER__KONI")
    # İşlevsel dış elemanlar (ölçülü izin; fazlası yakalanır): K kapı menteşeleri 20 × 140 × 22 · K acil stop Ø32 × 16 · E kapı kulpu 70 × 18 × 18
    _IZIN = {"K_GOVDE__celik": 22.5, "K_GOVDE__kirmizi": 16.5, "E_GOVDE__celik": 18.5}
    _on = []
    for a_, m_, _x in parcalar:
        if a_.startswith(_IST) or "__ACICI" in a_ or a_ in HARIC_T or not m_.P:
            continue
        zm = max(q[2] for q in m_.P) / MM
        if zm > _IZIN.get(a_, 0.5):
            _on.append((round(zm, 1), a_))
    print("   izinli dis elemanlar (islevsel): K kapi mentesesi +22 · K acil stop +16 · E kapi kulpu +18 · acici kafasi +180 (acik konu)")
    print("ON YUZ DENETIMI (z <= 0,5 mm; acici kafasi haric): %s" % ("GECTI" if not _on else "TASAN: %s" % sorted(_on, reverse=True)[:10]))
    assert not _on, "makinenin on yuzunden tasan parca var"
    print("hat_v47.glb · %d dugum''')
degis('usdz_yaz([os.path.join(OUT, "hat_v46.usdz")], "hat_v46", _usd + E_USDZ, dokular)', 'usdz_yaz([os.path.join(OUT, "hat_v47.usdz")], "hat_v47", _usd + E_USDZ, dokular)')
degis('print("hat_v46.usdz · %.0f KB', 'print("hat_v47.usdz · %.0f KB')
degis('pafta="HAT_ATOSA_TABLALI v12 · v46 (animasyon duzeltmesi, geometri v45 ile ayni) ·',
      'pafta="HAT_ATOSA_TABLALI v12 · v47 (on yuzden tasan parcalar iceri, animasyon v46 duzeltmesi) ·')
# yolculuk gövdesi v46 → v47 (montajın içine gömülü kopya birebir değiştirilir)
yv46 = io.open(os.path.join(U, "yolculuk_v46.py"), encoding="utf-8").read()
yv47 = io.open(os.path.join(U, "yolculuk_v47.py"), encoding="utf-8").read()
assert s.count(yv46) == 1, "hat_montaj_v46 icindeki yolculuk govdesi yolculuk_v46.py ile birebir degil"
s = s.replace(yv46, yv47)
io.open(os.path.join(U, "hat_montaj_v47.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v47.py yazildi")
