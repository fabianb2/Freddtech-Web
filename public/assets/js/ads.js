/* One responsive display unit on the homepage; Google manages CMP consent. */
(() => {
  'use strict';
  const unit = document.querySelector('ins.adsbygoogle[data-ad-slot="1959689089"]');
  if (!unit || unit.dataset.requested) return;
  unit.dataset.requested = 'true';
  const options = document.querySelector('[data-privacy-options]');
  window.googlefc = window.googlefc || {};
  window.googlefc.callbackQueue = window.googlefc.callbackQueue || [];
  window.googlefc.callbackQueue.push({ CONSENT_API_READY: () => {
    if (!options || typeof window.googlefc.showRevocationMessage !== 'function') return;
    options.hidden = false;
    options.addEventListener('click', () => window.googlefc.callbackQueue.push(window.googlefc.showRevocationMessage));
  }});
  const loader = document.createElement('script');
  loader.async = true;
  loader.crossOrigin = 'anonymous';
  loader.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1728686227442320';
  loader.onerror = () => unit.closest('.ad-section').hidden = true;
  document.head.appendChild(loader);
  window.adsbygoogle = window.adsbygoogle || [];
  window.adsbygoogle.push({});
  new MutationObserver(() => {
    if (unit.dataset.adStatus === 'unfilled') unit.closest('.ad-section').hidden = true;
  }).observe(unit, { attributes: true, attributeFilter: ['data-ad-status'] });
})();
