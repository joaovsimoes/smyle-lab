from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

css = r'''
<style id="smyle-v43-recovery-style">
  #smyleRecoveryButton{
    width:100%;
    margin-top:12px;
    padding:10px 14px;
    border:0;
    background:transparent;
    color:#0C2340;
    font:inherit;
    font-size:13px;
    font-weight:800;
    cursor:pointer;
    text-decoration:none;
  }
  #smyleRecoveryButton:hover{color:#168F8A;text-decoration:underline}
  #smyleRecoveryModal{
    position:fixed;
    inset:0;
    z-index:1000000;
    display:none;
    align-items:center;
    justify-content:center;
    padding:20px;
    background:rgba(8,26,46,.46);
    backdrop-filter:blur(10px);
    -webkit-backdrop-filter:blur(10px);
  }
  #smyleRecoveryModal.open{display:flex}
  #smyleRecoveryModal .recovery-card{
    width:min(470px,calc(100vw - 32px));
    padding:28px;
    border-radius:26px;
    background:#fff;
    border:1px solid rgba(12,35,64,.08);
    box-shadow:0 30px 90px rgba(8,26,46,.22);
  }
  #smyleRecoveryModal .recovery-kicker{
    margin:0 0 8px;
    color:#168F8A;
    font-size:11px;
    font-weight:900;
    letter-spacing:.14em;
    text-transform:uppercase;
  }
  #smyleRecoveryModal h3{margin:0 0 8px;color:#0C2340;font-size:24px}
  #smyleRecoveryModal p{margin:0 0 20px;color:#617690;font-size:14px;line-height:1.5}
  #smyleRecoveryModal label{display:block;margin:14px 0 7px;color:#0C2340;font-size:13px;font-weight:800}
  #smyleRecoveryModal input{
    width:100%;
    min-height:48px;
    padding:0 14px;
    border:1px solid #D7E0E7;
    border-radius:14px;
    background:#fff;
    color:#0C2340;
    font:inherit;
    outline:none;
  }
  #smyleRecoveryModal input:focus{border-color:#63D9CF;box-shadow:0 0 0 3px rgba(99,217,207,.18)}
  #smyleRecoveryError{
    display:none;
    margin-top:12px;
    padding:11px 12px;
    border-radius:12px;
    background:#EFF8F9;
    border:1px solid #CDEDEA;
    color:#0C2340;
    font-size:13px;
    font-weight:700;
  }
  #smyleRecoveryError.show{display:block}
  #smyleRecoveryModal .recovery-actions{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:18px}
  #smyleRecoveryModal .recovery-actions button{
    min-height:46px;
    border-radius:13px;
    border:1px solid #D7E0E7;
    font:inherit;
    font-weight:800;
    cursor:pointer;
  }
  #smyleRecoveryCancel{background:#fff;color:#0C2340}
  #smyleRecoverySave{background:#0C2340!important;color:#fff!important;border-color:#0C2340!important}
  #smyleRecoverySuccess{
    display:none;
    margin-top:14px;
    padding:12px;
    border-radius:12px;
    background:#EAF9F7;
    border:1px solid #B8ECE7;
    color:#0C2340;
    font-size:13px;
    font-weight:800;
  }
  #smyleRecoverySuccess.show{display:block}
</style>
'''
if 'smyle-v43-recovery-style' not in html:
    html = html.replace('</head>', css + '\n</head>', 1)

js = r'''
<script id="smyle-v43-local-access-recovery">
(function(){
  function norm(v){ return String(v||'').trim().toLowerCase(); }
  function isCore(u){
    if(!u || typeof u!=='object') return false;
    var role=norm(u.role||u.perfil||u.profile||'');
    return String(u.id||u.uid||'')==='admin-default' || role.indexOf('smyle core')>=0 || role==='administrador' || role==='admin';
  }

  function collectUsers(){
    var out=[];
    var seen=new Set();
    function add(u,source){
      if(!u || typeof u!=='object') return;
      var username=String(u.username||u.user||u.login||'').trim();
      if(!username) return;
      var row=Object.assign({},u,{username:username,__source:source||''});
      var key=[norm(username),String(row.id||row.uid||''),String(row.role||row.perfil||'')].join('|');
      if(seen.has(key)) return;
      seen.add(key);
      out.push(row);
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
        var val; try{val=JSON.parse(raw);}catch(e){continue;}
        if(Array.isArray(val)) val.forEach(function(u){add(u,k);});
        else if(val && typeof val==='object'){
          if(Array.isArray(val.users)) val.users.forEach(function(u){add(u,k+'.users');});
          if('username' in val || 'user' in val || 'login' in val) add(val,k);
        }
      }
    }catch(e){}
    return out;
  }

  function findCore(username){
    var users=collectUsers().filter(function(u){return u.active!==false;});
    var exact=users.find(function(u){return norm(u.username)===norm(username) && isCore(u);});
    if(exact) return exact;
    var core=users.filter(isCore);
    var unique=[];
    var keys=new Set();
    core.forEach(function(u){
      var key=String(u.id||'')+'|'+norm(u.username);
      if(!keys.has(key)){keys.add(key);unique.push(u);}
    });
    return unique.length===1 ? unique[0] : null;
  }

  function patchLocalStorage(target,newPassword,typedUsername){
    var targetId=String(target.id||target.uid||'');
    var targetUser=norm(target.username);
    var desiredUsername=String(typedUsername||target.username||'').trim();

    function shouldPatch(u){
      if(!u || typeof u!=='object') return false;
      var uid=String(u.id||u.uid||'');
      var uname=norm(u.username||u.user||u.login||'');
      if(targetId && uid && uid===targetId) return true;
      if(targetUser && uname===targetUser) return true;
      return false;
    }

    try{
      for(var i=localStorage.length-1;i>=0;i--){
        var k=localStorage.key(i); if(!k) continue;
        var raw=localStorage.getItem(k); if(!raw || raw.length>3000000) continue;
        var val; try{val=JSON.parse(raw);}catch(e){continue;}
        var changed=false;
        function updateUser(u){
          if(!shouldPatch(u)) return u;
          changed=true;
          var copy=Object.assign({},u);
          copy.password=newPassword;
          if('senha' in copy) copy.senha=newPassword;
          if('pass' in copy) copy.pass=newPassword;
          if(desiredUsername){
            if('username' in copy || !('user' in copy) && !('login' in copy)) copy.username=desiredUsername;
            if('user' in copy) copy.user=desiredUsername;
            if('login' in copy) copy.login=desiredUsername;
          }
          return copy;
        }
        if(Array.isArray(val)) val=val.map(updateUser);
        else if(val && typeof val==='object'){
          if(Array.isArray(val.users)){
            var before=changed;
            val.users=val.users.map(updateUser);
            changed=changed||before;
          }
          if(shouldPatch(val)) val=updateUser(val);
          if(val.adminPassword!==undefined){val.adminPassword=newPassword;changed=true;}
          if(val.settings && typeof val.settings==='object' && val.settings.adminPassword!==undefined){val.settings.adminPassword=newPassword;changed=true;}
        }
        if(changed){
          try{localStorage.setItem(k,JSON.stringify(val));}catch(e){}
        }
      }
    }catch(e){console.warn('Falha ao sincronizar bases antigas',e);}

    try{
      if(typeof getUsers==='function' && typeof saveUsers==='function'){
        var users=getUsers(); if(!Array.isArray(users)) users=[];
        var idx=users.findIndex(function(u){
          return (targetId && String(u.id||'')===targetId) || norm(u.username)===targetUser;
        });
        if(idx<0){
          users.unshift({
            id:targetId||'admin-default',
            name:target.name||'Administrador',
            username:desiredUsername||target.username,
            password:newPassword,
            role:'Smyle Core ◉',
            active:true,
            photo:target.photo||''
          });
        }else{
          users[idx]=Object.assign({},users[idx],{
            username:desiredUsername||users[idx].username,
            password:newPassword,
            role:'Smyle Core ◉',
            active:true
          });
        }
        saveUsers(users);
      }
    }catch(e){console.warn('Falha na base canônica',e);}

    try{
      if(typeof getSettings==='function' && typeof setSettings==='function'){
        var s=getSettings()||{};
        s.adminPassword=newPassword;
        setSettings(s);
      }
    }catch(e){}
  }

  function ensureModal(){
    var modal=document.getElementById('smyleRecoveryModal');
    if(modal) return modal;
    modal=document.createElement('div');
    modal.id='smyleRecoveryModal';
    modal.setAttribute('role','dialog');
    modal.setAttribute('aria-modal','true');
    modal.innerHTML=''
      +'<div class="recovery-card">'
      +'<div class="recovery-kicker">Smyle Core</div>'
      +'<h3>Recuperar acesso</h3>'
      +'<p>Redefina a senha do acesso principal neste navegador. Sua nova senha não é enviada para o chat.</p>'
      +'<label for="smyleRecoveryUsername">Usuário</label>'
      +'<input id="smyleRecoveryUsername" autocomplete="username" />'
      +'<label for="smyleRecoveryPassword">Nova senha</label>'
      +'<input id="smyleRecoveryPassword" type="password" autocomplete="new-password" />'
      +'<label for="smyleRecoveryConfirm">Confirmar nova senha</label>'
      +'<input id="smyleRecoveryConfirm" type="password" autocomplete="new-password" />'
      +'<div id="smyleRecoveryError"></div>'
      +'<div id="smyleRecoverySuccess">Senha redefinida. Entrando no painel...</div>'
      +'<div class="recovery-actions"><button type="button" id="smyleRecoveryCancel">Cancelar</button><button type="button" id="smyleRecoverySave">Redefinir senha</button></div>'
      +'</div>';
    document.body.appendChild(modal);
    modal.addEventListener('click',function(e){if(e.target===modal) closeRecovery();});
    modal.querySelector('#smyleRecoveryCancel').addEventListener('click',closeRecovery);
    modal.querySelector('#smyleRecoverySave').addEventListener('click',saveRecovery);
    return modal;
  }

  function showRecoveryError(msg){
    var el=document.getElementById('smyleRecoveryError');
    if(!el) return;
    el.textContent=msg;
    el.classList.add('show');
    var s=document.getElementById('smyleRecoverySuccess'); if(s) s.classList.remove('show');
  }

  function closeRecovery(){
    var m=document.getElementById('smyleRecoveryModal'); if(m) m.classList.remove('open');
  }

  function openRecovery(){
    var modal=ensureModal();
    var loginUser=document.getElementById('adminUser');
    var u=modal.querySelector('#smyleRecoveryUsername');
    u.value=loginUser ? String(loginUser.value||'').trim() : '';
    modal.querySelector('#smyleRecoveryPassword').value='';
    modal.querySelector('#smyleRecoveryConfirm').value='';
    var err=modal.querySelector('#smyleRecoveryError'); err.classList.remove('show');err.textContent='';
    modal.querySelector('#smyleRecoverySuccess').classList.remove('show');
    modal.classList.add('open');
    setTimeout(function(){(u.value?modal.querySelector('#smyleRecoveryPassword'):u).focus();},40);
  }

  function saveRecovery(){
    var username=String(document.getElementById('smyleRecoveryUsername').value||'').trim();
    var pwd=String(document.getElementById('smyleRecoveryPassword').value||'');
    var confirm=String(document.getElementById('smyleRecoveryConfirm').value||'');
    if(!username){showRecoveryError('Informe o usuário do Smyle Core.');return;}
    if(pwd.length<6){showRecoveryError('A nova senha deve ter pelo menos 6 caracteres.');return;}
    if(pwd!==confirm){showRecoveryError('As senhas não conferem.');return;}
    var target=findCore(username);
    if(!target){
      showRecoveryError('Não encontrei um acesso Smyle Core salvo neste navegador.');
      return;
    }
    patchLocalStorage(target,pwd,username);
    var success=document.getElementById('smyleRecoverySuccess'); success.classList.add('show');
    var err=document.getElementById('smyleRecoveryError'); err.classList.remove('show');
    var loginUser=document.getElementById('adminUser'); if(loginUser) loginUser.value=username;
    var loginPass=document.getElementById('adminPassword'); if(loginPass) loginPass.value=pwd;
    setTimeout(function(){
      closeRecovery();
      if(typeof window.adminLogin==='function') window.adminLogin();
    },650);
  }

  function installButton(){
    if(document.getElementById('smyleRecoveryButton')) return;
    var gate=document.getElementById('adminGate'); if(!gate) return;
    var loginButton=gate.querySelector('button[onclick*="adminLogin"], button[type="submit"], .btn-primary, .primary-btn');
    if(!loginButton) return;
    var btn=document.createElement('button');
    btn.type='button';
    btn.id='smyleRecoveryButton';
    btn.textContent='Recuperar acesso';
    btn.addEventListener('click',openRecovery);
    loginButton.insertAdjacentElement('afterend',btn);
  }

  document.addEventListener('DOMContentLoaded',function(){ensureModal();installButton();});
  setTimeout(installButton,250);
  window.smyleOpenAccessRecovery=openRecovery;
})();
</script>
'''

if 'smyle-v43-local-access-recovery' not in html:
    pos = html.rfind('</body>')
    if pos < 0:
        raise RuntimeError('</body> não encontrado')
    html = html[:pos] + js + '\n' + html[pos:]

path.write_text(html,encoding='utf-8')
print('Patch V43 aplicado: recuperação local do acesso Smyle Core.')
