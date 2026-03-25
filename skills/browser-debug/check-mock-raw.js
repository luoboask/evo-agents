#!/usr/bin/env node

const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  await page.goto('http://localhost:3000/category', { 
    waitUntil: 'domcontentloaded', 
    timeout: 60000 
  });
  
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  console.log('📊 检查 Mock 数据结构:\n');
  
  const result = await page.evaluate(() => {
    // 获取 Mock 数据
    const mockStatus = window.__MTOP_MOCK_STATUS__;
    
    // 模拟拦截器返回的数据
    const MOCK_DATA = {
      'mtop.alibaba.jp.guide.page.get': {
        ret: ['SUCCESS::调用成功'],
        v: '1.0',
        data: {
          cardGroups: [
            {
              cardCode: 'channelPageBannerCard',
              identityName: 'channelPageBannerCard',
              contentInfo: {
                topCateList: [
                  { 
                    imageUrl: 'https://pic-cdn-jp.tao-media.co/kf/S86651dc659d452283b767be206a4706v.jpg',
                    targetUrl: '#'
                  }
                ]
              }
            },
            {
              cardCode: 'channelPageStandardCard',
              identityName: 'channelPageStandardCard',
              contentInfo: {
                moduleConfig: {
                  title: 'RECOMMEND',
                  customSpmc: 'rcmdprod',
                  cardContainerSize: '3:4',
                  cardRows: '2'
                }
              },
              elements: [{
                contentInfo: {
                  itemList: [
                    { 
                      itemId: 1001006085354675, 
                      title: { displayTitle: '商品 1' },
                      itemImage: 'https://pic-cdn-jp.tao-media.co/kf/S23c00cde0a4649579fe0d5a39a401533o.jpg',
                      itemPrice: {
                        cent: 2341,
                        currencySymbol: '¥',
                        discountRate: 36,
                        originalPrice: '¥ 3,712',
                        priceInfo: '¥ 2,341',
                        priceString: '2341'
                      }
                    }
                  ]
                }
              }]
            }
          ]
        }
      }
    };
    
    // 检查结构
    const data = MOCK_DATA['mtop.alibaba.jp.guide.page.get'];
    const cardGroups = data.data.cardGroups;
    
    const check = {
      hasCardGroups: !!cardGroups,
      cardGroupsLength: cardGroups?.length,
      secondCard: cardGroups?.[1] ? {
        hasElements: !!cardGroups[1].elements,
        elementsLength: cardGroups[1].elements?.length,
        firstElement: cardGroups[1].elements?.[0] ? {
          hasContentInfo: !!cardGroups[1].elements[0].contentInfo,
          hasItemList: !!cardGroups[1].elements[0].contentInfo?.itemList,
          itemListLength: cardGroups[1].elements[0].contentInfo?.itemList?.length,
          firstItem: cardGroups[1].elements[0].contentInfo?.itemList?.[0] ? {
            itemId: cardGroups[1].elements[0].contentInfo.itemList[0].itemId,
            itemImage: cardGroups[1].elements[0].contentInfo.itemList[0].itemImage,
            itemPrice: cardGroups[1].elements[0].contentInfo.itemList[0].itemPrice ? '有' : '无',
            priceInfo: cardGroups[1].elements[0].contentInfo.itemList[0].itemPrice?.priceInfo
          } : null
        } : null
      } : null
    };
    
    return { mockStatus, check };
  });
  
  console.log('Mock 状态:', result.mockStatus);
  console.log('\n数据结构检查:');
  console.log(JSON.stringify(result.check, null, 2));
  
  await browser.close();
})();
