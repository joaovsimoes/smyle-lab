from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

style = r'''
<style id="smyle-v58-auto-advance-style">
/* ==== Smyle Lab V58: avanço automático após feedback ==== */
#gameScreen #nextQuestionBtn{
  display:none !important;
}

#gameScreen .smyle-auto-next{
  margin-top:8px;
  padding:8px 12px;
  border:1px solid rgba(67,210,204,.35);
  border-radius:12px;
  background:rgba(67,210,204,.08);
  color:#0b2a4a;
  font-size:12px;
  line-height:1.25;
  font-weight:700;
  text-align:right;
}

#gameScreen .smyle-auto-next strong{
  color:#20bdb5;
  font-weight:800;
}

@media (max-height:820px) and (min-width:901px){
  #gameScreen .smyle-auto-next{
    margin-top:5px;
    padding:6px 9px;
    font-size:11px;
  }
}
</style>
'''

script = r'''
<script id="smyle-v58-auto-advance">
(function(){
  var WAIT_MS = 20000;
  var timeoutId = null;
  var intervalId = null;
  var activeButton = null;
  var activeFeedback = null;
  var activeToken = 0;
  var waitingFingerprint = null;
  var startedAt = 0;

  function gameScreen(){
    return document.getElementById('gameScreen');
  }

  function gameIsVisible(){
    var game = gameScreen();
    if(!game || game.hidden) return false;
    var s = window.getComputedStyle(game);
    return s.display !== 'none' && s.visibility !== 'hidden';
  }

  function advanceButton(){
    return document.getElementById('nextQuestionBtn');
  }

  function buttonIsReady(btn){
    if(!btn) return false;
    if(btn.hidden || btn.disabled) return false;
    if(btn.classList.contains('hidden')) return false;
    if(btn.getAttribute('aria-hidden') === 'true') return false;
    return true;
  }

  function feedbackElement(){
    var game = gameScreen();
    if(!game) return null;
    var items = game.querySelectorAll('#feedbackBox, .feedback');
    for(var i=0;i<items.length;i++){
      var el = items[i];
      if(el.hidden || el.classList.contains('hidden')) continue;
      if(el.getAttribute('aria-hidden') === 'true') continue;
      if(el.style && el.style.display === 'none') continue;
      if(String(el.textContent || '').trim()) return el;
    }
    return null;
  }

  function questionFingerprint(){
    var game = gameScreen();
    if(!game) return '';
    var selectors = [
      '.round-kicker',
      '.question-text',
      '.model-prompt',
      '.scenario-question',
      '.sequence-title',
      '.matching-title'
    ];
    var parts = [];
    selectors.forEach(function(sel){
      var el = game.querySelector(sel);
      if(el && String(el.textContent || '').trim()){
        parts.push(String(el.textContent).replace(/\s+/g,' ').trim());
      }
    });
    return parts.join(' | ');
  }

  function removeStatus(){
    document.querySelectorAll('#gameScreen .smyle-auto-next').forEach(function(el){
      el.remove();
    });
  }

  function clearTimers(removeMessage){
    if(timeoutId){ clearTimeout(timeoutId); timeoutId = null; }
    if(intervalId){ clearInterval(intervalId); intervalId = null; }
    activeButton = null;
    activeFeedback = null;
    startedAt = 0;
    activeToken++;
    if(removeMessage !== false) removeStatus();
  }

  function statusLabel(btn, seconds){
    var text = String((btn && btn.textContent) || '').toLowerCase();
    var prefix = text.indexOf('resultado') !== -1 ? 'Resultado em' : 'Próximo desafio em';
    return prefix + ' <strong>' + seconds + 's</strong>';
  }

  function makeStatus(feedback, btn){
    removeStatus();
    var status = document.createElement('div');
    status.className = 'smyle-auto-next';
    status.setAttribute('aria-live','polite');
    status.innerHTML = statusLabel(btn, 20);
    feedback.appendChild(status);
    return status;
  }

  function startCountdown(btn, feedback){
    clearTimers(true);
    activeButton = btn;
    activeFeedback = feedback;
    var token = ++activeToken;
    var fingerprint = questionFingerprint();
    var status = makeStatus(feedback, btn);
    startedAt = Date.now();

    function render(){
      if(token !== activeToken) return;
      var elapsed = Date.now() - startedAt;
      var seconds = Math.max(0, Math.ceil((WAIT_MS - elapsed) / 1000));
      if(status && status.isConnected){
        status.innerHTML = statusLabel(btn, seconds);
      }
    }

    render();
    intervalId = setInterval(render, 250);

    timeoutId = setTimeout(function(){
      if(token !== activeToken) return;
      if(!gameIsVisible()){
        clearTimers(true);
        return;
      }

      var currentBtn = advanceButton();
      var currentFeedback = feedbackElement();
      if(currentBtn !== btn || currentFeedback !== feedback || !buttonIsReady(currentBtn)){
        clearTimers(true);
        return;
      }

      if(intervalId){ clearInterval(intervalId); intervalId = null; }
      if(status && status.isConnected){
        status.textContent = 'Carregando próximo desafio...';
      }

      waitingFingerprint = fingerprint;
      timeoutId = null;
      activeButton = null;
      activeFeedback = null;
      activeToken++;

      setTimeout(function(){
        try{
          currentBtn.click();
        }catch(e){
          currentBtn.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window}));
        }
      }, 120);
    }, WAIT_MS);
  }

  function sync(){
    if(!gameIsVisible()){
      waitingFingerprint = null;
      clearTimers(true);
      return;
    }

    var currentFingerprint = questionFingerprint();
    if(waitingFingerprint){
      if(currentFingerprint === waitingFingerprint){
        return;
      }
      waitingFingerprint = null;
      clearTimers(true);
    }

    var btn = advanceButton();
    var feedback = feedbackElement();
    var ready = buttonIsReady(btn) && !!feedback;

    if(!ready){
      if(activeButton || activeFeedback) clearTimers(true);
      return;
    }

    if(activeButton === btn && activeFeedback === feedback && timeoutId){
      return;
    }

    startCountdown(btn, feedback);
  }

  document.addEventListener('DOMContentLoaded', function(){
    sync();
    var observer = new MutationObserver(function(){
      setTimeout(sync, 20);
    });
    observer.observe(document.body, {
      subtree:true,
      childList:true,
      attributes:true,
      characterData:true,
      attributeFilter:['class','style','hidden','disabled','aria-hidden']
    });
    setInterval(sync, 500);
  });

  document.addEventListener('click', function(){
    setTimeout(sync, 40);
    setTimeout(sync, 220);
  });
})();
</script>
'''

if 'id="smyle-v58-auto-advance-style"' not in html:
    if '</head>' in html:
        html = html.replace('</head>', style + '\n</head>', 1)
    else:
        html = html.replace('</style>', style + '\n</style>', 1)

if 'id="smyle-v58-auto-advance"' not in html:
    html = html.replace('</body>', script + '\n</body>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V58 aplicado: avanço automático em 20 segundos após o feedback.')
