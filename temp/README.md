# Temp/ - 临时脚本目录

**用途：** 存放临时脚本、测试代码、一次性工具

---

## 📝 使用规则

### 命名规范

1. **日期命名** (推荐)
   ```
   2026-03-23_test_embedding.py
   2026-03-24_migrate_data.py
   ```

2. **用途命名 + .tmp 后缀**
   ```
   debug_memory.tmp.py
   quick_fix.tmp.py
   ```

3. **描述性命名**
   ```
   test_new_feature.py
   benchmark_search.py
   ```

---

## 🗑️ 清理规则

**自动清理 (建议配置 cron):**
```bash
# 删除超过 7 天的临时脚本
find temp/ -name "*.py" -mtime +7 -delete

# 或删除所有 .tmp 文件
rm temp/*.tmp.py
```

**手动清理:**
```bash
# 查看临时脚本
ls -lt temp/

# 删除指定文件
rm temp/2026-03-20_*.py

# 清空整个目录
rm temp/*.py
```

---

## 📋 使用场景

- ✅ 临时修复脚本
- ✅ 测试/实验代码
- ✅ 调试工具
- ✅ 一次性数据转换
- ✅ 快速原型验证

- ❌ 长期使用的工具 (应移到 `scripts/`)
- ❌ 正式功能代码 (应移到 `skills/` 或 `libs/`)
- ❌ 重要数据 (应移到 `data/`)

---

## 🔄 工作流

1. **创建临时脚本**
   ```bash
   touch temp/2026-03-23_my_test.py
   ```

2. **测试/执行**
   ```bash
   python3 temp/2026-03-23_my_test.py
   ```

3. **清理**
   - 有用 → 移到 `scripts/` 或相应目录
   - 无用 → 删除

---

**最后清理时间：** 2026-03-23  
**下次清理时间：** 2026-03-30 (建议每周清理)
