#!/bin/bash
# ATN Marketplace UI 初始化脚本
# 安装shadcn/ui组件和依赖

echo "🎨 ATN Marketplace UI 初始化"
echo "=============================="

cd "$(dirname "$0")"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    exit 1
fi

echo "📦 安装依赖..."
npm install

echo ""
echo "🎨 初始化shadcn/ui..."
npx shadcn-ui@latest init -y --defaults

echo ""
echo "🧩 安装组件..."
components=("button" "card" "input" "badge" "dialog" "dropdown-menu" "table" "tabs")

for component in "${components[@]}"; do
    echo "  Installing $component..."
    npx shadcn-ui@latest add $component -y
done

echo ""
echo "🔗 安装Solana钱包适配器..."
npm install @solana/wallet-adapter-react @solana/wallet-adapter-react-ui @solana/wallet-adapter-wallets @solana/web3.js

echo ""
echo "✅ 初始化完成!"
echo ""
echo "启动开发服务器:"
echo "  npm run dev"
echo ""
echo "构建生产版本:"
echo "  npm run build"
