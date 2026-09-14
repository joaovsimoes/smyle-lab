from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

style = r'''
<style id="smyle-v59-home-entry-style">
#homeScreen .entry-btn.play,
#homeScreen .entry-btn.admin{
  pointer-events:auto !important;
  cursor:pointer !important;
  position:relative !important;
  z-index:50 !important;
}
#homeScreen .smyle-access-actions,
#homeScreen .smyle-access-card,
#homeScreen .smyle-side{
  pointer-events:auto !important;
}
</style>
'''

script = r'''
<script id="smyle-v59-home-entry-repair">
(function(){
  function visible(el){
    if(!el) return false;
    if(el.hidden) return false;
    var cs=getComputedStyle(el);
    return cs.display!=='none' && cs.visibility!=='hidden' && cs.opacity!=='0';
  }

  function hideScreen(el){
    if(!el) return;
    el.hidden=true;
    el.classList.remove('active');
    el.classList.add('hidden');
    el.style.display='none';
  }

  function forceScreen(id){
    var target=document.getElementById(id);
    if(!target) return false;
    ['homeScreen','setupScreen','gameScreen','adminScreen'].forEach(function(screenId){
      var el=document.getElementById(screenId);
      if(!el) return;
      if(screenId===id){
        el.hidden=false;
        el.classList.remove('hidden');
        el.classList.add('active');
        el.style.display='';
        el.style.visibility='visible';
        el.style.opacity='1';
      }else{
        hideScreen(el);
      }
    });
    window.scrollTo(0,0);
    return true;
  }

  function refreshSetup(){
    var names=['renderSetupOptions','renderGameModelCards','refreshSetupGames','refreshSetupCategories','updateSetupCategories'];
    names.forEach(function(name){
      try{
        if(typeof window[name]==='function') window[name]();
      }catch(e){ console.warn('Smyle V59:',name,e); }
    });
  }

  function openPlay(){
    var setup=document.getElementById('setupScreen');
    var worked=false;
    try{
      if(typeof window.showScreen==='function'){
        window.showScreen('setupScreen');
        worked=visible(setup);
      }
    }catch(e){
      console.warn('Smyle V59: showScreen falhou',e);
    }
    if(!worked) forceScreen('setupScreen');
    document.body.style.overflow='';
    refreshSetup();
  }

  function showAdminGateFallback(){
    var gate=document.getElementById('adminGate');
    if(!gate){
      var user=document.getElementById('adminUser');
      if(user){ gate=user.closest('.modal,[id]'); }
    }
    if(!gate) return false;
    gate.hidden=false;
    gate.classList.remove('hidden');
    gate.classList.add('active');
    gate.style.display='flex';
    gate.style.visibility='visible';
    gate.style.opacity='1';
    gate.style.pointerEvents='auto';
    document.body.style.overflow='hidden';
    try{
      var userField=document.getElementById('adminUser');
      if(userField) setTimeout(function(){ userField.focus(); },30);
    }catch(e){}
    return true;
  }

  function openAdmin(){
    var gate=document.getElementById('adminGate');
    var worked=false;
    try{
      if(typeof window.openAdminGate==='function'){
        window.openAdminGate();
        worked=visible(gate);
      }
    }catch(e){
      console.warn('Smyle V59: openAdminGate falhou',e);
    }
    if(!worked) showAdminGateFallback();
  }

  function prepButtons(){
    document.querySelectorAll('#homeScreen .entry-btn.play,#homeScreen .entry-btn.admin').forEach(function(btn){
      btn.disabled=false;
      btn.removeAttribute('disabled');
      btn.setAttribute('type','button');
      btn.style.pointerEvents='auto';
      btn.style.cursor='pointer';
    });
  }

  document.addEventListener('click',function(e){
    var btn=e.target.closest && e.target.closest('#homeScreen .entry-btn.play,#homeScreen .entry-btn.admin');
    if(!btn) return;
    e.preventDefault();
    e.stopPropagation();
    if(e.stopImmediatePropagation) e.stopImmediatePropagation();
    if(btn.classList.contains('play')) openPlay();
    else openAdmin();
  },true);

  document.addEventListener('DOMContentLoaded',function(){
    prepButtons();
    var home=document.getElementById('homeScreen');
    if(home){
      new MutationObserver(prepButtons).observe(home,{subtree:true,childList:true,attributes:true,attributeFilter:['class','style','disabled']});
    }
  });

  window.addEventListener('load',prepButtons);
})();
</script>
'''

if 'id="smyle-v59-home-entry-style"' not in html:
    html = html.replace('</head>', style + '\n</head>', 1)

if 'id="smyle-v59-home-entry-repair"' not in html:
    html = html.replace('</body>', script + '\n</body>', 1)

path.write_text(html, encoding='utf-8')
print('Patch V59 aplicado: botões Jogar e Administrador isolados e restaurados.')
