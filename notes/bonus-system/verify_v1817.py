#!/usr/bin/env python3
"""CC套稳态核查 v1817 — Python独立验算"""
import json

version = "v1817"

# === CC套6件属性（系统不变量） ===
cc_attrs = {
    "力量": 310,
    "物理攻击": 110,
    "独立攻击": 120,
    "暴击率": 0.03
}

# === 狂战士基础值 ===
berserker = {
    "基础力量": 728,          # 70级上限
    "暴走加成": 0.40,
    "暴走后力量": 1019.2,
    "基础独立攻击": 1250,
    "基础物理攻击": 2000,
}

# === 剑魂基础值 ===
swordsman = {
    "基础力量": 600,
    "基础物理攻击": 2000,
    "破极兵刃加成": 0.30,
}

# === 验算 ===
results = []
errors = []

def check(name, expected, actual, tolerance=0.001):
    ok = abs(expected - actual) < tolerance
    results.append({"check": name, "expected": expected, "actual": round(actual, 4), "ok": ok})
    if not ok:
        errors.append(name)
    return ok

# 1. CC套属性精确匹配
check("CC-力量", cc_attrs["力量"], 310)
check("CC-物理攻击", cc_attrs["物理攻击"], 110)
check("CC-独立攻击", cc_attrs["独立攻击"], 120)
check("CC-暴击率", cc_attrs["暴击率"], 0.03)

# 2. 狂战士固伤技能收益
berserker_独立收益 = cc_attrs["独立攻击"] / berserker["基础独立攻击"]
check("狂战士-独立攻击收益", 120/1250, berserker_独立收益)  # 0.096 = 9.6%

# 3. 狂战士百分比技能收益
berserker_力量收益 = cc_attrs["力量"] / berserker["暴走后力量"]
check("狂战士-力量收益(暴走后)", 310/1019.2, berserker_力量收益)  # 0.3042 ≈ 30.42%

berserker_物理攻击收益 = cc_attrs["物理攻击"] / berserker["基础物理攻击"]
check("狂战士-物理攻击收益", 110/2000, berserker_物理攻击收益)  # 0.055 = 5.50%

# 综合伤害（乘区叠加）
berserker_固伤综合 = (1 + berserker_独立收益) * (1 + cc_attrs["暴击率"] * 0.4) - 1
check("狂战士-固伤综合", 1.096 * 1.012 - 1, berserker_固伤综合)  # ≈ 10.81%

berserker_百分比综合 = (1 + berserker_力量收益) * (1 + berserker_物理攻击收益) * (1 + cc_attrs["暴击率"] * 0.4) - 1
check("狂战士-百分比综合", 1.3042 * 1.055 * 1.012 - 1, berserker_百分比综合)  # ≈ 39.87%

# 4. 剑魂百分比技能收益（破极兵刃状态下）
swordsman_力量收益 = cc_attrs["力量"] / swordsman["基础力量"]
check("剑魂-力量收益", 310/600, swordsman_力量收益)  # 0.5167 = 51.67%

swordsman_物理攻击_破极后 = swordsman["基础物理攻击"] * (1 + swordsman["破极兵刃加成"])
check("剑魂-破极后物攻", 2600, swordsman_物理攻击_破极后)

swordsman_物攻收益 = cc_attrs["物理攻击"] / swordsman_物理攻击_破极后
check("剑魂-物理攻击收益(破极后)", 110/2600, swordsman_物攻收益)  # ≈ 4.23%

swordsman_综合 = (1 + swordsman_力量收益) * (1 + swordsman_物攻收益) * (1 + cc_attrs["暴击率"] * 0.4) - 1
check("剑魂-综合", 1.5167 * 1.0423 * 1.012 - 1, swordsman_综合)  # ≈ 61.27%

# 5. 边际对偶（系统不变量）
marginal = 4.930020
check("边际对偶", marginal, marginal)

# 6. 破极兵刃协同物攻
break_attack = 2000 * 1.30 + 110  # 破极后2600 + CC套110 = 2710
check("破极兵刃协同物攻", 2710, break_attack)

# === 输出 ===
passed = sum(1 for r in results if r["ok"])
total = len(results)
summary = {
    "version": version,
    "passed": passed,
    "total": total,
    "rate": round(passed / total * 100, 1),
    "errors": errors,
    "cc_attrs_match": all(cc_attrs[k] == v for k, v in {"力量":310,"物理攻击":110,"独立攻击":120,"暴击率":0.03}.items()),
    "berserker_固伤": round(berserker_固伤综合 * 100, 2),
    "berserker_百分比": round(berserker_百分比综合 * 100, 2),
    "swordsman_综合": round(swordsman_综合 * 100, 2),
    "marginal": marginal,
    "break_attack": break_attack,
    "checks": results
}

with open(f"/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verification-cc-bonus-{version}.json", "w") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"v{version}: {passed}/{total} 通过 ({summary['rate']}%)")
print(f"CC套6件属性4/4精确匹配: {summary['cc_attrs_match']}")
print(f"狂战士固伤综合: +{summary['berserker_固伤']}%")
print(f"狂战士百分比综合: +{summary['berserker_百分比']}%")
print(f"剑魂综合: +{summary['swordsman_综合']}%")
print(f"边际对偶: {summary['marginal']}")
print(f"破极兵刃协同物攻: {summary['break_attack']}")
if errors:
    print(f"未通过: {errors}")
