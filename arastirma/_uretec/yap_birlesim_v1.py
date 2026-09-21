# -*- coding: utf-8 -*-
"""BİRLEŞİM DETAYLARI v1 → dört üretecin YENİ sürümünü yazar (eskilere dokunmaz):
   kasar_cad_v8 → kasar_cad_v9 · kiyma_cad_v3 → kiyma_cad_v4 · kusbasi_cad_v2 → kusbasi_cad_v3 · sucuk_cad_v1 → sucuk_cad_v2
Bütün detay kodu kaset_birlesim_v1.py'de TEK yerde; burada yalnız (a) sürüm adları, (b) tüp pimleri → tırnak, (c) kapak bloğu → BR.yatak_kapagi,
(d) tüp geçmesi 2,8 → 1,3 (O-ring yeri), (e) kap() sonunda BR.uygula(globals()) çağrısı."""
import io, os, re
U = os.path.dirname(os.path.abspath(__file__))
ISLER = [("kasar_cad_v8", "kasar_cad_v9", [("kasar_kabi_v8", "kasar_kabi_v9"), ("KASAR_KABI_v8", "KASAR_KABI_v9"), ("kasar_v8", "kasar_v9")]),
         ("kiyma_cad_v3", "kiyma_cad_v4", [("kiyma_kaseti_v3", "kiyma_kaseti_v4"), ("KIYMA_KASETI_v3", "KIYMA_KASETI_v4"), ("kiyma_v3", "kiyma_v4")]),
         ("kusbasi_cad_v2", "kusbasi_cad_v3", [("kusbasi_kaseti_v2", "kusbasi_kaseti_v3"), ("KUSBASI_KASETI_v2", "KUSBASI_KASETI_v3"), ("kusbasi_v2", "kusbasi_v3")]),
         ("sucuk_cad_v1", "sucuk_cad_v2", [("sucuk_kaseti_v1", "sucuk_kaseti_v2"), ("SUCUK_KASETI_v1", "SUCUK_KASETI_v2"), ("sucuk_v1", "sucuk_v2")])]

for eski, yeni, adlar in ISLER:
    s = io.open(os.path.join(U, eski + ".py"), encoding="utf-8").read(); n = 0
    for a, b in adlar: assert a in s, (eski, a); s = s.replace(a, b)
    def tek(desen, yerine, ad, bayrak=0):
        global s, n
        s2, k = re.subn(desen, lambda m_: yerine, s, count=1, flags=bayrak); assert k == 1, "%s: BULUNAMADI: %s" % (eski, ad); s = s2; n += 1
    tek(r"^import cadquery as cq\n", "import cadquery as cq\nimport kaset_birlesim_v1 as BR                                      # saplama · kulp · bayonet · contalar: dört kasette AYNI kod\n", "import", re.M)
    i = s.index('"""'); s = s[:i + 3] + "BİRLEŞİM DETAYLARI v1 (22 Eyl 2026) uygulandı — bkz. kaset_birlesim_v1.py: dişli saplama + pul + kör somun · kaynaklı kulp (saplama kulpa vidalanır) ·\nKLİKLİ bayonet (tırnak + tümsek + cep + O-ring yayı) · gövde contası · muylu O-ringleri · tüp O-ringi + M4 insert. Önceki sürüm: %s.py\n" % eski + s[i + 3:]
    m = re.search(r"tup = silz\(0, CY, (25\.0|RD), ZF - 2\.8, TUP_Z1\)", s); assert m, eski + ": tup gecmesi"
    s = s.replace(m.group(0), "tup = silz(0, CY, %s, ZF - 1.3, TUP_Z1)                # geçme 2,8 → 1,3: faturanın dibinde 1,7 mm O-ring yeri" % m.group(1), 1); n += 1
    tek(r"    for a in \(90\.0, 210\.0, 330\.0\):\n        (?:t = math\.radians\(a\); )?tup = tup\.union\([^\n]*240\.0\)\)\)\)\n",
        "    tup = BR.tirnak_ekle(tup, RT + 3.0, CY)                                                            # 3 bayonet TIRNAĞI (tüple tek parça)\n", "pim dongusu")
    tek(r"    kp = silz\(0, CY, .*?(?=    ekle\(\"yatak_kapagi\")", "    kp = BR.yatak_kapagi(RT, CY, TUP_Z1)                                                               # giriş → halka → tümsek → cep · O-ring kanalı\n", "kapak blogu", re.S)
    for a, b in (("3 bayonet pimi", "3 bayonet TIRNAĞI 8 × 4 × 3,2 (tüple tek parça) · plakaya geçme 1,3 + O-ring"),
                 ('"çeyrek tur · ön muyluyu', '"İT → 35° ÇEVİR → KLİK (tümsek 0,25 + cep + dayama · içindeki O-ring hem conta hem yay) · ön muyluyu'),
                 ("YATAK KAPAĞI|ÇEYREK TUR", "YATAK KAPAĞI|İT · 35° ÇEVİR · KLİK")):
        assert a in s, (eski, a); s = s.replace(a, b); n += 1
    assert s.count('ag(p["wp"])') == 2, eski; s = s.replace('ag(p["wp"])', "BR.web_ag(ag, p)"); n += 1                # küçük bağlantı elemanları web modelinde kaba ağ
    tek(r"\n\n\ndef makine\(\):", "\n    BR.uygula(globals())                                                                                 # birleşim detayları: dört kasette aynı\n\n\ndef makine():", "kap sonu")
    s = s.rstrip("\n") + "\n    sys.stdout.flush(); os._exit(0)                                     # OCC nesneleri kapanışta çöküyordu (exit 139): denetimler bittikten sonra doğrudan çık\n"
    io.open(os.path.join(U, yeni + ".py"), "w", encoding="utf-8").write(s); print("%s.py yazildi · %d yama" % (yeni, n))
