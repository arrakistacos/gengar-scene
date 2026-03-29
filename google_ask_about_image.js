#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
    console.log('Opening Google with image analysis...');
    
    const browser = await chromium.launch({
        headless: false,
        args: ['--start-maximized']
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    // Go to Google Lens directly with image
    console.log('Opening Google Lens...');
    await page.goto('https://lens.google.com');
    await page.waitForTimeout(3000);
    
    // Click upload
    console.log('Clicking upload...');
    await page.click('text=Upload image');
    await page.waitForTimeout(2000);
    
    // Upload the rendered model
    const filePath = '/home/freeman/.openclaw/workspace/gengar-project/render_fixed.png';
    const input = await page.$('input[type="file"]');
    if (input) {
        await input.setInputFiles(filePath);
        console.log('Uploaded render_fixed.png');
    }
    
    // Wait for analysis
    await page.waitForTimeout(10000);
    
    // Take screenshot of results
    await page.screenshot({ 
        path: '/home/freeman/.openclaw/workspace/gengar-project/lens_analysis.png',
        fullPage: true 
    });
    
    console.log('Lens analysis complete');
    
    // Now open Google search in new tab
    const newPage = await context.newPage();
    await newPage.goto('https://google.com');
    await newPage.waitForTimeout(2000);
    
    // Type question about the image
    console.log('Asking question about the image...');
    await newPage.fill('textarea[name="q"]', 
        'What character is in this image? file:///home/freeman/.openclaw/workspace/gengar-project/render_fixed.png');
    await newPage.press('textarea[name="q"]', 'Enter');
    
    await newPage.waitForTimeout(5000);
    
    // Screenshot the answer
    await newPage.screenshot({ 
        path: '/home/freeman/.openclaw/workspace/gengar-project/google_answer.png',
        fullPage: true 
    });
    
    console.log('Answer screenshot saved');
    
    await page.waitForTimeout(30000);
    await browser.close();
})();
