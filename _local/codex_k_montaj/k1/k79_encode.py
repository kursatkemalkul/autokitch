"""Re-encode all source sheets against stage79 verified geometry."""
from pathlib import Path
H=Path(__file__).resolve().parent;source=H/'k_sac_guncelle.py'
code=source.read_text(encoding='utf-8').replace("'k_parca.pkl'","'k_parca79_verified.pkl'").replace("'custom_flat_stock_audit.json'","'custom_flat_stock_audit79.json'").replace("'current_sheet_encoding_audit.json'","'current_sheet_encoding_audit79.json'").replace("'current_sheet_bending.json'","'current_sheet_bending79.json'")
exec(compile(code,str(source),'exec'),dict(__file__=str(source),__name__='__main__'))
