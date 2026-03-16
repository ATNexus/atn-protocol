#!/bin/bash
# ATN Protocol GitHub推送脚本
# 自动创建仓库并推送

set -e

echo "🚀 ATN Protocol GitHub推送"
echo "================================"

# 检查GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "📥 安装GitHub CLI..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install gh
    else
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt update
        sudo apt install gh
    fi
fi

# 检查登录状态
if ! gh auth status &> /dev/null; then
    echo ""
    echo "🔑 请登录GitHub:"
    gh auth login
fi

# 获取用户名
USERNAME=$(gh api user -q '.login')
echo ""
echo "👤 GitHub用户: $USERNAME"

# 创建仓库
echo ""
echo "📦 创建GitHub仓库..."
REPO_NAME="atn-protocol"

if gh repo view "$USERNAME/$REPO_NAME" &> /dev/null; then
    echo "⚠️  仓库已存在，使用现有仓库"
else
    gh repo create "$REPO_NAME" --public --description "ATN Protocol - AgentTrust Nexus" --source=. --remote=origin --push
    echo "✅ 仓库创建成功"
fi

# 配置远程
git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git" 2>/dev/null || true

# 推送代码
echo ""
echo "📤 推送代码到GitHub..."
git push -u origin main --force

echo ""
echo "✅ 推送完成!"
echo ""
echo "仓库地址: https://github.com/$USERNAME/$REPO_NAME"
echo "Actions: https://github.com/$USERNAME/$REPO_NAME/actions"
echo ""
echo "📝 下一步:"
echo "1. 访问仓库Settings > Secrets"
echo "2. 添加SOLANA_WALLET secret"
echo "3. 推送任意代码触发部署"
