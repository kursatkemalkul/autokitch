# -*- coding: utf-8 -*-
"""HAT v3.2 · ELEKTRİK TESİSATI v1 (30 Eyl gece · Claude · YEREL) — Kemal: "elektrik tesisatını tüm detaylarıyla kur, kablolar vs · havada olmasın,
kıskaçlarla duvarlara · motorlar, beyin, sürücüler de nereye konması gerekiyorsa oraya · ana PC ekransız, iPad / telefondan takip".
MİMARİ (yıldız · her istasyon kendi panosunda · ana pano QR'de, tasarımdaki yeri):
  BİNA 400 V 3F (CEE 32 A, QR tabanındaki zemin kutusundan) → QR ANA PANO: ana şalter · kaçak akım 30 mA · 6 sigorta (TOPPING · DOLAP · K · E · ROBOT · QR) ·
  24 V · ANA BİLGİSAYAR (RevPi Connect 4, ekransız, DIN) · 8 port endüstriyel switch (yıldız Ethernet: 4 istasyon PLC + robot + QR kilit kartı + 4G/Wi-Fi modem)
  → QR orta dikey kanalı → zemin kanalı (güç bölmesi) → zemin kanalı uzantısı (ray altından makine önüne) → DOLAP (teknik sütun, alttan) · E sağ-ön DIŞ
  dikey kanal → U_KE → üst hat kanalı (U_KE · U_F · TOPPING kuru bölme arkası) → K · E · TOPPING panolarına rakorlu iniş.
  Fırın (400 V 32 A) ve kompresör bina tesisat bandından (mevcut arka rakorları) — ayrı devre.
  iPad / telefon: ana bilgisayarın web paneli · modem (QR kilit kartı yanında, 4G + Wi-Fi) üzerinden (yerel Wi-Fi ya da uzaktan VPN).
v3.6 (1 Eki 2026 · Claude · YEREL): ANA PANO + BEYİN QR'dan U_F'ye (h3_ana_pano_v1, başka üreteç) · bu katman: QR istasyon kutusu · her istasyonda Harting Han 10B
  (TOPPING · K · E · DOLAP · A · F · QR · ROBOT) · ana hat (tek güç + tek veri) U_F → kanallar → istasyonlar · bina beslemesi zemin kanalından ana panoya ·
  A çevresindeki kanal / demet / emniyet kabloları kalktı · zemin üstü kanal ön ayakların arkasında · plint delikleri yok.
SÖZLEŞME (h3_ust_depo_v2 / bulasik_cad_v2 gibi): kur() · PARCALAR [ad, wp, mal, birim, grup, kaynak, bom] (DÜNYA) · dunya(p) · BIRIMLER · BIRIM_MODUL · MALZEME ·
  + DELIKLER [(modul, parça adı, dünya kesici, not)] (montaj başka modüllerin saclarına keser) · DUSUR [(modul, parça adı)] (montaj yerine yenisini koyar)."""
import math, os, sys, time
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_hesap_v1 as HS
import h3_elk_ortak as EO
from h3_elk_ortak import kut, sil, boru, kanal, kelepce, rakor

V = cq.Vector
Z_ON = 79.0
PARCALAR, DELIKLER, DUSUR = [], [], []
BIRIMLER_ = []
BIRIMLER = [
    ("ELK_QR_KUTU", "v3.6 · QR İSTASYON KUTUSU 300 × 220 × 200 (304, eski ana panonun yerinde): iC60N C10 · Mean Well NDR-120-24 (göz cihazları 24 V) · "
                    "Phoenix FL SWITCH 1008N · 10 klemens · üstte Harting Han 10B (ana hat: tek güç + tek veri) · altta 3 rakor (göz demeti · kart + modem · UPS)"),
    ("ELK_QR_KABLO", "QR içi kablolama: orta dikey yassı kanal (ana pano ↔ zemin) · göz cihazları (kapak motoru · sensör · mandal · ısıtıcı) demetleri dikmelerde P-kelepçeli · kilit kartına"),
    ("ELK_QR_MONTAJ", "QR göz cihaz montajı (braketler · kulaklar · menteşe ara plakaları) + v3.7 tam boy çentikli alt servis kapağı + 2 kablo giriş plakası (tekmelik kalktı)"),
    ("ELK_TOPPING", "TOPPING (+ A · F yükleme bandı) cihaz kabloları → kuru bölme panosu / sürücüler: kaset motorları · evaporatör fanları · sürücüler · valf adası · soğutma grubu KLF6.6 · "
                    "enerji zinciri sabit ucu · sabit tahrik motoru · x sıfır / limit sensörleri · tabla boş sensörü · kuru bölme tabanı rakorları (G1 · G2 · G3)"),
    ("ELK_K", "K cihaz kabloları → K panosu: EC5000 bant motoru · 4 ürün sensörü · DGRF sensörleri · itici X sensörleri · PulsaJet · yağ pompası + PM1704 · tartı yük hücresi (F|K duvarı rakoru G4)"),
    ("ELK_DOLAP", "Dolap cihaz kabloları: 21 çekmece reed sensörü → kolon kablo kanalları (motor M12 soketleri kanala dayalı) · Secop NLE8.8CN + 4 evaporatör fanı → kanallar / pano"),
    ("ELK_ANA_HAT", "Ana hat (v3.6 · U_F ana pano → istasyonlar, tek güç + tek veri / istasyon): üst hat kanalı U_KE 60 × 40 + U_F + TOPPING kuru bölmesi → A (U_A) 60 × 22 · "
                    "gövde kanalı + ana besleme kanalı (kuru bölme → C kaidesi → fırın altı → teknik sütun) · dolap dikey + pano altı kanalı · "
                    "K / E / TOPPING Harting Han 10B girişleri (soket istasyonda, fiş ana hat ucunda)"),
]
BIRIMLER += [("ELK_K_TARTI", "v3.7 · K yağ tartısı yük hücresi kablosu (tartı F üstü kabinde, K'nin onaylı istisnası) + F|K duvarı G4 rakoru · modüller arası (gerçek katı kesişimi 0)")]
BIRIMLER += [("ELK_ISTASYON", "İSTASYON GİRİŞLERİ + ANA PANO FİŞLERİ: A · F · DOLAP istasyon kutuları (v3.7 DOLAP teknik sütun arka bölmesinde, servis yüksekliği) · Harting Han 10B soket / fiş / M32 · ana pano soketlerine fiş")]
BIRIMLER += [("ELK_ZEMIN_KANALI", "Zemin ÜSTÜ kablo kanalı (gömme yok · v3.6 ön ayak sırasının arkasında, etekler kalktı): QR girişi başlığı → koridorun kör ucu (rampalı) → E / dolap altı → teknik sütun altı (+ DOLAP Harting fişi) · bina beslemesi kolu (bağlantı kutusu → kör uç) · kapaklar")]
BIRIMLER = BIRIMLER_ + BIRIMLER
BIRIM_MODUL = {"ELK_K_TARTI": "-", "ELK_QR_KUTU": "S", "ELK_ISTASYON": "-", "ELK_QR_KABLO": "S", "ELK_QR_MONTAJ": "S", "ELK_ANA_HAT": "-", "ELK_TOPPING": "C", "ELK_K": "K", "ELK_DOLAP": "B", "ELK_ZEMIN_KANALI": "-"}
MALZEME = {"pano": dict(renk=(0.86, 0.87, 0.88, 1.0), met=0.3, ruf=0.5), "din": dict(renk=(0.75, 0.77, 0.79, 1.0), met=0.9, ruf=0.3),
           "cihaz": dict(renk=(0.93, 0.93, 0.92, 1.0), met=0.0, ruf=0.6), "cihaz_koyu": dict(renk=(0.20, 0.21, 0.23, 1.0), met=0.1, ruf=0.5),
           "kanal": dict(renk=(0.62, 0.64, 0.66, 1.0), met=0.0, ruf=0.7), "kablo": dict(renk=(0.10, 0.10, 0.11, 1.0), met=0.0, ruf=0.6),
           "kablo_veri": dict(renk=(0.12, 0.35, 0.62, 1.0), met=0.0, ruf=0.6), "rakor": dict(renk=(0.14, 0.14, 0.15, 1.0), met=0.0, ruf=0.5),
           "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35), "paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30),
           "on_seffaf": dict(renk=(0.85, 0.88, 0.90, 0.25), met=0.0, ruf=0.1),
           "ayirici_kirmizi": dict(renk=(0.80, 0.08, 0.06, 1.0), met=0.0, ruf=0.5), "ayirici_sari": dict(renk=(0.98, 0.80, 0.05, 1.0), met=0.0, ruf=0.5)}
BOM_KAYNAK = "katalog adı · ölçü [VARSAYIM: föyden teyit]"


def ekle(ad, sh, mal, birim, bom=None, kaynak="h3_elektrik_v1"):
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=cq.Workplane(obj=sh), mal=mal, birim=birim, grup="SABIT", kaynak=kaynak, bom=bom))


def dunya(p):
    v = p["wp"].vals()
    return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])


def kablo(ad, pts, r, birim, mal="kablo", bom=None, kel=None):
    """kablo + (varsa) P-kelepçeleri · kel: [(segment, (yüzey koordinatı, yön))]"""
    ekle(ad, boru(pts, r), mal, birim, bom)
    for j, (_p, s) in enumerate(EO.kelepceler(pts, r, kel or [])):
        ekle("%s_kelepce_%d" % (ad, j), s, "celik", birim,
             bom=("P-kelepçe paslanmaz (kablo Ø%.0f) + M4 vida" % (2 * r), 1, "yüzeye vidalı / perçin somunlu", "") if j == 0 else None)


# ================================================================ KUR ================================================================
import h3_elk_qr_v1 as EQ
import h3_elk_hat_v1 as EH
import h3_elk_ist_v1 as EI
import h3_elk_rota as ER


ETEK_KALKAN = {"B_KASA|onyuz_plint", "B_KASA|onyuz_plint_donus_sol", "B_KASA|onyuz_plint_donus_sag", "E_GOVDE|onyuz_plint"}   # v3.6 montaj (QR tekmeliği kalır)


def dunya_ekle():
    """v3.7b · döküm (_dunya) U_F fanları / termostatı / baca kılıfı ve davlumbaz fanından ÖNCE alındı → h3_ust_depo_v2 + h3_firin_ust_v1'in dökümde OLMAYAN
    parçaları yol + çakışma dünyasına eklenir (montaj sonraki dökümde zaten içerir; aynı ad varsa dokunulmaz)"""
    import h3_ust_depo_v2 as UD_, h3_firin_ust_v1 as FU_
    var = set(d_[0] for d_ in EO.dokum()); n_ = 0
    for M_ in (UD_, FU_):
        if not M_.PARCALAR: M_.kur()
        for p_ in M_.PARCALAR:
            k_ = "%s|%s" % (p_["birim"], p_["ad"])
            if k_ in var: continue
            s_ = M_.dunya(p_); b_ = s_.BoundingBox()
            EO.dokum().append((k_, s_, (b_.xmin, b_.xmax, b_.ymin, b_.ymax, b_.zmin, b_.zmax))); n_ += 1
    print("v3.7b · dökümde olmayan U / F üstü parçası eklendi: %d" % n_)


def kur():
    t0 = time.time()
    PARCALAR[:] = []; DELIKLER[:] = []; DUSUR[:] = []
    import qr_cad_v1 as QR
    if not QR.PARCALAR: QR.kur()
    EQ.kur(ekle, DELIKLER, DUSUR, QR)
    EH.kur(ekle, DELIKLER, DUSUR)
    # v3.4 · düşen (DUSUR) makine parçaları yol bulma dünyasından da çıkar (ör. QR'nin eski alt servis kapağı: yerine kısa kapak + alt ön bant)
    _ON = {"QR": ("QR_",), "TC": ("TOPPING_MODUL",), "TU": ("TOPPING",), "KS": ("K_",), "KC": ("E_",), "SC": ("B_", "CEK_"), "FU": ("F_",), "UD": ("U_",),
           "RE": ("ROBOT", "ZEMIN"), "AK": ("A_",), "FT": ("F_TP10",), "KD": ("KAIDE_",)}
    _DS = [(_ON.get(m_, (m_,)), a_) for m_, a_ in DUSUR]
    _n0 = len(EO.dokum())
    EO.dokum()[:] = [d_ for d_ in EO.dokum() if not any(d_[0].split("|", 1)[0].startswith(p_) and d_[0].split("|", 1)[1] == a_ for p_, a_ in _DS)]
    print("v3.4 · yol dünyasından düşen parça: %d" % (_n0 - len(EO.dokum())))
    _n1 = len(EO.dokum())                                                             # v3.6 · montaj alt etekleri kaldırır (yol + çakışma dünyasından da çıkar)
    EO.dokum()[:] = [d_ for d_ in EO.dokum() if d_[0] not in ETEK_KALKAN]
    print("v3.6 · yol dünyasından düşen alt etek: %d" % (_n1 - len(EO.dokum())))
    dunya_ekle()
    for p in PARCALAR: ER.ekli_ekle(p["ad"], dunya(p))
    R = EI.kur(ekle, DELIKLER, DUSUR)
    ACIK_SOKET = EH.istasyon_kur(ekle, DELIKLER, DUSUR, ER, R, PARCALAR)                     # v3.6 · A + F kutuları · DOLAP Harting · ana pano fişleri + toplama kanalı
    print("İSTASYON KABLOLARI: %d yol · %d BULUNAMADI · %d askıda parça" % (len(R["yol"]), len(R["bulunamadi"]), len(R["askida"])))
    for x in R["bulunamadi"]: print("   BULUNAMADI:", x[0], [round(v) for v in x[1]], "→", [round(v) for v in x[2]], "engel:", x[3])
    for x in R["askida"][:30]: print("   ASKIDA:", x[0], [round(v) for v in x[3]])
    _birim_duzelt()
    print("h3_elektrik_v1 · %d parça · %d delik · %d düşen · %.0f sn" % (len(PARCALAR), len(DELIKLER), len(DUSUR), time.time() - t0))
    return PARCALAR


def _birim_duzelt():
    """döşeme altı zemin kanalı parçaları ayrı birim (koridorda · makine ön yüz kuralının dışında, ZEMIN_KANALI gibi)"""
    for p in PARCALAR:
        if p["ad"].startswith(("zemin_kanali_", "zemin_ustu_")): p["birim"] = "ELK_ZEMIN_KANALI"


def denetim(haric_ek=()):
    """yeni parçalar ↔ montaj dökümü (düşürülen / delinecek parçalar hariç) · yeni ↔ yeni"""
    if not PARCALAR: kur()
    kes = set(a for m, a, k, n in DELIKLER) | set(a for m, a in DUSUR)
    bul = []
    for p in PARCALAR:
        s = dunya(p)
        for ad, v in EO.cakisma(s):
            if ad.split("|", 1)[1] in kes: continue
            bul.append((v, p["ad"], ad))
    for v, a, c in sorted(bul, reverse=True)[:60]: print("   ÇAKIŞMA %8.1f mm³  %-40s ↔ %s" % (v, a, c))
    print("ÇAKIŞMA (yeni ↔ makine): %d" % len(bul))
    return bul


ONB = os.path.join(H3, "_elk")                                                     # üretilen elektrik katmanı önbelleği (montaj buradan yükler)


def kaydet():
    import io, json
    os.makedirs(ONB, exist_ok=True)
    cq.Compound.makeCompound([dunya(p) for p in PARCALAR]).exportBrep(os.path.join(ONB, "elk.brep"))
    cq.Compound.makeCompound([k for m, a, k, n in DELIKLER]).exportBrep(os.path.join(ONB, "delik.brep"))
    json.dump(dict(parca=[[p["ad"], p["mal"], p["birim"], list(p["bom"]) if p["bom"] else None] for p in PARCALAR],
                   delik=[[m, a, n] for m, a, k, n in DELIKLER], dusur=[list(d) for d in DUSUR]),
              io.open(os.path.join(ONB, "elk.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("h3_elektrik_v1 · önbellek yazıldı: %d parça · %d delik · %d düşen → %s" % (len(PARCALAR), len(DELIKLER), len(DUSUR), ONB))


def _cocuklar(sh):
    from OCP.TopoDS import TopoDS_Iterator
    it = TopoDS_Iterator(sh.wrapped); out = []
    while it.More():
        out.append(cq.Shape.cast(it.Value())); it.Next()
    return out


def yukle():
    """montaj: kur()'u (yol bulucu ~15 dk) koşmadan önbellekten PARCALAR / DELIKLER / DUSUR"""
    import io, json
    J = json.load(io.open(os.path.join(ONB, "elk.json"), encoding="utf-8"))
    P_ = _cocuklar(cq.Shape.importBrep(os.path.join(ONB, "elk.brep")))
    D_ = _cocuklar(cq.Shape.importBrep(os.path.join(ONB, "delik.brep")))
    assert len(P_) == len(J["parca"]) and len(D_) == len(J["delik"]), (len(P_), len(J["parca"]), len(D_), len(J["delik"]))
    PARCALAR[:] = []; DELIKLER[:] = []; DUSUR[:] = []
    for (ad, mal, bir, bom), sh in zip(J["parca"], P_):
        PARCALAR.append(dict(ad=ad, wp=cq.Workplane(obj=sh), mal=mal, birim=bir, grup="SABIT", kaynak="h3_elektrik_v1", bom=tuple(bom) if bom else None))
    for (m, a, n), k in zip(J["delik"], D_): DELIKLER.append((m, a, k, n))
    for m, a in J["dusur"]: DUSUR.append((m, a))
    _birim_duzelt()
    print("h3_elektrik_v1 · önbellekten: %d parça · %d delik · %d düşen" % (len(PARCALAR), len(DELIKLER), len(DUSUR)))
    return PARCALAR


if __name__ == "__main__":
    kur()
    bul_ = denetim()
    kaydet()
    sys.stdout.flush(); os._exit(0)
