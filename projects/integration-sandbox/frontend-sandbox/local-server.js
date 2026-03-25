#!/usr/bin/env node

/**
 * 本地资源服务器 - 所有资源都在本地 cdn/ 目录
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const CDN_DIR = path.join(__dirname, 'cdn');
const HTML_FILE = path.join(__dirname, 'page-local.html');
const DEBUG_FILE = path.join(__dirname, 'debug.html');

function setIframeHeaders(res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('Content-Security-Policy', "frame-ancestors *");
}

function getContentType(p) {
  if (p.endsWith('.js')) return 'application/javascript; charset=utf-8';
  if (p.endsWith('.css')) return 'text/css; charset=utf-8';
  if (p.endsWith('.html')) return 'text/html; charset=utf-8';
  if (p.endsWith('.png')) return 'image/png';
  if (p.endsWith('.jpg')) return 'image/jpeg';
  if (p.endsWith('.gif')) return 'image/gif';
  if (p.endsWith('.svg')) return 'image/svg+xml';
  if (p.endsWith('.ico')) return 'image/x-icon';
  if (p.endsWith('.woff')) return 'font/woff';
  if (p.endsWith('.woff2')) return 'font/woff2';
  return 'application/octet-stream';
}

const server = http.createServer((req, res) => {
  const url = req.url;
  console.log('[Request]', url);
  
  // 诊断页面
  if (url === '/debug' || url === '/debug.html') {
    console.log('[Server] 返回诊断页面');
    setIframeHeaders(res);
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    const html = fs.readFileSync(DEBUG_FILE, 'utf-8');
    res.write(html);
    res.end();
    return;
  }
  
  // React 测试页面
  if (url === '/test-react' || url === '/test-react.html') {
    console.log('[Server] 返回 React 测试页面');
    setIframeHeaders(res);
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    const html = fs.readFileSync(path.join(__dirname, 'test-react.html'), 'utf-8');
    res.write(html);
    res.end();
    return;
  }
  
  // HTML 页面
  if (url === '/' || url === '/index.html' || url === '/category') {
    console.log('[Server] 返回本地 HTML');
    setIframeHeaders(res);
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    
    const html = fs.readFileSync(HTML_FILE, 'utf-8');
    res.write(html);
    res.end();
    return;
  }
  
  // 本地 CDN 资源
  if (url.startsWith('/cdn/')) {
    const localPath = url.replace('/cdn', '');
    const filePath = CDN_DIR + localPath;
    
    console.log('[Local]', filePath);
    
    if (!fs.existsSync(filePath)) {
      res.statusCode = 404;
      res.end('Not Found: ' + localPath);
      return;
    }
    
    setIframeHeaders(res);
    res.setHeader('Content-Type', getContentType(localPath));
    res.setHeader('Cache-Control', 'public, max-age=31536000');
    
    const file = fs.createReadStream(filePath);
    file.pipe(res);
    return;
  }
  
  res.statusCode = 404;
  res.end('Not Found');
});

const PORT = 8107;

server.listen(PORT, () => {
  console.log('\n' + '='.repeat(70));
  console.log('🔌 本地资源服务器已启动');
  console.log('='.repeat(70));
  console.log('\n📍 访问：http://localhost:' + PORT);
  console.log('\n🔍 诊断页面：http://localhost:' + PORT + '/debug');
  console.log('\n✅ 所有资源都在本地 cdn/ 目录');
  console.log('✅ 不依赖外部 CDN');
  console.log('✅ 支持 iframe 嵌入');
  console.log('✅ Mock 拦截器已内置');
  console.log('\n📁 本地资源目录:', CDN_DIR);
  console.log('\n' + '='.repeat(70) + '\n');
});
