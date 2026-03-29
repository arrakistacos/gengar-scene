#!/usr/bin/env node
/**
 * Use Google Images camera icon for reverse image search
 */

const { chromium } = require('playwright');

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
    console.log('=== Google Images Camera Upload ===\n');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 300
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    try {
        const page = await context.newPage();
        
        // Navigate to Google Images
        console.log('Opening Google Images...');
        await page.goto('https://images.google.com', { waitUntil: 'networkidle' });
        await sleep(2000);
        
        // Take initial screenshot
        await page.screenshot({ path: '/home/freeman/.openclaw/workspace/gengar-project/gimages_initial.png' });
        
        // Look for camera icon
        console.log('Looking for camera icon...');
        
        // Try to find the camera icon by aria-label or src
        const cameraIcon = await page.$('[aria-label*="Search by image"], [aria-label*="camera"], img[src*="camera"], div[jsname]');
        
        if (cameraIcon) {
            console.log('✓ Found camera icon, clicking...');
            await cameraIcon.click();
        } else {
            console.log('Trying to find camera by text...');
            const cameraByText = await page.$('text=Search by image, text=camera');
            if (cameraByText) {
                await cameraByText.click();
            }
        }
        
        await sleep(3000);
        
        // Take screenshot after click
        await page.screenshot({ path: '/home/freeman/.openclaw/workspace/gengar-project/gimages_after_click.png', fullPage: true });
        console.log('✓ Screenshot after click saved');
        
        // Look for file input
        const fileInput = await page.$('input[type="file"]');
        if (fileInput) {
            console.log('✓ Found file input, uploading...');
            await fileInput.setInputFiles('/home/freeman/.openclaw/workspace/gengar-project/pikachu_iter5.png');
            console.log('✓ File uploaded');
        } else {
            console.log('⚠ No file input found');
            // Try clicking on "Upload an image" if visible
            const uploadText = await page.$('text=Upload an image');
            if (uploadText) {
                await uploadText.click();
                await sleep(2000);
                const fileInput2 = await page.$('input[type="file"]');
                if (fileInput2) {
                    await fileInput2.setInputFiles('/home/freeman/.openclaw/workspace/gengar-project/pikachu_iter5.png');
                    console.log('✓ File uploaded after click');
                }
            }
        }
        
        // Wait for results
        console.log('Waiting for analysis...');
        await sleep(10000);
        
        await page.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/gimages_results.png',
            fullPage: true 
        });
        console.log('✓ Results screenshot saved: gimages_results.png');
        
        // Extract results
        const results = await page.evaluate(() => {
            const texts = [];
            document.querySelectorAll('div, span, a').forEach(el => {
                const text = el.textContent?.trim();
                if (text && text.length > 3 && text.length < 100) {
                    texts.push(text);
                }
            });
            return [...new Set(texts)].slice(0, 20);
        });
        
        console.log('\n=== EXTRACTED TEXT ===');
        results.forEach((t, i) => console.log(`${i+1}. ${t}`));
        
        await sleep(15000);
        
    } catch (error) {
        console.error('Error:', error.message);
        const page = await context.newPage();
        await page.screenshot({ path: '/home/freeman/.openclaw/workspace/gengar-project/gimages_error.png' });
    } finally {
        await browser.close();
    }
})();
