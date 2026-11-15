/* nullsec auth v0.9b
var key = '0day';
var pass = [0xac, 0x3d, 0x89, 0x28, 0xf3, 0x80, 0x4b, 0x56, 0xc5, 0xb1, 0x9d, 0xe4, 0x33, 0xfe, 0x95];


function XOR(i) {
  return key.charCodeAt(i % key.length) ^ ((i * 0x1d) & 0xff);
}

function ROT3(v) {
  return ((v >>> 3) | (v << 5)) & 0xff;
}

function encryption(s) {
  var o = [], a = 0x5a;
  s = s.slice().reverse()
  for (var i = 0; i < s.length; i++) {
    var v = (ROT3(s[i]));
    var c = ((v - a)^ XOR(i)) & 0xff;
    o.push(c);
    a = (a + c * 3) & 0xff;

  }
  return o;
}

function verify(p) {
  if (p.length !== pass.length) return false;
  var e = encryption(p);
  for (var i = 0; i < e.length; i++) {
    if (e[i] !== pass[i]) return false;
  }
  return true;
}

function login() {
  var pw = document.getElementById('pw').value;
  var out = document.getElementById('out');
  if (!verify(pw)) {
    out.innerHTML = '<div class="err">&gt; неверный ключ. попытка записана в лог.</div>';
    return;
  }
  out.innerHTML = '<div>&gt; ключ принят локально, запрашиваю разделы...</div>';
  fetch('/vault?key=' + encodeURIComponent(pw))
    .then(function (r) { return r.text(); })
    .then(function (t) { out.innerHTML = t; });
}

document.getElementById('go').addEventListener('click', login);
document.getElementById('pw').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') login();
});
