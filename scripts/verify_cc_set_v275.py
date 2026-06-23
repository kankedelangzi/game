#!/usr/bin/env python3
"""
稳态核查 v275 - CC套（宫廷套装）各职业加成数值独立验算
验证时间: 2026-06-23 15:45 (Asia/Shanghai)
"""

print("=" * 60)
print("稳态核查 v275 - CC套独立验算")
print("=" * 60)

# ==================== 1. CC套单件属性验证 ====================
print("\n【1】CC套单件属性累加验证")
pieces = {
    "上衣": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击": 0.5},
    "下装": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击": 0.5},
    "头饰": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击": 0.5},
    "帽子": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击": 0.5},
    "脸部": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击": 0.5},
    "胸部": {"力量": 50, "物理攻击": 16, "独立攻击": 26, "暴击": 0.5},
}

total_power = sum(p["力量"] for p in pieces.values())
total_phy_atk = sum(p["物理攻击"] for p in pieces.values())
total_independent = sum(p["独立攻击"] for p in pieces.values())
total_crit = sum(p["暴击"] for p in pieces.values())

print(f"  力量合计: {total_power} (预期310) → {'✅' if total_power == 310 else '❌'}")
print(f"  物理攻击合计: {total_phy_atk} (预期110) → {'✅' if total_phy_atk == 110 else '❌'}")
print(f"  独立攻击合计: {total_independent} (预期120) → {'✅' if total_independent == 120 else '❌'}")
print(f"  暴击率合计: {total_crit}% (预期3.0%) → {'✅' if total_crit == 3.0 else '❌'}")

# ==================== 2. 狂战士固伤收益验证 ====================
print("\n【2】狂战士固伤收益验证")
berserker_ind = 1250
berserker_ind_new = berserker_ind + 120
ind_gain = (1 + berserker_ind_new / 250) / (1 + berserker_ind / 250) - 1
print(f"  独立攻击收益: {ind_gain*100:.2f}% (预期8.00%) → {'✅' if abs(ind_gain*100 - 8.00) < 0.01 else '❌'}")

berserker_crit_old = 0.55
berserker_crit_new = berserker_crit_old + 0.03
crit_coef_old = (1 - berserker_crit_old) + berserker_crit_old * 1.5
crit_coef_new = (1 - berserker_crit_new) + berserker_crit_new * 1.5
crit_gain = crit_coef_new / crit_coef_old - 1
print(f"  暴击收益: {crit_gain*100:.2f}% (预期1.18%) → {'✅' if abs(crit_gain*100 - 1.18) < 0.01 else '❌'}")

berserker_fixed_total = (1 + ind_gain) * (1 + crit_gain) - 1
print(f"  固伤综合收益: {berserker_fixed_total*100:.2f}% (预期9.27%) → {'✅' if abs(berserker_fixed_total*100 - 9.27) < 0.01 else '❌'}")

# ==================== 3. 狂战士百分比收益验证 ====================
print("\n【3】狂战士百分比收益验证")
berserker_str_base = 728
berserker_str_burst = berserker_str_base * 1.40  # 暴走+40%
berserker_str_new = berserker_str_burst + 310
str_gain_berserker = (1 + berserker_str_new / 250) / (1 + berserker_str_burst / 250) - 1
print(f"  力量收益(暴走后): {str_gain_berserker*100:.2f}% (预期24.42%) → {'✅' if abs(str_gain_berserker*100 - 24.42) < 0.01 else '❌'}")

berserker_phy_base = 2000
berserker_phy_new = berserker_phy_base + 110
phy_gain_berserker = berserker_phy_new / berserker_phy_base - 1
print(f"  物理攻击收益: {phy_gain_berserker*100:.2f}% (预期5.50%) → {'✅' if abs(phy_gain_berserker*100 - 5.50) < 0.01 else '❌'}")

berserker_pct_total = (1 + str_gain_berserker) * (1 + phy_gain_berserker) * (1 + crit_gain) - 1
print(f"  百分比综合收益: {berserker_pct_total*100:.2f}% (预期32.81%) → {'✅' if abs(berserker_pct_total*100 - 32.81) < 0.01 else '❌'}")

# ==================== 4. 剑魂百分比收益验证 ====================
print("\n【4】剑魂百分比收益验证")
swordsman_str_base = 600
swordsman_str_new = swordsman_str_base + 310
str_gain_swordsman = (1 + swordsman_str_new / 250) / (1 + swordsman_str_base / 250) - 1
print(f"  力量收益: {str_gain_swordsman*100:.2f}% (预期36.47%) → {'✅' if abs(str_gain_swordsman*100 - 36.47) < 0.01 else '❌'}")

swordsman_phy_base = 2600  # 破极后
swordsman_phy_new = swordsman_phy_base + 110
phy_gain_swordsman = swordsman_phy_new / swordsman_phy_base - 1
print(f"  物理攻击收益(破极后): {phy_gain_swordsman*100:.2f}% (预期4.23%) → {'✅' if abs(phy_gain_swordsman*100 - 4.23) < 0.01 else '❌'}")

swordsman_crit_old = 0.50
swordsman_crit_new = swordsman_crit_old + 0.03
swordsman_crit_coef_old = (1 - swordsman_crit_old) + swordsman_crit_old * 1.5
swordsman_crit_coef_new = (1 - swordsman_crit_new) + swordsman_crit_new * 1.5
swordsman_crit_gain = swordsman_crit_coef_new / swordsman_crit_coef_old - 1
print(f"  暴击收益: {swordsman_crit_gain*100:.2f}% (预期1.20%) → {'✅' if abs(swordsman_crit_gain*100 - 1.20) < 0.01 else '❌'}")

swordsman_pct_total = (1 + str_gain_swordsman) * (1 + phy_gain_swordsman) * (1 + swordsman_crit_gain) - 1
print(f"  百分比综合收益: {swordsman_pct_total*100:.2f}% (预期43.95%) → {'✅' if abs(swordsman_pct_total*100 - 43.95) < 0.01 else '❌'}")

# ==================== 5. 边际对偶验证 ====================
print("\n【5】边际对偶验证（系统固有频率）")
ratio = swordsman_pct_total / berserker_fixed_total
print(f"  剑魂百分比/狂战士固伤 = {ratio:.2f}倍 (预期4.74倍) → {'✅' if abs(ratio - 4.74) < 0.05 else '❌'}")

# ==================== 总结 ====================
print("\n" + "=" * 60)
print("稳态核查 v275 完成")
print("=" * 60)
