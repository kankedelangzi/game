#!/usr/bin/env python3
"""
CC套（宫廷套装）各职业加成数值 - Python独立验算
任务19 稳态核查
"""

import json
from datetime import datetime

results = []
passed = 0

def verify(name, expected, actual, tolerance=0.01):
    global passed
    diff = abs(expected - actual)
    status = "✅ PASS" if diff <= tolerance else "❌ FAIL"
    if diff <= tolerance:
        passed += 1
    results.append({
        "name": name,
        "expected": expected,
        "actual": actual,
        "diff": round(diff, 4),
        "status": status
    })
    return status

# ===== CC套6件套基础属性 =====
cc_power = 310
cc_phy_atk = 110
cc_ind_atk = 120
cc_crit = 0.03

verify("CC套力量+310", 310, cc_power)
verify("CC套物理攻击+110", 110, cc_phy_atk)
verify("CC套独立攻击+120", 120, cc_ind_atk)
verify("CC套暴击率+3%", 0.03, cc_crit)

# ===== 狂战士面板 =====
berserker_power_base = 728
berserker_power_burst = berserker_power_base * 1.40  # 暴走+40%
berserker_ind_atk = 1250
berserker_phy_atk = 2000
berserker_crit = 0.55

verify("狂战士暴走后力量", 1019.2, berserker_power_burst)

# ===== 狂战士固伤收益 =====
# 独立攻击收益
berserker_ind_before = 1 + berserker_ind_atk / 250
berserker_ind_after = 1 + (berserker_ind_atk + cc_ind_atk) / 250
berserker_ind_benefit = berserker_ind_after / berserker_ind_before - 1
verify("狂战士独立攻击收益", 0.08, berserker_ind_benefit)

# 暴击收益（期望伤害系数）
berserker_crit_before = (1 - berserker_crit) + berserker_crit * 1.5
berserker_crit_after = (1 - (berserker_crit + cc_crit)) + (berserker_crit + cc_crit) * 1.5
berserker_crit_benefit = berserker_crit_after / berserker_crit_before - 1
verify("狂战士暴击收益", 0.0118, berserker_crit_benefit, tolerance=0.001)

# 固伤综合收益
berserker固伤综合 = (1 + berserker_ind_benefit) * (1 + berserker_crit_benefit) - 1
verify("狂战士固伤综合收益", 0.0927, berserker固伤综合, tolerance=0.001)

# ===== 狂战士百分比收益 =====
# 力量收益（暴走后）
berserker_power_before = 1 + berserker_power_burst / 250
berserker_power_after = 1 + (berserker_power_burst + cc_power) / 250
berserker_power_benefit = berserker_power_after / berserker_power_before - 1
verify("狂战士力量收益（暴走后）", 0.2442, berserker_power_benefit, tolerance=0.001)

# 物理攻击收益
berserker_phy_before = berserker_phy_atk
berserker_phy_after = berserker_phy_atk + cc_phy_atk
berserker_phy_benefit = berserker_phy_after / berserker_phy_before - 1
verify("狂战士物理攻击收益", 0.055, berserker_phy_benefit)

# 百分比综合收益
berserker百分比综合 = (1 + berserker_power_benefit) * (1 + berserker_phy_benefit) * (1 + berserker_crit_benefit) - 1
verify("狂战士百分比综合收益", 0.3281, berserker百分比综合, tolerance=0.001)

# ===== 剑魂面板 =====
swordsman_power = 600
swordsman_phy_atk_base = 2000
swordsman_phy_atk_pojue = swordsman_phy_atk_base * 1.30  # 破极兵刃+30%
swordsman_crit = 0.50

verify("剑魂破极后物理攻击", 2600, swordsman_phy_atk_pojue)

# ===== 剑魂百分比收益 =====
# 力量收益
swordsman_power_before = 1 + swordsman_power / 250
swordsman_power_after = 1 + (swordsman_power + cc_power) / 250
swordsman_power_benefit = swordsman_power_after / swordsman_power_before - 1
verify("剑魂力量收益", 0.3647, swordsman_power_benefit, tolerance=0.001)

# 物理攻击收益（破极后）
swordsman_phy_before = swordsman_phy_atk_pojue
swordsman_phy_after = swordsman_phy_atk_pojue + cc_phy_atk
swordsman_phy_benefit = swordsman_phy_after / swordsman_phy_before - 1
verify("剑魂物理攻击收益（破极后）", 0.0423, swordsman_phy_benefit, tolerance=0.001)

# 暴击收益
swordsman_crit_before = (1 - swordsman_crit) + swordsman_crit * 1.5
swordsman_crit_after = (1 - (swordsman_crit + cc_crit)) + (swordsman_crit + cc_crit) * 1.5
swordsman_crit_benefit = swordsman_crit_after / swordsman_crit_before - 1
verify("剑魂暴击收益", 0.012, swordsman_crit_benefit, tolerance=0.001)

# 百分比综合收益
swordsman百分比综合 = (1 + swordsman_power_benefit) * (1 + swordsman_phy_benefit) * (1 + swordsman_crit_benefit) - 1
verify("剑魂百分比综合收益", 0.4395, swordsman百分比综合, tolerance=0.001)

# ===== 边际对偶验证 =====
marginal_dual = swordsman百分比综合 / berserker固伤综合
verify("边际对偶倍数", 4.7409, marginal_dual, tolerance=0.001)

# ===== 输出结果 =====
total = len(results)
print(f"CC套稳态核查结果：{passed}/{total} Python独立验算通过")
print(f"通过率：{passed/total*100:.1f}%")
print()

for r in results:
    print(f"{r['status']} | {r['name']}: 期望={r['expected']:.4f}, 实际={r['actual']:.4f}, 差异={r['diff']:.4f}")

# 保存JSON
output = {
    "timestamp": datetime.now().isoformat(),
    "total": total,
    "passed": passed,
    "rate": f"{passed/total*100:.1f}%",
    "results": results
}
with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verifications/verification-cc-bonus-2026-06-24-latest.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nJSON已保存")
