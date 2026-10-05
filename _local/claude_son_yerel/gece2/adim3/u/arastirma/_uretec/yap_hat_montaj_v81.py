# -*- coding: utf-8 -*-
"""hat_montaj_v80 → hat_montaj_v81 (29 Eyl 2026 · YEREL) — Kemal'in TOPPING soruları:
· "ayak neden sıfırında bitmiyor" + A|C köşesi → kaide_cad_v3 (A 1,5–700 · C 700–2500 · C arka −830: istasyon yüzleriyle aynı hiza, A|C arasında boşluk yok)
· A|C köşesi "iki istasyonun birleşimi gibi düşün, bağlantıları tabla ve rayıyla" → moduler_montaj_v3 (A–C çevre contası kalktı)
· "toppingde de delikler var neden" → topping_cad_v28 (HIWIN ray havşalarına DIN 912 M4 × 16)
· "sucuk dolarken tabla yanaşıyor, yer var mı" → kaset dönüş süpürmesi artık komşu istasyonlara (A açıcı kabini + fırın gövdesi / yükleme bandı / fırın üstü kabin)
  karşı da denetlenir ve en yakın pay yazılır. Çıktılar hat_v81."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v80.py"), encoding="utf-8").read()
NL = chr(10)
def degis(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:100]); s = s.replace(a, b)
degis('pafta="HAT v80 (29 Eyl · YEREL) ·', 'pafta="HAT v81 (29 Eyl · YEREL) · KAIDELER ISTASYON YUZLERIYLE AYNI HIZA (A 1,5-700 · C 700-2500) · A-C CONTASI KALKTI · RAY CIVATALARI (DIN 912 M4) · DONUS SUPURMESI KOMSU ISTASYONLARLA DENETLENIR · v80:')
degis('print("ALCAK HAT SOZLESMESI (v80 ·', 'print("ALCAK HAT SOZLESMESI (v81 ·')
for a_ in ("hat_v80.glb", "hat_v80.usdz", '"hat_v80"'):
    assert a_ in s, a_
    s = s.replace(a_, a_.replace("v80", "v81"))
degis('import qr_cad_v1 as QR, tezgah_cad_v1 as TZ, ray_ek_cad_v1 as RE, kaide_cad_v2 as KD',
      'import qr_cad_v1 as QR, tezgah_cad_v1 as TZ, ray_ek_cad_v1 as RE, kaide_cad_v3 as KD      # v81: kaideler istasyon yüzleriyle aynı hiza')
degis('import topping_hesap_v7 as TH, topping_cad_v27 as TC ', 'import topping_hesap_v7 as TH, topping_cad_v28 as TC ')   # v81: ray cıvataları
degis('_dis_birim(KD, "GERCEK_KAIDE", "kaide_cad_v2.py",', '_dis_birim(KD, "GERCEK_KAIDE", "kaide_cad_v3.py",')
degis('print("KAIDE (kaide_cad_v2 ·', 'print("KAIDE (kaide_cad_v3 ·')
degis('import types as _ty, moduler_montaj_v2 as MOD72                   # v79: v2 = bağlantı parçaları yok (Kemal)',
      'import types as _ty, moduler_montaj_v3 as MOD72                   # v81: v3 = A–C çevre contası da yok (v79: v2 bağlantı parçaları yok)')
# ---- dönüş süpürmesi ↔ komşu istasyonlar ----
degis('''    for _ad_, x0_, x1_ in _IST:
        sw_ = _supur(x0_, x1_)
        for c_, sc in _ENG:
            if _bbk(sw_, sc):
                v_ = _hacim(sw_, sc)
                if v_ > 1.0 or v_ < 0: _cak_it.append((round(v_, 1), "DONUS(%s)" % _ad_, c_))''',
      '''    # v81 · komşu istasyonlar da engel (Kemal: "sucuk dolarken tabla fırına yanaşıyor — yer var mı"): A açıcı kabini + A duvarı · fırın gövdesi + yükleme bandı + fırın üstü kabin
    _tk = lambda wp: ((wp.vals()[0] if len(wp.vals()) == 1 else cq.Compound.makeCompound([o for o in wp.vals() if isinstance(o, cq.Shape)])) if hasattr(wp, "vals") else wp)
    _KOM = [("FIRIN:" + p["birim"] + ":" + p["ad"], FT.dunya(p)) for p in FT.PARCALAR]
    _KOM += [("F_UST:" + p["ad"], FU.dunya(p)) for p in FU.PARCALAR]
    _KOM = [(c_, sc) for c_, sc in _KOM if sc.BoundingBox().xmin < 2620.0]
    _KOM += [(c_, sc) for c_, sc in [("A:" + p["ad"], _tk(p["wp"])) for p in AK.PARCALAR] if sc.BoundingBox().xmax > 580.0]
    _KOM += [("A_MODULER:" + p["name"], p["shape"]) for p in MODULER_YENI if p["module"] == "A" and p["shape"].BoundingBox().xmax > 580.0]
    _PAY = {}
    for _ad_, x0_, x1_ in _IST:
        sw_ = _supur(x0_, x1_)
        for c_, sc in _ENG + _KOM:
            if _bbk(sw_, sc):
                v_ = _hacim(sw_, sc)
                if v_ > 1.0 or v_ < 0: _cak_it.append((round(v_, 1), "DONUS(%s)" % _ad_, c_))
        if _ad_ in ("sos", "sucuk"):                                                              # en uç istasyonlar: komşuya en yakın pay (katılardan)
            _b = sw_.BoundingBox()
            _y = [(c_, sc) for c_, sc in _KOM if sc.BoundingBox().xmin < _b.xmax + 40.0 and sc.BoundingBox().xmax > _b.xmin - 40.0
                  and sc.BoundingBox().ymin < _b.ymax + 40.0 and sc.BoundingBox().ymax > _b.ymin - 40.0 and sc.BoundingBox().zmin < _b.zmax + 40.0 and sc.BoundingBox().zmax > _b.zmin - 40.0]
            _d = sorted((sw_.distance(sc), c_) for c_, sc in _y) if _y else [(99.0, "-")]
            _PAY[_ad_] = (_d[0][0], _d[0][1], _b.xmin, _b.xmax)
    print("   v81 · DONUS SUPURMESI ↔ KOMSU ISTASYONLAR (%d parca: A acici kabini + A duvari · firin govdesi + yukleme bandi + firin ustu kabin): %s · sos supurmesi en sol x %.1f (istasyon siniri 700) → en yakin %s %.1f mm · sucuk supurmesi en sag x %.1f (istasyon siniri 2500) → en yakin %s %.1f mm"
          % (len(_KOM), "TEMIZ" if not [x_ for x_ in _cak_it if x_[2].startswith(("FIRIN:", "F_UST:", "A:", "A_MODULER:"))] else "BULGU",
             _PAY["sos"][2], _PAY["sos"][1], _PAY["sos"][0], _PAY["sucuk"][3], _PAY["sucuk"][1], _PAY["sucuk"][0]))''')
s = s.replace('"""', '"""hat_montaj_v81 (29 Eyl 2026 · YEREL): kaide v3 (aynı hiza) · A–C contası yok · ray cıvataları · dönüş süpürmesi komşu istasyonlarla — yap_hat_montaj_v81.py.\n', 1)
compile(s, "hat_montaj_v81.py", "exec")
io.open(os.path.join(U, "hat_montaj_v81.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v81.py yazildi")
