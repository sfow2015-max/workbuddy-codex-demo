# workbuddy-codex-demo

一个最小可验证的 demo：LLM 调用成本计算工具（纯标准库，无第三方依赖，除测试用的 pytest）。

## 文件

- `llm_cost.py` — 核心模块：`Rates`（费率）+ `call_cost`（单次调用成本，支持缓存折扣）+ `off_peak_cost`（低谷时段打折）
- `test_llm_cost.py` — 7 个单元测试

## 本地运行

```bash
python llm_cost.py          # 直接跑示例
pip install pytest && pytest -v   # 跑测试
```

## 背景

WorkBuddy（薛雨肖）生成，用于验证「WorkBuddy 写代码 → 推 GitHub → Codex 拉取验证」链路。
代码故意保持简单，欢迎 review：关注边界条件（负数 token、缓存超过输入、discount 越界）是否处理正确。
