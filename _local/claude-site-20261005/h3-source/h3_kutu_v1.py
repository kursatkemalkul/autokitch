# -*- coding: utf-8 -*-
"""HAT VERSİYON 3 · E KUTU KATLAMA ADAPTÖRÜ v1 (30 Eyl 2026 · Claude · YEREL) — montajda 'import h3_kutu_v1 as KC' (kutu_cad_v14 yerine).
kutu_cad_v14 YENİDEN ÇİZİLMEZ ve DEĞİŞMEZ: bütün sabitler / kinematik işlevler (quat, blank_acilar, DUGUM, CORNER, uygula, grup_matrisi, blank_dunya …)
buradan AYNEN yayımlanır; yalnız PARÇA LİSTESİ (PARCALAR) v3 için yeniden kurulur.

v2 → v3 (Kemal HAT v2.7: "çöpü kaldır komple sağa çek çekmeceleri" · dolabın soğutması + panosu dolabın KENDİ teknik sütununda, K'nın altında):
  ÇIKAN   icecek_* (6 koli + altlık = 7 parça) → içecek yedeği makinenin üstündeki U_KE deposunda (h3_ust_depo_v1 · v2 ile aynı)
          v2'nin ealt_* (Secop + pano + perde + gider + panjur) YOK → dolabın teknik sütunu (h3_store_v1: Secop NLE8.8CN + pano + kaşar / sucuk deposu)
  YENİ    ecop_*  ROBOT ÇÖPÜ (v2'de dolabın sağ ucundaki şerit 3810–4000; v3'te dolap K'nın altına uzadığı için E'nin sol altında):
                  store_cad_v14 B_COP'un parçaları AYNEN (15 L kova 165 × 300 × 400 · poşet · kızak · 45° düşme oluğu · 130 × 130 yaylı klape + menteşe + yaprak)
                  · kova + kızak + poşet E gövdesinde (sol dikmenin arkası, asansör ray plakasının solu) · klape + oluk SOL ALT KANADIN iç yüzünde (kanatla açılır;
                  kova öne çekilerek boşaltılır) · B şeridinin kendi ön panelleri / klipsleri gerekmez (kanat panel)
  DEĞİŞEN onyuz_alt_kanat_sol: klape açıklığı 130 × 130 (dış yüz) + klapenin içe dönme cebi (arkası)
KLAPE (dünya): x 4464–4594 · y 610–740 = h3_store_v1.KLAPE_AC (montaj metni okur) · menteşe y 748.
KOORDİNAT: E yereli (kutu_cad_v14 ile aynı) — x 0…830 (dünya = x + 4400) · y yerden · z ön +79 / arka −830.
Çalıştır (öz denetim): python ob_calistir.py h3/h3_kutu_v1.py"""
import math, os, sys, time, importlib.util as _ilu

H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_hesap_v1 as HS
import kutu_cad_v14 as E14

# ================================================================ kutu_cad_v14'ün HER ŞEYİ (sabitler + işlevler) aynen ================================================================
for _k, _v in list(vars(E14).items()):
    if _k.startswith("__") and _k.endswith("__"):
        continue
    globals()[_k] = _v

V = cq.Vector
PARCALAR = []                      # v3 parça listesi (kimliği korunur: PARCALAR[:] = …) · E14.PARCALAR v1 olarak kalır
DEGISEN, CIKAN, YENI = [], [], []
X_E = HS.E_X[0]                    # 4400
K_DUVAR_DELIKLERI = []             # v3: K'dan gider geçmez (dolabın yoğuşma suyu kendi teknik sütununun tavasında)

# ================================================================ İÇECEK YEDEĞİ: E'DE YOK (v2 ile aynı) ================================================================
ICECEK_YEDEK = dict(x=(0.0, 0.0), y=(0.0, 0.0), z=(0.0, 0.0), koli=0, kutu=0,
                    tasindi="h3_ust_depo_v1.ICECEK_YEDEK (U_KE üst deposu, y 1862–2200 · 6 koli = 144)")


def icecek_on_olcum():
    """E'de içecek yedeği YOK (6 koli U_KE üst deposunda). Dönüş biçimi v6'daki ile aynı (montajın assert'i geçer) — ÖLÇÜM DEĞİL, BEYAN."""
    return dict(on=[], net=(0.0, 0.0), sutun=[dict(x=None, engel=[], bindirme=0.0), dict(x=None, engel=[], bindirme=0.0)],
                sag_bos=0.0, ara=0.0, icecek_yok=True, tasindi=ICECEK_YEDEK["tasindi"])


# ================================================================ ROBOT ÇÖPÜ (store_cad_v14 B_COP → E yereli) ================================================================
# kova + kızak + poşet: x −(3814 − 16) → E yereli 16–198 (sol dikme 1,5–21,5 z ≥ 29 · asansör ray plakası x ≥ 200 z −378…−354) ·
#   y +1,5 (E taban sacı üstü 126) · z −8 (önü +29 = sol dikmenin arkası · kızak arka dudağı −397,5 ↔ şarjör kapı eşiği −399: 1,5)
KOVA_T = (16.0 - 3814.0, 1.5, -8.0)
# klape + menteşe + yaprak + oluk: x −3776 (KLAPE_AC 3840–3970 → dünya 4464–4594 = E yereli 64–194 · kova ağzının 126 / 130 mm üstü · kanat menteşeleri ≤ 41,5) · klape y / z AYNI (kanat dış yüzü +79 = B paneliyle aynı düzlem) ·
#   oluk z −20 (kanadın iç yüzünün 59 gerisinde kalır: B'de 40'lık panel dönüşünün arkasındaydı, E kanadı 20 kalın)
KLAPE_T = (64.0 - 3840.0, 0.0, 0.0)
OLUK_T = (KLAPE_T[0], 0.0, -20.0)
KLAPE_AC = (3840.0 + KLAPE_T[0] + X_E, 3970.0 + KLAPE_T[0] + X_E, 610.0, 740.0)     # dünya 4464–4594 × 610–740
KLAPE_ACI = (0.0, 15.0, 30.0, 45.0)                                                  # robot eli iter · mekanik stop 45° (kalıp rafı ayağı x 90–130, z −90…−50 önünde: 57°'de değerdi)
KOVA_AD = ("cop_kova_kizagi", "robot_cop_kovasi_15L", "robot_cop_poseti")
KANAT_AD = ("klape_levhasi", "klape_mentesesi", "klape_mentese_yapragi", "serit_dusme_olugu")
B_ALINMAYAN = {"serit_on_kapak": "B şeridinin servis paneli — E'de sol alt kanat panel",
               "serit_on_klape_paneli": "B şeridinin klape paneli — klape açıklığı E'nin sol alt kanadında",
               "serit_panel_klipsi_": "B servis panelinin klipsleri — kanat menteşeli"}
E_ALT_BIRIM = [
    ("E_COP", "ROBOT ÇÖPÜ E'nin sol altında (v3 · v2'de dolabın sağ ucunda): 15 L kova 165 × 300 × 400 (poşetli, kızaklı, öne çekilir) · sol alt kanatta "
              "130 × 130 yaylı klape (dünya x 4464–4594 · y 610–740 · menteşe 748) + 45° düşme oluğu (kanadın iç yüzünde) · soğuk DEĞİL", ("ecop_",)),
]
E_ALT_BIRIM_MAP = {k: o for k, _a, o in E_ALT_BIRIM}
E_ALT_ONEK = E_ALT_BIRIM_MAP       # montaj: E_BIRIM += [(k, ad, KC.E_ALT_ONEK[k]) …]


# ================================================================ YARDIMCILAR ================================================================
def _tek(wp):
    if hasattr(wp, "vals"):
        v = [o for o in wp.vals() if isinstance(o, cq.Shape)]
        return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)
    return wp


def _wp(sh):
    return cq.Workplane(obj=sh)


def _ekle(ad, sh, mal, bom=None, kaynak="h3_kutu_v1", grup="SABIT"):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=_wp(sh) if isinstance(sh, cq.Shape) else sh, mal=mal, grup=grup, bom=bom, kaynak=kaynak))
    YENI.append(ad)


_SC = []


def _store():
    """store_cad_v14 ayrı modül nesnesi (montajdaki dolaba dokunmaz) · bir kez"""
    if not _SC:
        sp = _ilu.spec_from_file_location("store_cad_v14_h3kutu", os.path.join(_U, "store_cad_v14.py"))
        m = _ilu.module_from_spec(sp); sp.loader.exec_module(m)
        m.modul()
        _SC.append(m)
    return _SC[0]


def cop_parcalari():
    """B_COP → E yereli: {ad: (şekil, mal, bom, kanatta mı)}"""
    SC = _store()
    out = {}
    for p in SC.PARCALAR:
        if p["birim"] != "B_COP": continue
        a = p["ad"]
        if a.startswith(tuple(B_ALINMAYAN)): continue
        s = _tek(p["wp"])
        if a in KOVA_AD: t = KOVA_T
        elif a == "serit_dusme_olugu": t = OLUK_T
        elif a in KANAT_AD: t = KLAPE_T
        else: raise AssertionError("B_COP parçası sınıfsız: %s" % a)
        out[a] = (s.translate(V(*t)), p["mal"], p.get("bom"), a in KANAT_AD)
    assert set(out) == set(KOVA_AD) | set(KANAT_AD), sorted(out)
    return out


def klape_cebi():
    """sol alt kanada kesilen: dış yüzde 130 × 130 açıklık + arkasında klapenin (levha + menteşe + yaprak) durduğu ve içe döndüğü cep"""
    CP = cop_parcalari()
    bb = cq.Compound.makeCompound([CP[a][0] for a in ("klape_levhasi", "klape_mentesesi", "klape_mentese_yapragi")]).BoundingBox()
    x0, x1 = KLAPE_AC[0] - X_E, KLAPE_AC[1] - X_E
    ac = kut(x0, x1, KLAPE_AC[2], KLAPE_AC[3], Z_ON - 2.0, Z_ON + 1.0).val()
    cep = kut(bb.xmin - 1.0, bb.xmax + 1.0, bb.ymin - 1.0, bb.ymax + 1.0, Z_PANEL - 1.0, Z_ON - 1.5).val()
    return ac.fuse(cep)


def modul():
    """v3 parça listesi: kutu_cad_v14.modul() (v1, dokunulmaz) → kopya − icecek_* + klapeli sol alt kanat + ecop_* · İDEMPOTENT"""
    t0 = time.time()
    E14.modul()
    PARCALAR[:] = []; DEGISEN[:] = []; CIKAN[:] = []; YENI[:] = []
    for p in E14.PARCALAR:
        if p["ad"].startswith("icecek_"):
            CIKAN.append(p["ad"]); continue
        PARCALAR.append(dict(p))
    ad = {p["ad"]: p for p in PARCALAR}
    p = ad["onyuz_alt_kanat_sol"]
    p["wp"] = p["wp"].cut(_wp(klape_cebi()))
    b = list(p["bom"]); b[2] = b[2] + " · v3: robot çöpü klapesi 130 × 130 (dış yüz) + arkasında klape cebi"
    p["bom"] = tuple(b); p["kaynak"] = "kutu_cad_v14 + h3_kutu_v1 klape kesimi"
    DEGISEN.append("onyuz_alt_kanat_sol")
    for a, (s, mal, bom, kanat) in cop_parcalari().items():
        _ekle("ecop_" + a, s, mal, bom, kaynak="store_cad_v14:%s (%s)" % (a, "sol alt kanatta" if kanat else "E gövdesinde"))
    print("h3_kutu_v1 · E v3 parca listesi: %d (v1 %d · cikan %d icecek_ · degisen %d · yeni %d ecop_) · %.0f sn"
          % (len(PARCALAR), len(E14.PARCALAR), len(CIKAN), len(DEGISEN), len(YENI), time.time() - t0))
    return PARCALAR


# ================================================================ DENETİM ================================================================
def _bbk(A, B, pay=0.05):
    return A.xmin < B.xmax - pay and B.xmin < A.xmax - pay and A.ymin < B.ymax - pay and B.ymin < A.ymax - pay and A.zmin < B.zmax - pay and B.zmin < A.zmax - pay


def _hacim(a, b):
    try:
        return a.intersect(b).Volume()
    except Exception:
        return -1.0


def capraz(S, T, esik=0.1):
    S = [(a, s, s.BoundingBox()) for a, s in S]; T = [(a, s, s.BoundingBox()) for a, s in T]
    out = []
    for a, sa, A in S:
        for c, sc, B in T:
            if a == c or not _bbk(A, B):
                continue
            v = _hacim(sa, sc)
            if v > esik or v < 0:
                out.append((round(v, 3), a, c))
    return sorted(out, reverse=True)


DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger))
    print("  %-150s %s %s" % (ad, "GECTI" if sart else "** KALDI **", deger))


def _klape_don(s, aci):
    """klape grubu menteşe ekseni (x boyunca, y 748 · z +72) etrafında İÇE (−z) döner"""
    ky, kz = _store().KLAPE_EKSEN
    return s.rotate(V(0, ky, kz), V(1, ky, kz), aci)


def denetim():
    t0 = time.time()
    if not PARCALAR:
        modul()
    DEN[:] = []
    P = {p["ad"]: p for p in PARCALAR}
    SH = {a: _tek(p["wp"]) for a, p in P.items()}
    YN = list(YENI)
    print("DENETIM h3_kutu_v1 (E v3 · %d parca · yeni %d)" % (len(PARCALAR), len(YN)))
    v1 = {p["ad"]: p for p in E14.PARCALAR}
    ayni = [a for a in v1 if a in P and a not in DEGISEN and P[a]["wp"] is v1[a]["wp"]]
    kontrol("LISTE: v1 %d = v3 %d − yeni %d + cikan %d (icecek_*) · degisen %s · geri kalan %d parca v1 katisinin KENDISI"
            % (len(v1), len(PARCALAR), len(YN), len(CIKAN), DEGISEN, len(ayni)),
            len(v1) == len(PARCALAR) - len(YN) + len(CIKAN) and len(CIKAN) == 7 and len(ayni) == len(v1) - len(CIKAN) - len(DEGISEN))
    kontrol("COP PARCALARI %d (B_COP 13 − B'ye ozgu panel/klips 6) · hepsi gecerli tek kati" % len(YN),
            len(YN) == 7 and all(SH[a].isValid() for a in YN), str([a for a in YN if not SH[a].isValid()]))
    YS = [(a, SH[a]) for a in YN]
    DIGER = [(a, SH[a]) for a in P if a not in YENI and P[a]["grup"] in ("SABIT", "ASANSOR", "SABIT_REF")]
    c1 = capraz(YS, DIGER)
    for x_ in c1[:12]: print("   %10.3f mm3  %s  <->  %s" % x_)
    kontrol("CAKISMA dinlenme: cop %d ↔ E SABIT + ASANSOR + REF %d parca (klapeli sol kanat dahil) > 0,1 mm³ = 0" % (len(YS), len(DIGER)), not c1, "%d bulgu" % len(c1))
    c2 = []
    for i in range(len(YS)):
        c2 += capraz([YS[i]], YS[i + 1:])
    kontrol("CAKISMA cop ↔ cop > 0,1 mm³ = 0", not c2, str(c2[:4]))
    # hareketli gruplar (bütün döngü) + asansör stroku
    BB_Y = cq.Compound.makeCompound([s for _a, s in YS]).BoundingBox()
    HG = [p for p in PARCALAR if p["grup"] not in ("SABIT", "ASANSOR", "SABIT_REF") and p["ad"] not in YENI]
    anlar = [round(0.25 * i, 2) for i in range(int(DONGU / 0.25) + 1)]
    bul4 = []
    for t in anlar:
        W_ = blank_dunya(t)
        for p in HG:
            g = p["grup"]
            M = W_[g] if g.startswith("B_") else grup_matrisi(g, t)
            s = uygula(_tek(p["wp"]), M); b = s.BoundingBox()
            if not _bbk(b, BB_Y):
                continue
            for a, sy in YS:
                if _bbk(b, sy.BoundingBox()):
                    v = _hacim(s, sy)
                    if v > 0.1 or v < 0:
                        bul4.append((round(v, 2), "%s@%.2f" % (p["ad"], t), a))
    kontrol("HAREKETLI GRUPLAR: %d parca × %d an (0 … %.1f sn) ↔ cop parcalari = 0" % (len(HG), len(anlar), DONGU), not bul4, str(bul4[:4]))
    AS = [(p["ad"], _tek(p["wp"])) for p in PARCALAR if p["grup"] == "ASANSOR"]
    strok = SH["asansor_ust_yatak"].BoundingBox().ymin - SH["asansor_somunu"].BoundingBox().ymax
    bul5 = []
    for dy in (0.0, 25.0, 100.0, 200.0, 400.0, strok):
        bul5 += [(v, a + "@dy%.0f" % dy, c) for v, a, c in capraz([(a, s.translate(V(0, dy, 0))) for a, s in AS], YS)]
    kontrol("ASANSOR STROKU 0 … %.0f mm (6 konum) ↔ cop parcalari = 0" % strok, not bul5, str(bul5[:3]))
    # klape içe açılır (robot eli iter) · kanatla birlikte gelen parçalar hariç sabit parçalara değmez
    KL = [a for a in YN if a.endswith(("klape_levhasi",))]
    SAB = [(a, SH[a]) for a in P if P[a]["grup"] in ("SABIT", "ASANSOR", "SABIT_REF") and a not in KL and a != "onyuz_alt_kanat_sol"]
    bul6 = []
    for aci in KLAPE_ACI[1:]:
        bul6 += [(v, "%s@%.0f" % (a, aci), c) for a in KL for v, _a, c in capraz([(a, _klape_don(SH[a], aci))], SAB)]
    kontrol("KLAPE ICE ACILIR %s° (mekanik stop %.0f°) ↔ sabit parcalar (kova, olugun kendisi, kalip rafi, menteşeler) = 0" % (list(KLAPE_ACI[1:]), KLAPE_ACI[-1]),
            not bul6, str(bul6[:4]))
    # sol alt kanat açılır (klape + oluk kanatla döner) ↔ E gövdesi + kova
    KN = ["onyuz_alt_kanat_sol"] + ["ecop_" + a for a in KANAT_AD]
    GOV = [(a, SH[a]) for a in P if P[a]["grup"] in ("SABIT", "ASANSOR", "SABIT_REF") and a not in KN and not a.startswith(("onyuz_mentese_",))]
    bul7 = []
    for aci in KAPI_ACILARI:
        M = kapi_matrisi("onyuz_alt_kanat_sol", aci)
        for a in KN:
            bul7 += [(v, "%s@%d" % (a, aci), c) for v, _a, c in capraz([(a, uygula(SH[a], M))], GOV)]
    kontrol("SOL ALT KANAT %d aci (1°…%.0f°) + uzerindeki klape / oluk ↔ E govdesi + kova = 0" % (len(KAPI_ACILARI), KAPI_MAX_ACI), not bul7, str(bul7[:4]))
    # atma yolu: klape açıklığının arkası (oluk + klape dışında) boş · kova ağzı açıklığın altında
    kova = SH["ecop_robot_cop_kovasi_15L"].BoundingBox(); ol = SH["ecop_serit_dusme_olugu"].BoundingBox()
    x0, x1 = KLAPE_AC[0] - X_E, KLAPE_AC[1] - X_E
    yol = kut(x0, x1, kova.ymax + 1.0, KLAPE_AC[3], ol.zmin, Z_PANEL - 0.5).val()
    dolu = [a for a, s in P.items() if a not in ("ecop_serit_dusme_olugu", "ecop_klape_levhasi") and _bbk(SH[a].BoundingBox(), yol.BoundingBox()) and _hacim(SH[a], yol) > 0.1]
    ust = min(x1, kova.xmax) - max(x0, kova.xmin)
    kontrol("ATMA YOLU: klape arkasi (x %.0f–%.0f · y %.0f–%.0f · z %.0f…%.0f) oluk + klape disinda bos · kova agzi (x %.0f–%.0f) klape acikliginin %.0f / %.0f mm'sinin altinda · oluk alt kenari z %.1f ≤ kova onu %.1f"
            % (x0, x1, kova.ymax + 1.0, KLAPE_AC[3], ol.zmin, Z_PANEL - 0.5, kova.xmin, kova.xmax, ust, x1 - x0, ol.zmin, kova.zmax),
            not dolu and ust >= 0.9 * (x1 - x0) and ol.zmin <= kova.zmax, str(dolu[:4]))
    ion = icecek_on_olcum()
    ge_ = min(_tek(p["wp"]).BoundingBox().ymin for p in PARCALAR if p["grup"] == "SABIT" and not p["ad"].startswith(("ayak_", "plint_on", "onyuz_plint", "asansor_")))
    kontrol("MONTAJ UYUMU: icecek_on_olcum() bos · SABIT govde alti %.2f = Y_PLINT %.0f · cop parcalarinin en onu %.1f ≤ +79 · KLAPE_AC dunya %s" % (
        ge_, Y_PLINT, max(s.BoundingBox().zmax for _a, s in YS), KLAPE_AC),
            ion["on"] == [] and abs(ge_ - Y_PLINT) < 0.05 and max(s.BoundingBox().zmax for _a, s in YS) <= Z_ON + 1e-6)
    kal = [d for d in DEN if not d[1]]
    print("DENETIM h3_kutu_v1: %d madde · %d KALDI · %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    return DEN


if __name__ == "__main__":
    modul()
    D = denetim()
    kal = [d[0] for d in D if not d[1]]
    assert not kal, kal
    sys.stdout.flush(); os._exit(0)
