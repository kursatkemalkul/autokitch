import json,struct,sys
raw=open(sys.argv[1],'rb').read(); jl=struct.unpack('<I',raw[12:16])[0]; J=json.loads(raw[20:20+jl])
MEK=J['scenes'][0]['extras']['mekanizmalar']
print(len(MEK)); print([ (i,m) for i,m in enumerate(MEK) if 'B' in str(m)[:4] or 'ekmece' in str(m)])
print(len(J['nodes']))
for i,n in enumerate(J['nodes']):
  nm=n.get('name','')
  if nm.startswith('B') or 'CEK' in nm.upper():
    print(i,nm,'mesh' in n, {k:n[k] for k in ('translation','rotation','scale') if k in n}, n.get('children',[])[:5], json.dumps(n.get('extras',{}),ensure_ascii=False)[:200])
