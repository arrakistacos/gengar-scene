#!/usr/bin/env node
/**
 * Iteration 1: Upload reference image to Google and ask for feature description
 */

const { chromium } = require('playwright');

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
    console.log('=== ITERATION 1: Analyzing Reference Image ===\n');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 300
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    try {
        // Open Google Images
        console.log('Opening Google Images...');
        const page = await context.newPage();
        await page.goto('https://images.google.com');
        await sleep(3000);
        
        // Click camera icon for image search
        console.log('Clicking camera icon...');
        await page.click('div[aria-label*="Search by image"], [aria-label*="camera"]');
        await sleep(2000);
        
        // Upload reference image
        console.log('Uploading Pikachu reference...');
        const fileInput = await page.$('input[type="file"]');
        await fileInput.setInputFiles('/home/freeman/.openclaw/workspace/gengar-project/reference_pikachu.jpg');
        console.log('✓ Reference uploaded');
        
        // Wait for analysis
        console.log('Waiting for analysis...');
        await sleep(15000);
        
        // Take screenshot
        await page.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/iter1_ref_analysis.png',
            fullPage: true 
        });
        
        // Extract text
        const analysis = await page.evaluate(() => {
            const results = [];
            document.querySelectorAll('div, h2, h3, span').forEach(el => {
                const text = el.textContent?.trim();
                if (text && text.length > 3 && text.length < 200) {
                    if (text.includes('Pikachu') || text.includes('pokemon') || text.includes('character') ||
                        text.includes('yellow') || text.includes('mouse') || text.includes('cartoon') ||
                        text.includes(' Nintendo') || text.includes('anime')) {
                        results.push(text);
                    }
                }
            });
            return [...new Set(results)];
        });
        
        console.log('\n=== GOOGLE ANALYSIS OF REFERENCE ===');
        analysis.forEach((text, i) => console.log(`${i+1}. ${text}`));
        console.log('====================================\n');
        
        // Save to file
        require('fs').writeFileSync(
            '/home/freeman/.openclaw/workspace/gengar-project/iter1_ref_features.txt',
            analysis.join('\n')
        );
        
        // Now open regular Google search to ask specific questions
        console.log('Opening Google Search to ask detailed questions...');
        const searchPage = await context.newPage();
        await searchPage.goto('https://google.com');
        await sleep(2000);
        
        // Ask about Pikachu features
        const question = 'Describe Pikachu physical features: body shape, ears, tail, face, colors';
        console.log(`Asking: "${question}"`);
        await searchPage.fill('textarea[name="q"]', question);
        await searchPage.press('textarea[name="q"]', 'Enter');
        await sleep(5000);
        
        await searchPage.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/iter1_feature_answer.png',
            fullPage: true 
        });
        
        // Extract answer
        const answer = await searchPage.evaluate(() => {
            const texts = [];
            document.querySelectorAll('[data-attrid*="description"], .VwiC3b, .hgKElc').forEach(el => {
                const t = el.textContent?.trim();
                if (t && t.length > 30 && t.length < 1000) texts.push(t);
            });
            return texts.slice(0, 3);
        });
        
        console.log('\n=== PIKACHU FEATURE DESCRIPTION ===');
        answer.forEach((text, i) => console.log(`${i+1}. ${text.substring(0, 200)}...`));
        console.log('====================================\n');
        
        require('fs').writeFileSync(
            '/home/freeman/.openclaw/workspace/gengar-project/iter1_features.txt',
            answer.join('\n')
        );
        
        console.log('✓ Iteration 1 complete!');
        console.log('  - iter1_ref_analysis.png');
        console.log('  - iter1_feature_answer.png');
        console.log('  - iter1_features.txt');
        
        await sleep(10000);
        
    } catch (error) {
        console.error('Error:', error);
    } finally {
        await browser.close();
    }
})();
