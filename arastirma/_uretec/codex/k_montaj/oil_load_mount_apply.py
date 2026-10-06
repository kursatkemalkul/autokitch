"""Reuse the checked source-bound repair writer; no shared chain activation."""
from pathlib import Path
source=Path(__file__).with_name('oil_shelf_mount_apply.py')
code=source.read_text(encoding='utf-8').replace("/'oil_shelf_mount_candidate'","/'oil_load_mount_candidate'")
code=code.replace('k_parca_bottom_verified.pkl','k_parca_oil_verified.pkl')
code=code.replace("'prototype':'oil shelf wall mounts; not full shelf/pump fixing'","'prototype':'six wall mounts and eight load-deck/plate mounts; pump-to-plate fixing remains open'")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
