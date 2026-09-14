from pathlib import Path

path = Path("public/index.html")
text = path.read_text(encoding="utf-8")

# ==========================================================
# Smyle Lab v32
# Ajustes visuais + autenticação segura SEM redefinir funções
# de forma hoisted no final do arquivo.
# ==========================================================

# ----- Tela inicial mais limpa -----
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

# ----- Login sem credencial exposta -----
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
''', '', 1)

ui_css = r'''
<style id="smyle-v32-ui-fix">
  .smyle-access-card .smyle-access-copy{max-width:100%;margin-bottom:20px}
  .smyle-access-actions{gap:14px}
  .entry-btn.smyle-simple-entry{min-height:72px;justify-content:center!important;text-align:center;padding:0 28px!important}
  .entry-btn.smyle-simple-entry strong{font-size:20px;line-height:1}
  .smyle-access-note.smyle-learning-note{text-align:center;font-weight:700;color:#4e6780;margin-top:18px}
  .smyle-access-brand{margin-bottom:18px}
</style>
'''
if 'smyle-v32-ui-fix' not in text:
    text = text.replace('</head>', ui_css + '\n</head>', 1)

# ----- Corrige APENAS a última getUsers() (v15) -----
# O código antigo forçava o login do administrador de volta para "admin"
# a cada carregamento. Agora preservamos o usuário que foi salvo.
old_get_users = r'''function getUsers(){
  let list=[];
  try{ list=JSON.parse(localStorage.getItem(SMYLE_USERS_STORAGE_KEY)||'[]'); }catch(e){ list=[]; }
  if(!Array.isArray(list)) list=[];

  const settings=getSettings();
  const existingAdminIndex=list.findIndex(u => String(u?.username||'').toLowerCase()==='admin' || u?.id==='admin-default');
  const seedAdmin={
    id:'admin-default',
    name:'João Vitor',
    username:'admin',
    password:settings.adminPassword || 'dojo2026',
    role:'Administrador',
    active:true,
    photo:''
  };

  if(existingAdminIndex<0){
    list.unshift(seedAdmin);
  }else{
    const old=list[existingAdminIndex] || {};
    const normalizedAdmin={
      ...seedAdmin,
      ...old,
      id:old.id || 'admin-default',
      username:'admin',
      role:old.role || 'Administrador',
      active:old.active !== false,
      password:old.password || settings.adminPassword || 'dojo2026',
      photo:old.photo || ''
    };
    list.splice(existingAdminIndex,1);
    list.unshift(normalizedAdmin);
  }

  const seen=new Set();
  list=list.filter(Boolean).map((u,i)=>({
    id:u.id || ('user-'+Date.now()+'-'+i),
    name:u.name || (String(u.username||'').toLowerCase()==='admin' ? 'João Vitor' : 'Usuário'),
    username:u.username || ('usuario'+(i+1)),
    password:u.password || '123456',
    role:u.role || 'Administrador',
    active:u.active !== false,
    photo:u.photo || ''
  })).filter(u=>{
    const key=String(u.username).toLowerCase();
    if(seen.has(key)) return false;
    seen.add(key); return true;
  });

  saveUsers(list);
  return list;
}'''

new_get_users = r'''function getUsers(){
  let list=[];
  try{ list=JSON.parse(localStorage.getItem(SMYLE_USERS_STORAGE_KEY)||'[]'); }catch(e){ list=[]; }
  if(!Array.isArray(list)) list=[];

  const settings=getSettings();
  let existingAdminIndex=list.findIndex(u => u?.id==='admin-default');
  if(existingAdminIndex<0){
    existingAdminIndex=list.findIndex(u => String(u?.username||'').toLowerCase()==='admin');
  }

  const seedAdmin={
    id:'admin-default',
    name:'João Vitor',
    username:'admin',
    password:settings.adminPassword || 'dojo2026',
    role:'Administrador',
    active:true,
    photo:''
  };

  if(existingAdminIndex<0){
    list.unshift(seedAdmin);
  }else{
    const old=list[existingAdminIndex] || {};
    const normalizedAdmin={
      ...seedAdmin,
      ...old,
      id:'admin-default',
      name:old.name || 'João Vitor',
      username:String(old.username || 'admin').trim() || 'admin',
      role:old.role || 'Administrador',
      active:old.active !== false,
      password:String(old.password || settings.adminPassword || 'dojo2026'),
      photo:old.photo || ''
    };
    list.splice(existingAdminIndex,1);
    list.unshift(normalizedAdmin);
  }

  const seen=new Set();
  list=list.filter(Boolean).map((u,i)=>({
    id:u.id || ('user-'+Date.now()+'-'+i),
    name:u.name || 'Usuário',
    username:String(u.username || ('usuario'+(i+1))).trim(),
    password:String(u.password || '123456'),
    role:u.role || 'Administrador',
    active:u.active !== false,
    photo:u.photo || ''
  })).filter(u=>{
    const key=String(u.username).toLowerCase();
    if(seen.has(key)) return false;
    seen.add(key); return true;
  });

  saveUsers(list);
  return list;
}'''

if old_get_users not in text:
    raise RuntimeError('Bloco getUsers v15 não encontrado. Deploy interrompido para evitar regressão.')
text = text.replace(old_get_users, new_get_users, 1)

# ----- Login final: usa exclusivamente os usuários realmente cadastrados -----
# Inserido como atribuição no FINAL do script. Isso evita hoisting e não interfere
# na inicialização dos jogos.
safe_overrides = r'''

// ==== Smyle Lab v32 safe runtime overrides ====
adminLogin = function(){
  const userField=document.getElementById('adminUser');
  const passField=document.getElementById('adminPassword');
  if(!userField || !passField){ alert('Não foi possível localizar os campos de acesso.'); return; }

  const username=String(userField.value||'').trim().toLowerCase();
  const password=String(passField.value||'');
  if(!username || !password){ alert('Informe seu usuário e senha.'); return; }

  const users=getUsers();
  const found=users.find(u =>
    u.active!==false &&
    String(u.username||'').trim().toLowerCase()===username &&
    String(u.password||'')===password
  );

  if(!found){ alert('Usuário ou senha incorretos.'); return; }

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
  passField.value='';
};

saveSettings = function(){
  const s=getSettings();
  s.title=document.getElementById('settingTitle').value.trim() || defaults.settings.title;
  s.timePerQuestion=Math.max(5,Number(document.getElementById('settingTime').value||20));
  s.pointsPerHit=Math.max(10,Number(document.getElementById('settingPoints').value||100));
  s.maxSpeedBonus=Math.max(0,Number(document.getElementById('settingSpeedBonus').value||25));
  const p=document.getElementById('settingPassword').value;
  if(p) s.adminPassword=p;
  setSettings(s);

  if(p){
    const users=getUsers();
    let idx=users.findIndex(u=>u.id==='admin-default');
    if(idx<0) idx=users.findIndex(u=>String(u.username||'').toLowerCase()==='admin');
    if(idx>=0){
      users[idx]={...users[idx],password:p};
      saveUsers(users);
    }
  }

  alert('Configurações salvas.');
  loadSettingsForm();
};
'''

marker='</script>'
pos=text.rfind(marker)
if pos<0:
    raise RuntimeError('Script principal não encontrado.')
if 'Smyle Lab v32 safe runtime overrides' not in text:
    text=text[:pos]+safe_overrides+'\n'+text[pos:]

path.write_text(text, encoding='utf-8')
print('Patch v32 aplicado com sucesso.')
