# -*- coding: utf-8 -*-
"""v8za ↔ v8zb: geometri (BIN + JSON'un extras dışı) birebir mi; her üçgen tek mek + tek kat mı; kpk aynı mı."""
import json,struct,sys,copy
def oku(y):
    raw=open(y,'rb').read();jl=struct.unpack('<I',raw[12:16])[0];J=json.loads(raw[20:20+jl]);bo=20+jl
    bl=struct.unpack('<I',raw[bo:bo+4])[0];return J,raw[bo+8:bo+8+bl]
A,BA=oku(sys.argv[1]);B,BB=oku(sys.argv[2])
print('BIN ayni:',BA==BB,len(BA))
def sade(J):
    J=copy.deepcopy(J);J['scenes'][0].pop('extras',None)
    for m in J['meshes']:
        for p in m['primitives']:
            e=p.get('extras',{});e.pop('mek',None);e.pop('kat',None)
    return J
print('JSON (etiket disi) ayni:',sade(A)==sade(B))
nm=len(B['scenes'][0]['extras']['mekanizmalar']);nk=len(B['scenes'][0]['extras']['kategoriler'])
hata=0;tot=0;kpk=0
for ma,mb in zip(A['meshes'],B['meshes']):
    for pa,pb in zip(ma['primitives'],mb['primitives']):
        n=B['accessors'][pb['indices']]['count'];tot+=n
        if pa.get('extras',{}).get('kpk')!=pb.get('extras',{}).get('kpk'): kpk+=1
        for key,lim in(('mek',nm),('kat',nk)):
            L=pb['extras'][key];pos=0
            for i in range(0,len(L),3):
                if L[i+1]!=pos or L[i+2]<=0 or L[i+2]%3 or not(0<=L[i]<lim): hata+=1
                pos+=L[i+2]
            if pos!=n: hata+=1
print('indis toplami',tot,'(ucgen',tot//3,') · etiket hatasi',hata,'· kpk farki',kpk)
