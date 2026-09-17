from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')
marker = '<!-- Smyle Lab V63: favicon oficial -->'
links = '''<!-- Smyle Lab V63: favicon oficial -->
<link rel="icon" type="image/png" sizes="64x64" href="/assets/smyle-favicon-64.png?v=63">
<link rel="icon" type="image/png" sizes="512x512" href="/assets/smyle-favicon-512.png?v=63">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png?v=63">
<meta name="theme-color" content="#61D7D3">
'''

if marker not in html:
    head_close = html.find('</head>')
    if head_close < 0:
        raise RuntimeError('Fechamento </head> principal não encontrado.')
    html = html[:head_close] + links + html[head_close:]

path.write_text(html, encoding='utf-8')
print('V63 aplicada: favicon oficial Smyle configurado.')
