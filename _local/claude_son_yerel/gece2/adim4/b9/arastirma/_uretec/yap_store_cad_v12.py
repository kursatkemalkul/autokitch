# -*- coding: utf-8 -*-
"""store_cad_v11 → store_cad_v12 (29 Eyl 2026 · YEREL) — Kemal (alttan görünüş): "sağdaki yerde neden iki seyyar çubuk · ortadaki yerde havalandırma
şeyleri çubuğa çarpıyor, biraz sağa alman gerekmiyor muydu" + (kesit): "buralar neden birleşmiyor".
1 · K4 EMİŞ PENCERELERİ AÇIK: fırın altının ilk ayağı (ve altındaki enine alt şase profili, 60 geniş — moduler_montaj_v1 B 60×80×3) x 2517,5 → 2530:
    profil 2500–2560 → K4 sağ şerit penceresi (…2495,5) ile 4,5 boşluk; dikme (2502,5–2532,5) hâlâ profilin TAM üstünde. Denetim: hiçbir alt şase
    profili emiş penceresinin altına girmez.
2 · SAĞ UÇTA TEK ENİNE: x 3940'taki uç ayak çifti kalktı (hemen solundaki 3792,5 dikme ayağıyla 147 mm arayla ikinci profil oluyordu); sağ uç
    boyuna profillerle 207 konsol (60×80×3 · aşağıda hesap).
3 · K1 KABLO KANALI KÖŞESİ: üst yatay kanal K1'in dikey kanalının DIŞ kenarından (x +190) başlar → dikey ile yatay köşede birleşir (v11'de 40 × 25 boşluk).
Önceki: store_cad_v11.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v11.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v11 (29 Eyl 2026 · yap_store_cad_v11.py)',
      '"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v12 (29 Eyl 2026 · yap_store_cad_v12.py): K4 EMİŞ PENCERELERİ AÇIK (fırın altı ilk ayak 2530)'
      ' · SAĞ UÇTA TEK ENİNE (3940 ayakları kalktı) · K1 KABLO KANALI KÖŞESİ BİRLEŞİK' + NL + 'v11: ÜRETİM MODELİ v11 (29 Eyl 2026 · yap_store_cad_v11.py)')
degis('''AYAK_XZ = ([(x_, z_) for x_ in (60.0, 1000.0, 1960.0) for z_ in AYAK_Z] + [(x_, z_) for x_ in TD_X for z_ in AYAK_Z]
           + [(W_B - 60.0, z_) for z_ in (-110.0, -760.0)])''',
      '''ALT_SASE_YARI = 30.0                                                 # v12: B alt şase profili 60 geniş (moduler_montaj_v1 · 60×80×3) — ayak x'inde enine
AYAK_X_F = (2530.0, TD_X[1], TD_X[2])                                # v12: fırın altı ayak x'leri · 2517,5 → 2530 (K4 emiş penceresi 2495,5'e kadar) · 3940 KALKTI
AYAK_XZ = ([(x_, z_) for x_ in (60.0, 1000.0, 1960.0) for z_ in AYAK_Z] + [(x_, z_) for x_ in AYAK_X_F for z_ in AYAK_Z])   # v12: 12''')
# dikme desteği: profil (±30) dikmeyi (±15) tam taşır
degis('''            assert any(abs(xc_ - ax) < 0.05 and abs(zc_ - az) < 0.05 for ax, az in AYAK_XZ) or (
                any(abs(xc_ - ax) < 0.05 and abs(az - AYAK_Z[0]) < 0.05 for ax, az in AYAK_XZ) and any(abs(xc_ - ax) < 0.05 and abs(az - AYAK_Z[1]) < 0.05 for ax, az in AYAK_XZ)
                and AYAK_Z[1] < zc_ < AYAK_Z[0]), "%s altinda ayak / enine profil yok" % a''',
      '''            _px = [ax for ax, az in AYAK_XZ if abs(xc_ - ax) <= ALT_SASE_YARI - 15.0 + 0.01]      # v12: enine profil (±30) dikmeyi (±15) tam altından taşır
            assert _px and AYAK_Z[1] - 0.01 <= zc_ <= AYAK_Z[0] + 0.01 and all(any(abs(ax - px_) < 0.05 and abs(az - z_) < 0.05 for ax, az in AYAK_XZ) for px_ in _px[:1] for z_ in AYAK_Z), "%s altinda ayak / enine profil yok" % a''')
degis('''    assert {round(z_, 1) for _x, z_ in AYAK_XZ} == {round(z_, 1) for z_ in AYAK_Z}, "v11: ayak sirasi kenarda degil"''',
      '''    assert {round(z_, 1) for _x, z_ in AYAK_XZ} == {round(z_, 1) for z_ in AYAK_Z}, "v11: ayak sirasi kenarda degil"
    # v12 · K4 EMİŞ PENCERELERİ ↔ alt şase (enine: ayak x ± 30 · boyuna: ayak z ± 30 boydan boya) — pencerenin altı açık olmalı
    _kap = [(w_, "enine x %.1f" % ax) for w_ in EMIS_DELIK for ax in sorted({a_ for a_, _z in AYAK_XZ}) if ax - ALT_SASE_YARI < w_[1] - 0.01 and w_[0] + 0.01 < ax + ALT_SASE_YARI]
    _kap += [(w_, "boyuna z %.0f" % az) for w_ in EMIS_DELIK for az in AYAK_Z if az - ALT_SASE_YARI < w_[3] - 0.01 and w_[2] + 0.01 < az + ALT_SASE_YARI]
    _pay = min(min(abs(ax - ALT_SASE_YARI - w_[1]), abs(w_[0] - ax - ALT_SASE_YARI)) for w_ in EMIS_DELIK for ax in {a_ for a_, _z in AYAK_XZ})
    print("   v12 K4 EMIS PENCERELERI (%d) ↔ alt sase profilleri: %s · en yakin enine profil payi %.1f mm" % (len(EMIS_DELIK), "ACIK" if not _kap else "KAPALI %s" % _kap[:3], _pay))
    assert not _kap, "v12: alt sase profili K4 emis penceresini kapatiyor"
    _kons = W_B - max(a_ for a_, _z in AYAK_XZ); _q = 7.9e-6 * 9.81 * (60.0 * 80.0 - 54.0 * 74.0) + 0.5   # N/mm: profil + dolap payı [VARSAYIM 0,5 N/mm]
    _Ip = (60.0 * 80.0 ** 3 - 54.0 * 74.0 ** 3) / 12.0; _dk = _q * _kons ** 4 / (8.0 * 193000.0 * _Ip)
    print("   v12 SAG UC: tek enine x %.1f · konsol %.0f mm (60×80×3 · yayili %.2f N/mm VARSAYIM) -> uc sehim %.3f mm" % (max(a_ for a_, _z in AYAK_XZ), _kons, _q, _dk))
    assert _dk < 0.5''')
# K1 kablo kanalı köşesi
degis('ekle("kablo_kanali_ust", kut(K1X + KAN_X[1], K4X + KAN_X[1], KAN_UST[0]',
      'ekle("kablo_kanali_ust", kut(K1X + KAN_X[0], K4X + KAN_X[1], KAN_UST[0]')      # v12: K1 dikey kanalının dış kenarından → köşe birleşik
compile(s, "store_cad_v12.py", "exec")
io.open(os.path.join(U, "store_cad_v12.py"), "w", encoding="utf-8").write(s)
print("store_cad_v12.py yazildi")
