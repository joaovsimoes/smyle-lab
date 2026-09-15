from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

style_marker = '/* ==== Smyle Lab V61: feedback do jogo em modal ==== */'
css = r'''
/* ==== Smyle Lab V61: feedback do jogo em modal ==== */

/* O avanço agora acontece exclusivamente pelo modal de resultado. */
#gameScreen #nextQuestionBtn{
  display:none !important;
}

#gameScreen #feedbackBox{
  display:none !important;
}

#smyleRoundResultModal{
  position:fixed;
  inset:0;
  z-index:10050;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:24px;
  background:rgba(8,26,46,.58);
  backdrop-filter:blur(7px);
  -webkit-backdrop-filter:blur(7px);
}

#smyleRoundResultModal.hidden{
  display:none !important;
}

#smyleRoundResultModal .smyle-round-result-card{
  width:min(560px, calc(100vw - 32px));
  max-height:calc(100dvh - 40px);
  overflow:auto;
  background:#fff;
  border:1px solid rgba(12,35,64,.10);
  border-radius:24px;
  padding:26px;
  box-shadow:0 28px 80px rgba(8,26,46,.28);
  animation:smyleRoundResultIn .22s ease-out;
}

@keyframes smyleRoundResultIn{
  from{opacity:0;transform:translateY(12px) scale(.985)}
  to{opacity:1;transform:translateY(0) scale(1)}
}

#smyleRoundResultModal .smyle-round-result-icon{
  width:58px;
  height:58px;
  border-radius:18px;
  display:flex;
  align-items:center;
  justify-content:center;
  margin-bottom:16px;
  font-size:27px;
  font-weight:900;
  background:#E9FBF8;
  color:#0C2340;
  border:1px solid #BDEFE7;
}

#smyleRoundResultModal[data-result="wrong"] .smyle-round-result-icon{
  background:#F1F5F9;
  border-color:#D8E2EC;
}

#smyleRoundResultModal[data-result="timeout"] .smyle-round-result-icon{
  background:#F5F7FA;
  border-color:#D8E2EC;
}

#smyleRoundResultModal .smyle-round-result-kicker{
  margin:0 0 5px;
  color:#20A99A;
  font-size:12px;
  line-height:1.2;
  font-weight:900;
  letter-spacing:.08em;
  text-transform:uppercase;
}

#smyleRoundResultModal .smyle-round-result-title{
  margin:0;
  color:#081A2E;
  font-size:clamp(23px, 3vw, 30px);
  line-height:1.08;
  font-weight:900;
}

#smyleRoundResultModal .smyle-round-result-message{
  margin:8px 0 0;
  color:#536B82;
  font-size:14px;
  line-height:1.48;
}

#smyleRoundResultModal .smyle-round-result-points{
  display:inline-flex;
  align-items:center;
  width:max-content;
  margin-top:16px;
  padding:7px 11px;
  border-radius:999px;
  background:#E9FBF8;
  border:1px solid #BDEFE7;
  color:#0C2340;
  font-size:12px;
  font-weight:900;
}

#smyleRoundResultModal .smyle-round-result-explanation{
  margin-top:18px;
  padding:14px 16px;
  border-radius:16px;
  background:#F5F8FB;
  border:1px solid #E4EBF2;
  color:#435B72;
  font-size:13px;
  line-height:1.5;
}

#smyleRoundResultModal .smyle-round-result-extra{
  margin-top:9px;
  color:#0C2340;
  font-size:12px;
  line-height:1.45;
  font-weight:800;
}

#smyleRoundResultModal .smyle-round-result-next{
  width:100%;
  min-height:50px;
  margin-top:20px;
  border:0;
  border-radius:15px;
  padding:0 18px;
  background:#0C2340;
  color:#fff;
  font:inherit;
  font-size:14px;
  font-weight:900;
  cursor:pointer;
  transition:transform .16s ease, box-shadow .16s ease;
  box-shadow:0 10px 24px rgba(12,35,64,.16);
}

#smyleRoundResultModal .smyle-round-result-next:hover{
  transform:translateY(-1px);
  box-shadow:0 13px 28px rgba(12,35,64,.21);
}

#smyleRoundResultModal .smyle-round-result-next:focus-visible{
  outline:3px solid rgba(32,169,154,.28);
  outline-offset:3px;
}

@media (max-width:700px){
  #smyleRoundResultModal{padding:16px;}
  #smyleRoundResultModal .smyle-round-result-card{
    width:100%;
    padding:21px;
    border-radius:20px;
  }
  #smyleRoundResultModal .smyle-round-result-icon{
    width:52px;
    height:52px;
    border-radius:16px;
  }
}
'''

if style_marker not in html:
    head_close = html.rfind('</head>')
    if head_close < 0:
        raise RuntimeError('Fechamento </head> principal não encontrado.')
    html = html[:head_close] + '<style id="smyle-v61-round-result-style">\n' + css + '\n</style>\n' + html[head_close:]

modal_marker = 'id="smyleRoundResultModal"'
modal = r'''
<div id="smyleRoundResultModal" class="hidden" data-result="correct" role="dialog" aria-modal="true" aria-labelledby="smyleRoundResultTitle">
  <div class="smyle-round-result-card">
    <div id="smyleRoundResultIcon" class="smyle-round-result-icon">✓</div>
    <p id="smyleRoundResultKicker" class="smyle-round-result-kicker">Resultado da etapa</p>
    <h3 id="smyleRoundResultTitle" class="smyle-round-result-title">Resposta certa!</h3>
    <p id="smyleRoundResultMessage" class="smyle-round-result-message"></p>
    <div id="smyleRoundResultPoints" class="smyle-round-result-points">+0 pts</div>
    <div id="smyleRoundResultExplanation" class="smyle-round-result-explanation"></div>
    <div id="smyleRoundResultExtra" class="smyle-round-result-extra"></div>
    <button id="smyleRoundResultNext" class="smyle-round-result-next" type="button" onclick="advanceSmyleRoundFromModal()">Próximo desafio →</button>
  </div>
</div>
'''

script_marker = 'id="smyle-v61-round-result-js"'
script = r'''
<script id="smyle-v61-round-result-js">
(function(){
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
    setText('smyleRoundResultKicker',timedOut ? 'Tempo da etapa' : 'Resultado da etapa');
    setText('smyleRoundResultTitle',timedOut ? 'Tempo esgotado' : (correct ? 'Resposta certa! ✨' : 'Resposta incorreta'));
    setText('smyleRoundResultMessage',title || (correct ? 'Mandou bem nesta etapa.' : 'Confira a explicação antes de seguir.'));
    setText('smyleRoundResultExplanation',explanation || '');
    setText('smyleRoundResultExtra',extra || '');

    var points=document.getElementById('smyleRoundResultPoints');
    if(points){
      if(correct && Number(earned)>0){
        points.textContent='+'+Number(earned)+' pts';
        points.style.display='inline-flex';
      }else{
        points.style.display='none';
      }
    }

    var next=document.getElementById('smyleRoundResultNext');
    if(next){
      var isLast=window.gameState && Number(window.gameState.index)===4;
      next.textContent=isLast ? 'Ver resultado 🏆' : 'Próximo desafio →';
    }

    modal.classList.remove('hidden');
    document.body.style.overflow='hidden';
    setTimeout(function(){ try{ next && next.focus(); }catch(e){} },40);
  }

  window.advanceSmyleRoundFromModal=function(){
    var modal=document.getElementById('smyleRoundResultModal');
    if(modal) modal.classList.add('hidden');
    document.body.style.overflow='';
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

# Insere modal e script apenas no BODY PRINCIPAL, usando o último </body>.
if modal_marker not in html or script_marker not in html:
    body_close = html.rfind('</body>')
    if body_close < 0:
        raise RuntimeError('Fechamento </body> principal não encontrado.')
    additions = ''
    if modal_marker not in html:
        additions += modal + '\n'
    if script_marker not in html:
        additions += script + '\n'
    html = html[:body_close] + additions + html[body_close:]

path.write_text(html, encoding='utf-8')
print('V61 aplicada: feedback de cada etapa abre em modal com botão para avançar.')
