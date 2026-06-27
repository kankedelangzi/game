#!/usr/bin/env python3
"""
CC套（宫廷套装）加成数值稳态核查 v609
验证时间: 2026-06-27 12:26
"""
import json, math

results = []
all_pass = True

def check(name, expected, actual, tol=0.01):
    global all_pass
    diff = abs(expected - actual)
    passed = diff <= tol
    if not passed:
        all_pass = False
    results.append({
        "name": name,
        "expected": round(expected, 4),
        "actual": round(actual, 4),
        "diff": round(diff, 4),
        "passed": passed
    })
    return passed

# ============================================================
# 1. CC套6件套属性合计验证
# ============================================================
cc_str = 55 + 55 + 50 + 50 + 50 + 50  # 上衣+下装+头饰+帽子+脸部+胸部
cc_phy = 20 + 20 + 18 + 18 + 18 + 16
cc_ind = 20 + 20 + 18 + 18 + 18 + 26
cc_crit = 0.5 * 6

check("CC套力量合计", 310, cc_str)
check("CC套物理攻击合计", 110, cc_phy)
check("CC套独立攻击合计", 120, cc_ind)
check("CC套暴击率合计", 3.0, cc_crit)

# ============================================================
# 2. 狂战士固伤收益
# ============================================================
bers_str = 728
bers_str_burst = bers_str * 1.40  # 暴走+40%
bers_ind = 1250
bers_phy = 2000
bers_crit = 0.55

# 独立攻击收益
bers_ind_gain = (1 + (bers_ind + 120) / 250) / (1 + bers_ind / 250) - 1
check("狂战士独立攻击收益", 0.0800, bers_ind_gain, tol=0.001)

# 暴击收益（期望伤害系数）
bers_crit_new = bers_crit + 0.03
bers_crit_exp_old = (1 - bers_crit) + bers_crit * 1.5
bers_crit_exp_new = (1 - bers_crit_new) + bers_crit_new * 1.5
bers_crit_gain = bers_crit_exp_new / bers_crit_exp_old - 1
check("狂战士暴击收益", 0.0118, bers_crit_gain, tol=0.001)

# 固伤综合收益
bers_fixed_total = (1 + bers_ind_gain) * (1 + bers_crit_gain) - 1
check("狂战士固伤综合收益", 0.0927, bers_fixed_total, tol=0.001)

# ============================================================
# 3. 狂战士百分比收益
# ============================================================
# 力量收益（暴走后）
bers_str_gain = (1 + (bers_str_burst + 310) / 250) / (1 + bers_str_burst / 250) - 1
check("狂战士力量收益", 0.2442, bers_str_gain, tol=0.001)

# 物理攻击收益
bers_phy_gain = (bers_phy + 110) / bers_phy - 1
check("狂战士物理攻击收益", 0.0550, bers_phy_gain, tol=0.001)

# 百分比综合收益
bers_pct_total = (1 + bers_str_gain) * (1 + bers_phy_gain) * (1 + bers_crit_gain) - 1
check("狂战士百分比综合收益", 0.3281, bers_pct_total, tol=0.001)

# ============================================================
# 4. 剑魂百分比收益
# ============================================================
sw_str = 600
sw_phy = 2000
sw_phy_broken = sw_phy * 1.30  # 破极兵刃+30%
sw_crit = 0.50

# 力量收益
sw_str_gain = (1 + (sw_str + 310) / 250) / (1 + sw_str / 250) - 1
check("剑魂力量收益", 0.3647, sw_str_gain, tol=0.001)

# 物理攻击收益（破极后）
sw_phy_gain = (sw_phy_broken + 110) / sw_phy_broken - 1
check("剑魂物理攻击收益", 0.0423, sw_phy_gain, tol=0.001)

# 暴击收益
sw_crit_new = sw_crit + 0.03
sw_crit_exp_old = (1 - sw_crit) + sw_crit * 1.5
sw_crit_exp_new = (1 - sw_crit_new) + sw_crit_new * 1.5
sw_crit_gain = sw_crit_exp_new / sw_crit_exp_old - 1
check("剑魂暴击收益", 0.0120, sw_crit_gain, tol=0.001)

# 百分比综合收益
sw_pct_total = (1 + sw_str_gain) * (1 + sw_phy_gain) * (1 + sw_crit_gain) - 1
check("剑魂百分比综合收益", 0.4395, sw_pct_total, tol=0.001)

# ============================================================
# 5. 边际对偶验证
# ============================================================
marginal_duality = sw_pct_total / bers_fixed_total
check("边际对偶倍数", 4.740937, marginal_duality, tol=0.001)

# ============================================================
# 输出结果
# ============================================================
passed = sum(1 for r in results if r["passed"])
total = len(results)

output = {
    "version": "v609",
    "timestamp": "2026-06-27T12:26:00+08:00",
    "task": "任务19 - CC套（宫廷套装）各职业加成数值",
    "total_checks": total,
    "passed": passed,
    "failed": total - passed,
    "pass_rate": f"{passed}/{total} ({100*passed/total:.1f}%)",
    "all_pass": all_pass,
    "core_data": {
        "cc_set_6pc": {"str": 310, "phy": 110, "ind": 120, "crit": "3.0%"},
        "berserker_fixed": f"+{bers_fixed_total*100:.2f}%",
        "berserker_percent": f"+{bers_pct_total*100:.2f}%",
        "swordsman_percent": f"+{sw_pct_total*100:.2f}%",
        "marginal_duality": round(marginal_duality, 6)
    },
    "details": results
}

print(json.dumps(output, ensure_ascii=False, indent=2))

with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verifications/verification-cc-bonus-v609.json", "w") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n✅ 验证完成: {passed}/{total} 通过")
print(f"边际对偶: {marginal_duality:.6f}")
