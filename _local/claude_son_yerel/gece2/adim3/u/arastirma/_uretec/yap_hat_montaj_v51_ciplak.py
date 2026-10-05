# -*- coding: utf-8 -*-
"""hat_montaj_v51 · ÇIPLAK MODEL yaması (27 Eyl 2026) — yap_hat_montaj_v51.py'den SONRA çalışır, hat_montaj_v51.py'yi yerinde yamalar.
Kemal: "yalıtımı kaldır, yan ön arka taraf yüzeyi sacını sil, en alttaki etek sacını da kaldır — önce biz sistemleri tam görelim."
Yalnız GÖRSEL çıktı (GLB/USDZ/modul GLB'leri): kabuk saçları, yalıtım, PU duvarlar, fitil, süpürgelik/plint, kabin zarf kutuları çizilmez.
Denetimler (çakışma, ürün yolu, zarf) gerçek parçalarla koşmaya devam eder."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(U, "hat_montaj_v51.py")
s = io.open(p, encoding="utf-8").read()
assert "CIPLAK = True" not in s, "zaten yamali"


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis("def kutu_kat(b):",
      '''# ---- v51 · ÇIPLAK MODEL (Kemal 27 Eyl): yalıtım, yan/ön/arka yüzey sacları, etek (süpürgelik) ve kabin zarfları GÖRSELDE yok — sistemler görünsün.
# Yalnız GLB/USDZ çıktısı; denetimler gerçek parçalarla. Kapak/kabuk istenirse CIPLAK = False.
CIPLAK = True
CIPLAK_AD = ("arka_sac", "arka_dis_sac", "arka_ic_sac", "arka_pu", "yan_dis_sac", "yan_ic_sac", "yan_pu", "yan_on_donus", "on_cerceve_saci", "plint_on",
             "sol_sac", "sag_sac", "on_alt_sac", "on_ust_kapak", "sarjor_yan_kapisi", "kabin_sol_duvar", "kabin_sag_duvar", "kabin_arka_saci", "kabin_taban_saci",
             "yalitim_blogu", "on_fitil", "govde_kabugu", "yalitim_tasyunu", "f_arka_saci", "taban_kapisi", "ust_kapi")
CIPLAK_MAL = ("kabuk", "yalitim")
CIPLAK_KUTU = ("A_KABIN", "TOPPING_MODUL", "B_KASA", "D_TABAN_KABIN", "D_SUPURGELIK_KABIN")
CIPLAK_SAYAC = {"parca": 0, "kutu": 0}


def ciplak_mi(ad, mal=""):
    if CIPLAK and (str(ad).startswith(CIPLAK_AD) or mal in CIPLAK_MAL):
        CIPLAK_SAYAC["parca"] += 1; return True
    return False


def kutu_kat(b):''')
# E menteşeli düğümler
degis('''        for p in ps:
            if p["grup"] != g:
                continue
            m = TC_AG(p["wp"])                                              # E-yerel ağ (m)''',
      '''        for p in ps:
            if p["grup"] != g:
                continue
            if ciplak_mi(p["ad"], p["mal"]): continue
            m = TC_AG(p["wp"])                                              # E-yerel ağ (m)''')
# TOPPING v1 (TC) + v2 (TU.P)
degis('''                _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))''',
      '''                if ciplak_mi(p["ad"], p["mal"]): continue
                _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))''')
degis('''            for q in _v3:
                _kaba = q["ad"].startswith(("motor_", "reduktor_", "kasar_cad", "sucuk_cad"))''',
      '''            for q in _v3:
                if ciplak_mi(q["ad"], q["mal"]): continue
                _kaba = q["ad"].startswith(("motor_", "reduktor_", "kasar_cad", "sucuk_cad"))''')
# E sabit
degis('''                if g in E_MENTESE or g.startswith("B_"):
                    continue                                                   # menteşeli düğümler aşağıda (e_mentese_dugumleri)''',
      '''                if g in E_MENTESE or g.startswith("B_"):
                    continue                                                   # menteşeli düğümler aşağıda (e_mentese_dugumleri)
                if ciplak_mi(p["ad"], p["mal"]): continue''')
# K
degis('''            for p in ps:
                kaba = p["ad"].startswith(("surucu_", "guc_", "itici_motoru"))''',
      '''            for p in ps:
                if ciplak_mi(p["ad"], p["mal"]): continue
                kaba = p["ad"].startswith(("surucu_", "guc_", "itici_motoru"))''')
# STORE
degis('''            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(p["wp"]))''',
      '''            for p in ps:
                if ciplak_mi(p["ad"], p["mal"]): continue
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(p["wp"]))''')
# FIRIN
degis('''            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=FT.dunya(p)), p["ad"].startswith("giris_bandi_motoru")))''',
      '''            for p in ps:
                if ciplak_mi(p["ad"], p["mal"]): continue
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=FT.dunya(p)), p["ad"].startswith("giris_bandi_motoru")))''')
# kabin zarf kutuları
degis('''            parcalar.append((b["kod"], kutu_ag(b), mal_ad(b))); asm.add(kutu_kat(b), name=b["kod"], color=cq.Color(*RENK.get(b["mal"], RENK["kutu"])))''',
      '''            if CIPLAK and (b["kod"] in CIPLAK_KUTU or b["kod"].endswith("_KABIN")):
                CIPLAK_SAYAC["kutu"] += 1                                                    # v51: kabin/etek zarfı görselde yok
            else:
                parcalar.append((b["kod"], kutu_ag(b), mal_ad(b))); asm.add(kutu_kat(b), name=b["kod"], color=cq.Color(*RENK.get(b["mal"], RENK["kutu"])))''')
degis('''    ye = [a for a, _m, _x in parcalar if "__etiket_yuva_" in a]''',
      '''    print("CIPLAK MODEL (v51): gorselden cikarilan parca %d · kabin/etek kutusu %d (yalitim, yan/on/arka saclar, PU duvarlar, fitil, supurgelik) — denetimler tam parcayla" % (CIPLAK_SAYAC["parca"], CIPLAK_SAYAC["kutu"]))
    ye = [a for a, _m, _x in parcalar if "__etiket_yuva_" in a]''')
degis(' · K = kesme_cad_v2 (on kapaklar YOK) · 1 tam animasyon', ' · K = kesme_cad_v2 (on kapaklar YOK) · CIPLAK MODEL: yalitim, yan/on/arka saclar, etek ve kabin zarflari gorselde yok (Kemal 27 Eyl) · 1 tam animasyon')
io.open(p, "w", encoding="utf-8").write(s)
print("hat_montaj_v51.py ciplak yamasi uygulandi")
