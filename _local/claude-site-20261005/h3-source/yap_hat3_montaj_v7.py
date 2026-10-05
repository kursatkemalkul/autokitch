# -*- coding: utf-8 -*-
"""TASLAK · h3/hat3_montaj_v6.py (v3.6) → h3/hat3_montaj_v7.py (HAT v3.7 · ÖN YÜZ KAPAK SADELEŞTİRMESİ · Claude · YEREL) — metin yaması, her yama sayısı denetlenir.
Kemal 1 Eki (çizim images/47.webp): "kapakları benim çizdiğim şekilde yeniden oluştur, daha temiz daha simple; çizgiler birbirini takip etsin; fazla bölmeye gerek yok".
Geometri h3/h3_kapak_v1.py'de (bu klasördeki taslak; montaj işi açılınca h3/'e kopyalanır). KARAR'lar h3_kapak_v1.KARAR'da.

KULLANIM
  python yap_hat3_montaj_v7.py <h3 klasörü> --kuru   → yalnız çapaları sayar (hiçbir dosyaya yazmaz; v6 üretecini ÇALIŞTIRMAZ)
  python yap_hat3_montaj_v7.py <h3 klasörü>          → (montaj işinde) önce yap_hat3_montaj_v6.py, sonra hat3_montaj_v7.py yazar
"""
import io, os, runpy, sys

H3 = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else os.path.dirname(os.path.abspath(__file__))
KURU = "--kuru" in sys.argv
if H3 not in sys.path: sys.path.insert(0, H3)
if not KURU:
    runpy.run_path(os.path.join(H3, "yap_hat3_montaj_v6.py"))                     # önce v3.6 (hat3_montaj_v6.py)
s = io.open(os.path.join(H3, "hat3_montaj_v6.py"), encoding="utf-8").read()
N = []


def rep(a, b, n=None):
    global s
    c = s.count(a)
    ok = c >= 1 and (n is None or c == n)
    N.append((ok, c, a[:70].replace("\n", "⏎")))
    if not KURU: assert ok, (a[:100], c)
    s = s.replace(a, b)


rep("hat3_v6", "hat3_v7")
rep('surum="v3.6"', 'surum="v3.7"', 1)
rep('pafta="HAT v3.6 (1 Eki',
    'pafta="HAT v3.7 (1 Eki · Claude · YEREL): ÖN YÜZ KAPAKLARI SADE (Kemal çizimi): 788 çizgisi boydan boya · A tek kapak 788–2197 (robot ağzı pencere) · '
    'TOPPING 2 tam boy kanat (mekanizma kanadı + soğuk kapak tek kabuk) · fırın üstü 2 düşer kapak 1308–2197 (U_F ile birleşti) · K tek kapak · '
    'E 2 × 2 (785/788 + dikey derz 4861,5) · B teknik sütun derzi 455 (K6 ile tek çizgi) · U kapakları kalktı · yeni açılma taraması · '
    'U_F ısı: baca taş yünü + 4 termostatlı 24 V fan + pano Pt100 alarmı + süperkapasitörlü DC-UPS · davlumbaz yağ/karbon filtresi + kanal fanı · '
    'pano cihazları üretici STEP · istasyon içi kablolar + kilitlenebilir ana ayırıcı · fire sileceği ürün yolundan çıktı · fırın üstü pizza yedeği gerçek yığın || HAT v3.6 (1 Eki', 1)

# ---- 1 · B teknik sütun (SC kurulur kurulmaz; KP burada içe alınır — SC < AK < UD < FU < KS < KC sırası) ----
rep('SC.PARCALAR[:] = [p_ for p_ in SC.PARCALAR if not p_["ad"].startswith(V36_ETEK)]\n',
    'SC.PARCALAR[:] = [p_ for p_ in SC.PARCALAR if not p_["ad"].startswith(V36_ETEK)]\n'
    'import h3_kapak_v1 as KP                                                                   # v3.7 · ön yüz kapak sadeleştirmesi (Kemal çizimi)\n'
    'V37_R = []\n'
    'KP.bolge_B_sag(SC.PARCALAR, V37_R)                                                          # v3.7 · teknik sütun derzi 447 → 455 (K6 çekmece derziyle tek çizgi)\n', 1)

# ---- 2 · A tek kapak (birimden ÖNCE) ----
rep('_dis_birim(AK, "GERCEK_ACICI"',
    'KP.bolge_A(AK.PARCALAR, V37_R, rahat=(AK.KAPAK_RAHAT["x"], AK.KAPAK_RAHAT["z"]))                                                              # v3.7 · A: alt panel + servis kapağı → tek kapak 788–2197\n'
    '_dis_birim(AK, "GERCEK_ACICI"', 1)

# ---- 3 · U_A + U_KE kapakları düşer (UD birimden ÖNCE) ----
rep('_v34_ac(UD.PARCALAR, "ust_a_taban_sac")',
    'KP.bolge_A_ust(UD.PARCALAR, V37_R); KP.bolge_KE_ust(UD.PARCALAR, V37_R)                     # v3.7 · U_A / U_KE kapakları kalktı (A, K, E kapakları tavana)\n'
    '_v34_ac(UD.PARCALAR, "ust_a_taban_sac")', 1)

# ---- 4 · fırın üstü + U_F tek düşer kapak (FU birimden ÖNCE; UD birimi zaten kayıtlı — U_F zarfı yan saclardan, değişmez) ----
rep('_dis_birim(FU, "GERCEK_FIRIN_UST"',
    'KP.bolge_F(FU.PARCALAR, UD.PARCALAR, V37_R)                                                 # v3.7 · F üstü kapak + U_F kapağı TEK düşer kapak 1308–2197\n'
    '_dis_birim(FU, "GERCEK_FIRIN_UST"', 1)

# ---- 5 · K tek kapak (K_PARCA ayrımından ÖNCE) ----
rep('KS.modul()\n',
    'KS.modul()\n'
    'KP.bolge_K(KS.PARCALAR, V37_R)                                                              # v3.7 · K: 3 kapak → tek kapak 788–2197 (+ menteşe, bas-aç: v3.6\'da yoktu)\n', 1)

# ---- 6 · E 2 × 2 kapak (E_PARCA ayrımından ÖNCE) ----
_a6 = 'assert sorted(V36_DUSEN) == sorted(["B|onyuz_plint", "B|onyuz_plint_donus_sol", "B|onyuz_plint_donus_sag", "E|onyuz_plint"]), V36_DUSEN\n'
rep(_a6, _a6 + 'KP.bolge_E(KC.PARCALAR, V37_R, X_E=X_E, klape_kes=KC.klape_cebi())                                                              # v3.7 · E: 2 × 2 kapak, ağız penceresi, klape yerinde\n'
              'print("v3.7 · ÖN YÜZ KAPAKLARI: %d değişiklik · " % len(V37_R) + " · ".join(V37_R[:12]) + (" …" if len(V37_R) > 12 else ""))\n', 1)

# ---- 7 · TOPPING: TC her yeniden kuruluşta mekanizma kanadı kabukları düşer; ilk seferde TU K1/K2 dış sacıyla TEK KABUK olur ----
_TC = '''
V37_TC_KABUK = ("onyuz_mekanizma_kanadi_sol", "onyuz_mekanizma_kanadi_sag")


def _v37_tc():
    """v3.7 · TOPPING kanadı: mekanizma kanadı (TC, emiş/atış yarıklı) + K1/K2 dış sacı (TU) tek kabuk · TC kabuğu her TC.modul() sonrası düşer"""
    if not getattr(_v37_tc, "oldu", False):
        _tcp = {y_: [p for p in TC.PARCALAR if p["ad"] == "onyuz_mekanizma_kanadi_" + y_][0] for y_ in ("sol", "sag")}
        _tup = {y_: [q for q in TU.P if q["ad"] == "onyuz_K%d_dis_sac" % (1 if y_ == "sol" else 2)][0] for y_ in ("sol", "sag")}
        _of = lambda p_: cq.Vector(X_BC + V1_TASI.get(p_["ad"], (0.0, 0.0, 0.0))[0], Y_MEK + V1_TASI.get(p_["ad"], (0.0, 0.0, 0.0))[1], V1_TASI.get(p_["ad"], (0.0, 0.0, 0.0))[2])
        KP.bolge_TOPPING(_tcp, _tup, X_BC, _of, V37_R); _v37_tc.oldu = True
    TC.PARCALAR[:] = [p for p in TC.PARCALAR if p["ad"] not in V37_TC_KABUK]
'''
rep("\n# ---- v70: aktarma iticisi KALKTI", _TC + "\n# ---- v70: aktarma iticisi KALKTI", 1)
rep("TC.PARCALAR[:] = []; TC.modul()", "TC.PARCALAR[:] = []; TC.modul(); _v37_tc()", 2)        # ana döngü (1868) + fırın çakışma denetimi (2335)

# ---- 8 · AÇILMA TARAMASI (yeni denetim · temiz olmadan yayın yok) ----
_SUP = '''    # ---- v3.7 · KAPAK AÇILMA TARAMASI: 10–100° · engel = aynı / komşu modüllerin SABİT parçaları · diğer kapaklar KAPALI ----
    # ÇERÇEVELER (hepsi DÜNYAYA çevrilir): AK / UD / FU / SC dünya · KC (E) x + X_E · KS (K) x + X_K (K_SAC yaması dünya listesi verirse 0) · TU x + X_BC · TC + (X_BC + d, Y_MEK + d, d)
    _E37 = []; _KANAT37 = tuple("ecop_" + a_ for a_ in KC.KANAT_AD)                      # robot çöpü klapesi + oluğu E sol alt kanadıyla döner (engel değil, kanat gövdesi)
    for _M, _L in ((AK, AK.PARCALAR), (UD, UD.PARCALAR), (FU, FU.PARCALAR), (KS, KS.PARCALAR), (KC, KC.PARCALAR), (SC, SC.PARCALAR)):
        _dx = X_K if _L is KS.PARCALAR else (X_E if _M is KC else 0.0)
        for p_ in _L:
            if p_.get("grup", "SABIT") == "SABIT" and not p_["ad"].startswith("onyuz_kapak_") and not KP.DONANIM.search(p_["ad"]) and p_["ad"] not in _KANAT37 \
                    and not (_M is KS and "KSAC" in globals() and KSAC.kapakla_doner(p_["ad"])):   # kapak donanımı (menteşe/bas-aç) + K kapağıyla dönenler engel değil
                _E37.append((p_["ad"], KP.sekil(p_).translate(cq.Vector(_dx, 0.0, 0.0))))
    _E37 += [("TU:" + q_["ad"], q_["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))) for q_ in TU.P if q_["grup"] == "SABIT" and not q_["ad"].startswith(("onyuz_K1_", "onyuz_K2_", "onyuz_flipper"))]
    for p_ in TC.PARCALAR:                                                                # TOPPING çerçevesi (mekanizma çerçevesi dikme / kayıt) · kanat donanımı hariç
        if p_["ad"].startswith(("_bom", "onyuz_mekanizma_kanadi")) or p_["ad"] in KAPAK or p_["ad"] in AKTARMA_TP10 or not v1_kalir(p_["ad"]) or KP.DONANIM.search(p_["ad"]): continue
        _d = V1_TASI.get(p_["ad"], (0.0, 0.0, 0.0)); _sh = p_["wp"].val().translate(cq.Vector(X_BC + _d[0], Y_MEK + _d[1], _d[2]))
        if _sh.BoundingBox().zmax > -60.0: _E37.append(("TC:" + p_["ad"], _sh))
    _K37 = {p_["ad"]: KP.sekil(p_) for _L in (AK.PARCALAR, KS.PARCALAR, KC.PARCALAR) for p_ in _L}
    _K37.update({p_["ad"]: KP.sekil(p_).translate(cq.Vector(X_E, 0.0, 0.0)) for p_ in KC.PARCALAR})                         # E yerel → dünya
    _K37["onyuz_kapak_E_alt_sol"] = cq.Compound.makeCompound([_K37["onyuz_kapak_E_alt_sol"]] + [KP.sekil(p_).translate(cq.Vector(X_E, 0.0, 0.0)) for p_ in KC.PARCALAR if p_["ad"] in _KANAT37])
    _K37["onyuz_kapak_A"] = cq.Compound.makeCompound([KP.sekil(p_) for p_ in AK.PARCALAR if p_["grup"] == "SERVIS_KAPAGI"])          # A: kapak + omega + menteşe kanatları + hedef (dünya)
    if _K37["onyuz_kapak_K"].BoundingBox().xmin < X_K - 1.0: _K37["onyuz_kapak_K"] = _K37["onyuz_kapak_K"].translate(cq.Vector(X_K, 0.0, 0.0))   # K yerel kaldıysa (K_SAC yaması yoksa)
    _S37 = []
    for _ad, _n, _y, _i in KP.SUPURME:
        if _ad == "onyuz_kapak_A": _n = (AK.MENTESE["pivot"][0], 0.0, AK.MENTESE["pivot"][1])                                  # A gizli menteşe ekseni (h3_acici_v1)
        _bk = _K37[_ad].BoundingBox(); assert abs(_bk.xmin - _n[0]) < 10.0 or abs(_bk.xmax - _n[0]) < 10.0, ("v3.7 süpürme: eksen kapak kenarında değil (çerçeve?)", _ad, _n, _bk.xmin, _bk.xmax)
        _r = KP.supur(_K37[_ad], _n, _y, _i, [e_ for e_ in _E37 if e_[0] != _ad]); _S37 += [(_ad,) + r_ for r_ in _r]
    for _y in ("sol", "sag"):                                                             # TOPPING kanadı: sanal pivot ön dış köşe
        _q = [q_ for q_ in TU.P if q_["ad"] == "onyuz_K%d_dis_sac" % (1 if _y == "sol" else 2)][0]
        _kq = _q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0)); _bq = _kq.BoundingBox()
        assert abs(_bq.ymin - 788.0) < 1.0 and 1430.0 < _bq.xmin < 2000.0, ("v3.7 süpürme: TOPPING kabuğu dünyada değil / birleşmemiş", _bq.xmin, _bq.ymin)
        _r = KP.supur(_kq, ((_bq.xmin if _y == "sol" else _bq.xmax), 0.0, 79.0), (0, 1, 0), (-1 if _y == "sol" else 1), _E37); _S37 += [("TOPPING_" + _y,) + r_ for r_ in _r]
    for _g, (_n, _yon, _ac) in FU.KAPAK_EKSEN.items():                                     # fırın üstü düşer kapaklar (FU dünya)
        _kq = cq.Compound.makeCompound([FU.dunya(p_) for p_ in FU.PARCALAR if p_["grup"] == _g])
        _r = KP.supur(_kq, _n, _yon, 1, _E37, acilar=range(10, int(_ac) + 1, 10)); _S37 += [(_g,) + r_ for r_ in _r]
    print("v3.7 · KAPAK AÇILMA TARAMASI (%d kapak · %d engel): %s" % (len(KP.SUPURME) + 2 + len(FU.KAPAK_EKSEN), len(_E37), "TEMIZ" if not _S37 else _S37[:12]))
    assert not _S37, _S37
'''
rep("    _eksik32 = sorted(", _SUP + "    _eksik32 = sorted(", 1)

# ---- 8b · taban/üst hizası denetimi: E kapağı U_KE ile birleşti → E_GOVDE üstü kapak tepesi (KARAR KE_1862_KALKAR) ----
rep('("E_GOVDE ustu", _bk["E_GOVDE"]["y"][1], H_MAK)',
    '("E_GOVDE ustu (v3.7: kapak U_KE ile tek parça, tavana kadar)", _bk["E_GOVDE"]["y"][1], (KP.Y_TAVAN_KAPAK if KP.KARAR["KE_1862_KALKAR"] else H_MAK))', 1)

# ---- 8c · kaide denetimi: TOPPING birleşik ön kanadı (TU dış sac) artık 788'e iner — ön kapaklar kaide bandını örter (TC'de olduğu gibi onyuz_ hariç) ----
rep("    _tu_alt = min(sh.BoundingBox().ymin for _a, sh in _TUT)\n",
    "    _tu_alt = min(sh.BoundingBox().ymin for _a, sh in _TUT if not _a.startswith(\"TOPPING2:onyuz_\"))   # v3.7: birleşik ön kanat 788'e iner (kapak, kaide bandını örter)\n", 1)

# ---- 8d · ön yüz denetimi: ana hattın QR bölgesindeki kısmı (kilitlenebilir ana ayırıcı QR servis yanında + bina kablosu) koridorda, QR gibi —
#           x ≥ E sağ yüzü (5230) ya da zemin üstü kanal içinde (y ≤ 100, kanal ELK_ZEMIN_KANALI gibi koridordan QR'a geçer) köşeler hariç; makine boyunca ana hat +79 kuralına tabi ----
rep("        zm = max(q[2] for q in m_.P) / MM\n",
    "        zm = (max((q[2] for q in m_.P if q[0] / MM < 5230.0 and q[1] / MM > 100.0), default=-1e9) if a_.startswith(\"ELK_ANA_HAT\") else max(q[2] for q in m_.P)) / MM   # v3.7: ana ayırıcı QR yanında (koridor)\n", 1)

# ---- 9 · küçük düzeltmeler (v37_kucuk ajanı): fire sileceği −91 · fırın üstü pizza yedeği gerçek yığın ----
import importlib.util as _iu37
for _ad37 in ("yama_v37_fire.py", "yama_v37_pizza.py", "yama_v37_k_sac.py"):          # k_sac: K gövdesi üretim sacı (h3_k_sac_v1) · KP.bolge_K yerine (K YEREL çerçeve)
    _sp37 = _iu37.spec_from_file_location(_ad37[:-3], os.path.join(H3, _ad37)); _m37 = _iu37.module_from_spec(_sp37); _sp37.loader.exec_module(_m37)
    if KURU:
        try: _m37.uygula(s); N.append((True, 1, _ad37))
        except AssertionError as _e37: N.append((False, 0, _ad37 + " " + str(_e37)[:60]))
    else:
        s = _m37.uygula(s); N.append((True, 1, _ad37))

if KURU:
    for ok, c, a in N: print("%s  %2d  %s" % ("OK " if ok else "YOK", c, a))
    print("KURU: %d yama · %d sorunlu · dosya YAZILMADI" % (len(N), sum(1 for ok, c, a in N if not ok)))
else:
    io.open(os.path.join(H3, "hat3_montaj_v7.py"), "w", encoding="utf-8").write(s)
    print("hat3_montaj_v7.py yazıldı · %d yama" % len(N))
