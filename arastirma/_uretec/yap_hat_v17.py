# -*- coding: utf-8 -*-
"""hat_montaj_v16 -> v17 : HAREKET EDEN PAKETLER AYRI DUGUM.

Kemal: "neden simulasyonu ac deyince baska bir model geliyor, neden direkt modeli calistirmiyorsun?"
Haklı. Sim icin ayri (ve daha kaba) bir GLB uretiliyordu. Artik AYNI modul_C.glb hem sayfada
gosteriliyor hem simulasyonda oynatiliyor. Tek eksik oydu: donen parcalar govdeyle ayni mesh'te
birlesiyordu, ayri dondurulemiyordu. v17 onlari AYRI DUGUM olarak yaziyor:

    TOPPING_MODUL__celik              (sabit)
    TOPPING_MODUL__celik__ARABA       (x'te kayan araba paketi)
    TOPPING_MODUL__celik__TABLA       (donen tabla)
    KASET_KIYMA__celik__HELEZON       (kasetin dozaj mili)
    KASET_KIYMA__celik__KARISTIRICI   (kasetin karistirici mili)

MALZEME ADI DEGISMIYOR (M<modul>_<kod>__<ton>) -> model3d.js malzeme adiyla calisiyor, etkilenmiyor.
"""
import io, os, re

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v16.py"), encoding="utf-8").read()

# ---------------------------------------------------------------- 1) grup kurali
kural = '''
# ---- HAREKETLI PAKETLER (v17): parca adindan hangi grupta oldugu -------------------------------
# Bu liste sim_topping_v1.py'deki ayrimin aynisi; artik tek yerde, uretim modelinin icinde.
ARABA_P = ("kizak_blogu_", "araba_plakasi", "doner_yatak", "ayar_bilezigi", "donus_motoru", "tahrik_lokmasi",
           "siyirici_apron", "kayis_kolu", "kayis_kelepcesi_", "tabla_home_sensoru", "tabla_home_bayragi", "x_bayragi")
TABLA_P = ("tabla_gobegi", "tabla", "merkezleme_pimi_")


def grup_modul(ad):
    if ad.startswith(TABLA_P) and ad not in ("tabla_home_sensoru", "tabla_home_bayragi"): return "TABLA"
    if ad.startswith(ARABA_P): return "ARABA"
    return "SABIT"


def dugum_ad(kod, ton, grup):
    return "%s__%s" % (kod, ton) if grup == "SABIT" else "%s__%s__%s" % (kod, ton, grup)

'''
anc = "def mal_ad(b, ton=None):"
assert anc in s
s = s.replace(anc, kural.lstrip("\n") + "\n" + anc, 1)

# ---------------------------------------------------------------- 2) MODUL dali: ARABA / TABLA ayrilir
eski = '''                ton.setdefault(p["mal"], Mesh()).ekle(TC_AG(cq.Workplane(obj=sh)))
                asm.add(sh, name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK.get(p["mal"], RENK["kutu"])))
            for t_, m_ in sorted(ton.items()):
                parcalar.append((b["kod"] + "__" + t_, m_, mal_ad(b, t_)))'''
yeni = '''                ton.setdefault((p["mal"], grup_modul(p["ad"])), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh)))
                asm.add(sh, name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK.get(p["mal"], RENK["kutu"])))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))'''
assert eski in s, "MODUL dali bulunamadi"
s = s.replace(eski, yeni, 1)

# ---------------------------------------------------------------- 3) KASET dali: HELEZON / KARISTIRICI ayrilir
eski = '''                ton.setdefault(p["mal"], Mesh()).ekle(V.ag(cq.Workplane(obj=sh), 0.12, 0.35))   # v7: kasetin kendi sayfasiyla AYNI incelik
                asm.add(sh, name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK["pom"]))
            for t_, m_ in sorted(ton.items()):
                parcalar.append((b["kod"] + "__" + t_, m_, mal_ad(b, t_)))'''
yeni = '''                gr_ = p.get("grup")
                gr_ = "SABIT" if not gr_ else ("HELEZON" if gr_ == "helezon" else "KARISTIRICI")
                ton.setdefault((p["mal"], gr_), Mesh()).ekle(V.ag(cq.Workplane(obj=sh), 0.12, 0.35))   # v7: kasetin kendi sayfasiyla AYNI incelik
                asm.add(sh, name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK["pom"]))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))'''
assert eski in s, "KASET dali bulunamadi"
s = s.replace(eski, yeni, 1)

# ---------------------------------------------------------------- 4) cikti adlari v16 -> v17
s = s.replace("hat_v16", "hat_v17").replace("HAT_v16_YERLESIM", "HAT_v17_YERLESIM")

# ---------------------------------------------------------------- 5) hareketli paket sayimi (denetim)
eski = '''    ucgen = sum(len(m.I) // 3 for _a, m, _mal in parcalar)'''
yeni = '''    hp = [a for a, _m, _x in parcalar if a.count("__") == 2]
    print("HAREKETLI PAKET (v17): %d dugum · %s" % (len(hp), " · ".join(sorted({a.rsplit("__", 1)[1] for a in hp}))))
    assert hp, "hicbir hareketli paket ayrilmadi — grup kurali tutmuyor"
    ucgen = sum(len(m.I) // 3 for _a, m, _mal in parcalar)'''
assert eski in s
s = s.replace(eski, yeni, 1)

io.open(os.path.join(U, "hat_montaj_v17.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v17.py yazildi · %d satir" % s.count("\n"))
