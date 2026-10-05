# -*- coding: utf-8 -*-
import sys, os, pickle
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'adim6')); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim as Y
P = pickle.load(open('parca.pkl', 'rb'))
ads = list(P)
r = Y.son_kesisim(P, ads, eps=3e-4)
for k, v in sorted(r.items()): print(k, v)
