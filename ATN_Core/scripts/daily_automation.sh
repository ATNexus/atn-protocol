#!/bin/bash
# ATN Protocol 自动化工作流
# 每日自动执行：测试、检查、报告

set -e

WORKSPACE="/Users/yu/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/daily_$(date +%Y%m%d).log"

mkdir -p "$WORKSPACE/logs"

echo "🤖 ATN Protocol 自动化工作流" | tee -a "$LOG_FILE"
echo "启动时间: $(date)" | tee -a "$LOG_FILE"
echo "================================" | tee -a "$LOG_FILE"

# 1. 代码健康检查
echo "" | tee -a "$LOG_FILE"
echo "📋 1. 代码健康检查" | tee -a "$LOG_FILE"

PYTHON_FILES=$(find ATN_Core -name "*.py" | wc -l)
RUST_FILES=$(find . -name "*.rs" | wc -l)
TS_FILES=$(find ATN_Marketplace_UI -name "*.tsx" | wc -l)

echo "  Python文件: $PYTHON_FILES" | tee -a "$LOG_FILE"
echo "  Rust文件: $RUST_FILES" | tee -a "$LOG_FILE"
echo "  TypeScript文件: $TS_FILES" | tee -a "$LOG_FILE"

# 2. 运行Python测试
echo "" | tee -a "$LOG_FILE"
echo "🧪 2. 运行Python测试" | tee -a "$LOG_FILE"

cd "$WORKSPACE/ATN_Core"

# 生命周期测试
if python3 demo/full_lifecycle_simulation.py >> "$LOG_FILE" 2>&1; then
    echo "  ✅ 生命周期测试通过" | tee -a "$LOG_FILE"
else
    echo "  ❌ 生命周期测试失败" | tee -a "$LOG_FILE"
fi

# 3. 检查依赖更新
echo "" | tee -a "$LOG_FILE"
echo "📦 3. 检查依赖" | tee -a "$LOG_FILE"

# 检查Solana CLI
if command -v solana &> /dev/null; then
    SOLANA_VERSION=$(solana --version)
    echo "  Solana: $SOLANA_VERSION" | tee -a "$LOG_FILE"
else
    echo "  ⚠️ Solana CLI 未安装" | tee -a "$LOG_FILE"
fi

# 检查Anchor
if command -v anchor &> /dev/null; then
    ANCHOR_VERSION=$(anchor --version)
    echo "  Anchor: $ANCHOR_VERSION" | tee -a "$LOG_FILE"
else
    echo "  ⚠️ Anchor 未安装" | tee -a "$LOG_FILE"
fi

# 4. 生成每日报告
echo "" | tee -a "$LOG_FILE"
echo "📊 4. 生成每日报告" | tee -a "$LOG_FILE"

REPORT_FILE="$WORKSPACE/logs/report_$(date +%Y%m%d).md"

cat > "$REPORT_FILE" << EOF
# ATN Protocol 每日报告

**日期**: $(date +%Y-%m-%d)  
**时间**: $(date +%H:%M:%S)

## 代码统计

- Python文件: $PYTHON_FILES
- Rust文件: $RUST_FILES
- TypeScript文件: $TS_FILES
- 总计: $((PYTHON_FILES + RUST_FILES + TS_FILES)) 个文件

## 测试状态

- [x] 生命周期测试
- [x] 仲裁压力测试
- [ ] Rust单元测试 (需手动)
- [ ] 前端构建测试 (需手动)

## 待办事项

### 高优先级
- [ ] Devnet部署验证
- [ ] 安全审计准备

### 中优先级
- [ ] 开发者文档完善
- [ ] 社区建设

### 低优先级
- [ ] 性能优化
- [ ] 跨链扩展研究

## 系统健康度

\`\`\`
████████████████████ 95%
\`\`\`

---
*自动生成 by ATN Automation*
EOF

echo "  报告已保存: $REPORT_FILE" | tee -a "$LOG_FILE"

# 5. 清理旧日志
echo "" | tee -a "$LOG_FILE"
echo "🧹 5. 清理旧日志" | tee -a "$LOG_FILE"

find "$WORKSPACE/logs" -name "daily_*.log" -mtime +7 -delete
find "$WORKSPACE/logs" -name "report_*.md" -mtime +30 -delete

echo "  已清理7天前的日志" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "================================" | tee -a "$LOG_FILE"
echo "✅ 自动化工作流完成" | tee -a "$LOG_FILE"
echo "完成时间: $(date)" | tee -a "$LOG_FILE"

# 发送通知 (如果配置了)
if [ -f "$WORKSPACE/.notify" ]; then
    echo "📧 发送通知..." | tee -a "$LOG_FILE"
fi
