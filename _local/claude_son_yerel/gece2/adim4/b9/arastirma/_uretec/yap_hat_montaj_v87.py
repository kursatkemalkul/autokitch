# -*- coding: utf-8 -*-
"""hat_montaj_v86 → v87 (30 Eyl 2026 gece · YEREL · v86 b1fb5c9 üstüne). Yalnız ayrı kayıtlı montaj worktree'sinde çalıştır.
Codex K400 v7 (kesme_cad_v7, commit 524daa2) ana montaja: Codex'in hazırladığı _local/k400-v7/promote.py yaması aynen uygulanır
(W_K 400 · X_E 4400 · HAT 5230 · bulaşık K'dan kalkar (Kemal onayı) · E saati KS.e_time), üstüne yalnız sürüm metni + sayfa bağlantısı."""
import importlib.util, re
from pathlib import Path
U = Path(__file__).resolve().parent
_sp = importlib.util.spec_from_file_location("k400_promote", U.parent.parent / "_local" / "k400-v7" / "promote.py")
PR = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(PR)
s = PR.build((U / "hat_montaj_v86.py").read_text(encoding="utf-8-sig"))


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:100], s.count(a), n)
    s = s.replace(a, b)


rep('"""hat_montaj_v86 (29 Eyl 2026 gece · YEREL · Codex v85 üstüne)',
    '"""hat_montaj_v87 (30 Eyl 2026 · YEREL · v86 b1fb5c9 üstüne): Codex K400 v7 — kısa düz itici, bulaşık K\'dan kalktı (Kemal onayı), HAT 5230 — yap_hat_montaj_v87.py (_local/k400-v7/promote.py)\n'
    'hat_montaj_v86 (29 Eyl 2026 gece · YEREL · Codex v85 üstüne)')
rep('pafta="HAT v86 (29 Eyl gece · YEREL)', 'pafta="HAT v87 (30 Eyl · YEREL): K400 KISA DUZ ITICI (Codex kesme_cad_v7) + BULASIK K\'DAN KALKTI + HAT 5230; VANTUZLU E11 KORUNDU; K KINEMATIK PROTOTIP. v86 (29 Eyl gece · YEREL)')
assert "hat_v86" not in s and "hat_v85" not in s
compile(s, "hat_montaj_v87.py", "exec")
(U / "hat_montaj_v87.py").write_text(s, encoding="utf-8")
for name in ("makine.html", "index.html"):
    p = U.parent.parent / "otonom" / "hat" / name
    data = p.read_bytes()
    assert b"hat_v86" in data, name
    data = re.sub(rb"hat_v86\.(glb|usdz)\?v=86[\w-]*", rb"hat_v87.\1?v=87", data)
    assert b"hat_v86" not in data, name
    p.write_bytes(data)
print("v87 montaj üreteci yazıldı (v86 + Codex K400 v7) · makine.html / index.html model bağlantısı v87")
