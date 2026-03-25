#!/usr/bin/env node

const puppeteer = require('puppeteer');

(async () => {
  console.log('🔍 检查 Mock 数据...\n');
  
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  page.on('console', msg => {
    if (msg.text().includes('MTOP Mock') || msg.text().includes('返回数据')) {
      console.log(`[${msg.type()}] ${msg.text()}`);
    }
  });
  
  await page.goto('http://localhost:3000/category', { 
    waitUntil: 'networkidle0', 
    timeout: 60000 
  });
  
  await new Promise(resolve => setTimeout(resolve, 3000));
  
  console.log('\n💉 检查返回的 Mock 数据...\n');
  
  const mockData = await page.evaluate(() => {
    return window.__MTOP_MOCK_STATUS__ ? {
      enabled: window.__MTOP_MOCK_STATUS__.enabled,
      interceptedCount: window.__MTOP_MOCK_STATUS__.interceptedCount,
      lastAPI: window.__MTOP_MOCK_STATUS__.lastAPI
    } : null;
  });
  
  console.log('Mock 状态:', mockData);
  
  console.log('\n📊 检查 dataSource...\n');
  
  const dataSource = await page.evaluate(() => {
    return window.debugDataSource || null;
  });
  
  if (dataSource && dataSource.data && dataSource.data.cardGroups) {
    console.log('✅ 有 cardGroups 数据');
    console.log('数量:', dataSource.data.cardGroups.length);
    
    dataSource.data.cardGroups.forEach((card, i) => {
      console.log(`\n卡片 ${i + 1}:`);
      console.log('  cardCode:', card.cardCode);
      console.log('  identityName:', card.identityName);
      
      if (card.elements && card.elements[0]) {
        const itemList = card.elements[0].contentInfo?.itemList;
        if (itemList && itemList.length > 0) {
          console.log('  itemList 数量:', itemList.length);
          console.log('  第一个商品:');
          console.log('    - itemId:', itemList[0].itemId);
          console.log('    - title:', itemList[0].title?.displayTitle);
          console.log('    - itemImage:', itemList[0].itemImage);
          console.log('    - itemPrice:', itemList[0].itemPrice);
          console.log('    - itemPrice.priceInfo:', itemList[0].itemPrice?.priceInfo);
        }
      }
    });
  } else {
    console.log('❌ 没有 cardGroups 数据');
    console.log('dataSource:', JSON.stringify(dataSource, null, 2).substring(0, 500));
  }
  
  await browser.close();
  
  console.log('\n✅ 检查完成\n');
})();
