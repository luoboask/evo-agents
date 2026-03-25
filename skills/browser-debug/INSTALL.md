# browser-debug - 浏览器调试技能安装指南

**直接控制浏览器进行网页调试、截图、查看控制台日志。**

> 基于 Puppeteer，支持 Chrome/Chromium 自动化控制

---

## ⚡ 一键安装（推荐）

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/browser-debug

# 2. 安装依赖
npm install

# 3. 测试安装
node check.js http://example.com
```

**就这么简单！** 安装脚本会自动：
- ✅ 检查 Node.js 和 npm
- ✅ 安装 Puppeteer
- ✅ 下载 Chromium（首次运行）
- ✅ 验证安装

---

## 📋 安装前检查

### 必需

- ✅ Node.js 16+ 
- ✅ npm（随 Node.js 安装）
- ✅ 约 200MB 磁盘空间（Puppeteer + Chromium）
- ✅ 网络连接（首次安装需下载 Chromium）

### 可选

- ⭕ Chrome/Chromium（如已有可跳过下载）

---

## 🚀 详细安装步骤

### Step 1: 检查 Node.js

```bash
# 检查 Node.js 版本
node --version  # 需要 16+

# 检查 npm 版本
npm --version
```

### Step 2: 安装依赖

```bash
cd ~/.openclaw/workspace/skills/browser-debug

# 安装所有依赖（包括 Puppeteer）
npm install
```

**安装过程：**
```
added 50 packages in 30s

Puppeteer will download Chromium (~150MB)
```

### Step 3: 验证安装

```bash
# 运行基础检查
node check.js http://example.com

# 应该看到：
# ✅ 页面加载成功
# ✅ 标题：Example Domain
# ✅ 截图已保存
```

---

## 🔧 配置说明

### Puppeteer 配置

编辑 `debug.js` 或 `check.js` 中的配置（如需要）：

```javascript
const puppeteer = require('puppeteer');

const launchOptions = {
  headless: 'new',  // 无头模式
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage'
  ]
};
```

### 使用系统 Chrome（可选）

如果已有 Chrome，可配置使用系统浏览器：

```javascript
const launchOptions = {
  headless: 'new',
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  args: ['--no-sandbox']
};
```

---

## 📁 安装后的目录结构

```
~/.openclaw/workspace/skills/browser-debug/
├── SKILL.md              # 技能定义
├── INSTALL.md            # 本文件
├── package.json          # npm 配置
├── package-lock.json     # 依赖锁定
├── check.js              # 基础检查
├── check-structure.js    # 页面结构检查
├── check-mock.js         # Mock 检查
├── check-mock-raw.js     # Mock 原始数据检查
├── debug.js              # 调试主脚本
├── full-check.js         # 完整检查
├── node_modules/         # 依赖包
└── output/               # 输出目录（截图等）
```

---

## 🎯 常用命令

```bash
# 打开页面并调试
node debug.js open http://localhost:3000/category

# 查看控制台日志
node debug.js logs http://localhost:3000/category

# 截图
node debug.js screenshot http://localhost:3000

# 执行 JavaScript
node debug.js eval http://localhost:3000 "document.title"

# 查看网络请求
node debug.js requests http://localhost:3000

# 查看特定元素
node debug.js element http://localhost:3000 "#mock-debug-panel"

# 完整检查
node full-check.js http://localhost:3000
```

---

## ✅ 安装验证

运行以下命令验证安装：

```bash
# 1. 基础页面检查
node check.js http://example.com

# 2. 页面结构检查
node check-structure.js http://example.com

# 3. 截图测试
node debug.js screenshot http://example.com

# 4. 检查输出目录
ls -la output/
```

---

## ❓ 常见问题

### Q: 安装时提示 "Permission denied"

**A:** 检查目录权限：

```bash
chmod -R 755 ~/.openclaw/workspace/skills/browser-debug
```

### Q: Puppeteer 下载 Chromium 失败

**A:** 网络问题，可手动指定 Chromium 路径或使用国内镜像：

```bash
# 使用国内镜像
export PUPPETEER_DOWNLOAD_HOST=https://npmmirror.com/mirrors
npm install puppeteer
```

或使用已有 Chrome：
```javascript
// 修改 debug.js
executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
```

### Q: 运行时提示 "Cannot find module 'puppeteer'"

**A:** 重新安装依赖：

```bash
cd ~/.openclaw/workspace/skills/browser-debug
rm -rf node_modules package-lock.json
npm install
```

### Q: 浏览器无法启动

**A:** 检查系统依赖（Linux）：

```bash
# Ubuntu/Debian
sudo apt-get install -y \
  libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 \
  libxi6 libxtst6 libnss3 libcups2 libxss1 libxrandr2 \
  libgconf2-4 libasound2 libatk1.0-0 libgtk-3-0
```

macOS 通常无需额外依赖。

### Q: 如何卸载技能？

**A:** 删除技能目录：

```bash
rm -rf ~/.openclaw/workspace/skills/browser-debug
```

---

## 📚 相关技能

| 技能 | 说明 |
|------|------|
| **browser-test** | 浏览器测试（简化版） |
| **browser-debug** | 浏览器调试（完整版） |

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| **SKILL.md** | 技能定义和用法详解 |
| **INSTALL.md** | 本文件 - 安装指南 |
| **debug.js** | 调试主脚本（内嵌帮助） |

---

## 🆘 获取帮助

遇到问题？

1. 运行 `node check.js http://example.com` 检查安装
2. 查看 Puppeteer 文档：https://pptr.dev/
3. 检查技能的 `SKILL.md` 文件
4. 在 OpenClaw 社区提问：https://discord.com/invite/clawd

---

## 📝 更新日志

- **2026-03-22**: 创建独立安装文档
- **2026-03-17**: browser-debug 技能创建

---

**最后更新：** 2026-03-22  
**版本：** 1.0.0  
**工作区：** /Users/dhr/.openclaw/workspace  
**作者：** OpenClaw Assistant
