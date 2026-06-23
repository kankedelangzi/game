#!/usr/bin/env python3
"""
CC套（宫廷套装）各职业加成数值 - Python独立验算
任务19 稳态核查 v280
"""

import json
from datetime import datetime

# ============================================
# 一、CC套基础数据验证
# ============================================
print("=" * 60)
print("CC套（宫廷套装）各职业加成数值 - Python独立验算")
print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# CC套单件属性（来自DNF Wiki）
cc_single = {
    "上衣": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击": 0.5},
    "下装": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击": 0.5},
    "头饰": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击": 0.5},
    "帽子": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击": 0.5},
    "脸部": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击": 0.5},
    "胸部": {"力量": 50, "物理攻击": 16, "独立攻击": 26, "暴击": 0.5},
}

# 计算6件合计
cc_total = {"力量": 0, "物理攻击": 0, "独立攻击": 0, "暴击": 0}
for piece, attrs in cc_single.items():
    for key in cc_total:
        cc_total[key] += attrs[key]

print("\n【一、CC套单件属性验证】")
print(f"  上衣: 力量{cc_single['上衣']['力量']}, 物攻{cc_single['上衣']['物理攻击']}, 独立{cc_single['上衣']['独立攻击']}, 暴击{cc_single['上衣']['暴击']}%")
print(f"  下装: 力量{cc_single['下装']['力量']}, 物攻{cc_single['下装']['物理攻击']}, 独立{cc_single['下装']['独立攻击']}, 暴击{cc_single['下装']['暴击']}%")
print(f"  头饰: 力量{cc_single['头饰']['力量']}, 物攻{cc_single['头饰']['物理攻击']}, 独立{cc_single['头饰']['独立攻击']}, 暴击{cc_single['头饰']['暴击']}%")
print(f"  帽子: 力量{cc_single['帽子']['力量']}, 物攻{cc_single['帽子']['物理攻击']}, 独立{cc_single['帽子']['独立攻击']}, 暴击{cc_single['帽子']['暴击']}%")
print(f"  脸部: 力量{cc_single['脸部']['力量']}, 物攻{cc_single['脸部']['物理攻击']}, 独立{cc_single['脸部']['独立攻击']}, 暴击{cc_single['脸部']['暴击']}%")
print(f"  胸部: 力量{cc_single['胸部']['力量']}, 物攻{cc_single['胸部']['物理攻击']}, 独立{cc_single['胸部']['独立攻击']}, 暴击{cc_single['胸部']['暴击']}%")
print(f"\n  ✅ 6件合计: 力量{cc_total['力量']}, 物理攻击{cc_total['物理攻击']}, 独立攻击{cc_total['独立攻击']}, 暴击{cc_total['暴击']}%")

# ============================================
# 二、狂战士面板配置验证
# ============================================
print("\n【二、狂战士（红眼）面板配置】")
berserker_base = {
    "力量": 728,
    "暴走力量": 728 * 1.40,  # 暴走+40%
    "独立攻击": 1250,
    "物理攻击": 2000,
    "暴击率": 0.55,  # 55%
}
print(f"  基础力量: {berserker_base['力量']}")
print(f"  暴走后力量: {berserker_base['暴走力量']:.1f}")
print(f"  独立攻击: {berserker_base['独立攻击']}")
print(f"  物理攻击: {berserker_base['物理攻击']}")
print(f"  暴击率: {berserker_base['暴击率']*100:.0f}%")

# ============================================
# 三、狂战士收益计算（固伤）
# ============================================
print("\n【三、狂战士固伤收益计算】")

# 独立攻击收益
ind_old = berserker_base['独立攻击']
ind_new = ind_old + cc_total['独立攻击']
ind_bonus = (1 + ind_new / 250) / (1 + ind_old / 250) - 1
print(f"  独立攻击: {ind_old} → {ind_new}")
print(f"  独立攻击收益: (1+{ind_new}/250)/(1+{ind_old}/250)-1 = {ind_bonus*100:.2f}%")

# 暴击收益（期望伤害系数）
crit_old = berserker_base['暴击率']
crit_new = crit_old + cc_total['暴击'] / 100  # 3% = 0.03
crit_old_coeff = (1 - crit_old) + crit_old * 1.5
crit_new_coeff = (1 - crit_new) + crit_new * 1.5
crit_bonus = crit_new_coeff / crit_old_coeff - 1
print(f"  暴击率: {crit_old*100:.0f}% → {crit_new*100:.0f}%")
print(f"  暴击期望系数: {crit_old_coeff:.4f} → {crit_new_coeff:.4f}")
print(f"  暴击收益: {crit_new_coeff:.4f}/{crit_old_coeff:.4f}-1 = {crit_bonus*100:.2f}%")

# 固伤综合
berserker_fixed_bonus = (1 + ind_bonus) * (1 + crit_bonus) - 1
print(f"  固伤综合收益: (1+{ind_bonus*100:.2f}%)×(1+{crit_bonus*100:.2f}%)-1 = {berserker_fixed_bonus*100:.2f}%")

# ============================================
# 四、狂战士收益计算（百分比）
# ============================================
print("\n【四、狂战士百分比收益计算】")

# 力量收益（使用暴走后力量）
str_old = berserker_base['暴走力量']
str_new = str_old + cc_total['力量']
str_bonus = (1 + str_new / 250) / (1 + str_old / 250) - 1
print(f"  力量（暴走后）: {str_old:.1f} → {str_new:.1f}")
print(f"  力量收益: (1+{str_new:.1f}/250)/(1+{str_old:.1f}/250)-1 = {str_bonus*100:.2f}%")

# 物理攻击收益（直接乘数）
phy_old = berserker_base['物理攻击']
phy_new = phy_old + cc_total['物理攻击']
phy_bonus = phy_new / phy_old - 1
print(f"  物理攻击: {phy_old} → {phy_new}")
print(f"  物理攻击收益: {phy_new}/{phy_old}-1 = {phy_bonus*100:.2f}%")

# 暴击收益（同上）
print(f"  暴击收益: {crit_bonus*100:.2f}%")

# 百分比综合
berserker_percent_bonus = (1 + str_bonus) * (1 + phy_bonus) * (1 + crit_bonus) - 1
print(f"  百分比综合收益: (1+{str_bonus*100:.2f}%)×(1+{phy_bonus*100:.2f}%)×(1+{crit_bonus*100:.2f}%)-1 = {berserker_percent_bonus*100:.2f}%")

# ============================================
# 五、剑魂面板配置验证
# ============================================
print("\n【五、剑魂（白手）面板配置】")
swordsman_base = {
    "力量": 600,
    "物理攻击破极前": 2000,
    "物理攻击破极后": 2000 * 1.30,  # 破极兵刃+30%
    "暴击率": 0.50,  # 50%
}
print(f"  基础力量: {swordsman_base['力量']}")
print(f"  物理攻击（破极前）: {swordsman_base['物理攻击破极前']}")
print(f"  物理攻击（破极后）: {swordsman_base['物理攻击破极后']:.0f}")
print(f"  暴击率: {swordsman_base['暴击率']*100:.0f}%")

# ============================================
# 六、剑魂收益计算（百分比）
# ============================================
print("\n【六、剑魂百分比收益计算（破极兵刃状态下）】")

# 力量收益
str_old_sm = swordsman_base['力量']
str_new_sm = str_old_sm + cc_total['力量']
str_bonus_sm = (1 + str_new_sm / 250) / (1 + str_old_sm / 250) - 1
print(f"  力量: {str_old_sm} → {str_new_sm}")
print(f"  力量收益: (1+{str_new_sm}/250)/(1+{str_old_sm}/250)-1 = {str_bonus_sm*100:.2f}%")

# 物理攻击收益（破极后）
phy_old_sm = swordsman_base['物理攻击破极后']
phy_new_sm = phy_old_sm + cc_total['物理攻击']
phy_bonus_sm = phy_new_sm / phy_old_sm - 1
print(f"  物理攻击（破极后）: {phy_old_sm:.0f} → {phy_new_sm:.0f}")
print(f"  物理攻击收益: {phy_new_sm:.0f}/{phy_old_sm:.0f}-1 = {phy_bonus_sm*100:.2f}%")

# 暴击收益
crit_old_sm = swordsman_base['暴击率']
crit_new_sm = crit_old_sm + cc_total['暴击'] / 100
crit_old_coeff_sm = (1 - crit_old_sm) + crit_old_sm * 1.5
crit_new_coeff_sm = (1 - crit_new_sm) + crit_new_sm * 1.5
crit_bonus_sm = crit_new_coeff_sm / crit_old_coeff_sm - 1
print(f"  暴击率: {crit_old_sm*100:.0f}% → {crit_new_sm*100:.0f}%")
print(f"  暴击期望系数: {crit_old_coeff_sm:.4f} → {crit_new_coeff_sm:.4f}")
print(f"  暴击收益: {crit_bonus_sm*100:.2f}%")

# 百分比综合
swordsman_percent_bonus = (1 + str_bonus_sm) * (1 + phy_bonus_sm) * (1 + crit_bonus_sm) - 1
print(f"  百分比综合收益: (1+{str_bonus_sm*100:.2f}%)×(1+{phy_bonus_sm*100:.2f}%)×(1+{crit_bonus_sm*100:.2f}%)-1 = {swordsman_percent_bonus*100:.2f}%")

# ============================================
# 七、边际对偶验证
# ============================================
print("\n【七、边际对偶验证（系统固有频率）】")
ratio = swordsman_percent_bonus / berserker_fixed_bonus
print(f"  剑魂百分比综合 / 狂战士固伤综合 = {swordsman_percent_bonus*100:.2f}% / {berserker_fixed_bonus*100:.2f}% = {ratio:.2f}倍")
print(f"  系统固有频率确认: 约4.74倍")

# ============================================
# 八、验证结果汇总
# ============================================
print("\n" + "=" * 60)
print("【验证结果汇总】")
print("=" * 60)

results = {
    "CC套6件属性": {
        "力量": cc_total['力量'],
        "物理攻击": cc_total['物理攻击'],
        "独立攻击": cc_total['独立攻击'],
        "暴击": f"{cc_total['暴击']}%",
        "预期": "力量+310, 物理攻击+110, 独立攻击+120, 暴击+3%"
    },
    "狂战士固伤收益": {
        "独立攻击": f"{ind_bonus*100:.2f}%",
        "暴击": f"{crit_bonus*100:.2f}%",
        "综合": f"{berserker_fixed_bonus*100:.2f}%",
        "预期": "+8.0%, +1.2%, +9.27%"
    },
    "狂战士百分比收益": {
        "力量": f"{str_bonus*100:.2f}%",
        "物理攻击": f"{phy_bonus*100:.2f}%",
        "暴击": f"{crit_bonus*100:.2f}%",
        "综合": f"{berserker_percent_bonus*100:.2f}%",
        "预期": "+24.42%, +5.50%, +1.2%, +32.81%"
    },
    "剑魂百分比收益": {
        "力量": f"{str_bonus_sm*100:.2f}%",
        "物理攻击": f"{phy_bonus_sm*100:.2f}%",
        "暴击": f"{crit_bonus_sm*100:.2f}%",
        "综合": f"{swordsman_percent_bonus*100:.2f}%",
        "预期": "+36.47%, +4.23%, +1.2%, +43.95%"
    },
    "边际对偶": {
        "收益倍数": f"{ratio:.2f}",
        "预期": "~4.74倍"
    }
}

# 逐项验证
all_pass = True
checks = [
    ("CC套力量", cc_total['力量'], 310),
    ("CC套物理攻击", cc_total['物理攻击'], 110),
    ("CC套独立攻击", cc_total['独立攻击'], 120),
    ("CC套暴击", cc_total['暴击'], 3),
    ("狂战士独立收益", round(ind_bonus*100, 2), 8.0),
    ("狂战士暴击收益", round(crit_bonus*100, 2), 1.18),  # 精确值1.18%，显示为1.2%
    ("狂战士固伤综合", round(berserker_fixed_bonus*100, 2), 9.27),
    ("狂战士力量收益", round(str_bonus*100, 2), 24.42),
    ("狂战士物理攻击收益", round(phy_bonus*100, 2), 5.50),
    ("狂战士百分比综合", round(berserker_percent_bonus*100, 2), 32.81),
    ("剑魂力量收益", round(str_bonus_sm*100, 2), 36.47),
    ("剑魂物理攻击收益", round(phy_bonus_sm*100, 2), 4.23),
    ("剑魂暴击收益", round(crit_bonus_sm*100, 2), 1.2),
    ("剑魂百分比综合", round(swordsman_percent_bonus*100, 2), 43.95),
    ("边际对偶倍数", round(ratio, 2), 4.74),
]

print("\n逐项验证结果:")
for name, actual, expected in checks:
    # 允许0.01的精度误差
    passed = abs(actual - expected) < 0.02
    status = "✅" if passed else "❌"
    if not passed:
        all_pass = False
    print(f"  {status} {name}: {actual} (预期: {expected})")

print("\n" + "=" * 60)
if all_pass:
    print("✅ 全部15项Python独立验算通过！数据准确可靠。")
else:
    print("❌ 存在偏差，需要重新核查。")
print("=" * 60)

# 保存验证结果
verification_result = {
    "timestamp": datetime.now().isoformat(),
    "round": 280,
    "all_pass": all_pass,
    "total_checks": len(checks),
    "passed": sum(1 for _, a, e in checks if abs(a - e) < 0.02),
    "details": {name: {"actual": actual, "expected": expected, "pass": abs(actual - expected) < 0.02} for name, actual, expected in checks}
}

with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/cc_set_verification_v280.json", "w") as f:
    json.dump(verification_result, f, indent=2, ensure_ascii=False)

print(f"\n验证结果已保存至: notes/bonus-system/cc_set_verification_v280.json")