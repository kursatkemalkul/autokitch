# -*- coding: utf-8 -*-
"""kutu_cad_v13 → v14 (30 Eyl 2026 · Claude): v13'ün tamamı + kutu_ek_v14.py eki (ağız üst kirişi kalkar · sağ ön dikey kablo kanalı tek parça).
v13 dosyası değişmez; v14 = v13 metni + ek (v10 → v11 → v12 → v13 yöntemiyle aynı)."""
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / "kutu_cad_v13.py").read_text(encoding="utf-8-sig")
assert "\nif __name__ == \"__main__\":" not in s, "v13 ana bloğu olmamalı"
ek = (U / "kutu_ek_v14.py").read_text(encoding="utf-8")
s = "# -*- coding: utf-8 -*-\n# kutu_cad_v14.py — yap_kutu_cad_v14.py üretir: kutu_cad_v13.py + kutu_ek_v14.py (30 Eyl 2026 · Claude · ağız üst kirişi kalktı · dikey kablo kanalı tek parça)\n" + s + "\n" + ek
compile(s, "kutu_cad_v14.py", "exec")
(U / "kutu_cad_v14.py").write_text(s, encoding="utf-8")
print("kutu_cad_v14.py yazıldı (v13 + kutu_ek_v14)")
