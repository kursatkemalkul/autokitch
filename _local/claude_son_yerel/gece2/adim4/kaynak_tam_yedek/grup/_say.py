import json,struct,sys,collections
raw=open(sys.argv[1],'rb').read();jl=struct.unpack('<I',raw[12:16])[0];J=json.loads(raw[20:20+jl])
ex=J['scenes'][0]['extras'];MEK=[m['kod'] for m in ex['mekanizmalar']];KAT=[k['kod'] for k in ex['kategoriler']]
cm=collections.Counter();ck=collections.Counter();tot=0;lab=0;nodes=collections.defaultdict(set);bad=0
for nd in J['nodes']:
  if 'mesh' not in nd: continue
  for p in J['meshes'][nd['mesh']]['primitives']:
    n=J['accessors'][p['indices']]['count'];tot+=n
    e=p.get('extras',{});
    for key,c in(('mek',cm),('kat',ck)):
      L=e.get(key) or [];s=0;pos=0
      for k in range(0,len(L),3):
        if L[k+1]!=pos: bad+=1
        pos=L[k+1]+L[k+2]; c[L[k]]+=L[k+2]//3; s+=L[k+2]
        if key=='mek': nodes[L[k]].add(nd['name'].split('__')[0])
      if s!=n: print('EKSIK',key,nd['name'],s,n)
print('toplam ucgen',tot//3,'bad',bad)
for i,m in enumerate(MEK): print(i,m,cm[i],sorted(nodes[i])[:8])
for i,k in enumerate(KAT): print(k,ck[i])
print('-1',cm[-1],ck[-1])
