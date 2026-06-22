#!/usr/bin/env python3
"""
DNF 70版本 CC套（宫廷套装）加成数值 Python独立验算
稳态核查 v269 - 2026-06-23
"""

import json
from datetime import datetime

# ============================================
# 基础数据（来自HTML报告）
# ============================================

# CC套6件套属性
CC_POWER = 310
CC_PHY_ATK = 110
CC_INDEPENDENT = 120
CC_CRIT = 0.03  # 3%

# 狂战士面板（毕业级）
BERSERKER_BASE_POWER = 728
BERSERKER_BURST_POWER = 728 * 1.40  # 暴走+40% = 1019.2
BERSERKER_INDEPENDENT = 1250
BERSERKER_PHY_ATK = 2000
BERSERKER_CRIT = 0.55  # 55%

# 剑魂面板（毕业级，破极兵刃状态）
SWORDSMAN_POWER = 600
SWORDSMAN_PHY_ATK_BASE = 2000
SWORDSMAN_PHY_ATK_BROKEN = 2000 * 1.30  # 破极兵刃+30% = 2600
SWORDSMAN_CRIT = 0.50  # 50%

# DNF 70公式常数
CRIT_DMG_MULTIPLIER = 1.5  # 暴击伤害倍率

# ============================================
# 验算函数
# ============================================

def calc_independent_benefit(independent_old, independent_add):
    """固伤独立攻击收益"""
    old_factor = 1 + independent_old / 250
    new_factor = 1 + (independent_old + independent_add) / 250
    return new_factor / old_factor - 1

def calc_power_benefit(power_old, power_add):
    """百分比力量收益"""
    old_factor = 1 + power_old / 250
    new_factor = 1 + (power_old + power_add) / 250
    return new_factor / old_factor - 1

def calc_phy_atk_benefit(phy_old, phy_add):
    """百分比物理攻击收益（直接乘数）"""
    return (phy_old + phy_add) / phy_old - 1

def calc_crit_benefit(crit_old, crit_add):
    """暴击期望收益"""
    old_expect = (1 - crit_old) + crit_old * CRIT_DMG_MULTIPLIER
    new_expect = (1 - (crit_old + crit_add)) + (crit_old + crit_add) * CRIT_DMG_MULTIPLIER
    return new_expect / old_expect - 1

# ============================================
# 验算测试
# ============================================

tests = []

# === 狂战士固伤流 ===
test_id = 1
name = "狂战士固伤-独立攻击收益"
result = calc_independent_benefit(BERSERKER_INDEPENDENT, CC_INDEPENDENT)
expected = 0.08  # +8.0%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": expected * 100,
    "pass": abs(result - expected) < 0.001
})
test_id += 1

test_id = 2
name = "狂战士固伤-暴击收益"
result = calc_crit_benefit(BERSERKER_CRIT, CC_CRIT)
expected = 0.0118  # +1.18% ≈ +1.2%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": round(expected * 100, 2),
    "pass": abs(result - expected) < 0.001
})
test_id += 1

test_id = 3
name = "狂战士固伤综合收益"
ind_benefit = calc_independent_benefit(BERSERKER_INDEPENDENT, CC_INDEPENDENT)
crit_benefit = calc_crit_benefit(BERSERKER_CRIT, CC_CRIT)
result = (1 + ind_benefit) * (1 + crit_benefit) - 1
expected = 0.0927  # +9.27%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": expected * 100,
    "pass": abs(result - expected) < 0.001
})
test_id += 1

# === 狂战士百分比流 ===
test_id = 4
name = "狂战士百分比-力量收益（暴走后）"
result = calc_power_benefit(BERSERKER_BURST_POWER, CC_POWER)
expected = 0.2442  # +24.42%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": expected * 100,
    "pass": abs(result - expected) < 0.001
})
test_id += 1

test_id = 5
name = "狂战士百分比-物理攻击收益"
result = calc_phy_atk_benefit(BERSERKER_PHY_ATK, CC_PHY_ATK)
expected = 0.055  # +5.50%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": expected * 100,
    "pass": abs(result - expected) < 0.001
})
test_id += 1

test_id = 6
name = "狂战士百分比-暴击收益"
result = calc_crit_benefit(BERSERKER_CRIT, CC_CRIT)
expected = 0.0118  # +1.18%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": round(expected * 100, 2),
    "pass": abs(result - expected) < 0.001
})
test_id += 1

test_id = 7
name = "狂战士百分比综合收益"
power_b = calc_power_benefit(BERSERKER_BURST_POWER, CC_POWER)
phy_b = calc_phy_atk_benefit(BERSERKER_PHY_ATK, CC_PHY_ATK)
crit_b = calc_crit_benefit(BERSERKER_CRIT, CC_CRIT)
result = (1 + power_b) * (1 + phy_b) * (1 + crit_b) - 1
expected = 0.3281  # +32.81%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": expected * 100,
    "pass": abs(result - expected) < 0.001
})
test_id += 1

# === 剑魂百分比流 ===
test_id = 8
name = "剑魂百分比-力量收益"
result = calc_power_benefit(SWORDSMAN_POWER, CC_POWER)
expected = 0.3647  # +36.47%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": expected * 100,
    "pass": abs(result - expected) < 0.001
})
test_id += 1

test_id = 9
name = "剑魂百分比-物理攻击收益（破极后）"
result = calc_phy_atk_benefit(SWORDSMAN_PHY_ATK_BROKEN, CC_PHY_ATK)
expected = 0.0423  # +4.23%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": expected * 100,
    "pass": abs(result - expected) < 0.001
})
test_id += 1

test_id = 10
name = "剑魂百分比-暴击收益"
result = calc_crit_benefit(SWORDSMAN_CRIT, CC_CRIT)
expected = 0.012  # +1.2%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": expected * 100,
    "pass": abs(result - expected) < 0.001
})
test_id += 1

test_id = 11
name = "剑魂百分比综合收益"
power_b = calc_power_benefit(SWORDSMAN_POWER, CC_POWER)
phy_b = calc_phy_atk_benefit(SWORDSMAN_PHY_ATK_BROKEN, CC_PHY_ATK)
crit_b = calc_crit_benefit(SWORDSMAN_CRIT, CC_CRIT)
result = (1 + power_b) * (1 + phy_b) * (1 + crit_b) - 1
expected = 0.4395  # +43.95%
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result * 100, 2),
    "expected": expected * 100,
    "pass": abs(result - expected) < 0.001
})
test_id += 1

# === 边际对偶验证 ===
test_id = 12
name = "系统固有频率：剑魂百分比/狂战士固伤"
berserker_gu = (1 + calc_independent_benefit(BERSERKER_INDEPENDENT, CC_INDEPENDENT)) * (1 + calc_crit_benefit(BERSERKER_CRIT, CC_CRIT)) - 1
swordsman_percent = (1 + calc_power_benefit(SWORDSMAN_POWER, CC_POWER)) * (1 + calc_phy_atk_benefit(SWORDSMAN_PHY_ATK_BROKEN, CC_PHY_ATK)) * (1 + calc_crit_benefit(SWORDSMAN_CRIT, CC_CRIT)) - 1
result = swordsman_percent / berserker_gu
expected = 4.74
tests.append({
    "id": test_id,
    "name": name,
    "result": round(result, 2),
    "expected": expected,
    "pass": abs(result - expected) < 0.1
})
test_id += 1

# === CC套基础属性验证 ===
test_id = 13
name = "CC套6件力量合计验证"
cc_power_total = 55 + 55 + 50 + 50 + 50 + 50  # 上衣+下装+头+帽+脸+胸
tests.append({
    "id": test_id,
    "name": name,
    "result": cc_power_total,
    "expected": 310,
    "pass": cc_power_total == 310
})
test_id += 1

test_id = 14
name = "CC套6件物理攻击合计验证"
cc_phy_total = 20 + 20 + 18 + 18 + 18 + 16
tests.append({
    "id": test_id,
    "name": name,
    "result": cc_phy_total,
    "expected": 110,
    "pass": cc_phy_total == 110
})
test_id += 1

test_id = 15
name = "CC套6件独立攻击合计验证"
cc_ind_total = 20 + 20 + 18 + 18 + 18 + 26
tests.append({
    "id": test_id,
    "name": name,
    "result": cc_ind_total,
    "expected": 120,
    "pass": cc_ind_total == 120
})
test_id += 1

# ============================================
# 输出结果
# ============================================

passed = sum(1 for t in tests if t["pass"])
total = len(tests)
pass_rate = passed / total * 100

print("=" * 60)
print("DNF 70版本 CC套加成数值 Python独立验算报告")
print(f"稳态核查 v269 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)
print()

for t in tests:
    status = "✅" if t["pass"] else "❌"
    print(f"{status} 测试{t['id']:2d}: {t['name']}")
    print(f"      结果: {t['result']} | 期望: {t['expected']}")
    if not t["pass"]:
        print(f"      ⚠️ 偏差: {abs(t['result'] - t['expected']):.4f}")
    print()

print("=" * 60)
print(f"验算结果: {passed}/{total} 通过 ({pass_rate:.1f}%)")
print("=" * 60)

if pass_rate == 100:
    print("✅ 稳态核查通过，数据准确可靠")
else:
    print("❌ 存在偏差，需核查修正")

# 输出JSON供后续处理
result_json = {
    "version": "v269",
    "timestamp": datetime.now().isoformat(),
    "passed": passed,
    "total": total,
    "pass_rate": pass_rate,
    "tests": tests
}
print("\n---JSON---")
print(json.dumps(result_json, ensure_ascii=False, indent=2))