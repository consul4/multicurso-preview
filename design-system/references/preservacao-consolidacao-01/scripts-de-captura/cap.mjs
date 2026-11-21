import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
const [,, base, prefixo] = process.argv;
const b = await chromium.launch();
for (const [w,h,d] of [[1440,900,'desktop'],[390,844,'celular']]) {
  const p = await b.newPage({ viewport:{width:w,height:h} });
  for (const r of ['cursos','video','leitura','atividade','laboratorio']) {
    await p.goto(`${base}/mc-design-10/#${r}`); await p.waitForTimeout(900);
    await p.screenshot({ path: `${prefixo}-${d}-${r}.png` });
  }
  await p.close();
}
await b.close();
