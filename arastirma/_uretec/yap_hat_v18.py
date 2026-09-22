# -*- coding: utf-8 -*-
"""hat_montaj_v17 -> v18 : YUVA ETIKETLERININ YAZISI.

topping_cad_v11 plakayi koydu; yaziyi buraya yapistiriyoruz (kaset etiketleriyle ayni yontem:
doku_ad ile PNG uretilir, plakanin ON yuzune UV'li bir dortgen konur).
Kotlar TC.ET_* ve urun adlari TC.URUN'den OKUNUR — burada tek sayi/yazi elle tanimlanmaz.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v17.py"), encoding="utf-8").read()

# 1) v11 modulu
assert "topping_cad_v10 as TC" in s
s = s.replace("topping_cad_v10 as TC", "topping_cad_v11 as TC", 1)

# 2) yuva etiketi uretici
anc = "def kaset_etiketleri(V, b, dokular):"
yeni = '''def yuva_etiketleri(b, dokular):
    """v18 · yuvanin ustundeki plakaya urun adi. Kaset govdeleri ORTAK oldugu icin urun bilgisi
    makinede duruyor (Kemal: 'belki de yuvalarin onune etiket koymak lazim').
    Kotlar topping_cad_v11'den okunur; burada tek sayi tanimlanmaz."""
    L, x0m, y0m = [], b["x"][0], b["y"][0]
    z1 = TC.ET_Z1 * MM                                            # plakanin ON yuzu (+z'ye bakar)
    for ad, x0, x1, gen in TC.YUVA:
        # DIKKAT: kodda CIFT ALT CIZGI olmamali — dugum adi "<birim>__<ton>" kalibinda, ucuncu bir "__"
        # hareketli paket sanilip sahte grup aciyor (sim3d dugum adini "__" ile boluyor).
        tr = {"Ç": "C", "Ğ": "G", "İ": "I", "Ö": "O", "Ş": "S", "Ü": "U"}
        kod = "".join(tr.get(c, c) for c in ad.replace(" ", "_"))
        kod = "".join(c if (c.isalnum() and ord(c) < 128) else "_" for c in kod)
        while "__" in kod: kod = kod.replace("__", "_")
        ton = "etiket_yuva_" + kod
        dokular[ton] = doku_ad(TC.URUN[ad], "yuva %.0f mm  ·  kaset %s" % (gen, TC.KASET_CAD[ad]), ok_sol=False)
        MALZEME.setdefault(ton, dict(MALZEME["etiket_ad"]))       # ton tablosu kaset etiketiyle ayni
        ma = mal_ad(b, ton); MALZEME[ma]["doku"] = ton
        ax0, ax1 = (x0m + x0 + 15.0) * MM, (x0m + x1 - 15.0) * MM
        ay0, ay1 = (y0m + TC.ET_Y0) * MM, (y0m + TC.ET_Y1) * MM
        m = Mesh()
        m.quad((ax0, ay0, z1), (ax1, ay0, z1), (ax1, ay1, z1), (ax0, ay1, z1), (0, 0, 1),
               uv=[(0, 1), (1, 1), (1, 0), (0, 0)])
        L.append((ton, m.duzelt(), ma))
    return L


'''
assert anc in s
s = s.replace(anc, yeni + anc, 1)

# 3) MODUL dalinda etiketleri de parcalara ekle
anc2 = """            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)"""
yeni2 = """            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            for i_, (ad_, m_, mal_) in enumerate(yuva_etiketleri(b, DOKU)):      # v18: yuva urun etiketleri
                parcalar.append(("%s__%s%d" % (b["kod"], ad_, i_), m_, mal_))
            b["parca"] = len(ps)"""
assert anc2 in s, "MODUL dali parcalar blogu"
s = s.replace(anc2, yeni2, 1)

# 4) cikti adlari
s = s.replace("hat_v17", "hat_v18").replace("HAT_v17_YERLESIM", "HAT_v18_YERLESIM")

# 5) denetim: 6 yuva etiketi cikmali
anc3 = '    hp = [a for a, _m, _x in parcalar if a.count("__") == 2]'
yeni3 = '''    ye = [a for a, _m, _x in parcalar if "__etiket_yuva_" in a]
    print("YUVA ETIKETI (v18): %d" % len(ye))
    assert len(ye) == 6, "6 yuva etiketi bekleniyordu, %d cikti" % len(ye)
''' + anc3
assert anc3 in s
s = s.replace(anc3, yeni3, 1)

io.open(os.path.join(U, "hat_montaj_v18.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v18.py yazildi")
