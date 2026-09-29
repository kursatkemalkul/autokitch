# -*- coding: utf-8 -*-
"""firin_tp10_cad_v8 → firin_tp10_cad_v9 (29 Eyl 2026) — BANTLI TABLA ANA MONTAJA (bantli_tabla_hesap_v1 ayar b · B kavramı):
  · YÜKLEME BANDI (bantli_tabla_cad_v1 bölüm 5, PTFE 296 · Ø12 burun 2528 · Ø30 tahrik 2830) eski giriş bandının yerine, ısıtılmayan ön odada
    → ön oda 64 → 352 (giriş duvarı 2852–2912) · ısıtılan 2912–3940 = 1028 (aynı anda 3 ürün; v8: 1316 / 4) · güç föyle ölçekli ≈10,9 kW VARSAYIM
  · yükleme bandı tahriki: STP-MTR-23079 (gerçek STEP) teknik bölmede, GT2 1:1, mil teknik bölme duvarından geçer (v8 giriş bandı düzeninin aynısı)
  · ön kabuk giriş ağzının alt kenarı 984 → 965 (rotor kabı sucukta dönerken 970'e iner) · YARIK_V2 = topping_cad_v27
  · konveyör / yalıtım / ısıtıcılar / ray braketleri / gergi yeni ön odaya göre (giriş rulosu 2882)
Gövde dış ölçüsü, çıkış, raf, kalkan, arka yüz v8 ile aynı."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "firin_tp10_cad_v8.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('from kaset_3d_v3 import Mesh, MM, MALZEME',
      'from kaset_3d_v3 import Mesh, MM, MALZEME' + NL + 'import bantli_tabla_montaj_v1 as BT                                   # v9: yükleme bandı + kaset burnu (tek kaynak bantli_tabla_cad_v1)')
degis('ON_ODA, DUVAR = 64.0, 60.0                       # giriş ön odası (ısıtılmaz) · uç duvarı (yalıtım + rulo içinde)',
      'DUVAR = 60.0                                     # uç duvarı (yalıtım + rulo içinde)' + NL +
      'ISI0 = BT.YB_TAHRIK[0] + BT.YB_TAHRIK[2] + 67.0  # 2912 · v9: ısıtma yükleme bandının tahrik rulosundan 67 sonra başlar (bantli_tabla_cad_v1 ISI0)' + NL +
      'ON_ODA = ISI0 - DUVAR - X_F0                     # 352 · v9 giriş ön odası (ısıtılmaz: yükleme bandı burada · v8: 64)')
degis('X_DISK_KENAR = 2507.0                            # TOPPING tabla aktarma konumunda disk kenarı (700 + 1637 + 170)',
      'X_DISK_KENAR = BT.AKT + BT.H.X_UC                # 2518,9 · v9: kaset burnu aktarmada (yükleme bandı burnuna 3) · v8: disk kenarı 2507')
degis('GB_RY = BANT_UST_HAT - 1.5 - 10.0                # 986,5 giriş bandı rulo ekseni',
      'YB_BURUN, YB_TAHRIK, YB_SON = BT.YB_BURUN, BT.YB_TAHRIK, BT.YB_SON   # v9 yükleme bandı (x, y, r) · sağ ucu 2845,3' + NL +
      'GB_RY = YB_BURUN[1]                              # v9 uyumluluk: yükleme bandı burun ekseni')
degis('GB_XB = X_DISK_KENAR + 2.0 + 1.5 + 10.0          # 2520,5 burun (disk kenarına 2)', 'GB_XB = YB_BURUN[0]                              # v9: yükleme bandı burnu')
degis('GB_XT = BANT_X[0] - 2.5 - 1.5 - 10.0             # 2554 tahrik (fırın bandı ucuna 2,5)', 'GB_XT = YB_TAHRIK[0]                             # v9: yükleme bandı tahriki')
degis('GB_MOTOR = (2530.0, BANT_UST_HAT + 124.0, -431.0)   # 1122 (v6 1290) · NEMA23 (mil yüzü z) · ağzın üstünde, ön odanın içinde · v7: bant kotuna bağlı',
      'GB_MOTOR = (YB_TAHRIK[0] - 50.0, BANT_UST_HAT + 124.0, -431.0)   # v9: yükleme bandı motoru teknik bölmede, tahrik rulosunun sol üstünde (GT2 1:1; fırın bandı gergisi 2844–2864 boş kalır)')
degis('YARIK_V2 = ((2492.0, 2498.5, DISK_UST - 23.0, DISK_UST + 42.0, -417.0, -5.0), (2491.0, 2499.5, DISK_UST - 13.0, DISK_UST + 38.0, -409.0, -13.0))',
      'YARIK_V2 = ((2492.0, 2498.5, BT.H.AGIZ_YENI_ALT - 10.0, DISK_UST + 42.0, -417.0, 0.0), (2491.0, 2499.5, BT.H.AGIZ_YENI_ALT, DISK_UST + 38.0, -409.0, -8.0))   # v9 = topping_cad_v27 (alt 965 · ön −8)')
# ağız alt kenarı 984 → 965
degis('    kab = kab.cut(kut(x0 - 1.0, x0 + 2.0, DISK_UST - 16.0, DISK_UST + 42.0, -341.0 - ZS, -10.0 - ZS))',
      '    kab = kab.cut(kut(x0 - 1.0, x0 + 2.0, BT.H.AGIZ_YENI_ALT, DISK_UST + 42.0, -341.0 - ZS, -10.0 - ZS))   # v9: alt 984 → 965 (kaset rotor kabı)')
# teknik bölme duvarı: giriş bandı motoru penceresi yerine yükleme bandı tahrik mili deliği
degis('        .cut(kut(GB_MOTOR[0] - 33.0, GB_MOTOR[0] + 33.0, GB_MOTOR[1] - 33.0, GB_MOTOR[1] + 33.0, TUNEL_Z[0] - 7.0, TUNEL_Z[0] - 2.0))   # giriş bandı motoru penceresi',
      '        .cut(silz(YB_TAHRIK[0], YB_TAHRIK[1], 5.5, TUNEL_Z[0] - 7.0, TUNEL_Z[0] - 2.0))   # v9: yükleme bandı tahrik mili geçişi (v8: giriş bandı motoru penceresi)')
# gergi konsolu + vida: giriş rulosuna bağlı (v8'de x 2556 sabit yazılıydı)
degis('ekle("gergi_konsolu", kut(2556.0, 2560.0,', 'ekle("gergi_konsolu", kut(RULO_X[0] - 38.0, RULO_X[0] - 34.0,')
degis('ekle("gergi_vidasi", silx(RULO_Y, -510.0, 4.0, 2560.0, RULO_X[0] - 18.0)', 'ekle("gergi_vidasi", silx(RULO_Y, -510.0, 4.0, RULO_X[0] - 34.0, RULO_X[0] - 18.0)')
# ray braketleri yeni ray boyunda (ray 2876–3976)
degis('    for i, xb in enumerate((2700.0, 3000.0, 3300.0, 3600.0, 3900.0)):',
      '    for i, xb in enumerate((2960.0, 3200.0, 3440.0, 3680.0, 3900.0)):                        # v9: ray 2876–3976 (v8: 2700…3900)')
# 3.1 giriş bandı → yükleme bandı
a0 = s.index('    # ---- 3.1 GİRİŞ BANDI')
a1 = s.index('    # ---- 3.2 ÇIKIŞ ÖLÜ PLAKASI')
YENI = '''    # ---- 3.1 v9 · YÜKLEME BANDI (bantli_tabla_cad_v1 bölüm 5 · DÜNYA, KAYMAZ): kaset burnu 2518,9 → yükleme bandı 2522 → fırın bandı 2856 · PTFE 296 · eksen −170 ----
    YB_ = "F_YUKLEME_BANDI"
    XT_, YT_, RT_ = YB_TAHRIK
    for p_ in BT.YB:
        sh_ = p_["sh"]
        if p_["ad"] == "yb_tahrik_rulosu":                                                      # mil arkaya, teknik bölmeye uzar (GT2 kasnağı orada)
            sh_ = sh_.fuse(cq.Workplane(obj=silz(XT_, YT_, 5.0, -436.0, -330.0).val()).val())
        g_ = {"yb_burun_rulosu": "RULO_GB_BURUN", "yb_tahrik_rulosu": "RULO_GB_TAHRIK"}.get(p_["ad"], "SABIT")
        ekle(p_["ad"], cq.Workplane(obj=sh_), {"celik": "celik", "ptfe_bant": "ptfe_bant"}.get(p_["mal"], p_["mal"]), YB_, grup=g_,
             kaynak="bantli_tabla_cad_v1 bölüm 5", bom=p_["bom"])
    MX, MY, MZF = GB_MOTOR
    if nema23 is not None:
        ekle("yb_motoru", cq.Workplane(obj=nema23.translate(cq.Vector(MX, MY, MZF))), "motor", YB_, kaynak="STP-MTR-23079 GERÇEK CAD",
             bom=("Yükleme bandı motoru · NEMA23 STP-MTR-23079", 1, "1,95 N·m kapalı çevrim · teknik bölmede", "GT2 1:1 · aktarmada kaset bandıyla eş hız, sonra fırın bandı hızı"))
    ekle("yb_motor_plakasi", kut(MX - 31.0, XT_ + 12.0, YT_ - 17.5, MY + 32.0, MZF, MZF + 3.0).cut(silz(MX, MY, 20.0, MZF - 1, MZF + 4)).cut(silz(XT_, YT_, 5.5, MZF - 1, MZF + 4)),
         "sac", YB_, bom=("Yükleme bandı motor plakası 3 mm", 1, "304 lazer", "teknik bölme duvarına 2 takozla (arka yüz)"))
    for i_, xa_ in enumerate((MX - 31.0, MX + 21.0)):
        ekle("yb_motor_takozu_%d" % i_, kut(xa_, xa_ + 10.0, YT_ - 17.0, YT_ - 7.0, MZF + 3.0, TUNEL_Z_D[0] - 5.5), "sac", YB_,
             bom=("Motor plakası takozu 10 × 10", 2, "304", "plaka → teknik bölme duvarı (M5)") if i_ == 0 else None)
    ekle("yb_kasnak_rulo", silz(XT_, YT_, 7.5, MZF + 3.0, MZF + 11.0).cut(silz(XT_, YT_, 5.0, MZF + 2.0, MZF + 12.0)), "aluminyum", YB_, grup="RULO_GB_TAHRIK",
         bom=("GT2 kasnak 24 diş Ø15", 2, "alüminyum · sıkma bilezikli", "tahrik rulosu mili + motor mili"))
    ekle("yb_kasnak_motor", silz(MX, MY, 7.5, MZF + 3.0, MZF + 11.0), "aluminyum", YB_)
    L_ = math.hypot(MX - XT_, MY - YT_); a_ = math.degrees(math.atan2(MY - YT_, MX - XT_))
    kay = cq.Workplane("XY", origin=((XT_ + MX) / 2.0, (YT_ + MY) / 2.0, MZF + 3.0)).slot2D(L_ + 17.0, 17.0, a_).extrude(8.0)
    kay = kay.cut(cq.Workplane("XY", origin=((XT_ + MX) / 2.0, (YT_ + MY) / 2.0, MZF + 2.0)).slot2D(L_ + 15.0, 15.0, a_).extrude(10.0))
    ekle("yb_gt2_kayis", kay, "koyu", YB_, bom=("GT2 kayış 6 mm kapalı", 1, "kauçuk", "1:1 · teknik bölmede"))
'''
s = s[:a0] + YENI + s[a1:]
degis('    ("F_GIRIS_BANDI", "Giriş bandı (bizim) · ön odada · disk kenarı 2507 → fırın bandı 2568 · Ø20 burun + tahrik · NEMA23 + GT2 · PTFE 320 · eksen −170 (v5) · F\'ye köprü braketleriyle"),',
      '    ("F_YUKLEME_BANDI", "Yükleme bandı (bizim · v9) · ısıtılmayan ön odada · kaset burnu 2518,9 → bant 2522–2845 → fırın bandı 2856 · Ø12 burun + Ø30 tahrik · PTFE 296 · eksen −170 · NEMA23 + GT2 teknik bölmede · ayakları gövde tabanına"),')
degis('("F_TP10_GOVDE", "Fırın gövdesi · TP10 kesiti (730 × 517) · boy 1500 ÖZEL SİPARİŞ · giriş ön odası 64 + uç duvarları 60 · ısıtılan 1316 · IR üst + alt 2 bölge',
      '("F_TP10_GOVDE", "Fırın gövdesi · TP10 kesiti (730 × 517) · boy 1500 ÖZEL SİPARİŞ · v9: giriş ön odası %.0f (yükleme bandı) + uç duvarları 60 · ısıtılan %.0f (%d ürün) · IR üst + alt 2 bölge" % (ON_ODA, ODA, N_URUN) + "')
s = s.replace('"""', '"""firin_tp10_cad_v9 (29 Eyl 2026): BANTLI TABLA — yükleme bandı ön odada (352), ısıtılan 1028, ağız alt 965 (yap_firin_tp10_cad_v9.py).\n', 1)
compile(s, "firin_tp10_cad_v9.py", "exec")
io.open(os.path.join(U, "firin_tp10_cad_v9.py"), "w", encoding="utf-8").write(s)
print("firin_tp10_cad_v9.py yazildi · %d satir" % s.count(NL))
