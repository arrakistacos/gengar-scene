#!/usr/bin/env node
/**
 * Robust Google Images reverse search
 */

const { chromium } = require('playwright');

(async () => {
    console.log('=== Google Images Reverse Search ===\n');
    
    try {
        const browser = await chromium.launch({ 
            headless: false,
            slowMo: 800
        });
        
        const context = await browser.newContext({
            viewport: { width: 1920, height: 1080 }
        });
        
        const page = await context.newPage();
        
        // Method 1: Try direct URL for reverse image search
        console.log('Opening Google Images...');
        await page.goto('https://images.google.com');
        await page.waitForTimeout(2000);
        
        // Screenshot initial state
        await page.screenshot({ path: '/home/freeman/.openclaw/workspace/gengar-project/gimages_initial.png' });
        
        // Look for camera icon by SVG path or position
        console.log('Looking for camera icon...');
        
        // Try different selectors for the camera icon
        const selectors = [
            'svg[focusable="false"]',
            'div[jsaction*="mousedown"][jsaction*="click"]',
            'div[role="button"][jsaction*="sf"]',
            'div[aria-label*="camera" i]',
            'div[aria-label*="Search by image" i]',
        ];
        
        let found = false;
        for (const selector of selectors) {
            try {
                const elements = await page.$$(selector);
                console.log(`Found ${elements.length} elements for: ${selector}`);
                
                for (const el of elements) {
                    const ariaLabel = await el.getAttribute('aria-label');
                    const title = await el.getAttribute('title');
                    console.log(`  Element: aria-label="${ariaLabel}", title="${title}"`);
                    
                    if ((ariaLabel && ariaLabel.toLowerCase().includes('camera')) ||
                        (ariaLabel && ariaLabel.toLowerCase().includes('search by image'))) {
                        console.log('✓ Found camera icon!');
                        await el.click({ force: true });
                        found = true;
                        break;
                    }
                }
                if (found) break;
            } catch (e) {
                console.log(`  Error with selector ${selector}: ${e.message}`);
            }
        }
        
        if (!found) {
            console.log('⚠ Camera icon not found, trying position-based click...');
            // Try clicking at position where camera icon usually is
            // It's typically in the search bar, right side
            await page.mouse.click(900, 200); // Approximate position
        }
        
        await page.waitForTimeout(3000);
        
        // Screenshot after click
        await page.screenshot({ path: '/home/freeman/.openclaw/workspace/gengar-project/gimages_after_click.png' });
        console.log('✓ Screenshot after click saved');
        
        // Look for upload dialog
        console.log('Looking for upload dialog...');
        
        // Try to find "Paste image URL" or "Upload an image" tabs
        const tabSelectors = [
            'text=Upload an image',
            'text=Paste image URL',
            'div[role="tab"]',
            'div[jsname*="tab"]',
        ];
        
        let uploadTabFound = false;
        for (const sel of tabSelectors) {
            try {
                const tab = await page.$(sel);
                if (tab) {
                    const text = await tab.textContent();
                    console.log(`Found tab: "${text}"`);
                    if (text && text.toLowerCase().includes('upload')) {
                        await tab.click();
                        uploadTabFound = true;
                        break;
                    }
                }
            } catch (e) {}
        }
        
        await page.waitForTimeout(2000);
        
        // Look for file input
        console.log('Looking for file input...');
        const fileInput = await page.$('input[type="file"]');
        
        if (fileInput) {
            console.log('✓ Found file input!');
            await fileInput.setInputFiles('/home/freeman/.openclaw/workspace/gengar-project/pikachu_iter5.png');
            console.log('✓ Image uploaded');
            await page.waitForTimeout(10000);
            
            await page.screenshot({ path: '/home/freeman/.openclaw/workspace/gengar-project/gimages_results.png' });
            console.log('✓ Results saved: gimages_results.png');
            
            // Try to extract results
            const results = await page.evaluate(() => {
                const texts = [];
                document.querySelectorAll('div, span, a, h3').forEach(el => {
                    const text = el.textContent?.trim();
                    if (text && text.length > 0 && text.length < 100) {
                        texts.push(text);
                    }
                });
                return [...new Set(texts)].slice(0, 20);
            });
            
            console.log('\n=== Results ===');
            results.forEach((t, i) => console.log(`${i+1}. ${t}`));
        } else {
            console.log('⚠ File input not found. Check screenshot.');
        }
        
        await browser.close();
        console.log('\nDone!');
        
    } catch (error) {
        console.error('Error:', error.message);
    }
})();
