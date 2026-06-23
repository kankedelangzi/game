#!/usr/bin/env python3
"""
任务19 CC套（宫廷套装）剑魂收益独立验算
数据来源：SWORDSMAN.md + dnf-costume-bonus.html
"""

print("=" * 60)
print("任务19 CC套剑魂收益独立验算")
print("=" * 60)

# === 基础面板（毕业级，破极兵刃状态） ===
swordsman_power = 600
swordsman_phy_atk_base = 2000
swordsman_phy_atk_buffed = 2000 * 1.30  # 破极兵刃 = 2600
swordsman_crit = 0.50

# === CC套加成 ===
cc_power = 310
cc_phy_atk = 110
cc_crit = 0.03

# === 1. 力量收益 ===
power_old = 1 + swordsman_power / 250
power_new = 1 + (swordsman_power + cc_power) / 250
power_benefit = power_new / power_old - 1
print(f"\n【力量收益】")
print(f"  基准力量: {swordsman_power}")
print(f"  CC后力量: {swordsman_power + cc_power}")
print(f"  收益比: {power_benefit*100:.2f}%")
print(f"  预期: +36.47%")
assert abs(power_benefit - 0.3647) < 0.001, f"力量收益偏差: {power_benefit}"

# === 2. 物理攻击收益（破极后） ===
phy_atk_benefit = (swordsman_phy_atk_buffed + cc_phy_atk) / swordsman_phy_atk_buffed - 1
print(f"\n【物理攻击收益（破极后）】")
print(f"  基准物理攻击（破极后）: {swordsman_phy_atk_buffed}")
print(f"  CC后物理攻击: {swordsman_phy_atk_buffed + cc_phy_atk}")
print(f"  收益比: {phy_atk_benefit*100:.2f}%")
print(f"  预期: +4.23%")
assert abs(phy_atk_benefit - 0.0423) < 0.001, f"物理攻击收益偏差: {phy_atk_benefit}"

# === 3. 暴击收益 ===
crit_old_expect = (1 - swordsman_crit) + swordsman_crit * 1.5
crit_new_expect = (1 - (swordsman_crit + cc_crit)) + (swordsman_crit + cc_crit) * 1.5
crit_benefit = crit_new_expect / crit_old_expect - 1
print(f"\n【暴击收益】")
print(f"  基准暴击: {swordsman_crit*100:.0f}%")
print(f"  CC后暴击: {(swordsman_crit + cc_crit)*100:.0f}%")
print(f"  期望系数: {crit_old_expect:.4f} → {crit_new_expect:.4f}")
print(f"  收益比: {crit_benefit*100:.2f}%")
print(f"  预期: +1.20%")
assert abs(crit_benefit - 0.012) < 0.001, f"暴击收益偏差: {crit_benefit}"

# === 4. 百分比综合收益 ===
percent_total = (1 + power_benefit) * (1 + phy_atk_benefit) * (1 + crit_benefit) - 1
print(f"\n【百分比综合收益】")
print(f"  综合收益: {percent_total*100:.2f}%")
print(f"  预期: +43.95%")
assert abs(percent_total - 0.4395) < 0.001, f"百分比综合收益偏差: {percent_total}"

# === 5. 边际对偶验证（系统固有频率） ===
solid_total = 0.0927  # 狂战士固伤综合
swordsman_percent = percent_total
ratio = swordsman_percent / solid_total
print(f"\n【边际对偶验证】")
print(f"  剑魂百分比收益: {swordsman_percent*100:.2f}%")
print(f"  狂战士固伤收益: {solid_total*100:.2f}%")
print(f"  收益倍数: {ratio:.2f}倍")
print(f"  预期: ~4.74倍")
assert abs(ratio - 4.74) < 0.1, f"边际对偶偏差: {ratio}"

print("\n" + "=" * 60)
print("✅ 剑魂验算全部通过（4/4项）")
print("✅ 边际对偶验证通过（4.74倍系统固有频率确认）")
print("=" * 60)
