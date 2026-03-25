# MTOP Mock 拦截器

已创建 MTOP 接口拦截器脚本，用于拦截 Control UI 页面中的 mtop 接口请求并返回本地 mock 数据。

## 文件位置

- **拦截器脚本**: `/Users/dhr/.openclaw/workspace/projects/integration-sandbox/mtop-mock-interceptor.js`
- **Mock 数据**: `/Users/dhr/.openclaw/workspace/projects/integration-sandbox/mockData.txt`

## 使用方法

### 方式 1：在浏览器控制台手动注入

打开 OpenClaw Control UI 页面（`http://localhost:8080/control-ui` 或实际地址），在浏览器控制台粘贴以下内容：

```javascript
// 加载并执行拦截器
const script = document.createElement('script');
script.src = 'file:///Users/dhr/.openclaw/workspace/projects/integration-sandbox/mtop-mock-interceptor.js';
document.head.appendChild(script);
```

### 方式 2：使用浏览器扩展

安装用户脚本管理器扩展（如 Tampermonkey、Violentmonkey），然后创建新脚本：

```javascript
// ==UserScript==
// @name         MTOP Mock Interceptor
// @match        *://*/control-ui/*
// @grant        none
// ==/UserScript==

(function() {
    // 将 mtop-mock-interceptor.js 的内容复制到这里
    // ... 脚本内容 ...
})();
```

### 方式 3：修改 index.html（开发环境）

在 `/opt/homebrew/lib/node_modules/openclaw/dist/control-ui/index.html` 的 `<head>` 中添加：

```html
<script src="/Users/dhr/.openclaw/workspace/projects/integration-sandbox/mtop-mock-interceptor.js"></script>
```

## 拦截的 API 列表

根据 mockData.txt，以下 API 将被拦截并返回 mock 数据：

| API | 说明 |
|-----|------|
| `mtop.relationrecommend.tiantaojprecommend.recommend` | 商品推荐 |
| `mtop.alibaba.jp.guide.page.get` | 导购页面获取 |
| `mtop.jp.wishlist.item.add` | 添加心愿单 |
| `mtop.jptao.ug.popx.list` | 弹窗列表 |
| `mtop.jp.interaction.execute` | 交互执行 |
| `mtop.jptao.ug.popx.check` | 弹窗检查 |
| `mtop.jp.pc.render` | PC 渲染 |
| `mtop.alibaba.jp.guide.gateway.aldpage` | 导购网关 |

## 功能特性

- ✅ 不改变页面样式
- ✅ 自动拦截 fetch 请求
- ✅ 自动拦截 XMLHttpRequest
- ✅ 返回本地 mock 数据
- ✅ 控制台日志显示拦截状态
- ✅ 响应头添加 `X-MTOP-MOCK: true` 标识

## 注意事项

1. **文件访问权限**: 如果直接使用 `file://` 协议加载脚本，可能需要浏览器允许访问本地文件
2. **CORS**: 如果遇到跨域问题，建议使用用户脚本管理器扩展
3. **Mock 数据更新**: 修改 mockData.txt 后需要重新加载拦截器

## 验证拦截是否生效

打开浏览器控制台，如果看到以下日志表示拦截器已激活：

```
[MTOP Mock] Interceptor loaded, mocking X APIs
[MTOP Mock] ✅ Interceptor active
[MTOP Mock] Mocked APIs: [...]
[MTOP Mock] Intercepted: mtop.xxx.xxx
```
