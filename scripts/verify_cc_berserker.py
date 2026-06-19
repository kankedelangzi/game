#!/usr/bin/env python3
"""
任务19 CC套（宫廷套装）狂战士收益独立验算
验证基准：v150修正版本（暴走后力量1019.2作为基准）
"""

print("=" * 60)
print("任务19 CC套狂战士收益独立验算")
print("=" * 60)

# ============================================
# 1. 基础面板配置（毕业级）
# ============================================
print("\n【1. 基础面板配置】")
berserker_base = {
    "力量": 728,
    "暴走后力量": 728 * 1.40,  # 暴走+40%
    "独立攻击": 1250,
    "物理攻击": 2000,
    "暴击率": 0.55
}
print(f"  力量: {berserker_base['力量']}")
print(f"  暴走后力量: {berserker_base['暴走后力量']:.1f}")
print(f"  独立攻击: {berserker_base['独立攻击']}")
print(f"  物理攻击: {berserker_base['物理攻击']}")
print(f"  暴击率: {berserker_base['暴击率']*100:.0f}%")

# ============================================
# 2. CC套加成
# ============================================
print("\n【2. CC套加成】")
cc_bonus = {
    "力量": 310,
    "物理攻击": 110,
    "独立攻击": 120,
    "暴击率": 0.03
}
print(f"  力量: +{cc_bonus['力量']}")
print(f"  物理攻击: +{cc_bonus['物理攻击']}")
print(f"  独立攻击: +{cc_bonus['独立攻击']}")
print(f"  暴击率: +{cc_bonus['暴击率']*100:.0f}%")

# ============================================
# 3. 固伤收益计算
# ============================================
print("\n【3. 固伤收益计算】")
# 独立攻击收益
ind_before = 1 + berserker_base["独立攻击"] / 250
ind_after = 1 + (berserker_base["独立攻击"] + cc_bonus["独立攻击"]) / 250
ind_bonus = ind_after / ind_before - 1
print(f"  独立攻击收益: ({ind_after:.4f})/({ind_before:.4f}) - 1 = {ind_bonus*100:.2f}%")

# 暴击收益（期望伤害系数）
crit_before = (1 - berserker_base["暴击率"]) + berserker_base["暴击率"] * 1.5
crit_after = (1 - (berserker_base["暴击率"] + cc_bonus["暴击率"])) + (berserker_base["暴击率"] + cc_bonus["暴击率"]) * 1.5
crit_bonus = crit_after / crit_before - 1
print(f"  暴击收益: ({crit_after:.4f})/({crit_before:.4f}) - 1 = {crit_bonus*100:.2f}%")

# 固伤综合
berserker_fixed_bonus = (1 + ind_bonus) * (1 + crit_bonus) - 1
print(f"  固伤综合收益: (1+{ind_bonus*100:.2f}%) × (1+{crit_bonus*100:.2f}%) - 1 = {berserker_fixed_bonus*100:.2f}%")

# ============================================
# 4. 百分比收益计算
# ============================================
print("\n【4. 百分比收益计算（使用暴走后力量1019.2）】")
# 力量收益（使用暴走后力量作为基准）
str_before = 1 + berserker_base["暴走后力量"] / 250
str_after = 1 + (berserker_base["暴走后力量"] + cc_bonus["力量"]) / 250
str_bonus = str_after / str_before - 1
print(f"  力量收益: ({str_after:.4f})/({str_before:.4f}) - 1 = {str_bonus*100:.2f}%")

# 物理攻击收益
phy_before = 1 + berserker_base["物理攻击"] / 2500
phy_after = 1 + (berserker_base["物理攻击"] + cc_bonus["物理攻击"]) / 2500
phy_bonus = phy_after / phy_before - 1
print(f"  物理攻击收益: ({phy_after:.4f})/({phy_before:.4f}) - 1 = {phy_bonus*100:.2f}%")

# 暴击收益（同固伤）
print(f"  暴击收益: {crit_bonus*100:.2f}%")

# 百分比综合
berserker_pct_bonus = (1 + str_bonus) * (1 + phy_bonus) * (1 + crit_bonus) - 1
print(f"  百分比综合收益: (1+{str_bonus*100:.2f}%) × (1+{phy_bonus*100:.2f}%) × (1+{crit_bonus*100:.2f}%) - 1 = {berserker_pct_bonus*100:.2f}%")

# ============================================
# 5. 剑魂收益计算
# ============================================
print("\n【5. 剑魂收益计算（百分比流，破极兵刃状态）】")
swordsman_base = {
    "力量": 600,
    "物理攻击_破极后": 2000 * 1.30,  # 破极兵刃+30%
    "暴击率": 0.50
}
print(f"  力量: {swordsman_base['力量']}")
print(f"  物理攻击（破极后）: {swordsman_base['物理攻击_破极后']:.0f}")
print(f"  暴击率: {swordsman_base['暴击率']*100:.0f}%")

# 力量收益
str_before_s = 1 + swordsman_base["力量"] / 250
str_after_s = 1 + (swordsman_base["力量"] + cc_bonus["力量"]) / 250
str_bonus_s = str_after_s / str_before_s - 1
print(f"  力量收益: ({str_after_s:.4f})/({str_before_s:.4f}) - 1 = {str_bonus_s*100:.2f}%")

# 物理攻击收益（破极后）
phy_before_s = 1 + swordsman_base["物理攻击_破极后"] / 2500
phy_after_s = 1 + (swordsman_base["物理攻击_破极后"] + cc_bonus["物理攻击"]) / 2500
phy_bonus_s = phy_after_s / phy_before_s - 1
print(f"  物理攻击收益: ({phy_after_s:.4f})/({phy_before_s:.4f}) - 1 = {phy_bonus_s*100:.2f}%")

# 暴击收益
crit_before_s = (1 - swordsman_base["暴击率"]) + swordsman_base["暴击率"] * 1.5
crit_after_s = (1 - (swordsman_base["暴击率"] + cc_bonus["暴击率"])) + (swordsman_base["暴击率"] + cc_bonus["暴击率"]) * 1.5
crit_bonus_s = crit_after_s / crit_before_s - 1
print(f"  暴击收益: ({crit_after_s:.4f})/({crit_before_s:.4f}) - 1 = {crit_bonus_s*100:.2f}%")

# 剑魂综合
swordsman_bonus = (1 + str_bonus_s) * (1 + phy_bonus_s) * (1 + crit_bonus_s) - 1
print(f"  剑魂综合收益: (1+{str_bonus_s*100:.2f}%) × (1+{phy_bonus_s*100:.2f}%) × (1+{crit_bonus_s*100:.2f}%) - 1 = {swordsman_bonus*100:.2f}%")

# ============================================
# 6. 结果汇总与对比
# ============================================
print("\n" + "=" * 60)
print("【验算结果汇总】")
print("=" * 60)
print(f"  狂战士固伤综合:   {berserker_fixed_bonus*100:.2f}%  (报告值: +9.3%)")
print(f"  狂战士百分比综合: {berserker_pct_bonus*100:.2f}%  (报告值: +28.97%)")
print(f"  剑魂百分比综合:   {swordsman_bonus*100:.2f}%  (报告值: +41.1%)")

# ============================================
# 7. 验证结论
# ============================================
print("\n" + "=" * 60)
print("【验证结论】")
print("=" * 60)
tolerance = 0.05  # 允许0.05%的精度差异

checks = [
    ("狂战士固伤综合", berserker_fixed_bonus*100, 9.3),
    ("狂战士百分比综合", berserker_pct_bonus*100, 28.97),
    ("剑魂百分比综合", swordsman_bonus*100, 41.1),
]

all_passed = True
for name, actual, expected in checks:
    diff = abs(actual - expected)
    status = "✅ 通过" if diff <= tolerance else "❌ 失败"
    if diff > tolerance:
        all_passed = False
    print(f"  {name}: 计算值={actual:.2f}%, 报告值={expected}%, 差异={diff:.2f}pp {status}")

print("\n" + "=" * 60)
if all_passed:
    print("✅ 全部验算通过，数据准确可靠")
else:
    print("❌ 存在精度差异，需进一步核查")
print("=" * 60)