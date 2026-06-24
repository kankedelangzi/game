#!/usr/bin/env python3
"""
任务19 CC套（宫廷套装）稳态核查 - Python独立验算
版本：v380 | 日期：2026-06-25
"""

import json
from datetime import datetime

# ==================== CC套基础属性 ====================
cc_single = {
    "上衣": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击": 0.5},
    "下装": {"力量": 55, "物理攻击": 20, "独立攻击": 20, "暴击": 0.5},
    "头饰": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击": 0.5},
    "帽子": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击": 0.5},
    "脸部": {"力量": 50, "物理攻击": 18, "独立攻击": 18, "暴击": 0.5},
    "胸部": {"力量": 50, "物理攻击": 16, "独立攻击": 26, "暴击": 0.5},
}

cc_6piece_total = {
    "力量": sum(v["力量"] for v in cc_single.values()),
    "物理攻击": sum(v["物理攻击"] for v in cc_single.values()),
    "独立攻击": sum(v["独立攻击"] for v in cc_single.values()),
    "暴击": sum(v["暴击"] for v in cc_single.values()),
}

# ==================== 狂战士面板（毕业级） ====================
berserker = {
    "力量": 728,
    "暴走力量": 728 * 1.40,  # 暴走+40%
    "独立攻击": 1250,
    "物理攻击": 2000,
    "暴击率": 0.55,
}

# ==================== 剑魂面板（毕业级，破极后） ====================
swordsman = {
    "力量": 600,
    "物理攻击_基础": 2000,
    "物理攻击_破极": 2000 * 1.30,  # 破极兵刃+30%
    "暴击率": 0.50,
}

# ==================== 验算结果 ====================
results = []
passed = 0
failed = 0

def verify(name, expected, actual, tolerance=0.0001):
    global passed, failed
    diff = abs(expected - actual)
    status = "✅ PASS" if diff < tolerance else "❌ FAIL"
    if diff < tolerance:
        passed += 1
    else:
        failed += 1
    results.append({
        "name": name,
        "expected": round(expected, 6),
        "actual": round(actual, 6),
        "diff": round(diff, 6),
        "status": status
    })
    return status

# --- CC套6件属性验算 ---
verify("CC套6件-力量", 310, cc_6piece_total["力量"])
verify("CC套6件-物理攻击", 110, cc_6piece_total["物理攻击"])
verify("CC套6件-独立攻击", 120, cc_6piece_total["独立攻击"])
verify("CC套6件-暴击", 3.0, cc_6piece_total["暴击"])

# --- 狂战士固伤收益验算 ---
# 独立攻击收益：(1 + (1250+120)/250) / (1 + 1250/250) - 1
berserker_indep = (1 + (berserker["独立攻击"] + 120) / 250) / (1 + berserker["独立攻击"] / 250) - 1
verify("狂战士-独立攻击收益", 0.08, berserker_indep, 0.0001)

# 暴击收益：期望伤害系数
crit_old = (1 - berserker["暴击率"]) + berserker["暴击率"] * 1.5
crit_new = (1 - (berserker["暴击率"] + 0.03)) + (berserker["暴击率"] + 0.03) * 1.5
berserker_crit = crit_new / crit_old - 1
verify("狂战士-暴击收益", 0.0118, berserker_crit, 0.0001)

# 固伤综合收益
berserker_fixed_total = (1 + berserker_indep) * (1 + berserker_crit) - 1
verify("狂战士-固伤综合收益", 0.0927, berserker_fixed_total, 0.0001)

# --- 狂战士百分比收益验算 ---
# 力量收益（暴走后）
berserker_str = (1 + (berserker["暴走力量"] + 310) / 250) / (1 + berserker["暴走力量"] / 250) - 1
verify("狂战士-力量收益(暴走后)", 0.2442, berserker_str, 0.0001)

# 物理攻击收益（直接乘数）
berserker_phy = (berserker["物理攻击"] + 110) / berserker["物理攻击"] - 1
verify("狂战士-物理攻击收益", 0.055, berserker_phy, 0.0001)

# 百分比综合
berserker_pct_total = (1 + berserker_str) * (1 + berserker_phy) * (1 + berserker_crit) - 1
verify("狂战士-百分比综合收益", 0.3281, berserker_pct_total, 0.0001)

# --- 剑魂百分比收益验算 ---
# 力量收益
swordsman_str = (1 + (swordsman["力量"] + 310) / 250) / (1 + swordsman["力量"] / 250) - 1
verify("剑魂-力量收益", 0.3647, swordsman_str, 0.0001)

# 物理攻击收益（破极后）
swordsman_phy = (swordsman["物理攻击_破极"] + 110) / swordsman["物理攻击_破极"] - 1
verify("剑魂-物理攻击收益(破极后)", 0.0423, swordsman_phy, 0.0001)

# 暴击收益
crit_old_s = (1 - swordsman["暴击率"]) + swordsman["暴击率"] * 1.5
crit_new_s = (1 - (swordsman["暴击率"] + 0.03)) + (swordsman["暴击率"] + 0.03) * 1.5
swordsman_crit = crit_new_s / crit_old_s - 1
verify("剑魂-暴击收益", 0.012, swordsman_crit, 0.0001)

# 百分比综合
swordsman_pct_total = (1 + swordsman_str) * (1 + swordsman_phy) * (1 + swordsman_crit) - 1
verify("剑魂-百分比综合收益", 0.4395, swordsman_pct_total, 0.0001)

# --- 边际对偶倍数验算 ---
marginal_dual = swordsman_pct_total / berserker_fixed_total
verify("边际对偶倍数", 4.7409, marginal_dual, 0.0001)

# ==================== 输出结果 ====================
print("=" * 60)
print("任务19 CC套（宫廷套装）稳态核查 - Python独立验算")
print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

for r in results:
    print(f"{r['status']} | {r['name']}: 期望={r['expected']}, 实际={r['actual']}, 差异={r['diff']}")

print("=" * 60)
print(f"总计：{passed} 通过，{failed} 失败")
print(f"通过率：{passed}/{passed+failed} = {passed/(passed+failed)*100:.1f}%")
print("=" * 60)

# 保存验算JSON
output = {
    "task": "任务19 - CC套（宫廷套装）各职业加成数值",
    "version": "v380",
    "timestamp": datetime.now().isoformat(),
    "cc_6piece": cc_6piece_total,
    "berserker": {
        "base_stats": berserker,
        "indep_bonus": round(berserker_indep, 6),
        "crit_bonus": round(berserker_crit, 6),
        "fixed_total": round(berserker_fixed_total, 6),
        "str_bonus": round(berserker_str, 6),
        "phy_bonus": round(berserker_phy, 6),
        "pct_total": round(berserker_pct_total, 6),
    },
    "swordsman": {
        "base_stats": swordsman,
        "str_bonus": round(swordsman_str, 6),
        "phy_bonus": round(swordsman_phy, 6),
        "crit_bonus": round(swordsman_crit, 6),
        "pct_total": round(swordsman_pct_total, 6),
    },
    "marginal_dual": round(marginal_dual, 6),
    "results": results,
    "summary": {
        "passed": passed,
        "failed": failed,
        "total": passed + failed,
        "pass_rate": round(passed / (passed + failed) * 100, 1),
    }
}

with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verifications/verification-cc-bonus-2026-06-25.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n验算JSON已保存至：notes/bonus-system/verifications/verification-cc-bonus-2026-06-25.json")
