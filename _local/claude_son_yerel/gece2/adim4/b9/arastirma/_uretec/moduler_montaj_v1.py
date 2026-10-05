# -*- coding: utf-8 -*-
"""AUTOKITCH · BAĞIMSIZ İSTASYONLAR → ANA MONTAJ v1 (29 Eyl 2026) · Kemal: "Codex'in modüler işini bizimkine ekle, yaptığın değişikliklerin üstüne".

Kaynak yöntem: Codex arastirma/_uretec/moduler_istasyon_v1/model.py (v69 üstüne ayrı model; yayında otonom/hat/moduler-v1). Burada aynı geometri kuralları
ANA MONTAJIN kendi üreteç parçalarına uygulanır (v71: bantlı tabla + fırın v10 korunur):
  · A açıcı: kendi 1,5 mm 304 sağ duvarı (ray/tabla geçiş ağzı + pnömatik rakor delikleri açık) + A–C sökülür EPDM çevre contası · A sağ çerçeve üyeleri −2 mm
  · B / K / E: süpürgelik içinde alt şase (B 60×80×3, K/E 40×60×3 kutu profil) + M12 ayak yuvaları · B içinde A/C yükünü taşıyan 30×40×2 kiriş + 30×30×2 dikme + 3 mm GFRP ısı kesici,
    köpük/saclarda gerçek oturma cepleri
  · B–K, K–E alt bağlama plakaları + M8 · A/C → B M8 bağlama (B kirişine kaynak somunu)
  · taşıma kızakları ve kiriş hesapları buraya ALINMAZ (kurulu makine)
Mevcut parçalar yerinde değiştirilir (p["wp"] güncellenir); yeni parçalar YENI listesinde döner (dünya koordinatı)."""
import cadquery as cq

V = cq.Vector


def box(x0, x1, y0, y1, z0, z1): return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))
def bb(s):
    b = s.BoundingBox(); return [b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax]
def overlap(a, b, t=.05): return all(min(a[2 * i + 1], b[2 * i + 1]) - max(a[2 * i], b[2 * i]) > t for i in range(3))
def cyl_y(x, z, r, y0, y1): return cq.Solid.makeCylinder(r, y1 - y0, V(x, y0, z), V(0, 1, 0))
def _tek(wp):
    v = [o for o in wp.vals() if isinstance(o, cq.Shape)]
    return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)


PARTS, YENI, DEGISEN = [], [], []


def add(name, mod, shape, mat="304", kind="frame", note=""):
    if isinstance(shape, cq.Workplane): shape = shape.val()
    p = dict(name=name, module=mod, shape=shape, material=mat, kind=kind, note=note, new=True, src=None, off=0.0)
    PARTS.append(p); YENI.append(p); return p


def rhs(name, mod, b, axis, t=3, note=""):
    inner = list(b)
    for i in range(3):
        inner[2 * i] += -1 if i == axis else t; inner[2 * i + 1] += 1 if i == axis else -t
    return add(name, mod, box(*b).cut(box(*inner)), note=note)


def _kaynak(M):
    """ana montajın B / K / E / A / kaide parçaları (dünya şekli + geri yazma bilgisi)"""
    def ekle(p, mod, off):
        s = _tek(p["wp"]).translate(V(off, 0, 0)) if off else _tek(p["wp"])
        mat, kind, name = p["mal"], "inside", p["ad"]
        if any(k in name for k in ("sac", "duvar", "yalitim", "pu_", "kapak", "govde", "profil", "kaide", "dikme", "kusak", "ayak", "onyuz")): kind = "shell"
        if mat in ("pu", "yalitim_gorunur"): mat, kind = "PU", "insulation"
        PARTS.append(dict(name=name, module=mod, shape=s, material=mat, kind=kind, note=p.get("birim", mod), new=False, src=p, off=off, s0=s))
    for p in M.SC.PARCALAR: ekle(p, "B", 0.0)
    for p in M.KS.PARCALAR: ekle(p, "K", M.X_K)
    for p in M.KC.PARCALAR:
        if p["ad"].startswith(("robot_catal_", "robot_flansi", "REF_")): continue
        ekle(p, "E", M.X_E)
    for p in M.AK.PARCALAR: ekle(p, "A", 0.0)
    for p in M.KD.PARCALAR: ekle(p, "A" if p["birim"] == "KAIDE_A" else "C", 0.0)


def _A(M):
    wall = box(698, 699.5, 893.5, 1860.5, -828.5, 59)
    throat = box(697, 701, 892.5, 1042.5, -510.5, 5.5)
    wall = wall.cut(throat)
    for y, z in M.TC.RAKOR_ACICI:
        wall = wall.cut(cq.Solid.makeCylinder(7, 4, V(697, y + M.Y_MEK, z), V(1, 0, 0)))
    for p in PARTS:
        if p["module"] != "A" or p["new"] or p["note"] not in ("A_GOVDE", "A_ONYUZ"): continue
        b = bb(p["shape"])
        if b[0] >= 650 and ("sag" in p["name"] or "lama" in p["name"]):
            p["shape"] = p["shape"].translate(V(-2, 0, 0))
        elif "kusak_arka" in p["name"] or "kayit_ust" in p["name"]:
            p["shape"] = p["shape"].intersect(box(-10, 668, 780, 1900, -850, 100))
    add("A_bagimsiz_sag_duvar_1p5", "A", wall, kind="shell", note="304 1,5 · A'nın kendi sağ duvarı · ray/tabla geçiş ağzı açık")
    seal = box(699.5, 700, 893.5, 1860.5, -828.5, 59).cut(box(699, 701, 903.5, 1850.5, -818.5, 49)).cut(throat)
    add("A_C_sokulur_cevre_contasi", "A", seal, "EPDM", "gasket", "0,5 mm oturmuş derz · sıkışma üretici föyüne göre")
    for p in PARTS:
        if p["new"] or p["module"] != "A" or p["note"] not in ("A_GOVDE", "A_ONYUZ", "KAIDE_A"): continue
        if overlap(bb(p["shape"]), bb(wall)):
            if abs(p["shape"].intersect(wall).Volume()) > .1: p["shape"] = p["shape"].cut(wall)


def _alt_sase(mod, feet):
    zs = sorted(set(round(z, 2) for x, z in feet)); half = 30 if mod == "B" else 20; y0 = 43 if mod == "B" else 63
    members = []
    for i, z in enumerate(zs):
        xs = [x for x, zz in feet if abs(z - zz) < .1]
        if len(xs) < 2: continue
        lo, hi = (1.5, 3998.5) if mod == "B" and z in (-110, -760) else (min(xs) - 20, max(xs) + 20)
        members.append(rhs(mod + "_alt_sasi_boyuna_" + str(i), mod, (lo, hi, y0, 123, z - half, z + half), 0, note=("60×80×3" if mod == "B" else "40×60×3") + " kutu profil"))
    for i, x in enumerate(sorted(set(round(x, 2) for x, z in feet))):
        local = [z for xx, z in feet if abs(x - xx) < .1]
        if len(local) < 2: continue
        extra = mod == "E" and len([xx for xx, zz in feet if zz == min(local)]) == 1
        r = rhs(mod + "_alt_sasi_enine_" + str(i), mod, (x - half, x + half, y0, 123, min(local) + (-half if extra else half), max(local) + (half if extra else -half)), 2, note="kutu profil · boyunaya kaynaklı")
        for other in members:
            if overlap(bb(r["shape"]), bb(other["shape"])): r["shape"] = r["shape"].cut(box(*bb(other["shape"])))
        solids = r["shape"].Solids(); r["shape"] = solids[0]; seg = [r]
        for k, s_ in enumerate(solids[1:]): seg.append(add(r["name"] + "_parca_" + str(k + 1), mod, s_, note="ayrı profil parçası"))
        members.extend(seg)
    for x, z in feet:
        bore = cyl_y(x, z, 6.5, y0 - 1, 124)
        for p in members:
            if overlap(bb(p["shape"]), bb(bore)): p["shape"] = p["shape"].cut(bore)
        add(mod + "_M12_ayak_yuvasi_%g_%g" % (x, z), mod, box(x - 12, x + 12, 108, 120, z - 12, z + 12).cut(cyl_y(x, z, 6.5, 107, 121)), note="M12 kaynak somunu")


def _B_yuk():
    xs = [17, 700, 1355, 2010]
    for i, z in enumerate((-110, -747)):
        rhs("B_AC_ust_kiris_" + str(i), "B", (2, 2502.5, 743.5, 783.5, z - 15, z + 15), 0, 2, note="30×40×2 · A/C yükünü bölme dikmelerine")
        add("B_AC_ust_isikesici_" + str(i), "B", box(2, 2502.5, 783.5, 786.5, z - 15, z + 15), "GFRP", "thermal", "3 mm GFRP ısı kesici")
        for j, x in enumerate(xs):
            rhs("B_AC_dikme_%d_%d" % (i, j), "B", (x - 15, x + 15, 127.5, 743.5, z - 15, z + 15), 1, 2, note="30×30×2 · bölme / duvar içinde")
            add("B_AC_alt_isikesici_%d_%d" % (i, j), "B", box(x - 15, x + 15, 124.5, 127.5, z - 15, z + 15), "GFRP", "thermal", "3 mm GFRP")
            add("B_AC_alt_pabucluk_%d_%d" % (i, j), "B", box(max(1.5, x - 15), x + 15, 123, 124.5, z - 15, z + 15), note="taşıma pabucu")
    ins = [p for p in PARTS if p["new"] and p["module"] == "B" and p["name"].startswith("B_AC_")]
    for p in PARTS:
        if p["new"] or p["module"] != "B": continue
        if p["material"] != "PU" and not any(k in p["name"] for k in ("bolme_", "taban_", "tavan_", "yan_ic_sac")): continue
        b = bb(p["shape"])
        for q in ins:
            if overlap(b, bb(q["shape"])): p["shape"] = p["shape"].cut(q["shape"])


def _baglanti():
    for label, mod, xs in [("B_K", "K", (3970, 4050)), ("K_E", "E", (4550, 4660))]:
        plate = box(xs[0] - 15, xs[1] + 15, 59, 63, -125, -95)
        if label == "B_K": plate = box(xs[0] - 15, 4000, 39, 43, -125, -95).fuse(box(3996, 4000, 43, 63, -125, -95)).fuse(box(4000, xs[1] + 15, 59, 63, -125, -95))
        for x in xs:
            y = 39 if label == "B_K" and x == xs[0] else 59
            bore = cyl_y(x, -110, 4.5, y - 1, y + 17); plate = plate.cut(bore)
            for p in PARTS:
                if p["new"] and "alt_sasi" in p["name"] and overlap(bb(p["shape"]), bb(bore)): p["shape"] = p["shape"].cut(bore)
            add("M8_baglanti_civata_" + label + "_" + str(x), mod, cyl_y(x, -110, 4, y, y + 16).fuse(cyl_y(x, -110, 6.5, y - 5, y)), kind="connection")
            add("M8_baglanti_somun_" + label + "_" + str(x), mod, box(x - 6.5, x + 6.5, y + 7, y + 14, -116.5, -103.5).cut(cyl_y(x, -110, 4.2, y + 6, y + 15)), kind="connection")
        add("montaj_baglanti_" + label, mod, plate, kind="connection", note="304 4 mm bağlama plakası · M8")
    for mod, xs in [("A", (28, 672)), ("C", (728, 2472))]:
        for x in xs:
            z = -110; bore = cyl_y(x, z, 4.5, 770, 793)
            for p in PARTS:
                if p["module"] in (mod, "B") and p["kind"] != "inside" and overlap(bb(p["shape"]), bb(bore)): p["shape"] = p["shape"].cut(bore)
            add(mod + "_B_M8_civata_" + str(x), mod, cyl_y(x, z, 4, 771, 792).fuse(cyl_y(x, z, 6.5, 792, 797)), kind="connection")
            add(mod + "_B_M8_rondela_" + str(x), mod, cyl_y(x, z, 9, 790, 792).cut(cyl_y(x, z, 4.5, 789, 793)), kind="connection")
            add(mod + "_B_M8_disli_yuva_" + str(x), "B", box(x - 6.5, x + 6.5, 774.5, 781.5, z - 6.5, z + 6.5).cut(cyl_y(x, z, 4.2, 774, 782)), kind="connection")


def _kaplama_payi():
    st = [p for p in PARTS if p["new"] and p["kind"] == "frame"]
    for p in PARTS:
        if p["new"] or p["module"] not in ("B", "K", "E"): continue
        if not p["name"].startswith(("onyuz_plint", "taban_", "tavan_", "bolme_", "yan_pu")): continue
        b = bb(p["shape"])
        for q in st:
            if q["module"] == p["module"] and overlap(b, bb(q["shape"])):
                if abs(p["shape"].intersect(q["shape"]).Volume()) > .1: p["shape"] = p["shape"].cut(q["shape"])


def uygula(M):
    """M: ana montaj modül ad alanı (SC, KS, KC, AK, KD, TC, X_K, X_E, Y_MEK). Mevcut parçaları yerinde değiştirir, YENI döner."""
    PARTS[:] = []; YENI[:] = []; DEGISEN[:] = []
    _kaynak(M)
    _A(M)
    for mod in ("B", "K", "E"):
        feet = []
        for p in PARTS:
            if p["module"] == mod and not p["new"] and p["name"].startswith("ayak_"):
                b = bb(p["shape"]); feet.append(((b[0] + b[1]) / 2, (b[4] + b[5]) / 2))
        _alt_sase(mod, feet)
    _B_yuk(); _baglanti(); _kaplama_payi()
    for p in PARTS:                                                     # geri yaz: değişen mevcut parçalar
        if p["new"] or p["shape"] is p["s0"]: continue
        sh = p["shape"].translate(V(-p["off"], 0, 0)) if p["off"] else p["shape"]
        p["src"]["wp"] = cq.Workplane(obj=sh)
        DEGISEN.append(p["module"] + ":" + p["name"])
    return YENI
