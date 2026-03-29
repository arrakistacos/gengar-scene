#!/usr/bin/env node
const { chromium } = require('playwright');

(async () => {
    console.log('Careful Google Lens automation...');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 200  // Slow down for stability
    });
    
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1920, height: 1080 });
    
    try {
        // Go to Google Images search
        console.log('Opening Google Images...');
        await page.goto('https://images.google.com');
        
        // Wait for page to fully load
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(3000);
        
        console.log('Looking for camera icon...');
        
        // Try to find camera icon by looking at the page structure
        // The camera icon is typically in the search bar
        const pageContent = await page.content();
        
        // Look for the camera icon - it's usually near the search button
        // Try clicking by coordinates (camera is typically on the right side of search bar)
        const searchBar = await page.$('input[name="q"]');
        if (searchBar) {
            const box = await searchBar.boundingBox();
            if (box) {
                // Click to the right of search bar where camera should be
                await page.mouse.click(box.x + box.width + 50, box.y + box.height/2);
                console.log('Clicked near search bar (camera location)');
            }
        }
        
        await page.waitForTimeout(3000);
        
        // Now look for upload area
        console.log('Looking for upload area...');
        
        // Try multiple ways to find upload
        const uploadSelectors = [
            'input[type="file"]',
            '[accept*="image"]',
            'text=Upload',
            'text=Choose File',
            'text=Paste image URL'
        ];
        
        let uploadFound = false;
        for (const selector of uploadSelectors) {
            try {
                const element = await page.$(selector);
                if (element) {
                    console.log(`Found element: ${selector}`);
                    uploadFound = true;
                    break;
                }
            } catch (e) {}
        }
        
        if (!uploadFound) {
            console.log('Taking screenshot to see what loaded...');
            await page.screenshot({ 
                path: '/home/freeman/.openclaw/workspace/gengar-project/debug_after_click.png' 
            });
            console.log('Screenshot saved to debug_after_click.png');
        }
        
        // Keep open for manual interaction
        console.log('Browser will stay open. Please manually upload the image if needed.');
        console.log('Image path: /home/freeman/.openclaw/workspace/gengar-project/render_fixed.png');
        await page.waitForTimeout(60000);
        
    } catch (error) {
        console.error('Error:', error);
        await page.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/error.png' 
        });
    } finally {
        await browser.close();
    }
})();
