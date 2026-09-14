from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

css = r'''

/* ==== Smyle Lab V52: seleção em uma linha + CTA sempre visível ==== */
@media (min-width: 850px){
  #setupScreen{
    height:100dvh !important;
    min-height:100dvh !important;
    overflow:hidden !important;
  }
  #setupScreen > .container{
    height:100dvh !important;
    min-height:0 !important;
    padding:10px 0 !important;
    overflow:hidden !important;
  }
  #setupScreen .start-card{
    height:calc(100dvh - 130px) !important;
    max-height:calc(100dvh - 130px) !important;
    min-height:0 !important;
    overflow:hidden !important;
    padding:18px 22px 16px !important;
    display:flex !important;
    flex-direction:column !important;
    gap:10px !important;
  }
  #setupScreen .smyle-v52-grid{
    display:grid !important;
    grid-template-columns:repeat(4,minmax(0,1fr)) !important;
    grid-template-rows:150px !important;
    gap:12px !important;
    width:100% !important;
    min-height:150px !important;
    max-height:150px !important;
    margin:2px 0 6px !important;
    align-items:stretch !important;
  }
  #setupScreen .smyle-v52-card{
    width:100% !important;
    height:150px !important;
    min-height:150px !important;
    max-height:150px !important;
    min-width:0 !important;
    margin:0 !important;
    padding:13px 15px !important;
    border-radius:20px !important;
    overflow:hidden !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
  }
  #setupScreen .smyle-v52-card h1,
  #setupScreen .smyle-v52-card h2,
  #setupScreen .smyle-v52-card h3,
  #setupScreen .smyle-v52-card h4,
  #setupScreen .smyle-v52-card strong{
    font-size:15px !important;
    line-height:1.15 !important;
    margin:5px 0 3px !important;
  }
  #setupScreen .smyle-v52-card p{
    font-size:11.5px !important;
    line-height:1.28 !important;
    margin:2px 0 !important;
  }
  #setupScreen .smyle-v52-card > :last-child{
    margin-top:auto !important;
  }
  #setupScreen .smyle-v52-controls{
    flex:0 0 auto !important;
    display:grid !important;
    grid-template-columns:minmax(0,1fr) auto !important;
    gap:10px !important;
    align-items:end !important;
    width:100% !important;
    margin-top:auto !important;
  }
  #setupScreen .smyle-v52-controls select{
    height:44px !important;
    min-height:44px !important;
  }
  #setupScreen .smyle-v52-start{
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    width:100% !important;
    min-height:48px !important;
    height:48px !important;
    margin:8px 0 0 !important;
    align-items:center !important;
    justify-content:center !important;
    position:relative !important;
    inset:auto !important;
    z-index:50 !important;
  }
}

@media (min-width:850px) and (max-height:760px){
  #setupScreen .start-card{
    height:calc(100dvh - 112px) !important;
    max-height:calc(100dvh - 112px) !important;
    padding:12px 16px !important;
    gap:7px !important;
  }
  #setupScreen .smyle-v52-grid{
    grid-template-rows:125px !important;
    min-height:125px !important;
    max-height:125px !important;
    gap:8px !important;
  }
  #setupScreen .smyle-v52-card{
    height:125px !important;
    min-height:125px !important;
    max-height:125px !important;
    padding:10px 12px !important;
  }
  #setupScreen .smyle-v52-card h1,
  #setupScreen .smyle-v52-card h2,
  #setupScreen .smyle-v52-card h3,
  #setupScreen .smyle-v52-card h4,
  #setupScreen .smyle-v52-card strong{font-size:13.5px !important;}
  #setupScreen .smyle-v52-card p{font-size:10.5px !important;line-height:1.2 !important;}
  #setupScreen .smyle-v52-start{height:42px !important;min-height:42px !important;margin-top:5px !important;}
}
'''

if '/* ==== Smyle Lab V52: seleção em uma linha + CTA sempre visível ==== */' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

js = r'''
<script id="smyle-v52-force-one-row">
(function(){
  var names=['fato ou fake','qual é a jogada?','desembaralha!','conecta lab'];
  function norm(v){return String(v||'').replace(/\s+/g,' ').trim().toLowerCase();}
  function hits(el){
    var t=norm(el && el.textContent);
    var n=0;
    names.forEach(function(x){if(t.indexOf(x)!==-1)n++;});
    return n;
  }
  function exact(root,name){
    var all=root.querySelectorAll('h1,h2,h3,h4,h5,strong,b,span,div');
    for(var i=0;i<all.length;i++) if(norm(all[i].textContent)===name) return all[i];
    return null;
  }
  function cardFor(title){
    if(!title) return null;
    var node=title;
    var previous=title;
    while(node && node.parentElement){
      var p=node.parentElement;
      var pHits=hits(p);
      if(pHits>1) return node;
      previous=node;
      node=p;
    }
    return previous;
  }
  function lca(nodes){
    if(!nodes.length)return null;
    var a=[]; var n=nodes[0];
    while(n){a.push(n);n=n.parentElement;}
    for(var i=0;i<a.length;i++){
      var candidate=a[i];
      if(nodes.every(function(x){return candidate.contains(x);})){return candidate;}
    }
    return null;
  }
  function directChild(container,node){
    var cur=node;
    while(cur && cur.parentElement!==container) cur=cur.parentElement;
    return cur;
  }
  function findButton(root,needle){
    var btns=root.querySelectorAll('button,a');
    needle=norm(needle);
    for(var i=0;i<btns.length;i++) if(norm(btns[i].textContent).indexOf(needle)!==-1) return btns[i];
    return null;
  }
  function apply(){
    var setup=document.getElementById('setupScreen');
    if(!setup || window.innerWidth<850) return;

    var cards=[];
    names.forEach(function(name){
      var title=exact(setup,name);
      var card=cardFor(title);
      if(card && cards.indexOf(card)===-1) cards.push(card);
    });

    if(cards.length===4){
      var parent=lca(cards);
      if(parent){
        var items=cards.map(function(c){return directChild(parent,c) || c;});
        var unique=items.filter(function(x,i,a){return x && a.indexOf(x)===i;});
        if(unique.length===4){
          parent.classList.add('smyle-v52-grid');
          unique.forEach(function(item){
            item.classList.add('smyle-v52-card');
            item.style.height='150px';
            item.style.minHeight='150px';
            item.style.maxHeight='150px';
          });
        }else{
          cards.forEach(function(c){c.classList.add('smyle-v52-card');});
          if(cards[0].parentElement && cards.every(function(c){return c.parentElement===cards[0].parentElement;})){
            cards[0].parentElement.classList.add('smyle-v52-grid');
          }
        }
      }
    }

    var start=findButton(setup,'começar experiência') || findButton(setup,'comecar experiencia');
    if(start){
      start.classList.add('smyle-v52-start');
      start.style.display='flex';
      start.style.visibility='visible';
      start.style.opacity='1';
      var controls=start.parentElement;
      if(controls) controls.classList.add('smyle-v52-controls');
    }

    var selects=setup.querySelectorAll('select');
    if(selects.length){
      var select=selects[selects.length-1];
      var row=select.parentElement;
      for(var d=0;row && d<4;d++,row=row.parentElement){
        if(row.querySelector && row.querySelector('button')){
          row.classList.add('smyle-v52-controls');
          break;
        }
      }
    }
  }
  document.addEventListener('DOMContentLoaded',apply);
  window.addEventListener('load',apply);
  window.addEventListener('resize',apply);
  document.addEventListener('click',function(){setTimeout(apply,30);setTimeout(apply,180);});
  setTimeout(apply,250);
  setTimeout(apply,800);
  var obs=new MutationObserver(function(){apply();});
  document.addEventListener('DOMContentLoaded',function(){
    obs.observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['class','style','hidden']});
  });
})();
</script>
'''

if 'id="smyle-v52-force-one-row"' not in html:
    html = html.replace('</body>', js + '\n</body>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V52 aplicado: quatro jogos em uma linha e botão de início sempre visível.')
