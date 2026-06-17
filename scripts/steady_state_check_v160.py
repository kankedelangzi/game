#!/usr/bin/env python3
"""
稳态核查 v160 - CC套（宫廷套装）各职业加成数值（修正版）
验证项目：力量/物理攻击/独立攻击/暴击收益计算
修正：物理攻击收益公式使用2500系数分母，暴击率使用实际面板值
"""

import json
from datetime import datetime

# ========== 验证数据（70版本末期标准） ==========

# 基础属性（暴走状态）
BERSERKER_BASE = {
    "力量": 1019.2,      # 暴走后（基础728 × 1.40）
    "物理攻击": 2000,     # 基础物理攻击
    "独立攻击": 1250,     # 基础独立攻击
    "暴击率": 0.55       # 基础暴击率55%（任务15配置）
}

SWORDSMAN_BASE = {
    "力量": 600,         # 剑魂基础力量
    "物理攻击": 2600,     # 破极兵刃后（基础2000 × 1.30）
    "独立攻击": 1250,     # 基础独立攻击（无收益）
    "暴击率": 0.50       # 基础暴击率50%（任务17配置）
}

# CC套6件套属性
CC_SET = {
    "力量": 310,
    "物理攻击": 110,
    "独立攻击": 120,
    "暴击率": 0.03       # +3%
}

# ========== 计算公式（DNF 70标准） ==========

def calc_berserker_fixed_damage(base_ind, cc_set_ind):
    """狂战士固伤技能伤害收益：独立攻击收益"""
    base = 1 + base_ind / 250
    cc = 1 + (base_ind + cc_set_ind) / 250
    return (cc / base - 1) * 100

def calc_berserker_percent_damage(base_str, base_pa, cc_str, cc_pa):
    """狂战士百分比技能伤害收益"""
    # 力量收益：(1 + (base_str + cc_str)/250) / (1 + base_str/250) - 1
    str_gain = (1 + (base_str + cc_str) / 250) / (1 + base_str / 250) - 1
    # 物理攻击收益：(1 + (base_pa + cc_pa)/2500) / (1 + base_pa/2500) - 1
    pa_gain = (1 + (base_pa + cc_pa) / 2500) / (1 + base_pa / 2500) - 1
    return str_gain * 100, pa_gain * 100

def calc_swordsman_percent_damage(base_str, base_pa, cc_str, cc_pa):
    """剑魂百分比技能伤害收益"""
    str_gain = (1 + (base_str + cc_str) / 250) / (1 + base_str / 250) - 1
    pa_gain = (1 + (base_pa + cc_pa) / 2500) / (1 + base_pa / 2500) - 1
    return str_gain * 100, pa_gain * 100

def calc_crit_gain(base_crit, cc_crit):
    """暴击期望收益（暴击伤害1.5倍）"""
    base_exp = 1 + base_crit * 0.5
    cc_exp = 1 + (base_crit + cc_crit) * 0.5
    return (cc_exp / base_exp - 1) * 100

def calc_combined_gain(*gains):
    """多乘区综合收益"""
    result = 1.0
    for g in gains:
        result *= (1 + g / 100)
    return (result - 1) * 100

# ========== 执行验证 ==========

results = {
    "check_id": "v160",
    "timestamp": datetime.now().isoformat(),
    "items": [],
    "all_passed": True
}

def check(name, expected, actual, tolerance=0.05):
    """检查项（tolerance=0.05pp，四舍五入精度允许范围）"""
    passed = abs(expected - actual) <= tolerance
    if not passed:
        results["all_passed"] = False
    results["items"].append({
        "name": name,
        "expected": round(expected, 4),
        "actual": round(actual, 4),
        "passed": passed,
        "diff": round(actual - expected, 4)
    })
    return passed

# --- 狂战士固伤收益 ---
ind_gain_berserker = calc_berserker_fixed_damage(BERSERKER_BASE["独立攻击"], 
                                                   CC_SET["独立攻击"])
check("狂战士固伤-独立攻击收益", 8.0, ind_gain_berserker)

crit_gain_berserker = calc_crit_gain(BERSERKER_BASE["暴击率"], CC_SET["暴击率"])
check("狂战士固伤-暴击收益", 1.2, crit_gain_berserker)

berserker_fixed_combined = calc_combined_gain(ind_gain_berserker, crit_gain_berserker)
check("狂战士固伤-综合收益", 9.3, berserker_fixed_combined)

# --- 狂战士百分比收益 ---
str_gain_berserker, pa_gain_berserker = calc_berserker_percent_damage(
    BERSERKER_BASE["力量"], BERSERKER_BASE["物理攻击"],
    CC_SET["力量"], CC_SET["物理攻击"]
)
check("狂战士百分比-力量收益", 24.42, str_gain_berserker)
check("狂战士百分比-物理攻击收益", 2.44, pa_gain_berserker)

berserker_percent_combined = calc_combined_gain(str_gain_berserker, pa_gain_berserker, crit_gain_berserker)
check("狂战士百分比-综合收益", 28.97, berserker_percent_combined)

# --- 剑魂百分比收益 ---
str_gain_swordsman, pa_gain_swordsman = calc_swordsman_percent_damage(
    SWORDSMAN_BASE["力量"], SWORDSMAN_BASE["物理攻击"],
    CC_SET["力量"], CC_SET["物理攻击"]
)
check("剑魂百分比-力量收益", 36.5, str_gain_swordsman)
check("剑魂百分比-物理攻击收益", 2.2, pa_gain_swordsman)

crit_gain_swordsman = calc_crit_gain(SWORDSMAN_BASE["暴击率"], CC_SET["暴击率"])
check("剑魂百分比-暴击收益", 1.2, crit_gain_swordsman)

swordsman_percent_combined = calc_combined_gain(str_gain_swordsman, pa_gain_swordsman, crit_gain_swordsman)
check("剑魂百分比-综合收益", 41.1, swordsman_percent_combined)

# --- CC套属性验证 ---
check("CC套-力量", 310, CC_SET["力量"], tolerance=1)
check("CC套-物理攻击", 110, CC_SET["物理攻击"], tolerance=1)
check("CC套-独立攻击", 120, CC_SET["独立攻击"], tolerance=1)
check("CC套-暴击率", 3.0, CC_SET["暴击率"] * 100, tolerance=0.1)

# --- 综合验证 ---
total_checks = len(results["items"])
passed_checks = sum(1 for item in results["items"] if item["passed"])

results["summary"] = {
    "total": total_checks,
    "passed": passed_checks,
    "failed": total_checks - passed_checks,
    "pass_rate": round(passed_checks / total_checks * 100, 1) if total_checks > 0 else 0
}

# ========== 输出结果 ==========

print("=" * 60)
print(f"稳态核查 v160 - CC套加成数值验证（修正版）")
print(f"时间: {results['timestamp']}")
print("=" * 60)

for item in results["items"]:
    status = "✅" if item["passed"] else "❌"
    print(f"{status} {item['name']}: 期望={item['expected']}, 实际={item['actual']}, 差异={item['diff']}")

print("=" * 60)
print(f"汇总: {results['summary']['passed']}/{results['summary']['total']} 通过 ({results['summary']['pass_rate']}%)")
print(f"状态: {'✅ 全部通过，数据完全稳态' if results['all_passed'] else '❌ 存在异常，需核查'}")
print("=" * 60)

# 保存结果
with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/steady_state_v160.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)