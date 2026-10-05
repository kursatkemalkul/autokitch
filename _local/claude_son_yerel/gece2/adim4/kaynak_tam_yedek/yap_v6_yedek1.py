# -*- coding: utf-8 -*-
"""h3/hat3_montaj_v5.py (v3.5) → h3/hat3_montaj_v6.py (HAT v3.6 · 1 Eki 2026 · Claude · YEREL) — metin yaması, her değişiklik sayısı denetlenir.
Kemal 1 Eki: "bütün makinedeki alt eteği kaldır" · "bozuk zemini yeniden modelle" · "gövde üzerinde neden havada çubuklar var · şu boşluğu doldur".
  · ETEK: B (onyuz_plint + 2 dönüş) ve E (onyuz_plint) süpürgelikleri montajdan düşer → ayarlı ayaklar + alt şase görünür (kabul).
    Plintlere bağlı braket / vida / klips YOK (dökümde tarandı). QR tekmeliği (ELK_QR_MONTAJ, kablo girişleri üstünde) ve tezgâh plinti dükkân/elektrik katmanında — DÜŞMEZ.
    DİKKAT: elektrik önbelleğinde plintlere 3 delik var (KC onyuz_plint ×2, SC onyuz_plint_donus_sag) → elektrik ajanı kendi dosyasında temizlemeden
    tam montajda '_eksik32' assert'ü bunları listeler (tolerans EKLENMEDİ, Kemal kuralı).
  · ZEMİN: v3.5'e kadar ayrı zemin yoktu (yer = robot rayı kutusu + zincir oluğu + kanallar + sayfa ızgarası) → h3_zemin_v2: tek düzen karo zemin, üst yüz y 0.
  · HAVADA ÇUBUK / ÖN BOŞLUK: tarama sonuçları ve yapılanlar aşağıda (V36_* blokları).
  · h3_ana_pano_v1 varsa ANA_PANO birimi · yap_mek_v1 varsa mekanizma ağacı yaması."""
import io, os, runpy, importlib, sys
H3 = os.path.dirname(os.path.abspath(__file__))
if H3 not in sys.path: sys.path.insert(0, H3)
runpy.run_path(os.path.join(H3, "yap_hat3_montaj_v5.py"))                     # önce v3.5 (hat3_montaj_v5.py)
s = io.open(os.path.join(H3, "hat3_montaj_v5.py"), encoding="utf-8").read()
N = [0]


def rep(a, b, n=None):
    global s
    c = s.count(a)
    assert c >= 1 and (n is None or c == n), (a[:100], c)
    s = s.replace(a, b); N[0] += 1


rep("hat3_v5", "hat3_v6")
rep('surum="v3.5"', 'surum="v3.6"', 1)

# ---- 1 · ALT ETEK (süpürgelik) düşer: B dolabı + E ----
rep("SC_OZET = {k: (t, n) for k, t, n, _u, _a in SC.modul()}\n",
    "SC_OZET = {k: (t, n) for k, t, n, _u, _a in SC.modul()}\n"
    "V36_ETEK = (\"onyuz_plint\", \"plint_on\")                                              # v3.6 · Kemal: \"bütün makinedeki alt eteği kaldır\" (ayaklar görünür)\n"
    "V36_DUSEN = [\"B|\" + p_[\"ad\"] for p_ in SC.PARCALAR if p_[\"ad\"].startswith(V36_ETEK)]\n"
    "SC.PARCALAR[:] = [p_ for p_ in SC.PARCALAR if not p_[\"ad\"].startswith(V36_ETEK)]\n", 1)
rep("KC.modul()\n",
    "KC.modul()\n"
    "V36_DUSEN += [\"E|\" + p_[\"ad\"] for p_ in KC.PARCALAR if p_[\"ad\"].startswith(V36_ETEK)]\n"
    "KC.PARCALAR[:] = [p_ for p_ in KC.PARCALAR if not p_[\"ad\"].startswith(V36_ETEK)]\n"
    "print(\"v3.6 · ALT ETEK KALKTI: %d parça (%s) · ayarlı ayaklar görünür\" % (len(V36_DUSEN), \", \".join(V36_DUSEN)))\n"
    "assert sorted(V36_DUSEN) == sorted([\"B|onyuz_plint\", \"B|onyuz_plint_donus_sol\", \"B|onyuz_plint_donus_sag\", \"E|onyuz_plint\"]), V36_DUSEN\n", 1)

# ---- 2 · ZEMİN (h3_zemin_v2) + 5 · ANA PANO (h3_ana_pano_v1, varsa) ----
_ZM = '''
import h3_zemin_v2 as ZM                                                                    # v3.6 · Kemal: "bozuk zemini yeniden modelle" — tek düzen karo zemin, üst yüz y 0
ZM.kur()
for _k, _v in ZM.MALZEME.items():
    MALZEME.setdefault(_k, dict(renk=_v["renk"], met=_v["met"], ruf=_v["ruf"], saydam=False))
_dis_birim(ZM, "GERCEK_ZEMIN", "h3_zemin_v2.py", "hat/makine_v3.html")
AP = None
if os.path.exists(os.path.join(U, "h3", "h3_ana_pano_v1.py")):                            # v3.6 · ana pano modülü (başka ajan) — dosya yoksa atlanır
    import h3_ana_pano_v1 as AP
    AP.kur()
    if not hasattr(AP, "BIRIMLER"):
        AP.BIRIMLER = [("ANA_PANO", "Ana pano (h3_ana_pano_v1)")]
        for p_ in AP.PARCALAR: p_["birim"] = "ANA_PANO"
    if not hasattr(AP, "BIRIM_MODUL"): AP.BIRIM_MODUL = {k_: "S" for k_, _a in AP.BIRIMLER}
    for p_ in AP.PARCALAR:
        p_.setdefault("birim", "ANA_PANO"); p_.setdefault("grup", "SABIT"); p_.setdefault("mal", "paslanmaz")
        if "wp" not in p_ and "sh" in p_: p_["wp"] = p_["sh"]
    if not hasattr(AP, "dunya"): AP.dunya = lambda p_: (p_["wp"].val() if hasattr(p_["wp"], "val") else p_["wp"])
    for _k, _v in getattr(AP, "MALZEME", {}).items():
        _r = _v.get("renk", _v[0] if isinstance(_v, (tuple, list)) else (0.8, 0.82, 0.84, 1.0))
        MALZEME.setdefault(_k, dict(renk=_r, met=_v.get("met", 0.5) if isinstance(_v, dict) else 0.5, ruf=_v.get("ruf", 0.4) if isinstance(_v, dict) else 0.4,
                                    saydam=_v.get("saydam", False) if isinstance(_v, dict) else False))
    for p_ in AP.PARCALAR:
        MALZEME.setdefault(p_["mal"], dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.3, saydam=False))
    _dis_birim(AP, "GERCEK_ANA_PANO", "h3_ana_pano_v1.py", "hat/makine_v3.html")
    print("v3.6 · ANA PANO (h3_ana_pano_v1): %d parça · birim %s" % (len(AP.PARCALAR), [k_ for k_, _a in AP.BIRIMLER]))
else:
    print("v3.6 · ANA PANO: h3_ana_pano_v1.py yok — atlandı")
'''
rep('_dis_birim(TZ, "GERCEK_TEZGAH", "tezgah_cad_v2.py", "hat/service.html")\n',
    '_dis_birim(TZ, "GERCEK_TEZGAH", "tezgah_cad_v2.py", "hat/service.html")\n' + _ZM, 1)
rep("\n# ---- v57 · YOLCULUK SEÇİMLERİ",
    '\nGERCEK_DIS["GERCEK_ZEMIN"] = ZM                                                          # v3.6\n'
    'if AP is not None: GERCEK_DIS["GERCEK_ANA_PANO"] = AP\n'
    "\n# ---- v57 · YOLCULUK SEÇİMLERİ", 1)
rep("    if kod in KAT_BIRIM: return KAT_BIRIM[kod]\n",
    "    if kod in KAT_BIRIM: return KAT_BIRIM[kod]\n"
    "    if kod == \"ZEMIN_DOSEME\": return \"DUKKAN\"                                                 # v3.6 · zemin\n"
    "    if kod == \"ANA_PANO\": return \"GUC\"                                                        # v3.6 · ana pano\n", 1)
rep('_IST = ("ROBOT", "QR", "TEZGAH", "ZEMIN_KANALI",', '_IST = ("ZEMIN_DOSEME", "ANA_PANO", "ROBOT", "QR", "TEZGAH", "ZEMIN_KANALI",', 1)

# ---- 3 · HAVADA ÇUBUK / ÖN BOŞLUK (tarama: dökümde ön yüze uzanan 303 çubuk/dikme/kayıt adayı BRepExtrema ≤ 0,5 mm ile → HİÇ temassız yok;
#      tek temaslılar kapak omegaları (kendi saydam kapağına kaynaklı), kablo uçları (rakorda), menteşe/kulp — hepsi bağlı.
#      Ön görünüş z-tamponu: saydam kapaklar dahil 10 mm'den büyük delik yalnız işlevsel ağızlar (A robot ağzı · E çatal ağzı) + plint yarıkları;
#      opak görünüşte fırın üstü kabinin ön ÜST bandı (x 2503–3997 · y 1830,5–1860,5) boydan boya arka duvara kadar açıktı — A ve K'da üst kayıt var, F'de yoktu
#      → aynı 30 × 30 × 2 profille ön üst kayıt; ön dikme artık kayıt–dikme–kayıt çerçevesinin parçası, tavan kirişinin açık ucu kaydın arkasında kalır.)
_FU36 = r'''
if not any(p_["ad"].startswith("onyuz_f_ust_ust_kayit") for p_ in FU.PARCALAR):                # v3.6 · Kemal: "şu boşluğu doldur" — fırın üstü kabinin ön ÜST kaydı yoktu
    _fk36 = [p_ for p_ in FU.PARCALAR if p_["ad"] == "onyuz_f_ust_kayit"]; _kk36 = [p_ for p_ in FU.PARCALAR if p_["ad"] == "f_ust_tavan_kirisi"]
    assert len(_fk36) == 1 and len(_kk36) == 1, "v3.6 · fırın üstü alt kayıt / tavan kirişi yok"
    _fb36 = FU.dunya(_fk36[0]).BoundingBox(); _kb36 = FU.dunya(_kk36[0]).BoundingBox()
    # alt kayıtla aynı 30 × 30 × 2 profil, aynı z (27–57) · y = tavan kirişi (1830,5–1860,5: A'nın üst kaydıyla aynı kot) · x yan sac üst bükümleri arası
    _uk36 = FU.kutu_profil_x(_fb36.xmin + 1.5, _fb36.xmax - 1.5, _kb36.ymin, _kb36.ymax, _fb36.zmin, _fb36.zmax)
    FU.ekle("onyuz_f_ust_ust_kayit", _uk36, "paslanmaz", "F_UST_KABIN", kaynak="v3.6 montaj (Kemal: boşluğu doldur)",
            bom=("Ön üst kayıt 304 kutu profil 30 × 30 × 2 · L %.0f" % (_fb36.xlen - 3.0), 1, "üretim",
                 "yan sacların üst bükümlerine + tavan kirişinin ön ucuna kaynaklı · ön dikmenin üstünü kapatır (A üst kaydıyla aynı kot 1830,5–1860,5)", "ÜRETİM"))
    _kk36[0]["wp"] = cq.Workplane(obj=FU.dunya(_kk36[0]).cut(cq.Solid.makeBox(_fb36.xlen, _kb36.ylen + 2.0, _fb36.zlen + 1.0,
                                                                                     cq.Vector(_fb36.xmin, _kb36.ymin - 1.0, _fb36.zmin))))   # kiriş kayda alın alına (önü kaydın arkasında biter)
    print("v3.6 · FIRIN ÜSTÜ ÖN ÜST KAYIT eklendi: x %.1f–%.1f · y %.1f–%.1f · z %.0f–%.0f (tavan kirişi kaydın arkasında %.0f'de biter)"
          % (_fb36.xmin + 1.5, _fb36.xmax - 1.5, _kb36.ymin, _kb36.ymax, _fb36.zmin, _fb36.zmax, _fb36.zmin))
'''
rep('_dis_birim(FU, "GERCEK_FIRIN_UST", "firin_ust_kabin_cad_v1.py", "hat/oven.html")\n',
    _FU36.lstrip("\n") + '_dis_birim(FU, "GERCEK_FIRIN_UST", "firin_ust_kabin_cad_v1.py", "hat/oven.html")\n', 1)

# ---- 4 · pafta ----
V36_PAFTA = ("HAT v3.6 (1 Eki · Claude · YEREL): ALT ETEK KALKTI (B dolabı plinti + 2 dönüşü, E plinti · ayarlı ayaklar + alt şase görünür) · "
             "ZEMİN YENİDEN: tek düzen 600 × 600 karo + şap, üst yüz y 0 (önceden ayrı zemin yoktu) · "
             "FIRIN ÜSTÜ ÖN ÜST KAYIT (boşluk doldu, A ile aynı kot 1830,5–1860,5) · havada çubuk taraması: temassız parça yok (görünen çubuklar saydam kapak omegaları + TOPPING orta dikmesi) · "
             "ANA PANO modülü (varsa) · mekanizma ağacı (yap_mek_v1) || ")
rep('pafta="HAT v3.5 (1 Eki · Claude · YEREL): ', 'pafta="' + V36_PAFTA + 'HAT v3.5 (1 Eki · Claude · YEREL): ', 1)

# ---- mekanizma ağacı (sayfa ajanı) ----
if os.path.exists(os.path.join(H3, "yap_mek_v1.py")):
    import yap_mek_v1 as YM
    s = YM.uygula(s); N[0] += 1
    print("yap_mek_v1 uygulandı")
compile(s, "hat3_montaj_v6", "exec")
io.open(os.path.join(H3, "hat3_montaj_v6.py"), "w", encoding="utf-8").write(s)
print("hat3_montaj_v6.py yazıldı · %d yama" % N[0])
