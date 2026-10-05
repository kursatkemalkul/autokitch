# -*- coding: utf-8 -*-
"""Kalem 7b · çekmece / kapak önü kutu süpürmesi (kaba): python d7b_cekmece.py [cak/meta.json]
her CEK_* / B_DEPO CEKMECE birimi + bütün kpk ön kapaklar: ön yüz kutusu z +79 → +79+700 (çekmece) / kapak genişliği kadar (kapak açılma alanı, dikey menteşe kaba)
bölgesine giren, makine ön düzleminin ÖNÜNDE (lo_z > 79,5) duran başka bileşenler (aynı birim / ACIL_STOP kendi mantarı hariç)."""
import sys, json, re, numpy as np
from collections import defaultdict
M = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "cak/meta.json", encoding="utf-8"))["bil"]
on = [b for b in M if b["lo"][2] > 79.5 and not b["dugum"].startswith(("TEZGAH", "DUZ_TEZGAH", "ELK_ZEMIN", "URUN", "INSAN", "ROBOT"))]
print("makine ön düzleminin önünde duran bileşen:", len(on), "· düğümler:", sorted(set(b["dugum"].split("__")[0] for b in on)))
grp = defaultdict(list)
for b in M:
    if b["dugum"].startswith("CEK_") or ("CEKMECE" in b["dugum"] and b["dugum"].startswith("B_DEPO")): grp[b["dugum"].split("__")[0] + ("_DEPO" if "DEPO" in b["dugum"] else "")].append(b)
bul = 0
for g, L in sorted(grp.items()):
    lo = np.min([b["lo"] for b in L], 0); hi = np.max([b["hi"] for b in L], 0)
    s_lo = np.array([lo[0], lo[1], 79.5]); s_hi = np.array([hi[0], hi[1], hi[2] + 700])
    hit = [b for b in on if not b["dugum"].startswith(g.split("_DEPO")[0]) and (np.array(b["lo"]) <= s_hi).all() and (np.array(b["hi"]) >= s_lo).all()]
    hit = [b for b in hit if not (b["dugum"].startswith("ACIL_STOP") and lo[0] - 1 <= b["lo"][0] and b["hi"][0] <= hi[0] + 1 and lo[1] - 1 <= b["lo"][1] and b["hi"][1] <= hi[1] + 1)]
    if hit:
        bul += 1
        z0 = min(b["lo"][2] for b in hit)
        print("  %-22s x %.0f–%.0f y %.0f–%.0f · ön %.0f → 700 mm çekmede engel (ilk engel z %.0f → strok ≈ %.0f mm): %s" % (g, lo[0], hi[0], lo[1], hi[1], hi[2], z0, z0 - hi[2],
              sorted(set("%s %s" % (b["dugum"], b["ad"] or "") for b in hit))[:5]))
print("çekmece birimi", len(grp), "· engelli", bul)
