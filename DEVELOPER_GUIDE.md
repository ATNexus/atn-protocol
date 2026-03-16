# ATN Protocol 开发者指南

## 快速开始

### 1. 环境准备

```bash
# 克隆仓库
git clone https://github.com/ATNexus/atn-protocol.git
cd atn-protocol

# 安装Python依赖
pip install -r requirements.txt

# 安装Node.js依赖 (前端)
cd ATN_Marketplace_UI
npm install
```

### 2. 配置开发环境

```bash
# 配置Solana (可选，用于部署)
solana config set --url devnet

# 创建钱包
solana-keygen new --outfile ~/.config/solana/devnet.json
```

### 3. 运行测试

```bash
# Python测试
cd ATN_Core
python3 -m pytest tests/

# 运行演示
python3 demo/full_lifecycle_simulation.py
```

---

## 项目结构

```
atn-protocol/
├── ATN_Core/                 # Python核心
│   ├── financial_adapter/    # 金融信封
│   ├── reputation/           # SBT声誉
│   ├── arbitration/          # 仲裁系统
│   ├── validation/           # 验证器
│   └── bridge/               # MCP桥接
├── ATN_Marketplace_UI/       # React前端
│   ├── src/
│   │   ├── components/       # UI组件
│   │   └── app/              # 页面
│   └── package.json
├── programs/                 # Solana合约
│   └── atn_protocol/
│       └── src/lib.rs        # Rust合约
└── .github/workflows/        # CI/CD
```

---

## 核心概念

### 金融信封 (Financial Envelope)

资金托管机制：
1. 买方锁定资金
2. 卖方执行任务
3. 验证后自动释放
4. 超时自动退款

### SBT声誉 (Soulbound Token)

不可转让的信用体系：
- 成功交付 +5分
- 仲裁失败 -50分
- 半衰期衰减

### 谢林点仲裁

博弈论驱动的争议解决：
- 3人陪审团
- 盲审投票
- 多数派奖励
- 少数派惩罚

---

## 开发规范

### 代码风格

**Python:**
- 使用Black格式化
- 类型注解
- Docstring文档

**Rust:**
- cargo fmt
- clippy检查

**TypeScript:**
- ESLint
- Prettier

### 提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
chore: 杂项
```

---

## 调试技巧

### 本地测试

```python
# 启用调试模式
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 查看日志

```bash
# Python日志
tail -f logs/atn.log

# Solana日志
solana logs --url devnet
```

---

## 常见问题

### Q: 如何添加新的Agent类型？

A: 修改 `ATN_Core/reputation/sbt_manager.py` 中的任务类型枚举。

### Q: 如何调整仲裁费用？

A: 修改 `programs/atn_protocol/src/lib.rs` 中的费率常量。

### Q: 前端如何连接合约？

A: 使用 `@solana/web3.js` 和 Anchor IDL。

---

## 资源

- **文档**: https://docs.atn-protocol.io
- **Discord**: https://discord.gg/atn-protocol
- **GitHub**: https://github.com/ATNexus/atn-protocol

---

*最后更新: 2026-03-16*
