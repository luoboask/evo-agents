# 导购×营销联调自动化工作流 - 案例演示

## 📁 目录结构

```
case-demo/
├── step1-env/           # Step 1: 环境准备
├── step2-data/          # Step 2: 数据构造
├── step3-verify/        # Step 3: 场景验证
├── step4-debug/         # Step 4: 问题排查
├── step5-fix/           # Step 5: 自动修复
├── step6-regression/    # Step 6: 回归验证
├── step7-report/        # Step 7: 报告生成
├── scripts/             # 脚本工具
├── logs/                # 日志文件
└── README.md            # 本文档
```

## 🚀 快速开始

### 方式 1: 执行完整流程
```bash
cd /Users/dhr/.openclaw/workspace/projects/integration-sandbox/case-demo
./scripts/run-full-flow.sh
```

### 方式 2: 分步执行
```bash
# Step 1: 环境准备
./scripts/step1-env.sh

# Step 2: 数据构造
./scripts/step2-data.sh

# ... 依此类推
```

## 📊 流程说明

| 步骤 | 名称 | 说明 | 预计时间 |
|------|------|------|---------|
| Step 1 | 环境准备 | 启动 Java 服务、前端服务器 | 30 秒 |
| Step 2 | 数据构造 | 生成 Mock 数据 | 10 秒 |
| Step 3 | 场景验证 | 验证页面显示 | 20 秒 |
| Step 4 | 问题排查 | 检查并记录问题 | 15 秒 |
| Step 5 | 自动修复 | 修复发现的问题 | 30 秒 |
| Step 6 | 回归验证 | 验证修复结果 | 20 秒 |
| Step 7 | 报告生成 | 生成联调报告 | 10 秒 |

**总预计时间**: 约 2-3 分钟

## ✅ 完成标准

- [x] Java Mock 服务启动成功
- [x] 前端开发服务器启动成功
- [x] MTOP 拦截器工作正常
- [x] 商品卡片正常显示（2 个卡片，8 个商品）
- [x] 推荐区域正常显示（2 个推荐商品）
- [x] 所有商品图片、标题、价格正常显示
- [x] 联调报告生成成功

## 📝 日志查看

所有日志保存在 `logs/` 目录下：
- `step1-env.log` - 环境准备日志
- `step2-data.log` - 数据构造日志
- `step3-verify.log` - 场景验证日志
- `step4-debug.log` - 问题排查日志
- `step5-fix.log` - 自动修复日志
- `step6-regression.log` - 回归验证日志
- `step7-report.log` - 报告生成日志
- `full-flow.log` - 完整流程日志

## 🎯 通知方式

每步完成后会发送通知：
- 控制台输出：`✅ Step X: XXX 完成`
- 日志文件：`logs/stepX-xxx.log`
- 最终报告：`step7-report/final-report.md`
