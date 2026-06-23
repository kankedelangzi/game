#!/usr/bin/env python3
"""
任务19 CC套（宫廷套装）狂战士收益独立验算
数据来源：BERSERKER.md + dnf-costume-bonus.html
"""

print("=" * 60)
print("任务19 CC套狂战士收益独立验算")
print("=" * 60)

# === 基础面板（毕业级） ===
berserker_power_base = 728  # 暴走前
berserker_power_buffed = 728 * 1.40  # 暴走后 = 1019.2
berserker_indep = 1250
berserker_phy_atk = 2000
berserker_crit = 0.55

# === CC套加成 ===
cc_power = 310
cc_phy_atk = 110
cc_indep = 120
cc_crit = 0.03

# === 1. 独立攻击收益（固伤核心） ===
indep_old = 1 + berserker_indep / 250
indep_new = 1 + (berserker_indep + cc_indep) / 250
indep_benefit = indep_new / indep_old - 1
print(f"\n【独立攻击收益（固伤核心）】")
print(f"  基准独立: {berserker_indep}")
print(f"  CC后独立: {berserker_indep + cc_indep}")
print(f"  收益比: {indep_benefit*100:.2f}%")
print(f"  预期: +8.00%")
assert abs(indep_benefit - 0.08) < 0.001, f"独立攻击收益偏差: {indep_benefit}"

# === 2. 暴击收益 ===
crit_old_expect = (1 - berserker_crit) + berserker_crit * 1.5
crit_new_expect = (1 - (berserker_crit + cc_crit)) + (berserker_crit + cc_crit) * 1.5
crit_benefit = crit_new_expect / crit_old_expect - 1
print(f"\n【暴击收益】")
print(f"  基准暴击: {berserker_crit*100:.0f}%")
print(f"  CC后暴击: {(berserker_crit + cc_crit)*100:.0f}%")
print(f"  期望系数: {crit_old_expect:.4f} → {crit_new_expect:.4f}")
print(f"  收益比: {crit_benefit*100:.2f}%")
print(f"  预期: +1.18%")
assert abs(crit_benefit - 0.0118) < 0.001, f"暴击收益偏差: {crit_benefit}"

# === 3. 固伤综合收益 ===
solid_total = (1 + indep_benefit) * (1 + crit_benefit) - 1
print(f"\n【固伤综合收益】")
print(f"  综合收益: {solid_total*100:.2f}%")
print(f"  预期: +9.27%")
assert abs(solid_total - 0.0927) < 0.001, f"固伤综合收益偏差: {solid_total}"

# === 4. 百分比技能收益 ===
power_old = berserker_power_buffed  # 暴走后
power_new = power_old + cc_power
power_benefit = (1 + power_new/250) / (1 + power_old/250) - 1
print(f"\n【百分比技能 - 力量收益】")
print(f"  基准力量（暴走后）: {power_old:.1f}")
print(f"  CC后力量: {power_new:.1f}")
print(f"  收益比: {power_benefit*100:.2f}%")
print(f"  预期: +24.42%")
assert abs(power_benefit - 0.2442) < 0.001, f"力量收益偏差: {power_benefit}"

phy_atk_benefit = (berserker_phy_atk + cc_phy_atk) / berserker_phy_atk - 1
print(f"\n【百分比技能 - 物理攻击收益】")
print(f"  基准物理攻击: {berserker_phy_atk}")
print(f"  CC后物理攻击: {berserker_phy_atk + cc_phy_atk}")
print(f"  收益比: {phy_atk_benefit*100:.2f}%")
print(f"  预期: +5.50%")
assert abs(phy_atk_benefit - 0.055) < 0.001, f"物理攻击收益偏差: {phy_atk_benefit}"

# === 5. 百分比综合收益 ===
percent_total = (1 + power_benefit) * (1 + phy_atk_benefit) * (1 + crit_benefit) - 1
print(f"\n【百分比综合收益】")
print(f"  综合收益: {percent_total*100:.2f}%")
print(f"  预期: +32.81%")
assert abs(percent_total - 0.3281) < 0.001, f"百分比综合收益偏差: {percent_total}"

print("\n" + "=" * 60)
print("✅ 狂战士验算全部通过（5/5项）")
print("=" * 60)
