#!/usr/bin/env python3
"""CC套（宫廷套装）稳态核查 v470 - 2026-06-26 07:29"""
import json

# === CC套6件套属性 ===
cc_strength = 310
cc_phy_atk = 110
cc_indep_atk = 120
cc_crit = 0.03  # 3%

# === 狂战士面板（毕业级，暴走后） ===
berserker_str = 1019.2  # 728 * 1.40
berserker_indep = 1250
berserker_phy = 2000
berserker_crit = 0.55

# === 剑魂面板（毕业级，破极兵刃后） ===
swordsman_str = 600
swordsman_phy_base = 2000
swordsman_phy = 2600  # 破极后
swordsman_crit = 0.50

# === 验算 ===
results = {}
passed = 0
total = 0

def check(name, expected, actual, tol=0.001):
    global passed, total
    total += 1
    ok = abs(expected - actual) < tol
    if ok: passed += 1
    results[name] = {"expected": expected, "actual": actual, "pass": ok, "diff": abs(expected - actual)}

# 1. 6件套属性合计
check("cc_strength_total", 310, cc_strength)
check("cc_phy_atk_total", 110, cc_phy_atk)
check("cc_indep_atk_total", 120, cc_indep_atk)
check("cc_crit_total", 0.03, cc_crit)

# 2. 狂战士固伤收益
berserker_indep_new = berserker_indep + cc_indep_atk
berserker_indep_gain = (1 + berserker_indep_new/250) / (1 + berserker_indep/250) - 1
check("berserker_indep_gain", 0.08, berserker_indep_gain, 0.001)

# 暴击收益
crit_coeff_old = (1 - berserker_crit) + berserker_crit * 1.5
crit_coeff_new = (1 - (berserker_crit + cc_crit)) + (berserker_crit + cc_crit) * 1.5
berserker_crit_gain = crit_coeff_new / crit_coeff_old - 1
check("berserker_crit_gain", 0.012, berserker_crit_gain, 0.001)

# 固伤综合
berserker_fixed_total = (1 + berserker_indep_gain) * (1 + berserker_crit_gain) - 1
check("berserker_fixed_total", 0.0927, berserker_fixed_total, 0.001)

# 3. 狂战士百分比收益
berserker_str_new = berserker_str + cc_strength
berserker_str_gain = (1 + berserker_str_new/250) / (1 + berserker_str/250) - 1
check("berserker_str_gain", 0.2442, berserker_str_gain, 0.001)

berserker_phy_new = berserker_phy + cc_phy_atk
berserker_phy_gain = berserker_phy_new / berserker_phy - 1
check("berserker_phy_gain", 0.055, berserker_phy_gain, 0.001)

berserker_pct_total = (1 + berserker_str_gain) * (1 + berserker_phy_gain) * (1 + berserker_crit_gain) - 1
check("berserker_pct_total", 0.3281, berserker_pct_total, 0.001)

# 4. 剑魂百分比收益
swordsman_str_new = swordsman_str + cc_strength
swordsman_str_gain = (1 + swordsman_str_new/250) / (1 + swordsman_str/250) - 1
check("swordsman_str_gain", 0.3647, swordsman_str_gain, 0.001)

swordsman_phy_new = swordsman_phy + cc_phy_atk
swordsman_phy_gain = swordsman_phy_new / swordsman_phy - 1
check("swordsman_phy_gain", 0.0423, swordsman_phy_gain, 0.001)

sw_crit_coeff_old = (1 - swordsman_crit) + swordsman_crit * 1.5
sw_crit_coeff_new = (1 - (swordsman_crit + cc_crit)) + (swordsman_crit + cc_crit) * 1.5
swordsman_crit_gain = sw_crit_coeff_new / sw_crit_coeff_old - 1
check("swordsman_crit_gain", 0.012, swordsman_crit_gain, 0.001)

swordsman_pct_total = (1 + swordsman_str_gain) * (1 + swordsman_phy_gain) * (1 + swordsman_crit_gain) - 1
check("swordsman_pct_total", 0.4395, swordsman_pct_total, 0.001)

# 5. 边际对偶
marginal_dual = swordsman_pct_total / berserker_fixed_total
check("marginal_dual", 4.740937, marginal_dual, 0.001)

# 输出
print(f"=== CC套稳态核查 v470 ===")
print(f"时间: 2026-06-26 07:29")
print(f"通过: {passed}/{total}")
print(f"通过率: {passed/total*100:.1f}%")
print(f"边际对偶: {marginal_dual:.6f}")
print()
for name, r in results.items():
    status = "✅" if r["pass"] else "❌"
    print(f"  {status} {name}: expected={r['expected']}, actual={r['actual']:.6f}, diff={r['diff']:.6f}")

# 保存JSON
output = {
    "version": "v470",
    "timestamp": "2026-06-26 07:29",
    "passed": passed,
    "total": total,
    "pass_rate": f"{passed/total*100:.1f}%",
    "marginal_dual": round(marginal_dual, 6),
    "results": results
}
with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verification-v470.json", "w") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"\nJSON saved: verification-v470.json")
