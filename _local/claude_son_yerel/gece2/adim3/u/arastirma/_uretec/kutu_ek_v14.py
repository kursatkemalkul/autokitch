# ================================================================ E v14 (30 Eyl 2026 · Claude) ================================================================
# kutu_cad_v14 = kutu_cad_v13 + bu ek (yap_kutu_cad_v14.py). Kemal (30 Eyl, ekran görüntüsü): "bu neden kesik yarım ve oradaki yatay parça havada"
#  1 · AĞIZ ÜST KİRİŞİ KALKTI — 15 × 20 çelik çubuk (x 21,5–808,5 · y 1162–1177 · z 29–49). v1'de "ön köşe plow'larını taşır" diye kondu; plow'lar hiç
#      modellenmedi, v10'da yerlerine 4 motorlu köşe katlayıcı geldi → kirişin taşıdığı parça YOK: yalnız iki ucundaki ön dikmelere değiyor
#      (parça kutusu taraması). Ön dikmeler montajda ön kapaklarla birlikte saydam çizildiği için (ON_SEFFAF ^onyuz_) kiriş görüntüleyicide
#      havada duruyordu. Robot ağzı y 886–1062 → kiriş ağzın 100 mm ÜSTÜNDE (ağız kenarı değil); ön panellere de değmiyor (arkalarında 10 mm).
#      Ön çerçeve zaten 2 tam boy dikme + 2 kayıt (orta y 853–883 · üst y 1275–1305) — sağ servis kapağının arkasını da boşaltır.
#  2 · SAĞ ÖN DİKEY KABLO KANALI TEK PARÇA — v10'dan önce kiriş z −40…−20'de kanalın (z −50…−25) İÇİNDEN geçtiği için kanal y 1157–1177 arasında
#      20 mm kesikti (alt + üst iki parça). v10 kirişi z 29–49'a aldı, kesik boş kaldı ("kesik yarım"). Şimdi y 126–1827 tek boy 1701 mm.
# Kinematik v13 ile BİREBİR (hareketli parça yok) → K ↔ E ↔ montaj saatleri değişmez.

V14_CIKAN = ("agiz_ust_kirisi", "kablo_kanali_dikey_alt", "kablo_kanali_dikey_ust")
KANAL_DIKEY_V14 = dict(x=(806.0, 826.0), y=(Y_PLINT + 3.0, 1827.0), z=(-50.0, -25.0))   # v13'ün iki parçasının dış zarfı, kesiksiz
V14_YENI, V14_DEGISEN = [], []


def kiris_ve_kanal_v14():
    ad = {q["ad"]: q for q in PARCALAR}
    for n in V14_CIKAN:
        assert n in ad, ("v13'te beklenen parça yok", n)
    b = ad["agiz_ust_kirisi"]["wp"].val().BoundingBox()
    assert all(abs(u - v) < 0.05 for u, v in zip((b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax), (SAC + 20.0, W - SAC - 20.0, 1162.0, 1177.0, 29.0, 49.0))), \
        ("ağız üst kirişi v13 yerinde değil", b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)
    a_, u_ = ad["kablo_kanali_dikey_alt"]["wp"].val().BoundingBox(), ad["kablo_kanali_dikey_ust"]["wp"].val().BoundingBox()
    K_ = KANAL_DIKEY_V14
    assert abs(a_.ymin - K_["y"][0]) < 0.05 and abs(a_.ymax - 1157.0) < 0.05 and abs(u_.ymin - 1177.0) < 0.05 and abs(u_.ymax - K_["y"][1]) < 0.05, "kanal v13 ölçüsünde değil"
    assert all(abs(p.xmin - K_["x"][0]) < 0.05 and abs(p.xmax - K_["x"][1]) < 0.05 and abs(p.zmin - K_["z"][0]) < 0.05 and abs(p.zmax - K_["z"][1]) < 0.05 for p in (a_, u_))
    PARCALAR[:] = [q for q in PARCALAR if q["ad"] not in V14_CIKAN]
    ekle("kablo_kanali_dikey", kut(K_["x"][0], K_["x"][1], K_["y"][0], K_["y"][1], K_["z"][0], K_["z"][1]), "plastik",
         bom=("Kablo kanalı 20 × 25 (dikey)", 1, "sağ ön köşe · x 806–826 · y %.0f–%.0f tek boy %.0f (v14: eski kiriş kesiği kalktı)" % (K_["y"][0], K_["y"][1], K_["y"][1] - K_["y"][0]),
              "katalog ölçüsü VARSAYIM · 2 m boydan kesilir [V]"))


_v13_modul_v14 = modul


def modul():
    r = _v13_modul_v14()
    once = set(q["ad"] for q in PARCALAR)
    kiris_ve_kanal_v14()
    V14_YENI[:] = [q["ad"] for q in PARCALAR if q["ad"] not in once]
    return r
