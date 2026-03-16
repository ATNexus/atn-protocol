# GitHub推送指南

## 快速推送 (请手动执行)

### 方法1: 使用GitHub网站

1. **创建仓库**
   - 访问: https://github.com/new
   - 仓库名: `atn-protocol`
   - 描述: `ATN Protocol - AgentTrust Nexus`
   - 选择 Public
   - 点击 Create repository

2. **推送代码**
   ```bash
   cd /Users/yu/.openclaw/workspace
   
   # 添加远程仓库
   git remote add origin https://github.com/YOUR_USERNAME/atn-protocol.git
   
   # 推送
   git push -u origin main
   ```

### 方法2: 使用SSH (推荐)

```bash
# 生成SSH密钥 (如果没有)
ssh-keygen -t ed25519 -C "your@email.com"

# 添加到GitHub
# 访问: https://github.com/settings/keys
# 点击 New SSH key
# 粘贴 ~/.ssh/id_ed25519.pub 内容

# 推送
git remote add origin git@github.com:YOUR_USERNAME/atn-protocol.git
git push -u origin main
```

## 配置GitHub Actions Secrets

推送后，配置部署密钥：

1. 访问: `https://github.com/YOUR_USERNAME/atn-protocol/settings/secrets/actions`

2. 点击 **New repository secret**

3. 添加以下Secrets:

| Name | Value | 获取方式 |
|------|-------|---------|
| `SOLANA_WALLET` | 钱包JSON内容 | 见下方 |

### 生成Solana钱包

```bash
# 安装Solana CLI后执行:
solana-keygen new --no-passphrase --outfile deploy-wallet.json

# 查看内容
cat deploy-wallet.json

# 复制完整JSON到Secret
```

## 验证部署

配置完成后：

1. **触发部署**
   - 修改任意文件并推送
   - 或访问 Actions 页面手动触发

2. **查看状态**
   - 访问: `https://github.com/YOUR_USERNAME/atn-protocol/actions`
   - 等待工作流完成

3. **获取Program ID**
   - 部署成功后，在Artifacts中下载 `deployment-info`
   - 或在日志中查找 "Program Id:"

## 故障排除

### 推送被拒绝

```bash
# 强制推送 (如果仓库为空)
git push -u origin main --force

# 或先拉取
git pull origin main --rebase
git push
```

### Actions失败

1. 检查Secrets配置
2. 查看Actions日志
3. 确认钱包有余额

---

**当前状态**: 代码已提交，等待推送到GitHub

**下一步**: 按上述步骤创建仓库并推送
