# -*- coding: utf-8 -*-
"""AUTOKITCH · BANTLI TABLA → ANA MONTAJ köprüsü v1 (29 Eyl 2026)

bantli_tabla_cad_v1.py'nin parça üreten bölümleri (YARDIMCILAR · ÖLÇÜLER · 1 KASET · 2 BANT/KAYIŞ YOLLARI · 3 DÖNER ek pimler ·
4 SABİT TAHRİK · 5 YÜKLEME BANDI) AYNEN çalıştırılır (tek kaynak — ölçü burada tekrar yazılmaz). Bağlam / denetim / GLB bölümleri çalışmaz.
Ana montaj için yapılan tek şey:
  · sim sayfasında yalnız görüntü ağı olan üç sonsuz bant (kaset bandı, GT2 kayış, yükleme bandı) GERÇEK KATI yapılır (aynı hatve yolu ± t/2)
  · yükleme bandı köprü ayakları fırın gövdesinin iç tabanına (y 788 + 1,5) indirilir (bant CAD'inde 800'de, 10,5 mm havadaydı)
Koordinat: KASET / ROTOR / DONER yerel (x, z tabla eksenine göre; y dünya) · TAHRIK / YB dünya.
"""
import io, math, os, sys
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, U)
_kay = io.open(os.path.join(U, "bantli_tabla_cad_v1.py"), encoding="utf-8").read()
_bas = _kay.index("# ================================================================ YARDIMCILAR")
_son = _kay.index("# ================================================================ 6 · FIRIN VEKİLİ")
_ust = _kay[:_kay.index('"""', _kay.index('"""') + 3) + 3]
_g = {"__file__": os.path.join(U, "bantli_tabla_cad_v1.py"), "__name__": "bantli_tabla_cad_v1_parcalar"}
_bag = _kay[_kay.index("import csv"):_bas]                                   # importlar + yollar (dosya yazmaz)
exec(compile(_bag + _kay[_bas:_son], "bantli_tabla_cad_v1.py[1-5]", "exec"), _g)

H = _g["H"]
PARCALAR = _g["PARCALAR"]                   # dict(ad, grup, sh, mal, bom, kaynak)
BOM_EK = _g["BOM_EK"]
ZE, UST, AKT, LB_SOL = H.ZE, H.UST, H.AKT, H.LB_SOL
t_b, W_B = _g["t_b"], _g["W_B"]


def _serit_kati(yol, z0, z1, t, adim=1.0, bosluk=0.05):
    """hatve yolu (x, y, nx, ny, s) ± t/2 → z0..z1 boyunca kapalı halka katı (sonsuz bant / kayış) · iç yüz rulo/yatak yüzeyinden `bosluk` açık
    (çokgen kiriş sehimi rulo içine girmesin: r 6 rulo, 1 mm adım → sehim 0,02 mm)"""
    ps, son = [], None
    for (x, y, nx, ny, s) in yol:
        if son is None or s - son >= adim:
            ps.append((x, y, nx, ny)); son = s
    if math.hypot(ps[0][0] - ps[-1][0], ps[0][1] - ps[-1][1]) < 0.3:
        ps.pop()
    dis = [cq.Vector(x + nx * t / 2.0, y + ny * t / 2.0, z0) for x, y, nx, ny in ps]
    ic = [cq.Vector(x - nx * (t / 2.0 - bosluk), y - ny * (t / 2.0 - bosluk), z0) for x, y, nx, ny in ps]

    def alan(v):
        return 0.5 * sum(v[i].x * v[(i + 1) % len(v)].y - v[(i + 1) % len(v)].x * v[i].y for i in range(len(v)))
    if abs(alan(ic)) > abs(alan(dis)):
        dis, ic = ic, dis
    w_d = cq.Wire.makePolygon(dis + [dis[0]]); w_i = cq.Wire.makePolygon(ic + [ic[0]])
    f = cq.Face.makeFromWires(w_d, [w_i])
    sol = cq.Solid.extrudeLinear(f, cq.Vector(0, 0, z1 - z0))
    assert sol.isValid() and sol.Volume() > 0, "şerit katısı geçersiz"
    return sol


# ---- SABİT TAHRİK iç düzeltmesi (bant CAD'i tahriki yalnız çevreye karşı denetlemişti; kendi içinde 4 çakışma vardı) ----
#  · motor STEP'i kutu merkezine göre hizalanmıştı → konnektör çıkıntısı (y −31) yüzünden mil ekseni 1,49 mm kaçık · şimdi STEP orijini (mil ekseni) = tahrik ekseni
#  · motor 11 mm yüksekteydi (mil ucu −399, kaplinin tepesinden taşıp tahrik miline biniyordu) · STEP ölçüldü: flanş üstü +10,98 · pilot Ø38,1 üstü +12,51 · mil ucu +31,56
#    → pilot üstü −427,6 (motor kutusunun içinde) · mil ucu −408,55 · kaplin −418…−400 (motor mili 9,45 + boşluk 0,5 + tahrik mili 8,05 girer; yatak burcu −400'de başlar)
#  · motor kutusu y alt kenarı 957 → 954 (konnektör çıkıntısına 1,5 mm)
_KM = dict(H.KUTU_MOTOR); _KM["y"] = (954.0, _KM["y"][1])
Z_PILOT = -427.6
_kut, _silz = _g["kut"], _g["silz"]
_XS, _YS = _g["X_SUR"], _g["Y_SUR"]
for p in PARCALAR:
    if p["ad"] == "motor_kutusu":
        km = _kut(_KM["x"][0], _KM["x"][1], _KM["y"][0], _KM["y"][1], _KM["z"][0], _KM["z"][1]).cut(
            _kut(_KM["x"][0] + 1.5, _KM["x"][1] - 1.5, _KM["y"][0] + 1.5, _KM["y"][1] - 1.5, _KM["z"][0] + 1.5, _KM["z"][1] + 1))
        p["sh"] = km.val()
        p["bom"] = ("Motor kutusu 62 × 65 × 88", 1, "AISI 304 1,5 · arka kapak O-ring + 4 × M4 · kablo rakoru M16 IP68 (Lapp SKINTOP INOX)", "tahrik kutusuna TIG kaynaklı · konnektör çıkıntısına 1,5")
    elif p["ad"] == "tahrik_motoru":
        _m = cq.importers.importStep(_g["MOTOR_STEP"]).val()
        _bb = _m.BoundingBox()
        _m = cq.Workplane(obj=_m).intersect(_kut(-31.0, 31.0, -31.0, 31.0, _bb.zmin - 1.0, _bb.zmax + 1.0)).val()
        p["sh"] = _m.translate(cq.Vector(_XS, _YS, Z_PILOT - 12.507))
    elif p["ad"] == "kaplin":
        p["sh"] = _silz(_XS, _YS, 9.5, -418.0, -400.0).cut(_silz(_XS, _YS, 3.2, -419.0, -399.0)).val()
    elif p["ad"] == "tahrik_mili":
        _bb = p["sh"].BoundingBox()
        p["sh"] = _silz(_XS, _YS, 3.0, Z_PILOT + 19.05 + 0.5, _bb.zmax).val()

# ---- sonsuz bantlar gerçek katı ----
KASET_BANDI = _serit_kati(_g["yol_b"], -W_B / 2.0, W_B / 2.0, t_b)                                   # yerel (tabla ekseni)
GT2_KAYIS = _serit_kati(_g["yol_g"], _g["ZK0"] + 0.5, _g["ZK1"] - 0.5, 1.38)             # yerel
YB_BANDI = _serit_kati(_g["yol_y"], ZE - W_B / 2.0, ZE + W_B / 2.0, _g["t_yb"])                     # dünya

# ---- yükleme bandı ayakları gövde iç tabanına (788 + 1,5) ----
Y_GOVDE_IC = 788.0 + 1.5
for p in PARCALAR:
    if p["grup"] == "YB" and p["ad"].startswith("yb_ayak_"):
        bb = p["sh"].BoundingBox()
        xb = (bb.xmin + bb.xmax) / 2.0
        ZF = (ZE - W_B / 2.0 - 12.0, ZE + W_B / 2.0 + 12.0)
        p["sh"] = _g["kut"](xb - 10.0, xb + 10.0, Y_GOVDE_IC, 962.0, ZF[0] - 5.0, ZF[1] + 5.0).cut(
            _g["kut"](xb - 11.0, xb + 11.0, Y_GOVDE_IC + 5.0, 957.0, ZF[0], ZF[1])).val()


def grup(g):
    return [p for p in PARCALAR if p["grup"] == g]


# kaset (elle çıkar) = KASET + ROTOR + 2 bant katısı · DONER = ayar bileziğine / lokmaya ekler (TOPPING v27 kendi çizer → burada kullanılmaz)
KASET = grup("KASET") + grup("ROTOR") + [dict(ad="kaset_bandi", grup="BANT", sh=KASET_BANDI, mal="bant", bom=BOM_EK[0], kaynak="Forbo Transilon E 3/1 U0/U2 MT"),
                                          dict(ad="gt2_kayis", grup="GT2", sh=GT2_KAYIS, mal="koyu", bom=BOM_EK[1], kaynak="Gates 140-2GT-6")]
TAHRIK = grup("TAHRIK") + grup("TAHRIK_DISK")
YB = grup("YB") + [dict(ad="yukleme_bandi", grup="YB_BANT", sh=YB_BANDI, mal="ptfe_bant", bom=BOM_EK[2], kaynak="ZARF [V]")]
# yükleme bandı ölçüleri (fırın v9 ve montaj ürün yolu için)
YB_BURUN = (_g["X_YBN"], _g["Y_YBN"], 6.0)        # x · y · r
YB_TAHRIK = (_g["X_YBT"], _g["Y_YBT"], _g["R_YBT"])
YB_SON = _g["X_YBT"] + _g["R_YBT"] + _g["t_yb"]   # bandın sağ ucu (dünya x)
KASET_KG = None


if __name__ == "__main__":
    print("kaset %d parça · tahrik %d · yükleme bandı %d · YB %.1f → %.1f" % (len(KASET), len(TAHRIK), len(YB), YB_BURUN[0] - 6.0, YB_SON))
    for p in KASET + TAHRIK + YB:
        assert p["sh"].isValid(), p["ad"]
    print("hepsi geçerli · kaset bandı %.0f mm³ · GT2 %.0f · YB %.0f" % (KASET_BANDI.Volume(), GT2_KAYIS.Volume(), YB_BANDI.Volume()))
