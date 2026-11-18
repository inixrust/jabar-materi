const React = require('/opt/npm-tools/node_modules/react');
const { renderToStaticMarkup } = require('/opt/npm-tools/node_modules/react-dom/server');
const fa = require('/opt/npm-tools/node_modules/react-icons/fa');
const out = {};
for (const [n, C] of Object.entries(fa)) {
  try {
    const svg = renderToStaticMarkup(React.createElement(C, { size: 100 }));
    const vb = (svg.match(/viewBox="([^"]+)"/) || [])[1];
    const inner = svg.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
    if (vb && inner.length < 6000) out[n] = { vb, inner };
  } catch (e) {}
}
require('fs').writeFileSync('fa_icons.json', JSON.stringify(out));
console.log(Object.keys(out).length);
