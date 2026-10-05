# -*- coding: utf-8 -*-
"""hat_montaj_v85 → v86 (29 Eyl 2026 gece · YEREL · Codex v85 = E v11 üstüne). Yalnız ayrı kayıtlı montaj worktree'sinde çalıştır.
TOPPING (Kemal: "soğutma grubunu alta, sağ köşedekileri kaldır, o bölüm temiz boş · basamaklı yalıtımı kaldır, dikdörtgen · eşitlik isterim · temiz modelle"):
  · topping_uno_cad_v18: soğuk kutu DİKDÖRTGEN · K1 = K2 (mekanizma kanatlarıyla aynı derz) · evaporatör sağ üstte 400 (v17'nin yarıklı kapağıyla) · hatlar kaidedeki üniteye
  · topping_cad_v30: teknik cep KALKTI · Secop CU KLF6.6CND kaidede (arka-alt) · kanatların alt bandı ızgara (sol emiş + filtre / sağ atış) · teknik bölme · pano + UPS kuru bölmenin üstünde
  · kaide_cad_v4: C kaidesinde ünite cebi + hava pencereleri (A aynı)
  · ana hava hattı fırın üstünde arkaya (z −740), TOPPING'e kuru bölmeden girer (teknik cep yok)
  · denetim: kaide ↔ TOPPING'de "TC en alt ≥ 892" soğutma grubu cebi hariç + soğutma grubu ↔ çekmeceli dolap ayrı denetim (B tavanına ≥ 15)"""
import re
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / "hat_montaj_v85.py").read_text(encoding="utf-8-sig")


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:100], s.count(a), n)
    s = s.replace(a, b)


rep('"""hat_montaj_v83 (29 Eyl 2026 · YEREL · Codex v82 üstüne)',
    '"""hat_montaj_v86 (29 Eyl 2026 gece · YEREL · Codex v85 üstüne): TOPPING SOĞUTMA GRUBU KAİDEDE (TC v30 · Secop CU KLF6.6CND) · SOĞUK KUTU DİKDÖRTGEN + EŞİT KAPAKLAR (TU v18) · '
    'KAİDE v4 (ünite cebi + hava pencereleri) · ana hava hattı kuru bölmeye — yap_hat_montaj_v86.py\n'
    'hat_montaj_v85 (29 Eyl 2026 gece · Codex): E v11 vakumlu besleme + motorlu destek tablası\n'
    'hat_montaj_v84 (29 Eyl 2026 · Codex): E v10 tahrikli köşe / ön dil / kılavuzlu kapak katlama — yap_hat_montaj_v84.py\n'
    'hat_montaj_v83 (29 Eyl 2026 · YEREL · Codex v82 üstüne)')
rep("kaide_cad_v3 as KD      # v81: kaideler istasyon yüzleriyle aynı hiza", "kaide_cad_v4 as KD      # v86: C kaidesinde soğutma grubu cebi + hava pencereleri · v81: kaideler istasyon yüzleriyle aynı hiza")
rep("import topping_hesap_v7 as TH, topping_cad_v29 as TC", "import topping_hesap_v7 as TH, topping_cad_v30 as TC")
rep('"topping_uno_cad_v16.py (dünya y −168) + topping_cad_v29.py (yerel y + 892)"', '"topping_uno_cad_v18.py (dünya y −168) + topping_cad_v30.py (yerel y + 892)"')
rep('os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v16.py"))', 'os.path.join(os.path.dirname(os.path.abspath(__file__)), "topping_uno_cad_v18.py"))   # v86: dikdörtgen soğuk kutu + eşit kapaklar')
rep('print("v83 · TU topping_uno_cad_v16 modul denetimi %d / %d GECTI (den_assert zorunlu)"', 'print("v86 · TU topping_uno_cad_v18 modul denetimi %d / %d GECTI (den_assert zorunlu)"')
rep("ANA_V44 = [(3090, 1977, -380), (3090, 1977, -432), (1640, 1977, -432), (1640, 1977, -740), (1640, 1335, -740), (1650, 1335, -740)]",
    "ANA_V44 = [(3090, 1977, -380), (3090, 1977, -740), (1640, 1977, -740), (1640, 1335, -740), (1650, 1335, -740)]   # v86: fırın üstünde ARKAYA (z −740), TOPPING'e kuru bölmeden (teknik cep yok · TC v30 RAKOR_ANA)")
rep('_dis_birim(KD, "GERCEK_KAIDE", "kaide_cad_v3.py",', '_dis_birim(KD, "GERCEK_KAIDE", "kaide_cad_v4.py",')
rep('    _tc_alt = min(sh.BoundingBox().ymin for a_, sh in _TCT if a_.startswith("TOPPING:") and not a_.startswith("TOPPING:onyuz_"))   # v63: ön kapaklar kaide bandını örter',
    '    _tc_alt = min(sh.BoundingBox().ymin for a_, sh in _TCT if a_.startswith("TOPPING:") and not a_.startswith(("TOPPING:onyuz_", "TOPPING:sogutma_grubu")))   # v63: ön kapaklar kaide bandını örter · v86: soğutma grubu kaide cebinde\n'
    '    _CUG = [(a_, sh) for a_, sh in _TCT if a_.startswith("TOPPING:sogutma_grubu")]                                  # v86 · Secop CU KLF6.6CND + tepsi + askılar + cep perdesi\n'
    '    _c5 = _capraz(_CUG, [(a_, sb) for a_, sb in _SCP if _SCB[a_].ymax > Y_DUZ - 5.0 and _SCB[a_].xmin < X_BC + W_BC])\n'
    '    _cu_alt = min(sh.BoundingBox().ymin for _a, sh in _CUG) if _CUG else 9e9\n'
    '    print("v86 · SOGUTMA GRUBU (TC v30 · %d parca) kaide cebinde: en alt %.1f − dolap ustu %.0f = %.1f mm hava (>= 15) · cekmeceli dolapla kesisim %s  %s"\n'
    '          % (len(_CUG), _cu_alt, Y_DUZ, _cu_alt - Y_DUZ, "YOK" if not _c5 else "%d BULGU %s" % (len(_c5), _c5[:4]), _gk(bool(_CUG) and not _c5 and _cu_alt - Y_DUZ >= 15.0)))\n'
    '    assert _CUG and not _c5 and _cu_alt - Y_DUZ >= 15.0, "v86: soğutma grubu ↔ çekmeceli dolap"')
rep('print("KAIDE (kaide_cad_v3 · %d parca', 'print("KAIDE (kaide_cad_v4 · %d parca')
rep("Ø10 ana hat y 1809'da fırın üstünden TOPPING teknik cebine → kuru bölme → şartlandırıcı",
    "Ø10 ana hat y 1809'da fırın üstünde ARKADAN (z −740) TOPPING sağ yan sac rakorundan kuru bölmeye → dikine şartlandırıcıya (v86: teknik cep yok)")
s = s.replace("(topping_uno_cad_v16)", "(topping_uno_cad_v18)")
assert "hat_v86" not in s
s = s.replace("hat_v85", "hat_v86").replace("hat_montaj_v85.py", "hat_montaj_v86.py")
rep('pafta="HAT v85:', 'pafta="HAT v86 (29 Eyl gece · YEREL) · TOPPING: SOGUTMA GRUBU KAIDEDE (Secop CU KLF6.6CND, arka-alt, C kaidesi 3. goz · sol kanat alt bandi EMIS + filtre / sag kanat ATIS) · '
    'SAG UST TEKNIK CEP YOK · SOGUK KUTU DIKDORTGEN (648 L) + ESIT KAPAKLAR (K1 = K2 = kanatlar, derz 1597,75/1600,75) · EVAPORATOR SAG USTTE 400 (yarikli kapak) · PANO + UPS KURU BOLMENIN USTUNDE (ustten servis kapagi) · '
    'ANA HAVA HATTI KURU BOLMEYE (z −740) · KAIDE v4 · ACIK: Secop unite yonu / fan konumu sogutmaci firmayla, kaide pencere dayanimi (hesap 40 MPa) uretimde dogrulanacak. v85:')
compile(s, "hat_montaj_v86.py", "exec")
(U / "hat_montaj_v86.py").write_text(s, encoding="utf-8")
for name in ("makine.html", "index.html"):
    p = U.parent.parent / "otonom" / "hat" / name
    data = p.read_bytes()
    assert b"hat_v85" in data, name
    data = re.sub(rb"hat_v85\.(glb|usdz)\?v=85[\w-]*", rb"hat_v86.\1?v=86", data)
    assert b"hat_v85" not in data, name
    p.write_bytes(data)
print("v86 montaj üreteci yazıldı (Codex v85 üstüne · TOPPING TU v18 + TC v30 + kaide v4) · makine.html / index.html model bağlantısı v86")
