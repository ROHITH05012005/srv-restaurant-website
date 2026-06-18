const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: true});
  const page = await browser.newPage();
  
  await page.goto('file://' + __dirname.replace(/\\/g, '/') + '/index.html', {waitUntil: 'networkidle0'});
  
  const box = await page.evaluate(() => {
    const imgs = Array.from(document.querySelectorAll('img'));
    const idli = imgs.find(i => i.src.includes('idli_premium'));
    if (!idli) return 'NO IDLI FOUND';
    const rect = idli.getBoundingClientRect();
    return { w: rect.width, h: rect.height, src: idli.src, complete: idli.complete, naturalWidth: idli.naturalWidth };
  });

  console.log(box);
  await browser.close();
})();
