# Smyle Lab

Plataforma de experiências interativas e jogos de aprendizagem.

## Jogos
- Fato ou Fake
- Qual é a Jogada?
- Desembaralha!
- Conecta Lab

## Publicação
Este projeto está preparado para Firebase Hosting.

### Deploy manual
```bash
npm install -g firebase-tools
firebase login
firebase use <PROJECT_ID>
firebase deploy --only hosting
```

### GitHub + Firebase
Depois de vincular o repositório ao Firebase Hosting, os deploys podem ser automatizados pela integração oficial do Firebase com GitHub Actions.
