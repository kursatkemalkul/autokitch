# -*- coding: utf-8 -*-
"""hat_montaj_v90 → v91 (30 Eyl 2026 · Claude · base 4027c2e = v90 e161226 + K v11). Yalnız kayıtlı montaj worktree'sinde çalıştır.
Kemal (30 Eyl, 6 ekran görüntüsü):
1 · K v11: yağ tenekesi + tartı dolabın arkasına, pompa grubu tenekenin üstünde arkada rafta ("geriye en gidebileceği kadar it, ön tarafa bir şeyler koyayım")
2 · A: moduler_montaj_v4 — sağ duvar ağzının önünde sarkan şerit kalktı, ağız lento + dikme + alt kayıtla çerçevelendi ("4 taraftan çıtalarla, kutu gibi")
3 · ÖN ÇERÇEVELER ÇELİK: ON_SEFFAF yalnız kapak kanatlarına — çerçeve / dikme / kayıt / kuşak / plint / sensör / ışık perdesi opak
    (TOPPING'de "havada uçan" açık mavi çerçeve = mekanizma bandının ön çerçevesiydi, saydam kapak malzemesindeydi)
4 · E şarjör yan kapısı saydam değil — gövdeyle aynı sac ("kırmızı seçtiğim dış gövdeyle aynı olmalı")
5 · MONTAJ KATEGORİLERİ: her parçanın GLB'deki üçgen aralığı kategorisiyle kaydedilir (primitive extras "kat"), sayfada seç / birlikte göster (kategori.js)
6 · sayfa: model bağlantısı + sürüm etiketleri + kategori satırı"""
import re
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / "hat_montaj_v90.py").read_text(encoding="utf-8-sig")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:120], s.count(a), n)
    s = s.replace(a, b)


# ---------------------------------------------------------------- 0 · başlık + sürüm ----------------------------------------------------------------
rep('"""hat_montaj_v90 (30 Eyl 2026 · Claude · base b524dae)',
    '"""hat_montaj_v91 (30 Eyl 2026 · Claude · base 4027c2e): K v11 TENEKE ARKADA (pompa grubu rafta, önde 55 cm boş) + A SAĞ YAN ÇERÇEVELİ (moduler_montaj_v4) +\n'
    'ÖN ÇERÇEVELER ÇELİK (yalnız kapak kanatları saydam) + E ŞARJÖR YAN KAPISI GÖVDEYLE AYNI + MONTAJ KATEGORİLERİ (GLB extras "kat") — yap_hat_montaj_v91.py\n'
    'hat_montaj_v90 (30 Eyl 2026 · Claude · base b524dae)')
rep('pafta="HAT v90 (30 Eyl · Claude · YEREL)',
    'pafta="HAT v91 (30 Eyl · Claude · YEREL): K v11 TENEKE ARKADA + A SAG YAN CERCEVELI + ON CERCEVELER CELIK + E YAN KAPI GOVDEYLE AYNI + MONTAJ KATEGORILERI; HAT 5230 · v90 (30 Eyl · Claude · YEREL)')

# ---------------------------------------------------------------- 1 · K v11 · 2 · modüler v4 ----------------------------------------------------------------
n_ = s.count("kesme_cad_v10"); assert n_ >= 8, n_
s = s.replace("kesme_cad_v10", "kesme_cad_v11")
rep("import types as _ty, moduler_montaj_v3 as MOD72                   # v81:",
    "import types as _ty, moduler_montaj_v4 as MOD72                   # v91: v4 = A sağ yan çerçevesi (lento + boğaz dikmesi + alt kayıt, sarkan şerit yok) · v81:")

# ---------------------------------------------------------------- 3 · 4 · SAYDAMLIK: yalnız kapak kanatları ----------------------------------------------------------------
rep('goz_\\d\\d_musteri_kapisi$|on_kapak$|cekmece_onu$|on_ust_kapak$|sarjor_yan_kapisi$)")',
    'goz_\\d\\d_musteri_kapisi$|on_kapak$|cekmece_onu$|on_ust_kapak$)")\n'
    '# v91 · ÇERÇEVE SAYDAM DEĞİL (Kemal: TOPPING\'de "bu ne havada uçuyor" = mekanizma bandının ön çerçevesi) — "onyuz_" adlı çerçeve / dikme / kayıt / kuşak / plint /\n'
    '#       dayama dudağı / lama / menteşe tabanı / kılavuz / emniyet sensörü / ışık perdesi opak kalır; yalnız kapak kanadı, paneli ve kanada bağlı donanım saydam.\n'
    '#       v91 · E şarjör yan kapısı listeden çıktı (Kemal: "kırmızı seçtiğim dış gövdeyle aynı olmalı" — saydam kapıdan içerideki kılavuz taşıyıcı şerit gibi görünüyordu)\n'
    'ON_CERCEVE = _re61.compile(r"(cerceve(?!_saci)|dikme|kayit|kusak|plint|dayama|lama|mentese_tabani|kilavuz|emniyet_sensoru|isik_perdesi)")   # yüz sacı (çerçeve SACI) saydam kalır: B çekmeceleri görünsün\n\n\n'
    'def _seffaf_mi(ad):\n'
    '    return bool(ON_SEFFAF.match(ad)) and not ON_CERCEVE.search(ad)\n\n\n')
rep('        if ON_SEFFAF.match(_p61["ad"]):', '        if _seffaf_mi(_p61["ad"]):')
rep('                if ON_SEFFAF.match(_p63["ad"]): _p63["mal"] = "on_seffaf"', '                if _seffaf_mi(_p63["ad"]): _p63["mal"] = "on_seffaf"')

# ---------------------------------------------------------------- 5 · KATEGORİLER ----------------------------------------------------------------
rep('''def TC_AG(wp, *a, **k):
    try:
        f_ = sys._getframe(1); L_ = f_.f_locals; sat_ = _lc62.getline(f_.f_code.co_filename, f_.f_lineno)
        pv_ = L_.get("q") if 'q["' in sat_ else (L_.get("p") if 'p["' in sat_ else None)
        bv_ = L_.get("b")
        if isinstance(pv_, dict) and "ad" in pv_ and isinstance(bv_, dict) and "kod" in bv_:
            sh_ = wp.val() if hasattr(wp, "val") else wp; bb_ = sh_.BoundingBox()
            PARCA_KUTU.setdefault(bv_["kod"], []).append([pv_["ad"], 1 if pv_.get("mal") == "on_seffaf" else 0]
                                                        + [round(v_, 1) for v_ in (bb_.xmin, bb_.xmax, bb_.ymin, bb_.ymax, bb_.zmin, bb_.zmax)])
    except Exception:
        pass
    return _TC_AG_ASIL(wp, *a, **k)
''', '''def TC_AG(wp, *a, **k):
    kat_ = None
    try:
        f_ = sys._getframe(1); L_ = f_.f_locals; sat_ = _lc62.getline(f_.f_code.co_filename, f_.f_lineno)
        pv_ = L_.get("q") if 'q["' in sat_ else (L_.get("p") if 'p["' in sat_ else None)
        bv_ = L_.get("b")
        if isinstance(pv_, dict) and "ad" in pv_ and isinstance(bv_, dict) and "kod" in bv_:
            sh_ = wp.val() if hasattr(wp, "val") else wp; bb_ = sh_.BoundingBox()
            PARCA_KUTU.setdefault(bv_["kod"], []).append([pv_["ad"], 1 if pv_.get("mal") == "on_seffaf" else 0]
                                                        + [round(v_, 1) for v_ in (bb_.xmin, bb_.xmax, bb_.ymin, bb_.ymax, bb_.zmin, bb_.zmax)])
            kat_ = (bv_["kod"], pv_["ad"], pv_.get("mal"))                                        # v91: ağ kendi parçasını taşır → GLB'de kategori aralığı
    except Exception:
        pass
    m_ = _TC_AG_ASIL(wp, *a, **k)
    if kat_ is not None:
        try:
            m_._kat = kat_
        except Exception:
            pass
    return m_


# ---- v91 · MONTAJ KATEGORİLERİ (Kemal 30 Eyl: "kaç tane montaj şeyine ayırıyorlar … sen söyle kaç kategori olmalı … dış kabuk deyince diğerlerini gizleyecek,
#      elektrik tesisatı deyince sadece kabloları gösterecek, iki tane seçtiğimi birlikte gösterecek … eksikler olsa da kategoriler olsun")
#      Makine yapımındaki iş bölümüne göre (her kategori bir ustaya / firmaya gider): 9 makine kategorisi + 2 çevre kategorisi (ürün, dükkân).
#      Her parçanın GLB'deki üçgen aralığı (Mesh.ekle kaydı) kategorisiyle primitive "extras.kat"a yazılır → sayfa (kategori.js) seçilenleri gösterir.
KAT_LISTE = [
    dict(kod="GOVDE", ad="Gövde", icerik="şase, dış kabuk, kapaklar, ayaklar, kaide, yalıtım", kime="sac / şase atölyesi"),
    dict(kod="MEKANIZMA", ad="Mekanizma", icerik="raylar, arabalar, vidalı miller, kayış-kasnak, yataklar, kalıp ve takımlar", kime="mekanik montaj"),
    dict(kod="MOTOR", ad="Motor + sürücü", icerik="step / servo motorlar, redüktörler, frenler, motor sürücüleri", kime="servo / otomasyon firması"),
    dict(kod="GIDA", ad="Gıda hattı", icerik="gıdaya değen: hazneler, kasetler, dozaj, bantlar, fırın, nozül, yağ hattı", kime="gıda hijyeni"),
    dict(kod="HAVA", ad="Hava (pnömatik)", icerik="kompresör, şartlandırıcı, valf adası, silindirler, vakum, hava hortumları", kime="pnömatikçi"),
    dict(kod="SOGUTMA", ad="Soğutma", icerik="soğutma grubu, evaporatör, bakır hatlar, yoğuşma / tahliye", kime="soğutmacı"),
    dict(kod="GUC", ad="Elektrik güç", icerik="ana şalter, sigorta, güç kaynakları, UPS, güç kabloları, kablo kanalı, enerji zinciri", kime="elektrikçi"),
    dict(kod="KONTROL", ad="Kontrol (beyin)", icerik="PLC ve denetleyiciler, G/Ç, ağ, sensörler, emniyet, ekranlar, sinyal kabloları", kime="otomasyon firması"),
    dict(kod="ROBOT", ad="Robot", icerik="FR5, yer rayı, enerji zinciri, çatal, robot kontrol kutusu", kime="robot entegratörü"),
    dict(kod="URUN", ad="Ürün + sarf", icerik="hamur, pizza, kutu, içecek, yağ tenekesi (görsel)", kime="—"),
    dict(kod="DUKKAN", ad="Dükkân", icerik="tezgâh, bulaşık, evye, zemin kanalı, insan ölçeği (görsel)", kime="—"),
]
KAT_I = {k_["kod"]: i_ for i_, k_ in enumerate(KAT_LISTE)}
_KR_ONCE = [(k_, _re61.compile(r_, _re61.I)) for k_, r_ in (
    ("URUN", r"^(urun_(?!sensor)|pizza|pide_|kutu_blank|icecek_|koli_)|karton_yigin|yag_tenekesi|cop_kovasi|kovasi_15|_kova\\b|poset|_top_\\d+_\\d+$"),
    ("ROBOT", r"^robot_(?!cop|tarafi|yuzu|kapag)|robot_catal|fairino|_fr5"),
    ("SOGUTMA", r"sogutma|evap|kondens|secop|klf|nle8|bakir|txv|genlesme|sicak_gaz|yogusma|arka_hava_(kanali|izgarasi)|kaset_yuzu|kset_|buharlastirma|kapiler|kurutucu|gider_borusu"),
    ("MOTOR", r"motor|reduktor|surucu|stp-drv|el7062|servo|_fren|fren_|nema|pkp268|rollerdrive|ec5000"),
    ("KONTROL", r"plc_|beckhoff|sm122|siwarex|sensor|e3z|e2e|fotosel|isik_perdesi|emniyet|ekran|hmi|qr_okuyucu|pin_tus|modem|kilit_karti|enkoder|encoder|bayrag|home_|limit_|"
                r"ag_anahtar|kamera|pm1704|el6631|el9011|rss36|minitwin|musteri_panel|elektrikli_mandal|karsilik|sinyal|reed|soket|_miknatis_\\d|miknatis_ayagi"),
    ("HAVA", r"^hava_|hava_hortum|pnomati|valf_adasi|^valf_|ss5y|sy3120|aw20|sartlandirici|(?<!urun_)silindir|dgrf|cdq2|zp3c|zk2g|vakum|my1b|rodless|rakor_hava|kompresor_|jun_air|susturucu|hava_giris"),
    ("GUC", r"guc_|ndr-|ana_salter|sigorta|kontaktor|ups|klemens|din_ray|din_plaka|kablo|pano_|priz|enerji_zinciri|topraklama|ssr|g3pe|e5dc|trafo"),
)]
_KR_GIDA = _re61.compile(r"hazne|kaset|uno|helezon|dozaj|doner_valf|nozul|pulsajet|bant|konveyor|tepsi|kalip|bicak|sprey|^yag_|tabla|^bk_|firin|isitici|rezistans|koni|acici|"
                         r"pres|kasar|sucuk|kiyma|kusbasi|sos|harc|apron|siyirici|kirinti|rulo|tunel|olu_plaka|kayma_tablasi|yukleme|hamur", _re61.I)
_KR_MEK = _re61.compile(r"ray|hgr|hgh|kizak|araba|vida|sfu|tr16|tr8|somun|bk12|bf12|yatak|rulman|kayis|kasnak|disli|pinyon|kaplin|mil_|_mil|burc|yay|kam_|lm12|lineer|"
                        r"kol_|kolu|piston|parmak|itici|kopru|flap|asansor|besleyici|gergi|tampon|segman|lokma|bilezik|mafsal|masasi|catal|zimba|tahrik", _re61.I)
_KR_GOVDE = _re61.compile(r"^dis_|onyuz|sac|kabuk|govde|dikme|kayit|cerceve|kusak|panel|kapak|kapag|kapi|mentese|basac|kulp|plint|ayak|taban|tavan|duvar|_pu|^pu|yalitim|conta|fitil|"
                          r"omega|kosebend|lama|profil|kaide|raf|dolap|kasa|tava|etek|izgara|panjur|pencere|gecis_blogu|soguk_|kabin", _re61.I)
KAT_BIRIM = {}                                                                                     # __main__'de GERCEK kaset birimleri → GIDA
KAT_OZET = {}                                                                                      # dosya → {kategori: üçgen} · ana dosyada birim dağılımı


def _kat_birim(kod):
    if kod in KAT_BIRIM: return KAT_BIRIM[kod]
    if kod.startswith(("TEZGAH_", "INSAN", "D_BULASIK", "K_BULASIK")): return "DUKKAN"
    if kod.startswith(("ROBOT_", "ZEMIN_KANALI")) or kod == "QR_ROBOT_KONTROL": return "ROBOT"
    if kod in ("E_PIZZA", "E_KUTU", "E_ICECEK_YEDEK", "D_PIZZA_YEDEK_UST") or kod.startswith("URUN"): return "URUN"
    if kod == "HAVA_KOMPRESOR": return "HAVA"
    if kod == "B_SOGUTMA": return "SOGUTMA"
    if kod in ("QR_UPS", "B_KABLO", "QR_HAVALANDIRMA"): return "GUC"
    if kod.endswith("_ELEKTRIK") or kod in ("QR_ANA_PANO", "QR_KILIT_KARTI", "QR_MUSTERI_PANELI"): return "KONTROL"
    if kod in ("K_BANT", "K_YAG", "F_TP10_KONVEYOR", "F_YUKLEME_BANDI", "F_CIKIS_PLAKA", "B_DEPO", "QR_GOZLER") or kod.startswith(("CEK_", "F_DONER")): return "GIDA"
    if (kod.startswith("E_") and kod != "E_GOVDE") or kod in ("K_KESICI", "K_ITICI") or kod.startswith(("TOPPING_MODUL", "TOPPING_DONER")): return "MEKANIZMA"
    return "GOVDE"


def _karma(kod):                                                                                   # gövde / mekanizma / gıda karışık birimler: ada göre ayrılır
    return kod.startswith(("TOPPING_MODUL", "TOPPING_DONER", "CEK_", "F_TP10_", "F_DONER", "QR_GOZLER", "B_DEPO", "K_YAG", "K_BANT", "K_KESICI", "F_YUKLEME", "B_COP", "HAVA_KOMPRESOR"))


def kategori_bul(birim, ad, mal):
    kb = _kat_birim(birim)
    if kb in ("DUKKAN", "ROBOT", "URUN") or birim in ("HAVA_KOMPRESOR", "B_SOGUTMA"): return kb
    ton = (mal or "").split("__")[-1]
    if ad:
        for k_, r_ in _KR_ONCE:
            if r_.search(ad): return k_
    if ton == "motor": return "MOTOR"
    if ton in ("kart", "siemens", "sensor"): return "KONTROL"
    if ton == "kablo": return "GUC"
    if ton == "hava_ana": return "HAVA"
    if ton in ("hamur", "sos", "harc", "kasar", "kiyma", "kusbasi", "sucuk", "karton", "karton_yigin", "icecek"): return "URUN"
    if ton == "hortum_yag": return "GIDA"
    if ad and not birim.startswith("E_") and (_karma(birim) or kb in ("GIDA", "MEKANIZMA")) and _KR_GIDA.search(ad): return "GIDA"
    if ad and _karma(birim):
        if _KR_MEK.search(ad): return "MEKANIZMA"
        if _KR_GOVDE.search(ad): return "GOVDE"
    return kb


_MESH_EKLE_ASIL = Mesh.ekle


def _mesh_ekle_kat(self, o):
    """v91 · ağa eklenen her parçanın indis aralığı + parçası (kat) kaydedilir; iç içe birleştirmede alt aralıklar kaydırılarak taşınır"""
    i0 = len(self.I)
    _MESH_EKLE_ASIL(self, o)
    L_ = self.__dict__.setdefault("_katr", [])
    k_ = getattr(o, "_kat", None)
    if k_ is not None or not getattr(o, "_katr", None):
        L_.append((k_, i0, len(self.I) - i0))
    else:
        L_.extend((k2, i0 + s2, n2) for k2, s2, n2 in o._katr)
    return self


Mesh.ekle = _mesh_ekle_kat


def _kat_araliklari(m, adi, mal, sayac=None, birimsay=None):
    """düğüm ağının indis aralıkları → [kategori, ilk, sayı, …] (bitişik aynı kategori birleşir) · kaydı olmayan aralık düğümün birim varsayılanı"""
    birim = adi.split("__")[0]
    n = len(m.I)
    varsay = KAT_I[kategori_bul(birim, None, mal)]
    out, pos = [], 0

    def ek(c, s0, cnt):
        if cnt <= 0: return
        if out and out[-3] == c and out[-2] + out[-1] == s0: out[-1] += cnt
        else: out.extend([c, s0, cnt])
        if sayac is not None: sayac[c] = sayac.get(c, 0) + cnt // 3
        if birimsay is not None:
            d_ = birimsay.setdefault(birim, {}); d_[c] = d_.get(c, 0) + cnt // 3
    for k_, s0, cnt in sorted(getattr(m, "_katr", []), key=lambda r_: r_[1]):
        if s0 > pos: ek(varsay, pos, s0 - pos)
        if s0 < pos: cnt -= pos - s0; s0 = pos
        if cnt <= 0: continue
        ek(KAT_I[kategori_bul(k_[0], k_[1], k_[2])] if k_ else varsay, s0, cnt); pos = s0 + cnt
    if pos < n: ek(varsay, pos, n - pos)
    return out
''')
# 5b · kopya ağlar parça kaydını taşır (menteşeli E düğümleri · dönen TOPPING / fırın / QR düğümleri)
rep('yerel.N = list(m.N); yerel.I = list(m.I)', 'yerel.N = list(m.N); yerel.I = list(m.I); yerel._kat = getattr(m, "_kat", None)')
rep('y_.N = list(m_.N); y_.I = list(m_.I)', 'y_.N = list(m_.N); y_.I = list(m_.I); y_._katr = list(getattr(m_, "_katr", []))', 3)
# 5c · GLB: primitive extras "kat" + sahne extras "kategoriler"
rep('''        meshes.append({"name": adi, "primitives": [{"attributes": attr, "indices": ind, "material": kullanilan.index(mal)}]})''',
    '''        meshes.append({"name": adi, "primitives": [{"attributes": attr, "indices": ind, "material": kullanilan.index(mal),
                                                    "extras": {"kat": _kat_araliklari(m, adi, mal, _ks, _kb)}}]})''')
rep('''            prims.append({"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": kullanilan.index(k_)})''',
    '''            prims.append({"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2}, "indices": len(accs) - 1, "material": kullanilan.index(k_),
                          "extras": {"kat": _kat_araliklari(m, o["ad"], k_, _ks, _kb)}})''')
rep('''    kullanilan = sorted(set(mal for _a, _m, mal in parcalar) | set(k for o in ozel for k in o["tonlar"])); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]''',
    '''    kullanilan = sorted(set(mal for _a, _m, mal in parcalar) | set(k for o in ozel for k in o["tonlar"])); blob, views, accs, meshes, nodes = [], [], [], [], []; off = [0]
    _ks, _kb = {}, {}                                                                               # v91: kategori → üçgen · birim → kategori → üçgen
    KAT_OZET[os.path.basename(yol)] = dict(kategori=_ks, birim=_kb)''')
rep('''    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH hat_montaj_v16"}, "scene": 0, "scenes": [{"nodes": kok_dugum}], "nodes": nodes, "meshes": meshes,''',
    '''    g = {"asset": {"version": "2.0", "generator": "AUTOKITCH hat_montaj_v91"}, "scene": 0,
         "scenes": [{"nodes": kok_dugum, "extras": {"kategoriler": [dict(kod=k_["kod"], ad=k_["ad"], icerik=k_["icerik"], kime=k_["kime"]) for k_ in KAT_LISTE]}}],
         "nodes": nodes, "meshes": meshes,''')
# 5d · GERCEK kaset birimleri gıda · durum.json kategori özeti
rep('''    t0 = time.time(); parcalar, asm, sayac, AG = [], _StepYok(), {}, None''',
    '''    t0 = time.time(); parcalar, asm, sayac, AG = [], _StepYok(), {}, None
    for _b91 in B:
        if _b91["durum"] == "GERCEK": KAT_BIRIM[_b91["kod"]] = "GIDA"                              # v91: kasetler (kendi üreteçleri) gıda hattı''')
rep('''                       dosya=MODUL_DOSYA, birim=[''', '''                       dosya=MODUL_DOSYA, kategori=_kat_durum(), birim=[''')
rep('''    with io.open(os.path.join(OUT, "durum.json"), "w", encoding="utf-8") as f:''',
    '''    def _kat_durum():
        o_ = KAT_OZET.get("hat_v91.glb", dict(kategori={}, birim={}))
        top_ = sum(o_["kategori"].values()) or 1
        return dict(liste=KAT_LISTE, ucgen={KAT_LISTE[c_]["kod"]: n_ for c_, n_ in sorted(o_["kategori"].items())},
                    birim={b_: {KAT_LISTE[c_]["kod"]: n_ for c_, n_ in sorted(d_.items())} for b_, d_ in sorted(o_["birim"].items())}, toplam=top_)
    _kd = _kat_durum()
    print("v91 · KATEGORILER (hat_v91.glb ucgen): " + " · ".join("%s %d (%%%.1f)" % (k_, n_, 100.0 * n_ / _kd["toplam"]) for k_, n_ in _kd["ucgen"].items()))
    assert len(_kd["ucgen"]) >= 9, "v91: kategori eksik %s" % list(_kd["ucgen"])
    with io.open(os.path.join(OUT, "durum.json"), "w", encoding="utf-8") as f:''')

# ---------------------------------------------------------------- 6 · çıktı adları ----------------------------------------------------------------
n_ = s.count('os.path.join(OUT, "hat_v90.glb")') + s.count('os.path.join(OUT, "hat_v90.usdz")')
assert n_ == 2, n_
s = s.replace('os.path.join(OUT, "hat_v90.glb")', 'os.path.join(OUT, "hat_v91.glb")').replace('os.path.join(OUT, "hat_v90.usdz")', 'os.path.join(OUT, "hat_v91.usdz")')
rep('"hat_v90", _usd', '"hat_v91", _usd')
rep('print("hat_v90.glb · %d dugum', 'print("hat_v91.glb · %d dugum')
rep('print("hat_v90.usdz · %.0f KB', 'print("hat_v91.usdz · %.0f KB')
assert "hat_v90." not in s.replace("hat_v90.py", ""), [l for l in s.splitlines() if "hat_v90." in l][:3]
assert "moduler_montaj_v3" not in s and "kesme_cad_v10" not in s

compile(s, "hat_montaj_v91.py", "exec")
(U / "hat_montaj_v91.py").write_text(s, encoding="utf-8")

# ---------------------------------------------------------------- 7 · sayfa ----------------------------------------------------------------
H = U.parent.parent / "otonom" / "hat"
KAT_SATIR = ('\n  <div class="zc" id="kat-cubuk"><span style="color:#8d97a4;font:700 12px system-ui,sans-serif;letter-spacing:.04em">KATEGORİ</span>'
             '<span id="kat-dugmeler" style="display:flex;flex-wrap:wrap;gap:6px"></span>'
             '<span id="kat-durum" style="color:#cfd6df;font-size:13px" role="status">Model yükleniyor…</span></div>')
for name, ciftler in (("makine.html", (("1862 · montaj v90</span>", "1862 · montaj v91</span>"), ("1862 mm (montaj v90 ·", "1862 mm (montaj v91 ·"),
                                       ('role="status">Model yükleniyor…</span></div>\n  <div class="sip" id="sip"></div>',
                                        'role="status">Model yükleniyor…</span></div>' + KAT_SATIR + '\n  <div class="sip" id="sip"></div>'),
                                       ('<script src="kenar-cizgi.js?v=2"></script>', '<script src="kenar-cizgi.js?v=2"></script><script src="kategori.js?v=2"></script>'))),
                      ("index.html", (("GERÇEK ÜRETİM MODELİ (montaj v90 ·", "GERÇEK ÜRETİM MODELİ (montaj v91 ·"), ("186 (v90)", "186 (v91)"),
                                      ("· 30 Eyl 2026 · montaj v90 · dükkân v15", "· 30 Eyl 2026 · montaj v91 · dükkân v15")))):
    p = H / name
    with open(p, encoding="utf-8", newline="") as f_:
        t = f_.read()
    if "hat_v91" in t and ("kategori.js" in t or name != "makine.html"):
        continue                                                                         # sayfa zaten v91 (ikinci çalıştırma)
    crlf = "\r\n" in t
    t = re.sub(r"hat_v90\.(glb|usdz)\?v=90[\w-]*", r"hat_v91.\1?v=91", t)
    for a, b in ciftler:
        a2, b2 = (a.replace("\n", "\r\n"), b.replace("\n", "\r\n")) if crlf else (a, b)
        assert t.count(a2) == 1, (name, a[:60], t.count(a2))
        t = t.replace(a2, b2)
    assert "hat_v90" not in t, name
    with open(p, "w", encoding="utf-8", newline="") as f_:
        f_.write(t)
print("v91 montaj üreteci yazıldı (v90 + K v11 + modüler v4 + saydamlık + kategoriler) · makine.html / index.html v91 + kategori satırı")
