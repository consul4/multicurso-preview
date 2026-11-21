import { createRequire } from 'node:module';
const { chromium, devices } = createRequire(import.meta.url)('playwright');
const [,, base, saida] = process.argv;
const b = await chromium.launch();
for (const [d, o] of [['desktop',{viewport:{width:1440,height:900}}],['tablet',{viewport:{width:1024,height:768}}],['celular',{...devices['iPhone 13']}]]) {
  const ctx = await b.newContext(o); const p = await ctx.newPage();
  for (const r of ['video','leitura']) {
    await p.goto(`${base}/mc-design-10/#${r}`); await p.waitForTimeout(900);
    // libera a leitura na prévia (estado local de demonstração) para comparar conteúdo, não o bloqueio
    if (r==='leitura') { await p.evaluate(() => { const k='multicurso-design10-v1'; const s=JSON.parse(localStorage.getItem(k)||'{}'); s.done=['video']; localStorage.setItem(k, JSON.stringify(s)); }); await p.reload(); await p.waitForTimeout(900); }
    await p.screenshot({ path: `${saida}/previa-${d}-${r}.png` });
  }
  await ctx.close();
}
await b.close();
