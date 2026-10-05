# -*- coding: utf-8 -*-
"""HAT VERSİYON 2 · E KUTU KATLAMA ADAPTÖRÜ v1 (30 Eyl 2026 · Claude · YEREL) — montajda 'import kutu_cad_v14 as KC' yerine 'import h2_kutu_v1 as KC'.
kutu_cad_v14 YENİDEN ÇİZİLMEZ ve DEĞİŞMEZ: bütün sabitler / kinematik işlevler (quat, blank_acilar, DUGUM, CORNER, uygula, grup_matrisi, blank_dunya …)
buradan AYNEN yayımlanır; yalnız PARÇA LİSTESİ (PARCALAR) v2 için yeniden kurulur. kutu_cad_v14.PARCALAR v1 olarak kalır (kendi denetim işlevleri tutarlı).

v1 → v2 (h2_hesap_v1: "Secop NLE8.8CN + B panosu → E'nin altı · içecek yedeği yukarı çıkınca boşalan 803,5 × 462 × 379"):
  ÇIKAN   icecek_* (6 koli + PE-HD altlık = 7 parça) → içecek yedeği makinenin üstündeki U_KE deposuna (h2_ust_depo_v1)
  DEĞİŞEN onyuz_alt_kanat_sol / _sag (bu listedeki kopyası): lazer panjur yarıkları 2 × 27 × (145 × 8) — SOL kanat EMİŞ, SAĞ kanat ATIŞ ·
          sol_sac_pizza_penceresi (kopyası): Ø16 gider geçiş deliği (y ≈ 162 · z −760) · kutu_cad_v14'teki asılları DOKUNULMADI
  YENİ    ealt_secop_*  store_cad_v14 K4'ünden alınan Secop CU NLE8.8CN R290 ünitesi (taban + kondenser + fan + kompresör + 4 ped + 2 montaj rayı +
                        kondenser çevre contası + taban contası) y ekseni etrafında 90° döndürülüp E'nin alt önüne · buharlaştırma tavası (E ölçüsünde
                        yeniden) + SICAK GAZ SERPANTİNİ (tavayı ısıtır — hesap aşağıda)
          ealt_pano_*   store_cad_v14 B_ELEKTRIK'in 32 parçası (pano plakası, 2 DIN rayı, S7-1200 + 4 modül, NDR-240, EM-324C, 21 röle, klemens) sol yan saca
                        (emiş tarafında) 90° döndürülerek · + 4 mesafe burcu
          ealt_perde_*  BÖLME: arka perde · tavan · Z biçimli AYIRICI (sabit üst bant + sökülür Z) · kapak iç yüzüne basan EPDM şeritler · taban yanı contaları
          ealt_gider_*  B evaporatör gider hattının devamı: dünya (4000, 170, −760) Ø20 → eksantrik redüksiyon → Ø12 · K'nın alt arkasından (tartı / tava
                        üstünden) · E'de şarjör altından · kapı eşiğinin çatal yarığından (asansör arabasının altından) · arka perde → tava · her yerde ≥ %1
HAVA YOLU (Secop föyü 551 m³/h): SOL kanat panjuru (EMİŞ) → sol bölme (pano + tava: SERİN taraf) → kondenser (dış yüzü x 250, −x'e bakar) → fan → kompresör
  → SAĞ bölme → SAĞ kanat panjuru (ATIŞ). Ayırıcı kondenserin conta düzleminden (x 305) Z çizerek iki kanadın derzinin (x 416) arkasına gelir: iki kanat eşit
  ve simetrik yarıklı, sol yalnız emer, sağ yalnız atar. İç kısa devre yolu yok: ayırıcı + kondenser çevre contası + taban contası + arka perde + tavan + EPDM şeritler.
B'DEN ALINMAYANLAR (gerekçeli, B_ALINMAYAN): K4 emiş şeridi yan sacları / yan contaları / ön kapamaları — B'de kondenser ARKADAN (plenum + iki yan şerit)
  emiyordu; E'de emiş ÖNDEN, ayrım tek enine ayırıcıyla (ealt_perde_*) — o saclar E'de hiçbir şeyi ayırmaz, yalnız atış yolunu daraltırdı ·
  gider kelepçeleri (B'nin K4 şeritleri yok; B içi gider hattı başka asistanda) · ikinci çek valf (artık TEK gider) · ara raf / perde / kapak / klipsler (görev dışı).
KOORDİNAT: E yereli (kutu_cad_v14 ile aynı) — x 0…830 (dünya = x + 4400) · y yerden · z ön +79 / arka −830. Gider hattının K içindeki kısmı x −400…0.
MONTAJ: import h2_kutu_v1 as KC · E_BIRIM'den E_ICECEK_YEDEK satırı KALKAR (öneki artık hiçbir parçaya uymaz → boş zarf) + KC.E_ALT_BIRIM eklenir ·
  KS.modul()'den sonra KC.K_DUVAR_DELIKLERI K parçalarına kesilir (K'nın iki yan sacında gider deliği) · içecek sözleşmesi / kapasitesi h2_ust_depo_v1'e.
  kutu_cad_v14'ün PARCALAR kullanan kendi araçları (olcum_v7, cakisma, glb_yaz, bom_yaz …) v1 listesini görür; montajın kullandığı kinematik aynıdır.
AÇIK: (1) B gider çıkışı y 170 → %1 inişle K'nın sağ taban taşıyıcısını (üst y 156) 0,55 mm ile geçer — B çıkışı ≥ y 172,5 (3 mm) olmalı (GIDER_GIRIS değişince
  hat kendiliğinden yeniden kurulur) · (2) Ø20 → Ø12: asansör arabasının altından (7,1 mm) eşik çatal yarığından geçmek ve tavaya 21 mm yükseklik bırakmak için ·
  (3) sıcak gaz serpantini Secop basma hattına OEM değişikliği (onay) · (4) soğutma hatları + B pano kabloları E → K → B modellenmedi (SOGUTMA_HAT_ACIK) ·
  (5) Secop servis vanası yeri VARSAYIM (föy).
Çalıştır (öz denetim): python ob_calistir.py h2/h2_kutu_v1.py
"""
import math, os, sys, time, importlib.util as _ilu

H2 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H2)
for _p in (_U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h2_hesap_v1 as HS
import kutu_cad_v14 as E14

# ================================================================ kutu_cad_v14'ün HER ŞEYİ (sabitler + işlevler) aynen ================================================================
for _k, _v in list(vars(E14).items()):
    if _k.startswith("__") and _k.endswith("__"):
        continue
    globals()[_k] = _v

V = cq.Vector
PARCALAR = []                      # v2 parça listesi (kimliği korunur: PARCALAR[:] = …) · E14.PARCALAR v1 olarak kalır
DEGISEN, CIKAN, YENI = [], [], []  # modul() doldurur (denetim + montaj bilgisi)
X_E, X_K = HS.E_X[0], HS.K_X[0]    # 4400 · 4000
DX_K = X_K - X_E                   # −400: K yereli → E yereli

# ================================================================ İÇECEK YEDEĞİ: E'DE YOK (v2) ================================================================
ICECEK_YEDEK = dict(x=(0.0, 0.0), y=(0.0, 0.0), z=(0.0, 0.0), koli=0, kutu=0,
                    tasindi="h2_ust_depo_v1.ICECEK_YEDEK (U_KE üst deposu, y 1862–2200 · 6 koli = 144)")


def icecek_on_olcum():
    """v2 · E'de içecek yedeği YOK (6 koli U_KE üst deposunda — h2_ust_depo_v1). Dönüş biçimi v6'daki ile aynı (montajın assert'i geçer: önde engel yok,
    çünkü çekilecek koli yok) — ÖLÇÜM DEĞİL, BEYAN: net = (0, 0), sütunlar boş. Montaj E_ICECEK_YEDEK birimini ve bu metni kaldırmalı."""
    return dict(on=[], net=(0.0, 0.0), sutun=[dict(x=None, engel=[], bindirme=0.0), dict(x=None, engel=[], bindirme=0.0)],
                sag_bos=0.0, ara=0.0, icecek_yok=True, tasindi=ICECEK_YEDEK["tasindi"])


# ================================================================ ÖLÇÜLER (E yereli) ================================================================
Y_TABAN_UST = Y_PLINT + 3.0                    # 126 · taban_sac_3 üstü
Z_PERDE_ARKA = (-350.0, -349.0)                # arka perde 304 1,0 · asansör motor plakası (−351) ile 1 mm
Y_TAVAN_P = (513.5, 515.0)                     # bölme tavanı 304 1,5 · sol dikme lamı (≤ 520) ve kanat menteşelerinin (≥ 530) altında
Z_CONTA = (57.0, Z_PANEL)                      # kanat iç sacına (z 59) basan EPDM şeritler 57…59
X_AYIRICI = (305.0, 306.5)                     # ayırıcının kondenser düzlemindeki kolu (conta düzlemi x 300–310 içinde)
Z_AYIRICI_ORTA = (16.0, 17.0)                  # Z'nin orta kolu (ünite önünün 10 önü)
X_DERZ_ORTA = (X_ORTA_DERZ[0] + X_ORTA_DERZ[1]) / 2.0     # 416 · iki kanat arası derzin ortası
X_AYIRICI_ON = (X_DERZ_ORTA - 0.75, X_DERZ_ORTA + 0.75)  # Z'nin ön kolu derzin arkasında
# Secop: store_cad_v14 dünya → E yereli: y ekseni etrafında +90° [(x, y, z) → (z, y, −x)] + öteleme
#   kondenser (B z −554…−494) → x 250–310 (DIŞ yüzü x 250, −x'e bakar = emiş sol bölmeden) · ünite z −344…+6 (arka perdeye 5, B'deki SECOP_BOS gibi)
SECOP_T = (804.0, Y_TABAN_UST - 124.5, 2094.75)
RAY_Z = (-348.0, 40.0)                         # montaj rayları arka perde → taban önündeki dayama dudağının (z 45) 5 gerisi
# Pano: B_ELEKTRIK aynı dönüşle → plaka sol yan sacın iç yüzünde (x 1,5) 2,5 mesafe burcuyla x 4–6 · cihazlar +x'e (≤ 127) · z −347…+33 · y 197,5–463,5
PANO_T = (794.0, 65.5, 2070.5)
PANO_BURC = dict(r=6.0, y=(204.5, 456.5), z=(-340.0, 15.0))   # ön burçlar z 15: sol dikme lamının (z ≥ 29) gerisinde
# buharlaştırma tavası (E ölçüsü) + sıcak gaz serpantini
TAVA_E = (135.0, 240.0, Y_TABAN_UST, 147.0, -346.0, 43.0)       # 105 × 21 × 389 · pano (x ≤ 127) ile montaj rayının dikey kolu (x 242) arasında
TAVA_T = 1.5
SG = dict(r=4.0, x=(150.0, 172.0, 194.0, 216.0), z=(-330.0, 25.0), cikis=((150.0, 200.0), (216.0, 180.0)))   # Cu Ø8 · 4 kol · iki ucu kondenser yüzüne
# panjurlar (lazer yarık · B K4 paneli ile aynı yarık: 145 × 8, köprü 5 / 8)
PANJUR = dict(w=145.0, h=8.0, kopru_y=5.0, kopru_x=8.0, y0=150.0, n=27)
# gider hattı
GIDER_GIRIS = (X_K - X_E, 170.0, -760.0)       # dünya (4000, 170, −760) · Ø20 boru ekseni (başka asistan getirir: B'nin sağ dış sacı)
GIDER_EGIM = 0.010
R20, T20, R12, T12 = 10.0, 1.5, 6.0, 1.0       # Ø20 × 1,5 PVC (VARSAYIM: 20 dış çap) · Ø12 × 1 PVC (B'nin gider boruları gibi)
GIDER_PLAN = [(-400.0, -760.0), (-360.0, -760.0), (-340.0, -760.0), (206.0, -760.0), (206.0, -393.0), (190.0, -393.0), (190.0, -330.0)]
#            K sol sacı · Ø20 sonu · redüksiyon sonu · şarjör altında x → eşik yarığı (x 188–222) hizası · +z eşikten · ray plakasının (x ≥ 200) soluna · arka perde → tava
VALF_L = 10.0                                  # ördek gagası (Minivalve DU 120.001 · Ø14 × 10 — store_cad_v14 gider_cek_valfi_sol)
KELEPCE = ((0, 100.0), (1, -640.0), (1, -480.0))   # (koşu: 0 = x boyunca z −760 · 1 = x 206'da z boyunca, konum)
KUCUK_PAY = 3.0                                # gider ↔ komşu parça en küçük aralık hedefi (mm)
# bilgi: B evaporatörleri (dünya, görev tanımı) — soğutma hattı tahmini
EVAP = dict(sol=(1465.0, 1825.0), sag=(2775.0, 3135.0), z=(-752.0, -667.0), y=(215.0, 650.0))
SECOP_VANA_E = (330.0, 175.0, -330.0)          # Secop servis vanaları (E yereli · VARSAYIM: kondenser ucunda arka yanda — föyden teyit)
B_K4_X = (2027.5, 2500.0)

# ---- store_cad_v14'ten alınacaklar (K4 · B_SOGUTMA) ----
B_AL = ("sogutma_grubu_montaj_rayi_arka", "sogutma_grubu_montaj_rayi_on", "sogutma_grubu_takozu_0", "sogutma_grubu_takozu_1", "sogutma_grubu_takozu_2",
        "sogutma_grubu_takozu_3", "sogutma_grubu_taban", "sogutma_grubu_taban_contasi", "sogutma_grubu_kondenser", "sogutma_grubu_fan",
        "sogutma_grubu_kompresor", "k4_kondenser_contasi")
B_YENIDEN = {"buharlastirma_tavasi": "E ölçüsünde yeniden kuruldu (B'nin 465 × 115'i E'nin alt bölmesine sığmaz; gider kotu 21 mm yükseklik bırakır)",
             "gider_cek_valfi_sol": "tek gider hattının ucunda, yatay (ealt_gider_cek_valfi)"}
B_ALINMAYAN = {"k4_emis_yan_sac_sol": "B'nin arkadan emiş şeridi sacı — E'de emiş önden, ayrım enine ayırıcıyla (ealt_perde_ayirici_*)",
               "k4_emis_yan_sac_sag": "aynı", "k4_emis_yan_conta_sol": "aynı (yerine ealt_perde_conta_taban_yani_*)", "k4_emis_yan_conta_sag": "aynı",
               "k4_emis_on_kapama_sol": "B şeridinin ön kapaması — E'de şerit yok", "k4_emis_on_kapama_sag": "aynı",
               "gider_kelepcesi_sol_1": "B'nin K4 şeridindeki gider kelepçesi — K4 kalktı, B içi gider başka asistanda", "gider_kelepcesi_sol_2": "aynı",
               "gider_kelepcesi_sag_0": "aynı", "gider_kelepcesi_sag_1": "aynı", "gider_cek_valfi_sag": "ikinci gider yok (B tek Ø20 getirir)",
               "k4_ara_sac_alt": "ara raf (görev: alınmaz)", "k4_ara_pu": "ara raf", "k4_ara_sac_ust": "ara raf", "k4_ara_perde": "K4 bölme perdesi (görev: alınmaz)"}
B_YOK_SAYILAN = ("k4_kapak_sogutma_dis_sac", "k4_panel_klipsi_")      # K4 kapağı / klipsleri (zaten x aralığının dışına taşar)

E_ALT_BIRIM = [
    ("E_ALT_SOGUTMA", "B soğutması E'nin altında (v2): Secop CU NLE8.8CN R290 (K4'ten, 90° döndürülmüş, kondenser −x'e) + 4 ped + 2 L 40×40×3 montaj rayı + "
                      "kondenser çevre / taban contaları · buharlaştırma tavası 105 × 389 × 21 + sıcak gaz serpantini (Cu Ø8) · BÖLME: arka perde + tavan + "
                      "Z ayırıcı (sol kanat EMİŞ / sağ kanat ATIŞ, panjur 2 × 626 cm²) + EPDM şeritler · B evaporatör gideri Ø20 → Ø12 (K altından, E şarjör "
                      "altından, eşik çatal yarığından) ≥ %1 · soğutma hatları B'ye MODELLENMEDİ (SOGUTMA_HAT_ACIK)", ("ealt_secop_", "ealt_perde_", "ealt_gider_")),
    ("E_ALT_PANO", "B elektrik panosu E'nin altında (v2, K4'ten): S7-1200 1214C + 3 × SM1221 + SM1222 · NDR-240-24 · EM-324C · 21 seçici röle · klemens · "
                   "plaka sol yan saca 4 mesafe burcuyla, cihazlar emiş (serin) tarafında", ("ealt_pano_",)),
]
E_ALT_BIRIM_MAP = {k: o for k, _a, o in E_ALT_BIRIM}
E_ALT_ONEK = E_ALT_BIRIM_MAP       # yap_hat2_montaj_v1 bu adla okur: E_BIRIM += [(k, ad, KC.E_ALT_ONEK[k]) …]


# ================================================================ YARDIMCILAR ================================================================
def _tek(wp):
    if hasattr(wp, "vals"):
        v = [o for o in wp.vals() if isinstance(o, cq.Shape)]
        return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)
    return wp


def _wp(sh):
    return cq.Workplane(obj=sh)


def _y90(sh, t):
    """y ekseni etrafında +90° [(x, y, z) → (z, y, −x)] + öteleme t"""
    return sh.rotate(V(0, 0, 0), V(0, 1, 0), 90.0).translate(V(*t))


def _kaynak(ss):
    ss = [s for s in ss if s is not None]
    r = ss[0]
    for s in ss[1:]:
        r = r.fuse(s)
    return r.clean()


def _cyl(p0, p1, r):
    a, b = V(*p0), V(*p1)
    d = b - a
    return cq.Solid.makeCylinder(r, d.Length, a, d.normalized())


def _ekle(ad, sh, mal, bom=None, kaynak="h2_kutu_v1", grup="SABIT"):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=_wp(sh) if isinstance(sh, cq.Shape) else sh, mal=mal, grup=grup, bom=bom, kaynak=kaynak))
    YENI.append(ad)


# ================================================================ store_cad_v14 (ÖZEL KOPYA — montajın dolabına dokunmaz) ================================================================
_SC = []


def _store():
    """store_cad_v14 ayrı bir modül nesnesi olarak yüklenir (montajdaki SC / h2_store_v1'in listesine dokunmamak için) · bir kez"""
    if not _SC:
        sp = _ilu.spec_from_file_location("store_cad_v14_h2kutu", os.path.join(_U, "store_cad_v14.py"))
        m = _ilu.module_from_spec(sp); sp.loader.exec_module(m)
        m.modul()
        _SC.append(m)
    return _SC[0]


def b_k4_secimi():
    """görev kuralı: K4 (dünya x 2027,5–2500) içindeki B_SOGUTMA parçaları + bütün B_ELEKTRIK · her B_SOGUTMA parçası sınıflandırılmış olmalı"""
    SC = _store()
    sog, ele, sinifsiz = [], [], []
    for p in SC.PARCALAR:
        b = _tek(p["wp"]).BoundingBox()
        if p["birim"] == "B_ELEKTRIK":
            ele.append(p); continue
        if p["birim"] != "B_SOGUTMA" or b.xmin < B_K4_X[0] - 0.5 or b.xmax > B_K4_X[1] + 0.5:
            continue
        sog.append(p)
        if not (p["ad"] in B_AL or p["ad"] in B_YENIDEN or p["ad"] in B_ALINMAYAN or p["ad"].startswith(B_YOK_SAYILAN)):
            sinifsiz.append(p["ad"])
    assert not sinifsiz, "store_cad_v14 K4 B_SOGUTMA parcasi siniflandirilmamis: %s" % sinifsiz
    assert len(ele) == 32, "B_ELEKTRIK parca sayisi %d (32 bekleniyordu)" % len(ele)
    assert all(a in [p["ad"] for p in sog] for a in B_AL), "K4'te beklenen parca yok"
    return SC, sog, ele


# ================================================================ GİDER HATTI (eksen) ================================================================
def gider_ekseni():
    """plan noktaları → [(x, y_eksen, z, r)] · taban çizgisi (iç alt) GIDER_GIRIS'ten her koşuda GIDER_EGIM ile iner ·
    Ø20: eksen = taban + (R20 − T20) · Ø12: eksen = taban + (R12 − T12) · eksantrik redüksiyon: taban çizgisi sürekli (su birikmez)"""
    inv0 = GIDER_GIRIS[1] - (R20 - T20)
    s, out = 0.0, []
    for i, (x, z) in enumerate(GIDER_PLAN):
        if i:
            s += math.hypot(x - GIDER_PLAN[i - 1][0], z - GIDER_PLAN[i - 1][1])
        inv = inv0 - GIDER_EGIM * s
        r, t = (R20, T20) if i <= 1 else (R12, T12)
        out.append(dict(x=x, z=z, s=s, inv=inv, r=r, y=inv + (r - t)))
    return out


def gider_y(x, z):
    """(x, z) plan noktasında Ø12 ekseninin y'si (Ø20 bölgesinde Ø20'ninki) — denetim / delik yerleri için"""
    E = gider_ekseni()
    for a, b in zip(E, E[1:]):
        L = math.hypot(b["x"] - a["x"], b["z"] - a["z"])
        if L < 1e-9: continue
        u = ((x - a["x"]) * (b["x"] - a["x"]) + (z - a["z"]) * (b["z"] - a["z"])) / (L * L)
        d = math.hypot(a["x"] + u * (b["x"] - a["x"]) - x, a["z"] + u * (b["z"] - a["z"]) - z)
        if -1e-9 <= u <= 1 + 1e-9 and d < 1e-6:
            return a["y"] + u * (b["y"] - a["y"]) if a["r"] == b["r"] else (a["inv"] + u * (b["inv"] - a["inv"])) + (b["r"] - (T12 if b["r"] == R12 else T20))
    raise ValueError("gider ekseninde degil: %s" % str((x, z)))


def _uzat(a, b, da, db):
    """a → b doğru parçasını kendi ekseni boyunca a ucundan da, b ucundan db uzatır (eğimli silindirin dik uç yüzü komşusuna tam girsin)"""
    d = (V(*b) - V(*a)).normalized()
    return (V(*a) - d * da).toTuple(), (V(*b) + d * db).toTuple()


def _gider_boru():
    E = gider_ekseni()
    p = [(e["x"], e["y"], e["z"]) for e in E]
    ss = [_cyl(*_uzat(p[0], p[1], 0.5, 0.3), R20)]                         # baş: sonra x 4000'de düz kesilir · uç: redüksiyonun içine 0,3
    # redüksiyon uç çemberleri 0,02 içeride / dışarıda: boru yüzeyiyle ÇAKIŞIK kenar kalmasın (OCC birleşimi iki katıya bölüyordu)
    c1 = cq.Wire.assembleEdges([cq.Edge.makeCircle(R20 - 0.02, V(*p[1]), V(1, 0, 0))])
    c2 = cq.Wire.assembleEdges([cq.Edge.makeCircle(R12 + 0.02, V(*p[2]), V(1, 0, 0))])
    ss.append(cq.Solid.makeLoft([c1, c2], True))
    for i, (a, b) in enumerate(zip(p[2:-1], p[3:])):
        ss.append(_cyl(*_uzat(a, b, 0.3 if i == 0 else 0.0, 0.0), R12))      # ilk Ø12 redüksiyonun içinden başlar · dirsekler kürelerle
    for q in p[3:-1]:
        ss.append(cq.Solid.makeSphere(R12, V(*q), angleDegrees1=-90, angleDegrees2=90))
    # baş yüzü dünya x 4000'de DÜZ (eğimli silindirin dik yüzü B'nin dış sacına 0,1 mm taşıyordu) → B'nin Ø20 borusuna alın alına
    return _kaynak(ss).intersect(kut(GIDER_PLAN[0][0], W + 100.0, 0.0, 1000.0, -1000.0, 1000.0).val()).clean()


def _burc(eksen, merkez, r_boyun, r_flans, r_delik, boyun, flanslar):
    """EPDM geçme bileziği: boyun (duvar deliğinde) + flanşlar · eksen 'x' / 'z' · boyun = (a, b) · flanslar = [(a, b), …] (eksen boyunca)"""
    def sil(r, a, b):
        return (_cyl((a, merkez[0], merkez[1]), (b, merkez[0], merkez[1]), r) if eksen == "x" else _cyl((merkez[0], merkez[1], a), (merkez[0], merkez[1], b), r))
    s = sil(r_boyun, *boyun)
    for f in flanslar:
        s = s.fuse(sil(r_flans, *f))
    lo = min([boyun[0]] + [f[0] for f in flanslar]) - 1.0; hi = max([boyun[1]] + [f[1] for f in flanslar]) + 1.0
    return s.cut(sil(r_delik, lo, hi)).clean()


def k_duvar_kesicileri():
    """K (kesme_cad_v11) duvarlarında gider delikleri — K YERELİ · montaj KS.PARCALAR'a uygular (bu dosya K'ya dokunmaz)"""
    y0 = gider_y(-399.25, -760.0)                  # = ealt_gider_kilifi_K_sol ekseni
    y1 = gider_y(0.0, -760.0)                      # = ealt_gider_kilifi_K_E ekseni (iki duvar tek bilezik)
    return [("sol_sac_urun_girisi", _wp(_cyl((-1.0, y0, -760.0), (2.5, y0, -760.0), R20 + 2.0)), "Ø24 · Ø20 gider (B → K) · EPDM bilezik ealt_gider_kilifi_K_sol"),
            ("sag_sac_E_penceresi", _wp(_cyl((397.0, y1, -760.0), (401.0, y1, -760.0), R12 + 2.0)), "Ø16 · Ø12 gider (K → E) · çift duvar bileziği ealt_gider_kilifi_K_E")]


K_DUVAR_DELIKLERI = []      # modul() doldurur: [(K parça adı, kesici Workplane (K yereli), not)]


# ================================================================ PARÇALAR ================================================================
def _secop_ve_pano(SC, sog, ele):
    """store_cad_v14 parçaları → E yereli (ad önekli, malzeme / BOM korunur)"""
    for p in sog:
        a = p["ad"]
        if a not in B_AL:
            continue
        sh = _y90(_tek(p["wp"]), SECOP_T)
        bom = p["bom"]
        if a.startswith("sogutma_grubu_montaj_rayi_"):
            b = sh.BoundingBox()
            sh = sh.intersect(kut(b.xmin - 1.0, b.xmax + 1.0, b.ymin - 1.0, b.ymax + 1.0, RAY_Z[0], RAY_Z[1]).val())
            if bom:
                bom = ("Yoğuşturucu montaj rayı L 40×40×3", 2, "AISI 304 köşebent · %.0f boy (v2 E: z %.0f…%.0f) · E tabanına 2 × M6 perçin somun (uç plakasız)" % (RAY_Z[1] - RAY_Z[0], RAY_Z[0], RAY_Z[1]),
                       "ön ray SÖKÜLÜR değil: ünite pedleriyle ray üstünde öne kayar (servis)")
        elif a == "sogutma_grubu_taban" and bom:
            bom = (bom[0], bom[1], bom[2], bom[3] + " · v2: E'nin alt önünde, 90° dönük (kondenser −x: sol bölmeden emer, atış sağ kanattan)")
        _ekle("ealt_secop_" + a, sh, p["mal"], bom, kaynak="store_cad_v14:%s (y +90° · %s)" % (a, SECOP_T))
    for p in ele:
        _ekle("ealt_pano_" + p["ad"], _y90(_tek(p["wp"]), PANO_T), p["mal"], p["bom"], kaynak="store_cad_v14:%s (y +90° · %s)" % (p["ad"], PANO_T))
    i = 0
    for yb in PANO_BURC["y"]:
        for zb in PANO_BURC["z"]:
            _ekle("ealt_pano_mesafe_burcu_%d" % i, _cyl((SAC, yb, zb), (PANO_T[0] + (-790.0), yb, zb), PANO_BURC["r"]), "celik",
                  ("Mesafe burcu M5 · Ø12 × 2,5 paslanmaz", 4, "pano plakası ↔ E sol yan sacı (iç yüz x 1,5)", "katalog (E'nin kendi pano burcu gibi)") if i == 0 else None)
            i += 1
    # ---- buharlaştırma tavası (E ölçüsü · B tavasının yapısı: 1,5 büküm, üstü açık) ----
    x0, x1, y0, y1, z0, z1 = TAVA_E
    t = kut(*TAVA_E).cut(kut(x0 + TAVA_T, x1 - TAVA_T, y0 + TAVA_T, y1 + 1.0, z0 + TAVA_T, z1 - TAVA_T))
    ic = ((x1 - x0 - 2 * TAVA_T) * (z1 - z0 - 2 * TAVA_T))
    b0 = next(p for p in sog if p["ad"] == "buharlastirma_tavasi")["bom"]
    _ekle("ealt_secop_buharlastirma_tavasi", t, "sac",
          ("Buharlaştırma tavası 1,5 (v2 · E ölçüsü)", 1, "304 · %.0f × %.0f × %.0f · iç alan %.0f cm² · SICAK GAZ serpantinli · emiş (serin) bölmesinde, kondenser dış yüzünün önünde"
           % (x1 - x0, y1 - y0, z1 - z0, ic / 100.0), "B tavası (%s) E'ye sığmaz → yeniden · gider ördek gagası tava ağzının ≥ 1,5 üstünde" % (b0[2][:24] if b0 else "store_cad_v14")),
          kaynak="store_cad_v14:buharlastirma_tavasi (yeniden boyutlandı)")
    # ---- sıcak gaz serpantini: 4 kol tava tabanında + iki çıkış kondenser dış yüzüne (basma hattı: kompresör → tava → kondenser girişi) ----
    r, yS = SG["r"], y0 + TAVA_T + SG["r"]
    pts = []
    for k, xs in enumerate(SG["x"]):
        za, zb = (SG["z"][0], SG["z"][1]) if k % 2 == 0 else (SG["z"][1], SG["z"][0])
        pts += [(xs, yS, za), (xs, yS, zb)]
    ss = [_cyl(a, b, r) for a, b in zip(pts, pts[1:])] + [cq.Solid.makeSphere(r, V(*q), angleDegrees1=-90, angleDegrees2=90) for q in pts[1:-1]]
    for (xs, yh), uc in zip(SG["cikis"], (pts[0], pts[-1])):
        q = [(uc[0], yS, uc[2]), (uc[0], yh, uc[2]), (250.0, yh, uc[2])]
        ss += [_cyl(q[0], q[1], r), _cyl(q[1], q[2], r), cq.Solid.makeSphere(r, V(*q[1]), angleDegrees1=-90, angleDegrees2=90)]
    _ekle("ealt_secop_sicak_gaz_serpantini", _kaynak(ss), "bakir",
          ("Sıcak gaz serpantini Cu Ø8 × 0,8 (tava ısıtıcı)", 1, "basma hattına SERİ: kompresör → tava içinde 4 × %.0f mm kol → kondenser girişi · ~%.1f m"
           % (SG["z"][1] - SG["z"][0], (4 * (SG["z"][1] - SG["z"][0]) + 3 * 22.0 + 2 * 250.0) / 1000.0),
           "Secop ünitesinin basma hattına lehimli — OEM değişikliği, Secop onayı AÇIK (alternatif: 50 W tava ısıtıcısı)"), kaynak="yeni (v2)")


def _perde():
    """bölme: arka perde · tavan · Z ayırıcı · contalar (hepsi 304 / EPDM)"""
    # arka perde (gider deliği Ø16)
    yg = gider_y(190.0, (Z_PERDE_ARKA[0] + Z_PERDE_ARKA[1]) / 2.0)
    a = kut(SAC, W - SAC, Y_TABAN_UST, Y_TAVAN_P[1], Z_PERDE_ARKA[0], Z_PERDE_ARKA[1]).cut(_wp(_cyl((190.0, yg, -352.0), (190.0, yg, -347.0), R12 + 2.0)))
    _ekle("ealt_perde_arka", a, "sac", ("Bölme arka perdesi 304 1,0", 1, "%.0f × %.0f · tabana + yan saclara L köşebentle (perçin) · Ø16 gider deliği (EPDM bilezik)"
                                         % (W - 2 * SAC, Y_TAVAN_P[1] - Y_TABAN_UST), "şarjör altını Secop havasından ayırır (atış şarjöre / kartona gitmez)"))
    # tavan (kablo kanalı + sağ ön dikme çentikli)
    t = kut(SAC + LAM, W - SAC, Y_TAVAN_P[0], Y_TAVAN_P[1], Z_PERDE_ARKA[1], Z_CONTA[0])
    t = t.cut(kut(KANAL_DIKEY_V14["x"][0] - 0.5, KANAL_DIKEY_V14["x"][1] + 0.5, Y_TAVAN_P[0] - 1.0, Y_TAVAN_P[1] + 1.0, KANAL_DIKEY_V14["z"][0] - 0.5, KANAL_DIKEY_V14["z"][1] + 0.5))
    t = t.cut(kut(W - SAC - 20.5, W, Y_TAVAN_P[0] - 1.0, Y_TAVAN_P[1] + 1.0, Z_CERCEVE[0] - 0.5, Z_CONTA[0] + 1.0))
    _ekle("ealt_perde_tavan", t, "sac", ("Bölme tavanı 304 1,5", 1, "%.0f × %.0f · y %.1f–%.1f · kablo kanalı + sağ ön dikme çentikli · yan saclara köşebent" %
                                          (W - 2 * SAC - LAM, Z_CONTA[0] - Z_PERDE_ARKA[1], Y_TAVAN_P[0], Y_TAVAN_P[1]),
                                          "bölmeyi üstteki mekanizma boşluğundan ayırır (sıcak hava yukarıdan emişe dönmez)"))
    _ekle("ealt_perde_tavan_on_contasi", kut(SAC + TAVA_T, W - SAC - 20.5, 508.0, Y_TAVAN_P[1], Z_CONTA[0], Z_CONTA[1]), "conta",
          ("EPDM sünger şerit 2 × 7 yapışkanlı", 1, "tavanın ön kenarı ↔ kanatların iç sacı (kapalıyken basar)", "katalog"))
    # Z ayırıcı: sabit üst bant (ünitenin üstünde) + sökülür Z (servis: ünite öne çekilirken sökülür)
    _ekle("ealt_perde_ayirici_sabit", kut(X_AYIRICI[0], X_AYIRICI[1], 435.0, Y_TAVAN_P[0], Z_PERDE_ARKA[1], Z_AYIRICI_ORTA[0]), "sac",
          ("Ayırıcı sabit bant 304 1,5", 1, "ünitenin (üstü 430) 5 üstünden tavana · arka perde ↔ Z'nin orta kolu · kondenser çevre contası alt kenarına basar", "üretim"))
    z_ = kut(X_AYIRICI[0], X_AYIRICI[1], Y_TABAN_UST, 435.0, 11.0, Z_AYIRICI_ORTA[0])
    z_ = z_.union(kut(X_AYIRICI[0], X_AYIRICI_ON[1], Y_TABAN_UST, Y_TAVAN_P[0], Z_AYIRICI_ORTA[0], Z_AYIRICI_ORTA[1]))
    z_ = z_.union(kut(X_AYIRICI_ON[0], X_AYIRICI_ON[1], Y_TABAN_UST, Y_TAVAN_P[0], Z_AYIRICI_ORTA[1], Z_CONTA[0]))
    z_ = z_.cut(kut(X_AYIRICI_ON[0] - 0.5, X_AYIRICI_ON[1] + 0.5, Y_TABAN_UST - 1.0, Y_ALT[0] + 3.0, Z_PANEL - 14.0, Z_CONTA[0] + 1.0))   # taban dayama dudağı çentiği (dudağa tam oturur)
    _ekle("ealt_perde_ayirici_sokulur", z_, "sac",
          ("Z ayırıcı 304 1,5 (2 büküm)", 1, "kondenser conta düzlemi (x 305) → ünite önünün 10 önü (z 16) → kanat derzinin arkası (x 416) · 4 Fastmount klips (sökülür)",
           "EMİŞ (sol kanat) ↔ ATIŞ (sağ kanat) ayrımı · servis: sökülür, ünite öne çekilir"))
    _ekle("ealt_perde_ayirici_on_contasi", kut(X_ORTA_DERZ[0] - TAVA_T, X_ORTA_DERZ[1] + TAVA_T, Y_ALT[0] + 3.0, 508.0, Z_CONTA[0], Z_CONTA[1]), "conta",
          ("EPDM sünger şerit 6 × 2", 1, "Z ayırıcının ön kenarı ↔ iki kanadın derz kenarları (kapalıyken iki kanada basar)", "katalog"))
    for tag, za, zb in (("arka", Z_PERDE_ARKA[1], -344.0), ("on", 6.0, 11.0)):
        _ekle("ealt_perde_conta_taban_yani_" + tag, kut(300.0, 310.0, Y_TABAN_UST, 148.0, za, zb), "conta",
              ("EPDM sünger conta 10 × 5 × 22", 2, "ünite taban kenarı ↔ %s · ayırıcı düzleminde (kondenser çevre contası bunun üstünden başlar)" % ("arka perde" if tag == "arka" else "Z ayırıcı"),
               "katalog") if tag == "arka" else None)


def _gider():
    E = gider_ekseni()
    GB = _gider_boru()
    _ekle("ealt_gider_borusu", GB, "plastik",
          ("Gider borusu Ø20 × 1,5 → Ø12 × 1 PVC + eksantrik redüksiyon 20/12 (taban çizgisi sürekli)", 1,
           "B'nin sağ dış sacından (dünya 4000, 170, −760) · Ø20 %.0f + redüksiyon %.0f + Ø12 %.0f mm · 3 dirsek · her koşu %%%.1f iniş (sifon YOK)"
           % (E[1]["s"] - E[0]["s"], E[2]["s"] - E[1]["s"], E[-1]["s"] - E[2]["s"], 100.0 * GIDER_EGIM),
           "K altında tartı / tava üstünden · E'de şarjör altından + kapı eşiğinin çatal yarığından (asansör arabasının altından) · arka perde → tava"))
    # geçiş bilezikleri (EPDM): K sol sacı (Ø20) · K sağ + E sol sacı çift duvar (Ø12) · arka perde (Ø12)
    y0 = gider_y(-399.25, -760.0)
    _ekle("ealt_gider_kilifi_K_sol", _burc("x", (y0, -760.0), R20 + 2.0, R20 + 6.0, R20 + 0.1, (-400.0, -398.5), [(-398.5, -396.5)]), "conta",
          ("Geçme bileziği EPDM · delik Ø24 · iç Ø20", 1, "K sol sacı (1,5) · flanş yalnız K içinde (B tarafı B'nin bileziği)", "katalog (hortum geçiş lastiği)"))
    y1 = gider_y(0.0, -760.0)
    _ekle("ealt_gider_kilifi_K_E", _burc("x", (y1, -760.0), R12 + 2.0, R12 + 5.0, R12 + 0.1, (-1.5, 1.5), [(-3.5, -1.5), (1.5, 3.5)]), "conta",
          ("Çift duvar geçme bileziği EPDM · delik Ø16 · iç Ø12 · boyun 3", 1, "K sağ sacı + E sol sacı (bitişik) · istasyonlar ayrılırken boru bilezikten çekilir", "katalog"))
    y2 = gider_y(190.0, -349.5)
    _ekle("ealt_gider_kilifi_perde", _burc("z", (190.0, y2), R12 + 2.0, R12 + 5.0, R12 + 0.1, Z_PERDE_ARKA, [(-352.0, Z_PERDE_ARKA[0]), (Z_PERDE_ARKA[1], -347.0)]), "conta",
          ("Geçme bileziği EPDM · delik Ø16 · iç Ø12", 1, "bölme arka perdesi (1,0)", "katalog"))
    # kelepçeler: PA kelepçe + 304 ayak (E tabanına 2 × M4 perçin somun)
    for i, (k, u) in enumerate(KELEPCE):
        if k == 0:
            x, z = u, -760.0
            yc = gider_y(x, z)
            blk = kut(x - 5.0, x + 5.0, yc - 9.0, yc + 9.0, z - 9.0, z + 9.0)
            ayak = kut(x - 4.0, x + 4.0, Y_TABAN_UST, yc - 9.0, z - 4.0, z + 4.0)
        else:
            x, z = GIDER_PLAN[3][0], u
            yc = gider_y(x, z)
            blk = kut(x - 9.0, x + 9.0, yc - 9.0, yc + 9.0, z - 5.0, z + 5.0)
            ayak = kut(x - 4.0, x + 4.0, Y_TABAN_UST, yc - 9.0, z - 4.0, z + 4.0)
        c = blk.union(ayak).cut(_wp(GB))
        _ekle("ealt_gider_kelepcesi_%d" % i, c, "plastik",
              ("Boru kelepçesi Ø12 + 304 ayak 8 × 8", len(KELEPCE), "PA kelepçe · ayak E tabanına 2 × M4 perçin somun · şarjör altında (asansör platformu ≥ 229)", "katalog + üretim") if i == 0 else None)
    # ördek gagası (store_cad_v14 gider_cek_valfi_sol · B'de dikey Ø14 × 10) → borunun ucunda YATAY (+z), tavanın üstünde ·
    #   flanşlı gövde boru ucuna 5 mm geçer (iç Ø12,2 · tutucu kapak): gövde z son −5 … son + 10
    SC = _store()
    pv = next(p for p in SC.PARCALAR if p["ad"] == "gider_cek_valfi_sol")
    v = _tek(pv["wp"])
    c = v.BoundingBox().center
    son = E[-1]
    v = v.translate(V(-c.x, -c.y, -c.z)).rotate(V(0, 0, 0), V(1, 0, 0), -90.0).translate(V(son["x"], son["y"], son["z"] + VALF_L / 2.0))
    v = v.fuse(_cyl((son["x"], son["y"], son["z"] - 5.0), (son["x"], son["y"], son["z"]), 7.0)).cut(
        _cyl((son["x"], son["y"], son["z"] - 6.0), (son["x"], son["y"], son["z"] + 0.1), R12 + 0.1)).clean()
    bom = pv["bom"]
    _ekle("ealt_gider_cek_valfi", v, "silikon", (bom[0], 1, bom[2], (bom[3] if len(bom) > 3 else "") + " · v2: tek gider, boru ucuna 5 mm geçer, ucu yatay (+z), tava ağzının üstünde"),
          kaynak="store_cad_v14:gider_cek_valfi_sol (x −90° · gider ucu · geçme boynu)")


def _panjur_kesici(x0, x1):
    xc = (x0 + x1) / 2.0
    kol = ((xc - PANJUR["kopru_x"] / 2.0 - PANJUR["w"], xc - PANJUR["kopru_x"] / 2.0), (xc + PANJUR["kopru_x"] / 2.0, xc + PANJUR["kopru_x"] / 2.0 + PANJUR["w"]))
    k = None
    for i in range(PANJUR["n"]):
        y = PANJUR["y0"] + i * (PANJUR["h"] + PANJUR["kopru_y"])
        for a, b in kol:
            s = kut(a, b, y, y + PANJUR["h"], Z_PANEL - 1.0, Z_ON + 1.0)
            k = s if k is None else k.union(s)
    return k, kol


def panjur_alanlari():
    """her ALT kanadın panjur yarıkları: (kanat, [(x0, x1)], y0, y1, serbest alan mm²)"""
    out = []
    for ad, x0, x1, *_r in ON_PANEL:
        if ad in KUTU_KANAT:
            _k, kol = _panjur_kesici(x0, x1)
            out.append((ad, kol, PANJUR["y0"], PANJUR["y0"] + PANJUR["n"] * (PANJUR["h"] + PANJUR["kopru_y"]) - PANJUR["kopru_y"],
                        len(kol) * PANJUR["n"] * PANJUR["w"] * PANJUR["h"]))
    return out


def modul():
    """v2 parça listesi: kutu_cad_v14.modul() (v1, dokunulmaz) → kopya − icecek_* + panjurlu kanatlar + delikli sol sac + ealt_* · İDEMPOTENT"""
    t0 = time.time()
    E14.modul()
    PARCALAR[:] = []; DEGISEN[:] = []; CIKAN[:] = []; YENI[:] = []
    for p in E14.PARCALAR:
        if p["ad"].startswith("icecek_"):
            CIKAN.append(p["ad"]); continue
        PARCALAR.append(dict(p))                       # sığ kopya: wp nesnesi aynı (değişmeyenler v1'in katısı)
    ad = {p["ad"]: p for p in PARCALAR}
    for kn in KUTU_KANAT:
        x0, x1 = next((q[1], q[2]) for q in ON_PANEL if q[0] == kn)
        k, _kol = _panjur_kesici(x0, x1)
        p = ad[kn]; p["wp"] = p["wp"].cut(k)
        b = list(p["bom"]); b[2] = b[2] + " · v2: lazer panjur 2 × %d yarık %.0f × %.0f (köprü %.0f / %.0f) · %s" % (
            PANJUR["n"], PANJUR["w"], PANJUR["h"], PANJUR["kopru_y"], PANJUR["kopru_x"], "Secop EMİŞİ" if kn.endswith("sol") else "Secop ATIŞI")
        p["bom"] = tuple(b); p["kaynak"] = "kutu_cad_v14 + h2_kutu_v1 panjur kesimi"
        DEGISEN.append(kn)
    yg = gider_y(0.0, -760.0)                      # = ealt_gider_kilifi_K_E ekseni
    p = ad["sol_sac_pizza_penceresi"]
    p["wp"] = p["wp"].cut(_wp(_cyl((-1.0, yg, -760.0), (2.5, yg, -760.0), R12 + 2.0)))
    p["kaynak"] = "kutu_cad_v14 + h2_kutu_v1 gider deliği Ø16"
    DEGISEN.append("sol_sac_pizza_penceresi")
    SC, sog, ele = b_k4_secimi()
    _secop_ve_pano(SC, sog, ele)
    _perde()
    _gider()
    K_DUVAR_DELIKLERI[:] = k_duvar_kesicileri()
    print("h2_kutu_v1 · E v2 parca listesi: %d (v1 %d · cikan %d icecek_ · degisen %d · yeni %d ealt_) · %.0f sn"
          % (len(PARCALAR), len(E14.PARCALAR), len(CIKAN), len(DEGISEN), len(YENI), time.time() - t0))
    return PARCALAR


# ================================================================ SOĞUTMA HATTI (MODELLENMEDİ · tahmin) ================================================================
def sogutma_hatti_tahmini():
    """Secop servis vanaları (E) → B evaporatörleri: Manhattan yol (E arka perde → şarjör altı → E sol sacı → K arka alt → B sağ dış sac → B arka) · +%15 dirsek / sapma"""
    vx, vy, vz = SECOP_VANA_E[0] + X_E, SECOP_VANA_E[1], SECOP_VANA_E[2]
    zb = -760.0; ye = (EVAP["y"][0] + EVAP["y"][1]) / 2.0; ze = (EVAP["z"][0] + EVAP["z"][1]) / 2.0
    E_ = abs(vz - zb) + abs(vx - X_E)                          # E: arkaya + E sol sacına
    K_ = X_E - X_K                                             # K boyunca
    B_sag = (X_K - EVAP["sag"][1]) + abs(ye - vy) + abs(ze - zb)   # B'de sağ evaporatörün yakın ucuna
    sag = E_ + K_ + B_sag
    sol = sag + (EVAP["sag"][0] - EVAP["sol"][1]) + (EVAP["sag"][1] - EVAP["sag"][0])   # sağ evaporatörü geçip solun yakın ucuna
    k = 1.15
    return dict(durum="AÇIK — MODELLENMEDİ (v1 de modellememişti)", yol="E arka perde → şarjör altı → E sol sacı → K alt arka → B sağ dış sac (4000) → B arka evaporatörler",
                vana_E_yerel=SECOP_VANA_E, sag_evap_m=round(sag / 1000.0, 2), sol_evap_m=round(sol / 1000.0, 2),
                sag_evap_m_pay=round(k * sag / 1000.0, 2), sol_evap_m_pay=round(k * sol / 1000.0, 2),
                toplam_boru_m=round(2.0 * k * sol / 1000.0 + 2 * 0.3, 1),
                sivi_hatti_dolum_g=round(k * sol / 1000.0 * 17.7 * 0.48, 0),
                not_="sıvı Ø6,35 × 0,8 + emiş Ø9,52 yalıtımlı (Ø ≈ 28) · evaporatörler paralel, ayrım sağ evaporatörde (T) · R290 toplam dolum ≤ 150 g (EN/IEC 60335-2-89) "
                     "hesabı AÇIK · emiş hattı eşik yarığından geçemez (Ø28 + asansör arabası) → ayrı geçiş (sağ yan boşluk yalnız Ø6,35) AÇIK · "
                     "v1'de Secop K4'te, evaporatörlere ~1,0 / 1,3 m idi")


SOGUTMA_HAT_ACIK = sogutma_hatti_tahmini()


# ================================================================ DENETİM ================================================================
def _bbk(A, B, pay=0.05):
    return A.xmin < B.xmax - pay and B.xmin < A.xmax - pay and A.ymin < B.ymax - pay and B.ymin < A.ymax - pay and A.zmin < B.zmax - pay and B.zmin < A.zmax - pay


def _hacim(a, b):
    try:
        return a.intersect(b).Volume()
    except Exception:
        return -1.0


def _mesafe(a, b):
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    d = _DSS(a.wrapped, b.wrapped)
    return d.Value() if d.IsDone() else -1.0


def capraz(S, T, esik=0.1, haric=()):
    """S, T: [(ad, shape)] → gerçek kesişim > esik mm³ · haric: {(a, c)} çiftleri"""
    S = [(a, s, s.BoundingBox()) for a, s in S]; T = [(a, s, s.BoundingBox()) for a, s in T]
    out = []
    for a, sa, A in S:
        for c, sc, B in T:
            if a == c or (a, c) in haric or (c, a) in haric or not _bbk(A, B):
                continue
            v = _hacim(sa, sc)
            if v > esik or v < 0:
                out.append((round(v, 3), a, c))
    return sorted(out, reverse=True)


DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger))
    print("  %-150s %s %s" % (ad, "GECTI" if sart else "** KALDI **", deger))


def denetim():
    """öz denetim (assert'ler __main__'de) · montaj bunu çağırmaz"""
    t0 = time.time()
    if not PARCALAR:
        modul()
    DEN[:] = []
    P = {p["ad"]: p for p in PARCALAR}
    SH = {a: _tek(p["wp"]) for a, p in P.items()}
    YN = [a for a in YENI]
    print("DENETIM h2_kutu_v1 (E v2 · %d parca · yeni %d)" % (len(PARCALAR), len(YN)))
    # ---- 0 · liste / değişmeyenler ----
    v1 = {p["ad"]: p for p in E14.PARCALAR}
    ayni = [a for a in v1 if a in P and a not in DEGISEN and P[a]["wp"] is v1[a]["wp"]]
    kontrol("LISTE: v1 %d = v2 %d − yeni %d + cikan %d (icecek_* %d) · degisen %s · geri kalan %d parca v1 katisinin KENDISI (dokunulmadi)"
            % (len(v1), len(PARCALAR), len(YN), len(CIKAN), len([a for a in CIKAN if a.startswith("icecek_")]), DEGISEN, len(ayni)),
            len(v1) == len(PARCALAR) - len(YN) + len(CIKAN) and len(CIKAN) == 7 and all(a.startswith("icecek_") for a in CIKAN)
            and len(ayni) == len(v1) - len(CIKAN) - len(DEGISEN) and not [a for a in P if a.startswith("icecek_")])
    gec = [a for a in YN if not SH[a].isValid()]
    cok = [(a, len(SH[a].Solids())) for a in YN if len(SH[a].Solids()) != 1 and not a.startswith("ealt_pano_")]
    kontrol("KATILAR gecerli (yeni %d) · pano disindaki her yeni parca TEK kati (gider borusu Ø20 + redüksiyon + Ø12 + dirsekler kaynakli)" % len(YN), not gec and not cok, str(gec + cok))
    birimsiz = [a for a in YN if not any(a.startswith(o) for _k, _a, o_ in E_ALT_BIRIM for o in o_)]
    kontrol("BIRIM: her yeni parca E_ALT_BIRIM onekiyle (E_ALT_SOGUTMA %d · E_ALT_PANO %d)" % (
        len([a for a in YN if a.startswith(E_ALT_BIRIM_MAP["E_ALT_SOGUTMA"])]), len([a for a in YN if a.startswith(E_ALT_BIRIM_MAP["E_ALT_PANO"])])), not birimsiz, str(birimsiz))
    # ---- 1 · BOŞALAN HACİM (gerçek katılarla) ----
    KUTU = kut(SAC, W - SAC, Y_TABAN_UST, 588.0, -351.0, Z_PANEL).val()
    eng = []
    for a, p in v1.items():
        if a.startswith("icecek_") or a in KUTU_KANAT:
            continue
        s = _tek(p["wp"]); b = s.BoundingBox()
        if _bbk(b, KUTU.BoundingBox()) and p["grup"] in ("SABIT", "ASANSOR"):
            k = _hacim(s, KUTU)
            if k > 0.01:
                kb = s.intersect(KUTU).BoundingBox()
                eng.append((a, round(kb.xmin, 1), round(kb.xmax, 1), round(kb.ymin, 1), round(kb.ymax, 1), round(kb.zmin, 1), round(kb.zmax, 1)))
    print("   BOSALAN HACIM (x %.1f–%.1f · y %.0f–588 · z −351…+%.0f) icindeki v1 parcalari (icecek_ ve alt kanatlar haric):" % (SAC, W - SAC, Y_TABAN_UST, Z_PANEL))
    for e in eng:
        print("      %-34s x %6.1f–%6.1f · y %6.1f–%6.1f · z %7.1f…%7.1f" % e)
    kontrol("BOSALAN HACIM: icinde yalniz on cerceve (sol lam, sag dikme, dayama dudagi), 2 alt menteşe, dikey kablo kanali, asansor motor plakasi kenari — %d parca" % len(eng),
            all(e[0].startswith(("onyuz_dikme_", "onyuz_alt_dayama", "onyuz_mentese_", "kablo_kanali_dikey", "asansor_motor_plakasi", "asansor_motoru", "onyuz_basac_")) for e in eng),
            str([e[0] for e in eng]))
    # ---- 2 · ÜNİTE SIĞIYOR ----
    UN = ["ealt_secop_sogutma_grubu_taban", "ealt_secop_sogutma_grubu_kondenser", "ealt_secop_sogutma_grubu_fan", "ealt_secop_sogutma_grubu_kompresor"]
    ub = cq.Compound.makeCompound([SH[a] for a in UN]).BoundingBox()
    kb = SH["ealt_secop_sogutma_grubu_kondenser"].BoundingBox()
    kontrol("UNITE ZARFI x %.1f–%.1f (%.0f · 90° donuk) · y %.1f–%.1f (%.0f) · z %.1f…%.1f (%.0f) · kondenser dis yuzu x %.1f (−x'e) · on %.0f × %.0f"
            % (ub.xmin, ub.xmax, ub.xlen, ub.ymin, ub.ymax, ub.ylen, ub.zmin, ub.zmax, ub.zlen, kb.xmin, kb.zlen, kb.ylen),
            abs(ub.xlen - 450.0) < 0.1 and abs(ub.zlen - 350.0) < 0.1 and abs(kb.xmin - 250.0) < 0.01 and abs(ub.ymax - (Y_TABAN_UST + 7.0 + 297.0)) < 0.1)
    YUMUSAK = ("ealt_secop_sogutma_grubu_takozu_", "ealt_secop_sogutma_grubu_taban_contasi", "ealt_secop_k4_kondenser_contasi", "ealt_perde_conta_taban_yani_",
               "ealt_secop_sicak_gaz_serpantini")
    tem = []
    for a in UN:
        for c, s in SH.items():
            if c in UN or c.startswith(YUMUSAK) or not _bbk(SH[a].BoundingBox(), s.BoundingBox(), pay=-1.0):
                continue
            d = _mesafe(SH[a], s)
            if 0.0 <= d <= 0.05:
                tem.append((round(d, 2), a, c))
    kontrol("UNITE RIJIT TEMAS YOK: unite (taban/kondenser/fan/kompresor) yalniz pedlere, EPDM contalara ve sicak gaz serpantinine degiyor (B kurali)", not tem, str(tem[:5]))
    DUV = ("ealt_perde_arka", "ealt_perde_tavan", "ealt_perde_ayirici_sokulur", "ealt_perde_ayirici_sabit", "ealt_secop_buharlastirma_tavasi",
           "ealt_secop_sogutma_grubu_montaj_rayi_arka", "ealt_secop_sogutma_grubu_montaj_rayi_on", "ealt_pano_guc_kaynagi_NDR-240-24", "ealt_gider_cek_valfi")
    dmin = {c: min(_mesafe(SH[a], SH[c]) for a in UN) for c in DUV}
    kontrol("UNITE SIGIYOR: bolme saclarina ≥ 5 (B SECOP_BOS): %s · raylara (pedler 4 mm) ≥ 4" % " · ".join("%s %.1f" % (c.replace("ealt_", ""), v) for c, v in dmin.items()),
            all(v >= 5.0 - 0.01 for c, v in dmin.items() if "montaj_rayi" not in c) and all(v >= 4.0 - 0.01 for c, v in dmin.items() if "montaj_rayi" in c))
    # ---- 3 · ÇAKIŞMA: yeni ↔ bütün KC parçaları (dinlenme) · yeni ↔ yeni ----
    YS = [(a, SH[a]) for a in YN]
    DIGER = [(a, SH[a]) for a in P if a not in YENI and P[a]["grup"] in ("SABIT", "ASANSOR", "SABIT_REF")]
    c1 = capraz(YS, DIGER)
    for x_ in c1[:12]: print("   %10.3f mm3  %s  <->  %s" % x_)
    kontrol("CAKISMA dinlenme: yeni %d ↔ v2 SABIT + ASANSOR + REF %d parca (panjurlu kanatlar + delikli sol sac dahil) > 0,1 mm³ = 0" % (len(YS), len(DIGER)), not c1, "%d bulgu" % len(c1))
    c2 = []
    for i in range(len(YS)):
        c2 += capraz([YS[i]], YS[i + 1:])
    for x_ in c2[:12]: print("   %10.3f mm3  %s  <->  %s" % x_)
    kontrol("CAKISMA yeni ↔ yeni (%d) > 0,1 mm³ = 0" % len(YS), not c2, "%d bulgu" % len(c2))
    # ---- 4 · HAREKETLİ GRUPLAR bütün döngü + ASANSÖR stroku ----
    BB_Y = cq.Compound.makeCompound([s for _a, s in YS]).BoundingBox()
    HG = [p for p in PARCALAR if p["grup"] not in ("SABIT", "ASANSOR", "SABIT_REF") and p["ad"] not in YENI]
    anlar = [round(0.25 * i, 2) for i in range(int(DONGU / 0.25) + 1)]
    bul4, en_alt, n4 = [], (1e9, ""), 0
    for t in anlar:
        W_ = blank_dunya(t)
        for p in HG:
            g = p["grup"]
            M = W_[g] if g.startswith("B_") else grup_matrisi(g, t)
            s = uygula(_tek(p["wp"]), M); b = s.BoundingBox(); n4 += 1
            if b.ymin < en_alt[0]:
                en_alt = (b.ymin, "%s @%.2f" % (p["ad"], t))
            if not _bbk(b, BB_Y):
                continue
            for a, sy in YS:
                if _bbk(b, sy.BoundingBox()):
                    v = _hacim(s, sy)
                    if v > 0.1 or v < 0:
                        bul4.append((round(v, 2), "%s@%.2f" % (p["ad"], t), a))
    kontrol("HAREKETLI GRUPLAR: %d parca × %d an (0 … %.1f sn, adim 0,25 · blank B_* dahil) ↔ yeni parcalar = 0 · hareketlilerin en alti y %.1f (%s) > bolme tavani %.1f"
            % (len(HG), len(anlar), DONGU, en_alt[0], en_alt[1], Y_TAVAN_P[1]), not bul4 and en_alt[0] > Y_TAVAN_P[1], str(bul4[:4]))
    AS = [(p["ad"], _tek(p["wp"])) for p in PARCALAR if p["grup"] == "ASANSOR"]
    strok = SH["asansor_ust_yatak"].BoundingBox().ymin - SH["asansor_somunu"].BoundingBox().ymax
    bul5 = []
    for dy in (0.0, 10.0, 25.0, 50.0, 100.0, 200.0, 400.0, strok):
        bul5 += [(v, a + "@dy%.0f" % dy, c) for v, a, c in capraz([(a, s.translate(V(0, dy, 0))) for a, s in AS], YS)]
    d_ar = min(_mesafe(s, SH["ealt_gider_borusu"]) for a, s in AS)
    kontrol("ASANSOR STROKU 0 … %.0f mm (8 konum) ↔ yeni parcalar = 0 · en alt konumda asansor ↔ gider en yakin %.1f mm (araba y 170, gider eşik yariginda)" % (strok, d_ar),
            not bul5 and d_ar >= KUCUK_PAY, str(bul5[:3]))
    # ---- 5 · KANAT AÇILIŞI (panjurlu kopya) 1°…155° ↔ yeni parçalar ----
    bul6 = []
    for kn in KUTU_KANAT:
        k = SH[kn]
        for aci in KAPI_ACILARI:
            s = uygula(k, kapi_matrisi(kn, aci))
            bul6 += [(v, "%s@%d" % (kn, aci), c) for v, _a, c in capraz([(kn, s)], YS)]
    kontrol("ALT KANATLAR (panjurlu) %d aci (1°…%.0f°) ↔ yeni parcalar = 0 (kapali konumda EPDM seritler kanat ic sacina TEMAS: 0 hacim)" % (len(KAPI_ACILARI), KAPI_MAX_ACI),
            not bul6, str(bul6[:4]))
    # ---- 6 · PANJUR ALANI + AYRIM ----
    kn_face = kb.zlen * kb.ylen
    PA = panjur_alanlari()
    for kn, kol, y0, y1, A in PA:
        print("   PANJUR %-22s sutun x %s · y %.0f–%.0f · serbest %.0f cm² (kondenser yuzunun %.2f kati) · hiz %.2f m/s @ 551 m³/h"
              % (kn, " + ".join("%.1f–%.1f" % c for c in kol), y0, y1, A / 100.0, A / kn_face, 551.0 / 3600.0 / (A / 1e6)))
    dv = {kn: SH[kn].Volume() for kn in KUTU_KANAT}
    dv0 = {kn: _tek(v1[kn]["wp"]).Volume() for kn in KUTU_KANAT}
    kes = {kn: dv0[kn] - dv[kn] for kn in KUTU_KANAT}
    bekl = PANJUR["n"] * 2 * PANJUR["w"] * PANJUR["h"] * (TAVA_T + IC_SAC)
    kontrol("PANJUR serbest alan her kanatta %.0f cm² ≥ kondenser yuzu %.0f × %.0f = %.0f cm² × 0,5 = %.0f cm² · kesilen hacim (dis 1,5 + ic 1,0 sac) %s = beklenen %.0f mm³"
            % (PA[0][4] / 100.0, kb.zlen, kb.ylen, kn_face / 100.0, kn_face / 200.0, " / ".join("%.0f" % v for v in kes.values()), bekl),
            all(A >= 0.5 * kn_face for *_x, A in PA) and all(abs(v - bekl) < 1.0 for v in kes.values()))
    sol, sag = PA[0][1], PA[1][1]
    kontrol("EMIS / ATIS AYRIMI: sol kanat yariklari x %.1f–%.1f < ayirici on kolu x %.1f–%.1f < sag kanat yariklari x %.1f–%.1f · yariklar tavanin (%.1f) altinda (ust %.0f)"
            % (sol[0][0], sol[1][1], X_AYIRICI_ON[0], X_AYIRICI_ON[1], sag[0][0], sag[1][1], Y_TAVAN_P[0], PA[0][3]),
            sol[1][1] < X_AYIRICI_ON[0] and sag[0][0] > X_AYIRICI_ON[1] and PA[0][3] < Y_TAVAN_P[0] and PA[0][2] > Y_ALT[0] + 3.0)
    # ayırıcı yüzeyinin sürekliliği: üç düzlemde nokta ızgarası → her nokta bir katının İÇİNDE (ayırıcı / conta / ünite / dudak)
    AYR = [SH[a] for a in P if a.startswith(("ealt_perde_", "ealt_secop_sogutma_grubu_", "ealt_secop_k4_")) ] + [SH["onyuz_alt_dayama_dudagi"]]
    def ic_mi(pt):
        return any(s.isInside(V(*pt), 1e-3) for s in AYR)
    bos = []
    xp = (X_AYIRICI[0] + X_AYIRICI[1]) / 2.0
    for yy in [127.0 + 10.0 * i for i in range(39)] + [512.5]:
        for zz in [-348.5 + 9.0 * j for j in range(41)] + [15.5]:
            if zz <= Z_AYIRICI_ORTA[0] and not ic_mi((xp, yy, zz)): bos.append(("x305", yy, zz))
        for xx in [X_AYIRICI[0] + 0.5 + 11.0 * j for j in range(11)] + [X_AYIRICI_ON[1] - 0.5]:
            if not ic_mi((xx, yy, 16.5)): bos.append(("z16", xx, yy))
        for zz in [17.5 + 4.0 * j for j in range(11)] + [58.5]:
            if not ic_mi((X_DERZ_ORTA, yy, zz)): bos.append(("x416", yy, zz))
    kontrol("AYIRICI SUREKLI: 3 duzlem (x %.2f · z 16,5 · x %.1f) nokta izgarasi → her nokta ayirici / conta / unite / dudak icinde (kisa devre yolu yok)" % (xp, X_DERZ_ORTA),
            not bos, "%d bos: %s" % (len(bos), bos[:6]))
    # ---- 7 · GİDER: iniş · K içi · aralıklar · tava ----
    E_ = gider_ekseni()
    eg = [((a["inv"] - b["inv"]) / (b["s"] - a["s"]), a, b) for a, b in zip(E_, E_[1:])]
    kontrol("GIDER INISI: %d kosu · her kosuda taban cizgisi inisi %s (≥ %%1,0) · giris taban %.2f → cikis %.2f (%.0f mm yol) · redüksiyon eksantrik (taban surekli)"
            % (len(eg), " / ".join("%%%.2f" % (100 * e[0]) for e in eg), E_[0]["inv"], E_[-1]["inv"], E_[-1]["s"]), all(e[0] >= GIDER_EGIM - 1e-9 for e in eg))
    gb = SH["ealt_gider_borusu"]
    g0 = gb.intersect(kut(GIDER_PLAN[0][0] - 1.0, GIDER_PLAN[0][0] + 0.05, 0, 400, -800, -700).val())
    b0 = g0.BoundingBox()
    kontrol("GIDER BASI: dunya x %.2f'de duz yuz (B'nin Ø20 borusuna alin) · eksen y %.1f · z %.1f = arayuz (%.0f, %.0f, %.0f) · x < 4000'de gider parcasi yok"
            % (gb.BoundingBox().xmin + X_E, (b0.ymin + b0.ymax) / 2.0, (b0.zmin + b0.zmax) / 2.0, GIDER_GIRIS[0] + X_E, GIDER_GIRIS[1], GIDER_GIRIS[2]),
            abs(gb.BoundingBox().xmin - GIDER_PLAN[0][0]) < 1e-3 and abs((b0.ymin + b0.ymax) / 2.0 - GIDER_GIRIS[1]) < 0.05 and abs((b0.zmin + b0.zmax) / 2.0 - GIDER_GIRIS[2]) < 0.05
            and min(SH[a].BoundingBox().xmin for a in YN if a.startswith("ealt_gider_")) >= GIDER_PLAN[0][0] - 1e-3)
    sl = [(xx, gb.intersect(kut(xx - 0.5, xx + 0.5, 0, 400, -800, -700).val()).BoundingBox().ymin) for xx in (-395.0, -300.0, -100.0, 100.0, 200.0)]
    ge = [(a_["inv"] - b_["inv"]) / (b_["s"] - a_["s"]) for a_, b_ in zip(E_[2:4], E_[3:5])]
    kontrol("GIDER (kati olcusu): boru alt yuzu x %s → %s (Ø12 bolumunde egim %%%.2f)" % (" / ".join("%.0f" % s_[0] for s_ in sl), " / ".join("%.2f" % s_[1] for s_ in sl),
            100.0 * (sl[2][1] - sl[4][1]) / 300.0), (sl[2][1] - sl[4][1]) / 300.0 >= GIDER_EGIM - 1e-4 and all(sl[i][1] > sl[i + 1][1] for i in range(1, 4)))
    import kesme_cad_v11 as KS
    if not KS.PARCALAR:
        KS.modul()
    kesici = dict((a, _tek(k)) for a, k, _n in K_DUVAR_DELIKLERI)
    KP = []
    for p in KS.PARCALAR:
        if p["grup"] in ("URUN", "URUN_IZ", "REF", "SPREY"): continue
        s = _tek(p["wp"])
        if p["ad"] in kesici:
            s = s.cut(kesici[p["ad"]])
        KP.append(("K:" + p["ad"], s.translate(V(DX_K, 0, 0))))
    GD = [(a, SH[a]) for a in YN if a.startswith("ealt_gider_")]
    c7 = capraz(GD, KP)
    for x_ in c7[:8]: print("   %10.3f mm3  %s  <->  %s" % x_)
    kontrol("GIDER ↔ K (kesme_cad_v11, %d parca · duvar delikleri K_DUVAR_DELIKLERI ile kesilmis) > 0,1 mm³ = 0" % len(KP), not c7, "%d bulgu" % len(c7))
    KPd = dict(KP)
    tas = _mesafe(gb, KPd["K:taban_sac_tasiyici_380"]); tas0 = _mesafe(gb, KPd["K:taban_sac_tasiyici_20"])
    tv = _mesafe(gb, KPd["K:yag_damlama_tavasi_10"]); tp = _mesafe(gb, KPd["K:yag_tarti_platformu"])
    print("   GIDER ↔ K: sag taban tasiyicisi (ust y 156) %.2f mm · sol tasiyici %.2f · yag tavasi %.1f · tarti platformu %.1f" % (tas, tas0, tv, tp))
    kontrol("GIDER ↔ K SAG TABAN TASIYICISI (30×30×2 ust y 156, x 4365–4395) aralik %.2f mm ≥ 0 (kesisim yok) · HEDEF ≥ %.0f → %s"
            % (tas, KUCUK_PAY, "TUTMUYOR: B cikisi (y %.0f) %%1 inisle K'yi ancak %.2f mm ile geciyor → B cikisi ≥ y %.1f olmali (AÇIK)" % (GIDER_GIRIS[1], tas, GIDER_GIRIS[1] + KUCUK_PAY - tas)
               if tas < KUCUK_PAY else "TAMAM"), tas >= 0.0)
    ara7 = {}
    for c in ("asansor_arabasi", "asansor_arabasi_00", "asansor_ray_plakasi", "asansor_ray_plakasi_flansi", "sarjor_kapi_esigi", "asansor_rayi_0", "asansor_catali_0", "taban_sac_3"):
        ara7[c] = _mesafe(gb, SH[c])
    kontrol("GIDER ↔ E (en alt asansor konumu): %s · hepsi ≥ %.0f (taban sacina kelepce ayaklari basar)"
            % (" · ".join("%s %.1f" % kv for kv in ara7.items()), KUCUK_PAY), all(v >= KUCUK_PAY for c, v in ara7.items()))
    tb = SH["ealt_secop_buharlastirma_tavasi"].BoundingBox(); vb = SH["ealt_gider_cek_valfi"].BoundingBox()
    kontrol("TAVA: gider ordek gagasi alti y %.2f ≥ tava agzi %.1f + 1,5 · gaga x %.1f–%.1f · z %.1f…%.1f tava icinde (x %.0f–%.0f · z %.0f…%.0f)"
            % (vb.ymin, tb.ymax, vb.xmin, vb.xmax, vb.zmin, vb.zmax, tb.xmin, tb.xmax, tb.zmin, tb.zmax),
            vb.ymin >= tb.ymax + 1.5 - 1e-6 and tb.xmin < vb.xmin and vb.xmax < tb.xmax and tb.zmin < vb.zmin and vb.zmax < tb.zmax)
    # ---- 8 · TAVA KAPASİTESİ + BUHARLAŞMA (sıcak gaz) · PANO ISI ----
    Ai = (tb.xlen - 2 * TAVA_T) * (tb.zlen - 2 * TAVA_T) / 1e6
    Vi = Ai * (tb.ymax - 3.0 - (tb.ymin + TAVA_T))                  # m² × mm = L
    def p_s(T):  # doymuş buhar basıncı kPa (Magnus)
        return 0.61094 * math.exp(17.625 * T / (T + 243.04))
    def x_s(T):  # doymuş nem oranı kg/kg (101,325 kPa)
        return 0.622 * p_s(T) / (101.325 - p_s(T))
    pa = 0.5 * p_s(32.0)
    xa = 0.622 * pa / (101.325 - pa)                 # emiş havası 32 °C %50
    th = 25.0 + 19.0 * 1.0
    g_sg = th * Ai * (x_s(45.0) - xa) * 24.0; g_hv = th * Ai * (x_s(23.8) - xa) * 24.0
    print("   TAVA: ic alan %.4f m² · su hacmi (agzin 3 alti) %.2f L · defrost basina ≤ 0,25 L (B: gunde 4 defrost ≤ 1 L VARSAYIM)" % (Ai, Vi))
    print("   BUHARLASMA (VDI 2089 / Carrier: Θ = 25 + 19 v kg/m²h · emiş havasi 32 °C %%50 · v ≈ 1 m/s): sicak gazla su 45 °C → %.2f kg/gun · ısıtmasız (yas termometre 23,8 °C) → %.2f kg/gun"
          % (g_sg, g_hv))
    kontrol("TAVA KAPASITESI %.2f L ≥ 0,25 (bir defrost) · SICAK GAZLA buharlasma %.1f kg/gun ≥ 1,0 (ısıtmasız %.2f yetmez → serpantin ŞART)" % (Vi, g_sg, g_hv),
            Vi >= 0.25 and g_sg >= 1.0)
    Pp = 24.0
    kontrol("PANO ISISI %.0f W (store_cad_v14 PANO_W) emiş akişinda (551 m³/h): hava %.2f K isinir · pano emiş (serin) tarafinda" % (Pp, Pp / (1.2 * 1005.0 * 551.0 / 3600.0)),
            SH["ealt_pano_pano_montaj_plakasi"].BoundingBox().xmax < X_AYIRICI[0] and SH["ealt_pano_guc_kaynagi_NDR-240-24"].BoundingBox().xmax < X_AYIRICI[0])
    # ---- 9 · SERVİS YOLU: ünite (+ pedler + contalar) öne kayar · Z ayırıcı sökülür ----
    UNG = UN + ["ealt_secop_sogutma_grubu_taban_contasi", "ealt_secop_k4_kondenser_contasi"] + [a for a in YN if a.startswith("ealt_secop_sogutma_grubu_takozu_")]
    SOK = {"ealt_perde_ayirici_sokulur", "ealt_perde_ayirici_sabit", "ealt_perde_ayirici_on_contasi", "ealt_perde_conta_taban_yani_on", "ealt_secop_sicak_gaz_serpantini"} | set(KUTU_KANAT)
    SAB = [(a, s) for a, s in DIGER + YS if a not in UNG and a not in SOK]
    bul9 = []
    for dz in (50.0, 150.0, 300.0, 450.0):
        bul9 += [(v, a + "@+%.0f" % dz, c) for v, a, c in capraz([(a, SH[a].translate(V(0, 5.0, dz))) for a in UNG], SAB)]
    kontrol("SERVIS: kanatlar acik · Z ayirici (sabit bant + sokulur) + on conta + on taban contasi + serpantin (tavadan kaldirilir) sokuk → unite 5 mm kaldirilip one "
            "+50 / 150 / 300 / 450 ↔ sabitler (raylar, dudak, tava, pano, gider dahil) = 0", not bul9, str(bul9[:4]))
    # ---- 10 · montaj uyumu ----
    ion = icecek_on_olcum()
    kontrol("MONTAJ UYUMU: icecek_on_olcum() assert'i gecer (on [] · sutun engelsiz) · ICECEK_YEDEK kutu %d · koli %d · E_ALT_BIRIM %s" % (
        ICECEK_YEDEK["kutu"], ICECEK_YEDEK["koli"], [k for k, _a, _o in E_ALT_BIRIM]),
            ion["on"] == [] and not ion["sutun"][0]["engel"] and not ion["sutun"][1]["engel"] and ICECEK_YEDEK["kutu"] == 0)
    ge_ = min(_tek(p["wp"]).BoundingBox().ymin for p in PARCALAR if p["grup"] == "SABIT" and not p["ad"].startswith(("ayak_", "plint_on", "onyuz_plint", "asansor_")))
    kontrol("MONTAJ UYUMU: SABIT govde alti %.2f = Y_PLINT %.0f (montaj _ge denetimi) · yeni parcalarin en alti %.1f · en onu %.1f ≤ +79" % (
        ge_, Y_PLINT, min(s.BoundingBox().ymin for _a, s in YS), max(s.BoundingBox().zmax for _a, s in YS)),
            abs(ge_ - Y_PLINT) < 0.05 and max(s.BoundingBox().zmax for _a, s in YS) <= Z_ON + 1e-6)
    print("   SOGUTMA HATTI (MODELLENMEDI): %s" % SOGUTMA_HAT_ACIK)
    kal = [d for d in DEN if not d[1]]
    print("DENETIM h2_kutu_v1: %d madde · %d KALDI · %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    return DEN


if __name__ == "__main__":
    modul()
    D = denetim()
    kal = [d[0] for d in D if not d[1]]
    assert not kal, kal
    sys.stdout.flush(); os._exit(0)
