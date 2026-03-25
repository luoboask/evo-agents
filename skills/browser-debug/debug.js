#!/usr/bin/env node

/**
 * Browser Debug Tool - 浏览器调试工具
 * 使用 Puppeteer 直接调试页面
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const OUTPUT_DIR = path.join(__dirname, 'output');

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

let browser = null;
let page = null;
let consoleLogs = [];
let networkRequests = [];

async function init(url) {
  console.log('🚀 启动浏览器...');
  
  browser = await puppeteer.launch({
    headless: false,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--window-size=1920,1080'
    ]
  });
  
  console.log('📑 打开页面:', url);
  page = await browser.newPage();
  
  // 设置视口
  await page.setViewport({ width: 1920, height: 1080 });
  
  // 捕获控制台日志
  page.on('console', msg => {
    const type = msg.type();
    const text = msg.text();
    consoleLogs.push({ type, text, time: new Date().toISOString() });
    
    // 实时显示
    const icon = {
      'log': '📝',
      'error': '❌',
      'warn': '⚠️',
      'info': 'ℹ️'
    }[type] || '•';
    
    console.log(`${icon} [${type}] ${text}`);
  });
  
  // 捕获错误
  page.on('pageerror', error => {
    consoleLogs.push({ type: 'pageerror', text: error.message, time: new Date().toISOString() });
    console.log('❌ [Page Error]', error.message);
  });
  
  // 捕获网络请求
  page.on('request', request => {
    const url = request.url();
    const method = request.method();
    networkRequests.push({ url, method, status: 'pending', time: new Date().toISOString() });
  });
  
  page.on('response', response => {
    const url = response.url();
    const status = response.status();
    const req = networkRequests.find(r => r.url === url && r.status === 'pending');
    if (req) req.status = status;
  });
  
  // 导航完成
  page.on('load', () => {
    console.log('✅ 页面加载完成');
  });
  
  console.log('🌐 导航到:', url);
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
  
  console.log('✨ 准备就绪\n');
}

async function screenshot(name = 'screenshot') {
  if (!page) {
    console.log('❌ 请先初始化页面');
    return;
  }
  
  const filename = path.join(OUTPUT_DIR, `${name}-${Date.now()}.png`);
  await page.screenshot({ path: filename, fullPage: true });
  console.log('📸 截图已保存:', filename);
}

async function evalJS(code) {
  if (!page) {
    console.log('❌ 请先初始化页面');
    return;
  }
  
  console.log('🔧 执行 JS:', code);
  try {
    const result = await page.evaluate(code);
    console.log('✅ 结果:', result);
    return result;
  } catch (error) {
    console.log('❌ 错误:', error.message);
  }
}

async function getLogs(filter) {
  if (filter) {
    const filtered = consoleLogs.filter(log => 
      log.text.toLowerCase().includes(filter.toLowerCase())
    );
    console.log(`📝 找到 ${filtered.length} 条匹配 "${filter}" 的日志:`);
    filtered.forEach(log => {
      console.log(`  ${log.type}: ${log.text}`);
    });
    return filtered;
  }
  
  console.log(`📝 共 ${consoleLogs.length} 条日志:`);
  consoleLogs.forEach(log => {
    console.log(`  ${log.type}: ${log.text}`);
  });
  return consoleLogs;
}

async function getRequests(filter) {
  if (filter) {
    const filtered = networkRequests.filter(req => 
      req.url.toLowerCase().includes(filter.toLowerCase())
    );
    console.log(`🌐 找到 ${filtered.length} 个匹配 "${filter}" 的请求:`);
    filtered.forEach(req => {
      console.log(`  [${req.status}] ${req.method} ${req.url}`);
    });
    return filtered;
  }
  
  console.log(`🌐 共 ${networkRequests.length} 个请求:`);
  networkRequests.forEach(req => {
    console.log(`  [${req.status}] ${req.method} ${req.url}`);
  });
  return networkRequests;
}

async function getElement(selector) {
  if (!page) {
    console.log('❌ 请先初始化页面');
    return;
  }
  
  console.log('🔍 查找元素:', selector);
  try {
    const element = await page.$(selector);
    if (!element) {
      console.log('❌ 未找到元素');
      return null;
    }
    
    const info = await page.evaluate(el => {
      return {
        tag: el.tagName,
        id: el.id,
        className: el.className,
        text: el.innerText?.substring(0, 200),
        visible: el.offsetParent !== null,
        width: el.offsetWidth,
        height: el.offsetHeight
      };
    }, element);
    
    console.log('✅ 元素信息:', info);
    return info;
  } catch (error) {
    console.log('❌ 错误:', error.message);
  }
}

async function close() {
  if (browser) {
    console.log('👋 关闭浏览器...');
    await browser.close();
    browser = null;
    page = null;
  }
}

// CLI 命令处理
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
🔧 Browser Debug Tool

用法:
  node debug.js open <url>     - 打开页面
  node debug.js logs [filter]  - 查看日志
  node debug.js screenshot     - 截图
  node debug.js eval <code>    - 执行 JS
  node debug.js requests       - 查看网络请求
  node debug.js element <sel>  - 查看元素
  node debug.js close          - 关闭浏览器

示例:
  node debug.js open http://localhost:3000/category
  node debug.js logs "MTOP Mock"
  node debug.js screenshot
  node debug.js eval "window.__MTOP_MOCK_STATUS__"
  node debug.js element "#mock-debug-panel"
    `);
    return;
  }
  
  try {
    switch (command) {
      case 'open':
        if (!args[1]) {
          console.log('❌ 请提供 URL');
          return;
        }
        await init(args[1]);
        console.log('✅ 页面已打开，保持运行中...\n按 Ctrl+C 退出');
        break;
        
      case 'logs':
        if (!page) await init('about:blank');
        await getLogs(args[1]);
        break;
        
      case 'screenshot':
        if (!page) await init('about:blank');
        await screenshot();
        break;
        
      case 'eval':
        if (!page) await init('about:blank');
        await evalJS(args.slice(1).join(' '));
        break;
        
      case 'requests':
        if (!page) await init('about:blank');
        await getRequests(args[1]);
        break;
        
      case 'element':
        if (!page) await init('about:blank');
        await getElement(args[1]);
        break;
        
      case 'close':
        await close();
        break;
        
      default:
        console.log('❌ 未知命令:', command);
    }
  } catch (error) {
    console.log('❌ 错误:', error.message);
    await close();
  }
}

// 如果直接运行
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { init, screenshot, evalJS, getLogs, getRequests, getElement, close };
