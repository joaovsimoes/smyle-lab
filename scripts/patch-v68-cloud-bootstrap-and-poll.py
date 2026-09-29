from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

marker = 'id="smyle-v68-cloud-bootstrap-and-poll"'
script = r'''
<script id="smyle-v68-cloud-bootstrap-and-poll">
(function(){
  'use strict';

  var DOC_URL='https://firestore.googleapis.com/v1/projects/smyle-lab/databases/(default)/documents/smyleShared/gameContent';
  var KEYS=['dojo_questions_v1','dojo_settings_v1','smyle_lab_game_catalog_v1','smyle_lab_native_content_v17'];
  var lastCloudStamp='';
  var bootstrapping=false;

  function adminIsActive(){
    try{ if(sessionStorage.getItem('dojo_admin_session_v1')==='1') return true; }catch(e){}
    try{ if(localStorage.getItem('smyle_lab_current_user_id')) return true; }catch(e){}
    try{
      var el=document.getElementById('adminScreen');
      if(el && !el.classList.contains('hidden')) return true;
    }catch(e){}
    return false;
  }

  function parseDoc(doc){
    try{
      var raw=doc?.fields?.contentJson?.stringValue;
      if(!raw) return null;
      return JSON.parse(raw);
    }catch(e){ return null; }
  }

  function applyCloudExact(data){
    if(!data || typeof data!=='object') return false;
    var changed=false;
    KEYS.forEach(function(k){
      if(!Object.prototype.hasOwnProperty.call(data,k)) return;
      var next=String(data[k]);
      if(localStorage.getItem(k)!==next){
        localStorage.setItem(k,next);
        changed=true;
      }
    });
    return changed;
  }

  async function publishLocalAdmin(){
    if(!adminIsActive()) return false;
    var payload={};
    KEYS.forEach(function(k){
      var v=localStorage.getItem(k);
      if(v!==null) payload[k]=v;
    });
    var response=await fetch(DOC_URL,{
      method:'PATCH',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        fields:{
          contentJson:{stringValue:JSON.stringify(payload)},
          version:{integerValue:'68'},
          updatedAt:{timestampValue:new Date().toISOString()}
        }
      })
    });
    if(!response.ok){
      var t=''; try{t=await response.text();}catch(e){}
      throw new Error('HTTP '+response.status+' '+t.slice(0,250));
    }
    console.info('Smyle Lab: base administrativa publicada como fonte oficial.');
    return true;
  }

  async function bootstrapAdminIfCloudEmpty(){
    if(bootstrapping || !adminIsActive()) return;
    bootstrapping=true;
    try{
      var response=await fetch(DOC_URL,{cache:'no-store'});
      if(response.status===404){
        await publishLocalAdmin();
      }
    }catch(e){
      console.error('Smyle Lab bootstrap:',e);
    }finally{
      bootstrapping=false;
    }
  }

  async function pollCloudForPlayers(){
    if(adminIsActive()) return;
    try{
      var response=await fetch(DOC_URL,{cache:'no-store'});
      if(!response.ok) return;
      var doc=await response.json();
      var stamp=doc?.fields?.updatedAt?.timestampValue || '';
      if(stamp && stamp===lastCloudStamp) return;
      var data=parseDoc(doc);
      if(!data) return;
      lastCloudStamp=stamp;
      if(applyCloudExact(data)){
        try{
          if(typeof renderSetupOptions==='function') renderSetupOptions();
          if(typeof populateGameSelects==='function') populateGameSelects();
        }catch(e){}
        console.info('Smyle Lab: conteúdo atualizado pela Administração.');
      }
    }catch(e){}
  }

  function installAdminHooks(){
    [
      'saveQuestion','saveGameItems','saveGameItem','saveGameItemV18',
      'toggleQuestion','deleteQuestion','toggleGameItem','deleteGameItem','saveSettings'
    ].forEach(function(name){
      var fn=window[name];
      if(typeof fn!=='function' || fn.__smyleV68Wrapped) return;
      var wrapped=function(){
        var result=fn.apply(this,arguments);
        setTimeout(function(){
          publishLocalAdmin().catch(function(err){
            console.error('Smyle Lab publish:',err);
          });
        },120);
        return result;
      };
      wrapped.__smyleV68Wrapped=true;
      window[name]=wrapped;
    });
  }

  window.smylePublishCurrentAdminBase=publishLocalAdmin;

  function tick(){
    installAdminHooks();
    if(adminIsActive()) bootstrapAdminIfCloudEmpty();
    else pollCloudForPlayers();
  }

  document.addEventListener('DOMContentLoaded',function(){
    installAdminHooks();
    setTimeout(tick,200);
    setTimeout(tick,1200);
  });
  window.addEventListener('load',tick);
  setInterval(tick,10000);
})();
</script>
'''

if marker not in html:
    pos=html.rfind('</body>')
    if pos<0: raise RuntimeError('Fechamento </body> principal não encontrado.')
    html=html[:pos]+script+'\n'+html[pos:]

path.write_text(html,encoding='utf-8')
print('V68 aplicada: Administração cria a base em nuvem quando vazia e jogadores recebem atualizações sem poder sobrescrever.')
