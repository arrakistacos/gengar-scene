#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
    console.log('Launching browser...');
    
    const browser = await chromium.launch({
        headless: false,
        args: ['--start-maximized']
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    // Navigate to Google Lens
    console.log('Opening Google Lens...');
    await page.goto('https://lens.google.com');
    
    // Wait for the upload button
    console.log('Waiting for upload button...');
    await page.waitForTimeout(3000);
    
    // Click on "Upload image" button
    // Google Lens has a camera icon or "Upload image" text
    const uploadButton = await page.$('text=Upload image');
    if (uploadButton) {
        await uploadButton.click();
        console.log('Clicked upload button');
    } else {
        // Try clicking on the camera icon area
        await page.click('[aria-label*="Upload"]');
        console.log('Clicked camera icon');
    }
    
    await page.waitForTimeout(2000);
    
    // Upload the file
    const filePath = '/home/freeman/.openclaw/workspace/gengar-project/render_iteration6.png';
    const input = await page.$('input[type="file"]');
    if (input) {
        await input.setInputFiles(filePath);
        console.log('File uploaded:', filePath);
    } else {
        console.log('File input not found, trying drag and drop...');
    }
    
    // Wait for analysis
    console.log('Waiting for analysis...');
    await page.waitForTimeout(15000);
    
    // Take screenshot
    await page.screenshot({ 
        path: '/home/freeman/.openclaw/workspace/gengar-project/lens_results.png',
        fullPage: true 
    });
    
    console.log('Screenshot saved to lens_results.png');
    console.log('Browser will stay open for 60 seconds');
    
    await page.waitForTimeout(60000);
    
    await browser.close();
})();
