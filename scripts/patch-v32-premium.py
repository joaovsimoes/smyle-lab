from pathlib import Path
import re

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

new_home = '''<h2>Bem-vindo(a)</h2>
            <p class="smyle-access-copy">Escolha como deseja entrar no sistema.</p>

            <div class="smyle-access-actions premium-home-actions">
              <button class="entry-btn play" onclick="showScreen('setupScreen')">
                <span class="entry-left entry-copy-only">
                  <span><strong>Jogar</strong><small>Inicie uma rodada com os jogos disponíveis.</small></span>
                </span>
              </button>

              <button class="entry-btn admin" onclick="openAdminGate()">
                <span class="entry-left entry-copy-only">
                  <span><strong>Administrador</strong><small>Acesse o painel para gerenciar jogos e relatórios.</small></span>
                </span>
              </button>
            </div>

            <div class="smyle-access-highlights" aria-hidden="true">
              <div class="smyle-highlight-card">
                <strong>Rodadas rápidas</strong>
                <span>Comece em poucos cliques.</span>
              </div>
              <div class="smyle-highlight-card">
                <strong>Painel completo</strong>
                <span>Organize jogos, conteúdos e resultados.</span>
              </div>
            </div>

            <div class="smyle-access-note">Smyle Lab a sua forma de aprender através de jogos.</div>'''

pattern = re.compile(
    r'<h2>Bem-vindo\(a\)</h2>.*?<div class="smyle-access-note">.*?</div>',
    re.S
)
html, count = pattern.subn(new_home, html, count=1)
print(f'Home atualizada: {count}')

css = r'''

/* ==== Smyle Lab V32 premium ==== */
select{
  -webkit-appearance:none !important;
  -moz-appearance:none !important;
  appearance:none !important;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%230C2340' stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E") !important;
  background-repeat:no-repeat !important;
  background-position:right 18px center !important;
  background-size:16px !important;
  padding-right:52px !important;
}
select::-ms-expand{display:none !important}

.modal,
.modal.smyle-game-modal,
#questionModal.modal,
#userModal.modal,
#gameModal.modal{
  background:rgba(7,18,33,.46) !important;
  backdrop-filter:blur(10px) saturate(1.05) !important;
  -webkit-backdrop-filter:blur(10px) saturate(1.05) !important;
}
.modal-card,
.smyle-modal-card,
.content-editor-modal,
.user-modal-card,
.smyle-game-modal-card{
  border-radius:30px !important;
  border:1px solid rgba(255,255,255,.55) !important;
  box-shadow:0 30px 90px rgba(6,18,34,.18),0 8px 24px rgba(6,18,34,.10) !important;
  background:linear-gradient(180deg,#fff 0%,#fbfcfd 100%) !important;
}
.modal-head{
  position:sticky !important;
  top:-1px !important;
  z-index:2 !important;
  background:linear-gradient(180deg,#fff 0%,rgba(255,255,255,.96) 100%) !important;
  padding-bottom:14px !important;
}

#homeScreen.smyle-home-screen{
  background:
    radial-gradient(circle at 78% 18%,rgba(99,217,207,.14),transparent 22%),
    radial-gradient(circle at 18% 78%,rgba(99,217,207,.09),transparent 18%),
    linear-gradient(135deg,#F3F7F8 0%,#EEF4F5 52%,#F8F6F7 100%) !important;
}
#homeScreen .home-wrap.smyle-home{
  grid-template-columns:minmax(0,1.12fr) minmax(430px,575px) !important;
  gap:18px !important;
  background:transparent !important;
  border:none !important;
  box-shadow:none !important;
  overflow:visible !important;
}
#homeScreen .smyle-home .hero{
  border-radius:34px !important;
  box-shadow:0 18px 56px rgba(8,26,46,.10) !important;
}
#homeScreen .smyle-side{
  padding:0 !important;
  background:transparent !important;
  justify-content:center !important;
}
#homeScreen .smyle-access-card{
  width:min(575px,100%) !important;
  padding:34px 32px 28px !important;
  border-radius:34px !important;
  border:1px solid rgba(255,255,255,.62) !important;
  background:linear-gradient(180deg,rgba(255,255,255,.90) 0%,rgba(255,255,255,.82) 100%) !important;
  box-shadow:0 24px 70px rgba(8,26,46,.09) !important;
  backdrop-filter:blur(12px) !important;
  min-height:0 !important;
}
#homeScreen .smyle-access-brand,
#homeScreen .smyle-mini-games,
#homeScreen .smyle-home .entry-icon,
#homeScreen .smyle-home .entry-btn > span:last-child{
  display:none !important;
}
#homeScreen .smyle-access-card h2{
  font-size:30px !important;
  margin:0 0 6px !important;
  letter-spacing:-.03em !important;
}
#homeScreen .smyle-access-copy{
  margin:0 0 20px !important;
  font-size:15.5px !important;
  color:#5F7288 !important;
}
#homeScreen .premium-home-actions{
  display:grid !important;
  grid-template-columns:1fr 1fr !important;
  gap:14px !important;
  margin-bottom:14px !important;
}
#homeScreen .smyle-home .entry-btn{
  min-height:126px !important;
  padding:22px 20px !important;
  border-radius:26px !important;
  justify-content:center !important;
  text-align:center !important;
  box-shadow:0 18px 34px rgba(8,26,46,.08) !important;
  position:relative !important;
  overflow:hidden !important;
}
#homeScreen .smyle-home .entry-btn::before{
  content:"" !important;
  position:absolute !important;
  right:-13% !important;
  bottom:-45% !important;
  width:110px !important;
  height:110px !important;
  border-radius:999px !important;
  background:rgba(255,255,255,.18) !important;
}
#homeScreen .smyle-home .entry-btn.play{
  background:linear-gradient(135deg,#63D9CF 0%,#8FE7DD 100%) !important;
}
#homeScreen .smyle-home .entry-btn.admin{
  background:linear-gradient(135deg,#0C2340 0%,#102C52 100%) !important;
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
  font-size:21px !important;
}
#homeScreen .smyle-home .entry-btn small{
  display:block !important;
  margin-top:7px !important;
  font-size:13px !important;
  line-height:1.45 !important;
  max-width:200px !important;
}
#homeScreen .smyle-access-highlights{
  display:grid !important;
  grid-template-columns:1fr 1fr !important;
  gap:12px !important;
  margin:0 0 16px !important;
}
#homeScreen .smyle-highlight-card{
  padding:14px !important;
  border-radius:18px !important;
  background:rgba(247,250,251,.94) !important;
  border:1px solid rgba(12,35,64,.07) !important;
}
#homeScreen .smyle-highlight-card strong{
  display:block !important;
  color:#081A2E !important;
  font-size:13px !important;
  margin-bottom:5px !important;
}
#homeScreen .smyle-highlight-card span{
  display:block !important;
  color:#667B92 !important;
  font-size:12.5px !important;
  line-height:1.45 !important;
}
#homeScreen .smyle-access-note{
  margin-top:0 !important;
  padding:14px 16px !important;
  text-align:center !important;
  border-radius:18px !important;
  background:linear-gradient(180deg,#F8FBFC 0%,#F3F7F8 100%) !important;
  border:1px solid rgba(12,35,64,.06) !important;
  color:#5B748E !important;
  font-size:13.5px !important;
  font-weight:800 !important;
}

#setupScreen > .container{
  width:min(1180px,calc(100vw - 36px)) !important;
  max-width:1180px !important;
}
#setupScreen .start-card{
  max-width:1180px !important;
  margin:0 auto !important;
  padding:24px 26px !important;
  border-radius:30px !important;
}
#setupScreen .smyle-player-code-card{
  text-align:center !important;
  align-items:center !important;
  justify-content:center !important;
}
#setupScreen .smyle-player-code-card span,
#setupScreen .smyle-player-code-card strong{
  display:block !important;
  width:100% !important;
  text-align:center !important;
}

@media(max-width:1200px){
  #homeScreen .home-wrap.smyle-home{grid-template-columns:1fr !important}
  #homeScreen .smyle-access-card{width:min(680px,100%) !important}
}
@media(max-width:760px){
  #homeScreen .premium-home-actions,
  #homeScreen .smyle-access-highlights{grid-template-columns:1fr !important}
  #homeScreen .smyle-home .entry-btn{min-height:96px !important;padding:16px !important;border-radius:20px !important}
  #homeScreen .smyle-home .entry-btn strong{font-size:18px !important}
  #homeScreen .smyle-access-card{padding:26px 22px 22px !important;border-radius:26px !important}
  #setupScreen > .container{width:min(calc(100vw - 20px),1180px) !important}
}
'''

if '/* ==== Smyle Lab V32 premium ==== */' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

path.write_text(html, encoding='utf-8')
print('Patch premium V32 aplicado com sucesso.')
