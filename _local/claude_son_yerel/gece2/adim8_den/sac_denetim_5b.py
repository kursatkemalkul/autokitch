# -*- coding: utf-8 -*-
"""ADIM 5b · E / U üretim sacı üreteçlerinin BAĞIMSIZ denetimi + çıktıları (yalnız bu klasöre yazar).
  1 · sac: doğrula (açınımdan yeniden büküm) + DFM (+ abkant) · profil DFM · gövde↔gövde OCC çakışma (GO.denetle)
  2 · DOĞRU çakışma aracı (govde_denetim_dogru: manifold3d + VTK yoğun örnekleme + OCC teyit): yeni gövde parçaları ↔ bugünkü modelin (hat3_v8zq)
      bölgedeki bütün parçaları (eski gövde düğümleri HARİÇ) + sac↔sac
  3 · havada (her parça başka bir parçaya ≤ 0,05 mm değiyor) · dış zarf ±0,5 · PU / yalıtım görünmez · açınım her sacda
  4 · GLB + parça listesi CSV + açınım JSON + görüntüler (birleşik + patlatılmış)"""
import os, sys, json, time, csv, re, collections, pickle, struct, math
import numpy as np
BUR = os.path.dirname(os.path.abspath(__file__))
os.environ["ADIM5"] = BUR
os.environ["AUTOKITCH_SAC_STANDART"] = os.path.abspath(os.path.join(BUR, "..", "..", "sac_standart"))
SCR = os.path.abspath(os.path.join(BUR, "..", ".."))
W_ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8"
H3 = os.path.join(W_, "arastirma", "_uretec", "h3")
for p in (H3, os.path.dirname(H3), SCR, os.path.join(SCR, "sac_standart")):
    if p not in sys.path: sys.path.insert(0, p)
import cadquery as cq
import h3_sac_v1 as S
import h3_govde_ortak_v1 as GO
V8ZQ = os.path.join(SCR, "hat3_v8zq.glb")
LOGF = None


def log(*a):
    s = " ".join(str(x) for x in a); print(s); sys.stdout.flush()
    if LOGF: LOGF.write(s + "\n"); LOGF.flush()


def sekil(p):
    return p["sh"] if p.get("sh") is not None else p["wp"].val()


# ------------------------------------------------------------------------------------------------ GLB (bileşik denetim modeli)
def _tess(sh, tol=0.05, aci=0.2):
    vs, tr = sh.tessellate(tol, aci)
    if not tr: return np.zeros((0, 3, 3))
    P = np.array([[v.x, v.y, v.z] for v in vs], float); T = np.array(tr, np.int64)
    return P[T]


def glb_yaz_ucgen(yol, dugumler):
    """dugumler: [(ad, P (n,3,3) mm)] → GLB (m, indeksiz)"""
    blob, views, accs, meshes, nodes = [], [], [], [], []
    off = 0
    for ad, P in dugumler:
        if not len(P): continue
        X = (P.reshape(-1, 3) / 1000.0).astype("<f4"); I = np.arange(len(X), dtype="<u4")
        for arr, tgt in ((X, 34962), (I, 34963)):
            b = arr.tobytes(); pad = (-len(b)) % 4
            views.append({"buffer": 0, "byteOffset": off, "byteLength": len(b), "target": tgt}); blob.append(b + b"\0" * pad); off += len(b) + pad
        accs.append({"bufferView": len(views) - 2, "componentType": 5126, "count": len(X), "type": "VEC3", "min": X.min(0).tolist(), "max": X.max(0).tolist()})
        accs.append({"bufferView": len(views) - 1, "componentType": 5125, "count": len(I), "type": "SCALAR"})
        meshes.append({"primitives": [{"attributes": {"POSITION": len(accs) - 2}, "indices": len(accs) - 1}]})
        nodes.append({"name": ad, "mesh": len(meshes) - 1})
    bb = b"".join(blob)
    g = {"asset": {"version": "2.0"}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes, "meshes": meshes, "accessors": accs,
         "bufferViews": views, "buffers": [{"byteLength": len(bb)}]}
    js = json.dumps(g, separators=(",", ":")).encode(); js += b" " * ((-len(js)) % 4)
    with open(yol, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(bb))); f.write(struct.pack("<II", len(js), 0x4E4F534A)); f.write(js)
        f.write(struct.pack("<II", len(bb), 0x004E4942)); f.write(bb)


_D8 = None


def v8_dugumler():
    global _D8
    if _D8 is None:
        import govde_denetim_dogru as GD
        t0 = time.time(); _D8 = GD.glb_oku(V8ZQ); log("v8zq okundu: %d düğüm · %.0f s" % (len(_D8), time.time() - t0))
    return _D8


def bilesik_glb(yol, yeni, bolge, haric, onek="SAC__", kismi=None, ortam=()):
    """kismi: {düğüm deseni: [(lo, hi) kutuları]} → o düğümün bu kutuların İÇİNDE kalan bileşenleri (yeni gövdeyle değişen parçalar) atılır"""
    import govde_denetim_dogru as GD
    D = v8_dugumler(); lo, hi = np.array(bolge[0]), np.array(bolge[1]); out = []; atilan = []
    for ad, P in D.items():
        if not len(P) or haric.search(ad): continue
        Q = P.reshape(-1, 3)
        if (Q.max(0) < lo).any() or (Q.min(0) > hi).any(): continue
        kut = [k for d, ks in (kismi or {}).items() if re.search(d, ad) for k in ks]
        if kut:
            kal = []
            for b in GD.bilesenler(ad, P):
                if any((b.lo >= np.array(k[0]) - 0.6).all() and (b.hi <= np.array(k[1]) + 0.6).all() for k in kut):
                    atilan.append((ad, np.round(b.lo, 1).tolist(), np.round(b.hi, 1).tolist())); continue
                kal.append(b.P)
            if not kal: continue
            P = np.concatenate(kal)
        out.append((ad, P))
    if atilan: log("bileşik: değişen (atılan) mevcut bileşen %d: %s" % (len(atilan), atilan[:12]))
    for p in ortam: out.append(("ORTAM_ESAC__" + p["ad"], _tess(sekil(p))))
    for p in yeni: out.append((onek + p["ad"], _tess(sekil(p))))
    glb_yaz_ucgen(yol, out)
    log("bileşik denetim GLB: %d düğüm (%d mevcut + %d yeni) → %s" % (len(out), len(out) - len(yeni), len(yeni), os.path.basename(yol)))


def dogru_cakisma(yol, onek, izinli, cikti):
    import govde_denetim_dogru as GD
    R = GD.denetle(yol, [("YENI", (onek,), False)], None, cikti, yaz=log, occ=True)["YENI"]
    kal, izn = [], []
    for r in R["cakisma"]:
        a = r["parca"].split("[")[0][len(onek):]; b = r["komsu"].split("[")[0]; b = b[len(onek):] if b.startswith(onek) else b
        occ = r.get("occ_derinlik")
        if isinstance(occ, list) and occ and max(occ) <= 0.05:                    # OCC teyidi: kapsayan katının içinde değil → sahte (çakışık yüz)
            izn.append(dict(r, a=a, b=b, not_="OCC teyidi 0 (çakışık yüz)")); continue
        (izn if izinli(a, b) else kal).append(dict(r, a=a, b=b))
    return dict(cakisma=kal, izinli=izn, incele=R["incele"], acik_ag=R["acik_ag"], temas=len(R["temas"]), bilesen=R["parca_sayisi"])


def havada(parcalar, ortam_kutulari=(), zemin=0.05, esik=0.05):
    """her parça başka bir yeni parçaya (ya da ortam kutusuna / zemine) ≤ esik değiyor mu"""
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    ss = [(p["ad"], sekil(p)) for p in parcalar]; bb = [s.BoundingBox() for _a, s in ss]
    out = []
    for i, (a, s) in enumerate(ss):
        b = bb[i]
        if b.ymin <= zemin: continue
        ok = False
        for j in range(len(ss)):
            if i == j: continue
            c = bb[j]
            if not (b.xmin <= c.xmax + 0.1 and c.xmin <= b.xmax + 0.1 and b.ymin <= c.ymax + 0.1 and c.ymin <= b.ymax + 0.1 and b.zmin <= c.zmax + 0.1 and c.zmin <= b.zmax + 0.1): continue
            d = BRepExtrema_DistShapeShape(s.wrapped, ss[j][1].wrapped); d.Perform()
            if d.IsDone() and d.Value() <= esik: ok = True; break
        if not ok:
            for (lo, hi) in ortam_kutulari:
                if all(b_ <= h + esik for b_, h in zip((b.xmin, b.ymin, b.zmin), hi)) and all(h_ >= l - esik for h_, l in zip((b.xmax, b.ymax, b.zmax), lo)):
                    ok = "ortam"; break
        if not ok: out.append((a, [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]))
    return out


def zarf(parcalar):
    b = [sekil(p).BoundingBox() for p in parcalar]
    return [round(min(x.xmin for x in b), 2), round(max(x.xmax for x in b), 2), round(min(x.ymin for x in b), 2), round(max(x.ymax for x in b), 2),
            round(min(x.zmin for x in b), 2), round(max(x.zmax for x in b), 2)]


def acinim_bulanik(g):
    """açınım doğrulaması: OCC'nin çakışık yüzlü büyük levhalarda boolean'ı boş döndürdüğü durumda (ΔV < %0,5 ama simetrik fark %100/200)
    simetrik fark BULANIK boolean (tol 1e-4) ile yeniden hesaplanır · sonuç sac.dogrula() önbelleğine yazılır (denetle aynı sonucu okur)"""
    import json as _j
    out = []
    for s in g.SAC:
        r = s.dogrula()
        if r.get("acinim_gecti") or r.get("hacim_farki_yuzde") is None or r["hacim_farki_yuzde"] >= 0.5: continue
        A = s.kati_temel(); C, _ = S.acinimdan_kati(_j.loads(_j.dumps(s.acinim())))
        try:
            d = A.cut(C, tol=1e-4).Volume() + C.cut(A, tol=1e-4).Volume()
            sim = round(100.0 * d / A.Volume(), 5)
        except Exception as e:
            sim = None
        r["simetrik_fark_yuzde_ilk"] = r.get("simetrik_fark_yuzde"); r["simetrik_fark_yuzde"] = sim
        r["simetrik_not"] = "OCC çakışık yüz → bulanık boolean (tol 1e-4) ile yeniden"
        r["acinim_gecti"] = sim is not None and sim < 0.5
        out.append((s.ad, r["simetrik_fark_yuzde_ilk"], sim, r["acinim_gecti"]))
    if out: log("açınım bulanık yeniden doğrulama: %s" % out)
    return out


# ------------------------------------------------------------------------------------------------ CSV
def parca_csv(g, R, yol, dunya):
    sat = []
    pem_sac = collections.Counter(); vida_sac = collections.Counter()
    for s in g.SAC:
        for P in s.paneller:
            for k in P.kesikler:
                if k.tip in ("pem_saplama", "pem_somun"): pem_sac[s.ad] += 1
                if k.tip in ("vida_deligi",): vida_sac[s.ad] += 1
    for s in g.SAC:
        a = s.acinim(); r = R["sac"].get(s.ad, {})
        bk = " | ".join("%s %g° %s R%g" % (B.cocuk.ad.split(".")[-1], B.aci, "yukarı" if B.yon > 0 else "aşağı", B.R) for B in s.bukumler)
        sat.append(dict(parca=s.ad, tur="sac", malzeme=s.malzeme, kalinlik=s.t, acinim="%.1f × %.1f" % (a["levha"]["boy"], a["levha"]["en"]), kutle_kg=a["levha"]["kutle_kg"],
                        bukum_sayisi=len(s.bukumler), bukumler=bk, R_ic=s.R, K=s.K, delik_kesik=len(a["ic_konturlar"]), pem=pem_sac[s.ad], vida_deligi=vida_sac[s.ad],
                        punta=sum(p["adet"] for p in s.puntalar), kose_kaynagi=len([k for k in s.kaynaklar if k["tip"] == "kose"]),
                        abkant_sira=r.get("abkant_sira"), acinim_dogrulama="GEÇTİ" if r.get("gecti") else "KALDI", dfm_hata=len(r.get("dfm_hata", [])),
                        dfm_uyari=len(r.get("dfm_uyari", [])), not_="kapakla döner" if g.kapakla_doner(s.ad) else ""))
    for p in g.PROF.values():
        k = p.kesim_satiri()
        sat.append(dict(parca=p.ad, tur="profil (kesim listesi)", malzeme="AISI 304 boru", kalinlik=p.t,
                        acinim="L %.1f · kesit %s" % (k["L"], "×".join("%g" % v for v in k["kesit"][:3])), kutle_kg=k["kg"], bukum_sayisi=0,
                        bukumler="uçlar 90° · " + "; ".join("%s %s a=%.1f %s" % (q["tip"], q["yuz"], q["a"], ("Ø%g" % q["cap"]) if q.get("cap") else "%g×%g" % tuple(q["olcu"])) for q in k["kesikler"])[:900],
                        delik_kesik=len(k["kesikler"]), dfm_hata=len(k["dfm_hata"])))
    bom = S.bom_topla([q for q in g.ELEMAN])
    for b in bom:
        sat.append(dict(parca=b["tanim"], tur="bağlantı / katalog (%s)" % b["tedarik"], malzeme=b["standart"], acinim=b["olcu"], adet=b["adet"]))
    ka = collections.Counter((p["bom"][0] if p.get("bom") else p["ad"]) for p in g.KAYNAK)
    for k_, n in ka.items(): sat.append(dict(parca=k_, tur="kaynak", adet=n))
    ar = S.bom_topla(g.ARAYUZ)
    for b in ar:
        sat.append(dict(parca=b["tanim"], tur="ARAYÜZ (montajda takılır · karşı parçada delik)", malzeme=b["standart"], acinim=b["olcu"], adet=b["adet"]))
    alanlar = ["parca", "tur", "malzeme", "kalinlik", "acinim", "kutle_kg", "bukum_sayisi", "bukumler", "R_ic", "K", "delik_kesik", "pem", "vida_deligi", "punta",
               "kose_kaynagi", "abkant_sira", "acinim_dogrulama", "dfm_hata", "dfm_uyari", "adet", "not_"]
    with open(yol, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=alanlar, delimiter=";"); w.writeheader()
        for r in sat: w.writerow({k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v) for k, v in r.items() if k in alanlar})
    pem_top = sum(pem_sac.values()); pem_ar = sum(b["adet"] for b in ar if "PEM" in b["standart"])
    log("CSV %s: %d satır · sac %d · profil %d · PEM deliği %d (arayüz saplaması %d)" % (os.path.basename(yol), len(sat), len(g.SAC), len(g.PROF), pem_top, pem_ar))
    return dict(satir=len(sat), pem_delik=pem_top, arayuz_pem=pem_ar)


# ------------------------------------------------------------------------------------------------ görüntü
def goruntu(parcalar, yol, patlat=None, baslik="", elev=22, azim=122, tol=0.6):
    import _ciz
    from PIL import Image
    L = []
    for p in parcalar:
        s = sekil(p)
        if patlat:
            d = patlat(p)
            if d is not None and any(d): s = s.translate(cq.Vector(*d))
        L.append(dict(ad=p["ad"], sh=s, tur=p.get("tur", "sac") if p.get("tur") in ("sac", "baglanti", "kaynak", "ayak") else ("ayak" if p.get("tur") == "profil" else "sac")))
    png = yol.replace(".jpg", ".png")
    _ciz.ciz(L, png, elev=elev, azim=azim, tol=tol, boyut=(12, 10), baslik=baslik)
    Image.open(png).convert("RGB").save(yol, quality=90); os.remove(png)
    log("görüntü %s" % os.path.basename(yol))


# ================================================================================================ ORTAK AKIŞ
def calistir_U(M, hizli=False):
    global LOGF
    T0 = time.time()
    LOGF = open(os.path.join(BUR, "U_denetim_log.txt"), "w", encoding="utf-8")
    GG = M.kur(log)
    D = dict(kod="U", birimler={})
    PAR = []
    RR = {}
    for k, g in GG.items():
        log("==================== %s" % g.birim)
        acinim_bulanik(g)
        R = GO.denetle(g, acinim_klasoru=os.path.join(BUR, "acinim_U"), abkant=not hizli, supurme=False, log=log)
        RR[k] = R
        P = M.govde_parcalari(g); PAR += P
        D["birimler"][g.birim] = dict(ozet=R["ozet"], sac_ozet=R["sac_ozet"], profil_ozet=R["profil_ozet"], govde_govde_occ=R["cakisma"],
                                      mekanizma_saplama=len(getattr(g, "MEK_SAPLAMA", [])), mekanizma_atla=getattr(g, "MEK_ATLA", []),
                                      arayuz=[dict(ad=p["ad"], karsi=p["arayuz"]["karsi"][:160], gerek=p["arayuz"]["gerek"]) for p in g.ARAYUZ],
                                      karsi_delik=g.KARSI_DELIK, notlar=g.NOT)
    adlar = collections.Counter(p["ad"] for p in PAR)
    assert all(v == 1 for v in adlar.values()), [a for a, v in adlar.items() if v > 1][:5]
    gw = [(p["ad"], sekil(p), p.get("meta", {})) for p in PAR]
    c = GO.cakisma(gw, gw, esik=0.5, ayni=True, izin=GO.ic_ice_izni)
    D["birimler_arasi_occ"] = c
    log("U birimleri arası + içi OCC çakışma: %d %s" % (len(c), c[:12]))
    S.glb_yaz(os.path.join(BUR, "U_sac_v1.glb"), PAR)
    rows = []
    for k, g in GG.items():
        tmp = os.path.join(BUR, "_U_%s.csv" % k)
        parca_csv(g, RR[k], tmp, None)
        with open(tmp, encoding="utf-8-sig") as f:
            L_ = f.read().splitlines()
        if not rows: rows.append("birim;" + L_[0])
        rows += ["%s;%s" % (g.birim, l) for l in L_[1:]]
        os.remove(tmp)
    with open(os.path.join(BUR, "U_parca.csv"), "w", encoding="utf-8-sig") as f:
        f.write("\n".join(rows) + "\n")
    log("U_parca.csv: %d satır" % (len(rows) - 1))
    yol = os.path.join(BUR, "_U_bilesik.glb")
    haric = re.compile(r"^(U_F_GOVDE__(sac|paslanmaz)|U_KE_GOVDE__|F_UST_KABIN__(sac|yalitim)|E_GOVDE__|E_MODULER__)")
    import h3_e_sac_v1 as ES                                                  # E'nin YENİ üretim sacı gövdesi ortam olarak (U_KE M8 vidaları E üst sacındaki PEM SP-M8'e girer)
    gE = ES.kur(lambda *a: None); ortamE = [p for p in ES.govde_parcalari(gE, dunya=True) if sekil(p).BoundingBox().ymax > 1700]
    kismi = {r"^ELK_ZINCIR__paslanmaz$": [((3914, 2080, -831), (3984, 2168, -789))],
             r"^F_DAVLUMBAZ__sac$": [((2501, 1347, -442), (3999, 1861, -439.9))],
             r"^F_UST_KABIN__paslanmaz$": [((2501, 1316, -829), (3999, 1347, 58)), ((3325, 1347, -828), (3357, 1861, 58)), ((2502, 1830, 26), (3998, 1861, 58))]}
    bilesik_glb(yol, PAR, ((2480, 780, -850), (5250, 2210, 100)), haric, onek="SACU__", kismi=kismi, ortam=ortamE)
    icice = {}
    for p in PAR:
        for x in (p.get("meta") or {}).get("ic_ice", []) or []: icice.setdefault(p["ad"], set()).add(x)

    def izinli(a, b):
        return b in icice.get(a, ()) or a in icice.get(b, ())
    C = dogru_cakisma(yol, "SACU__", izinli, os.path.join(BUR, "den_U"))
    D["dogru_cakisma"] = dict(gercek=[(c_["a"], c_["b"], c_["derinlik"], c_.get("occ_derinlik")) for c_ in C["cakisma"]], izinli_pem=len(C["izinli"]),
                              incele=[(c_["parca"], c_["komsu"], c_["hacim"]) for c_ in C["incele"]], acik_ag=C["acik_ag"][:40], temas=C["temas"], bilesen=C["bilesen"])
    log("DOĞRU ÇAKIŞMA U: gerçek %d · PEM gömme başı (izinli) %d · incele %d · temas %d · açık ağ %d" % (len(C["cakisma"]), len(C["izinli"]), len(C["incele"]), C["temas"], len(C["acik_ag"])))
    for c_ in C["cakisma"][:80]: log("   ÇAKIŞMA %s ↔ %s %.3f mm · OCC %s" % (c_["a"], c_["b"], c_["derinlik"], c_.get("occ_derinlik")))
    H = havada(PAR)
    D["havada"] = H
    log("HAVADA U: %d %s" % (len(H), H[:10]))
    REF = {"U_F_GOVDE": [2500.0, 4000.0, 1862.0, 2200.0, -830.0, 59.0], "U_KE_GOVDE": [4000.0, 5230.0, 1862.0, 2200.0, -830.0, 59.0],
           "F_UST_KABIN": [2500.0, 4000.0, 788.0, 1862.0, -830.0, 59.0]}
    D["zarf"] = {}
    for k, g in GG.items():
        P = [p for p in PAR if p["birim"] == g.birim]; z = zarf(P); ref = REF[g.birim]
        f = [round(a - b, 2) for a, b in zip(z, ref)]
        tas = []
        for p in P:
            bb = sekil(p).BoundingBox(); v = (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)
            if any(v[i] < ref[i] - 0.5 for i in (0, 2, 4)) or any(v[i] > ref[i] + 0.5 for i in (1, 3, 5)): tas.append((p["ad"], [round(x, 2) for x in v]))
        D["zarf"][g.birim] = dict(zarf=z, ref=ref, fark=f, gecti=all(abs(x) <= 0.5 for x in f), tasan=tas[:20])
        log("ZARF %s: %s · bugünkü %s · fark %s → %s %s" % (g.birim, z, ref, f, "GEÇTİ" if D["zarf"][g.birim]["gecti"] else "KALDI", tas[:6]))
    D["yalitim_gorunur"] = yalitim_gorunurluk([p for p in PAR if p.get("tur") == "yalitim"], [p for p in PAR if p.get("tur") != "yalitim"])
    log("YALITIM görünürlük (ad, örnek nokta, açıkta kalan): %s" % D["yalitim_gorunur"])
    json.dump(D, open(os.path.join(BUR, "U_denetim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    try:
        def patlat(p):
            a = p["ad"]; b = p["birim"]
            dy = {"U_F_GOVDE": 500, "U_KE_GOVDE": 500, "F_UST_KABIN": 0}[b]
            if "tavan" in a or "omega" in a: dy += 250
            dz = -300 if ("arka_sac" in a or "giris_cebi" in a or "panjur" in a) else 0
            dx = (-250 if a.endswith("yan_sol") else 0) + (250 if a.endswith("yan_sag") else 0)
            return (dx, dy, dz)
        goruntu(PAR, os.path.join(BUR, "U_birlesik.jpg"), baslik="U_F + U_KE + F üst kabin · üretim sacı v1 · birleşik")
        goruntu(PAR, os.path.join(BUR, "U_patlatilmis.jpg"), patlat=patlat, baslik="U_F + U_KE + F üst kabin · patlatılmış")
        goruntu([p for p in PAR if p["birim"] == "F_UST_KABIN" and not ("arka_sac" in p["ad"] or "tavan_sac" in p["ad"])], os.path.join(BUR, "U_f_ust_kabin_ic.jpg"),
                baslik="F üst kabin · arka + tavan gizli (çerçeve · taban · taş yünü kılıfı · bölme)", azim=-120, elev=30)
    except Exception as e:
        log("görüntü hatası: %r" % e)
    log("U BİTTİ · %.0f s" % (time.time() - T0))
    LOGF.close(); LOGF = None
    return D


def yalitim_gorunurluk(yal, diger, adim=40.0, ofs=0.25):
    """taş yünü bloğunun DIŞ ZARF yüzlerinin 0,25 mm dışındaki ızgara noktaları başka bir gövde katısının (taban levhası / kılıf / kovan) içinde mi →
    açıkta kalan nokta sayısı (0 = görünmez)"""
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.gp import gp_Pnt
    from OCP.TopAbs import TopAbs_IN, TopAbs_ON
    out = []
    ds = [(p["ad"], sekil(p)) for p in diger]
    for p in yal:
        b = sekil(p).BoundingBox(); lo = np.array([b.xmin, b.ymin, b.zmin]); hi = np.array([b.xmax, b.ymax, b.zmax])
        top = 0; acik = 0; ornek = []
        for ax in range(3):
            o = [i for i in range(3) if i != ax]
            g0 = np.arange(lo[o[0]] + 1.0, hi[o[0]] - 0.5, adim if hi[o[0]] - lo[o[0]] > 40 else 4.0)
            g1 = np.arange(lo[o[1]] + 1.0, hi[o[1]] - 0.5, adim if hi[o[1]] - lo[o[1]] > 40 else 4.0)
            for sg, v in ((-1, lo[ax] - ofs), (1, hi[ax] + ofs)):
                for a in g0:
                    for c in g1:
                        q = np.zeros(3); q[ax] = v; q[o[0]] = a; q[o[1]] = c
                        top += 1; ok = False
                        for ad, s in ds:
                            bb = s.BoundingBox()
                            if not (bb.xmin - 0.1 <= q[0] <= bb.xmax + 0.1 and bb.ymin - 0.1 <= q[1] <= bb.ymax + 0.1 and bb.zmin - 0.1 <= q[2] <= bb.zmax + 0.1): continue
                            cl = BRepClass3d_SolidClassifier(s.wrapped, gp_Pnt(*map(float, q)), 1e-6)
                            if cl.State() in (TopAbs_IN, TopAbs_ON): ok = True; break
                        if not ok:
                            acik += 1
                            if len(ornek) < 6: ornek.append(np.round(q, 1).tolist())
        out.append((p["ad"], top, acik, ornek))
    return out


def akis(kod, g, parcalar, bolge, haric, ref_zarf, patlat, hizli, ek=None):
    global LOGF
    T0 = time.time()
    LOGF = open(os.path.join(BUR, "%s_denetim_log.txt" % kod), "w", encoding="utf-8")
    acinim_bulanik(g)
    R = GO.denetle(g, cerceve=g.cerceve, acinim_klasoru=os.path.join(BUR, "acinim_%s" % kod), abkant=not hizli, supurme=False, log=log)
    D = dict(kod=kod, ozet=R["ozet"], sac_ozet=R["sac_ozet"], profil_ozet=R["profil_ozet"], govde_govde_occ=R["cakisma"])
    # GLB (yalnız gövde) + CSV
    S.glb_yaz(os.path.join(BUR, "%s_sac_v1.glb" % kod), parcalar)
    D["csv"] = parca_csv(g, R, os.path.join(BUR, "%s_parca.csv" % kod), parcalar)
    # doğru çakışma
    yol = os.path.join(BUR, "_%s_bilesik.glb" % kod)
    bilesik_glb(yol, parcalar, bolge, haric, onek="SAC%s__" % kod)
    icice = {}
    for p in parcalar:
        for x in (p.get("meta") or {}).get("ic_ice", []) or []: icice.setdefault(p["ad"], set()).add(x)
    def izinli(a, b):
        return b in icice.get(a, ()) or a in icice.get(b, ())
    C = dogru_cakisma(yol, "SAC%s__" % kod, izinli, os.path.join(BUR, "den_%s" % kod))
    D["dogru_cakisma"] = dict(gercek=[(c["a"], c["b"], c["derinlik"], c.get("occ_derinlik")) for c in C["cakisma"]], izinli_pem=len(C["izinli"]),
                              incele=[(c["parca"], c["komsu"], c["hacim"]) for c in C["incele"]], acik_ag=C["acik_ag"][:40], temas=C["temas"], bilesen=C["bilesen"])
    log("DOĞRU ÇAKIŞMA %s: gerçek %d · PEM gömme başı (izinli) %d · incele %d · temas %d · açık ağ %d" % (kod, len(C["cakisma"]), len(C["izinli"]), len(C["incele"]), C["temas"], len(C["acik_ag"])))
    for c in C["cakisma"][:60]: log("   ÇAKIŞMA %s ↔ %s %.3f mm · OCC %s" % (c["a"], c["b"], c["derinlik"], c.get("occ_derinlik")))
    # havada
    H = havada(parcalar)
    D["havada"] = H; log("HAVADA %s: %d %s" % (kod, len(H), H[:10]))
    # zarf
    z = zarf(parcalar); D["zarf"] = z; D["zarf_ref"] = ref_zarf
    D["zarf_fark"] = [round(a - b, 2) for a, b in zip(z, ref_zarf)]
    D["zarf_gecti"] = all(abs(x) <= 0.5 for x in D["zarf_fark"])
    tas = []
    for p in parcalar:
        bb = sekil(p).BoundingBox(); v = (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)
        if v[0] < ref_zarf[0] - 0.5 or v[1] > ref_zarf[1] + 0.5 or v[2] < ref_zarf[2] - 0.5 or v[3] > ref_zarf[3] + 0.5 or v[4] < ref_zarf[4] - 0.5 or v[5] > ref_zarf[5] + 0.5:
            tas.append((p["ad"], [round(x, 2) for x in v]))
    D["zarf_tasan"] = tas
    for t_ in tas[:15]: log("   ZARF DIŞI %s %s" % t_)
    log("ZARF %s: %s · bugünkü %s · fark %s → %s" % (kod, z, ref_zarf, D["zarf_fark"], "GEÇTİ" if D["zarf_gecti"] else "KALDI"))
    D["acinim_kalan"] = R["sac_ozet"]["dogrulama_kalan"]
    D["mekanizma_saplama"] = len(getattr(g, "MEK_SAPLAMA", [])); D["mekanizma_atla"] = getattr(g, "MEK_ATLA", [])
    D["arayuz"] = [dict(ad=p["ad"], karsi=p["arayuz"]["karsi"][:160], gerek=p["arayuz"]["gerek"]) for p in g.ARAYUZ]
    D["karsi_delik"] = g.KARSI_DELIK; D["notlar"] = g.NOT
    if ek: D.update(ek(g, parcalar, R))
    json.dump(D, open(os.path.join(BUR, "%s_denetim.json" % kod), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    # görüntüler
    try:
        goruntu(parcalar, os.path.join(BUR, "%s_birlesik.jpg" % kod), baslik="%s üretim sacı v1 · birleşik" % kod)
        goruntu(parcalar, os.path.join(BUR, "%s_patlatilmis.jpg" % kod), patlat=patlat, baslik="%s üretim sacı v1 · patlatılmış" % kod)
        goruntu([p for p in parcalar if not g.kapakla_doner(p["ad"])], os.path.join(BUR, "%s_kapaksiz_on.jpg" % kod), baslik="%s · kapaklar gizli · önden" % kod, azim=125, elev=20)
        goruntu(parcalar, os.path.join(BUR, "%s_birlesik_arka.jpg" % kod), baslik="%s üretim sacı v1 · birleşik · arkadan" % kod, azim=-58)
    except Exception as e:
        log("görüntü hatası: %r" % e)
    log("%s BİTTİ · %.0f s" % (kod, time.time() - T0))
    LOGF.close(); LOGF = None
    return D


def calistir_E(M, hizli=False):
    g = M.kur(log)
    P = M.govde_parcalari(g, dunya=True)
    ref = [4400.0, 5230.0, 0.0, 2197.0, -830.0, 79.0]
    haric = re.compile(r"^(E_GOVDE__|E_MODULER__)")
    def patlat(p):
        a = p["ad"]
        if g.kapakla_doner(a) or a.startswith("onyuz_kapak"): return (0, 0, 350)
        if a.startswith(("ust_sac", "govde_bag_ust", "govde_pem_m8")): return (0, 300, 0)
        if a.startswith(("sol_sac", "govde_bag_ust_sol")) or "_sol_" in a and a.startswith("govde_kulak") and False: return (-350, 0, 0)
        if a.startswith("sol_sac"): return (-350, 0, 0)
        if a.startswith(("sag_sac", "sarjor_yan_kapisi")) and "lama" not in a: return (350, 0, 0)
        if a.startswith("arka_sac"): return (0, 0, -350)
        if a.startswith(("kaide_e", "ayak_")): return (0, -250, 0)
        return (0, 0, 0)
    return akis("E", g, P, ((4380, -5, -850), (5250, 2210, 100)), haric, ref, patlat, hizli)
