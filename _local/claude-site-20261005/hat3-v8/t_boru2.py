import sys, os, math
sys.path.insert(0, "h3"); sys.path.insert(0, ".")
import h3_elk_ortak as EO
pts = [(0,0,0),(0,0.3,0),(100,0.3,0),(100,50,0),(100,50,-40),(100.05,50,-40),(130,50,-40)]
s = EO.boru(pts, 3.0); print(type(s).__name__, round(s.Volume()), len(s.Solids()))
sys.stdout.flush(); os._exit(0)
