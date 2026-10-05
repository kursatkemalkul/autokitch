# -*- coding: utf-8 -*-
"""h3_sac_v1 — AUTOKITCH ÜRETİME YÖNELİK SAC METAL KÜTÜPHANESİ v1 (2 Eki 2026 · Claude · YEREL · yalnız kütüphane, montaja bağlı DEĞİL)

NE YAPAR
  İstasyon gövdelerini (dış / iç panel, taban, tavan, kapak, iskelet sacı) GERÇEK ABKANT BÜKÜMLÜ SAC olarak kurar: her büküm iç yarıçapı R,
  dış yarıçapı R + t olan silindirik bölgedir; flanş boyları K faktörlü büküm payıyla açınımla birebir tutarlıdır. Lazer + abkant + TIG yapan
  atölye 3B'den açınım (JSON: dış kontur + delikler + büküm çizgileri, açı, yön, R, K, BA) alır.

KOORDİNAT
  Dünya: mm · x hat boyunca · y yukarı · z koridora (ön). Her panelin yerel çerçevesi: (u, v) sac düzleminde, z sac kalınlığı yönünde (+n).
  Yerel z = 0 'alt yüz', z = t 'üst yüz'. Bükümle yüz değişmez → AÇINIMDA BÜTÜN PANELLERİN ÜST YÜZÜ Z = t TARAFINDADIR.
  Büküm yönü: yon = +1 → çocuk flanş ebeveynin +n (üst yüz) tarafına döner (açınımda 'yukari'), yon = −1 → −n ('asagi').
  Panel poligonu CCW verilir; i. kenar = poly[i] → poly[i+1]; kenarın dış normali kenar yönünün sağıdır. Büküm teğet çizgisi = panel kenarı.
  flans() ile doğan panelin poligonu (s, w): s büküm bitişinden flanş boyunca, w ebeveyn kenarı boyunca (kenar başından).
    Kenar adları: 0 = 'bas' yanı (w küçük), 1 = 'uc' (serbest uç — dönüş / kıvırma buraya), 2 = 'son' yanı, 3 = bükümlü kenar (kullanılamaz).

SABİTLER (öncelik): sac_kararlar_v1.json  >  sac_standart_v1.json  >  varsayılan (304 · R = t · K 0,40 · min flanş 6t · relief t × (R+t) ...)
  Klasör: <scratchpad>/sac_standart (ya da AUTOKITCH_SAC_STANDART ortam değişkeni). STD nesnesi · standart_yukle() yeniden okur.
  K: standart büküm tablosundan (BD ölçümle doğrulanmış) · tabloda yoksa kararlar.K · yoksa 0,40.

API ÖZETİ
  Sac(ad, rol='dis'|'ic'|'yuk'|'kapak_dis'|'kapak_ic'|'braket', t=None, R=None, K=None, birim, grup, bolge='gida_disi'|'gida')
    .taban(poligon, O, ex, ey, ad)                          → Panel (kök)
    .kose(flansA, flansB, tip='acik'|'bindirme', ustte=None, rahat='kare'|'yuvarlak'|None, kaynak=None, bosluk=None)
    .punta(diger_sac, noktalar, cap)                        → punta etiketi (meta)
    .kati() / .kati_temel()                                 → cq.Shape (formlu / formsuz)
    .acinim()                                               → dict (JSON) — dış kontur, iç konturlar, bükümler, formlar, delikler
    .dogrula()                                              → açınımdan yeniden büküm + kalınlık + kesit yarıçap denetimi
    .dfm(abkant=True)                                       → üretilebilirlik maddeleri (HATA / UYARI / GEÇTİ / BİLGİ)
    .parca() / .parcalar() / .meta()                        → montaj parça sözlüğü (ad, wp, sh, mal, birim, grup, kaynak, bom, sac)
  Panel
    .flans(kenar, boy, aci=90, yon=+1, R=None, olcu='dis'|'ic'|'duz', bas=0, son=0, uzat_bas=0, uzat_son=0, rahat='otomatik', ad=None)
    .kivir(kenar, boy=None, tip='kapali'|'acik', yon=+1, bas=0, son=0)        (hem: 180°, R = iç çap / 2)
    .ofset(kenar, yukseklik, boy, aci=90, yon=+1)                              (joggle: iki ters büküm)
    .delik(u, v, cap) · .oblong(u, v, boy, en, aci) · .dikdortgen(u, v, boy, en, aci, r) · .kesik(poligon)
    .lazer_yarik_dizisi(u0, v0, n_sira, n_sutun, aci=0)     (standart: 5 × 60, R2,5, köprü ≥ 5, sıra ≥ 10)
    .dil(kenar, w0, en, boy)                                 (geçme dili) · .panjur(...) · .kabartma(...)
    .dunya(u, v, z) · .yerel(p) · .normal() · .kenar(i) · .icerir(u, v)
  Birleşim:  vidali_birlesim(A, B, nokta, tip='pem_somun'|'pem_saplama'|'percin_somun'|'somun'|'kor_percin', dis='M5', ...)
             saplama_baglantisi(A, nokta, yon, paket, dis='M5')   (sac + sac-dışı parça: menteşe plakası, braket)
             dil_yuva(dil_paneli, kenar, w0, en, yuva_paneli, bosluk=0.1)
  Bağlantı elemanı (gerçek ölçülü, BOM satırlı): pem_somun · pem_saplama · percin_somun · vida (ISO 7380 / DIN 7991 / ISO 4762) ·
             somun (ISO 4032 / ISO 10511 / DIN 1587) · pul (DIN 125 / DIN 9021) · kor_percin (ISO 15983) · ayarli_ayak · kor_burc ·
             kaynak_somunu (DIN 929) · gizli_mentese · piyano_mentese · kaynak_dikisi · kaynak_halka
  Çıktı:     glb_yaz(yol, parcalar) · parca_kutusu_satiri(p) · cakisma_denetle(parcalar)

SINIRLAR (v1): köşe kapama / köşe rahatlatma yalnız 90° dışbükey köşe + iki 90° aynı yönlü flanş · flanş yanları dik (konik flanş yok) ·
  büküm bölgesine taşan EĞRİ kesik 3B'de 0,1 mm basamakla yaklaşılır (açınım tam) · panjur / kabartma şekil (form) olarak modellenir,
  açınımda takım işareti (yeniden büküm ve kalınlık denetimi dışı) · abkant çarpışması düz bıçak + V kalıp + koç bloğuyla basit 3B denetim."""
import math, os, re, sys, json, time, struct
import numpy as np
import cadquery as cq
from OCP.gp import gp_Pnt, gp_Pnt2d, gp_Dir, gp_Vec, gp_Lin, gp_Pln, gp_Trsf
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.BRepClass import BRepClass_FaceClassifier
from OCP.TopAbs import TopAbs_IN, TopAbs_REVERSED
from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.BRepTools import BRepTools_WireExplorer
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.BRepLProp import BRepLProp_SLProps
from OCP.TopExp import TopExp
from OCP.BRep import BRep_Tool

V = cq.Vector
SURUM = "h3_sac_v1"
YOGUNLUK = 7.93e-6                      # kg/mm³ · AISI 304
EPS = 1e-7


# =====================================================================================================================================
# 1 · STANDART (kararlar > standart > varsayılan)
# =====================================================================================================================================
_BURADA = os.path.dirname(os.path.abspath(__file__))
_STD_KLASOR = os.environ.get("AUTOKITCH_SAC_STANDART") or os.path.abspath(os.path.join(_BURADA, "..", "..", "..", "..", "sac_standart"))


def _ifade(x, t):
    """'6t' · 't' · 't/4' · 3.5 → sayı (t yerine konur)"""
    if x is None: return None
    if isinstance(x, (int, float)): return float(x)
    s = str(x).strip().replace(",", ".").replace(" ", "")
    if not re.fullmatch(r"[0-9t\.\*/\+\-\(\)]+", s): return None
    s = re.sub(r"(\d)t", r"\1*t", s)
    try:
        return float(eval(s, {"__builtins__": {}}, {"t": t}))
    except Exception:
        return None


class Standart:
    """sac_kararlar_v1.json > sac_standart_v1.json > varsayılan. Her okunan değer kaynağıyla .kullanilan'a yazılır."""
    ROL = {"dis": (("kabuk_dis_t",), ("kalinlik", "ana_sac"), 1.2), "ic": (("ic_panel_t",), ("kalinlik", "ana_sac"), 1.0),
           "yuk": (("raf_tabla_t",), ("kalinlik", "yuk_saci"), 1.5), "kapak_dis": (("kapak_dis_t",), ("kapak", "dis_tava_t"), 1.2),
           "kapak_ic": (("kapak_ic_tava_t",), ("kapak", "ic_tava_t"), 1.0), "braket": (("braket_t",), ("kalinlik", "braket"), 3.0)}
    ROL_ES = {"taban": "yuk", "raf": "yuk", "tabla": "yuk", "kabuk": "dis", "tava_ic": "kapak_ic"}

    def __init__(self, klasor=None):
        self.klasor = klasor or _STD_KLASOR
        self.std, self.kar, self.dosyalar, self.kullanilan = {}, {}, [], {}
        for ad, hedef in (("sac_standart_v1.json", "std"), ("sac_kararlar_v1.json", "kar")):
            yol = os.path.join(self.klasor, ad)
            if os.path.exists(yol):
                with open(yol, encoding="utf-8") as f:
                    setattr(self, hedef, json.load(f))
                self.dosyalar.append(yol)

    def _yaz(self, ad, deger, kaynak):
        self.kullanilan[ad] = (deger, kaynak)
        return deger

    @staticmethod
    def _g(d, *yol):
        for k in yol:
            if not isinstance(d, dict) or k not in d: return None
            d = d[k]
        return d

    def _satir(self, t):
        tab = self.std.get("bukum") or {}
        if not tab: return None, None
        k, v = min(tab.items(), key=lambda kv: abs(float(kv[0]) - t))
        return (v, "standart.bukum[%s]" % k) if abs(float(k) - t) < 0.011 else (None, None)

    def t(self, rol):
        rol = self.ROL_ES.get(rol, rol)
        kk, sk, vv = self.ROL[rol]
        v = self._g(self.kar, *kk)
        if v is not None: return self._yaz("t_" + rol, float(v), "kararlar." + ".".join(kk))
        v = self._g(self.std, *sk)
        if v is not None: return self._yaz("t_" + rol, float(v), "standart." + ".".join(sk))
        return self._yaz("t_" + rol, vv, "varsayilan")

    def R(self, t):
        c = self._g(self.kar, "ic_radyus_carpan")
        if c is not None: return self._yaz("R(%g)" % t, round(float(c) * t, 4), "kararlar.ic_radyus_carpan")
        s, k = self._satir(t)
        if s and s.get("R_ic_model") is not None: return self._yaz("R(%g)" % t, float(s["R_ic_model"]), k)
        return self._yaz("R(%g)" % t, 1.0 * t, "varsayilan R = t")

    def K(self, t):
        s, k = self._satir(t)
        if s and s.get("K") is not None: return self._yaz("K(%g)" % t, float(s["K"]), k + " (BD tablosu)")
        v = self._g(self.kar, "K")
        if v is not None: return self._yaz("K(%g)" % t, float(v), "kararlar.K")
        return self._yaz("K(%g)" % t, 0.40, "varsayilan")

    def V(self, t):
        s, k = self._satir(t)
        if s and s.get("V_kalip"): return float(s["V_kalip"])
        return float(max(4, 2 * round(4 * t)))

    def min_flans(self, t):
        """(mutlak, tasarim) dış ölçü"""
        s, k = self._satir(t)
        if s and s.get("min_flans_mutlak") is not None:
            return self._yaz("min_flans(%g)" % t, (float(s["min_flans_mutlak"]), float(s["min_flans_tasarim"])), k)
        return self._yaz("min_flans(%g)" % t, (4.0 * t, 6.0 * t), "varsayilan 4t / 6t")

    def relief(self, t):
        """(genişlik, derinlik) — derinlik büküm teğet çizgisinden ebeveyne doğru"""
        s, k = self._satir(t)
        if s and s.get("relief_genislik") is not None:
            return self._yaz("relief(%g)" % t, (float(s["relief_genislik"]), float(s["relief_derinlik"])), k)
        return self._yaz("relief(%g)" % t, (t, self.R(t) + t), "varsayilan t × (R + t)")

    def mesafe(self, ad, t):
        """delik_flans · yarik_flans · panjur_flans (flanş İÇ yüzünden) · delik_kenar · delik_kopru · min_delik"""
        R = self.R(t)
        anahtar = {"delik_flans": "delik_flans_ic_yuz", "yarik_flans": "uzun_yarik_flans_ic_yuz", "panjur_flans": "panjur_flans_ic_yuz",
                   "delik_kenar": "delik_sac_kenari", "delik_kopru": "delik_kopru", "min_delik": "min_delik_cap"}[ad]
        s, k = self._satir(t)
        if s and s.get(anahtar) is not None: return self._yaz("%s(%g)" % (ad, t), float(s[anahtar]), k)
        vv = {"delik_flans": 2 * t + R, "yarik_flans": 4 * t + R, "panjur_flans": 3 * t + 2 * R, "delik_kenar": 2 * t, "delik_kopru": 2 * t,
              "min_delik": t}[ad]
        return self._yaz("%s(%g)" % (ad, t), vv, "varsayilan")

    def kose_bosluk(self, kaynakli=True):
        if kaynakli:
            a = self._g(self.std, "kose", "flans_ucu_araligi_kaynakli")
            if a: return self._yaz("kose_bosluk_kaynakli", round(sum(a) / len(a), 3), "standart.kose.flans_ucu_araligi_kaynakli (orta)")
            return self._yaz("kose_bosluk_kaynakli", 0.2, "varsayilan")
        a = self._g(self.std, "kose", "kaynaksiz_flans_bosluk_min")
        return self._yaz("kose_bosluk_kaynaksiz", float(a) if a is not None else 0.4, "standart.kose" if a is not None else "varsayilan")

    def kose_deligi(self, t):
        a = self._g(self.std, "kose", "gizli")
        m = re.search(r"O\s*=\s*([0-9.]*)t", a or "")
        c = float(m.group(1) or 1.0) if m else 2.0
        return self._yaz("kose_deligi(%g)" % t, c * t, "standart.kose.gizli" if m else "varsayilan 2t")

    def hem(self, t, tip="kapali"):
        """(R_ic, min_donus)"""
        d = self._g(self.std, "kenar", tip + "_hem")
        if d:
            ic = _ifade(d.get("ic_cap"), t); dn = _ifade(d.get("donus"), t)
            return self._yaz("hem_%s(%g)" % (tip, t), (ic / 2.0, dn), "standart.kenar.%s_hem" % tip)
        return self._yaz("hem_%s(%g)" % (tip, t), (0.5 * t, (6.0 if tip == "kapali" else 4.0) * t), "varsayilan")

    def derz(self):
        v = self._g(self.std, "kapak", "derz")
        return self._yaz("derz", float(v) if v is not None else 2.0, "standart.kapak.derz" if v is not None else "varsayilan")

    def montaj_boslugu(self):
        v = self._g(self.std, "kapak", "ic_dis_bosluk")
        return self._yaz("montaj_boslugu", float(v) if v is not None else 0.5, "standart.kapak.ic_dis_bosluk" if v is not None else "varsayilan")

    def max_acinim(self):
        v = self._g(self.std, "malzeme", "max_acinim")
        return self._yaz("max_acinim", tuple(sorted(float(x) for x in v)) if v else (1500.0, 3000.0), "standart.malzeme" if v else "varsayilan")

    def abkant_boy(self):
        v = self._g(self.std, "malzeme", "abkant_max_boy")
        return float(v) if v else 3100.0

    def pem_yasak(self):
        v = self._g(self.std, "baglanti", "sac_gizli_secenek_A_PEM", "yasak")
        return v if v else ["PEM CLS (HRB 70 sınırı, 304 sacta tutmaz)"]

    def pem_delik(self, tur, dis):
        """standarttan PEM delik çapı (SP somun / FHP saplama) ya da None"""
        A = self._g(self.std, "baglanti", "sac_gizli_secenek_A_PEM") or {}
        D = self._g(self.std, "baglanti", "pem_diger") or {}
        if tur == "SP":
            if (A.get("somun") or {}).get("dis") == dis: return A["somun"].get("delik"), A["somun"].get("kenar_eksen_min")
            r = D.get("SP-%s-1" % dis) or {}
            return r.get("delik"), r.get("kenar_eksen_min")
        if tur in ("FHP", "FH4", "FHS", "FH"):
            if (A.get("saplama") or {}).get("dis") == dis: return A["saplama"].get("delik"), A["saplama"].get("kenar_eksen_min")
            r = D.get("FHP-%s" % dis) or {}
            return r.get("delik"), r.get("kenar_eksen_min")
        return None, None

    def percin_somun(self, dis):
        v = self._g(self.std, "baglanti", "percin_somun", dis)
        return v or {}

    def delik_iso273(self, dis, seri="orta"):
        v = self._g(self.std, "baglanti", "delik_iso273_" + seri, dis)
        if v is not None: return float(v)
        return {"M3": 3.4, "M4": 4.5, "M5": 5.5, "M6": 6.6, "M8": 9.0, "M10": 11.0, "M12": 13.5}[dis]

    def gida_R_min(self):
        v = self._g(self.std, "kose", "urun_bolgesi_ic_R_min")
        return float(v) if v is not None else 3.0

    def lazer_yarik(self):
        v = self._g(self.std, "havalandirma", "lazer_yarik") or {}
        return dict(genislik=float(v.get("genislik", 5)), boy=float(v.get("boy", 60)), uc_R=float(v.get("uc_R", 2.5)),
                    kopru=float(v.get("kopru_min", 5)), sira=float(v.get("sira_araligi_min", 10)), kenar=float(v.get("kenar_min", 10)))

    def panjur_hmax(self, t):
        v = self._g(self.std, "havalandirma", "panjur_taret", "H_max")
        return _ifade(v, t) if v is not None else 3 * t

    def kapak(self):
        k = self._g(self.std, "kapak") or {}
        return dict(dis_donus=float(k.get("dis_tava_donus", 20)), ic_donus=float(k.get("ic_tava_donus", 15)),
                    ic_dis_bosluk=float(k.get("ic_dis_bosluk", 0.5)), kulp_cep=k.get("kulp", {}).get("cep_derinlik", [25, 30]) if isinstance(k.get("kulp"), dict) else [25, 30],
                    derz=self.derz())

    def ozet(self):
        return dict(dosyalar=self.dosyalar, kullanilan={k: dict(deger=v[0], kaynak=v[1]) for k, v in sorted(self.kullanilan.items())})


STD = Standart()


def standart_yukle(klasor=None):
    """sac_standart_v1.json + sac_kararlar_v1.json yeniden okunur (yeni Sac nesneleri yeni değerleri kullanır)"""
    global STD
    STD = Standart(klasor)
    return STD


# =====================================================================================================================================
# 2 · GEOMETRİ ARAÇLARI
# =====================================================================================================================================
def _n(v):
    v = np.asarray(v, float); L = float(np.linalg.norm(v))
    if L < 1e-12: raise ValueError("sıfır vektör")
    return v / L


def _rot(k, a):
    k = _n(k); K = np.array([[0.0, -k[2], k[1]], [k[2], 0.0, -k[0]], [-k[1], k[0], 0.0]])
    return np.eye(3) + math.sin(a) * K + (1.0 - math.cos(a)) * (K @ K)


def _M(Rm=None, o=(0.0, 0.0, 0.0)):
    M = np.eye(4)
    if Rm is not None: M[:3, :3] = Rm
    M[:3, 3] = np.asarray(o, float)
    return M


def _M_eksen(A, k, a):
    """A noktasından geçen k eksen doğrusu etrafında a (rad) dönüş"""
    Rm = _rot(k, a); A = np.asarray(A, float)
    return _M(Rm, A - Rm @ A)


def _M_ot(v):
    return _M(None, v)


def _cerceve(nokta, eksen, ref=None):
    """z = eksen · x = ref'in eksene dik bileşeni"""
    z = _n(eksen)
    r = np.asarray(ref, float) if ref is not None else (np.array([1.0, 0, 0]) if abs(z[0]) < 0.9 else np.array([0, 1.0, 0]))
    x = _n(r - np.dot(r, z) * z); y = np.cross(z, x)
    return _M(np.column_stack([x, y, z]), nokta)


def _tr(M):
    tr = gp_Trsf()
    tr.SetValues(*[float(M[i, j]) for i in range(3) for j in range(4)])
    return tr


def _tasi(sh, M):
    if sh is None: return None
    if np.allclose(M, np.eye(4), atol=1e-12): return sh
    return cq.Shape.cast(BRepBuilderAPI_Transform(sh.wrapped, _tr(M), True).Shape())


def _p(M, p):
    return (M @ np.r_[np.asarray(p, float), 1.0])[:3]


def _H_M(H):
    """2B rijit dönüşüm (3×3) → 4×4 (z korunur)"""
    M = np.eye(4); M[0, 0], M[0, 1], M[1, 0], M[1, 1] = H[0, 0], H[0, 1], H[1, 0], H[1, 1]; M[0, 3], M[1, 3] = H[0, 2], H[1, 2]
    return M


def _Hp(H, p):
    return (H @ np.array([p[0], p[1], 1.0]))[:2]


def _yuz_tasi(f, H):
    return _tasi(f, _H_M(H))


def _alan2(pts):
    return 0.5 * sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))


def _V2(x, y):
    return V(float(x), float(y), 0.0)


def yuz_poligon(pts):
    if _alan2(pts) < 0: pts = list(reversed(pts))
    return cq.Face.makeFromWires(cq.Wire.makePolygon([_V2(*p) for p in pts], close=True))


def yuz_daire(cx, cy, r):
    return cq.Face.makeFromWires(cq.Wire.makeCircle(float(r), _V2(cx, cy), V(0, 0, 1)))


def yuz_dikd(x0, x1, y0, y1):
    return yuz_poligon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def yuz_oblong(cx, cy, L, W, aci=0.0):
    """L uç uca toplam boy, W genişlik (uçlar tam yarım daire)"""
    if L <= W + 1e-9: return yuz_daire(cx, cy, W / 2.0)
    r = W / 2.0; a = math.radians(aci); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux; h = L / 2.0 - r
    p = lambda s, q: _V2(cx + ux * s + nx * q, cy + uy * s + ny * q)
    e = [cq.Edge.makeLine(p(-h, -r), p(h, -r)), cq.Edge.makeThreePointArc(p(h, -r), p(h + r, 0), p(h, r)),
         cq.Edge.makeLine(p(h, r), p(-h, r)), cq.Edge.makeThreePointArc(p(-h, r), p(-h - r, 0), p(-h, -r))]
    return cq.Face.makeFromWires(cq.Wire.assembleEdges(e))


def yuz_dikd_r(cx, cy, L, W, aci=0.0, r=0.0):
    """merkezli, döndürülmüş, köşesi r yuvarlatılmış dikdörtgen"""
    a = math.radians(aci); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    p = lambda s, q: _V2(cx + ux * s + nx * q, cy + uy * s + ny * q)
    hx, hy = L / 2.0, W / 2.0
    r = min(max(r, 0.0), hx - 1e-6, hy - 1e-6)
    if r <= 1e-6:
        return cq.Face.makeFromWires(cq.Wire.makePolygon([p(-hx, -hy), p(hx, -hy), p(hx, hy), p(-hx, hy)], close=True))
    c = r * (1 - math.sqrt(0.5))
    e = [cq.Edge.makeLine(p(-hx + r, -hy), p(hx - r, -hy)), cq.Edge.makeThreePointArc(p(hx - r, -hy), p(hx - c, -hy + c), p(hx, -hy + r)),
         cq.Edge.makeLine(p(hx, -hy + r), p(hx, hy - r)), cq.Edge.makeThreePointArc(p(hx, hy - r), p(hx - c, hy - c), p(hx - r, hy)),
         cq.Edge.makeLine(p(hx - r, hy), p(-hx + r, hy)), cq.Edge.makeThreePointArc(p(-hx + r, hy), p(-hx + c, hy - c), p(-hx, hy - r)),
         cq.Edge.makeLine(p(-hx, hy - r), p(-hx, -hy + r)), cq.Edge.makeThreePointArc(p(-hx, -hy + r), p(-hx + c, -hy + c), p(-hx + r, -hy))]
    return cq.Face.makeFromWires(cq.Wire.assembleEdges(e))


def _prizma(face, h):
    return cq.Shape.cast(BRepPrimAPI_MakePrism(face.wrapped, gp_Vec(0.0, 0.0, float(h))).Shape())


def _bb_kesisir(a, b, pay=1e-6):
    return a.xmin <= b.xmax + pay and b.xmin <= a.xmax + pay and a.ymin <= b.ymax + pay and b.ymin <= a.ymax + pay and a.zmin <= b.zmax + pay and b.zmin <= a.zmax + pay


def _birlestir(ss, temizle=True):
    ss = [s for s in ss if s is not None]
    if not ss: return None
    s = ss[0] if len(ss) == 1 else ss[0].fuse(*ss[1:])
    return s.clean() if temizle else s


def _alan(sh):
    return 0.0 if sh is None else sum(f.Area() for f in sh.Faces())


def _icinde(face, p, tol=1e-7):
    for f in (face.Faces() if face is not None else []):
        if BRepClass_FaceClassifier(f.wrapped, gp_Pnt(float(p[0]), float(p[1]), float(p[2]) if len(p) > 2 else 0.0), tol).State() == TopAbs_IN:
            return True
    return False


def _ic_nokta(face):
    """düzlemsel yüzün içinde bir nokta"""
    for f in face.Faces():
        c = f.Center()
        if _icinde(f, (c.x, c.y, c.z)): return (c.x, c.y, c.z)
        bb = f.BoundingBox()
        for i in range(1, 12):
            for j in range(1, 12):
                q = (bb.xmin + bb.xlen * i / 12.0, bb.ymin + bb.ylen * j / 12.0, c.z)
                if _icinde(f, q): return q
    return None


def _sektor(A0, k, rho, e3, w0, w1, r0, r1, phi0, dphi):
    """A0'dan geçen k ekseni etrafında, başlangıçta rho yönündeki r0–r1 / w0–w1 dikdörtgeninin phi0 → phi0 + dphi taranmasıyla
    oluşan halka dilimi (gerçek silindirik büküm bölgesi)"""
    A0, k, rho, e3 = (np.asarray(x, float) for x in (A0, k, rho, e3))
    r0 = max(r0, 1e-3)
    Q = lambda w, r: V(*(A0 + e3 * w + rho * r))
    tel = cq.Wire.makePolygon([Q(w0, r0), Q(w1, r0), Q(w1, r1), Q(w0, r1)], close=True)
    s = cq.Solid.revolve(tel, [], math.degrees(dphi), V(*A0), V(*(A0 + k)))
    if abs(phi0) > 1e-12: s = s.rotate(V(*A0), V(*(A0 + k)), math.degrees(phi0))
    return s


def _dikd_ayir(yuz_sw, BA, dw=0.1):
    """(s, w) düzlemindeki şerit parçasını eksene paralel dikdörtgenlere ayırır → [(s0, s1, w0, w1)].
    Dikdörtgen kenarlı parça TAM ayrılır; eğik / eğri kenar varsa w'de dw adımlı basamak (yaklaşık)."""
    out = []
    if yuz_sw is None: return out
    for f in yuz_sw.Faces():
        bb = f.BoundingBox(); A = f.Area()
        if A < 1e-9: continue
        if abs(A - bb.xlen * bb.ylen) <= 1e-7 * max(1.0, bb.xlen * bb.ylen):
            out.append((max(0.0, bb.xmin), min(BA, bb.xmax), bb.ymin, bb.ymax)); continue
        ws = {round(bb.ymin, 9), round(bb.ymax, 9)}
        for e in f.Edges():
            eb = e.BoundingBox()
            ws.update([round(eb.ymin, 9), round(eb.ymax, 9)])
            duz = e.geomType() == "LINE" and (eb.xlen < 1e-7 or eb.ylen < 1e-7)
            if not duz:
                n = max(1, int(math.ceil(eb.ylen / dw)))
                ws.update(round(eb.ymin + eb.ylen * i / n, 9) for i in range(n + 1))
        ws = sorted(ws)
        for w0, w1 in zip(ws[:-1], ws[1:]):
            if w1 - w0 < 1e-7: continue
            satir = f.intersect(yuz_dikd(-1.0, BA + 1.0, w0, w1))
            for g in satir.Faces():
                gb = g.BoundingBox()
                if g.Area() > 1e-10: out.append((max(0.0, gb.xmin), min(BA, gb.xmax), w0, w1))
    return out


# =====================================================================================================================================
# 3 · SAC PARÇA MODELİ
# =====================================================================================================================================
class Kesik:
    """panel yerel (u, v) koordinatında kesik; açınım anlamında: hedef None ise dokunduğu her bölgeyi keser"""
    def __init__(self, sahip, yuz, tip, meta=None, dfm=True, hedef=None):
        self.sahip, self.yuz, self.tip, self.meta, self.dfm, self.hedef = sahip, yuz, tip, dict(meta or {}), dfm, hedef


class Bukum:
    def __init__(self, **k):
        self.__dict__.update(k)

    def ozet(self):
        return dict(no=self.no, ad=self.cocuk.ad, ebeveyn=self.ebeveyn.ad, kenar=self.kenar, aci=round(self.aci, 4),
                    yon="yukari" if self.yon > 0 else "asagi", R=round(self.R, 4), K=round(self.K, 4), BA=round(self.BA, 4),
                    boy=round(self.b - self.a, 3), duz_flans=round(self.Lf, 3), olcu=self.olcu, olcu_deger=self.boy, tip=self.tip)


class Panel:
    def __init__(self, sac, no, ad, poly, M, D, ebeveyn=None, bukum=None):
        self.sac, self.no, self.ad = sac, no, ad
        self.poly = [(float(p[0]), float(p[1])) for p in poly]
        self.M, self.D = M, D
        self.ebeveyn, self.bukum = ebeveyn, bukum
        self.cocuklar, self.dil_kenar = {}, {}
        self.kesikler, self.ekler, self.formlar = [], [], []

    def __repr__(self):
        return "<Panel %s/%s>" % (self.sac.ad, self.ad)

    # ---------------- geometri
    def kenar(self, i):
        n = len(self.poly); p0 = np.array(self.poly[i % n]); p1 = np.array(self.poly[(i + 1) % n])
        L = float(np.linalg.norm(p1 - p0)); e2 = (p1 - p0) / L; out2 = np.array([e2[1], -e2[0]])
        return dict(p0=p0, p1=p1, L=L, e2=e2, out2=out2)

    def dunya(self, u, v, z=0.0):
        return _p(self.M, (u, v, z))

    def yerel(self, p):
        return _p(np.linalg.inv(self.M), p)

    def normal(self):
        return self.M[:3, 2].copy()

    def icerir(self, u, v):
        x, y, ic = u, v, False; P = self.poly
        for i in range(len(P)):
            (x0, y0), (x1, y1) = P[i], P[(i + 1) % len(P)]
            if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0: ic = not ic
        return ic

    # ---------------- bükümler
    def flans(self, kenar, boy, aci=90.0, yon=+1, R=None, olcu="dis", bas=0.0, son=0.0, uzat_bas=0.0, uzat_son=0.0, rahat="otomatik", ad=None, K=None, tip="flans"):
        return self.sac._bukum_ekle(self, kenar, boy, aci, yon, R, olcu, bas, son, uzat_bas, uzat_son, rahat, ad, K, tip)

    def kivir(self, kenar, boy=None, tip="kapali", yon=+1, bas=0.0, son=0.0, uzat_bas=0.0, uzat_son=0.0, rahat="otomatik", ad=None):
        """kenar kıvırma (hem) · 180° · iç yarıçap standarttan (iç çap = t) · boy = dönüşün düz boyu"""
        R, dmin = STD.hem(self.sac.t, tip)
        return self.flans(kenar, boy if boy is not None else dmin, 180.0, yon, R=R, olcu="duz", bas=bas, son=son, uzat_bas=uzat_bas,
                          uzat_son=uzat_son, rahat=rahat, ad=ad or "%s.kivirma%d" % (self.ad, kenar), tip="kivirma_" + tip)

    def ofset(self, kenar, yukseklik, boy, aci=90.0, yon=+1, bas=0.0, son=0.0, ad=None):
        """joggle: aci ile çık, yukseklik (alt yüzden alt yüze dik kaçıklık) kadar yüksel, ters aci ile dön, boy kadar devam et"""
        t, R, K = self.sac.t, self.sac.R, self.sac.K
        th = math.radians(aci)
        # 1. bükümün çocuğunun s = 0'daki alt yüz noktası ve 2. bükümün alt yüz kaçıklığı (sıfır ağ boyuyla) — ebeveyn yerelinde
        kn = self.kenar(kenar); p0 = np.r_[kn["p0"], 0.0]; e3 = np.r_[kn["e2"], 0.0]; o3 = np.r_[kn["out2"], 0.0]; nz = np.array([0, 0, 1.0])
        A0, k = (p0 + nz * (t + R), -e3) if yon > 0 else (p0 - nz * R, e3)
        Rk = _rot(k, th); org = A0 + Rk @ (p0 - A0); ex = Rk @ o3; nn = Rk @ nz
        A1, k1 = (org - nn * R, e3) if yon > 0 else (org + nn * (t + R), -e3)      # 2. büküm ters yön (−yon)
        Rk1 = _rot(k1, th); org2 = A1 + Rk1 @ (org - A1)
        c0 = float(np.dot(org2 - p0, nz)) * (1 if yon > 0 else -1)
        web = (yukseklik - c0) / math.sin(th)
        if web < -1e-9: raise ValueError("ofset: yükseklik %.2f < en küçük %.2f (iki büküm bitişik)" % (yukseklik, c0))
        web = max(web, 0.0)
        g = self.flans(kenar, web if web > 1e-6 else 1e-3, aci, yon, olcu="duz", bas=bas, son=son, ad=(ad or "%s.ofset%d" % (self.ad, kenar)) + "_ag", tip="ofset")
        return g.flans(1, boy, aci, -yon, olcu="duz", ad=(ad or "%s.ofset%d" % (self.ad, kenar)), tip="ofset")

    # ---------------- kesikler (panel yerel u, v)
    def _kesik(self, yuz, tip, meta=None, dfm=True, hedef=None):
        k = Kesik(self, yuz, tip, meta, dfm, hedef); self.kesikler.append(k); self.sac._gecersiz(); return k

    def delik(self, u, v, cap, tip="delik", **meta):
        return self._kesik(yuz_daire(u, v, cap / 2.0), tip, dict(meta, sekil="daire", merkez=[u, v], cap=cap))

    def oblong(self, u, v, boy, en, aci=0.0, tip="yarik", **meta):
        return self._kesik(yuz_oblong(u, v, boy, en, aci), tip, dict(meta, sekil="oblong", merkez=[u, v], boy=boy, en=en, aci=aci))

    def dikdortgen(self, u, v, boy, en, aci=0.0, r=0.0, tip="kesik", dfm=True, **meta):
        """dfm=False: kenara açılan bilinçli çentik (delik–büküm kuralı dışı)"""
        return self._kesik(yuz_dikd_r(u, v, boy, en, aci, r), tip, dict(meta, sekil="dikdortgen", merkez=[u, v], boy=boy, en=en, aci=aci, r=r), dfm=dfm)

    def kesik(self, pts, tip="kesik", dfm=True, **meta):
        return self._kesik(yuz_poligon(pts), tip, dict(meta, sekil="poligon"), dfm=dfm)

    def lazer_yarik_dizisi(self, u0, v0, n_sira, n_sutun, aci=0.0, boy=None, en=None, kopru=None, sira=None):
        """standart havalandırma yarığı: boy × en (uçlar tam R) · aynı sırada köprü, sıralar arası 'sira' (kenardan kenara) · (u0, v0) dizinin merkezi"""
        L = STD.lazer_yarik()
        boy, en, kopru, sira = boy or L["boy"], en or L["genislik"], kopru or L["kopru"], sira or L["sira"]
        a = math.radians(aci); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
        out = []
        for i in range(n_sira):
            for j in range(n_sutun):
                s = (j - (n_sutun - 1) / 2.0) * (boy + kopru); q = (i - (n_sira - 1) / 2.0) * (en + sira)
                out.append(self.oblong(u0 + ux * s + nx * q, v0 + uy * s + ny * q, boy, en, aci, tip="havalandirma_yarigi"))
        return out

    def dil(self, kenar, w0, en, boy):
        """geçme dili: kenarın w0 … w0 + en aralığından dışarı boy kadar (açınımda panel konturuna eklenir)"""
        if kenar in self.cocuklar: raise ValueError("dil: kenar %d bükümlü" % kenar)
        kn = self.kenar(kenar); p = lambda w, s: tuple(kn["p0"] + kn["e2"] * w + kn["out2"] * s)
        yz = yuz_poligon([p(w0, 0.0), p(w0 + en, 0.0), p(w0 + en, boy), p(w0, boy)])
        d = dict(tip="dil", yuz=yz, kenar=kenar, w0=w0, en=en, boy=boy)
        self.ekler.append(d); self.dil_kenar.setdefault(kenar, []).append(d); self.sac._gecersiz()
        return d

    # ---------------- şekiller (form) — 3B'de modellenir, açınımda takım işareti
    def panjur(self, u, v, boy, en, h=None, aci=0.0, yon=+1, agiz=-1):
        """taret panjuru: boy (yarık boyu) × en (yükselen bölge), h ≤ 3t · agiz: açık tarafın en yönündeki işareti"""
        h = STD.panjur_hmax(self.sac.t) if h is None else h
        d = dict(tip="panjur", u=u, v=v, boy=boy, en=en, h=h, aci=aci, yon=yon, agiz=agiz)
        self.formlar.append(d); self.sac._gecersiz(); return d

    def kabartma(self, u, v, boy, en, h, r=0.0, egim=20.0, yon=+1):
        """dikdörtgen kabartma (takviye / kabartı): taban boy × en, yükseklik h, yan eğim (dikeyden) egim°"""
        d = dict(tip="kabartma", u=u, v=v, boy=boy, en=en, h=h, r=r, egim=egim, yon=yon)
        self.formlar.append(d); self.sac._gecersiz(); return d

    # ---------------- iç
    def _ham_yuz(self):
        f = yuz_poligon(self.poly)
        if self.ekler: f = _birlestir([f] + [e["yuz"] for e in self.ekler])
        return f


class Sac:
    def __init__(self, ad, rol="dis", t=None, R=None, K=None, malzeme=None, mal="paslanmaz", birim="SAC", grup="SABIT", kaynak=None, bolge="gida_disi", adet=1):
        self.ad, self.rol = ad, rol
        self.t = float(t) if t is not None else STD.t(rol)
        self.R = float(R) if R is not None else STD.R(self.t)
        self.K = float(K) if K is not None else STD.K(self.t)
        self.malzeme = malzeme or (STD._g(STD.kar, "malzeme") or "AISI 304 (1.4301)")
        self.mal, self.birim, self.grup, self.kaynak, self.bolge, self.adet = mal, birim, grup, kaynak or SURUM, bolge, adet
        self.paneller, self.bukumler, self.kaynaklar, self.puntalar, self.notlar = [], [], [], [], []
        self._c = {}

    def __repr__(self):
        return "<Sac %s t=%g R=%g K=%g · %d panel · %d büküm>" % (self.ad, self.t, self.R, self.K, len(self.paneller), len(self.bukumler))

    def _gecersiz(self):
        self._c.clear()

    def panel(self, ad):
        for p in self.paneller:
            if p.ad == ad: return p
        raise KeyError(ad)

    # ---------------- kuruluş
    def taban(self, poly, O=(0.0, 0.0, 0.0), ex=(1.0, 0.0, 0.0), ey=(0.0, 1.0, 0.0), ad="taban"):
        if self.paneller: raise ValueError("taban yalnız bir kez")
        if _alan2(poly) <= 0: raise ValueError("taban poligonu CCW olmalı (kenar numaraları buna göre)")
        ex = _n(ex); ey = np.asarray(ey, float); ey = _n(ey - np.dot(ey, ex) * ex); n = np.cross(ex, ey)
        P = Panel(self, 0, ad, poly, _M(np.column_stack([ex, ey, n]), O), np.eye(3))
        self.paneller.append(P); self._gecersiz()
        return P

    def _bukum_ekle(self, P, i, boy, aci, yon, R, olcu, bas, son, uz_a, uz_b, rahat, ad, K, tip):
        n = len(P.poly); i %= n
        if i in P.cocuklar or i in P.dil_kenar: raise ValueError("%s kenar %d dolu" % (P.ad, i))
        if P.bukum is not None and i == 3: raise ValueError("%s: kenar 3 bükümlü kenar" % P.ad)
        if not (0.0 < aci <= 180.0): raise ValueError("açı 0–180")
        if R is None: R = self.R
        # dış/iç ölçülü bir flanşın UCUNA yeni büküm gelirse ebeveyn flanşın dış ölçüsü korunur: düz boyu yeni bükümün geri çekmesi kadar kısalır
        if P.bukum is not None and i == 1 and P.bukum.olcu in ("dis", "ic"):
            thn = math.radians(aci)
            geri = (R + self.t) if aci >= 179.999 else math.tan(thn / 2.0) * ((R + self.t) if P.bukum.olcu == "dis" else R)
            Bp = P.bukum
            if Bp.Lf - geri <= 1e-6: raise ValueError("%s: dış ölçü %.2f iki bükümü taşımıyor" % (P.ad, Bp.boy))
            Bp.Lf -= geri; Bp.uc_geri = geri
            P.poly = [(min(p[0], Bp.Lf), p[1]) for p in P.poly]
        kn = P.kenar(i); L = kn["L"]; a, b = float(bas), L - float(son)
        if not (-1e-9 <= a < b <= L + 1e-9): raise ValueError("flanş aralığı geçersiz %.2f–%.2f / %.2f" % (a, b, L))
        t = self.t; R = float(R); K = self.K if K is None else float(K)
        th = math.radians(aci); BA = th * (R + K * t)
        if olcu == "duz": Lf = float(boy)
        elif olcu == "dis": Lf = float(boy) - math.tan(th / 2.0) * (R + t)
        elif olcu == "ic": Lf = float(boy) - math.tan(th / 2.0) * R
        else: raise ValueError("olcu: dis / ic / duz")
        if aci >= 179.999 and olcu != "duz": raise ValueError("180° için olcu='duz'")
        if Lf <= 1e-6: raise ValueError("%s: flanş boyu %.2f büküme yetmiyor (düz kısım %.3f)" % (ad or P.ad, boy, Lf))
        p0 = np.r_[kn["p0"], 0.0]; e3 = np.r_[kn["e2"], 0.0]; o3 = np.r_[kn["out2"], 0.0]; nz = np.array([0.0, 0.0, 1.0])
        if yon > 0: A0, k, rho = p0 + nz * (t + R), -e3, -nz
        else: A0, k, rho = p0 - nz * R, e3, nz
        Rk = _rot(k, th); org = A0 + Rk @ (p0 - A0)
        Lb = _M(np.column_stack([Rk @ o3, e3, Rk @ nz]), org)                                    # çocuk yereli → ebeveyn yereli (bükük)
        Ld = _M(np.column_stack([o3, e3, nz]), p0 + o3 * BA)                                     # çocuk yereli → ebeveyn yereli (düz)
        Hs = np.array([[o3[0], e3[0], p0[0]], [o3[1], e3[1], p0[1]], [0.0, 0.0, 1.0]])          # şerit (s, w) → ebeveyn 2B
        Hc = np.array([[o3[0], e3[0], p0[0] + BA * o3[0]], [o3[1], e3[1], p0[1] + BA * o3[1]], [0.0, 0.0, 1.0]])
        B = Bukum(no=len(self.bukumler), ebeveyn=P, kenar=i, a=a, b=b, aci=float(aci), th=th, yon=1 if yon > 0 else -1, R=R, K=K, BA=BA, Lf=Lf,
                  boy=float(boy), olcu=olcu, tip=tip, A0=A0, k=k, rho=rho, e3=e3, o3=o3, p0=p0, Lb=Lb, Ld=Ld, Hs=Hs, uz_a=float(uz_a), uz_b=float(uz_b))
        poly = [(0.0, a - uz_a), (Lf, a - uz_a), (Lf, b + uz_b), (0.0, b + uz_b)]
        C = Panel(self, len(self.paneller), ad or "%s.k%d" % (P.ad, i), poly, P.M @ Lb, P.D @ Hc, ebeveyn=P, bukum=B)
        B.cocuk = C
        P.cocuklar[i] = B; self.paneller.append(C); self.bukumler.append(B)
        if rahat == "otomatik": rahat = "dikdortgen"
        B.rahat = []
        if rahat in ("dikdortgen", "yuvarlak"):
            for uc, w in (("bas", a), ("son", b)):
                if (uc == "bas" and a > 1e-6) or (uc == "son" and b < L - 1e-6):
                    self._rahatlatma(B, uc, w, rahat)
        self._gecersiz()
        return C

    def _rahatlatma(self, B, uc, w, tip):
        P = B.ebeveyn; wr, d = STD.relief(self.t)
        kn = P.kenar(B.kenar); p = lambda ww, s: tuple(kn["p0"] + kn["e2"] * ww + kn["out2"] * s)
        w0, w1 = (w - wr, w) if uc == "bas" else (w, w + wr)
        if tip == "yuvarlak":
            yz = _birlestir([yuz_poligon([p(w0, -d + wr / 2.0), p(w1, -d + wr / 2.0), p(w1, 0.5), p(w0, 0.5)]),
                             yuz_daire(*p((w0 + w1) / 2.0, -d + wr / 2.0), wr / 2.0)])
        else:
            yz = yuz_poligon([p(w0, -d), p(w1, -d), p(w1, 0.5), p(w0, 0.5)])
        P._kesik(yz, "rahatlatma", dict(bukum=B.no, uc=uc, genislik=wr, derinlik=d, sekil=tip), dfm=False, hedef={("P", P.no)})
        B.rahat.append(dict(uc=uc, tip=tip, genislik=wr, derinlik=d))

    def kose(self, f1, f2, tip="acik", ustte=None, rahat="kare", kaynak=None, bosluk=None, rahat_boyut=None):
        """aynı panelin komşu iki kenarındaki 90° aynı yönlü flanşların köşesi.
        tip 'bindirme': ustte (f1/f2) diğerinin ucunu örter: e_üst = R + t − g, e_alt = R − g (g: kaynaklı köşe aralığı) · 'acik': uzatma yok.
        rahat 'kare': köşede c × c kesik (bükümler köşede c kısalır) · 'yuvarlak': köşe deliği Ø (standart 2t) · None.
        kaynak: köşe dikişi (bindirmede varsayılan True)."""
        B1, B2 = f1.bukum, f2.bukum; P = B1.ebeveyn
        if B2.ebeveyn is not P: raise ValueError("kose: iki flanş aynı panelde olmalı")
        n = len(P.poly)
        if (B1.kenar + 1) % n == B2.kenar: Ba, Bb = B1, B2
        elif (B2.kenar + 1) % n == B1.kenar: Ba, Bb = B2, B1
        else: raise ValueError("kose: kenarlar komşu değil")
        ka, kb = P.kenar(Ba.kenar), P.kenar(Bb.kenar)
        if abs(np.dot(ka["e2"], kb["e2"])) > 1e-6 or (ka["e2"][0] * kb["e2"][1] - ka["e2"][1] * kb["e2"][0]) <= 0:
            raise ValueError("kose: yalnız 90° dışbükey köşe")
        if Ba.b < ka["L"] - 1e-6 or Bb.a > 1e-6: raise ValueError("kose: flanşlar köşeye kadar uzanmalı (bas / son = 0)")
        if abs(Ba.aci - 90) > 1e-6 or abs(Bb.aci - 90) > 1e-6 or Ba.yon != Bb.yon or abs(Ba.R - Bb.R) > 1e-9:
            raise ValueError("kose: iki flanş 90°, aynı yön, aynı R olmalı")
        t, R = self.t, Ba.R
        if kaynak is None: kaynak = tip == "bindirme"
        g = bosluk if bosluk is not None else STD.kose_bosluk(kaynakli=bool(kaynak))
        if tip == "bindirme":
            for C in (Ba.cocuk, Bb.cocuk):
                if C.cocuklar: raise ValueError("kose: köşe kapamayı %s alt flanşlarından ÖNCE çağırın" % C.ad)
            ust = (ustte or f1).bukum
            e_ust, e_alt = R + t - g, R - g
            for Bx, uc in ((Ba, "son"), (Bb, "bas")):
                e = e_ust if Bx is ust else e_alt
                if uc == "son": Bx.uz_b = e
                else: Bx.uz_a = e
                C = Bx.cocuk; Lf = Bx.Lf
                C.poly = [(0.0, Bx.a - Bx.uz_a), (Lf, Bx.a - Bx.uz_a), (Lf, Bx.b + Bx.uz_b), (0.0, Bx.b + Bx.uz_b)]
        elif tip != "acik":
            raise ValueError("kose tip: acik / bindirme")
        Vtx = kb["p0"]; d1, d2 = -ka["e2"], kb["e2"]
        q = lambda al, be: tuple(Vtx + d1 * al + d2 * be)
        hedef = {("P", P.no), ("B", Ba.no), ("B", Bb.no)}
        if rahat == "kare":
            c = rahat_boyut if rahat_boyut is not None else max(t, STD.relief(t)[0])
            yz = yuz_poligon([q(-Bb.BA, -Ba.BA), q(c, -Ba.BA), q(c, c), q(-Bb.BA, c)])
            P._kesik(yz, "kose_rahatlatma", dict(sekil="kare", boyut=c, bukumler=[Ba.no, Bb.no]), dfm=False, hedef=hedef)
        elif rahat == "yuvarlak":
            c = rahat_boyut if rahat_boyut is not None else STD.kose_deligi(t)
            P._kesik(yuz_daire(Vtx[0], Vtx[1], c / 2.0), "kose_rahatlatma", dict(sekil="yuvarlak", cap=c, bukumler=[Ba.no, Bb.no]), dfm=False, hedef=hedef)
        elif rahat is not None:
            raise ValueError("rahat: kare / yuvarlak / None")
        kayit = dict(tip=tip, bukumler=[Ba.no, Bb.no], bosluk=g if tip == "bindirme" else None, rahat=rahat, kaynak=bool(kaynak),
                     ustte=(ustte or f1).ad if tip == "bindirme" else None)
        Ba.kose_son = kayit; Bb.kose_bas = kayit
        if kaynak: self.kaynaklar.append(dict(tip="kose", Ba=Ba, Bb=Bb, kayit=kayit))
        self._gecersiz()
        return kayit

    def punta(self, diger, noktalar, cap=5.0, not_=""):
        """punta (direnç nokta kaynağı) etiketi — katı yok, meta"""
        k = dict(tip="punta", parcalar=[self.ad, diger.ad if hasattr(diger, "ad") else str(diger)], cap=cap,
                 noktalar=[[round(float(c), 2) for c in p] for p in noktalar], adet=len(noktalar), not_=not_)
        self.puntalar.append(k)
        return k

    # ---------------- bölgeler (A ve B ortak): son 2B yüzler
    def _bolgeler(self):
        if "bolge" in self._c: return self._c["bolge"]
        kes = [k for P in self.paneller for k in P.kesikler]
        pan, ser = {}, {}
        for P in self.paneller:
            F = P._ham_yuz(); bb = F.BoundingBox(); Di = np.linalg.inv(P.D)
            for k in kes:
                if k.hedef is not None and ("P", P.no) not in k.hedef: continue
                cf = k.yuz if k.sahip is P else _yuz_tasi(k.yuz, Di @ k.sahip.D)
                if _bb_kesisir(cf.BoundingBox(), bb): F = F.cut(cf)
            pan[P.no] = F
        for B in self.bukumler:
            S = yuz_dikd(0.0, B.BA, B.a, B.b); bb = S.BoundingBox(); Si = np.linalg.inv(B.ebeveyn.D @ B.Hs)
            for k in kes:
                if k.hedef is not None and ("B", B.no) not in k.hedef: continue
                cf = _yuz_tasi(k.yuz, Si @ k.sahip.D)
                if _bb_kesisir(cf.BoundingBox(), bb): S = S.cut(cf)
            ser[B.no] = S
        self._c["bolge"] = (pan, ser)
        return pan, ser

    def _yerel_katilar(self):
        """panel prizmaları (panel yerelinde) + büküm dilimleri (ebeveyn yerelinde)"""
        if "yk" in self._c: return self._c["yk"]
        pan, ser = self._bolgeler(); t = self.t
        pk = {no: (_prizma(F, t) if _alan(F) > 1e-9 else None) for no, F in pan.items()}
        sk = {}
        for B in self.bukumler:
            sk[B.no] = [_sektor(B.A0, B.k, B.rho, B.e3, w0, w1, B.R, B.R + t, B.th * s0 / B.BA, B.th * (s1 - s0) / B.BA)
                        for s0, s1, w0, w1 in _dikd_ayir(ser[B.no], B.BA) if s1 - s0 > 1e-9]
        self._c["yk"] = (pk, sk)
        return pk, sk

    def _bolge_katilari(self):
        """dünyada her bölgenin ayrı katısı: [(etiket, katı)]"""
        pk, sk = self._yerel_katilar(); out = []
        for P in self.paneller:
            if pk[P.no] is not None: out.append((("P", P.no), _tasi(pk[P.no], P.M)))
        for B in self.bukumler:
            for s in sk[B.no]: out.append((("B", B.no), _tasi(s, B.ebeveyn.M)))
        return out

    def kati_temel(self):
        """3B katı (şekil/form özellikleri hariç) — açınım doğrulaması bununla yapılır"""
        if "temel" not in self._c:
            self._c["temel"] = _birlestir([s for _e, s in self._bolge_katilari()])
        return self._c["temel"]

    def kati(self):
        """3B katı (panjur / kabartma dahil)"""
        if "kati" in self._c: return self._c["kati"]
        sh = self.kati_temel()
        for P in self.paneller:
            for fm in P.formlar:
                ekle, cikar = _form_araclari(fm, self.t)
                if cikar is not None: sh = sh.cut(_tasi(cikar, P.M))
                if ekle is not None: sh = sh.fuse(_tasi(ekle, P.M))
                if fm["tip"] == "kabartma" and fm.get("_ic") is not None: pass
        sh = sh.clean()
        self._c["kati"] = sh
        return sh

    # ---------------- açınım (B)
    def _duz_yuz(self):
        if "duz" in self._c: return self._c["duz"]
        pan, ser = self._bolgeler()
        yz = [_yuz_tasi(F, P.D) for P in self.paneller for F in [pan[P.no]] if _alan(F) > 1e-9]
        yz += [_yuz_tasi(ser[B.no], B.ebeveyn.D @ B.Hs) for B in self.bukumler if _alan(ser[B.no]) > 1e-9]
        F = _birlestir(yz)
        self._c["duz"] = F
        return F

    def acinim(self):
        """AÇINIM (flat pattern) — JSON'a hazır sözlük. Koordinat: kök panelin yereli (Z = t üst yüz). DXF'e birebir aktarılabilir."""
        if "acinim" in self._c: return self._c["acinim"]
        F = self._duz_yuz(); yuzler = F.Faces()
        dis, ic = [], []
        for f in yuzler:
            dis.append(_tel_varliklari(f.outerWire(), f))
            for w in f.innerWires(): ic.append(_tel_varliklari(w, f))
        bk = []
        pan, ser = self._bolgeler()
        for B in self.bukumler:
            S = B.ebeveyn.D @ B.Hs
            T0 = [_Hp(S, (0.0, B.a)), _Hp(S, (0.0, B.b))]; T1 = [_Hp(S, (B.BA, B.a)), _Hp(S, (B.BA, B.b))]
            Cz = [_Hp(S, (B.BA / 2.0, B.a)), _Hp(S, (B.BA / 2.0, B.b))]
            ws = [g.BoundingBox() for g in ser[B.no].Faces()]
            gercek = [min(w.ymin for w in ws), max(w.ymax for w in ws)] if ws else [B.a, B.b]
            bk.append(dict(no=B.no + 1, ad=B.cocuk.ad, aci=round(B.aci, 4), yon="yukari" if B.yon > 0 else "asagi", R=round(B.R, 4), K=round(B.K, 4),
                           BA=round(B.BA, 5), tip=B.tip, t=self.t, V_kalip=STD.V(self.t),
                           cizgi=[[round(c, 5) for c in p] for p in Cz], baslangic=[[round(c, 5) for c in p] for p in T0],
                           bitis=[[round(c, 5) for c in p] for p in T1], nominal_boy=round(B.b - B.a, 4),
                           gercek_aralik=[round(gercek[0], 4), round(gercek[1], 4)], gercek_boy=round(gercek[1] - gercek[0], 4)))
        pts = [p for kontur in dis for e in kontur for p in _varlik_noktalari(e)]
        L, W, aci = _min_dikdortgen(pts)
        alan = _alan(F)
        sabit = _ic_nokta(_yuz_tasi(pan[0], self.paneller[0].D)) if _alan(pan[0]) > 1e-9 else None
        kes = []
        for P in self.paneller:
            for k in P.kesikler:
                c = k.meta.get("merkez")
                kes.append(dict(panel=P.ad, tip=k.tip, sekil=k.meta.get("sekil"), merkez_duz=[round(x, 4) for x in _Hp(P.D, c)] if c else None,
                                **{kk: vv for kk, vv in k.meta.items() if kk in ("cap", "boy", "en", "aci", "parca", "std", "uc", "genislik", "derinlik", "boyut")}))
        fm = []
        for P in self.paneller:
            for f in P.formlar:
                c = _Hp(P.D, (f["u"], f["v"])); a = math.degrees(math.atan2(P.D[1, 0], P.D[0, 0])) + f.get("aci", 0.0)
                fm.append(dict(panel=P.ad, tip=f["tip"], merkez=[round(c[0], 4), round(c[1], 4)], aci=round(a, 4), boy=f["boy"], en=f["en"], h=f["h"],
                               yon="yukari" if f["yon"] > 0 else "asagi", not_="taret/form takımı · lazer kesmez" if f["tip"] == "panjur" else "kabartma kalıbı"))
        a = dict(parca=self.ad, surum=SURUM, malzeme=self.malzeme, t=self.t, R=self.R, K=self.K, adet=self.adet,
                 birim="mm", ust_yuz="Z = t yüzü = kök panelin +n yüzü (bütün panellerin yerel z = t yüzü)",
                 dis_kontur=dis[0] if len(dis) == 1 else dis, ek_dis_konturlar=dis[1:] if len(dis) > 1 else [],
                 ic_konturlar=ic, bukumler=bk, formlar=fm, kesikler=kes, parca_sayisi=len(yuzler),
                 levha=dict(boy=round(float(max(L, W)), 3), en=round(float(min(L, W)), 3), aci=round(float(aci), 4), alan_mm2=round(alan, 2),
                            kutle_kg=round(alan * self.t * YOGUNLUK, 4)),
                 sabit_yuz=[round(sabit[0], 5), round(sabit[1], 5)] if sabit else None,
                 donusum_3b=[[round(float(x), 9) for x in r] for r in self.paneller[0].M])
        self._c["acinim"] = a
        return a

    # ---------------- doğrulama
    def dogrula(self, kesit=True):
        """açınımdan yeniden bükülen katı ↔ 3B · kalınlık · kesit yarıçapları"""
        if "dogrula" in self._c: return self._c["dogrula"]
        A = self.kati_temel(); vA = A.Volume(); acn = self.acinim()
        r = dict(parca=self.ad, V_3b=round(vA, 3), kati_sayisi=len(A.Solids()), gecerli=A.isValid())
        try:
            C, rap = acinimdan_kati(json.loads(json.dumps(acn)))
            vC = C.Volume(); r.update(V_acinimdan=round(vC, 3), hacim_farki_yuzde=round(100.0 * abs(vA - vC) / vA, 5), yeniden_bukum=rap)
            try:
                d = A.cut(C).Volume() + C.cut(A).Volume()
                r["simetrik_fark_yuzde"] = round(100.0 * d / vA, 5)
            except Exception as e:
                r["simetrik_fark_yuzde"] = None; r["simetrik_hata"] = str(e)[:120]
            r["acinim_gecti"] = r["hacim_farki_yuzde"] < 0.5 and (r.get("simetrik_fark_yuzde") is None or r["simetrik_fark_yuzde"] < 0.5)
        except Exception as e:
            r.update(acinim_gecti=False, yeniden_bukum_hatasi=repr(e)[:300])
        Vd = acn["levha"]["alan_mm2"] * self.t
        r["V_duz_alanxt"] = round(Vd, 3); r["duz_3b_fark_yuzde"] = round(100.0 * (Vd - vA) / vA, 5)
        bek = sum(B.th * self.t * self.t * (B.K - 0.5) * (B.b - B.a) for B in self.bukumler)     # nötr eksen (R + Kt) ↔ orta yüzey (R + t/2)
        r["duz_3b_beklenen_fark_yuzde"] = round(100.0 * bek / vA, 5)
        r["kalinlik"] = kalinlik_denetle(A, self.t)
        if kesit:
            ks = []
            for B in self.bukumler:
                pan, ser = self._bolgeler()
                fs = ser[B.no].Faces()
                if not fs: continue
                bb = max(fs, key=lambda f: f.Area()).BoundingBox(); wm = (bb.ymin + bb.ymax) / 2.0
                Pw = _p(B.ebeveyn.M, B.A0 + B.e3 * wm); kw = B.ebeveyn.M[:3, :3] @ B.e3
                yr = kesit_yaricaplari(A, Pw, kw, eksen=Pw, tol=1e-3)
                bek = sorted({round(B.R, 3), round(B.R + self.t, 3)}) if B.R > 1e-3 else [round(self.t, 3)]
                ks.append(dict(bukum=B.no + 1, bulunan=sorted(set(round(x, 3) for x in yr)), beklenen=bek,
                               gecti=all(any(abs(x - y) < 1e-3 for x in yr) for y in bek)))
            r["kesit"] = ks; r["kesit_gecti"] = all(k["gecti"] for k in ks)
        self._c["dogrula"] = r
        return r

    # ---------------- DFM
    def dfm(self, abkant=True):
        if ("dfm", abkant) in self._c: return self._c[("dfm", abkant)]
        out = dfm_denetle(self, abkant=abkant)
        self._c[("dfm", abkant)] = out
        return out

    # ---------------- montaj uyumu
    def meta(self, dfm_ozet=True):
        a = self.acinim()
        m = dict(tur="sac", surum=SURUM, malzeme=self.malzeme, rol=self.rol, t=self.t, R=self.R, K=self.K, adet=self.adet,
                 bukum_sayisi=len(self.bukumler), bukumler=[B.ozet() for B in self.bukumler],
                 acinim=dict(boy=a["levha"]["boy"], en=a["levha"]["en"], alan_mm2=a["levha"]["alan_mm2"], kutle_kg=a["levha"]["kutle_kg"],
                             delik=len(a["ic_konturlar"]), dosya="%s_acinim.json" % self.ad),
                 kose=[dict(B.kose_son, bukum=B.no + 1) for B in self.bukumler if hasattr(B, "kose_son")],
                 punta=sum(p["adet"] for p in self.puntalar), kaynak=len(self.kaynaklar))
        if dfm_ozet and ("dfm", True) in self._c:
            d = self._c[("dfm", True)]
            m["dfm"] = dict(hata=sum(1 for x in d if x["durum"] == "HATA"), uyari=sum(1 for x in d if x["durum"] == "UYARI"))
        return m

    def parca(self):
        sh = self.kati(); bb = sh.BoundingBox(); a = self.acinim()
        return dict(ad=self.ad, wp=cq.Workplane("XY").add(sh), sh=sh, mal=self.mal, birim=self.birim, grup=self.grup, kaynak=self.kaynak, tur="sac",
                    bom=("Sac %s · AISI 304 t %g · %d büküm (R %g, K %g) · açınım %.0f × %.0f" % (self.ad, self.t, len(self.bukumler), self.R, self.K,
                                                                                             a["levha"]["boy"], a["levha"]["en"]),
                         self.adet, "%.1f × %.1f × %.1f" % (bb.xlen, bb.ylen, bb.zlen),
                         "lazer + abkant%s · %.2f kg" % (" + TIG" if self.kaynaklar else "", a["levha"]["kutle_kg"]), "ÜRETİM"),
                    sac=self.meta())

    def parcalar(self):
        """sac + kaynak dikişleri (ayrı katılar, sac ile yüz teması)"""
        return [self.parca()] + kaynak_parcalari(self)


# =====================================================================================================================================
# 4 · FORM (panjur / kabartma) araçları — panel yerelinde
# =====================================================================================================================================
def _form_araclari(fm, t):
    """(eklenecek, çıkarılacak) katı — panel yerelinde"""
    a = math.radians(fm.get("aci", 0.0)); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    u0, v0, yon = fm["u"], fm["v"], fm["yon"]
    if fm["tip"] == "panjur":
        L, W, h, ag = fm["boy"], fm["en"], fm["h"], fm.get("agiz", -1)
        # yerel (s: boy yönü, q: en yönü, z): kapalı taraf q = −ag·W/2, açık taraf q = +ag·W/2
        def P(s, q, z):
            qq = q * ag
            return (u0 + ux * s + nx * qq, v0 + uy * s + ny * qq, z if yon > 0 else t - z)
        def kati(pts6):                       # alt 3 + üst 3 nokta (üçgen / dörtgen prizma) → convex hull benzeri: iki uç düzlemden loft
            return cq.Solid.makeLoft([cq.Wire.makePolygon([V(*p) for p in pts6[0]], close=True), cq.Wire.makePolygon([V(*p) for p in pts6[1]], close=True)], True)
        hw = W / 2.0; hl = L / 2.0
        kesik = kati([[P(-hl, -hw, -1), P(-hl, hw, -1), P(-hl, hw, t + 1), P(-hl, -hw, t + 1)],
                      [P(hl, -hw, -1), P(hl, hw, -1), P(hl, hw, t + 1), P(hl, -hw, t + 1)]])
        # başlık: kapalı kenardan (q = −hw, z 0) açık kenara (q = +hw, z h) eğimli levha (t kalın) + iki yan üçgen
        bas = kati([[P(-hl, -hw, 0), P(-hl, hw, h), P(-hl, hw, h + t), P(-hl, -hw, t)],
                    [P(hl, -hw, 0), P(hl, hw, h), P(hl, hw, h + t), P(hl, -hw, t)]])
        yan = [kati([[P(s0, -hw, t), P(s0, hw, t), P(s0, hw, h + t)], [P(s0 + ds, -hw, t), P(s0 + ds, hw, t), P(s0 + ds, hw, h + t)]])
               for s0, ds in ((-hl - t, t), (hl, t))]
        return _birlestir([bas] + yan), kesik
    if fm["tip"] == "kabartma":
        L, W, h, r, eg = fm["boy"], fm["en"], fm["h"], fm.get("r", 0.0), math.radians(fm.get("egim", 20.0))
        tan = math.tan(eg)
        def frustum(LL, WW, rr, z0, hh):
            f = yuz_dikd_r(0.0, 0.0, LL, WW, 0.0, rr)
            LL2, WW2 = LL - 2 * hh * tan, WW - 2 * hh * tan
            f2 = yuz_dikd_r(0.0, 0.0, LL2, WW2, 0.0, max(0.0, rr - hh * tan)).translate(V(0, 0, hh))
            s = cq.Solid.makeLoft([f.outerWire(), f2.outerWire()], True)
            return s.translate(V(0, 0, z0))
        dis_ = frustum(L, W, r, t, h)                                        # dış (üst yüzden h yükselen)
        ic_ = frustum(L - 2 * t, W - 2 * t, max(0.0, r - t), -1.0, h + 1.0)  # iç boşluk (alt yüzden)
        M = _M(np.array([[ux, nx, 0], [uy, ny, 0], [0, 0, 1.0]]), (u0, v0, 0.0))
        if yon < 0:
            M = M @ _M(np.diag([1.0, -1.0, -1.0]), (0, 0, t))
        return _tasi(dis_, M), _tasi(ic_, M)
    raise ValueError(fm["tip"])


# =====================================================================================================================================
# 5 · AÇINIM DIŞA AKTARMA + AÇINIMDAN YENİDEN BÜKÜM (bağımsız yol: yalnız JSON verisiyle)
# =====================================================================================================================================
def _r5(x):
    return round(float(x), 5)


def _tel_varliklari(tel, yuz):
    out = []
    ex = BRepTools_WireExplorer(tel.wrapped, yuz.wrapped)
    while ex.More():
        E = ex.Current(); e = cq.Edge(E)
        p0 = BRep_Tool.Pnt_s(TopExp.FirstVertex_s(E, True)); p1 = BRep_Tool.Pnt_s(TopExp.LastVertex_s(E, True))
        a0, a1 = [_r5(p0.X()), _r5(p0.Y())], [_r5(p1.X()), _r5(p1.Y())]
        g = e.geomType()
        if g == "LINE":
            out.append(dict(t="L", p=[a0, a1]))
        elif g == "CIRCLE":
            c = BRepAdaptor_Curve(E); u0, u1 = c.FirstParameter(), c.LastParameter(); pm = c.Value((u0 + u1) / 2.0)
            cc = c.Circle().Location(); r = c.Circle().Radius()
            if abs(abs(u1 - u0) - 2 * math.pi) < 1e-6:
                out.append(dict(t="C", c=[_r5(cc.X()), _r5(cc.Y())], r=_r5(r)))
            else:
                out.append(dict(t="A", p=[a0, [_r5(pm.X()), _r5(pm.Y())], a1], c=[_r5(cc.X()), _r5(cc.Y())], r=_r5(r)))
        else:
            c = BRepAdaptor_Curve(E); u0, u1 = c.FirstParameter(), c.LastParameter()
            if E.Orientation() == TopAbs_REVERSED: u0, u1 = u1, u0
            n = 24; q = [c.Value(u0 + (u1 - u0) * i / n) for i in range(n + 1)]
            for i in range(n): out.append(dict(t="L", p=[[_r5(q[i].X()), _r5(q[i].Y())], [_r5(q[i + 1].X()), _r5(q[i + 1].Y())]]))
        ex.Next()
    return out


def _varlik_noktalari(e):
    if e["t"] == "L": return [tuple(e["p"][0]), tuple(e["p"][1])]
    if e["t"] == "A": return [tuple(p) for p in e["p"]] + [(e["c"][0] + e["r"] * math.cos(a), e["c"][1] + e["r"] * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 33)
                                                          if _yay_icinde(e, a)]
    return [(e["c"][0] + e["r"] * math.cos(a), e["c"][1] + e["r"] * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 33)]


def _yay_icinde(e, a):
    c = e["c"]; s, m, f = (math.atan2(p[1] - c[1], p[0] - c[0]) for p in e["p"])
    def ara(x, a0, a1): return (x - a0) % (2 * math.pi) <= (a1 - a0) % (2 * math.pi) + 1e-9
    return ara(a, s, f) if ara(m, s, f) else ara(a, f, s)


def _min_dikdortgen(pts):
    """dışbükey zarf + döner kumpas → (L, W, açı°) en küçük alanlı dikdörtgen"""
    P = sorted(set((round(x, 6), round(y, 6)) for x, y in pts))
    if len(P) < 3:
        return 0.0, 0.0, 0.0
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(hi) >= 2 and cr(hi[-2], hi[-1], p) <= 0: hi.pop()
        hi.append(p)
    H = np.array(lo[:-1] + hi[:-1]); en = (1e18, 0, 0, 0)
    for i in range(len(H)):
        d = H[(i + 1) % len(H)] - H[i]; L = np.linalg.norm(d)
        if L < 1e-9: continue
        u = d / L; w = np.array([-u[1], u[0]]); a = H @ u; b = H @ w
        A = (a.max() - a.min()) * (b.max() - b.min())
        if A < en[0]: en = (A, a.max() - a.min(), b.max() - b.min(), math.degrees(math.atan2(u[1], u[0])))
    return en[1], en[2], en[3]


def _varliklardan_tel(ents):
    es = []
    for e in ents:
        if e["t"] == "L":
            es.append(cq.Edge.makeLine(_V2(*e["p"][0]), _V2(*e["p"][1])))
        elif e["t"] == "A":
            es.append(cq.Edge.makeThreePointArc(_V2(*e["p"][0]), _V2(*e["p"][1]), _V2(*e["p"][2])))
        elif e["t"] == "C":
            return cq.Wire.makeCircle(e["r"], _V2(*e["c"]), V(0, 0, 1))
    return cq.Wire.assembleEdges(es)


def _varliklardan_yuz(dis, icler):
    konturlar = dis if (dis and isinstance(dis[0], list)) else [dis]
    F = _birlestir([cq.Face.makeFromWires(_varliklardan_tel(k)) for k in konturlar], temizle=False)
    for k in icler:
        F = F.cut(cq.Face.makeFromWires(_varliklardan_tel(k)))
    return F


def acinimdan_kati(acn, dw=0.1):
    """BAĞIMSIZ YENİDEN BÜKÜM: yalnız açınım JSON'u (kontur + büküm çizgileri + açı/yön/R/BA + sabit yüz + kök dönüşümü) okunur.
    Açınım büküm şeritlerinden bölünür, paneller bağlantı ağacıyla (BFS) katlanır. Dönüş (katı, rapor)."""
    t = float(acn["t"]); Z = np.array([0.0, 0.0, 1.0])
    F = _varliklardan_yuz(acn["dis_kontur"] if not acn.get("ek_dis_konturlar") else [acn["dis_kontur"]] + acn["ek_dis_konturlar"], acn["ic_konturlar"])
    bk = []
    for b in acn["bukumler"]:
        T0 = np.array(b["baslangic"], float); T1 = np.array(b["bitis"], float); BA = float(b["BA"])
        e = _n(T0[1] - T0[0]); m = (T1[0] - T0[0]) / BA
        rect = yuz_poligon([tuple(T0[0]), tuple(T0[1]), tuple(T1[1]), tuple(T1[0])])
        bk.append(dict(b=b, T0=T0, T1=T1, BA=BA, e=e, m=_n(m), rect=rect))
    U = _birlestir([x["rect"] for x in bk]) if bk else None
    paneller = (F.cut(U) if U is not None else F).Faces()
    paneller = [p for p in paneller if p.Area() > 1e-6]
    def hangi(q):
        for i, p in enumerate(paneller):
            if _icinde(p, (q[0], q[1], 0.0), 1e-9): return i
        return None
    kenarlar = []
    for j, x in enumerate(bk):
        parc = [g for g in F.intersect(x["rect"]).Faces() if g.Area() > 1e-9]
        x["parca"] = parc
        if not parc: continue
        g = max(parc, key=lambda f: f.Area()); c = g.Center(); cc = np.array([c.x, c.y])
        wm = float(np.dot(cc - x["T0"][0], x["e"]))
        eps = 1e-3
        q0 = x["T0"][0] + x["e"] * wm - x["m"] * eps; q1 = x["T1"][0] + x["e"] * wm + x["m"] * eps
        x["yan"] = (hangi(q0), hangi(q1))
        kenarlar.append(j)
    s0 = acn.get("sabit_yuz")
    kok = hangi(s0) if s0 else 0
    if kok is None: raise ValueError("sabit yüz bulunamadı")
    T = {kok: np.array(acn["donusum_3b"], float)}
    sira, sektorler, kullanilan = [kok], [], set()
    while sira:
        p = sira.pop(0)
        for j in kenarlar:
            if j in kullanilan: continue
            x = bk[j]; a, b_ = x["yan"]
            if p not in (a, b_): continue
            if a == p: sabit_cizgi, yon_v, cocuk = x["T0"], x["m"], b_
            else: sabit_cizgi, yon_v, cocuk = x["T1"], -x["m"], a
            if cocuk is None: raise ValueError("büküm %d: karşı panel yok" % x["b"]["no"])
            kullanilan.add(j)
            th = math.radians(x["b"]["aci"]); R = float(x["b"]["R"]); up = x["b"]["yon"] == "yukari"; BA = x["BA"]
            A = np.r_[sabit_cizgi[0], 0.0] + Z * ((t + R) if up else -R)
            d3 = np.r_[yon_v, 0.0]
            k = np.cross(d3, Z) if up else np.cross(Z, d3)
            rho = -Z if up else Z
            Fm = _M_eksen(A, k, th) @ _M_ot(-BA * d3)
            if cocuk in T:
                continue
            T[cocuk] = T[p] @ Fm
            sira.append(cocuk)
            # şerit dilimleri: (s, w') sağ elli (w' = Z × yön)
            wv = np.array([-yon_v[1], yon_v[0]]); o2 = sabit_cizgi[0]
            H = np.array([[yon_v[0], wv[0], o2[0]], [yon_v[1], wv[1], o2[1]], [0, 0, 1.0]])
            Hi = np.linalg.inv(H)
            for g in x["parca"]:
                for a0, a1, w0, w1 in _dikd_ayir(_yuz_tasi(g, Hi), BA, dw):
                    if a1 - a0 < 1e-9: continue
                    sk = _sektor(A, k, rho, np.r_[wv, 0.0], w0, w1, R, R + t, th * a0 / BA, th * (a1 - a0) / BA)
                    sektorler.append(_tasi(sk, T[p]))
    eksik = [i for i in range(len(paneller)) if i not in T]
    if eksik: raise ValueError("katlanamayan panel: %s" % eksik)
    ss = [_tasi(_prizma(paneller[i], t), T[i]) for i in range(len(paneller))] + sektorler
    return _birlestir(ss), dict(panel=len(paneller), bukum=len(kullanilan), sektor=len(sektorler), kok=kok)


# =====================================================================================================================================
# 6 · KALINLIK DOĞRULAYICI + KESİT
# =====================================================================================================================================
def _yuz_ornekleri(f, n=3):
    S = BRepAdaptor_Surface(f.wrapped, True)
    u0, u1, v0, v1 = S.FirstUParameter(), S.LastUParameter(), S.FirstVParameter(), S.LastVParameter()
    out = []
    for fu, fv in ((0.5, 0.5), (0.31, 0.37), (0.69, 0.63), (0.23, 0.77), (0.77, 0.23), (0.5, 0.13), (0.13, 0.5), (0.87, 0.5), (0.5, 0.87)):
        u, v = u0 + (u1 - u0) * fu, v0 + (v1 - v0) * fv
        if BRepClass_FaceClassifier(f.wrapped, gp_Pnt2d(u, v), 1e-9).State() != TopAbs_IN: continue
        pr = BRepLProp_SLProps(S, u, v, 1, 1e-9)
        if not pr.IsNormalDefined(): continue
        nn = pr.Normal(); nv = np.array([nn.X(), nn.Y(), nn.Z()])
        if f.wrapped.Orientation() == TopAbs_REVERSED: nv = -nv
        p = S.Value(u, v)
        out.append((np.array([p.X(), p.Y(), p.Z()]), nv))
        if len(out) >= n: break
    return out


def kalinlik_denetle(sh, t, tol=None, haric=None):
    """Sac kalınlığı her yerde t mi? · her yüzde ≤ 3 örnek noktadan iç normal yönünde ışın: karşı yüze uzaklık = t ise 'ana yüz';
    değilse yüz 'kenar şeridi' mi (genişliği t: alan / (çevre/2)) bakılır; ikisi de değilse HATA."""
    tol = tol if tol is not None else max(0.01, 0.01 * t)
    it = IntCurvesFace_ShapeIntersector(); it.Load(sh.wrapped, 1e-7)
    r = dict(t=t, yuz=0, ana=0, kenar=0, haric=0, hata=[], olcum_min=None, olcum_max=None)
    ol = []
    for i, f in enumerate(sh.Faces()):
        r["yuz"] += 1
        ornek = _yuz_ornekleri(f)
        if haric and ornek and all(any(_kutu_icinde(p, k) for k in haric) for p, _n_ in ornek):
            r["haric"] += 1; continue
        ds = []
        for p, nv in ornek:
            q = p - nv * 1e-5
            it.Perform(gp_Lin(gp_Pnt(*q), gp_Dir(*(-nv))), 1e-7, 1e5)
            ws = sorted(it.WParameter(j) for j in range(1, it.NbPnt() + 1) if it.WParameter(j) > 1e-7)
            ds.append(ws[0] + 1e-5 if ws else float("inf"))
        if ds and all(abs(d - t) < tol for d in ds):
            r["ana"] += 1; ol.extend(ds); continue
        A = f.Area(); P = sum(e.Length() for e in f.Edges())
        w1 = A / (P / 2.0) if P > 0 else 0; dsc = (P / 2.0) ** 2 - 4 * A
        ws_ = [w1] + ([(P / 2.0 - math.sqrt(dsc)) / 2.0, (P / 2.0 + math.sqrt(dsc)) / 2.0] if dsc >= 0 else [])
        if min(abs(w - t) for w in ws_) < 0.03 * t:                 # kesim kenarı şeridi (genişliği t; kısa şeritte büyük kök)
            r["kenar"] += 1; continue
        if f.geomType() == "CYLINDER":                               # delik / yuvarlak kesik duvarı: eksen boyunca boyu t
            ax = BRepAdaptor_Surface(f.wrapped, True).Cylinder().Axis().Direction(); ax = np.array([ax.X(), ax.Y(), ax.Z()])
            zz = [float(np.dot(np.array(v.toTuple()), ax)) for v in f.Vertices()]
            if zz and abs((max(zz) - min(zz)) - t) < tol:
                r["kenar"] += 1; continue
        if A < 0.05 * t * t:                                         # eğri kesiğin basamak yüzü (0,1 mm adım) — yaklaşım artığı
            r["basamak"] = r.get("basamak", 0) + 1; continue
        r["hata"].append(dict(yuz=i, tip=f.geomType(), alan=round(A, 3), isin=[round(d, 4) for d in ds], w=[round(w, 4) for w in ws_]))
    if ol: r["olcum_min"], r["olcum_max"] = round(min(ol), 5), round(max(ol), 5)
    r["gecti"] = not r["hata"]
    return r


def _kutu_icinde(p, k):
    return k[0] <= p[0] <= k[1] and k[2] <= p[1] <= k[3] and k[4] <= p[2] <= k[5]


def kesit_yaricaplari(sh, nokta, normal, eksen=None, tol=1e-3):
    """nokta'dan geçen, normal'e dik düzlemle kesit → daire yaylarının yarıçapları (eksen verilirse yalnız o merkezli yaylar)"""
    sec = BRepAlgoAPI_Section(sh.wrapped, gp_Pln(gp_Pnt(*map(float, nokta)), gp_Dir(*map(float, _n(normal)))), False)
    sec.Build()
    out = []
    for e in cq.Shape.cast(sec.Shape()).Edges():
        if e.geomType() != "CIRCLE": continue
        c = e.arcCenter()
        if eksen is not None and np.linalg.norm(np.array([c.x, c.y, c.z]) - np.asarray(eksen)) > tol: continue
        out.append(e.radius())
    return out


def kesit_kenarlari(sh, nokta, normal, adim=24):
    """kesit çizimi için: [(tip, [noktalar])] — doğru ve yaylar ayrıklaştırılmış"""
    sec = BRepAlgoAPI_Section(sh.wrapped, gp_Pln(gp_Pnt(*map(float, nokta)), gp_Dir(*map(float, _n(normal)))), False)
    sec.Build(); out = []
    for e in cq.Shape.cast(sec.Shape()).Edges():
        c = BRepAdaptor_Curve(e.wrapped); u0, u1 = c.FirstParameter(), c.LastParameter()
        n = 1 if e.geomType() == "LINE" else adim
        out.append((e.geomType(), [tuple(np.array([c.Value(u0 + (u1 - u0) * i / n).X(), c.Value(u0 + (u1 - u0) * i / n).Y(), c.Value(u0 + (u1 - u0) * i / n).Z()])) for i in range(n + 1)]))
    return out


# =====================================================================================================================================
# 7 · DFM (üretilebilirlik)
# =====================================================================================================================================
def _madde(kural, durum, detay, **k):
    return dict(kural=kural, durum=durum, detay=detay, **k)


def _ic_yuz_payi(B):
    """büküm teğet çizgisinden flanş iç yüzüne"""
    return B.R * math.tan(min(B.th, math.pi / 2) / 2.0)


def dfm_denetle(sac, abkant=True):
    t = sac.t; out = []
    mut, tas = STD.min_flans(t)
    # 1 · min flanş / hem dönüşü
    for B in sac.bukumler:
        poly = B.cocuk.poly; Lmin = min(p[0] for p in poly if p[0] > 1e-9) if any(p[0] > 1e-9 for p in poly) else B.Lf
        if B.tip.startswith("kivirma"):
            R_, dmin = STD.hem(t, B.tip.split("_")[1])
            d = "%s dönüş %.2f ≥ %.2f (%s)" % (B.cocuk.ad, Lmin, dmin, B.tip)
            out.append(_madde("min_flans", "GEÇTİ" if Lmin >= dmin - 1e-6 else "HATA", d, bukum=B.no + 1))
            if t > 1.5 and B.tip == "kivirma_kapali": out.append(_madde("hem_kalinlik", "HATA", "304 kapalı hem t ≤ 1,5 (standart)", bukum=B.no + 1))
            continue
        dis = (Lmin + math.tan(min(B.th, math.radians(179)) / 2.0) * (t + B.R) if B.aci < 179 else Lmin) + getattr(B, "uc_geri", 0.0)
        dur = "GEÇTİ" if dis >= tas - 1e-6 else ("UYARI" if dis >= mut - 1e-6 else "HATA")
        if B.tip == "ofset" and dur != "GEÇTİ": dur = "BİLGİ"
        out.append(_madde("min_flans", dur, "%s dış %.2f (düz %.2f) · mutlak %.1f · tasarım %.1f%s" % (B.cocuk.ad, dis, Lmin, mut, tas,
                                                                                                 " · ofset kalıbıyla tek vuruş" if B.tip == "ofset" else ""), bukum=B.no + 1))
    # 2 · aynı parçada tek R
    Rs = sorted({round(B.R, 4) for B in sac.bukumler if not B.tip.startswith("kivirma")})
    Rh = sorted({round(B.R, 4) for B in sac.bukumler if B.tip.startswith("kivirma")})
    if sac.bukumler:
        out.append(_madde("tek_R", "GEÇTİ" if len(Rs) <= 1 else "HATA", "büküm R %s%s" % (Rs, " · kıvırma (ayrı takım) R %s" % Rh if Rh else "")))
    if sac.bolge == "gida":
        rm = STD.gida_R_min()
        out.append(_madde("gida_ic_R", "GEÇTİ" if all(r >= rm - 1e-9 for r in Rs) else "HATA", "gıda bölgesi iç R ≥ %.1f · bulunan %s" % (rm, Rs)))
        if any(k["kayit"]["tip"] == "bindirme" for k in sac.kaynaklar): out.append(_madde("gida_bindirme", "HATA", "gıda bölgesinde bindirme yok (standart)"))
    # 3 · relief / köşe
    pan, ser = sac._bolgeler()
    for B in sac.bukumler:
        P = B.ebeveyn; kn = P.kenar(B.kenar)
        for uc, w, sg in (("bas", B.a, -1), ("son", B.b, +1)):
            kos = getattr(B, "kose_bas" if uc == "bas" else "kose_son", None)
            q = kn["p0"] + kn["e2"] * (w + sg * 0.05) - kn["out2"] * 0.05
            ham = _icinde(P._ham_yuz(), (q[0], q[1], 0.0))          # kesiksiz panelde büküm ucunun yanında malzeme var mı
            son_ = _icinde(pan[P.no], (q[0], q[1], 0.0))            # kesiklerden sonra hâlâ var mı
            if kos is not None:
                if kos["rahat"] is None:
                    out.append(_madde("kose_rahatlatma", "UYARI", "%s %s ucu: köşede rahatlatma yok (lazer köşe deliği Ø2t önerilir)" % (B.cocuk.ad, uc), bukum=B.no + 1))
                else:
                    out.append(_madde("kose_rahatlatma", "GEÇTİ", "%s %s ucu: köşe %s rahatlatma" % (B.cocuk.ad, uc, kos["rahat"]), bukum=B.no + 1))
                continue
            if ham:
                out.append(_madde("relief", "HATA" if son_ else "GEÇTİ", "%s %s ucu: kenar büküm ucunda devam ediyor · relief %s" % (B.cocuk.ad, uc, "YOK" if son_ else "VAR"),
                                  bukum=B.no + 1))
    # 4 · delik ↔ büküm / kenar / köprü / çap / PEM
    D = sac._duz_yuz()
    dis_tel = [f.outerWire() for f in D.Faces()]
    serit_duz = {B.no: _yuz_tasi(ser[B.no], B.ebeveyn.D @ B.Hs) for B in sac.bukumler if _alan(ser[B.no]) > 1e-9}
    dfm_kes = [(P, k, _yuz_tasi(k.yuz, P.D)) for P in sac.paneller for k in P.kesikler if k.dfm]
    md = STD.mesafe("min_delik", t); dk = STD.mesafe("delik_kenar", t); kp = STD.mesafe("delik_kopru", t)
    yasak = " ".join(STD.pem_yasak())
    for P, k, kf in dfm_kes:
        ad = "%s/%s" % (P.ad, k.tip)
        olc = k.meta.get("cap") or min(k.meta.get("en") or 1e9, k.meta.get("boy") or 1e9)
        if olc and olc < 1e8 and olc < md - 1e-9 and k.tip not in ("yuva",):
            out.append(_madde("min_delik_cap", "HATA", "%s Ø/en %.2f < %.2f" % (ad, olc, md)))
        if k.tip in ("pem_somun", "pem_saplama"):
            kural = "pem_eksen_flans"; ihtiyac = k.meta.get("kenar_min", 7.0)
        elif k.tip in ("yarik", "havalandirma_yarigi") or k.meta.get("sekil") == "oblong":
            kural = "yarik_flans"; ihtiyac = STD.mesafe("yarik_flans", t)
        else:
            kural = "delik_flans"; ihtiyac = STD.mesafe("delik_flans", t)
        for B in sac.bukumler:
            if B.no not in serit_duz: continue
            d = kf.distance(serit_duz[B.no])
            if k.tip in ("pem_somun", "pem_saplama"):
                c = k.meta["merkez"]; cd = _Hp(P.D, c); d = serit_duz[B.no].distance(cq.Vertex.makeVertex(cd[0], cd[1], 0.0))
                gerek = ihtiyac + B.R
                dd = d                         # eksen → teğet; standart: eksen → flanş iç yüzü ≥ kenar + R ⇔ eksen → teğet ≥ kenar
                if dd + _ic_yuz_payi(B) < gerek - 1e-6:
                    out.append(_madde(kural, "HATA", "%s eksen → büküm %d iç yüzü %.2f < %.2f" % (ad, B.no + 1, dd + _ic_yuz_payi(B), gerek)))
            elif k.tip == "yuva":
                continue
            elif d + _ic_yuz_payi(B) < ihtiyac - 1e-6:
                out.append(_madde(kural, "HATA", "%s → büküm %d iç yüzü %.2f < %.2f" % (ad, B.no + 1, d + _ic_yuz_payi(B), ihtiyac)))
        dke = min(kf.distance(w) for w in dis_tel)
        if k.tip in ("pem_somun", "pem_saplama"):
            c = _Hp(P.D, k.meta["merkez"]); dke = min(w.distance(cq.Vertex.makeVertex(c[0], c[1], 0.0)) for w in dis_tel)
            if dke < k.meta.get("kenar_min", 7.0) - 1e-6:
                out.append(_madde("pem_kenar", "HATA", "%s eksen → sac kenarı %.2f < %.2f" % (ad, dke, k.meta.get("kenar_min", 7.0))))
            pt = k.meta.get("pem_tip", "")
            if any(pt and pt in w_.split(" ")[1:2] for w_ in STD.pem_yasak()) or ("CLS" in pt and "CLS" in yasak):
                out.append(_madde("pem_malzeme", "HATA", "%s PEM %s 304 sacta yasak (%s)" % (ad, pt, yasak)))
            if t < k.meta.get("min_sac", 0) - 1e-9:
                out.append(_madde("pem_min_sac", "HATA", "%s sac %.2f < PEM min %.2f" % (ad, t, k.meta["min_sac"])))
        elif dke < dk - 1e-6 and k.tip != "yuva":
            out.append(_madde("delik_kenar", "HATA", "%s → sac kenarı %.2f < %.2f" % (ad, dke, dk)))
    for i in range(len(dfm_kes)):
        for j in range(i + 1, len(dfm_kes)):
            a, b = dfm_kes[i][2], dfm_kes[j][2]
            if not _bb_kesisir(a.BoundingBox(), b.BoundingBox(), kp + 1.0): continue
            d = a.distance(b)
            if d < kp - 1e-6:
                out.append(_madde("delik_kopru", "HATA", "%s ↔ %s köprü %.2f < %.2f" % (dfm_kes[i][0].ad, dfm_kes[j][0].ad, d, kp)))
    if not any(m["kural"] in ("delik_flans", "yarik_flans", "pem_eksen_flans", "delik_kenar", "pem_kenar", "delik_kopru", "min_delik_cap", "pem_malzeme")
               for m in out):
        out.append(_madde("delikler", "GEÇTİ", "%d delik/kesik: büküm iç yüzü (delik %.1f · yarık %.1f · PEM kenar+R) · kenar %.1f · köprü %.1f · Ø ≥ %.1f"
                          % (len(dfm_kes), STD.mesafe("delik_flans", t), STD.mesafe("yarik_flans", t), dk, kp, md)))
    # 5 · dil
    for P in sac.paneller:
        for e in P.ekler:
            if e["tip"] == "dil":
                ok = e["en"] >= 2 * t - 1e-9 and e["boy"] <= 5 * e["en"] + 1e-9
                out.append(_madde("dil", "GEÇTİ" if ok else "UYARI", "%s dil %.1f × %.1f (en ≥ 2t, boy ≤ 5 en)" % (P.ad, e["en"], e["boy"])))
    # 6 · levha boyu + abkant boyu + tek parça
    a = sac.acinim(); Lmax, Wmax = STD.max_acinim()[1], STD.max_acinim()[0]
    L, W = a["levha"]["boy"], a["levha"]["en"]
    out.append(_madde("levha", "GEÇTİ" if (L <= Lmax + 1e-6 and W <= Wmax + 1e-6) else "HATA", "açınım %.1f × %.1f ≤ %.0f × %.0f" % (L, W, Lmax, Wmax)))
    bmax = max([B.b - B.a for B in sac.bukumler] or [0.0])
    if sac.bukumler:
        out.append(_madde("abkant_boy", "GEÇTİ" if bmax <= STD.abkant_boy() else "HATA", "en uzun büküm %.1f ≤ %.0f" % (bmax, STD.abkant_boy())))
    out.append(_madde("tek_parca_duz", "GEÇTİ" if a["parca_sayisi"] == 1 else "HATA", "açınım %d parça" % a["parca_sayisi"]))
    K = sac.kati_temel()
    bs = sac._bolge_katilari(); top = sum(s.Volume() for _e, s in bs); vk = K.Volume()
    out.append(_madde("tek_parca_3b", "GEÇTİ" if len(K.Solids()) == 1 else "HATA", "3B %d katı" % len(K.Solids())))
    ort = top - vk
    out.append(_madde("kendi_cakisma", "GEÇTİ" if ort < 1e-3 * max(1.0, vk) * 1e-3 + 1e-3 else "HATA", "bölgeler toplamı − birleşik hacim = %.4f mm³" % ort))
    # 7 · abkant sırası / çarpışma
    if abkant and sac.bukumler:
        ab = abkant_denetle(sac)
        sor = ab["varsayilan_carpisma"]
        if not sor:
            out.append(_madde("abkant", "GEÇTİ", "sıra %s · bıçak / kalıp / koç çarpması yok%s" % (ab["sira"], " · " + ab["not_"] if ab["not_"] else ""), sira=ab["sira"]))
        elif ab["oneri_sira"] and not ab["oneri_carpisma"]:
            out.append(_madde("abkant", "UYARI", "tanım sırasında çarpışma %s → ÖNERİLEN SIRA %s temiz" % (sor[:3], ab["oneri_sira"]), sira=ab["oneri_sira"]))
        else:
            ar = ab.get("arama") or {}
            out.append(_madde("abkant", "HATA", "düz bıçak + V kalıpla HİÇBİR sırada temiz değil (%s %d sıra denemesi%s) · en iyi sıra %s · çarpışma %s → kaz boynu bıçak + bölünmüş kalıp "
                              "ya da profil ayrı parça" % ("tam arama" if ar.get("tam") else "sınırda kesildi", ar.get("deneme", 0), "", ab["oneri_sira"],
                                                          [(c["bukum"], c["evre"], c["arac"], c["bolge"]) for c in (ab["oneri_carpisma"] or sor)[:4]]),
                              sira=ab["oneri_sira"]))
    return out


# =====================================================================================================================================
# 8 · ABKANT ÇARPIŞMA (basit 3B: düz bıçak + koç bloğu + V kalıp)
# =====================================================================================================================================
BICAK = dict(uc_aci=85.0, govde=26.0, yukseklik=100.0, koc_gen=80.0, koc_yuk=500.0, kalip_gen=None, kalip_yuk=80.0, kalip_aci=88.0, kalip_tasma=5.0)   # kalip_gen None → V + 18 (tek V kalıp) · kalip_tasma: kalıbın büküm boyundan taşması (0 = bölünmüş kalıp)


def _arac_kati(B, t, uc_aci, H, wa, wb):
    """B'nin ebeveyn yerelinde (düz durum) bıçak + koç ve kalıp katıları · wa–wb gerçek büküm aralığı (bölünmüş bıçak boyu)"""
    R = B.R; d = (1 if B.yon > 0 else -1) * np.array([0, 0, 1.0]); q = B.o3; e = B.e3
    wa, wb = wa + 0.2, wb - 0.2
    def kati2(poly2, w0, w1):
        pts = [V(*(B.A0 + q * a_ + d * b_ + e * w0)) for a_, b_ in poly2]
        return cq.Solid.extrudeLinear(cq.Wire.makePolygon(pts, close=True), [], V(*(e * (w1 - w0))))
    be = math.radians(uc_aci / 2.0); Rp = max(R - 0.05, 0.05)
    T1, T0 = (Rp * math.cos(be), -Rp * math.sin(be)), (-Rp * math.cos(be), -Rp * math.sin(be))
    lam = (BICAK["govde"] / 2.0 - Rp * math.cos(be)) / math.sin(be); db = -Rp * math.sin(be) + lam * math.cos(be)
    g = BICAK["govde"] / 2.0; kg = BICAK["koc_gen"] / 2.0
    bicak = kati2([T0, T1, (g, db), (g, H), (kg, H), (kg, H + BICAK["koc_yuk"]), (-kg, H + BICAK["koc_yuk"]), (-kg, H), (-g, H), (-g, db)], wa, wb)
    uc = cq.Solid.makeCylinder(Rp, wb - wa, V(*(B.A0 + e * wa)), V(*e))
    bicak = bicak.fuse(uc)
    Vk = STD.V(t); top = -(R + t) - 0.01; gd = (Vk / 2.0) / math.tan(math.radians(BICAK["kalip_aci"] / 2.0))
    kw, kh = (BICAK["kalip_gen"] or (Vk + 18.0)) / 2.0, BICAK["kalip_yuk"]
    kalip = kati2([(-kw, top - kh), (kw, top - kh), (kw, top), (Vk / 2.0, top), (0.0, top - gd), (-Vk / 2.0, top), (-kw, top)], wa - BICAK["kalip_tasma"], wb + BICAK["kalip_tasma"])
    return bicak, kalip


def abkant_denetle(sac, sira=None, esik=0.5):
    """büküm sırası çarpışma denetimi. Her büküm için: (1) düz durumda bıçak + kalıp, (2) bükük durumda (θ/2 dönmüş) bıçak.
    Daha önce bükülmüş flanşlar parça üzerinde. Kıvırma (hem) ve ofset ayrı takımla → atlanır (sırada yine yer alır)."""
    pk, sk = sac._yerel_katilar(); pan, ser = sac._bolgeler(); t = sac.t
    dsk = {B.no: _H_M(B.Hs) for B in sac.bukumler}
    duz_serit = {B.no: (_tasi(_prizma(ser[B.no], t), dsk[B.no]) if _alan(ser[B.no]) > 1e-9 else None) for B in sac.bukumler}
    onbellek = {}

    def durum_katilari(bukuk):
        M = {0: np.eye(4)}
        for B in sac.bukumler:
            M[B.cocuk.no] = M[B.ebeveyn.no] @ (B.Lb if B.no in bukuk else B.Ld)
        ss = [(("P", P.no), _tasi(pk[P.no], M[P.no])) for P in sac.paneller if pk[P.no] is not None]
        for B in sac.bukumler:
            if B.no in bukuk: ss += [(("B", B.no), _tasi(s, M[B.ebeveyn.no])) for s in sk[B.no]]
            elif duz_serit[B.no] is not None: ss.append((("B", B.no), _tasi(duz_serit[B.no], M[B.ebeveyn.no])))
        return M, ss

    def dene(k, yapilan):
        anahtar = (k, frozenset(yapilan))
        if anahtar in onbellek: return onbellek[anahtar]
        B = sac.bukumler[k]; sorun = []
        if B.tip.startswith("kivirma") or B.tip == "ofset":
            onbellek[anahtar] = sorun; return sorun
        uc_aci = BICAK["uc_aci"] if B.aci <= 95.0 else max(20.0, 180.0 - B.aci - 5.0)
        fs = ser[B.no].Faces()
        wa, wb = (min(f.BoundingBox().ymin for f in fs), max(f.BoundingBox().ymax for f in fs)) if fs else (B.a, B.b)
        bicak, kalip = _arac_kati(B, t, uc_aci, BICAK["yukseklik"], wa, wb)
        for evre, bukuk in (("baslangic", set(yapilan)), ("bitis", set(yapilan) | {k})):
            M, ss = durum_katilari(bukuk)
            Mp = M[B.ebeveyn.no]
            araclar = [("bicak", _tasi(bicak, Mp))] if evre == "bitis" else [("bicak", _tasi(bicak, Mp)), ("kalip", _tasi(kalip, Mp))]
            if evre == "bitis":
                araclar = [("bicak", _tasi(bicak.rotate(V(*B.A0), V(*(B.A0 + B.k)), B.aci / 2.0), Mp))]
            for an, ar in araclar:
                ab = ar.BoundingBox()
                for et, s in ss:
                    if not _bb_kesisir(ab, s.BoundingBox()): continue
                    try:
                        v = ar.intersect(s).Volume()
                    except Exception:
                        v = 0.0
                    if v > esik:
                        sorun.append(dict(bukum=k + 1, evre=evre, arac=an, bolge="%s%d" % et, hacim=round(v, 2)))
        onbellek[anahtar] = sorun
        return sorun

    n = len(sac.bukumler)
    vars_ = [B.no for B in sorted(sac.bukumler, key=lambda B: (B.tip.startswith("kivirma"), B.no))]
    sira = list(sira) if sira else vars_
    def sirala(s):
        bulunan = []
        for i, k in enumerate(s):
            bulunan += dene(k, s[:i])
        return bulunan
    c0 = sirala(sira)
    oneri, c1 = None, None
    if c0:
        # geri izlemeli arama (DFS): her adımda çarpışmasız bükümler denenir · üst sınır 600 deneme
        sayac = [0]; bulunan = [None]; ziyaret = set()
        def ara(yap, kalan):
            if bulunan[0] is not None or sayac[0] > 600: return
            if not kalan: bulunan[0] = list(yap); return
            if frozenset(yap) in ziyaret: return
            ziyaret.add(frozenset(yap))
            for k in kalan:
                sayac[0] += 1
                if not dene(k, yap):
                    ara(yap + [k], [x for x in kalan if x != k])
                    if bulunan[0] is not None: return
        ara([], list(vars_))
        if bulunan[0] is not None:
            oneri, c1 = bulunan[0], []
        else:
            yap, kalan, c1 = [], list(vars_), []
            while kalan:
                sec = next((k for k in kalan if not dene(k, yap)), None)
                if sec is None:
                    sec = kalan[0]; c1 += dene(sec, yap)
                yap.append(sec); kalan.remove(sec)
            oneri = yap
    atl = [B.no + 1 for B in sac.bukumler if B.tip.startswith("kivirma") or B.tip == "ofset"]
    arama = dict(deneme=sayac[0], sinir=600, tam=sayac[0] <= 600, durum_sayisi=len(onbellek)) if c0 else None
    return dict(sira=[k + 1 for k in sira], varsayilan_carpisma=c0, oneri_sira=[k + 1 for k in oneri] if oneri else None,
                oneri_carpisma=c1, arama=arama, not_=("kıvırma/ofset %s ayrı takım (denetim dışı)" % atl) if atl else "", bicak=dict(BICAK, V_kalip=STD.V(sac.t)))


# =====================================================================================================================================
# 9 · KAYNAK DİKİŞİ
# =====================================================================================================================================
def kaynak_dikisi(p0, p1, u1, u2, a, ad="kaynak", yontem="TIG 141", dolgu="ER308LSi", taraf="ic", birim="SAC", not_=""):
    """köşe (iç bükey) dikişi: p0 → p1 doğrusu boyunca, iki yüz doğrultusunda a bacaklı üçgen kesitli katı"""
    p0, p1, u1, u2 = (np.asarray(x, float) for x in (p0, p1, u1, u2))
    tel = cq.Wire.makePolygon([V(*p0), V(*(p0 + _n(u1) * a)), V(*(p0 + _n(u2) * a))], close=True)
    sh = cq.Solid.extrudeLinear(tel, [], V(*(p1 - p0)))
    L = float(np.linalg.norm(p1 - p0))
    return dict(ad=ad, wp=cq.Workplane("XY").add(sh), sh=sh, mal="paslanmaz", birim=birim, grup="SABIT", kaynak=SURUM, tur="kaynak",
                bom=("Köşe kaynak dikişi · %s · dolgu %s · a %.1f" % (yontem, dolgu, a), 1, "%.0f mm" % L, "%s %s" % (taraf, not_), "ÜRETİM"),
                meta=dict(tur="kaynak", tip="kose", yontem=yontem, dolgu=dolgu, a=a, boy=round(L, 2), taraf=taraf, iso2553="a%g ◺ %g" % (a, round(L))))


def kaynak_halka(merkez, eksen, r, a, ad="kaynak_halka", yontem="TIG 141", dolgu="ER308LSi", birim="SAC"):
    """silindir (r) ile düzlemin birleşim çevresine iç bükey halka dikiş — merkez düzlemde, eksen düzlemden uzağa"""
    M = _cerceve(merkez, eksen)
    tel = cq.Wire.makePolygon([V(r, 0, 0), V(r + a, 0, 0), V(r, 0, a)], close=True)
    sh = _tasi(cq.Solid.revolve(tel, [], 360.0, V(0, 0, 0), V(0, 0, 1)), M)
    return dict(ad=ad, wp=cq.Workplane("XY").add(sh), sh=sh, mal="paslanmaz", birim=birim, grup="SABIT", kaynak=SURUM, tur="kaynak",
                bom=("Çevre kaynak dikişi · %s · dolgu %s · a %.1f" % (yontem, dolgu, a), 1, "Ø%.0f çevre %.0f mm" % (2 * r, 2 * math.pi * r), "", "ÜRETİM"),
                meta=dict(tur="kaynak", tip="cevre", yontem=yontem, dolgu=dolgu, a=a, boy=round(2 * math.pi * r, 1)))


def kaynak_parcalari(sac):
    out = []
    for i, k in enumerate(sac.kaynaklar):
        if k["tip"] != "kose": continue
        Ba, Bb = k["Ba"], k["Bb"]; Ca, Cb = Ba.cocuk, Bb.cocuk; t = sac.t
        zi = t if Ba.yon > 0 else 0.0
        na, nb = Ca.M[:3, 2], Cb.M[:3, 2]
        pa, pb = _p(Ca.M, (0, 0, zi)), _p(Cb.M, (0, 0, zi))
        h = Ca.M[:3, 0]; oa = _p(Ca.M, (0, 0, 0))
        A = np.array([na, nb, h]); b = np.array([na @ pa, nb @ pb, h @ oa])
        P0 = np.linalg.solve(A, b)
        L = min(Ba.Lf, Bb.Lf)
        ua = Ca.M[:3, 1] * (1 if np.dot(_p(Ca.M, (0, (Ba.a + Ba.b) / 2.0, 0)) - P0, Ca.M[:3, 1]) > 0 else -1)
        ub = Cb.M[:3, 1] * (1 if np.dot(_p(Cb.M, (0, (Bb.a + Bb.b) / 2.0, 0)) - P0, Cb.M[:3, 1]) > 0 else -1)
        a = round(min(t, 3.0), 2)
        out.append(kaynak_dikisi(P0, P0 + h * L, ua, ub, a, ad="%s_kose_kaynagi_%d" % (sac.ad, i + 1), birim=sac.birim,
                                 not_="(dış köşe TIG kapatılır + taşlanır; katı iç köşede temsil)"))
    return out


# =====================================================================================================================================
# 10 · BAĞLANTI ELEMANLARI (gerçek ölçülü · standart numaralı · BOM)
# =====================================================================================================================================
D_NOM = {"M3": 3.0, "M4": 4.0, "M5": 5.0, "M6": 6.0, "M8": 8.0, "M10": 10.0, "M12": 12.0}
ISO7380 = {"M3": (5.7, 1.65, 2.0), "M4": (7.6, 2.2, 2.5), "M5": (9.5, 2.75, 3.0), "M6": (10.5, 3.3, 4.0), "M8": (14.0, 4.4, 5.0), "M10": (17.5, 5.5, 6.0)}   # dk, k, s
DIN7991 = {"M3": (6.0, 1.7, 2.0), "M4": (8.0, 2.3, 2.5), "M5": (10.0, 2.8, 3.0), "M6": (12.0, 3.3, 4.0), "M8": (16.0, 4.4, 5.0), "M10": (20.0, 5.5, 6.0)}
ISO4762 = {"M3": (5.5, 3.0, 2.5), "M4": (7.0, 4.0, 3.0), "M5": (8.5, 5.0, 4.0), "M6": (10.0, 6.0, 5.0), "M8": (13.0, 8.0, 6.0), "M10": (16.0, 10.0, 8.0), "M12": (18.0, 12.0, 10.0)}
ISO4032 = {"M3": (5.5, 2.4), "M4": (7.0, 3.2), "M5": (8.0, 4.7), "M6": (10.0, 5.2), "M8": (13.0, 6.8), "M10": (16.0, 8.4), "M12": (18.0, 10.8)}   # s, m
ISO10511 = {"M4": (7.0, 5.0), "M5": (8.0, 5.0), "M6": (10.0, 6.0), "M8": (13.0, 8.0), "M10": (16.0, 10.0), "M12": (18.0, 12.0)}
DIN1587 = {"M4": (7.0, 8.0), "M5": (8.0, 10.0), "M6": (10.0, 12.0), "M8": (13.0, 15.0), "M10": (17.0, 18.0), "M12": (19.0, 22.0)}
DIN125 = {"M3": (3.2, 7.0, 0.5), "M4": (4.3, 9.0, 0.8), "M5": (5.3, 10.0, 1.0), "M6": (6.4, 12.0, 1.6), "M8": (8.4, 16.0, 1.6), "M10": (10.5, 20.0, 2.0), "M12": (13.0, 24.0, 2.5)}
DIN9021 = {"M3": (3.2, 9.0, 0.8), "M4": (4.3, 12.0, 1.0), "M5": (5.3, 15.0, 1.2), "M6": (6.4, 18.0, 1.6), "M8": (8.4, 24.0, 2.0), "M10": (10.5, 30.0, 2.5), "M12": (13.0, 37.0, 3.0)}
DIN929 = {"M6": (10.0, 5.0), "M8": (14.0, 6.5), "M10": (17.0, 8.0), "M12": (19.0, 10.0)}
VIDA_BOY = [4, 5, 6, 8, 10, 12, 14, 16, 20, 25, 30, 35, 40, 45, 50, 60]
PEM_SOMUN = {   # S / CLS / SP aynı zarf (PEM bülteni, yaklaşık — sipariş öncesi teyit)
    "M3": dict(delik=4.22, C=4.20, E=6.35, T=1.5, kenar=4.8, kod={0: (0.8, 0.77), 1: (1.0, 0.97), 2: (1.4, 1.38)}),
    "M4": dict(delik=5.41, C=5.38, E=7.87, T=2.0, kenar=6.9, kod={0: (0.8, 0.77), 1: (1.0, 0.97), 2: (1.4, 1.38)}),
    "M5": dict(delik=6.40, C=6.38, E=8.89, T=2.0, kenar=7.1, kod={0: (0.8, 0.77), 1: (1.0, 0.97), 2: (1.4, 1.38)}),
    "M6": dict(delik=8.75, C=8.73, E=11.18, T=4.08, kenar=8.6, kod={1: (1.4, 1.38), 2: (2.3, 2.21)}),
    "M8": dict(delik=10.5, C=10.47, E=12.7, T=5.47, kenar=9.7, kod={1: (1.4, 1.38), 2: (2.3, 2.21)})}
PEM_SOMUN_TIP = {"S": "karbon çelik (304'te kullanılmaz)", "CLS": "303 paslanmaz · sac ≤ HRB 70 → 304 sacta TUTMAZ",
                 "SP": "A286 / sertleştirilmiş paslanmaz · sac ≤ HRB 90 (304 için)"}
PEM_SAPLAMA = {   # FH / FHS / FHP / FH4 (gömme başlı saplama, yaklaşık)
    "M3": dict(delik=3.0, H=4.8, h=0.8, kenar=5.6, min_sac=1.0), "M4": dict(delik=4.0, H=5.8, h=0.9, kenar=7.0, min_sac=1.0),
    "M5": dict(delik=5.0, H=6.9, h=1.0, kenar=7.2, min_sac=1.0), "M6": dict(delik=6.0, H=8.0, h=1.2, kenar=7.9, min_sac=1.3)}
PEM_SAPLAMA_TIP = {"FH": "karbon çelik", "FHS": "300 paslanmaz · sac ≤ HRB 70", "FHP": "A286 · sac ≤ HRB 92 (304 için, gıda servisi)", "FH4": "400 serisi (standartta yasak)"}
SAPLAMA_BOY = [6, 8, 10, 12, 15, 18, 20, 25, 30, 35]
PERCIN_SOMUN = {"M4": dict(delik=6.0, D=5.95, Dk=9.0, hk=0.8, L=10.0, kavrama=(0.5, 3.0)), "M5": dict(delik=7.0, D=6.95, Dk=10.0, hk=1.0, L=12.0, kavrama=(0.5, 3.0)),
                "M6": dict(delik=9.0, D=8.95, Dk=13.0, hk=1.5, L=15.0, kavrama=(0.5, 3.5)), "M8": dict(delik=11.0, D=10.95, Dk=15.0, hk=1.5, L=17.0, kavrama=(0.5, 3.5))}
KOR_PERCIN = {3.2: dict(delik=3.3, dk=6.5, k=1.1), 4.0: dict(delik=4.1, dk=8.0, k=1.5), 4.8: dict(delik=4.9, dk=9.5, k=1.7)}   # ISO 15983 A2/A2


def _bp(ad, sh, std, tanim, olcu, malzeme="A2-70", adet=1, birim="BAGLANTI", meta=None, uretim=False, mal="katalog"):
    return dict(ad=ad, wp=cq.Workplane("XY").add(sh), sh=sh, mal=mal, birim=birim, grup="SABIT", kaynak=SURUM, tur="baglanti",
                bom=(tanim, adet, olcu, "%s · %s" % (std, malzeme), "ÜRETİM" if uretim else "SATIN ALMA"),
                std=std, meta=dict(meta or {}, tur="baglanti", std=std, malzeme=malzeme))


def _altigen(s, h, z0=0.0):
    r = s / math.sqrt(3.0)
    return cq.Solid.extrudeLinear(cq.Wire.makePolygon([V(r * math.cos(math.radians(30 + 60 * i)), r * math.sin(math.radians(30 + 60 * i)), z0) for i in range(6)], close=True),
                                  [], V(0, 0, h))


def _silindir(r, h, z0=0.0):
    return cq.Solid.makeCylinder(r, h, V(0, 0, z0), V(0, 0, 1))


def _halka(r_dis, r_ic, h, z0=0.0):
    return _silindir(r_dis, h, z0).cut(_silindir(r_ic, h + 2, z0 - 1))


def _boy_sec(gerek, seri, pay=0.0):
    for L in seri:
        if L >= gerek + pay - 1e-9: return float(L)
    return float(seri[-1])


def vida(std, dis, boy, nokta, eksen, ad="vida", birim="BAGLANTI", malzeme="A2-70"):
    """nokta: baş oturma yüzeyi merkezi (havşada dış yüz) · eksen: uca doğru"""
    d = D_NOM[dis]; ds = d * 0.98
    if std in ("ISO7380", "ISO 7380-1"):
        dk, k, s = ISO7380[dis]
        prof = [V(0, 0, 0), V(dk / 2, 0, 0), V(dk / 2, 0, -0.15 * k), V(0.8 * dk / 2, 0, -0.65 * k), V(0.45 * dk / 2, 0, -0.93 * k), V(0, 0, -k)]
        bas = cq.Solid.revolve(cq.Wire.makePolygon(prof, close=True), [], 360.0, V(0, 0, 0), V(0, 0, 1)).cut(_altigen(s, 0.6 * k + 0.1, -k - 0.1))
        sh = bas.fuse(_silindir(ds / 2, boy)); ad_s = "ISO 7380-1"; tanim = "Bombe başlı imbus vida %s×%g" % (dis, boy)
    elif std in ("DIN7991", "ISO10642", "DIN 7991"):
        dk, k, s = DIN7991[dis]
        bas = cq.Solid.makeCone(dk / 2, ds / 2, k, V(0, 0, 0), V(0, 0, 1)).cut(_altigen(s, 0.6 * k, -0.01))
        sh = bas.fuse(_silindir(ds / 2, boy)); ad_s = "DIN 7991 / ISO 10642"; tanim = "Havşa başlı imbus vida %s×%g" % (dis, boy)
    elif std in ("ISO4762", "DIN912", "ISO 4762"):
        dk, k, s = ISO4762[dis]
        sh = _silindir(dk / 2, k, -k).cut(_altigen(s, 0.5 * k, -k - 0.01)).fuse(_silindir(ds / 2, boy)); ad_s = "ISO 4762"; tanim = "Silindir başlı imbus cıvata %s×%g" % (dis, boy)
    else:
        raise ValueError(std)
    return _bp(ad, _tasi(sh, _cerceve(nokta, eksen)), ad_s, tanim, "%s×%g" % (dis, boy), malzeme, birim=birim, meta=dict(dis=dis, boy=boy))


def somun(std, dis, nokta, eksen, ad="somun", birim="BAGLANTI", malzeme="A2"):
    """nokta: oturma yüzü merkezi · eksen: somunun uzandığı yön"""
    d = D_NOM[dis]
    if std == "ISO4032": s, m = ISO4032[dis]; ad_s, tn = "ISO 4032", "Altıgen somun %s" % dis
    elif std == "ISO10511": s, m = ISO10511[dis]; ad_s, tn = "ISO 10511", "Fiberli (naylon halkalı) somun %s" % dis
    elif std == "DIN1587": s, m = DIN1587[dis]; ad_s, tn = "DIN 1587", "Kör (kapalı) somun %s" % dis
    else: raise ValueError(std)
    sh = _altigen(s, m).cut(_silindir(d / 2, (m + 0.02) if std != "DIN1587" else 0.75 * m, -0.01))
    return _bp(ad, _tasi(sh, _cerceve(nokta, eksen)), ad_s, tn, "%s s%g m%g" % (dis, s, m), malzeme, birim=birim, meta=dict(dis=dis, s=s, m=m))


def pul(std, dis, nokta, eksen, ad="pul", birim="BAGLANTI", malzeme="A2"):
    d1, d2, h = (DIN125 if std == "DIN125" else DIN9021)[dis]
    ad_s = "DIN 125-A / ISO 7089" if std == "DIN125" else "DIN 9021 / ISO 7093"
    return _bp(ad, _tasi(_halka(d2 / 2, d1 / 2, h), _cerceve(nokta, eksen)), ad_s, "%s pul %s" % ("Düz" if std == "DIN125" else "Geniş", dis),
               "%g/%g×%g" % (d1, d2, h), malzeme, birim=birim, meta=dict(dis=dis, d1=d1, d2=d2, h=h))


def pem_somun(tip, dis, nokta, eksen, sac_t, ad="pem_somun", birim="BAGLANTI"):
    """PEM kendinden kenetli somun · nokta: gövdenin oturduğu sac yüzü merkezi · eksen: gövde tarafına (sacdan dışarı).
    Gövde yüzünün karşısı (sap ucu) sacla aynı düzlemde (flush) → karşı parça o yüze gelir."""
    c = dict(PEM_SOMUN[dis])
    if tip == "SP":
        dl, kn = STD.pem_delik("SP", dis)
        if dl: c["delik"] = float(dl)
        if kn: c["kenar"] = float(kn)
    kod = max((k for k, (ms, A) in c["kod"].items() if ms <= sac_t + 1e-9), default=None)
    if kod is None: raise ValueError("PEM %s-%s: sac %.2f < en küçük kod" % (tip, dis, sac_t))
    ms, A = c["kod"][kod]
    d = D_NOM[dis]
    sh = _silindir(c["delik"] / 2 - 0.01, A, -A).fuse(_silindir(c["E"] / 2, c["T"] - A, 0.0)).cut(_silindir(d / 2, c["T"] + 2, -A - 1))
    parca = "%s-%s-%d" % (tip, dis, kod)
    return _bp(ad, _tasi(sh, _cerceve(nokta, eksen)), "PEM %s" % parca, "PEM kendinden kenetli somun %s (%s)" % (parca, PEM_SOMUN_TIP.get(tip, "")),
               "delik Ø%.2f · gövde Ø%.2f × %.2f" % (c["delik"], c["E"], c["T"]), {"SP": "A286 pasive", "CLS": "303", "S": "çelik"}.get(tip, tip),
               birim=birim, meta=dict(dis=dis, pem_tip=tip, parca=parca, delik=c["delik"], kenar_min=c["kenar"], min_sac=ms, sap=A, T=c["T"])), c, ms


def pem_saplama(tip, dis, boy, nokta, eksen, ad="pem_saplama", birim="BAGLANTI", sac_ad=None):
    """PEM gömme başlı saplama · nokta: baş tarafındaki sac yüzü (flush) · eksen: saplamanın çıktığı yön.
    Baş sacın içinde (malzeme başın çevresine akar) → ic_ice izni sac_ad ile."""
    c = dict(PEM_SAPLAMA[dis])
    dl, kn = STD.pem_delik(tip, dis)
    if dl: c["delik"] = float(dl)
    if kn: c["kenar"] = float(kn)
    d = D_NOM[dis]
    sh = _silindir(c["H"] / 2, c["h"], 0.0).fuse(_silindir(d / 2 - 0.03, boy, 0.0))
    parca = "%s-%s-%g" % (tip, dis, boy)
    p = _bp(ad, _tasi(sh, _cerceve(nokta, eksen)), "PEM %s" % parca, "PEM gömme başlı saplama %s (%s)" % (parca, PEM_SAPLAMA_TIP.get(tip, "")),
            "delik Ø%.2f · %s×%g" % (c["delik"], dis, boy), {"FHP": "A286 pasive", "FHS": "300 paslanmaz", "FH4": "400 serisi", "FH": "çelik"}.get(tip, tip),
            birim=birim, meta=dict(dis=dis, pem_tip=tip, parca=parca, delik=c["delik"], kenar_min=c["kenar"], min_sac=c["min_sac"], boy=boy))
    if sac_ad: p["meta"]["ic_ice"] = [sac_ad]
    return p, c


def percin_somun(dis, kavrama, nokta, eksen, ad="percin_somun", birim="BAGLANTI", kapali=False):
    """perçin somun (rivnut) düz baş · nokta: baş tarafı sac yüzü · eksen: içeri (kör taraf) · kavrama = sac paketi kalınlığı"""
    c = dict(PERCIN_SOMUN[dis]); s = STD.percin_somun(dis)
    if s.get("delik"): c["delik"] = float(s["delik"]); c["D"] = float(s["delik"]) - 0.05
    if s.get("kavrama"): c["kavrama"] = tuple(s["kavrama"])
    d = D_NOM[dis]
    sh = _silindir(c["Dk"] / 2, c["hk"], -c["hk"]).fuse(_silindir(c["D"] / 2, kavrama, 0.0))
    sh = sh.fuse(_silindir(c["D"] / 2 + 1.2, 2.0, kavrama)).fuse(_silindir(c["D"] / 2, max(0.5, c["L"] - kavrama - 3.5), kavrama + 2.0))
    sh = sh.cut(_silindir(d / 2, c["L"] + 5, -c["hk"] - 1))
    return _bp(ad, _tasi(sh, _cerceve(nokta, eksen)), "perçin somun (üretici std., DIN yok)", "Perçin somun %s düz baş %s A2" % (dis, "kapalı uç" if kapali else "açık uç"),
               "delik Ø%.1f · kavrama %.2f (%g–%g)" % (c["delik"], kavrama, c["kavrama"][0], c["kavrama"][1]), "A2", birim=birim,
               meta=dict(dis=dis, delik=c["delik"], kavrama=kavrama, aralik=list(c["kavrama"]))), c


def kor_percin(cap, boy, nokta, eksen, ad="kor_percin", birim="BAGLANTI", kavrama=None):
    c = KOR_PERCIN[cap]
    sh = cq.Solid.makeCone(c["dk"] / 2, c["dk"] / 2 * 0.6, c["k"], V(0, 0, 0), V(0, 0, -1)).fuse(_silindir(cap / 2 - 0.03, boy, 0.0))
    if kavrama is not None: sh = sh.fuse(_silindir(cap / 2 * 1.35, 1.2, kavrama))
    return _bp(ad, _tasi(sh, _cerceve(nokta, eksen)), "ISO 15983", "Kör perçin Ø%g×%g bombe baş A2/A2" % (cap, boy), "delik Ø%.1f" % c["delik"], "A2/A2",
               birim=birim, meta=dict(cap=cap, boy=boy, delik=c["delik"]))


def kaynak_somunu(dis, nokta, eksen, ad="kaynak_somunu", birim="BAGLANTI"):
    s, m = DIN929[dis]
    sh = _altigen(s, m).cut(_silindir(D_NOM[dis] / 2, m + 2, -1))
    return _bp(ad, _tasi(sh, _cerceve(nokta, eksen)), "DIN 929", "Altıgen kaynak somunu %s" % dis, "s%g m%g" % (s, m), "A2 (1.4301)", birim=birim, meta=dict(dis=dis))


def kor_burc(dis, nokta, eksen, D=None, H=None, derinlik=None, ad="ayak_burcu", birim="AYAK"):
    """kaynaklı kör (kapalı uçlu) ayak burcu · nokta: kaynak yüzü (sac alt yüzü) · eksen: sacdan uzağa (aşağı)"""
    d = D_NOM[dis]; D = D or (30.0 if d >= 12 else 25.0); H = H or (30.0 if d >= 12 else 25.0); derinlik = derinlik or (H - 5.0)
    sh = _silindir(D / 2, H).cut(_silindir(d / 2, derinlik + 1, H - derinlik))
    return _bp(ad, _tasi(sh, _cerceve(nokta, eksen)), "özel imalat (torna)", "Kaynaklı kör ayak burcu %s · Ø%g × %g · kapalı uç" % (dis, D, H),
               "Ø%g × %g · diş derinliği %g" % (D, H, derinlik), "AISI 304", birim=birim, uretim=True, mal="paslanmaz", meta=dict(dis=dis, D=D, H=H, derinlik=derinlik))


def ayarli_ayak(dis, taban_noktasi, yukari, kot_burc_alt, ise=None, D_taban=60.0, ad="ayarli_ayak", birim="AYAK", kontra=True):
    """hijyenik ayarlı ayak (GN 20 sınıfı) · taban_noktasi: zemindeki ayak merkezi · kot_burc_alt: zeminden burç alt yüzüne · ise: burç içine diş boyu"""
    d = D_NOM[dis]; ise = ise or 1.5 * d + 2.0
    mil_ust = kot_burc_alt + ise
    sh = cq.Solid.makeCone(D_taban / 2, D_taban / 2 - 4.0, 12.0, V(0, 0, 0), V(0, 0, 1))
    sh = sh.fuse(_silindir(D_taban * 0.28, 10.0, 12.0)).fuse(_altigen(22.0 if d >= 12 else 17.0, 8.0, 22.0)).fuse(_silindir(d / 2 - 0.03, mil_ust - 30.0, 30.0))
    parts = [_bp(ad, _tasi(sh, _cerceve(taban_noktasi, yukari)), "GN 20 sınıfı (hijyenik)", "Ayarlı ayak %s · taban Ø%g · AISI 304 · dudak contalı" % (dis, D_taban),
                 "yükseklik %.0f · ayar ±20" % kot_burc_alt, "AISI 304", birim=birim, meta=dict(dis=dis, D=D_taban, statik_kN=16))]
    if kontra:
        s, m = ISO4032[dis]; ps = np.asarray(taban_noktasi, float) + _n(yukari) * (kot_burc_alt - m)
        parts.append(somun("ISO4032", dis, ps, yukari, ad=ad + "_kontra", birim=birim))
    return parts


def gizli_mentese(cerceve, x_mentese, x_yan, z_kol, z_plaka, kol_gen=12.0, yuk=50.0, govde=(16.0, 12.0), plaka=(3.0, 70.0), plaka_delik=(), ad="gizli_mentese", birim="KAPAK"):
    """gizli 180° kaldır-çıkar menteşe (Southco R6 sınıfı, ölçüler TEMSİLİ) — cerceve: X kapak kenarından içe, Y, Z kapaktan gövdeye (sağ elli);
    orijin kapak iç yüzü (arka) · kapak gövdesi Z 0 … −govde[1] (kapak cebinde) · kol Z 0 … z_kol · plaka yan iç yüzünde (X = x_yan) Z z_plaka aralığı ·
    plaka_delik: [(Y, Z, Ø)] plakadaki bağlantı delikleri (X yönünde)"""
    gw, gd = govde; tp, Lp = plaka
    def kutu(x0, x1, y0, y1, z0, z1): return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))
    sh = kutu(x_mentese - gw / 2, x_mentese + gw / 2, -yuk / 2, yuk / 2, -gd, 0.0)
    sh = sh.fuse(kutu(x_mentese - kol_gen / 2, x_mentese + kol_gen / 2, -yuk / 2 + 5, yuk / 2 - 5, -0.5, z_kol))
    sh = sh.fuse(kutu(x_yan, x_mentese + kol_gen / 2, -yuk / 2 + 5, yuk / 2 - 5, z_kol - 10.0, z_kol))
    sh = sh.fuse(kutu(x_yan, x_yan + tp, -yuk / 2 - 10, yuk / 2 + 10, z_plaka[0], z_plaka[1]))
    for yy, zz, cp in plaka_delik:
        sh = sh.cut(cq.Solid.makeCylinder(cp / 2.0, tp + 2.0, V(x_yan - 1.0, yy, zz), V(1, 0, 0)))
    return _bp(ad, _tasi(sh.clean(), cerceve), "Southco R6 sınıfı", "Gizli 180° kaldır-çıkar menteşe AISI 304 pasive (ölçüler temsili, katalogdan)",
               "gövde %g×%g×%g · plaka %g×%g" % (gw, yuk, gd, tp, Lp), "AISI 304", birim=birim, meta=dict(kaldir_cikar=True, aci=180))


def piyano_mentese(cerceve, boy, kanat=20.0, kalinlik=1.0, d_mafsal=4.0, aci=180.0, delik_aralik=50.0, ad="piyano_mentese", birim="KAPAK"):
    """DIN 7954 piyano menteşe · cerceve: Z mafsal ekseni (boy), kanat 1 +X, kanat 2 X'ten aci° dönmüş"""
    k1 = cq.Solid.makeBox(kanat, kalinlik, boy, V(0, -kalinlik / 2, 0))
    k2 = k1.rotate(V(0, 0, 0), V(0, 0, 1), aci)
    sh = k1.fuse(k2).fuse(_silindir(d_mafsal / 2, boy))
    for z in np.arange(delik_aralik / 2, boy, delik_aralik):
        for kk in (0.0, aci):
            c = cq.Solid.makeCylinder(2.1, 4.0, V(kanat * 0.6, -2.0, z), V(0, 1, 0)).rotate(V(0, 0, 0), V(0, 0, 1), kk)
            sh = sh.cut(c)
    return _bp(ad, _tasi(sh, cerceve), "DIN 7954", "Piyano menteşe AISI 304 %g×%g×%g" % (2 * kanat, kalinlik, boy), "kanat %g · mafsal Ø%g" % (kanat, d_mafsal), "AISI 304",
               birim=birim, meta=dict(boy=boy))


# =====================================================================================================================================
# 11 · BİRLEŞİM YARDIMCILARI
# =====================================================================================================================================
def _yigin(A, B, nokta):
    """A ve B panellerinin eksen boyunca konumu: d (A → B), A dış yüzünden uzaklıklar (a1 = tA, b0, b1)"""
    nA = A.normal()
    if abs(abs(np.dot(nA, B.normal())) - 1.0) > 1e-6: raise ValueError("birleşim: paneller paralel değil (%s / %s)" % (A.ad, B.ad))
    ya = A.yerel(nokta); pA0 = A.dunya(ya[0], ya[1], 0.0); tA, tB = A.sac.t, B.sac.t
    yb = B.yerel(nokta)
    sb = sorted(float(np.dot(B.dunya(yb[0], yb[1], z) - pA0, nA)) for z in (0.0, tB))
    if sb[0] >= tA - 1e-6: d, dis0 = nA, pA0
    elif sb[1] <= 1e-6: d, dis0 = -nA, A.dunya(ya[0], ya[1], tA); sb = sorted(tA - s for s in sb)
    else: raise ValueError("birleşim: %s ile %s iç içe" % (A.ad, B.ad))
    return d, dis0, tA, sb[0], sb[1]


def vidali_birlesim(A, B, nokta, tip="pem_somun", dis="M5", vida_std="ISO7380", pul_std=None, somun_std="ISO10511", pem_tip=None, boy=None, ad="baglanti", birim="BAGLANTI"):
    """iki paralel sac arası vidalı birleşim — delik + PEM/somun + vida AYNI EKSENDE otomatik.
    A: baş tarafındaki panel (vida başı / saplama başı / perçin başı) · B: karşı panel.
      pem_somun : A'da ISO 273 geçiş deliği, B'de PEM SP somun (gövde B'nin uzak yüzünde), vida A dışından
      pem_saplama: A'da PEM FHP gömme saplama (baş A dış yüzünde flush), B'de geçiş deliği, B uzak yüzünde pul + somun
      percin_somun: iki sacı birlikte kavrayan perçin somun (A dışından takılır)
      somun     : iki geçiş deliği, vida + pul + somun · kor_percin: iki delik, kör perçin"""
    d, dis0, tA, b0, b1 = _yigin(A, B, nokta)
    P = lambda x: dis0 + d * x
    ua = A.yerel(dis0); ub = B.yerel(P(b0 + 1e-9))
    for pan, uu in ((A, ua), (B, ub)):
        if not pan.icerir(uu[0], uu[1]): raise ValueError("birleşim noktası %s düz bölgesinde değil" % pan.ad)
    parcalar, delikler = [], []
    def dl(pan, uu, cap, tp, **m):
        pan.delik(uu[0], uu[1], cap, tip=tp, **m); delikler.append(dict(sac=pan.sac.ad, panel=pan.ad, cap=round(cap, 3), tip=tp, merkez=[round(c, 4) for c in pan.dunya(uu[0], uu[1], 0.0)]))
    gecis = STD.delik_iso273(dis)
    if tip == "pem_somun":
        pt = pem_tip or "SP"
        ps, c, ms = pem_somun(pt, dis, P(b1), d, B.sac.t, ad=ad + "_pem", birim=birim)
        dl(A, ua, gecis, "vida_deligi", parca="ISO 273 orta")
        dl(B, ub, c["delik"], "pem_somun", parca=ps["meta"]["parca"], pem_tip=pt, kenar_min=c["kenar"], min_sac=ms)
        hp = DIN9021[dis][2] if pul_std else 0.0
        gerek = b1 - ps["meta"]["sap"] + ps["meta"]["T"] + hp
        L = boy or _boy_sec(gerek, [x for x in VIDA_BOY if x >= 1.2 * D_NOM[dis]])        # katalogda en kısa ≈ 1,2d
        if pul_std: parcalar.append(pul(pul_std, dis, P(-hp), d, ad=ad + "_pul", birim=birim))
        parcalar += [vida(vida_std, dis, L, P(-hp), d, ad=ad + "_vida", birim=birim), ps]
    elif tip == "pem_saplama":
        pt = pem_tip or "FHP"
        dl(B, ub, gecis, "vida_deligi", parca="ISO 273 orta")
        pu = pul(pul_std or "DIN9021", dis, P(b1), d, ad=ad + "_pul", birim=birim)
        so_s, so_m = (ISO10511 if somun_std == "ISO10511" else ISO4032)[dis]
        gerek = b1 + pu["meta"]["h"] + so_m + 1.5
        L = boy or _boy_sec(gerek, SAPLAMA_BOY)
        sp, c = pem_saplama(pt, dis, L, P(0.0), d, ad=ad + "_saplama", birim=birim, sac_ad=A.sac.ad)
        dl(A, ua, c["delik"], "pem_saplama", parca=sp["meta"]["parca"], pem_tip=pt, kenar_min=c["kenar"], min_sac=c["min_sac"])
        parcalar += [sp, pu, somun(somun_std, dis, P(b1 + pu["meta"]["h"]), d, ad=ad + "_somun", birim=birim)]
    elif tip == "percin_somun":
        rs, c = percin_somun(dis, b1, P(0.0), d, ad=ad + "_percin_somun", birim=birim)
        if not (c["kavrama"][0] - 1e-9 <= b1 <= c["kavrama"][1] + 1e-9): raise ValueError("perçin somun kavrama %.2f ∉ %s" % (b1, c["kavrama"]))
        dl(A, ua, c["delik"], "percin_somun", parca="perçin somun %s" % dis); dl(B, ub, c["delik"], "percin_somun", parca="perçin somun %s" % dis)
        parcalar.append(rs)
    elif tip == "somun":
        dl(A, ua, gecis, "vida_deligi"); dl(B, ub, gecis, "vida_deligi")
        h1 = DIN125[dis][2]; so_s, so_m = (ISO10511 if somun_std == "ISO10511" else ISO4032)[dis]
        L = boy or _boy_sec(b1 + 2 * h1 + so_m + 1.5, VIDA_BOY)
        parcalar += [pul("DIN125", dis, P(-h1), d, ad=ad + "_pul1", birim=birim), vida(vida_std, dis, L, P(-h1), d, ad=ad + "_vida", birim=birim),
                     pul("DIN125", dis, P(b1), d, ad=ad + "_pul2", birim=birim), somun(somun_std, dis, P(b1 + h1), d, ad=ad + "_somun", birim=birim)]
    elif tip == "kor_percin":
        cap = float(dis) if not isinstance(dis, str) else 4.0
        c = KOR_PERCIN[cap]
        dl(A, ua, c["delik"], "kor_percin"); dl(B, ub, c["delik"], "kor_percin")
        L = boy or _boy_sec(b1 + 1.5 * cap, [6, 8, 10, 12, 14, 16, 18, 20])
        parcalar.append(kor_percin(cap, L, P(0.0), d, ad=ad + "_percin", birim=birim, kavrama=b1))
    else:
        raise ValueError(tip)
    # eş eksen doğrulaması: deliklerin merkezleri ve elemanların eksenleri aynı doğru üzerinde
    ek = [np.asarray(x["merkez"]) for x in delikler]
    sap = max(float(np.linalg.norm((q - dis0) - np.dot(q - dis0, d) * d)) for q in ek)
    return dict(ad=ad, tip=tip, dis=dis, eksen=[round(float(c), 6) for c in d], nokta=[round(float(c), 4) for c in dis0], aralik=round(b0 - tA, 4),
                paket=round(b1, 4), parcalar=parcalar, delikler=delikler, es_eksen_sapma_mm=round(sap, 6), sac=[A.sac.ad, B.sac.ad])


def saplama_baglantisi(A, nokta, yon, paket, dis="M5", pem_tip="FHP", pul_std="DIN9021", somun_std="ISO10511", ad="saplama", birim="BAGLANTI"):
    """A sacına gömme başlı PEM saplama (baş A'nın 'yon'a ters yüzünde flush) · saplama 'yon' tarafındaki sac-dışı parçadan
    (A'nın yon tarafı yüzünden itibaren 'paket' kalınlığı: araç / menteşe plakası / braket) geçer · uzak yüzde pul + somun · saplama boyu otomatik"""
    d = _n(yon); nA = A.normal(); tA = A.sac.t
    if abs(abs(np.dot(d, nA)) - 1.0) > 1e-6: raise ValueError("saplama: yön sac normaline paralel değil")
    ya = A.yerel(nokta); P0 = A.dunya(ya[0], ya[1], 0.0 if np.dot(d, nA) > 0 else tA)
    if not A.icerir(ya[0], ya[1]): raise ValueError("saplama noktası %s düz bölgesinde değil" % A.ad)
    b1 = tA + paket
    pu = pul(pul_std, dis, P0 + d * b1, d, ad=ad + "_pul", birim=birim)
    so_m = (ISO10511 if somun_std == "ISO10511" else ISO4032)[dis][1]
    L = _boy_sec(b1 + pu["meta"]["h"] + so_m + 1.5, SAPLAMA_BOY)
    sp, c = pem_saplama(pem_tip, dis, L, P0, d, ad=ad + "_saplama", birim=birim, sac_ad=A.sac.ad)
    A.delik(ya[0], ya[1], c["delik"], tip="pem_saplama", parca=sp["meta"]["parca"], pem_tip=pem_tip, kenar_min=c["kenar"], min_sac=c["min_sac"])
    so = somun(somun_std, dis, P0 + d * (b1 + pu["meta"]["h"]), d, ad=ad + "_somun", birim=birim)
    return dict(ad=ad, tip="pem_saplama_paket", dis=dis, paket=paket, eksen=[round(float(c_), 6) for c_ in d], nokta=[round(float(c_), 4) for c_ in P0],
                parcalar=[sp, pu, so], delikler=[dict(sac=A.sac.ad, panel=A.ad, cap=c["delik"], tip="pem_saplama")], es_eksen_sapma_mm=0.0, sac=[A.sac.ad])


def dil_yuva(dil_paneli, kenar, w0, en, yuva_paneli, bosluk=0.1, cikinti=0.0):
    """geçme dil + yuva: dil_paneli kenarından düzlem içinde çıkan dil, yuva_paneline açılan yuvadan geçer (dil boyu ve yuva konumu otomatik)"""
    kn = dil_paneli.kenar(kenar); t = dil_paneli.sac.t
    ws = w0 + en / 2.0
    p_orta = dil_paneli.dunya(*(kn["p0"] + kn["e2"] * ws), z=t / 2.0)
    out3 = dil_paneli.M[:3, :3] @ np.r_[kn["out2"], 0.0]
    ny = yuva_paneli.normal()
    if abs(np.dot(out3, ny)) < 0.5: raise ValueError("dil_yuva: dil yuva sacına dik değil")
    ss = []
    for z in (0.0, yuva_paneli.sac.t):
        q = yuva_paneli.dunya(0, 0, z); ss.append(float(np.dot(q - p_orta, ny) / np.dot(out3, ny)))
    yak, uz = sorted(ss)
    if yak < -1e-6: raise ValueError("dil_yuva: yuva sacı kenarın gerisinde")
    boy = uz + cikinti
    dil_paneli.dil(kenar, w0, en, boy)
    merkez = p_orta + out3 * (yak + uz) / 2.0
    uv = yuva_paneli.yerel(merkez)
    e3 = dil_paneli.M[:3, :3] @ np.r_[kn["e2"], 0.0]
    ey = yuva_paneli.M[:3, :3].T @ e3
    aci = math.degrees(math.atan2(ey[1], ey[0]))
    yuva_paneli.dikdortgen(uv[0], uv[1], en + 2 * bosluk, t + 2 * bosluk, aci, tip="yuva", parca="dil-yuva", dil=dil_paneli.ad)
    return dict(dil=dil_paneli.ad, yuva=yuva_paneli.ad, en=en, boy=round(boy, 3), yuva_olcu=[round(en + 2 * bosluk, 3), round(t + 2 * bosluk, 3)],
                merkez=[round(float(c), 3) for c in merkez])


# =====================================================================================================================================
# 12 · MONTAJ UYUMU + ÇIKTI
# =====================================================================================================================================
def _sekil(p):
    if p.get("sh") is not None: return p["sh"]
    w = p["wp"]; vs = w.vals()
    return vs[0] if len(vs) == 1 else cq.Compound.makeCompound(vs)


def parca_kutusu_satiri(p, saydam=0):
    """parca_kutulari.json satırı: [ad, saydam, xmin, xmax, ymin, ymax, zmin, zmax]"""
    b = _sekil(p).BoundingBox()
    return [p["ad"], saydam] + [round(v, 1) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]


def cakisma_denetle(parcalar, esik=0.5):
    """parçalar arası kesişim hacmi > esik (mm³) · meta['ic_ice'] izinli çiftler (PEM gömme başı)"""
    ss = [(p["ad"], _sekil(p), p.get("meta", {}).get("ic_ice", [])) for p in parcalar]
    bb = [s.BoundingBox() for _a, s, _i in ss]
    out, izinli = [], []
    for i in range(len(ss)):
        for j in range(i + 1, len(ss)):
            if not _bb_kesisir(bb[i], bb[j], -1e-4): continue
            try:
                v = ss[i][1].intersect(ss[j][1]).Volume()
            except Exception:
                v = -1.0
            if v > esik or v < 0:
                if ss[j][0] in ss[i][2] or ss[i][0] in ss[j][2]: izinli.append((ss[i][0], ss[j][0], round(v, 3)))
                else: out.append((ss[i][0], ss[j][0], round(v, 3)))
    return out, izinli


_RENK = {"sac": ((0.78, 0.80, 0.83, 1.0), 0.85, 0.32), "baglanti": ((0.36, 0.40, 0.46, 1.0), 0.6, 0.4), "kaynak": ((0.80, 0.55, 0.25, 1.0), 0.4, 0.5),
         "ayak": ((0.55, 0.58, 0.62, 1.0), 0.7, 0.35)}


def glb_yaz(yol, parcalar, tol=0.05, aci=0.25):
    """parça başına düğüm · metre · y yukarı · extras: parçanın 'sac' / 'meta' sözlüğü + bom"""
    blob, views, accs, meshes, nodes, mats, mi = [], [], [], [], [], [], {}
    off = [0]
    def gomu(bt, hedef=None):
        while off[0] % 4: blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef: v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt)
        return len(views) - 1
    for p in parcalar:
        tur = p.get("tur", "sac")
        if tur not in mi:
            r, m, rg = _RENK.get(tur, _RENK["sac"])
            mi[tur] = len(mats); mats.append({"name": tur, "pbrMetallicRoughness": {"baseColorFactor": list(r), "metallicFactor": m, "roughnessFactor": rg}, "doubleSided": True})
        vs, tris = _sekil(p).tessellate(tol, aci)
        P = np.array([[v.x, v.y, v.z] for v in vs], float) * 0.001; I = np.array(tris, np.uint32).reshape(-1, 3)
        N = np.zeros_like(P)
        fn = np.cross(P[I[:, 1]] - P[I[:, 0]], P[I[:, 2]] - P[I[:, 0]])
        for k in range(3): np.add.at(N, I[:, k], fn)
        N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)
        vp = gomu(P.astype("<f4").tobytes(), 34962); vn = gomu(N.astype("<f4").tobytes(), 34962); vi = gomu(I.astype("<u4").tobytes(), 34963)
        accs += [{"bufferView": vp, "componentType": 5126, "count": len(P), "type": "VEC3", "min": P.min(0).tolist(), "max": P.max(0).tolist()},
                 {"bufferView": vn, "componentType": 5126, "count": len(N), "type": "VEC3"},
                 {"bufferView": vi, "componentType": 5125, "count": int(I.size), "type": "SCALAR"}]
        meshes.append({"name": p["ad"], "primitives": [{"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": mi[tur]}]})
        ex = {"bom": list(p.get("bom", ())), "birim": p.get("birim"), "tur": tur}
        if p.get("sac"): ex["sac"] = p["sac"]
        if p.get("meta"): ex["meta"] = p["meta"]
        nodes.append({"mesh": len(meshes) - 1, "name": p["ad"], "extras": json.loads(json.dumps(ex, ensure_ascii=False, default=str))})
    while off[0] % 4: blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    g = {"asset": {"version": "2.0", "generator": SURUM}, "scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes, "meshes": meshes,
         "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}]}
    js = json.dumps(g, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    while len(js) % 4: js += b" "
    with open(yol, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + 8 + len(bb)))
        f.write(struct.pack("<II", len(js), 0x4E4F534A)); f.write(js)
        f.write(struct.pack("<II", len(bb), 0x004E4942)); f.write(bb)
    return dict(yol=yol, dugum=len(nodes), bayt=12 + 16 + len(js) + len(bb))


def bom_topla(parcalar):
    """aynı tanım + ölçü + standart satırlarını toplar"""
    t = {}
    for p in parcalar:
        b = p.get("bom")
        if not b: continue
        k = (b[0], b[2], b[3], b[4])
        t[k] = t.get(k, 0) + b[1]
    return [dict(tanim=k[0], olcu=k[1], standart=k[2], tedarik=k[3], adet=v) for k, v in sorted(t.items(), key=lambda kv: (kv[0][3], kv[0][0]))]
