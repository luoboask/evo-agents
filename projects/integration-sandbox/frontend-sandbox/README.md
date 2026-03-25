# Frontend Sandbox - 前端沙箱

用于运行和测试前端页面的隔离环境，自动拦截 mtop 请求并返回 mock 数据。

---

## 🚀 快速启动

### 方式 1: Python 简单服务器

```bash
cd /Users/dhr/.openclaw/workspace/projects/integration-sandbox/frontend-sandbox
python3 -m http.server 8080
```

然后访问：http://localhost:8080

### 方式 2: Node.js http-server

```bash
npm install -g http-server
cd /Users/dhr/.openclaw/workspace/projects/integration-sandbox/frontend-sandbox
http-server -p 8080
```

### 方式 3: VS Code Live Server

1. 在 VS Code 中打开 `frontend-sandbox` 文件夹
2. 安装 Live Server 扩展
3. 右键 `index.html` → "Open with Live Server"

---

## 📁 文件结构

```
frontend-sandbox/
├── index.html          # 前端入口 (注入 mock 拦截器)
├── mtop-mock.js        # MTOP 请求拦截器
└── README.md           # 说明文档
```

---

## 🔌 Mock 拦截说明

### 拦截的 API

| API | 说明 | Mock 数据 |
|-----|------|----------|
| `mtop.relationrecommend.tiantaojprecommend.recommend` | 商品推荐 | 2 个商品 |
| `mtop.alibaba.jp.guide.page.get` | 导购页面 | 空卡片列表 |
| `mtop.jptao.ug.popx.check` | 弹窗检查 | 允许显示 |
| `mtop.jptao.ug.popx.list` | 弹窗列表 | 空列表 |
| `mtop.jp.wishlist.item.add` | 添加心愿单 | 成功 |
| `mtop.jp.interaction.execute` | 交互执行 | 成功 |

### 拦截方式

拦截器会拦截以下 3 种请求方式：

1. **mtop.request()** - 阿里 MTOP 库的直接调用
2. **fetch()** - 原生 fetch API
3. **XMLHttpRequest** - 传统 XHR 请求

### 调试面板

页面右上角会显示一个调试面板，显示：
- ✅ Mock 是否激活
- 📊 拦截次数
- 🔌 已配置的 API 列表

---

## 🛠️ 自定义 Mock 数据

编辑 `mtop-mock.js` 中的 `MOCK_DATA` 对象：

```javascript
const MOCK_DATA = {
  'mtop.your.api.name': {
    ret: ['SUCCESS::调用成功'],
    v: '1.0',
    data: {
      // 你的 mock 数据
    }
  }
};
```

---

## 🔍 调试技巧

### 控制台日志

打开浏览器开发者工具，查看控制台日志：

```
[MTOP Mock] 拦截器加载开始...
[MTOP Mock] ✅ mtop.request 拦截成功
[MTOP Mock] ✅ fetch 拦截成功
[MTOP Mock] ✅ XHR 拦截成功
[MTOP Mock] 🎉 拦截器加载完成！
[MTOP Mock] 拦截请求：mtop.xxx.xxx
[MTOP Mock] ✅ 返回 mock 数据：mtop.xxx.xxx
```

### 监听 Mock 事件

```javascript
window.addEventListener('mtop-mock-response', (e) => {
  console.log('收到 mock 响应:', e.detail.api, e.detail.data);
});
```

### 查看拦截状态

```javascript
console.log(window.__MTOP_MOCK_STATUS__);
// 输出：
// {
//   enabled: true,
//   interceptedCount: 5,
//   mockedAPIs: [...],
//   lastAPI: 'mtop.xxx'
// }
```

---

## ⚠️ 注意事项

1. **加载顺序**: `mtop-mock.js` 必须在 `mtop.js` 之前加载
2. **CORS**: 本地运行时可能遇到 CORS 问题，建议使用 http-server
3. **缓存**: 修改 mock 数据后需要硬刷新 (Cmd+Shift+R)

---

## 🐛 故障排查

### Mock 不生效？

1. 检查控制台是否有 `[MTOP Mock]` 日志
2. 确认 `mtop-mock.js` 在 `mtop.js` 之前加载
3. 检查 API 名称是否完全匹配

### 页面不显示？

1. 检查网络连接（CDN 资源需要联网）
2. 查看控制台是否有 JS 错误
3. 确认 `#ice-container` 存在

---

## 📝 下一步

1. 启动本地服务器
2. 访问 http://localhost:8080
3. 打开控制台查看拦截日志
4. 根据需要修改 mock 数据

🐾 祝调试顺利！
