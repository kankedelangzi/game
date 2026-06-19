#!/usr/bin/env python3
"""
CC套（宫廷套装）各职业加成数值 - 稳态核查验算
任务19 独立验证脚本
"""

print("=" * 60)
print("CC套（宫廷套装）稳态核查 - 独立验算")
print("=" * 60)

# ============================================
# 一、CC套基础属性验证
# ============================================
print("\n【一、CC套基础属性验证】")

# 单件属性（来自DNF Wiki）
costume_parts = {
    "上衣": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击率": 0.5},
    "下装": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击率": 0.5},
    "头饰": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击率": 0.5},
    "帽子": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击率": 0.5},
    "脸部": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击率": 0.5},
    "胸部": {"力量": 50, "物理攻击": 16, "独立攻击": 26, "暴击率": 0.5},
}

total_power = sum(p["力量"] for p in costume_parts.values())
total_phy_atk = sum(p["物理攻击"] for p in costume_parts.values())
total_independent = sum(p["独立攻击"] for p in costume_parts.values())
total_crit = sum(p["暴击率"] for p in costume_parts.values())

print(f"  6件合计 - 力量: {total_power} (预期: 310) ✅" if total_power == 310 else f"  力量: {total_power} ❌")
print(f"  6件合计 - 物理攻击: {total_phy_atk} (预期: 110) ✅" if total_phy_atk == 110 else f"  物理攻击: {total_phy_atk} ❌")
print(f"  6件合计 - 独立攻击: {total_independent} (预期: 120) ✅" if total_independent == 120 else f"  独立攻击: {total_independent} ❌")
print(f"  6件合计 - 暴击率: {total_crit}% (预期: 3.0%) ✅" if total_crit == 3.0 else f"  暴击率: {total_crit}% ❌")

# ============================================
# 二、狂战士收益验算
# ============================================
print("\n【二、狂战士收益验算】")

# 基础面板（毕业级）
berserker_base = {
    "力量": 728,
    "暴走后力量": 728 * 1.40,  # 暴走+40%
    "独立攻击": 1250,
    "物理攻击": 2000,
    "暴击率": 0.55,
}

print(f"  基础面板: 力量={berserker_base['力量']}, 暴走后={berserker_base['暴走后力量']:.1f}, 独立={berserker_base['独立攻击']}, 物理攻击={berserker_base['物理攻击']}, 暴击={berserker_base['暴击率']*100:.0f}%")

# 固伤收益
independent_before = berserker_base["独立攻击"]
independent_after = independent_before + 120
independent_benefit = (1 + independent_after / 250) / (1 + independent_before / 250) - 1

# 暴击收益（期望伤害系数）
crit_before = berserker_base["暴击率"]
crit_after = crit_before + 0.03
crit_expect_before = (1 - crit_before) + crit_before * 1.5
crit_expect_after = (1 - crit_after) + crit_after * 1.5
crit_benefit = crit_expect_after / crit_expect_before - 1

# 固伤综合
berserker_fixed_benefit = (1 + independent_benefit) * (1 + crit_benefit) - 1

print(f"\n  固伤技能收益:")
print(f"    独立攻击: ({1 + independent_after/250:.4f} / {1 + independent_before/250:.4f}) - 1 = {independent_benefit*100:.2f}% (预期: +8.0%)")
print(f"    暴击期望: ({crit_expect_after:.4f} / {crit_expect_before:.4f}) - 1 = {crit_benefit*100:.2f}% (预期: +1.2%)")
print(f"    固伤综合: (1+{independent_benefit*100:.2f}%)×(1+{crit_benefit*100:.2f}%) - 1 = {berserker_fixed_benefit*100:.2f}% (预期: +9.3%)")

# 百分比技能收益
power_before = berserker_base["暴走后力量"]
power_after = power_before + 310
power_benefit = (1 + power_after / 250) / (1 + power_before / 250) - 1

phy_atk_before = berserker_base["物理攻击"]
phy_atk_after = phy_atk_before + 110
phy_atk_benefit = (1 + phy_atk_after / 2500) / (1 + phy_atk_before / 2500) - 1

crit_benefit_percent = crit_benefit  # 同上

berserker_percent_benefit = (1 + power_benefit) * (1 + phy_atk_benefit) * (1 + crit_benefit_percent) - 1

print(f"\n  百分比技能收益:")
print(f"    力量: ({1 + power_after/250:.4f} / {1 + power_before/250:.4f}) - 1 = {power_benefit*100:.2f}% (预期: +24.42%)")
print(f"    物理攻击: ({1 + phy_atk_after/2500:.4f} / {1 + phy_atk_before/2500:.4f}) - 1 = {phy_atk_benefit*100:.2f}% (预期: +2.44%)")
print(f"    暴击: {crit_benefit*100:.2f}% (预期: +1.2%)")
print(f"    百分比综合: (1+{power_benefit*100:.2f}%)×(1+{phy_atk_benefit*100:.2f}%)×(1+{crit_benefit_percent*100:.2f}%) - 1 = {berserker_percent_benefit*100:.2f}% (预期: +28.97%)")

# ============================================
# 三、剑魂收益验算
# ============================================
print("\n【三、剑魂收益验算】")

# 基础面板（毕业级，破极兵刃状态）
swordsman_base = {
    "力量": 600,
    "物理攻击破极前": 2000,
    "物理攻击破极后": 2000 * 1.30,  # 破极兵刃+30%
    "暴击率": 0.50,
}

print(f"  基础面板: 力量={swordsman_base['力量']}, 物理攻击破极后={swordsman_base['物理攻击破极后']:.0f}, 暴击={swordsman_base['暴击率']*100:.0f}%")

# 力量收益
power_before_s = swordsman_base["力量"]
power_after_s = power_before_s + 310
power_benefit_s = (1 + power_after_s / 250) / (1 + power_before_s / 250) - 1

# 物理攻击收益（破极后）
phy_before_s = swordsman_base["物理攻击破极后"]
phy_after_s = phy_before_s + 110
phy_benefit_s = (1 + phy_after_s / 2500) / (1 + phy_before_s / 2500) - 1

# 暴击收益
crit_before_s = swordsman_base["暴击率"]
crit_after_s = crit_before_s + 0.03
crit_expect_before_s = (1 - crit_before_s) + crit_before_s * 1.5
crit_expect_after_s = (1 - crit_after_s) + crit_after_s * 1.5
crit_benefit_s = crit_expect_after_s / crit_expect_before_s - 1

# 综合收益
swordsman_benefit = (1 + power_benefit_s) * (1 + phy_benefit_s) * (1 + crit_benefit_s) - 1

print(f"\n  百分比技能收益（破极兵刃状态）:")
print(f"    力量: ({1 + power_after_s/250:.4f} / {1 + power_before_s/250:.4f}) - 1 = {power_benefit_s*100:.2f}% (预期: +36.5%)")
print(f"    物理攻击: ({1 + phy_after_s/2500:.4f} / {1 + phy_before_s/2500:.4f}) - 1 = {phy_benefit_s*100:.2f}% (预期: +2.2%)")
print(f"    暴击: ({crit_expect_after_s:.4f} / {crit_expect_before_s:.4f}) - 1 = {crit_benefit_s*100:.2f}% (预期: +1.2%)")
print(f"    百分比综合: (1+{power_benefit_s*100:.2f}%)×(1+{phy_benefit_s*100:.2f}%)×(1+{crit_benefit_s*100:.2f}%) - 1 = {swordsman_benefit*100:.2f}% (预期: +41.1%)")

# ============================================
# 四、汇总验证
# ============================================
print("\n" + "=" * 60)
print("【四、稳态核查汇总】")
print("=" * 60)

checks = [
    ("CC套力量+310", total_power == 310, total_power),
    ("CC套物理攻击+110", total_phy_atk == 110, total_phy_atk),
    ("CC套独立攻击+120", total_independent == 120, total_independent),
    ("CC套暴击+3%", total_crit == 3.0, total_crit),
    ("狂战士固伤独立+8.0%", abs(independent_benefit - 0.08) < 0.001, f"{independent_benefit*100:.2f}%"),
    ("狂战士固伤暴击+1.2%", abs(crit_benefit - 0.012) < 0.001, f"{crit_benefit*100:.2f}%"),
    ("狂战士固伤综合+9.3%", abs(berserker_fixed_benefit - 0.093) < 0.002, f"{berserker_fixed_benefit*100:.2f}%"),
    ("狂战士百分比力量+24.42%", abs(power_benefit - 0.2442) < 0.001, f"{power_benefit*100:.2f}%"),
    ("狂战士百分比物理攻击+2.44%", abs(phy_atk_benefit - 0.0244) < 0.001, f"{phy_atk_benefit*100:.2f}%"),
    ("狂战士百分比综合+28.97%", abs(berserker_percent_benefit - 0.2897) < 0.002, f"{berserker_percent_benefit*100:.2f}%"),
    ("剑魂百分比力量+36.5%", abs(power_benefit_s - 0.365) < 0.001, f"{power_benefit_s*100:.2f}%"),
    ("剑魂百分比物理攻击+2.2%", abs(phy_benefit_s - 0.022) < 0.001, f"{phy_benefit_s*100:.2f}%"),
    ("剑魂百分比暴击+1.2%", abs(crit_benefit_s - 0.012) < 0.001, f"{crit_benefit_s*100:.2f}%"),
    ("剑魂百分比综合+41.1%", abs(swordsman_benefit - 0.411) < 0.002, f"{swordsman_benefit*100:.2f}%"),
]

passed = 0
failed = 0
for name, result, value in checks:
    status = "✅" if result else "❌"
    if result:
        passed += 1
    else:
        failed += 1
    print(f"  {status} {name}: {value}")

print(f"\n{'='*60}")
print(f"稳态核查结果: {passed}/{len(checks)} 通过 ({passed/len(checks)*100:.0f}%)")
if failed == 0:
    print("✅ 数据完全稳态，所有核心数据100%精确匹配")
else:
    print(f"❌ 有 {failed} 项未通过，需核查")
print("=" * 60)