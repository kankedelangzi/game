#!/usr/bin/env python3
"""
CC套（宫廷套装）各职业加成数值 - Python独立验算
稳态核查 v261
"""

print("=" * 60)
print("CC套（宫廷套装）加成数值 - Python独立验算")
print("=" * 60)

# ==================== 基础数据 ====================
# CC套6件套属性
cc_power = 310
cc_phy_atk = 110
cc_independent = 120
cc_crit = 0.03  # 3%

# 暴击伤害倍率（DNF 70标准）
crit_dmg = 1.5

# ==================== 狂战士面板 ====================
# 暴走后力量
berserker_base_power = 728
berserker_buff_power = 728 * 1.40  # 暴走+40%
berserker_independent = 1250
berserker_phy_atk = 2000
berserker_crit = 0.55  # 55%

# ==================== 剑魂面板 ====================
swordsman_base_power = 600
swordsman_phy_atk_normal = 2000
swordsman_phy_atk_buff = 2000 * 1.30  # 破极兵刃+30%
swordsman_crit = 0.50  # 50%

print("\n" + "=" * 60)
print("一、狂战士收益验算")
print("=" * 60)

# --- 固伤技能收益 ---
print("\n【固伤技能收益】")

# 独立攻击收益
independent_old = 1 + berserker_independent / 250
independent_new = 1 + (berserker_independent + cc_independent) / 250
independent_benefit = independent_new / independent_old - 1
print(f"  独立攻击: {berserker_independent} → {berserker_independent + cc_independent}")
print(f"  收益比: ({independent_new:.4f} / {independent_old:.4f}) - 1 = {independent_benefit*100:.2f}%")

# 暴击收益（期望伤害系数）
crit_old = (1 - berserker_crit) + berserker_crit * crit_dmg
crit_new = (1 - (berserker_crit + cc_crit)) + (berserker_crit + cc_crit) * crit_dmg
crit_benefit = crit_new / crit_old - 1
print(f"  暴击期望: {crit_old:.4f} → {crit_new:.4f}")
print(f"  收益比: {crit_new:.4f} / {crit_old:.4f} - 1 = {crit_benefit*100:.2f}%")

# 固伤综合收益
berserker_fixed_total = (1 + independent_benefit) * (1 + crit_benefit) - 1
print(f"  固伤综合: (1+{independent_benefit*100:.2f}%) × (1+{crit_benefit*100:.2f}%) - 1 = {berserker_fixed_total*100:.2f}%")

# --- 百分比技能收益 ---
print("\n【百分比技能收益（暴走后）】")

# 力量收益
power_old = 1 + berserker_buff_power / 250
power_new = 1 + (berserker_buff_power + cc_power) / 250
power_benefit = power_new / power_old - 1
print(f"  力量: {berserker_buff_power:.1f} → {berserker_buff_power + cc_power:.1f}")
print(f"  收益比: ({power_new:.4f} / {power_old:.4f}) - 1 = {power_benefit*100:.2f}%")

# 物理攻击收益
phy_old = berserker_phy_atk
phy_new = berserker_phy_atk + cc_phy_atk
phy_benefit = phy_new / phy_old - 1
print(f"  物理攻击: {phy_old} → {phy_new}")
print(f"  收益比: {phy_new} / {phy_old} - 1 = {phy_benefit*100:.2f}%")

# 暴击收益
print(f"  暴击收益: {crit_benefit*100:.2f}%（同上）")

# 百分比综合收益
berserker_percent_total = power_benefit + phy_benefit + crit_benefit + power_benefit * phy_benefit + power_benefit * crit_benefit + phy_benefit * crit_benefit + power_benefit * phy_benefit * crit_benefit
# 更准确的计算
berserker_percent_total_v2 = (power_new / power_old) * (phy_new / phy_old) * (crit_new / crit_old) - 1
print(f"  百分比综合: ({power_new:.4f}/{power_old:.4f}) × ({phy_new}/{phy_old}) × ({crit_new:.4f}/{crit_old:.4f}) - 1 = {berserker_percent_total_v2*100:.2f}%")

print("\n" + "=" * 60)
print("二、剑魂收益验算（破极兵刃状态下）")
print("=" * 60)

# --- 百分比技能收益 ---
print("\n【百分比技能收益】")

# 力量收益
s_power_old = 1 + swordsman_base_power / 250
s_power_new = 1 + (swordsman_base_power + cc_power) / 250
s_power_benefit = s_power_new / s_power_old - 1
print(f"  力量: {swordsman_base_power} → {swordsman_base_power + cc_power}")
print(f"  收益比: ({s_power_new:.4f} / {s_power_old:.4f}) - 1 = {s_power_benefit*100:.2f}%")

# 物理攻击收益（破极后）
s_phy_old = swordsman_phy_atk_buff
s_phy_new = swordsman_phy_atk_buff + cc_phy_atk
s_phy_benefit = s_phy_new / s_phy_old - 1
print(f"  物理攻击（破极后）: {s_phy_old:.0f} → {s_phy_new:.0f}")
print(f"  收益比: {s_phy_new:.0f} / {s_phy_old:.0f} - 1 = {s_phy_benefit*100:.2f}%")

# 暴击收益
s_crit_old = (1 - swordsman_crit) + swordsman_crit * crit_dmg
s_crit_new = (1 - (swordsman_crit + cc_crit)) + (swordsman_crit + cc_crit) * crit_dmg
s_crit_benefit = s_crit_new / s_crit_old - 1
print(f"  暴击期望: {s_crit_old:.4f} → {s_crit_new:.4f}")
print(f"  收益比: {s_crit_new:.4f} / {s_crit_old:.4f} - 1 = {s_crit_benefit*100:.2f}%")

# 百分比综合收益
swordsman_percent_total = (s_power_new / s_power_old) * (s_phy_new / s_phy_old) * (s_crit_new / s_crit_old) - 1
print(f"  百分比综合: ({s_power_new:.4f}/{s_power_old:.4f}) × ({s_phy_new:.0f}/{s_phy_old:.0f}) × ({s_crit_new:.4f}/{s_crit_old:.4f}) - 1 = {swordsman_percent_total*100:.2f}%")

print("\n" + "=" * 60)
print("三、对比验证")
print("=" * 60)

# 边际对偶验证：剑魂/狂战士固伤收益倍数
ratio = swordsman_percent_total / berserker_fixed_total
print(f"\n【边际对偶验证】")
print(f"  剑魂百分比综合 / 狂战士固伤综合 = {swordsman_percent_total*100:.2f}% / {berserker_fixed_total*100:.2f}% = {ratio:.2f}倍")
print(f"  系统固有频率: 4.74倍 ✓")

print("\n" + "=" * 60)
print("四、验算结果汇总")
print("=" * 60)

results = [
    ("狂战士固伤-独立攻击收益", independent_benefit * 100, 8.00),
    ("狂战士固伤-暴击收益", crit_benefit * 100, 1.18),
    ("狂战士固伤-综合收益", berserker_fixed_total * 100, 9.27),
    ("狂战士百分比-力量收益", power_benefit * 100, 24.42),
    ("狂战士百分比-物理攻击收益", phy_benefit * 100, 5.50),
    ("狂战士百分比-暴击收益", crit_benefit * 100, 1.18),
    ("狂战士百分比-综合收益", berserker_percent_total_v2 * 100, 32.81),
    ("剑魂百分比-力量收益", s_power_benefit * 100, 36.50),
    ("剑魂百分比-物理攻击收益", s_phy_benefit * 100, 4.23),
    ("剑魂百分比-暴击收益", s_crit_benefit * 100, 1.20),
    ("剑魂百分比-综合收益", swordsman_percent_total * 100, 43.95),
    ("边际对偶倍数", ratio, 4.74),
]

passed = 0
failed = 0
for name, actual, expected in results:
    diff = abs(actual - expected)
    tolerance = 0.1  # 0.1% 容差
    status = "✅" if diff <= tolerance else "❌"
    if diff <= tolerance:
        passed += 1
    else:
        failed += 1
    print(f"  {status} {name}: {actual:.2f}% (预期 {expected:.2f}%, 差异 {diff:.2f}pp)")

print(f"\n{'='*60}")
print(f"验算完成: {passed}/{len(results)} 通过, {failed} 失败")
print(f"{'='*60}")

if failed == 0:
    print("\n🎉 所有验算项100%通过！数据准确可靠。")
else:
    print(f"\n⚠️ 有 {failed} 项验算未通过，需核查。")