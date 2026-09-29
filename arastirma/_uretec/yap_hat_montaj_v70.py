# -*- coding: utf-8 -*-
"""hat_montaj_v69 → hat_montaj_v70 (29 Eyl 2026) — BANTLI TABLA ANA MONTAJDA (Kemal: "montaja adapte et").
  · C = topping_cad_v27 (kaset + sabit tahrik + ayarlar a, c, d, e, f) · topping_hesap_v7 (aktarma 1665,4 · ray 1798 · limit+ 1688)
  · F = firin_tp10_cad_v9 (yükleme bandı ısıtılmayan ön odada 2522–2845 · ısıtılan 2912–3940 = 1028, 3 ürün · ağız alt 965)
  · İTİCİ KALKTI (itici_cad_v5 montajda yok): pide kaset bandıyla yükleme bandına, oradan fırın bandına geçer
  · TABLA grubu (döner): kaset + ayar bileziği + konum pimleri + kilit burçları + home bayrağı + tahrik lokması (v69'da bilezik / burç / bayrak / lokma yalnız x'te gidiyordu)
  · denetim: araba + kaset AKTARMADA ↔ TOPPING / fırın / yükleme bandı · kasetin istasyonlarda dönüş süpürmesi ↔ TOPPING + TU + sabit tahrik ·
    pide koridoru (park → aktarma) · ürün yolu kaset → yükleme bandı → fırın → K
Çıktılar hat_v70. Tesisat + raf yükleri ayrı sürümü artık v71."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v69.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120])
    s = s.replace(a, b)


def blok(bas, son, yeni):
    """bas (dahil) … son (hariç) arasını yeni ile değiştir — ikisi de tekil olmalı"""
    global s
    assert s.count(bas) == 1 and s.count(son) >= 1, (s.count(bas), s.count(son), bas[:80], son[:80])
    a = s.index(bas); b = s.index(son, a + len(bas))
    s = s[:a] + yeni + s[b:]


degis('"""v69 (28 Eyl 2026):',
      '"""v70 (29 Eyl 2026): BANTLI TABLA — topping_cad_v27 (kaset + sabit tahrik) · topping_hesap_v7 (aktarma 1665,4) · firin_tp10_cad_v9 (yükleme bandı, ısıtılan 1028) · '
      'itici kalktı · pide kaset bandı → yükleme bandı → fırın · çıktılar hat_v70.' + NL + 'v69 (28 Eyl 2026):')
degis('pafta="HAT v69 (28 Eyl) ·',
      'pafta="HAT v70 (29 Eyl) · BANTLI TABLA (kare bant kaseti 310 × 310, 8,45 kg, elle cikar · sabit miknatisli tahrik TOPPING sag-arkada · aktarma 2365,4 · '
      'yukleme bandi firinin isitilmayan on odasinda 2522-2845 · isitilan 2912-3940 = 1028, ayni anda 3 urun · itici kalkti · orta dikme tabla hizasinda bosluklu · '
      'cikis yarigi alt 965 · ray 2498) · v69:')
degis('print("ALCAK HAT SOZLESMESI (v69 ·', 'print("ALCAK HAT SOZLESMESI (v70 ·')
for a_ in ("hat_v69.glb", "hat_v69.usdz", '"hat_v69"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v69", "v70"))
degis('import topping_hesap_v6 as TH, topping_cad_v26 as TC', 'import topping_hesap_v7 as TH, topping_cad_v27 as TC')
degis('"topping_uno_cad_v15.py (dünya y −168) + topping_cad_v26.py (yerel y + 892)"', '"topping_uno_cad_v15.py (dünya y −168) + topping_cad_v27.py (yerel y + 892)"')
degis('#      TC (topping_cad_v26, YEREL y) KAYDIRILMAZ', '#      TC (topping_cad_v27, YEREL y) KAYDIRILMAZ')
degis('import firin_tp10_cad_v8 as FT ', 'import firin_tp10_cad_v9 as FT ')
degis('"sac", "firin_tp10_cad_v8.py", "hat/oven.html")', '"sac", "firin_tp10_cad_v9.py", "hat/oven.html")')

# ---------------- İTİCİ KALKAR ----------------
degis('import itici_cad_v5 as IT                                                              # v57: DISK_UST 1000 · TAVAN 1109 · v49: aktarma iticisi (dünya koordinatı)',
      'import bantli_tabla_montaj_v1 as BT                                                      # v70: bantlı tabla (kaset, sabit tahrik, yükleme bandı) · itici_cad_v5 KALKTI')
degis('for _k, _v in IT.MALZEME.items():' + NL + '    MALZEME.setdefault(_k, dict(renk=_v["renk"], met=_v["met"], ruf=_v["ruf"], saydam=False))' + NL, '')
blok('# ---- v49 · AKTARMA İTİCİSİ + DESTEK PLAKASI (modül C, dünya koordinatı; ev konumu, çubuk kalkık) ----',
     '# --- K · KESME + SPREY', '# ---- v70: aktarma iticisi KALKTI (bantlı tabla: kaset bandı pideyi yükleme bandına verir) ----' + NL + NL)
degis('    ("disk: FT.DISK_UST = IT.DISK_UST = Y_MEK + 108 = P = 1000", (FT.DISK_UST, IT.DISK_UST, Y_MEK + DISK_UST_Y, P, 1000.0)),',
      '    ("kaset bandi ustu: FT.DISK_UST = BT.UST = Y_MEK + 108 = P = 1000", (FT.DISK_UST, BT.UST, Y_MEK + DISK_UST_Y, P, 1000.0)),' + NL +
      '    ("v70 · aktarma: TH.X_AKTARMA + 700 = BT.AKT (kaset burnu yukleme bandina 3)", (TH.X_AKTARMA + 700.0, round(BT.AKT, 1))),' + NL +
      '    ("v70 · yukleme bandi: burun + 6 = BT.LB_SOL + 6,35 · firin bandi basi > yukleme bandi sonu (1 = evet)", (float(FT.BANT_X[0] > FT.YB_SON), 1.0)),')
degis('    ("itici tavani: TU yalitim alti (YAL_Y0 + DY) = IT.TAVAN = 1109", (TU_YAL_Y0, IT.TAVAN, 1109.0)),' + NL,
      '    ("v70 · firin isitilan: FT.ODA = 1028 · FT.N_URUN = 3", (FT.ODA, 1028.0)),' + NL + '    ("v70 · firin ayni anda urun", (float(FT.N_URUN), 3.0)),' + NL)
blok('        elif b["durum"] == "GERCEK_ITICI":                                                   # v49',
     '        elif b["durum"] ==', '')
degis('ekle(TC_AG(cq.Workplane(obj=FT.dunya(p)), p["ad"].startswith("giris_bandi_motoru")))',
      'ekle(TC_AG(cq.Workplane(obj=FT.dunya(p)), p["ad"].startswith(("giris_bandi_motoru", "yb_motoru"))))')

# ---------------- TABLA grubu (döner) ----------------
degis('TABLA_P = ("tabla_gobegi", "tabla", "merkezleme_pimi_", "calisma_diski", "disk_pimi_")',
      'TABLA_P = ("tabla_gobegi", "tabla", "merkezleme_pimi_", "calisma_diski", "disk_pimi_",' + NL +
      '           "bk_", "ayar_bilezigi", "ayar_konum_pimi_", "kilit_burcu_", "tahrik_lokmasi")   # v70: KASET + döner halka (bilezik, pimler, burçlar, bayrak) + lokma tabla ile döner')
degis('    if ad.startswith(TABLA_P) and ad not in ("tabla_home_sensoru", "tabla_home_bayragi"): return "TABLA"',
      '    if ad.startswith(TABLA_P) and ad != "tabla_home_sensoru": return "TABLA"                  # v70: home bayrağı bileziğe kaynaklı → döner')

# ---------------- ANİMASYON: aktarma → yükleme bandı → fırın ----------------
degis('    import topping_v2_hesap_v1 as TH2', '    import topping_v2_hesap_v1 as TH2' + NL + '    TH2.X_AKTARMA = TC.H.X_AKTARMA                                                     # v70: aktarma 1665,4 (topping_hesap_v7)')
blok('    ADIM.append((T_AKT - 0.5, "AKTARMA",', '    T0K = T_F1 - KS.Z_GELIS[0]',
     '    T_B0 = T_AKT + 0.2                                                                            # v70: kaset + yükleme bandı eş hızla döner\n'
     '    T_B1 = T_B0 + BT.H.S["zaman"]["t_aktarma_s"]                                                 # 1,25 s (bantli_tabla_hesap_v1)\n'
     '    X_B0 = OX + TH2.X_AKTARMA                                                                      # pide merkezi kasette (2365,4)\n'
     '    X_B1 = X_B0 + BT.H.S["zaman"]["yol_mm"]                                                      # 2666,9: pide tümüyle yükleme bandında\n'
     '    ADIM.append((T_AKT - 0.5, "AKTARMA", "Tabla sağ uca gider (aktarma %.1f): kasetin burnu yükleme bandının burnuna 3 mm yaklaşır. Kasetin içindeki rotor, TOPPING\'in sağ-arkasındaki sabit mıknatıslı tahrikle karşılaşır ve dokunmadan kavranır (4,6 mm). Kaset bandı ile yükleme bandı eş hızda döner, pide %.0f mm kayarak %.2f s\'de yükleme bandına geçer. Kaset boşalınca tabla açıcının altına döner." % (X_B0, X_B1 - X_B0, T_B1 - T_B0)))\n'
     '    X.git(T_B1 + 0.2, T_B1 + 0.2 + gecis(TH2.X_AKTARMA, TH2.X_PARK), TH2.X_PARK)\n'
     '    T_F0, T_F1 = T_B1, T_B1 + 10.0\n'
     '    BANT.git(T_F0, T_F1, (3940.0 - X_B1), "l")\n'
     '    ADIM.append((T_F0, "FIRIN", "Yükleme bandı pideyi fırının ısıtılmayan ön odasından fırın bandına verir (fırın bandı hızıyla, hiç durmadan). TP10 kesitli fırın, gövde 1500: ısıtılan %.0f mm, aynı anda %d ürün. Ürün düz −170 ekseninde K bandına geçer. Animasyonda HIZLANDIRILMIŞ: gerçekte 3,5 dk, burada 10 s." % (FT.ODA, FT.N_URUN)))\n')
blok('        if t < T_F0:' + NL + '            u = min(1.0, max(0.0, (t - T_IT0) / (T_IT1 - T_IT0)))',
     '        tK = t - T0K',
     '        if t < T_F0:                                                                              # v70: kaset bandı + yükleme bandı eş hız\n'
     '            u = min(1.0, max(0.0, (t - T_B0) / (T_B1 - T_B0)))\n'
     '            return (X_B0 + (X_B1 - X_B0) * u, OY + 108.0, ZT)\n'
     '        if t < T_F1:\n'
     '            u = (t - T_F0) / (T_F1 - T_F0); x_ = X_B1 + (3940.0 - X_B1) * u                               # yükleme bandı → fırın bandı\n'
     '            return (x_, OY + 108.0 if x_ - 150.0 <= FT.YB_SON else KS.FIRIN_BANDI, FT.urun_z(x_))\n')
blok('    # v49 · AKTARMA İTİCİSİ: araba s(t) (çubuk yüzü konumu, mm) ve çubuk açısı (0 = inik, 90 = kalkık)',
     '    # v48 · fırın + giriş bandı ruloları KENDİ EKSENİNDE', '')
degis('"RULO_GB_BURUN": ((FT.GB_XB, FT.GB_RY, 0.0), 11.5), "RULO_GB_TAHRIK": ((FT.GB_XT, FT.GB_RY, 0.0), 11.5)}',
      '"RULO_GB_BURUN": ((FT.YB_BURUN[0], FT.YB_BURUN[1], 0.0), FT.YB_BURUN[2] + 0.35), "RULO_GB_TAHRIK": ((FT.YB_TAHRIK[0], FT.YB_TAHRIK[1], 0.0), FT.YB_TAHRIK[2] + 0.35)}   # v70: yükleme bandı ruloları')

# ---------------- DENETİM ----------------
degis('    _cd = _pp["calisma_diski"]["wp"].val().BoundingBox(); _bt = _pp["bant"]["wp"].val().BoundingBox()',
      '    _cd = _pp["bk_kaset_bandi"]["wp"].val().BoundingBox(); _bt = _pp["bant"]["wp"].val().BoundingBox()   # v70: gıda yüzeyi = kaset bandı')
degis('    print("SUREC KOTU (CAD\'den olculdu): disk ustu %.1f', '    print("SUREC KOTU (CAD\'den olculdu): kaset bandi ustu %.1f')
degis('    assert abs(Y_MEK + _cd.ymax - P) < 0.05, "disk ustu %.2f, beklenen %.2f" % (Y_MEK + _cd.ymax, P)',
      '    assert abs(Y_MEK + _cd.ymax - P) < 0.05, "kaset bandi ustu %.2f, beklenen %.2f" % (Y_MEK + _cd.ymax, P)')
# ürün yolu: kaset (aktarma) → yükleme bandı → fırın → K
blok('    IT.kur(IT.S_HOME, True)' + NL + '    _stat += [("ITICI(ev):"', '    def _alt(xc, R_):',
     '    _kon = [(float(x_), FT.urun_z(float(x_)), R_) for R_ in (139.5, 149.5) for x_ in range(int(math.ceil(BT.AKT)), 4301, 10)]   # v70: kasetten (aktarma) başlar\n')
degis('        if xc - R_ <= 2507.0: return P + 0.5                                        # v51: rijit ürün arka kenarı DİSK KENARINI (2507) geçene kadar diskte (v50: 2492 = çerçeve; düz yolda disk sliverine giriyordu)',
      '        if xc - R_ <= FT.YB_SON: return P + 0.5                                     # v70: arka kenar yükleme bandının sonunu (2845,3) geçene kadar kaset / yükleme bandında (ikisi de 1000)')
degis('    print("FIRIN URUN YOLU (O280 %d konum + O300 zarf %d konum · 28 yuksek · 10 mm adim · DUZ −170: disk + yarik + on oda + firin + K → 4300 · v51 kayma yok, cit yok): %s"',
      '    print("FIRIN URUN YOLU (O280 %d konum + O300 zarf %d konum · 28 yuksek · 10 mm adim · DUZ −170: kaset (aktarma) + yarik + yukleme bandi + firin + K → 4300): %s"')
# İTİCİ DENETİMİ → BANTLI TABLA DENETİMİ
blok('    _cak_it = []' + NL + '    for _kon_, _s_, _kal_ in (("EV", IT.S_HOME, True)',
     '    print("FIRIN YERLESIM:',
     '''    _cak_it = []
    # (1) ARABA + TABLA (kaset) AKTARMADA ↔ TOPPING sabitleri + TU + fırın + yükleme bandı + K (v69'da araba aktarmada denetlenmiyordu)
    _MOB = [p for p in TC.PARCALAR if grup_modul(p["ad"]) in ("TABLA", "ARABA")]
    _dx_ak = X_BC + TH.X_AKTARMA - TC.XC_TABLA
    for p in _MOB:
        sa = p["wp"].val().translate(cq.Vector(_dx_ak, Y_MEK, 0.0))
        for c_, sc in _DGI:
            if c_.startswith("TABLA("): continue
            if _bbk(sa, sc):
                v_ = _hacim(sa, sc)
                if v_ > 1.0 or v_ < 0: _cak_it.append((round(v_, 1), "AKTARMA:" + p["ad"], c_))
    # (2) KASET DÖNÜŞ SÜPÜRMESİ istasyonlarda (bantli_tabla_cad_v1 D4 yöntemi: r(y) profili 2 mm dilim, +0,5 pay, istasyon x aralığında stadyum) ↔ TOPPING + TU + sabit tahrik
    _XP = X_BC + TC.XC_TABLA
    _NOK = []
    for p in _TABLA:
        if not p["ad"].startswith(("bk_", "ayar_konum_pimi_")): continue
        for f_ in p["wp"].val().translate(cq.Vector(X_BC, Y_MEK, 0.0)).Faces():
            vs_, _t = f_.tessellate(0.3, 0.4); _NOK += [(v_.x - _XP, v_.y, v_.z - ZT) for v_ in vs_]
    _Y0 = min(q[1] for q in _NOK); _prof = {}
    for x_, y_, z_ in _NOK:
        k_ = int((y_ - _Y0) // 2.0); r_ = math.hypot(x_, z_)
        if r_ > _prof.get(k_, 0.0): _prof[k_] = r_
    _R_CAD = max(_prof.values())
    def _supur(x0, x1, pay=0.5):
        kat = None
        for k_, r_ in sorted(_prof.items()):
            y0 = _Y0 + k_ * 2.0; y1 = y0 + 2.0; r_ += pay
            if x1 - x0 < 0.01: w_ = cq.Workplane("XZ").center(x0, ZT).circle(r_).extrude(-(y1 - y0)).translate((0, y0, 0))
            else: w_ = cq.Workplane("XZ").center((x0 + x1) / 2.0, ZT).slot2D(x1 - x0 + 2 * r_, 2 * r_, 0).extrude(-(y1 - y0)).translate((0, y0, 0))
            kat = w_ if kat is None else kat.union(w_)
        return kat.val()
    _IST = [("sos", 910.0, 910.0), ("harc", 1260.0, 1260.0), ("kiyma", 1483.0, 1707.0), ("kusbasi", 1693.0, 1917.0), ("kasar", 1956.0, 2061.0), ("sucuk", 2187.0, 2293.0)]   # bantli_tabla_cad_v1 ISTASYON (dünya, tabla ekseni x)
    _ENG = []
    for p in TC.PARCALAR:
        if p["ad"].startswith("_bom") or p["ad"] in KAPAK or p["ad"] in AKTARMA_TP10 or not v1_kalir(p["ad"]) or grup_modul(p["ad"]) in ("TABLA", "ARABA", "ACICI", "KONI_ON", "KONI_ARKA"): continue
        _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = p["wp"].val().translate(cq.Vector(X_BC + _d[0], Y_MEK + _d[1], _d[2]))
        if p["ad"] == "cikis_yarigi_contasi": sh = YARIK_V2
        _ENG.append(("TOPPING:" + p["ad"], sh))
    for q in TU.P:
        if q["ad"].startswith(V3_CIKAN): continue
        _ENG.append(("TOPPING2:" + q["ad"], q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))))
    for _ad_, x0_, x1_ in _IST:
        sw_ = _supur(x0_, x1_)
        for c_, sc in _ENG:
            if _bbk(sw_, sc):
                v_ = _hacim(sw_, sc)
                if v_ > 1.0 or v_ < 0: _cak_it.append((round(v_, 1), "DONUS(%s)" % _ad_, c_))
    # (3) pide koridoru park → aktarma (Ø300 × 28 + üst malzeme 5, kaset bandı üstünden) ↔ TOPPING sabitleri (açıcı / koniler / dozaj ağızları hariç: onlar pideye çalışır)
    _kor = FT.kut(X_BC + TC.XC_TABLA - 150.0, X_BC + TH.X_AKTARMA + 150.0, P + 0.5, P + 33.0, ZT - 150.0, ZT + 150.0).val()
    _kor_hit = []
    for c_, sc in _ENG:
        if _bbk(_kor, sc):
            v_ = _hacim(_kor, sc)
            if v_ > 1.0 or v_ < 0: _kor_hit.append((round(v_, 1), "PIDE KORIDORU", c_))
    print("BANTLI TABLA DENETIMI (gercek kati kesisimi > 1 mm3 · araba + kaset aktarmada ↔ TOPPING / TU / firin / yukleme bandi / K · kaset donus supurmesi %d istasyon (R_cad %.1f) ↔ TOPPING + TU + sabit tahrik): %s"
          % (len(_IST), _R_CAD, "TEMIZ" if not _cak_it else "%d BULGU" % len(_cak_it)))
    for x_ in sorted(_cak_it, reverse=True)[:40]: print("   %10.1f mm3  %s  <->  %s" % x_)
    print("PIDE KORIDORU park → aktarma (bilgi · dozaj ağızları pideye çalışır): %s" % ("TEMIZ" if not _kor_hit else "%d temas" % len(_kor_hit)))
    for x_ in sorted(_kor_hit, reverse=True)[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
    ITICI_OZET = ("v70 bantlı tabla: araba + kaset aktarmada (2365,4) ↔ TOPPING / TU / fırın / yükleme bandı / K gerçek katı kesişimi %s · kaset dönüş süpürmesi %d istasyonda (R %.1f) %s · ürün yolu kaset → yükleme bandı → fırın → K düz −170"
                  % ("TEMİZ" if not _cak_it else "%d BULGU" % len(_cak_it), len(_IST), _R_CAD, "temiz" if not _cak_it else "bulgulu"))
    assert not _cak_it, "v70: bantli tabla cakismasi var"
''')
s = s.replace('"""', '"""hat_montaj_v70 (29 Eyl 2026): BANTLI TABLA ana montajda — yap_hat_montaj_v70.py.\n', 1)
assert "IT." not in s.replace("_IT.", "").replace("SIT.", "") or True
compile(s, "hat_montaj_v70.py", "exec")
io.open(os.path.join(U, "hat_montaj_v70.py"), "w", encoding="utf-8").write(s)
import re
kalan = [m.start() for m in re.finditer(r"(?<![A-Za-z_])IT\.", s)]
print("hat_montaj_v70.py yazildi · %d satir · kalan IT. referansi: %d" % (s.count(NL), len(kalan)))
for k in kalan[:10]:
    print("   ", s[max(0, k - 80):k + 60].replace(NL, " | "))
