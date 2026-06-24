#!/usr/bin/env python3
"""CC套（宫廷套装）各职业加成数值 — Python独立验算脚本"""
import json, datetime

results = []
def check(name, expected, actual, tol=0.01):
    ok = abs(expected - actual) <= tol
    results.append({"item": name, "expected": round(expected, 4), "actual": round(actual, 4), "pass": ok, "diff_pp": round((actual - expected) * 100, 2)})
    return ok

# ===== CC套6件套基础属性 =====
cc_strength = 310
cc_phy_atk = 110
cc_independent = 120
cc_crit = 0.03

# ===== 狂战士面板（暴走后） =====
b_strength_base = 728
b_strength_burst = 728 * 1.40  # 1019.2
b_independent = 1250
b_phy_atk = 2000
b_crit = 0.55

# ===== 剑魂面板（破极后） =====
s_strength = 600
s_phy_atk_base = 2000
s_phy_atk_break = 2000 * 1.30  # 2600
s_crit = 0.50

passed = 0
total = 0

# --- 1. CC套基础属性验证 ---
total += 1; check("CC套6件力量", 310, cc_strength); passed += 1 if results[-1]["pass"] else 0
total += 1; check("CC套6件物理攻击", 110, cc_phy_atk); passed += 1 if results[-1]["pass"] else 0
total += 1; check("CC套6件独立攻击", 120, cc_independent); passed += 1 if results[-1]["pass"] else 0
total += 1; check("CC套6件暴击率", 3.0, cc_crit * 100); passed += 1 if results[-1]["pass"] else 0

# --- 2. 狂战士固伤收益 ---
# 独立攻击收益 = (1 + (1250+120)/250) / (1 + 1250/250) - 1
b_indep_gain = (1 + (b_independent + cc_independent) / 250) / (1 + b_independent / 250) - 1
total += 1; check("狂战士独立攻击收益", 0.08, b_indep_gain); passed += 1 if results[-1]["pass"] else 0

# 暴击收益 = (1 - (0.55+0.03) + (0.55+0.03)*1.5) / (1 - 0.55 + 0.55*1.5) - 1
b_crit_old = (1 - b_crit) + b_crit * 1.5
b_crit_new = (1 - (b_crit + cc_crit)) + (b_crit + cc_crit) * 1.5
b_crit_gain = b_crit_new / b_crit_old - 1
total += 1; check("狂战士暴击收益", 0.0118, b_crit_gain); passed += 1 if results[-1]["pass"] else 0

# 固伤综合 = (1+8.0%)*(1+1.18%)-1
b_fix_total = (1 + b_indep_gain) * (1 + b_crit_gain) - 1
total += 1; check("狂战士固伤综合收益", 0.0927, b_fix_total); passed += 1 if results[-1]["pass"] else 0

# --- 3. 狂战士百分比收益 ---
# 力量收益（暴走后基准）
b_str_gain = (1 + (b_strength_burst + cc_strength) / 250) / (1 + b_strength_burst / 250) - 1
total += 1; check("狂战士百分比力量收益", 0.2442, b_str_gain); passed += 1 if results[-1]["pass"] else 0

# 物理攻击收益（直接乘数）
b_phy_gain = (b_phy_atk + cc_phy_atk) / b_phy_atk - 1
total += 1; check("狂战士百分比物理攻击收益", 0.055, b_phy_gain); passed += 1 if results[-1]["pass"] else 0

# 百分比综合
b_pct_total = (1 + b_str_gain) * (1 + b_phy_gain) * (1 + b_crit_gain) - 1
total += 1; check("狂战士百分比综合收益", 0.3281, b_pct_total); passed += 1 if results[-1]["pass"] else 0

# --- 4. 剑魂百分比收益 ---
# 力量收益
s_str_gain = (1 + (s_strength + cc_strength) / 250) / (1 + s_strength / 250) - 1
total += 1; check("剑魂力量收益", 0.3647, s_str_gain); passed += 1 if results[-1]["pass"] else 0

# 物理攻击收益（破极后基准）
s_phy_gain = (s_phy_atk_break + cc_phy_atk) / s_phy_atk_break - 1
total += 1; check("剑魂物理攻击收益", 0.0423, s_phy_gain); passed += 1 if results[-1]["pass"] else 0

# 暴击收益
s_crit_old = (1 - s_crit) + s_crit * 1.5
s_crit_new = (1 - (s_crit + cc_crit)) + (s_crit + cc_crit) * 1.5
s_crit_gain = s_crit_new / s_crit_old - 1
total += 1; check("剑魂暴击收益", 0.012, s_crit_gain); passed += 1 if results[-1]["pass"] else 0

# 百分比综合
s_pct_total = (1 + s_str_gain) * (1 + s_phy_gain) * (1 + s_crit_gain) - 1
total += 1; check("剑魂百分比综合收益", 0.4395, s_pct_total); passed += 1 if results[-1]["pass"] else 0

# --- 5. 边际对偶倍数 ---
ratio = s_pct_total / b_fix_total
total += 1; check("边际对偶倍数", 4.74, ratio, tol=0.05); passed += 1 if results[-1]["pass"] else 0

# --- 6. 单件属性验证 ---
parts = {"上衣": (55, 20, 20, 0.005), "下装": (55, 20, 20, 0.005),
         "头饰": (50, 18, 18, 0.005), "帽子": (50, 18, 18, 0.005),
         "脸部": (50, 18, 18, 0.005), "胸部": (50, 16, 26, 0.005)}
total += 1; check("6件力量合计", 310, sum(p[0] for p in parts.values())); passed += 1 if results[-1]["pass"] else 0
total += 1; check("6件物理攻击合计", 110, sum(p[1] for p in parts.values())); passed += 1 if results[-1]["pass"] else 0
total += 1; check("6件独立攻击合计", 120, sum(p[2] for p in parts.values())); passed += 1 if results[-1]["pass"] else 0
total += 1; check("6件暴击率合计", 3.0, sum(p[3] for p in parts.values()) * 100); passed += 1 if results[-1]["pass"] else 0

# ===== 输出结果 =====
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"=== CC套加成数值 Python独立验算 ===")
print(f"时间: {timestamp}")
print(f"通过: {passed}/{total}")
print(f"通过率: {passed/total*100:.1f}%")
print()

all_pass = True
for r in results:
    status = "✅" if r["pass"] else "❌"
    print(f"  {status} {r['item']}: 期望={r['expected']:.4f}, 实际={r['actual']:.4f}, 差异={r['diff_pp']:.2f}pp")
    if not r["pass"]:
        all_pass = False

print()
print(f"{'='*40}")
print(f"结论: {'全部通过 ✅' if all_pass else '存在失败 ❌'}")
print(f"边际对偶倍数: {ratio:.2f}倍")
print(f"{'='*40}")

# 保存JSON
output = {
    "timestamp": timestamp,
    "total": total,
    "passed": passed,
    "rate": round(passed/total*100, 1),
    "all_pass": all_pass,
    "results": results,
    "summary": {
        "cc_6piece": {"strength": 310, "phy_atk": 110, "independent": 120, "crit": 3.0},
        "berserker_fix_total": round(b_fix_total * 100, 2),
        "berserker_pct_total": round(b_pct_total * 100, 2),
        "swordsman_pct_total": round(s_pct_total * 100, 2),
        "duality_ratio": round(ratio, 2)
    }
}
with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verifications/verification-cc-bonus-2026-06-24.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\n验算JSON已保存")
