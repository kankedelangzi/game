#!/usr/bin/env python3
"""
任务19 CC套稳态核查 - Python独立验算
验证CC套对狂战士和剑魂的收益计算
"""

import json
from datetime import datetime

# ==================== 基础数据 ====================
# CC套6件套属性
CC_POWER = 310
CC_PHY_ATK = 110
CC_INDEP_ATK = 120
CC_CRIT = 0.03

# 暴击伤害倍率
CRIT_DMG = 1.5

# ==================== 狂战士面板（暴走后） ====================
berserker = {
    'power_base': 728,
    'power_berserk': 728 * 1.40,  # 1019.2
    'indep_atk': 1250,
    'phy_atk': 2000,
    'crit_rate': 0.55
}

# ==================== 剑魂面板（破极兵刃后） ====================
swordsman = {
    'power_base': 600,
    'phy_atk_base': 2000,
    'phy_atk_polarized': 2000 * 1.30,  # 2600
    'crit_rate': 0.50
}

# ==================== 验算函数 ====================

def calc_crit_expectation(crit_rate):
    """计算暴击期望伤害系数"""
    return (1 - crit_rate) + crit_rate * CRIT_DMG

def calc_power_benefit(power_base, power_add):
    """计算力量收益比"""
    old_factor = 1 + power_base / 250
    new_factor = 1 + (power_base + power_add) / 250
    return new_factor / old_factor - 1

def calc_phy_atk_benefit(phy_base, phy_add):
    """计算物理攻击收益比（直接乘数）"""
    return (phy_base + phy_add) / phy_base - 1

def calc_indep_atk_benefit(indep_base, indep_add):
    """计算独立攻击收益比"""
    old_factor = 1 + indep_base / 250
    new_factor = 1 + (indep_base + indep_add) / 250
    return new_factor / old_factor - 1

# ==================== 狂战士验算 ====================
print("=" * 60)
print("狂战士 CC套收益验算")
print("=" * 60)

# 暴走后力量
berserk_power = berserker['power_berserk']
print(f"\n暴走后力量: {berserk_power:.1f}")

# 独立攻击收益
indep_benefit = calc_indep_atk_benefit(berserker['indep_atk'], CC_INDEP_ATK)
print(f"\n独立攻击收益:")
print(f"  基础独立: {berserker['indep_atk']}")
print(f"  CC套加成: +{CC_INDEP_ATK}")
print(f"  收益比: {indep_benefit*100:.2f}%")
print(f"  验算: (1 + {berserker['indep_atk'] + CC_INDEP_ATK}/250) / (1 + {berserker['indep_atk']}/250) - 1")
print(f"       = {1 + (berserker['indep_atk'] + CC_INDEP_ATK)/250:.4f} / {1 + berserker['indep_atk']/250:.4f} - 1")
print(f"       = {(1 + (berserker['indep_atk'] + CC_INDEP_ATK)/250) / (1 + berserker['indep_atk']/250):.4f} - 1")
print(f"       = {indep_benefit*100:.2f}%")

# 暴击收益
old_crit_exp = calc_crit_expectation(berserker['crit_rate'])
new_crit_exp = calc_crit_expectation(berserker['crit_rate'] + CC_CRIT)
crit_benefit = new_crit_exp / old_crit_exp - 1
print(f"\n暴击收益:")
print(f"  基础暴击率: {berserker['crit_rate']*100:.0f}%")
print(f"  CC套加成: +{CC_CRIT*100:.0f}%")
print(f"  新暴击率: {(berserker['crit_rate'] + CC_CRIT)*100:.0f}%")
print(f"  旧期望: {old_crit_exp:.4f}")
print(f"  新期望: {new_crit_exp:.4f}")
print(f"  收益比: {crit_benefit*100:.2f}%")

# 固伤综合收益
fixed_composite = (1 + indep_benefit) * (1 + crit_benefit) - 1
print(f"\n固伤综合收益: {fixed_composite*100:.2f}%")
print(f"  验算: (1 + {indep_benefit*100:.2f}%) × (1 + {crit_benefit*100:.2f}%) - 1")
print(f"       = {1 + indep_benefit:.4f} × {1 + crit_benefit:.4f} - 1")
print(f"       = {(1 + indep_benefit) * (1 + crit_benefit) - 1:.4f}")
print(f"       = {fixed_composite*100:.2f}%")

# 力量收益（百分比技能）
power_benefit_berserk = calc_power_benefit(berserk_power, CC_POWER)
print(f"\n力量收益（百分比技能）:")
print(f"  暴走后力量: {berserk_power:.1f}")
print(f"  CC套加成: +{CC_POWER}")
print(f"  收益比: {power_benefit_berserk*100:.2f}%")
print(f"  验算: (1 + {berserk_power + CC_POWER:.1f}/250) / (1 + {berserk_power:.1f}/250) - 1")
print(f"       = {1 + (berserk_power + CC_POWER)/250:.4f} / {1 + berserk_power/250:.4f} - 1")
print(f"       = {(1 + (berserk_power + CC_POWER)/250) / (1 + berserk_power/250):.4f} - 1")
print(f"       = {power_benefit_berserk*100:.2f}%")

# 物理攻击收益（百分比技能）
phy_benefit_berserk = calc_phy_atk_benefit(berserker['phy_atk'], CC_PHY_ATK)
print(f"\n物理攻击收益（百分比技能）:")
print(f"  基础物理攻击: {berserker['phy_atk']}")
print(f"  CC套加成: +{CC_PHY_ATK}")
print(f"  收益比: {phy_benefit_berserk*100:.2f}%")
print(f"  验算: {berserker['phy_atk'] + CC_PHY_ATK}/{berserker['phy_atk']} - 1")
print(f"       = {(berserker['phy_atk'] + CC_PHY_ATK)/berserker['phy_atk']:.4f} - 1")
print(f"       = {phy_benefit_berserk*100:.2f}%")

# 百分比综合收益
percent_composite_berserk = (1 + power_benefit_berserk) * (1 + phy_benefit_berserk) * (1 + crit_benefit) - 1
print(f"\n百分比综合收益: {percent_composite_berserk*100:.2f}%")
print(f"  验算: (1 + {power_benefit_berserk*100:.2f}%) × (1 + {phy_benefit_berserk*100:.2f}%) × (1 + {crit_benefit*100:.2f}%) - 1")
print(f"       = {1 + power_benefit_berserk:.4f} × {1 + phy_benefit_berserk:.4f} × {1 + crit_benefit:.4f} - 1")
print(f"       = {(1 + power_benefit_berserk) * (1 + phy_benefit_berserk) * (1 + crit_benefit) - 1:.4f}")
print(f"       = {percent_composite_berserk*100:.2f}%")

# ==================== 剑魂验算 ====================
print("\n" + "=" * 60)
print("剑魂 CC套收益验算")
print("=" * 60)

# 力量收益
power_benefit_swordsman = calc_power_benefit(swordsman['power_base'], CC_POWER)
print(f"\n力量收益:")
print(f"  基础力量: {swordsman['power_base']}")
print(f"  CC套加成: +{CC_POWER}")
print(f"  收益比: {power_benefit_swordsman*100:.2f}%")
print(f"  验算: (1 + {swordsman['power_base'] + CC_POWER}/250) / (1 + {swordsman['power_base']}/250) - 1")
print(f"       = {1 + (swordsman['power_base'] + CC_POWER)/250:.4f} / {1 + swordsman['power_base']/250:.4f} - 1")
print(f"       = {(1 + (swordsman['power_base'] + CC_POWER)/250) / (1 + swordsman['power_base']/250):.4f} - 1")
print(f"       = {power_benefit_swordsman*100:.2f}%")

# 物理攻击收益（破极后）
phy_benefit_swordsman = calc_phy_atk_benefit(swordsman['phy_atk_polarized'], CC_PHY_ATK)
print(f"\n物理攻击收益（破极兵刃后）:")
print(f"  破极后物理攻击: {swordsman['phy_atk_polarized']}")
print(f"  CC套加成: +{CC_PHY_ATK}")
print(f"  收益比: {phy_benefit_swordsman*100:.2f}%")
print(f"  验算: {swordsman['phy_atk_polarized'] + CC_PHY_ATK}/{swordsman['phy_atk_polarized']} - 1")
print(f"       = {(swordsman['phy_atk_polarized'] + CC_PHY_ATK)/swordsman['phy_atk_polarized']:.4f} - 1")
print(f"       = {phy_benefit_swordsman*100:.2f}%")

# 暴击收益
old_crit_exp_s = calc_crit_expectation(swordsman['crit_rate'])
new_crit_exp_s = calc_crit_expectation(swordsman['crit_rate'] + CC_CRIT)
crit_benefit_s = new_crit_exp_s / old_crit_exp_s - 1
print(f"\n暴击收益:")
print(f"  基础暴击率: {swordsman['crit_rate']*100:.0f}%")
print(f"  CC套加成: +{CC_CRIT*100:.0f}%")
print(f"  新暴击率: {(swordsman['crit_rate'] + CC_CRIT)*100:.0f}%")
print(f"  旧期望: {old_crit_exp_s:.4f}")
print(f"  新期望: {new_crit_exp_s:.4f}")
print(f"  收益比: {crit_benefit_s*100:.2f}%")

# 百分比综合收益
percent_composite_swordsman = (1 + power_benefit_swordsman) * (1 + phy_benefit_swordsman) * (1 + crit_benefit_s) - 1
print(f"\n百分比综合收益: {percent_composite_swordsman*100:.2f}%")
print(f"  验算: (1 + {power_benefit_swordsman*100:.2f}%) × (1 + {phy_benefit_swordsman*100:.2f}%) × (1 + {crit_benefit_s*100:.2f}%) - 1")
print(f"       = {1 + power_benefit_swordsman:.4f} × {1 + phy_benefit_swordsman:.4f} × {1 + crit_benefit_s:.4f} - 1")
print(f"       = {(1 + power_benefit_swordsman) * (1 + phy_benefit_swordsman) * (1 + crit_benefit_s) - 1:.4f}")
print(f"       = {percent_composite_swordsman*100:.2f}%")

# ==================== 边际对偶验证 ====================
print("\n" + "=" * 60)
print("边际对偶验证")
print("=" * 60)

# 剑魂/狂战士固伤收益比
ratio = percent_composite_swordsman / fixed_composite
print(f"\n剑魂百分比综合 / 狂战士固伤综合 = {percent_composite_swordsman*100:.2f}% / {fixed_composite*100:.2f}% = {ratio:.2f}倍")
print(f"预期: ~4.74倍（系统固有频率）")
print(f"实际: {ratio:.2f}倍")
if abs(ratio - 4.74) < 0.1:
    print("✅ 边际对偶验证通过")
else:
    print(f"⚠️ 边际对偶偏差: {abs(ratio - 4.74):.2f}")

# ==================== 汇总 ====================
print("\n" + "=" * 60)
print("验算汇总")
print("=" * 60)

results = {
    'timestamp': datetime.now().isoformat(),
    'berserker': {
        'fixed_skill_benefit': round(fixed_composite * 100, 2),
        'percent_skill_benefit': round(percent_composite_berserk * 100, 2),
        'indep_benefit': round(indep_benefit * 100, 2),
        'crit_benefit': round(crit_benefit * 100, 2),
        'power_benefit': round(power_benefit_berserk * 100, 2),
        'phy_benefit': round(phy_benefit_berserk * 100, 2)
    },
    'swordsman': {
        'percent_skill_benefit': round(percent_composite_swordsman * 100, 2),
        'power_benefit': round(power_benefit_swordsman * 100, 2),
        'phy_benefit': round(phy_benefit_swordsman * 100, 2),
        'crit_benefit': round(crit_benefit_s * 100, 2)
    },
    'ratio': round(ratio, 2),
    'expected_ratio': 4.74,
    'ratio_pass': abs(ratio - 4.74) < 0.1
}

print(f"\n{json.dumps(results, indent=2, ensure_ascii=False)}")

# ==================== 断言验证 ====================
print("\n" + "=" * 60)
print("断言验证")
print("=" * 60)

checks = [
    ("狂战士固伤综合 +9.27%", abs(fixed_composite * 100 - 9.27) < 0.05),
    ("狂战士百分比综合 +32.81%", abs(percent_composite_berserk * 100 - 32.81) < 0.05),
    ("剑魂百分比综合 +43.95%", abs(percent_composite_swordsman * 100 - 43.95) < 0.05),
    ("边际对偶 4.74倍", abs(ratio - 4.74) < 0.1),
    ("独立攻击收益 +8.0%", abs(indep_benefit * 100 - 8.0) < 0.05),
    ("暴击收益 +1.2%", abs(crit_benefit * 100 - 1.2) < 0.05),
]

passed = 0
for name, result in checks:
    status = "✅" if result else "❌"
    print(f"  {status} {name}")
    if result:
        passed += 1

print(f"\n总计: {passed}/{len(checks)} 通过")
if passed == len(checks):
    print("🎉 全部验算通过！")
else:
    print("⚠️ 存在验算失败项")
