#!/usr/bin/env node

const puppeteer = require('puppeteer');

(async () => {
  console.log('🔍 启动浏览器检查页面...\n');
  
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  // 捕获所有控制台消息
  const logs = [];
  page.on('console', msg => {
    logs.push({
      type: msg.type(),
      text: msg.text()
    });
    console.log(`[${msg.type()}] ${msg.text()}`);
  });
  
  page.on('pageerror', error => {
    console.log('❌ [Page Error]', error.message);
    logs.push({ type: 'error', text: error.message });
  });
  
  console.log('🌐 打开页面: http://localhost:3000/category\n');
  await page.goto('http://localhost:3000/category', { 
    waitUntil: 'networkidle0', 
    timeout: 60000 
  });
  
  console.log('\n📊 页面信息:');
  const title = await page.title();
  console.log('  标题:', title);
  
  const url = page.url();
  console.log('  URL:', url);
  
  console.log('\n🔍 检查关键元素:');
  
  const elements = {
    '#mock-debug-panel': 'Mock 调试面板',
    '#ice-container': 'ICE 容器',
    '#catePage': '分类页面',
    '.recommendWrapper--yiTw9Imr': '推荐容器'
  };
  
  for (const [selector, name] of Object.entries(elements)) {
    try {
      const el = await page.$(selector);
      if (el) {
        const visible = await page.evaluate(el => {
          const style = window.getComputedStyle(el);
          return style.display !== 'none' && style.visibility !== 'hidden' && el.offsetWidth > 0;
        }, el);
        console.log(`  ✅ ${name} (${selector}) - ${visible ? '可见' : '隐藏'}`);
      } else {
        console.log(`  ❌ ${name} (${selector}) - 不存在`);
      }
    } catch (error) {
      console.log(`  ❌ ${name} (${selector}) - 错误：${error.message}`);
    }
  }
  
  console.log('\n💉 执行诊断脚本...');
  
  const debugInfo = await page.evaluate(() => {
    return {
      hasWindowLib: !!window.lib,
      hasWindowLibMtop: !!window.lib?.mtop,
      hasMockStatus: !!window.__MTOP_MOCK_STATUS__,
      mockStatus: window.__MTOP_MOCK_STATUS__ || null,
      hasDataSource: !!(window.debugDataSource || window.debugCardGroups)
    };
  });
  
  console.log('\n📋 诊断结果:');
  console.log('  window.lib:', debugInfo.hasWindowLib);
  console.log('  window.lib.mtop:', debugInfo.hasWindowLibMtop);
  console.log('  window.__MTOP_MOCK_STATUS__:', debugInfo.hasMockStatus);
  if (debugInfo.mockStatus) {
    console.log('    - enabled:', debugInfo.mockStatus.enabled);
    console.log('    - interceptedCount:', debugInfo.mockStatus.interceptedCount);
    console.log('    - mockedAPIs:', debugInfo.mockStatus.mockedAPIs?.length);
  }
  
  console.log('\n📝 过滤后的日志:');
  const importantLogs = logs.filter(log => 
    log.text.includes('MTOP') || 
    log.text.includes('Mock') ||
    log.text.includes('Category') ||
    log.type === 'error'
  );
  
  importantLogs.forEach(log => {
    console.log(`  [${log.type}] ${log.text}`);
  });
  
  console.log('\n📸 截图...');
  const screenshotPath = '/Users/dhr/.openclaw/workspace/skills/browser-debug/output/debug-' + Date.now() + '.png';
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log('  已保存:', screenshotPath);
  
  await browser.close();
  
  console.log('\n✅ 检查完成\n');
})();
