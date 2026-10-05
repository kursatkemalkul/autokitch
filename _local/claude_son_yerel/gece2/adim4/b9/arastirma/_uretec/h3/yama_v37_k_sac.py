# -*- coding: utf-8 -*-
"""yama_k_sac — K GÖVDESİ ÜRETİM SACI (h3_k_sac_v1) → hat3_montaj metnine bağlama TASLAĞI (2 Eki 2026 · Claude · YEREL · montaja YAZILMADI)

Kullanım (bir sonraki yap_hat3_montaj_vN.py içinde, hat3_montaj_v7 metni üzerinde — v6 metninde de çalışır):
    import importlib.util as _ilu; _sp = _ilu.spec_from_file_location("yama_k_sac", <bu dosya>); YK = _ilu.module_from_spec(_sp); _sp.loader.exec_module(YK)
    s = YK.uygula(s)          # her rep sayısı assert'li · zaten yamalıysa aynen döner · sonunda compile
Montaj işinde h3_k_sac_v1.py h3/ klasöründe olmalı (bu taslakta orada). Elektrik önbelleği (h3/_elk) DEĞİŞMEZ: hedef adlar 'ust_sac' ve 'sol_sac_urun_girisi' korunur,
delikler sacda zaten var (montajın _ELK_DELIK kesimi boşa keser, _eksik32 assert'i geçer).

REP'LER
  1 · K gövdesi: v7'de 'KP.bolge_K(KS.PARCALAR, V37_R)' satırı (h3_kapak_v1 taslağının K kapağı: DÜNYA koordinatıyla yazılmış, KS yerel → bb_kontrol assert'i düşerdi)
      → 'KSAC.uygula_ks(KS, V37_R)' (eski 21 gövde parçası çıkar · 336 üretim parçası girer, tek kapak dahil) · v6 metninde KS.modul()'den hemen sonra.
  2 · K_BIRIM K_GOVDE öneklerine 'govde_' (kulak / bağlantı / M8 noktası parçaları) + birim metni.
  3 · (yalnız v7) kapak açılma taraması: KS parçaları dünyaya taşınarak engel olur · _K37['onyuz_kapak_K'] = kapakla dönen bütün parçalar (dış + iç tava, kanat yarıları, kaynaklar).
"""
import io, os, sys, runpy

ISARET = "# ---- K_SAC_V1"
_KP_K = "KP.bolge_K(KS.PARCALAR, V37_R)"
_KS_MODUL = "KS.modul()\n"
_ONEK_ESKI = '("ayak_", "taban_sac", "taban_hortum_rakoru", "plint_on", "istasyon_tabani", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "kose_dikmesi", "onyuz_")),'
_ONEK_YENI = '("ayak_", "taban_sac", "taban_hortum_rakoru", "plint_on", "istasyon_tabani", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "kose_dikmesi", "onyuz_", "govde_")),'
_BIRIM_ESKI = 'taban 788 · istasyon tabanı 892 · ön alt bant sacı + 2 ön kapak (tava 20, ön düzlem +79)",'
_BIRIM_YENI = ('taban 788 · istasyon tabanı 892 · ÜRETİM SACI (h3_k_sac_v1): 30×30×2 kaynaklı iskelet + 1,5 bükümlü paneller (R 2,25 · K 0,45) + PEM/FHP + '
               'tek çift cidarlı kapak (3 gizli menteşe · 3 bas-aç) · ön düzlem +79",')
_SUP_E = "(KS, KS.PARCALAR), (KC, KC.PARCALAR), (SC, SC.PARCALAR)):"
_SUP_E_YENI = "(KS, KSAC.dunya_listesi(KS.PARCALAR)), (KC, KC.PARCALAR), (SC, SC.PARCALAR)):"
_SUP_K = '_K37 = {p_["ad"]: KP.sekil(p_) for _L in (AK.PARCALAR, KS.PARCALAR, KC.PARCALAR) for p_ in _L}'
_SUP_K_YENI = ('_K37 = {p_["ad"]: KP.sekil(p_) for _L in (AK.PARCALAR, KSAC.dunya_listesi(KS.PARCALAR), KC.PARCALAR) for p_ in _L}\n'
               '    _K37["onyuz_kapak_K"] = KSAC.kapak_dunya(KS.PARCALAR)                                   ' + ISARET + ' · K kapağı: kapakla dönen bütün parçalar (dünya)')


def _say(s, a, n, ad):
    c = s.count(a)
    assert c == n, "yama_k_sac: %s çapası %d (beklenen %d): %s" % (ad, c, n, a[:80])
    return c


def uygula(s, rapor=None):
    """hat3_montaj metni → K üretim sacı gövdesi bağlı metin · her rep sayısı assert'li · idempotent · compile"""
    if ISARET in s:
        return s
    say = []
    if _KP_K in s:                                                                     # v7 (h3_kapak_v1 taslağı)
        _say(s, _KP_K, 1, "v7 KP.bolge_K")
        satir = [l for l in s.split("\n") if _KP_K in l][0]
        s = s.replace(satir + "\n", "import h3_k_sac_v1 as KSAC                                                                 " + ISARET +
                      " · K gövdesi üretim sacı (tek kapak dahil; h3_kapak_v1.bolge_K yerine)\nKSAC.uygula_ks(KS, V37_R)\n", 1); say.append(("v7 KP.bolge_K → KSAC", 1))
        v7 = True
    else:                                                                              # v6
        _say(s, _KS_MODUL, 1, "v6 KS.modul()")
        s = s.replace(_KS_MODUL, _KS_MODUL + "import h3_k_sac_v1 as KSAC                                                                 " + ISARET +
                      " · K gövdesi üretim sacı\nKSAC.uygula_ks(KS, [])\n", 1); say.append(("v6 KS.modul() + KSAC", 1))
        v7 = False
    _say(s, _ONEK_ESKI, 1, "K_GOVDE önekleri"); s = s.replace(_ONEK_ESKI, _ONEK_YENI, 1); say.append(("K_GOVDE + govde_", 1))
    _say(s, _BIRIM_ESKI, 1, "K_GOVDE metni"); s = s.replace(_BIRIM_ESKI, _BIRIM_YENI, 1); say.append(("K_GOVDE metni", 1))
    if v7:
        _say(s, _SUP_E, 1, "v7 süpürme engel listesi"); s = s.replace(_SUP_E, _SUP_E_YENI, 1); say.append(("v7 süpürme engelleri KS dünya", 1))
        _say(s, _SUP_K, 1, "v7 süpürme kapak sözlüğü"); s = s.replace(_SUP_K, _SUP_K_YENI, 1); say.append(("v7 süpürme K kapağı bileşik", 1))
    compile(s, "hat3_montaj_k_sac", "exec")
    if rapor is not None: rapor.extend(say)
    return s


def _v7_metni(h3):
    """yap_hat3_montaj_v7.py --kuru: v6 metni + v7 yamaları BELLEKTE (hiçbir dosyaya yazmaz, v6 üretecini çalıştırmaz)"""
    eski = list(sys.argv)
    try:
        sys.argv = [os.path.join(h3, "yap_hat3_montaj_v7.py"), h3, "--kuru"]
        g = runpy.run_path(os.path.join(h3, "yap_hat3_montaj_v7.py"), run_name="yap_v7_kuru")
    finally:
        sys.argv = eski
    sorun = [x for x in g["N"] if not x[0]]
    return g["s"], len(g["N"]), sorun


if __name__ == "__main__":
    BUR = os.path.dirname(os.path.abspath(__file__))
    H3 = os.path.abspath(os.path.join(BUR, "..", "b3", "arastirma", "_uretec", "h3"))
    print("=== yama_k_sac · KURU DENEME (yalnız sayım + compile · hiçbir dosya yazılmaz) ===")
    s6 = io.open(os.path.join(H3, "hat3_montaj_v6.py"), encoding="utf-8").read()
    r6 = []; t6 = uygula(s6, r6); assert uygula(t6) == t6
    print("v6 metni: %s · derlendi · %+d karakter" % (r6, len(t6) - len(s6)))
    s7, n7, sorun7 = _v7_metni(H3)
    print("v7 metni bellekte kuruldu (yap_hat3_montaj_v7 --kuru): %d yama · sorunlu %d %s" % (n7, len(sorun7), [x[2][:50] for x in sorun7]))
    r7 = []; t7 = uygula(s7, r7); assert uygula(t7) == t7
    print("v7 metni: %s · derlendi · %+d karakter" % (r7, len(t7) - len(s7)))
    for a, b in ((_KP_K, 0), ("KSAC.uygula_ks(KS, V37_R)", 1), ('"onyuz_", "govde_"))', 1), ("KSAC.kapak_dunya(KS.PARCALAR)", 1), ("KSAC.dunya_listesi(KS.PARCALAR)", 2)):
        assert t7.count(a) == b, (a, t7.count(a), b)
    print("v7 sonrası sayım: KP.bolge_K 0 · KSAC.uygula_ks 1 · govde_ öneki 1 · kapak_dunya 1 · dunya_listesi 2 → TAMAM")
    sys.stdout.flush(); os._exit(0)
