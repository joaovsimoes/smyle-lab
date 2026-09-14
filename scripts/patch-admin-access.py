from pathlib import Path

path = Path("public/index.html")
text = path.read_text(encoding="utf-8")

# Remove a informação de primeiro acesso e deixa o campo de usuário neutro.
text = text.replace(
    '<input id="adminUser" value="admin" autocomplete="username" />',
    '<input id="adminUser" placeholder="Digite seu usuário" autocomplete="username" />',
    1,
)
text = text.replace(
    '''        <div class="smyle-login-help">\n          <strong>Primeiro acesso</strong>\n          <span>Usuário <b>admin</b> • Senha <b>dojo2026</b></span>\n        </div>\n''',
    '',
    1,
)

# O bloco abaixo é inserido no final do script principal. Por ser a última definição,
# passa a ser a regra oficial para usuários, login e alteração do administrador.
override = r'''

// ==== Smyle Lab admin access fix v28 ====
function getUsers(){
  let list=[];
  try{ list=JSON.parse(localStorage.getItem(SMYLE_USERS_STORAGE_KEY)||'[]'); }catch(e){ list=[]; }
  if(!Array.isArray(list)) list=[];

  const settings=getSettings();
  const existingAdminIndex=list.findIndex(u => u?.id==='admin-default' || String(u?.username||'').toLowerCase()==='admin');
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
      name:old.name || seedAdmin.name,
      username:String(old.username || seedAdmin.username).trim(),
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
    if(!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  saveUsers(list);
  return list;
}

function adminLogin(){
  const userField=document.getElementById('adminUser');
  const passField=document.getElementById('adminPassword');
  if(!userField || !passField){
    alert('Não foi possível localizar os campos de acesso.');
    return;
  }

  const username=userField.value.trim().toLowerCase();
  const password=passField.value;
  if(!username || !password){
    alert('Informe seu usuário e senha.');
    return;
  }

  let found=null;
  try{
    const users=getUsers();
    found=users.find(u =>
      String(u.username||'').trim().toLowerCase()===username &&
      String(u.password||'')===password &&
      u.active!==false
    ) || null;
  }catch(e){ console.warn('Falha ao validar usuário:',e); }

  if(!found){
    alert('Usuário ou senha incorretos.');
    return;
  }

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
  const duplicated=users.find(u=>u.username.toLowerCase()===username.toLowerCase() && u.id!==id);
  if(duplicated){ alert('Já existe um usuário com esse login.'); return; }

  const payload={
    id:id || ('user-'+Date.now()),
    name,username,role,active,
    password:password || current?.password || '123456',
    photo:smyleUserPhotoCache || current?.photo || ''
  };
  const updated=current ? users.map(u=>u.id===id?payload:u) : [payload,...users];
  saveUsers(updated);

  if(payload.id==='admin-default'){
    const s=getSettings();
    s.adminPassword=payload.password;
    setSettings(s);
  }

  const logged=getCurrentAdminUser();
  if(logged && logged.id===payload.id) setCurrentAdminUser(payload);
  refreshCurrentUserUI();
  renderUsersManagement();
  closeUserModal();
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
    const users=getUsers().map(u=>u.id==='admin-default' ? {...u,password:p} : u);
    saveUsers(users);
  }
  alert('Configurações salvas.');
  loadSettingsForm();
}
'''

marker = "</script>"
pos = text.rfind(marker)
if pos == -1:
    raise RuntimeError("Não foi possível localizar o script principal do Smyle Lab.")

# Evita duplicar o patch em execuções futuras.
if "Smyle Lab admin access fix v28" not in text:
    text = text[:pos] + override + "\n" + text[pos:]

path.write_text(text, encoding="utf-8")
print("Patch de acesso administrativo aplicado com sucesso.")
