# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 44 · B ÇEKMECE ÜNİTESİ DÜZELTMELERİ (4 Eki 2026 · Claude · YEREL · Kemal onayı: tek çekmece montaj animasyonu v2 geri bildirimi)
python 44_cekmece_duzeltme.py girdi.glb cikti.glb      (zincir: hat3_v9k.glb → hat3_v9l.glb)

21 çekmecenin hepsine (CEK_K*_*), her çekmecenin SOL / SAĞ sabit rayına göre ötelenerek (geometri: cek3geo.py — montaj animasyonu v3 ile ORTAK):
 A1  kayış çenesi kola kaynaklı değil: kol (kutuya kaynaklı) + kol tablası 2,5 (kola kaynaklı, 2 × Ø3,4) · ayrı çene bloğu = alt gövde (alt çene 2,5 + ara 1,2 TIG)
     + üst çene 2,5 · 2 × ISO 7380 M3 × 12 + 2 × ISO 4032 M3 (tabla + üst çene + ara + alt çene) — çekmece AÇIKKEN takılır.
     Mıknatıs (Littelfuse 57135) tablaya kaynaklı 2 mm kulağa: 2 × ISO 7380 M3 × 8 → 2 × PEM CLS-M3-2 · mıknatısta 2 yarık (Ø3,18 × 7,82).
 A3  sensör plakası (arka duvar, kablo kanalı köşesinin içinde, lamaya bağsız) KALDIRILDI — lama uzatılamaz (ELK_IC köşesi z −756,8'de), plaka işlevsiz.
 RD  reed sensörler (Littelfuse 59135, 2 adet) 2 mm reed plakasına (lamaya punta): 2 × ISO 7380 M3 × 8 → 2 × PEM CLS-M3-2 · sensörde 2 yarık · sensör +2 mm sağa.
 AV  avara mili 1469,2 → 1482,0 (+1 mm), E segman yuvası Ø5 × 0,75 + DIN 6799 RS 5 · mil avara kasnağıyla eş eksenli (eski mil 0,25 mm kaçıktı).
 MB  motor braketi delikli (2 × M5 havşa, 4 × M3 havşa) + 2 × DIN 7991 M5 × 6 + arka iç sacda 2 × PEM SP-M5-1 (Ø6,4 delik) + 2 köpük kapağı (PU cebi)
     + 4 × DIN 7991 M3 × 6 (motor yüzünde 4 × M3 dişli delik, derinlik 5) + motor kasnağı DIN 913 M3 × 4 setskur (radyal delik).
 PR  (v2 önerisi kör perçin UYGULANMADI: Ø6,5 perçin başı ön çerçevenin önünde üst çekmecenin fitiline biniyor — çerçeve önü tümüyle fitil oturma yüzeyi.
     Avara kolu ön flanşı çerçevenin ARKASINA içeriden TIG köşe dikişiyle bağlanır; modelde dikiş yok, animasyonda gösterilir.)
 KB  kızak köşebendi 1,5 × 4 + 4 × ISO 7380 M4 × 6 + kızak lamalarında 2 × M4 dişli kör delik (sol + sağ).
 OB  ön braketlerde 2 × Ø5,5 + 4 × PEM FHS-M5-10 saplama (kapak iç paneli) + 4 × DIN 125 M5 + 4 × ISO 4032 M5.
 PU  ön kapak içine PU köpük (dış kabuk ↔ iç panel arası; kapak kutusu − 1,5).
 KK  ray vidası köpük kapakları (126) 1 mm derin + PU cebi 1 mm derin → DIN 7991 M5 × 6 ucu kapağa basmaz.
Kaynak dikişleri / puntalar modelde yok (montaj animasyonunda gösterilir)."""
import os, sys, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
sys.path.insert(0, os.environ.get("CEK3GEO") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "veri"))
import cek3geo as C
import manifold3d as mf

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
g = Glb(gi)
KAYIT = dict(cekmece={}, sayim={})


def bc(d):
    g._bc.pop(d, None); g.bilesen(d, 0); return g._bc[d]


def bul(d, lo, ext=None, tol=0.3, coklu=False):
    L = [b for b in bc(d) if np.all(np.abs(b["lo"] - lo) < tol) and (ext is None or np.all(np.abs((b["hi"] - b["lo"]) - ext) < tol))]
    if coklu: return L
    return L[0] if len(L) == 1 else None


def tri(man, d):
    return SE.mf_P(man.translate([float(x) for x in d]))


def ekle(dugum, man, lab, d):
    P = tri(man, d); kat, mek, kpk = lab
    g.ekle_dugum(dugum, P, kat=kat, mek=mek, kpk=kpk); return len(P)


def degistir(b, P):
    ilk = [True]
    def f(_):
        if ilk[0]: ilk[0] = False; return P
        return None
    g.donustur(b, f)


def kes(d, b, kesiciler, dv):
    P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])
    m = SE.mf_ucgen(P)
    if m is None: return None
    k = None
    for c in kesiciler:
        c = c.translate([float(x) for x in dv]); k = c if k is None else k + c
    v0 = m.volume(); n = m - k; v1 = n.volume()
    if v0 - v1 < 1e-3: return 0.0
    degistir(b, SE.mf_P(n)); return v0 - v1


def birlesik(D):
    out = None
    for v in D.values():
        if isinstance(v, tuple): v = v[0] + v[1]
        out = v if out is None else out + v
    return out


CEK = sorted(set(n.get("name", "").split("__")[0] for n in g.J["nodes"] if n.get("name", "").startswith("CEK_")))
LOG("adım 44: %d çekmece" % len(CEK))
assert len(CEK) == 21
A1, RD, AV, MO = C.geo_a1(), C.geo_reed(), C.geo_avara(), C.geo_motor()
KM = C.kes_motor()
KO = C.geo_kose()
ORTAK = dict(sac=[], pu=[], cerceve=[], pas=[], conta=[])      # B_KASA'ya sonra uygulanacak (kesici / eleman, öteleme)
LAB_PAS = LAB_CONTA = None
for ck in CEK:
    n_cel, n_cc, n_pl, n_plc, n_al, n_mo, n_on = (ck + "__celik", ck + "__celik__CEKMECE", ck + "__plastik", ck + "__plastik__CEKMECE",
                                                 ck + "__aluminyum", ck + "__motor", ck + "__on_seffaf__CEKMECE")
    raylar = sorted([b for b in bc(n_cel) if np.all(np.abs((b["hi"] - b["lo"]) - [8.5, 45.7, 700.0]) < 0.1)], key=lambda b: b["lo"][0])
    assert len(raylar) == 2, (ck, len(raylar))
    R, Rr = raylar[0]["lo"], raylar[1]["lo"]; dL = R - C.R0; dR = Rr - C.RR0
    rk = dict(dL=np.round(dL, 2).tolist(), dR=np.round(dR, 2).tolist(), yapilan=[])
    rel = lambda v: C.R0 + np.asarray(v, float) + dL
    # ---- A1: kayış laması (kol + çene tek parça) → ayrı parçalar
    b = bul(n_cc, rel([17.0, 37.45, -74.0]), [13.0, 6.26, 184.0]); assert b is not None, (ck, "kayış laması")
    b2 = bul(n_cc, rel([17.0, 43.71, -74.0]), [6.35, 2.29, 28.57]); assert b2 is not None, (ck, "mıknatıs ayağı")
    lab_cc = g.etiket_b(b); g.sil_b(b); g.sil_b(b2)
    for k in ("kol", "tabla", "kulak", "cene_alt", "cene_ust", "vida_cene_1", "vida_cene_2", "somun_cene_1", "somun_cene_2",
              "pem_kulak_1", "pem_kulak_2", "vida_miknatis_1", "vida_miknatis_2"):
        ekle(n_cc, A1[k], lab_cc, dL)
    b = bul(n_plc, rel([17.0, 46.0, -74.0]), [6.35, 19.05, 28.57]); assert b is not None, (ck, "mıknatıs")
    lab = g.etiket_b(b); g.sil_b(b); ekle(n_plc, A1["miknatis"], lab, dL)
    rk["yapilan"].append("A1 çene bloğu ayrı + tabla + kulak + mıknatıs")
    # ---- reed sensörler + plakalar
    av = [b for b in bc(n_cel) if np.all(np.abs(b["lo"][[0, 2]] - rel([1.0, 18.0, 648.0])[[0, 2]]) < 0.3) and abs((b["hi"] - b["lo"])[0] - 24.7) < 0.3]
    assert len(av) == 1, (ck, "avara braketi", len(av))
    av = av[0]; lab_cel = g.etiket_b(av)
    for k in ("arka", "on"):
        zr = C.RZ[k][0] - C.R0[2]
        b = bul(n_pl, rel([10.05, 46.0, zr]), [6.35, 19.05, 28.57]); assert b is not None, (ck, "reed", k)
        lab = g.etiket_b(b); g.sil_b(b); ekle(n_pl, RD["reed_" + k], lab, dL)
        for e in ("reed_plaka_%s" % k, "pem_reed_%s_1" % k, "pem_reed_%s_2" % k, "vida_reed_%s_1" % k, "vida_reed_%s_2" % k):
            ekle(n_cel, RD[e], lab_cel, dL)
    rk["yapilan"].append("reed × 2 + plaka + PEM + vida")
    # ---- A3: sensör plakası (+ arka duvardaki küçük artıklar) kaldırılır
    sil = [b for b in bc(n_cel) if -113.6 < b["lo"][2] - R[2] < -110.4 and b["lo"][0] - R[0] < 17.0 and (b["hi"] - b["lo"])[0] < 17.0]
    for b in sil: g.sil_b(b)
    rk["yapilan"].append("A3 sensör plakası sil (%d bileşen)" % len(sil))
    # ---- avara mili + segman
    b = bul(n_cel, rel([15.7, 23.09, 673.02]), [11.8, 5.91, 5.96]); assert b is not None, (ck, "avara mili")
    P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]]).copy()
    uc = P[..., 0].max(); P[..., 0][np.abs(P[..., 0] - uc) < 0.01] += C.MIL_X1_YENI - C.MIL_X1          # mil ucu +1 mm (kasnakla aynı çokgen korunur)
    m = SE.mf_ucgen(P); assert m is not None, (ck, "mil kapalı değil")
    degistir(b, SE.mf_P(m - C.kes_segman_yuvasi().translate([float(x) for x in dL])))
    ekle(n_cel, AV["e_segman"], lab_cel, dL)
    # ---- motor braketi + vidalar + motor dişleri + setskur
    b = bul(n_cel, rel([27.5, 4.0, -113.0]), [43.0, 44.0, 38.5]); assert b is not None, (ck, "motor braketi")
    lab_mb = g.etiket_b(b); g.sil_b(b); ekle(n_cel, MO["motor_braketi"], lab_mb, dL)
    for k in ("vida_braket_1", "vida_braket_2", "vida_motor_1", "vida_motor_2", "vida_motor_3", "vida_motor_4"):
        ekle(n_cel, MO[k], lab_mb, dL)
    nk = 0
    for b in bc(n_mo):
        if b["lo"][0] - R[0] > 30.4 and b["hi"][0] - R[0] < 146.5:
            v = kes(n_mo, b, KM["motor"], dL); nk += 1 if v else 0
    assert nk >= 1, (ck, "motor dişli delik")
    b = bul(n_al, rel([15.5, 9.49, -108.88]), [11.0, 33.51, 33.75]); assert b is not None, (ck, "motor kasnağı")
    lab_al = g.etiket_b(b); kes(n_al, b, KM["kasnak"], dL); ekle(n_al, MO["setskur"], lab_al, dL)
    for k in ("pem_arka_1", "pem_arka_2"): ORTAK["pas"].append((MO[k], dL))
    for k in ("kopuk_kapagi_arka_1", "kopuk_kapagi_arka_2"): ORTAK["conta"].append((MO[k], dL))
    ORTAK["sac"] += [(c, dL) for c in KM["sac"]]; ORTAK["pu"] += [(c, dL) for c in KM["pu"]]
    rk["yapilan"].append("motor braketi delikli + 2 M5 + 4 M3 + motor dişleri (%d) + setskur" % nk)
    # ---- köşebent + M4 + lama dişleri
    for yan, dv, lo_rel in (("sol", dL, C.R0 + [12.7, 0.0, 80.0]), ("sag", dR, C.RR0 + [-21.5, 0.0, 80.0])):
        b = bul(n_cc, lo_rel + dv, [17.3, 6.0, 616.0]); assert b is not None, (ck, "lama", yan)
        lab = g.etiket_b(b); kes(n_cc, b, C.kes_lama(yan), dv)
        for kd in C.kose_list():
            if kd["yan"] != yan: continue
            ekle(n_cc, KO[kd["ad"]][0] + KO[kd["ad"]][1], lab, dv); ekle(n_cc, KO["vida_" + kd["ad"]], lab, dv)
    rk["yapilan"].append("köşebent × 4 + M4 × 4 + lama dişleri")
    # ---- ön braketler + saplamalar
    nb = 0
    for yan, dv, x_rel in (("sol", dL, C.R0[0] + 30.0), ("sag", dR, C.RR0[0] - 36.5)):
        L = [b for b in bc(n_cc) if abs(b["lo"][0] - (x_rel + dv[0])) < 0.3 and abs((b["hi"] - b["lo"])[0] - 15.0) < 0.3 and abs((b["hi"] - b["lo"])[2] - 17.0) < 0.3
             and b["lo"][2] - R[2] > 690.0]
        if len(L) != 1: continue
        b = L[0]; lo, hi = b["lo"].copy(), b["hi"].copy(); lab = g.etiket_b(b)
        kes(n_cc, b, C.kes_stud(yan, lo, hi), np.zeros(3))
        for k, m in C.geo_stud(yan, lo, hi).items(): ekle(n_cc, m, lab, np.zeros(3))
        nb += 1
    rk["yapilan"].append("ön braket + saplama (%d braket)" % nb)
    # ---- ön kapak PU
    kp = [b for b in bc(n_on) if 30.0 < (b["hi"] - b["lo"])[2] < 45.0 and (b["hi"] - b["lo"])[0] > 400.0] if any(p["name"] == n_on for p in g.prims) else []
    for b in kp:
        ekle(n_on, C.geo_kapak_pu(b["lo"], b["hi"]), g.etiket_b(b), np.zeros(3))
    rk["yapilan"].append("kapak PU (%d)" % len(kp))
    KAYIT["cekmece"][ck] = rk
    LOG("  %s · dL %s · %s" % (ck, rk["dL"], " · ".join(rk["yapilan"])))
    g._bc.clear()

# ---- B_KASA: arka iç sac PEM delikleri, PU cepleri, çerçeve perçin delikleri, PEM + köpük kapağı ekle
def ortak_kes(d, L, ad):
    n = 0
    for b in bc(d):
        ks = [(c, dv) for c, dv in L if np.all(np.asarray(c.bounding_box()[3:]) + dv >= b["lo"] - 0.1) and np.all(np.asarray(c.bounding_box()[:3]) + dv <= b["hi"] + 0.1)]
        if not ks: continue
        P = np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]]); m = SE.mf_ucgen(P)
        if m is None: LOG("  UYARI %s[%d] kapalı değil, kesilemedi" % (d, b["no"])); continue
        k = None
        for c, dv in ks:
            c = c.translate([float(x) for x in dv]); k = c if k is None else k + c
        v0 = m.volume(); nn = m - k; dv_ = v0 - nn.volume()
        if dv_ > 1e-3: degistir(b, SE.mf_P(nn)); n += 1; LOG("  %s: %s[%d] −%.1f mm³ (%d kesici)" % (ad, d, b["no"], dv_, len(ks)))
    g._bc.clear(); return n


ortak_kes("B_KASA__sac", ORTAK["sac"], "arka iç sac PEM deliği")
ortak_kes("B_KASA__pu", ORTAK["pu"], "PU köpük kapağı cebi")
ornek_pas = [b for b in bc("B_KASA__paslanmaz") if np.all(np.abs((b["hi"] - b["lo"]) - [2.0, 8.89, 8.88]) < 0.1)][0]
lab_pas = g.etiket_b(ornek_pas)
for m, dv in ORTAK["pas"]: ekle("B_KASA__paslanmaz", m, lab_pas, dv)
# ---- köpük kapakları 1 mm derin (ray vidaları, 126) + PU cebi
KAP = [b for b in bc("B_KASA__conta") if np.all(np.abs((b["hi"] - b["lo"]) - [1.83, 10.48, 10.48]) < 0.06)]
LOG("  ray vidası köpük kapağı: %d (beklenen 126)" % len(KAP))
assert len(KAP) == 126
lab_conta = g.etiket_b(KAP[0])
PEMR = [b for b in bc("B_KASA__paslanmaz") if np.all(np.abs((b["hi"] - b["lo"]) - [2.0, 8.89, 8.88]) < 0.1)]
pu_kes = []
kutular = []
for b in KAP:
    c = (b["lo"] + b["hi"]) / 2
    pm = min(PEMR, key=lambda q: np.linalg.norm((q["lo"] + q["hi"]) / 2 - c)); pc = (pm["lo"] + pm["hi"]) / 2
    yon = -1.0 if pc[0] > c[0] else 1.0                                   # taban PEM'in tersi yönde
    taban = b["lo"][0] if yon < 0 else b["hi"][0]
    kutular.append((b["lo"].copy(), b["hi"].copy(), yon, taban))
    pu_kes.append((C.G.silindir((taban - yon * 0.01, c[1], c[2]), (yon, 0, 0), 5.24, 1.0 + 0.01, 40), np.zeros(3)))
for lo, hi, yon, taban in kutular:
    g._bc.clear(); b = g.bilesen("B_KASA__conta", lo=lo, hi=hi, tol=0.05)
    esik = taban - yon * 0.81                                              # dış taban + iç taban (0,8 et) düzlemleri
    def f(Pw, _y=yon, _e=esik):
        m = (Pw[..., 0] - _e) * _y > 0
        Pw[..., 0][m] += _y * 1.0
        return Pw
    g.donustur(b, f)
g._bc.clear()
for m, dv in ORTAK["conta"]: ekle("B_KASA__conta", m, lab_conta, dv)
ortak_kes("B_KASA__pu", pu_kes, "PU cebi +1 mm (ray vidası kapağı)")
tmp = go + ".e1.glb"; g.kaydet(tmp); del g
SE.sikistir(tmp, go); os.remove(tmp)
KAYIT["sayim"] = dict(cekmece=len(CEK), ray_kapagi=len(KAP))
json.dump(KAYIT, open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
LOG("ADIM 44 bitti · %s · %.0f sn" % (go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
