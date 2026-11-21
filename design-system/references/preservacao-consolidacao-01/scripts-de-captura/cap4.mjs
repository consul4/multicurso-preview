import { createRequire } from 'node:module';
const { chromium, devices } = createRequire(import.meta.url)('playwright');
const [,, base, saida] = process.argv;
const b = await chromium.launch();
for (const [d, o] of [['desktop',{viewport:{width:1440,height:900}}],['celular',{...devices['iPhone 13']}]]) {
  const p = await (await b.newContext(o)).newPage();
  for (const r of ['gestao','estrutura','construtor','editor','recursos','previa']) { await p.goto(`${base}/mc-design-10/#${r}`); await p.waitForTimeout(700); await p.screenshot({ path: `${saida}/admin-${d}-${r}.png`, fullPage: d==='desktop' }); }
}
await b.close();
