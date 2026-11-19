// Isole le CSS de la landing camping sous .camping-page (aucune fuite vers le reste du site)
import fs from 'node:fs'
import postcss from 'postcss'
import prefixer from 'postcss-prefix-selector'

const [, , input, output] = process.argv
const css = fs.readFileSync(input, 'utf8')
const P = '.camping-page'
const out = postcss([
  // les polices viennent déjà du site (assets/css/fonts.css)
  { postcssPlugin: 'drop-font-face', AtRule: { 'font-face': (r) => r.remove() } },
  prefixer({
    prefix: P,
    transform(prefix, selector) {
      if (selector === ':root' || selector === 'body' || selector === 'html') return P
      if (selector === '*') return `${P}, ${P} *`
      if (selector.startsWith('html.')) {
        const [htmlPart, ...rest] = selector.split(' ')
        return `${htmlPart} ${P} ${rest.join(' ')}`.trim()
      }
      if (selector.startsWith('body ')) return `${P} ${selector.slice(5)}`
      return `${P} ${selector}`
    },
  }),
]).process(css, { from: undefined }).css
fs.writeFileSync(output, out)
console.log(`CSS isolé : ${output} (${out.length} car.)`)
