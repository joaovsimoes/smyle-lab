from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

style = r'''
<style id="smyle-v57-restore-game-flow">
/* ==== Smyle Lab V57: restaura fluxo natural do gameplay ==== */
@media (min-width:901px){
  #gameScreen{
    height:100dvh !important;
    min-height:100dvh !important;
    overflow:hidden !important;
  }

  #gameScreen > .container.game-shell{
    height:100dvh !important;
    min-height:0 !important;
    overflow:hidden !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
  }

  /* O card não ocupa artificialmente todo o restante da viewport. */
  #gameScreen .question-card,
  #gameScreen .model-question-card{
    position:relative !important;
    flex:0 0 auto !important;
    height:auto !important;
    min-height:0 !important;
    max-height:calc(100dvh - 185px) !important;
    overflow:hidden !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
    padding:13px 20px 13px !important;
    gap:0 !important;
  }

  /* Remove o espaço elástico que estava criando o grande vazio branco. */
  #gameScreen #smyleGameStage,
  #gameScreen .smyle-game-stage{
    flex:0 0 auto !important;
    height:auto !important;
    min-height:0 !important;
    max-height:none !important;
    overflow:visible !important;
    margin:0 !important;
    padding:0 !important;
  }

  #gameScreen .question-card.smyle-next-visible{
    padding-bottom:13px !important;
  }

  #gameScreen .question-text,
  #gameScreen .model-prompt{
    margin:4px 0 8px !important;
    line-height:1.08 !important;
  }

  #gameScreen .answer-grid,
  #gameScreen .scenario-grid,
  #gameScreen .decision-options,
  #gameScreen .choice-list{
    flex:0 0 auto !important;
    margin:0 !important;
    gap:8px !important;
  }

  #gameScreen .answer-btn{
    min-height:50px !important;
    height:50px !important;
    padding:8px 13px !important;
  }

  #gameScreen .scenario-option{
    min-height:52px !important;
    padding:8px 13px !important;
  }

  /* Desembaralha */
  #gameScreen .sequence-workspace{
    flex:0 0 auto !important;
    height:auto !important;
    min-height:0 !important;
    max-height:none !important;
    gap:9px !important;
    margin:2px 0 0 !important;
  }

  #gameScreen .sequence-zone{
    min-height:120px !important;
    height:auto !important;
    max-height:235px !important;
    overflow:hidden !important;
    padding:8px 10px !important;
  }

  #gameScreen .sequence-chip{
    min-height:30px !important;
    padding:5px 8px !important;
    margin-bottom:4px !important;
  }

  #gameScreen .sequence-actions,
  #gameScreen .smyle-sequence-actions{
    flex:0 0 auto !important;
    position:static !important;
    inset:auto !important;
    margin:7px 0 0 !important;
    gap:8px !important;
  }

  #gameScreen .sequence-actions button,
  #gameScreen .smyle-sequence-actions button{
    height:38px !important;
    min-height:38px !important;
  }

  /* Conecta Lab */
  #gameScreen .matching-workspace,
  #gameScreen .matching-board{
    flex:0 0 auto !important;
    height:auto !important;
    min-height:0 !important;
    max-height:none !important;
    gap:8px !important;
    margin:2px 0 0 !important;
  }

  #gameScreen .matching-zone,
  #gameScreen .match-column{
    min-height:0 !important;
    gap:6px !important;
  }

  #gameScreen .match-card,
  #gameScreen .match-chip{
    min-height:40px !important;
    padding:7px 10px !important;
  }

  #gameScreen .match-status{
    min-height:30px !important;
    margin-top:6px !important;
    padding:6px 9px !important;
  }

  /* Feedback volta para a sequência natural do conteúdo. */
  #gameScreen #feedbackBox,
  #gameScreen .feedback{
    position:static !important;
    inset:auto !important;
    flex:0 0 auto !important;
    margin:8px 0 0 !important;
    min-height:0 !important;
    padding:8px 11px !important;
  }

  #gameScreen .feedback strong{
    font-size:14px !important;
    line-height:1.18 !important;
  }

  #gameScreen .feedback p{
    font-size:11px !important;
    line-height:1.22 !important;
    margin:2px 0 0 !important;
  }

  /* Footer próprio do jogo. Ele fica DEPOIS do feedback, não sobreposto. */
  #gameScreen .smyle-game-footer{
    display:block !important;
    flex:0 0 auto !important;
    width:100% !important;
    margin:8px 0 0 !important;
    padding:0 !important;
    position:static !important;
    inset:auto !important;
    z-index:20 !important;
  }

  /* Neutraliza explicitamente os patches anteriores que deixavam o botão absoluto. */
  #gameScreen .smyle-game-footer #nextQuestionBtn,
  #gameScreen #nextQuestionBtn:not(.hidden){
    position:static !important;
    inset:auto !important;
    left:auto !important;
    right:auto !important;
    top:auto !important;
    bottom:auto !important;
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    width:100% !important;
    min-width:0 !important;
    max-width:none !important;
    height:42px !important;
    min-height:42px !important;
    max-height:42px !important;
    margin:0 !important;
    padding:0 16px !important;
    border-radius:13px !important;
    align-items:center !important;
    justify-content:center !important;
    transform:none !important;
    clip:auto !important;
    clip-path:none !important;
    overflow:visible !important;
    pointer-events:auto !important;
    z-index:20 !important;
  }

  #gameScreen .smyle-game-footer #nextQuestionBtn.hidden{
    display:none !important;
  }
}

@media (min-width:901px) and (max-height:820px){
  #gameScreen .question-card,
  #gameScreen .model-question-card{
    max-height:calc(100dvh - 165px) !important;
    padding:9px 14px !important;
  }

  #gameScreen .question-text,
  #gameScreen .model-prompt{
    font-size:clamp(16px,1.55vw,23px) !important;
    margin:2px 0 6px !important;
  }

  #gameScreen .answer-btn,
  #gameScreen .scenario-option{
    min-height:42px !important;
    height:auto !important;
    padding:6px 10px !important;
  }

  #gameScreen .sequence-zone{
    min-height:105px !important;
    max-height:190px !important;
  }

  #gameScreen .sequence-chip{
    min-height:27px !important;
    padding:4px 7px !important;
    margin-bottom:3px !important;
  }

  #gameScreen .match-card,
  #gameScreen .match-chip{
    min-height:35px !important;
    padding:5px 8px !important;
  }

  #gameScreen #feedbackBox,
  #gameScreen .feedback{
    margin-top:5px !important;
    padding:6px 9px !important;
  }

  #gameScreen .feedback strong{font-size:12.5px !important;}
  #gameScreen .feedback p{font-size:10px !important;line-height:1.16 !important;}

  #gameScreen .smyle-game-footer{
    margin-top:5px !important;
  }

  #gameScreen .smyle-game-footer #nextQuestionBtn,
  #gameScreen #nextQuestionBtn:not(.hidden){
    height:36px !important;
    min-height:36px !important;
    max-height:36px !important;
    font-size:12.5px !important;
  }
}
</style>
'''

# V57 precisa ser o último estilo da página para vencer os !important anteriores.
if 'id="smyle-v57-restore-game-flow"' not in html:
    html = html.replace('</head>', style + '\n</head>', 1)

script = r'''
<script id="smyle-v57-restore-game-flow-js">
(function(){
  function ensureFooter(){
    var game=document.getElementById('gameScreen');
    var btn=document.getElementById('nextQuestionBtn');
    if(!game || !btn) return;

    var card=btn.closest('.question-card,.model-question-card') || game.querySelector('.question-card,.model-question-card');
    if(!card) return;

    var footer=card.querySelector(':scope > .smyle-game-footer');
    if(!footer){
      footer=document.createElement('div');
      footer.className='smyle-game-footer';
      card.appendChild(footer);
    }

    if(btn.parentElement!==footer){
      footer.appendChild(btn);
    }

    // Remove efeitos de patches antigos que posicionavam o CTA fora do fluxo.
    btn.style.position='';
    btn.style.left='';
    btn.style.right='';
    btn.style.top='';
    btn.style.bottom='';
    btn.style.transform='';

    var visible=!btn.classList.contains('hidden');
    card.classList.toggle('smyle-next-visible',visible);
  }

  function run(){
    ensureFooter();
  }

  document.addEventListener('DOMContentLoaded',function(){
    run();
    var game=document.getElementById('gameScreen');
    if(game){
      new MutationObserver(function(){
        requestAnimationFrame(run);
      }).observe(game,{subtree:true,childList:true,attributes:true,attributeFilter:['class','style','hidden']});
    }
  });

  document.addEventListener('click',function(){
    setTimeout(run,0);
    setTimeout(run,60);
    setTimeout(run,180);
  });

  window.addEventListener('load',run);
})();
</script>
'''

# V57 também deve ser o último script da página.
if 'id="smyle-v57-restore-game-flow-js"' not in html:
    html = html.replace('</body>', script + '\n</body>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V57 aplicado: botão próximo desafio restaurado ao fluxo natural após o feedback.')
