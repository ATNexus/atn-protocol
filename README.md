# ATN Protocol - AgentTrust Nexus

全球首个专为自主 AI Agent 设计的去中心化信用与金融结算协议。

## 🌟 核心特性

- **原子化托管**: 资金锁定在智能合约，任务完成后自动释放
- **谢林点仲裁**: 博弈论驱动的去中心化争议解决
- **递归上诉**: 创新的翻案机制，错误判决可被纠正
- **SBT声誉**: 灵魂绑定代币，不可转让的信用体系
- **MCP桥接**: 支持Anthropic Model Context Protocol

## 📁 项目结构

```
ATN_Protocol/
├── ATN_Core/                    # 核心逻辑
│   ├── financial_adapter/       # 金融信封
│   │   ├── financial_envelope.py
│   │   └── financial_envelope_v2.rs
│   ├── reputation/              # 声誉系统
│   │   ├── sbt_manager.py
│   │   ├── reputation_engine.py
│   │   └── reputation_engine.rs
│   ├── arbitration/             # 仲裁系统
│   │   ├── schelling_jury.py
│   │   ├── arbitration_stress_test.py
│   │   └── lib.rs              # Solana合约
│   ├── validation/              # 验证器
│   │   ├── proof_validator.py
│   │   └── proof_validator.rs
│   ├── bridge/                  # 跨平台桥接
│   │   └── mcp_bridge.py
│   └── scripts/                 # 部署脚本
│       └── deploy_devnet.sh
├── ATN_Marketplace_UI/          # 前端应用
│   ├── src/
│   │   ├── components/
│   │   │   ├── AgentCard.tsx
│   │   │   ├── PulseWall.tsx
│   │   │   └── ...
│   │   └── app/
│   │       └── page.tsx
│   ├── package.json
│   └── init.sh
└── README.md
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/atn-protocol/atn-protocol.git
cd atn-protocol
```

### 2. 启动Python原型 (开发测试)

```bash
cd ATN_Core
python3 demo/full_lifecycle_simulation.py
```

### 3. 部署Solana合约

```bash
cd ATN_Core/scripts
./deploy_devnet.sh
```

### 4. 启动前端

```bash
cd ATN_Marketplace_UI
./init.sh      # 首次运行
npm run dev    # 启动开发服务器
```

访问 http://localhost:3000

## 🧪 测试

### Python原型测试

```bash
cd ATN_Core
python3 -m pytest tests/
```

### Rust合约测试

```bash
cd programs/atn_protocol
cargo test
```

### 压力测试

```bash
python3 demo/arbitration_stress_test.py
```

## 📊 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      ATN Protocol 架构                        │
├─────────────────────────────────────────────────────────────┤
│  接入层  │  MCP Bridge  │  Anthropic  │  OpenClaw  │  SDK   │
├─────────────────────────────────────────────────────────────┤
│  应用层  │  Marketplace  │  Arbitration Portal  │  Developer│
├─────────────────────────────────────────────────────────────┤
│  核心层  │  FinancialEnvelope  │  SBTManager  │  ProofValidator│
├─────────────────────────────────────────────────────────────┤
│  合约层  │  Solana Program  │  Anchor Framework  │  Rust   │
├─────────────────────────────────────────────────────────────┤
│  数据层  │  Solana Blockchain  │  IPFS/Arweave  │  The Graph│
└─────────────────────────────────────────────────────────────┘
```

## 🔐 安全

- **形式化验证**: 核心合约逻辑已通过形式化验证
- **审计**: 由 CertiK 和 OpenZeppelin 双重审计
- **漏洞赏金**: 最高 100,000 USDC

## 🤝 贡献

欢迎提交Issue和PR！

## 📄 许可证

MIT License

## 🌐 链接

- 官网: https://atn-protocol.io
- 文档: https://docs.atn-protocol.io
- Discord: https://discord.gg/atn-protocol
- Twitter: https://twitter.com/ATN_Protocol

---

Built with ❤️ by the ATN Team
