const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: true});
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
  
  await page.goto('file://' + __dirname.replace(/\\/g, '/') + '/index.html', {waitUntil: 'networkidle0'});
  
  const categories = await page.$$('.menu-tab');
  console.log('Categories found:', categories.length);
  
  const items = await page.$$('.food-card');
  console.log('Items found:', items.length);
  
  if (items.length > 0) {
      const visibility = await page.evaluate(() => {
          const el = document.querySelector('.food-card');
          return window.getComputedStyle(el).opacity;
      });
      console.log('First item opacity:', visibility);
  }
  
  await browser.close();
})();
