#!/usr/bin/env node

/**
 * MTOP Mock Server - Node.js 版本
 * 模拟 Java Spring Boot 服务提供 Mock 数据
 */

const http = require('http');
const url = require('url');

const PORT = 8090;

// Mock 数据
const MOCK_DATA = {
  'mtop.alibaba.jp.guide.page.get': {
    ret: ['SUCCESS::调用成功'],
    v: '1.0',
    data: {
      pageCode: '541699',
      pageName: '新分类 - 女性穿搭',
      cardGroups: [
        {
          cardCode: 'xiaowupinlei1',
          identityName: 'channelPageStandardCard',
          contentInfo: {
            moduleConfig: { customSpmc: 'xiaowupinlei1', title: '小物品类 1' },
            elements: [{
              itemList: [
                createItem('1001006104017075', 'レディース ボストン型 ショルダーバッグ', '9267', '10267', '9'),
                createItem('1001006096311386', '大容量 本革トートバッグ', '8362', '9362', '10'),
                createItem('1001006098713583', 'レトロデザインの大容量本革トートバッグ', '7852', '8852', '11'),
                createItem('1001006107296768', '極上の柔らかさの腋下バッグ', '26225', '27225', '3')
              ],
              isDiscountExist: true
            }]
          }
        },
        {
          cardCode: 'xiaowupinlei3',
          identityName: 'channelPageStandardCard',
          contentInfo: {
            moduleConfig: { customSpmc: 'xiaowupinlei3', title: '旅をラクにするスーツケース厳選' },
            elements: [{
              itemList: [
                createItem('1001006107613343', '男女兼用 本革 羊革製 トラベルバッグ', '4208', '5208', '19'),
                createItem('1001006097916009', '大容量アルミフレーム旅行カバン', '7872', '8872', '11'),
                createItem('1001006107198446', 'ヴィンテージクレイジーホーススキントラベルバッグ', '10971', '11971', '8'),
                createItem('1001006098003196', '軽量で堅牢なキャリーケース', '5425', '6425', '15')
              ],
              isDiscountExist: true
            }]
          }
        }
      ]
    }
  },
  
  'mtop.relationrecommend.TianTaoJpRecommend.recommend': {
    ret: ['SUCCESS::调用成功'],
    v: '1.0',
    data: {
      result: [{
        mods: {
          listItems: [
            createItem('1001006107296768', '極上の柔らかさの腋下バッグ', '26225', '27225', '3'),
            createItem('1001006096311386', '大容量 本革トートバッグ', '8362', '9362', '10'),
            createItem('1001006098713583', 'レトロデザインの大容量本革トートバッグ', '7852', '8852', '11'),
            createItem('1001006104017075', 'レディース ボストン型 ショルダーバッグ', '9267', '10267', '9')
          ]
        }
      }],
      rcmdTitle: { title: 'RECOMMEND', tItemType: 'nt_rcmd_title' }
    }
  },
  
  'mtop.jptao.ug.popx.check': {
    ret: ['SUCCESS::调用成功'],
    v: '1.0',
    data: { result: true, success: true, uuid: 'mock_' + Date.now() }
  },
  
  'mtop.jptao.ug.popx.list': {
    ret: ['SUCCESS::调用成功'],
    v: '1.0',
    data: { success: true, activities: [], actions: [], traces: [], updateTime: Date.now() }
  },
  
  'mtop.jp.wishlist.item.add': {
    ret: ['SUCCESS::调用成功'],
    v: '1.0',
    data: { result: 'true' }
  },
  
  'mtop.jp.interaction.execute': {
    ret: ['SUCCESS::调用成功'],
    data: { result: 'true' }
  }
};

// 创建商品对象
function createItem(itemId, title, price, originalPrice, discount) {
  return {
    itemId: parseInt(itemId),
    itemImage: `https://pic-cdn-jp.tao-media.co/kf/S${itemId}.jpg_400x400q75.jpg_.webp`,
    itemPrice: {
      cent: parseInt(price),
      currencySymbol: '¥',
      discountRate: parseInt(discount),
      originalPrice: '¥ ' + formatPrice(originalPrice),
      priceInfo: '¥ ' + formatPrice(price),
      priceString: price,
      color: '#333333',
      discountRateLineBreak: discount + '%-OFF',
      displayText: discount + '%OFF',
      originalCent: parseInt(originalPrice)
    },
    itemStatus: { status: 1 },
    sales: Math.floor(Math.random() * 200),
    supplementSellingPoints: [{ displayText: '好評アイテム', pointType: 'POSITIVE_EVALUATION_POINT' }]
  };
}

// 格式化价格
function formatPrice(priceStr) {
  return parseInt(priceStr).toLocaleString();
}

// 创建 HTTP 服务器
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const api = parsedUrl.query.api;
  
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  
  // 设置 CORS 头
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Content-Type', 'application/json;charset=UTF-8');
  
  // 处理 OPTIONS 请求
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  // 获取 Mock 数据
  let responseData = { ret: ['SUCCESS::调用成功'], v: '1.0', traceId: 'mock_' + Date.now() };
  
  if (api && MOCK_DATA[api]) {
    responseData.data = MOCK_DATA[api].data;
    console.log(`  ✅ 返回 Mock 数据：${api}`);
  } else {
    responseData.data = {};
    console.log(`  ⚠️ 未找到 API: ${api}`);
  }
  
  res.writeHead(200);
  res.end(JSON.stringify(responseData));
});

// 启动服务器
server.listen(PORT, () => {
  console.log('');
  console.log('='.repeat(60));
  console.log('🚀 MTOP Mock Server 已启动');
  console.log('='.repeat(60));
  console.log('');
  console.log('📍 服务地址：http://localhost:' + PORT);
  console.log('');
  console.log('📋 支持的 API:');
  Object.keys(MOCK_DATA).forEach(api => {
    console.log('   - ' + api);
  });
  console.log('');
  console.log('🔗 测试链接:');
  console.log('   http://localhost:' + PORT + '/mtop/comet/async.api?api=mtop.alibaba.jp.guide.page.get');
  console.log('   http://localhost:' + PORT + '/mtop/comet/async.api?api=mtop.relationrecommend.TianTaoJpRecommend.recommend');
  console.log('');
  console.log('='.repeat(60));
  console.log('');
});
