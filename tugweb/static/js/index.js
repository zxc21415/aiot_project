
  var red = document.getElementById('red');
  var green = document.getElementById('greenn');
  green.addEventListener('animationend', greeninred, once = true);
  function greeninred() {
    red.appendChild(green);
    green.className = 'new_green'
  }

