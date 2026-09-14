from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

css = r'''

/* ==== Smyle Lab V54: seletor uniforme + categoria legível ==== */
@media (min-width: 850px){
  #setupScreen{
    height:100dvh !important;
    min-height:100dvh !important;
    overflow:hidden !important;
    padding:10px 14px 14px !important;
  }

  #setupScreen > .container{
    height:auto !important;
    min-height:0 !important;
    max-height:100% !important;
    display:flex !important;
    flex-direction:column !important;
    justify-content:flex-start !important;
    overflow:visible !important;
  }

  #setupScreen .topbar{
    min-height:64px !important;
    margin-bottom:8px !important;
  }

  #setupScreen .start-card{
    flex:0 0 auto !important;
    height:auto !important;
    min-height:0 !important;
    max-height:none !important;
    padding:16px 18px 18px !important;
    gap:8px !important;
    overflow:visible !important;
  }

  #setupScreen .game-model-grid,
  #setupScreen .smyle-v52-grid{
    grid-template-columns:repeat(2,minmax(0,1fr)) !important;
    grid-template-rows:repeat(2,82px) !important;
    min-height:172px !important;
    max-height:172px !important;
    margin:4px 0 8px !important;
  }

  #setupScreen .game-model-card,
  #setupScreen .smyle-v52-card{
    height:82px !important;
    min-height:82px !important;
    max-height:82px !important;
  }

  /* Corrige texto cortado no select de categoria */
  #setupScreen select{
    box-sizing:border-box !important;
    height:46px !important;
    min-height:46px !important;
    line-height:1.2 !important;
    padding:0 44px 0 16px !important;
    font-size:13.5px !important;
    text-indent:0 !important;
    vertical-align:middle !important;
    overflow:visible !important;
  }

  #setupScreen .form-group{
    min-height:0 !important;
    gap:5px !important;
  }

  #setupScreen .v19-category-row,
  #setupScreen .smyle-v52-controls{
    margin-top:2px !important;
    align-items:end !important;
  }

  #setupScreen .v19-new-code-btn{
    height:46px !important;
    min-height:46px !important;
  }

  #setupScreen .model-start-btn,
  #setupScreen .smyle-v52-start{
    height:50px !important;
    min-height:50px !important;
    margin-top:4px !important;
  }

  /* Evita o grande vazio criado pelo card ocupando toda a viewport */
  #setupScreen .start-card::after{
    content:none !important;
    display:none !important;
  }
}

@media (min-width:850px) and (max-height:760px){
  #setupScreen .topbar{min-height:54px !important;margin-bottom:5px !important;}
  #setupScreen .start-card{padding:12px 14px 14px !important;gap:6px !important;}
  #setupScreen .game-model-grid,
  #setupScreen .smyle-v52-grid{
    grid-template-rows:repeat(2,72px) !important;
    min-height:150px !important;
    max-height:150px !important;
    margin-bottom:6px !important;
  }
  #setupScreen .game-model-card,
  #setupScreen .smyle-v52-card{
    height:72px !important;
    min-height:72px !important;
    max-height:72px !important;
  }
  #setupScreen select,
  #setupScreen .v19-new-code-btn{height:42px !important;min-height:42px !important;}
  #setupScreen .model-start-btn,
  #setupScreen .smyle-v52-start{height:44px !important;min-height:44px !important;}
}
'''

marker = '/* ==== Smyle Lab V54: seletor uniforme + categoria legível ==== */'
if marker not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V54 aplicado: categoria legível e seletor sem espaço vazio excessivo.')
