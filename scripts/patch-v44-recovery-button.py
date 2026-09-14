from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

js = r'''
<script id="smyle-v44-recovery-button">
(function(){
  function openRecovery(){
    if(typeof window.smyleOpenAccessRecovery === 'function'){
      window.smyleOpenAccessRecovery();
      return;
    }
    alert('A recuperação de acesso ainda não foi carregada. Atualize a página e tente novamente.');
  }

  function findLoginButton(){
    var pass=document.getElementById('adminPassword');
    var user=document.getElementById('adminUser');
    if(!pass && !user) return null;

    var roots=[];
    var el=pass || user;
    for(var i=0; el && i<7; i++, el=el.parentElement){
      roots.push(el);
    }
    roots.push(document);

    for(var r=0;r<roots.length;r++){
      var buttons=roots[r].querySelectorAll ? roots[r].querySelectorAll('button') : [];
      for(var b=0;b<buttons.length;b++){
        var txt=String(buttons[b].textContent||'').trim().toLowerCase();
        var onclick=String(buttons[b].getAttribute('onclick')||'').toLowerCase();
        if(txt.indexOf('entrar no painel')>=0 || onclick.indexOf('adminlogin')>=0){
          return buttons[b];
        }
      }
    }
    return null;
  }

  function install(){
    var existing=document.getElementById('smyleRecoveryButton');
    if(existing){
      existing.style.display='block';
      existing.style.visibility='visible';
      existing.style.opacity='1';
      return true;
    }

    var loginButton=findLoginButton();
    if(!loginButton) return false;

    var btn=document.createElement('button');
    btn.type='button';
    btn.id='smyleRecoveryButton';
    btn.textContent='Recuperar acesso';
    btn.setAttribute('aria-label','Recuperar acesso do Smyle Core');
    btn.style.cssText='display:block;width:100%;margin:10px 0 0;padding:10px 14px;border:1px solid rgba(12,35,64,.12);border-radius:12px;background:#F5F7F8;color:#0C2340;font:inherit;font-size:13px;font-weight:800;line-height:1.2;cursor:pointer;text-align:center;visibility:visible;opacity:1;';
    btn.addEventListener('click',openRecovery);
    loginButton.insertAdjacentElement('afterend',btn);
    return true;
  }

  function boot(){
    install();
    var attempts=0;
    var timer=setInterval(function(){
      attempts++;
      if(install() || attempts>40) clearInterval(timer);
    },250);

    if('MutationObserver' in window){
      var observer=new MutationObserver(function(){ install(); });
      observer.observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:['class','style']});
      setTimeout(function(){observer.disconnect();},15000);
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
  else boot();
})();
</script>
'''

if 'smyle-v44-recovery-button' not in html:
    pos=html.rfind('</body>')
    if pos<0: raise RuntimeError('</body> não encontrado')
    html=html[:pos]+js+'\n'+html[pos:]

path.write_text(html,encoding='utf-8')
print('Patch V44 aplicado: botão Recuperar acesso instalado de forma resiliente.')
