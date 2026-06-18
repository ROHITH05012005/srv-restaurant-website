const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: true});
  const page = await browser.newPage();
  
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto('file://' + __dirname.replace(/\\/g, '/') + '/index.html', {waitUntil: 'networkidle0'});
  
  // Wait a bit just in case
  await new Promise(r => setTimeout(r, 1000));
  
  await page.screenshot({path: 'C:/Users/rohib/.gemini/antigravity/brain/cc13a8d4-8187-4b1a-8d20-77f4f1d8406f/scratch/screenshot.png', fullPage: true});
  
  await browser.close();
  console.log("Screenshot saved!");
})();
