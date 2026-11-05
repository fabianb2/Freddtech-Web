const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const code = fs.readFileSync('public/assets/js/ads.js', 'utf8');
function environment(present = true) {
  const section = {hidden: false};
  const unit = {dataset: {}, closest: () => section};
  const options = {hidden: true, addEventListener: (_, fn) => options.click = fn};
  const scripts = [];
  let observer;
  const context = {window: {}, document: {
    querySelector: selector => selector.startsWith('ins.') ? (present ? unit : null) : options,
    createElement: () => ({}), head: {appendChild: script => scripts.push(script)}
  }, MutationObserver: class {constructor(fn) {observer = fn;} observe() {}}};
  return {run: () => vm.runInNewContext(code, context), section, unit, options, scripts, context, observe: () => observer()};
}
let e = environment(); e.run(); e.run();
assert.equal(e.scripts.length, 1, 'Only one Google loader');
assert.equal(e.context.window.adsbygoogle.length, 1, 'Only one ad request');
assert.match(e.scripts[0].src, /client=ca-pub-1728686227442320$/);
assert.equal(e.options.hidden, true, 'No false consent control before API');
let revoked = 0;
e.context.window.googlefc.showRevocationMessage = () => revoked++;
e.context.window.googlefc.callbackQueue[0].CONSENT_API_READY();
assert.equal(e.options.hidden, false); e.options.click();
e.context.window.googlefc.callbackQueue[1](); assert.equal(revoked, 1);
e.unit.dataset.adStatus = 'unfilled'; e.observe(); assert.equal(e.section.hidden, true);
e = environment(); e.run(); e.scripts[0].onerror(); assert.equal(e.section.hidden, true);
e = environment(false); e.run(); assert.equal(e.scripts.length, 0);
for (const page of ['public/404.html', 'public/soporte/index.html', 'public/privacidad/web/index.html']) {
  const html = fs.readFileSync(page,'utf8');
  assert.ok(!html.includes('data-ad-slot=')); assert.ok(!html.includes('./assets/js/ads.js'));
}
const home = fs.readFileSync('public/index.html','utf8');
assert.equal((home.match(/data-ad-slot="1959689089"/g)||[]).length, 1);
assert.ok(home.indexOf('data-ad-slot=') > home.indexOf('id="aplicaciones"'));
console.log('OK: one request, correct client, no ads on excluded pages, CMP revocation, blocked loader and unfilled handling.');
