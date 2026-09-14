from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

js = r'''
<script id="smyle-v42-core-password-sync">
(function(){
  function norm(v){ return String(v||'').trim().toLowerCase(); }
  function isCore(u){
    if(!u) return false;
    var role=norm(u.role);
    return String(u.id||'')==='admin-default' || role.indexOf('smyle core')>=0 || role==='administrador' || role==='admin';
  }

  function readAllUsers(){
    var out=[];
    var seen=new Set();
    function add(u,source){
      if(!u || typeof u!=='object') return;
      var username=String(u.username||u.user||u.login||'').trim();
      if(!username) return;
      var row=Object.assign({},u,{username:username,__source:source||''});
      var key=[norm(username),String(row.id||''),String(row.password||'')].join('|');
      if(seen.has(key)) return;
      seen.add(key); out.push(row);
    }

    try{
      if(typeof getUsers==='function'){
        var list=getUsers();
        if(Array.isArray(list)) list.forEach(function(u){add(u,'getUsers');});
      }
    }catch(e){}

    try{
      for(var i=0;i<localStorage.length;i++){
        var k=localStorage.key(i); if(!k) continue;
        var raw=localStorage.getItem(k); if(!raw || raw.length>3000000) continue;
        var val; try{ val=JSON.parse(raw); }catch(e){ continue; }
        if(Array.isArray(val)) val.forEach(function(u){add(u,k);});
        else if(val && typeof val==='object'){
          if(Array.isArray(val.users)) val.users.forEach(function(u){add(u,k+'.users');});
          if('username' in val || 'user' in val || 'login' in val) add(val,k);
        }
      }
    }catch(e){}
    return out;
  }

  function settingsPassword(){
    var vals=[];
    try{
      if(typeof getSettings==='function'){
        var s=getSettings();
        if(s && s.adminPassword) vals.push(String(s.adminPassword));
      }
    }catch(e){}

    try{
      for(var i=0;i<localStorage.length;i++){
        var k=localStorage.key(i); if(!k) continue;
        var raw=localStorage.getItem(k); if(!raw || raw.length>1000000) continue;
        var val; try{ val=JSON.parse(raw); }catch(e){ continue; }
        if(val && typeof val==='object'){
          if(val.adminPassword) vals.push(String(val.adminPassword));
          if(val.settings && val.settings.adminPassword) vals.push(String(val.settings.adminPassword));
        }
      }
    }catch(e){}
    return vals.filter(Boolean);
  }

  function saveCanonical(found,password){
    try{
      if(typeof getUsers!=='function' || typeof saveUsers!=='function') return;
      var users=getUsers(); if(!Array.isArray(users)) users=[];
      var uname=norm(found.username);
      var idx=users.findIndex(function(u){
        return String(u.id||'')===String(found.id||'') || norm(u.username)===uname;
      });
      var row={
        id:(found.id || (idx>=0&&users[idx].id) || 'admin-default'),
        name:found.name || (idx>=0&&users[idx].name) || 'Administrador',
        username:String(found.username||'').trim(),
        password:String(password||found.password||''),
        role:(typeof smyleNormalizeRole==='function'?smyleNormalizeRole(found.role):(found.role||'Smyle Core ◉')),
        active:found.active!==false,
        photo:found.photo || (idx>=0&&users[idx].photo) || ''
      };
      if(idx>=0) users[idx]=Object.assign({},users[idx],row);
      else users.unshift(row);
      saveUsers(users);
    }catch(e){ console.warn('Falha ao sincronizar usuário Core',e); }
  }

  function showError(msg){
    var old=document.getElementById('smyleLoginErrorBox'); if(old) old.remove();
    var pass=document.getElementById('adminPassword');
    var box=document.createElement('div');
    box.id='smyleLoginErrorBox';
    box.textContent=msg;
    box.style.cssText='margin:12px 0 0;padding:12px 14px;border-radius:12px;background:#EFF8F9;border:1px solid #CDEDEA;color:#0C2340;font-size:13px;font-weight:700;line-height:1.4;text-align:left;';
    if(pass&&pass.parentElement) pass.parentElement.insertAdjacentElement('afterend',box);
  }

  function enter(found,password){
    saveCanonical(found,password);
    try{ sessionStorage.setItem(KEYS.adminSession,'1'); }catch(e){}
    try{ sessionStorage.setItem('smyle_lab_current_user_id',found.id||'admin-default'); }catch(e){}
    var effective=Object.assign({},found,{password:String(password||found.password||'')});
    try{ if(typeof setCurrentAdminUser==='function') setCurrentAdminUser(effective); }catch(e){}
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
    var uf=document.getElementById('adminUser');
    var pf=document.getElementById('adminPassword');
    if(!uf||!pf){ showError('Não foi possível localizar os campos de acesso.'); return; }
    var username=norm(uf.value), password=String(pf.value||'');
    if(!username||!password){ showError('Informe seu usuário e senha.'); return; }

    var users=readAllUsers();
    var exact=users.find(function(u){
      return u.active!==false && norm(u.username)===username && String(u.password||'')===password;
    });
    if(exact){ enter(exact,password); return; }

    var sameUser=users.filter(function(u){ return u.active!==false && norm(u.username)===username; });
    var candidate=sameUser[0] || null;

    // Se for o usuário Core principal, também aceita qualquer senha administrativa
    // válida encontrada nas configurações/versões antigas e sincroniza o cadastro.
    if(candidate && isCore(candidate)){
      var pwds=settingsPassword();
      users.filter(isCore).forEach(function(u){ if(u.password) pwds.push(String(u.password)); });
      var valid=pwds.some(function(p){ return p===password; });
      if(valid){ enter(candidate,password); return; }
    }

    // Compatibilidade para o admin renomeado: se existir exatamente um Smyle Core,
    // usa o nome de usuário digitado quando a senha administrativa confere.
    var coreUsers=users.filter(function(u){ return u.active!==false && isCore(u); });
    if(!candidate && coreUsers.length===1){
      var pwds2=settingsPassword();
      if(coreUsers[0].password) pwds2.push(String(coreUsers[0].password));
      if(pwds2.some(function(p){return p===password;})){
        var recovered=Object.assign({},coreUsers[0],{username:String(uf.value||'').trim(),role:'Smyle Core ◉'});
        enter(recovered,password); return;
      }
    }

    showError('Usuário ou senha incorretos.');
  };
})();
</script>
'''

if 'smyle-v42-core-password-sync' not in html:
    pos=html.rfind('</body>')
    if pos<0: raise RuntimeError('</body> não encontrado')
    html=html[:pos]+js+'\n'+html[pos:]

path.write_text(html,encoding='utf-8')
print('Patch V42 aplicado: sincronização do usuário/senha Smyle Core.')
