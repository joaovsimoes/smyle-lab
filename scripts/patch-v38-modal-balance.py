from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

css = r'''

/* ==== Smyle Lab V38: modal proporcional + rolagem invisível ==== */
@media (min-width: 901px){
  /* A rolagem, quando necessária, acontece no overlay e não dentro da caixa. */
  #questionModal.modal{
    padding:18px 20px !important;
    overflow-y:auto !important;
    overflow-x:hidden !important;
    align-items:flex-start !important;
    justify-content:center !important;
    scrollbar-width:none !important;
  }
  #questionModal.modal::-webkit-scrollbar{
    width:0 !important;
    height:0 !important;
    display:none !important;
  }

  /* Volta para uma caixa equilibrada, sem ocupar a tela inteira. */
  #questionModal .content-editor-modal{
    position:relative !important;
    width:min(1120px,calc(100vw - 40px)) !important;
    max-width:1120px !important;
    height:auto !important;
    min-height:0 !important;
    max-height:none !important;
    margin:auto !important;
    padding:20px 24px 22px !important;
    overflow:visible !important;
    display:block !important;
    border-radius:28px !important;
  }

  #questionModal .modal-head{
    position:relative !important;
    top:auto !important;
    z-index:auto !important;
    min-height:0 !important;
    margin:0 0 14px !important;
    padding:0 0 12px !important;
    background:transparent !important;
  }
  #questionModal .modal-head h3{
    font-size:22px !important;
    line-height:1.15 !important;
  }

  #questionModal .form-group{
    gap:5px !important;
    margin:0 !important;
  }
  #questionModal .form-group label,
  #questionModal label{
    font-size:12px !important;
    line-height:1.2 !important;
    margin-bottom:3px !important;
  }

  #questionModal input,
  #questionModal select{
    min-height:42px !important;
    height:42px !important;
    padding:8px 13px !important;
    border-radius:13px !important;
    font-size:14px !important;
  }
  #questionModal textarea{
    min-height:72px !important;
    height:72px !important;
    max-height:72px !important;
    padding:10px 13px !important;
    border-radius:13px !important;
    resize:none !important;
    font-size:14px !important;
  }

  #questionModal .dynamic-content-fields{
    display:grid !important;
    grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;
    gap:12px 18px !important;
    align-items:start !important;
    margin:8px 0 0 !important;
  }
  #questionModal .dynamic-content-fields > *{
    min-width:0 !important;
    margin:0 !important;
  }
  #questionModal .dynamic-content-fields .grid-2,
  #questionModal .dynamic-content-fields > .grid-2{
    gap:10px 12px !important;
  }
  #questionModal .sequence-editor-grid,
  #questionModal .dynamic-content-fields .sequence-editor-grid{
    display:grid !important;
    grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;
    gap:14px 18px !important;
  }
  #questionModal .editor-option-row,
  #questionModal .editor-pair-grid{
    gap:8px !important;
    margin-bottom:6px !important;
  }
  #questionModal .editor-option-row input,
  #questionModal .editor-pair-grid input{
    min-height:40px !important;
    height:40px !important;
  }

  #questionModal .content-editor-modal > .form-group[style*="margin-top"]{
    margin-top:10px !important;
  }

  /* Botões voltam para o fluxo normal do formulário. */
  #questionModal .content-editor-modal > .grid-2:last-child{
    position:relative !important;
    left:auto !important;
    right:auto !important;
    bottom:auto !important;
    z-index:auto !important;
    display:grid !important;
    grid-template-columns:1fr 1fr !important;
    gap:12px !important;
    margin:14px 0 0 !important;
    padding:0 !important;
    background:transparent !important;
    box-shadow:none !important;
  }
  #questionModal .content-editor-modal > .grid-2:last-child button{
    min-height:44px !important;
    height:44px !important;
    margin:0 !important;
    border-radius:13px !important;
  }

  @media (max-height: 760px){
    #questionModal.modal{padding:10px 16px !important;}
    #questionModal .content-editor-modal{
      width:min(1040px,calc(100vw - 32px)) !important;
      max-width:1040px !important;
      padding:16px 20px 18px !important;
    }
    #questionModal .modal-head{margin-bottom:8px !important;padding-bottom:8px !important;}
    #questionModal input,
    #questionModal select{
      min-height:38px !important;
      height:38px !important;
      font-size:13px !important;
    }
    #questionModal textarea{
      min-height:58px !important;
      height:58px !important;
      max-height:58px !important;
      font-size:13px !important;
    }
    #questionModal .dynamic-content-fields{gap:8px 14px !important;margin-top:5px !important;}
    #questionModal .content-editor-modal > .grid-2:last-child{margin-top:10px !important;}
    #questionModal .content-editor-modal > .grid-2:last-child button{height:40px !important;min-height:40px !important;}
  }
}
'''

if '/* ==== Smyle Lab V38: modal proporcional + rolagem invisível ==== */' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V38 aplicado: modal proporcional com rolagem invisível no overlay.')
