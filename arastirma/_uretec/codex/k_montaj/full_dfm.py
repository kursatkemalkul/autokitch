from pathlib import Path
import os,sys,json,gzip,hashlib,collections
ROOT=Path(__file__).resolve().parents[4]
U=ROOT/'arastirma/_uretec'; H=U/'h3'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
os.environ['AUTOKITCH_SAC_STANDART']=str(H/'yama_v9/sac_standart')
for p in (U,H): sys.path.insert(0,str(p))
import h3_k_sac_v1 as K
import h3_sac_v1 as S
OUT=ROOT/'_local/codex_k_montaj';OUT.mkdir(parents=True,exist_ok=True)
def clean(v):
 if isinstance(v,dict):return {k:clean(x) for k,x in v.items() if k not in ('sh','wp','yuz','M','D','cut')}
 if isinstance(v,(tuple,list)):return [clean(x) for x in v]
 if hasattr(v,'tolist'):return v.tolist()
 if isinstance(v,(str,int,float,bool)) or v is None:return v
 return str(v)
g=K.kur(); report={'source_step':61,'source_commit':'cb7d1ecf59b2be6b30f65e3006aadfe2b01b1a1d','source_sha256':'948b20c4520cf917711a8dea730ea037379793b11bb6e975c649155c83ef9c1d','manufacturing_release':False,'sheets':[],'joins':clean(g.BIRLESIM),'profiles':[],'hardware':[],'interfaces':clean(g.ARAYUZ),'notes':clean(g.NOT)}
for i,s in enumerate(g.SAC):
 a=s.acinim(); dfm=s.dfm(abkant=True)
 report['sheets'].append({'name':s.ad,'flat':a,'dfm':clean(dfm)})
 print('SHEET',i+1,len(g.SAC),s.ad,'bends',len(s.bukumler),flush=True)
for p in g.PROFIL:report['profiles'].append(clean(vars(p)))
for p in g.ELEMAN:report['hardware'].append(clean(p))
(OUT/'source_cad_full_dfm.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('COUNTS',len(g.SAC),len(g.PROFIL),len(g.ELEMAN),len(g.KAYNAK),len(g.BIRLESIM),flush=True)
print('DFM',json.dumps([(s['name'],s['dfm']) for s in report['sheets'] if any(x.get('durum')!='GEÇTİ' for x in s['dfm'])],ensure_ascii=False)[:15000],flush=True)
sys.stdout.flush();os._exit(0)
