# -*- coding: utf-8 -*-
"""HAT v3 · HIZLI + ARTIMSAL DENETİMLER (1 Eki 2026 · Claude) — mevcut denetimlerin BİREBİR aynı sonucunu veren paralel / önbellekli sürümleri.
Yöntem (h3_hiz_ortak): döküm bir kez indekslenir (parça → içerik hash'i + kutu), aday çiftler kutu ön elemesiyle AYNI kuralla çıkarılır,
her çiftin OCC sonucu (BRepExtrema mesafesi / kesişim hacmi) (hashA, hashB) anahtarıyla önbellekte — değişmeyen parçaların çiftleri yeniden hesaplanmaz.
Eksik çiftler boş belleğe göre N işçide (her işçi yalnız gerektirdiği parçaları depodan açar, 250 MB dökümü değil).

Kullanım (cwd = arastirma/_uretec, eski zincirle aynı):
  python h3/h3_hiz_denetim.py havada_hedefli      ≡ h3_havada_paralel_v1.py parca K N + birlestir N   (çıktı _dunya_tam/havada_hizli_v1.json)
  python h3/h3_hiz_denetim.py havada_tam [h3/_dunya_tam] ≡ h3_havada_v1.py (tüm makine, eskiden ~2 saat)  (çıktı <DD>/havada_v1.json)
  python h3/h3_hiz_denetim.py envanter h3/_dunya_tam  ≡ cihaz_envanter.py
  python h3/h3_hiz_denetim.py son_elk                ≡ son_denetim_elk.py
  python h3/h3_hiz_denetim.py hepsi                  → havada_hedefli + envanter + son_elk (+ havada_tam, H3_HIZ_TAM=1 ise)"""
import io, json, os, re, sys, time
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import h3_hiz_ortak as HO


def _ok_havada(r, tol):
    d, v = r
    if d == 2: return True                         # istisna → bağlı say (eski koddaki except: ok = True)
    if d == 1: return False                        # IsDone değil
    return v <= tol


def _ust(bi, bj, t):
    return not (bj.xmin > bi.xmax + t or bi.xmin > bj.xmax + t or bj.ymin > bi.ymax + t or bi.ymin > bj.ymax + t or bj.zmin > bi.zmax + t or bi.zmin > bj.zmax + t)


# ================================================================ HEDEFLİ HAVADA (h3_havada_paralel_v1 ile aynı) ================================================================
DEGISEN = ("TOPPING_MODUL|harc", "TOPPING_MODUL|evap_kaseti", "TOPPING_MODUL|arka_duvar_kaset", "TOPPING_MODUL|kaset_penceresi",
           "ROBOT_", "A_GOVDE|a_govde_ust", "A_GOVDE|a_ust_kusak", "U_A_GOVDE|", "QR_GOVDE|servis", "ZEMIN")


def havada_hedefli(DD=None):
    t0 = time.time(); TOL = 0.5
    DD = DD or os.path.join(H3, "_dunya_tam")
    R = [r for r in HO.dokum_indeks(DD) if not r["b"].startswith("INSAN")]
    L = [("%s|%s" % (r["b"], r["a"]), r) for r in R]
    ilk = json.load(io.open(os.path.join(H3, "_dunya", "havada_v1.json"), encoding="utf-8"))
    ilk_havada = set(u for d in ilk["bilesen"] for u in d["uye"])
    aday = [i for i, (ad, r) in enumerate(L) if ad.startswith(("ELK_", "DUZ_") + DEGISEN) or ad in ilk_havada]
    B = [r["bb"] for ad, r in L]
    ciftler = []
    for i in aday:
        bi = B[i]
        for j in range(len(L)):
            if j == i: continue
            if _ust(bi, B[j], TOL): ciftler.append((i, j))
    C = HO.hesapla("M", [(L[i][1]["h"], L[j][1]["h"]) for i, j in ciftler])
    kom = {i: [] for i in aday}
    for i, j in ciftler:
        if _ok_havada(C[(L[i][1]["h"], L[j][1]["h"])], TOL): kom[i].append(j)
    json.dump(dict(n=len(L), kom={str(k): v for k, v in kom.items()}), io.open(os.path.join(DD, "havada_par_hiz.json"), "w", encoding="utf-8"))
    # ---- birleştir (h3_havada_paralel_v1 'birlestir' ile aynı) ----
    kom = {i: set(v) for i, v in kom.items()}
    for i, v in list(kom.items()):
        for j in v:
            if j in kom: kom[j].add(i)
    A = set(aday)
    gor = set(j for j in range(len(L)) if j not in A) | set(i for i in aday if B[i].ymin <= TOL)
    degisti = True
    while degisti:
        degisti = False
        for i in aday:
            if i not in gor and kom[i] & gor:
                gor.add(i); degisti = True
    havada = [L[i][0] for i in aday if i not in gor]
    print("HEDEFLİ HAVADA PARALEL (v3.4): %d parça döküm · %d aday (değişen makine parçaları dahil) · HAVADA %d · %.0f sn" % (len(L), len(aday), len(havada), time.time() - t0))
    for h in havada[:80]: print("   HAVADA:", h)
    json.dump(dict(aday=len(aday), havada=havada), io.open(os.path.join(DD, "havada_hizli_v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    return havada


# ================================================================ TAM HAVADA (h3_havada_v1 + denetim_temas_v1.havada ile aynı) ================================================================
def _tur(ad):
    a = ad.lower()
    if re.search(r"motor", a) and not re.search(r"plaka|braket|kasnag|mil|kaplin|konsol|yatak|flans", a): return "MOTOR"
    if re.search(r"surucu|sürücü|beckhoff|plc|siwarex|ndr-|hdr-|guc_|ups|klemens|role|din_ray|kart", a): return "BEYIN/SURUCU"
    if re.search(r"pano", a): return "PANO"
    if re.search(r"kablo|hortum", a): return "KABLO/HORTUM"
    if re.search(r"sensor|sensör", a): return "SENSOR"
    return "DIGER"


def havada_tam(DD=None):
    import denetim_temas_v1 as DT
    t0 = time.time(); tol = 0.5; zemin_y = 0.0
    DD = DD or os.path.join(H3, "_dunya")
    R = HO.dokum_indeks(DD)
    print("döküm: %d parça · %.0f sn" % (len(R), time.time() - t0)); sys.stdout.flush()
    L = [("%s|%s" % (r["b"], r["a"]), r, r["bb"]) for r in R if not r["b"].startswith(("INSAN",)) and r["bb"] is not None]
    n = len(L)
    sirali = sorted(range(n), key=lambda i: L[i][2].xmin)
    ciftler = []
    for ii, i in enumerate(sirali):
        bi = L[i][2]
        for j in sirali[ii + 1:]:
            bj = L[j][2]
            if bj.xmin > bi.xmax + tol: break
            if bj.ymin > bi.ymax + tol or bi.ymin > bj.ymax + tol or bj.zmin > bi.zmax + tol or bi.zmin > bj.zmax + tol: continue
            ciftler.append((i, j))
    C = HO.hesapla("M", [(L[i][1]["h"], L[j][1]["h"]) for i, j in ciftler])
    kom = [[] for _ in range(n)]
    for i, j in ciftler:
        if _ok_havada(C[(L[i][1]["h"], L[j][1]["h"])], tol):
            kom[i].append(j); kom[j].append(i)
    kok = [i for i in range(n) if L[i][2].ymin <= zemin_y + tol]
    gor = [False] * n; yig = list(kok)
    for i in kok: gor[i] = True
    while yig:
        i = yig.pop()
        for j in kom[i]:
            if not gor[j]: gor[j] = True; yig.append(j)
    bil = []; gor2 = list(gor)
    for i in range(n):
        if gor2[i]: continue
        uy, yig = [], [i]; gor2[i] = True
        while yig:
            k = yig.pop(); uy.append(k)
            for j in kom[k]:
                if not gor2[j]: gor2[j] = True; yig.append(j)
        en = max(uy, key=lambda k: L[k][2].xlen * L[k][2].ylen * L[k][2].zlen)
        bil.append(dict(en=L[en][0], uye=[L[k][0] for k in uy], bb=L[en][2]))
    bil.sort(key=lambda d: -len(d["uye"]))
    son = dict(parca=n, aday=len(ciftler), kok=len(kok), bagli=sum(gor), bilesen=bil, sure=time.time() - t0)
    DT.yaz(son, en_cok=60, baslik="HAVADA · TÜM MAKİNE v3.1")
    rap = []
    for d in son["bilesen"]:
        uy = d["uye"]
        tl = sorted(set(_tur(u.split("|", 1)[1]) for u in uy))
        rap.append(dict(en=d["en"], uye=uy, tur=tl, bb=[round(v, 1) for v in (d["bb"].xmin, d["bb"].xmax, d["bb"].ymin, d["bb"].ymax, d["bb"].zmin, d["bb"].zmax)]))
    json.dump(dict(parca=son["parca"], bilesen=rap), io.open(os.path.join(DD, "havada_v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    from collections import Counter
    c = Counter(t for r in rap for t in r["tur"])
    print("HAVADA bileşen türleri:", dict(c))
    return rap


# ================================================================ CİHAZ ENVANTERİ (cihaz_envanter.py ile aynı) ================================================================
CIHAZ = re.compile(r"(motoru|_motor$|motor_govde|sensoru|_sensor$|sensoru_(alt|ust)|_fani_\d|^fan_(sol|sag)_\d|valf_adasi|pompasi|^sogutma_grubu_kompresor$|KLF66$|PM1704|SMT-8M_\d|PulsaJet_AAB|yuk_hucresi|reed_(acik|kapali)|isik_perdesi_(ust|alt)$|emniyet_sensoru(_alt)?$|kuru_surucu_\d|EC5000_354)", re.I)
HARIC_BIRIM = ("CEK_", "E_", "QR_", "F_TP10", "HAVA_KOMPRESOR", "INSAN", "TEZGAH", "D_BULASIK", "K_BULASIK", "ROBOT", "URUN", "BULASIK")
HARIC_AD = re.compile(r"braket|bayrag|hedefi|miknatis|lami|tutucu|somun|kizak|kablo|soket|kapak|zarf", re.I)
TASIYICI = re.compile(r"^ELK_|motor_kablosu|_m12_soket|M8_kablo|M8_soketi|EC5000_kablo|kuru_din_rayi|tahrik_rulosu_EC5000_kablo", re.I)
BILINEN = {"donus_motoru": "araba üstünde · enerji zincirinden", "tabla_home_sensoru": "araba üstünde · enerji zincirinden",
           "acici_motoru_on": "açıcı hazır alınır · yalnız görsel (Kemal 1 Eki)", "acici_motoru_arka": "açıcı hazır alınır · yalnız görsel (Kemal 1 Eki)",
           "valf_adasi_SS5Y3-20-04": "pano içinde · DIN ray/valf kablosu pano iç tesisatı", "yb_kasnak_motor": "cihaz değil: motor kasnağı (kayışla motora bağlı)",
           **{_a36: "A açıcı paketi · tedarikçinin kendi emniyet devresi (Kemal 1 Eki: açıcı çevresindeki elektrik kalkar)" for _a36 in ("onyuz_emniyet_sensoru", "onyuz_emniyet_sensoru_alt", "onyuz_isik_perdesi_ust", "onyuz_isik_perdesi_alt")}}


def envanter(DD):
    R = HO.dokum_indeks(DD, log=lambda *a: None)
    L = [("%s|%s" % (r["b"], r["a"]), r["b"], r) for r in R]
    cihazlar = [(a, b, r) for a, b, r in L if CIHAZ.search(a.split("|", 1)[1]) and not b.startswith(HARIC_BIRIM) and not HARIC_AD.search(a.split("|", 1)[1])]
    tas = [(a, r) for a, b, r in L if TASIYICI.search(b) or TASIYICI.search(a.split("|", 1)[1])]
    t = 0.6
    # 1 · cihaz + ona değen kendi birimindeki parçalar (kutu ön elemesi eskisiyle aynı: _yakin)
    c1 = [(r["h"], r2["h"]) for a, b, r in cihazlar for a2, b2, r2 in L if b2 == b and a2 != a and _ust(r["bb"], r2["bb"], t)]
    C = HO.hesapla("M", c1, log=lambda *a: None)

    def yakin(r1, r2):
        if not _ust(r1["bb"], r2["bb"], t): return False
        d, v = C[(r1["h"], r2["h"])]
        if d == 2: raise RuntimeError("BRepExtrema istisnası (eski kod da burada durur): %s ↔ %s" % (r1["a"], r2["a"]))
        return d == 0 and v <= t
    gruplar = [[r] + [r2 for a2, b2, r2 in L if b2 == b and a2 != a and yakin(r, r2)] for a, b, r in cihazlar]
    # 2 · grup ↔ taşıyıcılar · eski kod any() ile İLK temasta durur → burada da: her cihazın aday çiftleri eski sırayla, turlar hâlinde
    #     (her turda çözülmemiş cihazların sıradaki K çifti birlikte paralel hesaplanır) · sonuç any() ile aynı (sıra yalnız süreyi etkiler)
    aday = [[(g, r2) for g in G for ta, r2 in tas if _ust(g["bb"], r2["bb"], t)] for G in gruplar]
    sonuc = [None] * len(cihazlar); konum = [0] * len(cihazlar); K = 6
    while True:
        acik = [k for k in range(len(cihazlar)) if sonuc[k] is None]
        for k in acik:                                                                # önbellekte olanlarla çözülebilenler
            while sonuc[k] is None and konum[k] < len(aday[k]) and (aday[k][konum[k]][0]["h"], aday[k][konum[k]][1]["h"]) in C:
                g, r2 = aday[k][konum[k]]
                if yakin(g, r2): sonuc[k] = True
                konum[k] += 1
            if sonuc[k] is None and konum[k] >= len(aday[k]): sonuc[k] = False
        acik = [k for k in range(len(cihazlar)) if sonuc[k] is None]
        if not acik: break
        iste = [(g["h"], r2["h"]) for k in acik for g, r2 in aday[k][konum[k]:konum[k] + K]]
        C.update(HO.hesapla("M", iste, log=lambda *a: None))
    kablosuz = []
    for (a, b, r), ok in zip(cihazlar, sonuc):
        if not ok:
            bb = r["bb"]; kablosuz.append((a, [round(v) for v in (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)]))
    bil = [(a, b) for a, b in kablosuz if a.split("|", 1)[1] in BILINEN]
    gercek = [(a, b) for a, b in kablosuz if a.split("|", 1)[1] not in BILINEN]
    print("CİHAZ ENVANTERİ: %d cihaz · KABLOSUZ %d (bilinen istisna %d)" % (len(cihazlar), len(gercek), len(bil)))
    for a, b in gercek: print("   KABLOSUZ:", a, b)
    for a, b in bil: print("   istisna:", a, "·", BILINEN[a.split("|", 1)[1]])
    return gercek


# ================================================================ SON DENETİM ELEKTRİK (son_denetim_elk.py ile aynı) ================================================================
def son_elk():
    import h3_elektrik_v1 as EL, h3_duzeltme_v1 as DZM
    R = HO.dokum_indeks(os.path.join(H3, "_dunya"), log=lambda *a: None)
    D = [("%s|%s" % (r["b"], r["a"]), r) for r in R]
    EL.yukle()
    adaylar = []                                                                     # (etiket, ad, hash, kutu)

    def ekle(etiket, sh):
        b = sh.BoundingBox()
        adaylar.append((etiket, HO.kaydet(sh), (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)))
    for p in EL.PARCALAR: ekle(p["ad"], EL.dunya(p))
    DZM.kur()
    for p in DZM.PARCALAR: ekle("DUZ:" + p["ad"], DZM.dunya(p))

    def ust(a, b, t=0.05):
        return a[0] < b[1] - t and b[0] < a[1] - t and a[2] < b[3] - t and b[2] < a[3] - t and a[4] < b[5] - t and b[4] < a[5] - t
    cif = []
    for et, h, bb in adaylar:
        for ad, r in D:
            sb = (r["bb"].xmin, r["bb"].xmax, r["bb"].ymin, r["bb"].ymax, r["bb"].zmin, r["bb"].zmax)
            if ust(bb, sb): cif.append((et, ad, h, r["h"]))
    C = HO.hesapla("K", [(h, h2) for et, ad, h, h2 in cif], log=lambda *a: None)
    bul = []
    for et, ad, h, h2 in cif:
        d, v = C[(h, h2)]
        v = -1.0 if d == 2 else v
        if v > 0.5 or v < 0: bul.append((round(round(v, 1), 1), et, ad))
    for x in sorted(bul, reverse=True)[:40]: print("  ÇAKIŞMA %8.1f mm³  %-42s ↔ %s" % x)
    print("SON DENETİM (elektrik + düzeltme ↔ delikleri açılmış makine, istisnasız): %d çakışma" % len(bul))
    return bul


if __name__ == "__main__":
    t0 = time.time()
    k = sys.argv[1]
    DD_ = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None                  # döküm klasörü (cwd'ye göre) · yoksa eski betiklerin varsayılanı
    if k == "havada_hedefli": havada_hedefli(DD_)
    elif k == "havada_tam": havada_tam(DD_)
    elif k == "envanter": envanter(DD_ or os.path.join(H3, "_dunya_tam"))
    elif k == "son_elk": son_elk()
    elif k == "hepsi":
        son_elk(); havada_hedefli(); envanter(os.path.join(H3, "_dunya_tam"))
        if os.environ.get("H3_HIZ_TAM"): havada_tam(os.path.join(H3, "_dunya_tam"))
    else: raise SystemExit(__doc__)
    print("hız · %s bitti · %.1f sn" % (k, time.time() - t0))
    sys.stdout.flush(); os._exit(0)
