# -*- coding: utf-8 -*-
"""TEST v3.5 (1 Eki 2026 · Claude · YEREL) — yama_qr_step_v35'i KOPYAYA uygular (h3_elk_qr_v1_STEP_TEST.py; asıl dosyaya dokunmaz),
yalnız QR panosu parçalarını sahte toplayıcıyla kurar (sahte QR: göz parçası yok → yalnız pano / kanal / giriş parçaları) ve denetler:
  İSTENEN (> 0,3 mm³ = KALDI):
    1 · ray komşuları: aynı raydaki her cihaz çifti (STEP cihazları + iC60N kutuları + klemensler) katı kesişimi · en yakın aralık
    2 · montaj plakası (pano_montaj_plakasi) ile kesişim
    3 · pano gövdesi 400 × 350 × 250 (pano_ana_govde) + kapak + plaka burçları + rakorlar ile kesişim
    4 · cihaz pano iç hacminde mi (iç duvarlar · kapak iç yüzü · sınır kutusu payları) — sığmazsa AÇIKÇA yazılır, pano ölçüsü DEĞİŞTİRİLMEZ
  EK (bilgi / uyarı): DIN rayı kutusuyla bindirme (tırnak flanşın arkasına kıvrılır; ray modeli dolu kutu → beklenen) · pano kablo kanalları ·
    öbür raydaki cihazlar · eski (v3.4 kutu) dizilişle konum farkı
KOMUT: python test_qr_step_v35.py   (çıkış kodu 0 = istenen denetimler GEÇTİ)"""
import importlib, io, math, os, sys, time
sys.dont_write_bytecode = True
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import yama_qr_step_v35 as Y

ESIK = 0.3
STEP_AD = {"ana_salter_iSW_4P_40A": "A9S65440", "kacak_akim_iID_4P_40A_30mA": "A9R21440", "guc_24V_NDR-120-24": "NDR-120-24",
           "hmi_ana_bilgisayar_RevPi_Connect_4": "PR100378", "ag_anahtari_FL_SWITCH_1008N": "1085256"}


class SahteQR:
    PARCALAR = []


def kur(modul):
    P = {}
    def ekle(ad, sh, mal, birim, bom=None):
        assert ad not in P, ad
        P[ad] = dict(sh=sh, mal=mal, birim=birim, bom=bom)
    modul.kur(ekle, [], [], SahteQR)
    return P


def kutu(sh):
    b = sh.BoundingBox(); return (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)


def ust(a, b, p=0.0):
    return a[0] < b[1] + p and b[0] < a[1] + p and a[2] < b[3] + p and b[2] < a[3] + p and a[4] < b[5] + p and b[4] < a[5] + p


def kesisim(a, b):
    if not ust(kutu(a), kutu(b), 0.01): return 0.0
    try: return a.intersect(b).Volume()
    except Exception: return -1.0


def mesafe(a, b):
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    d = BRepExtrema_DistShapeShape(a.wrapped, b.wrapped); d.Perform()
    return d.Value() if d.IsDone() else -1.0


def main():
    t0 = time.time()
    hedef = os.path.join(H3, "h3_elk_qr_v1_STEP_TEST.py")
    Y.uygula(hedef=hedef)
    EQT = importlib.import_module("h3_elk_qr_v1_STEP_TEST")
    EQ0 = importlib.import_module("h3_elk_qr_v1")
    P = kur(EQT); P0 = kur(EQ0)
    print("kurulum: yamalı %d parça · eski %d parça · %.0f sn" % (len(P), len(P0), time.time() - t0))
    assert set(P) == set(P0), ("parça adları değişti", sorted(set(P) ^ set(P0)))
    AP = EQT.AP; x0, x1 = AP["x"]; y0, y1 = AP["y"]; z0, z1 = AP["z"]; t = AP["t"]
    IC = (x0 + t, x1 - t, y0 + t, y1 - t, z0 + 2.0, z1 - t)                                   # iç hacim: yan duvarlar · kapak iç yüzü (z0 + 2) · arka duvar
    cihaz = [a for a in P if a in STEP_AD or a.startswith(("sigorta_iC60N", "klemens_PT2_5"))]
    ray_of = {a: ("A" if abs((kutu(P[a]["sh"])[2] + kutu(P[a]["sh"])[3]) / 2.0 - EQT.RAY_A_Y) < abs((kutu(P[a]["sh"])[2] + kutu(P[a]["sh"])[3]) / 2.0 - EQT.RAY_B_Y) else "B") for a in cihaz}
    if True:                                                                              # STEP cihazında ray oluğu ortası = ray ortası (kutu ortası değil)
        import katalog_step_v1 as KS
        for a, k in STEP_AD.items(): ray_of[a] = "A" if k in ("A9S65440", "A9R21440") else "B"
    kal, uyari = [], []

    # ---------------- 0 · dizilim ----------------
    print("\n=== DİZİLİM (x · gerçek ölçü) ===")
    for r in ("A", "B"):
        L = sorted([a for a in cihaz if ray_of[a] == r], key=lambda a: kutu(P[a]["sh"])[0])
        print("ray %s (y %.0f):" % (r, EQT.RAY_A_Y if r == "A" else EQT.RAY_B_Y))
        for a in L:
            b = kutu(P[a]["sh"]); b0 = kutu(P0[a]["sh"])
            if a.startswith("klemens_PT2_5") and a not in ("klemens_PT2_5_00", "klemens_PT2_5_15"): continue
            print("   %-36s x %7.1f–%7.1f (w %5.1f) y %7.1f–%7.1f z %6.1f–%6.1f  %s | v3.4 kutu x %7.1f–%7.1f" % (
                a, b[0], b[1], b[1] - b[0], b[2], b[3], b[4], b[5], ("STEP " + STEP_AD[a]) if a in STEP_AD else "kutu", b0[0], b0[1]))

    # ---------------- 1 · ray komşuları ----------------
    print("\n=== 1 · RAY KOMŞULARI (katı kesişimi > %.1f mm³ = KALDI) ===" % ESIK)
    for r in ("A", "B"):
        L = sorted([a for a in cihaz if ray_of[a] == r], key=lambda a: kutu(P[a]["sh"])[0])
        for i in range(len(L)):
            for j in range(i + 1, len(L)):
                a, b = L[i], L[j]; v = kesisim(P[a]["sh"], P[b]["sh"])
                komsu = j == i + 1
                if komsu and (a in STEP_AD or b in STEP_AD):
                    d = mesafe(P[a]["sh"], P[b]["sh"])
                    print("   %s  %-34s ↔ %-34s kesişim %7.2f mm³ · en yakın %5.2f mm" % ("KALDI" if (v > ESIK or v < 0) else "tamam", a, b, v, d))
                if v > ESIK or v < 0:
                    kal.append(("komşu", a, b, v))
                    if not (komsu and (a in STEP_AD or b in STEP_AD)): print("   KALDI  %-34s ↔ %-34s kesişim %7.2f mm³" % (a, b, v))

    # ---------------- 2 · 3 · plaka · pano gövdesi · kapak · burç · rakor ----------------
    print("\n=== 2 · 3 · MONTAJ PLAKASI + PANO GÖVDESİ / KAPAK / BURÇ / RAKOR ===")
    pano = ["pano_montaj_plakasi", "pano_ana_govde_400x350x250", "onyuz_ana_pano_kapagi"] + sorted(a for a in P if a.startswith(("pano_plaka_burcu_", "pano_rakoru_")))
    for a in cihaz:
        vs = [(c, kesisim(P[a]["sh"], P[c]["sh"])) for c in pano]
        kotu = [(c, v) for c, v in vs if v > ESIK or v < 0]
        if a in STEP_AD or kotu:
            dp = mesafe(P[a]["sh"], P["pano_montaj_plakasi"]["sh"]) if a in STEP_AD else float("nan")
            print("   %s  %-36s plaka %6.2f · gövde %6.2f · kapak %6.2f mm³ · plakaya aralık %5.2f mm%s" % (
                "KALDI" if kotu else "tamam", a, vs[0][1], vs[1][1], vs[2][1], dp, ("  ← " + ", ".join("%s %.1f" % kv for kv in kotu)) if kotu else ""))
        for c, v in kotu: kal.append(("pano", a, c, v))
    print("   (iC60N kutuları + klemensler de denetlendi: %s)" % ("sorun yok" if not [k for k in kal if k[0] == "pano" and k[1] not in STEP_AD] else "SORUN VAR"))

    # ---------------- 4 · iç hacim ----------------
    print("\n=== 4 · PANO İÇ HACMİ (400 × 350 × 250 · iç x %.1f–%.1f · y %.1f–%.1f · z %.1f (kapak iç yüzü)–%.1f) ===" % IC)
    for a in cihaz:
        b = kutu(P[a]["sh"])
        pay = (b[0] - IC[0], IC[1] - b[1], b[2] - IC[2], IC[3] - b[3], b[4] - IC[4], IC[5] - b[5])
        ic = min(pay) >= 0.0
        if not ic: kal.append(("hacim", a, "dışarı taşıyor", min(pay)))
        if a in STEP_AD or not ic:
            print("   %s  %-36s pay: sol %6.1f sağ %6.1f alt %6.1f üst %6.1f ön(kapak) %6.1f arka %6.1f" % ("İÇİNDE" if ic else "SIĞMIYOR", a, *pay))

    # ---------------- EK · ray kutusu · kanallar · öbür ray ----------------
    print("\n=== EK (bilgi) ===")
    kanal = sorted(a for a in P if a.startswith("pano_kablo_kanali_"))
    for a in STEP_AD:
        r = "din_rayi_%s" % ray_of[a]; vr = kesisim(P[a]["sh"], P[r]["sh"])
        vk = [(c, kesisim(P[a]["sh"], P[c]["sh"])) for c in kanal]; kk = [(c, v) for c, v in vk if v > ESIK or v < 0]
        dk = min(mesafe(P[a]["sh"], P[c]["sh"]) for c in kanal if ust(kutu(P[a]["sh"]), kutu(P[c]["sh"]), 15.0)) if any(ust(kutu(P[a]["sh"]), kutu(P[c]["sh"]), 15.0) for c in kanal) else float("nan")
        print("   %-36s DIN rayı kutusu ∩ %7.1f mm³ (tırnak / kilit dili → beklenen) · kanal ∩ %s · en yakın kanal %s mm" % (
            a, vr, ", ".join("%s %.1f" % kv for kv in kk) if kk else "yok", ("%.2f" % dk) if dk == dk else "> 15"))
        for c, v in kk: uyari.append(("kanal", a, c, v))
    oA = [a for a in cihaz if ray_of[a] == "A"]; oB = [a for a in cihaz if ray_of[a] == "B"]
    capraz = [(a, b, kesisim(P[a]["sh"], P[b]["sh"])) for a in oA for b in oB if ust(kutu(P[a]["sh"]), kutu(P[b]["sh"]))]
    print("   ray A ↔ ray B cihazları: %s" % ("kesişim yok" if not [c for c in capraz if c[2] > ESIK] else capraz))
    for c in capraz:
        if c[2] > ESIK: uyari.append(("capraz",) + c)

    print("\n=== BOM (yamalı satırlar) ===")
    for a in list(STEP_AD) + ["sigorta_iC60N_1PN_C16_TOPPING"]:
        print("   %-36s %s" % (a, P[a]["bom"]))
    print("\n=== SONUÇ ===")
    print("İSTENEN DENETİMLER (komşu · plaka · pano · iç hacim): %s" % ("GEÇTİ" if not kal else "KALDI · %d bulgu" % len(kal)))
    for k in kal: print("   ", k)
    print("EK UYARI: %s" % ("yok" if not uyari else uyari))
    print("süre %.0f sn" % (time.time() - t0))
    return 0 if not kal else 1


if __name__ == "__main__":
    k = main()
    sys.stdout.flush(); os._exit(k)
