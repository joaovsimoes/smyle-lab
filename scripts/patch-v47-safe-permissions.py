from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

# Smyle Lab V47
# Mantém o login/usuários exatamente no mecanismo anterior às novas permissões.
# As permissões entram somente como camada de interface, sem migrar usuários,
# alterar senha, status, username ou localStorage.

old_roles = '''<select id="uRole">
                <option value="Administrador">Administrador</option>
                <option value="Editor">Editor</option>
                <option value="Analista">Analista</option>
              </select>'''
new_roles = '''<select id="uRole" onchange="smyleSafeRoleHint()">
                <option value="Smyle Go ✦">Smyle Go ✦</option>
                <option value="Smyle Creator 🧪">Smyle Creator 🧪</option>
                <option value="Smyle Core ◉">Smyle Core ◉</option>
              </select>
              <small id="smyleSafeRoleDescription" class="smyle-safe-role-description"></small>'''
html = html.replace(old_roles, new_roles, 1)

css = r'''
<style id="smyle-v47-safe-permissions-style">
  #userModal .smyle-safe-role-description{
    display:block;margin-top:7px;color:#687D94;font-size:11px;line-height:1.45;font-weight:600;
  }

  body[data-smyle-access="go"] #gameAdminAddBtn,
  body[data-smyle-access="go"] .report-head-actions,
  body[data-smyle-access="go"] .side-link[data-page="settings"],
  body[data-smyle-access="go"] .v22-content-actions button:not(.game-test-btn){display:none!important}

  body[data-smyle-access="creator"] #settingsUsersTab,
  body[data-smyle-access="creator"] #settingsUsersPane{display:none!important}

  body[data-smyle-access="go"] #settingsUsersTab,
  body[data-smyle-access="go"] #settingsUsersPane{display:none!important}
</style>
'''
if 'smyle-v47-safe-permissions-style' not in html:
    html = html.replace('</head>', css + '\n</head>', 1)

js = r'''
<script id="smyle-v47-safe-permissions">
(function(){
  var GO='Smyle Go ✦';
  var CREATOR='Smyle Creator 🧪';
  var CORE='Smyle Core ◉';

  function norm(v){ return String(v||'').trim().toLowerCase(); }

  function normalizeRole(role){
    var r=norm(role);
    if(r.indexOf('smyle core')>=0 || r==='administrador' || r==='admin') return CORE;
    if(r.indexOf('smyle creator')>=0 || r==='editor') return CREATOR;
    if(r.indexOf('smyle go')>=0 || r==='analista') return GO;
    return GO;
  }
  window.smyleNormalizeRole=normalizeRole;

  window.smyleSafeRoleHint=function(){
    var select=document.getElementById('uRole');
    var hint=document.getElementById('smyleSafeRoleDescription');
    if(!select || !hint) return;
    var role=normalizeRole(select.value);
    if(role===CORE) hint.textContent='Acesso completo: jogos, conteúdos, relatórios, configurações e gestão de usuários.';
    else if(role===CREATOR) hint.textContent='Cria e gerencia conteúdos, configura jogos e pode emitir, imprimir e exportar relatórios.';
    else hint.textContent='Acessa a Visão Geral, testa os jogos e consulta relatórios, sem alterar conteúdos ou configurações.';
  };

  function currentUser(){
    try{
      if(typeof getCurrentAdminUser==='function') return getCurrentAdminUser();
    }catch(e){}
    try{
      var id=sessionStorage.getItem('smyle_lab_current_user_id');
      if(id && typeof getUsers==='function'){
        var users=getUsers();
        if(Array.isArray(users)) return users.find(function(u){return String(u.id||'')===String(id);}) || null;
      }
    }catch(e){}
    return null;
  }

  window.smyleApplyAccessPermissions=function(){
    var u=currentUser();
    var role=normalizeRole(u && u.role ? u.role : CORE);
    var key=role===CORE?'core':(role===CREATOR?'creator':'go');
    document.body.setAttribute('data-smyle-access',key);

    var usersTab=document.getElementById('settingsUsersTab');
    var usersPane=document.getElementById('settingsUsersPane');
    if(usersTab) usersTab.style.display=key==='core'?'':'none';
    if(usersPane && key!=='core') usersPane.classList.remove('active');

    var settingsLink=document.querySelector('.side-link[data-page="settings"]');
    if(settingsLink) settingsLink.style.display=key==='go'?'none':'';

    var reportActions=document.querySelector('.report-head-actions');
    if(reportActions) reportActions.style.display=key==='go'?'none':'';

    var addBtn=document.getElementById('gameAdminAddBtn');
    if(addBtn) addBtn.style.display=key==='go'?'none':'';

    document.querySelectorAll('.v22-content-actions').forEach(function(group){
      group.querySelectorAll('button').forEach(function(btn){
        var text=String(btn.textContent||'').trim().toLowerCase();
        var isTest=btn.classList.contains('game-test-btn') || text==='testar';
        btn.style.display=(key==='go' && !isTest)?'none':'';
      });
    });

    var pwd=document.getElementById('settingPassword');
    if(pwd && pwd.closest('.form-group')) pwd.closest('.form-group').style.display=key==='core'?'':'none';
  };

  function keepRoleSelectorCompatible(){
    var select=document.getElementById('uRole');
    if(!select) return;
    var value=normalizeRole(select.value);
    var values=Array.from(select.options||[]).map(function(o){return o.value;});
    if(values.indexOf(GO)<0 || values.indexOf(CREATOR)<0 || values.indexOf(CORE)<0){
      select.innerHTML='<option value="'+GO+'">'+GO+'</option><option value="'+CREATOR+'">'+CREATOR+'</option><option value="'+CORE+'">'+CORE+'</option>';
    }
    select.value=value;
    window.smyleSafeRoleHint();
  }

  // Importante: NÃO sobrescreve adminLogin, getUsers, saveUsers ou saveSettings.
  // Apenas observa quando a área administrativa é aberta e aplica as permissões.
  document.addEventListener('click',function(){
    setTimeout(function(){
      keepRoleSelectorCompatible();
      if(document.getElementById('adminScreen') && !document.getElementById('adminScreen').classList.contains('hidden')){
        window.smyleApplyAccessPermissions();
      }
    },30);
  },true);

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',function(){keepRoleSelectorCompatible();});
  }else{
    keepRoleSelectorCompatible();
  }
})();
</script>
'''

if 'smyle-v47-safe-permissions' not in html:
    pos = html.rfind('</body>')
    if pos < 0:
        raise RuntimeError('</body> não encontrado')
    html = html[:pos] + js + '\n' + html[pos:]

path.write_text(html, encoding='utf-8')
print('Patch V47 aplicado: permissões sem interferir no login ou nas credenciais.')
