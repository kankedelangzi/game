#!/usr/bin/env python3
"""CC套稳态核查 v527 — 2026-06-26 17:51"""
import json, math, datetime

results = []
all_pass = True

def check(name, expected, actual, tol=0.001):
    global all_pass
    passed = abs(expected - actual) < tol
    if not passed:
        all_pass = False
    results.append({"name": name, "expected": expected, "actual": round(actual, 6), "passed": passed, "diff": round(abs(expected - actual), 6)})
    status = "✅" if passed else "❌"
    print(f"  {status} {name}: expected={expected}, actual={actual:.6f}, diff={abs(expected-actual):.6f}")

# === 1. CC套6件套属性合计 ===
print("=== 1. CC套6件套属性合计 ===")
strength_sum = 55 + 55 + 50 + 50 + 50 + 50
phys_atk_sum = 20 + 20 + 18 + 18 + 18 + 16
indep_atk_sum = 20 + 20 + 18 + 18 + 18 + 26
crit_sum = 0.5 * 6
check("力量合计", 310, strength_sum)
check("物理攻击合计", 110, phys_atk_sum)
check("独立攻击合计", 120, indep_atk_sum)
check("暴击率合计", 3.0, crit_sum)

# === 2. 狂战士固伤收益 ===
print("\n=== 2. 狂战士固伤收益 ===")
indep_bonus = 120 / 250
check("狂战士独立攻击收益", 0.48, indep_bonus)
crit_expect = 1 + 0.03 * 1.5
check("狂战士暴击期望系数", 1.045, crit_expect)
# 固伤综合 = (1+独立/250) × 暴击期望 - 1
fixed_combined = (1 + 120/250) * (1 + 0.03*1.5) - 1
check("狂战士固伤综合", 0.5466, fixed_combined)

# === 3. 狂战士百分比收益 ===
print("\n=== 3. 狂战士百分比收益 ===")
str_bonus = 310 / 2500
check("狂战士力量收益", 0.124, str_bonus)
phy_bonus = 110 / 2500
check("狂战士物理攻击收益", 0.044, phy_bonus)
# 百分比综合 = (1+力量/2500) × (1+物理攻击/2500) × 暴击期望 - 1
pct_combined = (1 + 310/2500) * (1 + 110/2500) * (1 + 0.03*1.5) - 1
check("狂战士百分比综合", 0.22626, pct_combined)

# === 4. 剑魂百分比收益 ===
print("\n=== 4. 剑魂百分比收益 ===")
sw_str_bonus = 310 / 2500
check("剑魂力量收益", 0.124, sw_str_bonus)
sw_phy_bonus = 110 / 2500
check("剑魂物理攻击收益", 0.044, sw_phy_bonus)
sw_crit_expect = 1 + 0.03 * 1.5
check("剑魂暴击期望系数", 1.045, sw_crit_expect)
sw_pct_combined = (1 + 310/2500) * (1 + 110/2500) * (1 + 0.03*1.5) - 1
check("剑魂百分比综合", 0.22626, sw_pct_combined)

# === 5. 边际对偶 ===
print("\n=== 5. 边际对偶 ===")
# 边际对偶 = 固伤综合 / 百分比综合（近似）
# 但实际边际对偶是系统固有频率
marginal = fixed_combined / pct_combined
check("边际对偶", 4.740937, marginal)

# === 汇总 ===
print(f"\n=== 汇总 ===")
print(f"总验算项: {len(results)}")
print(f"通过: {sum(1 for r in results if r['passed'])}")
print(f"失败: {sum(1 for r in results if not r['passed'])}")
print(f"通过率: {sum(1 for r in results if r['passed'])}/{len(results)} = {sum(1 for r in results if r['passed'])/len(results)*100:.1f}%")

# 保存JSON
output = {
    "version": "v527",
    "timestamp": datetime.datetime.now().isoformat(),
    "total": len(results),
    "passed": sum(1 for r in results if r['passed']),
    "failed": sum(1 for r in results if not r['passed']),
    "pass_rate": f"{sum(1 for r in results if r['passed'])}/{len(results)}",
    "all_pass": all_pass,
    "results": results,
    "core_data": {
        "cc_6pc": {"strength": 310, "phys_atk": 110, "indep_atk": 120, "crit": 3.0},
        "berserker": {"fixed_combined": round(fixed_combined, 4), "pct_combined": round(pct_combined, 4)},
        "swordsman": {"pct_combined": round(sw_pct_combined, 4)},
        "marginal": round(marginal, 6)
    }
}
with open("notes/bonus-system/verifications/verification-cc-bonus-v527-2026-06-26.json", "w") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(f"\n✅ 验算JSON已保存: notes/bonus-system/verifications/verification-cc-bonus-v527-2026-06-26.json")