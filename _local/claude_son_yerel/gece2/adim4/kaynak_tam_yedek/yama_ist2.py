import io
P = "h3_elk_rota.py"
s = io.open(P, encoding="utf-8").read()
a = '''        for a_, b_ in zip(q[:-1], q[1:]):                           # parça parça (ince kutular → az aday) · sonuç önbellekte
            k_ = (tuple(round(v, 1) for v in a_), tuple(round(v, 1) for v in b_), r)
            if k_ not in _ONB:
                seg = EO.sil(a_, b_, r).fuse(cq.Solid.makeSphere(r, V(*b_), angleDegrees1=-90, angleDegrees2=90))'''
b = '''        for j_, (a_, b_) in enumerate(zip(q[:-1], q[1:])):          # parça parça (ince kutular → az aday) · sonuç önbellekte
            son_ = j_ == len(q) - 2                                 # son parçanın ucu düz (kanal / pano yüzüne dayanır)
            k_ = (tuple(round(v, 1) for v in a_), tuple(round(v, 1) for v in b_), r, son_)
            if k_ not in _ONB:
                seg = EO.sil(a_, b_, r)
                if not son_: seg = seg.fuse(cq.Solid.makeSphere(r, V(*b_), angleDegrees1=-90, angleDegrees2=90))'''
assert s.count(a) == 1; s = s.replace(a, b)
io.open(P, "w", encoding="utf-8").write(s)

P = "h3_elk_ist_v1.py"
s = io.open(P, encoding="utf-8").read()
i0 = s.index("    # çekmece reed sensörleri")
i1 = s.index("    return RAPOR", i0)
yeni = '''    # çekmece reed sensörleri (açık + kapalı): lama yanından (lamaya kablo bağıyla) arkaya · motor üstünden kolon kablo kanalının yan yüzüne (parmak yuvası)
    D = {ad: sb for ad, s_, sb in EO.dokum()}
    kanallar = {k.split("|")[1].replace("kablo_kanali_", ""): v for k, v in D.items() if k.startswith("B_KABLO|kablo_kanali_K")}
    n = 0
    for k, sb in sorted(D.items()):
        if not (k.startswith("CEK_") and k.endswith("_reed_acik")): continue
        grp = k.split("|")[0]; kol = grp.split("_")[1]
        kn = kanallar.get(kol); rk = D.get(k.replace("_reed_acik", "_reed_kapali"))
        if kn is None or rk is None: RAPOR["bulunamadi"].append(("DOLAP_reed_" + grp, sb[:2], sb[2:4], "kanal/kapalı sensör yok")); continue
        rxc, ryc = (sb[0] + sb[1]) / 2.0, (sb[2] + sb[3]) / 2.0
        cx, cy = sb[0] - 2.3, sb[3] + 2.0                        # lama yan yüzüne dayalı (0,3 mm) · reed üst hizası
        yc = min(ryc, kn[3] - 12.0)                               # kanal üst ucunu aşmasın
        a_ = [(rxc, ryc, sb[4]), (rxc, ryc, sb[4] - 4.0), (cx, ryc, sb[4] - 4.0), (cx, cy, sb[4] - 4.0), (cx, cy, -777.0), (cx, yc, -777.0), (kn[0] - 0.2, yc, -777.0)]
        k_ = [(rxc, ryc, rk[4]), (rxc, ryc, -771.0), (rxc, yc, -771.0), (kn[0] - 0.2, yc, -771.0)]
        for nm, pts in (("acik", a_), ("kapali", k_)):
            q = [pts[0]]
            for p in pts[1:]:
                if math.dist(p, q[-1]) > 1e-6: q.append(p)
            sh = boru(q, 2.0)
            ok, engel = ER.temiz(sh)
            if not ok:
                RAPOR["bulunamadi"].append(("DOLAP_reed_%s_%s" % (grp, nm), q[0], q[-1], engel)); continue
            ad = "DOLAP_reed_%s_%s" % (grp, nm)
            ekle("kablo_%s" % ad, sh, "kablo", "ELK_DOLAP",
                 ("Reed sensör kablosu 2 × 0,25 PUR (lamaya kablo bağıyla · kolon kanalına)", 42, "", "motor M12 soketi zaten kanala dayalı") if n == 0 else None)
            ER.ekli_ekle("kablo_" + ad, sh); n += 1
            RAPOR["yol"].append((ad, round(EO.uzunluk(q)), len(q) - 1, 0))
    # soğutma grubu (Secop NLE8.8CN): kompresör üstünden kondenserin üstünü aşıp pano altı kanalının alt yüzüne
    cihaz("DOLAP_secop_NLE88", (4213.0, 308.5, -244.0), (4213.0, 410.8, -809.0), 4.0, "B",
          via=[(4213.0, 435.0, -244.0), (4213.0, 435.0, -600.0), (4213.0, 410.8, -600.0)])
    # 4 evaporatör fanı → en yakın kolon kanalının yan yüzü (evaporatörün üstünden arkaya)
    for nm, S, T in (("fan_sol_1", (1783.5, 509.5, -628.5), (1683.5 + 2.7, 668.0, -777.0)), ("fan_sol_2", (1963.5, 509.5, -628.5), (2298.5 - 2.7, 668.0, -777.0)),
                     ("fan_sag_1", (3093.5, 422.0, -628.5), (2993.5 + 2.7, 520.0, -777.0)), ("fan_sag_2", (3273.5, 422.0, -628.5), (3608.5 - 2.7, 520.0, -777.0))):
        cihaz("DOLAP_evap_%s" % nm, S, T, 2.5, "B", itme=[(1, 6.0)])
'''
s = s[:i0] + yeni + s[i1:]
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
