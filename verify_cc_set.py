#!/usr/bin/env python3
"""
CC套（宫廷套装）稳态核查 - Python独立验算
验证任务19的核心数据准确性
"""

print("=" * 60)
print("CC套（宫廷套装）稳态核查 - Python独立验算")
print("=" * 60)

# ==================== 基础数据 ====================
# CC套6件套属性
cc_power = 310
cc_phy_atk = 110
cc_independent = 120
cc_crit = 0.03  # 3%

# ==================== 狂战士面板（毕业级） ====================
print("\n【狂战士面板配置】")
berserker_power = 728
bks_power_burst = berserker_power * 1.40  # 暴走+40%
bks_independent = 1250
bks_phy_atk = 2000
bks_crit = 0.55

print(f"基础力量: {berserker_power}")
print(f"暴走后力量: {bks_power_burst:.1f}")
print(f"独立攻击: {bks_independent}")
print(f"物理攻击: {bks_phy_atk}")
print(f"暴击率: {bks_crit*100:.0f}%")

# ==================== 狂战士收益计算 ====================
print("\n【狂战士收益计算】")

# 固伤收益（独立攻击）
bks_ind_before = 1 + bks_independent / 250
bks_ind_after = 1 + (bks_independent + cc_independent) / 250
bks_ind_gain = bks_ind_after / bks_ind_before - 1
print(f"独立攻击收益: ({bks_ind_after:.4f} / {bks_ind_before:.4f}) - 1 = {bks_ind_gain*100:.2f}%")

# 暴击收益（期望伤害系数）
bks_crit_before = (1 - bks_crit) + bks_crit * 1.5
bks_crit_after = (1 - (bks_crit + cc_crit)) + (bks_crit + cc_crit) * 1.5
bks_crit_gain = bks_crit_after / bks_crit_before - 1
print(f"暴击收益: ({bks_crit_after:.4f} / {bks_crit_before:.4f}) - 1 = {bks_crit_gain*100:.2f}%")

# 固伤综合收益
bks_fixed_total = (1 + bks_ind_gain) * (1 + bks_crit_gain) - 1
print(f"固伤综合收益: (1+{bks_ind_gain*100:.2f}%) × (1+{bks_crit_gain*100:.2f}%) - 1 = {bks_fixed_total*100:.2f}%")

# 百分比收益（力量）
bks_pow_before = 1 + bks_power_burst / 250
bks_pow_after = 1 + (bks_power_burst + cc_power) / 250
bks_pow_gain = bks_pow_after / bks_pow_before - 1
print(f"\n力量收益: ({bks_pow_after:.4f} / {bks_pow_before:.4f}) - 1 = {bks_pow_gain*100:.2f}%")

# 百分比收益（物理攻击）
bks_phy_before = bks_phy_atk
bks_phy_after = bks_phy_atk + cc_phy_atk
bks_phy_gain = bks_phy_after / bks_phy_before - 1
print(f"物理攻击收益: {bks_phy_after} / {bks_phy_before} - 1 = {bks_phy_gain*100:.2f}%")

# 百分比综合收益
bks_percent_total = (1 + bks_pow_gain) * (1 + bks_phy_gain) * (1 + bks_crit_gain) - 1
print(f"百分比综合收益: (1+{bks_pow_gain*100:.2f}%) × (1+{bks_phy_gain*100:.2f}%) × (1+{bks_crit_gain*100:.2f}%) - 1 = {bks_percent_total*100:.2f}%")

# ==================== 剑魂面板（毕业级） ====================
print("\n【剑魂面板配置】")
sword_power = 600
sword_phy_atk_base = 2000
sword_phy_atk_burst = sword_phy_atk_base * 1.30  # 破极兵刃+30%
sword_crit = 0.50

print(f"力量: {sword_power}")
print(f"物理攻击（破极后）: {sword_phy_atk_burst:.0f}")
print(f"暴击率: {sword_crit*100:.0f}%")

# ==================== 剑魂收益计算 ====================
print("\n【剑魂收益计算】")

# 力量收益
sw_pow_before = 1 + sword_power / 250
sw_pow_after = 1 + (sword_power + cc_power) / 250
sw_pow_gain = sw_pow_after / sw_pow_before - 1
print(f"力量收益: ({sw_pow_after:.4f} / {sw_pow_before:.4f}) - 1 = {sw_pow_gain*100:.2f}%")

# 物理攻击收益（破极后）
sw_phy_before = sword_phy_atk_burst
sw_phy_after = sword_phy_atk_burst + cc_phy_atk
sw_phy_gain = sw_phy_after / sw_phy_before - 1
print(f"物理攻击收益: {sw_phy_after:.0f} / {sw_phy_before:.0f} - 1 = {sw_phy_gain*100:.2f}%")

# 暴击收益
sw_crit_before = (1 - sword_crit) + sword_crit * 1.5
sw_crit_after = (1 - (sword_crit + cc_crit)) + (sword_crit + cc_crit) * 1.5
sw_crit_gain = sw_crit_after / sw_crit_before - 1
print(f"暴击收益: ({sw_crit_after:.4f} / {sw_crit_before:.4f}) - 1 = {sw_crit_gain*100:.2f}%")

# 百分比综合收益
sw_percent_total = (1 + sw_pow_gain) * (1 + sw_phy_gain) * (1 + sw_crit_gain) - 1
print(f"百分比综合收益: (1+{sw_pow_gain*100:.2f}%) × (1+{sw_phy_gain*100:.2f}%) × (1+{sw_crit_gain*100:.2f}%) - 1 = {sw_percent_total*100:.2f}%")

# ==================== 验证结果 ====================
print("\n" + "=" * 60)
print("【验证结果汇总】")
print("=" * 60)

expected = {
    "狂战士固伤综合": 9.27,
    "狂战士百分比综合": 32.81,
    "剑魂百分比综合": 43.95,
}

actual = {
    "狂战士固伤综合": bks_fixed_total * 100,
    "狂战士百分比综合": bks_percent_total * 100,
    "剑魂百分比综合": sw_percent_total * 100,
}

all_pass = True
for key in expected:
    exp = expected[key]
    act = actual[key]
    diff = abs(act - exp)
    status = "✅" if diff < 0.1 else "❌"
    if diff >= 0.1:
        all_pass = False
    print(f"{status} {key}: 预期 {exp:.2f}% | 实际 {act:.2f}% | 差异 {diff:.2f}pp")

# 边际对偶验证
ratio = sw_percent_total / bks_fixed_total
print(f"\n🔬 边际对偶验证: 剑魂百分比/狂战士固伤 = {ratio:.2f}倍")
print(f"   预期值: 4.74倍 | 实际值: {ratio:.2f}倍 | {'✅' if abs(ratio - 4.74) < 0.1 else '❌'}")

print("\n" + "=" * 60)
if all_pass:
    print("✅ 所有核心数据验证通过！稳态核查完成。")
else:
    print("❌ 存在数据偏差，需要修正！")
print("=" * 60)
