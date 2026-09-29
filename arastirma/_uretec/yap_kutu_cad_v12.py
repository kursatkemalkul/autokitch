# -*- coding: utf-8 -*-
"""kutu_cad_v11 → v12 (30 Eyl 2026 · Claude): v11'in tamamı + kutu_zaman_v12.py eki (gerçek süreler · kafa inişi 2,20 · BOM karşılıkları).
v11 dosyası değişmez; v12 = v11 metni + ek (Codex'in v10 → v11 yöntemiyle aynı)."""
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / "kutu_cad_v11.py").read_text(encoding="utf-8-sig")
assert "\nif __name__ == \"__main__\":" not in s, "v11 ana bloğu olmamalı"
ek = (U / "kutu_zaman_v12.py").read_text(encoding="utf-8")
s = "# -*- coding: utf-8 -*-\n# kutu_cad_v12.py — yap_kutu_cad_v12.py üretir: kutu_cad_v11.py + kutu_zaman_v12.py (30 Eyl 2026 · Claude · E GERÇEK SÜRELER)\n" + s + "\n" + ek
compile(s, "kutu_cad_v12.py", "exec")
(U / "kutu_cad_v12.py").write_text(s, encoding="utf-8")
print("kutu_cad_v12.py yazıldı (v11 + kutu_zaman_v12)")
