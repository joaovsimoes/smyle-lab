from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

style_marker = '/* ==== Smyle Lab V61: feedback do jogo em modal ==== */'
css = r'''
<style id="smyle-v61-round-result-style">
/* ==== Smyle Lab V61: feedback do jogo em modal ==== */

/* O avanço agora acontece exclusivamente pelo modal de resultado. */
#gameScreen #nextQuestionBtn,
#gameScreen #feedbackBox{
  display:none !important;
}

#smyleRoundResultModal{
  position:fixed !important;
  inset:0 !important;
  z-index:10050 !important;
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  padding:24px !important;
  background:rgba(8,26,46,.56) !important;
  backdrop-filter:blur(5px) !important;
  -webkit-backdrop-filter:blur(5px) !important;
  box-sizing:border-box !important;
}

#smyleRoundResultModal.hidden{
  display:none !important;
}

#smyleRoundResultModal,
#smyleRoundResultModal *{
  box-sizing:border-box !important;
}

#smyleRoundResultModal .smyle-round-result-card{
  width:min(760px, calc(100vw - 40px)) !important;
  max-height:calc(100dvh - 48px) !important;
  overflow:hidden !important;
  background:#fff !important;
  border:1px solid rgba(12,35,64,.10) !important;
  border-radius:24px !important;
  box-shadow:0 30px 85px rgba(8,26,46,.30) !important;
  animation:smyleRoundResultIn .20s ease-out !important;
  color:#0C2340 !important;
}

@keyframes smyleRoundResultIn{
  from{opacity:0;transform:translateY(10px) scale(.985)}
  to{opacity:1;transform:translateY(0) scale(1)}
}

#smyleRoundResultModal .smyle-round-result-header{
  display:flex !important;
  align-items:flex-start !important;
  justify-content:space-between !important;
  gap:24px !important;
  padding:28px 30px 24px !important;
  border-bottom:1px solid #E4EAF0 !important;
  background:#fff !important;
}

#smyleRoundResultModal .smyle-round-result-heading{
  min-width:0 !important;
}

#smyleRoundResultModal .smyle-round-result-kicker{
  margin:0 0 6px !important;
  color:#20A99A !important;
  font-size:12px !important;
  line-height:1.2 !important;
  font-weight:900 !important;
  letter-spacing:.09em !important;
  text-transform:uppercase !important;
}

#smyleRoundResultModal .smyle-round-result-title{
  margin:0 !important;
  color:#081A2E !important;
  font-size:clamp(23px,2.6vw,30px) !important;
  line-height:1.1 !important;
  font-weight:900 !important;
}

#smyleRoundResultModal .smyle-round-result-close{
  flex:0 0 auto !important;
  width:48px !important;
  height:48px !important;
  border:0 !important;
  border-radius:15px !important;
  background:#F2F4F6 !important;
  color:#081A2E !important;
  font-size:27px !important;
  font-weight:400 !important;
  line-height:1 !important;
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  cursor:pointer !important;
  padding:0 !important;
}

#smyleRoundResultModal .smyle-round-result-content{
  padding:26px 30px !important;
  background:#fff !important;
  overflow:auto !important;
  max-height:calc(100dvh - 250px) !important;
}

#smyleRoundResultModal .smyle-round-result-summary{
  display:grid !important;
  grid-template-columns:64px 1fr !important;
  gap:18px !important;
  align-items:start !important;
  padding:20px !important;
  border-radius:20px !important;
  border:1px solid #CFE0F4 !important;
  background:#F6FAFF !important;
}

#smyleRoundResultModal .smyle-round-result-icon{
  width:58px !important;
  height:58px !important;
  border-radius:18px !important;
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  margin:0 !important;
  font-size:28px !important;
  font-weight:900 !important;
  background:#0C2340 !important;
  color:#fff !important;
  border:0 !important;
}

#smyleRoundResultModal[data-result="correct"] .smyle-round-result-icon{
  background:#0C2340 !important;
}

#smyleRoundResultModal[data-result="wrong"] .smyle-round-result-icon,
#smyleRoundResultModal[data-result="timeout"] .smyle-round-result-icon{
  background:#324A62 !important;
}

#smyleRoundResultModal .smyle-round-result-message{
  margin:1px 0 7px !important;
  color:#0C2340 !important;
  font-size:17px !important;
  line-height:1.35 !important;
  font-weight:900 !important;
}

#smyleRoundResultModal .smyle-round-result-explanation{
  margin:0 !important;
  padding:0 !important;
  border:0 !important;
  background:transparent !important;
  color:#5A6E83 !important;
  font-size:14px !important;
  line-height:1.55 !important;
}

#smyleRoundResultModal .smyle-round-result-extra{
  margin:7px 0 0 !important;
  color:#0C2340 !important;
  font-size:13px !important;
  line-height:1.5 !important;
  font-weight:800 !important;
}

#smyleRoundResultModal .smyle-round-result-scorebox{
  margin-top:18px !important;
  padding:16px 20px !important;
  border:1px dashed #C9D6E4 !important;
  border-radius:18px !important;
  background:#fff !important;
  text-align:center !important;
}

#smyleRoundResultModal .smyle-round-result-scorelabel{
  display:block !important;
  margin-bottom:5px !important;
  color:#92A0B1 !important;
  font-size:11px !important;
  font-weight:800 !important;
  letter-spacing:.12em !important;
  text-transform:uppercase !important;
}

#smyleRoundResultModal .smyle-round-result-points{
  display:block !important;
  margin:0 !important;
  padding:0 !important;
  border:0 !important;
  border-radius:0 !important;
  background:transparent !important;
  color:#0C2340 !important;
  font-size:24px !important;
  line-height:1.15 !important;
  font-weight:900 !important;
}

#smyleRoundResultModal .smyle-round-result-footer{
  display:flex !important;
  justify-content:flex-end !important;
  align-items:center !important;
  padding:18px 30px !important;
  border-top:1px solid #E4EAF0 !important;
  background:#fff !important;
}

#smyleRoundResultModal .smyle-round-result-next{
  min-width:220px !important;
  min-height:52px !important;
  margin:0 !important;
  border:0 !important;
  border-radius:15px !important;
  padding:0 24px !important;
  background:#0C2340 !important;
  color:#fff !important;
  font:inherit !important;
  font-size:14px !important;
  font-weight:900 !important;
  cursor:pointer !important;
  box-shadow:none !important;
}

#smyleRoundResultModal .smyle-round-result-next:hover{
  filter:brightness(1.07) !important;
}

#smyleRoundResultModal .smyle-round-result-close:focus-visible,
#smyleRoundResultModal .smyle-round-result-next:focus-visible{
  outline:3px solid rgba(32,169,154,.28) !important;
  outline-offset:3px !important;
}

@media (max-width:700px){
  #smyleRoundResultModal{
    padding:14px !important;
  }

  #smyleRoundResultModal .smyle-round-result-card{
    width:100% !important;
    border-radius:20px !important;
  }

  #smyleRoundResultModal .smyle-round-result-header{
    padding:22px 20px 18px !important;
  }

  #smyleRoundResultModal .smyle-round-result-close{
    width:42px !important;
    height:42px !important;
    border-radius:13px !important;
  }

  #smyleRoundResultModal .smyle-round-result-content{
    padding:20px !important;
  }

  #smyleRoundResultModal .smyle-round-result-summary{
    grid-template-columns:52px 1fr !important;
    gap:14px !important;
    padding:16px !important;
  }

  #smyleRoundResultModal .smyle-round-result-icon{
    width:50px !important;
    height:50px !important;
    border-radius:15px !important;
    font-size:24px !important;
  }

  #smyleRoundResultModal .smyle-round-result-footer{
    padding:16px 20px 20px !important;
  }

  #smyleRoundResultModal .smyle-round-result-next{
    width:100% !important;
    min-width:0 !important;
  }
}
</style>
'''

modal_marker = 'id="smyleRoundResultModal"'
modal = r'''
<div id="smyleRoundResultModal" class="hidden" data-result="correct" role="dialog" aria-modal="true" aria-labelledby="smyleRoundResultTitle">
  <div class="smyle-round-result-card">
    <div class="smyle-round-result-header">
      <div class="smyle-round-result-heading">
        <p id="smyleRoundResultKicker" class="smyle-round-result-kicker">RESULTADO DA ETAPA</p>
        <h3 id="smyleRoundResultTitle" class="smyle-round-result-title">Resposta certa!</h3>
      </div>
      <button class="smyle-round-result-close" type="button" aria-label="Avançar" title="Avançar" onclick="advanceSmyleRoundFromModal()">×</button>
    </div>

    <div class="smyle-round-result-content">
      <div class="smyle-round-result-summary">
        <div id="smyleRoundResultIcon" class="smyle-round-result-icon">✓</div>
        <div>
          <p id="smyleRoundResultMessage" class="smyle-round-result-message"></p>
          <p id="smyleRoundResultExplanation" class="smyle-round-result-explanation"></p>
          <p id="smyleRoundResultExtra" class="smyle-round-result-extra"></p>
        </div>
      </div>

      <div id="smyleRoundResultScorebox" class="smyle-round-result-scorebox">
        <span class="smyle-round-result-scorelabel">PONTUAÇÃO DA ETAPA</span>
        <strong id="smyleRoundResultPoints" class="smyle-round-result-points">+0 pts</strong>
      </div>
    </div>

    <div class="smyle-round-result-footer">
      <button id="smyleRoundResultNext" class="smyle-round-result-next" type="button" onclick="advanceSmyleRoundFromModal()">Próximo desafio →</button>
    </div>
  </div>
</div>
'''

script_marker = 'id="smyle-v61-round-result-js"'
script = r'''
<script id="smyle-v61-round-result-js">
(function(){
  var previousBodyOverflow='';

  function setText(id,value){
    var el=document.getElementById(id);
    if(el) el.textContent=value || '';
  }

  function openRoundResult(correct,earned,title,explanation,extra,timedOut){
    var modal=document.getElementById('smyleRoundResultModal');
    if(!modal) return;

    var result=timedOut ? 'timeout' : (correct ? 'correct' : 'wrong');
    modal.setAttribute('data-result',result);

    setText('smyleRoundResultIcon',timedOut ? '⏱' : (correct ? '✓' : '×'));
    setText('smyleRoundResultKicker',timedOut ? 'TEMPO DA ETAPA' : 'RESULTADO DA ETAPA');
    setText('smyleRoundResultTitle',timedOut ? 'Tempo esgotado' : (correct ? 'Resposta correta' : 'Resposta incorreta'));
    setText('smyleRoundResultMessage',title || (correct ? 'Você acertou esta etapa.' : 'Confira a explicação antes de seguir.'));
    setText('smyleRoundResultExplanation',explanation || '');
    setText('smyleRoundResultExtra',extra || '');

    var scorebox=document.getElementById('smyleRoundResultScorebox');
    var points=document.getElementById('smyleRoundResultPoints');
    if(scorebox && points){
      if(correct && Number(earned)>0){
        points.textContent='+'+Number(earned)+' pts';
      }else{
        points.textContent='0 pts';
      }
      scorebox.style.display='block';
    }

    var next=document.getElementById('smyleRoundResultNext');
    if(next){
      var isLast=window.gameState && Number(window.gameState.index)===4;
      next.textContent=isLast ? 'Ver resultado 🏆' : 'Próximo desafio →';
    }

    previousBodyOverflow=document.body.style.overflow || '';
    modal.classList.remove('hidden');
    document.body.style.overflow='hidden';
    setTimeout(function(){ try{ next && next.focus(); }catch(e){} },40);
  }

  window.advanceSmyleRoundFromModal=function(){
    var modal=document.getElementById('smyleRoundResultModal');
    if(modal) modal.classList.add('hidden');
    document.body.style.overflow=previousBodyOverflow;
    if(typeof window.nextQuestion==='function') window.nextQuestion();
  };

  function install(){
    if(window.__smyleV61RoundResultInstalled) return;
    if(typeof window.finalizeModelRound!=='function') return;

    var original=window.finalizeModelRound;
    window.finalizeModelRound=function(correct,earned,title,explanation,extra,timedOut){
      var result=original.apply(this,arguments);

      var feedback=document.getElementById('feedbackBox');
      if(feedback) feedback.classList.add('hidden');

      var oldNext=document.getElementById('nextQuestionBtn');
      if(oldNext) oldNext.classList.add('hidden');

      openRoundResult(Boolean(correct),earned,title,explanation,extra,Boolean(timedOut));
      return result;
    };

    window.__smyleV61RoundResultInstalled=true;
  }

  install();
  document.addEventListener('DOMContentLoaded',install);
  window.addEventListener('load',install);
})();
</script>
'''

# Tudo do V61 entra junto no BODY PRINCIPAL. Não usamos </head>, pois existe
# outro <head> dentro do template de impressão de relatórios.
body_close = html.rfind('</body>')
if body_close < 0:
    raise RuntimeError('Fechamento </body> principal não encontrado.')

additions = ''
if style_marker not in html:
    additions += css + '\n'
if modal_marker not in html:
    additions += modal + '\n'
if script_marker not in html:
    additions += script + '\n'

if additions:
    html = html[:body_close] + additions + html[body_close:]

path.write_text(html, encoding='utf-8')
print('V61 aplicada: modal central de feedback com layout Smyle e botão de avanço.')
