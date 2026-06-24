#!/usr/bin/env python3
"""CC套（宫廷套装）各职业加成数值 — Python独立验算（稳态核查 v379）"""
import json, math
from datetime import datetime

results = []
def check(name, expected, actual, tolerance=0.01):
    ok = abs(expected - actual) <= tolerance
    results.append({"name": name, "expected": round(expected, 4), "actual": round(actual, 4), "pass": ok, "diff": round(abs(expected - actual), 4)})
    return ok

# ====== CC套6件套属性 ======
cc_power = 310
cc_phy_atk = 110
cc_independent = 120
cc_crit = 0.03

# ====== 狂战士面板 ======
bs_power_base = 728
bs_power_burst = bs_power_base * 1.40  # 1019.2
bs_independent = 1250
bs_phy_atk = 2000
bs_crit = 0.55

# ====== 剑魂面板 ======
sw_power = 600
sw_phy_atk_pre = 2000
sw_phy_atk_post = sw_phy_atk_pre * 1.30  # 2600
sw_crit = 0.50

print("=" * 60)
print("CC套（宫廷套装）各职业加成数值 — Python独立验算")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# ====== 一、6件套属性合计验证 ======
print("\n【一、6件套属性合计验证】")
check("力量合计", 310, 55+55+50+50+50+50)
check("物理攻击合计", 110, 20+20+18+18+18+16)
check("独立攻击合计", 120, 20+20+18+18+18+26)
check("暴击率合计", 0.03, 0.005*6)

# ====== 二、狂战士收益验证 ======
print("\n【二、狂战士收益验证】")

# 固伤：独立攻击收益
bs_indep_new = bs_independent + cc_independent  # 1370
bs_indep_gain = (1 + bs_indep_new / 250) / (1 + bs_independent / 250) - 1
check("狂战士-独立攻击收益", 0.08, bs_indep_gain)

# 固伤：暴击收益（期望伤害系数）
bs_crit_old_exp = (1 - bs_crit) + bs_crit * 1.5  # 1.275
bs_crit_new_exp = (1 - (bs_crit + cc_crit)) + (bs_crit + cc_crit) * 1.5  # 1.29
bs_crit_gain = bs_crit_new_exp / bs_crit_old_exp - 1
check("狂战士-暴击收益", 0.0118, bs_crit_gain)

# 固伤：综合收益
bs_fixed_total = (1 + bs_indep_gain) * (1 + bs_crit_gain) - 1
check("狂战士-固伤综合收益", 0.0927, bs_fixed_total)

# 百分比：力量收益（暴走后）
bs_power_gain = (1 + (bs_power_burst + cc_power) / 250) / (1 + bs_power_burst / 250) - 1
check("狂战士-百分比力量收益", 0.2442, bs_power_gain)

# 百分比：物理攻击收益
bs_phy_gain = (bs_phy_atk + cc_phy_atk) / bs_phy_atk - 1
check("狂战士-百分比物理攻击收益", 0.0550, bs_phy_gain)

# 百分比：综合收益
bs_percent_total = (1 + bs_power_gain) * (1 + bs_phy_gain) * (1 + bs_crit_gain) - 1
check("狂战士-百分比综合收益", 0.3281, bs_percent_total)

# ====== 三、剑魂收益验证 ======
print("\n【三、剑魂收益验证】")

# 百分比：力量收益
sw_power_gain = (1 + (sw_power + cc_power) / 250) / (1 + sw_power / 250) - 1
check("剑魂-力量收益", 0.3647, sw_power_gain)

# 百分比：物理攻击收益（破极后）
sw_phy_gain = (sw_phy_atk_post + cc_phy_atk) / sw_phy_atk_post - 1
check("剑魂-物理攻击收益", 0.0423, sw_phy_gain)

# 百分比：暴击收益
sw_crit_old_exp = (1 - sw_crit) + sw_crit * 1.5  # 1.25
sw_crit_new_exp = (1 - (sw_crit + cc_crit)) + (sw_crit + cc_crit) * 1.5  # 1.265
sw_crit_gain = sw_crit_new_exp / sw_crit_old_exp - 1
check("剑魂-暴击收益", 0.012, sw_crit_gain)

# 百分比：综合收益
sw_percent_total = (1 + sw_power_gain) * (1 + sw_phy_gain) * (1 + sw_crit_gain) - 1
check("剑魂-百分比综合收益", 0.4395, sw_percent_total)

# ====== 四、边际对偶验证 ======
print("\n【四、边际对偶验证】")
marginal_dual = sw_percent_total / bs_fixed_total
check("边际对偶倍数", 4.7409, marginal_dual)
print(f"  精确值: {marginal_dual:.6f}")

# ====== 五、暴击收益精确值 ======
print("\n【五、暴击收益精确值】")
check("狂战士暴击期望系数", 1.29, bs_crit_new_exp)
check("狂战士暴击期望系数(旧)", 1.275, bs_crit_old_exp)
check("剑魂暴击期望系数", 1.265, sw_crit_new_exp)
check("剑魂暴击期望系数(旧)", 1.25, sw_crit_old_exp)

# ====== 汇总 ======
print("\n" + "=" * 60)
passed = sum(1 for r in results if r["pass"])
total = len(results)
print(f"验算结果: {passed}/{total} 通过 ({'✅ 全部通过' if passed == total else '❌ 有失败项'})")
for r in results:
    status = "✅" if r["pass"] else "❌"
    print(f"  {status} {r['name']}: 期望={r['expected']}, 实际={r['actual']}, 差异={r['diff']}")

# 保存验算JSON
output = {
    "version": "v379",
    "timestamp": datetime.now().isoformat(),
    "total_checks": total,
    "passed": passed,
    "results": results,
    "summary": {
        "cc_set_6pc": {"power": cc_power, "phy_atk": cc_phy_atk, "independent": cc_independent, "crit": cc_crit},
        "berserker": {"fixed_total": round(bs_fixed_total, 4), "percent_total": round(bs_percent_total, 4)},
        "swordsman": {"percent_total": round(sw_percent_total, 4)},
        "marginal_dual": round(marginal_dual, 6)
    }
}
with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verifications/verification-cc-bonus-2026-06-25.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\n验算JSON已保存")
