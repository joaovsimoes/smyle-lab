from pathlib import Path

path = Path('public/index.html')
if not path.exists():
    raise SystemExit('public/index.html não encontrado')

html = path.read_text(encoding='utf-8')

marker = 'id="smyle-v66-authoritative-cloud-content"'
script = r'''
<script id="smyle-v66-authoritative-cloud-content">
(function(){
  'use strict';

  // Impede que conteúdo padrão excluído pelo administrador seja recriado.
  window.smyleV66ExactContent = true;

  function safeParse(raw, fallback){
    try{
      var v = JSON.parse(raw);
      return v == null ? fallback : v;
    }catch(e){ return fallback; }
  }

  function exactQuestions(){
    var raw = localStorage.getItem('dojo_questions_v1');
    if(raw === null){
      var seed = (typeof defaults!=='undefined' && Array.isArray(defaults.questions)) ? defaults.questions : [];
      localStorage.setItem('dojo_questions_v1', JSON.stringify(seed));
      raw = localStorage.getItem('dojo_questions_v1');
    }
    var list = safeParse(raw, []);
    return Array.isArray(list) ? list.map(function(q){
      var gid = q.gameId || 'fato-fake';
      var name = q.gameName || 'Fato ou Fake';
      try{
        if(typeof getModel==='function') name = q.gameName || getModel(gid).name || name;
      }catch(e){}
      return Object.assign({},q,{
        gameId:gid,
        gameName:name,
        stats:q.stats || {hits:0,misses:0}
      });
    }) : [];
  }

  function exactNativeContent(){
    var key = (typeof SMYLE_NATIVE_CONTENT_KEY!=='undefined')
      ? SMYLE_NATIVE_CONTENT_KEY
      : 'smyle_lab_native_content_v17';

    var raw = localStorage.getItem(key);
    if(raw === null){
      var seed = {};
      try{
        if(typeof SMYLE_NATIVE_DEFAULT_CONTENT!=='undefined'){
          seed = JSON.parse(JSON.stringify(SMYLE_NATIVE_DEFAULT_CONTENT));
        }
      }catch(e){}
      localStorage.setItem(key, JSON.stringify(seed));
      raw = localStorage.getItem(key);
    }

    var data = safeParse(raw,{});
    return data && typeof data === 'object' ? data : {};
  }

  function installExactReaders(){
    // O código original possui mais de uma declaração dessas funções.
    // Atribuímos no window depois de todos os scripts para garantir precedência.
    window.getQuestions = exactQuestions;
    window.ensureFatoFakeSeed = function(){
      if(localStorage.getItem('dojo_questions_v1') === null){
        var seed = (typeof defaults!=='undefined' && Array.isArray(defaults.questions)) ? defaults.questions : [];
        localStorage.setItem('dojo_questions_v1', JSON.stringify(seed));
      }
    };
    window.getNativeContent = exactNativeContent;

    window.saveQuestions = function(data){
      localStorage.setItem('dojo_questions_v1',JSON.stringify(Array.isArray(data)?data:[]));
    };
    window.saveNativeContent = function(data){
      var key = (typeof SMYLE_NATIVE_CONTENT_KEY!=='undefined')
        ? SMYLE_NATIVE_CONTENT_KEY
        : 'smyle_lab_native_content_v17';
      localStorage.setItem(key,JSON.stringify(data && typeof data==='object' ? data : {}));
    };
  }

  function refreshVisibleContent(){
    try{
      if(typeof renderSetupOptions==='function' && !document.getElementById('setupScreen')?.classList.contains('hidden')){
        renderSetupOptions();
      }
    }catch(e){}
    try{
      if(typeof renderQuestionsTable==='function' && document.getElementById('adminScreen') && !document.getElementById('adminScreen').classList.contains('hidden')){
        renderQuestionsTable();
      }
    }catch(e){}
  }

  installExactReaders();
  document.addEventListener('DOMContentLoaded',function(){
    installExactReaders();
    setTimeout(installExactReaders,50);
    setTimeout(installExactReaders,250);
  });
  window.addEventListener('load',function(){
    installExactReaders();
    refreshVisibleContent();
  });
})();
</script>
'''

if marker not in html:
    pos = html.rfind('</body>')
    if pos < 0:
        raise RuntimeError('Fechamento </body> principal não encontrado.')
    html = html[:pos] + script + '\n' + html[pos:]

path.write_text(html, encoding='utf-8')
print('V66 aplicada: exclusões e reduções de perguntas passam a ser autoritativas; conteúdo padrão não é recriado.')
