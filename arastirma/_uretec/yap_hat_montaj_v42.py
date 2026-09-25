# -*- coding: utf-8 -*-
"""hat_montaj_v41 -> v42 : TOPPING v2 (UNO'lu) ANA MONTAJDA
Kemal (25 Eyl 2026): "siteye koy — montajda son halinde göremedim".
Modül C = topping_cad_v22'nin TABLA MEKANİZMASI + açıcı + dış kabuk + bant + soğutma/pano (bazısı yer değiştirdi)
        + topping_uno_cad_v3 (4 UNO + kaşar/sucuk kaseti + tahrikleri + yeni soğuk hücre + hava tesisatı + spreader).
v1'den ÇIKAN: soğuk kutu PU + iç kabuk + bölmeler + yuva rayları + 12 kaset tahriki + dozaj kovanları + hava perdesi +
 8 sürücü + uzun DIN rayı (UNO'lar havalı; 4 sürücü kuru bölmeye). YER DEĞİŞTİREN: soğutma grubu x+790, pano +80,
 UPS +140, güç +1196, 4 sürücü kuru bölmeye, kırıntı sileceği x+520 (harç–kıyma arası). Valf adası evaporatörün sağına.
Kompresör + Ø10 ana hat ayrı birim (K tabanı / F tabanı arkası).
"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v41.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, "YOK/COK (%d): %s" % (s.count(a), a[:90])
    s = s.replace(a, b)


degis('"""v41 (25 Eyl 2026):', '"""v42 (25 Eyl 2026): TOPPING v2 (UNO\'lu) · topping_uno_cad_v3 + v22 tabla mekanizması · kompresör K tabanında.\nv41 (25 Eyl 2026):')
degis("ÇIKTI: otonom/hat3d/hat_v41.glb + .usdz", "ÇIKTI: otonom/hat3d/hat_v42.glb + .usdz")
degis('''KASET_CAD = {"KAŞAR KABI": ("kasar_cad_v14", "Kaşar kabı v14 + Codex v15 parçaları (helezon B·C·D, çıkış tüpü) · ADAY", "kaset3d/index.html?k=kasar_v14"),
             "KÜP SUCUK": ("sucuk_cad_v7", "Küp sucuk kaseti v7 + Codex V2 parçaları (helezon D, çıkış tüpü) · ADAY", "kaset3d/index.html?k=sucuk_v7")}''',
      '''KASET_CAD = {}   # v42: kaşar + sucuk kasetleri TOPPING v2 modelinin (topping_uno_cad_v3) içinde, yeni yerlerinde''')
degis('''birim("TOPPING_MODUL", "TOPPING modülü: kabin + yalıtım + 6 yuva + 12 tahrik + soğutma + pano", "C", "GERCEK_MODUL",
      (X_BC, X_BC + W_BC), (H_B, H_B + TC.Y), (-DZ, 0.0), "sac", "topping_cad_v22.py", "")''',
      '''birim("TOPPING_MODUL", "TOPPING v2 (UNO'lu): 4 UNO çekirdeği (sos · harç · kıyma · kuşbaşı) + kaşar ve küp sucuk kaseti + hava tesisatı · tabla mekanizması v1'den", "C", "GERCEK_MODUL",
      (X_BC, X_BC + W_BC), (H_B, H_B + TC.Y), (-DZ, 0.0), "sac", "topping_uno_cad_v3.py + topping_cad_v22.py", "hat/topping_v2.html")
birim("HAVA_KOMPRESOR", "Kompresör JUN-AIR OF302-15B (yağsız, 15 L) + Ø10 ana hat · K tabanı → F tabanı arkası → TOPPING", "K", "GERCEK_HAVA",
      (X_BC + 1800.0, X_BC + 3900.0), (123.0, 1100.0), (-DZ, 0.0), "sac", "topping_uno_cad_v3.py", "hat/topping_v2.html")
# ---- v42 · TOPPING v2 parçaları ----
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location("TU3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v3.py"))
TU = _ilu.module_from_spec(_sp); _sp.loader.exec_module(TU)
for _k, (_r, _m, _ru, _say) in TU.M.items():
    MALZEME.setdefault(_k, dict(renk=_r, met=_m, ruf=_ru, saydam=_say))
V1_CIKAN = ("pu_", "ic_kabuk", "bolme", "on_kapak", "kapak_contasi", "dozaj_kovani_", "konum_pimi_", "kovan_", "mil_", "motor_", "reduktor_",
            "soket_", "yay_", "ray_", "yuva_etiketi_", "hava_perdesi", "din_ray", "_bom")


def v1_kalir(ad):
    if ad.startswith(("ray_kirisi", "ray_ortu")): return True
    if ad.startswith("surucu_"): return ad in ("surucu_0", "surucu_1", "surucu_2", "surucu_3")
    if ad == "din_ray_ups": return True
    return not ad.startswith(V1_CIKAN)


V1_TASI = {"sogutma_grubu": (790.0, 0.0, 0.0), "pano_kutusu": (80.0, 0.0, 0.0), "ups": (140.0, 0.0, 0.0), "din_ray_ups": (140.0, 0.0, 0.0),
           "guc_kaynagi": (1196.0, 0.0, 0.0), "fire_silecegi": (520.0, 0.0, 0.0)}
for _i in range(4):
    V1_TASI["surucu_%d" % _i] = (480.0 - 605.0, 1600.0 - 1776.0, -620.0)
V3_CIKAN = ("kabin_", "tabla_diski", "pide", "baglam_", "teknik_bant_", "kompresor_", "hava_ana_hatti")
V3_HAVA = ("kompresor_", "hava_ana_hatti")''')
degis('''            ps = [p for p in TC.PARCALAR if not p["ad"].startswith("_bom") and p["ad"] not in KAPAK]
            ton = {}
            for p in ps:
                sh = p["wp"].val().translate(cq.Vector(b["x"][0], b["y"][0], 0.0))''',
      '''            ps = [p for p in TC.PARCALAR if v1_kalir(p["ad"]) and p["ad"] not in KAPAK]
            ton = {}
            for p in ps:
                _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
                sh = p["wp"].val().translate(cq.Vector(b["x"][0] + _d[0], b["y"][0] + _d[1], _d[2]))''')
degis('''            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            for i_, (ad_, m_, mal_) in enumerate(yuva_etiketleri(b, DOKU)):      # v18: yuva urun etiketleri
                parcalar.append(("%s__%s%d" % (b["kod"], ad_, i_), m_, mal_))
            b["parca"] = len(ps)''',
      '''            _v3 = [q for q in TU.P if not q["ad"].startswith(V3_CIKAN)]
            _yt = [q for q in _v3 if q["ad"] == "yalitim_tabani"][0]
            _yt["sh"] = _yt["sh"].cut(TU.kut(TU.W - 170.0, TU.W - 130.0, 1182.0, 1260.0, -150.0, -190.0).val()).cut(TU.kut(765.0, 795.0, 1182.0, 1232.0, -104.0, -360.0).val())
            for q in _v3:
                _kaba = q["ad"].startswith(("motor_", "reduktor_", "kasar_cad", "sucuk_cad"))
                sh = q["sh"].translate(cq.Vector(b["x"][0], 0.0, 0.0))
                ton.setdefault((q["mal"], "SABIT"), Mesh()).ekle(TC_AG(cq.Workplane(obj=sh), _kaba))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps) + len(_v3)
        elif b["durum"] == "GERCEK_HAVA":
            ton = {}
            _hv = [q for q in TU.P if q["ad"].startswith(V3_HAVA)]
            for q in _hv:
                ton.setdefault((q["mal"], "SABIT"), Mesh()).ekle(TC_AG(cq.Workplane(obj=q["sh"].translate(cq.Vector(X_BC, 0.0, 0.0))), False))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(_hv)''')
degis('''    assert len(ye) == 6, "6 yuva etiketi bekleniyordu, %d cikti" % len(ye)''', '''    assert len(ye) == 0, "v42: yuva etiketi olmamali (yuvalar kalkti)"''')
degis('''    assert sorted(b["kod"] for b in kas) == ["KASET_KAŞAR_KABI", "KASET_KÜP_SUCUK"], "v41: yalniz kasar + kup sucuk olmali"''',
      '''    assert not kas, "v42: kasetler TOPPING v2 modelinin icinde"''')
degis('''    assert len(CODEX_RAPOR) == 6, "Codex parcalari eksik yerlesti"''', '''    print("   v42: kaset + UNO denetimi topping_uno_cad_v3 icinde (56 madde)")''')
degis('''    b1 = glb_yaz(os.path.join(OUT, "hat_v41.glb"), parcalar, dokular, anim=False)''', '''    b1 = glb_yaz(os.path.join(OUT, "hat_v42.glb"), parcalar, dokular, anim=False)''')
degis('''print("hat_v41.glb · %d birim''', '''print("hat_v42.glb · %d birim''')
degis('''usdz_yaz([os.path.join(OUT, "hat_v41.usdz")], "hat_v41",''', '''usdz_yaz([os.path.join(OUT, "hat_v42.usdz")], "hat_v42",''')
degis('''print("hat_v41.usdz · %.0f KB''', '''print("hat_v42.usdz · %.0f KB''')
degis('''· v41 · kasetler kasar + kup sucuk (Codex 3B, aday) ·''', '''· v42 · TOPPING v2 UNO'lu (topping_uno_cad_v3) · kompresor K tabaninda ·''')
io.open(os.path.join(U, "hat_montaj_v42.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v42.py yazildi")
