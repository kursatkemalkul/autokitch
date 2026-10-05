"""Private, reproducible CAD runner. Never writes the primary checkout."""
import importlib.abc
import importlib.util
import os
from pathlib import Path
import re
import runpy
import shutil
import sys
import types

U = Path(__file__).resolve().parent
ROOT = U.parent.parent
PRIVATE = ROOT / '_local' / 'kutu-v9'
PRIMARY = Path('C:/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH')
sys.dont_write_bytecode = True

def setup():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(U))
    class Missing(importlib.abc.MetaPathFinder, importlib.abc.Loader):
        def find_spec(self, fullname, path=None, target=None):
            if '.' in fullname or (U / (fullname + '.py')).exists():
                return None
            p = PRIVATE / 'dependencies' / (fullname + '.py')
            src = U / 'moduler_istasyon_v1' / 'legacy_dependencies' / p.name
            if not src.exists():
                src = PRIMARY / 'arastirma' / '_uretec' / p.name
            if not p.exists() and not src.exists():
                return None
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists():
                shutil.copyfile(src, p)
            return importlib.util.spec_from_loader(fullname, self)
        def create_module(self, spec):
            return None
        def exec_module(self, module):
            p = PRIVATE / 'dependencies' / (module.__name__ + '.py')
            module.__file__ = str(U / p.name)
            exec(compile(p.read_text(encoding='utf-8-sig'), module.__file__, 'exec'), module.__dict__)
    sys.meta_path.insert(0, Missing())
    import cadquery as cq
    src = (U / 'onbellek.py').read_text(encoding='utf-8')
    seed = Path(os.environ.get('AUTOKITCH_SEED_CACHE', str(Path(os.environ['LOCALAPPDATA']) / 'AUTOKITCH_onbellek')))
    cache = PRIVATE / 'cache'
    src = re.sub(r'^KOK = .*$', lambda _: 'KOK = ' + repr(str(cache)), src, count=1, flags=re.M)
    helper = '''\ndef _seed(path):
    if os.path.exists(path): return True
    source=os.path.join(SEED,os.path.relpath(path,KOK))
    if os.path.isfile(source):
        os.makedirs(os.path.dirname(path),exist_ok=True)
        shutil.copyfile(source,path)
        return True
    return False
'''
    src = src.replace('def _h(*p):', helper + '\ndef _h(*p):').replace('if os.path.exists(yol):', 'if _seed(yol):')
    src = src.replace('BB_YOL = os.path.join(KOK, "bb.pkl")', 'BB_YOL = os.path.join(KOK, "bb.pkl")\n_seed(BB_YOL)')
    ob = types.ModuleType('onbellek')
    ob.__file__ = str(U / 'onbellek.py')
    ob.SEED, ob.shutil = str(seed), shutil
    sys.modules['onbellek'] = ob
    exec(compile(src, ob.__file__, 'exec'), ob.__dict__)
    original = cq.importers.importStep
    def step(path, *a, **kw):
        p = Path(path)
        if not p.exists():
            rel = p.resolve().relative_to(ROOT)
            src = PRIMARY / rel
            dst = PRIVATE / 'assets' / rel
            if src.exists() and not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
            if dst.exists():
                p = dst
        return original(str(p), *a, **kw)
    cq.importers.importStep = step
    return ob

if __name__ == '__main__':
    ob = setup()
    target = sys.argv[1]
    sys.argv = sys.argv[1:]
    original_exit = os._exit
    def clean_exit(code=0):
        ob.ozet()
        sys.stdout.flush()
        original_exit(code)
    os._exit = clean_exit
    try:
        runpy.run_path(str(U / target), run_name='__main__')
    except BaseException:
        ob.ozet()
        raise
    clean_exit(0)
