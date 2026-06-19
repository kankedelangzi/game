#!/usr/bin/env python3
"""
稳态核查 v194 - CC套（宫廷套装）各职业加成数值
独立验算，不依赖任何已有结论
"""

print("=" * 60)
print("稳态核查 v194 - CC套加成数值独立验算")
print("=" * 60)

# ==================== CC套基础属性 ====================
print("\n【1】CC套6件套属性验证")
print("-" * 40)

cc_power = 310      # 力量
cc_phy_atk = 110    # 物理攻击
cc_independent = 120  # 独立攻击
cc_crit = 0.03      # 暴击率

print(f"力量: +{cc_power}")
print(f"物理攻击: +{cc_phy_atk}")
print(f"独立攻击: +{cc_independent}")
print(f"暴击率: +{cc_crit*100:.1f}%")

# ==================== 狂战士面板 ====================
print("\n【2】狂战士基础面板（E2 6件 + 力量首饰）")
print("-" * 40)

berserker_power_base = 728
berserker_power_burst = berserker_power_base * 1.40  # 暴走+40%
berserker_independent = 1250
berserker_phy_atk = 2000
berserker_crit = 0.55

print(f"基础力量: {berserker_power_base}")
print(f"暴走后力量: {berserker_power_burst:.1f}")
print(f"独立攻击: {berserker_independent}")
print(f"物理攻击: {berserker_phy_atk}")
print(f"暴击率: {berserker_crit*100:.0f}%")

# ==================== 剑魂面板 ====================
print("\n【3】剑魂基础面板（巨剑流 + 破极兵刃）")
print("-" * 40)

swordsman_power = 600
swordsman_phy_atk_base = 2000
swordsman_phy_atk_burst = swordsman_phy_atk_base * 1.30  # 破极兵刃+30%
swordsman_crit = 0.50

print(f"力量: {swordsman_power}")
print(f"物理攻击（破极前）: {swordsman_phy_atk_base}")
print(f"物理攻击（破极后）: {swordsman_phy_atk_burst:.0f}")
print(f"暴击率: {swordsman_crit*100:.0f}%")

# ==================== 收益计算 ====================
print("\n【4】收益计算")
print("-" * 40)

# --- 狂战士固伤收益 ---
print("\n▶ 狂战士固伤收益")
independent_gain = (1 + (berserker_independent + cc_independent) / 250) / (1 + berserker_independent / 250) - 1
print(f"  独立攻击收益: (1 + {berserker_independent + cc_independent}/250) / (1 + {berserker_independent}/250) - 1")
print(f"  = (1 + {berserker_independent + cc_independent}/250) / {1 + berserker_independent / 250} - 1")
print(f"  = {(1 + (berserker_independent + cc_independent) / 250):.4f} / {(1 + berserker_independent / 250):.4f} - 1")
print(f"  = {independent_gain*100:.2f}%")

# 暴击期望系数
crit_old_berserker = berserker_crit
crit_new_berserker = berserker_crit + cc_crit
crit_expect_old = (1 - crit_old_berserker) + crit_old_berserker * 1.5
crit_expect_new = (1 - crit_new_berserker) + crit_new_berserker * 1.5
crit_gain_berserker = crit_expect_new / crit_expect_old - 1
print(f"  暴击收益: ({crit_expect_new:.4f} / {crit_expect_old:.4f}) - 1 = {crit_gain_berserker*100:.2f}%")

berserker_fixed_total = (1 + independent_gain) * (1 + crit_gain_berserker) - 1
print(f"  固伤综合收益: (1 + {independent_gain*100:.2f}%) × (1 + {crit_gain_berserker*100:.2f}%) - 1 = {berserker_fixed_total*100:.2f}%")

# --- 狂战士百分比收益 ---
print("\n▶ 狂战士百分比收益（使用暴走后力量）")
power_gain_berserker = (1 + (berserker_power_burst + cc_power) / 250) / (1 + berserker_power_burst / 250) - 1
print(f"  力量收益: (1 + {berserker_power_burst + cc_power:.1f}/250) / (1 + {berserker_power_burst:.1f}/250) - 1")
print(f"  = (1 + {berserker_power_burst + cc_power:.1f}/250) / {1 + berserker_power_burst / 250:.4f} - 1")
print(f"  = {(1 + (berserker_power_burst + cc_power) / 250):.4f} / {(1 + berserker_power_burst / 250):.4f} - 1")
print(f"  = {power_gain_berserker*100:.2f}%")

phy_atk_gain_berserker = (1 + (berserker_phy_atk + cc_phy_atk) / 2500) / (1 + berserker_phy_atk / 2500) - 1
print(f"  物理攻击收益: (1 + {berserker_phy_atk + cc_phy_atk}/2500) / (1 + {berserker_phy_atk}/2500) - 1")
print(f"  = (1 + {berserker_phy_atk + cc_phy_atk}/2500) / {1 + berserker_phy_atk / 2500:.4f} - 1")
print(f"  = {(1 + (berserker_phy_atk + cc_phy_atk) / 2500):.4f} / {(1 + berserker_phy_atk / 2500):.4f} - 1")
print(f"  = {phy_atk_gain_berserker*100:.2f}%")

berserker_percent_total = (1 + power_gain_berserker) * (1 + phy_atk_gain_berserker) * (1 + crit_gain_berserker) - 1
print(f"  百分比综合收益: (1 + {power_gain_berserker*100:.2f}%) × (1 + {phy_atk_gain_berserker*100:.2f}%) × (1 + {crit_gain_berserker*100:.2f}%) - 1 = {berserker_percent_total*100:.2f}%")

# --- 剑魂百分比收益 ---
print("\n▶ 剑魂百分比收益（破极兵刃状态下）")
power_gain_swordsman = (1 + (swordsman_power + cc_power) / 250) / (1 + swordsman_power / 250) - 1
print(f"  力量收益: (1 + {swordsman_power + cc_power}/250) / (1 + {swordsman_power}/250) - 1")
print(f"  = (1 + {swordsman_power + cc_power}/250) / {1 + swordsman_power / 250:.4f} - 1")
print(f"  = {(1 + (swordsman_power + cc_power) / 250):.4f} / {(1 + swordsman_power / 250):.4f} - 1")
print(f"  = {power_gain_swordsman*100:.2f}%")

phy_atk_gain_swordsman = (1 + (swordsman_phy_atk_burst + cc_phy_atk) / 2500) / (1 + swordsman_phy_atk_burst / 2500) - 1
print(f"  物理攻击收益: (1 + {swordsman_phy_atk_burst + cc_phy_atk:.0f}/2500) / (1 + {swordsman_phy_atk_burst:.0f}/2500) - 1")
print(f"  = (1 + {swordsman_phy_atk_burst + cc_phy_atk:.0f}/2500) / {1 + swordsman_phy_atk_burst / 2500:.4f} - 1")
print(f"  = {(1 + (swordsman_phy_atk_burst + cc_phy_atk) / 2500):.4f} / {(1 + swordsman_phy_atk_burst / 2500):.4f} - 1")
print(f"  = {phy_atk_gain_swordsman*100:.2f}%")

crit_old_swordsman = swordsman_crit
crit_new_swordsman = swordsman_crit + cc_crit
crit_expect_old_s = (1 - crit_old_swordsman) + crit_old_swordsman * 1.5
crit_expect_new_s = (1 - crit_new_swordsman) + crit_new_swordsman * 1.5
crit_gain_swordsman = crit_expect_new_s / crit_expect_old_s - 1
print(f"  暴击收益: ({crit_expect_new_s:.4f} / {crit_expect_old_s:.4f}) - 1 = {crit_gain_swordsman*100:.2f}%")

swordsman_percent_total = (1 + power_gain_swordsman) * (1 + phy_atk_gain_swordsman) * (1 + crit_gain_swordsman) - 1
print(f"  百分比综合收益: (1 + {power_gain_swordsman*100:.2f}%) × (1 + {phy_atk_gain_swordsman*100:.2f}%) × (1 + {crit_gain_swordsman*100:.2f}%) - 1 = {swordsman_percent_total*100:.2f}%")

# ==================== 结果汇总 ====================
print("\n" + "=" * 60)
print("【结果汇总】")
print("=" * 60)

expected = {
    "狂战士固伤综合": 9.3,
    "狂战士百分比综合": 28.97,
    "剑魂百分比综合": 41.1
}

actual = {
    "狂战士固伤综合": berserker_fixed_total * 100,
    "狂战士百分比综合": berserker_percent_total * 100,
    "剑魂百分比综合": swordsman_percent_total * 100
}

all_pass = True
for key in expected:
    exp = expected[key]
    act = actual[key]
    diff = abs(act - exp)
    status = "✅ 通过" if diff < 0.5 else "❌ 偏差"
    if diff >= 0.5:
        all_pass = False
    print(f"{key}: 预期 {exp:.2f}% | 实际 {act:.2f}% | 差异 {diff:.2f}pp | {status}")

print("\n" + "=" * 60)
if all_pass:
    print("✅ 稳态核查 v194 全部通过！数据完全稳态。")
else:
    print("❌ 稳态核查存在偏差，需修正。")
print("=" * 60)