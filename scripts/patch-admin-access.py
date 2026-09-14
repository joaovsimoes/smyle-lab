from pathlib import Path

path = Path("public/index.html")
text = path.read_text(encoding="utf-8")

# ==== Simplifica a tela inicial ====
text = text.replace('<h2>Bem-vindo de volta</h2>', '<h2>Bem-vindo(a)</h2>', 1)
text = text.replace(
    '<p class="smyle-access-copy">Escolha como deseja acessar o sistema. Você pode iniciar uma rodada ou entrar no modo administrador para cadastrar jogos, editar perguntas e acompanhar resultados.</p>',
    '<p class="smyle-access-copy">Escolha como deseja entrar no sistema</p>',
    1,
)
text = text.replace(
'''              <button class="entry-btn play" onclick="showScreen('setupScreen')">
                <span class="entry-left">
                  <span class="entry-icon">🎮</span>
                  <span><strong>Jogar</strong><small>Acesse os jogos disponíveis e inicie uma rodada</small></span>
                </span>
                <span>→</span>
              </button>''',
'''              <button class="entry-btn play smyle-simple-entry" onclick="showScreen('setupScreen')"><strong>Jogar</strong></button>''',
    1,
)
text = text.replace(
'''              <button class="entry-btn admin" onclick="openAdminGate()">
                <span class="entry-left">
                  <span class="entry-icon">⚙️</span>
                  <span><strong>Administrador</strong><small>Cadastre jogos, gerencie conteúdos e veja relatórios</small></span>
                </span>
                <span>→</span>
              </button>''',
'''              <button class="entry-btn admin smyle-simple-entry" onclick="openAdminGate()"><strong>Administrador</strong></button>''',
    1,
)
text = text.replace(
'''            <div class="smyle-mini-games">
              <span class="smyle-mini-game">Fato ou Fake</span>
              <span class="smyle-mini-game">Quiz</span>
              <span class="smyle-mini-game">Desafios</span>
              <span class="smyle-mini-game">Novos jogos</span>
            </div>

''', '', 1)
text = text.replace(
    '<div class="smyle-access-note"><strong>Acesso do administrador:</strong> use o usuário e a senha cadastrados para acessar o painel do Smyle Lab.</div>',
    '<div class="smyle-access-note smyle-learning-note">Smyle Lab a sua forma de aprender através de jogos.</div>',
    1,
)
text = text.replace(
'''              <div>
                <strong>Smyle Lab</strong>
                <span>Plataforma de jogos e experiências</span>
              </div>
''', '', 1)

# Remove a informação de primeiro acesso e deixa o campo de usuário neutro.
text = text.replace(
    '<input id="adminUser" value="admin" autocomplete="username" />',
    '<input id="adminUser" placeholder="Digite seu usuário" autocomplete="username" />',
    1,
)
text = text.replace(
    '''        <div class="smyle-login-help">
          <strong>Primeiro acesso</strong>
          <span>Usuário <b>admin</b> • Senha <b>dojo2026</b></span>
        </div>
''',
    '',
    1,
)

ui_css = r'''
<style id="smyle-v29-ui-fix">
  .smyle-access-card .smyle-access-copy{max-width:100%;margin-bottom:20px}
  .smyle-access-actions{gap:14px}
  .entry-btn.smyle-simple-entry{min-height:72px;justify-content:center!important;text-align:center;padding:0 28px!important}
  .entry-btn.smyle-simple-entry strong{font-size:20px;line-height:1}
  .smyle-access-note.smyle-learning-note{text-align:center;font-weight:700;color:#4e6780;margin-top:18px}
  .smyle-access-brand{margin-bottom:18px}
</style>
'''
if 'smyle-v29-ui-fix' not in text:
    text = text.replace('</head>', ui_css + '\n</head>', 1)

# ==== Autenticação robusta ====
override = r'''

// ==== Smyle Lab robust auth fix v29 ====
const SMYLE_AUTH_STORAGE_KEY_V2 = 'smyle_lab_auth_users_v2';
const SMYLE_DISABLE_DEFAULT_RECOVERY_KEY = 'smyle_lab_disable_default_recovery_v2';

function smyleNormalizeUser(u, i){
  const username=String(u?.username||'').trim();
  return {
    id:String(u?.id || ('user-'+Date.now()+'-'+i)),
    name:String(u?.name || 'Usuário').trim() || 'Usuário',
    username,
    password:String(u?.password ?? ''),
    role:String(u?.role || 'Administrador'),
    active:u?.active !== false,
    photo:u?.photo || ''
  };
}

function smyleReadArray(key){
  try{
    const raw=localStorage.getItem(key);
    if(!raw) return [];
    const value=JSON.parse(raw);
    return Array.isArray(value) ? value : [];
  }catch(e){ return []; }
}

function smyleMergeUsers(){
  const legacyKey=(typeof SMYLE_USERS_STORAGE_KEY!=='undefined' ? SMYLE_USERS_STORAGE_KEY : 'smyle_lab_admin_users_v1');
  const sources=[...smyleReadArray(SMYLE_AUTH_STORAGE_KEY_V2),...smyleReadArray(legacyKey)];
  const users=[];
  sources.forEach((raw,i)=>{
    const u=smyleNormalizeUser(raw,i);
    if(!u.username) return;
    const duplicate=users.find(x=>x.id===u.id || x.username.toLowerCase()===u.username.toLowerCase());
    if(!duplicate) users.push(u);
  });
  if(!users.length){
    const settings=(typeof getSettings==='function' ? getSettings() : {}) || {};
    users.push({id:'admin-default',name:'João Vitor',username:'admin',password:String(settings.adminPassword||'dojo2026'),role:'Administrador',active:true,photo:''});
  }
  return users;
}

function smylePersistUsers(list){
  const normalized=(Array.isArray(list)?list:[]).map(smyleNormalizeUser).filter(u=>u.username);
  localStorage.setItem(SMYLE_AUTH_STORAGE_KEY_V2,JSON.stringify(normalized));
  try{
    const legacyKey=(typeof SMYLE_USERS_STORAGE_KEY!=='undefined' ? SMYLE_USERS_STORAGE_KEY : 'smyle_lab_admin_users_v1');
    localStorage.setItem(legacyKey,JSON.stringify(normalized));
  }catch(e){}
  return normalized;
}

function getUsers(){ return smylePersistUsers(smyleMergeUsers()); }
function saveUsers(list){ return smylePersistUsers(list); }

function smyleCompleteAdminLogin(found){
  sessionStorage.setItem(KEYS.adminSession,'1');
  sessionStorage.setItem('smyle_lab_current_user_id',found.id||'admin-default');
  if(typeof setCurrentAdminUser==='function') setCurrentAdminUser(found);
  document.body.style.overflow='';
  showScreen('adminScreen');
  if(typeof refreshCurrentUserUI==='function') refreshCurrentUserUI();
  if(typeof showAdminPage==='function'){
    const dash=document.querySelector('.side-link[data-page="dashboard"]');
    showAdminPage('dashboard',dash);
  }
  const passField=document.getElementById('adminPassword');
  if(passField) passField.value='';
}

function adminLogin(){
  const userField=document.getElementById('adminUser');
  const passField=document.getElementById('adminPassword');
  if(!userField || !passField){ alert('Não foi possível localizar os campos de acesso.'); return; }
  const username=String(userField.value||'').trim().toLowerCase();
  const password=String(passField.value||'');
  if(!username || !password){ alert('Informe seu usuário e senha.'); return; }

  const users=getUsers();
  let found=users.find(u=>u.active!==false && String(u.username||'').trim().toLowerCase()===username && String(u.password||'')===password) || null;

  if(!found && localStorage.getItem(SMYLE_DISABLE_DEFAULT_RECOVERY_KEY)!=='1' && username==='admin' && password==='dojo2026'){
    const currentAdmin=users.find(u=>u.id==='admin-default');
    const recovered={...(currentAdmin||{}),id:'admin-default',name:currentAdmin?.name||'João Vitor',username:'admin',password:'dojo2026',role:currentAdmin?.role||'Administrador',active:true,photo:currentAdmin?.photo||''};
    const updated=users.some(u=>u.id==='admin-default') ? users.map(u=>u.id==='admin-default'?recovered:u) : [recovered,...users];
    saveUsers(updated);
    found=recovered;
  }

  if(!found){ alert('Usuário ou senha incorretos.'); return; }
  smyleCompleteAdminLogin(found);
}

function saveUserItem(){
  const id=document.getElementById('editingUserId').value;
  const name=document.getElementById('uName').value.trim();
  const username=document.getElementById('uUsername').value.trim();
  const role=document.getElementById('uRole').value;
  const active=document.getElementById('uStatus').value==='active';
  const password=document.getElementById('uPassword').value;
  if(!name || !username){ alert('Preencha nome e usuário.'); return; }

  const users=getUsers();
  const current=users.find(u=>u.id===id);
  if(!current && !password){ alert('Defina uma senha para o novo usuário.'); return; }
  const duplicated=users.find(u=>String(u.username).toLowerCase()===username.toLowerCase() && u.id!==id);
  if(duplicated){ alert('Já existe um usuário com esse login.'); return; }

  const payload={id:id || ('user-'+Date.now()),name,username,role,active,password:password || current?.password || '123456',photo:smyleUserPhotoCache || current?.photo || ''};
  const updated=current ? users.map(u=>u.id===id?payload:u) : [payload,...users];
  saveUsers(updated);

  if(payload.id==='admin-default'){
    localStorage.setItem(SMYLE_DISABLE_DEFAULT_RECOVERY_KEY,'1');
    const s=getSettings();
    s.adminPassword=payload.password;
    setSettings(s);
  }

  const logged=typeof getCurrentAdminUser==='function' ? getCurrentAdminUser() : null;
  if(logged && logged.id===payload.id && typeof setCurrentAdminUser==='function') setCurrentAdminUser(payload);
  if(typeof refreshCurrentUserUI==='function') refreshCurrentUserUI();
  if(typeof renderUsersManagement==='function') renderUsersManagement();
  if(typeof closeUserModal==='function') closeUserModal();
}

function saveSettings(){
  const s=getSettings();
  s.title=document.getElementById('settingTitle').value.trim() || defaults.settings.title;
  s.timePerQuestion=Math.max(5,Number(document.getElementById('settingTime').value||20));
  s.pointsPerHit=Math.max(10,Number(document.getElementById('settingPoints').value||100));
  s.maxSpeedBonus=Math.max(0,Number(document.getElementById('settingSpeedBonus').value||25));
  const p=document.getElementById('settingPassword').value;
  if(p) s.adminPassword=p;
  setSettings(s);
  if(p){
    let users=getUsers();
    let idx=users.findIndex(u=>u.id==='admin-default');
    if(idx<0) idx=users.findIndex(u=>String(u.username).toLowerCase()==='admin');
    if(idx>=0) users[idx]={...users[idx],password:p};
    else users.unshift({id:'admin-default',name:'João Vitor',username:'admin',password:p,role:'Administrador',active:true,photo:''});
    saveUsers(users);
    localStorage.setItem(SMYLE_DISABLE_DEFAULT_RECOVERY_KEY,'1');
  }
  alert('Configurações salvas.');
  loadSettingsForm();
}

(function smyleBindAdminLoginV29(){
  const bind=()=>{
    const btn=document.querySelector('#adminLoginScreen button[onclick*="adminLogin"]');
    if(btn){btn.removeAttribute('onclick');btn.onclick=(ev)=>{ev.preventDefault();adminLogin();};}
    const pass=document.getElementById('adminPassword');
    if(pass && !pass.dataset.smyleEnterBound){
      pass.dataset.smyleEnterBound='1';
      pass.addEventListener('keydown',ev=>{if(ev.key==='Enter'){ev.preventDefault();adminLogin();}});
    }
  };
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',bind,{once:true}); else bind();
})();
'''

marker='</script>'
pos=text.rfind(marker)
if pos == -1:
    raise RuntimeError('Não foi possível localizar o script principal do Smyle Lab.')
if 'Smyle Lab robust auth fix v29' not in text:
    text=text[:pos]+override+'\n'+text[pos:]

path.write_text(text,encoding='utf-8')
print('Patch v29 aplicado com sucesso.')
