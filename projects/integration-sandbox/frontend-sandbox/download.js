#!/usr/bin/env node

/**
 * 下载所有 CDN 资源到本地
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const BASE_DIR = path.join(__dirname, 'cdn');
const CDN_BASE = 'https://g.alicdn.com';

// 从 HTML 中提取的资源列表
const RESOURCES = [
  // CSS
  { url: '/jp-fe/jp-new-homepage-category-page/0.0.41/css/main.css', path: '/jp-fe/jp-new-homepage-category-page/0.0.41/css/main.css' },
  { url: '/jp-fe/jp-new-homepage-category-page/0.0.41/css/962.css', path: '/jp-fe/jp-new-homepage-category-page/0.0.41/css/962.css' },
  { url: '/jp-fe/jp-new-homepage-category-page/0.0.41/css/p_category.css', path: '/jp-fe/jp-new-homepage-category-page/0.0.41/css/p_category.css' },
  { url: '/g/ae-fe/cosmos/0.0.254/pc/index.css', path: '/g/ae-fe/cosmos/0.0.254/pc/index.css' },
  
  // JS - 组合 URL
  { url: '/??code/lib/react/18.3.1/umd/react.production.min.js,code/lib/react-dom/18.3.1/umd/react-dom.production.min.js,aes/tracker/3.3.9/index.js,mtb/lib-mtop/2.7.2/mtop.js,mtb/lib-windvane/3.0.7/windvane.js,aes/tracker-plugin-pv/3.0.6/index.js,aes/tracker-plugin-event/3.0.0/index.js,aes/tracker-plugin-jserror/3.0.3/index.js,aes/tracker-plugin-api/3.1.3/index.js,aes/tracker-plugin-resourceError/3.0.4/index.js,aes/tracker-plugin-perf/3.1.0/index.js,aes/tracker-plugin-eventTiming/3.0.0/index.js,aes/tracker-plugin-autolog/3.0.13/index.js', path: '/react-bundle.js' },
  
  // JS - 单独文件
  { url: '/jp-fe/jp-new-homepage-category-page/0.0.41/js/962.js', path: '/jp-fe/jp-new-homepage-category-page/0.0.41/js/962.js' },
  { url: '/jp-fe/jp-new-homepage-category-page/0.0.41/js/p_category.js', path: '/jp-fe/jp-new-homepage-category-page/0.0.41/js/p_category.js' },
  { url: '/jp-fe/jp-new-homepage-category-page/0.0.41/js/framework.js', path: '/jp-fe/jp-new-homepage-category-page/0.0.41/js/framework.js' },
  { url: '/jp-fe/jp-new-homepage-category-page/0.0.41/js/178.js', path: '/jp-fe/jp-new-homepage-category-page/0.0.41/js/178.js' },
  { url: '/jp-fe/jp-new-homepage-category-page/0.0.41/js/main.js', path: '/jp-fe/jp-new-homepage-category-page/0.0.41/js/main.js' },
  { url: '/mtb/lib-windvane/3.0.7/windvane.js', path: '/mtb/lib-windvane/3.0.7/windvane.js' },
  { url: '/jp-fe/jp-fsp-analyser/0.0.4/sfsp_v2.js', path: '/jp-fe/jp-fsp-analyser/0.0.4/sfsp_v2.js' },
  
  // 其他
  { url: '/AWSC/et/1.83.41/et_f.js', path: '/AWSC/et/1.83.41/et_f.js' },
  { url: '/sd/baxia/2.5.36/baxiaCommon.js', path: '/sd/baxia/2.5.36/baxiaCommon.js' },
  { url: '/AWSC/AWSC/awsc.js', path: '/AWSC/AWSC/awsc.js' },
  { url: '/secdev/sufei_data/3.9.14/index.js', path: '/secdev/sufei_data/3.9.14/index.js' },
  { url: '/o.alicdn.com/baxia/baxia-entry-gray/index.js', path: '/o.alicdn.com/baxia/baxia-entry-gray/index.js', base: 'https://o.alicdn.com' },
  { url: '/alilog/mlog/aplus_v2.js', path: '/alilog/mlog/aplus_v2.js', base: 'https://g.alicdn.com' },
  
  // 图片
  { url: '/jp-fe/jp-new-homepage-category-page/0.0.41/assets/gujiatu.ee7891da.gif', path: '/jp-fe/jp-new-homepage-category-page/0.0.41/assets/gujiatu.ee7891da.gif' },
];

function download(url, dest, base = CDN_BASE) {
  return new Promise((resolve, reject) => {
    const fullUrl = base + url;
    const destPath = BASE_DIR + dest;
    
    // 创建目录
    const dir = path.dirname(destPath);
    fs.mkdirSync(dir, { recursive: true });
    
    console.log('[Download]', fullUrl, '->', destPath);
    
    https.get(fullUrl, {
      headers: { 'Accept-Encoding': 'gzip' }
    }, (res) => {
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => {
        const buffer = Buffer.concat(chunks);
        const enc = res.headers['content-encoding'];
        
        if (enc === 'gzip') {
          zlib.gunzip(buffer, (err, dec) => {
            if (err) reject(err);
            else {
              fs.writeFileSync(destPath, dec);
              console.log('[OK]', dest);
              resolve();
            }
          });
        } else {
          fs.writeFileSync(destPath, buffer);
          console.log('[OK]', dest);
          resolve();
        }
      });
    }).on('error', reject);
  });
}

async function main() {
  console.log('\n' + '='.repeat(60));
  console.log('📥 开始下载 CDN 资源...');
  console.log('='.repeat(60) + '\n');
  
  let success = 0;
  let failed = 0;
  
  for (const res of RESOURCES) {
    try {
      await download(res.url, res.path, res.base || CDN_BASE);
      success++;
    } catch (err) {
      console.error('[FAIL]', res.path, err.message);
      failed++;
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log(`✅ 完成！成功：${success}, 失败：${failed}`);
  console.log('='.repeat(60) + '\n');
}

main();
