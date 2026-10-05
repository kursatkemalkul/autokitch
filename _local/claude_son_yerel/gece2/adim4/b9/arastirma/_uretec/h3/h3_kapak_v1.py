# -*- coding: utf-8 -*-
"""HAT v3.7 · ÖN YÜZ KAPAK SADELEŞTİRMESİ (TASLAK · 1 Eki 2026 · Claude · YEREL) — Kemal çizimi (images/47.webp):
"kapakları benim çizdiğim şekilde yeniden oluştur, daha temiz daha simple; çizgiler birbirini takip etsin; fazla bölmeye gerek yok".

Montaj (hat3_montaj_v7) her modülün PARCALAR listesini kurduktan SONRA, birime ayırmadan / _dis_birim'den ÖNCE bu modülü çağırır.
Bütün şekiller DÜNYA koordinatında (x hat boyunca · y yukarı, zemin 0 · z koridora, ön düzlem +79). İstisnalar fonksiyonlarda yazılı (TU: x − X_BC).

YENİ KAPAK DÜZENİ (yatay çizgiler: 788 her yerde · 1305 yalnız fırın üstü · 455 sağ alt; dikey çizgiler: istasyon sınırları + 1967,5 + 3250 + E_DERZ):
  A        tek kapak      736–1434,5 × 788–2197  (A alt panel + servis kapağı + U_A kapağı birleşti) · robot ağzı PENCERE 986–1186 × 960–1160
  TOPPING  2 kapak        1438–1966 / 1969–2497 × 788–2197 (mekanizma kanadı + K1/K2 soğuk kapak TEK KANAT; üst kısım PU sandviç, alt kısım tava)
  F üstü   2 düşer kapak  2500–3248 / 3252–4000 × 1308–2197 (F üstü kapak + U_F kapağı birleşti; menteşe/gazlı yay altta aynı yerde)
  K        tek kapak      4003–4398 × 788–2197  (K alt/orta/üst + U_KE sol birleşti)
  E        4 kapak        4402–E_DERZ0 / E_DERZ1–5230 × (126–785 | 788–2197) · robot ağzı sol üst kapakta PENCERE · robot çöpü klapesi sol alt kapakta
  B sağ    teknik sütun soğutma paneli 126–454 / depo kapağı 456–785 (K6 içecek çekmece derzi 454/456 ile TEK ÇİZGİ · çekmeceler DEĞİŞMEZ)
"""
import re
import cadquery as cq

Z_ON, T, T_IC, KENAR, DERZ = 79.0, 1.5, 1.0, 20.0, 3.0
Y_DUZ, Y_TAVAN_KAPAK = 788.0, 2197.0
B_UST = 785.0                                    # B çekmece önleri üstü (dolap) → 788 derzi
# ---- KARARLAR (Kemal'e sorulacaklar · varsayılan = önerilen) ----
KARAR = dict(
    E_DERZ=(4860.0, 4863.0),                      # E dikey derz: ağzın sağ kenarı 4840 + 20 çerçeve → ağız kapalı PENCERE (Kemal çizgisi ~4858–4870 ölçüldü)
    KE_1862_KALKAR=True,                          # K + E: U_KE kapağıyla birleşme (çizimdeki tepe X'i) · False → 1862 çizgisi kalır, U_KE ikiye bölünür (4861,5)
    F_KAPAK="duser",                              # "duser" (alttan menteşeli, mevcut tip) · "yan" (dikey eksen) → TOPPING sağ ve K kapaklarıyla köşede çarpışır, önerilmez
    B_SAG_CIZGI=455.0,                            # teknik sütun derzi 447 → 455 (K6 çekmece derzi); çekmece yükseklikleri DEĞİŞMEZ
)
A_X, A_PEN = (736.0, 1434.5), (986.0, 1186.0, 960.0, 1160.0)
K_X = (4003.0, 4398.0)
E_X = (4402.0, 5230.0)
E_AGIZ = (4485.0, 4840.0, 886.0, 1062.0)        # kutu_cad_v14 AGIZ (85–440 yerel) dünya
E_KLAPE = (4464.0, 4594.0, 610.0, 740.0)        # h3_kutu_v1 KLAPE (dünya)


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def _bir(*s):
    r = s[0]
    for q in s[1:]:
        r = r.fuse(q)
    return r.clean()


def tava(x0, x1, y0, y1, kenar=KENAR, pencereler=(), acik_kenar=(), ic_sac=False):
    """304 1,5 tava kapak: ön yüz (z 77,5–79) + 4 kenar dönüşü (derinlik kenar) · pencere = (x0, x1, y0, y1) kesik + 4 iç dönüş ·
    acik_kenar ⊂ {'alt','ust','sol','sag'} dönüşsüz (birleşme kenarı) · ic_sac = KUTU KESİT kapatma sacı 1,0 (E alt kanatları gibi)"""
    z1, z0 = Z_ON, Z_ON - kenar
    p = [kutu(x0, x1, y0, y1, z1 - T, z1)]
    if "alt" not in acik_kenar: p.append(kutu(x0, x1, y0, y0 + T, z0, z1 - T))
    if "ust" not in acik_kenar: p.append(kutu(x0, x1, y1 - T, y1, z0, z1 - T))
    if "sol" not in acik_kenar: p.append(kutu(x0, x0 + T, y0, y1, z0, z1 - T))
    if "sag" not in acik_kenar: p.append(kutu(x1 - T, x1, y0, y1, z0, z1 - T))
    if ic_sac: p.append(kutu(x0 + T, x1 - T, y0 + T, y1 - T, z0, z0 + T_IC))
    s = _bir(*p)
    for (a0, a1, b0, b1) in pencereler:
        s = s.cut(kutu(a0, a1, b0, b1, z0 - 1.0, z1 + 1.0))
        s = _bir(s, kutu(a0 - T, a0, b0, b1, z0, z1 - T), kutu(a1, a1 + T, b0, b1, z0, z1 - T),
                 kutu(a0 - T, a1 + T, b0 - T, b0, z0, z1 - T), kutu(a0 - T, a1 + T, b1, b1 + T, z0, z1 - T))
    return s


def omega(x0, x1, y0, h=40.0):
    """omega takviye 1,0 (mevcut omegalarla aynı zarf z 62–78 · yükseklik 40): taban kanatları + gövde"""
    return _bir(kutu(x0, x1, y0, y0 + 8.0, Z_ON - T - T_IC, Z_ON - T), kutu(x0, x1, y0 + h - 8.0, y0 + h, Z_ON - T - T_IC, Z_ON - T),
                kutu(x0, x1, y0 + 7.0, y0 + 8.0, 62.0, Z_ON - T), kutu(x0, x1, y0 + h - 8.0, y0 + h - 7.0, 62.0, Z_ON - T),
                kutu(x0, x1, y0 + 7.0, y0 + h - 7.0, 62.0, 63.0))


# ---------------------------------------------------------------- liste yardımcıları ----------------------------------------------------------------
def sekil(p):
    """parçanın katısı (çok katılı Workplane → Compound) · ÇERÇEVE parçanın tutulduğu çerçevedir (dönüşüm YOK)"""
    w = p["wp"] if "wp" in p else p["sh"]
    if hasattr(w, "vals"):
        v = [o for o in w.vals() if isinstance(o, cq.Shape)]
        return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)
    return w


def koy(p, s):
    if "wp" in p: p["wp"] = cq.Workplane(obj=s)
    else: p["sh"] = s


def bul(L, ad):
    q = [p for p in L if p["ad"] == ad]
    assert len(q) == 1, ("v3.7 kapak: parça yok / çift", ad, len(q))
    return q[0]


def dus(L, adlar, rapor):
    adlar = set(adlar)
    var = set(p["ad"] for p in L)
    eksik = adlar - var
    assert not eksik, ("v3.7 kapak: düşecek parça yok", sorted(eksik))
    L[:] = [p for p in L if p["ad"] not in adlar]
    rapor.extend(sorted(adlar))


def yeni(L, ornek, ad, s, rapor, **kw):
    assert all(p["ad"] != ad for p in L), ad
    d = dict(ornek, ad=ad, **kw)
    d.pop("wp", None); d.pop("sh", None)
    d["wp" if "wp" in ornek else "sh"] = cq.Workplane(obj=s) if "wp" in ornek else s
    L.append(d); rapor.append(ad)
    return d


def tasi(p, dy=0.0, dx=0.0):
    koy(p, sekil(p).translate(cq.Vector(dx, dy, 0.0)))


def bb_kontrol(p, beklenen, tol=1.0, ad=""):
    b = sekil(p).BoundingBox(); g = (b.xmin, b.xmax, b.ymin, b.ymax)
    assert all(abs(u - v) <= tol for u, v in zip(g, beklenen)), ("v3.7 kapak: koordinat sözleşmesi bozuk (dünya mı?)", ad or p["ad"], g, beklenen)


# ================================================================ BÖLGELER ================================================================
def bolge_A(AK_L, rapor, rahat=(748.0, 62.0)):
    """A + U_A → tek kapak (grup SERVIS_KAPAGI: mevcut sol gizli menteşe ekseni AK.MENTESE['pivot'] (743 · 72) aynen)"""
    eski = bul(AK_L, "onyuz_servis_kapagi"); bb_kontrol(eski, (736.0, 1434.5, 1110.5, 1859.0), 1.5)
    # ÇERÇEVE: AK (h3_acici_v1) DÜNYA · rahat = AK.KAPAK_RAHAT (x, z): menteşe tarafında dönüşler z 62'de biter (gizli menteşe süpürmesi, acici denetçi 2)
    s = tava(A_X[0], A_X[1], Y_DUZ, Y_TAVAN_KAPAK, pencereler=[A_PEN])
    s = s.cut(kutu(A_X[0] - 1.0, rahat[0], Y_DUZ - 1.0, Y_TAVAN_KAPAK + 1.0, Z_ON - KENAR - 1.0, rahat[1]))
    k = yeni(AK_L, eski, "onyuz_kapak_A", s, rapor, grup="SERVIS_KAPAGI",
             bom=("A ön kapağı 304 fırçalı 1,5 tava 20 · %.1f × %.0f · robot ağzı penceresi 200 × 200" % (A_X[1] - A_X[0], Y_TAVAN_KAPAK - Y_DUZ), 1, "üretim",
                  "v3.7 · alt panel + servis kapağı + U_A kapağı TEK KAPAK (Kemal çizimi) · 3 gizli menteşe sol · 3 bas-aç sağ", "ÜRETİM"))
    for i, y0 in enumerate((850.0, 1340.0, 1600.0, 1990.0)):          # ağız 960–1160 ve menteşe/mandal hizaları dışında
        yeni(AK_L, eski, "onyuz_kapak_A_omega_%d" % i, omega(771.0, 1366.0, y0), rapor, grup="SERVIS_KAPAGI")
    # menteşe: 1240 / 1700 yerinde + 3. menteşe 920 (sol dikme 894'ten başlar)
    for par in ("sabit", "kanat", "pim"):
        m0 = bul(AK_L, "onyuz_servis_kapagi_mentese_0_%s" % par)
        yeni(AK_L, m0, "onyuz_servis_kapagi_mentese_2_%s" % par, sekil(m0).translate(cq.Vector(0, -320.0, 0)), rapor)
    # bas-aç: 1460 yerinde + alt (sağ alt dikme 791–894) + üst (U_A sağ yan önünde, eski U_A bas-aç yeri)
    md = bul(AK_L, "onyuz_servis_kapagi_basac_mandal")
    yeni(AK_L, md, "onyuz_servis_kapagi_basac_mandal_alt", sekil(md).translate(cq.Vector(0, 840.0 - 1460.0, 0)), rapor)
    yeni(AK_L, md, "onyuz_servis_kapagi_basac_mandal_ust", sekil(md).translate(cq.Vector(0, 2120.0 - 1460.0, 0)), rapor)
    dus(AK_L, ["onyuz_servis_kapagi", "onyuz_servis_kapagi_omega_0", "onyuz_servis_kapagi_omega_1",
               "onyuz_alt_panel", "onyuz_alt_panel_omega"] + ["onyuz_alt_panel_tutucu_%d" % i for i in range(4)] +
        ["onyuz_emniyet_hedefi_alt", "onyuz_emniyet_sensoru_alt",               # tek kapak → tek kilit sensörü (1540 RSS 36 kalır)
         "onyuz_cerceve_orta_kayit_sol", "onyuz_cerceve_orta_kayit_sag"], rapor)    # yalnız 1107,5/1110,5 derzinin dayamasıydı (opak çizgi bırakırdı)
    return k


def bolge_A_ust(UD_L, rapor):
    """U_A kapağı + donanımı düşer (A kapağı tavana kadar) · U_A alt/üst kayıt YERİNDE (A ile tek kutu, v3.4)"""
    dus(UD_L, ["onyuz_ust_a_kapak_tek", "onyuz_ust_a_kapak_tek_alt_kutusu", "onyuz_ust_a_mentese_sabit_tek_0", "onyuz_ust_a_mentese_hareketli_tek_0",
               "onyuz_ust_a_mentese_sabit_tek_1", "onyuz_ust_a_mentese_hareketli_tek_1", "onyuz_ust_a_bas_ac_tek_sol", "onyuz_ust_a_bas_ac_tek_sag",
               "onyuz_ust_a_kapak_tek_tipon_plakasi_sol", "onyuz_ust_a_kapak_tek_tipon_plakasi_sag"], rapor)


def bolge_F(FU_L, UD_L, rapor):
    """F üstü + U_F → 2 düşer kapak 1308–2197 (alt menteşe + gazlı yay + burulma kutusu YERİNDE · bas-aç tepede: U_F'nin mevcut bas-açı 2130–2150)
    ÇERÇEVE: FU (h3_firin_ust_v1) ve UD (h3_ust_depo_v2) DÜNYA."""
    for yon, YON in (("sol", "SOL"), ("sag", "SAG")):
        f, u = bul(FU_L, "onyuz_f_ust_kapak_" + yon), bul(UD_L, "onyuz_ust_f_kapak_" + yon)
        bf, bu = sekil(f).BoundingBox(), sekil(u).BoundingBox()
        dolgu = kutu(bf.xmin, bf.xmax, bf.ymax - 1.0, bu.ymin + 1.0, Z_ON - T, Z_ON)                     # 1859–1862 derzi yüzde kapanır
        ic_kes = kutu(bf.xmin + T, bf.xmax - T, bf.ymax - T - 0.5, bu.ymin + T + 0.5, Z_ON - KENAR - 1.0, Z_ON - T)   # birleşme kenarlarının iç dönüşleri
        s = _bir(sekil(f), sekil(u), dolgu).cut(ic_kes)
        koy(f, s); f["bom"] = (("Fırın üstü kapağı %s 304 1,5 tava 20 · %.0f × %.0f (v3.7: U_F kapağıyla tek kanat)" % (yon, bf.xlen, bu.ymax - bf.ymin)), 1, "üretim",
                              "v3.7 · alttan menteşeli düşer kapak · gazlı yay YENİDEN HESAP (kütle ≈ 2,4 × moment)", "ÜRETİM")
        rapor.append("onyuz_f_ust_kapak_%s (+U_F birleşti)" % yon)
        ku = bul(UD_L, "onyuz_ust_f_kapak_%s_alt_kutusu" % yon)                                      # U_F alt burulma kutusu → orta takviye (kanatla döner)
        yeni(FU_L, f, "onyuz_f_ust_kapak_%s_orta_kutusu" % yon, sekil(ku), rapor, grup="KAPAK_F_" + YON)
        tp = bul(FU_L, "onyuz_f_ust_kapak_%s_tipon_plakasi" % yon); tasi(tp, dy=2130.0 - 1810.0)        # karşılık plakası (kanatla döner) tepeye
    dus(FU_L, ["onyuz_f_ust_bas_ac_sol", "onyuz_f_ust_bas_ac_sag"], rapor)                          # bas-aç: U_F yan sacındaki mevcut bas-aç (2130–2150) KALIR
    dus(UD_L, ["onyuz_ust_f_kapak_sol", "onyuz_ust_f_kapak_sag", "onyuz_ust_f_kapak_sol_alt_kutusu", "onyuz_ust_f_kapak_sag_alt_kutusu"] +
        ["onyuz_ust_f_mentese_%s_%s_%d" % (t, y, i) for t in ("sabit", "hareketli") for y in ("sol", "sag") for i in (0, 1)] +
        ["onyuz_ust_f_kapak_sol_tipon_plakasi_sol", "onyuz_ust_f_kapak_sag_tipon_plakasi_sag"], rapor)


def bolge_KE_ust(UD_L, rapor):
    """U_KE kapakları + donanımı düşer (K ve E kapakları tavana kadar) · alt/üst kayıt, raf, kirişler YERİNDE"""
    if not KARAR["KE_1862_KALKAR"]:
        return
    dus(UD_L, ["onyuz_ust_ke_kapak_sol", "onyuz_ust_ke_kapak_sag", "onyuz_ust_ke_kapak_sol_alt_kutusu", "onyuz_ust_ke_kapak_sag_alt_kutusu"] +
        ["onyuz_ust_ke_mentese_%s_%s_%d" % (t, y, i) for t in ("sabit", "hareketli") for y in ("sol", "sag") for i in (0, 1)] +
        ["onyuz_ust_ke_bas_ac_sol_sol", "onyuz_ust_ke_bas_ac_sag_sag", "onyuz_ust_ke_kapak_sol_tipon_plakasi_sol", "onyuz_ust_ke_kapak_sag_tipon_plakasi_sag"], rapor)


def bolge_K(KS_L, rapor):
    """K: alt/orta/üst kapak → tek kapak 788–2197 · sol gizli menteşe (EMKA 1046 sınıfı, sanal pivot ön-sol köşe x 4003 · z 79) · v3'te K kapaklarında menteşe YOKTU"""
    eski = bul(KS_L, "onyuz_kapak_orta"); bb_kontrol(eski, (4003.0, 4398.0, 886.0, 1305.0), 1.5)
    y1 = Y_TAVAN_KAPAK if KARAR["KE_1862_KALKAR"] else 1859.0
    yeni(KS_L, eski, "onyuz_kapak_K", tava(K_X[0], K_X[1], Y_DUZ, y1, ic_sac=False), rapor,
         bom=("K ön kapağı 304 1,5 tava 20 · 395 × %.0f" % (y1 - Y_DUZ), 1, "üretim", "v3.7 · tek kapak (Kemal çizimi) · 3 menteşe sol · 3 bas-aç sağ · 2 omega", "ÜRETİM"))
    for i, y0 in enumerate((1250.0, 1700.0)):
        yeni(KS_L, eski, "onyuz_kapak_K_omega_%d" % i, omega(K_X[0] + 25.0, K_X[1] - 25.0, y0), rapor)
    for i, y0 in enumerate((900.0, 1360.0, 1750.0)):      # E gizli menteşesiyle aynı zarf 20 × 60 · z 49–78 (K köşe dikmesi z 27–57 ile 8 mm bindirir)
        yeni(KS_L, eski, "onyuz_kapak_K_mentese_%d" % i, kutu(4015.0, 4035.0, y0, y0 + 60.0, 49.0, 78.0), rapor)
    for i, y0 in enumerate((1000.0, 1700.0, 2138.0)):      # E bas-aç zarfı 20 × 30 · z 39–57 · sağ köşe dikmesi (4365–4395) önünde · üstteki U_KE üst kaydının altına değer
        yeni(KS_L, eski, "onyuz_kapak_K_basac_%d" % i, kutu(4375.0, 4395.0, y0, y0 + 30.0, 39.0, 57.0), rapor)
    dus(KS_L, ["onyuz_kapak_alt", "onyuz_kapak_orta", "onyuz_kapak_ust"], rapor)


def bolge_E(KC_L, rapor, X_E=4400.0, klape_kes=None):
    """E: 2 × 2 kapak · yatay derz 785/788 (B çekmece üstüyle tek çizgi) · dikey derz KARAR E_DERZ (boydan boya) · ağız ve klape korunur.
    ÇERÇEVE: montaj E parçalarını E YERELİNDE tutar (x 0–830 · dünya = x + X_E · y / z dünya). Ölçüler dünyada yazılır, parçaya yerel (−X_E) yazılır.
    klape_kes = h3_kutu_v1.klape_cebi() (E yereli: dış yüzde 130 × 130 açıklık + klapenin içe dönme cebi) — verilmezse yalnız açıklık kesilir."""
    d0, d1 = KARAR["E_DERZ"]
    y1 = Y_TAVAN_KAPAK if KARAR["KE_1862_KALKAR"] else 1859.0
    YER = cq.Vector(-X_E, 0.0, 0.0)
    ls, lr = bul(KC_L, "onyuz_alt_kanat_sol"), bul(KC_L, "onyuz_alt_kanat_sag")
    bb_kontrol(ls, (4402.0 - X_E, 4814.0 - X_E, 126.0, 883.0), 1.5)                                   # E YEREL (2–414) — dünya gelirse burada durur
    s_ls = tava(E_X[0], d0, 126.0, B_UST, ic_sac=True).translate(YER)
    s_ls = s_ls.cut(klape_kes) if klape_kes is not None else s_ls.cut(kutu(E_KLAPE[0], E_KLAPE[1], E_KLAPE[2], E_KLAPE[3], -200.0, Z_ON + 1.0).translate(YER))
    yeni(KC_L, ls, "onyuz_kapak_E_alt_sol", s_ls, rapor)
    yeni(KC_L, lr, "onyuz_kapak_E_alt_sag", tava(d1, E_X[1], 126.0, B_UST, ic_sac=True).translate(YER), rapor)
    us = bul(KC_L, "onyuz_ust_kanat_sol")
    yeni(KC_L, us, "onyuz_kapak_E_ust_sol", tava(E_X[0], d0, Y_DUZ, y1, pencereler=[E_AGIZ]).translate(YER), rapor)     # robot ağzı = pencere (sağ çerçeve 20)
    yeni(KC_L, us, "onyuz_kapak_E_ust_sag", tava(d1, E_X[1], Y_DUZ, y1).translate(YER), rapor)
    for i, (x0, x1, y0) in enumerate(((4425.0, d0 - 20.0, 1300.0), (4425.0, d0 - 20.0, 1700.0), (d1 + 20.0, 5205.0, 1300.0), (d1 + 20.0, 5205.0, 1700.0))):
        yeni(KC_L, us, "onyuz_kapak_E_ust_omega_%d" % i, omega(x0, x1, y0).translate(YER), rapor)
    # yeni orta yatay kayıt (785/788 derzinin dayaması) + orta dikme (dikey derzin dayaması; ağız sağ kenarından 6,5 mm sağda)
    ko = bul(KC_L, "onyuz_kayit_orta"); bko = sekil(ko).BoundingBox()
    yeni(KC_L, ko, "onyuz_kayit_788", sekil(ko).translate(cq.Vector(0, 773.0 - bko.ymin, 0)), rapor)          # yalnız y kayar (çerçeveden bağımsız)
    xm = (d0 + d1) / 2.0
    yeni(KC_L, ko, "onyuz_dikme_orta", kutu(xm - 15.0, xm + 15.0, 129.0, 1860.0, bko.zmin, bko.zmax).cut(kutu(xm - 16.0, xm + 16.0, 773.0, 803.0, bko.zmin - 1, bko.zmax + 1)).translate(YER), rapor)
    # menteşeler: dış kenarlarda (sol x 4422 · sağ 5188) — alt 3 × (300/530/680) · üst 3 × (900/1360/1750) · yalnız y kayar
    ml, mr = bul(KC_L, "onyuz_mentese_0"), bul(KC_L, "onyuz_mentese_3")
    for taraf, m in (("sol", ml), ("sag", mr)):
        bm = sekil(m).BoundingBox()
        for i, y0 in enumerate((300.0, 530.0, 680.0, 900.0, 1360.0, 1750.0)):
            yeni(KC_L, m, "onyuz_kapak_E_mentese_%s_%d" % (taraf, i), sekil(m).translate(cq.Vector(0, y0 - bm.ymin, 0)), rapor)
    # bas-aç: orta dikmenin önünde, iki kanat kenarında · alt 1 çift (700) · üst 2 çift (1000 · 1700) · x dünyada hesaplanır → yerel
    b0 = bul(KC_L, "onyuz_basac_0"); bb0 = sekil(b0).BoundingBox()
    for i, y0 in enumerate((700.0, 1000.0, 1700.0)):
        for taraf, xa in (("sol", d0 - 20.0), ("sag", d1)):
            yeni(KC_L, b0, "onyuz_kapak_E_basac_%s_%d" % (taraf, i), sekil(b0).translate(cq.Vector((xa - X_E) - bb0.xmin, y0 - bb0.ymin, 0)), rapor)
    dk = bul(KC_L, "onyuz_dikme_orta")                                                              # bas-aç gövdeleri orta dikmenin CEBİNDE (pencere kesiği, K sac pilotu gibi)
    koy(dk, sekil(dk).cut(cq.Compound.makeCompound([sekil(q) for q in KC_L if q["ad"].startswith("onyuz_kapak_E_basac_")])))
    dus(KC_L, ["onyuz_alt_kanat_sol", "onyuz_alt_kanat_sag", "onyuz_orta_sabit_panel", "onyuz_orta_servis_kapagi", "onyuz_ust_kanat_sol", "onyuz_ust_kanat_sag",
               "onyuz_kayit_orta", "onyuz_kayit_ust"] + ["onyuz_mentese_%d" % i for i in range(12)] + ["onyuz_basac_%d" % i for i in range(5)], rapor)
    # NOT: klape levhası / menteşesi / yaprağı + düşme oluğu (ecop_*, KANAT_AD) kanatla döner — ad / grup DEĞİŞMEZ, yeni kanadın arkasında aynı yerde


def bolge_B_sag(SC_L, rapor):
    """B teknik sütun önü (K'nın altı): soğutma paneli 126–445,5 → 126–453,5 · depo kapağı 448,5–785 → 456,5–785 (K6 çekmece derzi 453,5/456,5 ile TEK ÇİZGİ)
    ÇERÇEVE: SC (h3_store_v1) DÜNYA. Depo fitili yalnız ALT bacağından +8 uzar/kısalır (üst bacak depo tavanına dayalı, kaymaz) · iç sac yerinde."""
    yc = KARAR["B_SAG_CIZGI"]; y_ust, y_alt = yc - DERZ / 2.0, yc + DERZ / 2.0          # 453,5 · 456,5
    sp = bul(SC_L, "tk_kapak_sogutma_dis_sac"); bs = sekil(sp).BoundingBox(); bb_kontrol(sp, (4012.5, 4400.0, 126.0, 445.5), 1.5)
    s = sekil(sp).cut(kutu(bs.xmin - 1, bs.xmax + 1, bs.ymax - T - 0.2, bs.ymax + 1, bs.zmin - 1, Z_ON - T))      # eski üst dönüş
    s = _bir(s, kutu(bs.xmin, bs.xmax, bs.ymax - 1.0, y_ust, Z_ON - T, Z_ON), kutu(bs.xmin, bs.xmax, y_ust - T, y_ust, bs.zmin, Z_ON - T))
    koy(sp, s); rapor.append("tk_kapak_sogutma_dis_sac 126–%.1f" % y_ust)
    dp = bul(SC_L, "tk_kapak_depo_dis_sac_1.5"); bd = sekil(dp).BoundingBox(); dy = y_alt - bd.ymin             # +8
    s = sekil(dp).cut(kutu(bd.xmin - 1, bd.xmax + 1, bd.ymin - 1, y_alt + T, bd.zmin - 1, bd.zmax + 1))
    s = _bir(s, kutu(bd.xmin, bd.xmax, y_alt, y_alt + T, bd.zmin, Z_ON))                                       # yeni alt dönüş (+ yüz kenarı)
    koy(dp, s); rapor.append("tk_kapak_depo_dis_sac_1.5 %.1f–785" % y_alt)
    pu = bul(SC_L, "tk_kapak_depo_pu"); bp = sekil(pu).BoundingBox()
    koy(pu, sekil(pu).cut(kutu(bp.xmin - 1, bp.xmax + 1, bp.ymin - 1, y_alt + T, bp.zmin - 1, bp.zmax + 1)))
    ft = bul(SC_L, "tk_kapak_depo_fitil"); f = sekil(ft); bf = f.BoundingBox()                                 # halka: alt bacak +dy, yan bacaklar kısalır
    alt = f.intersect(kutu(bf.xmin - 1, bf.xmax + 1, bf.ymin - 1, bf.ymin + 15.0, bf.zmin - 1, bf.zmax + 1)).translate(cq.Vector(0, dy, 0))
    koy(ft, _bir(f.intersect(kutu(bf.xmin - 1, bf.xmax + 1, bf.ymin + dy, bf.ymax + 1, bf.zmin - 1, bf.zmax + 1)), alt))
    rapor.append("depo fitili alt bacak +%.0f" % dy)


def bolge_TOPPING(TC_parca, TU_parca, X_BC, tc_ofset, rapor):
    # ÇERÇEVE: TC parçaları TC yerelinde (dünya = + tc_ofset(p)) · TU parçaları x − X_BC (y, z dünya; −168 kaydırması YAPILMIŞ olmalı)
    """TOPPING: mekanizma kanadı (TC, yarıklı) + K1/K2 dış sacı (TU) TEK KABUK · TC kabuğu düşer, birleşik kabuk TU parçasına yazılır.
    TC_parca / TU_parca: {'sol': p, 'sag': p} · tc_ofset(p) → TC yerelinden dünyaya Vector · TU sh = dünya − (X_BC, 0, 0)"""
    for yon in ("sol", "sag"):
        tc, tu = TC_parca[yon], TU_parca[yon]
        w_tc = sekil(tc).translate(tc_ofset(tc)); w_tu = sekil(tu).translate(cq.Vector(X_BC, 0, 0))
        b1, b2 = w_tc.BoundingBox(), w_tu.BoundingBox()
        assert abs(b1.xmin - b2.xmin) < 1.0 and abs(b1.xmax - b2.xmax) < 1.0 and b1.ymax < b2.ymin < b1.ymax + 4.0, ("TOPPING kabuk hizası", b1.__dict__, b2.__dict__)
        dolgu = kutu(b1.xmin, b1.xmax, b1.ymax - 1.0, b2.ymin + 1.0, Z_ON - T, Z_ON)
        ic_kes = kutu(b1.xmin + T, b1.xmax - T, b1.ymax - T - 0.5, b2.ymin + T + 0.5, 39.0 - 1.0, Z_ON - T)   # birleşme kenarı iç dönüşleri (40 + 20 derin)
        s = _bir(w_tc, w_tu, dolgu).cut(ic_kes).translate(cq.Vector(-X_BC, 0, 0))
        koy(tu, s); rapor.append("TU %s: mekanizma kanadı + dış sac TEK KABUK 788–%.0f" % (tu["ad"], b2.ymax))


# ================================================================ AÇILMA TARAMASI (v3.7 yeni denetim) ================================================================
def supur(kapak, nokta, yon, isaret, engeller, acilar=range(10, 101, 10), esik=1.0):
    """kapak (dünya katısı) nokta/yon ekseni etrafında isaret·açı döner (dışa = +z) · engeller [(ad, katı)] · dönüş: [(açı, ad, hacim mm³)]"""
    bul_ = []
    for a in acilar:
        k = kapak.rotate(cq.Vector(*nokta), cq.Vector(*nokta) + cq.Vector(*yon), isaret * a)
        kb = k.BoundingBox()
        for ad, e in engeller:
            eb = e.BoundingBox()
            if eb.xmin > kb.xmax or eb.xmax < kb.xmin or eb.ymin > kb.ymax or eb.ymax < kb.ymin or eb.zmin > kb.zmax or eb.zmax < kb.zmin:
                continue
            v = k.intersect(e).Volume()
            if v > esik: bul_.append((a, ad, round(v, 1)))
    return bul_


DONANIM = re.compile(r"mentese|_pim$|basac|bas_ac|mandal|tipon|yay_pimi|gazli_yay|dayama")   # taramada engel sayılmaz (kapağın kendi donanımı)
# kapak · eksen noktası · yön · işaret (dışa +z) — sol menteşe: y ekseni −1 · sağ: +1 · düşer kapak: x ekseni +1
SUPURME = [("onyuz_kapak_A", (743.0, 0.0, 72.0), (0, 1, 0), -1),   # A ekseni montajda AK.MENTESE["pivot"]ten yeniden okunur
           ("onyuz_kapak_K", (4003.0, 0.0, 79.0), (0, 1, 0), -1),
           ("onyuz_kapak_E_alt_sol", (4402.0, 0.0, 79.0), (0, 1, 0), -1), ("onyuz_kapak_E_ust_sol", (4402.0, 0.0, 79.0), (0, 1, 0), -1),
           ("onyuz_kapak_E_alt_sag", (5230.0, 0.0, 79.0), (0, 1, 0), 1), ("onyuz_kapak_E_ust_sag", (5230.0, 0.0, 79.0), (0, 1, 0), 1)]
#  TOPPING (sanal pivot ön dış köşe 1438 / 2497 · z 79) ve F düşer kapakları (FU.KAPAK_EKSEN) montajda eklenir
