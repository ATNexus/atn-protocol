# SSH密钥创建与GitHub配置教程

## 快速创建 (2分钟)

### 步骤1: 生成SSH密钥

打开终端，执行：

```bash
# 生成ED25519密钥 (推荐)
ssh-keygen -t ed25519 -C "brianfokshelter@gmail.com" -f ~/.ssh/id_ed25519

# 或生成RSA密钥 (兼容性好)
# ssh-keygen -t rsa -b 4096 -C "brianfokshelter@gmail.com"
```

**执行后会提示：**
```
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase): [直接回车，不设置密码]
Enter same passphrase again: [直接回车]
```

### 步骤2: 查看公钥

```bash
cat ~/.ssh/id_ed25519.pub
```

**输出示例：**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDIhz2GK/XCUj4i6Q5yQJNL1MXMY0RxzPV2QrBqfHrDq brianfokshelter@gmail.com
```

**复制这整行内容** (包括ssh-ed25519开头和邮箱结尾)

### 步骤3: 添加到GitHub

1. 访问: https://github.com/settings/keys
2. 点击 **"New SSH key"**
3. **Title**: `My MacBook` (任意名称)
4. **Key type**: Authentication Key
5. **Key**: 粘贴刚才复制的公钥内容
6. 点击 **"Add SSH key"**

### 步骤4: 测试连接

```bash
ssh -T git@github.com
```

**看到以下提示表示成功：**
```
Hi brianfokshelter! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## 使用SSH推送代码

```bash
cd /Users/yu/.openclaw/workspace

# 设置SSH远程地址
git remote set-url origin git@github.com:brianfokshelter/atn-protocol.git

# 推送
git push -u origin main
```

---

## 常见问题

### 权限错误

```bash
# 确保SSH agent运行
eval "$(ssh-agent -s)"

# 添加密钥
ssh-add ~/.ssh/id_ed25519
```

### 密钥位置

- 私钥: `~/.ssh/id_ed25519` (保密，不要分享)
- 公钥: `~/.ssh/id_ed25519.pub` (可以分享，用于添加到GitHub)

---

## 验证步骤

执行完上述步骤后，告诉我：

1. ✅ 密钥已生成
2. ✅ 已添加到GitHub
3. ✅ 测试连接成功

然后我立即执行推送。
