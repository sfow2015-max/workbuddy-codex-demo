"""LLM 调用成本计算工具。

用于按 token 用量和费率计算一次 LLM 调用的成本，
支持缓存命中折扣与高峰/低谷时段费率。

仅依赖标准库，方便任何环境（包括 Codex）直接拉取验证。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rates:
    """每百万 token 的费率（单位：美元）。"""

    input: float
    output: float
    cached_input: float = 0.0  # 缓存命中输入单价，默认不打折


def call_cost(
    input_tokens: int,
    output_tokens: int,
    rates: Rates,
    cached_tokens: int = 0,
) -> float:
    """计算单次调用成本（美元）。

    cached_tokens 是 input_tokens 中命中缓存的部分，
    按缓存价计费，剩余部分按普通输入价计费。
    """
    if input_tokens < 0 or output_tokens < 0 or cached_tokens < 0:
        raise ValueError("token 数量不能为负数")
    if cached_tokens > input_tokens:
        raise ValueError("缓存命中数不能超过输入 token 总数")

    uncached = input_tokens - cached_tokens
    cost = (
        uncached / 1_000_000 * rates.input
        + cached_tokens / 1_000_000 * rates.cached_input
        + output_tokens / 1_000_000 * rates.output
    )
    return round(cost, 6)


def off_peak_cost(
    input_tokens: int,
    output_tokens: int,
    rates: Rates,
    discount: float = 0.5,
) -> float:
    """低谷时段成本：全部费率按 discount 比例打折。"""
    if not 0 < discount <= 1:
        raise ValueError("discount 必须在 (0, 1] 区间内")
    discounted = Rates(
        input=rates.input * discount,
        output=rates.output * discount,
        cached_input=rates.cached_input * discount,
    )
    return call_cost(input_tokens, output_tokens, discounted)


if __name__ == "__main__":
    # 示例：GLM-5.3 官方价 $1.40 输入 / $4.40 输出 / $0.26 缓存输入
    glm53 = Rates(input=1.40, output=4.40, cached_input=0.26)
    demo_cost = call_cost(
        input_tokens=20_000, output_tokens=5_000, rates=glm53, cached_tokens=10_000
    )
    print(f"示例调用成本: ${demo_cost:.4f}")
