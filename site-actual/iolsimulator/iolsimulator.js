(function(){
  var link=document.getElementById('iols-video-link'), dlg=document.getElementById('iols-dialog');
  if(!link||!dlg||typeof dlg.showModal!=='function') return; // sin <dialog>: el enlace abre el mp4 directo
  var v=dlg.querySelector('video');
  link.addEventListener('click',function(e){e.preventDefault();dlg.showModal();v.play();});
  dlg.addEventListener('close',function(){v.pause();});
  dlg.querySelector('.iols-close').addEventListener('click',function(){dlg.close();});
  dlg.addEventListener('click',function(e){if(e.target===dlg) dlg.close();});
})();
