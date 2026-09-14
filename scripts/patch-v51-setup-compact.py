from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

css = r'''

/* ==== Smyle Lab V51: seleção compacta com CTA visível ==== */
@media (min-width: 901px){
  #setupScreen{
    height:100dvh !important;
    min-height:100dvh !important;
    overflow:hidden !important;
  }

  #setupScreen > .container{
    width:min(1680px,calc(100vw - 28px)) !important;
    max-width:1680px !important;
    height:100dvh !important;
    min-height:0 !important;
    padding:10px 0 !important;
    margin:0 auto !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:center !important;
    overflow:hidden !important;
  }

  #setupScreen .start-card{
    width:100% !important;
    max-width:none !important;
    height:auto !important;
    max-height:calc(100dvh - 112px) !important;
    min-height:0 !important;
    padding:18px 22px 16px !important;
    margin:0 !important;
    overflow:hidden !important;
    border-radius:26px !important;
    display:flex !important;
    flex-direction:column !important;
    gap:12px !important;
  }

  /* grade real que contém os quatro jogos */
  #setupScreen .smyle-game-selection-grid{
    display:grid !important;
    grid-template-columns:repeat(4,minmax(0,1fr)) !important;
    gap:12px !important;
    align-items:stretch !important;
    width:100% !important;
    margin:4px 0 2px !important;
  }

  #setupScreen .smyle-setup-game-card{
    width:100% !important;
    min-width:0 !important;
    height:168px !important;
    min-height:168px !important;
    max-height:168px !important;
    padding:14px 16px !important;
    border-radius:22px !important;
    overflow:hidden !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
  }

  #setupScreen .smyle-setup-game-card > *{
    min-width:0 !important;
  }

  #setupScreen .smyle-setup-game-card h3,
  #setupScreen .smyle-setup-game-card strong{
    font-size:16px !important;
    line-height:1.15 !important;
    margin:5px 0 4px !important;
  }

  #setupScreen .smyle-setup-game-card p{
    font-size:12.5px !important;
    line-height:1.32 !important;
    margin:2px 0 !important;
  }

  #setupScreen .smyle-setup-game-card .smyle-compact-label,
  #setupScreen .smyle-setup-game-card > :last-child{
    margin-top:auto !important;
  }

  #setupScreen .smyle-setup-game-card [class*="icon"],
  #setupScreen .smyle-setup-game-card > div:first-child:empty{
    width:46px !important;
    height:46px !important;
    min-width:46px !important;
    min-height:46px !important;
  }

  /* seletor e ações sempre aparecem abaixo dos cards */
  #setupScreen select{
    min-height:44px !important;
    height:44px !important;
  }

  #setupScreen .smyle-start-experience{
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    width:100% !important;
    min-height:48px !important;
    height:48px !important;
    flex:0 0 48px !important;
    margin:2px 0 0 !important;
    align-items:center !important;
    justify-content:center !important;
    position:relative !important;
    inset:auto !important;
    z-index:10 !important;
  }

  #setupScreen .smyle-setup-actions{
    flex:0 0 auto !important;
    margin-top:auto !important;
    position:relative !important;
    z-index:9 !important;
  }
}

@media (min-width:901px) and (max-width:1280px){
  #setupScreen .smyle-game-selection-grid{
    grid-template-columns:repeat(2,minmax(0,1fr)) !important;
    gap:9px !important;
  }
  #setupScreen .smyle-setup-game-card{
    height:128px !important;
    min-height:128px !important;
    max-height:128px !important;
    padding:10px 13px !important;
  }
  #setupScreen .smyle-setup-game-card p{
    font-size:11.5px !important;
    line-height:1.24 !important;
  }
}

@media (min-width:901px) and (max-height:760px){
  #setupScreen .start-card{
    max-height:calc(100dvh - 78px) !important;
    padding:12px 16px 11px !important;
    gap:8px !important;
  }
  #setupScreen .smyle-setup-game-card{
    height:138px !important;
    min-height:138px !important;
    max-height:138px !important;
    padding:10px 13px !important;
  }
  #setupScreen .smyle-setup-game-card h3,
  #setupScreen .smyle-setup-game-card strong{
    font-size:14px !important;
  }
  #setupScreen .smyle-setup-game-card p{
    font-size:11px !important;
    line-height:1.22 !important;
  }
  #setupScreen select{
    height:40px !important;
    min-height:40px !important;
  }
  #setupScreen .smyle-start-experience{
    height:42px !important;
    min-height:42px !important;
    flex-basis:42px !important;
  }
}
'''

if '/* ==== Smyle Lab V51: seleção compacta com CTA visível ==== */' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

js = r'''
<script id="smyle-v51-setup-compact">
(function(){
  function norm(s){
    return String(s||'').replace(/\s+/g,' ').trim().toLowerCase();
  }

  var gameNames=['fato ou fake','qual é a jogada?','desembaralha!','conecta lab'];

  function countGameNames(el){
    var text=norm(el && el.textContent);
    return gameNames.reduce(function(total,name){
      return total + (text.indexOf(name)!==-1 ? 1 : 0);
    },0);
  }

  function findCardFromTitle(titleEl){
    var node=titleEl;
    var best=null;
    for(var depth=0; node && depth<8; depth++,node=node.parentElement){
      var r=node.getBoundingClientRect();
      var games=countGameNames(node);
      if(games===1 && r.width>=240 && r.height>=90 && r.height<=360){
        best=node;
      }
      if(games>1) break;
    }
    return best;
  }

  function commonParent(cards){
    if(!cards.length) return null;
    var p=cards[0].parentElement;
    while(p){
      if(cards.every(function(card){ return p===card.parentElement || p.contains(card); })){
        if(countGameNames(p)>=4) return p;
      }
      p=p.parentElement;
    }
    return null;
  }

  function apply(){
    var setup=document.getElementById('setupScreen');
    if(!setup) return;

    var cards=[];
    gameNames.forEach(function(name){
      var title=null;
      setup.querySelectorAll('h1,h2,h3,h4,strong,b,span').forEach(function(el){
        if(!title && norm(el.textContent)===name) title=el;
      });
      if(!title) return;
      var card=findCardFromTitle(title);
      if(card){
        card.classList.add('smyle-setup-game-card');
        cards.push(card);
      }
    });

    if(cards.length>=4){
      var grid=commonParent(cards);
      if(grid) grid.classList.add('smyle-game-selection-grid');
    }

    setup.querySelectorAll('button').forEach(function(btn){
      var t=norm(btn.textContent);
      if(t.indexOf('começar experiência')!==-1 || t.indexOf('comecar experiência')!==-1 || t.indexOf('comecar experiencia')!==-1){
        btn.classList.add('smyle-start-experience');
        if(btn.parentElement) btn.parentElement.classList.add('smyle-setup-actions');
      }
    });
  }

  document.addEventListener('DOMContentLoaded',apply);
  window.addEventListener('load',apply);
  document.addEventListener('click',function(){ setTimeout(apply,30); setTimeout(apply,180); });
  window.addEventListener('resize',apply);

  var observer=new MutationObserver(function(){ apply(); });
  document.addEventListener('DOMContentLoaded',function(){
    observer.observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['class','style','hidden']});
  });
})();
</script>
'''

if 'id="smyle-v51-setup-compact"' not in html:
    html = html.replace('</body>', js + '\n</body>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V51 aplicado: cards compactos em grade horizontal e CTA sempre visível.')
