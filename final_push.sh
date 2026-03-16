#!/bin/bash
# ATN Protocol 最终推送脚本
# SSH已配置，等待仓库创建

echo "🚀 ATN Protocol GitHub推送"
echo "================================"
echo ""
echo "✅ SSH密钥已配置"
echo "✅ 认证成功: Hi ATNexus!"
echo ""
echo "❌ 仓库不存在: brianfokshelter/atn-protocol"
echo ""
echo "请手动创建仓库:"
echo ""
echo "1. 访问: https://github.com/new"
echo "2. 仓库名: atn-protocol"
echo "3. 描述: ATN Protocol - AgentTrust Nexus"
echo "4. 选择 Public"
echo "5. 点击 Create repository"
echo ""
echo "创建完成后，按回车继续推送..."
read

cd /Users/yu/.openclaw/workspace

echo ""
echo "正在推送..."
git remote set-url origin git@github.com:brianfokshelter/atn-protocol.git
git push -u origin main

echo ""
echo "✅ 推送完成!"
echo ""
echo "查看仓库: https://github.com/brianfokshelter/atn-protocol"
echo "查看Actions: https://github.com/brianfokshelter/atn-protocol/actions"
