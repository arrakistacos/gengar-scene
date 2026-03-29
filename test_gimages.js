#!/usr/bin/env node
/**
 * Alternative: Use Google Images directly instead of Google Lens
 */

const { chromium } = require('playwright');

(async () => {
    console.log('=== Testing Google Images Upload ===\n');
    
    try {
        const browser = await chromium.launch({ 
            headless: false,
            slowMo: 500
        });
        
        const context = await browser.newContext({
            viewport: { width: 1920, height: 1080 }
        });
        
        const page = await context.newPage();
        
        // Go to Google Images
        console.log('Opening Google Images...');
        await page.goto('https://images.google.com');
        await page.waitForTimeout(3000);
        
        // Click camera icon for reverse image search
        console.log('Looking for camera icon...');
        
        // The camera icon should be in the search bar
        const cameraButton = await page.$('div[aria-label="Search by image"], svg[focusable="false"]');
        if (cameraButton) {
            console.log('Found camera button, clicking...');
            await cameraButton.click();
        } else {
            // Try alternative - look for any clickable element
            console.log('Trying alternative selectors...');
            const buttons = await page.$$('div[role="button"], button');
            for (const btn of buttons) {
                const title = await btn.getAttribute('aria-label');
                if (title && title.includes('camera')) {
                    console.log('Found camera button by aria-label');
                    await btn.click();
                    break;
                }
            }
        }
        
        await page.waitForTimeout(2000);
        
        // Look for upload option
        console.log('Looking for upload option...');
        await page.screenshot({ path: '/home/freeman/.openclaw/workspace/gengar-project/gimages_after_click.png' });
        
        // Try to find and use file input
        const fileInput = await page.$('input[type="file"]');
        if (fileInput) {
            console.log('Found file input, uploading...');
            await fileInput.setInputFiles('/home/freeman/.openclaw/workspace/gengar-project/pikachu_iter5.png');
            console.log('✓ Uploaded!');
            await page.waitForTimeout(10000);
            
            await page.screenshot({ path: '/home/freeman/.openclaw/workspace/gengar-project/gimages_results.png' });
            console.log('✓ Results saved: gimages_results.png');
        } else {
            console.log('⚠ No file input found');
        }
        
        await browser.close();
        console.log('Done!');
        
    } catch (error) {
        console.error('Error:', error.message);
    }
})();
