# GitHub Token 生成指南

## 重要说明

GitHub已于2021年8月禁用密码认证，必须使用 **Personal Access Token**。

---

## 快速生成Token (2分钟)

### 步骤1: 访问Token设置
打开: https://github.com/settings/tokens

### 步骤2: 生成新Token
1. 点击 **"Generate new token (classic)"**
2. 输入Note: `ATN Protocol Deploy`
3. 有效期: 选择 **30天** 或 **No expiration**
4. 勾选以下权限:
   - ✅ **repo** (完整仓库访问)
   - ✅ **workflow** (Actions工作流)

### 步骤3: 生成并复制
- 点击 **Generate token**
- **立即复制Token** (只显示一次!)
- Token格式: `ghp_xxxxxxxxxxxxxxxxxxxx`

---

## 使用Token推送

将Token发给我，我立即执行推送：

```bash
git remote set-url origin https://TOKEN@github.com/brianfokshelter/atn-protocol.git
git push -u origin main
```

---

## 安全提示

⚠️ **Token安全**: 
- Token等同于密码，请妥善保管
- 建议设置30天有效期
- 推送完成后可在GitHub删除Token

⚠️ **密码已禁用**:
- 您提供的密码 `ilovexdf1!` 无法用于Git操作
- 这是GitHub的安全策略，非技术问题

---

## 替代方案: GitHub Desktop (无需Token)

如果不想使用Token：

1. 下载: https://desktop.github.com
2. 登录GitHub账号
3. File > Add local repository
4. 选择: `/Users/yu/.openclaw/workspace`
5. 点击 Publish repository

---

**请生成Token后发送给我，立即完成推送。**
