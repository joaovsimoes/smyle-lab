from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

js = r'''
<script id="smyle-v41-login-recovery">
(function(){
  function normalizeUsername(v){ return String(v||'').trim().toLowerCase(); }

  function collectCandidateUsers(){
    var candidates=[];
    var seen=new Set();

    function pushUser(u, source){
      if(!u || typeof u!=='object') return;
      var username=String(u.username||u.user||u.login||'').trim();
      if(!username) return;
      var password=(u.password!==undefined && u.password!==null) ? String(u.password) : '';
      var id=String(u.id||u.uid||'');
      var key=[normalizeUsername(username),password,id].join('|');
      if(seen.has(key)) return;
      seen.add(key);
      candidates.push(Object.assign({},u,{username:username,password:password,__source:source||''}));
    }

    try{
      if(typeof getUsers==='function'){
        var canonical=getUsers();
        if(Array.isArray(canonical)) canonical.forEach(function(u){ pushUser(u,'getUsers'); });
      }
    }catch(e){ console.warn('Leitura getUsers falhou',e); }

    try{
      for(var i=0;i<localStorage.length;i++){
        var key=localStorage.key(i);
        if(!key) continue;
        var raw=localStorage.getItem(key);
        if(!raw || raw.length>3000000) continue;
        var parsed;
        try{ parsed=JSON.parse(raw); }catch(ignore){ continue; }
        if(Array.isArray(parsed)){
          parsed.forEach(function(u){
            if(u && typeof u==='object' && ('username' in u || 'user' in u || 'login' in u)) pushUser(u,key);
          });
        }else if(parsed && typeof parsed==='object'){
          if(Array.isArray(parsed.users)) parsed.users.forEach(function(u){ pushUser(u,key+'.users'); });
          if('username' in parsed || 'user' in parsed || 'login' in parsed) pushUser(parsed,key);
        }
      }
    }catch(e){ console.warn('Varredura do armazenamento falhou',e); }

    return candidates;
  }

  function migrateRecoveredUser(found){
    try{
      if(typeof getUsers!=='function' || typeof saveUsers!=='function') return;
      var users=getUsers();
      if(!Array.isArray(users)) users=[];
      var uname=normalizeUsername(found.username);
      var idx=users.findIndex(function(u){
        return String(u.id||'')===String(found.id||'') || normalizeUsername(u.username)===uname;
      });
      var normalized={
        id:found.id || (idx>=0 && users[idx].id) || ('user-'+Date.now()),
        name:found.name || (idx>=0 && users[idx].name) || 'Usuário',
        username:String(found.username||'').trim(),
        password:String(found.password||''),
        role:(typeof smyleNormalizeRole==='function' ? smyleNormalizeRole(found.role) : (found.role||'Smyle Go ✦')),
        active:found.active!==false,
        photo:found.photo || (idx>=0 && users[idx].photo) || ''
      };
      if(idx>=0) users[idx]=Object.assign({},users[idx],normalized);
      else users.unshift(normalized);
      saveUsers(users);
    }catch(e){ console.warn('Migração automática de usuário falhou',e); }
  }

  function brandedLoginError(message){
    var old=document.getElementById('smyleLoginErrorBox');
    if(old) old.remove();
    var card=document.querySelector('#adminGate .smyle-login-card, #adminGate .login-card, #adminGate .admin-login-card, #adminGate .smyle-admin-login-card');
    var pass=document.getElementById('adminPassword');
    var box=document.createElement('div');
    box.id='smyleLoginErrorBox';
    box.textContent=message;
    box.style.cssText='margin:12px 0 0;padding:12px 14px;border-radius:12px;background:#EFF8F9;border:1px solid #CDEDEA;color:#0C2340;font-size:13px;font-weight:700;line-height:1.4;text-align:left;';
    if(pass && pass.parentElement) pass.parentElement.insertAdjacentElement('afterend',box);
    else if(card) card.appendChild(box);
    else alert(message);
  }

  window.adminLogin=function(){
    var userField=document.getElementById('adminUser');
    var passField=document.getElementById('adminPassword');
    if(!userField || !passField){ brandedLoginError('Não foi possível localizar os campos de acesso.'); return; }

    var username=normalizeUsername(userField.value);
    var password=String(passField.value||'');
    if(!username || !password){ brandedLoginError('Informe seu usuário e senha.'); return; }

    var users=collectCandidateUsers();
    var found=users.find(function(u){
      return u.active!==false && normalizeUsername(u.username)===username && String(u.password||'')===password;
    });

    if(!found){
      try{
        var canonical=(typeof getUsers==='function')?getUsers():[];
        var admin=Array.isArray(canonical)?canonical.find(function(u){ return String(u.id||'')==='admin-default' || normalizeUsername(u.username)===username; }):null;
        var settings=(typeof getSettings==='function')?getSettings():null;
        if(admin && settings && normalizeUsername(admin.username)===username && String(settings.adminPassword||'')===password){
          found=Object.assign({},admin,{password:password});
          migrateRecoveredUser(found);
        }
      }catch(ignore){}
    }

    if(!found){ brandedLoginError('Usuário ou senha incorretos.'); return; }

    migrateRecoveredUser(found);
    try{ sessionStorage.setItem(KEYS.adminSession,'1'); }catch(e){}
    try{ sessionStorage.setItem('smyle_lab_current_user_id',found.id||'admin-default'); }catch(e){}
    try{ if(typeof setCurrentAdminUser==='function') setCurrentAdminUser(found); }catch(e){}
    document.body.style.overflow='';
    if(typeof showScreen==='function') showScreen('adminScreen');
    try{ if(typeof refreshCurrentUserUI==='function') refreshCurrentUserUI(); }catch(e){}
    try{ if(typeof smyleApplyAccessPermissions==='function') smyleApplyAccessPermissions(); }catch(e){}
    try{
      if(typeof showAdminPage==='function'){
        var dash=document.querySelector('.side-link[data-page="dashboard"]');
        showAdminPage('dashboard',dash);
      }
    }catch(e){}
    passField.value='';
    var err=document.getElementById('smyleLoginErrorBox');
    if(err) err.remove();
  };

  document.addEventListener('keydown',function(e){
    if(e.key==='Enter' && document.getElementById('adminUser') && document.activeElement && ['adminUser','adminPassword'].indexOf(document.activeElement.id)>=0){
      e.preventDefault();
      window.adminLogin();
    }
  });
})();
</script>
'''

if 'smyle-v41-login-recovery' not in html:
    pos=html.rfind('</body>')
    if pos < 0:
        raise RuntimeError('</body> não encontrado')
    html=html[:pos]+js+'\n'+html[pos:]

path.write_text(html,encoding='utf-8')
print('Patch V41 aplicado: recuperação de login e migração automática de usuários.')
