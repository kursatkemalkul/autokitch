# -*- coding: utf-8 -*-
"""HAT v3 · KATALOG STEP YÜKLEYİCİ v1 (1 Eki 2026 · Claude · YEREL) — QR ana panosunun DIN rayı cihazları ÜRETİCİ STEP'LERİNDEN
(Kemal 1 NUMARALI KURAL + "motor koy deyince kutu modelleyip bırakıyorsun": üretici STEP'i + gerçek ölçü).

KULLANIM (h3_elk_qr_v1.din() kutularıyla AYNI yerleşim sözleşmesi):
    import katalog_step_v1 as KS
    sh = KS.cihaz_step("A9R21440", x0, RAY_A_Y, RAY_Z[1], yon=-1)    # cq.Compound · dünya koordinatı
    w, h, d = KS.olcu("A9R21440")                                    # gerçek dış ölçü (ray boyu × düşey × derinlik, tırnak / klemens dahil)
  · ray ekseni dünya x · cihazın SOL kenarı (min x) = x0
  · ray merkezi (TS35 oluğunun ortası) = y_ray
  · z_plaka = montaj plakasının ön yüzü (rayın arkası) · ray önü = z_plaka + yon × 7,5 (TS35 × 7,5) · cihazın ray oluğu tabanı (35 mm'lik
    flanşların oturduğu yüz) ray önüne oturur · yon = −1: cihaz önü −z (QR panosu: kapak z 675'te) · yon = +1: önü +z.
  · tırnak / kilit dilleri flanşın ARKASINA kıvrılır → dolu kutu ray modeliyle küçük bindirme normaldir (gerçek ray içi boş şapka profil).

YÖN (her STEP ayrı ayrı incelendi · ışın profili + kesit · görünüşler stepan/*.png):
  STEP ekseni → dünya ekseni (kanonik çerçeve: x ray boyu · y yukarı · z ray önü 0, cihaz önü −z) · hepsi DÖNME (det +1, ayna yok)
  A9S65440 iSW   x→−x  y→+y  z→−z  (STEP'te ön +z: kol + vida başları · arka z −74,44 · kilit dili altta, y −)
  A9R21440 iID   x→−x  y→+y  z→−z  (aynı Schneider düzeni · arka z 0)
  NDR-120-24     y→+x  z→+y  x→+z  (STEP'te x derinlik: ön x −13,9, DIN klipsi x +99…+110 · z yukarı: kilit sürgüsü altta z −54,6)
  PR100378       x→−x  z→+y  y→+z  (STEP'te y derinlik: ön y −103, klipsler y +1,8…+7,3 · z yukarı: RS485 üstte, X2 / X4 altta, sıra föyle aynı)
  1085256        x→−x  y→+y  z→−z  (ön z +98,4 RJ45 · arka z 0 · üst kanca + alttan besleme fişi)
  ray oluğu (STEP koordinatı): ray_on = flanşların oturduğu yüz (derinlik ekseni), ray_h = oluğun ortası (yükseklik ekseni) — tablo KATALOG.

SADELEŞTİRME (3B sayfa için): dışarıdan GÖRÜNMEYEN katılar atılır (18 yönden 0,5 mm ızgara ışın · ilk çarpılan katı görünür sayılır ·
  ≥ 4 vuruş = ≥ ~1 mm² görünür alan) · dış zarfı tanımlayan katılar (sınır kutusuna değen) her durumda kalır → dış ölçü DEĞİŞMEZ (denetlenir) ·
  STEP içindeki hazır üçgen ağı silinir (BRepTools.Clean · montaj kendi toleransıyla ağlar: TC_AG 0,6 / 1,0).
ÖNBELLEK: h3/_katalog_cache/<KOD>_v1.brep.gz (kanonik, sadeleştirilmiş · gzip'li ASCII BREP) + .json (imza, ölçü, sayım) · STEP değişirse (sha1) ya da tablo
  değişirse yeniden kurulur · STEP bulunamazsa önbellek kullanılır.
STEP ARAMA: arastirma/katalog/step (proje kütüphanesi) → $AUTOKITCH_KATALOG_STEP → oturum indirme klasörü (katalog_v34).
KOMUT: python katalog_step_v1.py [--yeniden]  → 5 cihazı kurar + tablo basar (ölçü · ray ofsetleri · katı / yüz / üçgen önce → sonra)."""
import gzip, hashlib, io, json, math, os, sys, time

H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3); KOK = os.path.dirname(U)          # KOK = arastirma
import cadquery as cq

SURUM = "v1"
ONB = os.path.join(H3, "_katalog_cache")
ARAMA = [os.path.join(KOK, "katalog", "step"),
         os.environ.get("AUTOKITCH_KATALOG_STEP", ""),
         r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\katalog_v34"]
RAY_DERINLIK = 7.5                         # TS35 × 7,5 (EN 60715)
TOL_AG = (0.6, 1.0)                        # hat3_montaj TC_AG (kiyma_cad_v6.ag 0,6 / 1,0) · üçgen sayımı bununla
GORUNUR = dict(adim=0.5, esik=4, ag=(0.2, 0.3), kabuk_oran=0.6)
#   sade "gorunur": yalnız HİÇ görünmeyen katı atılır (vuruş < esik) · "kabuk" (ağır modeller): görünür yüzey oranı (vuruş × adım² / katı alanı,
#   18 yönün toplamı · tam açık dışbükey ≈ 4,5 · gövde kabuğu ≈ 1,6) < kabuk_oran olan iç bileşen (PCB, soket, pim) de atılır; dış zarf kalır

# ---------------------------------------------------------------- KATALOG (yön + ray oluğu: STEP koordinatında, elle ölçüldü) ----------------------------------------------------------------
KATALOG = {
    "A9S65440": dict(dosya="a9s65440.stp", uretici="Schneider Electric", ad="Acti9 iSW yük ayırıcı 4P 40 A 415 V",
                     kaynak="https://www.se.com/uk/en/product/A9S65440/switch-disconnector-isw-4p-40-a-415-v/",
                     eksen=("-x", "+y", "-z"), ray_on=-68.94, ray_h=48.16,
                     olcum="oluk y 30,81 (kilit dili yüzü) – 65,51 (üst basamak) = 34,7 · oluk tabanı z −68,94 · arka z −74,44 (rayın 5,5 arkası)"),
    "A9R21440": dict(dosya="a9r21440.stp", uretici="Schneider Electric", ad="Acti9 iID kaçak akım rölesi 4P 40 A 30 mA tip A",
                     kaynak="https://www.se.com/uk/en/product/A9R21440/acti9-iid-rccb-4p-40a-30ma-type-a/",
                     eksen=("-x", "+y", "-z"), ray_on=5.50, ray_h=43.30,
                     olcum="oluk y 25,70 (kilit dili) – 60,90 (üst basamak) = 35,2 · oluk tabanı z 5,5 · arka z 0 (rayın 5,5 arkası)"),
    "NDR-120-24": dict(dosya="ndr-120-24.stp", uretici="MEAN WELL", ad="NDR-120-24 DIN ray güç kaynağı 24 V 120 W",
                       kaynak="https://www.meanwell.com/webapp/product/search.aspx?prod=NDR-120 (3D OUTLINE: NDR-120-3D.zip)",
                       eksen=("+y", "+z", "+x"), ray_on=105.35, ray_h=11.95,
                       olcum="sac klips yan kulakları arka kenarı x 105,35 (ray önü) · alt basamak z −6,0 – üst kanca cebi z 29,9 · kilit sürgüsü altta"),
    "PR100378": dict(dosya="pr100378_without_wlan.stp", uretici="KUNBUS (Revolution Pi)", ad="RevPi Connect 4 (4 GB RAM · 32 GB eMMC · WLAN'sız)",
                     kaynak="https://revolutionpi.com/en/support/downloads (STEP Files > RevPi Connect 4 · RevPi-Connect-4-without-WLAN.step)",
                     eksen=("-x", "+z", "+y"), ray_on=0.77, ray_h=43.75, sade="kabuk",
                     olcum="oluk z 26,05 – 61,45 = 35,4 · flanş cebi y 0,77 · arka y 7,27 (rayın 6,5 arkası) · PR100378 = WLAN YOK (RP-SMA yalnız 100377/379/380)"),
    "1085256": dict(dosya="1085256.stp", uretici="Phoenix Contact", ad="FL SWITCH 1008N endüstriyel switch 8 × RJ45 24 V",
                    kaynak="https://www.phoenixcontact.com/en-pc/products/industrial-ethernet-switch-fl-switch-1008n-1085256",
                    eksen=("-x", "+y", "-z"), ray_on=6.00, ray_h=75.855,
                    olcum="oluk y 58,17 (alt basamak) – 93,54 (üst kanca cebi) = 35,4 · oluk tabanı z 6,0 · arka z 0"),
}
KODLAR = list(KATALOG)
_BELLEK = {}


# ---------------------------------------------------------------- yardımcılar ----------------------------------------------------------------
def _step_yolu(dosya):
    for d in ARAMA:
        if d and os.path.isfile(os.path.join(d, dosya)): return os.path.join(d, dosya)
    return None


def _sha1(yol):
    h = hashlib.sha1()
    with open(yol, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def _obb(sh):
    """kesin sınır kutusu (ağsız, geometriden)"""
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    b = Bnd_Box(); BRepBndLib.AddOptimal_s(sh.wrapped, b, False, False)
    return b.Get()                                                     # xmin, ymin, zmin, xmax, ymax, zmax


def _matris(eksen):
    """("-x", "+y", "-z") → dünya X = −STEP x ... · 3 × 3 satır matrisi · det +1 denetimi"""
    M = []
    for e in eksen:
        r = [0.0, 0.0, 0.0]; r["xyz".index(e[1])] = 1.0 if e[0] == "+" else -1.0; M.append(r)
    det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
           + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    assert abs(det - 1.0) < 1e-9, ("ayna dönüşüm (det %.0f): eksen tablosu yanlış" % det, eksen)
    return M


def _temizle(sh):
    from OCP.BRepTools import BRepTools
    BRepTools.Clean_s(sh.wrapped)
    return sh


def _ucgen(sh, tol=TOL_AG, temiz=True):
    """montaj toleransında üçgen sayısı (temiz=False: STEP'in hazır ağı varsa o sayılır)"""
    s = _temizle(sh.copy()) if temiz else sh
    try:
        vs, ts = s.tessellate(*tol)
        return len(ts)
    except Exception:
        return -1


def _yon_vektorleri():
    out = []
    for i in range(3):
        for s in (1.0, -1.0):
            d = [0.0, 0.0, 0.0]; d[i] = s; out.append(d)
    k = 1.0 / math.sqrt(2.0)
    for i, j in ((0, 1), (0, 2), (1, 2)):
        for si in (1.0, -1.0):
            for sj in (1.0, -1.0):
                d = [0.0, 0.0, 0.0]; d[i] = si * k; d[j] = sj * k; out.append(d)
    return out


def _gorunurluk(katilar, adim=None, esik=None, ag=None):
    """her katının dışarıdan kaç ışınla İLK çarpılan olduğunu sayar (VTK StaticCellLocator) · döner: vuruş listesi"""
    import vtk
    adim = adim or GORUNUR["adim"]; ag = ag or GORUNUR["ag"]
    pts = vtk.vtkPoints(); polys = vtk.vtkCellArray(); sid = vtk.vtkIntArray(); sid.SetName("kati")
    for i, s in enumerate(katilar):
        q = _temizle(s.copy())
        try: vs, ts = q.tessellate(*ag)
        except Exception: continue
        o = pts.GetNumberOfPoints()
        for v in vs: pts.InsertNextPoint(v.x, v.y, v.z)
        for a, b, c in ts:
            polys.InsertNextCell(3); polys.InsertCellPoint(a + o); polys.InsertCellPoint(b + o); polys.InsertCellPoint(c + o); sid.InsertNextValue(i)
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(polys)
    loc = vtk.vtkStaticCellLocator(); loc.SetDataSet(pd); loc.SetNumberOfCellsPerNode(8); loc.BuildLocator()
    xmin, xmax, ymin, ymax, zmin, zmax = pd.GetBounds()
    c = [(xmin + xmax) / 2.0, (ymin + ymax) / 2.0, (zmin + zmax) / 2.0]
    R = math.sqrt((xmax - xmin) ** 2 + (ymax - ymin) ** 2 + (zmax - zmin) ** 2) / 2.0 + 2.0
    kose = [(x, y, z) for x in (xmin, xmax) for y in (ymin, ymax) for z in (zmin, zmax)]
    vur = [0] * len(katilar)
    t = vtk.reference(0.0); x = [0.0, 0.0, 0.0]; pc = [0.0, 0.0, 0.0]; sub = vtk.reference(0); cid = vtk.reference(0); hc = vtk.vtkGenericCell()
    for d in _yon_vektorleri():
        # ışın düzlemi tabanı (d'ye dik u, v)
        a = [1.0, 0.0, 0.0] if abs(d[0]) < 0.9 else [0.0, 1.0, 0.0]
        u = [d[1] * a[2] - d[2] * a[1], d[2] * a[0] - d[0] * a[2], d[0] * a[1] - d[1] * a[0]]
        lu = math.sqrt(sum(q * q for q in u)); u = [q / lu for q in u]
        v = [d[1] * u[2] - d[2] * u[1], d[2] * u[0] - d[0] * u[2], d[0] * u[1] - d[1] * u[0]]
        pu = [sum((k_[i] - c[i]) * u[i] for i in range(3)) for k_ in kose]; pv = [sum((k_[i] - c[i]) * v[i] for i in range(3)) for k_ in kose]
        su = min(pu) - adim
        while su <= max(pu) + adim:
            sv = min(pv) - adim
            while sv <= max(pv) + adim:
                p1 = [c[i] + u[i] * su + v[i] * sv - d[i] * R for i in range(3)]
                p2 = [c[i] + u[i] * su + v[i] * sv + d[i] * R for i in range(3)]
                if loc.IntersectWithLine(p1, p2, 1e-6, t, x, pc, sub, cid, hc):
                    vur[sid.GetValue(int(cid))] += 1
                sv += adim
            su += adim
    return vur


# ---------------------------------------------------------------- KURULUM (STEP → kanonik + sade) ----------------------------------------------------------------
def _imza(kod, yol):
    k = KATALOG[kod]
    return dict(surum=SURUM, dosya=k["dosya"], boyut=os.path.getsize(yol) if yol else None, sha1=_sha1(yol) if yol else None,
                eksen=list(k["eksen"]), ray_on=k["ray_on"], ray_h=k["ray_h"], sade=k.get("sade", "gorunur"), gorunur=GORUNUR)


def _kur(kod, yol, imza):
    k = KATALOG[kod]; t0 = time.time()
    w = cq.importers.importStep(yol)
    ham = [v for v in w.vals() if isinstance(v, cq.Shape)]
    ham = ham[0] if len(ham) == 1 else cq.Compound.makeCompound(ham)
    katilar0 = ham.Solids()
    M = _matris(k["eksen"])
    # ray oluğu kanonik eksende: Y_ray = s_y × ray_h · Z_ray = s_z × ray_on
    iy = "xyz".index(k["eksen"][1][1]); iz = "xyz".index(k["eksen"][2][1])
    y_ray = M[1][iy] * k["ray_h"]; z_ray = M[2][iz] * k["ray_on"]
    from OCP.gp import gp_Trsf
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
    tr = gp_Trsf(); tr.SetValues(M[0][0], M[0][1], M[0][2], 0.0, M[1][0], M[1][1], M[1][2], 0.0, M[2][0], M[2][1], M[2][2], 0.0)
    # OCP tuzağı (topping_cad din_parca): çok katılı Compound'u tek hamlede dönüştürmek geçersiz Compound verebiliyor → katı katı
    don = [cq.Shape.cast(BRepBuilderAPI_Transform(s.wrapped, tr, True).Shape()) for s in katilar0]
    b = _obb(cq.Compound.makeCompound(don))
    T = cq.Vector(-b[0], -y_ray, -z_ray)
    kan = [s.translate(T) for s in don]
    tam = cq.Compound.makeCompound(kan); bt = _obb(tam)
    # görünürlük ayıklaması
    vur = _gorunurluk(kan); kip = k.get("sade", "gorunur")
    oran = [vur[i] * GORUNUR["adim"] ** 2 / max(s.Area(), 1e-9) for i, s in enumerate(kan)]
    kal, at, zorunlu = [], [], []
    for i, s in enumerate(kan):
        sb = _obb(s); sinir = any(abs(sb[j] - bt[j]) < 0.02 for j in range(6))       # dış ölçüyü tanımlayan katı her durumda kalır
        gor = vur[i] >= GORUNUR["esik"] and (kip != "kabuk" or oran[i] >= GORUNUR["kabuk_oran"])
        (kal if (gor or sinir) else at).append(i)
        if sinir and not gor: zorunlu.append(i)
    sade = cq.Compound.makeCompound([_temizle(kan[i].copy()) for i in kal]); bs = _obb(sade)
    assert all(abs(bs[j] - bt[j]) < 0.02 for j in range(6)), ("sadeleştirme dış ölçüyü değiştirdi", kod, bt, bs)
    assert sade.isValid() or all(kan[i].isValid() for i in kal), ("geçersiz katı", kod)
    # ray (dolu TS35 kutusu) bindirmesi = tırnak / kilit dili hacmi (bilgi) · arka çıkıntı (rayın arkası) plakaya ulaşmamalı
    W = bt[3] - bt[0]
    ray = cq.Solid.makeBox(W + 2.0, 35.0, RAY_DERINLIK, cq.Vector(-1.0, -17.5, 0.0))
    try: bind = sade.intersect(ray).Volume()
    except Exception: bind = -1.0
    arka = bt[5]
    assert arka < RAY_DERINLIK - 0.3, ("cihaz arkası montaj plakasına değiyor", kod, arka)
    _temizle(sade)
    os.makedirs(ONB, exist_ok=True)
    yb = os.path.join(ONB, "%s_%s.brep.gz" % (kod, SURUM))
    buf = io.BytesIO(); sade.exportBrep(buf)
    with open(yb, "wb") as f: f.write(gzip.compress(buf.getvalue(), 6))                    # ASCII BREP + gzip (~%20 boyut · baglam_engel_v1.brep.gz gibi)
    s = dict(imza=imza, kod=kod, ad=k["ad"], uretici=k["uretici"], kaynak=k["kaynak"], dosya=k["dosya"], olcum=k["olcum"],
             olcu=[round(bt[3] - bt[0], 2), round(bt[4] - bt[1], 2), round(bt[5] - bt[2], 2)],
             kanonik_kutu=[round(v, 3) for v in bt],
             ray=dict(alt=round(-bt[1], 2), ust=round(bt[4], 2), on=round(-bt[2], 2), arka=round(bt[5], 2), bindirme_mm3=round(bind, 1)),
             sayim=dict(kati=[len(katilar0), len(kal)], yuz=[len(ham.Faces()), len(sade.Faces())],
                        ucgen_hazir=_ucgen(ham, temiz=False), ucgen=[_ucgen(tam), _ucgen(sade)],
                        step_mb=round(os.path.getsize(yol) / 1048576.0, 2), brep_mb=round(os.path.getsize(yb) / 1048576.0, 2)),
             sade=kip, zorunlu=zorunlu,
             kalan=[dict(i=i, vurus=vur[i], oran=round(oran[i], 2), yuz=len(kan[i].Faces()), kutu=[round(v, 1) for v in _obb(kan[i])]) for i in kal],
             atilan=[dict(i=i, vurus=vur[i], oran=round(oran[i], 2), yuz=len(kan[i].Faces()), kutu=[round(v, 1) for v in _obb(kan[i])]) for i in at],
             sure_sn=round(time.time() - t0, 1), tarih=time.strftime("%Y-%m-%d %H:%M"))
    io.open(os.path.join(ONB, "%s_%s.json" % (kod, SURUM)), "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, indent=1))
    return sade, s


def _yukle(kod, yeniden=False):
    if kod in _BELLEK and not yeniden: return _BELLEK[kod]
    assert kod in KATALOG, ("katalogda yok", kod, KODLAR)
    yb = os.path.join(ONB, "%s_%s.brep.gz" % (kod, SURUM)); yj = os.path.join(ONB, "%s_%s.json" % (kod, SURUM))
    yol = _step_yolu(KATALOG[kod]["dosya"])
    meta = json.load(io.open(yj, encoding="utf-8")) if os.path.isfile(yj) else None
    gecerli = meta is not None and os.path.isfile(yb) and not yeniden
    if gecerli:
        im = meta["imza"]; k = KATALOG[kod]
        tablo_ayni = (im["surum"] == SURUM and im["dosya"] == k["dosya"] and im["eksen"] == list(k["eksen"]) and im["ray_on"] == k["ray_on"]
                      and im["ray_h"] == k["ray_h"] and im.get("sade") == k.get("sade", "gorunur") and im["gorunur"] == json.loads(json.dumps(GORUNUR)))
        if yol: gecerli = tablo_ayni and im["boyut"] == os.path.getsize(yol) and im["sha1"] == _sha1(yol)
        else:
            assert tablo_ayni, ("%s: tablo değişti ama STEP bulunamadı (%s) → önbellek yeniden kurulamıyor" % (kod, KATALOG[kod]["dosya"]))
    if gecerli:
        with open(yb, "rb") as f: sh = cq.Shape.importBrep(io.BytesIO(gzip.decompress(f.read())))
    else:
        assert yol, ("%s: STEP bulunamadı (%s) ve önbellek yok · arama: %s" % (kod, KATALOG[kod]["dosya"], [a for a in ARAMA if a]))
        sh, meta = _kur(kod, yol, _imza(kod, yol))
    _BELLEK[kod] = (sh, meta)
    return sh, meta


# ---------------------------------------------------------------- DIŞ ARAYÜZ ----------------------------------------------------------------
def olcu(kod):
    """gerçek dış ölçü (w ray boyu, h düşey, d derinlik) mm · tırnak / kilit dili / klemens dahil"""
    return tuple(_yukle(kod)[1]["olcu"])


def bilgi(kod):
    """önbellek meta: ölçü · ray ofsetleri (alt / üst: ray merkezinin altı / üstü · on: ray önünden cihaz önüne · arka: ray önünün arkasına) · sayımlar"""
    return _yukle(kod)[1]


def cihaz_step(kod, x0, y_ray, z_plaka, yon=-1, ray_derinlik=RAY_DERINLIK, z_ray_on=None):
    """üretici STEP'inden cihaz (cq.Compound, dünya): sol kenar x0 · ray oluğu ortası y_ray · oluk tabanı ray önünde
    (z_plaka + yon × ray_derinlik; ya da doğrudan z_ray_on) · yon −1: önü −z · +1: önü +z"""
    sh, meta = _yukle(kod)
    zo = z_ray_on if z_ray_on is not None else z_plaka + yon * ray_derinlik
    if yon > 0:
        sh = sh.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 180.0)               # x → −x, z → −z (ray oluğu y / z = 0 yerinde kalır)
        dx = x0 + meta["olcu"][0]
    else:
        dx = x0
    return sh.moved(cq.Location(cq.Vector(dx, y_ray, zo)))


def _sayi(v, n=1):
    return ("%.*f" % (n, v)).rstrip("0").rstrip(".").replace(".", ",") if n else "%d" % round(v)


def bom_kaynak(kod):
    """BOM 3. sütunu: üretici STEP (dosya, kaynak URL) · gerçek ölçü"""
    m = bilgi(kod); w, h, d = m["olcu"]
    return "üretici STEP (%s, %s) · %s × %s × %s mm (genişlik × yükseklik × derinlik, tırnak / klemens dahil)" % (
        m["dosya"], m["kaynak"], _sayi(w, 2), _sayi(h, 2), _sayi(d, 2))


def rapor(kodlar=None):
    print("%-11s %-24s %7s %7s %7s | %6s %6s %6s %6s | %8s | %-9s %-11s %-13s %-11s | %s" % (
        "KOD", "dosya", "w", "h", "d", "alt", "ust", "on", "arka", "ray∩mm3", "kati", "yuz", "ucgen(0,6)", "MB stp→gz", "STEP hazır ağ"))
    for kod in (kodlar or KODLAR):
        m = bilgi(kod); s = m["sayim"]; r = m["ray"]
        print("%-11s %-24s %7.2f %7.2f %7.2f | %6.2f %6.2f %6.2f %6.2f | %8.1f | %3d→%-4d %5d→%-5d %6d→%-6d %5.2f→%-5.2f | %d" % (
            kod, m["dosya"], m["olcu"][0], m["olcu"][1], m["olcu"][2], r["alt"], r["ust"], r["on"], r["arka"], r["bindirme_mm3"],
            s["kati"][0], s["kati"][1], s["yuz"][0], s["yuz"][1], s["ucgen"][0], s["ucgen"][1], s["step_mb"], s["brep_mb"], s["ucgen_hazir"]))


if __name__ == "__main__":
    yen = "--yeniden" in sys.argv
    for kod in KODLAR:
        t0 = time.time(); _yukle(kod, yeniden=yen); print("%s hazır (%.1f sn)" % (kod, time.time() - t0)); sys.stdout.flush()
    rapor()
    sys.stdout.flush(); os._exit(0)
