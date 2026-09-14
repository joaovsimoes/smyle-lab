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

path.write_text(text, encoding="utf-8")
print("Correção v30 de inicialização aplicada com sucesso.")
