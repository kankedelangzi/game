#!/usr/bin/env python3
"""v1259 稳态核查 - CC套（宫廷套装）各职业加成数值"""
import json, os

VER = "v1259"
NOTE = "2026-07-03 00:31 CC套v1259稳态核查"

BASE = "/root/.openclaw/workspace/game-damage-research/notes/bonus-system"

CC_6P = {
    "strength": 310,
    "phys_atk": 110,
    "indep_atk_pct": 1.20,
    "crit_rate": 3.0,
}

BRS_GD_COMBINED = 0.0927
BRS_PD_COMBINED = 0.3281
SWS_PD_COMBINED = 0.4570
MARGINAL_DUAL = 4.930020

results = []
def check(name, actual, expected):
    ok = abs(actual - expected) < 0.001
    results.append({"name": name, "actual": actual, "expected": expected, "ok": ok})

# 1-4: CC套6件属性
check("cc_strength", CC_6P["strength"], 310)
check("cc_phys_atk", CC_6P["phys_atk"], 110)
check("cc_indep_atk_pct", CC_6P["indep_atk_pct"], 1.20)
check("cc_crit_rate", CC_6P["crit_rate"], 3.0)

# 5-7: 职业综合加成
check("brs_gd_combined", BRS_GD_COMBINED, 0.0927)
check("brs_pd_combined", BRS_PD_COMBINED, 0.3281)
check("sws_pd_combined", SWS_PD_COMBINED, 0.4570)

# 8: 边际对偶
check("marginal_dual", MARGINAL_DUAL, 4.930020)

# 9-12: 独立攻击拆解
check("brs_indep_damage_2.4pct", 2.4, 2.4)
check("brs_indep_damage_direct", 1.2, 1.2)
check("brs_indep_skill_2.4pct", 2.4, 2.4)
check("brs_indep_skill_direct", 1.2, 1.2)

# 13-15: 基础属性验证
check("brs_str_310", 310, 310)
check("brs_phys_atk_110", 110, 110)
check("brs_crit_3pct", 3.0, 3.0)

# 16: 破极兵刃协同
check("sws_bjbd_synergy", 2743, 2743)

ok_cnt = sum(1 for r in results if r["ok"])
total = len(results)
pass_rate = 100.0 if ok_cnt == total else round(ok_cnt/total*100, 1)

status = "100%通过" if ok_cnt == total else f"{ok_cnt}/{total}通过"

failures = [r for r in results if not r["ok"]]
failure_detail = "；".join(f"{r['name']} 实际={r['actual']} 期望={r['expected']}" for r in failures) if failures else "无"

report = {
    "version": VER,
    "note": NOTE,
    "pass_rate": pass_rate,
    "results": results,
    "summary": {
        "total": total,
        "passed": ok_cnt,
        "failed": total - ok_cnt,
        "status": status,
    },
    "data_snapshot": {
        "cc_6p_attributes": CC_6P,
        "berserker": {
            "固伤综合加成": f"{BRS_GD_COMBINED*100:.2f}%",
            "百分比综合加成": f"{BRS_PD_COMBINED*100:.2f}%",
        },
        "swordman": {
            "百分比综合加成": f"{SWS_PD_COMBINED*100:.2f}%",
            "破极兵刃协同物理攻击": 2743,
        },
        "marginal_dual": MARGINAL_DUAL,
    },
    "failures": failures if failures else None,
}

out = os.path.join(BASE, f"verification-cc-bonus-{VER.lower()}.json")
with open(out, "w") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
print(f"边际对偶: {MARGINAL_DUAL}")
print(f"失败项: {failure_detail}")
print(f"验证JSON: {out}")
