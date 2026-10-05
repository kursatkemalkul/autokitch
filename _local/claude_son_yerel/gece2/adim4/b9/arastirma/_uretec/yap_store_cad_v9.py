# -*- coding: utf-8 -*-
"""store_cad_v8 → store_cad_v9 (28 Eyl 2026) — ÜRETİM DÜZELTMELERİ (katı denetimi denetim_kati_v1.py · Kemal: "düzelt, onaylıyorum yap").
1 · KAPAK İÇ SACI TEK PARÇA: v8'de 1,0 iç sac, fitil geçme kanalı (6,4 × 8,4 süpürme) tarafından boydan boya kesilip İKİ ayrık parçaya (dış halka + orta panel)
    bölünüyordu — halka yalnız köpüğe yapışık kalırdı. v9: kanalın DIŞINDAKİ halka dış sacın ARKA DÖNÜŞÜ (304 1,5, dört kenar bükümünün devamı, kanal
    kenarına kadar); iç sac yalnız kanalın İÇİNDEKİ panel (304 1,0, tek parça). Fitil dişi, dış sacın dönüşü ile iç panel arasındaki 6,4 kanala geçer
    (standart sandviç kapak düzeni). Kanal, fitil, kapak ölçüleri ve kotlar AYNI. 24 çekmece önü + K4 depo kapağı.
2 · ISI KALKANI SOL SACI TEK PARÇA: v8'de sac x 2517'de, fırın taşıyıcısının dikmeleri + çaprazı (x 2502,5–2532,5) aynı düzlemden geçip sacı ÜÇE bölüyordu.
    v9: sac x 2534–2535 (çerçevenin dışında, B4 bölmesinin sağ sacının tam üstü); yalnız 2 taşıyıcı kiriş üstten çentik açar, sac tek parça.
    Isı kalkanı / ışınım sacı / ayırma sacı 2534'ten başlar (hava boşluğu 17 mm kısaldı: 1257 → 1240), üst PU 2534'e uzar (B4 bölmesinin üstü tam dolu).
BOM 1_STORE_v12. Önceki: store_cad_v8.py"""
import io, os
U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "store_cad_v8.py"), encoding="utf-8").read()
NL = chr(10)


def degis(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


degis('"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v8 (28 Eyl 2026 gece)',
      '"""AUTOKITCH · ÇEKMECELİ DOLAP (B) — ÜRETİM MODELİ v9 (28 Eyl 2026 akşam · yap_store_cad_v9.py): KAPAK İÇ SACI TEK PARÇA (kanal dışı halka = dış sacın arka dönüşü)'
      ' · ISI KALKANI SOL SACI TEK PARÇA (x 2534, taşıyıcı çerçevenin dışında) · BOM 1_STORE_v12 · önceki store_cad_v8.py' + NL +
      'v8: ÜRETİM MODELİ v8 (28 Eyl 2026 gece)')
degis('X_F = (2517.0, 3793.0)                          # fırın altı ısı kalkanı x (SPEC) · fırın 2500–4000',
      'X_F = (2534.0, 3793.0)                          # v9: 2517 → 2534 — sol sac taşıyıcı dikme / çapraz düzleminin (2502,5–2532,5) dışında, B4 sağ sacının üstü (tek parça) · fırın 2500–4000')
degis('''        kn = cevre_supur(acik[0], acik[1], acik[2], acik[3], KANAL)
        pu, ic = pu.cut(kn), ic.cut(kn)
    ekle(ad + "_dis_sac_1.5", ds, "sac", bir, grup=grup, bom=bom)''',
      '''        kn = cevre_supur(acik[0], acik[1], acik[2], acik[3], KANAL)
        pu, ic = pu.cut(kn), ic.cut(kn)
        # v9 · kanalın DIŞINDAKİ halka = dış sacın ARKA DÖNÜŞÜ (1,5) · iç sac = yalnız kanalın İÇİNDEKİ panel (v8: 1,0 iç sac kanalla ikiye bölünüyordu)
        _pl = kut(a_ + 1.0, b_ - 1.0, c_ + 1.0, d_ - 1.0, Z_ON0, Z_ON0 + 1.5).cut(kn)
        _pp = sorted(_pl.solids().vals(), key=lambda s_: -s_.BoundingBox().xlen * s_.BoundingBox().ylen)
        assert len(_pp) == 2, "%s: kanal dış halkası %d parça" % (ad, len(_pp))
        _halka = cq.Workplane(obj=_pp[0])
        ds = ds.union(_halka)
        pu = pu.cut(_halka)
        _ip = sorted(ic.solids().vals(), key=lambda s_: s_.BoundingBox().xlen * s_.BoundingBox().ylen)
        assert len(_ip) == 2, "%s: iç sac %d parça" % (ad, len(_ip))
        ic = cq.Workplane(obj=_ip[0])
        assert len(ds.solids().vals()) == 1, "%s: dış sac tek parça değil" % ad
    ekle(ad + "_dis_sac_1.5", ds, "sac", bir, grup=grup, bom=bom)''')
degis('"""kulpsuz 40\'lık ön: dış sac 1,5 (dört kenardan bükülü) + PU + iç sac 1,0; iç sacda fitil kanalı; fitil"""',
      '"""kulpsuz 40\'lık ön: dış sac 1,5 (dört kenardan bükülü + arkada kanal kenarına kadar DÖNÜŞ) + PU + iç panel 1,0 (kanalın içi); fitil kanalı dönüş ile panel arası; fitil"""')
degis('"dış 304 1,5 bükme + PU 37,5 köpük + iç 304 1,0 (fitil kanallı)"',
      '"dış 304 1,5 bükme (4 kenar + arkada kanal kenarına dönüş) + PU 37,5 köpük + iç panel 304 1,0 · fitil dişi dönüş ile panel arasındaki 6,4 kanala geçer"')
degis('"dış 304 1,5 + PU 37,5 + iç 304 1,0 (fitil kanallı) · bas-aç (Accuride DZ3832-TR)"',
      '"dış 304 1,5 (arkada kanal kenarına dönüş) + PU 37,5 + iç panel 304 1,0 (fitil kanalı dönüş ile panel arası) · bas-aç (Accuride DZ3832-TR)"')
degis('print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v11")))', 'print("BOM:", bom_yaz(os.path.join(KOK, "arastirma", "1_STORE_v12")))')
compile(s, "store_cad_v9.py", "exec")
io.open(os.path.join(U, "store_cad_v9.py"), "w", encoding="utf-8").write(s)
print("store_cad_v9.py yazildi · %d satir" % s.count(NL))
