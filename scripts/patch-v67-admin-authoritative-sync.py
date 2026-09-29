from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

marker = 'id="smyle-v67-admin-authoritative-sync"'
script = r'''
<script id="smyle-v67-admin-authoritative-sync">
(function(){
  'use strict';

  var CLOUD_DOC = 'https://firestore.googleapis.com/v1/projects/smyle-lab/databases/(default)/documents/smyleShared/gameContent';
  var originalFetch = window.fetch.bind(window);

  function isCloudContentUrl(input){
    try{
      var u = typeof input === 'string' ? input : (input && input.url) || '';
      return String(u).indexOf('/documents/smyleShared/gameContent') >= 0;
    }catch(e){return false;}
  }

  function methodOf(input, init){
    try{
      return String((init && init.method) || (input && input.method) || 'GET').toUpperCase();
    }catch(e){return 'GET';}
  }

  function adminIsActive(){
    try{
      if(sessionStorage.getItem('dojo_admin_session_v1') === '1') return true;
    }catch(e){}
    try{
      if(localStorage.getItem('smyle_lab_current_user_id')) return true;
    }catch(e){}
    try{
      var admin = document.getElementById('adminScreen');
      if(admin && !admin.classList.contains('hidden')) return true;
    }catch(e){}
    return false;
  }

  // Jogadores podem ler da nuvem, mas nunca sobrescrever o conteúdo.
  window.fetch = function(input, init){
    if(isCloudContentUrl(input) && methodOf(input,init) === 'PATCH' && !adminIsActive()){
      console.info('Smyle Lab: envio de conteúdo ignorado fora da Administração.');
      return Promise.resolve(new Response('{}',{
        status:200,
        headers:{'Content-Type':'application/json'}
      }));
    }
    return originalFetch(input,init);
  };

  async function publishAdminContentNow(){
    if(!adminIsActive()) return false;

    var keys=[
      'dojo_questions_v1',
      'dojo_settings_v1',
      'smyle_lab_game_catalog_v1',
      'smyle_lab_native_content_v17'
    ];
    var data={};
    keys.forEach(function(k){
      var v=localStorage.getItem(k);
      if(v!==null) data[k]=v;
    });

    var body={
      fields:{
        contentJson:{stringValue:JSON.stringify(data)},
        version:{integerValue:'67'},
        updatedAt:{timestampValue:new Date().toISOString()}
      }
    };

    var response=await originalFetch(CLOUD_DOC,{
      method:'PATCH',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(body)
    });
    if(!response.ok){
      var t='';
      try{t=await response.text();}catch(e){}
      throw new Error('Falha ao publicar conteúdo: HTTP '+response.status+' '+t.slice(0,200));
    }
    console.info('Smyle Lab: conteúdo administrativo publicado na nuvem.');
    return true;
  }

  window.smylePublishAdminContentNow = publishAdminContentNow;

  function wrapAdminSave(name){
    var fn=window[name];
    if(typeof fn!=='function' || fn.__smyleV67Wrapped) return;
    var wrapped=function(){
      var result=fn.apply(this,arguments);
      setTimeout(function(){
        publishAdminContentNow().catch(function(err){
          console.error('Smyle Lab cloud publish:',err);
        });
      },80);
      return result;
    };
    wrapped.__smyleV67Wrapped=true;
    window[name]=wrapped;
  }

  function install(){
    [
      'saveQuestion',
      'saveGameItems',
      'saveGameItem',
      'saveGameItemV18',
      'toggleQuestion',
      'deleteQuestion',
      'toggleGameItem',
      'deleteGameItem',
      'saveSettings'
    ].forEach(wrapAdminSave);
  }

  install();
  document.addEventListener('DOMContentLoaded',function(){
    install();
    setTimeout(install,100);
    setTimeout(install,500);
  });
  window.addEventListener('load',install);
})();
</script>
'''

if marker not in html:
    pos = html.rfind('</body>')
    if pos < 0:
        raise RuntimeError('Fechamento </body> principal não encontrado.')
    html = html[:pos] + script + '\n' + html[pos:]

path.write_text(html, encoding='utf-8')
print('V67 aplicada: somente a Administração publica conteúdo; jogadores ficam somente-leitura na nuvem.')
