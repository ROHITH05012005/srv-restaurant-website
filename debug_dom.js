const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: true});
  const page = await browser.newPage();
  
  await page.goto('file://' + __dirname.replace(/\\/g, '/') + '/index.html', {waitUntil: 'networkidle0'});
  
  const box = await page.evaluate(() => {
    const img = document.querySelector('.food-card-img img');
    if (!img) return 'NO IMG FOUND';
    const rect = img.getBoundingClientRect();
    return { w: rect.width, h: rect.height, src: img.src, complete: img.complete, naturalWidth: img.naturalWidth };
  });

  console.log(box);
  await browser.close();
})();
