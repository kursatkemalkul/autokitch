# -*- coding: utf-8 -*-
"""Döküm komutlarından 'python betik ... giris.glb ... cikis.glb' ve cp/mv/sikistir satırlarını ayıklar (yerel saat = UTC+2)."""
import json, glob, os, re, sys, datetime
P = r"C:\Users\Kemal\.claude\projects\C--Users-Kemal-Desktop-Kemal-WEBS-TE"
dosyalar = [os.path.join(P, "f3ef876a-f062-4b29-bb81-775cc8a1a6d8.jsonl")] + glob.glob(os.path.join(P, "f3ef876a-f062-4b29-bb81-775cc8a1a6d8", "subagents", "*.jsonl"))
GLB = r"[^\s'\";|&]*hat3_v8[a-z0-9_]*\.glb|[^\s'\";|&]*\b(?:e\d|t\d|p\d|a\d|w\d|y\d|z\d|za1|v8x_[abc])\.glb"
out = []
for f in dosyalar:
    ag = os.path.basename(f).replace("agent-", "")[:8]
    for line in open(f, encoding="utf-8", errors="replace"):
        try: d = json.loads(line)
        except Exception: continue
        if d.get("type") != "assistant": continue
        ts = d.get("timestamp", "")
        try: t = (datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")) + datetime.timedelta(hours=2)).strftime("%m-%d %H:%M:%S")
        except Exception: t = ts
        for c in (d.get("message", {}).get("content") or []):
            if not isinstance(c, dict) or c.get("type") != "tool_use": continue
            cmd = (c.get("input", {}) or {}).get("command") or ""
            for seg in re.split(r"&&|;|\n|\|\|", cmd):
                s = seg.strip()
                if re.search(r"\bpython[3]?\s+(-u\s+)?[^\s-][^\s]*\.py", s) or re.match(r"(cp|mv|bash)\s", s):
                    gl = re.findall(GLB, s)
                    if len(gl) >= 1 and (re.match(r"(cp|mv)\s", s) or len(gl) >= 2 or "sikistir" in s or "b4.py" in s or "b5run" in s or "zincir" in s):
                        out.append((t, ag, s[:400]))
                    elif re.match(r"bash\s", s) and ("zincir" in s or "run" in s):
                        out.append((t, ag, s[:400]))
out.sort()
for t, a, c in out:
    print(t, a, "|", c)
