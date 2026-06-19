#!/usr/bin/env python3
"""任务19 CC套稳态核查 — Python独立验算"""

print("=" * 60)
print("任务19 CC套稳态核查 — Python独立验算")
print("=" * 60)

# =============================================
# 1. CC套6件套属性验证
# =============================================
print("\n【1】CC套6件套属性验证")
parts = {
    "上衣": (55, 20, 20, 0.5),
    "下装": (55, 20, 20, 0.5),
    "头饰": (50, 18, 18, 0.5),
    "帽子": (50, 18, 18, 0.5),
    "脸部": (50, 18, 18, 0.5),
    "胸部": (50, 16, 26, 0.5)
}
total_str = sum(p[0] for p in parts.values())
total_phy = sum(p[1] for p in parts.values())
total_ind = sum(p[2] for p in parts.values())
total_crit = sum(p[3] for p in parts.values())
print(f"  力量合计: {total_str} (预期310) → {'✅' if total_str == 310 else '❌'}")
print(f"  物理攻击合计: {total_phy} (预期110) → {'✅' if total_phy == 110 else '❌'}")
print(f"  独立攻击合计: {total_ind} (预期120) → {'✅' if total_ind == 120 else '❌'}")
print(f"  暴击率合计: {total_crit}% (预期3.0%) → {'✅' if total_crit == 3.0 else '❌'}")

# =============================================
# 2. 狂战士固伤收益验算
# =============================================
print("\n【2】狂战士固伤收益验算")
ind_base = 1250
ind_new = ind_base + 120
ind_gain = (1 + ind_new/250) / (1 + ind_base/250) - 1
crit_base = 0.55
crit_new = crit_base + 0.03
crit_old_exp = (1 - crit_base) + crit_base * 1.5
crit_new_exp = (1 - crit_new) + crit_new * 1.5
crit_gain = crit_new_exp / crit_old_exp - 1
berserker_fgu = (1 + ind_gain) * (1 + crit_gain) - 1
print(f"  独立攻击收益: {ind_gain*100:.2f}% (报告+8.0%) → {'✅' if abs(ind_gain*100 - 8.0) < 0.05 else '❌'}")
print(f"  暴击收益: {crit_gain*100:.2f}% (报告+1.2%) → {'✅' if abs(crit_gain*100 - 1.2) < 0.05 else '❌'}")
print(f"  固伤综合收益: {berserker_fgu*100:.2f}% (报告+9.3%) → {'✅' if abs(berserker_fgu*100 - 9.3) < 0.05 else '❌'}")

# =============================================
# 3. 狂战士百分比收益验算（暴走后力量基准）
# =============================================
print("\n【3】狂战士百分比收益验算（暴走后力量基准）")
str_base = 728 * 1.40
str_new = str_base + 310
str_gain = (1 + str_new/250) / (1 + str_base/250) - 1
phy_base = 2000
phy_new = phy_base + 110
phy_gain = (1 + phy_new/2500) / (1 + phy_base/2500) - 1
berserker_percent = (1 + str_gain) * (1 + phy_gain) * (1 + crit_gain) - 1
print(f"  暴走后力量: {str_base} (预期1019.2)")
print(f"  力量收益: {str_gain*100:.2f}% (报告+24.42%) → {'✅' if abs(str_gain*100 - 24.42) < 0.05 else '❌'}")
print(f"  物理攻击收益: {phy_gain*100:.2f}% (报告+2.44%) → {'✅' if abs(phy_gain*100 - 2.44) < 0.05 else '❌'}")
print(f"  百分比综合收益: {berserker_percent*100:.2f}% (报告+28.97%) → {'✅' if abs(berserker_percent*100 - 28.97) < 0.05 else '❌'}")

# =============================================
# 4. 剑魂百分比收益验算
# =============================================
print("\n【4】剑魂百分比收益验算（破极兵刃状态下）")
sword_str_base = 600
sword_str_new = sword_str_base + 310
sword_str_gain = (1 + sword_str_new/250) / (1 + sword_str_base/250) - 1
sword_phy_base = 2000 * 1.30  # 破极后
sword_phy_new = sword_phy_base + 110
sword_phy_gain = (1 + sword_phy_new/2500) / (1 + sword_phy_base/2500) - 1
sword_crit_base = 0.50
sword_crit_new = sword_crit_base + 0.03
sword_crit_old_exp = (1 - sword_crit_base) + sword_crit_base * 1.5
sword_crit_new_exp = (1 - sword_crit_new) + sword_crit_new * 1.5
sword_crit_gain = sword_crit_new_exp / sword_crit_old_exp - 1
sword_percent = (1 + sword_str_gain) * (1 + sword_phy_gain) * (1 + sword_crit_gain) - 1
print(f"  力量收益: {sword_str_gain*100:.2f}% (报告+36.5%) → {'✅' if abs(sword_str_gain*100 - 36.5) < 0.05 else '❌'}")
print(f"  物理攻击收益: {sword_phy_gain*100:.2f}% (报告+2.2%) → {'✅' if abs(sword_phy_gain*100 - 2.2) < 0.05 else '❌'}")
print(f"  暴击收益: {sword_crit_gain*100:.2f}% (报告+1.2%) → {'✅' if abs(sword_crit_gain*100 - 1.2) < 0.05 else '❌'}")
print(f"  百分比综合收益: {sword_percent*100:.2f}% (报告+41.1%) → {'✅' if abs(sword_percent*100 - 41.1) < 0.05 else '❌'}")

# =============================================
# 5. 收益差异分析
# =============================================
print("\n【5】收益差异分析")
ratio = sword_percent / berserker_fgu
print(f"  剑魂百分比收益 / 狂战士固伤收益 = {sword_percent*100:.2f}% / {berserker_fgu*100:.2f}% = {ratio:.1f}倍")
print(f"  报告结论：约4.4倍 → {'✅' if abs(ratio - 4.4) < 0.1 else '❌'}")

# =============================================
# 总结
# =============================================
print("\n" + "=" * 60)
all_pass = (
    total_str == 310 and total_phy == 110 and total_ind == 120 and total_crit == 3.0 and
    abs(ind_gain*100 - 8.0) < 0.05 and abs(crit_gain*100 - 1.2) < 0.05 and abs(berserker_fgu*100 - 9.3) < 0.05 and
    abs(str_gain*100 - 24.42) < 0.05 and abs(phy_gain*100 - 2.44) < 0.05 and abs(berserker_percent*100 - 28.97) < 0.05 and
    abs(sword_str_gain*100 - 36.5) < 0.05 and abs(sword_phy_gain*100 - 2.2) < 0.05 and abs(sword_crit_gain*100 - 1.2) < 0.05 and abs(sword_percent*100 - 41.1) < 0.05
)
if all_pass:
    print("✅ 稳态核查通过：所有14项数据100%匹配")
else:
    print("❌ 稳态核查发现偏差，需修正")
print("=" * 60)
