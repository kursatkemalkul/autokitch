# -*- coding: utf-8 -*-
"""h3_ust_depo_v1.py → h3_ust_depo_v2.py (HAT v3.2): U_F'e (fırın üstü kutu yığınının TAM ÜSTÜ) pizza kutusu yedeği — Kemal: "kutular 4 günlük değil,
üstündeki rafa da ekle". Raf 1,5 + 3 taşıyıcı profil (U_KE içecek rafıyla aynı dil: alt kayıtın 1,5 üstü → kutular düz sürülür) + 170 kutu (tavan kirişinin 0,5 altı)."""
import io, os
H3 = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(H3, "h3_ust_depo_v1.py"), encoding="utf-8").read()
N = [0]


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, "yama bulunamadı (%d ≠ %d): %r" % (c, n, a[:120])
    s = s.replace(a, b); N[0] += 1


rep('''"""HAT VERSİYON 2 · ÜST DEPO (modül U) v1''', '''"""HAT v3.2 · ÜST DEPO v2 (30 Eyl gece · Claude): v1 + U_F'de PİZZA KUTUSU YEDEĞİ (fırın üstü 320'lik yığının tam üstünde, raf 1895, 170 kutu) —
Kemal: "kutular 4 günlük değil, üstündeki rafa da ekle" · şarjör 419 (beslenebilir) + fırın üstü 320 + U_F 170 = 909 ≥ 4 gün 720 (v3.1: 739, pay yalnız 19).
--- v1 ---
HAT VERSİYON 2 · ÜST DEPO (modül U) v1''')
rep('''KOLI_ON = RAF_Z[1] - 2.0                                            # ön sıra kolinin önü +23''',
    '''KOLI_ON = RAF_Z[1] - 2.0                                            # ön sıra kolinin önü +23
# v2 · pizza kutusu yedeği (U_F) — fırın üstü yığınla AYNI iz (firin_ust_kabin_cad_v1.PIZZA x 2520–3324 · z −424…−20) · kutu 1,6 (düz açılım 804 × 404)
KUTU_T = 1.6
PZ_X, PZ_Z = (2520.0, 3324.0), (-424.0, -20.0)
PZ_RAF_X = (PZ_X[0] - 5.0, PZ_X[1] + 5.0)                          # raf yığından 5 taşar
PZ_TAVAN = 2168.5                                                   # U_F tavan kirişi altı (2785–2815 yığının üstünden geçer)
PZ_ADET = int((PZ_TAVAN - 0.5 - RAF_Y[1]) / KUTU_T)                  # 170 · yığın üstü tavan kirişinin ≥ 0,5 altında (fırın üstü kuralıyla aynı pay)
KUTU_YEDEK = dict(kutu=0)''')
rep('''    ("U_ICECEK_YEDEK", "İçecek yedeği 6 koli × 24 = 144 kutu (3 yan yana × 2 sıra · koli 400 × 267 × 123) · U_KE rafında, soğutmasız · dolaptaki 144 ile 288 ≥ 4 gün 277"),''',
    '''    ("U_ICECEK_YEDEK", "İçecek yedeği 6 koli × 24 = 144 kutu (3 yan yana × 2 sıra · koli 400 × 267 × 123) · U_KE rafında, soğutmasız · dolaptaki 144 ile 288 ≥ 4 gün 277"),
    ("U_KUTU_YEDEK", "v3.2 · PİZZA KUTUSU YEDEĞİ U_F rafında (fırın üstü 320'lik yığının tam üstü) · 170 düz kutu 804 × 404 × 1,6 · şarjör 419 + fırın üstü 320 + 170 = 909 ≥ 4 gün 720"),''')
rep('''def kur():
    PARCALAR[:] = []
    KAPAK_EKSEN.clear()
    for k in KUTULAR:
        kutu(k)
    baca()
    icecek()
    return PARCALAR''', '''def kutu_yedegi():
    """v2 · U_F: raf (1,5) + 3 taşıyıcı profil (z boyunca, yığının iki ucu + ortası) + 170 düz pizza kutusu (tek yığın)"""
    xs = [(PZ_RAF_X[0], PZ_RAF_X[0] + PROFIL), ((PZ_X[0] + PZ_X[1]) / 2.0 - PROFIL / 2.0, (PZ_X[0] + PZ_X[1]) / 2.0 + PROFIL / 2.0), (PZ_RAF_X[1] - PROFIL, PZ_RAF_X[1])]
    rz = (PZ_Z[0] - 6.0, RAF_Z[1])
    for i, (xa, xb) in enumerate(xs):
        ekle("ust_f_raf_kirisi_%d" % i, kutu_profil_z(xa, xb, Y_TABAN[1], RAF_Y[0], rz[0], rz[1]), "paslanmaz", "U_F_GOVDE",
             bom=("Raf taşıyıcı profil 304 kutu 30 × 30 × 2 · L %.0f" % (rz[1] - rz[0]), 3, "üretim", "U_F tabanına kaynaklı · kutu rafının altında", "ÜRETİM") if i == 0 else None)
    ekle("ust_f_kutu_rafi", kut(PZ_RAF_X[0], PZ_RAF_X[1], RAF_Y[0], RAF_Y[1], rz[0], rz[1]), "sac", "U_F_GOVDE",
         bom=("Kutu rafı 304 1,5 · %.0f × %.0f" % (PZ_RAF_X[1] - PZ_RAF_X[0], rz[1] - rz[0]), 1, "lazer",
              "3 profile punta · raf üstü 1895 > alt kayıt üstü 1893,5 → kutular düz sürülür (U_KE içecek rafı gibi)", "ÜRETİM"))
    y1 = RAF_Y[1] + PZ_ADET * KUTU_T
    ekle("ust_f_pizza_kutusu_yigini", kut(PZ_X[0], PZ_X[1], RAF_Y[1], y1, PZ_Z[0], PZ_Z[1]), "karton", "U_KUTU_YEDEK",
         bom=("Pizza kutusu yedeği (düz açılım, sarf)", PZ_ADET, "804 × 404 × 1,6 · 32 × 32 × 4,2 E-dalga", "v3.2 · fırın üstü 320'lik yığının tam üstü · operatör şarjöre buradan besler", "SARF"))
    KUTU_YEDEK.update(x=PZ_X, y=(RAF_Y[1], y1), z=PZ_Z, kutu=PZ_ADET, yer="U_F", tavan_pay=PZ_TAVAN - y1)
    assert PZ_TAVAN - y1 >= 0.5 - 1e-9 and PZ_ADET >= 150, KUTU_YEDEK


def kur():
    PARCALAR[:] = []
    KAPAK_EKSEN.clear()
    for k in KUTULAR:
        kutu(k)
    baca()
    icecek()
    kutu_yedegi()
    return PARCALAR''')
io.open(os.path.join(H3, "h3_ust_depo_v2.py"), "w", encoding="utf-8").write(s)
print("h3_ust_depo_v2.py yazıldı · %d yama" % N[0])
