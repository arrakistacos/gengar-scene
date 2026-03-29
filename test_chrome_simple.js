#!/usr/bin/env node
/**
 * Simple Chrome test
 */

const { chromium } = require('playwright');

(async () => {
    console.log('Testing Chrome...');
    
    try {
        const browser = await chromium.launch({ 
            headless: false,
            slowMo: 500
        });
        
        const context = await browser.newContext();
        const page = await context.newPage();
        
        console.log('Opening Google...');
        await page.goto('https://google.com');
        
        console.log('Waiting 5 seconds...');
        await page.waitForTimeout(5000);
        
        console.log('Taking screenshot...');
        await page.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/chrome_test.png',
            fullPage: true 
        });
        
        console.log('✓ Chrome test complete! Screenshot saved: chrome_test.png');
        
        await browser.close();
        
    } catch (error) {
        console.error('Error:', error.message);
    }
})();
