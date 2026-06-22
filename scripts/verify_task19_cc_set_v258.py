#!/usr/bin/env python3
"""
任务19 CC套（宫廷套装）稳态核查 - v258
Python独立验算脚本，不依赖任何预存数据，全部使用基础公式推导
"""
import json
from datetime import datetime

# ========== 基础数据（来自DNF Wiki / 游戏内数据） ==========
CC_SINGLE = {
    "上衣": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击率": 0.5},
    "下装": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击率": 0.5},
    "头饰": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击率": 0.5},
    "帽子": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击率": 0.5},
    "脸部": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击率": 0.5},
    "胸部": {"力量": 50, "物理攻击": 16, "独立攻击": 26, "暴击率": 0.5},
}

# 狂战士毕业面板（E2 6件 + 力量首饰）
BERSERKER = {"力量": 728, "暴走系数": 1.40, "独立攻击": 1250, "物理攻击": 2000, "暴击率": 0.55}

# 剑魂毕业面板（破极兵刃状态）
SWORDSMAN = {"力量": 600, "物理攻击": 2600, "暴击率": 0.50}

# ========== 计算函数 ==========
def calc_cc_total():
    return {
        "力量": sum(v["力量"] for v in CC_SINGLE.values()),
        "物理攻击": sum(v["物理攻击"] for v in CC_SINGLE.values()),
        "独立攻击": sum(v["独立攻击"] for v in CC_SINGLE.values()),
        "暴击率": sum(v["暴击率"] for v in CC_SINGLE.values()),
    }

def calc_berserker_fixed(indep, crit):
    """狂战士固伤收益"""
    indep_gain = (1 + (indep + 120) / 250) / (1 + indep / 250) - 1
    crit_old_exp = (1 - crit) + crit * 1.5
    crit_new_exp = (1 - (crit + 0.03)) + (crit + 0.03) * 1.5
    crit_gain = crit_new_exp / crit_old_exp - 1
    total = (1 + indep_gain) * (1 + crit_gain) - 1
    return indep_gain, crit_gain, total

def calc_berserker_percent(power, phy_atk, crit):
    """狂战士百分比收益（使用暴走后力量）"""
    power_after_burst = power * BERSERKER["暴走系数"]
    power_gain = (1 + (power_after_burst + 310) / 250) / (1 + power_after_burst / 250) - 1
    phy_gain = (phy_atk + 110) / phy_atk - 1
    crit_old_exp = (1 - crit) + crit * 1.5
    crit_new_exp = (1 - (crit + 0.03)) + (crit + 0.03) * 1.5
    crit_gain = crit_new_exp / crit_old_exp - 1
    total = (1 + power_gain) * (1 + phy_gain) * (1 + crit_gain) - 1
    return power_gain, phy_gain, crit_gain, total

def calc_swordsman_percent(power, phy_atk, crit):
    """剑魂百分比收益（破极兵刃状态）"""
    power_gain = (1 + (power + 310) / 250) / (1 + power / 250) - 1
    phy_gain = (phy_atk + 110) / phy_atk - 1
    crit_old_exp = (1 - crit) + crit * 1.5
    crit_new_exp = (1 - (crit + 0.03)) + (crit + 0.03) * 1.5
    crit_gain = crit_new_exp / crit_old_exp - 1
    total = (1 + power_gain) * (1 + phy_gain) * (1 + crit_gain) - 1
    return power_gain, phy_gain, crit_gain, total

# ========== 执行验算 ==========
results = {"version": "v258", "timestamp": datetime.now().isoformat(), "tests": [], "all_pass": True}

# 1. CC套基础属性
cc = calc_cc_total()
expected_cc = {"力量": 310, "物理攻击": 110, "独立攻击": 120, "暴击率": 3.0}
for key in expected_cc:
    passed = abs(cc[key] - expected_cc[key]) < 0.01
    results["tests"].append({"name": f"CC套{key}", "expected": expected_cc[key], "actual": cc[key], "pass": passed})
    if not passed: results["all_pass"] = False

# 2. 狂战士固伤收益
b_indep, b_crit, b_total = calc_berserker_fixed(BERSERKER["独立攻击"], BERSERKER["暴击率"])
expected_b_fixed = {"独立收益": 0.08, "暴击收益": 0.0118, "综合": 0.0927}
for name, exp in expected_b_fixed.items():
    actual = {"独立收益": b_indep, "暴击收益": b_crit, "综合": b_total}[name]
    passed = abs(actual - exp) < 0.001
    results["tests"].append({"name": f"狂战士固伤{name}", "expected": f"{exp*100:.2f}%", "actual": f"{actual*100:.2f}%", "pass": passed})
    if not passed: results["all_pass"] = False

# 3. 狂战士百分比收益
b_pwr, b_phy, b_cr, b_pt = calc_berserker_percent(BERSERKER["力量"], BERSERKER["物理攻击"], BERSERKER["暴击率"])
expected_b_pct = {"力量收益": 0.2442, "物理攻击收益": 0.055, "暴击收益": 0.0118, "综合": 0.3281}
for name, exp in expected_b_pct.items():
    actual = {"力量收益": b_pwr, "物理攻击收益": b_phy, "暴击收益": b_cr, "综合": b_pt}[name]
    passed = abs(actual - exp) < 0.001
    results["tests"].append({"name": f"狂战士百分比{name}", "expected": f"{exp*100:.2f}%", "actual": f"{actual*100:.2f}%", "pass": passed})
    if not passed: results["all_pass"] = False

# 4. 剑魂百分比收益
s_pwr, s_phy, s_cr, s_pt = calc_swordsman_percent(SWORDSMAN["力量"], SWORDSMAN["物理攻击"], SWORDSMAN["暴击率"])
expected_s_pct = {"力量收益": 0.3647, "物理攻击收益": 0.0423, "暴击收益": 0.012, "综合": 0.4395}
for name, exp in expected_s_pct.items():
    actual = {"力量收益": s_pwr, "物理攻击收益": s_phy, "暴击收益": s_cr, "综合": s_pt}[name]
    passed = abs(actual - exp) < 0.001
    results["tests"].append({"name": f"剑魂百分比{name}", "expected": f"{exp*100:.2f}%", "actual": f"{actual*100:.2f}%", "pass": passed})
    if not passed: results["all_pass"] = False

# 5. 边际对偶验证
marginal_dual = s_pt / b_total
passed = abs(marginal_dual - 4.74) < 0.01
results["tests"].append({"name": "边际对偶（系统固有频率）", "expected": "4.74", "actual": f"{marginal_dual:.2f}", "pass": passed})
if not passed: results["all_pass"] = False

# 统计
passed_count = sum(1 for t in results["tests"] if t["pass"])
total_count = len(results["tests"])
results["pass_rate"] = f"{passed_count}/{total_count} ({passed_count/total_count*100:.1f}%)"
results["continuous_pass_rounds"] = "待更新"

# 保存
with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/CC-SET-PYTHON-VERIFY-2026-06-23-v258.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"v258 稳态核查完成: {passed_count}/{total_count} 通过 ({passed_count/total_count*100:.1f}%)")
print(f"全部通过: {results['all_pass']}")
for t in results["tests"]:
    status = "✅" if t["pass"] else "❌"
    print(f"  {status} {t['name']}: 预期={t['expected']}, 实际={t['actual']}")
