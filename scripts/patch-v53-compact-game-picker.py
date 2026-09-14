from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

css = r'''

/* ==== Smyle Lab V53: seletor de jogos como botões compactos ==== */
@media (min-width: 850px){
  #setupScreen{
    height:100dvh !important;
    min-height:100dvh !important;
    overflow:hidden !important;
    padding:8px 14px !important;
  }

  #setupScreen > .container{
    width:min(1280px,calc(100vw - 28px)) !important;
    max-width:1280px !important;
    height:100% !important;
    min-height:0 !important;
    margin:0 auto !important;
    padding:0 !important;
    display:flex !important;
    flex-direction:column !important;
    overflow:hidden !important;
  }

  #setupScreen .topbar{
    flex:0 0 auto !important;
    min-height:60px !important;
    margin:0 0 6px !important;
  }

  #setupScreen .smyle-setup-wordmark{
    width:118px !important;
    max-width:118px !important;
    height:auto !important;
    max-height:52px !important;
    object-fit:contain !important;
  }

  #setupScreen .back-btn{
    padding:9px 15px !important;
    border-radius:16px !important;
    font-size:13px !important;
  }

  #setupScreen .start-card{
    flex:1 1 auto !important;
    height:auto !important;
    max-height:none !important;
    min-height:0 !important;
    overflow:hidden !important;
    padding:14px 18px !important;
    border-radius:24px !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
    gap:7px !important;
  }

  #setupScreen .panel-title{
    flex:0 0 auto !important;
    margin:0 0 3px !important;
    gap:12px !important;
    align-items:flex-start !important;
  }

  #setupScreen .panel-title h2{
    margin:0 !important;
    font-size:18px !important;
    line-height:1.15 !important;
  }

  #setupScreen .panel-title p{
    margin:3px 0 0 !important;
    font-size:11.5px !important;
    line-height:1.3 !important;
  }

  #setupScreen .smyle-player-code-card{
    min-width:150px !important;
    padding:8px 12px !important;
    border-radius:17px !important;
  }

  #setupScreen .smyle-player-code-card span{
    font-size:9px !important;
  }

  #setupScreen .smyle-player-code-card strong{
    font-size:16px !important;
    line-height:1.1 !important;
  }

  #setupScreen .game-model-grid,
  #setupScreen .smyle-v52-grid{
    flex:0 0 auto !important;
    display:grid !important;
    grid-template-columns:repeat(2,minmax(0,1fr)) !important;
    grid-template-rows:repeat(2,82px) !important;
    gap:8px !important;
    width:100% !important;
    min-height:172px !important;
    max-height:172px !important;
    margin:3px 0 7px !important;
    align-items:stretch !important;
  }

  #setupScreen .game-model-card,
  #setupScreen .smyle-v52-card{
    position:relative !important;
    width:100% !important;
    height:82px !important;
    min-height:82px !important;
    max-height:82px !important;
    min-width:0 !important;
    margin:0 !important;
    padding:9px 12px !important;
    border-radius:18px !important;
    overflow:hidden !important;
    display:grid !important;
    grid-template-columns:42px minmax(0,1fr) auto !important;
    grid-template-rows:auto auto !important;
    grid-template-areas:
      'icon title type'
      'icon desc type' !important;
    column-gap:10px !important;
    row-gap:2px !important;
    align-items:center !important;
    text-align:left !important;
  }

  #setupScreen .game-model-icon,
  #setupScreen .smyle-v52-card .game-model-icon{
    grid-area:icon !important;
    width:42px !important;
    height:42px !important;
    min-width:42px !important;
    min-height:42px !important;
    margin:0 !important;
    border-radius:13px !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    font-size:21px !important;
  }

  #setupScreen .game-model-card strong,
  #setupScreen .smyle-v52-card strong{
    grid-area:title !important;
    min-width:0 !important;
    margin:0 !important;
    font-size:13.5px !important;
    line-height:1.15 !important;
    align-self:end !important;
    white-space:nowrap !important;
    overflow:hidden !important;
    text-overflow:ellipsis !important;
  }

  #setupScreen .game-model-card p,
  #setupScreen .smyle-v52-card p{
    grid-area:desc !important;
    min-width:0 !important;
    margin:0 !important;
    font-size:10.5px !important;
    line-height:1.2 !important;
    align-self:start !important;
    white-space:nowrap !important;
    overflow:hidden !important;
    text-overflow:ellipsis !important;
  }

  #setupScreen .game-model-type,
  #setupScreen .smyle-v52-card .game-model-type{
    grid-area:type !important;
    align-self:center !important;
    justify-self:end !important;
    margin:0 !important;
    padding:5px 7px !important;
    border-radius:999px !important;
    font-size:8.5px !important;
    line-height:1 !important;
    letter-spacing:.07em !important;
    white-space:nowrap !important;
  }

  #setupScreen .v19-category-row,
  #setupScreen .smyle-v52-controls{
    flex:0 0 auto !important;
    display:grid !important;
    grid-template-columns:minmax(0,1fr) auto !important;
    gap:9px !important;
    width:100% !important;
    margin:0 !important;
    align-items:end !important;
  }

  #setupScreen .form-group{
    gap:4px !important;
  }

  #setupScreen label{
    font-size:11px !important;
  }

  #setupScreen select{
    height:42px !important;
    min-height:42px !important;
    font-size:13px !important;
    border-radius:14px !important;
  }

  #setupScreen .v19-new-code-btn{
    height:42px !important;
    min-height:42px !important;
    padding:0 14px !important;
    border-radius:14px !important;
    font-size:12px !important;
    white-space:nowrap !important;
  }

  #setupScreen .model-start-btn,
  #setupScreen .smyle-v52-start{
    flex:0 0 auto !important;
    display:flex !important;
    visibility:visible !important;
    opacity:1 !important;
    width:100% !important;
    height:46px !important;
    min-height:46px !important;
    margin:2px 0 0 !important;
    padding:0 18px !important;
    border-radius:16px !important;
    align-items:center !important;
    justify-content:center !important;
    position:relative !important;
    inset:auto !important;
    z-index:60 !important;
    font-size:13.5px !important;
  }
}

@media (min-width:850px) and (max-height:760px){
  #setupScreen .topbar{min-height:52px !important;}
  #setupScreen .smyle-setup-wordmark{width:105px !important;max-width:105px !important;}
  #setupScreen .start-card{padding:10px 14px !important;gap:5px !important;}
  #setupScreen .panel-title h2{font-size:16.5px !important;}
  #setupScreen .panel-title p{font-size:10.5px !important;}
  #setupScreen .game-model-grid,
  #setupScreen .smyle-v52-grid{
    grid-template-rows:repeat(2,72px) !important;
    min-height:152px !important;
    max-height:152px !important;
    gap:6px !important;
  }
  #setupScreen .game-model-card,
  #setupScreen .smyle-v52-card{
    height:72px !important;
    min-height:72px !important;
    max-height:72px !important;
    padding:7px 10px !important;
  }
  #setupScreen .game-model-icon{width:36px !important;height:36px !important;min-width:36px !important;min-height:36px !important;font-size:18px !important;}
  #setupScreen .game-model-card strong{font-size:12.5px !important;}
  #setupScreen .game-model-card p{font-size:9.5px !important;}
  #setupScreen select,
  #setupScreen .v19-new-code-btn{height:38px !important;min-height:38px !important;}
  #setupScreen .model-start-btn,
  #setupScreen .smyle-v52-start{height:42px !important;min-height:42px !important;}
}
'''

marker = '/* ==== Smyle Lab V53: seletor de jogos como botões compactos ==== */'
if marker not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V53 aplicado: cards dos jogos reduzidos e CTA mantido visível.')
