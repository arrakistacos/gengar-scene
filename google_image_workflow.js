#!/usr/bin/env node
/**
 * Complete workflow: Upload image to Google, get analysis, ask follow-up questions
 */

const { chromium } = require('playwright');
const fs = require('fs');

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
    console.log('=== Google Image Analysis Workflow ===\n');
    
    const browser = await chromium.launch({ 
        headless: false,
        slowMo: 300
    });
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    try {
        // Step 1: Go to Google Images
        console.log('Step 1: Opening Google Images...');
        const page = await context.newPage();
        await page.goto('https://www.google.com/imghp');
        await page.waitForLoadState('networkidle');
        await sleep(3000);
        
        // Step 2: Click camera icon
        console.log('Step 2: Finding camera icon...');
        
        // The camera icon is usually the last icon in the search bar
        // Try to find it by looking at all buttons in the search area
        const searchArea = await page.$('form[role="search"]');
        if (!searchArea) {
            console.log('Search form not found, trying alternative...');
        }
        
        // Try clicking by looking for camera-related elements
        const buttons = await page.$$('button, div[role="button"]');
        console.log(`Found ${buttons.length} clickable elements`);
        
        // Look for camera icon by examining inner HTML
        for (const button of buttons) {
            const html = await button.innerHTML().catch(() => '');
            if (html.includes('camera') || html.includes('M12.75')) {
                console.log('Found camera button!');
                await button.click();
                break;
            }
        }
        
        await sleep(3000);
        
        // Step 3: Upload the rendered model
        console.log('Step 3: Uploading rendered model...');
        const imagePath = '/home/freeman/.openclaw/workspace/gengar-project/render_fixed.png';
        
        // Find file input
        const fileInput = await page.$('input[type="file"]');
        if (fileInput) {
            await fileInput.setInputFiles(imagePath);
            console.log('✓ Image uploaded');
        } else {
            console.log('✗ File input not found, looking for alternatives...');
            // Maybe it's a drag-and-drop area
            const dropArea = await page.$('[data-text="Drag an image here"]');
            if (dropArea) {
                console.log('Found drop area, but cannot automate drag from local file');
            }
        }
        
        // Step 4: Wait for analysis
        console.log('Step 4: Waiting for Google analysis (20s)...');
        await sleep(20000);
        
        // Screenshot the results
        await page.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/step4_analysis.png',
            fullPage: true
        });
        console.log('✓ Analysis screenshot saved');
        
        // Step 5: Extract what Google found
        console.log('Step 5: Extracting analysis results...');
        const analysisText = await page.evaluate(() => {
            // Look for various result sections
            const results = [];
            
            // Try to find "Visually similar" or "Best guess" sections
            const sections = document.querySelectorAll('div, h2, h3');
            sections.forEach(el => {
                const text = el.textContent?.trim();
                if (text && text.length > 5 && text.length < 200) {
                    if (text.includes('guess') || text.includes('similar') || 
                        text.includes('result') || text.includes('Pokémon') ||
                        text.includes('character') || text.includes('cartoon')) {
                        results.push(text);
                    }
                }
            });
            
            return [...new Set(results)]; // Remove duplicates
        });
        
        console.log('\n=== GOOGLE ANALYSIS RESULTS ===');
        analysisText.forEach((text, i) => {
            console.log(`${i + 1}. ${text}`);
        });
        console.log('=================================\n');
        
        // Save results
        fs.writeFileSync(
            '/home/freeman/.openclaw/workspace/gengar-project/google_analysis_results.txt',
            analysisText.join('\n')
        );
        
        // Step 6: Open new tab to ask follow-up question
        console.log('Step 6: Opening Google Search to ask follow-up question...');
        const searchPage = await context.newPage();
        await searchPage.goto('https://google.com');
        await sleep(2000);
        
        // Ask a question based on what we found
        const question = analysisText.length > 0 
            ? `What Pokemon character is this? ${analysisText[0]}`
            : 'What Pokemon character is a purple ghost with big ears?';
        
        console.log(`Asking: "${question}"`);
        await searchPage.fill('textarea[name="q"]', question);
        await searchPage.press('textarea[name="q"]', 'Enter');
        
        await sleep(5000);
        
        await searchPage.screenshot({ 
            path: '/home/freeman/.openclaw/workspace/gengar-project/step6_answer.png',
            fullPage: true
        });
        console.log('✓ Answer screenshot saved');
        
        // Step 7: Extract answer
        const answerText = await searchPage.evaluate(() => {
            const results = [];
            // Look for featured snippets, AI overview, or top results
            const selectors = [
                '[data-attrid*="description"]',
                '.VwiC3b',
                '.hgKElc',
                '[data-ved] div span',
                'h3'
            ];
            
            selectors.forEach(sel => {
                document.querySelectorAll(sel).forEach(el => {
                    const text = el.textContent?.trim();
                    if (text && text.length > 20 && text.length < 500) {
                        results.push(text);
                    }
                });
            });
            
            return [...new Set(results)].slice(0, 5);
        });
        
        console.log('\n=== GOOGLE ANSWER ===');
        answerText.forEach((text, i) => {
            console.log(`${i + 1}. ${text}`);
        });
        console.log('=====================\n');
        
        fs.writeFileSync(
            '/home/freeman/.openclaw/workspace/gengar-project/google_answer_results.txt',
            answerText.join('\n')
        );
        
        console.log('✓ Workflow complete! Check:');
        console.log('  - step4_analysis.png (Google Lens results)');
        console.log('  - step6_answer.png (Google Search answer)');
        console.log('  - google_analysis_results.txt (extracted text)');
        console.log('  - google_answer_results.txt (answer text)');
        
        // Keep browser open for review
        console.log('\nBrowser will stay open for 30 seconds...');
        await sleep(30000);
        
    } catch (error) {
        console.error('Error:', error.message);
        console.error(error.stack);
    } finally {
        await browser.close();
    }
})();
