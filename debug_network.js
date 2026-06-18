const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: true});
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('requestfailed', request => {
    console.log('REQUEST FAILED:', request.url(), request.failure().errorText);
  });
  page.on('response', response => {
    if(!response.ok()) {
      console.log('RESPONSE NOT OK:', response.url(), response.status());
    }
  });

  await page.goto('file://' + __dirname.replace(/\\/g, '/') + '/index.html', {waitUntil: 'networkidle0'});
  
  await browser.close();
})();
