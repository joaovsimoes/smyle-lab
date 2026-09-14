from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

css = r'''

/* ==== Smyle Lab V37: botões sempre visíveis + confirmação de salvamento ==== */
@media (min-width: 901px){
  #questionModal.modal{
    padding:10px 14px !important;
    overflow:hidden !important;
    align-items:center !important;
    justify-content:center !important;
  }

  #questionModal .content-editor-modal{
    position:relative !important;
    width:min(1380px,calc(100vw - 30px)) !important;
    max-width:1380px !important;
    height:min(94dvh,820px) !important;
    max-height:min(94dvh,820px) !important;
    padding:18px 24px 78px !important;
    overflow:hidden !important;
    border-radius:28px !important;
    display:block !important;
  }

  #questionModal .modal-head{
    margin:0 0 10px !important;
    padding:0 0 10px !important;
    min-height:54px !important;
    display:flex !important;
    align-items:center !important;
  }
  #questionModal .modal-head h3{
    font-size:22px !important;
    line-height:1.1 !important;
  }

  #questionModal .form-group{
    gap:4px !important;
    margin:0 !important;
  }
  #questionModal .form-group label,
  #questionModal label{
    font-size:11.5px !important;
    line-height:1.15 !important;
    margin-bottom:2px !important;
  }

  #questionModal input,
  #questionModal select{
    min-height:40px !important;
    height:40px !important;
    padding:7px 12px !important;
    border-radius:13px !important;
    font-size:14px !important;
  }

  #questionModal textarea{
    min-height:64px !important;
    height:64px !important;
    max-height:64px !important;
    padding:9px 12px !important;
    border-radius:13px !important;
    resize:none !important;
    font-size:14px !important;
  }

  #questionModal .dynamic-content-fields{
    display:grid !important;
    grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;
    gap:10px 18px !important;
    align-items:start !important;
    margin:6px 0 0 !important;
  }
  #questionModal .dynamic-content-fields > *{
    min-width:0 !important;
    margin:0 !important;
  }
  #questionModal .dynamic-content-fields .grid-2,
  #questionModal .dynamic-content-fields > .grid-2{
    gap:8px 12px !important;
  }

  #questionModal .sequence-editor-grid,
  #questionModal .dynamic-content-fields .sequence-editor-grid{
    display:grid !important;
    grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;
    gap:12px 18px !important;
  }

  #questionModal .editor-option-row,
  #questionModal .editor-pair-grid{
    gap:7px !important;
    margin-bottom:6px !important;
  }
  #questionModal .editor-option-row input,
  #questionModal .editor-pair-grid input{
    height:38px !important;
    min-height:38px !important;
  }

  #questionModal .content-editor-modal > .form-group[style*="margin-top"]{
    margin-top:8px !important;
  }

  /* Footer sempre visível, sem depender de rolagem */
  #questionModal .content-editor-modal > .grid-2:last-child{
    position:absolute !important;
    left:24px !important;
    right:24px !important;
    bottom:16px !important;
    z-index:12 !important;
    display:grid !important;
    grid-template-columns:1fr 1fr !important;
    gap:12px !important;
    margin:0 !important;
    padding:0 !important;
    background:#fff !important;
    box-shadow:0 -12px 24px rgba(255,255,255,.96) !important;
  }
  #questionModal .content-editor-modal > .grid-2:last-child button{
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    min-height:44px !important;
    height:44px !important;
    margin:0 !important;
    border-radius:13px !important;
  }

  /* Telas mais baixas recebem uma compactação extra */
  @media (max-height: 760px){
    #questionModal .content-editor-modal{
      height:calc(100dvh - 16px) !important;
      max-height:calc(100dvh - 16px) !important;
      padding:14px 20px 68px !important;
    }
    #questionModal .modal-head{
      min-height:44px !important;
      margin-bottom:6px !important;
      padding-bottom:6px !important;
    }
    #questionModal input,
    #questionModal select{
      min-height:36px !important;
      height:36px !important;
      font-size:13px !important;
    }
    #questionModal textarea{
      min-height:54px !important;
      height:54px !important;
      max-height:54px !important;
      font-size:13px !important;
    }
    #questionModal .dynamic-content-fields{
      gap:7px 14px !important;
      margin-top:3px !important;
    }
    #questionModal .content-editor-modal > .grid-2:last-child{
      left:20px !important;
      right:20px !important;
      bottom:12px !important;
    }
    #questionModal .content-editor-modal > .grid-2:last-child button{
      min-height:40px !important;
      height:40px !important;
    }
  }
}

/* Caixa de confirmação */
#smyleContentSavedDialog{
  position:fixed !important;
  inset:0 !important;
  z-index:99999 !important;
  display:none;
  align-items:center !important;
  justify-content:center !important;
  padding:20px !important;
  background:rgba(8,26,46,.42) !important;
  backdrop-filter:blur(8px) !important;
  -webkit-backdrop-filter:blur(8px) !important;
}
#smyleContentSavedDialog.open{display:flex !important}
#smyleContentSavedDialog .smyle-success-card{
  width:min(420px,calc(100vw - 32px)) !important;
  padding:30px 28px 26px !important;
  border-radius:24px !important;
  background:#fff !important;
  border:1px solid rgba(12,35,64,.08) !important;
  box-shadow:0 28px 80px rgba(8,26,46,.22) !important;
  text-align:center !important;
}
#smyleContentSavedDialog .smyle-success-mark{
  width:58px !important;
  height:58px !important;
  margin:0 auto 16px !important;
  border-radius:18px !important;
  display:grid !important;
  place-items:center !important;
  background:linear-gradient(135deg,#63D9CF,#8FE7DD) !important;
  color:#081A2E !important;
  font-size:30px !important;
  font-weight:900 !important;
}
#smyleContentSavedDialog h3{
  margin:0 0 8px !important;
  color:#0C2340 !important;
  font-size:22px !important;
  line-height:1.15 !important;
}
#smyleContentSavedDialog p{
  margin:0 0 20px !important;
  color:#5F7288 !important;
  font-size:14px !important;
  line-height:1.5 !important;
}
#smyleContentSavedDialog button{
  width:100% !important;
  min-height:46px !important;
  border:0 !important;
  border-radius:13px !important;
  background:#0C2340 !important;
  color:#fff !important;
  font-weight:800 !important;
  cursor:pointer !important;
}
'''

if '/* ==== Smyle Lab V37: botões sempre visíveis + confirmação de salvamento ==== */' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

js = r'''
<script>
(function(){
  function ensureSuccessDialog(){
    var existing=document.getElementById('smyleContentSavedDialog');
    if(existing) return existing;

    var overlay=document.createElement('div');
    overlay.id='smyleContentSavedDialog';
    overlay.setAttribute('role','dialog');
    overlay.setAttribute('aria-modal','true');
    overlay.setAttribute('aria-labelledby','smyleSavedTitle');
    overlay.innerHTML=''
      +'<div class="smyle-success-card">'
      +  '<div class="smyle-success-mark">✓</div>'
      +  '<h3 id="smyleSavedTitle">Conteúdo salvo com sucesso</h3>'
      +  '<p>As informações foram registradas no Smyle Lab e já estão disponíveis para uso.</p>'
      +  '<button type="button" id="smyleSavedContinue">Continuar</button>'
      +'</div>';
    document.body.appendChild(overlay);

    function close(){ overlay.classList.remove('open'); }
    overlay.addEventListener('click',function(e){ if(e.target===overlay) close(); });
    overlay.querySelector('#smyleSavedContinue').addEventListener('click',close);
    document.addEventListener('keydown',function(e){ if(e.key==='Escape' && overlay.classList.contains('open')) close(); });
    return overlay;
  }

  window.smyleShowContentSaved=function(){
    var overlay=ensureSuccessDialog();
    overlay.classList.add('open');
    setTimeout(function(){
      var btn=overlay.querySelector('#smyleSavedContinue');
      if(btn) btn.focus();
    },30);
  };

  function modalIsHidden(modal){
    if(!modal) return true;
    var style=window.getComputedStyle(modal);
    return modal.hidden ||
      modal.classList.contains('hidden') ||
      style.display==='none' ||
      style.visibility==='hidden' ||
      modal.offsetParent===null;
  }

  /* Mostra a confirmação somente depois que o salvamento fecha o modal original. */
  document.addEventListener('click',function(e){
    var btn=e.target && e.target.closest ? e.target.closest('button') : null;
    if(!btn) return;
    var text=(btn.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
    if(text!=='salvar conteúdo' && text!=='salvar conteudo') return;

    var modal=btn.closest('#questionModal') || document.getElementById('questionModal');
    var fired=false;
    var observer=null;

    function checkSaved(){
      if(fired) return;
      if(modalIsHidden(modal)){
        fired=true;
        if(observer) observer.disconnect();
        window.smyleShowContentSaved();
      }
    }

    if(modal){
      observer=new MutationObserver(checkSaved);
      observer.observe(modal,{attributes:true,attributeFilter:['class','style','hidden']});
    }
    setTimeout(checkSaved,80);
    setTimeout(function(){ if(observer) observer.disconnect(); },1800);
  },false);

  document.addEventListener('DOMContentLoaded',ensureSuccessDialog);
})();
</script>
'''

if 'smyleShowContentSaved' not in html:
    html = html.replace('</body>', js + '\n</body>')

path.write_text(html, encoding='utf-8')
print('Patch V37 aplicado: formulários compactos, botões visíveis e confirmação de salvamento.')
