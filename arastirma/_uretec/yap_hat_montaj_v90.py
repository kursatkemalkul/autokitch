# -*- coding: utf-8 -*-
"""hat_montaj_v89 → v90 (30 Eyl 2026 · Claude · base b524dae = v89 4bde308 + E v14). Yalnız kayıtlı montaj worktree'sinde çalıştır.
Kemal (30 Eyl, ekran görüntüsü): "bu neden kesik yarım ve oradaki yatay parça havada"
1 · E v14: ağız üst kirişi kalktı (taşıdığı parça yoktu; yalnız saydam ön dikmelere değdiği için havada görünüyordu) · sağ ön dikey kablo kanalı tek parça
    (eski kiriş geçişinden kalan 20 mm boş kesik kalktı) · E kinematiği v13 ile birebir
2 · sayfa bağlantıları v89 → v90 (yalnız model bağlantısı + sürüm etiketleri)"""
import re
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / "hat_montaj_v89.py").read_text(encoding="utf-8-sig")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:110], s.count(a), n)
    s = s.replace(a, b)


# ---------------------------------------------------------------- 0 · başlık + sürüm ----------------------------------------------------------------
rep('"""hat_montaj_v89 (30 Eyl 2026 · Claude · base 34f362b)',
    '"""hat_montaj_v90 (30 Eyl 2026 · Claude · base b524dae): E v14 — AĞIZ ÜST KİRİŞİ KALKTI (hiçbir şey taşımıyordu, saydam ön dikmelere asılı havada görünüyordu) +\n'
    'SAĞ ÖN DİKEY KABLO KANALI TEK PARÇA (eski kiriş geçişinden kalan boş kesik) — yap_hat_montaj_v90.py\n'
    'hat_montaj_v89 (30 Eyl 2026 · Claude · base 34f362b)')
rep('pafta="HAT v89 (30 Eyl · Claude · YEREL)',
    'pafta="HAT v90 (30 Eyl · Claude · YEREL): E v14 AGIZ UST KIRISI KALKTI (HAVADA GORUNUYORDU) + SAG ON DIKEY KABLO KANALI TEK PARCA; HAT 5230 · v89 (30 Eyl · Claude · YEREL)')

# ---------------------------------------------------------------- 1 · E v14 ----------------------------------------------------------------
rep("import kutu_cad_v13 as KC ", "import kutu_cad_v14 as KC ")
rep('"v88: E v13 saati v12\'den farkli (K v9 saat bagi v12\'ye kurulu)"', '"v88/v90: E v14 saati v12\'den farkli (K v9 saat bagi v12\'ye kurulu)"')
rep('"sac", "kutu_cad_v13.py", "hat/pack.html")', '"sac", "kutu_cad_v14.py", "hat/pack.html")')
rep('("E_GOVDE", "KUTU modülü gövdesi: 304 kabuk (saydam) · ayaklar · taban · ağız kirişi · şarjör yan kapısı · üst ön kapak · alt önü AÇIK (v58: ön alt sac kalktı)", '
    '("ayak_", "taban_sac", "plint_on", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "sarjor_yan_kapisi", "on_ust_kapak", "agiz_ust_kirisi", "kose_dikme_", "onyuz_")),',
    '("E_GOVDE", "KUTU modülü gövdesi: 304 kabuk (saydam) · ayaklar · taban · şarjör yan kapısı · ön çerçeve + kapaklar · alt önü AÇIK (v58: ön alt sac kalktı) · v90: ağız üst kirişi kalktı", '
    '("ayak_", "taban_sac", "plint_on", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "sarjor_yan_kapisi", "on_ust_kapak", "kose_dikme_", "onyuz_")),')
assert "kutu_cad_v13" not in s, [l for l in s.splitlines() if "kutu_cad_v13" in l][:3]

# ---------------------------------------------------------------- 2 · çıktı adları ----------------------------------------------------------------
n_ = s.count('os.path.join(OUT, "hat_v89.glb")') + s.count('os.path.join(OUT, "hat_v89.usdz")')
assert n_ == 2, n_
s = s.replace('os.path.join(OUT, "hat_v89.glb")', 'os.path.join(OUT, "hat_v90.glb")').replace('os.path.join(OUT, "hat_v89.usdz")', 'os.path.join(OUT, "hat_v90.usdz")')
rep('"hat_v89", _usd', '"hat_v90", _usd')
rep('print("hat_v89.glb · %d dugum', 'print("hat_v90.glb · %d dugum')
rep('print("hat_v89.usdz · %.0f KB', 'print("hat_v90.usdz · %.0f KB')
assert "hat_v89." not in s.replace("hat_v89.py", ""), [l for l in s.splitlines() if "hat_v89." in l][:3]

compile(s, "hat_montaj_v90.py", "exec")
(U / "hat_montaj_v90.py").write_text(s, encoding="utf-8")

# ---------------------------------------------------------------- 3 · sayfa: model bağlantısı + sürüm etiketleri (haber kartları / metinler dokunulmaz) ----------------------------------------------------------------
H = U.parent.parent / "otonom" / "hat"
for name, ciftler in (("makine.html", (("1862 · montaj v89</span>", "1862 · montaj v90</span>"), ("1862 mm (montaj v89 ·", "1862 mm (montaj v90 ·"))),
                      ("index.html", (("GERÇEK ÜRETİM MODELİ (montaj v89 ·", "GERÇEK ÜRETİM MODELİ (montaj v90 ·"), ("186 (v89)", "186 (v90)"),
                                      ("· 30 Eyl 2026 · montaj v89 · dükkân v15", "· 30 Eyl 2026 · montaj v90 · dükkân v15")))):
    p = H / name
    with open(p, encoding="utf-8", newline="") as f_:                    # satır sonları olduğu gibi kalır (CRLF / LF)
        t = f_.read()
    t = re.sub(r"hat_v89\.(glb|usdz)\?v=89[\w-]*", r"hat_v90.\1?v=90", t)
    for a, b in ciftler:
        assert t.count(a) == 1, (name, a, t.count(a))
        t = t.replace(a, b)
    assert "hat_v89" not in t, name
    with open(p, "w", encoding="utf-8", newline="") as f_:
        f_.write(t)
print("v90 montaj üreteci yazıldı (v89 + E v14) · makine.html / index.html model bağlantısı + sürüm etiketleri v90")
