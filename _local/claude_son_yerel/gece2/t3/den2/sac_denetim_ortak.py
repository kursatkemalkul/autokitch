# -*- coding: utf-8 -*-
"""ADIM 5a · üretim sacı üreteçlerinin (h3_a_sac_v1 / h3_b_sac_v1) BAĞIMSIZ DENETİMİ + ÇIKTILARI (yalnız bu klasöre yazar).
  1 sac: dogrula (açınımdan yeniden büküm + kalınlık + kesit R) + DFM (abkant) + açınım JSON · 2 profil DFM · 3 dış zarf (bugünkü ± 0,5)
  4 gövde ↔ gövde OCC kesişim hacmi (PEM gömme başı izinli) · 5 gövde ↔ v8zq parçaları: govde_denetim_dogru.cift (manifold + yoğun örnekleme + derinlik)
  6 havada: temas grafiği (OCC uzaklık ≤ 0,6) → zemine (B / kaide / ayak) bağlı olmayan parça · 7 PU görünmez (B) · 8 GLB · CSV · JPG · rapor"""
import os, sys, json, time, re, csv, pickle, collections, math
S_ = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad"
os.environ.setdefault("AUTOKITCH_SAC_STANDART", os.path.join(S_, "sac_standart"))
W_ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3"
for p in (S_, os.path.join(S_, "sac_standart"), W_, os.path.dirname(W_)):
    if p not in sys.path: sys.path.insert(0, p)
import numpy as np
import cadquery as cq
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
import h3_sac_v1 as S
import govde_denetim_dogru as GD

BUR = os.path.dirname(os.path.abspath(__file__))
V = cq.Vector
T0 = time.time()
LOG = []


def log(m):
    s = "[%6.1fs] %s" % (time.time() - T0, m); print(s); LOG.append(s); sys.stdout.flush()


def sekil(p):
    if p.get("sh") is not None: return p["sh"]
    w = p["wp"]; return w.val() if hasattr(w, "val") else w


def bbk(a, b, pay=0.0):
    return a.xmin < b.xmax + pay and b.xmin < a.xmax + pay and a.ymin < b.ymax + pay and b.ymin < a.ymax + pay and a.zmin < b.zmax + pay and b.zmin < a.zmax + pay


def ucgen(sh, tol=0.05, aci=0.2):
    vs, tr = sh.tessellate(tol, aci)
    P = np.array([[v.x, v.y, v.z] for v in vs], float); T = np.array(tr, np.int64).reshape(-1, 3)
    if not len(T): return np.zeros((0, 3, 3))
    Q = P[T]; ar = np.linalg.norm(np.cross(Q[:, 1] - Q[:, 0], Q[:, 2] - Q[:, 0]), axis=1)
    return Q[ar > 1e-9]


def uzaklik(a, b):
    d = BRepExtrema_DistShapeShape(a.wrapped, b.wrapped); d.Perform()
    return d.Value() if d.IsDone() else 1e9


def kumele(ad):
    a = re.sub(r"_(\d+|[ab])$", "", ad)
    a = re.sub(r"_\d+(_\d+)*$", "", a)
    return a


def calistir(MOD, kod, haric, ankraj, pu_grubu=None, gorunum=None, izin_dis=None, ek_rapor=None):
    """MOD: üreteç modülü · kod 'A' / 'B' · haric: v8zq'da yerine geçilen düğümler (regex) · ankraj(p_dunya_bbox) → zemine bağlı mı ·
    pu_grubu: PU parçası mı (ad → bool) · gorunum: patlatma ötelemesi (ad → (dx, dy, dz)) · izin_dis(govde_ad, komsu_dugum) → açıklama ya da None"""
    CIK = os.path.join(BUR); os.makedirs(os.path.join(CIK, "acinim_%s" % kod), exist_ok=True)
    R = dict(surum="%s · %s · %s" % (MOD.SURUM, S.SURUM, "sac_denetim_ortak"), tarih="4 Eki 2026", standart=S.STD.ozet())
    G = MOD.kur(log)
    GOV = MOD.govde_parcalari()
    GW = MOD.dunya_listesi(GOV)
    ARW = MOD.dunya_listesi([dict(p, tur="arayuz") for p in G.ARAYUZ])
    # ================================================================ 1 · SAC
    sacR, hata_top, uyari_top, satir = {}, 0, 0, []
    for s in G.SAC:
        r = s.dogrula(); d = s.dfm(abkant=True); a = s.acinim()
        with open(os.path.join(CIK, "acinim_%s" % kod, s.ad + ".json"), "w", encoding="utf-8") as f:
            json.dump(a, f, ensure_ascii=False, indent=1)
        kb = getattr(MOD, "DFM_KABUL", {}).get(s.ad, {})
        for m in d:
            if m["durum"] == "HATA" and m["kural"] in kb: m["durum"] = "KABUL"; m["detay"] = kb[m["kural"]] + " · " + m["detay"]; log("        KABUL %s %s · %s" % (s.ad, m["kural"], kb[m["kural"]]))
        h = [m for m in d if m["durum"] == "HATA"]; u = [m for m in d if m["durum"] == "UYARI"]
        hata_top += len(h); uyari_top += len(u)
        ab = [m for m in d if m["kural"] == "abkant"]
        say = collections.Counter(k["tip"] for k in a["kesikler"])
        gecti = bool(r.get("acinim_gecti")) and r["kalinlik"]["gecti"] and r.get("kesit_gecti") is not False
        sacR[s.ad] = dict(t=s.t, R=s.R, K=s.K, rol=s.rol, bukum=len(s.bukumler), levha=a["levha"], delik=len(a["ic_konturlar"]), abkant_sira=(ab[0].get("sira") if ab else None),
                          dogrula=dict(acinim_gecti=r.get("acinim_gecti"), hacim_farki_yuzde=r.get("hacim_farki_yuzde"), simetrik_fark_yuzde=r.get("simetrik_fark_yuzde"),
                                       kalinlik_gecti=r["kalinlik"]["gecti"], kesit_gecti=r.get("kesit_gecti"), hata=r.get("yeniden_bukum_hatasi")),
                          dfm_hata=h, dfm_uyari=u, punta=sum(p["adet"] for p in s.puntalar), kesik=dict(say))
        satir.append(dict(parca=s.ad, malzeme=s.malzeme.split(",")[0] if s.mal != "on_seffaf" else s.malzeme.split(",")[0], t=s.t, acinim="%.1f × %.1f" % (a["levha"]["boy"], a["levha"]["en"]),
                          kg=a["levha"]["kutle_kg"], bukum=len(s.bukumler), R=s.R, K=s.K,
                          pem=say.get("pem_somun", 0) + say.get("pem_saplama", 0), vida_deligi=say.get("vida_deligi", 0) + say.get("percin_somun", 0) + say.get("kor_percin", 0),
                          kaynak=len(s.kaynaklar), punta=sum(p["adet"] for p in s.puntalar), acinim_dogrulama="GEÇTİ" if gecti else "KALDI",
                          dfm="%d HATA / %d UYARI" % (len(h), len(u)), abkant_sira=" ".join(str(x) for x in (ab[0].get("sira") or [])) if ab else ""))
        if h or u or not gecti:
            log("%-34s t%.1f · %d büküm · açınım %.0f×%.0f · ΔV %s sim %s · kalınlık %s · kesit %s · DFM %d HATA %d UYARI" % (s.ad, s.t, len(s.bukumler), a["levha"]["boy"], a["levha"]["en"],
                r.get("hacim_farki_yuzde"), r.get("simetrik_fark_yuzde"), r["kalinlik"]["gecti"], r.get("kesit_gecti"), len(h), len(u)))
            for m in h + u: log("        %s %-18s %s" % (m["durum"], m["kural"], m["detay"][:200]))
            if not gecti: log("        DOĞRULAMA: %s" % (r.get("yeniden_bukum_hatasi") or r["kalinlik"].get("hata", [])[:2]))
    dog_kal = [a for a, x in sacR.items() if not (x["dogrula"]["acinim_gecti"] and x["dogrula"]["kalinlik_gecti"] and x["dogrula"]["kesit_gecti"] is not False)]
    R["sac"] = sacR; R["sac_ozet"] = dict(adet=len(G.SAC), dfm_hata=hata_top, dfm_uyari=uyari_top, dogrulama_kalan=dog_kal)
    log("SAC: %d parça · açınım doğrulaması kalan %d · DFM %d HATA · %d UYARI" % (len(G.SAC), len(dog_kal), hata_top, uyari_top))
    # ================================================================ 2 · PROFİL
    prof, ph = [], 0
    for p in getattr(G, "PROFIL", []):
        d = p.dfm(); hh = [m for m in d if m["durum"] == "HATA"]; ph += len(hh)
        pp = p.parca(); prof.append(dict(ad=p.ad, L=pp["meta"]["L"], kg=pp["meta"]["kg"], kesit=pp["meta"]["kesit"], kesikler=pp["meta"]["kesikler"], dfm_hata=hh))
        for m in hh: log("   PROFİL HATA %s" % m["detay"])
    R["profil"] = dict(adet=len(prof), dfm_hata=ph, liste=prof)
    log("PROFİL: %d boru · %.1f m · DFM %d HATA" % (len(prof), sum(x["L"] for x in prof) / 1000.0, ph))
    # ================================================================ 3 · ZARF
    x0, x1, y0, y1, z0, z1 = MOD.ZARF; xo = getattr(MOD, "X_A", 0.0)
    tas = []
    lo = np.array([1e9] * 3); hi = -lo
    for p in GW:
        b = sekil(p).BoundingBox()
        lo = np.minimum(lo, [b.xmin, b.ymin, b.zmin]); hi = np.maximum(hi, [b.xmax, b.ymax, b.zmax])
        if b.xmin < x0 + xo - 0.5 or b.xmax > x1 + xo + 0.5 or b.ymin < y0 - 0.5 or b.ymax > y1 + 0.5 or b.zmin < z0 - 0.5 or b.zmax > z1 + 0.5:
            kz = cq.Solid.makeBox(x1 - x0 + 1, y1 - y0 + 1, z1 - z0 + 1, V(x0 + xo - 0.5, y0 - 0.5, z0 - 0.5))
            try: dis = sekil(p).Volume() - sekil(p).intersect(kz).Volume()
            except Exception: dis = -1
            if dis > 1e-3 or dis < 0: tas.append((p["ad"], [round(v, 2) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)], round(dis, 3)))
    hedef = [x0 + xo, x1 + xo, y0, y1, z0, z1]; bul = [lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]]
    fark = [round(a - b, 3) for a, b in zip(bul, hedef)]
    R["zarf"] = dict(hedef=hedef, bulunan=[round(v, 3) for v in bul], fark=fark, tasan=tas, gecti=(not tas) and all(abs(f) <= 0.5 for f in fark))
    log("ZARF: hedef %s · bulunan %s · fark %s · taşan %d → %s" % (hedef, [round(v, 1) for v in bul], fark, len(tas), "GEÇTİ" if R["zarf"]["gecti"] else "KALDI"))
    # ================================================================ 4 · GÖVDE ↔ GÖVDE
    ss = [(p["ad"], sekil(p), p.get("meta", {}) or {}) for p in GW]
    bb = [s.BoundingBox() for _a, s, _m in ss]
    ic, izinli = [], []
    for i in range(len(ss)):
        for j in range(i + 1, len(ss)):
            if not bbk(bb[i], bb[j], -1e-4): continue
            try: v = ss[i][1].intersect(ss[j][1]).Volume()
            except Exception: v = -1.0
            if v > 0.1 or v < 0:
                a, b = ss[i][0], ss[j][0]
                if b in (ss[i][2].get("ic_ice") or []) or a in (ss[j][2].get("ic_ice") or []): izinli.append((a, b, round(v, 3), "PEM gömme başı (sacın içine preslenir)"))
                elif (ss[i][2].get("tur") == "kaynak" or ss[j][2].get("tur") == "kaynak") and v < 20: izinli.append((a, b, round(v, 3), "kaynak dikişi ↔ ana metal (erime bölgesi)"))
                else: ic.append((a, b, round(v, 3)))
    R["govde_govde"] = dict(cakisma=ic, izinli=izinli)
    log("GÖVDE ↔ GÖVDE: kesişim %d%s · izinli (işaretli) %d" % (len(ic), (" → %s" % ic[:12]) if ic else "", len(izinli)))
    # ================================================================ 5 · GÖVDE ↔ v8zq (doğru araç)
    TUM = pickle.load(open(os.path.join(BUR, "_is", "bil_hepsi.pkl"), "rb"))
    hr = re.compile(haric)
    DIS = []
    for b in TUM:
        if hr.search(b["ad"]): continue
        P = b["P"]; bl = GD.Bil(b["ad"], b["no"], P, *_vf(P), b["kapali"]); DIS.append(bl)
    LO = np.array([b.lo for b in DIS]); HI = np.array([b.hi for b in DIS])
    cak, inc, tem = [], [], []
    for p in GW:
        if p.get("tur") == "arayuz": continue
        tp = time.time()
        P = ucgen(sekil(p), 0.1 if p.get("tur") == "pu" else 0.05)
        if not len(P): continue
        for A in GD.bilesenler(p["ad"], P):
            m = ((LO <= A.hi + GD.PAY) & (HI >= A.lo - GD.PAY)).all(1)
            for j in np.where(m)[0]:
                tc = time.time()
                r = GD.cift(A, DIS[j])
                if time.time() - tc > 5: log("   yavaş çift %s ↔ %s[%d] %.0f s → %s" % (p["ad"], DIS[j].dugum, DIS[j].no, time.time() - tc, r[0] if r else None))
                if r is None: continue
                k = dict(parca=A.ad, komsu="%s[%d]" % (DIS[j].dugum, DIS[j].no), tip=r[0], derinlik=r[1], hacim=None if r[2] is None else round(r[2], 3),
                         nokta=(r[3] or {}).get("nokta"))
                if r[0] == "CAKISMA":
                    iz = izin_dis(p["ad"], DIS[j].dugum, DIS[j]) if izin_dis else None
                    if iz: k["izin"] = iz; tem.append(k)
                    else: cak.append(k)
                elif r[0] == "INCELE": inc.append(k)
                else: tem.append(k)
    R["dis_cakisma"] = dict(cakisma=cak, incele=inc, temas_sayisi=len(tem), izinli=[k for k in tem if k.get("izin")])
    log("GÖVDE ↔ v8zq (%d bileşen · hariç %s): ÇAKIŞMA %d · İNCELE %d · TEMAS %d (izinli %d)" % (len(DIS), haric, len(cak), len(inc), len(tem), len(R["dis_cakisma"]["izinli"])))
    for k in sorted(cak, key=lambda k: -k["derinlik"])[:40]: log("   ÇAKIŞMA %-50s ↔ %-44s %.3f mm · hacim %s · %s" % (k["parca"], k["komsu"], k["derinlik"], k["hacim"], k["nokta"]))
    for k in inc[:10]: log("   İNCELE  %-50s ↔ %-44s hacim %s" % (k["parca"], k["komsu"], k["hacim"]))
    # arayüz elemanlarının kestiği parçalar (karşı delik / diş gerekir)
    gerek = collections.defaultdict(list)
    for p in ARW:
        P = ucgen(sekil(p), 0.1, 0.3)
        for A in GD.bilesenler(p["ad"], P):
            m = ((LO <= A.hi) & (HI >= A.lo)).all(1)
            for j in np.where(m)[0]:
                r = GD.cift(A, DIS[j])
                if r and r[0] == "CAKISMA": gerek["%s[%d]" % (DIS[j].dugum, DIS[j].no)].append(p["ad"])
    R["arayuz"] = [dict(ad=p["ad"], karsi=p["arayuz"]["karsi"], gerek=p["arayuz"]["gerek"], not_=p["arayuz"]["not_"], bom=list(p["bom"])) for p in G.ARAYUZ]
    R["arayuz_karsi_delik"] = {k: sorted(set(v)) for k, v in sorted(gerek.items())}
    log("ARAYÜZ: %d eleman · kestiği v8zq parçası %d → %s" % (len(G.ARAYUZ), len(gerek), sorted(gerek)[:12]))
    # ================================================================ 6 · HAVADA (temas grafiği)
    gov = [(p["ad"], sekil(p)) for p in GW if p.get("tur") != "arayuz"]
    gb = [s.BoundingBox() for _a, s in gov]
    komsu = collections.defaultdict(set)
    for i in range(len(gov)):
        for j in range(i + 1, len(gov)):
            if not bbk(gb[i], gb[j], 0.65): continue
            if uzaklik(gov[i][1], gov[j][1]) <= 0.6: komsu[i].add(j); komsu[j].add(i)
    kok = [i for i, b in enumerate(gb) if ankraj(gov[i][0], b)]
    gor = set(kok); yigin = list(kok)
    while yigin:
        i = yigin.pop()
        for j in komsu[i]:
            if j not in gor: gor.add(j); yigin.append(j)
    hav = [gov[i][0] for i in range(len(gov)) if i not in gor]
    R["havada"] = dict(kok=len(kok), parca=len(gov), bagli=len(gor), havada=hav)
    log("HAVADA: %d parça · zemine bağlı kök %d · bağlı %d · HAVADA %d%s" % (len(gov), len(kok), len(gor), len(hav), (" → %s" % hav[:15]) if hav else ""))
    # ================================================================ 7 · PU görünmez
    if pu_grubu is not None:
        kut = [dict(ad="GOMULU_%d" % i, sh=cq.Solid.makeBox(g[2] - g[1], g[4] - g[3], g[6] - g[5], V(g[1], g[3], g[5])), tur="gomulu") for i, g in enumerate(getattr(MOD, "GOMULU", []))]
        kut += [dict(ad="ORTU_%d" % i, sh=sh_, tur="gomulu") for i, sh_ in enumerate(MOD.pu_ortu() if hasattr(MOD, "pu_ortu") else [])]
        R["pu"] = pu_denetle(GW + ARW + kut, pu_grubu, DIS, LO, HI)
        log("PU GÖRÜNMEZ: %d PU parçası · açıkta yüz noktası %d → %s" % (R["pu"]["pu_sayisi"], R["pu"]["acik_nokta"], "GEÇTİ" if R["pu"]["acik_nokta"] == 0 else R["pu"]["ornek"][:5]))
    # ================================================================ 8 · ÇIKTILAR
    glbp = []
    for p in GW + ARW:
        q = dict(p); q.pop("wp", None)
        q["tur"] = "kapak" if p["ad"].startswith("onyuz_kapak") and p.get("tur") == "sac" else (p.get("tur") or "sac")
        if q["tur"] == "pu": q["tur"] = "pu"
        glbp.append(q)
    S._RENK.setdefault("pu", ((0.95, 0.85, 0.30, 1.0), 0.0, 0.9))
    g = S.glb_yaz(os.path.join(CIK, "%s_sac_v2.glb" % kod), glbp)
    log("GLB %s_sac_v1.glb · %d düğüm · %.0f kB (dünya koordinatı, metre · arayüz elemanları kırmızı)" % (kod, g["dugum"], g["bayt"] / 1024.0))
    # CSV parça listesi
    bag = S.bom_topla([p for p in GW if p.get("tur") == "baglanti"])
    kay = [p for p in GW if p.get("tur") == "kaynak"]
    with open(os.path.join(CIK, "%s_parca.csv" % kod), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["bolum", "parca", "malzeme", "kalinlik_mm", "acinim_mm (boy x en)", "kutle_kg", "bukum_sayisi", "R_ic", "K", "PEM_adet", "vida/percin_deligi",
                    "kose_kaynagi", "punta", "acinim_dogrulama", "DFM", "abkant_sirasi"])
        for x in satir:
            w.writerow(["SAC", x["parca"], x["malzeme"], x["t"], x["acinim"], x["kg"], x["bukum"], x["R"], x["K"], x["pem"], x["vida_deligi"], x["kaynak"], x["punta"],
                        x["acinim_dogrulama"], x["dfm"], x["abkant_sira"]])
        for x in prof:
            w.writerow(["PROFİL", x["ad"], "AISI 304", x["kesit"][2], "L %.1f (kesit %g × %g)" % (x["L"], x["kesit"][0], x["kesit"][1]), x["kg"], 0, "", "", "",
                        len([k for k in x["kesikler"] if "civata" in k["tip"] or "percin" in k["tip"] or "vida" in k["tip"]]), "", "", "—", "%d HATA" % len(x["dfm_hata"]), ""])
        for b_ in bag:
            w.writerow(["BAĞLANTI", b_["tanim"], b_["standart"], "", b_["olcu"], "", "", "", "", b_["adet"] if "PEM" in b_["standart"] else "", b_["adet"] if "PEM" not in b_["standart"] else "",
                        "", "", "", b_["tedarik"], ""])
        kz = collections.Counter((p.get("meta", {}) or {}).get("tip", "?") for p in kay)
        kb = collections.Counter()
        for p in kay: kb[(p.get("meta", {}) or {}).get("tip", "?")] += float((p.get("meta", {}) or {}).get("boy", 0) or 0)
        for k, v in kz.items():
            w.writerow(["KAYNAK", "kaynak dikişi · %s" % k, "ER308LSi · TIG 141", "", "toplam %.0f mm" % kb[k], "", "", "", "", "", "", v, "", "", "", ""])
        for p in ([] if not getattr(G, "KAYNAK_ETIKET", None) else G.KAYNAK_ETIKET):
            w.writerow(["KAYNAK (etiket)", p["ad"], p.get("yontem", "TIG 141"), "", p.get("olcu", ""), "", "", "", "", "", "", 1, "", "", "", p.get("not_", "")])
        for b_ in S.bom_topla(G.ARAYUZ):
            w.writerow(["ARAYÜZ (karşı tarafta delik / diş gerekir · gövdeye dahil değil)", b_["tanim"], b_["standart"], "", b_["olcu"], "", "", "", "", "", b_["adet"], "", "", "", b_["tedarik"], ""])
    log("CSV %s_parca.csv · sac %d · profil %d · bağlantı satırı %d (%d adet) · kaynak %d" % (kod, len(satir), len(prof), len(bag), sum(b_["adet"] for b_ in bag), len(kay)))
    # görünümler
    try:
        import _ciz5 as _ciz
        ana = [dict(sh=sekil(p), tur=("kapak" if p["ad"].startswith("onyuz_kapak") else p.get("tur", "sac"))) for p in GW if p.get("tur") != "arayuz" and p.get("tur") != "kaynak"
               and not (p.get("tur") == "baglanti" and sekil(p).BoundingBox().DiagonalLength < 40)]
        _ciz.RENK.update({"kapak": (0.62, 0.78, 0.95), "profil": (0.62, 0.66, 0.72), "pu": (0.95, 0.82, 0.25), "conta": (0.2, 0.2, 0.2), "sac": (0.80, 0.82, 0.85)})
        gorunum_ciz(_ciz, kod, GW, gorunum)
        log("görünümler yazıldı")
    except Exception as e:
        import traceback; traceback.print_exc()
        log("görünüm atlandı: %r" % e)
    if ek_rapor: ek_rapor(R, GW, G)
    say = collections.Counter(p.get("tur") for p in GW)
    R["ozet"] = dict(govde_parca=len([p for p in GW if p.get("tur") != "arayuz"]), sac=len(G.SAC), profil=len(prof), baglanti_elemani=say.get("baglanti", 0),
                     kaynak_dikisi=say.get("kaynak", 0), arayuz=len(G.ARAYUZ), dogrulama_kalan=len(dog_kal), dfm_hata=hata_top, dfm_uyari=uyari_top, profil_dfm_hata=ph,
                     zarf_gecti=R["zarf"]["gecti"], govde_govde=len(ic), dis_cakisma=len(cak), incele=len(inc), havada=len(hav),
                     pu_acik=(R.get("pu") or {}).get("acik_nokta"))
    R["notlar"] = G.NOT; R["log"] = LOG
    with open(os.path.join(CIK, "%s_rapor.json" % kod), "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, indent=1, default=str)
    log("ÖZET %s" % json.dumps(R["ozet"], ensure_ascii=False))
    return R


def _vf(P):
    key = np.round(P.reshape(-1, 3), 3)
    uu, inv = np.unique(key, axis=0, return_inverse=True)
    return uu, inv.reshape(-1, 3)


def gorunum_ciz(_ciz, kod, GW, gorunum):
    secim = [p for p in GW if p.get("tur") not in ("arayuz", "kaynak", "pu") and not (p.get("tur") == "baglanti" and sekil(p).BoundingBox().DiagonalLength < 30)]   # PU kapalı (görünmez) — çizimde gösterilmez
    def ts(p): return "kapak" if p["ad"].startswith("onyuz_kapak") else p.get("tur", "sac")
    _ciz.ciz([dict(sh=sekil(p), tur=ts(p)) for p in secim], os.path.join(BUR, "%s_birlesik.jpg" % kod), elev=18, azim=-62, tol=2.0, boyut=(12, 10),
             baslik="%s · üretim sacı v1 · birleşik (önden-soldan)" % kod)
    sec2 = [p for p in secim if not p["ad"].startswith("onyuz_kapak")]
    _ciz.ciz([dict(sh=sekil(p), tur=ts(p)) for p in sec2 if not gorunum or not gorunum(p["ad"], gizle=True)], os.path.join(BUR, "%s_kapaksiz_ic.jpg" % kod),
             elev=22, azim=-62, tol=2.0, boyut=(12, 10), baslik="%s · kapak / ön paneller gizli (iç kurgu)" % kod)
    if gorunum:
        ex = []
        for p in secim:
            d = gorunum(p["ad"])
            if d is None: continue
            ex.append(dict(sh=sekil(p).translate(V(*d)), tur=ts(p)))
        _ciz.ciz(ex, os.path.join(BUR, "%s_patlatilmis.jpg" % kod), elev=20, azim=-62, tol=2.0, boyut=(13, 11), baslik="%s · patlatılmış görünüş" % kod)


def pu_denetle(GW, pu_mu, DIS, LO, HI, ADIM=10.0, OFS=0.4):
    """her PU yüzü ≤ ADIM aralıkla örneklenir, yüz normali boyunca OFS DIŞARI kaydırılır · nokta bir sacın / başka PU'nun / gömülü elemanın (gövde ya da v8zq)
    İÇİNDE olmalı (VTK kapalı yüzey testi) · değilse PU yüzü havaya bakıyor (görünür / sac ile PU arası boşluk)"""
    pu = [p for p in GW if pu_mu(p["ad"])]
    ort = []
    for p in GW:                                                               # gövde + arayüz elemanları (delikteki cıvata / pul) + gömülü eleman zarfları
        P = ucgen(sekil(p), 0.05, 0.2)
        if not len(P): continue
        uu, F = _vf(P); ort.append((p["ad"], P.reshape(-1, 3).min(0), P.reshape(-1, 3).max(0), uu, F))
    acik, toplam = [], 0
    for p in pu:
        sh = sekil(p); Q = []
        for f in sh.Faces():
            vs, tr = f.tessellate(0.05, 0.2)
            Vv = np.array([[q.x, q.y, q.z] for q in vs]); T = np.array(tr)
            if not len(T): continue
            Pp = Vv[T]; n = np.cross(Pp[:, 1] - Pp[:, 0], Pp[:, 2] - Pp[:, 0]); ln = np.linalg.norm(n, axis=1); ar = ln / 2
            for k in range(len(T)):
                if ar[k] < 1e-9: continue
                nk = n[k] / ln[k]
                m = max(1, int(math.ceil(math.sqrt(2 * ar[k]) / ADIM)))
                for a_ in range(m):
                    for b_ in range(m - a_):
                        u, v = (a_ + 1 / 3) / m, (b_ + 1 / 3) / m
                        Q.append(Pp[k, 0] + u * (Pp[k, 1] - Pp[k, 0]) + v * (Pp[k, 2] - Pp[k, 0]) + nk * OFS)
        Q = np.array(Q); toplam += len(Q)
        if not len(Q): continue
        # yüz normali dışa mı? (OCC tessellate yönü katı dışına) — güvence: katının içine düşen noktalar ters çevrilir
        ok = np.zeros(len(Q), bool)
        for ad, lo, hi, uu, F in ort:
            if ad == p["ad"]: continue
            m = ((Q >= lo - 1e-6) & (Q <= hi + 1e-6)).all(1) & ~ok
            if not m.any(): continue
            ok[np.where(m)[0][GD.icerde(GD.vtk_yuzey(uu, F), Q[m])]] = True
        if not ok.all():
            idx = np.where(~ok)[0]; R = Q[idx]
            mm = ((LO[:, None, :] <= R[None, :, :] + 1e-6) & (HI[:, None, :] >= R[None, :, :] - 1e-6)).all(2) if len(R) * len(LO) < 4e7 else None
            if mm is not None:
                for j in np.where(mm.any(1))[0]:
                    if not DIS[j].kapali: continue
                    sel = np.where(mm[j] & ~ok[idx])[0]
                    if not len(sel): continue
                    ok[idx[sel[GD.icerde(DIS[j].yz(), R[sel])]]] = True
        for q in Q[~ok]: acik.append((p["ad"], np.round(q, 1).tolist()))
    orn = collections.defaultdict(list)
    for a_, q_ in acik:
        if len(orn[a_]) < 12: orn[a_].append(q_)
    return dict(pu_sayisi=len(pu), nokta=toplam, acik_nokta=len(acik), ornek=acik[:60], ornek_parca=dict(orn), parca_bazinda=dict(collections.Counter(a for a, _q in acik)))
