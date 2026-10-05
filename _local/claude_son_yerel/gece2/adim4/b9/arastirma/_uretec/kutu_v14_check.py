# -*- coding: utf-8 -*-
"""E v14 denetimi (30 Eyl 2026 · Claude) — Kemal: "bu neden kesik yarım ve oradaki yatay parça havada"
1 · v13 ↔ v14 PARÇA PARÇA: çıkan tam olarak ağız üst kirişi + dikey kanalın iki parçası, eklenen yalnız tek parça dikey kanal;
    kalan her parça ad · grup · malzeme · BOM · hacim · zarf AYNI (0,01)
2 · kinematik v13 ile BİREBİR: bütün hareket grupları 0…DONGU 0,05 s adımla aynı matris · blank_dunya aynı · gerçek saat sabitleri aynı
3 · yeni kanal: zarf x 806–826 · y 126–1827 · z −50…−25 · durağan çakışma 0 (aynı grup dahil)
4 · v13 denetimleri aynen: katılar geçerli · zaman ihlali 0 · kafa↔besleme ≥ 3 mm · tam tarama (bütün hareketliler ↔ bütün parçalar) kesişim 0 · makine↔karton 0
5 · 'baglanti': 0,25 mm temas grafiği · tek bileşen (+ asansör kayışı, v13 gibi) · GÖRSEL HAVADA: bütün komşuları ön yüz (onyuz_* — montajda saydam
    ön kapak malzemesi) olan opak parça 0 (Kemal'in gördüğü hata sınıfı) · bilgi: bütün komşuları saydam dış kabuk (kabuk) olanlar
Çıktı: _local/e-v14/denetim.json (+ baglanti.json) · 'hizli' argümanı tam taramayı atlar."""
import json, sys, time, hashlib
from pathlib import Path
import kutu_cad_v13 as K13
import kutu_cad_v14 as K

t0 = time.time()
K13.modul()
K.modul()
P = {p["ad"]: p for p in K.PARCALAR}
S = {n: p["wp"].val() for n, p in P.items()}
P13 = {p["ad"]: p for p in K13.PARCALAR}
OUT = Path(__file__).resolve().parents[2] / "_local" / "e-v14"; OUT.mkdir(parents=True, exist_ok=True)
R = dict(kaynak_sha256=hashlib.sha256(Path(K.__file__).read_bytes()).hexdigest(), parca=len(P), parca_v13=len(P13),
         gecersiz=[n for n, s in S.items() if not s.isValid()],
         dongu_eski=K.DONGU, dongu_gercek=round(K.DONGU_GERCEK, 2), zaman_ihlal=K.zaman_denetimi_v12(), yakin=[], kesisim=[], tam=False)
print("E v14 · %d parça (v13 %d) · geçersiz %d · döngü eski %.1f s → gerçek %.2f s" % (len(P), len(P13), len(R["gecersiz"]), K.DONGU, K.DONGU_GERCEK), flush=True)
print("   ZAMAN İHLALİ (gerçek saatte sınırı aşan eksen): %s" % (R["zaman_ihlal"] or "YOK"), flush=True)

# 1 · v13 ↔ v14 parça parça
cikan, eklenen = sorted(set(P13) - set(P)), sorted(set(P) - set(P13))
fark = []
for n in sorted(set(P) & set(P13)):
    a, b = P13[n], P[n]
    sa, sb = a["wp"].val(), b["wp"].val()
    ba, bb = sa.BoundingBox(), sb.BoundingBox()
    zarf = max(abs(u - v) for u, v in zip((ba.xmin, ba.xmax, ba.ymin, ba.ymax, ba.zmin, ba.zmax), (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)))
    dv = abs(sa.Volume() - sb.Volume())
    if a["grup"] != b["grup"] or a["mal"] != b["mal"] or a.get("bom") != b.get("bom") or zarf > 0.01 or dv > 0.01:
        fark.append([n, a["grup"], b["grup"], a["mal"], b["mal"], round(zarf, 3), round(dv, 3)])
R["v13_v14"] = dict(cikan=cikan, eklenen=eklenen, degisen=fark)
ok1 = cikan == sorted(K.V14_CIKAN) and eklenen == ["kablo_kanali_dikey"] and not fark and K.V14_YENI == ["kablo_kanali_dikey"]
print("   1 · v13 ↔ v14: çıkan %s · eklenen %s · değişen %d → %s" % (cikan, eklenen, len(fark), "AYNI (beklenen)" if ok1 else "FARK VAR"), flush=True)
for f in fark[:10]:
    print("      DEĞİŞEN %s" % f, flush=True)

# 2 · kinematik
gruplar = sorted(set(p["grup"] for p in K.PARCALAR if not p["grup"].startswith("B_")))
kin = []
n_an = int(round(K.DONGU / 0.05))
for i in range(n_an + 1):
    t = round(i * 0.05, 3)
    for g in gruplar:
        A, B = K13.grup_matrisi(g, t), K.grup_matrisi(g, t)
        if max(abs(A[r][c] - B[r][c]) for r in range(len(A)) for c in range(len(A[r]))) > 1e-9:
            kin.append([t, g])
    W13, W14 = K13.blank_dunya(t), K.blank_dunya(t)
    if set(W13) != set(W14) or any(max(abs(W13[k][r][c] - W14[k][r][c]) for r in range(len(W13[k])) for c in range(len(W13[k][r]))) > 1e-9 for k in W13):
        kin.append([t, "blank_dunya"])
sabit = {k: (getattr(K13, k), getattr(K, k)) for k in ("DONGU", "DONGU_GERCEK", "E_HAZIR_GERCEK", "Z_CATAL_GERCEK", "Z_CATAL")}
sabit_fark = {k: v for k, v in sabit.items() if v[0] != v[1]}
R["kinematik"] = dict(an=n_an + 1, grup=len(gruplar), fark=kin[:50], sabit_fark={k: [str(v[0]), str(v[1])] for k, v in sabit_fark.items()})
ok2 = not kin and not sabit_fark
print("   2 · kinematik: %d an × %d grup + blank_dunya · fark %d · saat sabitleri fark %s → %s" % (n_an + 1, len(gruplar), len(kin), list(sabit_fark) or "YOK",
                                                                                                 "BİREBİR" if ok2 else "FARK VAR"), flush=True)

GRUPSUZ = ("PIZZA", "CATAL", "K_ITICI", "SABIT_REF")
# 3 · yeni kanal: zarf + durağan çakışma (t 0 · aynı grup dahil)
kb = S["kablo_kanali_dikey"].BoundingBox()
kz = tuple(round(v, 2) for v in (kb.xmin, kb.xmax, kb.ymin, kb.ymax, kb.zmin, kb.zmax))
R["kanal_zarf"] = kz
_W0 = {}
for _n in S:
    if P[_n]["grup"] in GRUPSUZ: continue
    _M = K.blank_dunya(0.0)[P[_n]["grup"]] if P[_n]["grup"].startswith("B_") else K.grup_matrisi(P[_n]["grup"], 0.0)
    _sh = K.uygula(S[_n], _M); _W0[_n] = (_sh, _sh.BoundingBox())
R["v14_durgan"] = []
for _a in K.V14_YENI:
    _sa, _ba = _W0[_a]
    for _b, (_sb, _bb) in _W0.items():
        if _b == _a or not K._bb_kesisir(_ba, _bb) or K._istisna(_a, _b): continue
        _v = _sa.intersect(_sb).Volume()
        if _v > 0.5:
            R["v14_durgan"].append([_a, _b, round(_v, 2)]); print("      v14 DURAĞAN ÇAKIŞMA %s ↔ %s %.1f mm³" % (_a, _b, _v), flush=True)
ok3 = kz == (806.0, 826.0, 126.0, 1827.0, -50.0, -25.0) and not R["v14_durgan"]
print("   3 · tek parça kanal zarfı %s (boy %.0f) · durağan çakışma %d" % (kz, kb.ymax - kb.ymin, len(R["v14_durgan"])), flush=True)


def dunya(t):
    W = K.blank_dunya(t)
    M = {n: (W[P[n]["grup"]] if P[n]["grup"].startswith("B_") else K.grup_matrisi(P[n]["grup"], t)) for n in S if P[n]["grup"] not in GRUPSUZ}
    return M


cache = {}


def sekil(n, M):
    key = (n, tuple(round(v, 6) for row in M[:3] for v in row))
    if key not in cache:
        sh = K.uygula(S[n], M); cache[key] = (sh, sh.BoundingBox())
    return cache[key]


# 4 · v13 denetimleri aynen
KAFA_G = ("PISTON", "CNR_LIFT", "FRONT_Y", "PARMAK") + tuple(K.CORNER)
BES_G = ("ITICI", "VAC_Y")
kafa_p = [n for n in S if P[n]["grup"] in KAFA_G]
bes_p = [n for n in S if P[n]["grup"] in BES_G]
en_kisa = (1e9, None)
t = 1.85
while t <= 2.80 + 1e-9:
    M = dunya(t)
    for a in kafa_p:
        sa, ba = sekil(a, M[a])
        for b in bes_p:
            sb, bb = sekil(b, M[b])
            if ba.xmin > bb.xmax + 20 or bb.xmin > ba.xmax + 20 or ba.ymin > bb.ymax + 20 or bb.ymin > ba.ymax + 20 or ba.zmin > bb.zmax + 20 or bb.zmin > ba.zmax + 20:
                continue
            d = sa.distance(sb)
            if d < en_kisa[0]: en_kisa = (d, (round(t, 3), a, b))
            if d < 0.01 and sa.intersect(sb).Volume() > 0.5:
                R["kesisim"].append([round(t, 3), a, b])
    t += 0.005
R["yakin"] = dict(en_kisa_mm=round(en_kisa[0], 2), an=en_kisa[1])
print("   4 · KAFA İNİŞİ ↔ BESLEME (eski 1,85–2,80 · 5 ms): en kısa %.2f mm %s · kesişim %d" % (en_kisa[0], en_kisa[1], len(R["kesisim"])), flush=True)

if "hizli" not in sys.argv:
    anlar = sorted(set([round(i * 0.25, 3) for i in range(int(K.DONGU * 4) + 1)] + [0.35, 0.65, 1.35, 1.65, 1.9, 2.2, 2.7, 2.858, 3.0, 3.7, 4.5, 5.3, 5.858,
                                                                                     6.3, 6.55, 6.85, 7.1, 8.0, 8.2, 8.7, 9.05, 9.5, 9.8, 10.15, 10.55, 10.8, 11.1,
                                                                                     13.6, 13.9, 14.2, 15.6, 15.9, 16.7, 18.1, 18.6, 20.3, 21.7, 22.8, 22.98]))
    hareketli = [n for n in S if P[n]["grup"] not in GRUPSUZ and P[n]["grup"] != "SABIT"]
    R["karton"] = []; R["karton_ic"] = []; ILK = set()
    for t in anlar:
        M = dunya(t)
        W = {n: sekil(n, M[n]) for n in M}
        gor = set()
        for a in hareketli:
            sa, ba = W[a]
            for b, (sb, bb) in W.items():
                if a == b or (b, a) in gor: continue
                gor.add((a, b))
                if not K._bb_kesisir(ba, bb): continue
                if P[a]["grup"] == P[b]["grup"] and not P[a]["grup"].startswith("B_"): continue
                if K._istisna(a, b): continue
                v = sa.intersect(sb).Volume()
                if v > 0.5:
                    ka = P[a]["grup"].startswith("B_") or P[a]["mal"] == "karton_yigin"
                    kb_ = P[b]["grup"].startswith("B_") or P[b]["mal"] == "karton_yigin"
                    liste = R["karton_ic"] if (ka and kb_) else R["karton"] if (ka or kb_) else R["kesisim"]
                    liste.append([t, a, b, round(v, 2)])
                    if (a, b) not in ILK:
                        ILK.add((a, b)); print("      %s %s ↔ %s %.1f mm³ (t %.2f)" % ("KARTON-İÇ" if (ka and kb_) else "KARTON" if (ka or kb_) else "KESİŞİM", a, b, v, t), flush=True)
    print("   4 · tam tarama %d an · kesişim %d · makine↔karton %d · karton içi %d (kat yeri kalınlık bindirmesi, v13 ile aynı sayılır) · %.0f s"
          % (len(anlar), len(R["kesisim"]), len(R["karton"]), len(R["karton_ic"]), time.time() - t0), flush=True)
    R["tam"] = True

ok4 = not R["gecersiz"] and not R["zaman_ihlal"] and not R["kesisim"] and not R.get("karton") and R["yakin"]["en_kisa_mm"] >= 3.0
ok5 = True
if "baglanti" in sys.argv:
    # v11 yöntemi: 0,25 mm (kayar geçmeler) içinde temas eden parçalar aynı bileşen
    names = [n for n in P if not P[n]["grup"].startswith("B_") and P[n]["grup"] not in GRUPSUZ and P[n]["mal"] != "karton_yigin" and not n.startswith("icecek_")]
    solids = {n: K.uygula(S[n], K.grup_matrisi(P[n]["grup"], 0)) for n in names}
    boxes = {n: s.BoundingBox() for n, s in solids.items()}
    graph = {n: set() for n in names}
    for i, n in enumerate(names):
        for m in names[i + 1:]:
            a, b = boxes[n], boxes[m]
            if any(getattr(a, k + "min") > getattr(b, k + "max") + .25 or getattr(b, k + "min") > getattr(a, k + "max") + .25 for k in "xyz"): continue
            if solids[n].distance(solids[m]) <= .25: graph[n].add(m); graph[m].add(n)
    todo = set(names); comps = []
    while todo:
        found = set(); stack = [next(iter(todo))]
        while stack:
            n = stack.pop()
            if n in found: continue
            found.add(n); stack.extend(graph[n] - found)
        todo -= found; comps.append(sorted(found))
    comps.sort(key=len, reverse=True)
    (OUT / "baglanti.json").write_text(json.dumps(comps, ensure_ascii=False, indent=1), encoding="utf-8")
    on_ = lambda n: n.startswith("onyuz_")
    saydam_ = lambda n: on_(n) or P[n]["mal"] in ("kabuk", "referans")
    gorsel = sorted(n for n in names if not saydam_(n) and graph[n] and all(on_(m) for m in graph[n]))
    kabuk_bilgi = sorted(n for n in names if not saydam_(n) and graph[n] and all(saydam_(m) for m in graph[n]) and n not in gorsel)
    R["baglanti"] = dict(bilesen=[len(c) for c in comps], tek=[c for c in comps[1:] if len(c) <= 3],
                         gorsel_havada_onyuz=gorsel, bilgi_yalniz_saydam_kabuga_degen=kabuk_bilgi,
                         kanal_komsu=sorted(graph.get("kablo_kanali_dikey", ())))
    ok5 = len(comps) <= 2 and all(c == ["asansor_kayisi"] for c in comps[1:]) and not gorsel
    print("   5 · BAĞLANTI: bileşen boyları %s · tek kalanlar %s" % ([len(c) for c in comps][:6], [c for c in comps[1:] if len(c) <= 3][:6]), flush=True)
    print("   5 · GÖRSEL HAVADA (yalnız saydam ön yüze değen opak parça): %d %s" % (len(gorsel), gorsel), flush=True)
    print("   5 · bilgi · yalnız saydam dış kabuğa (kabuk) değen opak parça: %d %s" % (len(kabuk_bilgi), kabuk_bilgi[:20]), flush=True)
    print("   5 · kanal komşuları: %s" % R["baglanti"]["kanal_komsu"], flush=True)
R["gecti"] = dict(v13_v14=ok1, kinematik=ok2, kanal=ok3, v13_denetim=ok4, baglanti=ok5)
(OUT / "denetim.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
ok = ok1 and ok2 and ok3 and ok4 and ok5
print("E v14 DENETİM: %s · v13↔v14 %s · kinematik %s · kanal %s · v13 denetimleri %s (kesişim %d · karton %d · kafa↔besleme %.2f mm) · bağlantı %s · %.0f s"
      % ("GEÇTİ" if ok else "KALDI", ok1, ok2, ok3, ok4, len(R["kesisim"]), len(R.get("karton", [])), R["yakin"]["en_kisa_mm"], ok5, time.time() - t0), flush=True)
