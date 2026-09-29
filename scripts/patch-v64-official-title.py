from pathlib import Path
import re

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')
marker = '<!-- Smyle Lab V64: titulo oficial -->'

if marker not in html:
    # Atualiza o título principal da página.
    html = re.sub(r'<title>.*?</title>', '<title>Smyle Lab</title>', html, count=1, flags=re.I|re.S)

    script = '''<!-- Smyle Lab V64: titulo oficial -->
<script id="smyle-v64-official-title">
(function(){
  const OFFICIAL_TITLE = 'Smyle Lab';

  function keepOfficialTitle(){
    if (document.title !== OFFICIAL_TITLE) document.title = OFFICIAL_TITLE;
    const titleEl = document.querySelector('head > title');
    if (titleEl && titleEl.textContent !== OFFICIAL_TITLE) titleEl.textContent = OFFICIAL_TITLE;
  }

  keepOfficialTitle();
  document.addEventListener('DOMContentLoaded', keepOfficialTitle);
  window.addEventListener('load', keepOfficialTitle);

  const titleEl = document.querySelector('head > title');
  if (titleEl) {
    new MutationObserver(keepOfficialTitle).observe(titleEl, {
      childList: true,
      characterData: true,
      subtree: true
    });
  }
})();
</script>
'''

    head_close = html.find('</head>')
    if head_close < 0:
        raise RuntimeError('Fechamento </head> principal não encontrado.')
    html = html[:head_close] + script + html[head_close:]

path.write_text(html, encoding='utf-8')
print('V64 aplicada: título oficial definido como Smyle Lab.')
