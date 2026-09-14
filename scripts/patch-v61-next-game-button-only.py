from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

marker = '/* ==== Smyle Lab V61: somente botão de avançar dos jogos ==== */'
css = r'''

/* ==== Smyle Lab V61: somente botão de avançar dos jogos ==== */
#gameScreen #nextQuestionBtn.hidden {
  display: none !important;
}

#gameScreen #nextQuestionBtn:not(.hidden) {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: fixed !important;
  left: 50% !important;
  right: auto !important;
  bottom: 18px !important;
  transform: translateX(-50%) !important;
  width: min(760px, calc(100vw - 40px)) !important;
  height: 52px !important;
  min-height: 52px !important;
  max-height: 52px !important;
  margin: 0 !important;
  padding: 0 22px !important;
  border-radius: 16px !important;
  z-index: 9999 !important;
  opacity: 1 !important;
  visibility: visible !important;
  pointer-events: auto !important;
  overflow: visible !important;
  box-shadow: 0 12px 30px rgba(8, 26, 46, .20) !important;
}

@media (max-width: 700px) {
  #gameScreen #nextQuestionBtn:not(.hidden) {
    bottom: 12px !important;
    width: calc(100vw - 24px) !important;
    height: 48px !important;
    min-height: 48px !important;
    max-height: 48px !important;
    border-radius: 14px !important;
  }
}
'''

if marker not in html:
    head_close = html.rfind('</head>')
    if head_close == -1:
        raise SystemExit('ERRO: fechamento </head> não encontrado')
    html = html[:head_close] + '<style>\n' + css + '\n</style>\n' + html[head_close:]

path.write_text(html, encoding='utf-8')
print('V61 aplicada: somente o botão de avançar dos jogos foi fixado na área visível.')
