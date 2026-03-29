#!/usr/bin/env node
/**
 * Fixed Google Lens automation with better error handling
 */

const { chromium } = require('playwright');

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
    console.log('=== Starting Google Lens Analysis ===\n');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 500
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    try {
        const page = await context.newPage();
        
        // Navigate directly to Google Lens
        console.log('Opening Google Lens...');
        await page.goto('https://lens.google.com', { waitUntil: 'networkidle' });
        await sleep(3000);
        
        // Wait for the page to fully load
        console.log('Waiting for Lens to load...');
        await page.waitForSelector('text=Search for images', { timeout: 30000 });
        console.log('✓ Google Lens loaded');
        
        // Look for upload button - try multiple selectors
        console.log('Looking for upload button...');
        const uploadSelectors = [
            'button:has-text("Upload")',
            'button:has-text("Upload an image")',
            '[aria-label*="Upload"]',
            'input[type="file"]',
            'div[role="button"]',
            'button'
        ];
        
        let uploadButton = null;
        for (const selector of uploadSelectors) {
            try {
                uploadButton = await page.$(selector);
                if (uploadButton) {
                    console.log(`✓ Found upload element: ${selector}`);
                    break;
                }
            } catch (e) {}
        }
        
        // Click the upload button
        if (uploadButton) {
            console.log('Clicking upload button...');
            await uploadButton.click();
            await sleep(2000);
        }
        
        // Look for file input
        console.log('Looking for file input...');
        const fileInput = await page.$('input[type="file"]');
        
        if (fileInput) {
            console.log('✓ Found file input, uploading image...');
            await fileInput.setInputFiles('/home/freeman/.openclaw/workspace/gengar-project/pikachu_iter5.png');
            console.log('✓ Image uploaded');
        } else {
            console.log('⚠ No file input found, trying alternative approach...');
            // Try pressing the upload key
            await page.keyboard.press('Tab');
            await page.keyboard.press('Tab');
            await page.keyboard.press('Tab');
            await page.keyboard.press('Enter');
            await sleep(1000);
            
            // Try again
            const fileInputRetry = await page.$('input[type="file"]');
            if (fileInputRetry) {
                await fileInputRetry.setInputFiles('/home/freeman/.openclaw/workspace/gengar-project/pikachu_iter5.png');
                console.log('✓ Image uploaded on retry');
            }
        }
        
        // Wait for analysis
        console.log('Waiting for analysis (15s)...');
        await sleep(15000);
        
        // Take screenshot
        console.log('Taking screenshot...');
        await page.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/lens_result_fixed.png',
            fullPage: true 
        });
        console.log('✓ Screenshot saved: lens_result_fixed.png');
        
        // Extract text results
        console.log('Extracting results...');
        const results = await page.evaluate(() => {
            const texts = [];
            // Look for common result patterns
            document.querySelectorAll('div, span, h2, h3, a').forEach(el => {
                const text = el.textContent?.trim();
                if (text && text.length > 2 && text.length < 100) {
                    if (text.toLowerCase().includes('pikachu') || 
                        text.toLowerCase().includes('pokemon') ||
                        text.toLowerCase().includes('nintendo') ||
                        text.toLowerCase().includes('character') ||
                        text.toLowerCase().includes('yellow') ||
                        text.toLowerCase().includes('cartoon') ||
                        text.toLowerCase().includes('toy') ||
                        text.toLowerCase().includes('figure')) {
                        texts.push(text);
                    }
                }
            });
            return [...new Set(texts)];
        });
        
        console.log('\n=== GOOGLE LENS RESULTS ===');
        if (results.length > 0) {
            results.forEach((text, i) => console.log(`${i+1}. ${text}`));
        } else {
            console.log('No relevant results found in page text');
            console.log('Check the screenshot: lens_result_fixed.png');
        }
        console.log('===========================\n');
        
        // Save results
        const fs = require('fs');
        fs.writeFileSync(
            '/home/freeman/.openclaw/workspace/gengar-project/lens_results_fixed.txt',
            results.join('\n') || 'No text results extracted'
        );
        
        console.log('✓ Analysis complete!');
        await sleep(30000); // Keep browser open for review
        
    } catch (error) {
        console.error('Error:', error.message);
        console.log('\nTaking error screenshot...');
        try {
            const page = await context.newPage();
            await page.screenshot({ 
                path: '/home/freeman/.openclaw/workspace/gengar-project/lens_error.png',
                fullPage: true 
            });
            console.log('✓ Error screenshot saved: lens_error.png');
        } catch (e) {}
    } finally {
        await browser.close();
    }
})();
