from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_sac_guncelle.py'
code=source.read_text(encoding='utf-8').replace("'k_parca.pkl'","'k_parca78_verified.pkl'").replace("'custom_flat_stock_audit.json'","'custom_flat_stock_audit78.json'").replace("'current_sheet_encoding_audit.json'","'current_sheet_encoding_audit78.json'").replace("'current_sheet_bending.json'","'current_sheet_bending78.json'")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))