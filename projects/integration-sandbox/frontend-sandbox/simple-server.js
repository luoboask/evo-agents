#!/usr/bin/env node

const http = require('http');
const https = require('https');
const zlib = require('zlib');
const fs = require('fs');
const path = require('path');

const HTML_FILE = path.join(__dirname, 'page.html');

// 代理资源
function proxy(res, url, base) {
  const fullUrl = base + url;
  console.log('[Proxy]', fullUrl);
  
  https.get(fullUrl, {
    headers: { 'Accept-Encoding': 'gzip', 'Referer': 'https://pages.tao.co/' }
  }, (cdnRes) => {
    const chunks = [];
    cdnRes.on('data', chunk => chunks.push(chunk));
    cdnRes.on('end', () => {
      const buffer = Buffer.concat(chunks);
      const enc = cdnRes.headers['content-encoding'];
      
      if (enc === 'gzip') {
        zlib.gunzip(buffer, (err, dec) => {
          if (err) { res.statusCode = 500; res.end('Error'); return; }
          setIframeHeaders(res);
          res.setHeader('Content-Type', getContentType(url));
          res.write(dec);
          res.end();
        });
      } else {
        setIframeHeaders(res);
        res.setHeader('Content-Type', getContentType(url));
        res.write(buffer);
        res.end();
      }
    });
  }).on('error', (e) => {
    res.statusCode = 500;
    res.end('CDN Error: ' + e.message);
  });
}

// 设置 iframe 允许的 headers
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
  
  if (url === '/' || url === '/index.html' || url === '/category') {
    console.log('[Server] 返回 HTML');
    setIframeHeaders(res);
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    
    const html = fs.readFileSync(HTML_FILE, 'utf-8');
    res.write(html);
    res.end();
    return;
  }
  
  if (url.startsWith('/jp-fe/')) {
    proxy(res, url, 'https://g.alicdn.com');
    return;
  }
  
  if (url.startsWith('/code/') || url.startsWith('/aes/') || url.startsWith('/mtb/')) {
    proxy(res, url, 'https://g.alicdn.com');
    return;
  }
  
  if (url.startsWith('/AWSC/') || url.startsWith('/sd/') || url.startsWith('/secdev/')) {
    proxy(res, url, 'https://g.alicdn.com');
    return;
  }
  
  if (url.startsWith('/??')) {
    proxy(res, url.replace('/??', '??'), 'https://g.alicdn.com/');
    return;
  }
  
  if (url.startsWith('/g/ae-fe/')) {
    proxy(res, url, 'https://assets.alicdn.com');
    return;
  }
  
  if (url.startsWith('/o.alicdn.com/')) {
    proxy(res, url, 'https://');
    return;
  }
  
  res.statusCode = 404;
  res.end('Not Found');
});

const PORT = 8106;

server.listen(PORT, () => {
  console.log('\n' + '='.repeat(70));
  console.log('🔌 Server 已启动 (支持 iframe 嵌入)');
  console.log('='.repeat(70));
  console.log('\n📍 访问：http://localhost:' + PORT);
  console.log('\n✅ 从 page.html 读取 HTML');
  console.log('✅ 代理所有 CDN 资源');
  console.log('✅ 支持 iframe 嵌入 (CORS + X-Frame-Options)');
  console.log('\n📋 Iframe 嵌入示例:');
  console.log('   <iframe src="http://localhost:' + PORT + '" width="100%" height="600"></iframe>');
  console.log('\n' + '='.repeat(70) + '\n');
});
