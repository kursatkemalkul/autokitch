# -*- coding: utf-8 -*-
# SİTE: (1) yeni sayfa otonom/hat/cekmece.html — çekmece tahrik sistemi detayı (animasyon + tüm teknik veriler)
#       (2) store.html içine 3B dolap sahnesi — çekmeceye tıklayınca kırmızı vurgu + cekmece.html'e gider
import io, os, shutil
SITE = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\otonom\hat"
ARA = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma"
IMG = os.path.join(SITE, "img")
AP = chr(39)

# ---- 1) görseller ----
for kaynak, hedef in ((os.path.join(ARA, "1_STORE", "CEKMECE_tahrik_animasyon.gif"), "cekmece_tahrik_animasyon.gif"),
                      (os.path.join(ARA, "1_STORE", "CEKMECE_tahrik_detay.png"), "cekmece_tahrik_detay.png"),
                      (os.path.join(ARA, "1_STORE", "STORE_kola_tepsi.png"), "store_3b_cekmeceler.png"),
                      (os.path.join(ARA, "1_STORE", "STORE_tahrik.png"), "store_3b_tahrik.png")):
    if os.path.exists(kaynak): shutil.copy2(kaynak, os.path.join(IMG, hedef)); print("  img:", hedef)

# ---- 2) çekmece detay sayfası ----
sayfa = """<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>STORE · çekmece tahrik sistemi</title><link rel="stylesheet" href="hat.css"></head><body>
<div class="top"><div class="in"><div class="crumb"><a href="../">Store</a><span>&rsaquo;</span><a href="index.html">HAT</a><span>&rsaquo;</span><a href="makine.html">Makine</a><span>&rsaquo;</span><a href="store.html">1 &middot; STORE</a><span>&rsaquo;</span><b>Çekmece tahriki</b></div><div><a href="store.html">&larr; STORE</a></div></div></div>
<div class="wrap"><h1>Çekmece tahrik sistemi<span class="tag" style="background:#d94a3a">17 çekmece · motorlu</span></h1>
<p class="lead">Her çekmece ana PC komutuyla kendi motoruyla açılır ve kapanır. Robot çekmeceyi çekmez; geldiğinde çekmece zaten açıktır. Kasada mekanizma yığını yok: motor, rayın devamına — çekmecenin arkasında kalan 57 mm boşluğa — oturur.</p>

<figure><img src="img/cekmece_tahrik_animasyon.gif" alt="Çekmece açılıp kapanma animasyonu — SolidWorks modeli" loading="lazy"><figcaption>Tek çekmece tahrik detayı — motor, kayış, kablo ve sensör görünür (üst raf gizlendi)</figcaption></figure>

<h2>1 · Nasıl çalışır · komut zinciri</h2><div class="card"><ol class="steps">
<li><b>Karar:</b> ana PC (BEYİN) siparişe göre "taze çekmece 3'ten 1 hamur" der.</li>
<li><b>İletim:</b> ana PC &rarr; Ethernet (Modbus TCP) &rarr; STORE panosundaki PLC. Çekmeceye komut gitmez, PLC'ye gider.</li>
<li><b>Sürme:</b> PLC ilgili röleyi çeker &rarr; 24 V, o çekmecenin motoruna gider &rarr; motor kasnağı kayışı çeker &rarr; çekmece 700 mm açılır (&asymp; 3,7 sn).</li>
<li><b>Durma:</b> motorun Hall enkoderi turu sayar; hedef konumda PLC röleyi keser. Sonsuz vida redüktör kendinden kilitlidir — akım kesilince çekmece kaydığı yerde durur.</li>
<li><b>Alma:</b> PLC "çekmece açık" bilgisini PC'ye döner; robot ancak bu bilgiden sonra kolu sokar (çarpma emniyeti).</li>
<li><b>Kapanma:</b> ters polarite ile motor çekmeceyi geri iter; kapandığını çekmecenin önündeki mıknatısı gören <b>reed sensör</b> doğrular. Sensör 2 sn içinde görmezse PLC alarm verir, hat durur.</li>
<li><b>Sıkışma:</b> sürücü akımı eşiği aşarsa (parmak/kasa sıkışması) motor durur, o çekmece devre dışı kalır, kalan çekmecelerle çalışmaya devam edilir + eleman uyarısı.</li>
</ol></div>

<h2>2 · Hangi motor · hangi parçalar</h2><div class="card"><div class="kv">
<b>Motor</b><span>24 V DC redüktörlü, gövde &Oslash;37 &times; 80 mm, sonsuz vida (kendinden kilitli), çıkış &asymp; 120 d/dk &middot; 5 N&middot;m</span>
<b>Konum geri bildirimi</b><span>Hall enkoder (motor arkasında) — tur sayarak konum; ayrı lineer cetvel yok</span>
<b>Hareket iletimi</b><span>kasnak &Oslash;30 (çevre 94 mm) + GT3 6 mm kayış; kayış çekmecenin yan yüzündeki pabuca kenetli</span>
<b>Hız / süre</b><span>188 mm/sn &rarr; 700 mm tam açılım <b>3,7 sn</b> (yumuşak kalkış-duruş dahil &asymp; 4,5 sn)</span>
<b>Ray</b><span>teleskopik tam açılım 700 mm, çift ray, 45 kg sınıfı (dolu 1 L çekmecesi 44 kg &rarr; 2 ray = 90 kg ✓)</span>
<b>Kapalı doğrulaması</b><span>reed sensör &Oslash;12 &times; 30 (kasada, söve iç yüzünde) + mıknatıs 15&times;8&times;3 (çekmece önünün iç yüzünde)</span>
<b>Kablo</b><span>motor başına tek M12 soket, 3 &times; 0,5 mm² (24 V +, −, enkoder). Soket kasada sabit &rarr; çekmece hareket ederken kablo oynamaz</span>
<b>Kablo yolu</b><span>arka sağ iç köşede dikey kanal 40 &times; 25 &rarr; üstte yatay kanal &rarr; klemens kutusu</span>
<b>Pano (üst teknik bölme)</b><span>24 V 10 A güç kaynağı + PLC (Modbus TCP) + 2 &times; 8 kanal röle kartı</span>
<b>Güç</b><span>aynı anda tek çekmece hareket eder: 24 V &times; 2,5 A &asymp; <b>60 W tepe</b>; bekleme &asymp; 5 W</span>
<b>Motor sayısı</b><span>17 (her çekmecede 1) — dolapta tek merkezi motor yok; tek motor + kavrama düzeneği daha karmaşık ve arızalı olurdu</span>
<b>Alan</b><span>çekmece 700 derin &rarr; kasa iç derinliği 757 &rarr; arkada kalan <b>57 mm</b> motorun yeri. Boşa duran hacim yok</span>
<b>Maliyet</b><span>motor + ray + kayış + sensör &asymp; 180 &euro;/çekmece &rarr; 17 &times; 180 &asymp; <b>3.100 &euro;</b> + pano &asymp; 400 &euro;</span>
</div></div>

<h2>3 · 3B model görüntüleri</h2>
<figure><img src="img/cekmece_tahrik_detay.png" alt="Çekmece tahrik detayı — SolidWorks" loading="lazy"><figcaption>Kesit detay: sağ arkada motor + redüktör + enkoder + M12 soket, kayış çekmeceye kenetli</figcaption></figure>
<div class="thumbs"><a href="img/store_3b_cekmeceler.png" target="_blank"><img src="img/store_3b_cekmeceler.png" loading="lazy"><span>çekmece içleri</span></a><a href="img/store_3b_tahrik.png" target="_blank"><img src="img/store_3b_tahrik.png" loading="lazy"><span>17 çekmece tahrikli</span></a></div>
<p class="note">Model: <code>arastirma/1_STORE/STORE.SLDASM</code> (174 bileşen) &middot; detay: <code>1_STORE/detay2/CEKMECE_TAHRIK_DETAY.SLDASM</code>. Motor, ray, kayış, kablo ve yuva tepsileri ortak parçadır — biri değişince tüm örnekleri değişir.</p>

<h2>4 · Tedarikçiler · alternatifler</h2><div class="card"><table>
<tr><th>Ne</th><th>Marka / kaynak</th><th style="width:170px">Not</th></tr>
<tr><td>Motorlu teleskopik ray (hazır)</td><td>Accuride 3634E · Thomas Regout · Rollon</td><td>tak-çalıştır, 24 V, uç anahtarları dahil</td></tr>
<tr><td>24 V redüktörlü DC motor</td><td>Dunkermotoren · Bühler · Nidec · (TR distribütör)</td><td>sonsuz vida = kendinden kilitli</td></tr>
<tr><td>Kayış + kasnak</td><td>GT3 6 mm, standart</td><td>gıda ortamı, yağsız</td></tr>
<tr><td>Reed sensör</td><td>Ifm · Balluff · standart NO</td><td>&Oslash;12, 24 V, IP67</td></tr>
<tr><td>PLC + röle kartı</td><td>Siemens LOGO! / Unitronics / endüstriyel PC I/O</td><td>Modbus TCP</td></tr>
</table></div>

<h2>5 · Soru işaretleri</h2><div class="card"><table>
<tr><th style="width:44px">#</th><th>Problem</th><th style="width:110px">Durum</th><th>Çözüm / not</th></tr>
<tr><td><b>T1</b></td><td>&minus;18 °C bölmedeki 4 çekmecede motor/kayış</td><td><span class="st on">AÇIK</span></td><td>düşük sıcaklık gresi + IP67 motor; tedarikçiye &minus;25 °C sürüm sorulacak</td></tr>
<tr><td><b>T2</b></td><td>Kayış gerginliği zamanla düşerse</td><td><span class="st on">ÖNERİ VAR</span></td><td>gergi makarası braketi (modelde var), 6 ayda bir bakım kalemi</td></tr>
<tr><td><b>T3</b></td><td>Sıkışma / parmak emniyeti</td><td><span class="st ok">ÇÖZÜLDÜ</span></td><td>akım eşiği + yumuşak kalkış; dükkân tarafında çekmece yok, hepsi servis alanında</td></tr>
<tr><td><b>T4</b></td><td>Temizlik: kayış ve motor gıda alanında</td><td><span class="st on">ÖNERİ VAR</span></td><td>kayış hattı yan duvarda, ürünün altında değil; motor kutusu kapalı</td></tr>
<tr><td><b>T5</b></td><td>Elektrik kesintisinde çekmece açık kalırsa</td><td><span class="st ok">ÇÖZÜLDÜ</span></td><td>sonsuz vida kilitli tutar; elektrik gelince PLC referansa döner (reed sensör)</td></tr>
</table></div>

<h2>6 · Sürüm geçmişi</h2><ul class="ver">
<li>v3 (8 Eyl): motor kasada sabit, kayışla tahrik, çekmece 700 derin — arkadaki 57 mm motora ayrıldı; detay montaj + animasyon</li>
<li>v2 (8 Eyl): hazır motorlu teleskopik ray kararı (kremayer-pinyon tasarımı iptal — fazla karmaşık)</li>
<li>v1 (8 Eyl): motorsuz seçenek (robot çeker) değerlendirildi — reddedildi, otomatik olacak</li>
</ul></div>
<div class="foot">AUTOKITCH &middot; HAT &middot; Yol C canlı tasarım defteri &middot; kaynak: arastirma/1_STORE &middot; 8 Eyl 2026</div></body></html>"""
io.open(os.path.join(SITE, "cekmece.html"), "w", encoding="utf-8").write(sayfa); print("  cekmece.html yazildi")

# ---- 3) store.html: 3B dolap sahnesi (çekmeceye tıkla → cekmece.html) ----
s = io.open(os.path.join(SITE, "store.html"), encoding="utf-8").read()
if "id=\"s3\"" not in s:
    cek = []
    for i, y in enumerate((148.4, 135.4, 122.4, 109.4), 1): cek.append(("icecek%d" % i, "İçecek çekmecesi %d — 70 kutu (7 kanal × 10)" % i, 6.6, y, 62.4, 12.4))
    cek.append(("bir_l", "1 L çekmecesi — 42 şişe (6 × 7)", 6.6, 77.2, 62.4, 31.6))
    for i, y in enumerate((150.9, 140.4, 129.9, 119.4, 108.9, 98.4, 87.9, 77.4), 1): cek.append(("taze%d" % i, "Taze hamur çekmecesi %d — 20 top" % i, 71.4, y, 62.4, 9.9))
    cek.append(("kaset", "Kaset katı klapesi — 4 donmuş kap", 6.6, 40.3, 62.4, 28.4))
    for i, (x, y) in enumerate(((6.6, 29.7), (6.6, 19.7), (71.4, 29.7), (71.4, 19.7)), 1): cek.append(("donmus%d" % i, "Donmuş hamur çekmecesi %d — 20 top" % i, x, y, 62.4, 9.4))
    sat = ",\n ".join("{id:%s%s%s,name:%s%s%s,href:%scekmece.html%s,color:%s#5b8def%s,hover:%s#e2564a%s,boxes:[[%.1f,0,%.1f,%.1f,4,%.1f]]}"
                      % (AP, cid, AP, AP, ad, AP, AP, AP, AP, AP, AP, AP, x, y, w, h) for cid, ad, x, y, w, h in cek)
    blok = ("<h2>3B model — çekmeceye tıkla</h2><p class=\"note\">Dolabın SolidWorks modelinden basitleştirilmiş görünüm. Çekmecenin üstüne gelince kırmızı olur; tıklayınca <a href=\"cekmece.html\">çekmece tahrik sistemi</a> sayfası açılır.</p>"
            "<div class=\"scene\" id=\"s3\"></div>"
            "<script src=\"https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js\"></script>"
            "<script src=\"https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js\"></script>"
            "<script src=\"scene.js\"></script>"
            "<script>buildScene(document.getElementById(\"s3\"),[\n"
            " {id:'zemin',name:'',color:'#eef1f5',boxes:[[-20,0,-2,180,84,2]]},\n"
            " {id:'kasa',name:'STORE kasası 140×84×197',color:'#cfd3d8',boxes:[[0,4,0,140,80,197]]},\n"
            " {id:'panel_ust',name:'Soğutma + pano bölmesi',color:'#aeb6c0',boxes:[[6.6,0,167,126.8,4,30]]},\n"
            " {id:'ayirici',name:'Yatay izoleli ayırıcı PU 80',color:'#aeb6c0',boxes:[[6.6,0,69,126.8,4,7.6]]},\n "
            + sat + "\n],{center:[70,42,98],depth:84,camOff:[0,300,240]});</script>")
    s = s.replace("<h2>3 · Teknik resimler</h2>", blok + "<h2>3 · Teknik resimler</h2>")
    # kararlar tablosuna tahrik satırı + sayfa linki
    s = s.replace("<b>Çekmeceler</b><span>17 çekmece", "<b>Tahrik</b><span>her çekmecede 24 V redüktörlü motor + kayış, ana PC → PLC → röle; <a href=\"cekmece.html\">detay sayfası →</a></span><b>Çekmeceler</b><span>17 çekmece")
    io.open(os.path.join(SITE, "store.html"), "w", encoding="utf-8").write(s); print("  store.html guncellendi (3B sahne + link)")
else: print("  store.html zaten guncel")
print("BITTI")
