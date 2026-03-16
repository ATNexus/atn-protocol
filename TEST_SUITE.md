# ATN Protocol 测试套件

## 单元测试

### 运行所有测试

```bash
cd ATN_Core
python3 -m pytest tests/ -v
```

### 特定模块测试

```bash
# 金融信封测试
python3 -m pytest tests/test_financial_envelope.py -v

# 声誉系统测试
python3 -m pytest tests/test_sbt_manager.py -v

# 仲裁系统测试
python3 -m pytest tests/test_arbitration.py -v
```

---

## 集成测试

### 完整生命周期测试

```bash
python3 demo/full_lifecycle_simulation.py
```

预期输出：
- ✅ 资金锁定
- ✅ 任务执行
- ✅ 验证通过
- ✅ 资金释放
- ✅ 声誉更新

### 仲裁压力测试

```bash
python3 demo/arbitration_stress_test.py
```

测试场景：
- 恶意行为检测
- 陪审团投票
- Slashing执行
- 资金重新分配

---

## 性能测试

### 负载测试

```python
# 模拟1000个并发任务
python3 tests/load_test.py --tasks 1000 --agents 100
```

### 压力测试

```python
# 模拟极端条件
python3 tests/stress_test.py --duration 3600
```

---

## 安全测试

### 漏洞扫描

```bash
# 静态分析
bandit -r ATN_Core/

# 依赖检查
safety check
```

### 模糊测试

```python
# 随机输入测试
python3 tests/fuzz_test.py --iterations 10000
```

---

## 测试覆盖率

### 生成报告

```bash
pytest --cov=ATN_Core --cov-report=html
coverage html
```

### 查看报告

```bash
open htmlcov/index.html
```

---

## 持续集成

### GitHub Actions

自动运行：
- ✅ Lint检查
- ✅ 单元测试
- ✅ 集成测试
- ✅ 安全扫描

### 本地预提交

```bash
# 安装pre-commit
pip install pre-commit
pre-commit install

# 手动运行
pre-commit run --all-files
```

---

## 测试数据

### Mock数据

```python
# 测试用的Agent数据
MOCK_AGENTS = [
    {
        "did": "did:atn:solana:agent_001",
        "name": "TestAgent",
        "tier": "gold",
        "score": 500
    }
]

# 测试用的市场数据
MOCK_MARKET_DATA = [
    {
        "route": "NYC-LAX",
        "avg_price": 450.0,
        "min_price": 380.0,
        "max_price": 620.0
    }
]
```

---

## 调试测试

### 启用详细日志

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 断点调试

```python
import pdb; pdb.set_trace()
```

---

*测试套件版本: v1.0.0*
