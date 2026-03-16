#!/bin/bash
# ATN Protocol Devnet 部署脚本
# 使用方法: ./deploy_devnet.sh

set -e

echo "🚀 ATN Protocol Devnet 部署脚本"
echo "================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查依赖
echo ""
echo "📋 检查依赖..."

if ! command -v solana &> /dev/null; then
    echo "${RED}❌ Solana CLI 未安装${NC}"
    echo "请安装: https://docs.solana.com/cli/install-solana-cli-tools"
    exit 1
fi

if ! command -v anchor &> /dev/null; then
    echo "${RED}❌ Anchor CLI 未安装${NC}"
    echo "请安装: npm install -g @coral-xyz/anchor-cli"
    exit 1
fi

echo "${GREEN}✅ 依赖检查通过${NC}"

# 设置网络
echo ""
echo "🌐 设置网络为 Devnet..."
solana config set --url devnet

# 检查钱包
echo ""
echo "👛 检查钱包..."
WALLET_PUBKEY=$(solana-keygen pubkey 2>/dev/null || echo "")

if [ -z "$WALLET_PUBKEY" ]; then
    echo "${YELLOW}⚠️ 未找到钱包，创建新钱包...${NC}"
    solana-keygen new --no-passphrase -o ~/.config/solana/id.json
    WALLET_PUBKEY=$(solana-keygen pubkey)
fi

echo "钱包地址: $WALLET_PUBKEY"

# 检查余额
echo ""
echo "💰 检查余额..."
BALANCE=$(solana balance 2>/dev/null || echo "0")
echo "当前余额: $BALANCE SOL"

if (( $(echo "$BALANCE < 2" | bc -l) )); then
    echo "${YELLOW}⚠️ 余额不足，正在请求空投...${NC}"
    solana airdrop 2
    sleep 2
    BALANCE=$(solana balance)
    echo "新余额: $BALANCE SOL"
fi

# 构建合约
echo ""
echo "🔨 构建合约..."
cd programs/atn_protocol

cargo build-bpf 2>&1 | tee build.log

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "${RED}❌ 构建失败${NC}"
    exit 1
fi

echo "${GREEN}✅ 构建成功${NC}"

# 部署合约
echo ""
echo "📤 部署合约到 Devnet..."

cd ../../

# 使用 Anchor 部署
anchor deploy --provider.cluster devnet 2>&1 | tee deploy.log

# 提取程序ID
PROGRAM_ID=$(grep "Program Id:" deploy.log | awk '{print $3}')

if [ -z "$PROGRAM_ID" ]; then
    echo "${RED}❌ 部署失败，无法获取程序ID${NC}"
    exit 1
fi

echo "${GREEN}✅ 部署成功!${NC}"
echo "程序ID: $PROGRAM_ID"

# 更新程序ID
echo ""
echo "📝 更新程序ID..."
sed -i.bak "s/declare_id!(\".*\")/declare_id!(\"$PROGRAM_ID\")/" programs/atn_protocol/src/lib.rs

echo "${GREEN}✅ 程序ID已更新${NC}"

# 初始化程序
echo ""
echo "🔧 初始化程序..."

# 创建初始化指令
solana program show $PROGRAM_ID

# 验证部署
echo ""
echo "✅ 验证部署..."
solana program show $PROGRAM_ID | grep "Program"

echo ""
echo "${GREEN}================================${NC}"
echo "${GREEN}🎉 ATN Protocol 部署完成!${NC}"
echo "${GREEN}================================${NC}"
echo ""
echo "程序ID: $PROGRAM_ID"
echo "网络: Devnet"
echo ""
echo "下一步:"
echo "1. 更新前端配置中的程序ID"
echo "2. 运行测试: anchor test"
echo "3. 启动前端: cd ATN_Marketplace_UI && npm run dev"
echo ""

# 保存部署信息
cat > deployment_info.json << EOF
{
  "network": "devnet",
  "program_id": "$PROGRAM_ID",
  "deployed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "deployer": "$WALLET_PUBKEY"
}
EOF

echo "部署信息已保存到: deployment_info.json"
