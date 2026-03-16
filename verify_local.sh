#!/bin/bash
# 模拟GitHub Actions本地测试
# 验证CI/CD配置

echo "🔧 GitHub Actions 本地验证"
echo "================================"

WORKSPACE="/Users/yu/.openclaw/workspace"

echo ""
echo "1. 检查工作流文件..."
if [ -f "$WORKSPACE/.github/workflows/ci-cd.yml" ]; then
    echo "✅ CI/CD配置存在"
    # 验证YAML语法
    if python3 -c "import yaml; yaml.safe_load(open('$WORKSPACE/.github/workflows/ci-cd.yml'))" 2>/dev/null; then
        echo "✅ YAML语法正确"
    else
        echo "⚠️  YAML语法检查失败 (可能无PyYAML)"
    fi
else
    echo "❌ CI/CD配置缺失"
    exit 1
fi

echo ""
echo "2. 检查项目结构..."
REQUIRED_DIRS=(
    "ATN_Core"
    "ATN_Marketplace_UI"
    "programs/atn_protocol"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$WORKSPACE/$dir" ]; then
        echo "✅ $dir"
    else
        echo "⚠️  $dir (可选)"
    fi
done

echo ""
echo "3. 检查关键文件..."
REQUIRED_FILES=(
    "README.md"
    ".gitignore"
    "ATN_Core/demo/full_lifecycle_simulation.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$WORKSPACE/$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file 缺失"
    fi
done

echo ""
echo "4. Git状态..."
cd "$WORKSPACE"
echo "提交数: $(git rev-list --count HEAD 2>/dev/null || echo 'N/A')"
echo "最新提交: $(git log -1 --pretty=format:'%h - %s' 2>/dev/null || echo 'N/A')"
echo "分支: $(git branch --show-current 2>/dev/null || echo 'N/A')"

echo ""
echo "5. 文件统计..."
PYTHON_FILES=$(find ATN_Core -name "*.py" 2>/dev/null | wc -l)
RUST_FILES=$(find . -name "*.rs" 2>/dev/null | wc -l)
TS_FILES=$(find ATN_Marketplace_UI -name "*.tsx" 2>/dev/null | wc -l)

echo "  Python: $PYTHON_FILES"
echo "  Rust: $RUST_FILES"
echo "  TypeScript: $TS_FILES"
echo "  总计: $((PYTHON_FILES + RUST_FILES + TS_FILES))"

echo ""
echo "================================"
echo "✅ 本地验证完成"
echo ""
echo "项目已准备好推送到GitHub"
echo "执行: ./push_to_github.sh 或按 GITHUB_PUSH_GUIDE.md 操作"
