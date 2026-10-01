r"""
Visor de ofertas guardadas en data/latest_jobs.json
Uso:
    .\.venv\Scripts\python.exe scripts\ver_ofertas.py           # top 15
    .\.venv\Scripts\python.exe scripts\ver_ofertas.py 30        # top 30
"""
import json
import sys
from pathlib import Path

# UTF-8 en Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TOP = int(sys.argv[1]) if len(sys.argv) > 1 else 15
JSON_PATH = Path("data/latest_jobs.json")

if not JSON_PATH.exists():
    print("❌ No hay ofertas. Ejecuta primero:")
    print("   .\\.venv\\Scripts\\python.exe -m src.main")
    sys.exit(1)

data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
print(f"\n📋 Total ofertas relevantes: {len(data)}")
print(f"   Mostrando las mejores {TOP}:\n")

# Cabecera de tabla
print(f"{'Score':>5} | {'Titulo':<40} | {'Empresa':<25} | Ubicacion")
print("-" * 110)

for j in data[:TOP]:
    score = j.get("score", 0)
    title = (j.get("title") or "")[:40]
    company = (j.get("company") or "")[:25]
    location = (j.get("location") or "")[:30]
    print(f"{score:>5} | {title:<40} | {company:<25} | {location}")

print("\n🔗 Enlaces:\n")
for i, j in enumerate(data[:TOP], 1):
    print(f"  [{i:>2}] {j.get('title')} @ {j.get('company')}")
    print(f"       {j.get('url')}")