# Browser Debug Skill - 浏览器调试技能

## 描述

直接控制浏览器打开页面、查看控制台、截图、调试网页。

## 功能

1. **打开页面** - 使用 Puppeteer 打开指定 URL
2. **查看控制台** - 获取页面控制台日志
3. **截图** - 对页面截图
4. **执行 JS** - 在页面上下文中执行 JavaScript
5. **查看网络请求** - 监控网络请求和响应
6. **查看元素** - 获取页面元素信息

## 使用方法

```bash
# 打开页面并调试
browser-debug open http://localhost:3000/category

# 查看控制台日志
browser-debug logs

# 截图
browser-debug screenshot

# 执行 JS
browser-debug eval "document.title"

# 查看网络请求
browser-debug requests

# 查看特定元素
browser-debug element "#mock-debug-panel"
```

## 安装依赖

```bash
npm install puppeteer
```

## 注意事项

- 需要安装 Chrome/Chromium
- 首次运行会下载 Chromium
- 调试完成后记得关闭浏览器
