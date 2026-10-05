# -*- coding: utf-8 -*-
"""Oturum dökümlerinden (ana + alt ajanlar) hat3_v8*.glb üreten/kullanan kabuk komutlarını zaman sırasıyla çıkarır."""
import json, glob, os, re, sys
P = r"C:\Users\Kemal\.claude\projects\C--Users-Kemal-Desktop-Kemal-WEBS-TE"
dosyalar = [os.path.join(P, "f3ef876a-f062-4b29-bb81-775cc8a1a6d8.jsonl")] + glob.glob(os.path.join(P, "f3ef876a-f062-4b29-bb81-775cc8a1a6d8", "subagents", "*.jsonl"))
dosyalar += [os.path.join(P, "e013e9e1-4e00-415e-a853-d8b298706959.jsonl")]
desen = re.compile(sys.argv[1] if len(sys.argv) > 1 else r"hat3_v8[a-z0-9_]*\.glb")
out = []
for f in dosyalar:
    ag = os.path.basename(f)[:20]
    for line in open(f, encoding="utf-8", errors="replace"):
        try: d = json.loads(line)
        except Exception: continue
        if d.get("type") != "assistant": continue
        ts = d.get("timestamp", "")
        for c in (d.get("message", {}).get("content") or []):
            if not isinstance(c, dict) or c.get("type") != "tool_use": continue
            inp = c.get("input", {})
            cmd = inp.get("command") or ""
            if c.get("name") in ("Write", "Edit"): continue
            if cmd and desen.search(cmd) and re.search(r"python|bash|\.sh|cp |copy|Copy-Item|mv ", cmd):
                out.append((ts, ag, cmd.replace("\n", " ⏎ ")[:700]))
out.sort()
for t, a, c in out:
    print(t[5:19], a, "|", c)
