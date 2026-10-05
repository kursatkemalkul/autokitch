# -*- coding: utf-8 -*-
import re
p = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat\mekanizma-v3.js"
s = open(p, encoding="utf-8").read()
a = "ids.length + ' mekanizma</small>'"
assert a in s
s = s.replace(a, "ids.length + (DISIPLIN ? ' ünite' : ' mekanizma') + '</small>'")
L = s.split("\n")
i = [k for k, x in enumerate(L) if "s.append(el('h3', null, '" in x][0]
L[i] = re.sub(r"el\('h3', null, ('[^']*')\)", r"el('h3', null, DISIPLIN ? 'Montaj ağacı · istasyon → ünite' : \1)", L[i])
open(p, "w", encoding="utf-8").write("\n".join(L)); print(L[i].strip())
h = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat\makine_v3_8.html"
t = open(h, encoding="utf-8").read()
n0 = len(t)
t = t.replace("hat3_v8.glb?v=8za", "hat3_v8.glb?v=8zb")
t = re.sub(r'  <div class="zc" id="kat-cubuk">.*?</div>\n', "", t, flags=re.S)
t = t.replace('<script src="kategori.js?v=2"></script>', "")
t = t.replace('<script src="mekanizma-v3.js?v=4"></script>',
              "<script>window.MEK3_JSON = '../hat3d/v3/mekanizma_v3_8.json?v=8zb'; window.MEK3_DISIPLIN = true;</script><script src=\"mekanizma-v3.js?v=5\"></script>")
assert "8zb" in t and "kategori.js" not in t and "kat-cubuk" not in t and "mekanizma-v3.js?v=5" in t
open(h, "w", encoding="utf-8").write(t); print("html", n0, "->", len(t))
