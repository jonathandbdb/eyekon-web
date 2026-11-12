// EyeKon — propuesta: menú móvil, comparador antes/después y selector de escenas.
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.querySelector('.mobile-nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Comparador: un <input type=range> invisible encima mueve la cortina (teclado y touch gratis).
  document.querySelectorAll('.compare').forEach(function (c) {
    var r = c.querySelector('input');
    if (!r) return; // .compare.auto: animado por CSS, sin control
    var set = function () { c.style.setProperty('--pos', r.value + '%'); };
    r.addEventListener('input', set);
    set();
  });

  // Comparador EyeKon: escena + lente izquierda/derecha. Cada escena lista las capturas disponibles.
  var SCENES = {
    ventana: ['catarata', 'monofocal'],
    lectura: ['monofocal', 'multifocal', 'edof'],
    living: ['monofocal', 'edof', 'multifocal'],
    ruta: ['monofocal', 'multifocal', 'edof']
  };
  var cmp = document.getElementById('cmp');
  if (cmp) {
    var names = JSON.parse(cmp.getAttribute('data-names'));
    var dir = '/assets/img/sim/eyekon/';
    var selA = document.querySelector('.lens-pick [data-side=a]');
    var selB = document.querySelector('.lens-pick [data-side=b]');
    var scene = 'ventana';
    var fill = function (sel, val) {
      sel.innerHTML = SCENES[scene].map(function (k) { return '<option value="' + k + '">' + names[k] + '</option>'; }).join('');
      sel.value = val;
    };
    var render = function () {
      cmp.querySelector('.before').src = dir + scene + '-' + selA.value + '.webp';
      cmp.querySelector('.after').src = dir + scene + '-' + selB.value + '.webp';
      cmp.querySelector('.lbl.l').textContent = names[selA.value];
      cmp.querySelector('.lbl.r').textContent = names[selB.value];
    };
    var setScene = function (s) {
      scene = s;
      var l = SCENES[s];
      fill(selA, l[0]); fill(selB, l[1]);
      render();
    };
    selA.addEventListener('change', render);
    selB.addEventListener('change', render);
    document.querySelectorAll('[data-scene]').forEach(function (b) {
      b.addEventListener('click', function () {
        document.querySelectorAll('[data-scene]').forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        setScene(b.getAttribute('data-scene'));
      });
    });
    setScene('ventana');
  }
})();

// Armazón de prueba (home): cada lente de la bandeja entra en el ojo derecho.
(function () {
  var view = document.getElementById('trial-view');
  if (!view) return;
  var name = document.getElementById('trial-name');
  var chips = document.querySelectorAll('.trial-lens');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      if (c.getAttribute('aria-pressed') === 'true') return;
      chips.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
      c.setAttribute('aria-pressed', 'true');
      var old = view.querySelector('img');
      var img = new Image();
      img.alt = old.alt;
      img.className = 'out';
      img.src = '/assets/img/sim/eyekon/lectura-' + c.getAttribute('data-lens') + '.webp';
      img.onload = function () {
        view.appendChild(img);
        void img.offsetWidth;
        requestAnimationFrame(function () { img.className = ''; old.className = 'out'; });
        setTimeout(function () { if (old.parentNode) old.parentNode.removeChild(old); }, 800);
      };
      name.textContent = c.querySelector('.tl-tab').textContent;
    });
  });
})();
