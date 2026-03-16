#!/bin/bash
# ATN Protocol 一键部署脚本 (优化版)
# 支持本地、Devnet、Mainnet部署

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
NETWORK="${1:-devnet}"  # 默认devnet
PROGRAM_NAME="atn_protocol"
WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"

echo "🚀 ATN Protocol 部署脚本"
echo "========================"
echo "网络: $NETWORK"
echo ""

# 检查依赖
check_dependencies() {
    echo "📋 检查依赖..."
    
    if ! command -v solana &> /dev/null; then
        echo -e "${RED}❌ Solana CLI 未安装${NC}"
        echo "安装: sh -c \"\$(curl -sSfL https://release.solana.com/v1.17.0/install)\""
        exit 1
    fi
    
    if ! command -v anchor &> /dev/null; then
        echo -e "${RED}❌ Anchor 未安装${NC}"
        echo "安装: npm install -g @coral-xyz/anchor-cli"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 依赖检查通过${NC}"
}

# 设置网络
setup_network() {
    echo ""
    echo "🌐 设置网络: $NETWORK"
    
    case $NETWORK in
        devnet)
            solana config set --url devnet
            ;;
        mainnet)
            solana config set --url mainnet-beta
            echo -e "${YELLOW}⚠️  主网部署，请确认${NC}"
            read -p "按回车继续..."
            ;;
        *)
            echo -e "${RED}❌ 未知网络: $NETWORK${NC}"
            exit 1
            ;;
    esac
    
    echo -e "${GREEN}✅ 网络设置完成${NC}"
}

# 检查钱包
check_wallet() {
    echo ""
    echo "👛 检查钱包..."
    
    WALLET_PUBKEY=$(solana-keygen pubkey)
    echo "钱包地址: $WALLET_PUBKEY"
    
    BALANCE=$(solana balance)
    echo "余额: $BALANCE SOL"
    
    if (( $(echo "$BALANCE < 0.5" | bc -l) )); then
        echo -e "${YELLOW}⚠️  余额不足，请求空投...${NC}"
        solana airdrop 2 || echo "空投可能受限"
    fi
}

# 构建程序
build_program() {
    echo ""
    echo "🔨 构建程序..."
    
    cd "$WORKSPACE/programs/atn_protocol"
    
    anchor build
    
    echo -e "${GREEN}✅ 构建完成${NC}"
}

# 部署程序
deploy_program() {
    echo ""
    echo "📤 部署程序..."
    
    cd "$WORKSPACE/programs/atn_protocol"
    
    # 部署并捕获输出
    DEPLOY_OUTPUT=$(anchor deploy --provider.cluster $NETWORK 2>&1)
    echo "$DEPLOY_OUTPUT"
    
    # 提取Program ID
    PROGRAM_ID=$(echo "$DEPLOY_OUTPUT" | grep "Program Id:" | awk '{print $3}')
    
    if [ -n "$PROGRAM_ID" ]; then
        echo ""
        echo -e "${GREEN}✅ 部署成功!${NC}"
        echo "Program ID: $PROGRAM_ID"
        
        # 保存部署信息
        cat > "$WORKSPACE/deployment_$NETWORK.json" << EOF
{
  "network": "$NETWORK",
  "program_id": "$PROGRAM_ID",
  "deployed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "wallet": "$WALLET_PUBKEY"
}
EOF
        
        echo ""
        echo "查看合约:"
        echo "  https://explorer.solana.com/address/$PROGRAM_ID?cluster=$NETWORK"
    else
        echo -e "${RED}❌ 部署失败${NC}"
        exit 1
    fi
}

# 验证部署
verify_deployment() {
    echo ""
    echo "🔍 验证部署..."
    
    solana program show "$PROGRAM_ID"
    
    echo -e "${GREEN}✅ 验证完成${NC}"
}

# 主流程
main() {
    check_dependencies
    setup_network
    check_wallet
    build_program
    deploy_program
    verify_deployment
    
    echo ""
    echo "========================"
    echo -e "${GREEN}🎉 部署完成!${NC}"
    echo "========================"
    echo ""
    echo "网络: $NETWORK"
    echo "Program ID: $PROGRAM_ID"
    echo "部署记录: deployment_$NETWORK.json"
    echo ""
}

# 执行
main
