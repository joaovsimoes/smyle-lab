from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')
html = path.read_text(encoding='utf-8')

css = r'''

/* ==== Smyle Lab V35: compact forms + one-screen games ==== */

/* Visão Geral: remove ações redundantes do topo */
#admin-dashboard .panel-title > div:last-child,
#admin-dashboard .panel-title .secondary-btn,
#admin-dashboard .panel-title .primary-btn{
  display:none !important;
}

/* Modais mais largos e compactos, sem barra interna no desktop */
@media (min-width: 901px){
  .modal{
    padding:12px !important;
    overflow:hidden !important;
  }
  .modal-card,
  .smyle-modal-card,
  .content-editor-modal,
  .user-modal-card,
  .smyle-game-modal-card{
    width:min(1480px, calc(100vw - 32px)) !important;
    max-width:1480px !important;
    max-height:calc(100dvh - 24px) !important;
    overflow:hidden !important;
    padding:24px 28px 22px !important;
    display:flex !important;
    flex-direction:column !important;
  }
  .modal-head{
    position:relative !important;
    top:auto !important;
    margin-bottom:12px !important;
    padding-bottom:10px !important;
    flex:0 0 auto !important;
  }
  .modal-head h3{font-size:22px !important;color:#0C2340 !important}
  .modal-card .form-group{gap:5px !important}
  .modal-card label{font-size:12.5px !important;color:#0C2340 !important}
  .modal-card input,
  .modal-card select{
    min-height:46px !important;
    height:46px !important;
    padding:9px 14px !important;
    border-radius:14px !important;
  }
  .modal-card textarea{
    min-height:78px !important;
    max-height:96px !important;
    padding:11px 14px !important;
    border-radius:14px !important;
  }
  .modal-card .grid-2{gap:14px !important}
  .modal-card .form-group[style*="margin-top"]{margin-top:10px !important}
  .dynamic-content-fields{margin-top:0 !important}
  .content-editor-modal > .grid-2:first-of-type{grid-template-columns:1fr 1fr !important}
  .content-editor-modal .dynamic-content-fields .grid-2,
  .content-editor-modal .dynamic-content-fields > .grid-2{
    gap:14px !important;
  }
  .content-editor-modal > .grid-2:last-child,
  .game-modal-footer,
  .user-modal-actions{
    position:relative !important;
    bottom:auto !important;
    margin-top:12px !important;
    padding-top:10px !important;
    background:#fff !important;
    flex:0 0 auto !important;
  }
  .content-editor-modal > .grid-2:last-child button,
  .game-modal-footer button,
  .user-modal-actions button{
    min-height:44px !important;
  }

  /* Desembaralha e demais editores: usar melhor a largura */
  .sequence-editor-grid,
  .dynamic-content-fields .sequence-editor-grid{
    grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;
    gap:18px !important;
  }
  .dynamic-content-fields input{height:44px !important}
}

/* Mobile/tablet: mantém rolagem apenas quando realmente necessária */
@media (max-width:900px){
  .modal{padding:10px !important;overflow:auto !important}
  .modal-card,
  .smyle-modal-card,
  .content-editor-modal,
  .user-modal-card,
  .smyle-game-modal-card{
    width:min(96vw, 900px) !important;
    max-height:none !important;
    overflow:visible !important;
    padding:20px !important;
  }
}

/* Jogos: tudo em uma única tela */
#gameScreen{
  height:100dvh !important;
  min-height:100dvh !important;
  overflow:hidden !important;
  padding:0 !important;
}
#gameScreen > .container.game-shell{
  width:min(1180px, calc(100vw - 28px)) !important;
  max-width:1180px !important;
  height:100dvh !important;
  margin:0 auto !important;
  padding:14px 0 !important;
  display:flex !important;
  flex-direction:column !important;
  justify-content:center !important;
  overflow:hidden !important;
}
#gameScreen .game-top{
  margin-bottom:8px !important;
  gap:12px !important;
  flex:0 0 auto !important;
}
#gameScreen .progress-wrap{height:8px !important}
#gameScreen .question-card{
  margin-top:8px !important;
  padding:20px 24px !important;
  border-radius:24px !important;
  max-height:calc(100dvh - 105px) !important;
  overflow:hidden !important;
  display:flex !important;
  flex-direction:column !important;
  justify-content:center !important;
}
#gameScreen .question-meta{margin-bottom:8px !important;font-size:11px !important}
#gameScreen .round-kicker{margin-bottom:5px !important;font-size:10px !important}
#gameScreen .question-text,
#gameScreen .model-prompt{
  font-size:clamp(20px,2.5vw,32px) !important;
  line-height:1.15 !important;
  margin:8px 0 16px !important;
}
#gameScreen .answer-grid{gap:12px !important}
#gameScreen .answer-btn{
  min-height:76px !important;
  padding:18px !important;
  border-radius:18px !important;
  font-size:18px !important;
}
#gameScreen .feedback{
  margin-top:10px !important;
  padding:12px 14px !important;
  border-radius:14px !important;
}
#gameScreen .feedback strong{font-size:16px !important}
#gameScreen .feedback p{font-size:12px !important;line-height:1.4 !important;margin-top:4px !important}
#gameScreen .mission-card{min-height:54px !important;padding:10px 12px !important}
#gameScreen .mission-icon{width:36px !important;height:36px !important;flex-basis:36px !important}
#gameScreen .arena-head{margin:8px 0 4px !important}
#gameScreen .belt-track{margin:8px 0 10px !important;gap:7px !important}
#gameScreen .belt-step{height:34px !important;border-radius:10px !important}
#gameScreen .sequence-workspace,
#gameScreen .matching-workspace{
  gap:10px !important;
  margin-top:8px !important;
}
#gameScreen .sequence-zone,
#gameScreen .matching-zone{
  padding:12px !important;
  border-radius:16px !important;
}
#gameScreen .sequence-chip,
#gameScreen .match-chip{
  padding:9px 11px !important;
  font-size:12px !important;
  border-radius:11px !important;
}
#gameScreen .sequence-actions{margin-top:8px !important;gap:8px !important}

@media (max-height:760px){
  #gameScreen > .container.game-shell{padding:8px 0 !important}
  #gameScreen .question-card{padding:14px 18px !important;max-height:calc(100dvh - 72px) !important}
  #gameScreen .question-text,#gameScreen .model-prompt{font-size:clamp(18px,2.2vw,26px) !important;margin:5px 0 10px !important}
  #gameScreen .answer-btn{min-height:62px !important;padding:13px !important;font-size:16px !important}
  #gameScreen .feedback{padding:9px 11px !important}
}
'''

if '/* ==== Smyle Lab V35: compact forms + one-screen games ==== */' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

js = r'''
<script>
(function(){
  function cleanDashboardActions(){
    document.querySelectorAll('#admin-dashboard button').forEach(function(btn){
      var t=(btn.textContent||'').trim().toLowerCase();
      if(t==='gerenciar jogos' || t.indexOf('nova pergunta')!==-1){
        btn.style.display='none';
      }
    });
  }
  document.addEventListener('DOMContentLoaded', cleanDashboardActions);
  window.addEventListener('load', cleanDashboardActions);
  setTimeout(cleanDashboardActions,400);
})();
</script>
'''
if 'cleanDashboardActions' not in html:
    html = html.replace('</body>', js + '\n</body>')

path.write_text(html, encoding='utf-8')
print('Patch V35 aplicado.')
