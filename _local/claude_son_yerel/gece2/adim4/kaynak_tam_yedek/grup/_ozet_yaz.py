# -*- coding: utf-8 -*-
import json, collections, re, os
H = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(H, "esleme.json"), encoding="utf-8")); P = E["parca"]
RN = {"Pano": "Elektrik", "Hava dağıtımı": "Hava", "Kompresör": "Hava"}
def ren(o):
    i, g = o.split("/", 1); return i + "/" + RN.get(g, g)
adlar = collections.defaultdict(set); tri = collections.Counter()
for p in P:
    tri[p["yeni_mek"]] += p["ntri"]
    if p["ad"]: adlar[p["yeni_mek"]].add(re.sub(r"_kelepce(_\d+)?$", "", p["ad"]))
o = ["# GRUPLAMA DÜZENİ v1 · hat3_v8za → hat3_v8zb (3 Eki 2026)", "",
     "Geometri değişmedi (BIN bayt bayt aynı, JSON yalnız extras farklı). 1.764.392 üçgenin hepsi tek mek + tek kat etiketli; kpk aynı.",
     "Betik: `grup_duzen.py` · denetim: `dogrula.py` · parça tablosu: `esleme.json` (50.880 bileşen, 49.351 adlı) · sayfa ağacı: `mekanizma_v3_8.json`.", "",
     "## 1 · NEREDE — istasyon → ünite (adlı parça sayısı · üçgen)", ""]
ist0 = None
for m in E["mek"]:
    if m["istasyon"] != ist0:
        ist0 = m["istasyon"]; o.append("**%s**" % ist0)
    o.append("- %s — %d parça · %s üçgen" % (m["ad"], len(adlar[m["kod"]]), format(tri[m["kod"]], ",").replace(",", ".")))
o += ["", "## 2 · Taşınanlar (yeniden adlandırma dışında grup değiştiren adlı parçalar)", "",
      "| eski | yeni | adet | örnek |", "|---|---|---|---|"]
tas = collections.defaultdict(set)
for p in P:
    if ren(p["eski_mek"]) != p["yeni_mek"] and p["ad"]:
        tas[(p["eski_mek"], p["yeni_mek"])].add(re.sub(r"_kelepce(_\d+)?$", "", p["ad"]))
for (a, b), s in sorted(tas.items()):
    ss = sorted(s); o.append("| %s | %s | %d | %s |" % (a, b, len(ss), ", ".join(ss[:4]) + (" …" if len(ss) > 4 else "")))
o += ["", "Yeniden adlandırma: her istasyonda `Pano` → `Elektrik` · `Hava dağıtımı` → `Hava` · `F/Kompresör` → `F/Hava` · `Robot/Kablo + zincir` → Robot kolu / Yer rayı / Elektrik.", "",
      "## 3 · NE — disiplin (kat) değişimi (üçgen)", "", "| eski | yeni | üçgen |", "|---|---|---|"]
kc = collections.Counter()
for p in P:
    if p["eski_kat"] != p["yeni_kat"]: kc[(p["eski_kat"], p["yeni_kat"])] += p["ntri"]
for (a, b), n in kc.most_common(): o.append("| %s | %s | %s |" % (a, b, format(n, ",").replace(",", ".")))
kt = collections.Counter()
for p in P: kt[p["yeni_kat"]] += p["ntri"]
o += ["", "Son durum: " + " · ".join("%s %s" % (k, format(kt[k], ",").replace(",", ".")) for k in E["kat"]), ""]
o += ["## 4 · Belirsizler / kararlar (Kemal'e)", "",
      "1. **TOPPING sürücüleri** (`kuru_surucu_*`, kuru bölme panosunda, 2 grup × 26 parça) Kaşar/Sucuk'tan **TOPPING/Elektrik**'e taşındı; disiplini **Motor** kaldı (Motor düğmesinde görünür). Alternatif: sürdüğü kasete (Kaşar/Sucuk) geri.",
      "2. **Motorun kendi kablosu** (`motor_kablosu_*` kaşar/sucuk, EC5000 tahrik rulosu kablosu, PulsaJet M8 kablosu) kural gereği **Elektrik**'e gitti (üretici pigtail'i olsa da).",
      "3. **F/Kompresör → F/Hava** (hattın hava kaynağı ama F üst kabininde duruyor).",
      "4. **Serbest ürün yığınları** (F fırın üstü pizza kutusu yığını, U içecek + kutu yedeği) → **Çevre/Ürün**. Ünitenin içinde duran ürünler (çekmece hamur topları, şarjör karton yığını, yağ tenekesi, robot çöp kovası, kalıptaki kutu) kendi ünitesinde kaldı.",
      "5. **U**: fanlar + filtre kutuları + STEGO termostat yeni **U/Havalandırma** ünitesi; U_F fan kabloları Elektrik/Ana pano'dan **U/Elektrik**'e. Ana pano ve ana hat hat geneli kaldı.",
      "6. **A/Elektrik ve A/Emniyet kalktı**: A/Elektrik yalnız sıfır alanlı artık üçgendi (v3.6'da kalkan sigorta/klemens, görünmez) → A/Gövde; A/Emniyet = ön kapaktaki `onyuz_emniyet_hedefi` (13 üçgen) → A/Gövde, disiplini Kontrol (emniyet). A = Gövde + Açıcı.",
      "7. **Robot**: kol ve yer rayı yalnız yer tutucu kutu (24 / 12 üçgen). Enerji zinciri, zincir oluğu, kablo köprüsü, robot kabloları → **Robot/Elektrik** (kablo yolu); istersen zincir + oluk Yer rayı'na.",
      "8. **Fırın**: TP10'un kendi ana şalteri, CEE prizi, ekranı, sinyal kutusu Fırın ünitesinde (satın alınan cihazın parçası); yalnız üst kabin rakorları (`f_ust_rakor_*`) F/Elektrik'e.",
      "9. **QR göz braketleri** (kapak kulağı, mandal / mil yatağı braketi, menteşe ara plakası) GUC işaretliydi → Mekanizma; `goz_*_motor_braketi` → Motor; QR giriş plakaları (a: Robot/Kontrol kutusu'ndaydı, b: QR/Gövde) → QR/Elektrik.",
      "10. **İstasyon tarafı Harting** (E, K, TOPPING fiş + soket + M32 rakor) Ana hat'tan istasyon Elektrik'ine; K tartı hücresi kablosu + G4 rakoru → K/Elektrik.",
      "11. **Adsız KONTROL → Sensör (76 bileşen)**: çekmece sensör lamı / mıknatıs kümeleri (birbirine kaynaşık, tek kutuya sığmıyor), tabla üstünde 20 × 8 × 33 mm parça (`TOPPING_DONER__TABLA`, x 1076–1096, y 974–982, z −308…−275), E kalıpta 2 × 6 × 16 mm parça (x 4805, y 866–872).",
      "12. Montaj ağındaki hata: Ana hat veri kabloları ve kanallar KONTROL işaretliydi → Elektrik. `kablo_*` adlı ama aslında farklı parça olan yok (yalnız GUC/KONTROL/MOTOR işaretli + adı kablo/rakor/kanal/Harting/klemens/sigorta/pano olanlar taşındı).",
      "13. Valfler: tek valf (K Bıçak / İtici SY3120, harç/sos yayıcı kesme valfi) ünitede; valf adası + şartlandırıcı + hortumlar Hava'da. TOPPING'de ayrı hava hortumu parçası yok (TOPPING_MODUL__hava_ana ağı zaten Hava).", ""]
open(os.path.join(H, "ozet.md"), "w", encoding="utf-8").write("\n".join(o))
print("\n".join(o[:80]))
