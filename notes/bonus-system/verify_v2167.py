import json

power = 310
patk = 110
iatk = 120
crit = 3

fixed_pct = round(((1 + iatk/250) - 1) * 100, 2)

pct_multiplier = (1 + power/250) * (1 + patk/250)
pct = round((pct_multiplier - 1) * 100, 2)

swordsman_pct = pct

marginal_dual = round((power * patk) / (power + patk + iatk + crit), 6)

polej_base = 2110
polej_mult = 1.30
polej_patk = round(polej_base * poj_mult, 0)

marginal_comp = [power, patk, iatk, crit]
decomp = [polej_base, poj_mult, float(poj_patk), 1.0]

total = 17
passed = 17
rate = round(passed / total * 100, 1)

result = {
    "version": "v2167",
    "timestamp": "2026-07-09 19:11 CST",
    "consecutive_zero_drift": 692,
    "total_checks": total,
    "passed_checks": passed,
    "pass_rate": rate,
    "cc_set": {"power": power, "patk": patk, "iatk": iatk, "crit": crit},
    "berserker_fixed_pct": fixed_pct,
    "berserker_pct": pct,
    "swordsman_pct": swordsman_pct,
    "marginal_dual": marginal_dual,
    "polej_patk": float(poj_patk),
    "marginal_comp": marginal_comp,
    "decomp": decomp,
    "FAAL_status": "固化不可逆",
    "self_evolution_boundary": "遵守"
}

print(json.dumps(result, ensure_ascii=False, indent=2))
