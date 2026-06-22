#!/usr/bin/env python3
"""
CC套（宫廷套装）收益验算脚本 - v254
验证任务19核心数据准确性
"""

print("=" * 60)
print("CC套（宫廷套装）收益验算 - v254")
print("=" * 60)

# ==================== 基础数据 ====================
# CC套6件套属性
cc_power = 310
cc_phy_atk = 110
cc_independent = 120
cc_crit = 0.03  # 3%

# 狂战士面板（暴走后）
berserker_base_power = 728
berserker_burst_power = 728 * 1.40  # 暴走+40% = 1019.2
berserker_independent = 1250
berserker_phy_atk = 2000
berserker_crit = 0.55  # 55%

# 剑魂面板（破极后）
swordsman_power = 600
swordsman_base_phy = 2000
swordsman_broken_phy = 2000 * 1.30  # 破极兵刃+30% = 2600
swordsman_crit = 0.50  # 50%

print("\n📊 基础数据确认:")
print(f"  CC套6件: 力量+{cc_power}, 物理攻击+{cc_phy_atk}, 独立攻击+{cc_independent}, 暴击+{cc_crit*100:.0f}%")
print(f"  狂战士暴走后: 力量={berserker_burst_power:.1f}, 独立={berserker_independent}, 物攻={berserker_phy_atk}, 暴击={berserker_crit*100:.0f}%")
print(f"  剑魂破极后: 力量={swordsman_power}, 物攻={swordsman_broken_phy:.0f}, 暴击={swordsman_crit*100:.0f}%")

# ==================== 狂战士固伤收益 ====================
print("\n" + "=" * 60)
print("🔴 狂战士 - 固伤技能收益")
print("=" * 60)

# 独立攻击收益
berserker_ind_before = 1 + berserker_independent / 250
berserker_ind_after = 1 + (berserker_independent + cc_independent) / 250
berserker_ind_gain = berserker_ind_after / berserker_ind_before - 1
print(f"\n  独立攻击收益:")
print(f"    基础: 1 + {berserker_independent}/250 = {berserker_ind_before:.4f}")
print(f"    CC套: 1 + {berserker_independent + cc_independent}/250 = {berserker_ind_after:.4f}")
print(f"    收益比: {berserker_ind_after:.4f}/{berserker_ind_before:.4f} - 1 = {berserker_ind_gain*100:.2f}%")

# 暴击收益（期望伤害系数）
berserker_crit_before = (1 - berserker_crit) + berserker_crit * 1.5
berserker_crit_after = (1 - (berserker_crit + cc_crit)) + (berserker_crit + cc_crit) * 1.5
berserker_crit_gain = berserker_crit_after / berserker_crit_before - 1
print(f"\n  暴击收益:")
print(f"    基础期望: (1-{berserker_crit:.2f}) + {berserker_crit:.2f}×1.5 = {berserker_crit_before:.4f}")
print(f"    CC套期望: (1-{berserker_crit + cc_crit:.2f}) + {berserker_crit + cc_crit:.2f}×1.5 = {berserker_crit_after:.4f}")
print(f"    收益比: {berserker_crit_after:.4f}/{berserker_crit_before:.4f} - 1 = {berserker_crit_gain*100:.2f}%")

# 固伤综合收益
berserker固伤综合 = (1 + berserker_ind_gain) * (1 + berserker_crit_gain) - 1
print(f"\n  ✅ 固伤综合收益: (1+{berserker_ind_gain*100:.2f}%)×(1+{berserker_crit_gain*100:.2f}%) - 1 = {berserker固伤综合*100:.2f}%")
print(f"    预期: +9.27% | 实际: +{berserker固伤综合*100:.2f}% | {'✅ 通过' if abs(berserker固伤综合*100 - 9.27) < 0.05 else '❌ 偏差'}")

# ==================== 狂战士百分比收益 ====================
print("\n" + "=" * 60)
print("🔴 狂战士 - 百分比技能收益")
print("=" * 60)

# 力量收益
berserker_pow_before = 1 + berserker_burst_power / 250
berserker_pow_after = 1 + (berserker_burst_power + cc_power) / 250
berserker_pow_gain = berserker_pow_after / berserker_pow_before - 1
print(f"\n  力量收益:")
print(f"    基础: 1 + {berserker_burst_power:.1f}/250 = {berserker_pow_before:.4f}")
print(f"    CC套: 1 + {berserker_burst_power + cc_power:.1f}/250 = {berserker_pow_after:.4f}")
print(f"    收益比: {berserker_pow_after:.4f}/{berserker_pow_before:.4f} - 1 = {berserker_pow_gain*100:.2f}%")

# 物理攻击收益
berserker_phy_gain = (berserker_phy_atk + cc_phy_atk) / berserker_phy_atk - 1
print(f"\n  物理攻击收益:")
print(f"    基础: {berserker_phy_atk}")
print(f"    CC套: {berserker_phy_atk + cc_phy_atk}")
print(f"    收益比: {berserker_phy_atk + cc_phy_atk}/{berserker_phy_atk} - 1 = {berserker_phy_gain*100:.2f}%")

# 暴击收益
print(f"\n  暴击收益: +{berserker_crit_gain*100:.2f}%（同上）")

# 百分比综合收益
berserker百分比综合 = (1 + berserker_pow_gain) * (1 + berserker_phy_gain) * (1 + berserker_crit_gain) - 1
print(f"\n  ✅ 百分比综合收益: (1+{berserker_pow_gain*100:.2f}%)×(1+{berserker_phy_gain*100:.2f}%)×(1+{berserker_crit_gain*100:.2f}%) - 1 = {berserker百分比综合*100:.2f}%")
print(f"    预期: +32.81% | 实际: +{berserker百分比综合*100:.2f}% | {'✅ 通过' if abs(berserker百分比综合*100 - 32.81) < 0.05 else '❌ 偏差'}")

# ==================== 剑魂百分比收益 ====================
print("\n" + "=" * 60)
print("🔵 剑魂 - 百分比技能收益")
print("=" * 60)

# 力量收益
sword_pow_before = 1 + swordsman_power / 250
sword_pow_after = 1 + (swordsman_power + cc_power) / 250
sword_pow_gain = sword_pow_after / sword_pow_before - 1
print(f"\n  力量收益:")
print(f"    基础: 1 + {swordsman_power}/250 = {sword_pow_before:.4f}")
print(f"    CC套: 1 + {swordsman_power + cc_power}/250 = {sword_pow_after:.4f}")
print(f"    收益比: {sword_pow_after:.4f}/{sword_pow_before:.4f} - 1 = {sword_pow_gain*100:.2f}%")

# 物理攻击收益（破极后）
sword_phy_gain = (swordsman_broken_phy + cc_phy_atk) / swordsman_broken_phy - 1
print(f"\n  物理攻击收益（破极后）:")
print(f"    基础: {swordsman_broken_phy:.0f}")
print(f"    CC套: {swordsman_broken_phy + cc_phy_atk:.0f}")
print(f"    收益比: {swordsman_broken_phy + cc_phy_atk:.0f}/{swordsman_broken_phy:.0f} - 1 = {sword_phy_gain*100:.2f}%")

# 暴击收益
sword_crit_before = (1 - swordsman_crit) + swordsman_crit * 1.5
sword_crit_after = (1 - (swordsman_crit + cc_crit)) + (swordsman_crit + cc_crit) * 1.5
sword_crit_gain = sword_crit_after / sword_crit_before - 1
print(f"\n  暴击收益:")
print(f"    基础期望: {sword_crit_before:.4f}")
print(f"    CC套期望: {sword_crit_after:.4f}")
print(f"    收益比: {sword_crit_gain*100:.2f}%")

# 百分比综合收益
sword百分比综合 = (1 + sword_pow_gain) * (1 + sword_phy_gain) * (1 + sword_crit_gain) - 1
print(f"\n  ✅ 百分比综合收益: (1+{sword_pow_gain*100:.2f}%)×(1+{sword_phy_gain*100:.2f}%)×(1+{sword_crit_gain*100:.2f}%) - 1 = {sword百分比综合*100:.2f}%")
print(f"    预期: +43.95% | 实际: +{sword百分比综合*100:.2f}% | {'✅ 通过' if abs(sword百分比综合*100 - 43.95) < 0.05 else '❌ 偏差'}")

# ==================== 边际对偶验证 ====================
print("\n" + "=" * 60)
print("🔬 边际对偶验证 - 系统固有频率")
print("=" * 60)

ratio = sword百分比综合 / berserker固伤综合
print(f"\n  剑魂百分比综合 / 狂战士固伤综合 = {sword百分比综合*100:.2f}% / {berserker固伤综合*100:.2f}% = {ratio:.2f}倍")
print(f"  预期: 4.74倍 | 实际: {ratio:.2f}倍 | {'✅ 系统固有频率确认' if abs(ratio - 4.74) < 0.05 else '⚠️ 需检查'}")

# ==================== 最终汇总 ====================
print("\n" + "=" * 60)
print("📋 验算汇总")
print("=" * 60)

results = [
    ("狂战士固伤综合", berserker固伤综合*100, 9.27),
    ("狂战士百分比综合", berserker百分比综合*100, 32.81),
    ("剑魂百分比综合", sword百分比综合*100, 43.95),
    ("边际对偶比率", ratio, 4.74),
]

all_pass = True
for name, actual, expected in results:
    status = "✅" if abs(actual - expected) < 0.05 else "❌"
    if abs(actual - expected) >= 0.05:
        all_pass = False
    print(f"  {status} {name}: 预期={expected:.2f}% | 实际={actual:.2f}% | 偏差={abs(actual-expected):.2f}pp")

print("\n" + "=" * 60)
if all_pass:
    print("✅ 全部验算通过！数据准确可靠。")
else:
    print("❌ 存在偏差，需检查修正。")
print("=" * 60)