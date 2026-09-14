from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

css = r'''

/* ==== Smyle Lab V50: gameplay em tela única ==== */
@media (min-width: 901px){
  html, body{height:100%;}

  /* Tela de seleção de jogos: sem rolagem e com os 4 cards visíveis */
  #setupScreen{
    height:100dvh !important;
    min-height:100dvh !important;
    overflow:hidden !important;
    padding:0 !important;
  }
  #setupScreen > .container{
    height:100dvh !important;
    min-height:0 !important;
    width:min(1440px,calc(100vw - 34px)) !important;
    max-width:1440px !important;
    padding:14px 0 !important;
    margin:0 auto !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:center !important;
    overflow:hidden !important;
  }
  #setupScreen .start-card{
    width:100% !important;
    max-width:none !important;
    min-height:0 !important;
    max-height:calc(100dvh - 108px) !important;
    padding:18px 22px !important;
    margin:0 !important;
    overflow:hidden !important;
    border-radius:24px !important;
  }
  #setupScreen .smyle-setup-game-card{
    min-height:0 !important;
    height:clamp(150px,23dvh,214px) !important;
    padding:16px 18px !important;
    overflow:hidden !important;
  }
  #setupScreen .smyle-setup-game-card h3,
  #setupScreen .smyle-setup-game-card strong{
    margin-top:6px !important;
    margin-bottom:4px !important;
  }
  #setupScreen .smyle-setup-game-card p{
    margin:4px 0 !important;
    line-height:1.35 !important;
  }
  #setupScreen .smyle-setup-game-card .smyle-compact-label{
    margin-top:auto !important;
  }
  #setupScreen select{
    min-height:44px !important;
    height:44px !important;
  }
  #setupScreen .smyle-start-experience{
    min-height:48px !important;
    height:48px !important;
    margin-top:10px !important;
  }

  /* Gameplay: estrutura rígida de uma única viewport */
  #gameScreen{
    height:100dvh !important;
    min-height:100dvh !important;
    overflow:hidden !important;
    padding:0 !important;
  }
  #gameScreen > .container.game-shell{
    width:min(1680px,calc(100vw - 28px)) !important;
    max-width:1680px !important;
    height:100dvh !important;
    min-height:0 !important;
    margin:0 auto !important;
    padding:10px 0 !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
    overflow:hidden !important;
  }
  #gameScreen .game-top{
    flex:0 0 auto !important;
    min-height:44px !important;
    margin:0 0 5px !important;
    gap:10px !important;
  }
  #gameScreen .progress-wrap{
    height:7px !important;
    margin:0 !important;
  }
  #gameScreen .arena-head{
    flex:0 0 auto !important;
    margin:4px 0 2px !important;
    min-height:40px !important;
  }
  #gameScreen .belt-track{
    flex:0 0 auto !important;
    margin:5px 0 8px !important;
    gap:8px !important;
  }
  #gameScreen .belt-step{
    height:38px !important;
    min-height:38px !important;
    border-radius:11px !important;
  }
  #gameScreen .question-card{
    flex:1 1 auto !important;
    min-height:0 !important;
    max-height:none !important;
    margin:0 !important;
    padding:16px 22px 14px !important;
    border-radius:24px !important;
    overflow:hidden !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
  }
  #gameScreen .question-meta,
  #gameScreen .round-kicker{
    margin-bottom:3px !important;
  }
  #gameScreen .question-text,
  #gameScreen .model-prompt{
    font-size:clamp(20px,2vw,31px) !important;
    line-height:1.08 !important;
    margin:5px 0 10px !important;
  }
  #gameScreen .answer-grid{
    gap:8px !important;
    margin:0 !important;
  }
  #gameScreen .answer-btn{
    min-height:58px !important;
    padding:12px 16px !important;
    border-radius:15px !important;
    font-size:clamp(15px,1.15vw,19px) !important;
  }
  #gameScreen .feedback{
    flex:0 0 auto !important;
    margin:8px 0 0 !important;
    padding:9px 12px !important;
    border-radius:14px !important;
    min-height:0 !important;
  }
  #gameScreen .feedback strong{font-size:15px !important;}
  #gameScreen .feedback p{
    font-size:12px !important;
    line-height:1.28 !important;
    margin:2px 0 !important;
  }
  #gameScreen .smyle-next-stage{
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    flex:0 0 46px !important;
    min-height:46px !important;
    height:46px !important;
    width:100% !important;
    margin:8px 0 0 !important;
    align-items:center !important;
    justify-content:center !important;
    position:relative !important;
    inset:auto !important;
    z-index:8 !important;
  }

  /* Qual é a Jogada: reduz opções para manter feedback + próxima etapa */
  #gameScreen .decision-options,
  #gameScreen .choice-list{
    gap:7px !important;
  }

  /* Desembaralha: elimina sobreposição entre feedback e botões */
  #gameScreen .sequence-workspace{
    flex:1 1 auto !important;
    min-height:0 !important;
    gap:10px !important;
    margin:4px 0 0 !important;
  }
  #gameScreen .sequence-zone{
    min-height:0 !important;
    padding:10px 12px !important;
    overflow:hidden !important;
  }
  #gameScreen .sequence-chip{
    min-height:38px !important;
    padding:8px 10px !important;
    margin-bottom:6px !important;
  }
  #gameScreen .sequence-actions,
  #gameScreen .smyle-sequence-actions{
    flex:0 0 auto !important;
    display:grid !important;
    grid-template-columns:minmax(130px,.7fr) minmax(220px,1.25fr) minmax(150px,.75fr) !important;
    gap:8px !important;
    align-items:center !important;
    margin:8px 0 0 !important;
    padding:0 !important;
    position:relative !important;
    inset:auto !important;
    z-index:8 !important;
    background:transparent !important;
  }
  #gameScreen .sequence-actions button,
  #gameScreen .smyle-sequence-actions button{
    min-height:44px !important;
    height:44px !important;
    margin:0 !important;
  }
  #gameScreen .sequence-actions .smyle-next-stage,
  #gameScreen .smyle-sequence-actions .smyle-next-stage{
    margin:0 !important;
    height:44px !important;
    min-height:44px !important;
  }

  /* Conecta Lab: compacta os pares e garante CTA no rodapé */
  #gameScreen .matching-workspace{
    flex:1 1 auto !important;
    min-height:0 !important;
    gap:8px !important;
    margin:4px 0 0 !important;
  }
  #gameScreen .matching-zone{
    min-height:0 !important;
    padding:8px 10px !important;
  }
  #gameScreen .match-chip{
    min-height:46px !important;
    padding:9px 12px !important;
    font-size:14px !important;
  }

  /* Evita qualquer barra de rolagem da página durante os jogos */
  body.smyle-game-active,
  body:has(#gameScreen:not([style*="display: none"])){
    overflow:hidden !important;
  }
}

@media (min-width:901px) and (max-height:820px){
  #gameScreen > .container.game-shell{padding:6px 0 !important;}
  #gameScreen .game-top{min-height:38px !important;}
  #gameScreen .arena-head{min-height:34px !important;margin:2px 0 !important;}
  #gameScreen .belt-track{margin:3px 0 5px !important;}
  #gameScreen .belt-step{height:32px !important;min-height:32px !important;}
  #gameScreen .question-card{padding:11px 16px 10px !important;}
  #gameScreen .question-text,#gameScreen .model-prompt{font-size:clamp(17px,1.7vw,25px) !important;margin:3px 0 7px !important;}
  #gameScreen .answer-btn{min-height:48px !important;padding:9px 12px !important;font-size:14px !important;}
  #gameScreen .feedback{margin-top:5px !important;padding:7px 10px !important;}
  #gameScreen .feedback p{font-size:11px !important;}
  #gameScreen .smyle-next-stage{min-height:40px !important;height:40px !important;flex-basis:40px !important;margin-top:5px !important;}
  #gameScreen .sequence-chip{min-height:32px !important;padding:6px 8px !important;margin-bottom:4px !important;}
  #gameScreen .sequence-actions button,#gameScreen .smyle-sequence-actions button{height:38px !important;min-height:38px !important;}
  #setupScreen .start-card{max-height:calc(100dvh - 78px) !important;padding:13px 18px !important;}
  #setupScreen .smyle-setup-game-card{height:clamp(126px,21dvh,165px) !important;padding:12px 14px !important;}
}
'''

if '/* ==== Smyle Lab V50: gameplay em tela única ==== */' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

js = r'''
<script id="smyle-v50-one-screen-games">
(function(){
  function norm(s){ return String(s||'').replace(/\s+/g,' ').trim().toLowerCase(); }

  function tagByText(root, text, className){
    if(!root) return null;
    var wanted=norm(text);
    var nodes=root.querySelectorAll('button,a,div,article,section');
    var best=null;
    for(var i=0;i<nodes.length;i++){
      var el=nodes[i];
      var value=norm(el.textContent);
      if(value===wanted || value.indexOf(wanted)!==-1){
        if(!best || el.children.length < best.children.length) best=el;
      }
    }
    if(best) best.classList.add(className);
    return best;
  }

  function tagSetup(){
    var setup=document.getElementById('setupScreen');
    if(!setup) return;
    ['Fato ou Fake','Qual é a Jogada?','Desembaralha!','Conecta Lab'].forEach(function(name){
      var candidates=setup.querySelectorAll('button,[role="button"],article,.card,.game-card,.game-option,.model-card,div');
      var best=null;
      for(var i=0;i<candidates.length;i++){
        var el=candidates[i];
        var t=norm(el.textContent);
        if(t.indexOf(norm(name))===-1) continue;
        var rect=el.getBoundingClientRect();
        if(rect.width<220 || rect.height<80 || rect.height>420) continue;
        if(!best || rect.width*rect.height < best.getBoundingClientRect().width*best.getBoundingClientRect().height) best=el;
      }
      if(best) best.classList.add('smyle-setup-game-card');
    });
    setup.querySelectorAll('button').forEach(function(btn){
      var t=norm(btn.textContent);
      if(t.indexOf('começar experiência')!==-1) btn.classList.add('smyle-start-experience');
    });
  }

  function tagGameActions(){
    var game=document.getElementById('gameScreen');
    if(!game) return;
    game.querySelectorAll('button').forEach(function(btn){
      var t=norm(btn.textContent);
      if(t.indexOf('próxima etapa')!==-1 || t.indexOf('proxima etapa')!==-1){
        btn.classList.add('smyle-next-stage');
      }
    });

    var seqButtons=[];
    game.querySelectorAll('button').forEach(function(btn){
      var t=norm(btn.textContent);
      if(t.indexOf('refazer')!==-1 || t.indexOf('verificar sequência')!==-1 || t.indexOf('verificar sequencia')!==-1 || t.indexOf('próxima etapa')!==-1 || t.indexOf('proxima etapa')!==-1){
        seqButtons.push(btn);
      }
    });
    if(seqButtons.length>=2){
      var parent=seqButtons[0].parentElement;
      if(parent && seqButtons.every(function(b){return b.parentElement===parent;})) parent.classList.add('smyle-sequence-actions');
    }
  }

  function syncGameBodyState(){
    var game=document.getElementById('gameScreen');
    if(!game) return;
    var visible=getComputedStyle(game).display!=='none' && !game.hidden;
    document.body.classList.toggle('smyle-game-active',visible);
  }

  function apply(){ tagSetup(); tagGameActions(); syncGameBodyState(); }
  document.addEventListener('DOMContentLoaded',apply);
  window.addEventListener('load',apply);
  document.addEventListener('click',function(){ setTimeout(apply,20); setTimeout(apply,180); });
  var obs=new MutationObserver(function(){ apply(); });
  document.addEventListener('DOMContentLoaded',function(){ obs.observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['style','class','hidden']}); });
})();
</script>
'''

if 'id="smyle-v50-one-screen-games"' not in html:
    html = html.replace('</body>', js + '\n</body>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V50 aplicado: jogos e seleção em tela única, ações sempre visíveis.')
