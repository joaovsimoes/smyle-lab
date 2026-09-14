from pathlib import Path
import re

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

# Substitui resíduos da paleta vermelha/original pela paleta oficial Smyle Lab.
replacements = {
    '#99001a':'#0C2340',
    '#99001A':'#0C2340',
    '#e2001b':'#63D9CF',
    '#E2001B':'#63D9CF',
    '#4c0f0f':'#081A2E',
    '#4C0F0F':'#081A2E',
    '#c10020':'#0C2340',
    '#C10020':'#0C2340',
    '#ff6e86':'#63D9CF',
    '#FF6E86':'#63D9CF',
    '#ffcccc':'#DDF6F3',
    '#FFCCCC':'#DDF6F3',
    '#ffe3e8':'#EAF9F7',
    '#FFE3E8':'#EAF9F7',
    '#fff5f5':'#F7FAFB',
    '#FFF5F5':'#F7FAFB',
    '#fff5f7':'#F7FAFB',
    '#FFF5F7':'#F7FAFB',
    '#fff0f2':'#F3F9F8',
    '#FFF0F2':'#F3F9F8',
    '#ffdde4':'#EAF9F7',
    '#FFDDE4':'#EAF9F7',
    '#ffebee':'#EAF9F7',
    '#FFEBEE':'#EAF9F7',
    '#8a4b56':'#5F7288',
    '#8A4B56':'#5F7288',
    '#6f2b36':'#5F7288',
    '#6F2B36':'#5F7288',
    '#FDB022':'#63D9CF',
    '#fdb022':'#63D9CF',
    '#936109':'#0C2340',
}
for old, new in replacements.items():
    html = html.replace(old, new)

# Tons vermelhos/rosados translúcidos.
rgba_replacements = {
    'rgba(226,0,27,':'rgba(99,217,207,',
    'rgba(153,0,26,':'rgba(12,35,64,',
    'rgba(255,204,204,':'rgba(143,231,221,',
    'rgba(239,68,68,':'rgba(12,35,64,',
    'rgba(245,158,11,':'rgba(99,217,207,',
    'rgba(249,115,22,':'rgba(99,217,207,',
    'rgba(251,146,60,':'rgba(99,217,207,',
}
for old, new in rgba_replacements.items():
    html = html.replace(old, new)

css = r'''

/* ==== Smyle Lab V34: Brand UI + modais sem rolagem interna ==== */

/* Paleta oficial em toda a interface */
body{
  background:
    radial-gradient(circle at 15% 10%,rgba(99,217,207,.10),transparent 24%),
    radial-gradient(circle at 85% 85%,rgba(143,231,221,.12),transparent 28%),
    #F5F7F8 !important;
}
label,
.form-group label,
.smyle-admin-main label,
#admin-settings label,
.modal-card label,
.settings-general-card label{
  color:#0C2340 !important;
}
input:focus,select:focus,textarea:focus{
  border-color:#63D9CF !important;
  box-shadow:0 0 0 3px rgba(99,217,207,.15) !important;
}
.ghost-btn:hover,.back-btn:hover,.secondary-btn:hover{
  background:rgba(99,217,207,.10) !important;
  border-color:rgba(99,217,207,.30) !important;
}

/* Seleções do painel na mesma linguagem dos jogos */
.smyle-side-nav .side-link.active,
.v19-game-nav .game-admin-link.active{
  background:linear-gradient(135deg,#63D9CF,#8FE7DD) !important;
  color:#081A2E !important;
  box-shadow:0 8px 18px rgba(99,217,207,.14) !important;
}
#admin-settings .settings-tab.active,
.settings-tab.active{
  background:linear-gradient(135deg,#63D9CF,#8FE7DD) !important;
  color:#081A2E !important;
  border-color:transparent !important;
}

/* Elementos do jogo 100% dentro da identidade Smyle */
.eyebrow{
  color:#0C2340 !important;
  background:rgba(99,217,207,.14) !important;
  border-color:rgba(99,217,207,.30) !important;
}
.hero:before{background:radial-gradient(circle,rgba(99,217,207,.14),transparent 62%) !important}
.hero p,.feedback p{color:#5F7288 !important}
.mini-stat{background:#F7FAFB !important;color:#5F7288 !important}
.chip{color:#0C2340 !important}
.chip.active{
  border-color:#63D9CF !important;
  background:#EAF9F7 !important;
  color:#081A2E !important;
}
.progress-wrap{background:#EAF9F7 !important}
.progress{background:linear-gradient(90deg,#63D9CF,#8FE7DD) !important}
.answer-btn.fact{
  background:linear-gradient(135deg,#63D9CF,#8FE7DD) !important;
  color:#081A2E !important;
}
.answer-btn.fake{
  background:linear-gradient(135deg,#0C2340,#081A2E) !important;
  color:#fff !important;
}
.score-pill{
  color:#0C2340 !important;
  background:#EAF9F7 !important;
  border-color:rgba(99,217,207,.28) !important;
}
.result-score{color:#0C2340 !important}
.mission-card{
  border-color:rgba(99,217,207,.30) !important;
  background:linear-gradient(135deg,rgba(99,217,207,.12),rgba(143,231,221,.08)) !important;
}
.mission-icon{background:rgba(99,217,207,.18) !important}
.mission-card strong,.arena-head strong,.round-kicker{color:#0C2340 !important}
.belt-step{color:#5F7288 !important}
.belt-step:after{background:#DDF6F3 !important}
.belt-step.active{
  border-color:#63D9CF !important;
  background:#EAF9F7 !important;
  color:#081A2E !important;
  box-shadow:0 0 0 3px rgba(99,217,207,.14),0 0 24px rgba(99,217,207,.10) !important;
}
.belt-step.done{
  background:linear-gradient(135deg,#0C2340,#081A2E) !important;
  border-color:#0C2340 !important;
  color:#fff !important;
}
.belt-step.done:after{background:#63D9CF !important}
.streak-pill,.combo-note{
  color:#0C2340 !important;
  background:rgba(99,217,207,.12) !important;
  border-color:rgba(99,217,207,.22) !important;
}
.sound-toggle{
  background:#F3FBFA !important;
  color:#0C2340 !important;
  border-color:rgba(99,217,207,.24) !important;
}
.sound-toggle:hover{background:#EAF9F7 !important;border-color:#63D9CF !important}
.question-card:before{background:radial-gradient(circle,rgba(99,217,207,.13),transparent 66%) !important}
.feedback.wrong{
  border-color:rgba(12,35,64,.16) !important;
  background:rgba(12,35,64,.045) !important;
}
.bar{background:#DDF6F3 !important}
.bar>span{background:linear-gradient(90deg,#63D9CF,#8FE7DD) !important}
.rank-row{background:#FAFCFD !important}

/* Modais: caixa maior e sem scrollbar interna pesada */
.modal{
  padding:12px 16px !important;
  overflow:hidden !important;
  align-items:center !important;
  justify-items:center !important;
}
.modal-card,
.smyle-modal-card,
.content-editor-modal,
.user-modal-card,
.smyle-game-modal-card{
  overflow:visible !important;
  scrollbar-width:none !important;
}
.modal-card::-webkit-scrollbar,
.smyle-modal-card::-webkit-scrollbar,
.content-editor-modal::-webkit-scrollbar,
.user-modal-card::-webkit-scrollbar,
.smyle-game-modal-card::-webkit-scrollbar{
  width:0 !important;
  height:0 !important;
  display:none !important;
}
.modal-head{
  position:relative !important;
  top:auto !important;
  margin-bottom:12px !important;
  padding-bottom:10px !important;
  border-bottom:1px solid rgba(12,35,64,.07) !important;
}
.modal-head h3,
.smyle-modal-card h3,
.smyle-game-modal-card .modal-head h3{
  color:#0C2340 !important;
}

/* Conteúdo/perguntas: aproveita largura, reduz altura e elimina rolagem interna */
#questionModal .content-editor-modal{
  width:min(1120px,calc(100vw - 30px)) !important;
  max-width:1120px !important;
  max-height:calc(100dvh - 24px) !important;
  padding:18px 22px 20px !important;
  overflow:hidden !important;
}
#questionModal .content-editor-modal > .grid-2{
  gap:14px !important;
  margin-top:6px !important;
}
#questionModal .dynamic-content-fields{
  display:grid !important;
  grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;
  gap:12px 16px !important;
  align-items:start !important;
  margin-top:10px !important;
}
#questionModal .dynamic-content-fields > *{margin:0 !important;min-width:0}
#questionModal .dynamic-content-fields > .grid-2{
  gap:10px !important;
  align-self:start !important;
}
#questionModal .form-group{gap:5px !important}
#questionModal label{font-size:12px !important}
#questionModal input,#questionModal select{
  min-height:42px !important;
  height:42px !important;
  padding-top:8px !important;
  padding-bottom:8px !important;
}
#questionModal textarea{
  min-height:72px !important;
  height:72px !important;
  max-height:72px !important;
  resize:none !important;
  padding:10px 12px !important;
}
#questionModal .editor-option-row,
#questionModal .editor-pair-grid{
  gap:8px !important;
  margin-bottom:6px !important;
}
#questionModal .editor-option-row input,
#questionModal .editor-pair-grid input{height:40px !important}
#questionModal .content-editor-modal > .form-group[style*="margin-top"]{margin-top:10px !important}
#questionModal .content-editor-modal > .grid-2:last-child{margin-top:12px !important}
#questionModal .content-editor-modal > .grid-2:last-child button{min-height:42px !important;padding:10px 14px !important}

/* Cadastro/edição de jogos também ocupa melhor o espaço */
#gameModal .smyle-game-modal-card{
  width:min(1080px,calc(100vw - 30px)) !important;
  max-width:1080px !important;
  max-height:calc(100dvh - 24px) !important;
  padding:18px 22px !important;
  overflow:hidden !important;
}
#gameModal .game-modal-grid{gap:12px 16px !important}
#gameModal .form-group{gap:5px !important}
#gameModal label{font-size:12px !important}
#gameModal input,#gameModal select{height:42px !important;min-height:42px !important}
#gameModal textarea{min-height:66px !important;height:66px !important;resize:none !important}
#gameModal .field-help{font-size:10px !important;margin-top:2px !important}
#gameModal .mechanic-help-card{margin-top:10px !important;padding:10px 12px !important;gap:10px !important}
#gameModal .mechanic-help-icon{width:36px !important;height:36px !important;border-radius:12px !important;font-size:17px !important}
#gameModal .game-modal-footer{position:relative !important;bottom:auto !important;margin-top:10px !important;padding:6px 0 0 !important}

/* Usuários e demais formulários */
#userModal .user-modal-card{
  width:min(980px,calc(100vw - 30px)) !important;
  max-width:980px !important;
  max-height:calc(100dvh - 24px) !important;
  overflow:hidden !important;
  padding:20px 22px !important;
}
#userModal .form-group{gap:5px !important}
#userModal input,#userModal select{min-height:42px !important;height:42px !important}

/* Evita títulos/labels antigos em vinho dentro do admin */
.smyle-admin-main h1,
.smyle-admin-main h2,
.smyle-admin-main h3,
.smyle-admin-main h4,
.smyle-admin-main .panel-title h2,
.smyle-admin-main .form-group label,
#admin-settings h2,
#admin-settings h3,
#admin-settings label{
  color:#0C2340 !important;
}

@media(max-width:900px){
  .modal{overflow:auto !important;align-items:flex-start !important;padding:10px !important}
  #questionModal .content-editor-modal,
  #gameModal .smyle-game-modal-card,
  #userModal .user-modal-card{
    width:min(100%,760px) !important;
    max-height:none !important;
    overflow:visible !important;
  }
  #questionModal .dynamic-content-fields{grid-template-columns:1fr !important}
  #questionModal textarea{height:82px !important;max-height:82px !important}
}
'''

if '/* ==== Smyle Lab V34: Brand UI + modais sem rolagem interna ==== */' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V34 aplicado: cores da marca, seleção mint e modais sem rolagem interna.')
