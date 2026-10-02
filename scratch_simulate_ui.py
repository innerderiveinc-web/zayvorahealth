with open('index.html') as f:
    text = f.read()

import re
scripts = re.findall(r'<script(?:\s+[^>]*)?>(.*?)</script>', text, re.DOTALL)

with open('scratch_test_interactions.js', 'w') as f:
    f.write('''
var mockElem = function(id) {
  return {
    id: id || '',
    style: {},
    classList: {
      add: function(c){},
      remove: function(c){},
      contains: function(c){ return false; }
    },
    setAttribute: function(k, v){},
    getAttribute: function(k){ return null; },
    appendChild: function(c){},
    querySelectorAll: function(sel){ return []; },
    querySelector: function(sel){ return mockElem(); },
    innerHTML: '',
    textContent: '',
    value: '',
    addEventListener: function(evt, fn){}
  };
};

var window = {
  location: { search: '', hash: '', pathname: '/', reload: function(){} },
  addEventListener: function(evt, fn){},
  localStorage: {
    _data: {},
    getItem: function(k){ return this._data[k] || null; },
    setItem: function(k, v){ this._data[k] = String(v); },
    removeItem: function(k){ delete this._data[k]; }
  },
  scrollTo: function(){},
  scrollY: 0,
  history: { pushState: function(){} }
};
var document = {
  documentElement: mockElem('html'),
  getElementById: function(id) { return mockElem(id); },
  querySelector: function(sel) { return mockElem(); },
  querySelectorAll: function(sel) { return []; },
  createElement: function(tag) { return mockElem(tag); },
  addEventListener: function(evt, fn){},
  readyState: 'complete'
};
var localStorage = window.localStorage;
var navigator = { onLine: true };
var fetch = function() { return Promise.resolve({ ok: true, json: function() { return Promise.resolve({}); } }); };
var URLSearchParams = function() { return { get: function() { return null; } }; };

''' + scripts[2] + '''

print("Testing initializeApp()...");
try {
  initializeApp();
  print("initializeApp() SUCCESS");
} catch(e) {
  print("initializeApp() ERROR: " + e + " at line " + e.line);
}

var roles = ['website', 'doctor', 'pharmacy', 'patient', 'nurse', 'clinic', 'admin', 'research', 'manufacturing', 'herbals'];
for (var i = 0; i < roles.length; i++) {
  var r = roles[i];
  print("Testing switchRole('" + r + "')...");
  try {
    switchRole(r, true);
    print("switchRole('" + r + "') SUCCESS");
  } catch(e) {
    print("switchRole('" + r + "') ERROR: " + e);
  }
}

print("Testing switchTab on website...");
var tabs = ['home', 'services', 'products', 'research', 'about', 'contact', 'philosophy', 'clinics', 'doctors', 'faqs'];
for (var j = 0; j < tabs.length; j++) {
  var t = tabs[j];
  print("Testing switchTab('" + t + "')...");
  try {
    switchTab(t);
    print("switchTab('" + t + "') SUCCESS");
  } catch(e) {
    print("switchTab('" + t + "') ERROR: " + e);
  }
}

print("ALL INTERACTIONS COMPLETED WITHOUT FATAL ERRORS");
''')

