# -*- coding: utf-8 -*-
"""otonom/kaset3d/akis_kiyma.html — SAYILAR kiyma_model.json'dan (= kiyma_akis_model_v1 çıktısı) okunur, elle yazılmaz."""
import io, json, os
K3 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "otonom", "kaset3d")
S = json.load(io.open(os.path.join(K3, "kiyma_model.json"), encoding="utf-8"))
tr = lambda x, n=1: (("%." + str(n) + "f") % x).replace(".", ",")
sec = "".join("<tr><td>%s</td><td>%s mm/s</td><td>%d mm</td><td><b>%%%d</b></td></tr>" % (x["ad"], tr(x["v"]), x["L"], x["kap"]) for x in S["secenek"])
H = u'''<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AUTOKITCH — Kıyma akış hesabı v1</title><meta name="robots" content="noindex, nofollow"><meta name="color-scheme" content="only light">
<style>
 :root{--line:#333336;--gray:#86868B;--gl:#A1A1A6;--blue:#2997FF;--sari:#ffd24a;--font:-apple-system,"SF Pro Text","Helvetica Neue",Arial,sans-serif}
 *{margin:0;padding:0;box-sizing:border-box} body{font-family:var(--font);background:#000;color:#fff;padding:22px 18px 70px;letter-spacing:-.01em;-webkit-font-smoothing:antialiased}
 .w{max-width:820px;margin:0 auto} h1{font-size:26px;font-weight:600} h2{font-size:13px;letter-spacing:.09em;color:var(--sari);margin:34px 0 10px;text-transform:uppercase}
 p{color:var(--gl);font-size:14.5px;line-height:1.6;margin-top:8px} b{color:#fff} a{color:var(--blue);text-decoration:none}
 .kart{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin-top:12px} .kart div{background:#1D1D1F;border:1px solid var(--line);border-radius:12px;padding:12px 14px;color:var(--gl);font-size:13px;line-height:1.45}
 .kart b{display:block;font-size:21px;margin-bottom:3px} table{width:100%;border-collapse:collapse;margin-top:12px;font-size:13.5px} th{color:var(--gray);font-weight:600;text-align:left;padding:7px 6px;border-bottom:1px solid var(--line);font-size:12px}
 td{padding:8px 6px;border-bottom:1px solid #232326;color:var(--gl)} .v{display:inline-block;background:#3a2a10;color:var(--sari);border-radius:6px;padding:1px 6px;font-size:11px;font-weight:700}
 .kutu{background:#3a1512;border:1px solid #7a2a24;border-radius:12px;padding:13px 15px;margin-top:12px;color:#f7dcd8;font-size:14px;line-height:1.55} .tasir{overflow-x:auto}
</style></head><body><div class="w">
<a href="index.html">← 3D model</a>
<h1 style="margin-top:10px">Kıyma akış hesabı · v1</h1>
<p>Kıymalı harç tane değil <b>macun</b>: serpilmez, memeden <b>şerit</b> olarak çıkar. Bu yüzden kaşar ve kuşbaşındaki “dönen tablaya serpme” hesabı burada geçerli değil. Geçerli olan iki satırlık süreklilik: <b>şeridin çıkış hızı = altındaki hamurun yüzey hızı</b> ve <b>şerit kesiti × serilen boy = doz hacmi</b>.</p>
<div class="kutu"><b>SONUÇ — bu kaset dozu verir ama pideyi KAPLAYAMAZ.</b> __PORS__ g harcın pideyi tam kaplaması için <b>__H__ mm</b>'lik katman gerekir. Şimdiki __AX__ × __AZ__ meme 10 saniyede yalnız <b>__L__ mm</b> şerit serer: pidenin <b>%__KAP__</b>'i. Karışımdaki parçalar (≈ __PM__ mm <span class="v">VARSAYIM</span>) yüzünden şerit __HMIN__ mm'den ince olamaz; o zaman <b>meme ne kadar geniş olursa olsun en çok %__KMAX__</b> kaplanır. Tam kaplama için serilen harcın <b>__YAY__ kat yayılması</b> gerekir: bir <b>yayıcı</b> (sıyırma bıçağı ya da rulo) ya da elle yayma. Spiral tek başına yetmez.</div>

<h2>1 · Sayılar</h2>
<div class="kart"><div><b>__PORS__ g</b>pide başına · 20 pide/gün · 2 gün __KG2__ kg</div><div><b>__Q__ mL/s</b>10 saniyelik dozda akış</div><div><b>__H__ mm</b>tam kaplama için katman</div><div><b>__V__ mm/s</b>şimdiki memeden çıkış hızı</div></div>

<h2>2 · Meme seçenekleri</h2>
<div class="tasir"><table><tr><th>meme</th><th>çıkış hızı</th><th>10 sn'de serilen boy</th><th>pidede kapladığı</th></tr>__SEC__</table></div>
<p>Son satır kuramsal: o incelikte yarıktan soğan ve domates parçaları geçmez.</p>

<h2>3 · Tabla nasıl dönmeli</h2>
<p>Kaşar ve kuşbaşında tabla 35 dev/dk döner. Macunda bu <b>yanlış</b>: r 105'te yüzey hızı __V35__ mm/s, şerit hızının <b>__KAT__ katı</b> — şerit kopar ya da sıvanır. Süreklilik için tabla, ağız dıştayken ≈ 1,6, içteyken ≈ 5,7 dev/dk dönmeli; 10 saniyede toplam <b>__TUR10__ tur</b>. 3D dozaj animasyonu artık bunu gösteriyor: yavaş dönen tabla ve pidenin üstünde __L__ mm'lik tek şerit.</p>

<h2>4 · Helezon</h2>
<p>Kuramsal __VT__ mL/tur · doluluk 0,40 <span class="v">VARSAYIM</span> → __GT__ g/tur · __PORS__ g = __TUR__ tur · ≈ __RPM__ dev/dk. Macunda Roberts formülü geçerli değil (o tane malzeme için); doluluk ve etin vidayla birlikte dönüp dönmediği ancak denemeyle bulunur.</p>

<h2>5 · Seçenekler · karar senin</h2>
<p><b>A · Yayıcı ekle (makine tarafı):</b> memenin arkasında, hamurun 3–4 mm üstünde sabit bir sıyırma bıçağı; tabla dönerken şeridi yayar. Pizza sosu makinelerindeki kepçe mantığı. Parçalı harçta hamuru yırtma riski var, denenmeli.<br><b>B · Piston / pompa satın al</b> ve yaymayı yine ayrı çöz — doz doğruluğu artar ama kaplama sorunu aynı kalır.<br><b>C · Kıymalıyı elle yay</b> (makine yalnız dozu verir). Lahmacun harcı için aynı sorun daha ağır: 110 g harç 1,8 mm katman demek.</p>
</div></body></html>'''
rp = {"__PORS__": "%d" % S["PORS"], "__KG2__": tr(S["KG2"]), "__Q__": tr(S["Q"]), "__H__": tr(S["H_GEREK"], 2), "__AX__": "%d" % S["AGIZ"][0], "__AZ__": "%d" % S["AGIZ"][1], "__L__": "%d" % S["L"], "__KAP__": "%d" % S["kap"],
      "__PM__": "%d" % (S["hmin"] / 2), "__HMIN__": "%d" % S["hmin"], "__KMAX__": "%d" % S["kap_max"], "__YAY__": tr(S["yay"]), "__V__": tr(S["v"]), "__SEC__": sec, "__V35__": "%d" % S["v35"], "__KAT__": "%d" % S["kat35"],
      "__TUR10__": tr(S["tur10"], 2), "__VT__": "%d" % S["Vt"], "__GT__": "%d" % S["g_tur"], "__TUR__": tr(S["tur"]), "__RPM__": "%d" % S["rpm"]}
for a, b in rp.items(): H = H.replace(a, b)
import re; assert not re.search(r"__[A-Z0-9]+__", H)
io.open(os.path.join(K3, "akis_kiyma.html"), "w", encoding="utf-8").write(H); print("akis_kiyma.html yazildi")
