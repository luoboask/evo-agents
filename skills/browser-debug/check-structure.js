#!/usr/bin/env node

const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  const mockResponses = [];
  
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('mtop.alibaba') || url.includes('TianTaoJpRecommend')) {
      try {
        const data = await response.json();
        mockResponses.push({
          api: url.split('api=')[1]?.split('&')[0] || 'unknown',
          data: data
        });
      } catch (e) {}
    }
  });
  
  await page.goto('http://localhost:3000/category', { 
    waitUntil: 'networkidle0', 
    timeout: 60000 
  });
  
  await new Promise(resolve => setTimeout(resolve, 3000));
  
  console.log('📊 Mock 响应数据:\n');
  
  mockResponses.forEach((res, i) => {
    console.log(`${i + 1}. API: ${res.api}`);
    console.log('   data 结构:');
    
    if (res.data && res.data.data) {
      const d = res.data.data;
      console.log('   - data.cardGroups:', d.cardGroups ? `有 (${d.cardGroups.length}个)` : '无');
      
      if (d.cardGroups && d.cardGroups[0]) {
        console.log('   - 第一个 cardGroups:');
        console.log('     - cardCode:', d.cardGroups[0].cardCode);
        console.log('     - elements:', d.cardGroups[0].elements ? `有 (${d.cardGroups[0].elements.length}个)` : '无');
        
        if (d.cardGroups[0].elements && d.cardGroups[0].elements[0]) {
          const elem = d.cardGroups[0].elements[0];
          console.log('     - elements[0].contentInfo:', elem.contentInfo ? '有' : '无');
          
          if (elem.contentInfo) {
            const ci = elem.contentInfo;
            console.log('     - contentInfo.itemList:', ci.itemList ? `有 (${ci.itemList.length}个)` : '无');
            
            if (ci.itemList && ci.itemList[0]) {
              console.log('     - itemList[0] 字段:');
              console.log('       - itemId:', ci.itemList[0].itemId);
              console.log('       - itemImage:', ci.itemList[0].itemImage);
              console.log('       - itemPrice:', ci.itemList[0].itemPrice ? '有' : '无');
              if (ci.itemList[0].itemPrice) {
                console.log('         - priceInfo:', ci.itemList[0].itemPrice.priceInfo);
              }
            }
          }
        }
      }
    }
    
    console.log('');
  });
  
  await browser.close();
})();
