# -*- coding: utf-8 -*-
"""robot_fuar_v6/build.py kopyası → v7 (Kemal 30 Eyl): pizza kutusu boş kapalı kutu · ray HAT v3 (936–5100 = 4164) · 2. sayfa kritik sorular"""
import io, sys
P = sys.argv[1]
s = io.open(P, encoding="utf-8").read()
R = [
 ('"""One A4 vendor brief. Interface dimensions from existing CAD, robot illustrative.',
  '"""v7 (30 Eyl 2026 · Claude · Kemal): v6 + pizza kutusu BOŞ KAPALI KUTU olarak çizildi (içi gösterilmez, ölçü aynı) · robot rayı HAT v3 ölçüsü\n'
  '(h3_hesap_v1.ROBOT_RAY_X 936–5100 = 4164 mm · en uzun geçiş ≈ 3,6 m) · 2. sayfa: fuarda sorulacak KRİTİK SORULAR (satıcıya verilmez, soran kişi için).\n'
  'One A4 vendor brief. Interface dimensions from existing CAD, robot illustrative.'),
 ("OUT = ROOT / 'output/pdf/robot-fuar-v6'", "OUT = ROOT / 'output/pdf/robot-fuar-v7'"),
 ("PDF = OUT / 'ROBOT_GENEL_TEKNIK_SARTLAR_A4_v6.pdf'",
  "PDF = OUT / 'ROBOT_GENEL_TEKNIK_SARTLAR_A4_v7.pdf'\n"
  "RAY_ZARF = 5100 - 936          # HAT v3 robot yer rayı (h3_hesap_v1.ROBOT_RAY_X) · v6: 4900 (v1 hattı 200–5100)\n"
  "RAY_GECIS = 3.6               # m · en uzun robot geçişi ≈ zarf − araba (v6: 4,9 → 4,3) · 1 m/sn + 1 m/sn² → ≈ 4,6 sn + yerleşme"),
 ("C.setTitle('Robot + tutucu + kamera | Genel teknik şartlar v5')", "C.setTitle('Robot + tutucu + kamera | Genel teknik şartlar v7')"),
 ("    text(86,108,'Ray zarfı: 4900 mm (çizimde kısaltıldı)',7.7,True,MUTED,'center')",
  "    text(86,108,'Ray zarfı: %d mm (çizimde kısaltıldı)' % RAY_ZARF,7.7,True,MUTED,'center')"),
 ("""        for a,b in [((-160,8,-160),(-154,45,160)),((154,8,-160),(160,45,160)),((-154,8,154),(154,45,160))]: s.cuboid(a,b,'#c8a16a')
        # Pizza shown with lid omitted only to explain the load; carried with lid closed.
        s.cyl((0,8,0),(0,20,0),142,'#dcb47b')
        s.cyl((0,20,0),(0,24,0),127,'#d29442')
        for xx,zz in [(-65,-55),(40,-60),(70,40),(-50,65),(0,0)]:
            s.cyl((xx,24,zz),(xx,27,zz),19,'#ac5742')""",
  """        # v7 · KAPALI KUTU (Kemal: "pizzayı sil, kutu olsun, aynı ölçüde") — 320 × 320 × 45, kapak kapalı, içerik gösterilmez
        for a,b in [((-160,8,-160),(-154,45,160)),((154,8,-160),(160,45,160)),((-154,8,154),(154,45,160)),((-154,8,-160),(154,45,-154))]: s.cuboid(a,b,'#c8a16a')
        s.cuboid((-160,45,-160),(160,48,160),'#d6b37c')                     # kapak
        s.cuboid((-160,40,154),(160,48,162),'#c19a62')                      # kapağın ön dili"""),
 ("    names=['HAMUR TOPU','DOLU PİZZA KUTUSU','KOLA KUTUSU','TATLI KABI']", "    names=['HAMUR TOPU','PİZZA KUTUSU','KOLA KUTUSU','TATLI KABI']"),
 ("      ['Pizza + kutu: en çok 1 kg*','320 × 320 × ~45 mm','Kapalı taşınır; içi gösterildi.'],", "      ['Kutu + içi: en çok 1 kg*','320 × 320 × ~45 mm','Kapalı taşınır.'],"),
 ("      ('Ray / geçiş hedefi','4900 mm toplam zarf; net strok ayrı. 4,3 m geçiş ≤6 sn hedef.'),",
  "      ('Ray / geçiş hedefi','%d mm toplam zarf; net strok ayrı. %s m geçiş ≤5 sn hedef.' % (RAY_ZARF, ('%.1f' % RAY_GECIS).replace('.', ','))),"),
 ("    text(12,292,'v6 / 29.09.2026 | Temsili görsel; CAD kotları korunur. Nihai tutuş, erişim ve güvenlik doğrulaması üreticiyle yapılmalı.',6.7,False,MUTED)\n    C.save()",
  "    text(12,292,'v7 / 30.09.2026 | Temsili görsel; CAD kotları korunur. Nihai tutuş, erişim ve güvenlik doğrulaması üreticiyle yapılmalı.',6.7,False,MUTED)\n    C.showPage()\n    sorular()\n    C.save()"),
 ("    r=PdfReader(str(PDF));assert len(r.pages)==1\n", "    r=PdfReader(str(PDF));assert len(r.pages)==2\n"),
 ("'1455,5','1570,5','191,5','4900','1,5 sn','0,5 sn']", "'1455,5','1570,5','191,5',str(RAY_ZARF),'1,5 sn','0,5 sn']"),
 ("if __name__=='__main__':build_v6()", "if __name__=='__main__':build_v6()   # v7 çıktısı (işlev adı v6'dan kaldı)"),
]
for a, b in R:
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)
SOR = '''

SORULAR = [
    ("Tutucu", "Dört ürünü (Ø66 kola kutusundan 320 × 320 kutuya kadar) TEK tutucuyla, uç değiştirmeden tutabilir misiniz? Hangi tutucu (marka / model, en büyük açıklık, kuvvet ayarı)?"),
    ("Robot", "Hangi robotu önerirsiniz? 3 kg uç yükle, 818 mm montajdan 191,5 mm (en alt) ile 1570,5 mm (en üst) arasına erişiyor mu; bu yükte gerçek hız kaç m/sn?"),
    ("Ray", "RAY_ZARF mm lineer ray (7. eksen) sizde var mı, robotla aynı kontrolden mi sürülüyor? RAY_GECIS m geçiş kaç saniye?"),
    ("Kamera + yazılım", "Ürün konumu ve yuva dolu / boş kontrolü 0,5 sn içinde olur mu? Kendi PC / PLC'mizden Ethernet API / SDK ile komut verebilir miyiz?"),
    ("Gıda + güvenlik", "Gıda ortamına uygun mu (yıkanabilir, IP sınıfı, gıdaya uygun ped)? Çitsiz, insanla aynı alanda çalışabilir mi?"),
    ("Deneme", "Bu dört ürünle numune denemesi yapıp video verebilir misiniz? CAD / URDF modeli verir misiniz?"),
    ("Fiyat + servis", "Robot + ray + tutucu + kamera + kurulum ayrı kalem fiyatı, teslim süresi; Türkiye'de servis ve yedek parça var mı?"),
]


def sorular():
    """2. sayfa: fuarda soran kişi için (satıcıya verilmez) · 7 kritik soru"""
    box(0,0,210,3,fill=AMBER)
    text(12,13,'ROBOT FUARI / SORULACAKLAR',9,True,AMBER)
    text(198,13,'SATICIYA VERİLMEZ',8,True,MUTED,'right')
    text(12,24,'Kritik sorular (7)',16,True)
    para(12,29,186,'1. sayfayı göster, sonra bu soruları sor. “Evet” cevabında <b>model adı, sayı ve fiyat</b> iste; söz değil veri sayfası.',8.6,11)
    y = 44
    for i, (baslik, soru) in enumerate(SORULAR):
        soru = soru.replace('RAY_ZARF', str(RAY_ZARF)).replace('RAY_GECIS', ('%.1f' % RAY_GECIS).replace('.', ','))
        box(12,y-5,186,0.4,fill='#c9d6da')
        badge(17,y+2,i+1,AMBER)
        text(24,y+3,baslik.upper(),8.6,True,AMBER)
        h = para(24,y+6,172,soru,9.6,12.5)
        para(24,y+9+h,172,'Cevap / model / sayı: ____________________________________________________________',8,11,MUTED)
        y += 14 + h + 11
    para(12,y+2,186,'<b>Dikkat:</b> işimizi / makinemizi anlatma. Yalnız 1. sayfadaki ürünler, ölçüler ve hızlar konuşulur.',8.6,11,RED)
    text(12,292,'v7 / 30.09.2026 | Soru sayfası · 1. sayfa satıcıya verilir, bu sayfa verilmez.',6.7,False,MUTED)
'''
assert s.count("\n\ndef build_v6():") == 1
s = s.replace("\n\ndef build_v6():", SOR + "\n\ndef build_v6():", 1)
io.open(P, "w", encoding="utf-8").write(s)
print("yama tamam", len(R))
