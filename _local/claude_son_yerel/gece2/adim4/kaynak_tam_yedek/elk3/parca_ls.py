import json,numpy as np,struct,sys,re
from vox import S
PJ=json.load(open(S+r"\elk2\zj\m8_parca.json"))['parca']
raw=open(S+r"\hat3_v8zj.glb",'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
M=[m['kod'] for m in J['scenes'][0]['extras']['mekanizmalar']]
pat=re.compile(sys.argv[1]); mp=re.compile(sys.argv[2]) if len(sys.argv)>2 else None
lo0=np.array([float(v) for v in sys.argv[3].split(',')]) if len(sys.argv)>3 else None
hi0=np.array([float(v) for v in sys.argv[4].split(',')]) if len(sys.argv)>4 else None
for i,q in enumerate(PJ):
    if not pat.search(q['ad']): continue
    if mp and not mp.search(M[q['mek']]): continue
    lo=np.array(q['lo']);hi=np.array(q['hi'])
    if lo0 is not None and not (np.all(hi>=lo0) and np.all(lo<=hi0)): continue
    print(i,q['ad'],M[q['mek']],q['kat'],q['n'],np.round(lo).astype(int).tolist(),np.round(hi).astype(int).tolist())
