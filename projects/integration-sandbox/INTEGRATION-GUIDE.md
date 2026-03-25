# 导购×营销联调自动化工作流 - 完整指南

> 从前端 Mock 到自动化联调的完整解决方案

---

## 📋 目录

1. [环境准备](#1-环境准备)
2. [前端沙箱](#2-前端沙箱)
3. [Mock 配置](#3-mock-配置)
4. [联调流程](#4-联调流程)
5. [故障排查](#5-故障排查)

---

## 1. 环境准备

### 1.1 目录结构

```
integration-sandbox/
├── frontend-sandbox/       # 前端沙箱
│   ├── index.html         # 前端入口（注入 mock）
│   ├── mtop-mock.js       # MTOP 拦截器
│   ├── start.sh           # 启动脚本
│   └── README.md
├── mockData.txt           # 完整 mock 数据
├── MTOP-MOCK-README.md    # Mock 说明
└── INTEGRATION-GUIDE.md   # 本文档
```

### 1.2 依赖检查

```bash
# 检查 Python
python3 --version

# 检查 Node.js
node --version

# 检查 http-server (可选)
http-server --version
```

---

## 2. 前端沙箱

### 2.1 快速启动

```bash
cd /Users/dhr/.openclaw/workspace/projects/integration-sandbox/frontend-sandbox

# 方式 1: 使用启动脚本
./start.sh

# 方式 2: 手动启动
python3 -m http.server 8080
```

### 2.2 访问页面

打开浏览器访问：http://localhost:8080

### 2.3 验证 Mock

打开浏览器控制台，应该看到：

```
[MTOP Mock] 拦截器加载开始...
[MTOP Mock] ✅ mtop.request 拦截成功
[MTOP Mock] ✅ fetch 拦截成功
[MTOP Mock] ✅ XHR 拦截成功
[MTOP Mock] 🎉 拦截器加载完成！
[MTOP Mock] 已配置 API: ['mtop.relationrecommend...', ...]
```

右上角会显示调试面板，显示拦截状态。

---

## 3. Mock 配置

### 3.1 默认 Mock API

| API | 用途 | 返回数据 |
|-----|------|----------|
| `mtop.relationrecommend.tiantaojprecommend.recommend` | 商品推荐 | 2 个商品 |
| `mtop.alibaba.jp.guide.page.get` | 导购页面 | 空卡片 |
| `mtop.jptao.ug.popx.check` | 弹窗检查 | 成功 |
| `mtop.jptao.ug.popx.list` | 弹窗列表 | 空列表 |
| `mtop.jp.wishlist.item.add` | 心愿单 | 成功 |
| `mtop.jp.interaction.execute` | 交互 | 成功 |

### 3.2 添加新 Mock

编辑 `frontend-sandbox/mtop-mock.js`：

```javascript
const MOCK_DATA = {
  // ... 现有配置 ...
  
  // 添加新的 API
  'mtop.your.new.api': {
    ret: ['SUCCESS::调用成功'],
    v: '1.0',
    traceId: 'mock_' + Date.now(),
    data: {
      // 你的数据结构
      result: [],
      success: true
    }
  }
};
```

### 3.3 使用完整 Mock 数据

`mockData.txt` 包含完整的 mock 配置，包含：
- 商品详情
- 推荐列表
- 活动信息
- 用户数据

可以通过脚本提取并转换为 JavaScript 对象。

---

## 4. 联调流程

### 4.1 7 步工作流

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 环境准备 → Step 2: 数据构造 → Step 3: 场景验证  │
│       ↓                    ↓                    ↓       │
│  Step 7: 报告生成 ← Step 6: 回归验证 ← Step 5: 自动修复  │
│       ↓                    ↓                    ↓       │
│  服务配置 + 终端      商品 + 活动 + 用户      执行测试   │
│  完成！              生成完毕              排查问题     │
└─────────────────────────────────────────────────────────┘
```

### 4.2 详细步骤

#### Step 1: 环境准备
- ✅ 启动前端沙箱
- ✅ 配置 Mock 拦截器
- ✅ 验证页面可访问

```bash
cd frontend-sandbox
./start.sh 8080
# 访问 http://localhost:8080
```

#### Step 2: 数据构造
- 📦 生成商品数据（3 个）
- 🎯 生成活动数据（2 个）
- 👤 生成用户数据（2 个）

```javascript
// 在 mtap-mock.js 中配置
const MOCK_DATA = {
  'mtop.alibaba.jp.guide.page.get': {
    data: {
      products: [...],  // 商品
      activities: [...], // 活动
      users: [...]       // 用户
    }
  }
};
```

#### Step 3: 场景验证
执行测试场景：

| 场景 | 操作 | 预期 |
|------|------|------|
| 场景 1 | 浏览商品列表 | 显示 3 个商品 |
| 场景 2 | 点击商品详情 | 显示详情 |
| 场景 3 | 添加到心愿单 | 成功提示 |
| 场景 4 | 查看活动 | 显示活动信息 |
| 场景 5 | 用户登录 | 登录成功 |

#### Step 4: 问题排查
检查失败场景：
- 查看控制台日志
- 检查网络请求
- 分析错误信息

#### Step 5: 自动修复
根据问题类型自动修复：
- 数据格式错误 → 修正 mock 数据
- 接口不匹配 → 更新 API 映射
- UI 异常 → 调整前端配置

#### Step 6: 回归验证
重新执行所有场景，确认问题已修复。

#### Step 7: 报告生成
生成联调报告：

```markdown
# 联调报告

## 执行概况
- 总场景：5
- 通过：5
- 失败：0
- 修复：0

## 详情
✅ 场景 1: 浏览商品列表 - 通过
✅ 场景 2: 点击商品详情 - 通过
...
```

---

## 5. 故障排查

### 5.1 Mock 不生效

**症状**: 页面正常但请求到真实接口

**检查**:
1. 控制台是否有 `[MTOP Mock]` 日志
2. `mtop-mock.js` 是否在 `mtop.js` 之前加载
3. API 名称是否完全匹配

**解决**:
```html
<!-- 错误：mtop.js 在 mock 之前 -->
<script src="mtop.js"></script>
<script src="mtop-mock.js"></script>

<!-- 正确：mock 在 mtop.js 之前 -->
<script src="mtop-mock.js"></script>
<script src="mtop.js"></script>
```

### 5.2 页面不显示

**症状**: 白屏或 `#ice-container` 为空

**检查**:
1. 控制台是否有 JS 错误
2. CDN 资源是否加载成功
3. 网络连接是否正常

**解决**:
```bash
# 检查 CDN 可访问性
curl -I https://g.alicdn.com/jp-fe/jp-new-homepage-category-page/0.0.41/js/main.js
```

### 5.3 CORS 错误

**症状**: 控制台显示 CORS 错误

**解决**:
```bash
# 使用 http-server 并添加 CORS 头
http-server -p 8080 --cors
```

### 5.4 调试技巧

#### 查看拦截状态
```javascript
console.log(window.__MTOP_MOCK_STATUS__);
```

#### 监听 Mock 事件
```javascript
window.addEventListener('mtop-mock-response', (e) => {
  console.log('API:', e.detail.api);
  console.log('Data:', e.detail.data);
});
```

#### 手动触发 Mock
```javascript
// 测试 mtop.request
mtop.request('mtop.relationrecommend.tiantaojprecommend.recommend', {}, (err, data) => {
  console.log('Mock 响应:', data);
});
```

---

## 📝 下一步

1. ✅ 启动前端沙箱
2. ✅ 验证 Mock 拦截
3. 📋 根据需求调整 mock 数据
4. 🧪 执行联调测试
5. 📊 生成联调报告

---

## 🐾 支持

遇到问题？查看：
- `frontend-sandbox/README.md` - 前端沙箱详细说明
- `MTOP-MOCK-README.md` - Mock 配置说明
- `mockData.txt` - 完整 mock 数据示例

🎉 祝联调顺利！
