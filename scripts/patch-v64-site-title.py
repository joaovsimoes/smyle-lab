from pathlib import Path
import re

path = Path("public/index.html")
if not path.exists():
    raise SystemExit("public/index.html não encontrado")

html = path.read_text(encoding="utf-8")

updated, count = re.subn(
    r"<title\b[^>]*>.*?</title>",
    "<title>Smyle Lab</title>",
    html,
    count=1,
    flags=re.IGNORECASE | re.DOTALL,
)

if count == 0:
    head_close = updated.lower().find("</head>")
    if head_close < 0:
        raise RuntimeError("</head> não encontrado")
    updated = updated[:head_close] + "<title>Smyle Lab</title>\n" + updated[head_close:]

path.write_text(updated, encoding="utf-8")
print("V64 aplicada: título do site definido como Smyle Lab.")
