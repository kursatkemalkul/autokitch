import io, re
s = io.open("makine_v2.html", encoding="utf-8").read()
R = [
 ("<title>MAKİNE v2 — iki katlı TOPPING, dar hat</title>", "<title>MAKİNE v3 — sos ve harç dik iner</title>"),
 ("u = '../hat3d/v2/parca_kutulari.json?v=1'", "u = '../hat3d/v3/parca_kutulari.json?v=1'"),
 ("<b>Makine v2</b></div><div><a href=\"makine.html\">v1 modeli &rarr;</a></div>", "<b>Makine v3</b></div><div><a href=\"makine_v2.html\">v2 modeli &rarr;</a> &middot; <a href=\"makine.html\">v1 &rarr;</a></div>"),
 ("<h1>MAKİNE v2 &mdash; iki katlı TOPPING, dar hat<span class=\"tag\" style=\"background:#1f6feb\" id=\"etiket\">4722,5 &times; 909 &times; 2200 · HAT v2.1</span></h1>",
  "<h1>MAKİNE v3 &mdash; sos ve harç dik iner<span class=\"tag\" style=\"background:#1f6feb\" id=\"etiket\">4494 &times; 909 &times; 2200 · HAT v3.1</span></h1>"),
 ("src=\"../hat3d/v2/hat2_v1.glb?v=1\" ios-src=\"../hat3d/v2/hat2_v1.usdz?v=1\" alt=\"AUTOKITCH hat versiyon 2 üretim modeli\"",
  "src=\"../hat3d/v3/hat3_v1.glb?v=1\" ios-src=\"../hat3d/v3/hat3_v1.usdz?v=1\" alt=\"AUTOKITCH hat versiyon 3 üretim modeli\""),
 ("camera-target=\"2.87m 1.05m 0.1m\"", "camera-target=\"2.98m 1.05m 0.1m\""),
 ("AUTOKITCH &middot; HAT v2 &middot; model: arastirma/_uretec/hat2_montaj_v1.py (h2_* üreteçleri)", "AUTOKITCH &middot; HAT v3 &middot; model: arastirma/_uretec/h3/hat3_montaj_v1.py (h3_* üreteçleri)"),
 ("U:'makine_v2.html'", "U:'makine_v3.html'"),
 ("B:'MODÜL B · ÇEKMECELİ DOLAP (21 çekmece)'", "B:'MODÜL B · ÇEKMECELİ DOLAP (21 çekmece + teknik sütun)'"),
 ("E:'MODÜL E · KUTU (+ B soğutması altında)'", "E:'MODÜL E · KUTU (+ robot çöpü altında)'"),
 ("parca:'../hat3d/v2/parca_kutulari.json?v=1'", "parca:'../hat3d/v3/parca_kutulari.json?v=1'"),
 ("fetch('../hat3d/v2/durum.json?v=1')", "fetch('../hat3d/v3/durum.json?v=1')"),
 ("HAT ' + (H.surum || 'v2')", "HAT ' + (H.surum || 'v3')"),
]
for a, b in R:
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
i0 = s.index('<div class="card v2"'); i1 = s.index('<span id="v2denetim"')
kart = ('<div class="card v2" style="border-left:4px solid #1f6feb;background:#f2f6fd;margin:12px 0"><b style="color:#1747a6">VERSİYON 3 (30 Eyl 2026 · yerel).</b> v1 ve v2 aynen duruyor; bu ayrı model.\n<ul>\n'
        '<li><b>SOS + HARÇ DİK İNER:</b> üst katta yalnız iki UNO · hortum sola gitmez, dik iner · yayıcılar alt kat dozajlayıcılarının arasında (sos kıyma ile kuşbaşının arası · harç kaşar kasetinin önü).</li>\n'
        '<li><b>A 700 AYNI</b> (736–1436) · TOPPING sol duvarı kıymanın dibinde · hat 4494.</li>\n'
        '<li><b>DOLAP K\'NIN ALTINA UZAR:</b> 21 çekmece (2 gün) + K altında teknik sütun: Secop + pano + kaşar / sucuk deposu.</li>\n'
        '<li><b>ROBOT ÇÖPÜ E\'NİN ALTINDA</b> · <b>YAĞ TENEKESİ FIRIN ÜSTÜNDE</b> (kompresör sola) · pompa grubu K\'nın üstünde.</li>\n</ul>')
s = s[:i0] + kart + s[i1:]
io.open("makine_v3.html", "w", encoding="utf-8").write(s)
print("ok", len(s))
