#!/usr/bin/env node

/**
 * Frontend Proxy Server - 原封不动代理
 * 
 * 从 https://pages.tao.co/mapp/jp-fe/jp-new-homepage-category-page/category 获取 HTML
 * 直接返回，不修改任何内容
 */

const http = require('http');
const https = require('https');
const zlib = require('zlib');

const TARGET = 'https://pages.tao.co/mapp/jp-fe/jp-new-homepage-category-page/category';

// 获取 HTML（不修改）
function fetchHTML(callback) {
  https.get(TARGET, {
    headers: {
      'Accept-Encoding': 'gzip',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
      'Referer': 'https://pages.tao.co/'
    }
  }, (res) => {
    if (res.statusCode !== 200) {
      callback(new Error('CDN: ' + res.statusCode), null);
      return;
    }
    
    const chunks = [];
    res.on('data', chunk => chunks.push(chunk));
    res.on('end', () => {
      const buffer = Buffer.concat(chunks);
      const enc = res.headers['content-encoding'];
      
      const html = enc === 'gzip' ? zlib.gunzipSync(buffer).toString('utf-8') : buffer.toString('utf-8');
      callback(null, html);
    });
  }).on('error', callback).end();
}

// 代理资源
function proxy(res, url, base) {
  https.get(base + url, {
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
          res.setHeader('Content-Type', getContentType(url));
          res.setHeader('Access-Control-Allow-Origin', '*');
          res.write(dec);
          res.end();
        });
      } else {
        res.setHeader('Content-Type', getContentType(url));
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.write(buffer);
        res.end();
      }
    });
  }).on('error', (e) => { res.statusCode = 500; res.end('Error: ' + e.message); });
}

function getContentType(path) {
  if (path.endsWith('.js')) return 'application/javascript; charset=utf-8';
  if (path.endsWith('.css')) return 'text/css; charset=utf-8';
  if (path.endsWith('.png')) return 'image/png';
  if (path.endsWith('.jpg')) return 'image/jpeg';
  if (path.endsWith('.svg')) return 'image/svg+xml';
  if (path.endsWith('.ico')) return 'image/x-icon';
  if (path.endsWith('.woff')) return 'font/woff';
  if (path.endsWith('.woff2')) return 'font/woff2';
  return 'application/octet-stream';
}

http.createServer((req, res) => {
  const url = req.url;
  console.log('[Request]', url);
  
  // HTML 页面 - 直接返回原始内容
  if (url === '/' || url === '/index.html' || url === '/category') {
    fetchHTML((err, html) => {
      if (err) {
        res.statusCode = 503;
        res.setHeader('Content-Type', 'text/html;charset=UTF-8');
        res.end('<h1>Error</h1><p>' + err.message + '</p>');
        return;
      }
      res.setHeader('Content-Type', 'text/html;charset=UTF-8');
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.write(html);
      res.end();
    });
    return;
  }
  
  // 代理资源
  if (url.startsWith('/jp-fe/')) {
    proxy(res, url, 'https://g.alicdn.com');
    return;
  }
  
  if (url.startsWith('/code/') || url.startsWith('/aes/') || url.startsWith('/mtb/')) {
    proxy(res, url, 'https://g.alicdn.com');
    return;
  }
  
  if (url.startsWith('/g/ae-fe/')) {
    proxy(res, url, 'https://assets.alicdn.com');
    return;
  }
  
  if (url.startsWith('/??')) {
    proxy(res, url.replace('/??', '??'), 'https://g.alicdn.com/');
    return;
  }
  
  res.statusCode = 404;
  res.end('Not Found');
}).listen(8104, () => {
  console.log('\n✅ Server running at http://localhost:8104');
  console.log('📍 Target:', TARGET);
  console.log('✨ 原封不动返回 HTML，不修改资源路径');
  console.log('');
});
