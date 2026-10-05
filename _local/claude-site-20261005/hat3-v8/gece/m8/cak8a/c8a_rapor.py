# -*- coding: utf-8 -*-
"""birlesik.json + occ_*.json + meta.json -> cakisma.json + cakisma.md"""
import json, glob, re
from collections import defaultdict, Counter
M = json.load(open("meta.json", encoding="utf-8")); BIL = M["bil"]
MEKIST = {m["kod"]: m["istasyon"] for m in M["mek"]}
D = json.load(open("birlesik.json"))
OCC = {}
for f in glob.glob("occ_*.json"): OCC.update({int(k): v for k, v in json.load(open(f)).items()})
YZ = {}
for f in glob.glob("yuzey_*.json"): YZ.update({int(k): v for k, v in json.load(open(f)).items()})

ON = [("TOPPING", "TOPPING"), ("ELK_TOPPING", "TOPPING"), ("A_", "A"), ("KAIDE_A", "A"), ("U_A_", "A"), ("B_", "B"), ("CEK_", "B"),
      ("DUZ_B", "B"), ("E_", "E"), ("DUZ_E", "E"), ("F_", "F"), ("U_F_", "F"), ("HAVA_KOMP", "F"), ("D_PIZZA", "F"), ("K_", "K"), ("ELK_K", "K"),
      ("U_KE", "K/E"), ("QR_", "QR"), ("ELK_QR", "QR"), ("TEZGAH", "TEZGAH"), ("DUZ_TEZGAH", "TEZGAH"), ("ELK_", "ELEKTRIK"), ("URUN", "URUN"), ("U_", "UST DOLAP")]


def istasyon(b):
    if b["mek"] and MEKIST.get(b["mek"]) and MEKIST[b["mek"]] not in ("Elektrik", "Çevre"): return MEKIST[b["mek"]]
    for o, s in ON:
        if b["dugum"].startswith(o): return s
    return "?"


def ad(b): return b["ad"] or "%s#%d" % (b["dugum"].split("__")[-1], b["no"])
def tam(b): return "%s · %s" % (b["dugum"], ad(b))


MEKAN = r"silindir|piston|mil_|_mil|mil$|kavrama|bogaz|mafsal|vida|somun|rulman|yata[kg]|burc|kasnak|kayis|disli|helezon|karistirici|kizak|araba|ray_|valf|aktuator|kam_|pim|yay_|dil|kilit|mentese|zincir|bilya|rotor|stator|motor|redukt|fren|kaplin|rakor|kovan|nozul|spreader|dagitici|braket"
SIKI = r"conta|rakor|kelepce|burc|pem|percin|kovan|halka|o_ring|oring|tapa|gecis"
BAGLANTI = r"pem|vida|civata|somun|percin|rivet|saplama|dubel|pul_|_pul|_m\d"
KABLO = r"kablo|demet|hortum|hava_hatti|kilif|tel_"
KANAL = r"kanal|zincir|kovan|rakor|gecis|kelepce|olug|oluk|spiral|bara|klemens|tava|delik|bogaz|kopru"


def sinifla(r, A, B):
    a, b = ad(A).lower() + " " + A["dugum"].lower(), ad(B).lower() + " " + B["dugum"].lower()
    ab = a + " | " + b; d = r["d"]
    occ = r.get("occ"); yz = r.get("yz")
    occ0 = isinstance(occ, list) and occ and max(occ) < 0.05
    if occ0 and (yz is None or yz["n"] == 0):
        return "şüpheli", "SAHTE olası: OCC derinlik 0 ve iki yüzey kesişmiyor (VTK iç testi kötü ağda yanıldı)"
    if yz is not None and yz["n"] == 0 and r["hacim"] is None and (not A["kapali"] or not B["kapali"]):
        return "şüpheli", "yüzeyler kesişmiyor; açık ağ tamamen diğerinin içinde (gömülü) ya da VTK yanılgısı"
    if A["kat"] == "URUN" or B["kat"] == "URUN" or A["dugum"].startswith("URUN") or B["dugum"].startswith("URUN"):
        return "şüpheli", "görsel ürün/sarf (hamur, pizza, kutu, teneke) yerleşimi"
    ayni_birim = A["dugum"].split("__")[0] == B["dugum"].split("__")[0]
    na, nb = (A["ad"] or "").lower(), (B["ad"] or "").lower(); nab = na + " | " + nb
    ayni_mek = A["mek"] is not None and A["mek"] == B["mek"]
    if A["dugum"] == B["dugum"] and A["ad"] and A["ad"] == B["ad"]:
        return "kasıtlı", "aynı parçanın alt katıları birbirine giriyor (tek parça; boolean birleşim yapılmamış)"
    if A["dugum"] == B["dugum"] and not A["ad"] and not B["ad"] and re.search(r"kablo|hava|hortum|boru", A["dugum"].lower()):
        return "kasıtlı", "aynı kablo/hortumun segmentleri birleşimde bindiriyor (tek parça)"
    if re.search(KABLO, a) and re.search(KABLO, b) and A["kat"] in ("GUC", "KONTROL", "HAVA") and B["kat"] in ("GUC", "KONTROL", "HAVA"):
        return "şüpheli", "kablo↔kablo demet içi geçiş (gerçekte üst üste/yan yana döşenir; güzergâh ofseti gerekir)"
    if "din_ray" in ab and re.search(r"cihaz|klemens|sigorta|salter|guc_24v|revpi|anahtari|kacak", ab):
        return "kasıtlı", "DIN raya geçme cihaz (cihazın ray yuvası modellenmemiş)"
    if "harting" in ab and "fis" in ab and "soket" in ab: return "kasıtlı", "geçme konnektör (fiş soketin içinde)"
    if d <= 0.2 and re.search(SIKI, ab): return "kasıtlı", "sıkı geçme ≤0,2 mm (conta/rakor/kelepçe/burç)"
    if ayni_birim and re.search(r"mil", nab) and re.search(r"yata[kg]|kol|burc|rulman|kasnak|disli|kaplin|gobek|kavrama", nab):
        return "kasıtlı", "mil ↔ yatak/göbek/kol geçmesi (birim-içi mekanizma)"
    if ayni_birim and re.search(MEKAN, na) and re.search(MEKAN, nb) and d > 0.2:
        return "kasıtlı", "birim-içi mekanizma parçaları (%s)" % (A["mek"] or A["dugum"].split("__")[0])
    if re.search(r"topping_doner__valf_", ab) and re.search(r"valf_blogu|aktuator", nab):
        return "şüpheli", "döner valf ↔ valf bloğu/aktüatör (mil-yuva geçmesi olası; yuva boşluğu modellenmemiş)"
    if "miknatis" in ab: return "şüpheli", "gömülü mıknatıs; diskte cep modellenmemiş"
    if "kelepce" in ab and "ferrule" in ab and d <= 1.0: return "şüpheli", "TC kelepçe ↔ ferrule oturması (kelepçe kanal profili basit)"
    if (re.search(KABLO, a) and re.search(KANAL, b)) or (re.search(KABLO, b) and re.search(KANAL, a)):
        return "kasıtlı", "kablo/hortum kanal-rakor-geçiş içinde"
    if ayni_mek and re.search(MEKAN, na) and re.search(MEKAN, nb): return "kasıtlı", "birim-içi mekanizma (aynı mek: %s)" % A["mek"]
    if re.search(BAGLANTI, a) or re.search(BAGLANTI, b):
        return "kasıtlı", "bağlantı elemanı (PEM/vida/somun) sac içinde; delik modellenmemiş"
    if ("__pu" in A["dugum"] or "__pu" in B["dugum"]) and ayni_birim:
        return "kasıtlı", "PU köpük içine gömülü eleman"
    if A["kpk"] > 0.5 or B["kpk"] > 0.5:
        return "şüpheli", "kapak/kanat (kpk) parçası; kapalı konumda bindirme"
    return "gerçek", ""


def oneri(A, B, r):
    d = r["d"]; a, b = ad(A), ad(B)
    if d <= 0.5: return "%.2f mm bindirme (ölçü yuvarlaması): %s ya da %s %.1f mm geri çekilsin" % (d, a, b, d + 0.5)
    ka = [h - l for l, h in zip(A["lo"], A["hi"])]; kb = [h - l for l, h in zip(B["lo"], B["hi"])]
    va = ka[0] * ka[1] * ka[2]; vb = kb[0] * kb[1] * kb[2]
    kucuk, buyuk = (A, B) if va < vb else (B, A)
    ince = min(min(ka), min(kb))
    if ince <= 3.1 and d >= ince * 0.8:
        return "ince parça (sac/levha) diğerini boydan geçiyor: %s üzerinde delik/kesik aç ya da %s %.0f mm kaydır" % (ad(buyuk), ad(kucuk), d + 1)
    return "%s, %s içine %.1f mm giriyor: küçük parçayı en kısa yönde ~%.0f mm kaydır ya da büyük parçada cep/kesik aç" % (ad(kucuk), ad(buyuk), d, d + 1)


L = []
for n, r in enumerate(D["cak"]):
    r["occ"] = OCC.get(n); r["yz"] = YZ.get(n); r["vtk_d"] = r["d"]
    if isinstance(r["occ"], list) and r["occ"] and max(r["occ"]) < 0.05 and r["yz"] and r["yz"]["n"] > 0:
        r["d"] = round(min(r["d"], min(h - l for l, h in zip(r["yz"]["lo"], r["yz"]["hi"]))), 2); r["bilgi"]["nokta"] = r["yz"]["orta"]
    A, B = BIL[r["i"]], BIL[r["j"]]
    tur, neden = sinifla(r, A, B)
    sA, sB = istasyon(A), istasyon(B)
    L.append(dict(dugum_a=A["dugum"], parca_a=ad(A), dugum_b=B["dugum"], parca_b=ad(B), bilesen=[A["dugum"] + "[%d]" % A["no"], B["dugum"] + "[%d]" % B["no"]],
                  istasyon=sA if sA == sB else "%s ↔ %s" % (sA, sB), mek=[A["mek"], B["mek"]], kat=[A["kat"], B["kat"]],
                  konum_mm=r["bilgi"]["nokta"], derinlik_mm=r["d"], vtk_derinlik=r["vtk_d"], yuzey_kesisim=r["yz"], occ_derinlik=r["occ"], kesisim_hacmi_mm3=r["hacim"],
                  kesisim_kutusu=r["bilgi"]["kutu"], yon=r["bilgi"]["yon"], acik_ag=[not A["kapali"], not B["kapali"]],
                  tur=tur, neden=neden, oneri=oneri(A, B, r) if tur != "kasıtlı" else ""))
L.sort(key=lambda x: -x["derinlik_mm"])
SY = Counter(x["tur"] for x in L)
INC = [dict(a=tam(BIL[r["i"]]), b=tam(BIL[r["j"]]), hacim=r["hacim"], kutu=r["bilgi"]["kutu"]) for r in D["inc"]]
json.dump(dict(model="hat3_v8x.glb",
               yontem="govde_denetim_dogru: bileşen ayrımı, manifold3d kesişim hacmi, 0,6 mm örnekleme + VTK iç testi iki yönlü, OCC doğrulama; ROBOT/INSAN/ZEMIN hariç; tüm düğüm çiftleri + aynı düğümdeki ayrık bileşenler",
               bilesen=len(BIL), temas=D["temas"], incele=INC, ozet=dict(SY), yavas=D["yavas"], hata=D["hata"], bulgular=L),
          open("cakisma.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

f = lambda v: "%.0f" % v


def occs(x):
    o = x["occ_derinlik"]
    return "%.2f" % max(o) if isinstance(o, list) and o else (str(o)[:24] if o else "-")


md = ["# HAT v3 · v8x · TÜM MODEL ÇAKIŞMA TARAMASI (madde 8a, salt okuma)", "",
      "Model `hat3_v8x.glb` · %d katı bileşen (ROBOT/İNSAN/ZEMİN hariç) · yöntem `govde_denetim_dogru` (0,6 mm örnekleme + iç testi iki yönlü, derinlik = kapsayanın yüzeyine uzaklık, OCC doğrulama) · eşik 0,05 mm." % len(BIL), "",
      "**Toplam çakışma %d** · gerçek **%d** · kasıtlı %d · şüpheli %d · temas (≤0,05 mm) %d · incele %d" % (len(L), SY["gerçek"], SY["kasıtlı"], SY["şüpheli"], D["temas"], len(INC)), ""]
G = defaultdict(list)
for x in L:
    if x["tur"] == "gerçek": G[x["istasyon"]].append(x)
md.append("## GERÇEK BULGULAR (istasyona göre; her grupta derinliğe göre sıralı)")
for s in sorted(G, key=lambda s: -max(x["derinlik_mm"] for x in G[s])):
    md += ["", "### %s · %d bulgu" % (s, len(G[s])), "", "| derinlik mm | A | B | konum x,y,z mm | OCC | öneri |", "|---|---|---|---|---|---|"]
    for x in G[s]:
        md.append("| %.2f | %s · %s | %s · %s | %s | %s | %s |" % (x["derinlik_mm"], x["dugum_a"], x["parca_a"], x["dugum_b"], x["parca_b"],
                  ", ".join(f(v) for v in x["konum_mm"]), occs(x), x["oneri"]))
KK = [x for x in L if x["neden"].startswith("kablo↔kablo")]
if KK:
    md += ["", "## ŞÜPHELİ · KABLO↔KABLO DEMET İÇİ GEÇİŞ (%d çift, en derin %.1f mm) — kablo çiftine göre özet" % (len(KK), max(x["derinlik_mm"] for x in KK)), "",
           "Ana hat / QR kablo demetlerinde kablolar aynı güzergâhta birbirinin içinden geçiyor. Üretimde sorun değil ama model ölçüsü yanlış: demet içi kablolar yan yana/üst üste ofsetlenmeli (kablo çapı kadar). Tam liste cakisma.json'da.", "",
           "| kablo A | kablo B | çift | en derin mm | örnek konum |", "|---|---|---|---|---|"]
    gg = defaultdict(list)
    for x in KK: gg[(x["parca_a"], x["parca_b"])].append(x)
    for (pa, pb), xs in sorted(gg.items(), key=lambda kv: -max(x["derinlik_mm"] for x in kv[1]))[:40]:
        xm = max(xs, key=lambda x: x["derinlik_mm"])
        md.append("| %s | %s | %d | %.2f | %s |" % (pa, pb, len(xs), xm["derinlik_mm"], ", ".join(f(v) for v in xm["konum_mm"])))
    if len(gg) > 40: md.append("| … | %d kablo çifti daha (json) | | | |" % (len(gg) - 40))
Z = [x for x in L if x["tur"] == "şüpheli" and not x["neden"].startswith("kablo↔kablo")]
md += ["", "## ŞÜPHELİ · DİĞER (%d)" % len(Z), "", "| derinlik mm | A | B | istasyon | konum x,y,z mm | neden |", "|---|---|---|---|---|---|"]
for x in Z:
    md.append("| %.2f | %s · %s | %s · %s | %s | %s | %s |" % (x["derinlik_mm"], x["dugum_a"], x["parca_a"], x["dugum_b"], x["parca_b"], x["istasyon"],
              ", ".join(f(v) for v in x["konum_mm"]), x["neden"]))
Z = [x for x in L if x["tur"] == "kasıtlı"]
md += ["", "## KASITLI (%d) — nedene göre özet (tam liste cakisma.json)" % len(Z), "", "| neden | adet | en derin mm | örnekler |", "|---|---|---|---|"]
gn = defaultdict(list)
for x in Z: gn[x["neden"]].append(x)
for nd, xs in sorted(gn.items(), key=lambda kv: -len(kv[1])):
    orn = "; ".join(sorted({"%s ↔ %s" % (x["parca_a"], x["parca_b"]) for x in xs})[:4])
    md.append("| %s | %d | %.2f | %s |" % (nd, len(xs), max(x["derinlik_mm"] for x in xs), orn))
for t in ():
    Z = [x for x in L if x["tur"] == t]
    md += ["", "## %s (%d)" % (t.upper(), len(Z)), "", "| derinlik mm | A | B | istasyon | konum x,y,z mm | neden |", "|---|---|---|---|---|---|"]
    for x in Z:
        md.append("| %.2f | %s · %s | %s · %s | %s | %s | %s |" % (x["derinlik_mm"], x["dugum_a"], x["parca_a"], x["dugum_b"], x["parca_b"], x["istasyon"],
                  ", ".join(f(v) for v in x["konum_mm"]), x["neden"]))
if INC:
    md += ["", "## İNCELE (örnekleme sınırı aşıldı, kesin değil)", ""] + ["- %s ↔ %s · hacim %s · kutu %s" % (i["a"], i["b"], i["hacim"], i["kutu"]) for i in INC]
open("cakisma.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print(dict(SY), "temas", D["temas"], "incele", len(INC))
