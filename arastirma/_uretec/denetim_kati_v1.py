# -*- coding: utf-8 -*-
"""KATI / ÜRETİLEBİLİRLİK DENETİMİ v1 (28 Eyl 2026 · Kemal: "parçalar solid mi, yani içi boş sac parçalar falan var mı? üretime gidemeyecek")

Montaj v68'in kurduğu bütün modüllerin (B · A kabin + kaide · C TOPPING TU + TC · F fırın + üst kabin · itici · K + bulaşık · E · S QR + tezgâh ·
ray ekleri · kasetler) HER PARÇASI OCC B-rep olarak denetlenir:
  K1 katı mı            : en az 1 Solid (yüzey / kabuk / tel değil)
  K2 geçerli mi         : BRepCheck isValid
  K3 içi kapalı boşluk  : bir Solid'de 1'den fazla Shell = içinde kapalı hava cebi (tek parça üretilemez)
  K4 hacim              : > 0,1 mm³
  K5 et kalınlığı       : t ≈ 2·V/A (ince levhada tam kalınlık) · sac malzemelerde (sac · kabuk · on_seffaf sac · tava) 0,5 mm'nin altı = "kağıt sac"
  K6 gövde sayısı       : birden çok ayrık Solid (bilgi — ör. aynı adla modellenen bir çift)
Montaja girmeyen parçalar (parca_kutulari.json'da yok) ayrı sayılır. Yer tutucu birimler (robot, ray, pizza kutusu yığını) parça değil, KUTU — ayrı yazılır.
Kullanım: python ob_calistir.py denetim_kati_v1.py   (önbellekle ~3–4 dk) · çıktı: denetim_kati_v1.json + ekrana özet."""
import io, json, os, re, sys, time, importlib
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U); os.chdir(U)
KOK = os.path.dirname(os.path.dirname(U))
t0 = time.time()

# ---- 1 · montaj v68'in modül kurulum kısmı AYNEN (dosya yazmaz; glb/usdz/json yazımı çok sonra) ----
SRC = io.open(os.path.join(U, "hat_montaj_v68.py"), encoding="utf-8").read()
_kes = SRC.index('_dis_birim(TZ, "GERCEK_TEZGAH"'); _kes = SRC.index("\n", _kes) + 1
G = {"__name__": "denetim_kati", "__file__": os.path.join(U, "hat_montaj_v68.py")}
_orj_stdout = sys.stdout
sys.stdout = io.StringIO()                                   # montajın kurulum çıktısı gizli
try:
    exec(compile(SRC[:_kes], "hat_montaj_v68.py[kurulum]", "exec"), G)
finally:
    _kurulum_cikti = sys.stdout.getvalue(); sys.stdout = _orj_stdout
print("[%3.0f sn] montaj v68 modülleri kuruldu (%d satır kurulum çıktısı gizlendi)" % (time.time() - t0, _kurulum_cikti.count("\n"))); sys.stdout.flush()

# TOPPING mekanizması (TC) montajda sonradan kurulur → burada kur · kasetler: montajın kullandığı Codex parçalarıyla
TC = G["TC"]; TC.PARCALAR[:] = []; TC.modul()
KASET = []
for modul, codex in (("kasar_cad_v14", {"helezon_B": "kasar_v2/cad/helezon_B_v15.step", "helezon_C": "kasar_v2/cad/helezon_C_v15.step",
                                         "helezon_D": "kasar_v2/cad/helezon_D_v15.step", "cikis_tupu": "kasar_v2/cad/cikis_tupu_v15.step"}),
                     ("sucuk_cad_v7", {"helezon_D": "sucuk_v2/cad/helezon_D_v2.step", "cikis_tupu": "sucuk_v2/cad/cikis_tupu_v2.step"})):
    V = importlib.import_module(modul); V.PARCALAR[:] = []
    _o = sys.stdout; sys.stdout = io.StringIO()
    try:
        V.kap()
    finally:
        sys.stdout = _o
    for p in V.PARCALAR:
        sh = p["wp"]
        if p["ad"] in codex:
            sh = cq.importers.importStep(os.path.join(KOK, "arastirma", "3_TOPPING", codex[p["ad"]]))
        if isinstance(sh, cq.Workplane):
            _v = [o for o in sh.vals() if isinstance(o, cq.Shape)]
            sh = _v[0] if len(_v) == 1 else cq.Compound.makeCompound(_v)
        KASET.append(("KASET:" + modul, p["ad"], p.get("mal", ""), sh))
print("[%3.0f sn] TC + kasetler kuruldu" % (time.time() - t0)); sys.stdout.flush()


def sekil(M, p):
    if hasattr(M, "dunya"):
        x = M.dunya(p)
    else:
        x = p.get("wp", p.get("sh"))
    if isinstance(x, cq.Workplane):
        v = [o for o in x.vals() if isinstance(o, cq.Shape)]
        x = v[0] if len(v) == 1 else cq.Compound.makeCompound(v)
    return x


MODUL = [("B · çekmeceli dolap (store_cad_v8)", G["SC"], "PARCALAR"), ("A · açıcı kabini (acici_kabin_cad_v1)", G["AK"], "PARCALAR"),
         ("A/C · kaide (kaide_cad_v2)", G["KD"], "PARCALAR"), ("C · TOPPING TU (topping_uno_cad_v14)", G["TU"], "P"),
         ("C · TOPPING mekanizma TC (topping_cad_v25)", TC, "PARCALAR"), ("F · fırın (firin_tp10_cad_v8)", G["FT"], "PARCALAR"),
         ("F · fırın üstü kabin (firin_ust_kabin_cad_v1)", G["FU"], "PARCALAR"), ("aktarma iticisi (itici_cad_v5)", G["IT"], "PARCALAR"),
         ("K · kesme + sprey (kesme_cad_v6)", G["KS"], "PARCALAR"), ("K altı · bulaşık (bulasik_cad_v2)", G["BM"], "PARCALAR"),
         ("E · kutu katlama (kutu_cad_v7)", G["KC"], "PARCALAR"), ("S · QR dolabı (qr_cad_v1)", G["QR"], "PARCALAR"),
         ("S · tezgâh (tezgah_cad_v1)", G["TZ"], "PARCALAR"), ("ray ekleri (ray_ek_cad_v1)", G["RE"], "PARCALAR")]
TUM = []
for ad_m, M, alan in MODUL:
    for p in getattr(M, alan):
        TUM.append((ad_m, p["ad"], p.get("mal", ""), sekil(M, p)))
TUM += [("C · kasetler (kasar_cad_v14 · sucuk_cad_v7 + Codex STEP)", a, m, s) for _mm, a, m, s in KASET]

# montajda görünen parça adları (parca_kutulari.json · v62)
PK = json.load(io.open(os.path.join(KOK, "otonom", "hat3d", "parca_kutulari.json"), encoding="utf-8"))
MONTAJ_ADLAR = {str(e[0]).split(":")[-1] for L_ in PK.get("parca", {}).values() for e in L_ if e}      # {birim: [[ad, grup, x0, x1, y0, y1, z0, z1], …]}

SAC_MAL = ("sac", "kabuk", "tava", "on_seffaf", "ayirma_saci", "fircali", "paslanmaz")
bulgu = {"KATI_DEGIL": [], "GECERSIZ": [], "IC_BOSLUK": [], "HACIM_YOK": [], "INCE_SAC": [], "COK_GOVDE": []}
say = 0; kal = []
for ad_m, ad, mal, sh in TUM:
    say += 1
    try:
        sol = sh.Solids()
    except Exception:
        sol = []
    if not sol:
        bulgu["KATI_DEGIL"].append((ad_m, ad, mal, type(sh).__name__)); continue
    if not sh.isValid():
        bulgu["GECERSIZ"].append((ad_m, ad, mal))
    for s_ in sol:
        if len(s_.Shells()) > 1:
            bulgu["IC_BOSLUK"].append((ad_m, ad, mal, len(s_.Shells()), round(s_.Volume(), 1))); break
    V = sum(s_.Volume() for s_ in sol); A = sum(s_.Area() for s_ in sol)
    if V < 0.1:
        bulgu["HACIM_YOK"].append((ad_m, ad, mal, V)); continue
    t = 2.0 * V / A if A > 0 else 0.0
    kal.append((ad_m, ad, mal, round(t, 2), len(sol)))
    if (mal in SAC_MAL or re.search(r"(^|_)sac(_|$)|_saci", ad)) and t < 0.5:
        bulgu["INCE_SAC"].append((ad_m, ad, mal, round(t, 3)))
    if len(sol) > 1:
        _gv = sorted(((round(s_.Volume(), 1), tuple(round(v, 1) for v in (lambda b: (b.xlen, b.ylen, b.zlen))(s_.BoundingBox()))) for s_ in sol), reverse=True)
        bulgu["COK_GOVDE"].append((ad_m, ad, mal, len(sol), _gv))
    if mal in ("sac", "kabuk", "tava") and t > 4.0:
        _b = sh.BoundingBox(); bulgu.setdefault("KALIN_SAC", []).append((ad_m, ad, mal, round(t, 1), (round(_b.xlen, 1), round(_b.ylen, 1), round(_b.zlen, 1))))

print("[%3.0f sn] %d parça denetlendi" % (time.time() - t0, say))
modul_say = {}
for ad_m, *_ in TUM:
    modul_say[ad_m] = modul_say.get(ad_m, 0) + 1
for k_, v_ in modul_say.items():
    print("   %-58s %4d parça" % (k_, v_))
ACIK = {"KALIN_SAC": "sac malzemeli ama 2V/A > 4 mm (blok mu levha mı — bilgi)", "KATI_DEGIL": "katı değil (yüzey / kabuk / tel)", "GECERSIZ": "geçersiz B-rep (BRepCheck)", "IC_BOSLUK": "içinde kapalı boşluk (1'den çok kabuk)",
        "HACIM_YOK": "hacim ≈ 0", "INCE_SAC": "sac et kalınlığı < 0,5 mm", "COK_GOVDE": "birden çok ayrık gövde (bilgi)"}
for k_, L in bulgu.items():
    ic = [x for x in L if x[1] in MONTAJ_ADLAR]
    print("%-42s %4d  (montajda görünen %d)" % (ACIK[k_], len(L), len(ic)))
    for x in L[:400]:
        print("      · %s · %s · %s%s" % (x[0], x[1], x[2], (" · " + " · ".join(str(y) for y in x[3:])) if len(x) > 3 else ""))
# sac kalınlık dağılımı (sac malzemeli parçalar)
tk = {}
for ad_m, ad, mal, t, n in kal:
    if mal in ("sac", "kabuk", "tava"):
        b_ = round(t * 2) / 2.0
        tk[b_] = tk.get(b_, 0) + 1
print("SAC ET KALINLIĞI dağılımı (2·V/A, 0,5 mm'ye yuvarlı · sac/kabuk/tava): " + " · ".join("%.1f mm: %d" % kv for kv in sorted(tk.items())))
json.dump(dict(tarih=time.strftime("%Y-%m-%d %H:%M"), parca=say, modul=modul_say, bulgu={k: [list(map(str, x)) for x in v] for k, v in bulgu.items()},
               kalinlik=tk), io.open(os.path.join(U, "denetim_kati_v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("toplam %.0f sn · denetim_kati_v1.json" % (time.time() - t0))
