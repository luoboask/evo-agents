#!/usr/bin/env node

/**
 * Browser Test Tool - 浏览器测试工具
 * 使用 Puppeteer 访问网页、截图、获取日志
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.join(__dirname, 'output');

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function testPage(url, options = {}) {
  console.log('🚀 启动浏览器...');
  
  const browser = await puppeteer.launch({
    headless: options.headless !== false,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--window-size=1920,1080'
    ]
  });
  
  console.log('📑 打开页面:', url);
  const page = await browser.newPage();
  
  // 设置视口
  await page.setViewport({ width: 1920, height: 1080 });
  
  // 收集控制台日志
  const logs = [];
  page.on('console', msg => {
    const log = {
      type: msg.type(),
      text: msg.text(),
      time: new Date().toISOString()
    };
    logs.push(log);
    
    // 实时显示
    const icon = {
      'log': '📝',
      'error': '❌',
      'warn': '⚠️',
      'info': 'ℹ️'
    }[log.type] || '•';
    
    console.log(`${icon} [${log.type}] ${log.text}`);
  });
  
  // 捕获错误
  page.on('pageerror', error => {
    logs.push({
      type: 'pageerror',
      text: error.message,
      time: new Date().toISOString()
    });
    console.log('❌ [Page Error]', error.message);
  });
  
  // 捕获请求
  page.on('request', request => {
    const url = request.url();
    if (url.includes('mtop') || url.includes('localhost:8090')) {
      console.log('🌐 [Request]', request.method(), url);
    }
  });
  
  // 捕获响应
  page.on('response', response => {
    const url = response.url();
    if (url.includes('mtop') || url.includes('localhost:8090')) {
      console.log('✅ [Response]', response.status(), url);
    }
  });
  
  console.log('🌐 导航到:', url);
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
  
  console.log('✅ 页面加载完成');
  
  // 等待一段时间让 JS 执行
  if (options.wait) {
    console.log(`⏳ 等待 ${options.wait}ms...`);
    await new Promise(resolve => setTimeout(resolve, options.wait));
  }
  
  // 截图
  if (options.screenshot) {
    const screenshotPath = path.join(OUTPUT_DIR, `screenshot-${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log('📸 截图已保存:', screenshotPath);
  }
  
  // 执行 JavaScript
  let jsResult = null;
  if (options.eval) {
    console.log('🔧 执行 JS:', options.eval);
    jsResult = await page.evaluate(options.eval);
    console.log('✅ JS 结果:', jsResult);
  }
  
  // 获取元素
  let elementContent = null;
  if (options.element) {
    console.log('🔍 获取元素:', options.element);
    elementContent = await page.$eval(options.element, el => el.innerHTML).catch(() => null);
    console.log('✅ 元素内容:', elementContent);
  }
  
  // 保存日志
  const logPath = path.join(OUTPUT_DIR, `logs-${Date.now()}.json`);
  fs.writeFileSync(logPath, JSON.stringify(logs, null, 2));
  console.log('📝 日志已保存:', logPath);
  
  // 摘要
  console.log('\n📊 日志摘要:');
  console.log('  总日志数:', logs.length);
  console.log('  错误数:', logs.filter(l => l.type === 'error' || l.type === 'pageerror').length);
  console.log('  警告数:', logs.filter(l => l.type === 'warn').length);
  
  const mtopLogs = logs.filter(l => l.text.includes('MTOP') || l.text.includes('mtop'));
  console.log('  MTOP 相关:', mtopLogs.length);
  
  if (mtopLogs.length > 0) {
    console.log('\n🔌 MTOP 日志:');
    mtopLogs.forEach(log => {
      console.log(`  [${log.type}] ${log.text}`);
    });
  }
  
  await browser.close();
  console.log('\n👋 浏览器已关闭');
  
  return { logs, jsResult, elementContent };
}

// CLI 命令处理
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const url = args[1];
  
  if (!command || !url) {
    console.log(`
🔧 Browser Test Tool

用法:
  node test.js open <url> [--screenshot] [--wait=5000]  # 打开页面
  node test.js logs <url>                               # 获取日志
  node test.js eval <url> "<js code>"                   # 执行 JS
  node test.js element <url> "<selector>"               # 获取元素

选项:
  --screenshot    保存截图
  --wait=N        等待 N 毫秒
  --headless      无头模式 (默认开启)

示例:
  node test.js open http://localhost:3000/category --screenshot --wait=5000
  node test.js eval http://localhost:3000/category "document.title"
  node test.js element http://localhost:3000/category "#mock-panel"
    `);
    return;
  }
  
  const options = {
    screenshot: args.includes('--screenshot'),
    wait: parseInt(args.find(a => a.startsWith('--wait='))?.split('=')[1] || '0'),
    eval: args.find(a => !a.startsWith('--') && !a.startsWith('http')),
    element: args.find(a => a.startsWith('#') || a.startsWith('.')),
    headless: !args.includes('--no-headless')
  };
  
  try {
    await testPage(url, options);
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { testPage };
