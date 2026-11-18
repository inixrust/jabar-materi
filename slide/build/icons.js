const React = require('react');
const { renderToStaticMarkup } = require('react-dom/server');
const sharp = require('sharp');
const fa = require('react-icons/fa');
const names = process.argv.slice(2);
const colors = { w: '#FFFFFF', b: '#0E5A8A', r: '#C00000', d: '#1A1A1A', g: '#7F7F7F' };
(async () => {
  for (const n of names) {
    const C = fa[n];
    if (!C) { console.log('MISSING', n); continue; }
    for (const [k, col] of Object.entries(colors)) {
      const svg = renderToStaticMarkup(React.createElement(C, { color: col, size: 256 }));
      await sharp(Buffer.from(svg)).png().toFile(`icons/${n}_${k}.png`);
    }
  }
  console.log('done', names.length);
})();
