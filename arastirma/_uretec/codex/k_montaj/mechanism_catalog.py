"""Read original K mechanism definitions; geometry remains source61-authoritative."""
import sys
sys.dont_write_bytecode=True
exec(open(__file__.replace('mechanism_catalog.py','inspect_source.py'),encoding='utf-8-sig').read().split('g=K.kur();')[0])
native=Path('C:/Users/Kemal/AppData/Local/Temp/claude/C--Users-Kemal-Desktop-Kemal-WEBS-TE/f3ef876a-f062-4b29-bb81-775cc8a1a6d8/scratchpad/b3/arastirma/_uretec')
assert native.is_dir()
sys.path.append(str(native))
import h3_kesme_v1 as KS
KS.modul()
records=[]
for p in KS.PARCALAR:
 sh=KS._tek(p['wp']);b=sh.BoundingBox()
 records.append({'name':p['ad'],'material':p['mal'],'group':p.get('grup'),
                 'lo':[b.xmin+4000,b.ymin,b.zmin],'hi':[b.xmax+4000,b.ymax,b.zmax],
                 'bom':clean(p.get('bom')),'source_definition':'original K adapter, requires final source matching'})
(OUT/'mechanism_catalog.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
print('MECHANISM_PARTS',len(records),flush=True)
sys.stdout.flush();os._exit(0)
