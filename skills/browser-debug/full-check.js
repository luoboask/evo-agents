#!/usr/bin/env node

const puppeteer = require('puppeteer');

(async () => {
  console.log('🔍 完整检查页面...\n');
  
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });
  
  const page = await browser.newPage();
  
  // 捕获所有控制台消息
  const allLogs = [];
  page.on('console', msg => {
    allLogs.push({
      type: msg.type(),
      text: msg.text(),
      args: msg.args()
    });
  });
  
  page.on('pageerror', error => {
    console.log('❌ [Page Error]', error.message);
    allLogs.push({ type: 'pageerror', text: error.message });
  });
  
  page.on('requestfailed', request => {
    console.log('❌ [Request Failed]', request.url(), '-', request.failure()?.errorText);
  });
  
  console.log('🌐 打开页面...\n');
  
  try {
    await page.goto('http://localhost:3000/category', { 
      waitUntil: 'domcontentloaded', 
      timeout: 30000 
    });
    
    console.log('✅ 页面加载完成\n');
    
    // 等待 5 秒让 JS 执行
    console.log('⏳ 等待 5 秒...\n');
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    console.log('📋 所有控制台日志:\n');
    allLogs.forEach((log, i) => {
      console.log(`${i + 1}. [${log.type}] ${log.text}`);
    });
    
    console.log('\n🔍 检查 window 对象...\n');
    
    const windowState = await page.evaluate(() => {
      return {
        hasWindow: !!window,
        hasLib: !!window.lib,
        hasLibMtop: !!window.lib?.mtop,
        hasAES: !!window.AES,
        hasReact: !!window.React,
        hasReactDOM: !!window.ReactDOM,
        documentReadyState: document.readyState,
        bodyInnerHTML: document.body.innerHTML.substring(0, 500)
      };
    });
    
    console.log('  window:', windowState.hasWindow);
    console.log('  window.lib:', windowState.hasLib);
    console.log('  window.lib.mtop:', windowState.hasLibMtop);
    console.log('  window.AES:', windowState.hasAES);
    console.log('  window.React:', windowState.hasReact);
    console.log('  document.readyState:', windowState.documentReadyState);
    console.log('\n  body.innerHTML 前 500 字符:');
    console.log('  ', windowState.bodyInnerHTML);
    
  } catch (error) {
    console.log('❌ 加载失败:', error.message);
  }
  
  await browser.close();
  
  console.log('\n✅ 检查完成\n');
})();
