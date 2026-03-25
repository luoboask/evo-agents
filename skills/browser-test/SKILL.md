# Browser Test Skill - 浏览器测试技能

## 描述

使用 Puppeteer 访问网页、截图、获取控制台日志、执行 JavaScript。

## 功能

1. **访问页面** - 打开指定 URL
2. **截图** - 保存页面截图
3. **获取日志** - 收集控制台日志
4. **执行 JS** - 在页面上下文中执行 JavaScript
5. **获取内容** - 获取页面 HTML 或特定元素内容

## 使用方法

```bash
# 访问页面并截图
browser-test open http://localhost:3000/category --screenshot

# 获取控制台日志
browser-test logs http://localhost:3000/category

# 执行 JavaScript
browser-test eval http://localhost:3000/category "document.title"

# 获取元素内容
browser-test element http://localhost:3000/category "#mock-panel"
```

## 安装依赖

```bash
npm install puppeteer
```

## 注意事项

- 需要安装 Chrome/Chromium
- 首次运行会下载 Chromium
