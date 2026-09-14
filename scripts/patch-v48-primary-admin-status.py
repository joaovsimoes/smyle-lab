from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

js = r'''
<script id="smyle-v48-primary-admin-status">
(function(){
  function repairPrimaryAdminStatus(){
    try{
      if(typeof getUsers!=='function' || typeof saveUsers!=='function') return;
      var users=getUsers();
      if(!Array.isArray(users) || !users.length) return;

      var changed=false;
      users=users.map(function(u){
        if(String(u && u.id || '')==='admin-default' && u.active===false){
          changed=true;
          return Object.assign({},u,{active:true});
        }
        return u;
      });

      if(changed) saveUsers(users);
    }catch(e){
      console.warn('Não foi possível reparar o status do administrador principal.',e);
    }
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',repairPrimaryAdminStatus);
  else repairPrimaryAdminStatus();
})();
</script>
'''

if 'smyle-v48-primary-admin-status' not in html:
    pos=html.rfind('</body>')
    if pos<0: raise RuntimeError('</body> não encontrado')
    html=html[:pos]+js+'\n'+html[pos:]

path.write_text(html,encoding='utf-8')
print('Patch V48 aplicado: status do administrador principal reparado sem alterar usuário ou senha.')
