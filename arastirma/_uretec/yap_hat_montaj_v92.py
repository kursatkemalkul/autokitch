# -*- coding: utf-8 -*-
"""hat_montaj_v91 → v92 (30 Eyl 2026 · Claude · base = claude-topping-v32 = v91 20f7ac6 + TOPPING v32). Yalnız kayıtlı montaj worktree'sinde çalıştır.
Kemal 30 Eyl: "bu rayın üstü kapanmalı, arasına hamur sos küp sucuk girmemeli" → "paslanmaz örtü bandı yap / yap işte ya doğru olanları hadi"
1 · C: topping_cad_v32 — alçak kızak HIWIN MGN15H (H 16) + KAPALI paslanmaz ray çatısı (üstte yarık yok) + çatının altından yandan dolanan kızak ayakları
    (ters kap labirent) · tabla / disk / aktarma kotu aynı · raylar −540…1793,5 · uç kapakları · dönüş motoru plakaya oturdu
2 · sayfa: model bağlantısı + sürüm etiketleri v92 (başka metin yok — yalnız ana 3B)"""
import re
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / "hat_montaj_v91.py").read_text(encoding="utf-8-sig")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:120], s.count(a), n)
    s = s.replace(a, b)


# ---------------------------------------------------------------- 0 · başlık + sürüm
rep('"""hat_montaj_v91 (30 Eyl 2026 · Claude · base 4027c2e)',
    '"""hat_montaj_v92 (30 Eyl 2026 · Claude · base = topping v32 üstü v91): TOPPING RAYININ ÜSTÜ TAMAMEN KAPALI — alçak kızak MGN15H + kapalı paslanmaz ray çatısı +\n'
    'yandan dolanan kızak ayakları (topping_cad_v32) — yap_hat_montaj_v92.py\n'
    'hat_montaj_v91 (30 Eyl 2026 · Claude · base 4027c2e)')
rep('pafta="HAT v91 (30 Eyl · Claude · YEREL)',
    'pafta="HAT v92 (30 Eyl · Claude · YEREL): TOPPING RAY USTU KAPALI (MGN15H alcak kizak + kapali paslanmaz cati + yandan dolanan kizak ayaklari, tabla kotu ayni); HAT 5230 · v91 (30 Eyl · Claude · YEREL)')
rep('"generator": "AUTOKITCH hat_montaj_v91"', '"generator": "AUTOKITCH hat_montaj_v92"')

# ---------------------------------------------------------------- 1 · TOPPING v32
n_ = s.count("topping_cad_v31"); assert n_ == 2, n_
s = s.replace("topping_cad_v31", "topping_cad_v32")

# ---------------------------------------------------------------- 2 · GÖVDEDEKİ MENTEŞE YARISI + KİLİT OPAK (Kemal: "bu ikisi sonuçta ayrı istasyon, kapakları ayrı olsun, tek kapak sola
#     tek kapak sağa, ona göre gövdelerinde yerleri olsun") — kapaklar zaten istasyon başına ayrı (A tek kapak sola · TOPPING sol yarı sola, sağ yarı sağa, menteşeler kendi
#     gövdesinde) ama gövdeye vidalı menteşe yarıları ve basmalı kilitler kapakla birlikte saydam sayılıyordu → "görünmez" modda hangi kapağın nereden açıldığı görünmüyordu
rep('ON_CERCEVE = _re61.compile(r"(cerceve(?!_saci)|dikme|kayit|kusak|plint|dayama|lama|mentese_tabani|kilavuz|emniyet_sensoru|isik_perdesi)")',
    'ON_CERCEVE = _re61.compile(r"(cerceve(?!_saci)|dikme|kayit|kusak|plint|dayama|lama|mentese_tabani|kilavuz|emniyet_sensoru|isik_perdesi|'
    'mentese_\\d+_sabit|mentese_sabit|mentese_\\d+_taban|basac(?!_K\\d)|panel_tutucu)")   # v92: gövdedeki menteşe yarısı, basmalı kilit, panel tutucusu da opak · TOPPING soğuk dolap K1/K2 kilidi saydam yüz sacına bağlı, kapakla saydam kalır')

# ---------------------------------------------------------------- 2 · çıktı adları
n_ = s.count("hat_v91.glb") + s.count("hat_v91.usdz"); assert n_ == 6, n_
s = s.replace("hat_v91.glb", "hat_v92.glb").replace("hat_v91.usdz", "hat_v92.usdz")
rep('"hat_v91", _usd', '"hat_v92", _usd')
assert "hat_v91." not in s.replace("hat_v91.py", ""), [l for l in s.splitlines() if "hat_v91." in l][:3]
assert "topping_cad_v31" not in s

compile(s, "hat_montaj_v92.py", "exec")
(U / "hat_montaj_v92.py").write_text(s, encoding="utf-8")

# ---------------------------------------------------------------- 3 · sayfa (yalnız model bağlantısı + sürüm etiketi)
H = U.parent.parent / "otonom" / "hat"
for name, ciftler in (("makine.html", (("1862 · montaj v91</span>", "1862 · montaj v92</span>"), ("1862 mm (montaj v91 ·", "1862 mm (montaj v92 ·"),
                                       ("parca_kutulari.json?v=88", "parca_kutulari.json?v=92"), ("durum.json?v=88", "durum.json?v=92"))),     # v92: veri dosyaları da tazelenir (v88'den beri aynı)
                      ("index.html", (("GERÇEK ÜRETİM MODELİ (montaj v91 ·", "GERÇEK ÜRETİM MODELİ (montaj v92 ·"), ("186 (v91)", "186 (v92)"),
                                      ("· 30 Eyl 2026 · montaj v91 · dükkân v15", "· 30 Eyl 2026 · montaj v92 · dükkân v15"), ("parca_kutulari.json?v=88", "parca_kutulari.json?v=92")))):
    p = H / name
    with open(p, encoding="utf-8", newline="") as f_:
        t = f_.read()
    if "hat_v92" in t:
        continue                                                                         # sayfa zaten v92 (ikinci çalıştırma)
    crlf = "\r\n" in t
    n_ = len(re.findall(r"hat_v91\.(glb|usdz)\?v=91[\w-]*", t)); assert n_ >= 1, (name, n_)
    t = re.sub(r"hat_v91\.(glb|usdz)\?v=91[\w-]*", r"hat_v92.\1?v=92", t)
    for a, b in ciftler:
        a2, b2 = (a.replace("\n", "\r\n"), b.replace("\n", "\r\n")) if crlf else (a, b)
        assert t.count(a2) == 1, (name, a[:60], t.count(a2))
        t = t.replace(a2, b2)
    assert "hat_v91" not in t, name
    with open(p, "w", encoding="utf-8", newline="") as f_:
        f_.write(t)
print("v92 montaj üreteci yazıldı (v91 + TOPPING v32: ray üstü kapalı) · makine.html / index.html v92")
