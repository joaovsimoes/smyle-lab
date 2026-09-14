from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

css = r'''

/* ==== Smyle Lab V56: fluxo compacto dos jogos ==== */
@media (min-width:901px){
  /* O conteúdo dinâmico tinha min-height:300px e criava um grande vazio. */
  #gameScreen #smyleGameStage,
  #gameScreen .smyle-game-stage{
    min-height:0 !important;
    height:auto !important;
    flex:0 0 auto !important;
    overflow:visible !important;
  }

  /* O card passa a ter apenas a altura necessária para o desafio atual. */
  #gameScreen .question-card,
  #gameScreen .model-question-card{
    flex:0 0 auto !important;
    height:auto !important;
    min-height:0 !important;
    max-height:none !important;
    overflow:hidden !important;
    justify-content:flex-start !important;
    padding:14px 20px 14px !important;
  }

  #gameScreen .question-card.smyle-next-visible{
    padding-bottom:68px !important;
  }

  #gameScreen .round-kicker{
    margin:0 0 3px !important;
  }

  #gameScreen .question-meta{
    margin:0 0 4px !important;
  }

  #gameScreen .model-prompt,
  #gameScreen .question-text{
    margin:5px 0 9px !important;
    line-height:1.08 !important;
  }

  #gameScreen .answer-grid{
    gap:10px !important;
    margin:0 !important;
  }

  #gameScreen .answer-btn{
    min-height:56px !important;
    height:56px !important;
    padding:10px 14px !important;
  }

  /* Qual é a Jogada */
  #gameScreen .scenario-grid{
    gap:8px !important;
    margin:0 !important;
  }

  #gameScreen .scenario-option{
    min-height:58px !important;
    padding:10px 14px !important;
  }

  /* Desembaralha */
  #gameScreen .sequence-workspace{
    margin:2px 0 0 !important;
    gap:10px !important;
    min-height:0 !important;
    height:auto !important;
  }

  #gameScreen .sequence-zone{
    min-height:150px !important;
    height:auto !important;
    padding:10px 12px !important;
  }

  #gameScreen .sequence-chip{
    min-height:34px !important;
    padding:6px 9px !important;
    margin-bottom:5px !important;
  }

  #gameScreen .sequence-actions{
    margin:7px 0 0 !important;
    gap:8px !important;
  }

  #gameScreen .sequence-actions button{
    height:42px !important;
    min-height:42px !important;
  }

  /* Conecta Lab */
  #gameScreen .matching-board{
    gap:10px !important;
    margin:0 !important;
  }

  #gameScreen .match-column{
    gap:7px !important;
  }

  #gameScreen .match-card{
    min-height:48px !important;
    padding:9px 12px !important;
  }

  #gameScreen .match-status{
    margin-top:8px !important;
    min-height:38px !important;
    padding:8px 10px !important;
  }

  /* Feedback vem imediatamente depois da interação, sem ser empurrado para o rodapé. */
  #gameScreen #feedbackBox,
  #gameScreen .feedback{
    flex:0 0 auto !important;
    margin:8px 0 0 !important;
    padding:9px 12px !important;
    min-height:0 !important;
  }

  #gameScreen .feedback strong{
    font-size:15px !important;
    line-height:1.2 !important;
  }

  #gameScreen .feedback p{
    margin:2px 0 0 !important;
    font-size:12px !important;
    line-height:1.25 !important;
  }

  /* O CTA real permanece na base do card compacto e totalmente visível. */
  #gameScreen #nextQuestionBtn:not(.hidden){
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    align-items:center !important;
    justify-content:center !important;
    left:20px !important;
    right:20px !important;
    bottom:12px !important;
    height:44px !important;
    min-height:44px !important;
    max-height:44px !important;
    border-radius:14px !important;
    z-index:40 !important;
    pointer-events:auto !important;
  }
}

@media (min-width:901px) and (max-height:760px){
  #gameScreen > .container.game-shell{
    padding:5px 0 !important;
  }

  #gameScreen .game-top{
    min-height:36px !important;
    margin-bottom:2px !important;
  }

  #gameScreen .arena-head{
    min-height:30px !important;
    margin:1px 0 !important;
  }

  #gameScreen .belt-track{
    margin:2px 0 4px !important;
  }

  #gameScreen .belt-step{
    height:30px !important;
    min-height:30px !important;
  }

  #gameScreen .question-card,
  #gameScreen .model-question-card{
    padding:9px 14px 10px !important;
  }

  #gameScreen .question-card.smyle-next-visible{
    padding-bottom:54px !important;
  }

  #gameScreen .model-prompt,
  #gameScreen .question-text{
    font-size:clamp(16px,1.55vw,23px) !important;
    margin:3px 0 6px !important;
  }

  #gameScreen .answer-btn,
  #gameScreen .scenario-option{
    min-height:44px !important;
    height:auto !important;
    padding:7px 10px !important;
  }

  #gameScreen .sequence-zone{
    min-height:125px !important;
    padding:7px 9px !important;
  }

  #gameScreen .sequence-chip{
    min-height:29px !important;
    padding:5px 7px !important;
    margin-bottom:3px !important;
  }

  #gameScreen .sequence-actions button{
    height:36px !important;
    min-height:36px !important;
  }

  #gameScreen .match-card{
    min-height:40px !important;
    padding:6px 9px !important;
  }

  #gameScreen .match-status{
    margin-top:5px !important;
    min-height:32px !important;
    padding:6px 8px !important;
  }

  #gameScreen #feedbackBox,
  #gameScreen .feedback{
    margin-top:5px !important;
    padding:6px 9px !important;
  }

  #gameScreen .feedback strong{font-size:13px !important;}
  #gameScreen .feedback p{font-size:10.5px !important;line-height:1.18 !important;}

  #gameScreen #nextQuestionBtn:not(.hidden){
    left:14px !important;
    right:14px !important;
    bottom:7px !important;
    height:38px !important;
    min-height:38px !important;
    max-height:38px !important;
    font-size:13px !important;
  }
}
'''

marker = '/* ==== Smyle Lab V56: fluxo compacto dos jogos ==== */'
if marker not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V56 aplicado: gameplay compacto, sem vazio central e CTA visível.')
