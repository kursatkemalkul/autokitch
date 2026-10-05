# -*- coding: utf-8 -*-
"""hat_montaj_v52 → hat_montaj_v53 (27 Eyl 2026): BULAŞIK MAKİNESİ GERÇEK MODEL (bulasik_cad_v1 · MEIKO M-iClean US föy ölçüleri).
Kemal: "bulaşık makinesi nerede modellediğin · neden detaylı modellemedin · yap". D_BULASIK kutusu kalkar, yerine 16 parça (gövde, kapak,
ekran, ışıklı kulp, filtre, 2 yıkama kolu, sepet, 4 ayak, 3 bağlantı). Denetim: bulaşık ↔ F dolabı birimleri + fırın (gerçek katı) ·
kapak açık zarfı ↔ robot/ray."""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "hat_montaj_v52.py"), encoding="utf-8").read()


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


NL = chr(10)
degis('"""v52 (27 Eyl 2026):', '"""v53 (27 Eyl 2026): BULAŞIK MAKİNESİ GERÇEK MODEL (bulasik_cad_v1 · MEIKO M-iClean US föyü) — D_BULASIK kutusu yerine 16 parça; kapak açık zarfı ↔ robot denetimi' + NL + 'v52 (27 Eyl 2026):')
degis('import itici_cad_v3 as IT                                                              # v49: aktarma iticisi + destek plakası (dünya koordinatı)',
      'import itici_cad_v3 as IT                                                              # v49: aktarma iticisi + destek plakası (dünya koordinatı)' + NL +
      'import bulasik_cad_v1 as BM                                                            # v53: MEIKO M-iClean US gerçek modeli (föy ölçüleri)' + NL +
      'for _k, _v in BM.MALZEME.items():' + NL + '    MALZEME.setdefault(_k, dict(renk=_v["renk"], met=_v["met"], ruf=_v["ruf"], saydam=False))')
i = s.index('        ("D_BULASIK", "Bulaşık makinesi · MEIKO M-iClean US'); j = s.index(NL, i) + 1
s = s[:i] + s[j:]
degis('# ---- v49 · AKTARMA İTİCİSİ + DESTEK PLAKASI (modül C, dünya koordinatı; ev konumu, çubuk kalkık) ----',
      '# ---- v53 · BULAŞIK MAKİNESİ (gerçek model, dünya koordinatı) ----' + NL +
      'BM.kur()' + NL +
      'for _k, _a in BM.BIRIMLER:' + NL +
      '    _bb = [BM.dunya(_p).BoundingBox() for _p in BM.PARCALAR if _p["birim"] == _k]' + NL +
      '    birim(_k, _a, "D", "GERCEK_BULASIK", (min(q.xmin for q in _bb), max(q.xmax for q in _bb)), (min(q.ymin for q in _bb), max(q.ymax for q in _bb)),' + NL +
      '          (min(q.zmin for q in _bb), max(q.zmax for q in _bb)), "sac", "bulasik_cad_v1.py", "hat/oven.html")' + NL +
      '# ---- v49 · AKTARMA İTİCİSİ + DESTEK PLAKASI (modül C, dünya koordinatı; ev konumu, çubuk kalkık) ----')
degis('        elif b["durum"] == "GERCEK":\n            V, ps = kaset_parcalari(b["kaynak"][:-3]); AG = AG or V',
      '''        elif b["durum"] == "GERCEK_BULASIK":                                                 # v53
            ps = [p for p in BM.PARCALAR if p["birim"] == b["kod"]]
            ton = {}
            for p in ps:
                ton.setdefault((p["mal"], p["grup"]), Mesh()).ekle(TC_AG(cq.Workplane(obj=BM.dunya(p))))
            for (t_, g_), m_ in sorted(ton.items()):
                parcalar.append((dugum_ad(b["kod"], t_, g_), m_, mal_ad(b, t_)))
            b["parca"] = len(ps)
        elif b["durum"] == "GERCEK":
            V, ps = kaset_parcalari(b["kaynak"][:-3]); AG = AG or V''')
degis('''            _DG.append(("D:" + b["kod"], kutu_kat(b).val()))
    _cak = []''', '''            _DG.append(("D:" + b["kod"], kutu_kat(b).val()))
    for p in BM.PARCALAR:                                                                # v53: bulaşık makinesi gerçek parçaları
        _DG.append(("BULASIK:" + p["ad"], BM.dunya(p)))
    _cak = []''')
degis('''    assert not _cik_cak, "cikinti bandina komsu parca giriyor"''', '''    assert not _cik_cak, "cikinti bandina komsu parca giriyor"
    # ---- v53 · BULAŞIK MAKİNESİ: gerçek parçalar ↔ F dolabındaki birimler (kutu) · dolap zarfı · kapak açık zarfı ↔ robot/ray ----
    _BMP = [(p["ad"], BM.dunya(p)) for p in BM.PARCALAR]
    _bm_cak = []
    for b in B:
        if b["modul"] == "D" and b["durum"] in ("KUTU", "KATALOG") and not b["kod"].startswith(("D_SUPURGELIK", "D_TABAN_KABIN", "D_DAVLUMBAZ")):
            kb = kutu_kat(b).val()
            for a_, sa in _BMP:
                if _bbk(sa, kb):
                    v_ = _hacim(sa, kb)
                    if v_ > 1.0 or v_ < 0: _bm_cak.append((round(v_, 1), a_, b["kod"]))
    _bmb = cq.Compound.makeCompound([sa for _a, sa in _BMP]).BoundingBox()
    _dol = next(b for b in B if b["kod"] == "D_TABAN_KABIN")
    _ic = (_dol["x"][0] <= _bmb.xmin and _bmb.xmax <= _dol["x"][1] and _dol["y"][0] <= _bmb.ymin and _bmb.ymax <= _dol["y"][1] and -DZ - 0.5 <= _bmb.zmin and _bmb.zmax <= 0.5)
    print("BULASIK MAKINESI (bulasik_cad_v1 · %d parca) ↔ F dolabi birimleri (gercek kati): %s · dolap zarfinda (x %.0f-%.0f · y %.0f-%.0f · z %.0f…%.0f): %s"
          % (len(_BMP), "TEMIZ" if not _bm_cak else "%d BULGU %s" % (len(_bm_cak), _bm_cak[:6]), _bmb.xmin, _bmb.xmax, _bmb.ymin, _bmb.ymax, _bmb.zmin, _bmb.zmax, "EVET" if _ic else "HAYIR"))
    assert not _bm_cak and _ic, "bulasik makinesi dolap birimlerine giriyor / dolaptan tasiyor"
    _kx, _ky, _kz = BM.kapi_acik_zarf()
    for b in B:
        if b["kod"] in ("ROBOT_RAY", "ROBOT_1", "ROBOT_1_KOL"):
            _yz = b["y"][0] < _ky[1] and _ky[0] < b["y"][1] and b["z"][0] < _kz[1] and _kz[0] < b["z"][1]
            _gx = b["x"][1] - b["x"][0]
            print("KAPAK ACIK ZARFI (x %.0f-%.0f · y %.0f-%.0f · z %.0f…%.0f) ↔ %s (y %.0f-%.0f · z %.0f…%.0f): %s"
                  % (_kx[0], _kx[1], _ky[0], _ky[1], _kz[0], _kz[1], b["kod"], b["y"][0], b["y"][1], b["z"][0], b["z"][1],
                     ("KESISIR (y/z) → robot bu birimiyle x %.0f-%.0f arasindayken kapak ACILMAZ: servis modu kilidi" % (_kx[0] - _gx, _kx[1] + _gx)) if _yz else "SERBEST (robot her konumda)"))''')
degis('pafta="HAT v52 (27 Eyl) ·', 'pafta="HAT v53 (27 Eyl) · BULASIK MAKINESI GERCEK MODEL (bulasik_cad_v1 · MEIKO M-iClean US foy olculeri, 16 parca) · v52:')
degis('print("ANA MONTAJ ANIMASYONU (v52):', 'print("ANA MONTAJ ANIMASYONU (v53):')
s = s.replace('hat_v52.glb', 'hat_v53.glb').replace('hat_v52.usdz', 'hat_v53.usdz').replace('"hat_v52"', '"hat_v53"')
io.open(os.path.join(U, "hat_montaj_v53.py"), "w", encoding="utf-8").write(s)
print("hat_montaj_v53.py yazildi")
