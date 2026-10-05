# -*- coding: utf-8 -*-
"""h3/hat3_montaj_v1.py → h3/hat3_montaj_v2.py (HAT v3.2) — metin yaması, her değişiklik sayısı denetlenir.
v3.2 (Kemal 30 Eyl gece): kutu yedeği 4 gün (U_F rafına ek yığın) · elektrik tesisatı · havada kalan cihazların montajı · ana PC + ağ · kategori eksikleri.
ADIM 1 (bu dosyanın ilk hali): DÜNYA KATI DÖKÜMÜ — her TC_AG çağrısındaki parça (birim, ad, malzeme, dünya katısı) h3/_dunya/ altına BREP + dizin olarak yazılır
(havada / çakışma / kablo yolu denetimleri montajı yeniden koşmadan bu dökümden yapılır)."""
import io, os, sys
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
KAYNAK = os.path.join(H3, "hat3_montaj_v1.py"); HEDEF = os.path.join(H3, "hat3_montaj_v2.py")
s = io.open(KAYNAK, encoding="utf-8").read()
N = [0]


def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, "yama bulunamadı (%d ≠ %d): %r" % (c, n, a[:140])
    s = s.replace(a, b); N[0] += 1


rep('''"""hat3_montaj_v1 (30 Eyl 2026 · Claude · YEREL) · HAT VERSİYON 3''',
    '''"""hat3_montaj_v2 (30 Eyl 2026 gece · Claude · YEREL) · HAT v3.2 — v3.1 + kutu yedeği 4 gün · elektrik tesisatı · cihaz montajı · ana PC + ağ (yap_hat3_montaj_v2).

--- v3.1 başlığı ---
hat3_montaj_v1 (30 Eyl 2026 · Claude · YEREL) · HAT VERSİYON 3''')
# ---- dünya katı dökümü (TC_AG kancası) ----
rep('''            kat_ = (bv_["kod"], pv_["ad"], pv_.get("mal"))                                        # v91: ağ kendi parçasını taşır → GLB'de kategori aralığı''',
    '''            kat_ = (bv_["kod"], pv_["ad"], pv_.get("mal"))                                        # v91: ağ kendi parçasını taşır → GLB'de kategori aralığı
            DUNYA_KATI.append((bv_["kod"], pv_["ad"], pv_.get("mal") or "", pv_.get("grup", "SABIT") or "SABIT", sh_))   # v3.2 · döküm''')
rep('''import linecache as _lc62
PARCA_KUTU = {}''', '''import linecache as _lc62
PARCA_KUTU = {}
DUNYA_KATI = []                                                                                    # v3.2 · (birim, ad, mal, grup, dünya katısı) — h3/_dunya/ dökümü''')
rep('''    print("v62 · parca_kutulari.json: %d birim · %d parca kutusu" % (len(PARCA_KUTU), sum(len(v) for v in PARCA_KUTU.values())))''',
    '''    print("v62 · parca_kutulari.json: %d birim · %d parca kutusu" % (len(PARCA_KUTU), sum(len(v) for v in PARCA_KUTU.values())))
    # v3.2 · DÜNYA KATI DÖKÜMÜ (E'nin menteşe düğümündeki yerel kopyaları parca_kutulari gibi süzülür)
    _DD = os.path.join(U, "h3", "_dunya"); os.makedirs(_DD, exist_ok=True)
    _dz = [d_ for d_ in DUNYA_KATI if not (d_[0].startswith("E_") and d_[4].BoundingBox().xmin < X_E - 5.0)]
    cq.Compound.makeCompound([d_[4] for d_ in _dz]).exportBrep(os.path.join(_DD, "dunya.brep"))
    json.dump([[d_[0], d_[1], d_[2], d_[3]] for d_ in _dz], io.open(os.path.join(_DD, "dunya.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("v3.2 · dunya katı dökümü: %d parça (%d süzüldü) → h3/_dunya/" % (len(_dz), len(DUNYA_KATI) - len(_dz)))''')
for a_, b_ in (("hat3_v1.glb", "hat3_v2.glb"), ("hat3_v1.usdz", "hat3_v2.usdz"), ('"hat3_v1"', '"hat3_v2"')):
    assert s.count(a_) >= 1, a_
    s = s.replace(a_, b_); N[0] += 1
rep('''surum="v3.1", pafta="HAT v3.1 (30 Eyl · Claude · YEREL): ''', '''surum="v3.2", pafta="HAT v3.2 (1 Eki · Claude · YEREL): KUTU YEDEĞİ 4 GÜN (U_F rafında fırın üstü yığının üstüne 170 kutu · şarjör 419 + fırın üstü 320 + U_F 170 = 909 ≥ 720) · ELEKTRİK TESİSATI (h3_elektrik_v1): QR ana panosu yükseltildi (ana şalter · kaçak akım 30 mA · 6 sigorta · 24 V · ANA BİLGİSAYAR RevPi Connect 4 ekransız · 8 port switch · 4G/Wi-Fi modem → iPad / telefondan web paneli) · zemin kanalı güç bölmesi → makine · dolap teknik sütun dikey kanalı · E sağ-ön dış dikey kanal · üst hat kanalı U_KE → U_F → TOPPING · istasyon cihaz kabloları kanallara / panolara (TOPPING KD1 + KD2 kanalı · A dikey kanal + 8 port M12 dağıtıcı · dolap reed sensörleri kolon kanallarına), uzun açık parçalar P-kelepçeli, sac geçişleri IP68 rakorlu · HAVADA KALANLAR monte edildi (tezgâh duvar kaplama sacı · serpantin tutucuları · E oluk flanşı · QR göz braketleri) · AÇIK: E iç kablolaması (E üretime hazır değil), pano içi kablolar şemaya göre, fırın + kompresör bina tesisat bandından || HAT v3.1 (30 Eyl · Claude · YEREL): ''')
rep('''V2_DENETIM = ("Denetim (v3.1): TOPPING statik''', '''V2_DENETIM = ("Denetim (v3.2): TOPPING statik''')
# ================= ADIM 2 · v3.2 KATMANLARI =================
# (a) üst depo v2 (U_F rafında pizza kutusu yedeği 170)
rep("import h3_ust_depo_v1 as UD", "import h3_ust_depo_v2 as UD")
rep('''_dis_birim(UD, "GERCEK_UST", "h3_ust_depo_v1.py", "hat/makine_v3.html")''', '''_dis_birim(UD, "GERCEK_UST", "h3_ust_depo_v2.py", "hat/makine_v3.html")
import h3_elektrik_v1 as EL, h3_duzeltme_v1 as DZM                                 # v3.2 · elektrik tesisatı (önbellek h3/_elk) + havada kalan parçaların montajı
EL.yukle(); DZM.kur()
_dis_birim(EL, "GERCEK_ELEKTRIK", "h3_elektrik_v1.py", "hat/makine_v3.html")
_dis_birim(DZM, "GERCEK_DUZELTME", "h3_duzeltme_v1.py", "hat/makine_v3.html")
_ELK_ONEK = {"TC": ("TOPPING_MODUL",), "TU": ("TOPPING",), "KS": ("K_",), "KC": ("E_",), "SC": ("B_", "CEK_"), "FU": ("F_",), "UD": ("U_",),
             "QR": ("QR_",), "RE": ("ROBOT", "ZEMIN"), "AK": ("A_",), "FT": ("F_TP10",)}                          # modül → montaj birim öneki (delikler dünya kesicisi)
_ELK_DELIK = {}
for _m32, _a32, _k32, _n32 in EL.DELIKLER: _ELK_DELIK.setdefault(_a32, []).append((_ELK_ONEK[_m32], _k32))
_ELK_DUS = set(_a32 for _m32, _a32 in EL.DUSUR)
_ELK_KESILEN = set()''')
# (b) QR: elektrik katmanının yükseltilmiş ana panosu eskisinin yerine
rep('''QR.kur()
_dis_birim(QR, "GERCEK_QR", "qr_cad_v1.py", "hat/service.html")''', '''QR.kur()
QR.PARCALAR[:] = [p_ for p_ in QR.PARCALAR if p_["ad"] not in _ELK_DUS]                           # v3.2 · ana pano yükseltildi (h3_elk_qr_v1)
QR.BIRIMLER[:] = [(k_, a_) for k_, a_ in QR.BIRIMLER if any(p_["birim"] == k_ for p_ in QR.PARCALAR)]
_dis_birim(QR, "GERCEK_QR", "qr_cad_v1.py", "hat/service.html")''')
# (c) malzemeler + dünya üreteçleri
rep('''for _M in (KD, RE, QR, TZ):
    for _k, _v in _M.MALZEME.items():''', '''for _M in (KD, RE, QR, TZ, EL, DZM):
    for _k, _v in _M.MALZEME.items():''')
rep('''"GERCEK_FIRIN_UST": FU, "GERCEK_UST": UD}''', '''"GERCEK_FIRIN_UST": FU, "GERCEK_UST": UD, "GERCEK_ELEKTRIK": EL, "GERCEK_DUZELTME": DZM}''')
# (d) delikler: her parça ağlanmadan önce dünya kesicisiyle kesilir (döküm de kesik hali alır)
rep('''            sh_ = wp.val() if hasattr(wp, "val") else wp; bb_ = sh_.BoundingBox()''', '''            sh_ = wp.val() if hasattr(wp, "val") else wp; bb_ = sh_.BoundingBox()
            for _pf32, _kc32 in _ELK_DELIK.get(pv_["ad"], ()):                                   # v3.2 · elektrik geçiş delikleri
                if bv_["kod"].startswith(_pf32):
                    sh_ = sh_.cut(_kc32); wp = cq.Workplane(obj=sh_); bb_ = sh_.BoundingBox(); _ELK_KESILEN.add(pv_["ad"])''')
# (e) kategoriler: elektrik katmanı GÜÇ / KONTROL · tezgâh duvarı DÜKKÂN · serpantin tutucu SOĞUTMA · kutu yedeği ÜRÜN
rep('''def _kat_birim(kod):
    if kod in KAT_BIRIM: return KAT_BIRIM[kod]''', '''def _kat_birim(kod):
    if kod in KAT_BIRIM: return KAT_BIRIM[kod]
    if kod.startswith("ELK_"): return "GUC"                                                       # v3.2 · elektrik katmanı (kategori_bul ada göre KONTROL ayırır)
    if kod == "DUZ_TEZGAH_DUVAR": return "DUKKAN"
    if kod == "DUZ_B_SERPANTIN": return "SOGUTMA"
    if kod == "U_KUTU_YEDEK": return "URUN"''')
rep('''def kategori_bul(birim, ad, mal):
    kb = _kat_birim(birim)''', '''_KR_ELK_K = _re61.compile(r"hmi|revpi|bilgisayar|ag_anahtar|modem|dagitici|veri|ethernet|plc|sensor|reed|emniyet|isik_perdesi|tarti|pm1704|smt8m|kilit", _re61.I)


def kategori_bul(birim, ad, mal):
    if birim.startswith("ELK_"): return "KONTROL" if _KR_ELK_K.search(ad or "") else "GUC"      # v3.2
    kb = _kat_birim(birim)''')
# (f) döküm: temel döküm elektrik + düzeltme katmanı HARİÇ (elektrik yol bulucusu bunu okur) · tam döküm _dunya_tam (havada denetimi)
rep('''    _dz = [d_ for d_ in DUNYA_KATI if not (d_[0].startswith("E_") and d_[4].BoundingBox().xmin < X_E - 5.0)]''',
    '''    _tam = [d_ for d_ in DUNYA_KATI if not (d_[0].startswith("E_") and d_[4].BoundingBox().xmin < X_E - 5.0)]
    _DT = os.path.join(U, "h3", "_dunya_tam"); os.makedirs(_DT, exist_ok=True)
    cq.Compound.makeCompound([d_[4] for d_ in _tam]).exportBrep(os.path.join(_DT, "dunya.brep"))
    json.dump([[d_[0], d_[1], d_[2], d_[3]] for d_ in _tam], io.open(os.path.join(_DT, "dunya.json"), "w", encoding="utf-8"), ensure_ascii=False)
    _dz = [d_ for d_ in _tam if not d_[0].startswith(("ELK_", "DUZ_"))]
    _eksik32 = sorted(set(a_ for m_, a_, k_, n_ in EL.DELIKLER) - _ELK_KESILEN)
    print("v3.2 · elektrik delikleri: %d parça kesildi · kesilemeyen %s" % (len(_ELK_KESILEN), _eksik32))
    assert not _eksik32, _eksik32''')

# (g) v48 karton kulesi yasağı: v3.2'nin U_F kutu yedeği (U_KUTU_YEDEK) bilinçli — yasak yalnız eski kuleye
rep('''or b["kod"].endswith("KUTU_YEDEK")], "yedek karton kutu hala var"''', '''or (b["kod"].endswith("KUTU_YEDEK") and b["kod"] != "U_KUTU_YEDEK")], "yedek karton kutu hala var"''')
# (h) ön yüz kuralı: koridor / S modülü tarafındaki elektrik + tezgâh duvar sacı (QR, tezgâh, zemin kanalı gibi) kural dışı
rep('''    _IST = ("ROBOT", "QR", "TEZGAH", "ZEMIN_KANALI", "URUN__")''', '''    _IST = ("ROBOT", "QR", "TEZGAH", "ZEMIN_KANALI", "URUN__", "ELK_QR", "ELK_ANA_PANO", "ELK_ZEMIN_KANALI", "DUZ_TEZGAH")   # v3.2''')
io.open(HEDEF, "w", encoding="utf-8").write(s)
print("hat3_montaj_v2.py yazıldı · %d yama" % N[0])
