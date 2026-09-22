# -*- coding: utf-8 -*-
"""hat_montaj_v6.py -> hat_montaj_v7.py
Kemal (22 Eyl): "kasette detaylar var, onlar topping istasyon montajinda gozukmuyor —
sari etiket, her sey gozuksun; agir olmasi onemli degil, ben PC'den bakarim."
=> 1 GLB yazicisi DOKU tasiyor (UV + images/textures/samplers) — v6'da 'dokular' parametresi aliniyordu
     ama HIC kullanilmiyordu, o yuzden sari etiketler duz renk bile cikmiyordu.
   2 Her kasetin SARI ETIKETI (ad yuzu + montaj yuzu + arka yuz) montaj modeline giriyor; her kasetin
     kendi dokusu uretiliyor (ad kasetin kendi adi + olcusu, montaj adimlari kaset ureteci kaynagindan okunur).
   3 Kaset agi INCE: v6'da 0.5/0.9 kaba agdi (yuvarlaklar kose kose gorunuyordu) -> 0.12/0.35, kasetin
     kendi sayfasindaki ag ayarinin ayni.
"""
import io, os

U = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\_uretec".replace("WEBSITE", "WEBS\u0130TE")
s = io.open(os.path.join(U, "hat_montaj_v6.py"), encoding="utf-8").read()
n = [0]


def rep(a, b):
    global s
    assert a in s, "BULUNAMADI: " + a[:110]
    n[0] += 1
    s = s.replace(a, b, 1)


s = (s.replace("hat_montaj_v6", "hat_montaj_v7").replace("hat_v6.glb", "hat_v7.glb").replace("hat_v6.usdz", "hat_v7.usdz")
     .replace('"hat_v6", parcalar', '"hat_v7", parcalar').replace("HAT_v6_YERLESIM", "HAT_v7_YERLESIM").replace("durum.json?v=6", "durum.json?v=7"))
i = s.index('"""')
s = s[:i + 3] + ("v7 (22 Eyl 2026): GLB yazicisi DOKU tasiyor; kasetlerin SARI ETIKETI montaj modelinde gorunuyor;\n"
                 "kaset agi ince (0.12/0.35) — kasetin kendi sayfasiyla ayni detay. Onceki: hat_montaj_v6.py\n") + s[i + 3:]

# ---------------------------------------------------------------- 1 · import: etiket yuzu + doku ureteci
rep("from kaset_3d_v3 import Mesh, MM, doku_ad, usdz_yaz, MALZEME",
    "from kaset_3d_v3 import Mesh, MM, doku_ad, doku_montaj, etiket_yuzu, usdz_yaz, MALZEME")

# ---------------------------------------------------------------- 2 · Mesh otelemesi + kaset etiketleri
rep('''def kaset_parcalari(modul):
    """kasetin BÜTÜN parçaları — kendi sayfasındakiyle birebir aynı model (v5)."""
    V = importlib.import_module(modul); V.PARCALAR[:] = []; V.kap()
    return V, [p for p in V.PARCALAR if alinir(p["ad"])]''',
    '''def kaset_parcalari(modul):
    """kasetin BÜTÜN parçaları — kendi sayfasındakiyle birebir aynı model (v5)."""
    V = importlib.import_module(modul); V.PARCALAR[:] = []; V.kap()
    return V, [p for p in V.PARCALAR if alinir(p["ad"])]


def mesh_otele(m, dx, dy, dz):
    """hazır ağı (MM ölçeğinde) kütükteki yerine taşır — etiket yüzleri katı değil, doğrudan ağ"""
    y = Mesh(); y.P = [(p[0] + dx, p[1] + dy, p[2] + dz) for p in m.P]; y.N = list(m.N); y.I = list(m.I)
    y.UV = list(m.UV) if m.UV else None
    return y


def montaj_adimlari(modul):
    """kaset üretecinin kaynağındaki doku_montaj([...]) listesini okur — etiketin montaj yüzü için.
    (etiketler() kaset üretecinde __main__ bloğunun İÇİNDE tanımlı, import edilince erişilemiyor.)"""
    import re
    yol = os.path.join(os.path.dirname(os.path.abspath(__file__)), modul + ".py")
    k = io.open(yol, encoding="utf-8").read()
    m = re.search(r"doku_montaj\\(\\[(.*?)\\]\\)", k, re.S)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else ["MONTAJ|KASET SAYFASINDA"]


def kaset_etiketleri(V, b, dokular):
    """kasetin sarı bandı: −x yüzünde AD, +x yüzünde MONTAJ, ikisinin arkasında sarı yüz.
    Geometri kaset üretecindekiyle birebir; doku her kasete ÖZEL üretilir (hepsinde aynı yazı çıkmasın)."""
    kod = "".join(c if (c.isalnum() and ord(c) < 128) else "_" for c in b["kod"])
    e0, e1 = (V.Y_UST - 56) * MM, (V.Y_UST - 8) * MM
    ez = (V.D / 2 - V.TP - 6) * MM; xo = (V.RB + V.ET + 0.4) * MM
    olcu = "%d × %d × %d mm" % (V.W, V.D, V.H)
    dokular["ad_" + kod] = doku_ad(b["ad"].upper(), "bu yönde tak  ·  " + olcu + "  ·  çıkış ÖNDE alttan", ok_sol=True)
    dokular["montaj_" + kod] = doku_montaj(montaj_adimlari(b["kaynak"][:-3]))
    # Malzeme adi mal_ad() kalibinda olmali: modul GLB'si parcalari mal[1] == modul harfi diye suzuyor
    # (duz "etiket_ad_..." adi o suzgece takilip modul dosyasina GIRMIYORDU). Ayrica "__" kalibi sayesinde
    # etikete gelince de kasetin kendisi seciliyor.
    for ton, dk in (("etiket_ad", "ad_" + kod), ("etiket_montaj", "montaj_" + kod), ("sari_arka", None)):
        ma = mal_ad(b, ton)
        if dk: MALZEME[ma]["doku"] = dk
    L = [("etiket_ad", etiket_yuzu(-xo, e0, e1, -ez, ez, -1)), ("etiket_montaj", etiket_yuzu(xo, e0, e1, ez, -ez, 1))]
    for _ad, xx, nx in ((1, -xo + 0.0002, 1), (2, xo - 0.0002, -1)):
        ar = Mesh(); ar.quad((xx, e0, -ez), (xx, e0, ez), (xx, e1, ez), (xx, e1, -ez), (nx, 0, 0))
        L.append(("sari_arka", ar.duzelt()))
    return [(t, m, mal_ad(b, t)) for t, m in L]''')

# ---------------------------------------------------------------- 3 · GERCEK dali: ince ag + etiketler
rep('''                ton.setdefault(p["mal"], Mesh()).ekle(V.ag(cq.Workplane(obj=sh), 0.5, 0.9))
                asm.add(sh, name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK["pom"]))
            for t_, m_ in sorted(ton.items()):
                parcalar.append((b["kod"] + "__" + t_, m_, mal_ad(b, t_)))
            b["parca"] = len(ps)''',
    '''                ton.setdefault(p["mal"], Mesh()).ekle(V.ag(cq.Workplane(obj=sh), 0.12, 0.35))   # v7: kasetin kendi sayfasiyla AYNI incelik
                asm.add(sh, name="%s__%s" % (b["kod"], p["ad"]), color=cq.Color(*RENK["pom"]))
            for t_, m_ in sorted(ton.items()):
                parcalar.append((b["kod"] + "__" + t_, m_, mal_ad(b, t_)))
            dx_, dy_, dz_ = (b["x"][0] + b["x"][1]) / 2.0 * MM, b["y"][0] * MM, (b["z"][1] - V.D / 2.0) * MM
            for i_, (ad_, m_, mal_) in enumerate(kaset_etiketleri(V, b, DOKU)):                   # v7: SARI ETIKET montaj modelinde
                parcalar.append(("%s__%s%d" % (b["kod"], ad_, i_), mesh_otele(m_, dx_, dy_, dz_), mal_))
            b["parca"] = len(ps)''')

# ---------------------------------------------------------------- 4 · glb_yaz: UV + doku
rep('''        meshes.append({"name": adi, "primitives": [{"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": kullanilan.index(mal)}]})''',
    '''        attr = {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}; ind = len(accs) - 1
        if m.UV:                                                                        # v7: etiket yuzleri doku koordinati tasiyor
            vu = gomu(struct.pack("<%df" % (2 * len(m.UV)), *[c for u in m.UV for c in u]), 34962)
            accs.append({"bufferView": vu, "componentType": 5126, "count": len(m.UV), "type": "VEC2"}); attr["TEXCOORD_0"] = len(accs) - 1
        meshes.append({"name": adi, "primitives": [{"attributes": attr, "indices": ind, "material": kullanilan.index(mal)}]})''')

rep('''    mats = []
    for k in kullanilan:
        d = MALZEME[k]; mm = {"name": k, "pbrMetallicRoughness": {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}, "doubleSided": True}
        if d.get("saydam"): mm["alphaMode"] = "BLEND"
        mats.append(mm)''',
    '''    images, textures, doku_idx = [], [], {}
    for k_, veri in sorted(dokular.items()):                                            # v7: PNG'ler GLB'ye gomulur
        images.append({"bufferView": gomu(veri), "mimeType": "image/png"}); textures.append({"source": len(images) - 1, "sampler": 0}); doku_idx[k_] = len(textures) - 1
    mats = []
    for k in kullanilan:
        d = MALZEME[k]; pbr = {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]}
        if d.get("doku") and d["doku"] in doku_idx: pbr["baseColorTexture"] = {"index": doku_idx[d["doku"]]}
        mm = {"name": k, "pbrMetallicRoughness": pbr, "doubleSided": not d.get("tekyuz", False)}
        if d.get("saydam"): mm["alphaMode"] = "BLEND"
        mats.append(mm)''')

rep('''         "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}]}''',
    '''         "materials": mats, "accessors": accs, "bufferViews": views, "buffers": [{"byteLength": len(bb)}],
         "images": images, "textures": textures, "samplers": [{"magFilter": 9729, "minFilter": 9987, "wrapS": 33071, "wrapT": 33071}]}''')

# ---------------------------------------------------------------- 5 · DOKU sozlugu: kutuk kurulurken dolar
rep('''def kutu_kat(b):''',
    '''DOKU = {}                                                          # v7: kaset basina etiket dokulari (kutuk kurulurken dolar)


def kutu_kat(b):''')
rep('''    dokular = {"ad": doku_ad("AUTOKITCH HAT v1",''',
    '''    dokular = dict(DOKU); dokular.update({"ad": doku_ad("AUTOKITCH HAT v1",''')
rep('''               "montaj": doku_ad("MAKİNE ANA MONTAJI", "birimler tek tek gerçek modele çevriliyor", ok_sol=False)}''',
    '''               "montaj": doku_ad("MAKİNE ANA MONTAJI", "birimler tek tek gerçek modele çevriliyor", ok_sol=False)})''')

io.open(os.path.join(U, "hat_montaj_v7.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v7.py yazildi ·", n[0], "yama")
