from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

js = r'''
<script id="smyle-v49-local-core-repair">
(function(){
  function norm(v){ return String(v||'').trim().toLowerCase(); }

  function normalizeRole(role){
    var r=norm(role);
    if(r.indexOf('smyle core')>=0 || r==='administrador' || r==='admin') return 'Smyle Core ◉';
    if(r.indexOf('smyle creator')>=0 || r==='editor') return 'Smyle Creator 🧪';
    if(r.indexOf('smyle go')>=0 || r==='analista') return 'Smyle Go ✦';
    return role || 'Smyle Go ✦';
  }

  function isCore(u){
    if(!u || typeof u!=='object') return false;
    var role=norm(u.role||u.perfil||u.profile||'');
    return String(u.id||u.uid||'')==='admin-default' || role.indexOf('smyle core')>=0 || role==='administrador' || role==='admin';
  }

  function passwordValues(u){
    var out=[];
    if(!u || typeof u!=='object') return out;
    ['password','senha','pass'].forEach(function(k){
      if(u[k]!==undefined && u[k]!==null && String(u[k])!=='') out.push(String(u[k]));
    });
    return out;
  }

  function canonicalUsers(){
    try{
      var list=(typeof getUsers==='function') ? getUsers() : [];
      return Array.isArray(list) ? list : [];
    }catch(e){ return []; }
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

    canonicalUsers().forEach(function(u){ add(u,'canonical'); });

    try{
      for(var i=0;i<localStorage.length;i++){
        var k=localStorage.key(i); if(!k) continue;
        var raw=localStorage.getItem(k); if(!raw || raw.length>3000000) continue;
        var parsed; try{ parsed=JSON.parse(raw); }catch(ignore){ continue; }

        function walk(value,depth){
          if(depth>4 || value===null || value===undefined) return;
          if(Array.isArray(value)){
            value.forEach(function(item){ walk(item,depth+1); });
            return;
          }
          if(typeof value!=='object') return;
          if('username' in value || 'user' in value || 'login' in value) add(value,k);
          if(Array.isArray(value.users)) value.users.forEach(function(item){ add(item,k+'.users'); });
          Object.keys(value).forEach(function(key){
            if(key==='photo' || key==='image' || key==='avatar') return;
            var child=value[key];
            if(child && (Array.isArray(child) || typeof child==='object')) walk(child,depth+1);
          });
        }
        walk(parsed,0);
      }
    }catch(e){ console.warn('Smyle V49: falha ao ler bases antigas',e); }
    return out;
  }

  function settingsPasswords(){
    var out=[];
    function add(v){ if(v!==undefined && v!==null && String(v)!=='') out.push(String(v)); }
    try{
      if(typeof getSettings==='function'){
        var s=getSettings();
        if(s){ add(s.adminPassword); add(s.password); }
      }
    }catch(e){}
    try{
      for(var i=0;i<localStorage.length;i++){
        var k=localStorage.key(i); if(!k) continue;
        var raw=localStorage.getItem(k); if(!raw || raw.length>1000000) continue;
        var v; try{v=JSON.parse(raw);}catch(ignore){continue;}
        if(v && typeof v==='object'){
          add(v.adminPassword);
          if(v.settings && typeof v.settings==='object') add(v.settings.adminPassword);
        }
      }
    }catch(e){}
    return Array.from(new Set(out));
  }

  function showError(message){
    var old=document.getElementById('smyleLoginErrorBox'); if(old) old.remove();
    var pass=document.getElementById('adminPassword');
    var box=document.createElement('div');
    box.id='smyleLoginErrorBox';
    box.textContent=message;
    box.style.cssText='margin:12px 0 0;padding:12px 14px;border-radius:12px;background:#EFF8F9;border:1px solid #CDEDEA;color:#0C2340;font-size:13px;font-weight:750;line-height:1.45;text-align:left;';
    if(pass && pass.parentElement) pass.parentElement.insertAdjacentElement('afterend',box);
    else alert(message);
  }

  function repairCanonical(found,password,typedUsername){
    try{
      if(typeof saveUsers!=='function') return Object.assign({},found,{password:password});
      var users=canonicalUsers();
      var id=String(found.id||found.uid||'');
      var uname=norm(found.username||typedUsername);
      var idx=users.findIndex(function(u){
        return (id && String(u.id||'')===id) || norm(u.username)===uname;
      });
      var base=idx>=0 ? users[idx] : {};
      var row=Object.assign({},base,found,{
        id:id || base.id || 'admin-default',
        name:found.name || base.name || 'Administrador',
        username:String(found.username||typedUsername||base.username||'').trim(),
        password:String(password),
        role:normalizeRole(found.role||base.role||'Smyle Core ◉'),
        active:true,
        photo:found.photo || base.photo || ''
      });
      delete row.__source;
      delete row.senha;
      delete row.pass;
      if(idx>=0) users[idx]=row; else users.unshift(row);
      saveUsers(users);

      try{
        if(typeof getSettings==='function' && typeof setSettings==='function' && isCore(row)){
          var s=getSettings()||{};
          s.adminPassword=String(password);
          setSettings(s);
        }
      }catch(ignore){}
      return row;
    }catch(e){
      console.warn('Smyle V49: reparo canônico falhou',e);
      return Object.assign({},found,{password:String(password),active:true});
    }
  }

  function enter(found,password,typedUsername,wasRepair){
    var user=repairCanonical(found,password,typedUsername);
    try{ sessionStorage.setItem(KEYS.adminSession,'1'); }catch(e){}
    try{ sessionStorage.setItem('smyle_lab_current_user_id',user.id||'admin-default'); }catch(e){}
    try{ if(typeof setCurrentAdminUser==='function') setCurrentAdminUser(user); }catch(e){}
    try{ if(wasRepair) localStorage.setItem('smyle_lab_v49_repaired_'+String(user.id||'admin-default'),'1'); }catch(e){}

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
      var core=sameUser.find(isCore);
      if(core && settingsPasswords().some(function(p){return p===password;})) match=core;
    }

    if(match){
      enter(match,password,typedUsername,false);
      return;
    }

    // Recuperação única e não destrutiva para o Smyle Core já existente neste navegador.
    // Só funciona se o usuário digitado for exatamente o usuário já salvo no registro Core.
    var canonical=canonicalUsers();
    var localCore=canonical.find(function(u){ return isCore(u) && norm(u.username)===username; });
    if(localCore){
      var flag='smyle_lab_v49_repaired_'+String(localCore.id||'admin-default');
      var already=false;
      try{ already=localStorage.getItem(flag)==='1'; }catch(e){}
      if(!already){
        enter(localCore,password,typedUsername,true);
        return;
      }
      showError('A senha informada não confere com o acesso salvo neste navegador.');
      return;
    }

    var primary=canonical.find(function(u){ return isCore(u); });
    if(primary && primary.username){
      showError('O usuário informado não corresponde ao acesso Smyle Core salvo neste navegador.');
    }else{
      showError('Usuário não localizado neste navegador.');
    }
  };

  document.addEventListener('keydown',function(e){
    if(e.key==='Enter' && document.activeElement && ['adminUser','adminPassword'].indexOf(document.activeElement.id)>=0){
      e.preventDefault();
      window.adminLogin();
    }
  });
})();
</script>
'''

if 'smyle-v49-local-core-repair' not in html:
    pos=html.rfind('</body>')
    if pos<0: raise RuntimeError('</body> não encontrado')
    html=html[:pos]+js+'\n'+html[pos:]

path.write_text(html,encoding='utf-8')
print('Patch V49 aplicado: reparo único e local do Smyle Core habilitado.')
