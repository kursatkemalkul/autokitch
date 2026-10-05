# -*- coding: utf-8 -*-
"""Kalanlar 4 · mekanizma_v3_8.json yenile (v8zi): liste + kutu GLB'den (p3_json mantigi) · parca: kaldirilmis parcalar silinir
(esleme kutusunda dugumun ucgeni kalmadi / acik sil listesi), yeni parcalar (TOPPING paketi YENI kayitlari, hortumlar, K/B/QR eklemeleri,
KD3 kor tapalari) unite GLB etiketinden eklenir · sayfa_degisiklik.md temizligi uygulanir. python j4_json.py eski.json cache esleme.json yeni.json"""
import sys, json, re, collections, numpy as np
ej, cd, esj, yj = sys.argv[1:5]
S = r"@@KOK_W@@"
J = json.load(open(ej, encoding="utf-8"))
D = np.load(cd + "/m8_onbellek.npz"); PJ = json.load(open(cd + "/m8_parca.json", encoding="utf-8"))
MEK = PJ["MEK"]; KOD = [m["kod"] for m in MEK]
J["liste"] = [{"kod": m["kod"], "istasyon": m["istasyon"], "ad": m["ad"]} for m in MEK]
T = np.stack([D["A"], D["B"], D["C"]], 1); mek = D["mek"]; K = {}
for i, k in enumerate(KOD):
    m = mek == i
    if not m.any(): continue
    Q = T[m].reshape(-1, 3); lo = Q.min(0) / 1000; hi = Q.max(0) / 1000
    K[k] = [round(float(x), 4) for x in (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])]
J["kutu"] = {**{k: v for k, v in J["kutu"].items() if k in KOD and k not in K}, **K}
# dugum -> ucgen indeksleri (gorunur)
PAR = PJ["parca"]; TP = D["P"]
ad_p = np.array([p["ad"] for p in PAR])
TAD = ad_p[TP]
mn = T.min(1); mx = T.max(1)
dug_idx = collections.defaultdict(list)
for i, a in enumerate(TAD): pass
order = np.argsort(TAD, kind="stable"); sa = TAD[order]
u, st = np.unique(sa, return_index=True); en = list(st[1:]) + [len(sa)]
DI = {a: order[s:e] for a, s, e in zip(u, st, en)}
def kutuda(dug, lo, hi, e=0.6):
    ii = DI.get(dug)
    if ii is None: return 0, None
    m = np.all(mn[ii] >= np.asarray(lo) - e, 1) & np.all(mx[ii] <= np.asarray(hi) + e, 1)
    if not m.any(): return 0, None
    return int(m.sum()), collections.Counter(mek[ii[m]].tolist()).most_common(1)[0][0]
def dugum_unite(dug):
    ii = DI.get(dug); return collections.Counter(mek[ii].tolist()).most_common(1)[0][0]
BOY = collections.defaultdict(list)
for p in PAR: BOY[p["ad"]].append(np.array(p["hi"]) - np.array(p["lo"]))
def ayni_boy(dug, lo, hi, e=1.0):
    b = np.array(hi) - np.array(lo)
    return any(np.all(np.abs(np.sort(q) - np.sort(b)) < e) for q in BOY.get(dug, []))
# 1 · kaldirilanlar
ES = {}
for e in json.load(open(esj, encoding="utf-8"))["parca"]:
    if e["ad"]: ES.setdefault(e["dugum"].split("__")[0] + "|" + e["ad"], []).append(e)
SIL_ACIK = ("ELK_ANA_PANO_UF|ana_pano_harting_soketi_ROBOT", "ELK_ANA_PANO_UF|ana_pano_harting_soketi_A", "ELK_QR_MONTAJ|qr_giris_plakasi_a")
SIL_DESEN = re.compile(r"\|(ana_hat_(A|ROBOT)_|.*harting_ANA_PANO_(A|ROBOT)|qrk_.*ROBOT|giris_a_KT_20_robot_kablosu$)")
SIL_YOKSA = re.compile(r"\|ana_pano_sigorta_.*_(A|ROBOT)$")
DEGISEN = re.compile(r"\|(evap_kaseti_|.*_spreader_(kesme_valfi|valf_|hava_rakoru)|kablo_TOPPING_motor_(kasar|sucuk)_|soguk_arka_dis_sac$|soguk_ic_kaplama$|.*__pnomatik_(arka_mafsal|on_bogaz|on_ayak)$|harc_urun_hortumu_D32$)")
yp = {}; sil = []
for k, v in J["parca"].items():
    if k in SIL_ACIK or SIL_DESEN.search(k): sil.append((k, "acik/desen")); continue
    el = ES.get(k)
    if el:
        var = any(kutuda(e["dugum"], e["lo"], e["hi"])[0] or ayni_boy(e["dugum"], e["lo"], e["hi"]) for e in el)
        if not var and SIL_YOKSA.search(k): sil.append((k, "modelde yok (A/ROBOT sigortasi)")); continue
        if not var and DEGISEN.search(k): sil.append((k, "modelde yok · TOPPING paketinde yenisiyle degisti")); continue
    yp[k] = v
yp["D_PIZZA_YEDEK_UST|f_ust_pizza_kutusu_yigini"] = "F/Gövde"
# 2 · yeni parcalar
yeni = []
rx = re.compile(r"^\s*YENI\s+(\S+)\s+(\S+)\s+\[([-\d., ]+)\]")
for f in ("tp1_log.txt", "tp2_log.txt", "tp3_log.txt"):
    for ln in open(S + r"\tpaket\\" + f, encoding="utf-8", errors="ignore"):
        m = rx.match(ln)
        if not m: continue
        nd, ad, b = m.group(1), m.group(2), [float(x) for x in m.group(3).split(",")]
        dug = nd if nd.startswith(("ELK_", "TOPPING_")) else "TOPPING_MODUL__" + nd
        n, mk = kutuda(dug, (b[0], b[2], b[4]), (b[1], b[3], b[5]))
        if mk is None or mk < 0: continue
        yeni.append((dug.split("__")[0] + "|" + ad, KOD[mk]))
for h in ("kiyma_on", "kiyma_arka", "kusbasi_on", "kusbasi_arka", "harc_on", "harc_arka", "sos_on", "sos_arka",
          "harc_spreader_A", "harc_spreader_B", "sos_spreader_A", "sos_spreader_B"):
    u_ = "TOPPING/" + {"kiyma": "Kıyma", "kusbasi": "Kuşbaşı", "harc": "Harç", "sos": "Sos"}[h.split("_")[0]]
    yeni.append(("TOPPING_MODUL|hava_hortumu_" + h, u_ if u_ in KOD else KOD[dugum_unite("TOPPING_MODUL__hava_ana")]))
for dug, ad in (("ELK_K__kablo", "K_kablolari_arka_kanal_yolu"), ("K_ELEKTRIK__sac", "k_arka_kablo_kanali_ters_T"), ("ELK_K__celik", "k_kanal_braketi_x4"),
                ("ELK_K__celik", "k_inis_P_kelepceleri"), ("ELK_K__celik", "k_giris_alici_L_dilli_kelepce"), ("ELK_DOLAP__celik", "reed_kablo_POM_klipsi_x105"),
                ("ELK_QR_KABLO__celik", "qr_ust_kelepce_L_braketi"), ("ELK_TOPPING__rakor", "KD3_kor_tapa_O8_x4")):
    yeni.append((dug.split("__")[0] + "|" + ad, KOD[dugum_unite(dug)]))
for k, v in yeni:
    if k not in yp: yp[k] = v
for v in yp.values(): assert v in KOD, v
J["parca"] = yp
J["birim"] = {k: v for k, v in J["birim"].items() if v in KOD}
J["glb"] = "hat3_v8.glb (v8zi)"
J["surum"] = re.sub(r" · v8z.*$", "", J["surum"]) + " · v8zi parça listesi GLB'den yenilendi (kalkanlar silindi, TOPPING/QR/K/B yenileri eklendi)"
json.dump(J, open(yj, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("silinen", len(sil)); [print("  SIL", k, n) for k, n in sil]
print("yeni", len([k for k, v in yeni])); [print("  YENI", k, v) for k, v in yeni]
print("parca", len(yp), "· kutu", len(K), "· liste", len(J["liste"]), "· eksik kutu", [k for k in KOD if k not in K])
