"""Versioned E revision; v9 remains byte-for-byte unchanged."""
from pathlib import Path
U = Path(__file__).resolve().parent
s = (U / 'kutu_cad_v9.py').read_text(encoding='utf-8-sig')
s = s.replace('"""v9: Motor taban ÜSTÜNDE;', '"""v10: Tahrikli köşe / ön dil / kılavuzlu kapak takımları — KİNEMATİK PROTOTİP.\nÖnceki v9: Motor taban ÜSTÜNDE;',1)
s = s.replace('Kutu açınımı TASLAK, köşe tırnağı kıvırıcısı eksik: tam otomatik katlama doğrulanmış değildir.', 'Kutu açınımı TASLAK; köşe tahrikleri v10 içinde eklendi. Gerçek kartonla otomatik katlama doğrulanmış değildir.',1)
marker = '\nif __name__ == "__main__":'
assert s.count(marker) == 1
s = s.split(marker)[0] + '\n' + (U / 'kutu_katlama_v10.py').read_text(encoding='utf-8')
s += '\nif __name__ == "__main__":\n    import runpy\n    runpy.run_path(os.path.join(U, "kutu_v10_check.py"), run_name="__main__")\n'
compile(s, 'kutu_cad_v10.py', 'exec')
(U / 'kutu_cad_v10.py').write_text(s, encoding='utf-8')
runner = (U / 'kutu_v9_build.py').read_text(encoding='utf-8-sig').replace("'kutu-v9'", "'kutu-v10'")
runner = runner.replace("source=os.path.join(SEED,os.path.relpath(path,KOK))\n    if os.path.isfile(source):\n        os.makedirs(os.path.dirname(path),exist_ok=True)\n        shutil.copyfile(source,path)\n        return True", "for seed_root in [SEED]+os.environ.get('AUTOKITCH_SEED_EXTRA','').split(os.pathsep):\n        if not seed_root: continue\n        source=os.path.join(seed_root,os.path.relpath(path,KOK))\n        if os.path.isfile(source):\n            os.makedirs(os.path.dirname(path),exist_ok=True)\n            shutil.copyfile(source,path)\n            return True")
(U / 'kutu_v10_build.py').write_text(runner, encoding='utf-8')
print('kutu_cad_v10.py + private runner generated')
