#!/usr/bin/env python3
"""
任务19 CC套（宫廷套装）加成数值 - Python独立验算脚本
稳态核查 v561（2026-06-27 04:21）
"""
import json
from datetime import datetime

results = []
passed = 0
failed = 0

def verify(name, expected, actual, tolerance=0.01):
    global passed, failed
    diff = abs(expected - actual)
    ok = diff <= tolerance
    if ok:
        passed += 1
    else:
        failed += 1
    results.append({
        "item": name,
        "expected": round(expected, 4),
        "actual": round(actual, 4),
        "diff": round(diff, 4),
        "status": "✅ PASS" if ok else "❌ FAIL"
    })
    return ok

# ==========================================
# 1. CC套基础属性验证
# ==========================================
verify("CC套6件力量合计", 310, 55+55+50+50+50+50)
verify("CC套6件物理攻击合计", 110, 20+20+18+18+18+16)
verify("CC套6件独立攻击合计", 120, 20+20+18+18+18+26)
verify("CC套6件暴击率合计", 3.0, 0.5+0.5+0.5+0.5+0.5+0.5)

# ==========================================
# 2. 狂战士固伤收益验证
# ==========================================
berserker_indep_base = 1250
berserker_indep_cc = 1250 + 120
berserker_crit_base = 0.55
berserker_crit_cc = 0.55 + 0.03

indep_berserker_base = 1 + berserker_indep_base / 250
indep_berserker_cc = 1 + berserker_indep_cc / 250
indep_berserker_gain = indep_berserker_cc / indep_berserker_base - 1
verify("狂战士独立攻击收益", 0.08, indep_berserker_gain)

crit_exp_base = (1 - berserker_crit_base) + berserker_crit_base * 1.5
crit_exp_cc = (1 - berserker_crit_cc) + berserker_crit_cc * 1.5
crit_berserker_gain = crit_exp_cc / crit_exp_base - 1
verify("狂战士暴击期望收益", 0.0117647, crit_berserker_gain, tolerance=0.001)

berserker_indep_total = indep_berserker_gain + crit_berserker_gain + indep_berserker_gain * crit_berserker_gain
verify("狂战士固伤综合收益", 0.0927, berserker_indep_total, tolerance=0.001)

# ==========================================
# 3. 狂战士百分比收益验证
# ==========================================
berserker_str_base = 728 * 1.40
berserker_str_cc = berserker_str_base + 310
berserker_phy_base = 2000
berserker_phy_cc = 2000 + 110

str_berserker_base = 1 + berserker_str_base / 250
str_berserker_cc = 1 + berserker_str_cc / 250
str_berserker_gain = str_berserker_cc / str_berserker_base - 1
verify("狂战士力量收益(百分比)", 0.2442, str_berserker_gain, tolerance=0.001)

phy_berserker_gain = berserker_phy_cc / berserker_phy_base - 1
verify("狂战士物理攻击收益", 0.055, phy_berserker_gain)

berserker_pct_total = str_berserker_gain + phy_berserker_gain + crit_berserker_gain + \
    str_berserker_gain * phy_berserker_gain + str_berserker_gain * crit_berserker_gain + \
    phy_berserker_gain * crit_berserker_gain + str_berserker_gain * phy_berserker_gain * crit_berserker_gain
verify("狂战士百分比综合收益", 0.3281, berserker_pct_total, tolerance=0.001)

# ==========================================
# 4. 剑魂百分比收益验证
# ==========================================
swordsman_str_base = 600
swordsman_str_cc = 600 + 310
swordsman_phy_base = 2600
swordsman_phy_cc = 2600 + 110
swordsman_crit_base = 0.50
swordsman_crit_cc = 0.50 + 0.03

str_swordsman_base = 1 + swordsman_str_base / 250
str_swordsman_cc = 1 + swordsman_str_cc / 250
str_swordsman_gain = str_swordsman_cc / str_swordsman_base - 1
verify("剑魂力量收益", 0.3647, str_swordsman_gain, tolerance=0.001)

phy_swordsman_gain = swordsman_phy_cc / swordsman_phy_base - 1
verify("剑魂物理攻击收益", 0.0423, phy_swordsman_gain, tolerance=0.001)

crit_exp_s_base = (1 - swordsman_crit_base) + swordsman_crit_base * 1.5
crit_exp_s_cc = (1 - swordsman_crit_cc) + swordsman_crit_cc * 1.5
crit_swordsman_gain = crit_exp_s_cc / crit_exp_s_base - 1
verify("剑魂暴击期望收益", 0.012, crit_swordsman_gain, tolerance=0.001)

swordsman_pct_total = str_swordsman_gain + phy_swordsman_gain + crit_swordsman_gain + \
    str_swordsman_gain * phy_swordsman_gain + str_swordsman_gain * crit_swordsman_gain + \
    phy_swordsman_gain * crit_swordsman_gain + str_swordsman_gain * phy_swordsman_gain * crit_swordsman_gain
verify("剑魂百分比综合收益", 0.4395, swordsman_pct_total, tolerance=0.001)

# ==========================================
# 5. 边际对偶验证
# ==========================================
dual_ratio = swordsman_pct_total / berserker_indep_total
verify("边际对偶倍数", 4.7409, dual_ratio, tolerance=0.01)

# ==========================================
# 6. 剑魂基础面板验证
# ==========================================
verify("剑魂基础力量", 600, 400 + 120 + 80)
verify("剑魂破极物理攻击", 2600, 2000 * 1.30)

# ==========================================
# 输出结果
# ==========================================
print("=" * 60)
print(f"任务19 CC套加成数值 - Python独立验算报告")
print(f"稳态核查 v561 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)
for r in results:
    print(f"  {r['status']}  {r['item']}: 期望={r['expected']}, 实际={r['actual']}, 差异={r['diff']}")
print("=" * 60)
print(f"总计: {passed} 通过, {failed} 失败")
print(f"通过率: {passed}/{passed+failed} = {passed/(passed+failed)*100:.1f}%")
print("=" * 60)

# 保存JSON
output = {
    "version": "v561",
    "timestamp": datetime.now().isoformat(),
    "total": passed + failed,
    "passed": passed,
    "failed": failed,
    "pass_rate": round(passed/(passed+failed)*100, 1),
    "results": results
}
with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verifications/verification-cc-bonus-v561.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\nJSON已保存: verification-cc-bonus-v561.json")