# -*- coding: utf-8 -*-
"""firin_tp10_cad_v9 → firin_tp10_cad_v10 (29 Eyl 2026) — Kemal: "fırın kapasitesini düşürme; pişirme alanı aynı; içeri alan bant hızlı, sonrası yavaş".
  · ısıtılan oda v8 ile AYNI: ön oda 64 · giriş duvarı 2564–2624 · ISITILAN 2624–3940 = 1316 · aynı anda 4 ürün · ≈14 kW
  · yükleme bandı (2522–2845) giriş duvarının geçidinden ISITILAN bölgenin başına girer (2624–2845 ısıda): kasetten hızlı alır (1,25 s), sonra fırın bandı hızında
    taşır ve fırın bandına (2856'dan, v9 ile aynı) verir → fırın konveyörünün giriş rulosu 2882 (bandın içinde, uç duvarında değil)
  · alt ısıtıcı 1 + braketleri ve kırıntı tepsisi yükleme bandından sonra başlar (bandın alt kolu ile çakışmasın) · üst ısıtıcı tam boy
  · yükleme bandı ayakları: ön odada gövde tabanına (x 2530–2550) + tünelde tünel tabanına (x 2780–2800) · tahrik mili tünel kaplaması + yalıtımdan
    teknik bölmeye geçer (delik), ön ucu çerçevede biter
  · yükleme bandı ısıda: PTFE (260 °C) YETMEZ → paslanmaz ince hatveli düz tel bant (özel sipariş, [V]) — geometri aynı (0,35 → kalınlık yeniden seçilecek)."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "firin_tp10_cad_v9.py"), encoding="utf-8").read()
NL = chr(10)


def d(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


d('ISI0 = BT.YB_TAHRIK[0] + BT.YB_TAHRIK[2] + 67.0  # 2912 · v9: ısıtma yükleme bandının tahrik rulosundan 67 sonra başlar (bantli_tabla_cad_v1 ISI0)',
  'ON_ODA0 = 64.0                                   # v10: v8 ön odası (ısıtılan 1316 korunur · Kemal: kapasite düşmez)')
d('ON_ODA = ISI0 - DUVAR - X_F0                     # 352 · v9 giriş ön odası (ısıtılmaz: yükleme bandı burada · v8: 64)',
  'ON_ODA = ON_ODA0                                 # 64 · v10 (v9: 352)')
d('RULO_X = (X_DUV0 + DUVAR / 2.0, X_F1 - DUVAR / 2.0)   # 2594 · 3970 (uç duvarlarının ortasında)',
  'RULO_X = (round(BT.YB_SON + 10.7 + 26.0), X_F1 - DUVAR / 2.0)   # v10: 2882 (yükleme bandının sonundan 10,7 + sarım 26; ısıtılan bölgenin içinde) · 3970')
# tünel kaplaması + yalıtım: yükleme bandı tahrik mili geçişi
d('    kap = kut(X_TUN0 - 1.0, X_TUN1 + 1.0, TUN_Y[0] - 1.0, TUN_Y[1] + 1.0, TUNEL_Z[0] - 1.0, TUNEL_Z[1] + 1.0) \\',
  '    _ybm = silz(BT.YB_TAHRIK[0], BT.YB_TAHRIK[1], 5.5, -520.0, -80.0)                          # v10: yükleme bandı tahrik mili (yerel z)' + NL +
  '    kap = kut(X_TUN0 - 1.0, X_TUN1 + 1.0, TUN_Y[0] - 1.0, TUN_Y[1] + 1.0, TUNEL_Z[0] - 1.0, TUNEL_Z[1] + 1.0).cut(_ybm).cut(silz(RULO_X[0], RULO_Y, 10.2, -600.0, -40.0)) \\')
d('    yal = kut(X_DUV0, x1 - 1.5, y0 + 1.5, y1 - 1.5, TUNEL_Z[0] - 3.5, -1.5) \\',
  '    yal = kut(X_DUV0, x1 - 1.5, y0 + 1.5, y1 - 1.5, TUNEL_Z[0] - 3.5, -1.5).cut(_ybm) \\')
# alt ısıtıcılar + kırıntı tepsisi yükleme bandından sonra
X_ALT0 = 'max(a, RULO_X[0] + SARIM_R + 5.0)'
d('        ekle("alt_isitici_%d" % (i + 1), kut(a, b, RULO_Y - 12.0, RULO_Y - 4.0,',
  '        ekle("alt_isitici_%d" % (i + 1), kut(' + X_ALT0 + ', b, RULO_Y - 12.0, RULO_Y - 4.0,')
d('        ekle("alt_isitici_braketi_%d_on" % (i + 1), kut(a, b, RULO_Y - 12.0,', '        ekle("alt_isitici_braketi_%d_on" % (i + 1), kut(' + X_ALT0 + ', b, RULO_Y - 12.0,')
d('        ekle("alt_isitici_braketi_%d_arka" % (i + 1), kut(a, b, RULO_Y - 12.0,', '        ekle("alt_isitici_braketi_%d_arka" % (i + 1), kut(' + X_ALT0 + ', b, RULO_Y - 12.0,')
d('    ekle("kirinti_tepsisi", kut(X_TUN0 + 12.0, X_TUN1 - 12.0,', '    ekle("kirinti_tepsisi", kut(max(X_TUN0 + 12.0, RULO_X[0] - SARIM_R + 4.0), X_TUN1 - 12.0,')
# yükleme bandı parçaları: tahrik mili ön ucu çerçevede · ayaklar
d('''        if p_["ad"] == "yb_tahrik_rulosu":                                                      # mil arkaya, teknik bölmeye uzar (GT2 kasnağı orada)
            sh_ = sh_.fuse(cq.Workplane(obj=silz(XT_, YT_, 5.0, -436.0, -330.0).val()).val())''',
  '''        if p_["ad"] == "yb_tahrik_rulosu":                                                      # v10: mil arkada teknik bölmeye (GT2) · önde çerçevede biter (tünelin ön duvarına girmez)
            _zf = BT.ZE + BT.W_B / 2.0 + 12.0
            sh_ = silz(XT_, YT_, RT_, BT.ZE - BT.W_B / 2.0 - 11.5, _zf - 0.5).union(silz(XT_, YT_, 5.0, -436.0, _zf + 5.0)).val()
        if p_["ad"].startswith("yb_ayak_"):                                                     # v10: ön odada gövde tabanına · tünelde tünel tabanına
            _zf0, _zf1 = BT.ZE - BT.W_B / 2.0 - 12.0, BT.ZE + BT.W_B / 2.0 + 12.0
            _xb, _y0 = ((2540.0, YG0 + 1.5) if p_["ad"].endswith("_0") else (2790.0, TUN_Y[0]))
            sh_ = kut(_xb - 10.0, _xb + 10.0, _y0, 962.0, _zf0 - 5.0, _zf1 + 5.0).cut(kut(_xb - 11.0, _xb + 11.0, _y0 + 5.0, 957.0, _zf0, _zf1)).val()''')
d('("F_YUKLEME_BANDI", "Yükleme bandı (bizim · v9) · ısıtılmayan ön odada ·',
  '("F_YUKLEME_BANDI", "Yükleme bandı (bizim · v10) · ön odadan ısıtılan bölgenin başına (2624–2845 ısıda) · kasetten hızlı alır, sonra fırın bandı hızında · paslanmaz ince tel bant (ısıda) ·')
d('"Fırın gövdesi · TP10 kesiti (730 × 517) · boy 1500 ÖZEL SİPARİŞ · v9: giriş ön odası %.0f (yükleme bandı) + uç duvarları 60',
  '"Fırın gövdesi · TP10 kesiti (730 × 517) · boy 1500 ÖZEL SİPARİŞ · v10: giriş ön odası %.0f + uç duvarları 60 (yükleme bandı geçitten ısıtılan bölgenin başına girer)')
s = s.replace('"""', '"""firin_tp10_cad_v10 (29 Eyl 2026): ısıtılan 1316 / 4 ürün korunur · yükleme bandı ısıtılan bölgenin başında (yap_firin_tp10_cad_v10.py).\n', 1)
compile(s, "firin_tp10_cad_v10.py", "exec")
io.open(os.path.join(U, "firin_tp10_cad_v10.py"), "w", encoding="utf-8").write(s)
print("firin_tp10_cad_v10.py yazildi")
