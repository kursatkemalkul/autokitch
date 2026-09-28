# -*- coding: utf-8 -*-
"""KATI / ÜRETİLEBİLİRLİK DENETİMİ v2 (28 Eyl 2026 · montaj v69 · Kemal: "düzelt, onaylıyorum yap")

v1 (denetim_kati_v1.py · montaj v68) ile aynı genel denetim (K1 katı · K2 geçerli · K3 kapalı boşluk · K4 hacim · K5 et kalınlığı · K6 gövde sayısı)
+ v69'da yapılan BEŞ ÜRETİM DÜZELTMESİNİN tek tek ölçümü (her biri GEÇTİ / KALDI):
  D1 kapak iç sacları tek parça (B 24 çekmece önü + K4 depo = 25 · TOPPING K1 / K2) · dış saclar da tek parça
  D2 ısı kalkanı sol sacı tek parça
  D3 E kapak masası = açıkça 2 levha (her biri tek parça) · TC ray örtüsü = 4 ayrı L şerit (her biri tek parça) · eski tek adlar yok
  D4 sucuk kaseti örümcekleri tek parça · Codex STEP çıkış tüpleri tek parça (kırıntı yok) — kaset üreteci + montajdaki TU kopyası
  D5 açıcı kolonu gerçek kutu profil (et 2V/A ≤ 6 mm · v68: 32 mm dolu blok)
Kullanım: python ob_calistir.py denetim_kati_v2.py · çıktı: denetim_kati_v2.json + ekrana özet."""
import io, json, os, re, sys, time, importlib
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U); os.chdir(U)
KOK = os.path.dirname(os.path.dirname(U))
t0 = time.time()
MONTAJ = "hat_montaj_v69.py"

# ---- 1 · montaj v69'un modül kurulum kısmı AYNEN (dosya yazmaz; glb/usdz/json yazımı çok sonra) ----
SRC = io.open(os.path.join(U, MONTAJ), encoding="utf-8").read()
_kes = SRC.index('_dis_birim(TZ, "GERCEK_TEZGAH"'); _kes = SRC.index("\n", _kes) + 1
G = {"__name__": "denetim_kati", "__file__": os.path.join(U, MONTAJ)}
_orj_stdout = sys.stdout
sys.stdout = io.StringIO()                                   # montajın kurulum çıktısı gizli
try:
    exec(compile(SRC[:_kes], MONTAJ + "[kurulum]", "exec"), G)
finally:
    _kurulum_cikti = sys.stdout.getvalue(); sys.stdout = _orj_stdout
print("[%3.0f sn] montaj v69 modülleri kuruldu (%d satır kurulum çıktısı gizlendi)" % (time.time() - t0, _kurulum_cikti.count("\n"))); sys.stdout.flush()


def tek(sh):
    if isinstance(sh, cq.Workplane):
        _v = [o for o in sh.vals() if isinstance(o, cq.Shape)]
        sh = _v[0] if len(_v) == 1 else cq.Compound.makeCompound(_v)
    return sh


# TOPPING mekanizması (TC) montajda sonradan kurulur → burada kur · kasetler: montajın kullandığı Codex parçalarıyla (v69: kırıntı süzgeci montajla aynı)
TC = G["TC"]; TC.PARCALAR[:] = []; TC.modul()
KASET = []
for modul, codex in (("kasar_cad_v14", {"helezon_B": "kasar_v2/cad/helezon_B_v15.step", "helezon_C": "kasar_v2/cad/helezon_C_v15.step",
                                         "helezon_D": "kasar_v2/cad/helezon_D_v15.step", "cikis_tupu": "kasar_v2/cad/cikis_tupu_v15.step"}),
                     ("sucuk_cad_v8", {"helezon_D": "sucuk_v2/cad/helezon_D_v2.step", "cikis_tupu": "sucuk_v2/cad/cikis_tupu_v2.step"})):
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
            _ss = sorted(sh.solids().vals(), key=lambda s_: -s_.Volume())
            if len(_ss) > 1 and all(s_.Volume() < 1e-3 * _ss[0].Volume() for s_ in _ss[1:]):
                sh = cq.Workplane(obj=_ss[0])
        KASET.append(("C · kaset " + modul, p["ad"], p.get("mal", ""), tek(sh)))
print("[%3.0f sn] TC + kasetler kuruldu" % (time.time() - t0)); sys.stdout.flush()


def sekil(M, p):
    if hasattr(M, "dunya"):
        x = M.dunya(p)
    else:
        x = p.get("wp", p.get("sh"))
    return tek(x)


MODUL = [("B · çekmeceli dolap (store_cad_v9)", G["SC"], "PARCALAR"), ("A · açıcı kabini (acici_kabin_cad_v1)", G["AK"], "PARCALAR"),
         ("A/C · kaide (kaide_cad_v2)", G["KD"], "PARCALAR"), ("C · TOPPING TU (topping_uno_cad_v15)", G["TU"], "P"),
         ("C · TOPPING mekanizma TC (topping_cad_v26)", TC, "PARCALAR"), ("F · fırın (firin_tp10_cad_v8)", G["FT"], "PARCALAR"),
         ("F · fırın üstü kabin (firin_ust_kabin_cad_v1)", G["FU"], "PARCALAR"), ("aktarma iticisi (itici_cad_v5)", G["IT"], "PARCALAR"),
         ("K · kesme + sprey (kesme_cad_v6)", G["KS"], "PARCALAR"), ("K altı · bulaşık (bulasik_cad_v2)", G["BM"], "PARCALAR"),
         ("E · kutu katlama (kutu_cad_v8)", G["KC"], "PARCALAR"), ("S · QR dolabı (qr_cad_v1)", G["QR"], "PARCALAR"),
         ("S · tezgâh (tezgah_cad_v1)", G["TZ"], "PARCALAR"), ("ray ekleri (ray_ek_cad_v1)", G["RE"], "PARCALAR")]
TUM = []
for ad_m, M, alan in MODUL:
    for p in getattr(M, alan):
        TUM.append((ad_m, p["ad"], p.get("mal", ""), sekil(M, p)))
TUM += KASET

# montajda görünen parça adları (parca_kutulari.json · montaj v69 yazdı)
PK = json.load(io.open(os.path.join(KOK, "otonom", "hat3d", "parca_kutulari.json"), encoding="utf-8"))
MONTAJ_ADLAR = {str(e[0]).split(":")[-1] for L_ in PK.get("parca", {}).values() for e in L_ if e}      # {birim: [[ad, grup, x0, x1, y0, y1, z0, z1], …]}

SAC_MAL = ("sac", "kabuk", "tava", "on_seffaf", "ayirma_saci", "fircali", "paslanmaz")
bulgu = {"KATI_DEGIL": [], "GECERSIZ": [], "IC_BOSLUK": [], "HACIM_YOK": [], "INCE_SAC": [], "COK_GOVDE": []}
say = 0; kal = []
OLCU = {}                                                     # (modül, ad) → (gövde sayısı, 2V/A, hacim, kutu hacmi)
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
    _bb = sh.BoundingBox()
    OLCU[(ad_m, ad)] = (len(sol), 2.0 * V / A if A > 0 else 0.0, V, _bb.xlen * _bb.ylen * _bb.zlen)
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
        bulgu.setdefault("KALIN_SAC", []).append((ad_m, ad, mal, round(t, 1), (round(_bb.xlen, 1), round(_bb.ylen, 1), round(_bb.zlen, 1))))

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
tk = {}
for ad_m, ad, mal, t, n in kal:
    if mal in ("sac", "kabuk", "tava"):
        b_ = round(t * 2) / 2.0
        tk[b_] = tk.get(b_, 0) + 1
print("SAC ET KALINLIĞI dağılımı (2·V/A, 0,5 mm'ye yuvarlı · sac/kabuk/tava): " + " · ".join("%.1f mm: %d" % kv for kv in sorted(tk.items())))

# ---- 2 · v69 DÜZELTMELERİ tek tek ----
SONUC = []


def olc(on_ek, ad):
    L = [(k[0], v) for k, v in OLCU.items() if k[0].startswith(on_ek) and k[1] == ad]
    return L[0][1] if len(L) == 1 else None


def d(ad_, gecti, deger):
    SONUC.append((ad_, bool(gecti), deger))
    print("  %s · %s · %s" % ("GEÇTİ" if gecti else "KALDI", ad_, deger))


print("v69 DÜZELTME KONTROLÜ")
# D1 · kapak iç + dış sacları
B_ = "B · "
_ic = sorted(a for (m, a) in OLCU if m.startswith(B_) and a.endswith("_ic_sac_1.0"))
_ds = sorted(a for (m, a) in OLCU if m.startswith(B_) and a.endswith("_dis_sac_1.5"))
_kotu = [(a, OLCU[(m, a)][0]) for (m, a) in OLCU if m.startswith(B_) and (a.endswith("_ic_sac_1.0") or a.endswith("_dis_sac_1.5")) and OLCU[(m, a)][0] != 1]
d("D1 · B kapak iç sacları (24 çekmece önü + K4 depo = 25) tek parça", len(_ic) == 25 and len(_ds) == 25 and not _kotu, "%d iç sac · %d dış sac · çok gövdeli: %s" % (len(_ic), len(_ds), _kotu))
for k_ in ("K1", "K2"):
    a_, b_ = olc("C · TOPPING TU", "onyuz_%s_ic_sac" % k_), olc("C · TOPPING TU", "onyuz_%s_dis_sac" % k_)
    d("D1 · TOPPING %s iç sacı + dış sacı tek parça" % k_, a_ and b_ and a_[0] == 1 and b_[0] == 1, "iç %s gövde · dış %s gövde" % (a_ and a_[0], b_ and b_[0]))
# D2
a_ = olc(B_, "isi_kalkani_sol_sac")
d("D2 · ısı kalkanı sol sacı tek parça", a_ and a_[0] == 1, "%s gövde · et %.2f mm" % (a_ and a_[0], a_[1] if a_ else -1))
# D3
_m = [olc("E · ", "kapak_masasi_%d" % i) for i in (0, 1)]
d("D3 · E kapak masası 2 levha, her biri tek parça · eski 'kapak_masasi' yok", all(x and x[0] == 1 for x in _m) and olc("E · ", "kapak_masasi") is None,
  "levhalar %s gövde" % [x and x[0] for x in _m])
_r = [olc("C · TOPPING mekanizma", "ray_ortu_catisi_%s_%s" % (u, y)) for u in ("on", "arka") for y in ("a", "b")]
d("D3 · TC ray örtüsü 4 ayrı L şerit, her biri tek parça · eski adlar yok", all(x and x[0] == 1 for x in _r)
  and olc("C · TOPPING mekanizma", "ray_ortu_catisi_on") is None and olc("C · TOPPING mekanizma", "ray_ortu_catisi_arka") is None,
  "şeritler %s gövde" % [x and x[0] for x in _r])
# D4
for on_ek, fmt in (("C · kaset sucuk_cad_v8", "%s"), ("C · TOPPING TU", "sucuk_cad_v8__%s")):
    _o = [olc(on_ek, fmt % ("orumcek_" + y)) for y in ("arka", "orta", "on")]
    d("D4 · sucuk örümcekleri tek parça (%s)" % on_ek, all(x and x[0] == 1 for x in _o), "%s gövde" % [x and x[0] for x in _o])
for on_ek, ad_ in (("C · kaset sucuk_cad_v8", "cikis_tupu"), ("C · kaset kasar_cad_v14", "cikis_tupu"), ("C · TOPPING TU", "sucuk_cad_v8__cikis_tupu"), ("C · TOPPING TU", "kasar_cad_v14__cikis_tupu")):
    a_ = olc(on_ek, ad_)
    d("D4 · Codex çıkış tüpü tek parça (%s · %s)" % (on_ek, ad_), a_ and a_[0] == 1, "%s gövde · hacim %.0f mm³" % (a_ and a_[0], a_[2] if a_ else -1))
# D5
a_ = olc("C · TOPPING mekanizma", "acici_kolonu")
d("D5 · açıcı kolonu kutu profil (2V/A ≤ 6 mm · hacim < kutu zarfının %40'ı)", a_ and a_[0] == 1 and a_[1] <= 6.0 and a_[2] < 0.4 * a_[3],
  "%s gövde · et 2V/A %.2f mm · hacim %.0f cm³ (zarf %.0f cm³ · oran %.2f)" % (a_ and a_[0], a_[1], a_[2] / 1000.0, a_[3] / 1000.0, a_[2] / a_[3]) if a_ else "yok")
# kapalı boşluk: yalnız gerçekten kapalı kaplar kalmalı
_ib = sorted(x[1] for x in bulgu["IC_BOSLUK"])
print("  bilgi · kapalı boşluklu parçalar: %s" % _ib)
_kaldi = [x for x in SONUC if not x[1]]
print("v69 DÜZELTME KONTROLÜ: %d / %d GEÇTİ%s" % (len(SONUC) - len(_kaldi), len(SONUC), "" if not _kaldi else " · KALDI: " + "; ".join(x[0] for x in _kaldi)))
json.dump(dict(tarih=time.strftime("%Y-%m-%d %H:%M"), montaj=MONTAJ, parca=say, modul=modul_say, bulgu={k: [list(map(str, x)) for x in v] for k, v in bulgu.items()},
               kalinlik=tk, v69_duzeltme=[list(map(str, x)) for x in SONUC]), io.open(os.path.join(U, "denetim_kati_v2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("toplam %.0f sn · denetim_kati_v2.json" % (time.time() - t0))
