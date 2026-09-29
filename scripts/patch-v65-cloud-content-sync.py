from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

marker = 'id="smyle-v65-cloud-content-sync"'
script = r'''
<script id="smyle-v65-cloud-content-sync">
(function(){
  'use strict';

  var VERSION = 65;
  var PROJECT_ID = 'smyle-lab';
  var DOC_URL = 'https://firestore.googleapis.com/v1/projects/' + PROJECT_ID + '/databases/(default)/documents/smyleShared/gameContent';
  var SYNC_KEYS = [
    'dojo_questions_v1',
    'dojo_settings_v1',
    'smyle_lab_game_catalog_v1',
    'smyle_lab_native_content_v17'
  ];
  var applyingCloud = false;
  var initialCloudCheckDone = false;
  var pushTimer = null;
  var originalSetItem = Storage.prototype.setItem;

  function isLocalStorage(storage){
    try{return storage === window.localStorage;}catch(e){return false;}
  }

  function getLocalPayload(){
    var data = {};
    SYNC_KEYS.forEach(function(key){
      var value = localStorage.getItem(key);
      if(value !== null) data[key] = value;
    });
    return data;
  }

  function parseCloud(doc){
    try{
      var raw = doc && doc.fields && doc.fields.contentJson && doc.fields.contentJson.stringValue;
      if(!raw) return null;
      var parsed = JSON.parse(raw);
      return parsed && typeof parsed === 'object' ? parsed : null;
    }catch(e){
      console.warn('Smyle Lab cloud sync: conteúdo remoto inválido.', e);
      return null;
    }
  }

  function changedAgainstLocal(payload){
    return SYNC_KEYS.some(function(key){
      if(!Object.prototype.hasOwnProperty.call(payload,key)) return false;
      return localStorage.getItem(key) !== String(payload[key]);
    });
  }

  function applyCloud(payload){
    if(!payload || typeof payload !== 'object') return false;
    var changed = changedAgainstLocal(payload);
    if(!changed) return false;

    applyingCloud = true;
    try{
      SYNC_KEYS.forEach(function(key){
        if(Object.prototype.hasOwnProperty.call(payload,key) && payload[key] != null){
          originalSetItem.call(localStorage,key,String(payload[key]));
        }
      });
    }finally{
      applyingCloud = false;
    }
    return true;
  }

  async function loadCloud(){
    try{
      var response = await fetch(DOC_URL, {cache:'no-store'});
      initialCloudCheckDone = true;

      if(response.status === 404){
        console.info('Smyle Lab cloud sync: aguardando primeira publicação do administrador.');
        return;
      }
      if(!response.ok) throw new Error('HTTP '+response.status);

      var doc = await response.json();
      var payload = parseCloud(doc);
      if(!payload) return;

      if(applyCloud(payload)){
        var stamp = (doc.fields && doc.fields.updatedAt && doc.fields.updatedAt.timestampValue) || 'v'+VERSION;
        var reloadKey = 'smyle_cloud_applied_' + stamp;
        if(sessionStorage.getItem(reloadKey) !== '1'){
          sessionStorage.setItem(reloadKey,'1');
          location.reload();
        }
      }
    }catch(err){
      initialCloudCheckDone = true;
      console.warn('Smyle Lab cloud sync: não foi possível carregar o conteúdo compartilhado.', err);
    }
  }

  async function pushCloud(){
    if(applyingCloud) return;
    var payload = getLocalPayload();
    if(!Object.keys(payload).length) return;

    var body = {
      fields: {
        contentJson: {stringValue: JSON.stringify(payload)},
        version: {integerValue: String(VERSION)},
        updatedAt: {timestampValue: new Date().toISOString()}
      }
    };

    try{
      var response = await fetch(DOC_URL, {
        method:'PATCH',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(body)
      });
      if(!response.ok){
        var detail='';
        try{detail=await response.text();}catch(e){}
        throw new Error('HTTP '+response.status+' '+detail.slice(0,300));
      }
      window.dispatchEvent(new CustomEvent('smyle:cloud-content-saved'));
      console.info('Smyle Lab cloud sync: conteúdo publicado para todos os jogadores.');
    }catch(err){
      console.error('Smyle Lab cloud sync: falha ao publicar conteúdo.', err);
    }
  }

  function schedulePush(){
    clearTimeout(pushTimer);
    pushTimer = setTimeout(pushCloud, 700);
  }

  Storage.prototype.setItem = function(key,value){
    var result = originalSetItem.call(this,key,value);
    try{
      if(isLocalStorage(this) && !applyingCloud && SYNC_KEYS.indexOf(String(key)) >= 0){
        if(initialCloudCheckDone) schedulePush();
        else setTimeout(schedulePush,1000);
      }
    }catch(e){}
    return result;
  };

  window.smyleCloudSyncNow = function(){
    return pushCloud();
  };

  loadCloud();
})();
</script>
'''

if marker not in html:
    pos = html.rfind('</body>')
    if pos < 0:
        raise RuntimeError('Fechamento </body> principal não encontrado.')
    html = html[:pos] + script + '\n' + html[pos:]

path.write_text(html, encoding='utf-8')
print('V65 aplicada: conteúdo dos jogos sincronizado pelo Firestore para todos os dispositivos.')
