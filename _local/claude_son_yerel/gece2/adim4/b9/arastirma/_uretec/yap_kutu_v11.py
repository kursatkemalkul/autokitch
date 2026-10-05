from pathlib import Path
U=Path(__file__).resolve().parent
s=(U/'kutu_cad_v10.py').read_text(encoding='utf-8-sig').split('\nif __name__ == "__main__":')[0]
s+='\n'+(U/'kutu_duzen_v11.py').read_text(encoding='utf-8')
compile(s,'kutu_cad_v11.py','exec')
(U/'kutu_cad_v11.py').write_text(s,encoding='utf-8')
print('v11 generated; v10 unchanged')
