from pathlib import Path
import re

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

# Home: estrutura mais limpa, inspirada no layout premium de referência.
new_home = '''<div class="smyle-access-eyebrow">SMYLE LAB</div>
            <h2>Bem-vindo(a)</h2>
            <p class="smyle-access-copy">Escolha como deseja entrar no sistema.</p>

            <div class="smyle-access-actions premium-home-actions">
              <button class="entry-btn play" onclick="showScreen('setupScreen')">
                <span class="entry-left entry-copy-only"><strong>Jogar</strong></span>
              </button>

              <button class="entry-btn admin" onclick="openAdminGate()">
                <span class="entry-left entry-copy-only"><strong>Administrador</strong></span>
              </button>
            </div>

            <div class="smyle-access-note">Smyle Lab a sua forma de aprender através de jogos.</div>'''

home_pattern = re.compile(
    r'(?:<div class="smyle-access-eyebrow">.*?</div>\s*)?<h2>Bem-vindo\(a\)</h2>.*?<div class="smyle-access-note">.*?</div>',
    re.S
)
html, home_count = home_pattern.subn(new_home, html, count=1)
print(f'Home premium V33 atualizada: {home_count}')

# Atualiza os pequenos destaques do painel esquerdo sem mexer em outros textos do sistema.
tag_pattern = re.compile(r'<div class="smyle-tag-row">.*?</div>', re.S)
new_tags = '''<div class="smyle-tag-row">
              <span class="smyle-tag">4 experiências</span>
              <span class="smyle-tag">Rodadas rápidas</span>
              <span class="smyle-tag">Resultados</span>
              <span class="smyle-tag">Gestão de conteúdo</span>
            </div>'''
html, tag_count = tag_pattern.subn(new_tags, html, count=1)
print(f'Tags da home atualizadas: {tag_count}')

css = r'''

/* ==== Smyle Lab V33: premium real + formulários refinados ==== */

/* Selects consistentes em todo o sistema */
select{
  -webkit-appearance:none !important;
  -moz-appearance:none !important;
  appearance:none !important;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%230C2340' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m7 10 5 5 5-5'/%3E%3C/svg%3E") !important;
  background-repeat:no-repeat !important;
  background-position:right 16px center !important;
  background-size:17px 17px !important;
  padding-right:48px !important;
}
select::-ms-expand{display:none !important}

/* Modais: sem scrollbar pesada do navegador */
.modal,
.modal.smyle-game-modal,
#questionModal.modal,
#userModal.modal,
#gameModal.modal{
  padding:22px !important;
  overflow:hidden !important;
  background:rgba(7,18,33,.42) !important;
  backdrop-filter:blur(9px) saturate(1.02) !important;
  -webkit-backdrop-filter:blur(9px) saturate(1.02) !important;
}
.modal-card,
.smyle-modal-card,
.content-editor-modal,
.user-modal-card,
.smyle-game-modal-card{
  max-height:calc(100dvh - 44px) !important;
  overflow-y:auto !important;
  overflow-x:hidden !important;
  overscroll-behavior:contain !important;
  scrollbar-width:thin !important;
  scrollbar-color:rgba(12,35,64,.24) transparent !important;
  scrollbar-gutter:stable !important;
  border-radius:26px !important;
  border:1px solid rgba(12,35,64,.08) !important;
  box-shadow:0 30px 90px rgba(6,18,34,.18) !important;
  background:#fff !important;
}
.modal-card::-webkit-scrollbar,
.smyle-modal-card::-webkit-scrollbar,
.content-editor-modal::-webkit-scrollbar,
.user-modal-card::-webkit-scrollbar,
.smyle-game-modal-card::-webkit-scrollbar{
  width:6px !important;
  height:6px !important;
}
.modal-card::-webkit-scrollbar-track,
.smyle-modal-card::-webkit-scrollbar-track,
.content-editor-modal::-webkit-scrollbar-track,
.user-modal-card::-webkit-scrollbar-track,
.smyle-game-modal-card::-webkit-scrollbar-track{
  background:transparent !important;
}
.modal-card::-webkit-scrollbar-thumb,
.smyle-modal-card::-webkit-scrollbar-thumb,
.content-editor-modal::-webkit-scrollbar-thumb,
.user-modal-card::-webkit-scrollbar-thumb,
.smyle-game-modal-card::-webkit-scrollbar-thumb{
  background:rgba(12,35,64,.22) !important;
  border-radius:999px !important;
}
.modal-card::-webkit-scrollbar-thumb:hover,
.smyle-modal-card::-webkit-scrollbar-thumb:hover,
.content-editor-modal::-webkit-scrollbar-thumb:hover,
.user-modal-card::-webkit-scrollbar-thumb:hover,
.smyle-game-modal-card::-webkit-scrollbar-thumb:hover{
  background:rgba(12,35,64,.36) !important;
}
.modal-card::-webkit-scrollbar-button,
.smyle-modal-card::-webkit-scrollbar-button,
.content-editor-modal::-webkit-scrollbar-button,
.user-modal-card::-webkit-scrollbar-button,
.smyle-game-modal-card::-webkit-scrollbar-button{
  display:none !important;
  width:0 !important;
  height:0 !important;
}

/* Cabeçalho e tipografia dos formulários nas cores da marca */
.modal-head{
  position:sticky !important;
  top:0 !important;
  z-index:3 !important;
  margin:-2px -2px 18px !important;
  padding:2px 2px 15px !important;
  background:rgba(255,255,255,.98) !important;
  border-bottom:1px solid rgba(12,35,64,.06) !important;
}
.modal-head h3,
.smyle-modal-card .modal-head h3,
.content-editor-modal .modal-head h3,
.user-modal-card .modal-head h3,
.smyle-game-modal-card .modal-head h3{
  color:#0C2340 !important;
  letter-spacing:-.02em !important;
}
.modal-card label,
.smyle-modal-card label,
.content-editor-modal label,
.user-modal-card label,
.smyle-game-modal-card label{
  color:#18355C !important;
  font-weight:800 !important;
}
.modal-card input:focus,
.modal-card textarea:focus,
.modal-card select:focus,
.smyle-modal-card input:focus,
.smyle-modal-card textarea:focus,
.smyle-modal-card select:focus{
  border-color:#63D9CF !important;
  box-shadow:0 0 0 4px rgba(99,217,207,.12) !important;
  outline:none !important;
}
.content-editor-modal{
  width:min(980px,calc(100vw - 56px)) !important;
  padding:28px 32px !important;
}
.user-modal-card,
.smyle-game-modal-card{
  padding:28px 30px !important;
}

/* HOME: composição dividida, limpa e próxima da referência premium */
#homeScreen.smyle-home-screen{
  min-height:100dvh !important;
  height:100dvh !important;
  padding:0 !important;
  overflow:hidden !important;
  background:#fff !important;
}
#homeScreen > .container{
  width:100% !important;
  max-width:none !important;
  height:100dvh !important;
  padding:0 !important;
  margin:0 !important;
}
#homeScreen .home-wrap.smyle-home{
  width:100% !important;
  height:100dvh !important;
  min-height:100dvh !important;
  display:grid !important;
  grid-template-columns:minmax(0,1.08fr) minmax(440px,.92fr) !important;
  gap:0 !important;
  border:none !important;
  border-radius:0 !important;
  box-shadow:none !important;
  overflow:hidden !important;
  background:#fff !important;
}
#homeScreen .smyle-home .hero{
  height:100dvh !important;
  min-height:0 !important;
  padding:48px 58px 32px !important;
  border-radius:0 !important;
  box-shadow:none !important;
  background:
    radial-gradient(circle at 78% 78%,rgba(99,217,207,.16),transparent 31%),
    radial-gradient(circle at 72% 42%,rgba(255,255,255,.025),transparent 28%),
    linear-gradient(135deg,#18355C 0%,#0C2340 48%,#081A2E 100%) !important;
}
#homeScreen .smyle-wordmark{
  width:150px !important;
  max-width:34% !important;
}
#homeScreen .smyle-hero-main{
  margin:auto 0 !important;
}
#homeScreen .smyle-kicker{
  color:#8FE7DD !important;
  font-size:10px !important;
  letter-spacing:.18em !important;
  margin-bottom:12px !important;
}
#homeScreen .smyle-hero-title{
  color:#fff !important;
  font-size:clamp(46px,5vw,74px) !important;
  line-height:.96 !important;
  letter-spacing:-.055em !important;
  margin-bottom:24px !important;
  max-width:650px !important;
}
#homeScreen .smyle-hero-title .accent{
  color:#63D9CF !important;
  text-shadow:0 0 34px rgba(99,217,207,.08) !important;
}
#homeScreen .smyle-tag-row{
  gap:9px !important;
}
#homeScreen .smyle-tag{
  padding:8px 13px !important;
  border-radius:999px !important;
  border:1px solid rgba(255,255,255,.16) !important;
  background:rgba(255,255,255,.035) !important;
  color:rgba(255,255,255,.94) !important;
  font-size:12px !important;
  font-weight:650 !important;
}
#homeScreen .smyle-hero-footer{
  color:rgba(245,247,248,.58) !important;
  font-size:11px !important;
}

#homeScreen .smyle-side{
  height:100dvh !important;
  min-height:0 !important;
  padding:48px 56px !important;
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  background:#fff !important;
}
#homeScreen .smyle-access-card{
  width:min(430px,100%) !important;
  padding:36px 36px 30px !important;
  border-radius:22px !important;
  border:1px solid #DFE7ED !important;
  background:#fff !important;
  box-shadow:0 22px 64px rgba(8,26,46,.09) !important;
  backdrop-filter:none !important;
  min-height:0 !important;
}
#homeScreen .smyle-access-brand,
#homeScreen .smyle-mini-games,
#homeScreen .smyle-access-highlights,
#homeScreen .smyle-home .entry-icon,
#homeScreen .smyle-home .entry-btn > span:last-child{
  display:none !important;
}
#homeScreen .smyle-access-eyebrow{
  margin:0 0 10px !important;
  color:#39CFC0 !important;
  font-size:10px !important;
  line-height:1 !important;
  font-weight:900 !important;
  letter-spacing:.16em !important;
  text-transform:uppercase !important;
}
#homeScreen .smyle-access-card h2{
  margin:0 0 7px !important;
  color:#0C2340 !important;
  font-size:31px !important;
  line-height:1.08 !important;
  letter-spacing:-.035em !important;
}
#homeScreen .smyle-access-copy{
  margin:0 0 26px !important;
  color:#687D94 !important;
  font-size:14px !important;
  line-height:1.45 !important;
}
#homeScreen .premium-home-actions{
  display:grid !important;
  grid-template-columns:1fr !important;
  gap:12px !important;
  margin:0 0 20px !important;
}
#homeScreen .smyle-home .entry-btn{
  width:100% !important;
  min-height:54px !important;
  height:54px !important;
  padding:0 18px !important;
  border-radius:12px !important;
  justify-content:center !important;
  text-align:center !important;
  box-shadow:none !important;
  position:relative !important;
  overflow:hidden !important;
}
#homeScreen .smyle-home .entry-btn::before{
  content:none !important;
  display:none !important;
}
#homeScreen .smyle-home .entry-btn.play{
  background:linear-gradient(135deg,#63D9CF 0%,#8FE7DD 100%) !important;
  color:#081A2E !important;
}
#homeScreen .smyle-home .entry-btn.admin{
  background:linear-gradient(135deg,#18355C 0%,#0C2340 100%) !important;
  color:#fff !important;
}
#homeScreen .smyle-home .entry-left,
#homeScreen .smyle-home .entry-copy-only{
  width:100% !important;
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  text-align:center !important;
}
#homeScreen .smyle-home .entry-btn strong{
  display:block !important;
  font-size:14px !important;
  font-weight:850 !important;
  letter-spacing:-.01em !important;
}
#homeScreen .smyle-home .entry-btn small{
  display:none !important;
}
#homeScreen .smyle-access-note{
  margin:0 !important;
  padding:0 !important;
  border:none !important;
  border-radius:0 !important;
  background:transparent !important;
  color:#718398 !important;
  font-size:11.5px !important;
  line-height:1.45 !important;
  font-weight:600 !important;
  text-align:left !important;
}

/* Mantém a tela de jogos equilibrada */
#setupScreen > .container{
  width:min(1180px,calc(100vw - 36px)) !important;
  max-width:1180px !important;
}
#setupScreen .start-card{
  max-width:1180px !important;
  margin:0 auto !important;
  padding:24px 26px !important;
  border-radius:28px !important;
}
#setupScreen .smyle-player-code-card,
#setupScreen .smyle-player-code-card span,
#setupScreen .smyle-player-code-card strong{
  text-align:center !important;
}

@media(max-width:980px){
  #homeScreen.smyle-home-screen{overflow:auto !important}
  #homeScreen > .container{height:auto !important;min-height:100dvh !important}
  #homeScreen .home-wrap.smyle-home{
    height:auto !important;
    min-height:100dvh !important;
    grid-template-columns:1fr !important;
    grid-template-rows:minmax(360px,44dvh) minmax(430px,56dvh) !important;
    overflow:visible !important;
  }
  #homeScreen .smyle-home .hero{
    height:auto !important;
    min-height:360px !important;
    padding:34px 42px 26px !important;
  }
  #homeScreen .smyle-side{
    height:auto !important;
    min-height:430px !important;
    padding:34px 32px !important;
  }
  #homeScreen .smyle-access-card{width:min(520px,100%) !important}
}
@media(max-width:620px){
  .modal{padding:10px !important}
  .modal-card,.smyle-modal-card,.content-editor-modal,.user-modal-card,.smyle-game-modal-card{
    max-height:calc(100dvh - 20px) !important;
    border-radius:20px !important;
  }
  .content-editor-modal,.user-modal-card,.smyle-game-modal-card{
    width:calc(100vw - 20px) !important;
    padding:22px 20px !important;
  }
  #homeScreen .home-wrap.smyle-home{grid-template-rows:auto auto !important}
  #homeScreen .smyle-home .hero{padding:28px 24px !important}
  #homeScreen .smyle-hero-title{font-size:clamp(42px,12vw,58px) !important}
  #homeScreen .smyle-side{padding:28px 20px 34px !important;min-height:390px !important}
  #homeScreen .smyle-access-card{padding:30px 26px 26px !important;border-radius:20px !important}
}
'''

if '/* ==== Smyle Lab V33: premium real + formulários refinados ==== */' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V33 aplicado com sucesso.')
