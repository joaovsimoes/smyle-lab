from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

js = r'''
<script id="smyle-v45-auth-record-fix">
(function(){
  function norm(v){ return String(v||'').trim().toLowerCase(); }

  function normalizeStatusSelect(){
    var select=document.getElementById('uStatus');
    if(!select) return;
    Array.from(select.options||[]).forEach(function(opt){
      var t=norm(opt.textContent);
      if(t==='ativo' || t==='active') opt.value='active';
      if(t==='inativo' || t==='inactive' || t==='desativado') opt.value='inactive';
    });
  }

  function passwordValues(u){
    var vals=[];
    if(!u || typeof u!=='object') return vals;
    ['password','senha','pass'].forEach(function(k){
      if(u[k]!==undefined && u[k]!==null && String(u[k])!=='') vals.push(String(u[k]));
    });
    return vals;
  }

  function isCore(u){
    if(!u || typeof u!=='object') return false;
    var role=norm(u.role||u.perfil||u.profile||'');
    return String(u.id||u.uid||'')==='admin-default' || role.indexOf('smyle core')>=0 || role==='administrador' || role==='admin';
  }

  function isActive(u){
    if(isCore(u)) return true;
    if(!u || typeof u!=='object') return true;
    if(u.active===false) return false;
    var raw=norm(u.active);
    if(['false','0','inactive','inativo','desativado','disabled'].indexOf(raw)>=0) return false;
    var status=norm(u.status||'');
    if(['inactive','inativo','desativado','disabled'].indexOf(status)>=0) return false;
    return true;
  }

  function collectUsers(){
    var out=[];
    var seen=new Set();
    function add(u,source){
      if(!u || typeof u!=='object') return;
      var username=String(u.username||u.user||u.login||'').trim();
      if(!username) return;
      var row=Object.assign({},u,{username:username,__source:source||''});
      var key=[norm(username),String(row.id||row.uid||''),passwordValues(row).join('§')].join('|');
      if(seen.has(key)) return;
      seen.add(key);
      out.push(row);
    }

    try{
      if(typeof getUsers==='function'){
        var list=getUsers();
        if(Array.isArray(list)) list.forEach(function(u){ add(u,'getUsers'); });
      }
    }catch(e){ console.warn('Smyle Auth: getUsers falhou',e); }

    try{
      for(var i=0;i<localStorage.length;i++){
        var key=localStorage.key(i); if(!key) continue;
        var raw=localStorage.getItem(key); if(!raw || raw.length>3000000) continue;
        var parsed; try{ parsed=JSON.parse(raw); }catch(ignore){ continue; }
        if(Array.isArray(parsed)) parsed.forEach(function(u){ add(u,key); });
        else if(parsed && typeof parsed==='object'){
          if(Array.isArray(parsed.users)) parsed.users.forEach(function(u){ add(u,key+'.users'); });
          if('username' in parsed || 'user' in parsed || 'login' in parsed) add(parsed,key);
        }
      }
    }catch(e){ console.warn('Smyle Auth: varredura local falhou',e); }
    return out;
  }

  function settingsPasswords(){
    var vals=[];
    try{
      if(typeof getSettings==='function'){
        var s=getSettings();
        if(s && s.adminPassword) vals.push(String(s.adminPassword));
      }
    }catch(e){}
    return vals;
  }

  function showError(msg){
    var old=document.getElementById('smyleLoginErrorBox'); if(old) old.remove();
    var pass=document.getElementById('adminPassword');
    var box=document.createElement('div');
    box.id='smyleLoginErrorBox';
    box.textContent=msg;
    box.style.cssText='margin:12px 0 0;padding:12px 14px;border-radius:12px;background:#EFF8F9;border:1px solid #CDEDEA;color:#0C2340;font-size:13px;font-weight:700;line-height:1.4;text-align:left;';
    if(pass && pass.parentElement) pass.parentElement.insertAdjacentElement('afterend',box);
  }

  function repairCanonical(found,password,typedUsername){
    try{
      if(typeof getUsers!=='function' || typeof saveUsers!=='function') return found;
      var users=getUsers(); if(!Array.isArray(users)) users=[];
      var foundId=String(found.id||found.uid||'');
      var uname=norm(found.username||typedUsername);
      var idx=users.findIndex(function(u){
        return (foundId && String(u.id||'')===foundId) || norm(u.username)===uname;
      });
      var base=idx>=0?users[idx]:{};
      var row=Object.assign({},base,found,{
        id:foundId || base.id || ('user-'+Date.now()),
        username:String(found.username||typedUsername||base.username||'').trim(),
        password:String(password),
        active:isCore(found)?true:isActive(found),
        role:(typeof smyleNormalizeRole==='function' ? smyleNormalizeRole(found.role||base.role) : (found.role||base.role||'Smyle Go ✦'))
      });
      delete row.__source;
      if(idx>=0) users[idx]=row; else users.unshift(row);
      saveUsers(users);
      return row;
    }catch(e){
      console.warn('Smyle Auth: reparo canônico falhou',e);
      return Object.assign({},found,{password:String(password),active:isCore(found)?true:isActive(found)});
    }
  }

  function enter(found,password,typedUsername){
    var user=repairCanonical(found,password,typedUsername);
    try{ sessionStorage.setItem(KEYS.adminSession,'1'); }catch(e){}
    try{ sessionStorage.setItem('smyle_lab_current_user_id',user.id||'admin-default'); }catch(e){}
    try{ if(typeof setCurrentAdminUser==='function') setCurrentAdminUser(user); }catch(e){}
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
    var pf=document.getElementById('adminPassword'); if(pf) pf.value='';
    var err=document.getElementById('smyleLoginErrorBox'); if(err) err.remove();
  }

  window.adminLogin=function(){
    normalizeStatusSelect();
    var uf=document.getElementById('adminUser');
    var pf=document.getElementById('adminPassword');
    if(!uf || !pf){ showError('Não foi possível localizar os campos de acesso.'); return; }

    var typedUsername=String(uf.value||'').trim();
    var username=norm(typedUsername);
    var password=String(pf.value||'');
    if(!username || !password){ showError('Informe seu usuário e senha.'); return; }

    var users=collectUsers();
    var sameUser=users.filter(function(u){ return norm(u.username)===username; });

    var match=sameUser.find(function(u){
      return passwordValues(u).some(function(p){ return p===password; });
    });

    if(!match){
      var coreCandidate=sameUser.find(isCore);
      if(coreCandidate){
        var settingsMatch=settingsPasswords().some(function(p){ return p===password; });
        if(settingsMatch) match=coreCandidate;
      }
    }

    if(!match){
      showError('Usuário ou senha incorretos.');
      return;
    }

    if(!isActive(match) && !isCore(match)){
      showError('Este usuário está inativo.');
      return;
    }

    enter(match,password,typedUsername);
  };

  function boot(){
    normalizeStatusSelect();
    var recovery=document.getElementById('smyleRecoveryButton'); if(recovery) recovery.remove();
    var recoveryModal=document.getElementById('smyleRecoveryModal'); if(recoveryModal) recoveryModal.remove();
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
  else boot();
  setTimeout(boot,300);
})();
</script>
'''

if 'smyle-v45-auth-record-fix' not in html:
    pos=html.rfind('</body>')
    if pos<0: raise RuntimeError('</body> não encontrado')
    html=html[:pos]+js+'\n'+html[pos:]

path.write_text(html,encoding='utf-8')
print('Patch V45 aplicado: autenticação reparada pelo registro real do usuário e status normalizado.')
