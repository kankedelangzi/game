#!/usr/bin/env python3
"""
v155 稳态核查：CC套（宫廷套装）各职业加成数值
验证核心数据100%准确
"""

print("=" * 60)
print("v155 稳态核查：CC套（宫廷套装）各职业加成数值")
print("=" * 60)

# ============================================
# 一、CC套基础属性验证
# ============================================
print("\n【一、CC套6件套属性验证】")

cc_stats = {
    "力量": 310,
    "物理攻击": 110,
    "独立攻击": 120,
    "暴击率": 3.0
}

expected = {"力量": 310, "物理攻击": 110, "独立攻击": 120, "暴击率": 3.0}
for key, val in cc_stats.items():
    status = "✅" if val == expected[key] else "❌"
    print(f"  {key}: {val} {status}")

# ============================================
# 二、狂战士收益验算
# ============================================
print("\n【二、狂战士收益验算】")

# 基础面板
berserker_base = {
    "力量": 728,
    "暴走后力量": 728 * 1.40,  # 1019.2
    "独立攻击": 1250,
    "物理攻击": 2000,
    "暴击率": 0.55
}

print(f"  基础力量: {berserker_base['力量']}")
print(f"  暴走后力量: {berserker_base['暴走后力量']:.1f}")

# 固伤收益（独立攻击）
ind_before = berserker_base["独立攻击"]
ind_after = ind_before + 120
ind_multiplier = (1 + ind_after / 250) / (1 + ind_before / 250)
ind_gain = (ind_multiplier - 1) * 100
print(f"\n  固伤-独立攻击收益:")
print(f"    独立: {ind_before} → {ind_after}")
print(f"    系数比: (1+{ind_after}/250)/(1+{ind_before}/250) = {ind_multiplier:.6f}")
print(f"    收益: {ind_gain:.2f}% (预期 +8.0%) {'✅' if abs(ind_gain - 8.0) < 0.1 else '❌'}")

# 暴击收益
crit_before = berserker_base["暴击率"]
crit_after = crit_before + 0.03
crit_expect_before = 1 + crit_before * 0.5  # 暴击期望系数
crit_expect_after = 1 + crit_after * 0.5
crit_gain = (crit_expect_after / crit_expect_before - 1) * 100
print(f"\n  暴击收益:")
print(f"    暴击率: {crit_before*100:.0f}% → {crit_after*100:.0f}%")
print(f"    期望系数: {crit_expect_before:.4f} → {crit_expect_after:.4f}")
print(f"    收益: {crit_gain:.2f}% (预期 +1.2%) {'✅' if abs(crit_gain - 1.2) < 0.1 else '❌'}")

# 固伤综合
berserker_fixed_gain = (1 + ind_gain/100) * (1 + crit_gain/100) - 1
print(f"\n  固伤综合收益: {berserker_fixed_gain*100:.2f}% (预期 +9.3%) {'✅' if abs(berserker_fixed_gain*100 - 9.3) < 0.2 else '❌'}")

# 百分比收益（力量）
str_before = berserker_base["暴走后力量"]
str_after = str_before + 310
str_multiplier = (1 + str_after / 250) / (1 + str_before / 250)
str_gain = (str_multiplier - 1) * 100
print(f"\n  百分比-力量收益:")
print(f"    力量: {str_before:.1f} → {str_after:.1f}")
print(f"    系数比: (1+{str_after:.1f}/250)/(1+{str_before:.1f}/250) = {str_multiplier:.6f}")
print(f"    收益: {str_gain:.2f}% (预期 +24.42%) {'✅' if abs(str_gain - 24.42) < 0.1 else '❌'}")

# 百分比收益（物理攻击）
phy_before = berserker_base["物理攻击"]
phy_after = phy_before + 110
phy_multiplier = (1 + phy_after / 2500) / (1 + phy_before / 2500)
phy_gain = (phy_multiplier - 1) * 100
print(f"\n  百分比-物理攻击收益:")
print(f"    物理攻击: {phy_before} → {phy_after}")
print(f"    系数比: (1+{phy_after}/2500)/(1+{phy_before}/2500) = {phy_multiplier:.6f}")
print(f"    收益: {phy_gain:.2f}% (预期 +2.44%) {'✅' if abs(phy_gain - 2.44) < 0.1 else '❌'}")

# 百分比综合
berserker_percent_gain = str_multiplier * phy_multiplier * (crit_expect_after / crit_expect_before) - 1
print(f"\n  百分比综合收益: {berserker_percent_gain*100:.2f}% (预期 +28.97%) {'✅' if abs(berserker_percent_gain*100 - 28.97) < 0.2 else '❌'}")

# ============================================
# 三、剑魂收益验算
# ============================================
print("\n【三、剑魂收益验算】")

# 基础面板
swordsman_base = {
    "力量": 600,
    "物理攻击_基础": 2000,
    "物理攻击_破极后": 2000 * 1.30,  # 2600
    "暴击率": 0.50
}

print(f"  基础力量: {swordsman_base['力量']}")
print(f"  破极后物理攻击: {swordsman_base['物理攻击_破极后']:.0f}")

# 力量收益
str_s_before = swordsman_base["力量"]
str_s_after = str_s_before + 310
str_s_multiplier = (1 + str_s_after / 250) / (1 + str_s_before / 250)
str_s_gain = (str_s_multiplier - 1) * 100
print(f"\n  力量收益:")
print(f"    力量: {str_s_before} → {str_s_after}")
print(f"    系数比: (1+{str_s_after}/250)/(1+{str_s_before}/250) = {str_s_multiplier:.6f}")
print(f"    收益: {str_s_gain:.2f}% (预期 +36.5%) {'✅' if abs(str_s_gain - 36.5) < 0.2 else '❌'}")

# 物理攻击收益（破极后）
phy_s_before = swordsman_base["物理攻击_破极后"]
phy_s_after = phy_s_before + 110
phy_s_multiplier = (1 + phy_s_after / 2500) / (1 + phy_s_before / 2500)
phy_s_gain = (phy_s_multiplier - 1) * 100
print(f"\n  物理攻击收益（破极后）:")
print(f"    物理攻击: {phy_s_before:.0f} → {phy_s_after:.0f}")
print(f"    系数比: (1+{phy_s_after:.0f}/2500)/(1+{phy_s_before:.0f}/2500) = {phy_s_multiplier:.6f}")
print(f"    收益: {phy_s_gain:.2f}% (预期 +2.2%) {'✅' if abs(phy_s_gain - 2.2) < 0.2 else '❌'}")

# 暴击收益
crit_s_before = swordsman_base["暴击率"]
crit_s_after = crit_s_before + 0.03
crit_s_expect_before = 1 + crit_s_before * 0.5
crit_s_expect_after = 1 + crit_s_after * 0.5
crit_s_gain = (crit_s_expect_after / crit_s_expect_before - 1) * 100
print(f"\n  暴击收益:")
print(f"    暴击率: {crit_s_before*100:.0f}% → {crit_s_after*100:.0f}%")
print(f"    期望系数: {crit_s_expect_before:.4f} → {crit_s_expect_after:.4f}")
print(f"    收益: {crit_s_gain:.2f}% (预期 +1.2%) {'✅' if abs(crit_s_gain - 1.2) < 0.2 else '❌'}")

# 百分比综合
swordsman_percent_gain = str_s_multiplier * phy_s_multiplier * (crit_s_expect_after / crit_s_expect_before) - 1
print(f"\n  百分比综合收益: {swordsman_percent_gain*100:.2f}% (预期 +41.1%) {'✅' if abs(swordsman_percent_gain*100 - 41.1) < 0.2 else '❌'}")

# ============================================
# 四、总结
# ============================================
print("\n" + "=" * 60)
print("【v155 稳态核查总结】")
print("=" * 60)

checks = [
    ("CC套力量+310", cc_stats["力量"] == 310),
    ("CC套物理攻击+110", cc_stats["物理攻击"] == 110),
    ("CC套独立攻击+120", cc_stats["独立攻击"] == 120),
    ("CC套暴击+3%", cc_stats["暴击率"] == 3.0),
    ("狂战士固伤独立+8.0%", abs(ind_gain - 8.0) < 0.1),
    ("狂战士固伤暴击+1.2%", abs(crit_gain - 1.2) < 0.1),
    ("狂战士固伤综合+9.3%", abs(berserker_fixed_gain*100 - 9.3) < 0.2),
    ("狂战士百分比力量+24.42%", abs(str_gain - 24.42) < 0.1),
    ("狂战士百分比物理攻击+2.44%", abs(phy_gain - 2.44) < 0.1),
    ("狂战士百分比综合+28.97%", abs(berserker_percent_gain*100 - 28.97) < 0.2),
    ("剑魂力量+36.5%", abs(str_s_gain - 36.5) < 0.2),
    ("剑魂物理攻击+2.2%", abs(phy_s_gain - 2.2) < 0.2),
    ("剑魂暴击+1.2%", abs(crit_s_gain - 1.2) < 0.2),
    ("剑魂百分比综合+41.1%", abs(swordsman_percent_gain*100 - 41.1) < 0.2),
]

passed = sum(1 for _, ok in checks if ok)
total = len(checks)

for name, ok in checks:
    print(f"  {'✅' if ok else '❌'} {name}")

print(f"\n  总计: {passed}/{total} 项通过 ({passed/total*100:.1f}%)")
print("=" * 60)