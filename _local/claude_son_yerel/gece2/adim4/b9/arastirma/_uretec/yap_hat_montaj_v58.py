# -*- coding: utf-8 -*-
"""hat_montaj_v57 → hat_montaj_v58 (27 Eyl 2026 gece) — Kemal: "deterjanları makinenin arkasına koyma, tabii şimdilik sil" · "ön taraflara kapak koyma".
Ev kuralı: v57 metnine sayısı denetlenen (count-assert) değiştirmeler; v57 DEĞİŞMEZ, çıktı yalnız hat_montaj_v58.py.
Yeni üreteçler: kesme_cad_v5 (deterjan_ 9 parça yok) · kutu_cad_v6 (on_alt_sac yok) · dolap store_cad_v6 KALIR (Kemal: "robot çöpü şeyleri kalsın" — store_cad_v7 kullanılmaz) — üçü de kendi
denetimlerinde önceki sürümle parça parça karşılaştırıldı (yalnız bu parçalar çıktı). Montajda:
  · K_DETERJAN birimi + deterjan metinleri kalktı · bulaşık denetimi deterjansız: bulaşığın arkası + MEIKO arka payı BOŞ (assert) · deterjan parçası 0 (assert)
  · birim metinleri: B_COP (önü açık) · E_ICECEK_YEDEK (önü açık · kutu_cad_v6.icecek_on_olcum ölçüleri) · E_GOVDE (alt önü açık, "on_alt_sac" öneki çıktı) ·
    K_GOVDE (ön kapak yok — eski "kapılar · acil stop" metni kesme v2'den beri yanlıştı) · K_ELEKTRIK
  · sözleşmeye 3 v58 eşitliği (K deterjan_ 0 · B_COP 3 parça · E on_alt_sac 0) · robot çöpü BİLGİ satırı (klape yerine atma açıklığı)
  · değişiklik kaydı v58 · durum 'pafta' v58 · çıktılar hat_v58.glb / .usdz (modul_* + durum.json aynı düzen). Başka davranış DEĞİŞMEZ."""
import io, os, re
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v57.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    """a metni TAM n kez geçmeli → b"""
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


def satir(bas, yeni, n=1):
    """`bas` ile BAŞLAYAN satır(lar) TAM n tane olmalı → satırın tamamı `yeni` (çok satırlı olabilir)"""
    global s
    L = s.split(NL)
    idx = [i for i, l in enumerate(L) if l.startswith(bas)]
    assert len(idx) == n, (len(idx), bas[:110])
    for i in idx:
        L[i] = yeni
    s = NL.join(L)


def once(bas, ek):
    """`bas` ile başlayan TEK satırın ÖNÜNE `ek` (sonunda NL olmalı) eklenir"""
    global s
    L = s.split(NL)
    idx = [i for i, l in enumerate(L) if l.startswith(bas)]
    assert len(idx) == 1, (len(idx), bas[:110])
    L[idx[0]] = ek + L[idx[0]]
    s = NL.join(L)


def blok(a, b, yeni):
    """a (tek) işaretinden b (tek) işaretine kadar (b hariç) → yeni"""
    global s
    assert s.count(a) == 1, (s.count(a), a[:110])
    assert s.count(b) == 1, (s.count(b), b[:110])
    i = s.index(a); j = s.index(b)
    assert i < j, (a[:60], b[:60])
    s = s[:i] + yeni + s[j:]


# ================================================================ 1 · DOCSTRING (değişiklik kaydı) ================================================================
degis('"""v57 (27 Eyl 2026):', '"""v58 (27 Eyl 2026 gece): ÖN TARAFLARA KAPAK YOK + DETERJAN YOK (Kemal: "deterjanları makinenin arkasına koyma, tabii şimdilik sil" · "ön taraflara kapak koyma"):' + NL +
      '  K = kesme_cad_v5 — bulaşığın arkasındaki kanister rafı + deterjan / parlatıcı bidonları + dozaj hortumları SİLİNDİ, K_DETERJAN birimi kalktı; bulaşık yeri AYNI,' + NL +
      '  arkası + MEIKO arka payı BOŞ (denetlenir) · B = store_cad_v6 AYNI (robot çöpü kapağı + klapesi kalır, Kemal) · animasyon: robot topu çekmeceden açıcıya TAŞIR' + NL +
      '  (çekmecenin açıcı tarafına park, x 700 konumuna taşır; top–omuz ≤ 779 her karede denetlenir) · E = kutu_cad_v6 — içecek yedeğinin önündeki ön alt sac kalktı →' + NL +
      "  6 koli önden açık (önde yalnız sol ön dikme + dikey kablo kanalı; ölçüler kutu_cad_v6.icecek_on_olcum'dan) · sözleşmeye 3 v58 eşitliği · bulaşık denetimi" + NL +
      '  deterjansız (bulaşığın arkası + arka pay BOŞ: assert) · birim metinleri (B_COP, E_ICECEK_YEDEK, E_GOVDE, K_GOVDE, K_ELEKTRIK) · çıktılar hat_v58.' + NL +
      'v57 (27 Eyl 2026):')

# ================================================================ 2 · B = store_cad_v7 (şeridin önü açık) ================================================================
_ATLA_B1 = ('import store_cad_v6 as SC', 'import store_cad_v7 as SC                                  # v58: robot çöpü şeridinin ÖNÜ AÇIK (servis kapağı + klape paneli + yaylı klape kalktı · Kemal) · v57: TEK PARÇA çekmeceli dolap 0–4000 × 123–788 (24 çekmece · fırın altı PU 60 + taşıyıcı · robot çöpü şeridi) · v44: tam kaplayan kapaklar')
# v58 (Kemal son kararı): B_COP metni ve kaynak adı v57'deki gibi kalır (robot çöpü kapağı + klapesi yerinde)

# ================================================================ 3 · K = kesme_cad_v5 (deterjan yok) ================================================================
satir('import kesme_cad_v4 as KS', 'import kesme_cad_v5 as KS                                  # v58: deterjan + parlatıcı kanisterleri, rafı ve dozaj hortumları KALKTI (Kemal: "şimdilik sil") · kutu_cad_v6\'yı içe alır · v57: alçak hat (taban 892, bant 996, üst 1862) + bulaşık yeri · v54: tank + pano yukarıda')
degis('"KESME istasyonu gövdesi: 304 kabuk · ayaklar · taban 123 · istasyon tabanı 892 (v57) · kapılar (üst PC pencereli, kilitli) · acil stop",',
      '"KESME istasyonu gövdesi: 304 kabuk · ayaklar · taban 123 · istasyon tabanı 892 (v57) · ön kapak YOK (kesme v2 · v58: ön taraflara kapak yok, Kemal)",')
degis('"Pano (arka duvarda, üstte · v57: K tabanının altında bulaşık + deterjan): ', '"Pano (arka duvarda, üstte · K tabanının altında yalnız bulaşık — v58: deterjan kalktı): ')
degis('''    ("K_DETERJAN", "Deterjan + parlatıcı kanisterleri 2 × 5 L (190 × 125 × 285 VARSAYIM) · bulaşığın ARKASINDA raf 325–330 · dozaj hortumları MEIKO arkasına (arka pay 25 korunur) · kanister değişimi için bulaşık öne çekilir (AÇIK)",
     ("deterjan_",)),
''', '''    # v58: K_DETERJAN birimi kalktı — kesme_cad_v5'te "deterjan_" parçası yok (Kemal: "deterjanları makinenin arkasına koyma, tabii şimdilik sil")
''')
degis('raise AssertionError("kesme_cad_v4 parcasi birimsiz kaldi: "', 'raise AssertionError("kesme_cad_v5 parcasi birimsiz kaldi: "')
degis('"sac", "kesme_cad_v4.py", "hat/kesme.html")', '"sac", "kesme_cad_v5.py", "hat/kesme.html")')
degis("· yer kesme_cad_v4'ten KS.BULASIK_YER", "· yer kesme_cad_v5'ten (v4 ile aynı) KS.BULASIK_YER")

# ================================================================ 4 · E = kutu_cad_v6 (içecek yedeğinin önü açık) ================================================================
satir('import kutu_cad_v5 as KC', 'import kutu_cad_v6 as KC                                  # v58: içecek yedeğinin ÖNÜ AÇIK (ön alt sac kalktı · Kemal: ön taraflara kapak yok) · v57: alçak hat (tepsi 936, alt raf 618–622, şarjör 462) + içecek yedeği 6 koli · v54: kalıp ayakları alt rafta')
once('E_BIRIM = [', '''_ION = KC.icecek_on_olcum()                                   # v58: içecek yedeğinin önü (kutu_cad_v6 katılardan ölçer: öndeki engeller · net açıklık · sütunların düz çekme yolu)
assert _ION["on"] == ["kablo_kanali_dikey_alt", "kose_dikme_on_0"] and [e_[0] for e_ in _ION["sutun"][0]["engel"]] == ["kose_dikme_on_0"] \\
    and [e_[0] for e_ in _ION["sutun"][1]["engel"]] == ["kablo_kanali_dikey_alt"], "v58: icecek yedeginin onu beklenen gibi degil: %s" % _ION
''')
degis('''    ("E_GOVDE", "KUTU modülü gövdesi: 304 kabuk (saydam) · ayaklar · taban · ağız kirişi · şarjör yan kapısı", ("ayak_", "taban_sac", "plint_on", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "sarjor_yan_kapisi", "on_alt_sac", "on_ust_kapak", "agiz_ust_kirisi", "kose_dikme_")),''',
      '''    ("E_GOVDE", "KUTU modülü gövdesi: 304 kabuk (saydam) · ayaklar · taban · ağız kirişi · şarjör yan kapısı · üst ön kapak · alt önü AÇIK (v58: ön alt sac kalktı)", ("ayak_", "taban_sac", "plint_on", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "sarjor_yan_kapisi", "on_ust_kapak", "agiz_ust_kirisi", "kose_dikme_")),''')
# denetçi düzeltmesi: 18,5 / 4,0 mm x'teki BİNDİRME (dikme / kanal sütunun önüne yandan biner) — "arkasında" DEĞİL: kolilerin önü dikmenin 61,5, kanalın 33,0 mm arkasında (kutu_cad_v6 olcum_v5)
degis('''    ("E_ICECEK_YEDEK", "İçecek yedeği 6 koli (2 sütun × 3 kat · koli 400 × 267 × 123 · 24 kutu) = 144 · E altı önde, soğutmasız · dolaptaki 144 + 144 = 288 (4 gün 277) · kapısız ön sacın arkasında (erişim AÇIK)", ("icecek_",)),''',
      '''    ("E_ICECEK_YEDEK", "İçecek yedeği 6 koli (2 sütun × 3 kat · koli 400 × 267 × 123 · 24 kutu) = 144 · E altı önde, soğutmasız · dolaptaki 144 + 144 = 288 (4 gün 277) · ÖNÜ AÇIK (v58 · Kemal: ön taraflara kapak yok — ön alt sac kalktı) · önde yalnız sol ön dikme + dikey kablo kanalı, net açıklık %.1f: tek koli düz geçer; dikme sol sütunun önüne %.1f mm, kanal sağ sütunun önüne %.1f mm yandan biner → koli yana kaydırılıp çekilir"
     % (_ION["net"][1] - _ION["net"][0], _ION["sutun"][0]["bindirme"], _ION["sutun"][1]["bindirme"]), ("icecek_",)),''')
degis('raise AssertionError("kutu_cad_v5 parcasi birimsiz kaldi: "', 'raise AssertionError("kutu_cad_v6 parcasi birimsiz kaldi: "')
degis('"sac", "kutu_cad_v5.py", "hat/pack.html")', '"sac", "kutu_cad_v6.py", "hat/pack.html")')

# ================================================================ 5 · yorum / metin: sürüm adları ================================================================
degis("store_cad_v6 / kesme_cad_v4 / kutu_cad_v5'ten SONRA kaydedilir", "store_cad_v6 / kesme_cad_v5 / kutu_cad_v6'dan SONRA kaydedilir")
degis("kutunun çataldaki yeri kutu_cad_v5'ten (catal_kutu).", "kutunun çataldaki yeri kutu_cad_v6'dan (catal_kutu).")
degis("· kutu_cad_v5: dz 900", "· kutu_cad_v6: dz 900")
degis('"kesme_cad_v4: sartlandirici_MS4 parcasi yok"', '"kesme_cad_v5: sartlandirici_MS4 parcasi yok"')
degis('print("   catal cekisi: kutu_cad_v5 kutuyu z', 'print("   catal cekisi: kutu_cad_v6 kutuyu z')
degis("· K = kesme_cad_v4 · E = kutu_cad_v5 · B = store_cad_v6 stroku ·", "· K = kesme_cad_v5 · E = kutu_cad_v6 · B = store_cad_v6 stroku ·")
degis('print("E KUTU MODULU (kutu_cad_v5):', 'print("E KUTU MODULU (kutu_cad_v6):')
degis('print("ANA MONTAJ ANIMASYONU (v57):', 'print("ANA MONTAJ ANIMASYONU (v58):')
degis("# v57: F→K ağzı kesme_cad_v4'ten (932–1072)", "# v57: F→K ağzı kesme_cad_v5'ten (v4 ile aynı, 932–1072)")

# ================================================================ 6 · SÖZLEŞME: 3 v58 eşitliği (model kurulmadan önce, montaj başında ölçülür) ================================================================
degis('''    ("E icecek yedegi: KC.ICECEK_YEDEK kutu = 144", (float(KC.ICECEK_YEDEK["kutu"]), 144.0)),
''', '''    ("E icecek yedegi: KC.ICECEK_YEDEK kutu = 144", (float(KC.ICECEK_YEDEK["kutu"]), 144.0)),
    ("v58 · K deterjan_ parcasi = 0 (kesme_cad_v5 · Kemal: simdilik sil)", (float(len([p for p in KS.PARCALAR if p["ad"].startswith("deterjan_")])), 0.0)),
    ("v58 · B_COP = 8 parca (store_cad_v6 · robot copu kapagi + klapesi yerinde, Kemal)", (float(len([p for p in SC.PARCALAR if p["birim"] == "B_COP"])), 8.0)),
    ("v58 · E on_alt_sac parcasi = 0 (kutu_cad_v6 · icecek yedeginin onu acik)", (float(len([p for p in KC.PARCALAR if p["ad"] == "on_alt_sac"])), 0.0)),
''')
degis('print("ALCAK HAT SOZLESMESI (v57 · %d esitlik', 'print("ALCAK HAT SOZLESMESI (v58 · %d esitlik')

# ================================================================ 7 · __main__: robot çöpü BİLGİ satırı + bulaşık denetimi (deterjansız) ================================================================
# v58: robot çöpü BİLGİ satırı v57'deki gibi kalır (klape yerinde)
degis("    # ---- v57 · BULAŞIK MAKİNESİ K ALTINDA (bulasik_cad_v1 · BM.X0/Y0/Z0 = KS.BULASIK_YER): gerçek parçalar ↔ K parçaları (deterjan + parlatıcı dahil) + robot çöp kovası · K iç zarfı ----",
      "    # ---- v57 · BULAŞIK MAKİNESİ K ALTINDA (bulasik_cad_v1 · BM.X0/Y0/Z0 = KS.BULASIK_YER): gerçek parçalar ↔ K parçaları + robot çöp kovası · K iç zarfı · v58: deterjan YOK (kesme_cad_v5) → bulaşığın arkası + MEIKO arka payı BOŞ ----")
degis('    _det = [c_ for c_, _s in _KSP if c_.startswith("K:deterjan_")]',
      '    _det = [c_ for c_, _s in _KSP if c_.startswith("K:deterjan_")]                     # v58: deterjan / parlatıcı parçası OLMAMALI (kesme_cad_v5)')
degis("↔ K parcalari (%d, deterjan/parlatici %d dahil) + robot cop kovasi (%d)", "↔ K parcalari (%d · deterjan/parlatici %d — v58: YOK) + robot cop kovasi (%d)")
degis('"EVET" if _ic else "HAYIR", _gk(not _bm_cak and _ic)))', '"EVET" if _ic else "HAYIR", _gk(not _bm_cak and _ic and not _det)))')
degis('    assert not _bm_cak and _ic, "v57: bulasik makinesi K parcalarina / kovaya giriyor ya da K ic zarfindan tasiyor"',
      '    assert not _bm_cak and _ic and not _det, "v58: bulasik makinesi K parcalarina / kovaya giriyor, K ic zarfindan tasiyor ya da deterjan parcasi kaldi"')
blok("    _ap = FT.kut(BM.X0, BM.X0 + BM.W, BM.Y0, BM.Y0 + BM.H, KS.BULASIK_ARKA_PAY[0], KS.BULASIK_ARKA_PAY[1]).val()", "    # ---- v54 · HAVA ANA HATTI (yeniden yollandı)",
     '''    # v58 · bulaşığın ARKASI + MEIKO arka payı (eski kanister rafı + bidonlar + dozaj hortumlarının yeri): K arka sacının önünden makinenin arkasına kadar BOŞ
    _ab = FT.kut(BM.X0, BM.X0 + BM.W, BM.Y0, BM.Y0 + BM.H, -KS.D + KS.SAC, KS.BULASIK_ARKA_PAY[1]).val()
    _ab_k = []
    for c_, sc in _KSP:
        if _bbk(_ab, sc):
            v_ = _hacim(_ab, sc)
            if v_ > 1.0 or v_ < 0: _ab_k.append((round(v_, 1), c_))
    print("BULASIGIN ARKASI + MEIKO arka payi (v58 · deterjan yok · x %.1f-%.1f · y %.0f-%.0f · z %.1f…%.0f; arka pay %.0f…%.0f dahil) ↔ K parcalari: %s  %s"
          % (BM.X0, BM.X0 + BM.W, BM.Y0, BM.Y0 + BM.H, -KS.D + KS.SAC, KS.BULASIK_ARKA_PAY[1], KS.BULASIK_ARKA_PAY[0], KS.BULASIK_ARKA_PAY[1],
             "BOS" if not _ab_k else "%d BULGU %s" % (len(_ab_k), _ab_k[:6]), _gk(not _ab_k)))
    assert not _ab_k, "v58: bulasigin arkasinda / MEIKO arka payinda K parcasi var: %s" % _ab_k[:6]
''')

# ================================================================ 7b · ANİMASYON: robot topu çekmeceden açıcıya TAŞIR (v57 denetim bulgusu: top 1,3 m tek başına uçuyordu) ================================================================
degis('    ROB = Iz(RX0); ROB.git(0.3, 3.0, top_x)',
      '''    X_PARK = _cb["x"][0] - 110.0                                        # v58: robot çekmecenin AÇICI TARAFINDA, açık çekmeceye girmez (kaide yarı genişliği 90 + pay 20)
    X_ROB_AC = 700.0                                                   # v58: topu açıcıya bırakırken robot x (açıcı 350'ye erişim ≤ 915 · zincir yüzünden ≥ 508)
    ROB = Iz(RX0); ROB.git(0.3, 3.0, X_PARK); ROB.git(4.2, 5.6, X_ROB_AC)   # v58: top–robot birlikte gider (TOPX 4,2–5,6 ile aynı aralık)
    _ey = max(math.sqrt((TOPX(t_ / 20.0) - ROB(t_ / 20.0)) ** 2 + (TOPY(t_ / 20.0) - OMUZ) ** 2 + (TOPZ(t_ / 20.0) - RZ) ** 2) for t_ in range(70, 139))
    print("   v58 · ROBOT TOPU TASIR: park x %.1f (cekmece %.1f-%.1f disinda) → aciciya x %.0f · top–omuz en uzak %.0f mm (3,5–6,9 s) ≤ pratik erisim %.0f  %s"
          % (X_PARK, _cb["x"][0], _cb["x"][1], X_ROB_AC, _ey, ERISIM, _gk(_ey <= ERISIM)))
    assert _ey <= ERISIM, "v58: robot topa erisemiyor (%.0f > %.0f)" % (_ey, ERISIM)''')
degis("FR5 rayda çekmecenin önüne gelir.", "FR5 rayda çekmecenin yanına (açıcı tarafına) gelir; topu alıp açıcıya taşır.")

# ================================================================ 8 · durum.json 'pafta' metni + çıktı adları ================================================================
PAFTA = ("HAT v58 (27 Eyl gece) · ON TARAFLARA KAPAK YOK + DETERJAN YOK (Kemal: deterjanlari makinenin arkasina koyma, simdilik sil · on taraflara kapak koyma): "
         "K = kesme_cad_v5 (bulasigin arkasindaki kanister rafi + deterjan/parlatici bidonlari + dozaj hortumlari silindi, K_DETERJAN birimi yok; bulasik yeri ayni, "
         "arkasi + MEIKO arka payi BOS) · B = store_cad_v6 ayni (robot copu kapagi + klapesi yerinde, Kemal: robot copu seyleri kalsin) · animasyon: robot topu cekmeceden "
         "aciciya tasir (park x cekmecenin acici tarafi, birakis x 700, top-omuz <= 779 denetlenir) · E = kutu_cad_v6 (icecek yedeginin on alt saci kalkti → 6 koli onden acik; onde "
         "yalniz sol on dikme + dikey kablo kanali: tek koli duz gecer, koliler yana kaydirilip cekilir) · ACIK: deterjanin yeri, E ust on kapagi (on_ust_kapak) kalsin mi")
assert '"' not in PAFTA and "\\" not in PAFTA
degis('pafta="HAT v57 (27 Eyl) ·', 'pafta="' + PAFTA + ' · v57:')
s = s.replace('hat_v57.glb', 'hat_v58.glb').replace('hat_v57.usdz', 'hat_v58.usdz').replace('"hat_v57"', '"hat_v58"')

# ================================================================ 9 · SON DENETİM (üretilen metin) ================================================================
_kod = s[s.index('\nimport importlib, io'):]                                   # docstring (tarihçe) hariç
for _eski in ("import store_cad_v7", "import kesme_cad_v4", "import kutu_cad_v5", '"store_cad_v7.py"', '"kesme_cad_v4.py"', '"kutu_cad_v5.py"', "hat_v57.glb", "hat_v57.usdz", '"hat_v57"',
              '("K_DETERJAN"', '("deterjan_",)', "ROB.git(0.3, 3.0, top_x)", '"sarjor_yan_kapisi", "on_alt_sac"',"kapılar (üst PC pencereli, kilitli)", "beklenen: yalniz 2 dozaj hortumu",
              "mm arkasında → koli yana"):
    assert _eski not in _kod, "v58: eski ad / metin kaldi: %s" % _eski
for _yeni in ("import store_cad_v6 as SC", "import kesme_cad_v5 as KS", "import kutu_cad_v6 as KC", "_ION = KC.icecek_on_olcum()", "X_ROB_AC = 700.0", "hat_v58.glb", "hat_v58.usdz",
              'pafta="HAT v58', "BULASIGIN ARKASI + MEIKO arka payi", "v58 · K deterjan_ parcasi = 0"):
    assert _yeni in s, "v58: eksik: %s" % _yeni
compile(s, "hat_montaj_v58.py", "exec")
io.open(os.path.join(U, "hat_montaj_v58.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v58.py yazildi · %d satir" % s.count(NL))
