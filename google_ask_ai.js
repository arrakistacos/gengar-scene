#!/usr/bin/env node
/**
 * Upload image to Google and ask AI about it
 */

const { chromium } = require('playwright');

(async () => {
    console.log('Google AI Image Analysis...');
    
    const browser = await chromium.launch({ headless: false });
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1920, height: 1080 });
    
    try {
        // Go to Google Lens directly
        console.log('Opening Google Lens...');
        await page.goto('https://lens.google.com');
        await page.waitForTimeout(2000);
        
        // Click "Upload an image"
        console.log('Clicking upload...');
        await page.click('text=Upload an image');
        await page.waitForTimeout(1500);
        
        // Upload file
        const imagePath = '/home/freeman/.openclaw/workspace/gengar-project/render_fixed.png';
        const input = await page.$('input[type="file"]');
        await input.setInputFiles(imagePath);
        console.log('Image uploaded');
        
        // Wait for analysis
        console.log('Waiting for analysis (15s)...');
        await page.waitForTimeout(15000);
        
        // Screenshot results
        await page.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/lens_final.png',
            fullPage: true 
        });
        
        console.log('Screenshot saved. Now opening regular Google search...');
        
        // Open new tab with Google search
        const newPage = await browser.newPage();
        await newPage.goto('https://google.com');
        await newPage.waitForTimeout(2000);
        
        // Ask Google AI about the character
        console.log('Asking Google AI about the image...');
        await newPage.fill('textarea[name="q"]', 
            'What Pokemon character looks like a purple ghost with big ears and wide smile?');
        await newPage.press('textarea[name="q"]', 'Enter');
        
        await newPage.waitForTimeout(5000);
        
        await newPage.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/google_ai_answer.png',
            fullPage: true 
        });
        
        console.log('AI answer screenshot saved');
        
        // Wait to see results
        await newPage.waitForTimeout(30000);
        
    } catch (error) {
        console.error('Error:', error.message);
    } finally {
        await browser.close();
    }
})();
