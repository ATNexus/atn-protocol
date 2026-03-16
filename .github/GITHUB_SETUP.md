# GitHub 设置指南

## 快速开始

### 1. 创建GitHub仓库

```bash
# 初始化Git仓库
git init
git add .
git commit -m "Initial commit: ATN Protocol v1.0.0"

# 创建GitHub仓库并推送
git remote add origin https://github.com/yourusername/atn-protocol.git
git branch -M main
git push -u origin main
```

### 2. 配置GitHub Secrets

在仓库 Settings > Secrets and variables > Actions 中添加：

| Secret Name | Value | 说明 |
|------------|-------|------|
| `SOLANA_WALLET` | 你的Solana钱包JSON | 部署用钱包 |

**生成钱包JSON：**

```bash
solana-keygen new --no-passphrase --outfile deploy-wallet.json
cat deploy-wallet.json | base64
# 复制输出到Secret
```

### 3. 启用GitHub Actions

推送代码后，Actions自动启用：

```bash
git add .github/workflows/ci-cd.yml
git commit -m "Add CI/CD pipeline"
git push
```

### 4. 查看部署状态

- 访问: `https://github.com/yourusername/atn-protocol/actions`
- 每次push自动触发部署
- 部署完成后查看Program ID

## 工作流说明

### 自动触发条件

| 事件 | 触发工作流 |
|------|-----------|
| Push to main | Lint + Test + Deploy |
| Push to develop | Lint + Test |
| Pull Request | Lint + Test + Security Scan |
| Tag push (v*) | Full pipeline + Release |

### 输出产物

- **frontend-build**: React静态文件
- **deployment-info**: 部署信息 (Program ID等)
- **Security report**: 安全扫描结果

## 故障排除

### 部署失败

1. 检查钱包余额
   ```bash
   solana balance --url devnet <WALLET_ADDRESS>
   ```

2. 检查Secret配置
   - Settings > Secrets > SOLANA_WALLET

3. 查看Action日志
   - Actions tab > 失败的工作流 > 查看日志

### 前端构建失败

```bash
cd ATN_Marketplace_UI
npm install
npm run build
# 本地测试通过后再推送
```

## 下一步

部署成功后：

1. **验证部署**
   - 访问: https://explorer.solana.com
   - 搜索Program ID
   - 确认在Devnet

2. **前端部署**
   - 使用Vercel/Netlify部署React应用
   - 配置API endpoint

3. **监控**
   - 设置SolanaFM监控
   - 配置Discord通知

---

*配置完成时间: 2026-03-16*  
*CI/CD版本: v1.0.0*
