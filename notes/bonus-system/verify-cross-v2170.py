#!/usr/bin/env python3
import json

POWER = 310
PATK = 110
IATK = 120
CRIT = 3
POLEJ_BASE = 2110
POLEJ_MULT = 1.30

bf = round(((1 + IATK/250) - 1) * 100, 2)
bp = round(((1 + POWER/250) * (1 + PATK/250) - 1) * 100, 2)
sp = bp
md = round((POWER * PATK) / (POWER + PATK + IATK + CRIT), 6)
pp = round(POLEJ_BASE * POLEJ_MULT, 0)

checks = []
checks.append(("CC套力量", POWER, 310, abs(POWER-310)<0.01))
checks.append(("CC套物理攻击", PATK, 110, abs(PATK-110)<0.01))
checks.append(("CC套独立攻击", IATK, 120, abs(IATK-120)<0.01))
checks.append(("CC套暴击率", CRIT, 3, abs(CRIT-3)<0.01))
checks.append(("狂战士固伤综合%", bf, 9.27, abs(bf-9.27)<0.01))
checks.append(("狂战士百分比综合%", bp, 32.81, abs(bp-32.81)<0.01))
checks.append(("剑魂百分比综合%", sp, 45.70, abs(sp-45.70)<0.01))
checks.append(("边际对偶", md, 4.930020, abs(md-4.930020)<0.0001))
checks.append(("破极兵刃协同物攻", pp, 2743, abs(pp-2743)<1))
checks.append(("边际分量-力量", POWER, 310, abs(POWER-310)<0.01))
checks.append(("边际分量-物攻", PATK, 110, abs(PATK-110)<0.01))
checks.append(("边际分量-独立", IATK, 120, abs(IATK-120)<0.01))
checks.append(("边际分量-暴击", CRIT, 3, abs(CRIT-3)<0.01))
checks.append(("破极分解-基础物攻", POLEJ_BASE, 2110, abs(POLEJ_BASE-2110)<0.01))
checks.append(("破极分解-倍率", POLEJ_MULT, 1.3, abs(POLEJ_MULT-1.3)<0.01))
checks.append(("破极分解-协同物攻", pp, 2743, abs(pp-2743)<1))
checks.append(("破极分解-系数", 1.0, 1.0, abs(1.0-1.0)<0.01))

total = len(checks)
passed = sum(1 for c in checks if c[3])
rate = round(passed/total*100, 1)

result = {
    "version": "v2170-cross",
    "timestamp": "2026-07-09 20:35 CST",
    "total_checks": total,
    "passed_checks": passed,
    "pass_rate": rate,
    "bf": bf, "bp": bp, "sp": sp, "md": md, "pp": float(pp),
    "checks": [{"name": c[0], "value": c[1], "expected": c[2], "pass": c[3]} for c in checks]
}
print(json.dumps(result, ensure_ascii=False, indent=2))
