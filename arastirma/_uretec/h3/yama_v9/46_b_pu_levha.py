# -*- coding: utf-8 -*-
"""ZİNCİR ADIM 46 · B PU LEVHALARI YENİDEN KESİLDİ (4 Eki 2026 · Claude · YEREL · Kemal: "PU levha olarak takılabilsin, köşeler flanş / köşebent kadar boşaltılsın,
boşluk kalırsa ayrı dolgu levhası; toplam yalıtım hacmi ve U değeri değişmesin")
python 46_b_pu_levha.py girdi.glb cikti.glb      (zincir: hat3_v9m.glb → hat3_v9n.glb)

B montaj animasyonu v3 denetimi (b3/denetim.md "MODEL AÇIĞI"): yerinde köpük modelinden gelen PU bloklarının bazıları sac flanşının / köşebendin
altına ya da büküm dış köşesine sarıyor → kesilmiş levha olarak takılamaz. Bu adım o blokları, her parçası TEK DOĞRU BOYUNCA takılabilen düz levhalara
ve köşe dolgu şeritlerine böler. Bölme tam (manifold3d boolean: parça = blok ∩ bölge, kalan = blok − bölgeler) → parçaların birleşimi = eski blok:
yalıtım hacmi, kalınlığı, U değeri ve PU'nun görünmezliği DEĞİŞMEZ (betik hacim toplamını denetler, fark > 1 mm³ ise DURUR).

  pu_arka_yuksek / pu_arka_alcak  → z = −805 düzleminde 2 katman: ARKA katman (z −828,5…−805 = dış arka sacın üst / alt flanşları ARASI, 23,5 mm; ek laması
        cebi arka yüzde frezelenir) + ÖN katman (z −805…−791,2, 13,8 mm, tam boy). Montaj: tezgâhta dış arka sac grubunun (arka 1 + ek laması + arka 2)
        içine önden (−z) yatırılır, grup arkadan yerine girer.
  pu_sol  → (1) ARKA ŞERİT: dış arka 1'in üst flanşının gölgesi (x 761…797,3, z < −805; arka katmanın devamı, tezgâh grubuyla gelir)
            (2) 3 ALT KÖŞE DOLGU ŞERİDİ: alt köşebentlerin büküm dış yayı ↔ yan sac / taban köşesi (köşebentten ÖNCE köşeye yatırılır)
            (3) 3 ÜST KÖŞE DOLGU ŞERİDİ: üst köşebentlerin iniş yolu (büküm dış yayı ↔ yan sac / tavan köşesi; köşebentten SONRA üstten)
            (4) ANA LEVHA: kalan (üstten; köşeleri köşebent / flanş kadar boşaltılmış).
  pu_taban_0 → şase M8 cıvatalarının (baş + Ø24 pul levhanın altında) üstünde Ø25 boydan boya delik + 10 PU tapa (cıvatadan sonra üstten).
  tk_depo_arka_pu / tk_depo_sag_pu → sağ üst köşebent 2'nin iniş yolundaki dış köşe dolgu şeritleri ayrılır (köşebentten sonra üstten), ana levha kalır.
Bölge = engel parçasının iniş / takılış yönünde süpürdüğü hacim (her üçgenin öteleme prizması ∪ katı; manifold3d hull + birleşim).
Çıktı: <çıktı>_ent.json (yeni parça → düğüm, kutu, hacim, takılış notu)."""
import os, sys, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sac_ent as SE
from m8kit import Glb
import manifold3d as mf

gi, go = sys.argv[1:3]
t0 = time.time(); LOG = SE.log
DUG = "B_KASA__pu"
# blok kutuları (v9b üreteç kutusu; adım 44 cepleri kutuyu değiştirmez)
BLOK = {"pu_sol": ((737.5, 124.5, -828.5), (797.3, 786.5, 23.0)),
        "pu_arka_yuksek": ((797.3, 124.5, -828.5), (2500.0, 786.5, -791.2)),
        "pu_arka_alcak": ((2500.0, 124.5, -828.5), (4027.3, 728.0, -791.2)),
        "tk_depo_arka_pu": ((4028.5, 463.5, -469.0), (4398.5, 786.5, -441.0)),
        "tk_depo_sag_pu": ((4338.5, 463.5, -441.0), (4398.5, 786.5, 23.0)),
        "pu_taban_0": ((797.3, 124.5, -791.2), (4027.3, 163.3, 23.0))}
SASE_M8 = [(x, z) for x in (1100.0, 1750.0, 2400.0, 3050.0, 3700.0) for z in (-110.0, -760.0)]   # taban ↔ şase M8 cıvataları (baş + DIN 9021 pul levhanın altında)
# engeller (B_KASA__sac / __paslanmaz bileşen kutusu)
ENGEL = {"dis_arka_1": ((736.0, 124.5, -830.0), (2090.75, 786.5, -805.0)),
         "kosebent_sol_alt_1": ((737.5, 124.5, -822.0), (762.5, 149.5, -722.5)),
         "kosebent_sol_alt_2": ((737.5, 124.5, -689.5), (762.5, 149.5, -126.5)),
         "kosebent_sol_alt_3": ((737.5, 124.5, -93.5), (762.5, 149.5, 21.0)),
         "kosebent_sol_ust_1": ((737.5, 761.5, -822.0), (762.5, 786.5, -722.5)),
         "kosebent_sol_ust_2": ((737.5, 761.5, -689.5), (762.5, 786.5, -126.5)),
         "kosebent_sol_ust_3": ((737.5, 761.5, -93.5), (762.5, 786.5, 21.0)),
         "kosebent_sag_ust_2": ((4373.5, 761.5, -467.5), (4398.5, 786.5, 21.0))}


def onar(P, r=0.01):
    """bileşen üçgenleri → manifold (köşeler r ızgarasına; adım 44 PU cebinde 0,01 mm'lik çift köşeler var)"""
    for rr in (1e-4, r, 0.05):
        u, inv = np.unique(np.round(P.reshape(-1, 3) / rr) * rr, axis=0, return_inverse=True); F = inv.reshape(-1, 3)
        F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
        m = mf.Manifold(mf.Mesh(vert_properties=u.astype(np.float32), tri_verts=F.astype(np.uint32)))
        if m.status() == mf.Error.NoError and not m.is_empty(): return m
    raise SystemExit("ADIM 46 DUR: manifold kurulamadı")


def ucg(b):
    return np.concatenate([p["X"][p["T"][t]] for p, t in b["parca"]])


g = Glb(gi)
DUGS = sorted(set(p["name"] for p in g.prims if p["name"].startswith("B_KASA__")))
for d in DUGS: g._bc.pop(d, None); g.bilesen(d, 0)


def bul(kutu, dugumler, tol=0.3):
    lo, hi = np.array(kutu[0]), np.array(kutu[1]); L = []
    for d in dugumler:
        L += [(d, b) for b in g._bc[d] if np.all(np.abs(b["lo"] - lo) < tol) and np.all(np.abs(b["hi"] - hi) < tol)]
    if len(L) != 1: raise SystemExit("ADIM 46 DUR: kutu %s → %d bileşen" % (kutu, len(L)))
    return L[0]


def yari(m, n, off):
    """m ∩ {n·p ≥ off} (manifold trim_by_plane: normal yönündeki taraf kalır)"""
    n = np.asarray(n, float); L = np.linalg.norm(n)
    return m.trim_by_plane((n / L).tolist(), float(off) / L)


def kutu_z(m, z0, z1):
    return yari(yari(m, (0, 0, 1), z0), (0, 0, -1), -z1)


def kose_alt(m, xw, yt, z0, z1, r=3.75, pay=3.75):
    """sol yan (x = xw) ↔ taban (y = yt) köşesinde köşebent büküm dış yayının dışı: x ≤ xw + r, y ≤ yt + r, (x − xw) + (y − yt) ≤ pay"""
    q = yari(yari(m, (-1, 0, 0), -(xw + r)), (0, -1, 0), -(yt + r))
    q = yari(q, (-1, -1, 0), -(xw + yt + pay))
    return kutu_z(q, z0, z1)


def kose_ust(m, xw, yt, z0, z1, sx=+1, r=3.75, pay=3.75):
    """yan (x = xw) ↔ tavan (y = yt) köşesi · sx = +1: yan solda (köşe x ≥ xw), −1: yan sağda"""
    q = yari(m, (-sx, 0, 0), -(sx * xw + r)) if sx > 0 else yari(m, (1, 0, 0), xw - r)
    q = yari(q, (0, 1, 0), yt - r)
    q = yari(q, (-sx, 1, 0), -sx * xw + yt - pay)
    return kutu_z(q, z0, z1)


def kapali_mi(P):
    """govde_denetim_dogru.bilesenler ile aynı yuvarlama (0,001 mm): her kenar tam 2 üçgende"""
    u, inv = np.unique(np.round(P.reshape(-1, 3), 3), axis=0, return_inverse=True); F = inv.reshape(-1, 3)
    F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
    e = np.sort(np.vstack([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1); _, c = np.unique(e, axis=0, return_counts=True)
    return bool(np.all(c == 2)), len(F)


SIL = [(ad, bul(kutu, [DUG])[1]) for ad, kutu in BLOK.items()]
for ad, k in ENGEL.items(): bul(k, [x for x in DUGS if x != DUG])    # engel (köşebent / dış arka 1) modelde beklenen yerde mi
KB = {k: (v[0][2], v[1][2]) for k, v in ENGEL.items()}          # köşebent z aralıkları
YENI = []        # (ad, manifold, kaynak blok, not, bileşen)
for ad, b in SIL:
    X = onar(ucg(b)); v0 = X.volume()
    parca = []
    if ad in ("pu_arka_yuksek", "pu_arka_alcak"):
        parca += [(ad + "_arka", yari(X, (0, 0, -1), 805.0), "arka katman 23,5 mm (dış arka sacın üst / alt flanşları arası) · tezgâhta sac grubuna önden"),
                  (ad + "_on", yari(X, (0, 0, 1), -805.0), "ön katman 13,8 mm · tezgâhta arka katmanın üstüne önden")]
    elif ad == "pu_sol":
        S = yari(yari(X, (0, 0, -1), 805.0), (1, 0, 0), 761.0)        # z ≤ −805 ∧ x ≥ 761: dış arka 1 üst flanşının gölgesi
        kalan = X - S
        parca.append(("pu_sol_arka_serit", S, "arka şerit (dış arka 1 üst flanşının altı, z < −805) · tezgâhta arka sac grubuyla"))
        for i in (1, 2, 3):
            z0, z1 = KB["kosebent_sol_alt_%d" % i]; A = kose_alt(kalan, 737.5, 124.5, z0, z1); kalan = kalan - A
            parca.append(("pu_sol_kose_alt_%d" % i, A, "alt köşe dolgu şeridi (köşebent alt %d büküm dış yayı ↔ yan sac / taban köşesi) · köşebentten önce köşeye" % i))
        for i in (1, 2, 3):
            z0, z1 = KB["kosebent_sol_ust_%d" % i]; U = kose_ust(kalan, 737.5, 786.5, z0, z1, +1); kalan = kalan - U
            parca.append(("pu_sol_kose_ust_%d" % i, U, "üst köşe dolgu şeridi (köşebent üst %d iniş yolu: büküm dış yayı ↔ yan sac / tavan köşesi) · köşebentten sonra üstten" % i))
        parca.insert(0, ("pu_sol", kalan, "ana levha (köşeler köşebent / flanş kadar boşaltılmış) · üstten"))
    elif ad == "pu_taban_0":
        # şase cıvatalarının başı ve pulu (Ø24) levhanın ALTINDA: levhada Ø25 boydan boya delik, üstüne cıvatadan sonra Ø25 PU tapa
        kalan = X
        for x, z in SASE_M8:
            c = mf.Manifold.cylinder(163.3 - 124.5 + 2.0, 12.5, 12.5, 64).transform([[1, 0, 0, x], [0, 0, 1, 123.5], [0, -1, 0, z]])
            T_ = X ^ c; kalan = kalan - c
            parca.append(("pu_taban_tapa_%d_%d" % (x, -z), T_, "PU tapa Ø25 (şase cıvatası başı + pulu üstüne, cıvatadan sonra üstten)"))
        parca.insert(0, (ad, kalan, "taban levhası (şase cıvatası yerlerinde Ø25 delikli) · üstten"))
    else:
        z0, z1 = KB["kosebent_sag_ust_2"]; U = kose_ust(X, 4398.5, 786.5, z0, z1, -1); kalan = X - U
        parca += [(ad, kalan, "ana levha · üstten"),
                  (ad + "_kose", U, "köşe dolgu şeridi (sağ üst köşebent 2 iniş yolu: büküm dış yayı ↔ sağ yan / tavan köşesi) · köşebentten sonra üstten")]
    vt = sum(p.volume() for _, p, _ in parca)
    if abs(vt - v0) > 1.0: raise SystemExit("ADIM 46 DUR: %s hacim %.2f → %.2f" % (ad, v0, vt))
    for n, p, s in parca:
        kab = [k for k in p.decompose()]
        P = SE.mf_P(p); ok, nt = kapali_mi(P)
        if len(kab) != 1 or not ok: raise SystemExit("ADIM 46 DUR: %s kabuk %d · kapalı %s" % (n, len(kab), ok))
    LOG("  %-16s %10.0f mm³ → %d parça (Σ %.1f, fark %.3f mm³): %s" % (ad, v0, len(parca), vt, vt - v0, ", ".join("%s %.0f" % (n, p.volume()) for n, p, _ in parca)))
    YENI += [(n, p, ad, s, b) for n, p, s in parca]

# ---------------------------------------------------------------- değiştir: eski blok bileşenleri silinir; levhalar B_KASA__pu'ya, şerit / dolgular
# YENİ düğüm B_KASA__pu_dolgu'ya (aynı PU malzemesi) — kesim yüzü ana levhayla aynı üçgenlemeyi paylaştığından aynı düğümde denetim (bilesenler) iki katıyı
# tek bileşen sanıyordu; ayrı düğümde her biri ayrı kapalı bileşen. İki teknik depo köşe şeridi (z −467,5…−441 ve −441…21) tek şerit (köşebent boyunca).
DOLGU = "B_KASA__pu_dolgu"
birles = {"tk_depo_arka_pu_kose": "tk_depo_kose_dolgu", "tk_depo_sag_pu_kose": "tk_depo_kose_dolgu"}
GRUP = {}
for n, p, kaynak, s, b in YENI:
    k = birles.get(n, n)
    if k in GRUP:
        q = GRUP[k]; GRUP[k] = (k, q[1] + p, q[2] + " + " + kaynak, "köşe dolgu şeridi (sağ üst köşebent 2 iniş yolu, köşebent boyu: teknik depo arka + sağ PU) · köşebentten sonra üstten", q[4])
    else:
        GRUP[k] = (k, p, kaynak, s, b)
KAYIT = {}; DOL = []
for k, (n, p, kaynak, s, b) in GRUP.items():
    lab = g.etiket_b(b); P = SE.mf_P(p)
    ok, _ = kapali_mi(P)
    if len(p.decompose()) != 1 or not ok: raise SystemExit("ADIM 46 DUR: %s birleşik şerit kapalı değil" % n)
    hedef = DOLGU if (n.startswith(("pu_sol_", "pu_taban_tapa")) or n.endswith("_dolgu")) else DUG
    if hedef == DUG: g.ekle_dugum(DUG, P, kat=lab[0], mek=lab[1], kpk=lab[2])
    else: DOL.append((n, P, lab))
    bb = p.bounding_box()
    KAYIT[n] = dict(dugum=hedef, kaynak=kaynak, kutu=[round(float(v), 3) for v in (bb[0], bb[3], bb[1], bb[4], bb[2], bb[5])], hacim=round(p.volume(), 2),
                    ucgen=int(len(P)), takilis=s, bom=["PU levha 40 kg/m³ (λ 0,022) kesilmiş · %s" % n])
for ad, b in SIL: g.sil_b(b)
tmp = go + ".e1.glb"; g.kaydet(tmp); del g
# yeni düğüm (ham GLB): B_KASA__pu malzemesi, üçgen çorbası (indisli), kat / mek / kpk aralıkları
H = SE.Ham(tmp); nd = H.hazirla(DOLGU, DUG)
pr = H.J["meshes"][nd["mesh"]]["primitives"][0]
XX, NN, II, ex_kat, ex_mek, kp = [], [], [], [], [], []; o = 0; ib = 0; AR = {}
for n, P, (kat, mek, kpk) in DOL:
    V = P.reshape(-1, 3); F = np.arange(len(V)).reshape(-1, 3)
    u, inv = np.unique(np.round(V, 6), axis=0, return_inverse=True); F = inv[F].reshape(-1, 3); V = u
    N = np.zeros_like(V); fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    for i in range(3): np.add.at(N, F[:, i], fn)
    N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)
    XX.append((V / 1000.0).astype(np.float32)); NN.append(N.astype(np.float32)); II.append((F.reshape(-1) + o).astype(np.uint32))
    m = 3 * len(F); ex_kat += [int(kat), ib, m]; ex_mek += [int(mek), ib, m]
    if kpk: kp += [ib, m]
    AR[n] = (ib, m); KAYIT[n]["indis"] = [ib, m]; o += len(V); ib += m
pr["attributes"] = {"POSITION": H._ekle(np.vstack(XX), "VEC3", 34962), "NORMAL": H._ekle(np.vstack(NN), "VEC3", 34962)}
pr["indices"] = H._ekle(np.concatenate(II).astype(np.uint32), "SCALAR", 34963)
pr["extras"] = {"kat": ex_kat, "mek": ex_mek, "kpk": kp}
LOG("  %s: %d parça · %d üçgen" % (DOLGU, len(DOL), ib // 3))
H.yaz(tmp + ".e2.glb")
SE.sikistir(tmp + ".e2.glb", go)
for f_ in (tmp, tmp + ".e2.glb"): os.remove(f_)
json.dump(dict(adim=46, ad="B PU levhaları yeniden kesildi", parca=KAYIT, log=SE.LOG), open(go[:-4] + "_ent.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
LOG("ADIM 46 bitti · %d blok → %d parça · %s · %.0f sn" % (len(SIL), len(KAYIT), go, time.time() - t0))
sys.stdout.flush(); os._exit(0)
