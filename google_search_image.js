#!/usr/bin/env node
/**
 * Upload image to Google Search and get AI analysis
 * Uses Google Lens integration in search
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
    const imagePath = '/home/freeman/.openclaw/workspace/gengar-project/render_fixed.png';
    
    console.log('Starting Google Search Image Analysis...');
    console.log('Image:', imagePath);
    
    // Verify image exists
    if (!fs.existsSync(imagePath)) {
        console.error('Image not found:', imagePath);
        process.exit(1);
    }
    
    const browser = await chromium.launch({
        headless: false,
        slowMo: 100  // Slow down for visibility
    });
    
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1920, height: 1080 });
    
    try {
        // Go to Google
        console.log('Opening Google...');
        await page.goto('https://www.google.com', { waitUntil: 'networkidle' });
        await page.waitForTimeout(2000);
        
        // Find and click the camera icon for image search
        console.log('Looking for camera icon...');
        
        // Try multiple selectors for the camera icon
        const cameraSelectors = [
            '[aria-label*="Search by image"]',
            '[aria-label*="camera"]',
            'div[role="button"][jsaction*="camera"]',
            '[data-ved*="camera"]',
            'div.TD8esb',  // Google's camera icon class
            'svg path[d*="camera"]',
            'form button svg'  // Generic camera icon
        ];
        
        let cameraClicked = false;
        for (const selector of cameraSelectors) {
            try {
                const element = await page.$(selector);
                if (element) {
                    await element.click();
                    console.log('Clicked camera icon using selector:', selector);
                    cameraClicked = true;
                    break;
                }
            } catch (e) {
                // Continue to next selector
            }
        }
        
        if (!cameraClicked) {
            // Alternative: Try clicking by position (camera is usually right side of search bar)
            console.log('Trying position-based click...');
            await page.click('input[name="q"]');  // Focus search
            await page.waitForTimeout(500);
            
            // Try clicking at coordinates where camera usually is
            const box = await page.$eval('input[name="q"]', el => {
                const rect = el.getBoundingClientRect();
                return { x: rect.right - 50, y: rect.top + rect.height / 2 };
            }).catch(() => null);
            
            if (box) {
                await page.mouse.click(box.x, box.y);
                cameraClicked = true;
            }
        }
        
        if (!cameraClicked) {
            console.error('Could not find camera icon');
            console.log('Taking screenshot for debugging...');
            await page.screenshot({ path: '/home/freeman/.openclaw/workspace/gengar-project/debug_no_camera.png' });
            await browser.close();
            return;
        }
        
        await page.waitForTimeout(2000);
        
        // Upload the image
        console.log('Uploading image...');
        const fileInput = await page.$('input[type="file"][accept*="image"]');
        if (fileInput) {
            await fileInput.setInputFiles(imagePath);
            console.log('Image uploaded successfully');
        } else {
            console.error('File input not found');
            await browser.close();
            return;
        }
        
        // Wait for Google to analyze
        console.log('Waiting for analysis...');
        await page.waitForTimeout(15000);
        
        // Take screenshot of results
        await page.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/google_image_analysis.png',
            fullPage: true 
        });
        console.log('Screenshot saved to google_image_analysis.png');
        
        // Try to extract text from the page
        console.log('Extracting analysis text...');
        const text = await page.evaluate(() => {
            // Look for analysis results, similar images descriptions, etc.
            const selectors = [
                '[data-attrid*="description"]',
                '.g-blk',
                '[jsname="Cpkphb"]',
                'h2',
                '.card-section',
                '[data-ved] div'
            ];
            
            let results = [];
            for (const sel of selectors) {
                const elements = document.querySelectorAll(sel);
                elements.forEach(el => {
                    if (el.textContent && el.textContent.trim().length > 10) {
                        results.push(el.textContent.trim());
                    }
                });
            }
            return results.join('\n---\n');
        });
        
        if (text) {
            console.log('\n=== GOOGLE ANALYSIS TEXT ===');
            console.log(text.substring(0, 2000));
            console.log('=== END ANALYSIS ===\n');
            
            // Save to file
            fs.writeFileSync(
                '/home/freeman/.openclaw/workspace/gengar-project/google_analysis_text.txt',
                text
            );
        }
        
        // Keep browser open for manual review
        console.log('Browser will remain open for 60 seconds...');
        await page.waitForTimeout(60000);
        
    } catch (error) {
        console.error('Error:', error.message);
        await page.screenshot({ path: '/home/freeman/.openclaw/workspace/gengar-project/error_screenshot.png' });
    } finally {
        await browser.close();
    }
})();
