# -*- coding: utf-8 -*-
"""hat_montaj_v71 → hat_montaj_v72 (29 Eyl 2026) — BAĞIMSIZ İSTASYONLAR ANA MONTAJA (Kemal: "Codex'in modüler işini bizimkine ekle, yaptığın değişikliklerin üstüne").
moduler_montaj_v1 (Codex moduler_istasyon_v1 yöntemi) v71'in üreteç parçalarına uygulanır: A sağ duvarı + A–C contası · B/K/E alt şase + M12 yuvaları ·
B içinde A/C taşıyıcı + GFRP · B–K, K–E, A/C→B bağlamaları · köpük/sac cepleri. Bantlı tabla + fırın 1316 aynen. Çıktılar hat_v72."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v71.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120])
    s = s.replace(a, b)


degis('pafta="HAT v71 (29 Eyl) ·', 'pafta="HAT v72 (29 Eyl) · BAGIMSIZ ISTASYONLAR (Codex moduler v1 ana montajda: A kendi sag duvari + A-C contasi · B/K/E alt sase + M12 ayak yuvalari · B icinde A/C tasiyici + GFRP isi kesici · B-K, K-E, A/C-B baglamalari) · v71:')
degis('print("ALCAK HAT SOZLESMESI (v71 ·', 'print("ALCAK HAT SOZLESMESI (v72 ·')
for a_ in ("hat_v71.glb", "hat_v71.usdz", '"hat_v71"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v71", "v72"))
degis('if __name__ == "__main__":' + NL,
      '# ---- v72 · BAĞIMSIZ İSTASYONLAR (moduler_montaj_v1 · Codex moduler_istasyon_v1 yöntemi) — mevcut parçalar yerinde değişir, yeni parçalar MODULER_YENI ----' + NL +
      'import types as _ty, moduler_montaj_v1 as MOD72' + NL +
      'for _k, _v in (("conta_epdm", dict(renk=(0.10, 0.10, 0.11, 1.0), met=0.0, ruf=0.8)), ("gfrp", dict(renk=(0.85, 0.80, 0.55, 1.0), met=0.0, ruf=0.6)), ("paslanmaz", dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.3))):' + NL +
      '    MALZEME.setdefault(_k, _v)' + NL +
      'MODULER_YENI = MOD72.uygula(_ty.SimpleNamespace(SC=SC, KS=KS, KC=KC, AK=AK, KD=KD, TC=TC, X_K=X_K, X_E=X_E, Y_MEK=Y_MEK))' + NL +
      'print("v72 · BAGIMSIZ ISTASYONLAR: %d yeni parca · %d mevcut parca uyarlandi (A cerceve −2, cepler, civata delikleri)" % (len(MODULER_YENI), len(MOD72.DEGISEN)))' + NL + NL +
      'if __name__ == "__main__":' + NL)
degis('    b1 = glb_yaz(os.path.join(OUT, "hat_v72.glb")',
      '    _ton72 = {}                                                                                  # v72 · bağımsız istasyon parçaları' + NL +
      '    for p in MODULER_YENI:' + NL +
      '        _ton72.setdefault((p["module"], {"304": "paslanmaz", "EPDM": "conta_epdm", "GFRP": "gfrp"}.get(p["material"], p["material"])), Mesh()).ekle(TC_AG(cq.Workplane(obj=p["shape"])))' + NL +
      '    for (m_, t_), g_ in sorted(_ton72.items()):' + NL +
      '        parcalar.append(("%s_MODULER__%s" % (m_, t_), g_, mal_ad({"kod": m_ + "_MODULER", "modul": m_}, t_)))' + NL +
      '    _st72 = [p for p in MOD72.PARTS if not p["new"]]' + NL +
      '    _tc72 = []' + NL +
      '    for p in TC.PARCALAR:' + NL +
      '        if p["ad"].startswith("_bom") or not v1_kalir(p["ad"]) or grup_modul(p["ad"]) != "SABIT": continue' + NL +
      '        _d = V1_TASI.get(p["ad"], (0.0, 0.0, 0.0)); sh = p["wp"].val().translate(cq.Vector(X_BC + _d[0], Y_MEK + _d[1], _d[2]))' + NL +
      '        if sh.BoundingBox().xmin < 710.0: _tc72.append(("TOPPING:" + p["ad"], sh))' + NL +
      '    _cak72 = []' + NL +
      '    for p in MODULER_YENI:' + NL +
      '        if p["kind"] == "connection": continue' + NL +
      '        for c_, sc in [("%s:%s" % (q["module"], q["name"]), q["shape"]) for q in _st72] + _tc72:' + NL +
      '            if _bbk(p["shape"], sc):' + NL +
      '                v_ = _hacim(p["shape"], sc)' + NL +
      '                if v_ > 1.0 or v_ < 0: _cak72.append((round(v_, 1), p["name"], c_))' + NL +
      '    print("v72 · BAGIMSIZ ISTASYON DENETIMI (yeni tasiyici / duvar / conta / isi kesici ↔ A, B, K, E, kaide, TOPPING sabitleri · > 1 mm3): %s" % ("TEMIZ" if not _cak72 else "%d BULGU" % len(_cak72)))' + NL +
      '    for x_ in sorted(_cak72, reverse=True)[:40]: print("   %10.1f mm3  %s  <->  %s" % x_)' + NL +
      '    b1 = glb_yaz(os.path.join(OUT, "hat_v72.glb")')
s = s.replace('"""', '"""hat_montaj_v72 (29 Eyl 2026): bağımsız istasyonlar (Codex moduler v1) v71 üstünde — yap_hat_montaj_v72.py.\n', 1)
compile(s, "hat_montaj_v72.py", "exec")
io.open(os.path.join(U, "hat_montaj_v72.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v72.py yazildi")
