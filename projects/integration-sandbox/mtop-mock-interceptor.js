/**
 * MTOP 接口拦截器
 * 拦截 mtop 接口请求并返回本地 mock 数据
 * 
 * 使用方法：在页面中注入此脚本
 */

(function() {
  'use strict';

  // Mock 数据配置
  const MOCK_CONFIG = {
    active: true,
    enable: true,
    id: "scene_2853267676541520",
    name: "导购",
    options: {
      mtop: {
        rules: [
          {
            api: "mtop.relationrecommend.tiantaojprecommend.recommend",
            enable: true,
            id: "rule_5430389577338997",
            type: "local",
            localData: JSON.stringify({
              "api": "mtop.relationrecommend.tiantaojprecommend.recommend",
              "data": {
                "result": [
                  {
                    "layoutInfo": {
                      "listHeader": ["rcmdTitle"]
                    },
                    "mods": {
                      "listItems": [
                        {
                          "image": {
                            "imgUrl": "https://pic-cdn-jp.tao-media.co/kf/S23c00cde0a4649579fe0d5a39a401533o.jpg",
                            "imgWidth": 3,
                            "imgHeight": 4,
                            "imgType": "3:4"
                          },
                          "itemType": "rmdproductV3",
                          "productId": "1001006085354675",
                          "title": {
                            "displayTitle": "極上の柔らかさのランニングパンツ【夏用・薄手・通気性・ゆったりフィット】",
                            "rowNum": 1
                          },
                          "prices": {
                            "originalPrice": {
                              "formattedPrice": "¥ 3,712",
                              "minPrice": 3712.0,
                              "currencyCode": "JPY"
                            },
                            "salePrice": {
                              "formattedPrice": "¥ 2,341",
                              "minPrice": 2341.0,
                              "discount": 36,
                              "currencyCode": "JPY"
                            }
                          }
                        }
                      ]
                    }
                  }
                ]
              },
              "ret": ["SUCCESS::调用成功"],
              "traceId": "mock_" + Date.now(),
              "v": "1.0"
            })
          },
          {
            api: "mtop.jp.wishlist.item.add",
            enable: true,
            id: "rule_1733744788940637",
            type: "local",
            localData: JSON.stringify({
              "api": "mtop.jp.wishlist.item.add",
              "data": {
                "result": "true"
              },
              "ret": ["SUCCESS::调用成功"],
              "v": "1.0"
            })
          },
          {
            api: "mtop.jp.interaction.execute",
            enable: true,
            id: "rule_407108490577201",
            type: "local",
            localData: JSON.stringify({
              "data": {
                "result": "true"
              }
            })
          },
          {
            api: "mtop.jptao.ug.popx.check",
            enable: true,
            id: "rule_5397697371819862",
            type: "local",
            localData: JSON.stringify({
              "api": "mtop.jptao.ug.popx.check",
              "data": {
                "result": true,
                "success": true,
                "uuid": "msite_2_744_20260114"
              },
              "ret": ["SUCCESS::调用成功"],
              "traceId": "mock_" + Date.now(),
              "v": "1.0"
            })
          },
          {
            api: "mtop.jptao.ug.popx.list",
            enable: true,
            id: "rule_4882201673159420",
            type: "local",
            localData: JSON.stringify({
              "api": "mtop.jptao.ug.popx.list",
              "v": "1.0",
              "data": {
                "traces": [],
                "manualActs": [],
                "updateTime": Date.now(),
                "success": true,
                "globalFreqs": [],
                "pageControl": [],
                "channelMutex": {},
                "actions": [],
                "activities": []
              },
              "ret": ["SUCCESS::调用成功"]
            })
          }
        ]
      }
    }
  };

  // 构建 mock 数据映射
  const mockDataMap = {};
  MOCK_CONFIG.options.mtop.rules.forEach(rule => {
    if (rule.enable && rule.localData) {
      try {
        mockDataMap[rule.api] = JSON.parse(rule.localData);
      } catch (e) {
        console.warn('[MTOP Mock] Failed to parse mock data for', rule.api, e);
      }
    }
  });

  console.log('[MTOP Mock] Interceptor loaded, mocking', Object.keys(mockDataMap).length, 'APIs');

  // 拦截 fetch 请求
  const originalFetch = window.fetch;
  window.fetch = function(...args) {
    const url = args[0] instanceof Request ? args[0].url : String(args[0]);
    
    // 检查是否是 mtop 接口
    if (url.includes('mtop.')) {
      // 提取 API 名称
      const urlObj = new URL(url, window.location.origin);
      const api = urlObj.searchParams.get('api') || extractApiFromPath(urlObj.pathname);
      
      if (api && mockDataMap[api]) {
        console.log('[MTOP Mock] Intercepted:', api);
        
        // 返回 mock 数据
        return Promise.resolve(new Response(JSON.stringify(mockDataMap[api]), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'X-MTOP-MOCK': 'true'
          }
        }));
      }
    }
    
    return originalFetch.apply(this, args);
  };

  // 拦截 XMLHttpRequest
  const originalXHROpen = XMLHttpRequest.prototype.open;
  const originalXHRSend = XMLHttpRequest.prototype.send;

  XMLHttpRequest.prototype.open = function(method, url, ...rest) {
    this._mockUrl = url;
    return originalXHROpen.apply(this, [method, url, ...rest]);
  };

  XMLHttpRequest.prototype.send = function(...args) {
    const url = this._mockUrl;
    
    if (url && url.includes('mtop.')) {
      // 尝试从 URL 或请求体中提取 API 名称
      let api = null;
      
      if (typeof url === 'string') {
        try {
          const urlObj = new URL(url, window.location.origin);
          api = urlObj.searchParams.get('api') || extractApiFromPath(urlObj.pathname);
        } catch (e) {
          api = extractApiFromPath(url);
        }
      }
      
      if (api && mockDataMap[api]) {
        console.log('[MTOP Mock] Intercepted XHR:', api);
        
        // 延迟返回以模拟网络请求
        setTimeout(() => {
          Object.defineProperty(this, 'responseText', {
            value: JSON.stringify(mockDataMap[api])
          });
          Object.defineProperty(this, 'response', {
            value: JSON.stringify(mockDataMap[api])
          });
          Object.defineProperty(this, 'status', {
            value: 200
          });
          
          // 触发事件
          if (this.onload) this.onload();
          if (this.onreadystatechange) this.onreadystatechange();
        }, 50);
        
        return;
      }
    }
    
    return originalXHRSend.apply(this, args);
  };

  // 辅助函数：从路径提取 API 名称
  function extractApiFromPath(pathname) {
    // 匹配类似 /mtop.api.name/1.0/ 的路径
    const match = pathname.match(/\/(mtop\.[a-zA-Z0-9_.]+)\//);
    return match ? match[1] : null;
  }

  // 在控制台添加状态指示
  console.log('[MTOP Mock] ✅ Interceptor active');
  console.log('[MTOP Mock] Mocked APIs:', Object.keys(mockDataMap));

})();
