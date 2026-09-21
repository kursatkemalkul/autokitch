# -*- coding: utf-8 -*-
"""TANE ÜRÜNLER (kuşbaşı · küp sucuk) için hesap sayfası — kullanım: python tane_sayfa_v1.py kusbasi | sucuk
otonom/kaset3d/akis_<ürün>.html + <ürün>_dagilim.png — SAYILAR kusbasi_model.json'dan (= kusbasi_akis_model_v1 çıktısı) okunur, elle yazılmaz."""
import io, json, math, os, random
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import importlib, sys
URUN = sys.argv[1] if len(sys.argv) > 1 else "kusbasi"
KM = importlib.import_module({"kusbasi": "kusbasi_akis_model_v2", "sucuk": "sucuk_akis_model_v1"}[URUN])
from kasar_akis_model_v2 import r_t, T_DOK, PIDE_R, KENAR

K3 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "otonom", "kaset3d")
S = json.load(io.open(os.path.join(K3, URUN + "_model.json"), encoding="utf-8")); G = S["giris"]["G"]
tr = lambda x, n=1: ("%." + str(n) + "f") % x if isinstance(x, float) else str(x)
tr = lambda x, n=1: (("%." + str(n) + "f") % x).replace(".", ",")

# ---------- grafik: pide üstüne düşen küpler (tek deneme) ----------
fig, axs = plt.subplots(1, 3, figsize=(12, 4.3), facecolor="#000")
for ax, d in zip(axs, ((10.0, 12.0, 15.0) if URUN == "kusbasi" else (6.0, 8.0, 10.0))):
    R = random.Random(3); N = int(round(KM.PORS / KM.kup(d))); w = 2 * math.pi * 35.0 / 60.0; xs, zs = [], []
    for k in range(N):
        t = T_DOK * (k + R.random()) / N; r = KM.r_t_k(t); a = -w * t
        x = r + R.uniform(-G["AGIZ"][0] / 2, G["AGIZ"][0] / 2) + R.gauss(0, 4); z = R.uniform(-G["AGIZ"][1] / 2, G["AGIZ"][1] / 2) + R.gauss(0, 4)
        xs.append(x * math.cos(a) - z * math.sin(a)); zs.append(x * math.sin(a) + z * math.cos(a))
    ax.set_facecolor("#000"); ax.add_patch(plt.Circle((0, 0), PIDE_R, color="#e8d9ae")); ax.add_patch(plt.Circle((0, 0), PIDE_R - KENAR, color="#dcc98f"))
    for x, z in zip(xs, zs): ax.add_patch(plt.Rectangle((x - d / 2, z - d / 2), d, d, color=("#8c2b28" if URUN == "kusbasi" else "#a8331a")))
    ax.set_xlim(-150, 150); ax.set_ylim(-150, 150); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("küp %d mm · %d adet" % (d, N), color="#fff", fontsize=13)
plt.tight_layout(); plt.savefig(os.path.join(K3, URUN + "_dagilim.png"), dpi=110, facecolor="#000"); plt.close()

# ---------- sayfa ----------
ok = lambda b: '<span class="ok">✓</span>' if b else '<span class="no">✗</span>'
tane = "".join("<tr><td><b>%d mm</b></td><td>%s g</td><td>%d</td><td>%s</td><td>%s%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
    t["d"], tr(t["m"], 2), t["n"], ok(t["bogaz"]), tr(t["R_on"], 2), " " + ok(t["R_on"] >= 1.75), ok(t["hatve"]), ok(t["agiz"]), ok(t["rotor"])) for t in S["tane"])
kap = "".join("<tr><td>%%%d</td><td>%s</td><td>Ø%s</td><td>%s</td><td>%s</td><td><b>%s</b></td></tr>" % (k["z"], tr(k["p"]), tr(k["mil"]), tr(k["Vt"]), tr(k["eta"], 2), tr(k["q"])) for k in S["kapasite"])
duy = " · ".join("φ %d° → %s" % (x["fi"], tr(x["q"])) for x in S["duyarlilik"])
doz = "".join("<tr><td>%s</td><td><b>%s g</b></td><td>%s tur</td><td>%s dev/dk</td><td>%s m/s</td><td>± %d°</td></tr>" % (tr(x["etaF"], 2), tr(x["g_tur"]), tr(x["tur"], 2), tr(x["rpm"]), tr(x["uc"], 3), x["aci"]) for x in S["doz"])
bel = "".join("<tr><td><b>%d mm</b></td><td>%s</td><td>± %s küp</td><td><b>± %%%s</b></td><td>%%%s</td></tr>" % (x["d"], tr(x["nk"]), tr(x["sig"], 2), tr(x["yuzde"]), tr(x["bir"])) for x in S["belirsizlik"])
dag = "".join("<tr><td><b>%d mm</b></td><td>%d</td><td>%s</td><td>%%%d</td><td>%%%d</td><td><b>%%%s</b></td></tr>" % (x["d"], x["N"], tr(x["ort"]), x["cv"], x["poisson"], tr(x["bos"])) for x in S["dagilim"])
D0 = [x for x in S["doz"] if abs(x["etaF"] - 0.6) < 1e-9][0]
tar = "".join("<tr%s><td><b>r %d</b>%s</td><td>%%%d</td><td>%%%s</td></tr>" % (' style="background:#15243a"' if x["secilen"] else "", x["r_max"], " ← seçilen" if x["secilen"] else "", x["cv"], tr(x["tas"])) for x in S["yasa_tarama"])
obk = "".join("<tr><td>%s</td><td><b>%%%s</b></td></tr>" % (x["ad"], tr(x["bos"])) for x in S["obek"])
ist = " · ".join("r %d: %s sn" % (x["r"], tr(x["sn"], 2)) for x in S["yasa"]["ist"] if x["sn"] >= 0.05)

H = u'''<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AUTOKITCH — Kuşbaşı akış hesabı v1</title><meta name="robots" content="noindex, nofollow"><meta name="color-scheme" content="only light">
<style>
 :root{--line:#333336;--gray:#86868B;--gl:#A1A1A6;--blue:#2997FF;--sari:#ffd24a;--font:-apple-system,"SF Pro Text","Helvetica Neue",Arial,sans-serif}
 *{margin:0;padding:0;box-sizing:border-box} body{font-family:var(--font);background:#000;color:#fff;padding:22px 18px 70px;letter-spacing:-.01em;-webkit-font-smoothing:antialiased}
 .w{max-width:820px;margin:0 auto} h1{font-size:26px;font-weight:600} h2{font-size:13px;letter-spacing:.09em;color:var(--sari);margin:34px 0 10px;text-transform:uppercase}
 p{color:var(--gl);font-size:14.5px;line-height:1.6;margin-top:8px} b{color:#fff} a{color:var(--blue);text-decoration:none}
 .kart{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin-top:12px} .kart div{background:#1D1D1F;border:1px solid var(--line);border-radius:12px;padding:12px 14px;color:var(--gl);font-size:13px;line-height:1.45}
 .kart b{display:block;font-size:21px;margin-bottom:3px} table{width:100%;border-collapse:collapse;margin-top:12px;font-size:13.5px} th{color:var(--gray);font-weight:600;text-align:left;padding:7px 6px;border-bottom:1px solid var(--line);font-size:12px}
 td{padding:8px 6px;border-bottom:1px solid #232326;color:var(--gl)} .ok{color:#34c759;font-weight:700} .no{color:#ff6b5e;font-weight:700} .v{display:inline-block;background:#3a2a10;color:var(--sari);border-radius:6px;padding:1px 6px;font-size:11px;font-weight:700}
 .kutu{background:#15243a;border:1px solid #274b78;border-radius:12px;padding:13px 15px;margin-top:12px;color:#d8e6f7;font-size:14px;line-height:1.55} img{width:100%;border-radius:12px;margin-top:12px;border:1px solid var(--line)} .tasir{overflow-x:auto}
</style></head><body><div class="w">
<a href="index.html">← 3D model</a>
<h1 style="margin-top:10px">Kuşbaşı akış hesabı · v1</h1>
<p>Kuşbaşı ne kaşar gibi hafif tane ne kıyma gibi macun: <b>ıslak, yumuşak, iri tane.</b> Bu yüzden hesabı tek sayı yönetiyor: <b>küp kenarı d</b>. Kasetin her ölçüsü d'nin katı olarak çıkıyor.</p>
<div class="kutu"><b>SONUÇ:</b> kaset <b>10 mm küpte bütün kuralları sağlıyor</b>, 12 mm'de tek kural sınırda (ağız 3,7 d), <b>15 mm'de çalışmaz</b>. Kasaba verilecek ölçü: <b>en çok 12 mm, hedef 10 mm.</b> Küp boyu <span class="v">VARSAYIM</span> — tarifler yalnız “olabildiğince minik” diyor, sayı yok; ilk iş bunu cetvelle ölçmek.</div>

<h2>1 · Ürün</h2>
<div class="kart"><div><b>__PORS__ g</b>pide başına · 20 pide/gün</div><div><b>__KG2__ kg</b>2 günlük = __LITRE__ L</div><div><b>__RHO__ g/mL</b>dökme yoğunluk <span class="v">VARSAYIM</span><br>1 cup çiğ küp et 170–198 g</div><div><b>μ __MU__</b>duvar sürtünmesi <span class="v">VARSAYIM</span><br>kas dokusu 0,29–0,36</div></div>

<h2>2 · Kurallar → ölçüler</h2>
<table><tr><th>kural</th><th>kaynak</th><th>gereken</th><th>kasette</th></tr>
<tr><td>Köprü kurmasın: düşey açıklık</td><td><a href="https://bulkinside.com/bulk-solids-handling/storage-transportation/ten-steps-to-an-effective-bin-design/">BulkInside</a> · tek boy tanede 4 ×, karışıkta 2–3 ×</td><td>≥ 4 d</td><td>boğaz = tekne <b>Ø__BOGAZ__</b> · ağız <b>__AGX__ × __AGZ__</b></td></tr>
<tr><td>Topak sıkışmasın: mil ile tekne arası</td><td><a href="https://www.kwsmfg.com/engineering-guides/screw-conveyor/bulk-material-characteristics/">CEMA 350 / KWS</a> · R = 1,75 · 2,5 · 4,5</td><td>≥ R · d</td><td><b>__KANAL__ mm</b> · konik kökte __KANALK__ mm</td></tr>
<tr><td>Küp iki kanat arasına sığsın</td><td>geometri</td><td>net boşluk ≥ 3 d</td><td>hatve __P0__ → __P1__, kanat 4 mm → <b>__HB__ mm</b> · çift ağız OLMAZ</td></tr>
<tr><td>İki hareketli yüzey arası küp ezmesin</td><td>geometri: ya giremesin ya rahat geçsin</td><td>&lt; d/3 ya da &gt; 1,5 d</td><td>lama–duvar <b>__LAMA__</b> · rotor–kanat <b>__ROTOR__</b></td></tr></table>
<p>CEMA'nın “hepsi topak” sınıfı (R = 4,5) 10 mm küpte bile 45 mm boşluk ister; 140'lık gövdeye sığmaz. O kural kömür, taş gibi <b>sert</b> topak için. Et yumuşak, ezilerek geçer; biz sınıf 2'yi (2,5) tutturduk. Sıkışma olursa ilk bakılacak yer burası.</p>

<h2>3 · Küp boyuna göre kaset geçer mi</h2>
<div class="tasir"><table><tr><th>küp</th><th>bir küp</th><th>pide başına</th><th>boğaz</th><th>R (mil–tekne)</th><th>hatve</th><th>ağız</th><th>rotor</th></tr>__TANE__</table></div>

<h2>4 · Helezon kapasitesi · Roberts</h2>
<p>Kaşardaki aynı formül. Arkada konik kök, öne doğru açılan hatve: kapasite <b>akış yönünde sürekli artıyor</b>, et hiçbir yerde sıkışmıyor ve hazne yalnız arkadan değil boyunca çekiliyor.</p>
<div class="tasir"><table><tr><th>yer (arka → ön)</th><th>hatve</th><th>mil</th><th>Vt mL/tur</th><th>verim</th><th>taşınan mL/tur</th></tr>__KAP__</table></div>
<p>Sürtünmeye duyarlılık (ön uç, mL/tur): __DUY__. Sürtünme iki katına çıksa kapasite %20 düşüyor — sonuç sürtünme varsayımına çok bağlı değil.</p>

<h2>5 · Doz ve devir</h2>
<div class="tasir"><table><tr><th>doluluk <span class="v">VARSAYIM</span></th><th>tur başına</th><th>145 g</th><th>10 sn'de</th><th>kanat ucu hızı</th><th>± %5 doz</th></tr>__DOZ__</table></div>
<p>Vida büyük olduğu için doz <b>≈ 2 turda</b> çıkıyor. Kaşardaki gibi olsaydı bu “pide başına 2 öbek” demekti. Onu şu çözüyor:</p>
<div class="kutu"><b>EŞİK + TIKAÇ:</b> kanat ağızdan <b>__TIK__ mm önce bitiyor.</b> Aradaki et yatağı arkadan gelenle <b>tıkaç gibi itiliyor</b> ve 6 mm'lik bir <b>eşiğin</b> üstünden aşıp ağza dökülüyor. Böylece akış tur tur değil <b>sürekli</b>: küpler tek tek düşüyor. Eşik aynı zamanda tüpün dibinde ≈ 50 mL <b>et suyunu tutuyor</b>, ağızdan damlamıyor. Tıkaçta itme basıncı yalnız <b>× __JAN__</b> artıyor (Janssen) — et ezilmez.</div>

<h2>6 · Hacimsel dozun alt sınırı</h2>
<p>Vida hacim ölçer, küp saymaz. Dozun başında ve sonunda kesme düzlemine denk gelen küpler “içeride mi dışarıda mı” belirsiz. Bu, hiçbir ayarla giderilemeyen <b>alt sınır</b>; doluluk oynarsa üstüne biner.</p>
<div class="tasir"><table><tr><th>küp</th><th>kesme düzleminde</th><th>belirsizlik</th><th>dozda</th><th>tek küp</th></tr>__BEL__</table></div>

<h2>7 · Pidenin üstü</h2>
<p>Tabla 35 dev/dk dönerken dıştan içe yürüyor, küpler sürekli düşüyor. 25 mm'lik hücrelerde küp sayıldı (8 deneme ortalaması). “Rastgele serpmenin sınırı” = bu kadar az küple elde edilebilecek en iyi düzgünlük.</p>
<img src="__PNG__" alt="pide üstünde küpler">
<div class="tasir"><table><tr><th>küp</th><th>adet</th><th>hücre başına</th><th>sapma</th><th>rastgele serpmenin sınırı</th><th>boş hücre</th></tr>__DAG__</table></div>
<p>Sapma her boyda rastgele serpmenin sınırında: <b>makine elinden geleni yapıyor</b>, boşluğu belirleyen küp sayısı. 10 mm'de hücrelerin %10'u boş, 15 mm'de yarısından fazlası. Düzgün görünen pide için de küçük küp gerekiyor.</p>

<h2>7b · Tabla her yere eşit veriyor mu · “pat diye” dökerse ne olur</h2>
<p>Hesap şu kurguyla yapıldı: helezon doz boyunca <b>sabit hızla</b> döner (sabit gram/saniye), tabla dönerken ağız pidenin <b>dışından içine</b> yürür. Her halkaya cm² başına aynı gram düşmesi için ağzın her yarıçapta ne kadar oyalanacağı <b>çözüldü</b> (negatif olmayan en küçük kareler, scipy).</p>
<p>Kaşarın hareket yasası burada tutmadı: kaşar eriyip ≈ 13 mm yayılıyor, küp yayılmıyor. Kaşar yasasıyla halkalar arası sapma <b>%__ECV__</b> (en dış halka ortalamanın %__EDIS__'i). Kuşbaşı için çözülen yasayla <b>%__YCV__</b> (en dış halka %__YDIS__).</p>
<div class="tasir"><table><tr><th>ağız merkezi en dışta</th><th>halkalar arası sapma</th><th>kenar payına (r &gt; 125) taşan</th></tr>__TAR__</table></div>
<p>Bu bir <b>takas</b>: ağız 48 mm geniş olduğu için en dış halkayı doldurmak, bir kısmını kenar payına taşırmadan olmuyor. Oyalanma süreleri: __IST__.</p>
<div class="tasir"><table><tr><th>aynı __PORS__ g nasıl düşerse (küp __DNOM__ mm)</th><th>pidede boş hücre</th></tr>__OBK__</table></div>
<div class="kutu"><b>“Pat diye” dökmek olmaz — sayı da bunu söylüyor:</b> sürekli akışta pidenin ≈ %13'ü boş, iki öbekte yarısı. Sürekliliği sağlayan şey <b>eşik + tıkaç</b>; bu kasetin <b>en kritik ve henüz denenmemiş</b> parçası. Denemede ilk bakılacak şey: küpler tek tek mi düşüyor, tur başına öbek öbek mi.</div>

<h2>8 · Tork</h2>
<p>Çalışma torku ≈ <b>__TORK__ N·m</b> (yatak __YATAK__ kg + hazne basıncı, sürtünme __F__ N). Redüktör 24 N·m veriyor; tehlike çalışma değil <b>sıkışma</b>. Sürücüde akım sınırı ≈ 3 N·m olmalı ki sinir parçası sıkışırsa baskı kanat kırılmasın, motor dursun.</p>

<h2>9 · Yapamadıklarım</h2>
<p><b>Doluluk (0,60) varsayım.</b> Islak küplerin kanalı ne kadar doldurduğu ancak tartıyla bulunur. <b>Eşiğin üstünden tıkaç akışı</b> hesapta tutarlı ama denenmedi: et yapışkansa eşikte birikebilir — o zaman eşik 6'dan 3'e iner. <b>Gerçek parçacık simülasyonu yok</b>; 7. bölüm bir serpme modeli, küplerin birbirine yapışmasını bilmez. <b>Sinir ve zar parçaları</b> modelde yok; sıkışmanın asıl sebebi onlar olur.</p>
<h2>10 · Deneme</h2>
<p>1) 20 küpü cetvelle ölç → d. 2) 1 litrelik kabı doldur, tart → dökme yoğunluk. 3) Helezonu elle 5 tur çevir, çıkanı tart → g/tur ve doluluk. Bu üç sayıyla bütün sayfa yeniden hesaplanır.</p>
</div></body></html>'''
rp = {"__PNG__": URUN + "_dagilim.png", "__PORS__": "%d" % S["giris"]["PORS"], "__KG2__": tr(S["giris"]["KG2"]), "__DNOM__": "%d" % KM.D_NOM, "__LITRE__": tr(G["KG2"] / G["RHO"], 2) if False else tr(S["giris"]["KG2"] / S["giris"]["RHO"], 2), "__RHO__": tr(S["giris"]["RHO"], 2), "__MU__": tr(S["giris"]["MU"], 2),
      "__BOGAZ__": "%d" % (2 * G["RT"]), "__AGX__": "%d" % G["AGIZ"][0], "__AGZ__": "%d" % G["AGIZ"][1], "__KANAL__": "%d" % (G["RT"] - G["R_MIL"]), "__KANALK__": "%d" % (G["RT"] - G["R_KOK"]),
      "__P0__": "%d" % G["P0"], "__P1__": tr(G["P1"]), "__HB__": "%d" % (G["P0"] - G["T"]), "__LAMA__": tr(G["LAMA_DUVAR"]), "__ROTOR__": "%d" % G["ROTOR_BOSLUK"],
      "__TANE__": tane, "__KAP__": kap, "__DUY__": duy, "__DOZ__": doz, "__TIK__": "%d" % (G["TIKAC"] + G["ESIK"]), "__JAN__": tr(S["janssen"], 2), "__BEL__": bel, "__DAG__": dag,
      "__TAR__": tar, "__OBK__": obk, "__IST__": ist, "__ECV__": "%d" % S["yasa"]["eski"]["cv"], "__EDIS__": "%d" % S["yasa"]["eski"]["profil"][-1], "__YCV__": "%d" % S["yasa"]["yeni"]["cv"], "__YDIS__": "%d" % S["yasa"]["yeni"]["profil"][-1],
      "__TORK__": tr(S["tork"]["T"], 2), "__YATAK__": tr(S["tork"]["yatak"], 2), "__F__": tr(S["tork"]["F"])}
for a, b in rp.items(): H = H.replace(a, b)
assert "__" not in H.replace("__main__", ""), [x for x in H.split() if "__" in x][:5]
if URUN == "sucuk":
    for a, b in (("Kuşbaşı akış hesabı · v1", "Küp sucuk akış hesabı · v1"), ("AUTOKITCH — Kuşbaşı akış hesabı v1", "AUTOKITCH — Küp sucuk akış hesabı v1"),
                 ("Kuşbaşı ne kaşar gibi hafif tane ne kıyma gibi macun: <b>ıslak, yumuşak, iri tane.</b> Bu yüzden hesabı tek sayı yönetiyor", "Küp sucuk <b>sert, yağlı, iri tane</b>: kuşbaşıyla AYNI kasete (gövde, vida, tüp, rotor birebir aynı) giriyor; yeniden kurulan şey hesap. Hesabı yine tek sayı yönetiyor"),
                 ("kaset <b>10 mm küpte bütün kuralları sağlıyor</b>, 12 mm'de tek kural sınırda (ağız 3,7 d), <b>15 mm'de çalışmaz</b>. Kasaba verilecek ölçü: <b>en çok 12 mm, hedef 10 mm.</b> Küp boyu <span class=\"v\">VARSAYIM</span> — tarifler yalnız “olabildiğince minik” diyor, sayı yok; ilk iş bunu cetvelle ölçmek.",
                  "kaset <b>6–10 mm küpte bütün kuralları sağlıyor</b>, 12 mm'de ağız sınırda, <b>15 mm'de çalışmaz</b>. Hedef <b>8 mm</b>: pizzalık küp pepperoni 5–10 mm (<a href=\"https://www.dla.mil/Portals/104/Documents/TroopSupport/Subsistence/Rations/mil/32541.pdf\">MIL-DTL-32541</a>). Küp küçüldükçe pide daha düzgün görünüyor (7. bölüm). Küp boyu <span class=\"v\">VARSAYIM</span> — alınacak ürünün ölçüsüyle değişecek."),
                 ("1 cup çiğ küp et 170–198 g", "sert küp gevşek istiflenir"), ("kas dokusu 0,29–0,36", "yağlı yüzey · ölçülecek"),
                 ("Et yumuşak, ezilerek geçer; biz sınıf 2'yi (2,5) tutturduk.", "Sucuk yarı sert; biz sınıf 2'nin (2,5) üstündeyiz."),
                 ("Eşik aynı zamanda tüpün dibinde ≈ 50 mL <b>et suyunu tutuyor</b>, ağızdan damlamıyor.", "Sucukta sızan sıvı yok; eşiğin işi yalnız akışı sürekli yapmak."), ("— et ezilmez.", "— küp ezilmez."),
                 ("et hiçbir yerde sıkışmıyor", "küp hiçbir yerde sıkışmıyor"), ("sinir parçası sıkışırsa", "iri bir parça sıkışırsa"),
                 ("<b>Eşiğin üstünden tıkaç akışı</b> hesapta tutarlı ama denenmedi: et yapışkansa eşikte birikebilir — o zaman eşik 6'dan 3'e iner.", "<b>Eşiğin üstünden tıkaç akışı</b> hesapta tutarlı ama denenmedi. <b>Soğukta yağ sertleşip küpleri birbirine yapıştırabilir</b> (topaklanma) — rotor bunun için var; denemede bakılacak."),
                 ("<b>Sinir ve zar parçaları</b> modelde yok; sıkışmanın asıl sebebi onlar olur.", "<b>Dilimleyiciye göre farkı:</b> bıçak, şarjör ve sayma yok; doz hacimle veriliyor, o yüzden 6. bölümdeki alt sınır geçerli."),
                 ("1) 20 küpü cetvelle ölç → d.", "1) Alınacak küp sucuğun 20 tanesini cetvelle ölç → d.")):
        assert a in H, a[:60]; H = H.replace(a, b)
io.open(os.path.join(K3, "akis_" + URUN + ".html"), "w", encoding="utf-8").write(H)
print(URUN + ": akis sayfasi + dagilim grafigi · doluluk 0,60: %s g/tur · %s tur · %s dev/dk" % (tr(D0["g_tur"]), tr(D0["tur"], 2), tr(D0["rpm"])))
