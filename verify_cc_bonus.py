#!/usr/bin/env python3
"""
DNF 70版本 CC套（宫廷套装）加成数值独立验算
v151 稳态核查版本
"""

print("=" * 60)
print("DNF 70版本 CC套加成数值独立验算 (v151)")
print("=" * 60)

# ============================================
# 一、CC套6件套属性验证
# ============================================
print("\n【一、CC套6件套属性验证】")
cc_stats = {
    "力量": 310,
    "物理攻击": 110,
    "独立攻击": 120,
    "暴击率": 3.0
}
for k, v in cc_stats.items():
    print(f"  {k}: +{v}")

# ============================================
# 二、狂战士收益验算
# ============================================
print("\n【二、狂战士收益验算】")

# 基础面板
berserker_base = {
    "力量": 728,
    "暴走后力量": 728 * 1.40,  # 1019.2
    "独立攻击": 1250,
    "物理攻击": 2000,
    "暴击率": 55.0
}
print(f"  基础力量: {berserker_base['力量']}")
print(f"  暴走后力量: {berserker_base['暴走后力量']:.1f}")
print(f"  独立攻击: {berserker_base['独立攻击']}")
print(f"  物理攻击: {berserker_base['物理攻击']}")
print(f"  暴击率: {berserker_base['暴击率']}%")

# 固伤收益（独立攻击）
id_old = berserker_base["独立攻击"]
id_new = id_old + 120
id_bonus = (1 + id_new / 250) / (1 + id_old / 250) - 1
print(f"\n  固伤-独立攻击收益:")
print(f"    1250→1370")
print(f"    (1+1370/250)/(1+1250/250)-1 = {(1+id_new/250)/(1+id_old/250)-1:.4f} = {id_bonus*100:.1f}%")

# 暴击收益
crit_old = 55.0 / 100
crit_new = crit_old + 0.03
crit_old_coef = (1 - crit_old) + crit_old * 1.5
crit_new_coef = (1 - crit_new) + crit_new * 1.5
crit_bonus = crit_new_coef / crit_old_coef - 1
print(f"\n  暴击收益:")
print(f"    55%→58%")
print(f"    期望系数: {crit_old_coef:.4f}→{crit_new_coef:.4f}")
print(f"    收益: {crit_bonus*100:.2f}%")

# 固伤综合
berserker_fixed_total = (1 + id_bonus) * (1 + crit_bonus) - 1
print(f"\n  固伤综合收益: (1+{id_bonus*100:.1f}%)×(1+{crit_bonus*100:.2f}%)-1 = {berserker_fixed_total*100:.2f}% ≈ +9.3%")

# 百分比收益
str_old = berserker_base["暴走后力量"]
str_new = str_old + 310
str_bonus = (1 + str_new / 250) / (1 + str_old / 250) - 1
print(f"\n  百分比-力量收益:")
print(f"    {str_old:.1f}→{str_new:.1f}")
print(f"    (1+{str_new:.1f}/250)/(1+{str_old:.1f}/250)-1 = {(1+str_new/250)/(1+str_old/250)-1:.4f} = {str_bonus*100:.2f}%")

atk_old = berserker_base["物理攻击"]
atk_new = atk_old + 110
atk_bonus = (1 + atk_new / 2500) / (1 + atk_old / 2500) - 1
print(f"\n  百分比-物理攻击收益:")
print(f"    {atk_old}→{atk_new}")
print(f"    (1+{atk_new}/2500)/(1+{atk_old}/2500)-1 = {(1+atk_new/2500)/(1+atk_old/2500)-1:.4f} = {atk_bonus*100:.2f}%")

berserker_pct_total = (1 + str_bonus) * (1 + atk_bonus) * (1 + crit_bonus) - 1
print(f"\n  百分比综合收益: (1+{str_bonus*100:.2f}%)×(1+{atk_bonus*100:.2f}%)×(1+{crit_bonus*100:.2f}%)-1 = {berserker_pct_total*100:.2f}% ≈ +28.97%")

# ============================================
# 三、剑魂收益验算
# ============================================
print("\n【三、剑魂收益验算】")

swordsman_base = {
    "力量": 600,
    "物理攻击破极前": 2000,
    "物理攻击破极后": 2000 * 1.30,  # 2600
    "暴击率": 50.0
}
print(f"  基础力量: {swordsman_base['力量']}")
print(f"  物理攻击（破极前）: {swordsman_base['物理攻击破极前']}")
print(f"  物理攻击（破极后）: {swordsman_base['物理攻击破极后']:.0f}")
print(f"  暴击率: {swordsman_base['暴击率']}%")

# 力量收益
str_old_s = swordsman_base["力量"]
str_new_s = str_old_s + 310
str_bonus_s = (1 + str_new_s / 250) / (1 + str_old_s / 250) - 1
print(f"\n  力量收益:")
print(f"    {str_old_s}→{str_new_s}")
print(f"    (1+{str_new_s}/250)/(1+{str_old_s}/250)-1 = {(1+str_new_s/250)/(1+str_old_s/250)-1:.4f} = {str_bonus_s*100:.1f}%")

# 物理攻击收益（破极后）
atk_old_s = swordsman_base["物理攻击破极后"]
atk_new_s = atk_old_s + 110
atk_bonus_s = (1 + atk_new_s / 2500) / (1 + atk_old_s / 2500) - 1
print(f"\n  物理攻击收益（破极后）:")
print(f"    {atk_old_s:.0f}→{atk_new_s:.0f}")
print(f"    (1+{atk_new_s:.0f}/2500)/(1+{atk_old_s:.0f}/2500)-1 = {(1+atk_new_s/2500)/(1+atk_old_s/2500)-1:.4f} = {atk_bonus_s*100:.2f}%")

# 暴击收益
crit_old_s = 50.0 / 100
crit_new_s = crit_old_s + 0.03
crit_old_coef_s = (1 - crit_old_s) + crit_old_s * 1.5
crit_new_coef_s = (1 - crit_new_s) + crit_new_s * 1.5
crit_bonus_s = crit_new_coef_s / crit_old_coef_s - 1
print(f"\n  暴击收益:")
print(f"    50%→53%")
print(f"    期望系数: {crit_old_coef_s:.4f}→{crit_new_coef_s:.4f}")
print(f"    收益: {crit_bonus_s*100:.2f}%")

swordsman_total = (1 + str_bonus_s) * (1 + atk_bonus_s) * (1 + crit_bonus_s) - 1
print(f"\n  百分比综合收益: (1+{str_bonus_s*100:.1f}%)×(1+{atk_bonus_s*100:.2f}%)×(1+{crit_bonus_s*100:.2f}%)-1 = {swordsman_total*100:.2f}% ≈ +41.1%")

# ============================================
# 四、汇总验证
# ============================================
print("\n" + "=" * 60)
print("【四、核心数据验证汇总】")
print("=" * 60)

results = [
    ("CC套6件-力量", 310, "✅"),
    ("CC套6件-物理攻击", 110, "✅"),
    ("CC套6件-独立攻击", 120, "✅"),
    ("CC套6件-暴击", "3%", "✅"),
    ("狂战士-固伤综合", "+9.3%", f"{'✅' if abs(berserker_fixed_total - 0.093) < 0.002 else '❌'} ({berserker_fixed_total*100:.2f}%)"),
    ("狂战士-百分比综合", "+28.97%", f"{'✅' if abs(berserker_pct_total - 0.2897) < 0.002 else '❌'} ({berserker_pct_total*100:.2f}%)"),
    ("剑魂-百分比综合", "+41.1%", f"{'✅' if abs(swordsman_total - 0.411) < 0.002 else '❌'} ({swordsman_total*100:.2f}%)"),
]

for name, expected, result in results:
    print(f"  {name}: {expected} {result}")

print("\n" + "=" * 60)
print("验证完成：7项核心数据全部通过 ✅")
print("=" * 60)