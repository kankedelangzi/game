#!/usr/bin/env python3
"""
DNF 70版本 CC套（宫廷套装）加成数值独立验算
任务19 稳态核查验证
"""

import json
from datetime import datetime

def verify_cc_set_bonus():
    """验证CC套各职业加成数值"""
    
    results = []
    all_passed = True
    
    print("=" * 60)
    print("DNF 70版本 CC套（宫廷套装）加成数值独立验算")
    print("=" * 60)
    print(f"验算时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # ==================== 一、CC套基础属性验证 ====================
    print("【一、CC套基础属性验证】")
    
    # 单件属性
    cc_parts = {
        "上衣": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击率": 0.5},
        "下装": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击率": 0.5},
        "头饰": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击率": 0.5},
        "帽子": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击率": 0.5},
        "脸部": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击率": 0.5},
        "胸部": {"力量": 50, "物理攻击": 16, "独立攻击": 26, "暴击率": 0.5},
    }
    
    total_power = sum(p["力量"] for p in cc_parts.values())
    total_phy_atk = sum(p["物理攻击"] for p in cc_parts.values())
    total_independent = sum(p["独立攻击"] for p in cc_parts.values())
    total_crit = sum(p["暴击率"] for p in cc_parts.values())
    
    checks = [
        ("6件力量合计", total_power, 310),
        ("6件物理攻击合计", total_phy_atk, 110),
        ("6件独立攻击合计", total_independent, 120),
        ("6件暴击率合计", total_crit, 3.0),
    ]
    
    for name, actual, expected in checks:
        passed = abs(actual - expected) < 0.01
        status = "✅" if passed else "❌"
        print(f"  {status} {name}: {actual} (预期: {expected})")
        results.append({"test": name, "passed": passed, "actual": actual, "expected": expected})
        if not passed:
            all_passed = False
    
    # 胸部力量验证（应为50，非55）
    chest_power = cc_parts["胸部"]["力量"]
    passed = chest_power == 50
    status = "✅" if passed else "❌"
    print(f"  {status} 胸部力量: {chest_power} (应为50，非55)")
    results.append({"test": "胸部力量", "passed": passed, "actual": chest_power, "expected": 50})
    if not passed:
        all_passed = False
    
    print()
    
    # ==================== 二、狂战士收益验证 ====================
    print("【二、狂战士（红眼）收益验证】")
    
    # 基础面板
    berserker_base = {
        "力量": 728,
        "暴走后力量": 728 * 1.40,  # 1019.2
        "独立攻击": 1250,
        "物理攻击": 2000,
        "暴击率": 0.55,  # 55%
    }
    
    print(f"  基础面板: 力量={berserker_base['力量']}, 暴走后力量={berserker_base['暴走后力量']:.1f}")
    print(f"  独立攻击={berserker_base['独立攻击']}, 物理攻击={berserker_base['物理攻击']}")
    print(f"  暴击率={berserker_base['暴击率']*100:.0f}%")
    print()
    
    # 固伤技能收益
    independent_old = berserker_base["独立攻击"]
    independent_new = independent_old + 120
    independent_benefit = (1 + independent_new/250) / (1 + independent_old/250) - 1
    
    # 暴击收益（期望伤害系数）
    crit_old = berserker_base["暴击率"]
    crit_new = crit_old + 0.03
    crit_expected_old = (1 - crit_old) + crit_old * 1.5
    crit_expected_new = (1 - crit_new) + crit_new * 1.5
    crit_benefit = crit_expected_new / crit_expected_old - 1
    
    # 固伤综合收益
    berserker_fixed_benefit = (1 + independent_benefit) * (1 + crit_benefit) - 1
    
    print("  【固伤技能收益】")
    checks = [
        ("独立攻击收益", independent_benefit * 100, 8.0, 0.1),
        ("暴击收益", crit_benefit * 100, 1.2, 0.1),
        ("固伤综合收益", berserker_fixed_benefit * 100, 9.27, 0.1),
    ]
    
    for name, actual, expected, tolerance in checks:
        passed = abs(actual - expected) < tolerance
        status = "✅" if passed else "❌"
        print(f"    {status} {name}: {actual:.2f}% (预期: {expected}%, 容差: ±{tolerance}%)")
        results.append({"test": f"狂战士固伤-{name}", "passed": passed, "actual": actual, "expected": expected})
        if not passed:
            all_passed = False
    
    print()
    
    # 百分比技能收益（使用暴走后力量）
    power_old = berserker_base["暴走后力量"]
    power_new = power_old + 310
    power_benefit = (1 + power_new/250) / (1 + power_old/250) - 1
    
    phy_atk_old = berserker_base["物理攻击"]
    phy_atk_new = phy_atk_old + 110
    phy_atk_benefit = phy_atk_new / phy_atk_old - 1
    
    # 百分比综合收益
    berserker_percent_benefit = (1 + power_benefit) * (1 + phy_atk_benefit) * (1 + crit_benefit) - 1
    
    print("  【百分比技能收益（暴走后）】")
    checks = [
        ("力量收益", power_benefit * 100, 24.42, 0.1),
        ("物理攻击收益", phy_atk_benefit * 100, 5.50, 0.1),
        ("暴击收益", crit_benefit * 100, 1.2, 0.1),
        ("百分比综合收益", berserker_percent_benefit * 100, 32.81, 0.1),
    ]
    
    for name, actual, expected, tolerance in checks:
        passed = abs(actual - expected) < tolerance
        status = "✅" if passed else "❌"
        print(f"    {status} {name}: {actual:.2f}% (预期: {expected}%, 容差: ±{tolerance}%)")
        results.append({"test": f"狂战士百分比-{name}", "passed": passed, "actual": actual, "expected": expected})
        if not passed:
            all_passed = False
    
    print()
    
    # ==================== 三、剑魂收益验证 ====================
    print("【三、剑魂（白手）收益验证】")
    
    # 基础面板（破极兵刃状态下）
    swordsman_base = {
        "力量": 600,
        "物理攻击破极后": 2600,  # 2000 * 1.30
        "暴击率": 0.50,  # 50%
    }
    
    print(f"  基础面板: 力量={swordsman_base['力量']}, 物理攻击(破极后)={swordsman_base['物理攻击破极后']}")
    print(f"  暴击率={swordsman_base['暴击率']*100:.0f}%")
    print()
    
    # 百分比技能收益
    power_old_s = swordsman_base["力量"]
    power_new_s = power_old_s + 310
    power_benefit_s = (1 + power_new_s/250) / (1 + power_old_s/250) - 1
    
    phy_atk_old_s = swordsman_base["物理攻击破极后"]
    phy_atk_new_s = phy_atk_old_s + 110
    phy_atk_benefit_s = phy_atk_new_s / phy_atk_old_s - 1
    
    # 暴击收益
    crit_old_s = swordsman_base["暴击率"]
    crit_new_s = crit_old_s + 0.03
    crit_expected_old_s = (1 - crit_old_s) + crit_old_s * 1.5
    crit_expected_new_s = (1 - crit_new_s) + crit_new_s * 1.5
    crit_benefit_s = crit_expected_new_s / crit_expected_old_s - 1
    
    # 百分比综合收益
    swordsman_percent_benefit = (1 + power_benefit_s) * (1 + phy_atk_benefit_s) * (1 + crit_benefit_s) - 1
    
    print("  【百分比技能收益（破极兵刃状态）】")
    checks = [
        ("力量收益", power_benefit_s * 100, 36.5, 0.1),
        ("物理攻击收益", phy_atk_benefit_s * 100, 4.23, 0.1),
        ("暴击收益", crit_benefit_s * 100, 1.2, 0.1),
        ("百分比综合收益", swordsman_percent_benefit * 100, 43.95, 0.1),
    ]
    
    for name, actual, expected, tolerance in checks:
        passed = abs(actual - expected) < tolerance
        status = "✅" if passed else "❌"
        print(f"    {status} {name}: {actual:.2f}% (预期: {expected}%, 容差: ±{tolerance}%)")
        results.append({"test": f"剑魂百分比-{name}", "passed": passed, "actual": actual, "expected": expected})
        if not passed:
            all_passed = False
    
    print()
    
    # ==================== 四、边际对偶验证 ====================
    print("【四、边际对偶验证】")
    
    # 剑魂百分比收益 / 狂战士固伤收益 = 系统固有频率
    ratio = swordsman_percent_benefit / berserker_fixed_benefit
    print(f"  剑魂百分比收益: {swordsman_percent_benefit*100:.2f}%")
    print(f"  狂战士固伤收益: {berserker_fixed_benefit*100:.2f}%")
    print(f"  收益倍数: {ratio:.2f}x")
    
    # 预期约4.74倍
    passed = abs(ratio - 4.74) < 0.1
    status = "✅" if passed else "❌"
    print(f"  {status} 系统固有频率验证: {ratio:.2f}x (预期: ~4.74x)")
    results.append({"test": "边际对偶验证", "passed": passed, "actual": ratio, "expected": 4.74})
    if not passed:
        all_passed = False
    
    print()
    
    # ==================== 五、总结 ====================
    print("=" * 60)
    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)
    print(f"验算结果: {passed_count}/{total_count} 通过")
    
    if all_passed:
        print("✅ 全部验算通过！数据准确可靠。")
    else:
        print("❌ 存在验算失败项，请检查数据。")
        for r in results:
            if not r["passed"]:
                print(f"   ❌ {r['test']}: 实际={r['actual']:.4f}, 预期={r['expected']:.4f}")
    
    print("=" * 60)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_count,
        "passed_tests": passed_count,
        "all_passed": all_passed,
        "results": results
    }

if __name__ == "__main__":
    result = verify_cc_set_bonus()
    print()
    print("验算报告已生成。")