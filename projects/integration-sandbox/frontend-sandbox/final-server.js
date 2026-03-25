#!/usr/bin/env node

/**
 * Final Server - 直接使用提供的 HTML
 */

const http = require('http');
const https = require('https');
const zlib = require('zlib');

// 你提供的完整 HTML
const HTML = `<!DOCTYPE html><html><head><meta name="data-spm" content="3d3def51"><meta charset="utf-8"><meta name="description" content="A new ice.js project."><meta name="referrer" content="no-referrer-when-downgrade"><meta name="aplus-core" content="aplus.js"><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover"><link href="https://pic-cdn-jp.tao-media.co/kf/Sd86651dc659d452283b767be206a4706v/64x64.png" rel="shortcut icon" type="image/x-icon"><link rel="stylesheet" href="https://assets.alicdn.com/g/ae-fe/cosmos/0.0.254/pc/index.css"><meta name="aplus-rhost-v" content="sg.mmstat.com"><meta name="aplus-rhost-g" content="sg.mmstat.com"><meta name="ice-meta-count" content="0"><title></title><link rel="stylesheet" type="text/css" href="https://g.alicdn.com/jp-fe/jp-new-homepage-category-page/0.0.41/css/main.css"><link rel="stylesheet" type="text/css" href="https://g.alicdn.com/jp-fe/jp-new-homepage-category-page/0.0.41/css/962.css"><link rel="stylesheet" type="text/css" href="https://g.alicdn.com/jp-fe/jp-new-homepage-category-page/0.0.41/css/p_category.css"><script src="https://g.alicdn.com/AWSC/et/1.83.41/et_f.js" id="AWSC_etModule"></script><script async="" src="//g.alicdn.com/sd/baxia/2.5.36/baxiaCommon.js" crossorigin="true"></script><script async="" src="https://g.alicdn.com/AWSC/AWSC/awsc.js" crossorigin="true"></script><script async="" src="https://g.alicdn.com/secdev/sufei_data/3.9.14/index.js" crossorigin="true"></script><script type="text/javascript" async="" src="https://o.alicdn.com/baxia/baxia-entry-gray/index.js" id="aplus-baxia"></script><script>/*! 2025-12-02 11:27:13 aplus_pc.js */
!function(t){function e(n){if(r[n])return r[n].exports;var a=r[n]={exports:{},id:n,loaded:!1};return t[n].call(a.exports,a,a.exports,e),a.loaded=!0,a.exports}var r={};return e.m=t,e.c=r,e.p="",e(0)}([function(t,e,r){t.exports=r(1)},function(t,e){"use strict";!function(){function t(t,e,r){t[_]((h?"on":"")+e,function(t){t=t||s.event;var e=t.target||t.srcElement;r(t,e)},!1)}function e(){return/&?\bspm=[^&#]*/.test(location.href)?location.href.match(/&?\bspm=[^&#]*/gi)[0].split("=")[1]:""}function r(t,e){if(t&&/&?\bspm=[^&#]*/.test(t)&&(t=t.replace(/&?\bspm=[^&#]*/g,"").replace(/&{2,}/g,"&").replace(/\?&/,"?").replace(/\?$/,"")),!e)return t;var r,n,a,i,o,c,p,s="&";if(t.indexOf("#")!=-1&&(a=t.split("#"),t=a.shift(),n=a.join("#")),i=t.split("?"),o=i.length-1,a=i[0].split("//"),a=a[a.length-1].split("/"),c=a.length>1?a.pop():"",o>0&&(r=i.pop(),t=i.join("?")),r&&o>1&&r.indexOf("&")==-1&&r.indexOf("%")!=-1&&(s="%26"),t=t+"?spm="+e+(r?s+r:"")+(n?"#"+n:""),p=c.indexOf(".")>-1?c.split(".").pop().toLowerCase():""){if({png:1,jpg:1,jpeg:1,gif:1,bmp:1,swf:1}.hasOwnProperty(p))return 0;!r&&o<=1&&(n||{htm:1,html:1,php:1}.hasOwnProperty(p)||(t+="&file="+c))}return t}function n(t){function e(t){return t=t.replace(/refpos[=(%3D)]\w*/gi,c).replace(i,"%3D"+n+"%26"+a.replace("=","%3D")).replace(o,n),a.length>0&&(t+="&"+a),t}var r=window.location.href,n=r.match(/mm_\d{0,24}_\d{0,24}_\d{0,24}/i),a=r.match(/[&\?](pvid=[^&]*)/i),i=new RegExp("%3Dmm_\\d+_\\d+_\\d+","ig"),o=new RegExp("mm_\\d+_\\d+_\\d+","ig");a=a&&a[1]?a[1]:"";var c=r.match(/(refpos=(\d{0,24}_\d{0,24}_\d{0,24})?(,[a-z]+)?)(,[a-z]+)?/i);return c=c&&c[0]?c[0]:"",n?(n=n[0],e(t)):t}function a(e){var r=s.KISSY;r?r.ready(e):s.jQuery?jQuery(m).ready(e):"complete"===m.readyState?e():t(s,"load",e)}function i(t,e){return t&&t.getAttribute?t.getAttribute(e)||"":""}function o(t){if(t){var e,r=g.length;for(e=0;e<r;e++)if(t.indexOf(g[e])>-1)return!0;return!1}}function c(t,e){if(t&&/&?\bspm=[^&#]*/.test(t)&&(t=t.replace(/&?\bspm=[^&#]*/g,"").replace(/&{2,}/g,"&").replace(/\?&/,"?").replace(/\?$/,"")),!e)return t;var r,n,a,i,o,c,p,s="&";if(t.indexOf("#")!=-1&&(a=t.split("#"),t=a.shift(),n=a.join("#")),i=t.split("?"),o=i.length-1,a=i[0].split("//"),a=a[a.length-1].split("/"),c=a.length>1?a.pop():"",o>0&&(r=i.pop(),t=i.join("?")),r&&o>1&&r.indexOf("&")==-1&&r.indexOf("%")!=-1&&(s="%26"),t=t+"?spm="+e+(r?s+r:"")+(n?"#"+n:""),p=c.indexOf(".")>-1?c.split(".").pop().toLowerCase():""){if({png:1,jpg:1,jpeg:1,gif:1,bmp:1,swf:1}.hasOwnProperty(p))return 0;!r&&o<=1&&(n||{htm:1,html:1,shtml:1,php:1}.hasOwnProperty(p)||(t+="&__file="+c))}return t}function p(t){if(o(t.href)){var r=i(t,u);if(!r){var n=l()(t),a=[n.a,n.b,n.c,n.d].join(".");n.e&&(n+="."+n.e),d&&(a=[n.a||"0",n.b||"0",n.c||"0",n.d||"0"].join("."),a=(e()||"0.0.0.0.0")+"_"+a),t.href=c(t.href,a),t.setAttribute(u,a)}}}var s=window,m=document;if(1!==s.aplus_spmact){s.aplus_spmact=1;var f=function(){return{a:0,b:0,c:0,d:0,e:0}},l=function(){return s.g_SPM&&s.g_SPM.getParam?s.g_SPM.getParam:f},d=!0;try{d=self.location!=top.location}catch(t){}var u="data-spm-act-id",g=["mclick.simba.taobao.com","click.simba.taobao.com","click.tanx.com","click.mz.simba.taobao.com","click.tz.simba.taobao.com","redirect.simba.taobao.com","rdstat.tanx.com","stat.simba.taobao.com","s.click.taobao.com"],h=!!m.attachEvent,b="attachEvent",v="addEventListener",_=h?b:v;t(m,"mousedown",function(t,e){for(var r,n=0;e&&(r=e.tagName);){if("A"==r||"AREA"==r){p(e);break}if("BODY"==r||"HTML"==r)break;e=e.parentNode,n+=1}}),a(function(){for(var t,a,o=document.getElementsByTagName("iframe"),c=0;c<o.length;c++){t=i(o[c],"mmsrc"),a=i(o[c],"mmworked");var p=l()(o[c]),s=[p.a||"0",p.b||"0",p.c||"0",p.d||"0",p.e||"0"].join(".");t&&!a?(d&&(s=[p.a||"0",p.b||"0",p.c||"0",p.d||"0"].join("."),s=e()+"_"+s),o[c].src=r(n(t),s),o[c].setAttribute("mmworked","mmworked")):o[c].setAttribute(u,s)}})}}()}]);/*! 2025-12-02 11:28:20 aplus_spmact.js */
!function(t){function e(n){if(r[n])return r[n].exports;var a=r[n]={exports:{},id:n,loaded:!1};return t[n].call(a.exports,a,a.exports,e),a.loaded=!0,a.exports}var r={};return e.m=t,e.c=r,e.p="",e(0)}([function(t,e,r){t.exports=r(1)},function(t,e){"use strict";!function(){function t(t,e,r){t[_]((h?"on":"")+e,function(t){t=t||s.event;var e=t.target||t.srcElement;r(t,e)},!1)}function e(){return/&?\bspm=[^&#]*/.test(location.href)?location.href.match(/&?\bspm=[^&#]*/gi)[0].split("=")[1]:""}function r(t,e){if(t&&/&?\bspm=[^&#]*/.test(t)&&(t=t.replace(/&?\bspm=[^&#]*/g,"").replace(/&{2,}/g,"&").replace(/\?&/,"?").replace(/\?$/,"")),!e)return t;var r,n,a,i,o,c,p,s="&";if(t.indexOf("#")!=-1&&(a=t.split("#"),t=a.shift(),n=a.join("#")),i=t.split("?"),o=i.length-1,a=i[0].split("//"),a=a[a.length-1].split("/"),c=a.length>1?a.pop():"",o>0&&(r=i.pop(),t=i.join("?")),r&&o>1&&r.indexOf("&")==-1&&r.indexOf("%")!=-1&&(s="%26"),t=t+"?spm="+e+(r?s+r:"")+(n?"#"+n:""),p=c.indexOf(".")>-1?c.split(".").pop().toLowerCase():""){if({png:1,jpg:1,jpeg:1,gif:1,bmp:1,swf:1}.hasOwnProperty(p))return 0;!r&&o<=1&&(n||{htm:1,html:1,shtml:1,php:1}.hasOwnProperty(p)||(t+="&__file="+c))}return t}function n(t){function e(t){return t=t.replace(/refpos[=(%3D)]\w*/gi,c).replace(i,"%3D"+n+"%26"+a.replace("=","%3D")).replace(o,n),a.length>0&&(t+="&"+a),t}var r=window.location.href,n=r.match(/mm_\d{0,24}_\d{0,24}_\d{0,24}/i),a=r.match(/[&\?](pvid=[^&]*)/i),i=new RegExp("%3Dmm_\\d+_\\d+_\\d+","ig"),o=new RegExp("mm_\\d+_\\d+_\\d+","ig");a=a&&a[1]?a[1]:"";var c=r.match(/(refpos=(\d{0,24}_\d{0,24}_\d{0,24})?(,[a-z]+)?)(,[a-z]+)?/i);return c=c&&c[0]?c[0]:"",n?(n=n[0],e(t)):t}function a(e){var r=s.KISSY;r?r.ready(e):s.jQuery?jQuery(m).ready(e):"complete"===m.readyState?e():t(s,"load",e)}function i(t,e){return t&&t.getAttribute?t.getAttribute(e)||"":""}function o(t){if(t){var e,r=g.length;for(e=0;e<r;e++)if(t.indexOf(g[e])>-1)return!0;return!1}}function c(t,e){if(t&&/&?\bspm=[^&#]*/.test(t)&&(t=t.replace(/&?\bspm=[^&#]*/g,"").replace(/&{2,}/g,"&").replace(/\?&/,"?").replace(/\?$/,"")),!e)return t;var r,n,a,i,o,c,p,s="&";if(t.indexOf("#")!=-1&&(a=t.split("#"),t=a.shift(),n=a.join("#")),i=t.split("?"),o=i.length-1,a=i[0].split("//"),a=a[a.length-1].split("/"),c=a.length>1?a.pop():"",o>0&&(r=i.pop(),t=i.join("?")),r&&o>1&&r.indexOf("&")==-1&&r.indexOf("%")!=-1&&(s="%26"),t=t+"?spm="+e+(r?s+r:"")+(n?"#"+n:""),p=c.indexOf(".")>-1?c.split(".").pop().toLowerCase():""){if({png:1,jpg:1,jpeg:1,gif:1,bmp:1,swf:1}.hasOwnProperty(p))return 0;!r&&o<=1&&(n||{htm:1,html:1,shtml:1,php:1}.hasOwnProperty(p)||(t+="&__file="+c))}return t}function p(t){if(o(t.href)){var r=i(t,u);if(!r){var n=l()(t),a=[n.a,n.b,n.c,n.d].join(".");n.e&&(n+="."+n.e),d&&(a=[n.a||"0",n.b||"0",n.c||"0",n.d||"0"].join("."),a=(e()||"0.0.0.0.0")+"_"+a),t.href=c(t.href,a),t.setAttribute(u,a)}}}var s=window,m=document;if(1!==s.aplus_spmact){s.aplus_spmact=1;var f=function(){return{a:0,b:0,c:0,d:0,e:0}},l=function(){return s.g_SPM&&s.g_SPM.getParam?s.g_SPM.getParam:f},d=!0;try{d=self.location!=top.location}catch(t){}var u="data-spm-act-id",g=["mclick.simba.taobao.com","click.simba.taobao.com","click.tanx.com","click.mz.simba.taobao.com","click.tz.simba.taobao.com","redirect.simba.taobao.com","rdstat.tanx.com","stat.simba.taobao.com","s.click.taobao.com"],h=!!m.attachEvent,b="attachEvent",v="addEventListener",_=h?b:v;t(m,"mousedown",function(t,e){for(var r,n=0;e&&(r=e.tagName);){if("A"==r||"AREA"==r){p(e);break}if("BODY"==r||"HTML"==r)break;e=e.parentNode,n+=1}}),a(function(){for(var t,a,o=document.getElementsByTagName("iframe"),c=0;c<o.length;c++){t=i(o[c],"mmsrc"),a=i(o[c],"mmworked");var p=l()(o[c]),s=[p.a||"0",p.b||"0",p.c||"0",p.d||"0",p.e||"0"].join(".");t&&!a?(d&&(s=[p.a||"0",p.b||"0",p.c||"0",p.d||"0"].join("."),s=e()+"_"+s),o[c].src=r(n(t),s),o[c].setAttribute("mmworked","mmworked")):o[c].setAttribute(u,s)}})}}()}]);</script><script async="" id="beacon-aplus" exparams="aplus&amp;sidx=aplusSidex&amp;ckx=aplusCkx" src="//g.alicdn.com/alilog/mlog/aplus_v2.js"></script><script type="text/javascript">
 (function(w, d, s, q) {
 w[q] = w[q] || [];
 var f = d.getElementsByTagName(s)[0],j = d.createElement(s);
 j.async = true;
 j.id = 'beacon-aplus';
 j.setAttribute('exparams','aplus&sidx=aplusSidex&ckx=aplusCkx');
 j.src = "//g.alicdn.com/alilog/mlog/aplus_v2.js";
 j.crossorigin = 'anonymous';
 f.parentNode.insertBefore(j, f);
 })(window, document, 'script', 'aplus_queue');
 </script></head><body data-spm="33676864"><div id="ice-container"><span style="display: inline;"><div><img src="https://g.alicdn.com/jp-fe/jp-new-homepage-category-page/0.0.41/assets/gujiatu.ee7891da.gif" style="width: 100%; height: auto;" data-spm-anchor-id="3d3def51.33676864.0.i0.6b08yLHCyLHC6t"></div></span><span style="display: none;"><div id="catePage" class="rax-view-v2 app--ljcVnc56" data-before-current-y="0"><div id="wrap" class="rax-view-v2 wrap--tFATNMgM"><div class="infinite-scroll-component__outerdiv"><div class="infinite-scroll-component comet-v2-infinite-scroll" style="height: auto; overflow: auto;"><div class="recommendWrapper--yiTw9Imr"><div class="recommendTitle--H4Y70i88">RECOMMEND</div><div class="recommendContent--uG9rwrrX"><div class="hyper-skeleton hyper-skeleton-animated hyper-skeleton-title" style="height: 60vw; width: 46vw;"></div><div class="hyper-skeleton hyper-skeleton-animated hyper-skeleton-title" style="height: 60vw; width: 46vw;"></div></div></div></div></div></div><div class="bar--ZZx00yfI" id="barheight"></div></div></span></div><script src="https://g.alicdn.com/??code/lib/react/18.3.1/umd/react.production.min.js,code/lib/react-dom/18.3.1/umd/react-dom.production.min.js,aes/tracker/3.3.9/index.js,mtb/lib-mtop/2.7.2/mtop.js,mtb/lib-windvane/3.0.7/windvane.js,aes/tracker-plugin-pv/3.0.6/index.js,aes/tracker-plugin-event/3.0.0/index.js,aes/tracker-plugin-jserror/3.0.3/index.js,aes/tracker-plugin-api/3.1.3/index.js,aes/tracker-plugin-resourceError/3.0.4/index.js,aes/tracker-plugin-perf/3.1.0/index.js,aes/tracker-plugin-eventTiming/3.0.0/index.js,aes/tracker-plugin-autolog/3.0.13/index.js"></script><script>!(function () {var a = window.__ICE_APP_CONTEXT__ || {};var b = {"appData":null,"loaderData":{"category":{"pageConfig":{}}},"routePath":"/category","matchedIds":["category"],"documentOnly":true,"renderMode":"CSR"};for (var k in a) {b[k] = a[k]}window.__ICE_APP_CONTEXT__=b;})();</script><script src="https://g.alicdn.com/jp-fe/jp-new-homepage-category-page/0.0.41/js/962.js"></script><script src="https://g.alicdn.com/jp-fe/jp-new-homepage-category-page/0.0.41/js/p_category.js"></script><script src="https://g.alicdn.com/jp-fe/jp-new-homepage-category-page/0.0.41/js/framework.js"></script><script src="https://g.alicdn.com/jp-fe/jp-new-homepage-category-page/0.0.41/js/178.js"></script><script src="https://g.alicdn.com/jp-fe/jp-new-homepage-category-page/0.0.41/js/main.js"></script><script src="//g.alicdn.com/mtb/lib-windvane/3.0.7/windvane.js" crossorigin="anonymous"></script><script src="https://g.alicdn.com/jp-fe/jp-fsp-analyser/0.0.4/sfsp_v2.js" crossorigin="anonymous"></script></body></html>`;

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
  }).on('error', (e) => {
    res.statusCode = 500;
    res.end('CDN Error: ' + e.message);
  });
}

function getContentType(path) {
  if (path.endsWith('.js')) return 'application/javascript; charset=utf-8';
  if (path.endsWith('.css')) return 'text/css; charset=utf-8';
  if (path.endsWith('.html')) return 'text/html; charset=utf-8';
  if (path.endsWith('.png')) return 'image/png';
  if (path.endsWith('.jpg')) return 'image/jpeg';
  if (path.endsWith('.gif')) return 'image/gif';
  if (path.endsWith('.svg')) return 'image/svg+xml';
  if (path.endsWith('.ico')) return 'image/x-icon';
  if (path.endsWith('.woff')) return 'font/woff';
  if (path.endsWith('.woff2')) return 'font/woff2';
  return 'application/octet-stream';
}

const server = http.createServer((req, res) => {
  const url = req.url;
  console.log('[Request]', url);
  
  // HTML 页面 - 直接返回提供的 HTML
  if (url === '/' || url === '/index.html' || url === '/category') {
    console.log('[Server] 返回 HTML');
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.write(HTML);
    res.end();
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

const PORT = 8105;

server.listen(PORT, () => {
  console.log('\n' + '='.repeat(70));
  console.log('🔌 Final Server 已启动');
  console.log('='.repeat(70));
  console.log('\n📍 访问：http://localhost:' + PORT);
  console.log('\n✅ 直接使用提供的 HTML');
  console.log('✅ 代理所有 CDN 资源');
  console.log('\n' + '='.repeat(70) + '\n');
});
