import json,numpy as np,struct,sys
from vox import S
PJ=json.load(open(S+r"\elk2\zj\m8_parca.json"))['parca']
raw=open(S+r"\hat3_v8zj.glb",'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
M=[m['kod'] for m in J['scenes'][0]['extras']['mekanizmalar']]
for i,q in enumerate(PJ):
    lo=np.array(q['lo']);hi=np.array(q['hi'])
    cross=[xf for xf in (1436,2500,4000,4400,5230) if lo[0]<xf-3 and hi[0]>xf+3]
    if cross and not q['ad'].startswith('ELK_ZINCIR') and not q['ad'].startswith(('B_','CEK','ZEMIN','INSAN','URUN','E_KUTU','B_MOD','U_')) and q['n']>0:
        if hi[1]>788 or q['ad'].startswith(('ELK','HAVA')):
            print(i,q['ad'],M[q['mek']],q['n'],cross,np.round(lo).astype(int).tolist(),np.round(hi).astype(int).tolist())
