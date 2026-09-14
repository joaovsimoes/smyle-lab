from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

# ==========================================================
# Smyle Lab V40
# - corrige definitivamente o salvamento de usuários
# - torna o botão Carregar imagem legível
# - comprime a foto antes de salvar no localStorage
# - substitui perfis antigos pelos perfis oficiais Smyle
# - aplica permissões de interface por perfil
# ==========================================================

# Botão da foto: texto e handler próprios.
html = html.replace(
    '<label class="photo-upload-btn" for="uPhoto">Escolher foto</label>',
    '<label class="photo-upload-btn" for="uPhoto" aria-label="Carregar imagem">Carregar imagem</label>',
    1,
)
html = html.replace(
    'onchange="handleUserPhotoUpload(event)"',
    'onchange="smyleHandleUserPhotoUpload(event)"',
    1,
)

# Perfis oficiais do Smyle Lab.
old_roles = '''<select id="uRole">
                <option value="Administrador">Administrador</option>
                <option value="Editor">Editor</option>
                <option value="Analista">Analista</option>
              </select>'''
new_roles = '''<select id="uRole" onchange="smyleUpdateRoleDescription()">
                <option value="Smyle Go ✦">Smyle Go ✦</option>
                <option value="Smyle Creator 🧪">Smyle Creator 🧪</option>
                <option value="Smyle Core ◉">Smyle Core ◉</option>
              </select>
              <small id="uRoleDescription" class="smyle-role-description"></small>'''
html = html.replace(old_roles, new_roles, 1)

# O botão não depende mais de versões antigas de saveUserItem().
html = html.replace(
    'onclick="saveUserItem()">Salvar usuário</button>',
    'onclick="smyleSaveUserFromModal(event)">Salvar usuário</button>',
    1,
)

css = r'''
<style id="smyle-v40-access-profiles">
  /* botão de imagem sempre legível */
  #userModal label.photo-upload-btn{
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    width:140px !important;
    min-height:46px !important;
    padding:10px 14px !important;
    background:#0C2340 !important;
    border:1px solid #0C2340 !important;
    border-radius:13px !important;
    color:#fff !important;
    font-size:12px !important;
    font-weight:850 !important;
    line-height:1 !important;
    text-indent:0 !important;
    opacity:1 !important;
    visibility:visible !important;
    cursor:pointer !important;
  }
  #userModal label.photo-upload-btn::before,
  #userModal label.photo-upload-btn::after{content:none !important}
  #userModal label.photo-upload-btn:hover{background:#18355C !important;border-color:#18355C !important}

  #userModal .smyle-role-description{
    display:block !important;
    margin-top:7px !important;
    color:#687D94 !important;
    font-size:11px !important;
    line-height:1.45 !important;
    font-weight:600 !important;
  }

  /* badges dos novos perfis */
  .user-role-badge[data-smyle-role="core"]{background:#0C2340 !important;color:#fff !important;border-color:#0C2340 !important}
  .user-role-badge[data-smyle-role="creator"]{background:#DDF8F5 !important;color:#0C2340 !important;border-color:#9BE8E1 !important}
  .user-role-badge[data-smyle-role="go"]{background:#EFF8F9 !important;color:#18355C !important;border-color:#D5EAED !important}

  /* Smyle Go: consulta e testes, sem edição/configuração/exportação */
  body[data-smyle-access="go"] .side-link[data-page="settings"],
  body[data-smyle-access="go"] #gameAdminAddBtn,
  body[data-smyle-access="go"] .report-head-actions,
  body[data-smyle-access="go"] .v22-content-actions button:not(.game-test-btn){display:none !important}

  /* Creator: sem gestão de usuários e sem troca de senha administrativa */
  body[data-smyle-access="creator"] #settingsUsersTab,
  body[data-smyle-access="creator"] #settingsUsersPane,
  body[data-smyle-access="creator"] #settingPassword{display:none !important}
  body[data-smyle-access="creator"] #settingPassword + *{display:none !important}
  body[data-smyle-access="creator"] .form-group:has(#settingPassword){display:none !important}

  /* Go também nunca acessa gestão de usuários */
  body[data-smyle-access="go"] #settingsUsersTab,
  body[data-smyle-access="go"] #settingsUsersPane{display:none !important}
</style>
'''
if 'smyle-v40-access-profiles' not in html:
    head_pos = html.rfind('</head>')
    if head_pos < 0:
        raise RuntimeError('</head> não encontrado')
    html = html[:head_pos] + css + '\n' + html[head_pos:]

js = r'''
<script id="smyle-v40-access-profiles-js">
(function(){
  var ROLE_GO='Smyle Go ✦';
  var ROLE_CREATOR='Smyle Creator 🧪';
  var ROLE_CORE='Smyle Core ◉';

  function normalizeRole(role){
    var raw=String(role||'').trim();
    var low=raw.toLowerCase();
    if(low.indexOf('smyle core')>=0 || low==='administrador' || low==='admin') return ROLE_CORE;
    if(low.indexOf('smyle creator')>=0 || low==='editor') return ROLE_CREATOR;
    if(low.indexOf('smyle go')>=0 || low==='analista') return ROLE_GO;
    return ROLE_GO;
  }
  window.smyleNormalizeRole=normalizeRole;

  function roleKey(role){
    role=normalizeRole(role);
    if(role===ROLE_CORE) return 'core';
    if(role===ROLE_CREATOR) return 'creator';
    return 'go';
  }

  function getRoleDescription(role){
    role=normalizeRole(role);
    if(role===ROLE_CORE) return 'Acesso completo: conteúdos, jogos, relatórios, configurações e gestão de usuários.';
    if(role===ROLE_CREATOR) return 'Cria e gerencia conteúdos, configura os jogos e pode emitir, imprimir e exportar relatórios.';
    return 'Explora e testa os jogos, acessa a Visão Geral e consulta relatórios, sem permissões de edição.';
  }

  window.smyleUpdateRoleDescription=function(){
    var select=document.getElementById('uRole');
    var hint=document.getElementById('uRoleDescription');
    if(!select || !hint) return;
    hint.textContent=getRoleDescription(select.value);
  };

  function ensureRoleOptions(){
    var select=document.getElementById('uRole');
    if(!select) return;
    var current=normalizeRole(select.value);
    select.innerHTML=''
      +'<option value="'+ROLE_GO+'">'+ROLE_GO+'</option>'
      +'<option value="'+ROLE_CREATOR+'">'+ROLE_CREATOR+'</option>'
      +'<option value="'+ROLE_CORE+'">'+ROLE_CORE+'</option>';
    select.value=current;
    window.smyleUpdateRoleDescription();
  }

  function migrateRoles(){
    try{
      if(typeof getUsers!=='function' || typeof saveUsers!=='function') return;
      var users=getUsers();
      if(!Array.isArray(users)) return;
      var changed=false;
      var migrated=users.map(function(u){
        var next=normalizeRole(u.role);
        if(next!==u.role) changed=true;
        return Object.assign({},u,{role:next});
      });
      if(changed) saveUsers(migrated);
    }catch(err){ console.warn('Migração de perfis Smyle:',err); }
  }

  function currentUser(){
    try{
      if(typeof getCurrentAdminUser==='function') return getCurrentAdminUser();
    }catch(e){}
    return null;
  }

  window.smyleApplyAccessPermissions=function(){
    var user=currentUser();
    var key=roleKey(user && user.role ? user.role : ROLE_CORE);
    document.body.setAttribute('data-smyle-access',key);

    var usersTab=document.getElementById('settingsUsersTab');
    var usersPane=document.getElementById('settingsUsersPane');
    if(usersTab) usersTab.style.display=(key==='core'?'':'none');
    if(usersPane && key!=='core') usersPane.classList.remove('active');

    var settingsLink=document.querySelector('.side-link[data-page="settings"]');
    if(settingsLink) settingsLink.style.display=(key==='go'?'none':'');

    var reportActions=document.querySelector('.report-head-actions');
    if(reportActions) reportActions.style.display=(key==='go'?'none':'');

    var addBtn=document.getElementById('gameAdminAddBtn');
    if(addBtn) addBtn.style.display=(key==='go'?'none':'');

    document.querySelectorAll('.v22-content-actions').forEach(function(group){
      group.querySelectorAll('button').forEach(function(btn){
        var isTest=btn.classList.contains('game-test-btn') || (btn.textContent||'').trim().toLowerCase()==='testar';
        btn.style.display=(key==='go' && !isTest)?'none':'';
      });
    });

    var password=document.getElementById('settingPassword');
    if(password && password.closest('.form-group')){
      password.closest('.form-group').style.display=(key==='core'?'':'none');
    }

    if(key==='creator'){
      var usersActive=usersPane && usersPane.classList.contains('active');
      if(usersActive && typeof showSettingsTab==='function') showSettingsTab('general');
    }
  };

  /* Comprime a imagem para não estourar o limite do localStorage. */
  window.smyleHandleUserPhotoUpload=function(event){
    var input=event && event.target;
    var file=input && input.files && input.files[0];
    if(!file) return;
    if(!/^image\//i.test(file.type||'')){
      alert('Selecione um arquivo de imagem.');
      input.value='';
      return;
    }
    if(file.size>8*1024*1024){
      alert('Escolha uma imagem de até 8 MB.');
      input.value='';
      return;
    }
    var reader=new FileReader();
    reader.onload=function(e){
      var img=new Image();
      img.onload=function(){
        var max=512;
        var scale=Math.min(1,max/Math.max(img.width||1,img.height||1));
        var w=Math.max(1,Math.round(img.width*scale));
        var h=Math.max(1,Math.round(img.height*scale));
        var canvas=document.createElement('canvas');
        canvas.width=w; canvas.height=h;
        var ctx=canvas.getContext('2d');
        ctx.drawImage(img,0,0,w,h);
        var data=canvas.toDataURL('image/jpeg',0.82);
        window.smyleUserPhotoCache=data;
        try{ smyleUserPhotoCache=data; }catch(ignore){}
        var preview=document.getElementById('uPhotoPreview');
        if(preview){
          preview.textContent='';
          preview.style.backgroundImage="url('"+data+"')";
          preview.style.backgroundSize='cover';
          preview.style.backgroundPosition='center';
        }
      };
      img.src=e.target.result;
    };
    reader.readAsDataURL(file);
  };

  function readPhoto(current){
    var photo='';
    try{ if(typeof smyleUserPhotoCache!=='undefined' && smyleUserPhotoCache) photo=smyleUserPhotoCache; }catch(e){}
    if(!photo && window.smyleUserPhotoCache) photo=window.smyleUserPhotoCache;
    if(!photo && current && current.photo) photo=current.photo;
    return photo||'';
  }

  window.smyleSaveUserFromModal=function(event){
    if(event){
      event.preventDefault();
      if(event.stopImmediatePropagation) event.stopImmediatePropagation();
      if(event.stopPropagation) event.stopPropagation();
    }
    try{
      var idEl=document.getElementById('editingUserId');
      var nameEl=document.getElementById('uName');
      var usernameEl=document.getElementById('uUsername');
      var roleEl=document.getElementById('uRole');
      var statusEl=document.getElementById('uStatus');
      var passwordEl=document.getElementById('uPassword');
      if(!nameEl || !usernameEl || !roleEl || !statusEl || !passwordEl){
        alert('Não foi possível localizar os campos do cadastro.');
        return false;
      }

      var id=idEl?String(idEl.value||''):'';
      var name=String(nameEl.value||'').trim();
      var username=String(usernameEl.value||'').trim();
      var role=normalizeRole(roleEl.value);
      var active=String(statusEl.value||'active')==='active';
      var password=String(passwordEl.value||'');

      if(!name || !username){
        alert('Preencha o nome completo e o usuário.');
        return false;
      }

      var users=(typeof getUsers==='function')?getUsers():[];
      if(!Array.isArray(users)) users=[];
      var current=users.find(function(u){return String(u.id||'')===id;});
      if(!current && !password){
        alert('Defina uma senha para o novo usuário.');
        return false;
      }

      var duplicate=users.find(function(u){
        return String(u.username||'').trim().toLowerCase()===username.toLowerCase() && String(u.id||'')!==id;
      });
      if(duplicate){
        alert('Já existe um usuário com esse login.');
        return false;
      }

      var payload={
        id:id || ('user-'+Date.now()),
        name:name,
        username:username,
        role:role,
        active:active,
        password:password || (current && current.password) || '',
        photo:readPhoto(current)
      };
      var updated=current
        ? users.map(function(u){return String(u.id||'')===id?payload:u;})
        : [payload].concat(users);

      try{
        if(typeof saveUsers==='function') saveUsers(updated);
        else localStorage.setItem('smyle_lab_admin_users_v1',JSON.stringify(updated));
      }catch(storageError){
        console.error(storageError);
        alert('Não foi possível salvar. A imagem pode estar muito grande para o armazenamento do navegador. Tente outra foto.');
        return false;
      }

      try{
        var logged=currentUser();
        if(logged && String(logged.id||'')===String(payload.id||'') && typeof setCurrentAdminUser==='function') setCurrentAdminUser(payload);
      }catch(e){}

      try{ if(typeof renderUsersManagement==='function') renderUsersManagement(); }catch(e){}
      try{ if(typeof renderUsersTable==='function') renderUsersTable(); }catch(e){}
      try{ if(typeof refreshCurrentUserUI==='function') refreshCurrentUserUI(); }catch(e){}
      try{ if(typeof closeUserModal==='function') closeUserModal(); else document.getElementById('userModal').classList.add('hidden'); }catch(e){}

      window.smyleApplyAccessPermissions();
      if(typeof window.smyleShowUserSaved==='function') window.smyleShowUserSaved();
      else alert('Usuário salvo com sucesso.');
      return false;
    }catch(err){
      console.error('Erro ao salvar usuário:',err);
      alert('Não foi possível salvar o usuário. Verifique os dados e tente novamente.');
      return false;
    }
  };

  /* Proteção adicional: captura o clique antes do onclick legado. */
  document.addEventListener('click',function(e){
    var btn=e.target && e.target.closest ? e.target.closest('#userModal .user-modal-actions .primary-btn') : null;
    if(btn && /salvar usu[aá]rio/i.test(btn.textContent||'')){
      window.smyleSaveUserFromModal(e);
      return;
    }

    var user=currentUser();
    var key=roleKey(user && user.role ? user.role : ROLE_CORE);
    var target=e.target && e.target.closest ? e.target.closest('button') : null;
    if(!target) return;

    if(key==='go'){
      if(target.closest('.report-head-actions') || target.id==='gameAdminAddBtn' || (target.closest('.v22-content-actions') && !target.classList.contains('game-test-btn'))){
        e.preventDefault(); e.stopImmediatePropagation();
        alert('O Smyle Go possui acesso de consulta e teste, sem permissão para alterar ou emitir informações.');
      }
      if(target.matches('.side-link[data-page="settings"]')){
        e.preventDefault(); e.stopImmediatePropagation();
      }
    }
    if(key!=='core' && (target.id==='settingsUsersTab' || target.classList.contains('users-add-btn') || target.closest('#settingsUsersPane'))){
      e.preventDefault(); e.stopImmediatePropagation();
      alert('A gestão de usuários é exclusiva do Smyle Core.');
    }
  },true);

  function decorateRoleBadges(){
    document.querySelectorAll('.user-role-badge').forEach(function(badge){
      var role=normalizeRole(badge.textContent);
      badge.textContent=role;
      badge.setAttribute('data-smyle-role',roleKey(role));
    });
  }

  function init(){
    migrateRoles();
    ensureRoleOptions();
    window.smyleUpdateRoleDescription();
    window.smyleApplyAccessPermissions();
    decorateRoleBadges();

    var observer=new MutationObserver(function(){
      ensureRoleOptions();
      decorateRoleBadges();
      window.smyleApplyAccessPermissions();
    });
    var admin=document.getElementById('adminScreen');
    if(admin) observer.observe(admin,{subtree:true,childList:true,attributes:true,attributeFilter:['class']});

    document.addEventListener('change',function(e){
      if(e.target && e.target.id==='uRole') window.smyleUpdateRoleDescription();
    });

    /* Novo usuário começa em Smyle Go por segurança. */
    document.addEventListener('click',function(e){
      var btn=e.target && e.target.closest ? e.target.closest('.users-add-btn') : null;
      if(btn){
        setTimeout(function(){
          ensureRoleOptions();
          var role=document.getElementById('uRole');
          if(role) role.value=ROLE_GO;
          window.smyleUpdateRoleDescription();
        },0);
      }
    });
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
  else init();
})();
</script>
'''

if 'smyle-v40-access-profiles-js' not in html:
    body_pos=html.rfind('</body>')
    if body_pos < 0:
        raise RuntimeError('</body> principal não encontrado')
    html=html[:body_pos] + js + '\n' + html[body_pos:]

path.write_text(html,encoding='utf-8')
print('Patch V40 aplicado: cadastro de usuários + perfis Smyle Go/Creator/Core.')
