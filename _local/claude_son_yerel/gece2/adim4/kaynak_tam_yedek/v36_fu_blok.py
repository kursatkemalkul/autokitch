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
