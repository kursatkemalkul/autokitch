# -*- coding: utf-8 -*-
"""HAT VERSİYON 2 · A AÇICI KABİNİ ADAPTÖRÜ v1 (30 Eyl 2026 · Claude · YEREL) — acici_kabin_cad_v1'in v2 yerleşimi.
YÖNTEM: v1 kabini (acici_kabin_cad_v1, DÜNYA x 0–700) YENİDEN ÇİZİLMEZ: her kur()'da v1 kur() çağrılır, bütün parçalar x + DXL (507,5) taşınır.
  · A modülü v2: x 507,5–1207,5 (h3_hesap_v1.A_X) · y 788–1862 · z −830…+79 — genişlik, kotlar, derinlik v1 ile birebir.
  · Parça adları / malzeme / birim / grup / BOM v1 ile AYNI (yalnız wp taşınır). Montaj p["wp"]'yi DÜNYA koordinatı olarak kullanır (v1 sözleşmesi).
  · x taşıyan her sabit (X_A0/X_A1, panel, robot ağzı, top yolu, ışık perdesi, disk, menteşe ekseni, sensörler, ara lamalar) + DXL ile yeniden yayımlanır;
    y / z sabitleri v1'den aynen gelir.
v1'in başka modüllere bağlılığı (denetlendi):
  · kaide_cad_v2: yalnız Y_DUZ 788 · Y_MEK 892 · A_SAC 1,5 · KZ[1] +35 (y / z) → v2'de aynı; A kaidesi de +507,5 kayar (h3_kaide_v1) → dikmeler yine taban sacına oturur.
  · TOPPING: açıcı kafası / tabla / koniler TOPPING CAD'inde; v2'de TOPPING'in sol dilimi (v1 x < 1106,5) de +507,5 kayar → açıcı ↔ kabin ilişkisi
    birebir aynı (acici_kapisi() v1 geometrisinde koşar, sonuç taşımadan bağımsız). A'nın sağ duvarı + rakor delikleri h3_moduler_v1'de (RAKOR_ACICI).
  · C paneli v1'de 701,5'te başlar → v2'de 1209 (TOPPING sol grubu da +507,5) · A|C derzi 3 aynı.
  · DUVAR_ARALIK (dükkân sol duvarı ≥ 10 mm, VARSAYIM) GÖRELİ kalır: duvar artık A'nın solu x 507,5'e göre ölçülür (dükkân planı Kemal'de).
SÖZLEŞME (v1 ile aynı): kur() · PARCALAR · dunya(p) · BIRIMLER · BIRIM_MODUL · ON_BIRIMLER · Z_ON · MALZEME · sozlesme() · KAPAK_EKSEN · kapak_pozu(aci) · acici_kapisi()
kur() İDEMPOTENT: her çağrı v1'den baştan kurar (çift kayma olmaz) · PARCALAR listesinin kimliği korunur (PARCALAR[:] = …).
Çalıştır (öz denetim): python ob_calistir.py h2/h3_acici_v1.py
"""
import math, os, sys, time

H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_hesap_v1 as H
import acici_kabin_cad_v1 as V1

# ---------------------------------------------------------------- v2 YERLEŞİM (h3_hesap_v1 tek sayı kaynağı) ----------------------------------------------------------------
DXL = H.A_X[0] - V1.X_A0                                                   # 507,5 · v1 kabini bu kadar sağa
assert abs(DXL - H.DXL) < 1e-9, (DXL, H.DXL)
assert abs((H.A_X[1] - H.A_X[0]) - (V1.X_A1 - V1.X_A0)) < 1e-9, "A genişliği v1 ile aynı olmalı (700)"


def _x(v):
    return v + DXL


def _xx(t):
    return (t[0] + DXL, t[1] + DXL)


X_A0, X_A1 = H.A_X                                                         # 507,5 · 1207,5 (v1 0 · 700)
# y / z sabitleri v1 ile AYNI
Y_DUZ, Y_MEK, H_MAK, Y_TABAN = V1.Y_DUZ, V1.Y_MEK, V1.H_MAK, V1.Y_TABAN
Z_ARKA, Z_ON, T, T_OM, KENAR, Z_PAN, Z_YUZ, Z_CER, DERZ = V1.Z_ARKA, V1.Z_ON, V1.T, V1.T_OM, V1.KENAR, V1.Z_PAN, V1.Z_YUZ, V1.Z_CER, V1.DERZ
Y_B_ON, Y_ALT, Y_UST, Y_SAC1, Y_KUSAK, Y_CER0, Y_ORTA, Y_PERDE_KAYIT = V1.Y_B_ON, V1.Y_ALT, V1.Y_UST, V1.Y_SAC1, V1.Y_KUSAK, V1.Y_CER0, V1.Y_ORTA, V1.Y_PERDE_KAYIT
Z_ON_DIKME, Z_KOSE_ARKA, Z_LAMA = V1.Z_ON_DIKME, V1.Z_KOSE_ARKA, V1.Z_LAMA
KOSE, ON_DIKME, CER, RO, DUVAR_ARALIK, MANDAL_Y = V1.KOSE, V1.ON_DIKME, V1.CER, V1.RO, V1.DUVAR_ARALIK, V1.MANDAL_Y
# x taşıyan sabitler (+DXL)
X_PAN = _xx(V1.X_PAN)                                                      # 507,5 … 1206 (v1 0 … 698,5) · C paneli 1209'da başlar → derz 3
XS_SOL, XS_SAG = _xx(V1.XS_SOL), _xx(V1.XS_SAG)                            # 509 … 539 · 1177,5 … 1207,5
X_ORTA_KES = _xx(V1.X_ORTA_KES)
AGIZ = dict(V1.AGIZ, x=_xx(V1.AGIZ["x"]))                                  # robot ağzı x 757,5–957,5 (v1 250–450)
TOP = dict(V1.TOP, x=_xx(V1.TOP["x"]))
PERDE = dict(V1.PERDE, x=_xx(V1.PERDE["x"]), tut_x=tuple(_xx(t) for t in V1.PERDE["tut_x"]))
ARA_LAMA = [dict(l, x=_xx(l["x"])) for l in V1.ARA_LAMA]
DISK = dict(V1.DISK, x=_xx(V1.DISK["x"]))
MENTESE = dict(V1.MENTESE, pivot=(_x(V1.MENTESE["pivot"][0]), V1.MENTESE["pivot"][1]))   # gizli menteşe ekseni x 514,5 · z 72 (v1 7 · 72)
KAPAK_RAHAT = dict(V1.KAPAK_RAHAT, x=_x(V1.KAPAK_RAHAT["x"]))
SENSOR, HEDEF = dict(V1.SENSOR, x=_xx(V1.SENSOR["x"])), dict(V1.HEDEF, x=_xx(V1.HEDEF["x"]))
SENSOR_ALT, HEDEF_ALT = dict(V1.SENSOR_ALT, x=_xx(V1.SENSOR_ALT["x"])), dict(V1.HEDEF_ALT, x=_xx(V1.HEDEF_ALT["x"]))
KAPAK_EKSEN = dict(V1.KAPAK_EKSEN, pivot=MENTESE["pivot"],
                   not_="GERÇEK menteşe ekseni (x %.1f · z %.0f, dikey · v2 = v1 x 7 + %.1f) · kapak 0–90° bu eksen etrafında döner · kapak_pozu(aci)" % (MENTESE["pivot"][0], MENTESE["pivot"][1], DXL))
X_C_PANEL = V1.X_PAN[1] + V1.DERZ + DXL                                    # 1209 · C (TOPPING) ön panelinin sol ucu (v1 701,5)


def _s(v):
    """Türkçe ondalık (507,5 · 1207,5 · 700)"""
    t = ("%.1f" % v).replace(".", ",")
    return t[:-2] if t.endswith(",0") else t


BIRIMLER = [
    ("A_GOVDE", "A AÇICI kabini gövdesi (kuru, PU yok) · HAT v2: x %s–%s (v1 kabini +%s) · y 788–1862 · z −830…+59 · 304 1,5 sol yan + üst + sökülür arka (delik yok) · "
                "arka köşe dikmeleri 30 × 30 × 2 · ön dikmeler + üst kayıt 30 × 50 × 2 · ön çerçeve 30 × 20 × 2 (z +39…+59) · ışık perdesi (SICK miniTwin4 × 2) · "
                "2 emniyet sensörü (RSS 36) · sağ duvar = kendi 1,5 sacı (h3_moduler_v1) · taban = A kaidesi (v2)" % (_s(X_A0), _s(X_A1), _s(DXL))),
    ("A_ONYUZ", "A ön yüz (z +59…+79, ön düzlem +79) · tava 20 304 fırçalı 1,5 · alt panel 788–1107,5 (sökülür) + üst servis kapağı 1110,5–1859 "
                "(gizli pim menteşe sol, eksen x %s · z 72, bas-aç, emniyet sensörü) · ROBOT AĞZI x %s–%s · y 960–1160 (kenarlar bükülü) · derz 3"
                % (_s(MENTESE["pivot"][0]), _s(AGIZ["x"][0]), _s(AGIZ["x"][1]))),
]
assert [k for k, _a in BIRIMLER] == [k for k, _a in V1.BIRIMLER]
BIRIM_MODUL = dict(V1.BIRIM_MODUL)
ON_BIRIMLER = tuple(V1.ON_BIRIMLER)
MALZEME = V1.MALZEME
kut = V1.kut
dunya = V1.dunya                                                           # qr_cad_v1.dunya: wp.vals() → tek şekil / Compound (DÜNYA)

PARCALAR = []
CER_PARCA = []            # ön çerçeve profilleri (ad, boy) · v1 ile aynı


def kur():
    """v1 kabinini baştan kurar, her parçayı x + DXL taşır · İDEMPOTENT (iki kez çağrılınca çift kayma yok) · PARCALAR nesnesi aynı kalır"""
    V1.kur()
    PARCALAR[:] = [dict(p, wp=p["wp"].translate((DXL, 0.0, 0.0))) for p in V1.PARCALAR]
    CER_PARCA[:] = list(V1.CER_PARCA)
    return PARCALAR


def kapak_pozu(aci):
    """servis kapağı grubunun açık konumu (derece, 0–90): (eksen noktası, eksen yönü, açı) — cq.Shape.rotate(a, b, aci) · v2 eksen x 514,5"""
    px, pz = MENTESE["pivot"]
    return (cq.Vector(px, 0.0, pz), cq.Vector(px, 1.0, pz), -float(aci))


def sozlesme():
    """montaj ölçü sözleşmesi (v1 ile aynı anahtarlar, x değerleri v2)"""
    s = V1.sozlesme()
    s.update(X=(X_A0, X_A1), PANEL_X=X_PAN, AGIZ=AGIZ, TOP=TOP, KAPAK_EKSEN=KAPAK_EKSEN, MENTESE=MENTESE,
             ISIK_PERDESI=dict(s["ISIK_PERDESI"], x=PERDE["x"]), C_PANEL_X0=X_C_PANEL, DXL=DXL)
    return s


def acici_kapisi(ps=None):
    """MONTAJ KAPISI (v1 denetçi 1): açıcı kafası ↔ kabin çakışmaları İSTİSNASIZ. v2'de TOPPING'in sol dilimi (açıcı dahil) kabinle birlikte +DXL kaydığından
    göreli geometri v1 ile birebir aynı → v1 kapısı v1 koordinatında koşar (verilen v2 parçaları −DXL geri taşınır). TOPPING sürümü v1'deki gibi kaide_cad_v2.tc_modul()."""
    ps = ps if ps is not None else kur()
    return V1.acici_kapisi([dict(p, wp=p["wp"].translate((-DXL, 0.0, 0.0))) for p in ps])


# ---------------------------------------------------------------- ÖZ DENETİM ----------------------------------------------------------------
DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-150s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))


def _bbt(s):
    b = s.BoundingBox(); return (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)


if __name__ == "__main__":
    t0 = time.time()
    ps = kur()
    kimlik = id(PARCALAR)
    V1.kur()                                                               # v1 referansı (taşınmamış)
    v1 = {p["ad"]: (p, V1.dunya(p)) for p in V1.PARCALAR}
    ps = kur(); ps2 = [dict(p) for p in ps]; ps = kur()                     # 3 kez kur → çift kayma olmamalı
    print("h3_acici_v1 · %d parça (v1 %d) · DXL %.1f · A x %.1f–%.1f · %.1f sn" % (len(ps), len(v1), DXL, X_A0, X_A1, time.time() - t0))
    print("ÖZ DENETİM (h3_acici_v1)")
    kontrol("İDEMPOTENT: kur() 3 kez → parça sayısı %d = %d · adlar aynı sırada · PARCALAR nesnesi aynı (id)" % (len(ps), len(ps2)),
            len(ps) == len(ps2) == len(v1) and [p["ad"] for p in ps] == [p["ad"] for p in ps2] and id(PARCALAR) == kimlik and ps is PARCALAR)
    idem = max(max(abs(a - b) for a, b in zip(_bbt(dunya(p)), _bbt(dunya(q)))) for p, q in zip(ps, ps2))
    kontrol("İDEMPOTENT: art arda iki kur() arasında en büyük sınır kutusu farkı %.2e mm (çift kayma yok)" % idem, idem < 1e-6)
    # 1 · her parça = v1 parçası + DXL (x) · y / z / hacim / geçerlilik / ad / malzeme / birim / grup / BOM aynı
    fark, meta, gec = 0.0, [], []
    for p in ps:
        q, sq = v1[p["ad"]]
        a, b = _bbt(dunya(p)), _bbt(sq)
        fark = max(fark, abs(a[0] - b[0] - DXL), abs(a[1] - b[1] - DXL), *(abs(a[i] - b[i]) for i in range(2, 6)), abs(dunya(p).Volume() - sq.Volume()))
        if any(p[k] != q[k] for k in ("mal", "birim", "grup", "bom", "kaynak")): meta.append(p["ad"])
        if not dunya(p).isValid(): gec.append(p["ad"])
    kontrol("her parça = v1 parçası + %.1f x (sınır kutusu x0/x1 + DXL, y/z aynı, hacim aynı) · en büyük sapma %.2e" % (DXL, fark), fark < 1e-6)
    kontrol("ad / malzeme / birim / grup / BOM / kaynak v1 ile aynı (%d parça)" % len(ps), not meta, str(meta[:6]))
    kontrol("katılar geçerli", not gec, ", ".join(gec))
    # 2 · zarf
    bb = {p["ad"]: dunya(p).BoundingBox() for p in ps}
    X0_, X1_ = min(b.xmin for b in bb.values()), max(b.xmax for b in bb.values())
    Y0_, Y1_ = min(b.ymin for b in bb.values()), max(b.ymax for b in bb.values())
    Z0_, Z1_ = min(b.zmin for b in bb.values()), max(b.zmax for b in bb.values())
    v1b = [sq.BoundingBox() for _q, sq in v1.values()]
    v1x = (min(b.xmin for b in v1b), max(b.xmax for b in v1b))
    tas = [a for a, b in bb.items() if b.xmin < X_A0 - 1e-6 or b.xmax > X_A1 + 1e-6]
    kontrol("ZARF x %.2f–%.2f · y %.1f–%.1f · z %.1f…%.1f ⊂ A v2 x %.1f–%.1f · y 788–1862 · z −830…+79 · A dışına taşan parça %d (v1: x %.1f–%.1f ⊂ 0–700, taşan yok)"
            % (X0_, X1_, Y0_, Y1_, Z0_, Z1_, X_A0, X_A1, len(tas), v1x[0], v1x[1]),
            not tas and abs(X0_ - X_A0) < 0.01 and abs(X1_ - X_A1) < 0.01 and abs(Y0_ - Y_DUZ) < 0.01 and abs(Y1_ - H_MAK) < 0.01 and abs(Z0_ - Z_ARKA) < 0.01 and abs(Z1_ - Z_ON) < 0.01, str(tas[:6]))
    # 3 · sözleşme x değerleri
    s1, s2 = V1.sozlesme(), sozlesme()
    xs_ok = (abs(s2["X"][0] - s1["X"][0] - DXL) < 1e-9 and abs(s2["X"][1] - s1["X"][1] - DXL) < 1e-9 and abs(s2["PANEL_X"][0] - s1["PANEL_X"][0] - DXL) < 1e-9
             and abs(s2["AGIZ"]["x"][0] - s1["AGIZ"]["x"][0] - DXL) < 1e-9 and abs(s2["TOP"]["x"][1] - s1["TOP"]["x"][1] - DXL) < 1e-9
             and abs(s2["KAPAK_EKSEN"]["pivot"][0] - s1["KAPAK_EKSEN"]["pivot"][0] - DXL) < 1e-9 and s2["KAPAK_EKSEN"]["pivot"][1] == s1["KAPAK_EKSEN"]["pivot"][1]
             and abs(s2["ISIK_PERDESI"]["x"][0] - s1["ISIK_PERDESI"]["x"][0] - DXL) < 1e-9 and s2["Y"] == s1["Y"] and s2["Z_ON"] == s1["Z_ON"] == 79.0)
    kontrol("sozlesme(): X %s · PANEL_X %s · AĞIZ x %s · TOP x %s · menteşe ekseni %s · ışık perdesi x %s = v1 + %.1f · Y / Z_ON aynı"
            % (s2["X"], s2["PANEL_X"], s2["AGIZ"]["x"], s2["TOP"]["x"], s2["KAPAK_EKSEN"]["pivot"], s2["ISIK_PERDESI"]["x"], DXL), xs_ok)
    # geometriden ölçülen sabitler (ağız / panel / menteşe pimi)
    ap, sk = bb["onyuz_alt_panel"], bb["onyuz_servis_kapagi"]
    pim = bb["onyuz_servis_kapagi_mentese_0_pim"]
    kontrol("ölçülen: alt panel / servis kapağı x %.1f–%.1f = X_PAN %s · menteşe pimi ekseni x %.2f = MENTESE %.1f · C paneline derz %.1f"
            % (ap.xmin, max(ap.xmax, sk.xmax), X_PAN, (pim.xmin + pim.xmax) / 2.0, MENTESE["pivot"][0], X_C_PANEL - max(ap.xmax, sk.xmax)),
            abs(ap.xmin - X_PAN[0]) < 0.01 and abs(max(ap.xmax, sk.xmax) - X_PAN[1]) < 0.01 and abs((pim.xmin + pim.xmax) / 2.0 - MENTESE["pivot"][0]) < 0.01
            and abs(X_C_PANEL - max(ap.xmax, sk.xmax) - DERZ) < 0.01)
    tun = kut(AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1], -200.0, Z_ON + 50.0).val()
    t_c = [(round(dunya(p).intersect(tun).Volume(), 3), p["ad"]) for p in ps if V1.QR._bbk(bb[p["ad"]], tun.BoundingBox())]
    t_c = [x for x in t_c if x[0] > 0.0]
    kontrol("ROBOT AĞZI x %.1f–%.1f · y %.0f–%.0f (z −200…+129 tüneli) temiz — kabin parçası girmez" % (AGIZ["x"][0], AGIZ["x"][1], AGIZ["y"][0], AGIZ["y"][1]), not t_c, str(t_c[:4]))
    # 4 · kendi arasında (v1 ile aynı olmalı)
    cak = V1.QR.kendi_arasinda(ps, istisna=lambda a, c: False, esik=0.1)
    kontrol("kabin kendi arasında çakışma = 0 (%d parça, > 0,1 mm³ · menteşe pimleri göz deliklerine temas)" % len(ps), not cak, str(cak[:6]))
    # 5 · servis kapağı açılma taraması (v1 denetçi 2) · v2 ekseniyle · 90° pozu = v1 90° pozu + DXL
    kp = [p for p in ps if p["grup"] == "SERVIS_KAPAGI"]
    kc = cq.Compound.makeCompound([dunya(p) for p in kp])
    kc1 = cq.Compound.makeCompound([sq for q, sq in v1.values() if q["grup"] == "SERVIS_KAPAGI"])
    sabit = [(p["ad"], dunya(p), bb[p["ad"]]) for p in ps if p["grup"] != "SERVIS_KAPAGI"]
    k_c, xmin_s, xmax_s, vmax = [], 1e9, -1e9, 0.0
    acilar = [0.5, 1.0, 1.5, 2.0] + [2.5 * i for i in range(1, 37)]
    for aci in acilar:
        r = kc.rotate(*kapak_pozu(aci)); rb = r.BoundingBox()
        xmin_s, xmax_s = min(xmin_s, rb.xmin), max(xmax_s, rb.xmax)
        for a_, s_, b_ in sabit:
            if V1.QR._bbk(b_, rb):
                v_ = r.intersect(s_).Volume(); vmax = max(vmax, v_)
                if v_ > 1.0: k_c.append((aci, a_, round(v_, 1)))
    r90, r90_1 = _bbt(kc.rotate(*kapak_pozu(90.0))), _bbt(kc1.rotate(*V1.kapak_pozu(90.0)))
    d90 = max(abs(r90[0] - r90_1[0] - DXL), abs(r90[1] - r90_1[1] - DXL), *(abs(r90[i] - r90_1[i]) for i in range(2, 6)))
    kontrol("SERVİS KAPAĞI AÇILMA TARAMASI: eksen x %.1f · z %.0f · %d adım 0–90° · sabit parçalara en büyük kesişim %.3f mm³ (eşik 1, v1 ile aynı) · sol payı x_min %.2f ≥ A solu − %.0f (%.1f) · x_max %.2f < C paneli %.1f"
            % (MENTESE["pivot"][0], MENTESE["pivot"][1], len(acilar), vmax, xmin_s, DUVAR_ARALIK - 2.0, X_A0 - (DUVAR_ARALIK - 2.0), xmax_s, X_C_PANEL),
            not k_c and xmin_s >= X_A0 - (DUVAR_ARALIK - 2.0) and xmax_s < X_C_PANEL - 0.5, str(k_c[:6]))
    kontrol("kapak 90° pozu (v2 ekseni) = v1 90° pozu + %.1f x · sapma %.2e (eksen doğru taşındı)" % (DXL, d90), d90 < 1e-6)
    # 6 · havada parça (kabin tek başına: v1 de kaideyle birlikte denetliyordu → burada kaide varsa onunla)
    try:
        import h3_kaide_v1 as KD2
        KD2.kur()
        kd = [p for p in KD2.PARCALAR if p["birim"] == "KAIDE_A"]
        print("   (h3_kaide_v1 bulundu: KAIDE_A %d parça)" % len(kd))
    except Exception as e:
        kd = None
        print("   BİLGİ · h3_kaide_v1 yok / yüklenemedi (%s) — kaide oturma + çakışma denetimi h2/_test_moduler_v1.py'de (kaide_cad_v4 A + DXL ara modeliyle)" % str(e)[:100])
    if kd:
        tum = ps + [dict(p, ad="KAIDE:" + p["ad"]) for p in kd]
        cak = V1.QR.kendi_arasinda(tum, istisna=lambda a, c: False, esik=0.1)
        kontrol("kabin + h3_kaide_v1 (KAIDE_A) çakışma = 0 (> 0,1 mm³)", not cak, str(cak[:6]))
        ts = [dunya(p).BoundingBox() for p in kd if p["ad"] == "kaide_A_mekanizma_taban_saci"][0]
        P_ = {p["ad"]: p for p in ps}
        oturma = []
        for ad_ in ("a_kose_dikmesi_arka_sol", "a_kose_dikmesi_arka_sag", "onyuz_cerceve_sol_dikme", "onyuz_cerceve_sag_dikme"):
            kes = dunya(P_[ad_]).intersect(kut(X_A0 - 5.0, X_A1 + 5.0, Y_TABAN, Y_TABAN + 1.0, Z_ARKA - 5.0, Z_ON + 5.0).val())
            des = kut(ts.xmin, ts.xmax, Y_TABAN, Y_TABAN + 1.0, ts.zmin, ts.zmax).val()
            if "cerceve" in ad_:
                alt = bb[ad_.replace("_dikme", "_alt_dikme")]
                des = des.fuse(kut(alt.xmin, alt.xmax, Y_TABAN, Y_TABAN + 1.0, alt.zmin, alt.zmax).val())
            oturma.append(100.0 * kes.intersect(des).Volume() / kes.Volume())
        kontrol("4 dikme h3_kaide_v1 taban sacına TAM oturur: %s" % " · ".join("%%%.2f" % v for v in oturma), all(v >= 99.99 for v in oturma))
    print("ÖZ DENETİM: %d madde · %d KALDI · %.0f sn" % (len(DEN), sum(1 for d_ in DEN if not d_[1]), time.time() - t0))
    assert all(d_[1] for d_ in DEN)
    sys.stdout.flush(); os._exit(0)
