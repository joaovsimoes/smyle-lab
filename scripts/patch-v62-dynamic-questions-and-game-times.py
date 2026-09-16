from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

style_marker = '/* ==== Smyle Lab V62: perguntas dinâmicas e tempo por jogo ==== */'
css = r'''
/* ==== Smyle Lab V62: perguntas dinâmicas e tempo por jogo ==== */
#smyleGameTimesSection{
  margin-top:22px;
  padding-top:20px;
  border-top:1px solid rgba(12,35,64,.10);
}
#smyleGameTimesSection .smyle-times-head{
  display:flex;
  align-items:flex-end;
  justify-content:space-between;
  gap:16px;
  margin-bottom:14px;
}
#smyleGameTimesSection .smyle-times-head h3{
  margin:0;
  color:#0C2340;
  font-size:17px;
}
#smyleGameTimesSection .smyle-times-head p{
  margin:5px 0 0;
  color:#6A7D94;
  font-size:12.5px;
  line-height:1.4;
}
#smyleGameTimesGrid{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:14px;
}
#smyleGameTimesGrid .smyle-time-field{
  padding:14px;
  border:1px solid rgba(12,35,64,.10);
  border-radius:16px;
  background:#F8FBFD;
}
#smyleGameTimesGrid .smyle-time-field label{
  display:block;
  margin-bottom:8px;
  color:#0C2340;
  font-size:12.5px;
  font-weight:800;
}
#smyleGameTimesGrid .smyle-time-row{
  display:flex;
  align-items:center;
  gap:8px;
}
#smyleGameTimesGrid input{
  width:100%;
  height:44px;
  border:1px solid rgba(12,35,64,.14);
  border-radius:12px;
  padding:0 12px;
  background:#fff;
  color:#0C2340;
  font:inherit;
  font-weight:800;
}
#smyleGameTimesGrid .smyle-time-unit{
  color:#6A7D94;
  font-size:12px;
  font-weight:800;
}
#beltTrack{
  scrollbar-width:none;
}
#beltTrack::-webkit-scrollbar{
  display:none;
}
@media(max-width:700px){
  #smyleGameTimesGrid{grid-template-columns:1fr;}
  #smyleGameTimesSection .smyle-times-head{align-items:flex-start;flex-direction:column;}
}
'''

if style_marker not in html:
    # Mantém o estilo junto do conteúdo principal, evitando o <head> interno do relatório.
    body_close = html.rfind('</body>')
    if body_close < 0:
        raise RuntimeError('Fechamento </body> principal não encontrado.')
    style = '<style id="smyle-v62-style">\n' + css + '\n</style>\n'
    html = html[:body_close] + style + html[body_close:]

script_marker = 'id="smyle-v62-dynamic-rounds-js"'
script = r'''
<script id="smyle-v62-dynamic-rounds-js">
(function(){
  var DEFAULT_TIMES = {
    'fato-fake':20,
    'qual-jogada':30,
    'desembaralha':40,
    'conecta-lab':45
  };

  function clampTime(value,fallback){
    var n=Number(value);
    if(!Number.isFinite(n)) n=Number(fallback)||20;
    return Math.max(5,Math.min(600,Math.round(n)));
  }

  function getGameTimeMap(){
    var s=typeof getSettings==='function' ? getSettings() : {};
    var saved=(s && s.gameTimes && typeof s.gameTimes==='object') ? s.gameTimes : {};
    var out={};
    var catalog=[];
    try{ catalog=typeof getGameCatalog==='function' ? getGameCatalog() : []; }catch(e){ catalog=[]; }
    catalog.forEach(function(g){
      var fallback=DEFAULT_TIMES[g.id];
      if(fallback==null){
        fallback=g.type==='scenario'?30:g.type==='sequence'?40:g.type==='matching'?45:20;
      }
      out[g.id]=clampTime(saved[g.id],fallback);
    });
    Object.keys(DEFAULT_TIMES).forEach(function(id){
      if(out[id]==null) out[id]=clampTime(saved[id],DEFAULT_TIMES[id]);
    });
    return out;
  }

  function totalRounds(){
    try{return Array.isArray(gameState.questions)?gameState.questions.length:0;}catch(e){return 0;}
  }

  function renderDynamicCounter(){
    var total=totalRounds();
    if(!total) return;
    var counter=document.getElementById('questionCounter');
    if(counter) counter.textContent='Desafio '+(gameState.index+1)+' de '+total;
    var progress=document.getElementById('gameProgress');
    if(progress) progress.style.width=((gameState.index/total)*100)+'%';
  }

  function renderGameTimes(){
    var pane=document.getElementById('settingsGeneralPane');
    if(!pane) return;
    var panel=pane.querySelector('.settings-general-card') || pane.querySelector('.panel');
    if(!panel) return;

    var legacy=document.getElementById('settingTime');
    var legacyGroup=legacy && legacy.closest ? legacy.closest('.form-group') : null;
    if(legacyGroup) legacyGroup.style.display='none';

    var section=document.getElementById('smyleGameTimesSection');
    if(!section){
      section=document.createElement('div');
      section.id='smyleGameTimesSection';
      var saveBtn=panel.querySelector('button[onclick="saveSettings()"]');
      if(saveBtn) panel.insertBefore(section,saveBtn);
      else panel.appendChild(section);
    }

    var times=getGameTimeMap();
    var catalog=[];
    try{ catalog=typeof getGameCatalog==='function' ? getGameCatalog().filter(function(g){return g.status!=='inactive';}) : []; }catch(e){ catalog=[]; }
    if(!catalog.length && typeof SMYLE_CORE_MODELS!=='undefined') catalog=SMYLE_CORE_MODELS.slice();

    section.innerHTML='<div class="smyle-times-head"><div><h3>Tempo por jogo</h3><p>Defina por quantos segundos cada desafio ficará disponível em cada experiência.</p></div></div><div id="smyleGameTimesGrid"></div>';
    var grid=section.querySelector('#smyleGameTimesGrid');
    catalog.forEach(function(g){
      var field=document.createElement('div');
      field.className='smyle-time-field';
      field.innerHTML='<label></label><div class="smyle-time-row"><input type="number" min="5" max="600" step="1" data-smyle-game-time=""><span class="smyle-time-unit">seg</span></div>';
      field.querySelector('label').textContent=g.name;
      var input=field.querySelector('input');
      input.setAttribute('data-smyle-game-time',g.id);
      input.value=times[g.id] || 20;
      grid.appendChild(field);
    });
  }

  function captureGameTimes(){
    var values={};
    document.querySelectorAll('[data-smyle-game-time]').forEach(function(input){
      var id=input.getAttribute('data-smyle-game-time');
      if(id) values[id]=clampTime(input.value,DEFAULT_TIMES[id]||20);
    });
    return values;
  }

  function installSettings(){
    if(window.__smyleV62SettingsInstalled) return;
    if(typeof window.loadSettingsForm!=='function' || typeof window.saveSettings!=='function') return;

    var originalLoad=window.loadSettingsForm;
    window.loadSettingsForm=function(){
      var result=originalLoad.apply(this,arguments);
      renderGameTimes();
      return result;
    };

    var originalSave=window.saveSettings;
    window.saveSettings=function(){
      var captured=captureGameTimes();
      var result=originalSave.apply(this,arguments);
      try{
        var s=getSettings();
        s.gameTimes=Object.assign({},s.gameTimes||{},captured);
        setSettings(s);
      }catch(e){console.warn('Smyle V62 gameTimes:',e);}
      renderGameTimes();
      return result;
    };

    window.__smyleV62SettingsInstalled=true;
    renderGameTimes();
  }

  function installGameFlow(){
    if(window.__smyleV62FlowInstalled) return;
    if(typeof window.renderQuestion!=='function' || typeof window.finalizeModelRound!=='function') return;

    window.roundSeconds=function(){
      var times=getGameTimeMap();
      var fallback=DEFAULT_TIMES[gameState.gameId] || 20;
      return clampTime(times[gameState.gameId],fallback);
    };

    window.updateBeltTrack=function(markCurrentDone){
      var track=document.getElementById('beltTrack');
      if(!track) return;
      var total=Math.max(1,totalRounds());
      track.style.gridTemplateColumns='repeat('+total+', minmax('+(total>8?'52px':'0')+', 1fr))';
      track.style.overflowX=total>8?'auto':'visible';
      track.innerHTML=Array.from({length:total},function(_,i){
        var done=i<gameState.index || (markCurrentDone && i===gameState.index);
        var active=!done && i===gameState.index;
        return '<div class="belt-step '+(done?'done ':'')+(active?'active':'')+'">'+(done?'✓':(i+1))+'</div>';
      }).join('');
    };

    var originalRender=window.renderQuestion;
    window.renderQuestion=function(){
      var result=originalRender.apply(this,arguments);
      renderDynamicCounter();
      try{window.updateBeltTrack(false);}catch(e){}
      return result;
    };

    var previousFinalize=window.finalizeModelRound;
    window.finalizeModelRound=function(){
      var result=previousFinalize.apply(this,arguments);
      var total=Math.max(1,totalRounds());
      var progress=document.getElementById('gameProgress');
      if(progress) progress.style.width=(((gameState.index+1)/total)*100)+'%';
      try{window.updateBeltTrack(true);}catch(e){}
      var isLast=gameState.index>=total-1;
      var hiddenNext=document.getElementById('nextQuestionBtn');
      if(hiddenNext) hiddenNext.textContent=isLast?'Ver resultado 🏆':'Próximo desafio →';
      var modalNext=document.getElementById('smyleRoundResultNext');
      if(modalNext) modalNext.textContent=isLast?'Ver resultado 🏆':'Próximo desafio →';
      return result;
    };

    window.nextQuestion=function(){
      var total=totalRounds();
      if(gameState.index<total-1){
        gameState.index++;
        renderQuestion();
      }else if(typeof finishGame==='function'){
        finishGame();
      }
    };

    window.startGame=function(){
      var player=(typeof getSmylePlayerCodeV19==='function') ? getSmylePlayerCodeV19() : (document.getElementById('playerName')?.value.trim()||'Participante');
      var gameId=document.getElementById('gameSelect')?.value||'fato-fake';
      var category=document.getElementById('gameCategory')?.value||'all';
      var mode='individual';
      var model=getModel(gameId);
      var pool=getGameItems(gameId).filter(function(x){
        return x.active!==false && (category==='all'||x.category===category);
      });
      if(!pool.length){
        alert('O jogo “'+model.name+'” não possui desafios ativos para a seleção atual.');
        return;
      }
      var rounds=shuffle(pool).map(function(x){return cloneData(x);});
      gameState={questions:rounds,index:0,score:0,hits:0,misses:0,player:player,category:category,mode:mode,timeLeft:0,timer:null,questionStartedAt:0,answers:[],streak:0,maxStreak:0,gameId:gameId,gameName:model.name,gameType:model.type,roundData:{}};
      showScreen('gameScreen');
      var title=document.getElementById('gameArenaTitle');
      if(title) title.textContent=model.name.toUpperCase();
      var subtitle=document.getElementById('gameArenaSubtitle');
      if(subtitle) subtitle.textContent='JOGADOR '+player+' • '+modelSubtitle(model.type);
      renderQuestion();
      try{
        if(typeof SMYLE_PLAYER_CODE_SESSION_KEY_V19!=='undefined') sessionStorage.removeItem(SMYLE_PLAYER_CODE_SESSION_KEY_V19);
      }catch(e){}
    };

    window.launchGameTestV18=function(gameId){
      try{
        var model=getModel(gameId);
        var pool=getGameItems(gameId).filter(function(x){return x.active!==false;});
        if(!pool.length){
          alert('Para testar “'+model.name+'”, cadastre pelo menos 1 desafio ativo.');
          showAdminPage('questions',document.querySelector('.side-link[data-page="questions"]'));
          populateGameSelects();
          var filter=document.getElementById('questionFilterGame');
          if(filter){filter.value=gameId;renderQuestionsTable();}
          return;
        }
        var rounds=shuffle(pool).map(function(x){return cloneData(x);});
        gameState={questions:rounds,index:0,score:0,hits:0,misses:0,player:'Teste do administrador',category:'all',mode:'individual',timeLeft:0,timer:null,questionStartedAt:0,answers:[],streak:0,maxStreak:0,gameId:gameId,gameName:model.name,gameType:model.type,roundData:{},isTest:true};
        showScreen('gameScreen');
        var title=document.getElementById('gameArenaTitle');
        if(title) title.textContent=model.name.toUpperCase();
        var subtitle=document.getElementById('gameArenaSubtitle');
        if(subtitle) subtitle.textContent='MODO TESTE • '+modelSubtitle(model.type);
        renderQuestion();
      }catch(err){console.error(err);alert('Não foi possível abrir o modo de teste deste jogo.');}
    };
    window.testGame=function(id){return window.launchGameTestV18(id);};

    window.__smyleV62FlowInstalled=true;
  }

  function install(){
    installSettings();
    installGameFlow();
  }

  install();
  document.addEventListener('DOMContentLoaded',install);
  window.addEventListener('load',install);
  setTimeout(install,120);
})();
</script>
'''

if script_marker not in html:
    body_close = html.rfind('</body>')
    if body_close < 0:
        raise RuntimeError('Fechamento </body> principal não encontrado.')
    html = html[:body_close] + script + '\n' + html[body_close:]

path.write_text(html,encoding='utf-8')
print('V62 aplicada: quantidade de desafios acompanha perguntas ativas e tempo passa a ser configurável por jogo.')
