"""Read-only v69 source adapter. Private cache; never writes the primary checkout."""
import os, sys, types, re, shutil, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
U=HERE.parent
ROOT=U.parent.parent
OUT=ROOT/'arastirma'/'MODULER_ISTASYON_v1'
OUT.mkdir(parents=True,exist_ok=True)
PRIMARY=Path(r'C:/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH/arastirma/_uretec')
sys.path.insert(0,str(U))

def cache():
    import cadquery
    src=(U/'onbellek.py').read_text(encoding='utf-8')
    seed=Path(os.environ['LOCALAPPDATA'])/'AUTOKITCH_onbellek'
    private=OUT/'.cache'
    src=re.sub(r'^KOK = .*$', lambda _: 'KOK = '+repr(str(private)),src,count=1,flags=re.M)
    helper='''\ndef _seed(path):
    if os.path.exists(path): return True
    source=os.path.join(SEED,os.path.relpath(path,KOK))
    if os.path.isfile(source):
        os.makedirs(os.path.dirname(path),exist_ok=True)
        shutil.copyfile(source,path)
        return True
    return False
'''
    src=src.replace('def _h(*p):',helper+'\ndef _h(*p):').replace('if os.path.exists(yol):','if _seed(yol):').replace('BB_YOL = os.path.join(KOK, "bb.pkl")','BB_YOL = os.path.join(KOK, "bb.pkl")\n_seed(BB_YOL)')
    m=types.ModuleType('onbellek');m.__file__=str(U/'onbellek.py');m.SEED=str(seed);m.shutil=shutil
    sys.modules['onbellek']=m;exec(compile(src,m.__file__,'exec'),m.__dict__)
    return m

def dependencies():
    # Only missing local source files are snapshotted. Imports resolve relative
    # assets in the isolated worktree, not the dirty primary checkout.
    import importlib.abc, importlib.util
    copied={}
    class Finder(importlib.abc.MetaPathFinder,importlib.abc.Loader):
        def find_spec(self,fullname,path=None,target=None):
            if '.' in fullname or (U/(fullname+'.py')).exists():return None
            source=PRIMARY/(fullname+'.py')
            dest=HERE/'legacy_dependencies'/source.name;dest.parent.mkdir(exist_ok=True)
            if not source.exists() and not dest.exists():return None
            if not dest.exists():shutil.copyfile(source,dest)
            copied[fullname]=str(dest.relative_to(ROOT))
            return importlib.util.spec_from_loader(fullname,self)
        def create_module(self,spec):return None
        def exec_module(self,module):
            name=module.__name__;module.__file__=str(U/(name+'.py'))
            exec(compile((HERE/'legacy_dependencies'/(name+'.py')).read_text(encoding='utf-8-sig'),module.__file__,'exec'),module.__dict__)
    sys.meta_path.insert(0,Finder())
    return copied

def load():
    dep=dependencies();ob=cache()
    import cadquery as cq
    original_step=cq.importers.importStep
    def step(path,*args,**kwargs):
        path=Path(path)
        if not path.exists():
            relative=path.resolve().relative_to(ROOT)
            primary=PRIMARY.parent.parent/relative
            dest=HERE/'legacy_assets'/relative
            if primary.exists() or dest.exists():
                dest.parent.mkdir(parents=True,exist_ok=True)
                if not dest.exists():shutil.copyfile(primary,dest)
                dep[str(relative)]=str(dest.relative_to(ROOT));path=dest
        return original_step(str(path),*args,**kwargs)
    cq.importers.importStep=step
    import hat_montaj_v69 as M
    M.TC.PARCALAR[:]=[];M.TC.modul()
    (OUT/'source_dependencies.json').write_text(json.dumps(dep,ensure_ascii=False,indent=2),encoding='utf-8')
    return M,ob

if __name__=='__main__':
    M,ob=load()
    print('SOURCE READY',len(M.TC.PARCALAR),len(M.SC.PARCALAR),len(M.TU.P),flush=True)
    ob.ozet();sys.stdout.flush();os._exit(0)
