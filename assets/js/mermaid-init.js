// External mermaid loader and renderer (moved out of head to avoid CSP/inline script issues)
(function() {
  try {
    console.log('mermaid-init: script loaded');
  } catch (e) {}

  function initMermaidAndRender() {
    try {
      console.log('mermaid-init: initMermaidAndRender start');
      var codes = document.querySelectorAll('pre > code.language-mermaid');
      console.log('mermaid-init: found mermaid code blocks:', codes.length);
      codes.forEach(function(code) {
        var pre = code.parentElement;
        var diagram = document.createElement('div');
        diagram.className = 'mermaid';
        diagram.textContent = code.textContent;
        pre.replaceWith(diagram);
      });
      if (typeof mermaid !== 'undefined') {
        mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });
        try { mermaid.run({ querySelector: '.mermaid' }); } catch (e) { console.error('mermaid.run error:', e); }
      } else {
        console.warn('mermaid is undefined after script load.');
      }
    } catch (e) {
      console.error('mermaid-init error:', e);
    }
  }

  function loadMermaid() {
    try {
      console.log('mermaid-init: loadMermaid called');
      var s = document.createElement('script');
      s.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js';
      s.defer = true;
      s.onload = function() { console.log('mermaid-init: mermaid script onload'); initMermaidAndRender(); };
      s.onerror = function() { console.error('mermaid-init: Failed to load mermaid.min.js from CDN.'); };
      document.head.appendChild(s);
    } catch (e) { console.error('mermaid-init load error:', e); }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadMermaid);
  } else {
    loadMermaid();
  }
})();
