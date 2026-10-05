# -*- coding: utf-8 -*-
"""kutu_cad_v12 → v13 (30 Eyl 2026 · Claude): v12'nin tamamı + kutu_zaman_v13.py eki (sıfır sensörleri · kafa freni · 13 eksen hareket denetimi).
v12 dosyası değişmez; v13 = v12 metni + ek (v10 → v11 → v12 yöntemiyle aynı)."""
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / "kutu_cad_v12.py").read_text(encoding="utf-8-sig")
assert "\nif __name__ == \"__main__\":" not in s, "v12 ana bloğu olmamalı"
ek = (U / "kutu_zaman_v13.py").read_text(encoding="utf-8")
s = "# -*- coding: utf-8 -*-\n# kutu_cad_v13.py — yap_kutu_cad_v13.py üretir: kutu_cad_v12.py + kutu_zaman_v13.py (30 Eyl 2026 · Claude · sıfır sensörleri · fren · 13 eksen denetim)\n" + s + "\n" + ek
compile(s, "kutu_cad_v13.py", "exec")
(U / "kutu_cad_v13.py").write_text(s, encoding="utf-8")
print("kutu_cad_v13.py yazıldı (v12 + kutu_zaman_v13)")
