from pathlib import Path

path = Path("public/index.html")
text = path.read_text(encoding="utf-8")

# Corrige o patch v29: as constantes abaixo eram declaradas depois de uma
# chamada antiga de getUsers(). Como a nova função getUsers era hoisted,
# o navegador parava a execução do JavaScript antes de carregar os jogos.
text = text.replace(
    "const SMYLE_AUTH_STORAGE_KEY_V2 = 'smyle_lab_auth_users_v2';",
    "var SMYLE_AUTH_STORAGE_KEY_V2 = 'smyle_lab_auth_users_v2';",
    1,
)
text = text.replace(
    "const SMYLE_DISABLE_DEFAULT_RECOVERY_KEY = 'smyle_lab_disable_default_recovery_v2';",
    "var SMYLE_DISABLE_DEFAULT_RECOVERY_KEY = 'smyle_lab_disable_default_recovery_v2';",
    1,
)

# Mesmo antes da atribuição final, usa chaves válidas e nunca a chave 'undefined'.
text = text.replace(
    "...smyleReadArray(SMYLE_AUTH_STORAGE_KEY_V2),...smyleReadArray(legacyKey)",
    "...smyleReadArray(SMYLE_AUTH_STORAGE_KEY_V2 || 'smyle_lab_auth_users_v2'),...smyleReadArray(legacyKey)",
    1,
)
text = text.replace(
    "localStorage.setItem(SMYLE_AUTH_STORAGE_KEY_V2,JSON.stringify(normalized));",
    "localStorage.setItem(SMYLE_AUTH_STORAGE_KEY_V2 || 'smyle_lab_auth_users_v2',JSON.stringify(normalized));",
    1,
)

# ==== V31: código do jogador em sequência ====
old = '''function generateSmylePlayerCodeV19(){
  const used = new Set();
  try{
    (getGames()||[]).forEach(g=>{ if(/^SMY\\.\\d{4}$/.test(g.player||'')) used.add(g.player); });
  }catch(e){}
  let code='SMY.0001';
  for(let i=0;i<12000;i++){
    const n=Math.floor(Math.random()*10000);
    const candidate='SMY.'+String(n).padStart(4,'0');
    if(!used.has(candidate)){ code=candidate; break; }
  }
  sessionStorage.setItem(SMYLE_PLAYER_CODE_SESSION_KEY_V19,code);
  return code;
}'''

new = '''const SMYLE_PLAYER_CODE_COUNTER_KEY_V31 = 'smyle_player_code_counter_v31';
function generateSmylePlayerCodeV19(){
  let current = Number(localStorage.getItem(SMYLE_PLAYER_CODE_COUNTER_KEY_V31) || '0');
  if(!Number.isFinite(current) || current < 0) current = 0;
  const next = current >= 9999 ? 1 : current + 1;
  localStorage.setItem(SMYLE_PLAYER_CODE_COUNTER_KEY_V31, String(next));
  const code = 'SMY.' + String(next).padStart(4,'0');
  sessionStorage.setItem(SMYLE_PLAYER_CODE_SESSION_KEY_V19, code);
  return code;
}'''

if old not in text:
    raise RuntimeError('Função de geração do código SMY não encontrada.')
text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("Correções v30/v31 aplicadas com sucesso.")
