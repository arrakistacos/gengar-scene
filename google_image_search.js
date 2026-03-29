#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
    console.log('Launching browser for Google image search...');
    
    const browser = await chromium.launch({
        headless: false,
        args: ['--start-maximized']
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    // Go to Google
    console.log('Opening Google...');
    await page.goto('https://www.google.com');
    await page.waitForTimeout(2000);
    
    // Click on the camera icon for image search
    console.log('Clicking image search icon...');
    // The camera icon is usually in the search bar
    try {
        await page.click('div[role="button"][aria-label*="Search by image"], div[aria-label*="camera"]');
    } catch (e) {
        console.log('Trying alternative selector...');
        await page.click('[data-ved*="camera"]');
    }
    
    await page.waitForTimeout(2000);
    
    // Upload image
    console.log('Uploading image...');
    const filePath = '/home/freeman/.openclaw/workspace/gengar-project/render_fixed.png';
    
    // Wait for file input and upload
    const fileInput = await page.$('input[type="file"]');
    if (fileInput) {
        await fileInput.setInputFiles(filePath);
        console.log('Image uploaded');
    } else {
        console.log('File input not found, trying drag and drop area...');
    }
    
    // Wait for upload and analysis
    console.log('Waiting for analysis...');
    await page.waitForTimeout(8000);
    
    // Take screenshot
    await page.screenshot({ 
        path: '/home/freeman/.openclaw/workspace/gengar-project/google_search_results.png',
        fullPage: true 
    });
    
    console.log('Screenshot saved to google_search_results.png');
    
    // Keep browser open for a while
    console.log('Browser will stay open for 60 seconds...');
    await page.waitForTimeout(60000);
    
    await browser.close();
})();
