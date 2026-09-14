from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

css = r'''

/* ==== Smyle Lab V55: botão Próximo desafio sempre acessível ==== */
@media (min-width: 901px){
  #gameScreen .question-card{
    position:relative !important;
  }

  /* O botão real do jogo é #nextQuestionBtn. Mantém escondido apenas enquanto a lógica do jogo pedir. */
  #gameScreen #nextQuestionBtn:not(.hidden){
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    align-items:center !important;
    justify-content:center !important;
    width:auto !important;
    min-width:0 !important;
    height:46px !important;
    min-height:46px !important;
    max-height:46px !important;
    position:absolute !important;
    left:22px !important;
    right:22px !important;
    bottom:12px !important;
    margin:0 !important;
    padding:0 18px !important;
    border-radius:15px !important;
    z-index:30 !important;
    overflow:visible !important;
    pointer-events:auto !important;
  }

  /* Reserva a faixa inferior do card para o CTA sem empurrá-lo para fora da tela. */
  #gameScreen .question-card.smyle-next-visible{
    padding-bottom:70px !important;
  }

  #gameScreen .question-card.smyle-next-visible .feedback{
    margin-bottom:0 !important;
  }

  /* Nos jogos com conteúdo mais alto, compacta só o necessário para preservar o CTA. */
  #gameScreen .question-card.smyle-next-visible .sequence-workspace,
  #gameScreen .question-card.smyle-next-visible .matching-workspace{
    min-height:0 !important;
  }

  #gameScreen .question-card.smyle-next-visible .sequence-zone,
  #gameScreen .question-card.smyle-next-visible .matching-zone{
    min-height:0 !important;
  }

  /* Garante que nenhum estilo antigo transforme o botão em uma faixa cortada. */
  #gameScreen #nextQuestionBtn:not(.hidden).primary-btn{
    transform:none !important;
    clip:auto !important;
    clip-path:none !important;
  }
}

@media (min-width:901px) and (max-height:820px){
  #gameScreen #nextQuestionBtn:not(.hidden){
    height:40px !important;
    min-height:40px !important;
    max-height:40px !important;
    left:16px !important;
    right:16px !important;
    bottom:8px !important;
    border-radius:13px !important;
    font-size:14px !important;
  }

  #gameScreen .question-card.smyle-next-visible{
    padding-bottom:56px !important;
  }

  #gameScreen .question-card.smyle-next-visible .feedback{
    padding:6px 9px !important;
    margin-top:4px !important;
  }

  #gameScreen .question-card.smyle-next-visible .feedback strong{
    font-size:13px !important;
  }

  #gameScreen .question-card.smyle-next-visible .feedback p{
    font-size:10.5px !important;
    line-height:1.2 !important;
  }
}
'''

marker = '/* ==== Smyle Lab V55: botão Próximo desafio sempre acessível ==== */'
if marker not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

js = r'''
<script id="smyle-v55-next-button">
(function(){
  function syncNextButton(){
    var game=document.getElementById('gameScreen');
    if(!game) return;

    var btn=document.getElementById('nextQuestionBtn');
    var card=game.querySelector('.question-card');
    if(!btn || !card) return;

    var visible=!btn.classList.contains('hidden') && getComputedStyle(btn).display!=='none';
    card.classList.toggle('smyle-next-visible',visible);

    if(visible){
      btn.classList.add('smyle-next-stage');
      btn.style.pointerEvents='auto';
    }
  }

  document.addEventListener('DOMContentLoaded',function(){
    syncNextButton();
    var btn=document.getElementById('nextQuestionBtn');
    if(btn){
      new MutationObserver(syncNextButton).observe(btn,{attributes:true,attributeFilter:['class','style'],childList:true,subtree:true});
    }
  });

  document.addEventListener('click',function(){
    setTimeout(syncNextButton,0);
    setTimeout(syncNextButton,80);
    setTimeout(syncNextButton,220);
  });

  window.addEventListener('load',syncNextButton);
})();
</script>
'''

if 'id="smyle-v55-next-button"' not in html:
    html = html.replace('</body>', js + '\n</body>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V55 aplicado: botão Próximo desafio permanece totalmente visível e clicável.')
