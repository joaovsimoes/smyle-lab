from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

# Ajusta o texto do botão de foto para ficar mais claro.
html = html.replace('>Escolher foto</label>', '>Adicionar foto</label>')

css = r'''

/* ==== Smyle Lab V39: gestão de usuários ==== */
#userModal .photo-upload-btn{
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  width:140px !important;
  min-height:44px !important;
  padding:10px 14px !important;
  border-radius:13px !important;
  background:#0C2340 !important;
  color:#FFFFFF !important;
  border:1px solid #0C2340 !important;
  font-size:12px !important;
  font-weight:800 !important;
  line-height:1 !important;
  cursor:pointer !important;
  white-space:nowrap !important;
}
#userModal .photo-upload-btn:hover{
  background:#12365F !important;
  border-color:#12365F !important;
}
#userModal .photo-remove-btn{
  width:140px !important;
  min-height:42px !important;
  color:#5F7288 !important;
}
#userModal .user-photo-preview{
  width:140px !important;
  height:140px !important;
  border-radius:24px !important;
}

#smyleUserSavedDialog{
  position:fixed !important;
  inset:0 !important;
  z-index:100000 !important;
  display:none;
  align-items:center !important;
  justify-content:center !important;
  padding:20px !important;
  background:rgba(8,26,46,.42) !important;
  backdrop-filter:blur(8px) !important;
  -webkit-backdrop-filter:blur(8px) !important;
}
#smyleUserSavedDialog.open{display:flex !important}
#smyleUserSavedDialog .smyle-user-success-card{
  width:min(420px,calc(100vw - 32px)) !important;
  padding:30px 28px 26px !important;
  border-radius:24px !important;
  background:#fff !important;
  border:1px solid rgba(12,35,64,.08) !important;
  box-shadow:0 28px 80px rgba(8,26,46,.22) !important;
  text-align:center !important;
}
#smyleUserSavedDialog .smyle-user-success-mark{
  width:58px !important;
  height:58px !important;
  margin:0 auto 16px !important;
  border-radius:18px !important;
  display:grid !important;
  place-items:center !important;
  background:linear-gradient(135deg,#63D9CF,#8FE7DD) !important;
  color:#081A2E !important;
  font-size:30px !important;
  font-weight:900 !important;
}
#smyleUserSavedDialog h3{
  margin:0 0 8px !important;
  color:#0C2340 !important;
  font-size:22px !important;
}
#smyleUserSavedDialog p{
  margin:0 0 20px !important;
  color:#5F7288 !important;
  font-size:14px !important;
  line-height:1.5 !important;
}
#smyleUserSavedDialog button{
  width:100% !important;
  min-height:46px !important;
  border:0 !important;
  border-radius:13px !important;
  background:#0C2340 !important;
  color:#fff !important;
  font-weight:800 !important;
  cursor:pointer !important;
}
'''

if '/* ==== Smyle Lab V39: gestão de usuários ==== */' not in html:
    html = html.replace('</style>', css + '\n</style>', 1)

js = r'''
<script>
(function(){
  function ensureUserSavedDialog(){
    var existing=document.getElementById('smyleUserSavedDialog');
    if(existing) return existing;
    var overlay=document.createElement('div');
    overlay.id='smyleUserSavedDialog';
    overlay.setAttribute('role','dialog');
    overlay.setAttribute('aria-modal','true');
    overlay.innerHTML=''
      +'<div class="smyle-user-success-card">'
      +  '<div class="smyle-user-success-mark">✓</div>'
      +  '<h3>Usuário salvo com sucesso</h3>'
      +  '<p>O acesso já está disponível na gestão de usuários do Smyle Lab.</p>'
      +  '<button type="button" id="smyleUserSavedContinue">Continuar</button>'
      +'</div>';
    document.body.appendChild(overlay);
    function close(){ overlay.classList.remove('open'); }
    overlay.addEventListener('click',function(e){ if(e.target===overlay) close(); });
    overlay.querySelector('#smyleUserSavedContinue').addEventListener('click',close);
    return overlay;
  }

  window.smyleShowUserSaved=function(){
    var overlay=ensureUserSavedDialog();
    overlay.classList.add('open');
    setTimeout(function(){
      var btn=overlay.querySelector('#smyleUserSavedContinue');
      if(btn) btn.focus();
    },30);
  };

  /* Override final para evitar conflito entre versões antigas de saveUserItem. */
  window.saveUserItem=function(){
    try{
      var idEl=document.getElementById('editingUserId');
      var nameEl=document.getElementById('uName');
      var usernameEl=document.getElementById('uUsername');
      var roleEl=document.getElementById('uRole');
      var statusEl=document.getElementById('uStatus');
      var passwordEl=document.getElementById('uPassword');

      if(!nameEl || !usernameEl || !roleEl || !statusEl || !passwordEl){
        alert('Não foi possível localizar os campos do cadastro de usuário.');
        return;
      }

      var id=idEl ? String(idEl.value||'') : '';
      var name=String(nameEl.value||'').trim();
      var username=String(usernameEl.value||'').trim();
      var role=String(roleEl.value||'Administrador');
      var active=String(statusEl.value||'active')==='active';
      var password=String(passwordEl.value||'');

      if(!name || !username){
        alert('Preencha o nome completo e o usuário.');
        return;
      }

      var users=(typeof getUsers==='function' ? getUsers() : []);
      if(!Array.isArray(users)) users=[];
      var current=users.find(function(u){ return String(u.id||'')===id; });

      if(!current && !password){
        alert('Defina uma senha para o novo usuário.');
        return;
      }

      var duplicate=users.find(function(u){
        return String(u.username||'').trim().toLowerCase()===username.toLowerCase() && String(u.id||'')!==id;
      });
      if(duplicate){
        alert('Já existe um usuário com esse login.');
        return;
      }

      var photo=(typeof smyleUserPhotoCache!=='undefined' && smyleUserPhotoCache)
        ? smyleUserPhotoCache
        : (current && current.photo ? current.photo : '');

      var payload={
        id:id || ('user-'+Date.now()),
        name:name,
        username:username,
        role:role,
        active:active,
        password:password || (current && current.password ? current.password : ''),
        photo:photo
      };

      var updated=current
        ? users.map(function(u){ return String(u.id||'')===id ? payload : u; })
        : [payload].concat(users);

      if(typeof saveUsers==='function'){
        saveUsers(updated);
      }else{
        localStorage.setItem('smyle_lab_admin_users_v1',JSON.stringify(updated));
      }

      var logged=null;
      try{ logged=(typeof getCurrentAdminUser==='function' ? getCurrentAdminUser() : null); }catch(e){}
      if(logged && String(logged.id||'')===String(payload.id||'') && typeof setCurrentAdminUser==='function'){
        setCurrentAdminUser(payload);
      }

      try{ if(typeof renderUsersManagement==='function') renderUsersManagement(); }catch(e){}
      try{ if(typeof renderUsersTable==='function') renderUsersTable(); }catch(e){}
      try{ if(typeof refreshCurrentUserUI==='function') refreshCurrentUserUI(); }catch(e){}
      try{ if(typeof closeUserModal==='function') closeUserModal(); }catch(e){
        var modal=document.getElementById('userModal');
        if(modal) modal.classList.add('hidden');
      }

      window.smyleShowUserSaved();
    }catch(err){
      console.error('Erro ao salvar usuário no Smyle Lab:',err);
      alert('Não foi possível salvar o usuário. Atualize a página e tente novamente.');
    }
  };

  document.addEventListener('DOMContentLoaded',function(){
    ensureUserSavedDialog();
    var upload=document.querySelector('#userModal .photo-upload-btn');
    if(upload) upload.textContent='Adicionar foto';
  });
})();
</script>
'''

if 'smyleShowUserSaved' not in html:
    body_pos=html.rfind('</body>')
    if body_pos < 0:
        raise RuntimeError('Fechamento </body> principal não encontrado.')
    html=html[:body_pos] + js + '\n' + html[body_pos:]

path.write_text(html,encoding='utf-8')
print('Patch V39 aplicado: salvamento de usuários e botão de foto corrigidos.')
