from pathlib import Path
import re

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

needle = 'printWindow.document.write(`'
start = html.find(needle)
if start < 0:
    raise RuntimeError('Bloco de impressão do relatório não encontrado.')

end = html.find('printWindow.document.close();', start)
if end < 0:
    raise RuntimeError('Fechamento do bloco de impressão não encontrado.')

segment = html[start:end]

# Alguns patches antigos usavam o primeiro </body> do arquivo. Como existe um
# </body> dentro do HTML do relatório de impressão, esses scripts acabavam
# presos dentro da template string e podiam encerrar o JavaScript principal.
# Recupera TODOS os scripts Smyle que tenham caído dentro dessa template.
script_re = re.compile(
    r'<script\b(?=[^>]*\bid=["\'](?P<id>smyle-[^"\']+)["\'])[^>]*>.*?<\\?/script>',
    re.IGNORECASE | re.DOTALL,
)

recovered = []
recovered_ids = []

for match in list(script_re.finditer(segment)):
    block = match.group(0).replace('<\\/script>', '</script>')
    recovered.append(block)
    recovered_ids.append(match.group('id'))

if recovered:
    segment = script_re.sub('', segment)

# Qualquer </script> legítimo pertencente ao HTML de impressão precisa ficar
# escapado para não encerrar o <script> principal no parser do navegador.
segment = segment.replace('</script>', '<\\/script>')
html = html[:start] + segment + html[end:]

# Recoloca os scripts recuperados no BODY REAL, sempre o último </body>.
for script_id, block in zip(recovered_ids, recovered):
    if f'id="{script_id}"' in html or f"id='{script_id}'" in html:
        continue
    body_pos = html.rfind('</body>')
    if body_pos < 0:
        raise RuntimeError('Fechamento </body> principal não encontrado.')
    html = html[:body_pos] + block + '\n' + html[body_pos:]

# Validação final do artefato que será publicado.
start = html.find(needle)
end = html.find('printWindow.document.close();', start)
segment = html[start:end]

if '</script>' in segment:
    raise RuntimeError('FALHA DE INTEGRIDADE: existe </script> literal dentro do relatório de impressão.')

trapped = re.findall(r'id=["\'](smyle-[^"\']+)["\']', segment, flags=re.IGNORECASE)
if trapped:
    raise RuntimeError('FALHA DE INTEGRIDADE: scripts Smyle ainda presos no relatório: ' + ', '.join(trapped))

required = [
    'function renderReports()',
    'adminLogin = function()',
    "showScreen('setupScreen')",
    'id="smyle-v57-restore-game-flow-js"',
    'id="smyle-v59-home-entry-repair"',
]
for marker in required:
    if marker not in html:
        raise RuntimeError(f'FALHA DE INTEGRIDADE: marcador essencial ausente: {marker}')

# Os reparos de entrada e gameplay precisam estar DEPOIS do bloco de impressão.
print_end = html.find('printWindow.document.close();', html.find(needle))
for script_id in ('smyle-v57-restore-game-flow-js', 'smyle-v59-home-entry-repair'):
    pos = html.find(f'id="{script_id}"')
    if pos <= print_end:
        raise RuntimeError(f'FALHA DE INTEGRIDADE: {script_id} não está no body principal.')

path.write_text(html, encoding='utf-8')
print('V60 OK: HTML íntegro. Scripts recuperados:', ', '.join(recovered_ids) if recovered_ids else 'nenhum')
