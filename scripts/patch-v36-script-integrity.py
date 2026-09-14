from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

needle = 'printWindow.document.write(`'
search_from = 0
fixed = 0

while True:
    start = html.find(needle, search_from)
    if start < 0:
        break
    end = html.find('printWindow.document.close();', start)
    if end < 0:
        raise RuntimeError('Bloco de impressão encontrado sem fechamento esperado.')

    segment = html[start:end]
    safe_segment = segment.replace('</script>', '<\\/script>')
    if safe_segment != segment:
        fixed += segment.count('</script>')
        html = html[:start] + safe_segment + html[end:]
        end = start + len(safe_segment)

    search_from = end

# Validação: um </script> literal dentro do HTML escrito pelo printWindow
# encerra o script principal do portal no parser do navegador e faz o restante
# do JavaScript aparecer como texto na página.
search_from = 0
while True:
    start = html.find(needle, search_from)
    if start < 0:
        break
    end = html.find('printWindow.document.close();', start)
    if end < 0:
        raise RuntimeError('Bloco de impressão inválido após correção.')
    segment = html[start:end]
    if '</script>' in segment:
        raise RuntimeError('Ainda existe </script> não escapado dentro do template de impressão.')
    search_from = end

# Confirma que funções essenciais continuam dentro do HTML final.
required = [
    "function renderReports()",
    "adminLogin = function()",
    "showScreen('setupScreen')",
]
for marker in required:
    if marker not in html:
        raise RuntimeError(f'Marcador essencial não encontrado: {marker}')

path.write_text(html, encoding='utf-8')
print(f'Patch V36 aplicado. Fechamentos de script corrigidos: {fixed}.')
