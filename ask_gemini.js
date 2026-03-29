#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
    console.log('Opening Gemini to analyze image...');
    
    const browser = await chromium.launch({
        headless: false,
        args: ['--start-maximized']
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    // Go to Gemini
    await page.goto('https://gemini.google.com');
    await page.waitForTimeout(3000);
    
    console.log('Please manually upload the image and ask:');
    console.log('"What Pokemon character is this? Describe its features."');
    console.log('');
    console.log('Image path: /home/freeman/.openclaw/workspace/gengar-project/render_fixed.png');
    
    // Keep browser open
    await page.waitForTimeout(120000);
    
    await browser.close();
})();
