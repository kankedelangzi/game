#!/usr/bin/env python3
"""
任务19 CC套稳态核查 - 狂战士收益验证 (v310)
独立数据源验证：基于DNF 70版本伤害公式，不依赖HTML报告
"""

print("=" * 60)
print("任务19 CC套稳态核查 - 狂战士收益验证 (v310)")
print("=" * 60)

# ===== 基础面板（毕业级） =====
berserker_base = {
    "力量": 728,
    "暴走倍率": 1.40,
    "独立攻击": 1250,
    "物理攻击": 2000,
    "暴击率": 0.55,
}

# ===== CC套6件加成 =====
cc_bonus = {
    "力量": 310,
    "物理攻击": 110,
    "独立攻击": 120,
    "暴击率": 0.03,
}

# ===== 暴走后力量 =====
berserker_burst_power = berserker_base["力量"] * berserker_base["暴走倍率"]
print(f"\n【狂战士基础面板】")
print(f"  基础力量: {berserker_base['力量']}")
print(f"  暴走后力量: {berserker_burst_power:.1f}")
print(f"  独立攻击: {berserker_base['独立攻击']}")
print(f"  物理攻击: {berserker_base['物理攻击']}")
print(f"  暴击率: {berserker_base['暴击率']*100:.0f}%")

# ===== 独立攻击收益（固伤核心） =====
ind_before = berserker_base["独立攻击"]
ind_after = ind_before + cc_bonus["独立攻击"]
ind_multiplier_before = 1 + ind_before / 250
ind_multiplier_after = 1 + ind_after / 250
ind_gain = ind_multiplier_after / ind_multiplier_before - 1

print(f"\n【独立攻击收益（固伤核心）】")
print(f"  基准: {ind_before} → {ind_after}")
print(f"  乘数: {ind_multiplier_before:.4f} → {ind_multiplier_after:.4f}")
print(f"  收益: {ind_gain*100:.2f}%")

# ===== 暴击收益 =====
crit_before = berserker_base["暴击率"]
crit_after = crit_before + cc_bonus["暴击率"]
crit_expect_before = (1 - crit_before) + crit_before * 1.5
crit_expect_after = (1 - crit_after) + crit_after * 1.5
crit_gain = crit_expect_after / crit_expect_before - 1

print(f"\n【暴击收益】")
print(f"  基准: {crit_before*100:.0f}% → {crit_after*100:.0f}%")
print(f"  期望系数: {crit_expect_before:.4f} → {crit_expect_after:.4f}")
print(f"  收益: {crit_gain*100:.2f}%")

# ===== 固伤综合收益 =====
berserker_gu_total = (1 + ind_gain) * (1 + crit_gain) - 1
print(f"\n【固伤综合收益】")
print(f"  (1+{ind_gain*100:.2f}%) × (1+{crit_gain*100:.2f}%) - 1 = {berserker_gu_total*100:.2f}%")

# ===== 百分比技能收益 =====
# 力量收益
power_before = berserker_burst_power
power_after = power_before + cc_bonus["力量"]
power_multiplier_before = 1 + power_before / 250
power_multiplier_after = 1 + power_after / 250
power_gain = power_multiplier_after / power_multiplier_before - 1

print(f"\n【百分比技能收益】")
print(f"  力量: {power_before:.1f} → {power_after:.1f}")
print(f"  乘数: {power_multiplier_before:.4f} → {power_multiplier_after:.4f}")
print(f"  力量收益: {power_gain*100:.2f}%")

# 物理攻击收益
phy_before = berserker_base["物理攻击"]
phy_after = phy_before + cc_bonus["物理攻击"]
phy_gain = phy_after / phy_before - 1
print(f"  物理攻击: {phy_before} → {phy_after}")
print(f"  物理攻击收益: {phy_gain*100:.2f}%")

# 暴击收益（同固伤）
print(f"  暴击收益: {crit_gain*100:.2f}%")

# 百分比综合
berserker_percent_total = (1 + power_gain) * (1 + phy_gain) * (1 + crit_gain) - 1
print(f"\n【百分比综合收益】")
print(f"  (1+{power_gain*100:.2f}%) × (1+{phy_gain*100:.2f}%) × (1+{crit_gain*100:.2f}%) - 1 = {berserker_percent_total*100:.2f}%")

# ===== 验证结果 =====
print("\n" + "=" * 60)
print("验证结果汇总")
print("=" * 60)

expected = {
    "独立攻击收益": 8.0,
    "暴击收益": 1.18,
    "固伤综合收益": 9.27,
    "力量收益(百分比)": 24.42,
    "物理攻击收益(百分比)": 5.50,
    "百分比综合收益": 32.81,
}

actual = {
    "独立攻击收益": round(ind_gain * 100, 2),
    "暴击收益": round(crit_gain * 100, 2),
    "固伤综合收益": round(berserker_gu_total * 100, 2),
    "力量收益(百分比)": round(power_gain * 100, 2),
    "物理攻击收益(百分比)": round(phy_gain * 100, 2),
    "百分比综合收益": round(berserker_percent_total * 100, 2),
}

all_pass = True
for key in expected:
    match = abs(actual[key] - expected[key]) < 0.05
    status = "✅" if match else "❌"
    if not match:
        all_pass = False
    print(f"  {status} {key}: 预期={expected[key]:.2f}%, 实际={actual[key]:.2f}%")

print(f"\n{'='*60}")
print(f"狂战士验证: {'全部通过 ✅' if all_pass else '存在差异 ❌'}")
print(f"{'='*60}")

# ===== 剑魂验证 =====
print("\n" + "=" * 60)
print("剑魂收益验证")
print("=" * 60)

swordsman_base = {
    "力量": 600,
    "物理攻击破极后": 2600,
    "暴击率": 0.50,
}

# 力量收益
sm_power_before = swordsman_base["力量"]
sm_power_after = sm_power_before + cc_bonus["力量"]
sm_power_gain = (1 + sm_power_after/250) / (1 + sm_power_before/250) - 1
print(f"  力量收益: {sm_power_before}→{sm_power_after}, 收益={sm_power_gain*100:.2f}%")

# 物理攻击收益
sm_phy_before = swordsman_base["物理攻击破极后"]
sm_phy_after = sm_phy_before + cc_bonus["物理攻击"]
sm_phy_gain = sm_phy_after / sm_phy_before - 1
print(f"  物理攻击收益: {sm_phy_before}→{sm_phy_after}, 收益={sm_phy_gain*100:.2f}%")

# 暴击收益
sm_crit_before = swordsman_base["暴击率"]
sm_crit_after = sm_crit_before + cc_bonus["暴击率"]
sm_crit_exp_before = (1 - sm_crit_before) + sm_crit_before * 1.5
sm_crit_exp_after = (1 - sm_crit_after) + sm_crit_after * 1.5
sm_crit_gain = sm_crit_exp_after / sm_crit_exp_before - 1
print(f"  暴击收益: {sm_crit_before*100:.0f}%→{sm_crit_after*100:.0f}%, 收益={sm_crit_gain*100:.2f}%")

# 综合
sm_total = (1 + sm_power_gain) * (1 + sm_phy_gain) * (1 + sm_crit_gain) - 1
print(f"  百分比综合收益: {sm_total*100:.2f}%")

# 边际对偶
marginal_ratio = sm_total / berserker_gu_total
print(f"\n  边际对偶倍数: {sm_total*100:.2f}% / {berserker_gu_total*100:.2f}% = {marginal_ratio:.2f}倍")

print(f"\n{'='*60}")
print("全部验证完成")
print(f"{'='*60}")
