# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 55 · STANDART UYUM — PUL TEK STANDART (4 Eki 2026 · Claude · YEREL · KUYRUK 3 iş 1 · Kemal: "vidasından radiusuna, sac kalınlığına
bir uyum olsun; saçma sapan şeyler yapma")
python 55_uyum.py girdi.glb cikti.glb      (zincir: hat3_v9v.glb → hat3_v9w.glb)

Standart tablo: yama_v9/sac_standart/sac_uyum_v1.json (tek kaynak · 'pul' bölümü). Uyum denetimi (scratchpad gece2/k3_uyum/RAPOR.md) iki gereksiz çeşit buldu:
  P1 · M5 panel bağlantısı (FHP-M5 saplama / vida + pul + ISO 10511 somun, kulak / iskelet tarafında): A, K ve E'nin bir kısmı DIN 9021 (Ø15 × 1,2),
       E'nin kalanı, U_F, U_KE, F_UST ve B bağlantıları DIN 125-A / ISO 7089 (Ø10 × 1,0) — aynı işlev, iki pul. Pul 2–3 mm kulağa / profile basar
       (ince sac değil) → standart ISO 7089 M5. DIN 9021 M5 → ISO 7089 M5: dış çap 15 → 10, kalınlık 1,2 → 1,0; somun 0,2 mm sac tarafına kayar
       (saplama çıkıntısı 0,2 artar). Oturma yüzü (sac tarafı) yerinde kalır.
  P2 · M8 modül / arayüz cıvatası (ISO 4762 M8): DIN 9021 (Ø24 × 2: A→TOPPING, TOPPING→F, B şase), DIN 125 (Ø16 × 1,6: A açıcı flanşı, U_F, K) ve
       ISO 7092 (Ø15 × 1,6: A→B, TOPPING→B — Ø16 servis deliğinden geçmek zorunda) — aynı cıvata, üç pul. ISO 7092 silindir başlı (ISO 4762)
       cıvatanın kendi pulu ve her yerden geçer → standart ISO 7092 M8. DIN 9021 → ISO 7092: cıvata (ya da somun) 0,4 mm sac tarafına;
       DIN 125 → ISO 7092: yalnız dış çap 16 → 15 (kalınlık aynı, kayma yok).
Yöntem: pul bileşeni (halka: dış Ø × dış Ø × kalınlık, bağlantı düğümlerinde) bulunur; ekseni = en ince yön. Somun (pulun bir yüzüne değen, pulu
  geçmeyen, boyu ≤ 1,15 × ISO 10511 yüksekliği olan eş eksenli bileşen — perçin somun / PEM sayılmaz) varsa o taraf somun tarafıdır; yoksa pulu geçen en geniş eş eksenli bileşen cıvatadır ve başı pulun kısa
  uzandığı yandadır. Pul köşeleri radyal (iç çap aynı) ve eksenel (oturma yüzü sabit) ölçeklenir → üçgen yapısı aynı; baş / somun Δ kalınlık
  kadar sac tarafına ötelenir. Etiket (kat / mek / kpk) korunur. Beklenen sayılar tutmazsa DURUR."""
import os, sys, time, json, re, subprocess
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
HERE = os.path.dirname(os.path.abspath(__file__))
STD = json.load(open(os.path.join(HERE, "sac_standart", "sac_uyum_v1.json"), encoding="utf-8"))["pul"]
# eski tip → yeni tip (iç Ø, dış Ø, kalınlık)
TIP = {"DIN9021_M5": (5.3, 15.0, 1.2), "DIN125_M5": (5.3, 10.0, 1.0), "DIN9021_M8": (8.4, 24.0, 2.0), "DIN125_M8": (8.4, 16.0, 1.6),
       "ISO7092_M8": (8.4, 15.0, 1.6)}
DONUSUM = {"DIN9021_M5": STD["M5"]["tip"], "DIN9021_M8": STD["M8"]["tip"], "DIN125_M8": STD["M8"]["tip"]}
assert DONUSUM == {"DIN9021_M5": "DIN125_M5", "DIN9021_M8": "ISO7092_M8", "DIN125_M8": "ISO7092_M8"}, DONUSUM
BEKLENEN = {"DIN9021_M5": (90, 100), "DIN9021_M8": (18, 18), "DIN125_M8": (10, 20)}      # (en az, en çok) — denetimde sayıldı
DUGUM = re.compile(r"^(A_GOVDE|K_GOVDE|E_GOVDE|U_F_GOVDE|U_KE_GOVDE|F_UST_KABIN|B_KASA|B_BAGLANTI|B_MODULER|TOPPING_GOVDE|KAIDE_A|KAIDE_C|E_MODULER)__(paslanmaz|celik|baglanti)$")


def tip_bul(lo, hi):
    s = np.sort(hi - lo)
    for k, (di, do, h) in TIP.items():
        if abs(s[0] - h) < 0.06 and abs(s[1] - do) < 0.25 and abs(s[2] - do) < 0.25: return k
    return None


g = Glb(gi)
DUG = sorted(d for d in set(p["name"] for p in g.prims) if DUGUM.match(d))
BIL = {}
for d in DUG:
    g.bilesen(d, no=0); BIL[d] = list(g._bc[d])
TUM = [(d, b) for d in DUG for b in BIL[d]]
LO = np.array([b["lo"] for d, b in TUM]); HI = np.array([b["hi"] for d, b in TUM])
PULLAR = [(i, d, b, tip_bul(b["lo"], b["hi"])) for i, (d, b) in enumerate(TUM)]
PULLAR = [(i, d, b, t) for i, d, b, t in PULLAR if t in DONUSUM]
say = {}
for i, d, b, t in PULLAR: say[t] = say.get(t, 0) + 1
LOG("pul adayları: %s" % say)
for t, (a, z) in BEKLENEN.items():
    assert a <= say.get(t, 0) <= z, "ADIM 55 DUR: %s sayısı %d (beklenen %d–%d)" % (t, say.get(t, 0), a, z)

KAYIT = dict(adim=55, ad="pul tek standart (M5 ISO 7089 · M8 ISO 7092)", pul=[], say=say)
islem = []
for i, d, b, t in PULLAR:
    lo, hi = b["lo"], b["hi"]; s = hi - lo; k = int(np.argmin(s)); c = (lo + hi) / 2; dik = [j for j in range(3) if j != k]
    f_lo, f_hi = lo[k], hi[k]
    # eş eksenli komşular (pul hariç)
    m = (np.abs((LO[:, dik] + HI[:, dik]) / 2 - c[dik]).max(1) < 0.8) & (HI[:, k] > f_lo - 60) & (LO[:, k] < f_hi + 60)
    m[i] = False
    adaylar = [j for j in np.where(m)[0] if tip_bul(LO[j], HI[j]) is None]
    m_somun = 5.0 if t.endswith("M5") else 8.0                                     # ISO 10511 yüksekliği · perçin somun / PEM (uzun gövde) somun sayılmaz
    somun = [j for j in adaylar if (abs(LO[j, k] - f_hi) < 0.15 or abs(HI[j, k] - f_lo) < 0.15) and (HI[j] - LO[j])[dik].min() > TIP[t][0] * 1.3
             and (HI[j, k] - LO[j, k]) <= 1.15 * m_somun]
    if somun:
        assert len(somun) == 1, ("çok somun", d, b["no"])
        j = somun[0]; yan = +1 if abs(LO[j, k] - f_hi) < 0.15 else -1; ne = "somun"
    else:
        civ = [j for j in adaylar if LO[j, k] < f_lo + 0.1 and HI[j, k] > f_hi - 0.1 and (HI[j] - LO[j])[dik].min() > TIP[t][0] * 1.3]
        assert civ, ("ADIM 55 DUR: pulun cıvatası / somunu yok", d, b["no"], c.round(1).tolist())
        j = max(civ, key=lambda q: (HI[q] - LO[q])[dik].min())
        uz_hi, uz_lo = HI[j, k] - f_hi, f_lo - LO[j, k]
        yan = +1 if uz_hi < uz_lo else -1; ne = "cıvata"
    islem.append((i, d, b, t, k, yan, j, ne))

for i, d, b, t, k, yan, j, ne in islem:
    di, do0, h0 = TIP[t]; yt = DONUSUM[t]; _, do1, h1 = TIP[yt]
    lo, hi = b["lo"], b["hi"]; c = (lo + hi) / 2; dik = [q for q in range(3) if q != k]
    oturma = lo[k] if yan > 0 else hi[k]                 # sac tarafı yüz (baş / somun karşı yüzde)
    r_dis = None

    def f(P, k=k, dik=dik, c=c, oturma=oturma, di=di, do1=do1, h0=h0, h1=h1):
        Q = P.reshape(-1, 3).copy()
        r = np.hypot(Q[:, dik[0]] - c[dik[0]], Q[:, dik[1]] - c[dik[1]])
        rm = r.max()
        ri = di / 2.0 + 0.0
        rn = np.where(r > ri + 0.3, ri + (r - ri) * (do1 / 2.0 - ri) / max(rm - ri, 1e-9), r)
        sc = np.where(r > 1e-9, rn / np.maximum(r, 1e-9), 1.0)
        for q in dik: Q[:, q] = c[q] + (Q[:, q] - c[q]) * sc
        Q[:, k] = oturma + (Q[:, k] - oturma) * (h1 / h0)
        return Q.reshape(P.shape)
    g.donustur(b, f)
    dlt = (h0 - h1) * (-yan)
    if abs(dlt) > 1e-9:
        dj, bj = TUM[j]; v = np.zeros(3); v[k] = dlt; g.tasi_b(bj, v)
    KAYIT["pul"].append(dict(dugum=d, no=int(b["no"]), eski=t, yeni=yt, merkez=np.round(c, 2).tolist(), eksen="xyz"[k], bas_yani=int(yan),
                             otelenen=ne, oteleme=round(float(dlt), 3), oteleme_dugum=TUM[j][0]))
ozet = {}
for p in KAYIT["pul"]:
    key = "%s %s → %s (%s)" % (p["dugum"], p["eski"], p["yeni"], p["otelenen"]); ozet[key] = ozet.get(key, 0) + 1
for k_, v_ in sorted(ozet.items()): LOG("  %-70s %d" % (k_, v_))
KAYIT["ozet"] = ozet
tmp = go + ".d55.glb"; g.kaydet(tmp); del g
r = subprocess.run([sys.executable, os.path.join(HERE, "50_sikilastir.py"), tmp, go]); assert r.returncode == 0
os.remove(tmp)
KAYIT["log"] = SE.LOG
json.dump(KAYIT, open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=float)
LOG("ADIM 55 bitti · %d pul · %s · %.0f sn" % (len(KAYIT["pul"]), go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
