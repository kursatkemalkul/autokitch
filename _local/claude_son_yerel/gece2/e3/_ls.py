import sys, os, numpy as np
sys.path.insert(0, os.path.join('..','cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g=G('../b4/51a/hat3_v9s.glb')
for i,m in enumerate(g.MEK): print(i,m if not isinstance(m,dict) else {k:v for k,v in m.items() if k in('kod','ad','ist','birim','tur')})
