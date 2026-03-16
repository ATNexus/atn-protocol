#!/bin/bash
# ATN Protocol Devnet 部署执行脚本
# 网络权限已批准

set -e

WORKSPACE="/Users/yu/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/deploy_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "$WORKSPACE/logs"

echo "🚀 ATN Protocol Devnet 部署" | tee -a "$LOG_FILE"
echo "================================" | tee -a "$LOG_FILE"
echo "开始时间: $(date)" | tee -a "$LOG_FILE"
echo ""

# 检查网络连接
echo "🌐 检查网络连接..." | tee -a "$LOG_FILE"
if curl -s https://api.devnet.solana.com > /dev/null; then
    echo "✅ Devnet RPC 可访问" | tee -a "$LOG_FILE"
else
    echo "❌ 无法连接到Devnet" | tee -a "$LOG_FILE"
    exit 1
fi

# 检查Solana CLI
if ! command -v solana &> /dev/null; then
    echo "📥 安装Solana CLI..." | tee -a "$LOG_FILE"
    sh -c "$(curl -sSfL https://release.solana.com/v1.17.0/install)"
    export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"
fi

# 设置Devnet
solana config set --url devnet | tee -a "$LOG_FILE"

# 检查/创建钱包
if [ ! -f "$HOME/.config/solana/id.json" ]; then
    echo "👛 创建新钱包..." | tee -a "$LOG_FILE"
    solana-keygen new --no-passphrase -o "$HOME/.config/solana/id.json"
fi

WALLET_PUBKEY=$(solana-keygen pubkey)
echo "钱包地址: $WALLET_PUBKEY" | tee -a "$LOG_FILE"

# 检查余额
BALANCE=$(solana balance 2>/dev/null || echo "0")
echo "当前余额: $BALANCE SOL" | tee -a "$LOG_FILE"

if (( $(echo "$BALANCE < 2" | bc -l) )); then
    echo "💰 请求空投..." | tee -a "$LOG_FILE"
    solana airdrop 2 || echo "⚠️ 空投可能受限，请手动充值"
    sleep 2
fi

# 模拟部署 (实际合约需要Rust编译环境)
echo "" | tee -a "$LOG_FILE"
echo "📦 准备部署..." | tee -a "$LOG_FILE"

# 创建模拟部署记录
cat > "$WORKSPACE/deployment_devnet.json" << EOF
{
  "network": "devnet",
  "status": "simulated",
  "wallet": "$WALLET_PUBKEY",
  "balance": "$BALANCE",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "note": "实际部署需要Rust/Anchor环境",
  "next_steps": [
    "安装Anchor: npm install -g @coral-xyz/anchor-cli",
    "构建合约: anchor build",
    "部署: anchor deploy --provider.cluster devnet"
  ]
}
EOF

echo "" | tee -a "$LOG_FILE"
echo "✅ 部署准备完成" | tee -a "$LOG_FILE"
echo "📄 部署信息: deployment_devnet.json" | tee -a "$LOG_FILE"
echo ""
echo "📝 手动部署命令:" | tee -a "$LOG_FILE"
echo "   anchor build" | tee -a "$LOG_FILE"
echo "   anchor deploy --provider.cluster devnet" | tee -a "$LOG_FILE"
echo ""
echo "完成时间: $(date)" | tee -a "$LOG_FILE"
