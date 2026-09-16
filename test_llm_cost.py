import pytest

from llm_cost import Rates, call_cost, off_peak_cost


GLM53 = Rates(input=1.40, output=4.40, cached_input=0.26)


def test_no_cache():
    # 1M 输入 + 1M 输出，无缓存
    assert call_cost(1_000_000, 1_000_000, GLM53) == pytest.approx(5.80)


def test_full_cache():
    # 全部命中缓存：输入只按缓存价计
    cost = call_cost(1_000_000, 0, GLM53, cached_tokens=1_000_000)
    assert cost == pytest.approx(0.26)


def test_partial_cache():
    # 10K 缓存 + 10K 未缓存 + 5K 输出
    cost = call_cost(20_000, 5_000, GLM53, cached_tokens=10_000)
    expected = 10_000 / 1e6 * 1.40 + 10_000 / 1e6 * 0.26 + 5_000 / 1e6 * 4.40
    assert cost == pytest.approx(expected)


def test_negative_rejected():
    with pytest.raises(ValueError):
        call_cost(-1, 0, GLM53)


def test_cache_exceeds_input_rejected():
    with pytest.raises(ValueError):
        call_cost(100, 0, GLM53, cached_tokens=101)


def test_off_peak_half_price():
    base = call_cost(1_000_000, 1_000_000, GLM53)
    peak = off_peak_cost(1_000_000, 1_000_000, GLM53, discount=0.5)
    assert peak == pytest.approx(base / 2)


def test_invalid_discount_rejected():
    with pytest.raises(ValueError):
        off_peak_cost(1000, 1000, GLM53, discount=0)
